# DKMS wallet-style signing integration

**Status:** Draft (pre-implementation)  
**Date:** 2026-04-06  
**Related:** [credential-services-design.md](./credential-services-design.md) (EVM `evm.send_transaction` / signer HTTP sketch)

## Goal

Shift from **exporting key material** from dKMS (and from the executor’s internal key-derivation server) to **dKMS performing signing** inside the trust boundary—aligned with the credential-service design (“simulate → sign → broadcast,” keys not exposed to agents).

This document inventories **where keys are fetched today**, **how transactions are actually built and signed** in `executor-go` and `claw-spawner`, and what that implies for dKMS API design **before** implementation.

### API surface vs key semantics (**decided**)

These are **two different things**:

1. **Legacy endpoints stay put.** Do **not** change existing contracts—at minimum dKMS **`POST /v1/get_key`** (request/response shape, semantics, behavior). **Additive rollout** here means: **add new routes** for signing / address / digest; leave the old endpoint as-is for whoever still calls it. That is **not** the same topic as “do keys match across stacks?”

2. **New endpoints, new contract.** Wallet-style signing lives on **separate paths** (e.g. `sign_transaction`, `get_address`, `sign_digest`). They can be designed and evolved **without** mutating `get_key`.

3. **Payment identity (x402) is pinned to the owner key** (see subsection above)—not the old `get_key` + **`DeriveX402Key`** address. Other surfaces (DA, future features) may still use **different** derivations from the same root without changing the `get_key` HTTP contract.

Executor-side surfaces (e.g. **`POST /v1/derive_key`**) follow the **same principle**: prefer **adding** proxy routes (`sign_transaction`, …) over silently changing behavior of an existing handler unless we explicitly decide to replace it in a coordinated deploy.

See **§3** (derivation consistency when we *choose* parity), **§6**, and **§8.11**.

### X402 payment: sign with the **owner key** (decided)

For **x402 on-chain settlement**, we **do not** apply the legacy second HKDF (`http_dkms_salt` / `DeriveX402Key`) on top of the owner root. The **payment signer** is the **owner root** for `(keyId, index)` interpreted directly as the **Ethereum secp256k1 private key** (same 32-byte material `POST /v1/get_key` already returns for that identity). dKMS **`sign_transaction`** / **`get_address`** use this rule.

**End-to-end steps (executor):**

1. Upstream returns **402**; payment requirements are parsed as today.
2. Executor **builds the unsigned EIP-1559** payment transaction (native or ERC-20), including nonce/gas/chain id—same construction as today, but **before** signing.
3. Executor calls dKMS **`sign_transaction`** with the unsigned tx RLP and identity fields (`keyId`, `index`, `Eth`). dKMS signs with the **owner Eth key** above (not the old X402 HKDF key).
4. Executor **broadcasts** the signed tx (retries, receipt wait), then **retries the original HTTP request** with the payment receipt header.

**Implication:** The **funded “payment address”** for a user is now the address of the **owner root** key, **not** the address produced by the old `get_key` → `DeriveX402Key` path. **`traffic-gen-internal`** (see `traffic-gen-internal/docs/dkms-payment-address.md`) uses the **DKMS Key precompile** for that address—no local derivation—so it **tracks the executor** once upgraded; **re-fund** if you had balances on the legacy HKDF-derived address.

**Executor `POST /v1/derive_key`:** For Eth, returns the **owner root** interpreted as the private key (aligned with signing routes), not `DeriveX402Key` over the root.

**Unchanged:** **`POST /v1/get_key`** response shape (still returns the owner root bytes). **DA** keys still use a **separate** HKDF from the owner root (`DAEncryptionSalt`); only **payment / Eth wallet** identity moved to “owner key only.”

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
- **Role:** Returns a **32-byte owner root key** per `(keyId, index)`; **payment** signing uses this material **as the Eth key** (no extra X402 HKDF). **DA** and other domains may still use HKDF from that root in the executor (`derivation.go`).

### 1.2 Executor “key derivation” HTTP server (`executor-go`)

Runs on a **dedicated port** (e.g. `:9200`), **Docker-only**, for **agent containers**.

