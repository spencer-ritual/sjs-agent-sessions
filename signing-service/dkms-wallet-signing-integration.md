# DKMS wallet-style signing integration

**Status:** Draft (pre-implementation)  
**Date:** 2026-04-06  
**Related:** [credential-services-design.md](./credential-services-design.md) (EVM `evm.send_transaction` / signer HTTP sketch)

## Goal

Shift from **exporting key material** from dKMS (and from the executor’s internal key-derivation server) to **dKMS performing signing** inside the trust boundary—aligned with the credential-service design (“simulate → sign → broadcast,” keys not exposed to agents).

This document inventories **where keys are fetched today**, **how transactions are actually built and signed** in `executor-go` and `claw-spawner`, and what that implies for dKMS API design **before** implementation.

**Implementation:** New signing APIs are **additive**; **`POST /v1/get_key` stays** until a separate deprecate/remove effort. See **§6–§8** (strategy, phased plan, alignment questions).

---

## Executive summary: who signs and broadcasts?

This is the distinction that matters for **agent-owned** behavior vs **executor-mediated** work.

| Context | Code (primary) | Who signs the EVM tx | Who calls `SendTransaction` |
|--------|----------------|----------------------|-----------------------------|
| **Claw agent sidecar** — on-chain **register** / **heartbeat** | `claw-spawner/agent-sidecar/pkg/heartbeat/heartbeat.go` | **The agent process** (`h.agentKey`) | **The agent process** (`h.ethClient`) |
| **x402 on-chain payment** (HTTP precompile / job on executor) | `executor-go/.../httpcall/x402/settler.go` | **The executor** (key derived in-process) | **The executor** |

### Claw heartbeater: step-by-step (agent signs and submits)

For heartbeat/register **chain transactions**, the sidecar does **not** route signing or broadcast through executor-go’s tx pipeline. The flow is:

1. **`dkmsClient.DeriveKey(0)`** — calls the executor’s **key-derivation** server (`POST /v1/derive_key`), which wraps dKMS `get_key` + HKDF; returns **private key hex** and **address** to the container.
2. Parse into **`h.agentKey`** (`*ecdsa.PrivateKey`), held **in memory in the sidecar** (`heartbeat.go` `New()`).
3. **`sendTx`** builds an **EIP-1559** tx (`types.DynamicFeeTx`: `ChainID`, nonce, gas tip/fee caps, gas limit, `To` = heartbeat contract, `Data` = calldata).
4. **`types.SignTx(tx, types.LatestSignerForChainID(chainID), h.agentKey)`** — the **agent** key signs.
5. **`h.ethClient.SendTransaction(ctx, signedTx)`** — the **agent** submits to the RPC.

**Executor TEE signatures are separate:** `SignRegistration` / `SignHeartbeat` on the same key-derivation base URL sign **digests with the executor TEE key** for fields the contract expects (`executorSignature`). That is attestation-style co-signing, **not** “executor submits the agent’s keyed tx.”

**References:** `heartbeat.go` — `New()` (derive + parse key), `sendTx()` (build, `SignTx`, `SendTransaction`).

---

## 1. Current architecture (two different “DKMS” surfaces)

Understanding the split is required for migration planning.

### 1.1 dKMS service (`dkms` repo)

- **Endpoint:** `POST /v1/get_key`
- **Request:** `keyId` (owner address), `executorId`, `index`, `dkmsKeyFormat` (`"Eth"`)
- **Response:** `ownerRootKey` (base64), `salt`
- **Transport / auth:** mTLS client cert tied to executor; on-chain registry checks (executor valid, `HTTP_CALL` capability today)
- **Role:** Returns a **32-byte owner root key**; all downstream app-specific keys are derived in the **client** (executor) via HKDF (`executor-go/internal/dkms/derivation.go`)

### 1.2 Executor “key derivation” HTTP server (`executor-go`)

Runs on a **dedicated port** (e.g. `:9200`), **Docker-only**, for **agent containers**.

| Route | Purpose |
|-------|---------|
| `POST /v1/derive_key` | Calls `dkms.Manager.GetOwnerRootKey` then `dkms.DeriveX402Key` and returns **`private_key` (hex) + `address`** to the caller |
| `POST /v1/sign_heartbeat` | Signs heartbeat digests with the **executor TEE private key** (not DKMS owner key) |
| `POST /v1/sign_registration` | Same: **executor TEE** attestation signing |

