# Claim Mapping: Old Docs vs Current Code

This file maps every concrete claim in `TX_ORIGIN_PRECOMPILE_VULNERABILITY.md` and
`TX_ORIGIN_PRECOMPILE_VULNERABILITY_IMPLEMENTATION_PLAN.md` (both written against pre-refactor
`origin/dev`) to the current state on `spencer/precomp-msg-sender-rerefresh`, which branches off
the post-refactor `arshan/upstream-merge` tip in `ritual-reth-internal` (HEAD at the time of this
mapping: `e059916fe`).

The rewritten "v2" docs in this directory consume this mapping; treat this file as the audit
trail behind any change in the v2 plan.

## Path Renames

| Old path (in docs) | Current path |
|---|---|
| `crates/ritual-async/src/detector.rs` | `crates/ritual/async/src/detector.rs` |
| `crates/ritual-async/src/wallet.rs` | `crates/ritual/async/src/wallet.rs` |
| `crates/ritual-async-fees/src/wallet.rs` | `crates/ritual/async-fees/src/wallet.rs` |
| `crates/ritual-async-fees/src/lib.rs` | `crates/ritual/async-fees/src/lib.rs` |
| `crates/ritual-block-verification/src/verifier.rs` | **Removed.** Logic split across `crates/ritual/block-verification/src/lib.rs` and `crates/ritual/block-verification/src/nonce_lock.rs`. |
| `crates/ritual-async-registry/src/lib.rs` | `crates/ritual/async-registry/src/lib.rs` |
| `crates/ritual-async-inspector/src/inspector.rs` | `crates/ritual/async-inspector/src/inspector.rs` |
| `crates/ethereum/payload/src/lib.rs` (as ritual async builder) | **Ritual logic lifted out.** That file is now a vanilla Ethereum builder. The ritual builder lives in `ritual-reth-nodebuilder-internal/crates/node/src/payload.rs`. |

The single largest structural change is the third row from the bottom: there is no longer a
single `verifier.rs` file owning duplicate-sender / wallet checks, and the last row: the most
common file cited in the old plan (`crates/ethereum/payload/src/lib.rs`) no longer hosts the
ritual async pipeline at all.

## Claim Audit

Status legend:

- **STILL TRUE**: code still works the way the docs describe.
- **CHANGED PATH ONLY**: behavior same, file or symbol moved.
- **CHANGED BEHAVIOR**: code now does something different.
- **NO LONGER EXISTS**: the named code is gone.
- **NEW STRUCTURE**: the concept exists but in a layout the docs do not describe.

### Detector and async result

1. *Detector "Step 10" derives `sender_address` from `scheduled_tx.caller`,
   `settlement_tx.user_address`, or `transaction.recover_signer()`.*
   **STILL TRUE.** `crates/ritual/async/src/detector.rs:1458-1471` still does exactly this and
   passes the result into `AsyncCallResult::new(...)` at `:1483-1491`. `caller_address` from the
   inspector is logged near `:1134` but not consulted for ownership.

2. *`AsyncCallResult::new(...)` exists and takes a derived sender.*
   **STILL TRUE.** `crates/ritual/async/src/detector.rs:687-708`. The first thing the constructor
   does is hand `sender_address` into `Self::create_commitment_tx(...)`.

3. *`AsyncCallResult` has no `job_sender` field.*
   **STILL TRUE.** Struct definition at `crates/ritual/async/src/detector.rs:663-678`. A repo-wide
   grep finds no `job_sender` or `msg_sender` field anywhere in `ritual-reth-internal`.

4. *Inspector exposes `BasicAsyncCallResult.caller_address`.*
   **STILL TRUE (path moved).** `crates/ritual/async-inspector/src/inspector.rs:119-130` defines
   the struct; `:205` sets `caller_address = Some(inputs.caller)` on the first matching async
   precompile call.

5. *`simulate_for_rpc_validation(...)` exposes both `caller_address` and a transaction-level
   `sender`.*
   **STILL TRUE.** `crates/ritual/async/src/detector.rs:194-208` defines `RpcSimulationResult`
   with both fields; the function at `:230-242` populates `sender` via `scheduled_caller(...)
   .unwrap_or_else(|| transaction.signer())`, not from `caller_address`.