| Route | Purpose |
|-------|---------|
| `POST /v1/derive_key` | Calls `dkms.Manager.GetOwnerRootKey` then treats the owner root as the Eth private key (`DeriveEthPrivateKeyFromOwnerRoot`) and returns **`private_key` (hex) + `address`** (aligned with dKMS signing; not the legacy X402 HKDF layer) |
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

**Flow (decided; see “X402 payment: sign with the owner key” above):**

1. `dkms.SettleX402Payment` (`internal/dkms/x402.go`): resolve payer via `manager.GetAddress` (owner-key address), then `x402.SettlePaymentWithDKMSSigning` — builds **unsigned** tx, calls `manager.SignTransaction` (dKMS **`sign_transaction`** with owner Eth key), **broadcast** in executor.

2. **Tx construction:** `internal/handlers/httpcall/x402/settler.go` — `buildUnsignedPaymentTx` + shared submit/receipt logic (`SettlePaymentWithDKMSSigning`).

**What the unsigned tx builder does (concrete construction):**

- `ethclient.DialContext` → RPC
- `ChainID`, `PendingNonceAt(payerAddress)` (payer = **owner-key** address)
- EIP-1559 fee fields: `SuggestGasTipCap`, latest header `BaseFee`, then `gasFeeCap = 2*baseFee + gasTipCap`
- Builds `types.DynamicFeeTx`:
  - **Native transfer:** `To = recipient`, `Value = amount`, `Gas = 21000`, `Data = nil`
  - **ERC20:** `To = token contract`, `Value = 0`, `Data = buildERC20TransferData(recipient, amount)`, `Gas = 100000`
- **Signing:** dKMS returns signed RLP (`sign_transaction`); executor does **not** hold the private key for payment.

**Implication for dKMS:** `sign_transaction` accepts **RLP-encoded unsigned EIP-1559 tx** + identity; signs with **owner root as Eth key** (see top of doc). Executor keeps **construction**; dKMS keeps **ECDSA only**.

**Legacy note:** The old flow was `get_key` → second HKDF (`http_dkms_salt`) → local `SignTx`. That HKDF layer has been **removed** from executor and dKMS code; payment uses the owner root as the Eth key.

**Config:** dKMS payment flows require `DKMS_PAYMENT_CONFIG` in secrets so the **user authorizes** RPC URL + network + asset limits (`settler.go` `SettlePaymentWithKey` + `ParseDkmsPaymentConfig`).

### 2.2 Other signing (not type-2 broadcast tx)

- **EIP-712 / permit-style x402 authorization:** `internal/handlers/httpcall/payment.go` — `SignX402Payment` builds an EIP-3009-style authorization and signs a digest with `registry.SignPermitDigest`. This is **not** the same code path as `settlePaymentInternal`; credential-service v1 explicitly de-scoped generic `sign_message`, but this exists for HTTP payment headers.
- **Poll delivery / SPC:** `internal/services/poll/submitter.go` — signs **delivery proofs** with executor key material, not DKMS owner keys.
- **Precompile “DKMS key” handler:** `internal/handlers/dkmskey/handler.go` — resolves **payment address** and **DA public key** via `dkms.DerivePaymentAddress` / `DeriveDAPublicKey` for on-chain visibility; does not submit EVM txs.

### 2.3 DA encryption keys (still root-key export)

- `internal/handlers/persistentagent/handler.go`, `sovereignagent/handler.go` — `GetOwnerRootKey` + `DeriveDAKeypair` for ECIES-style DA encryption.

These flows are **not** “submit EVM tx” but will remain sensitive if dKMS stops returning raw root keys; they may need **separate** policies or continued derivation APIs.

---

## 3. HKDF / key identity

Executor derives some keys from `ownerRootKey` using HKDF in `internal/dkms/derivation.go`:

- **Eth payment / x402 (current):** No second HKDF—the **owner root** from dKMS for `(keyId, index)` **is** the secp256k1 private key (`DeriveEthPrivateKeyFromOwnerRoot` on executor; dKMS `deriveEthSigningKey` uses the same `ToECDSA` rule). **Funded address** = `pubkey(owner_root)`.
- **Removed:** The old second HKDF on the owner root (`http_dkms_salt` / `DeriveX402Key`) for payment — **not** used anywhere in executor/dKMS for settlement or signing.
- **DA key:** salt `DAEncryptionSalt` — **unchanged**; still derived from owner root via HKDF (`DeriveDAKeypair`).