**Important:** Heartbeat/registration signing is **not** “wallet keys from dKMS”; it proves executor identity. Wallet-style payment signing is a separate path (below).

**Reference:** `executor-go/internal/services/keyderivation/server.go`, `heartbeat.go`

### 1.3 Claw-spawner agent sidecar

- HTTP client: `claw-spawner/agent-sidecar/pkg/dkms/dkms.go` — `POST /v1/derive_key`, `POST /v1/sign_heartbeat`, `POST /v1/sign_registration` (Bearer token).
- **Agent-owned chain txs:** see **Executive summary** above — heartbeater **`sendTx` → `SignTx` → `SendTransaction`** is entirely in the sidecar after `DeriveKey`.

---

## 2. Where wallet-relevant signing happens today (executor-go)

### 2.1 X402 on-chain settlement (primary “full tx” path)

**Entry points** (all converge on the same settlement core):

- `internal/handlers/httpcall/handler.go` — `settlePaymentWithDkms` → `dkms.SettleX402Payment`
- `internal/handlers/longrunninghttp/handler.go` — same pattern
- `internal/services/poll/service.go` — dKMS x402 settlement for poll jobs

**Flow today:**

1. `dkms.SettleX402Payment` (`internal/dkms/x402.go`):
   - `manager.GetOwnerRootKey(ctx, ownerAddress, keyIndex, format)`
   - `DeriveX402Key(ownerRootKey, keyFormat, keyIndex)` → `*ecdsa.PrivateKey`
   - `x402.SettlePaymentWithKey(ctx, requirements, signingKey, secrets)`

2. **Shared tx builder/signer:** `internal/handlers/httpcall/x402/settler.go` — `settlePaymentInternal`

**What `settlePaymentInternal` does (concrete construction):**

- `ethclient.DialContext` → RPC
- `ChainID`, `PendingNonceAt(payerAddress)`
- EIP-1559 fee fields: `SuggestGasTipCap`, latest header `BaseFee`, then `gasFeeCap = 2*baseFee + gasTipCap`
- Builds `types.DynamicFeeTx`:
  - **Native transfer:** `To = recipient`, `Value = amount`, `Gas = 21000`, `Data = nil`
  - **ERC20:** `To = token contract`, `Value = 0`, `Data = buildERC20TransferData(recipient, amount)`, `Gas = 100000`
- Signs: `types.LatestSignerForChainID(chainID)` + `types.SignTx(tx, signer, payerKey)`
- Submits with retries, waits for receipt

**Implication for dKMS:** Any “send transaction” API must either accept a **fully specified unsigned EIP-1559 tx** (or equivalent canonical fields) plus **chain id**, or duplicate this construction **inside** dKMS with RPC access. The executor already has a **single helper** for the economic + encoding details: `settlePaymentInternal` (plus `buildERC20TransferData`).

**Config:** dKMS payment flows require `DKMS_PAYMENT_CONFIG` in secrets so the **user authorizes** RPC URL + network + asset limits (`settler.go` `SettlePaymentWithKey` + `ParseDkmsPaymentConfig`).

### 2.2 Other signing (not type-2 broadcast tx)

- **EIP-712 / permit-style x402 authorization:** `internal/handlers/httpcall/payment.go` — `SignX402Payment` builds an EIP-3009-style authorization and signs a digest with `registry.SignPermitDigest`. This is **not** the same code path as `settlePaymentInternal`; credential-service v1 explicitly de-scoped generic `sign_message`, but this exists for HTTP payment headers.
- **Poll delivery / SPC:** `internal/services/poll/submitter.go` — signs **delivery proofs** with executor key material, not DKMS owner keys.
- **Precompile “DKMS key” handler:** `internal/handlers/dkmskey/handler.go` — resolves **payment address** and **DA public key** via `dkms.DerivePaymentAddress` / `DeriveDAPublicKey` for on-chain visibility; does not submit EVM txs.

### 2.3 DA encryption keys (still root-key export)

- `internal/handlers/persistentagent/handler.go`, `sovereignagent/handler.go` — `GetOwnerRootKey` + `DeriveDAKeypair` for ECIES-style DA encryption.

These flows are **not** “submit EVM tx” but will remain sensitive if dKMS stops returning raw root keys; they may need **separate** policies or continued derivation APIs.

---

## 3. HKDF / key identity (must stay consistent)

Executor derives application keys from `ownerRootKey` using fixed salts (`internal/dkms/derivation.go`):

- **X402 payment key:** salt `http_dkms_salt`, format byte + big-endian index
- **DA key:** different salt (`DAEncryptionSalt`)

