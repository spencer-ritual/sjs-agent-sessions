# Ritual-Reth Panic Target Audit

**Date:** 2026-02-26
**Scope:** All 17 `ritual-*` crates in `ritual-reth-internal`
**Goal:** Identify every production code path where the node can panic, prioritized by exploitability from external input (transactions, contract storage, executor output).

---

## Executive Summary

**28 production-code panic sites** found across 7 crates. 10 crates are clean.

| Risk | Count | Description |
|------|:-----:|-------------|
| CRITICAL | 2 | Directly triggerable by a single malicious transaction on consensus path |
| HIGH | 4 | On-chain state or RwLock on consensus path |
| MEDIUM | 5 | Requires malicious executor output or specific preconditions |
| LOW / Negligible | 17 | Guarded by invariants, RPC-only, or theoretically unreachable |

The most dangerous findings are in `ritual-async-fees` (user-controlled transaction input parsed with panicking `U256::to::<T>()`) which is called from both the block builder and block verifier.

**Important architectural note:** The `SpcVerifier` RwLock (6 unwrap sites in `ritual-spc-verification`) is **NOT on the consensus path** — it's only used by the RPC endpoint. The block builder and verifier read executor keys directly from contract storage. RwLock poisoning cannot halt the chain.

---

## CRITICAL — Chain-Halting from a Single Transaction

### C1. `ritual-async-fees/src/lib.rs:906-907` — Multimodal UX params from user input

```rust
let steps_raw = U256::from_be_slice(steps_word).to::<u128>();
let fps_raw = U256::from_be_slice(fps_word).to::<u128>();
```