**`get_key`** response bytes are unchanged; what changed is **which** transform we apply for **payment** signing (owner key directly vs old X402 HKDF).

---

## 4. Integration points to touch when dKMS signs (checklist)

| Layer | Component | Today | Likely change |
|-------|-----------|-------|---------------|
| dKMS service | `POST /v1/get_key` | Returns root key | **Add** new routes only; **do not change** `get_key` (see § intro). Signing identity may match old HKDF or differ by design (§3). |
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

## 6. Implementation strategy

**Principle:** Ship **new** dKMS routes and wire executors/agents to them. **Leave existing endpoints (e.g. `POST /v1/get_key`) unchanged**—additive means **new APIs**, not editing the old handler.

**Separate axis:** Whether signing on the new routes uses **byte-for-byte the same** derived key as `get_key` + HKDF is a **derivation decision** (§3). We can match for continuity or diverge on purpose; that does **not** require changing `get_key`.

| Phase | What we do | Notes |
|-------|------------|--------|
| **A — dKMS service** | Add sign-tx, sign-digest, get-address (paths TBD); implement derivation policy (match legacy vs new) | **Do not** alter `get_key` |
| **B — executor `internal/dkms` client** | HTTP client + manager failover for **new** routes | Call sites switch to remote signing; `GetOwnerRootKey` only where still needed |
| **C — integration** | x402, key-derivation proxy, claw-spawner, etc. | Prefer **new** executor routes that call dKMS; migrating off raw key export is a **deploy coordination** issue, not “same endpoint, different behavior” |
| **Cleanup** | Docs, metrics, registry policy | Optional deprecation of **callers** of old patterns; `get_key` can remain as long as useful |

This doc’s **implementation plan** (§7) lists steps for ordering; **freezing `get_key`** is the default for the legacy route.

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

1. Extend `Client` / `Manager` with signing helpers (e.g. `SignTransaction`, `GetAddress`), same discovery + failover as `GetOwnerRootKey` where applicable.
2. **`GetOwnerRootKey`:** Keep for flows that still need root material (e.g. DA); narrow usage elsewhere as call sites move to **new** dKMS routes—without changing dKMS `get_key` itself.

### Phase C — Call-site migration

1. e.g. `SettleX402Payment`: build unsigned tx → call dKMS sign → **broadcast in executor** (§5.1 v1); dKMS-side broadcast is out of scope for v1.
2. Key derivation server / claw: add **new** routes that proxy to dKMS signing; prefer not to repurpose `derive_key` in place—either keep it for legacy or add parallel endpoints, per intro.

### Phase D — Follow-up

- Tighten who may still call raw-key export paths; documentation; registry policy. **Default:** keep **`get_key`** stable; evolve behavior on **new** routes and new executor proxies.

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
11. **Legacy routes:** **Decided:** **Do not change** existing dKMS `get_key` (and apply the same discipline to other frozen endpoints). **New** routes may define different derivation/identity if we choose (see intro + §3)—that is **not** the same as editing `get_key`.

### Clients and rollout

12. **First consumer:** Executor x402 only, internal tests only, or another caller?
13. **Feature flag:** Env var name / default (off vs on) for “use remote sign” in executor?

### Testing

14. **Local dev:** Sign without full mTLS (existing dev mode pattern in dKMS?) — acceptable for CI?
15. **Vectors:** Do you want **golden test vectors** (fixed key material in test only) for cross-check with executor derivation?

---

## Manual verification checklist

Use this when validating an end-to-end deploy (executor + dKMS + chain + optional traffic-gen / agents). The first two items are distinct surfaces; the **`derive_key` consistency** subsection below is an optional cross-check.

### Agent-facing API vs dKMS (**executor-go**)

**Agents** (sidecars, containers on the executor Docker network) call **executor-go’s key-derivation HTTP server** (`internal/services/keyderivation/server.go`): **Bearer token** auth to routes such as **`/v1/derive_key`**, **`/v1/get_address`**, **`/v1/sign_transaction`**, **`/v1/sign_heartbeat`**, **`/v1/sign_registration`**. That server is the **agent-facing** surface—it is **not** “the agent opening mTLS to dKMS.”