Any move to **server-side signing** must preserve **the same derivation** for a given `(owner address, index, format)` or explicitly version/migrate identities.

---

## 4. Integration points to touch when dKMS signs (checklist)

| Layer | Component | Today | Likely change |
|-------|-----------|-------|---------------|
| dKMS service | `POST /v1/get_key` | Returns root key | **Add** signing routes; keep `get_key` unchanged until follow-up (see §6) |
| Executor | `internal/dkms/client.go` | `GetOwnerRootKey` HTTP | New methods: e.g. `SignTransaction`, `SendTransaction`, or `GetAddress` only |
| Executor | `internal/dkms/manager.go` | Failover around `GetOwnerRootKey` | Same pattern for new endpoints |
| Executor | `internal/dkms/x402.go` | Derive key locally → `SettlePaymentWithKey` | Call dKMS to sign+send (or sign-only) with structured payload; strip local private key |
| Executor | `internal/handlers/httpcall/x402/settler.go` | `settlePaymentInternal` | Reuse **construction** logic or move “build unsigned tx” to shared package; signing may move to dKMS |
| Executor | `httphandler` / `longrunninghttp` / `poll/service` | Call `SettleX402Payment` | No semantic change if `SettleX402Payment` switches implementation |
| Executor | `internal/services/keyderivation/server.go` | Returns **private key** to agents | **Major:** either remove raw key for payment indices, or proxy “request signature” to dKMS; security policy decision |
| Claw-spawner | `agent-sidecar/pkg/dkms/dkms.go` | `DeriveKey` | Align with new APIs if agents stop receiving raw keys |
| On-chain / registry | dKMS capability policy | `HTTP_CALL` for get_key | May need **DKMS-specific** capability or extended policy for signing |

---

## 5. Planned dKMS APIs: two signing modes

We intend to implement **both** of the following (naming and paths TBD): **(1)** sign an unsigned EVM transaction (RLP), **(2)** sign a **pre-hashed 32-byte digest** (no hashing inside dKMS; caller does all upstream hashing).

### 5.1 Sign unsigned transaction (EVM)

**Intent:** Sign a **canonical unsigned EVM transaction**—the same object callers build today with `go-ethereum` (`types.DynamicFeeTx`, etc.) before `SignTx`.

**Wire format (decided):** Use the **Ethereum-standard** representation: **RLP-encoded unsigned transaction** as hex (`0x…`). Callers construct `types.Transaction` without a signature, RLP-encode the unsigned form, and send that payload to dKMS. This matches go-ethereum, hardware wallets, and common custody APIs; **structured JSON** for EIP-1559 fields is **not** the primary format (could be added later for ergonomics only).

**Rough inputs:** key identity (`keyId` / owner + `index` + format), **unsigned transaction** = **RLP hex** as above.

**Rough output:** **Signed transaction** (hex), suitable for `SendTransaction` by the caller.

**Who broadcasts (v1):** For the first iteration, **the executor or the agent** submits the signed tx to RPC—**not** dKMS. Whether **dKMS should ever** own broadcast (policy, RPC allowlists, fewer round-trips) is **still open**; no commitment in this doc. The [credential-services](./credential-services-design.md) sketch mentions a combined `send_transaction`; treat that as a **possible** later shape, not a v1 requirement here.

**Use cases:**

| Use case | Why this API |
|----------|----------------|
| **x402 on-chain settlement** (`settlePaymentInternal`) | Tx is already built in the executor; only `SignTx` should move into dKMS. |
| **Claw heartbeater** (`sendTx` → `SignTx` → `SendTransaction`) | Full EIP-1559 tx to the heartbeat contract; remote signing replaces local `h.agentKey`. |
| **Any future “build tx locally, never hold key” flow** | Matches hardware-wallet behavior: unsigned tx in → signed tx out. |

### 5.2 Sign raw payload — **32-byte digest only (no hashing in dKMS)**

**Intent:** Sign a **final 32-byte digest** with the derived secp256k1 key—**not** a raw Ethereum transaction (that is §5.1). dKMS applies **no** hash function: the digest is the **opaque** input to ECDSA (whether the caller produced it via Keccak256, EIP-712, SHA-256, or anything else is **not** dKMS’s concern).

**Rule (decided):** The signing input must be **exactly 32 bytes** (e.g. `0x` + 64 hex characters). Any other length is **rejected**. There is **no** string payload path, **no** default Keccak of UTF-8, and **no** encoding enum in v1—callers **precompute** whatever the protocol requires (EIP-712 hash, permit digest, etc.) and submit the **resulting hash** only.

