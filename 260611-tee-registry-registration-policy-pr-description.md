# TEE Registry Registration Policy PR Stack

These PRs make TEE service registration consistent across the contracts, shared Go bindings, individual services, local-network config, and deployment config. The main effect is that every service now registers the same core metadata with the same policy checks: the TEE identity, payment address, endpoint policy, mTLS SPKI hash, attestation-bound extended data, and service capability are all handled deliberately instead of drifting by service.

That consistency matters because the cleanup caught three correctness issues that were easy to miss while each registration path owned its own slightly different version of the flow.

## PRs

- `ritual-sc-internal`: https://github.com/ritual-net/ritual-sc-internal/pull/239
- `ritual-go-common`: https://github.com/ritual-net/ritual-go-common/pull/62
- `executor-go-internal`: https://github.com/ritual-net/executor-go-internal/pull/183
- `dkms`: https://github.com/ritual-net/dkms/pull/36
- `ritual-vllm-proxy-go`: https://github.com/ritual-net/ritual-vllm-proxy-go/pull/46
- `ritual-streaming-service`: https://github.com/ritual-net/ritual-streaming-service/pull/24
- `ritual-agent-telemetry`: https://github.com/ritual-net/ritual-agent-telemetry/pull/10
- `ritual-node-internal`: https://github.com/ritual-net/ritual-node-internal/pull/379
- `chain-deployment-infra`: https://github.com/ritual-net/chain-deployment-infra/pull/399

## Correctness Issues Fixed

### 1. DKMS registration bypassed whitelist gating

`registerTdxDkmsWithPermit` did not check `whitelistRegistry`, while executor, streaming, vLLM proxy, and telemetry registration paths did.

If the whitelist is configured as a physical/provider deployment approval layer, that meant an attested DKMS workload could become discoverable without being approved through the same deployment gate as the other services. Attestation proves the workload identity and code path; it does not, by itself, prove that the TEE is running in an approved physical or provider environment.

The contract PR moves whitelist enforcement into shared registration preflight and adds DKMS whitelist coverage, so DKMS now follows the same configured whitelist policy as the other TDX service registration paths.

### 2. Some services could register without payment addresses

The registration paths disagreed on whether `paymentAddress` was required. Executor, streaming, and telemetry already rejected `address(0)`, while vLLM proxy and DKMS could be registered with a zero payment address.

That matters because operators contributing to the network could accidentally register in a way where they cannot be compensated.

The PR stack makes nonzero payment addresses required across all five TDX service families. The downstream service and config PRs then make that policy real outside the contract:

- `dkms` now requires `DKMS_PAYMENT_ADDRESS` when registration is enabled.
- `ritual-vllm-proxy-go` now requires `PAYMENT_ADDRESS` when registration is enabled.
- `ritual-node-internal` local-network generation funds and injects nonzero DKMS and vLLM proxy payment addresses.
- `chain-deployment-infra` wires payment addresses into the Phala vLLM proxy and DKMS deployment paths and records DKMS payment addresses in deployment artifacts.

### 3. Public-key registration metadata had inconsistent semantics

The old registration API exposed a generic `publicKey` field across service registrations, but the value did not mean the same thing everywhere. For non-executor services, the value being passed was effectively the TEE identity public key. For executor, the value was not the TEE identity public key; it was the executor's secrets/auth public key.

That created confusing and incorrect wiring: the same field name encouraged callers and reviewers to treat these keys as semantically equivalent, even though they represented different key material with different purposes and different blast-radius implications.

Key definitions:

- TEE identity key: the secp256k1 key generated/held by the TEE service. Its address is `teeAddress`. The service uses this key to sign registration permits/transactions, and the registry requires `msg.sender == teeAddress`. For DKMS, vLLM proxy, and telemetry, this was the key previously passed as registry `publicKey`.
- mTLS certificate key: a separate key generated inside the self-signed X.509 certificate managed by `mtls.Manager`. The certificate embeds `teeAddress` in its Common Name, and the service registers `mTlsSpkiHash = SHA256(cert.RawSubjectPublicKeyInfo)`. Other services look up this hash in `TEEServiceRegistry`, then compare it to the certificate presented during the TLS handshake. This key is not the registry `publicKey`.
- Executor secrets/auth key: a separate executor-only secp256k1 key. Executor registers this key as `executorSecretsAuthPublicKey` instead of the TEE identity public key. This makes executor unique among the confirmed services, and the key is currently overloaded across several purposes:
  - Job secret encryption/decryption key: the public half is passed to `TEEServiceRegistry.registerTdxExecutorWithPermit` and included in executor `extendedData` so users and clients can encrypt job secrets to this executor. The private half decrypts `encrypted_secrets` for multiple executor handlers, including LLM/HTTP calls, long-running HTTP, DKMS-key private inputs, and persistent-agent requests.
  - Job result signing/submission key: executor uses this private key for both normal job result attestation and asynchronous Phase 2 delivery. In the normal path, executor constructs a `SignatureAttestation` from the key and signs job computation results before submitting them back on-chain. In the Phase 2 path, delivery services pass the same private key bytes into submitters for long-running HTTP, persistent-agent spawn delivery, ZK proof delivery, FHE delivery, and related asynchronous callbacks.
  - Internal key-derivation auth root: executor runs an internal key-derivation HTTP server for co-located agent containers. Containers call this server to request derived DKMS keys after the executor has validated the relevant agent/job state. The server derives an HMAC key from the executor secrets/auth private key with HKDF, then uses that HMAC key for deterministic bearer tokens.