- **Code path:** `extract_output_ux_params_from_input()` — marked `CONSENSUS CRITICAL`
- **Called during:** Phase 2 block building AND verification only — when the executor delivers a settlement result. **Not called during Phase 1** (the user's initial ImageCall transaction inclusion).
- **Trigger:** User submits a multimodal precompile call where the ABI-encoded `num_inference_steps` or `fps` word has upper 128 bits set (value > `u128::MAX`). `ruint`'s `.to::<u128>()` calls `.expect()` internally.
- **Impact:** Crashes both block builder and all verifiers. Chain halts.
- **Why it works:** `U256::from_be_slice()` reads a raw 32-byte ABI slot. The subsequent `.to::<u128>()` panics if the value exceeds `u128::MAX`. The clamping on lines 910-911 never executes because the panic happens first.
- **Fix:** Replace with `.try_to::<u128>().unwrap_or(u128::MAX)` or add a bounds check before conversion.

**Current de-facto mitigation (fragile):** The Go executor validates `num_inference_steps` as `uint16` before processing a job. With `steps = 2^128`, the executor rejects or skips the job and never submits a Phase 2 delivery. No delivery = `create_delivery_settlement_transaction()` is never called = the panic site is never reached. Tested against the local network: Phase 1 tx is accepted and mined, chain stays alive, no Phase 2 settlement is produced.

**Why this is not a real fix:** The mitigation lives entirely in off-chain executor software, not in the protocol. Any of the following bypasses it:
- A different executor implementation (if we ever allow custom dapp impls) that doesn't validate `num_inference_steps` before submitting Phase 2
- A future executor version that changes its uint16 parsing behavior

**Ideal fix:** Enforce the field-width constraint in the precompile itself (on-chain, in `ritual-async-fees` or in the Solidity precompile entry point) so no executor can ever deliver a Phase 2 settlement for a job whose stored input would cause the Rust panic. The precompile should reject Phase 1 submissions where `num_inference_steps > u16::MAX` or `fps > u8::MAX` at the time the transaction is first validated, before it is stored on-chain.

### ~~C2/C3~~ DOWNGRADED: `ritual-spc-verification/src/verifier.rs` — RwLock unwraps (RPC-only, not consensus)

**CORRECTION:** After deeper tracing, the `SpcVerifier` struct with the `RwLock<ExecutorRegistry>` is **NOT on the consensus-critical path**. It is only used by:
- **RPC endpoint** (`rpc/rpc/src/ritual.rs`) — on-demand SPC verification via `ritual_verifySpc` RPC calls
- Created in `BuilderContext` and passed to the RPC module via `AddOnsContext`

The actual block builder (`ethereum/payload/src/lib.rs`) and block verifier (`ritual-block-verification/src/verifier.rs`) both read executor keys directly from contract storage via `read_executor_public_keys()` and call `verify_signature_core()` — they never touch the `SpcVerifier` struct or its RwLock.

**Remaining risk:** A poisoned RwLock would kill the RPC verification endpoint but would NOT halt the chain. Demoted to LOW.

**Additional RwLock poisoning analysis:**
- In Rust's `std::sync::RwLock`, only a panic while holding a **write guard** poisons the lock. Read guards do NOT poison.
- The **only** write lock acquisition is at `verifier.rs:194`: `*self.executor_registry.write().unwrap() = new_registry;`
- The write guard scope is a single struct assignment (drop old `ExecutorRegistry` + move new one in). `ExecutorRegistry` is `#[derive(Debug)]` with no custom `Drop` — it contains a `HashMap<Address, ExecutorInfo>` and a `usize`. Its drop cannot panic.
- **Conclusion:** The write guard scope is essentially zero-risk. Poisoning this lock requires an extremely exotic scenario (e.g., a signal/abort mid-assignment). The 6 `read().unwrap()` calls are therefore practically unreachable panics, not exploitable attack targets.

### C4. `ritual-precompile-codecs/src/long_running.rs:837` — FHE output size decode

```rust
Ok(val.as_u64())
```

- **Code path:** `extract_fhe_output_size()` — decodes FHE result delivery payloads
- **Called during:** FHE settlement transaction processing
- **Trigger:** `ethereum_types::U256::as_u64()` contains an internal `assert!` that panics if value > `u64::MAX`. Despite the ABI type being `Uint(64)`, `ethabi`'s decoder reads a full 32-byte slot into `U256` without enforcing bit-width. A crafted payload with `output_size_bytes` > 2^64 passes decode but panics on conversion.
- **Impact:** Crashes during settlement processing. Every other Uint→u64 conversion in this crate uses `u64::try_from(*val).map_err(...)`, making this the sole inconsistency.
- **Fix:** Replace with `u64::try_from(*val).map_err(|_| CodecError::InvalidFieldValue { ... })?`.

**Trigger requires a malicious executor.** The Go executor encodes `output_size_bytes` as `uint64`, so a legitimate executor can never submit a value > 2^64-1 — Go's type system bounds it at encoding time. However, a malicious registered executor can hand-craft the Phase 2 ABI delivery bytes with `output_size_bytes` set to any 32-byte value, bypassing the Go encoder entirely. Unlike C1 (which any user can trigger), C4 requires control of a registered FHE executor.

---

## HIGH — On-Chain State & Payload Builder Invariants

### ~~H1/H2~~ DOWNGRADED: `ethereum/payload/src/lib.rs` — execution_result / commitment_tx expects

**CORRECTION:** After tracing the async pool state machine, these `.expect()` calls are **unreachable** due to multiple layers of protection:

1. **Explicit `is_none()` guards before the `.expect()`:** The payload builder at lines 1157-1175 checks both `commitment_tx.is_none()` and `execution_result.is_none()` and skips the transaction with `continue` before reaching the `.expect()` at line 1343. For `commitment_tx` at lines 2885/3289, additional `ok_or_else()?` guards at lines 2785 and 2967 return `Err` before the `.expect()`.

2. **Atomic state transitions in the pool:** Both `fulfill_transaction()` and `add_async_result()` set `state = Fulfilled` and `execution_result = Some(...)` within the same `DashMap::get_mut()` lock scope (per-entry write lock). No reader can see `Fulfilled` without `execution_result = Some(...)`. `commitment_tx` is set to `Some(...)` at creation and never cleared.

**Reclassified as LOW.** The `.expect()` calls serve as belt-and-suspenders defense behind real guards.

### H3. `ritual-async-fees/src/registry.rs:224` — Model registry max_seq_len

```rust
let max_seq_len =
    if max_seq_len_u256.is_zero() { None } else { Some(max_seq_len_u256.to::<u64>()) };
```

- **Code path:** `read_model_from_db()` — called during fee calculation for every LLM transaction
- **Called during:** Block building and verification for LLM precompile calls
- **Trigger:** If `maxSeqLen` stored in the on-chain ModelRegistry contract exceeds `u64::MAX`. Requires a malicious governance proposal or contract upgrade bug to set an out-of-range value.
- **Impact:** Crashes on any block containing an LLM transaction referencing this model.
- **Note:** All other fields in the same function use safe checked conversions (`u256_to_f64_scaled()`, `u256_to_u128()`, `u256_to_u32()`). This field bypasses them.

### H5-H7. `ritual-sequencing-rights/src/reader.rs` — Cache RwLock (CONSENSUS)

| ID | Line | Pattern | Method |
|----|------|---------|--------|
| H5 | 68 | `.read().expect("RwLock poisoned")` | `read_ordering()` |
| H6 | 79 | `.write().expect("RwLock poisoned")` | `read_ordering()` |
| H7 | 325 | `.write().unwrap()` | `clear_cache()` |

- **Code path:** `SequencingRightsReader` — called during block building and verification for transaction ordering
- **Trigger:** Lock poisoning from a prior thread panic while holding the cache lock.
- **Same RwLock poisoning analysis applies:** The write guard scope in `read_ordering()` (line 79) covers only `cache.insert(contract, ordering.clone())` — a simple HashMap insert that cannot panic. The `clear_cache()` write guard covers only `cache.clear()`. Poisoning is practically unreachable.
- **Note:** H5/H6 have intentional `.expect()` messages acknowledging the design choice. H7 uses bare `.unwrap()` — inconsistent.

---

## MEDIUM — Malicious Executor Output

### M1-M2. `ritual-async-fees/src/llm.rs:459-460` — LLM token counts

```rust
let prompt_tokens_f64 = prompt_tokens.to::<u128>() as f64;
let completion_tokens_f64 = completion_tokens.to::<u128>() as f64;
```

- **Code path:** `decode_pricing_data()` — decodes encrypted LLM response pricing
- **Trigger:** Executor emits `prompt_tokens` or `completion_tokens` > `u128::MAX` in settlement delivery result.
- **Impact:** Crashes during settlement processing for that specific job.

### M3-M4. `ritual-async-fees/src/llm.rs:512-514` — Model metadata

```rust
let params_b = parameter_count.to::<u128>() as f64 / 1_000_000_000.0;
let theta = theta_scaled.to::<u128>() as f64 / THETA_SCALE;
let max_seq = if max_seq_len.is_zero() { None } else { Some(max_seq_len.to::<u64>()) };
```

- **Code path:** `decode_model_metadata()` — parses executor-emitted model metadata from non-encrypted LLM responses
- **Trigger:** Executor emits extreme values for `parameter_count`, `theta`, or `max_seq_len`.
- **Note:** The caller handles `Err`, but `.to::<T>()` panics rather than returning `Err`, bypassing error handling.

### M5. `ritual-async-fees/src/llm.rs:525` — Generic U256→f64 helper

```rust
pub fn read_u256_as_f64(word: &[u8]) -> f64 {
    let value = U256::from_be_slice(word);
    value.to::<u128>() as f64
}
```

- **Code path:** `read_u256_as_f64()` — called from `decode_completion_metrics()` for prompt/completion tokens in unencrypted LLM responses
- **Trigger:** Any 32-byte word with upper 128 bits set.

---

## LOW / NEGLIGIBLE — Guarded by Invariants or RPC-Only

These are technically `unwrap`/`expect` calls in production code, but are protected by prior checks, architectural isolation, or impractical trigger conditions. Listed for completeness.

| ID | Crate | File:Line | Pattern | Why safe |
|----|-------|-----------|---------|----------|
| L1 | spc-verification | verifier.rs:177,194,226,278,578,598 | 6x RwLock `.read()/.write().unwrap()` | **RPC-only path** — not used by builder/verifier. Lock poisoning requires panic during write guard, but write scope is a trivial struct assignment. |
| L2 | precompile-codecs | executor.rs:87-91 | 5x `tokens.pop().unwrap()` | Guarded by `tokens.len() != 5` check |
| L3 | scheduled-verification | lib.rs:159 | `.try_into().unwrap()` | Slice `[24..32]` is always 8 bytes |
| L4 | scheduled-verification | predicate.rs:95 | `.try_into().expect()` | Slice `[12..32]` is always 20 bytes |
| L5 | sequencing-rights | classifier.rs:136 | `.next().unwrap()` | Guarded by `match 1 =>` |
| L6 | sequencing-rights | classifier.rs:187 | `.next().unwrap()` | Guarded by `match 1 =>` |
| L7 | sequencing-rights | classifier.rs:211 | `.next().unwrap()` | Guarded by `if count == 1` |
| L8 | sequencing-rights | priority.rs:63 | `.max().unwrap()` | Guarded by `!is_empty()` |
| L9 | sequencing-rights | bucket.rs:185,191 | `assert_eq!` + `.expect()` | Intentional consensus safety net |
| L10 | async-commitment-validator | lib.rs:192 | `unreachable!()` | Outer match handles this variant |
| L11 | block-verification | nonce_lock.rs:389 | `.get().unwrap()` | HashMap populated in same loop |
| L12 | block-verification | nonce_lock.rs:398 | `.get().unwrap()` | Same invariant as L11 |

---

## Structural Risks — Implicit Invariants

### S1. `ritual-async-inspector/src/inspector.rs:110-113` — Three unwraps on Option fields

```rust
precompile_address: self.precompile_address.unwrap(),
input: self.precompile_input.clone().unwrap(),
caller_address: self.caller_address.unwrap(),
```

- **Code path:** `async_call_result()` — called after EVM inspection
- **Guard:** `if self.has_async_call` — but the invariant that `has_async_call == true` implies all three `Option` fields are `Some` is implicit and maintained across the struct. A future refactor that sets `has_async_call = true` without populating all fields would cause a panic.
- **Risk:** Low today, fragile to refactors.

---

## Clean Crates (No Production Panic Risks)

| Crate | Status |
|-------|--------|
| `ritual-async` | Clean — all unwraps in tests |
| `ritual-async-registry` | Clean — all unwraps in tests |
| `ritual-spc-signature` | Clean — all unwraps in tests |
| `ritual-tee-registry-reader` | Clean — all unwraps in tests |
| `ritual-scheduled-block-building` | Clean — no panic patterns at all |
| `ritual-blocking-pubsub` | Clean |
| `ritual-heartbeat-tracker` | Clean |
| `ritual-metrics` | Clean |

---

## Attack Surface Map

```
User Transaction Input (CONSENSUS-CRITICAL — crashes builder + all verifiers)
  │
  ├─► Multimodal precompile (Image/Audio/Video)
  │     └─► extract_output_ux_params_from_input() ──► C1 PANIC (steps/fps .to::<u128>())
  │         Called from: ethereum/payload/src/lib.rs:3037,3106 (builder)
  │                      ritual-block-verification/src/verifier.rs:957,1123 (verifier)
  │
  ├─► FHE precompile (0x0807)
  │     └─► extract_fhe_output_size() ──► C4 PANIC (output_size .as_u64())
  │         Called from: both builder and verifier Phase 2 fee paths
  │
  └─► LLM precompile (0x0802)
        └─► read_model_from_db() ──► H4 PANIC (max_seq_len .to::<u64>())
            Called from: both builder and verifier fee calculation

Async Pool State Machine (SAFE — guarded by is_none() checks + atomic DashMap transitions)
  │
  ├─► execution_result .expect() at L1343 ──► UNREACHABLE (guarded by L1169 is_none + continue)
  └─► commitment_tx .expect() at L2885/3289 ──► UNREACHABLE (guarded by L2797/2974 ok_or_else?)

Executor Settlement Output (crashes during settlement processing)
  │
  ├─► decode_pricing_data() ──► M1/M2 PANIC (token counts .to::<u128>())
  ├─► decode_model_metadata() ──► M3/M4 PANIC (params/theta/max_seq .to::<u128/u64>())
  └─► read_u256_as_f64() ──► M5 PANIC (.to::<u128>())

RPC Only (does NOT halt chain)
  │
  └─► SpcVerifier RwLock ──► kills ritual_verifySpc RPC endpoint only
```

---

## Key Architectural Insight

The block builder (`ethereum/payload/src/lib.rs`) and block verifier (`ritual-block-verification/src/verifier.rs`) do NOT use the `SpcVerifier` struct with the `RwLock<ExecutorRegistry>`. They both:
1. Read executor public keys directly from contract storage via `read_executor_public_keys()` (from `ritual-tee-registry-reader`)
2. Verify signatures directly via `verify_signature_core()` (from `ritual-spc-signature`)

The `SpcVerifier` struct (which holds `Arc<RwLock<ExecutorRegistry>>`) is only used by the RPC endpoint. **RwLock poisoning cannot halt the chain.**

---

## Recommended Investigation Order

For inducing panics during the audit, prioritize:

1. **C1** — Craft a multimodal precompile transaction (Image 0x0818 / Video 0x081A) with `steps` or `fps` ABI word > 2^128. This is the simplest to trigger. The input is directly user-controlled calldata. It hits both the builder (`ethereum/payload/src/lib.rs:3037`) and the verifier (`ritual-block-verification/src/verifier.rs:957`). Chain halts.
2. **C4** — Craft an FHE delivery result with `output_size_bytes` > 2^64 in the ABI slot. Requires getting a transaction through the async fulfillment pipeline, but the decode is straightforward.
3. **H4** — If governance can set `maxSeqLen` > 2^64 in ModelPricingRegistry, any subsequent LLM transaction panics in both builder and verifier.
4. **M1-M5** — Craft executor settlement payloads with extreme token counts. Requires being a registered executor.