**Executor-go** implements that HTTP API, then uses **`dkms.Manager`** internally to reach the **dKMS** service over **mTLS** (`get_key`, `sign_transaction`, `get_address`, etc.). So the chain is: **token-authenticated call → executor → mTLS → dKMS**.

When you **manually** verify agent flows, you exercise **executor-go’s** URL + token. When you test **dKMS** in isolation (no executor), you hit the dKMS service directly—that path is for operators or lower-level integration tests, not typical agent traffic.

### 1. X402 on-chain payment + DKMS Key precompile + traffic-gen

This is **one end-to-end check** for traffic-gen’s dKMS x402 path: settlement uses the executor, while **funding** uses the on-chain precompile—both must agree on the payer identity.

**Executor settlement:** `SettleX402Payment` → dKMS **`get_address`** + **`sign_transaction`**.

**Flow:** Upstream returns **402** → executor builds an **unsigned** EIP-1559 payment tx → dKMS signs with the owner Eth key → executor **broadcasts** → retry with payment receipt.

**Precompile / traffic-gen:** `traffic-gen-internal` dKMS x402 actions **do not** derive payment addresses in Python. They call **`get_dkms_payment_address_via_precompile`** (DKMS Key precompile **0x081B**) to mint/fund the payer before the job (see `traffic-gen-internal/docs/dkms-payment-address.md`). The executor’s **`dkmskey`** handler uses the same dKMS manager identity for jobs that use the DKMS Key precompile. A successful **`run-x402-dkms-http-call`** therefore exercises **precompile funding + executor remote signing** together; you do not need a separate manual step to prove precompile vs executor alignment when that run passes.

**What proves it works:** On-chain payment tx from the expected payer address, successful HTTP retry with `X-PAYMENT-RECEIPT` (or equivalent), no local payment private key required in the executor for the signing step; and the payer was funded at the address returned by the precompile (matching **`get_address`** for the same `(owner, index)`). For flows that use the precompile **without** traffic-gen x402 (e.g. some spawn paths), smoke-test those separately if you need coverage beyond this combined check.

### 2. Claw agent heartbeat / on-chain agent transactions (agent-owned chain txs)

**Sidecar** calls the executor **key-derivation** HTTP server:

- **`get_address`** (e.g. index **0**) for the agent’s funded address.
- **`sign_transaction`** with the unsigned agent tx RLP (register / heartbeat contract calls, etc.).

**Also on the same base URL (not DKMS owner keys):** **`sign_heartbeat`** and **`sign_registration`** — these sign with the **executor TEE** key for fields the contract expects (`executorSignature`). They **attest the executor**, not the user’s DKMS-derived wallet.

**Manual run (traffic-gen):** From **`traffic-gen-internal`**, use **`make run-spawn-agent`** to exercise the persistent-agent path (**0x0820** precompile → claw-spawner). That is the usual way to **start an agent** in dev when you want to **observe registration and heartbeats** on-chain and in logs. See the **`run-spawn-agent`** target in `traffic-gen-internal/Makefile` for defaults (`da`, `provider`, `model`, optional `executor=0x…`) and `ARGS`.

**What proves it works:** Agent registers and posts heartbeats on-chain; TEE-signed fields verify; agent chain txs are signed via **`sign_transaction`** without holding a long-lived private key in the sidecar from **`derive_key`** for those txs (if you have migrated to remote sign).

**Observing heartbeats (no separate dashboard):** The **agent-sidecar** (`claw-spawner/agent-sidecar/pkg/heartbeat/heartbeat.go`) is the source of truth in dev.

- **Success:** On each successful on-chain heartbeat, the sidecar logs at **INFO** a line like **`heartbeat tx`** with **`hash`** (transaction hash), **`nonce`**, and **`manifest_cid`**. Registration first logs **`registration confirmed`** with **`hash`** and **`block`**.
- **Failure:** Look for **`heartbeat tx failed`**, **`sign heartbeat failed`**, **`read heartbeatNonce failed`**, or **`too many consecutive failures`** (the loop may **`os.Exit`** after repeated errors). Executor TEE **`sign_heartbeat`** failures show up as **`sign heartbeat failed`** from the key-derivation client.
- **Where to read logs:** **`docker logs`** on the **agent instance** container spawned by claw-spawner (or the spawner’s own logs if it forwards them). There is **no** dedicated heartbeat metrics UI in these repos—use logs plus optional **RPC** inspection of the tx hash (receipt `status == 1`).