Separating the executor secrets/auth key from the TEE identity key is defensible. The TEE identity key is the registry identity: it controls `teeAddress`, signs registration permits/transactions, and is the address other contracts use to identify the registered TEE. Reusing that same key for arbitrary job-secret decryption or app-level result signing would expand the blast radius of the registry identity key and mix on-chain identity with executor application crypto.

Reusing the executor secrets/auth key across all executor application purposes is less clearly justified. The code does domain-separate the internal key-derivation server's HMAC key with HKDF, explicitly to avoid direct reuse between ECIES decryption and token signing. But the same underlying secp256k1 key still backs job-secret ECIES decryption and job-result ECDSA signing. That may be acceptable as an implementation shortcut, but it should be treated as a design decision to revisit rather than a clean key hierarchy.

The PR stack makes the API match the intended semantics:

- Executor keeps the key field, renamed to `executorSecretsAuthPublicKey`.
- Streaming, vLLM proxy, DKMS, and telemetry no longer accept or register a public-key parameter.
- Non-executor `TEEServiceNode.executorSecretsAuthPublicKey` values are stored as empty bytes.
- Non-executor `extendedData` is now `abi.encode(mTlsSpkiHash, endpoint, paymentAddress)`.
- Executor `extendedData` is now `abi.encode(mTlsSpkiHash, executorSecretsAuthPublicKey, paymentAddress, endpoint)`.

## Auditability Improvements

In addition to fixing those correctness issues, the PRs make the registration code easier to audit.

The contract now has shared TDX registration preflight for the checks that should not differ by service: self-registration, configured whitelist enforcement, nonzero payment address, endpoint validation, and nonzero mTLS SPKI hash. Service-specific capability checks remain visible in each public registration function, so the code avoids both policy drift and an opaque generic registration path.

The metadata names now say what they mean:

- `publicKey` became `executorSecretsAuthPublicKey`, making the executor-only behavior explicit.
- `certPubKeyHash` became `mTlsSpkiHash`, which is more precise because the value is `SHA256(cert.RawSubjectPublicKeyInfo)`: the X.509 SubjectPublicKeyInfo hash for the TLS certificate public key, not a hash of a private key or the full certificate.
- Solidity comments describe the SPKI hash in both practical TLS terms and exact encoding terms.

The Go side now has a shared non-executor registration helper in `ritual-go-common`. Streaming, vLLM proxy, DKMS, and telemetry all use the same flow for:

- encoding non-executor extended data,
- constructing TDX report data,
- generating real or dummy attestations,
- fetching nonce/deadline metadata,
- computing and signing the permit digest,
- locally verifying the recovered signing address,
- dispatching to the capability-specific registry method.

Executor registration intentionally remains separate because executor is the only service that binds executor secrets/auth key material.

## Rollout Shape

This is an ABI-breaking registration metadata cleanup, so the stack is intentionally coordinated:

- `ritual-sc-internal` changes the contract interface, validation policy, events, storage field names, and tests.
- `ritual-go-common` regenerates bindings and provides the shared non-executor registration helper.
- `dkms`, `ritual-vllm-proxy-go`, `ritual-streaming-service`, and `ritual-agent-telemetry` remove unused non-executor public-key registration arguments and use the shared helper.
- `executor-go-internal` follows the renamed executor key and mTLS SPKI fields, and stops treating DKMS registry lookups as a source of public-key metadata.
- `ritual-node-internal` and `chain-deployment-infra` update local/deployment config so the new payment-address requirement is satisfied in actual environments, not just in unit tests.

Endpoint policy is deliberately preserved rather than broadened in this stack. Non-executor services still require endpoints; executor keeps its existing optional endpoint behavior for backward compatibility.