6. *`RpcSimulationResult` type exists.*
   **STILL TRUE.** Same location as claim 5.

### Wallet

7. *`check_user_wallet_balance(...)` and `check_user_wallet_balance_with_provider(...)` exist.*
   **STILL TRUE (path moved).** `crates/ritual/async/src/wallet.rs:41-80`.

8. *Wallet charges scheduled caller, async-settlement `user_address`, otherwise signer.*
   **STILL TRUE.** `crates/ritual/async/src/wallet.rs:91-101`:

   ```text
   let user_address = if let Some(caller) = crate::detector::scheduled_caller(tx) {
       caller
   } else if let Some(user_address) = crate::detector::async_settlement_user_address(tx) {
       user_address
   } else {
       tx.signer()
   };
   ```

   The function does not read `async_result` for ownership, because there is no
   `async_result.job_sender` to read.

9. *`ritual_async_fees::wallet::verify_wallet_for_commitment(...)` exists and is called from
   these.*
   **STILL TRUE.** Defined at `crates/ritual/async-fees/src/wallet.rs:126`, re-exported at
   `crates/ritual/async-fees/src/lib.rs:49`, and called from
   `crates/ritual/async/src/wallet.rs:119-125`.

10. *Heartbeat bypass exists in the wallet validation path.*
    **STILL TRUE, but the bypass lives at call sites, not inside `wallet.rs`.**
    - Builder side: `ritual-reth-nodebuilder-internal/crates/node/src/payload.rs:2016-2025`
      skips the wallet check when `is_heartbeat_tx`.
    - Verifier side: `crates/ritual/block-verification/src/lib.rs:1108-1122` only runs
      `verify_wallet_for_commitment` when `!is_heartbeat_commitment`.

### Payload builder

11. *`crates/ethereum/payload/src/lib.rs` has a `seen_senders` dedup set in the async collection
    path.*
    **NO LONGER EXISTS (in this crate).** `crates/ethereum/payload/src/lib.rs` in
    `ritual-reth-internal` is now a roughly 495-line vanilla Ethereum builder with no
    `seen_senders`, no `detect_async`, and no async collection. Per-block commitment dedup now
    lives in:
    - `crates/ritual/block-verification/src/lib.rs:1059-1087` (verifier pre-exec)
    - `ritual-reth-nodebuilder-internal/crates/node/src/rpc.rs:2152-2177` (RPC post-exec)

    Builder-side per-block `seen_senders` is **not** present in the nodebuilder async collection
    path (`payload.rs:~4580-4757`).

12. *`seen_senders.contains/insert` use transaction-derived sender, not `job_sender`.*
    **CHANGED BEHAVIOR for builder; STILL TRUE for verifier.** Where dedup still happens, it
    still uses the metadata rule. Verifier:

    ```text
    crates/ritual/block-verification/src/lib.rs:1073-1087
    let sender = reth_ritual_async_fees::extract_commitment_sender(&original_tx)...;
    seen_senders.insert(sender, *tx.tx_hash());
    ```

13. *`job_exists_and_active(...)` runs in the async post-filter.*
    **CHANGED BEHAVIOR.** It is no longer the partner of a builder-side `seen_senders` dedup.
    The current builder uses `canonical_async_job_active(...)` to prune duplicate originals from
    the pool (`ritual-reth-nodebuilder-internal/crates/node/src/payload.rs:2724-2747`, called at
    `:4222` and `:5029`). The verifier still calls `job_exists_and_active(...)`-style logic
    inside `verify_async_commitments_pre_execution` at
    `crates/ritual/block-verification/src/lib.rs:1090-1095`.

14. *Phase 1 settlement `user_address` is derived from scheduled / original tx metadata, not
    `contract_job.sender`.*
    **CHANGED BEHAVIOR.** Current Phase 1 builder explicitly uses `contract_job.sender`:

    ```text
    ritual-reth-nodebuilder-internal/crates/node/src/payload.rs:2323-2331
    let settlement_tx = TxAsyncSettlement::new(
        ...
        contract_job.sender,
        ...
    );
    ```

    `contract_job` is read from `read_jobs_for_settlement(...)` at `:3408-3478`, which pulls
    `Job.sender` from on-chain storage. This is what the original docs proposed as the durable
    target, partially in place already.