**Rough inputs:** key identity (same as §5.3), **`digest`** (or equivalent field name) = **32 bytes** hex-encoded.

**Rough output:** ECDSA signature (`r`, `s`, `v` or 65-byte `0x` sig).

**Use cases:**

| Use case | Flow |
|----------|------|
| **EIP-712 / permit-style x402** | Executor runs `computeEIP712Hash` (or equivalent) → passes **32-byte** digest → dKMS signs. |
| **Any other protocol** | Caller produces the **final** hash off-chain → same. |

### 5.3 Shared concerns (both APIs)

- **Authorization (decided):** New signing endpoints use the **same authorization mechanism** as `POST /v1/get_key`—**mTLS**, **executor identity from the client cert**, and **on-chain registry checks** in the same way as existing `handleGetKey` (no separate auth stack for v1).
- **Identity:** Same as today’s `get_key`: owner address + **index** + **format** (Eth), unless we introduce opaque `signer_id` handles later.
- **Policy (beyond auth):** Quotas, allowlisted chains; **RPC egress from dKMS** only matters if dKMS gains a broadcast path later (see **Who broadcasts** under §5.1).
- **Idempotency:** Mutating operations should accept **`idempotency_key`** (per credential design).
- **Simulation:** Optional `eth_call` / simulation before sign for tx path; typically N/A for raw-payload-only.

**Address discovery:** **`GET` address for signer** (or equivalent) remains useful for funding and display without exporting private keys.

### 5.4 Recorded decisions (this iteration)

| Topic | Decision |
|-------|----------|
| **Auth on signing routes** | Same as `get_key`: mTLS + registry / executor verification, shared with existing flows. |
| **Unsigned tx on the wire** | **RLP** (hex), not structured JSON as the primary format. |
| **Who broadcasts** | **v1:** **Executor or agent** calls `SendTransaction` after receiving the signed tx from dKMS. Long-term: **TBD** whether dKMS should broadcast (or always stay sign-only). |
| **Raw payload (§5.2)** | **Exactly 32-byte digest** (hex). **No** hashing inside dKMS; caller precomputes (EIP-712, Keccak, etc. as required). |

---

## 6. Implementation strategy: additive first, no removal yet

**Principle:** Ship **new** signing endpoints and wire **one** client path behind a flag or parallel implementation **before** changing or removing **`POST /v1/get_key`** or any executor behavior that depends on exported keys.

| Phase | What we do | What we explicitly do *not* do yet |
|-------|------------|-------------------------------------|
| **A — dKMS service** | Add sign-tx + sign-raw-payload (+ optional get-address) routes; reuse existing key derivation inside the service; tests | **Delete**, **disable**, or **break** `get_key` |
| **B — executor `internal/dkms` client** | HTTP client methods + manager failover for new routes | Switch `SettleX402Payment` / keyderivation off `get_key` by default (unless you decide otherwise) |
| **C — integration** | Optional feature flag to use remote signing for one vertical (e.g. x402 only) | Remove `derive_key` private-key response from agent-facing server |
| **Follow-up (separate effort)** | Policy to restrict or remove raw key export; migrate agents | “Master delete” of legacy paths |

This doc’s **implementation plan** (§7) assumes **Phase A** is the first mergeable milestone unless you answer otherwise in §8.

---

## 7. Phased implementation plan (draft)

Steps are ordered for **safe incremental delivery**. Adjust after §8 is filled in.

### Phase A — `dkms` repo (server-only)

1. **Crypto:** Reuse existing `KeyManager` / `DeriveOwnerRootKey` + same HKDF as executor (`internal/crypto` or shared derivation—match `executor-go/internal/dkms/derivation.go` semantics for index/format).
2. **Sign EVM unsigned tx:** Accept **RLP hex** unsigned tx (§5.1), parse with go-ethereum, sign with derived secp256k1 key, return signed tx hex (and optionally raw bytes base64).
3. **Sign raw digest:** Accept **exactly 32-byte** digest (hex); reject otherwise; **no** hash step in dKMS; sign with derived key. Output `r,s,v` or 65-byte sig.
4. **Optional:** `GET` or `POST` **address** for `(keyId, index, format)` using same derivation as today (no private key in response).
5. **Auth:** Same as `handleGetKey` (§5.3, §5.4)—mTLS + registry; no separate auth model.
6. **Observability:** Metrics + structured logs (no secrets); audit fields TBD.
7. **Tests:** Unit tests for vectors; integration test with dev TLS skip if applicable.

