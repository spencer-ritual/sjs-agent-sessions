# Delegated Secrets: ECIES Ephemeral Key Flow

## Short Answer

In the traffic-gen flows, traffic-gen is the client-side producer that generates the ECIES ephemeral key. More precisely, traffic-gen calls `ExecutorRequest.encrypt_secrets(...)`, and the ECIES library invoked by that helper generates a fresh ephemeral secp256k1 keypair for that one encrypted secret blob.

The EOA private key is not the ephemeral key. The EOA private key signs the delegated-secret authorization preimage. The ECIES ephemeral private key is generated internally during encryption, used to derive the AES-GCM key, and then discarded. The matching ephemeral public key is embedded at the front of the `encrypted_secrets[i]` byte blob.

## Producer-Side Flow

1. An EOA or agent has:
   - a wallet private key for signing delegated-secret authorization;
   - a secret payload, such as API keys;
   - the selected executor address and executor public key.

2. traffic-gen builds the request and calls the shared Python helper:
   - `ExecutorRequest.encrypt_secrets(secrets, executor_public_key, secret_owner)` in the delegated-secrets PR shape;
   - older local checkouts may show the same call without `secret_owner`, but the PR adds the owner-bound envelope.

3. The helper wraps the plaintext secrets in an owner-bound JSON envelope before encryption:

   ```json
   {
     "version": 1,
     "secret_owner": "0x...",
     "secrets": {
       "API_KEY": "..."
     }
   }
   ```

4. The helper calls the ECIES encryption library. At that point traffic-gen, through the library, generates a fresh ephemeral keypair:

   ```text
   ephemeral_private_key, ephemeral_public_key = fresh secp256k1 keypair
   ```

5. The AES-GCM key is derived from ECDH between that fresh ephemeral private key and the executor public key:

   ```text
   shared_point = ECDH(ephemeral_private_key, executor_public_key)
   aes_key = HKDF-SHA256(ephemeral_public_key || shared_point)
   ```

6. The envelope JSON is encrypted with AES-256-GCM. The output blob is:

   ```text
   encrypted_secrets[i] =
     ephemeral_public_key[65 bytes: 0x04 || X || Y]
     || nonce[12 bytes]
     || tag[16 bytes]
     || ciphertext[variable]
   ```

7. Separately, the EOA private key signs the delegated-secret authorization preimage:

   ```text
   domain
   || chain_id
   || executor_address
   || secret_owner
   || keccak256(encrypted_secrets[i])
   ```

8. traffic-gen submits a request containing parallel arrays:

   ```text
   secret_owners[i]     = owner address
   encrypted_secrets[i] = ECIES blob containing the ephemeral public key inline
   secret_signature[i]  = EOA signature over the authorization preimage
   ```

## Chain / Precompile Flow

The ephemeral public key does not have its own ABI field. It flows through the system as the first 65 bytes of each `encrypted_secrets[i]` byte blob.

At submission time, the request is ABI-encoded and sent through the normal precompile path, such as `PrecompileConsumer` into the executor precompile request. The chain stores or emits the request data as part of the job/input flow. From the protocol's point of view, `encrypted_secrets[i]` is opaque bytes.

Important consequence: calldata observers can see the ephemeral public key because it is part of the public encrypted blob. In the Python-compatible uncompressed format, `encrypted_secrets[i][0:65]` is the full ephemeral public key (`0x04 || X || Y`); Observers still cannot derive the AES key without the executor private key or the ephemeral private key.

## Executor-Side Flow

1. executor-go receives a job and decodes the ABI request.

2. The decoded request has:

   ```text
   request.SecretOwners
   request.EncryptedSecrets
   request.SecretSignature
   request.Executor
   ```

3. The delegated-secrets validator reconstructs the authorization preimage from:

   ```text
   chain_id
   executor_address
   secret_owner
   keccak256(encrypted_secrets[i])
   ```

4. It recovers the signer from `secret_signature[i]` over that preimage and requires:

   ```text
   recovered_signer == secret_owners[i]
   ```

5. If `secret_owners[i]` is the actual caller/delegate, this is treated as direct owner use. Otherwise the executor checks on-chain delegation:

   ```text
   SecretsAccessControl.checkAccess(
     owner = secret_owners[i],
     delegate = caller,
     secretsHash = keccak256(encrypted_secrets[i])
   )
   ```

6. During decrypt, executor-go extracts the ephemeral public key from the front of `encrypted_secrets[i]`:

   ```text
   ephemeral_public_key = encrypted_secrets[i][0:65]
   nonce                = encrypted_secrets[i][65:77]
   tag                  = encrypted_secrets[i][77:93]
   ciphertext           = encrypted_secrets[i][93:]
   ```

7. The executor derives the same AES-GCM key using its private key:

   ```text
   shared_point = ECDH(executor_private_key, ephemeral_public_key)
   aes_key = HKDF-SHA256(ephemeral_public_key || shared_point)
   ```

8. AES-GCM verifies the tag and decrypts the ciphertext. Any byte substitution inside the encrypted JSON, including changing `secret_owner`, should fail tag verification unless the attacker can compute a valid tag.

9. After decryption, executor-go parses the owner-bound envelope and checks:

   ```text
   envelope.secret_owner == expectedOwner
   expectedOwner == secret_owners[i]
   ```

This is what blocks the old re-sign bypass. If an attacker copies a victim ciphertext, sets `secret_owners[i] = attacker`, and signs as attacker, the signature may match the explicit owner but the decrypted envelope still says `secret_owner = victim`, so the executor rejects.

## What Is And Is Not Bound

The ECIES AES key is bound to:

- the generated ephemeral private key;
- the executor public key;
- the inline ephemeral public key used in HKDF;
- the random AES-GCM nonce and authentication tag.

The ECIES AES key is not bound to:

- the EOA private key;
- the secret owner address;
- the request sender/delegate.

The secret owner binding is enforced by the combination of:

- owner address embedded inside the encrypted envelope;
- signature over the structured authorization preimage;
- executor-side signer recovery and owner comparison;
- executor-side decrypted-envelope owner check.

This is a post-decrypt owner-envelope binding. It is sufficient to address the re-sign bypass when every handler wires `secret_owners`, `chain_id`, `executor_address`, and the real caller/delegate correctly. It is weaker than a sender-authenticated ECIES design where the owner key participates in ECDH and wrong-owner ciphertexts fail before plaintext is materialized.

## Files To Inspect

- `traffic-gen-internal/src/action/*`: producer call sites that fetch executor info, call `ExecutorRequest.encrypt_secrets(...)`, and build the request.
- `ritual-common-internal/src/ritual_common/executor/base.py`: Python request helper, owner-bound envelope, authorization preimage, and signature creation.
- `ritual-go-common/ecies/ecies.go`: ECIES key generation, wire format, AES-GCM encryption, and decryption.
- `executor-go-internal/internal/delegatedsecrets/fetch.go`: executor-side authorization preimage reconstruction and signature/delegation validation.
- `executor-go-internal/internal/utils/ecies.go`: executor-side envelope parsing and `expectedOwner` check in the PR.