15. *Phase 2 settlement same property.*
    **CHANGED BEHAVIOR.** Phase 2 `create_delivery_settlement_transaction` uses
    `contract_job.sender` at `payload.rs:2691` and in the ABI encoding at `:2666`.

### Verifier and fees

16. *`crates/ritual-block-verification/src/verifier.rs` verifies duplicate-sender and wallet rules
    via `extract_commitment_sender(...)`.*
    **NEW STRUCTURE.** `verifier.rs` no longer exists. The work is now split:
    - `crates/ritual/block-verification/src/lib.rs:1051-1128` defines
      `verify_async_commitments_pre_execution`, which does duplicate-sender + wallet via
      `extract_commitment_sender` and `verify_wallet_for_commitment`.
    - `crates/ritual/block-verification/src/nonce_lock.rs:17+` defines `verify_nonce_locks`,
      which does its own duplicate-sender bookkeeping but uses `original_tx.sender()` for
      non-scheduled commitments (`:43-52`) and skips scheduled commitments outright (`:38-40`).

    Net effect for the plan: there are now two verifier surfaces that need to agree with the
    builder after the detector change, not one.

17. *`extract_commitment_sender(...)` mirrors the metadata-based sender rule.*
    **STILL TRUE.** `crates/ritual/async-fees/src/wallet.rs:508-528`:

    ```text
    OriginalTransaction::Scheduled(signed)         => signed.tx().caller
    OriginalTransaction::AsyncSettlement(signed)   => signed.tx().user_address
    // other variants fall through to recovered signer
    ```

### Settlement and registry

18. *`SettlementData` is defined in async-registry and currently has "stored sender" comments.*
    **STILL TRUE (path moved).** `crates/ritual/async-registry/src/lib.rs:126-155`. Field
    documented as "Read from contract slot `+8` (`Job.sender`)". Populated by storage reads at
    `:231-289`.

19. *`contract_job.sender` exists as authoritative stored sender.*
    **STILL TRUE.** The field is `SettlementData.sender`. Consumed in nodebuilder settlement
    builders at `payload.rs:2301`, `:2331`, `:2666`, `:2691`. Caveat: the on-chain `Job.sender`
    is itself written from `sender_address` at commitment time
    (`crates/ritual/async/src/detector.rs:774-783`), so today it reflects the metadata-derived
    sender. Settlement consumption is already aligned with the intended fix; only the value
    written at `addJob`-time needs to change.

## Additional Findings

### A. What replaced `verifier.rs`

`crates/ritual/block-verification/src/lib.rs` is the new pre/post-exec verifier and contains:

- `mod nonce_lock` (`:36`)
- Pre-exec entry `verify_pre_execution_block` (`:91`) which calls
  `verify_async_commitments_pre_execution`, `verify_settlement_payments_pre_execution`,
  `verify_nonce_locks`, scheduled/SPC verifiers.
- Post-exec entry `verify_post_execution_block` (`:137`).
- Helpers `verify_spc_calls`, `verify_settlement_payments*`, `verify_scheduled_*`, etc.

Duplicate-sender enforcement for commitments lives in `verify_async_commitments_pre_execution`
(`:1051-1087`) using `extract_commitment_sender`. Wallet enforcement for commitments lives in
the same function (`:1112-1122`), with heartbeat bypass. Nonce-lock dedup is its own pass in
`nonce_lock.rs:verify_nonce_locks` and is rule-asymmetric: scheduled commitments skipped,
others keyed on `original_tx.sender()` rather than `extract_commitment_sender`.

### B. Sender logic inside `crates/ritual/async-fees/`

| Symbol | Where | Role |
|---|---|---|
| `extract_commitment_sender` | `wallet.rs:508` | Reconstruct billed sender from embedded `OriginalTransaction` |
| `verify_wallet_for_commitment` | `wallet.rs:126` | Balance / lock check against a passed-in `user_address` |
| Re-exports | `lib.rs:49` | `extract_commitment_sender`, `verify_wallet_for_commitment` |