### Phase B — Executor client (`executor-go/internal/dkms`)

1. Extend `Client` / `Manager` with `SignEVMTransaction`, `SignRawPayload` (names TBD), same discovery + failover as `GetOwnerRootKey`.
2. **Do not** remove `GetOwnerRootKey`.

### Phase C — Call-site migration (optional, behind flag)

1. e.g. `SettleX402Payment`: build unsigned tx as today → call dKMS sign → **broadcast in executor** (§5.1 v1); dKMS-side broadcast is out of scope for v1.
2. Key derivation server / claw: **out of scope** for first merge unless you prioritize agent-side changes in §8.

### Phase D — Follow-up (not part of “first working” milestone)

- Deprecate `get_key` for certain indices, agent `derive_key` behavior, documentation, registry policy updates.

---

## 8. Questions to align before implementation

Answer inline in this doc, in a PR, or in thread. **Bold** items block a minimal first PR if unanswered.

### Scope and sequencing

1. **Which phase is the first merge target?** (A only, A+B, or A+B+C for a specific call site?)
2. **Sign transaction vs sign raw payload:** Implement **both** in the first dKMS PR, or **sign transaction first** and raw-payload in a fast follow?
3. **Broadcast:** **Decided for v1:** **sign-only** in dKMS; **executor or agent** broadcasts. **Open later:** dKMS-side broadcast / `send_transaction`-style endpoint.

### Request / response shape

4. **Unsigned tx format:** **Decided:** **RLP hex** (§5.1, §5.4). Revisit structured JSON only if ergonomics demand it later.
5. **Raw payload v1:** **Decided:** **Exactly 32-byte digest** (hex); caller pre-hashes; dKMS does not apply a hash function.
6. **Idempotency:** Required on sign endpoints from day one, or add when executor integrates?

### Security and policy

7. **Same auth as `get_key`?** **Decided:** **Yes** (§5.3). Follow-up: any **stricter** policy for signing (per-chain allowlist enforced **inside** dKMS)?
8. **Rate limits:** Separate limits for sign vs get_key?
9. **Production TEE:** Must signing code paths run only when attestation / production flags match existing dKMS expectations?

### Registry and capabilities

10. **New capability** (e.g. signing) vs **reuse** `HTTP_CALL` / existing DKMS registration for new routes?
11. **Breaking changes:** Confirm **zero** breaking change to `get_key` response or route in Phase A.

### Clients and rollout

12. **First consumer:** Executor x402 only, internal tests only, or another caller?
13. **Feature flag:** Env var name / default (off vs on) for “use remote sign” in executor?

### Testing

14. **Local dev:** Sign without full mTLS (existing dev mode pattern in dKMS?) — acceptable for CI?
15. **Vectors:** Do you want **golden test vectors** (fixed key material in test only) for cross-check with executor derivation?

---

## 9. Out of scope for this note

- OAuth and web2 credential flows
- Exact registry capability enum changes (listed in §8 instead when decided)
- Whether signing stays in dKMS only vs split with a separate “credential-service” front door
- Removing or restricting `get_key` / `derive_key` (explicitly **later phase**; see §6)

---

## 10. References (paths in repo)

| Path | Relevance |
|------|-----------|
| `dkms/internal/server/server.go` | `handleGetKey`, route registration |
| `executor-go/internal/dkms/client.go` | dKMS HTTP client, `GetKeyRequest` |
| `executor-go/internal/dkms/manager.go` | Endpoint failover |
| `executor-go/internal/dkms/x402.go` | `SettleX402Payment` |
| `executor-go/internal/dkms/derivation.go` | HKDF salts and `DeriveX402Key` |
| `executor-go/internal/handlers/httpcall/x402/settler.go` | **Transaction construction + SignTx** |
| `executor-go/internal/services/keyderivation/server.go` | Agent `derive_key` |
| `executor-go/internal/services/keyderivation/heartbeat.go` | Executor TEE signing (not DKMS wallet) |
| `claw-spawner/agent-sidecar/pkg/dkms/dkms.go` | HTTP client to key-derivation + TEE sign endpoints |
| `claw-spawner/agent-sidecar/pkg/heartbeat/heartbeat.go` | **Agent** `DeriveKey` → `sendTx` / `SignTx` / `SendTransaction` |