**How often:** With **WebSocket** block subscription (`SYSTEM_WS_URL` set), the sidecar reads **`defaultTimeout()`** from the heartbeat contract and posts roughly every **`defaultTimeout / 2` blocks** (re-read on a TTL). If the contract call fails, it falls back to **`HEARTBEAT_CHAIN_INTERVAL_BLOCKS`** from the environment (claw-spawner defaults **200** in `claw_spawner/config.py` and passes it into the instance). **Without WS**, a time-based ticker approximates the same interval (see **`Run`** / **`refreshInterval`** in `heartbeat.go`). The **LLM “heartbeat”** loop in OpenClaw (`agents.defaults.heartbeat.every` / entrypoint) is separate from this **on-chain** cadence.

---

### `POST /v1/derive_key` (key-derivation server) — what it is for

The executor exposes **`POST /v1/derive_key`** on a **Docker-only** port for **agent containers**, as part of **executor-go’s agent-facing API** (Bearer token—see **Agent-facing API vs dKMS** above). It is **not** the same as calling dKMS **`get_key`** directly; it is a **proxy** that:

1. Authenticates the caller (Bearer token tied to owner).
2. Calls **`GetOwnerRootKey`** on the dKMS manager (same owner + index as the request).
3. Interprets the returned 32-byte **owner root** as the **Ethereum private key** (`DeriveEthPrivateKeyFromOwnerRoot`) — same rule as dKMS **`sign_transaction`** / **`get_address`**.
4. Returns **`private_key` (hex)** and **`address`** in JSON.

**Why expose a key at all?** Some sidecar flows still need **raw key material** in-process, e.g. **escrow** (encrypting DA secrets with a derived key at a **non-zero index**), or **legacy tooling** that expects a hex key from `derive_key`. **Chain transactions** are preferably **`sign_transaction`** (no key export); **`derive_key`** remains for cases that cannot yet be expressed as “unsigned tx in, signed tx out.”

**Manual check:** Call `derive_key` with a test owner/index and verify the returned **address** matches **`get_address`** for the same identity; use that key only in trusted agent code paths you intend to support.

---

## 9. Out of scope for this note

- OAuth and web2 credential flows
- Exact registry capability enum changes (listed in §8 instead when decided)
- Whether signing stays in dKMS only vs split with a separate “credential-service” front door

**In scope:** Adding signing/proxy routes and migrating callers. **Out of scope for “silent” edits:** Changing the contract of **`POST /v1/get_key`** without a deliberate, versioned API change (default is leave it as-is).

---

## 10. References (paths in repo)

| Path | Relevance |
|------|-----------|
| `dkms/internal/server/server.go` | `handleGetKey`, route registration |
| `executor-go/internal/dkms/client.go` | dKMS HTTP client, `GetKeyRequest` |
| `executor-go/internal/dkms/manager.go` | Endpoint failover |
| `executor-go/internal/dkms/x402.go` | `SettleX402Payment` |
| `executor-go/internal/dkms/derivation.go` | `DeriveEthPrivateKeyFromOwnerRoot`, DA HKDF (`deriveKey`) |
| `executor-go/internal/handlers/httpcall/x402/settler.go` | Unsigned tx build + `SettlePaymentWithDKMSSigning` |
| `executor-go/internal/services/keyderivation/server.go` | Agent `derive_key`, `sign_transaction`, `get_address` |
| `executor-go/internal/services/keyderivation/heartbeat.go` | Executor TEE signing (not DKMS wallet) |
| `claw-spawner/agent-sidecar/pkg/dkms/dkms.go` | HTTP client to key-derivation + TEE sign endpoints |
| `claw-spawner/agent-sidecar/pkg/heartbeat/heartbeat.go` | `GetAddress` + `sign_transaction` + `SendTransaction` |
| `dkms/internal/server/signing.go` | `deriveEthSigningKey` (owner root → `crypto.ToECDSA`) |