No `job_sender` / `msg_sender` / `caller_address` handling in async-fees.

### C. End-to-end async detection today

1. Inspector (`crates/ritual/async-inspector/src/inspector.rs:205`):
   `caller_address = Some(inputs.caller)` on the first matching async precompile call.
2. Detector (`crates/ritual/async/src/detector.rs`, `detect_async_transaction_with_provider`
   around `:911`): runs inspector, then Step 10 builds `AsyncCallResult` with tx-metadata
   `sender_address` (claim 1), ignoring `basic_result.caller_address`.
3. Commitment construction (`detector.rs:774-783`): emits `addJobCall { sender: sender_address,
   ... }`.
4. Builder pre-flight (nodebuilder): `detect_async_transaction_with_provider` →
   `execute_detected_async_commitment` → `check_user_wallet_balance_with_provider` (tx-metadata
   user, claim 8).

No new explicit `job_sender` field landed during the refactor.

### D. Ritual payload sections in nodebuilder

The "old" `crates/ethereum/payload/src/lib.rs` content moved here:

| Section | Function / region | Approx lines |
|---|---|---|
| Main build entry | `default_ritual_payload` | `:2886+` |
| Phase 1 fulfillment + settlement loop | fulfilled-async prep | `:3220-3710` |
| Phase 1 settlement tx | `create_settlement_transaction` | `:2208-2350` |
| Phase 2 delivery settlement tx | `create_delivery_settlement_transaction` | `:2547-2711` |
| Phase 2 inclusion loop | delivery-ready loop | `:3726-3897+` |
| Async collection / post-filter | parallel sim + `payload_async_collection_subsection_combined_post_filter` | `:4580-4757` |

Settlement `user_address` sourcing in both phases: `contract_job.sender` from `SettlementData`
(read via `read_jobs_for_settlement`).

### E. RPC validation surfacing

- `RpcSimulationResult` still carries both `caller_address` and `sender`
  (`detector.rs:194-208`), distinct fields.
- `simulate_for_rpc_validation` / its generic variant: still present (`:230`, `:249`).
- Node-side RPC wallet validation in `ritual-reth-nodebuilder-internal/crates/node/src/rpc.rs`
  consumes `result.sender` (`:1227-1228`); the `sender` passed into simulation is
  `recovered.signer()` (`:1269-1275`), while the wrapper inside detector populates `sender` via
  `scheduled_caller` OR signer (`detector.rs:241-242`). This is the same misleading double-meaning
  the original docs called out: `sender` here is transaction-level, never `caller_address`.

### F. Partial move toward `msg.sender` semantics?

No ownership branch has been switched onto `caller_address`. The field is captured, surfaced on
RPC, and logged for diagnostics; commitment ownership, wallet billing, and verifier dedup all
still use transaction-metadata senders. The one place where the docs' proposed semantics already
land is **settlement consumption**: nodebuilder reads `contract_job.sender` (= on-chain
`Job.sender`) rather than reconstructing from original-tx metadata. That is necessary but not
sufficient, because the on-chain `Job.sender` is written from the same metadata-derived
`sender_address` at `addJob` time.

## Bottom Line

The refactor moved code around without fixing the bug:

- The path of every claim has changed, sometimes meaningfully (`verifier.rs` is gone, ritual
  payload moved repos).
- The core attribution rule is still transaction-derived: detector Step 10 → commitment →
  on-chain `Job.sender` → settlement consumption.
- Settlement now uses `contract_job.sender` end-to-end, which makes implementation-plan chunk 5
  partially done — the only remaining fix in that chunk is the value that *enters* `Job.sender`
  at commitment time, which is also what chunks 1, 2, 4 are about.
- The plan must absorb two new realities for chunks 3 and 4: builder-side `seen_senders` dedup
  no longer exists in `ethereum/payload`, and verifier dedup is now split across `lib.rs`
  (commitments) and `nonce_lock.rs` (nonce locks) with subtly different sender rules. Builder /
  verifier symmetry now means three call sites have to agree, not two.
- RPC surfacing is unchanged: `RpcSimulationResult` still exposes both names; renaming work
  must touch both `detector.rs` and at least one nodebuilder RPC consumer.
