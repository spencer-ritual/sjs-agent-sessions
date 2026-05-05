# PT1 Sad Springboard Validity-Constraint Audit

## Task

Re-check the PT1 sad-path and prior validity-constraint hypotheses against the current `dev` branch code, rather than treating the older PT1 analysis as current. The goal is to decide which issues are still real, which are stale or already fixed, and whether the current code suggests new categories of validity-constraint problems.

## Source Of Truth

- Current Reth checkout: `/home/ritual/repos/ritual-reth-internal`
- Current branch: `dev`
- Current observed commit: `851b51500` / `origin/dev`
- Contract checkout for cross-checks: `/home/ritual/repos/ritual-sc-internal` on `dev`

The older PT1 docs in `/home/ritual/repos/sjs-agent-sessions/pt1-sad-path` are hypothesis sources only. Any candidate from those docs needs current-code verification before being treated as live.

## Current Summary

Current `dev` still has several live validity-constraint concerns from the old PT1/validity audit themes. The highest-signal confirmed issue is async commitment coverage: the verifier validates commitments that exist, but does not appear to require commitments for every in-block async precompile call. Other live categories are admission-only validation, builder/verifier timeout-policy asymmetry, purity-only inclusion checks for delivery and heartbeat/revival work, runtime-env consensus parameters, and duplicated semantic classification.

The most useful new categorization is:

- **Admission-only validation:** RPC/pool/shared validation rejects something, but direct block verification does not replay the same rule.
- **Purity-only validation:** verifier checks protocol txs if present, but does not require them when chain-visible obligations exist.
- **Builder-local escape hatch vs verifier hard rule:** builder can skip or degrade a rule under local deadline/cap policy, while verifier still enforces it unconditionally.
- **Local runtime knob with consensus effect:** env/config affects block validity, fee math, contract address reads, or deterministic execution.
- **Semantic classification drift:** addresses are centralized, but downstream code still reimplements precompile-family membership or ABI offsets.

## What I Am Checking

- Async commitment coverage: whether in-block async precompile calls, including nested calls from delivery callbacks, must have matching commitments in the verifier.
- Async payload validation parity: whether RPC, pool, builder, verifier, and contract paths enforce the same payload shape, size, TTL, deadline, and precompile-family rules.
- Settlement and async FSM edges: expired settlements, non-existent jobs, timeout/refund inclusion, phase-2 deadline interactions, multi-settlement atomicity, and fee overflow or accounting drift.
- System transaction validity: scheduled, heartbeat, revival, settlement, and commitment transaction sender/signature/value/gas-accounting rules.
- Builder/verifier inclusion gaps: cases where the builder is expected to include protocol work but the verifier only validates it if present.
- Hidden consensus parameters: env vars, local runtime knobs, deadlines, caps, and addresses that affect block validity or deterministic execution.
- New categorization candidates: especially "constraint enforced in one path but not another path," "builder-only inclusion expectation," "admission-only validation," and "stale/dead audit surface."

## Current Working Categories

- Validity gap: invalid protocol transaction can be included and still pass block verification.
- Inclusion gap: required protocol work can be omitted because the verifier only checks purity when present.
- Consistency gap: builder, verifier, RPC, contract, or executor paths enforce different rules.
- Global block correctness gap: validity depends on relationships across the whole block, not one transaction in isolation.
- Determinism gap: native execution, timeouts, env config, or floating-point behavior can make honest nodes disagree.
- Surface-area gap: dead or pre-production code remains reviewable enough to generate findings but is not clearly removed or de-scoped.

## Running Notes

- Confirmed before this pass: `/home/ritual/repos/ritual-reth-internal` is on `dev...origin/dev` at `851b51500`.
- Doc-by-doc PT1 verification is now split across:
  - `/home/ritual/repos/sjs-agent-sessions/pt1-sad-path/static-analysis-findings.html`
  - `/home/ritual/repos/sjs-agent-sessions/pt1-sad-path/precompile-sad-paths.html`

## Current-Code Findings

### Finding 1 - Async commitment coverage gap still appears real

**Status:** confirmed in current `dev` by code read.

**Category:** inclusion gap / global block correctness gap / builder-verifier asymmetry.

**Evidence:**

- `crates/ritual-block-verification/src/verifier.rs::verify_block_concrete()` runs `verify_async_commitments()` as Phase 1, then settlement, SPC, scheduled, nonce-lock, sequencing-rights, and scheduled-censorship checks. There is no visible phase that scans every non-commitment transaction for async precompile calls.
- `crates/ritual-block-verification/src/verifier.rs::verify_async_commitments()` loops over block transactions and only enters validation when `tx.as_async_commitment()` is present.
- `crates/ritual-async-commitment-validator/src/lib.rs::validate_commitment_with_state()` re-simulates the origin transaction for an existing commitment and requires the detected precompile/input to match. That is a purity check for commitments that are present, not a coverage check for async calls whose commitments were omitted.
- `crates/ethereum/payload/src/lib.rs` still has builder-side async detection and commitment construction paths for regular/scheduled transactions and async settlement/nested callback cases.

**Why it matters:**

Issue `#353` still looks relevant on current `dev`: a proposer can potentially include a transaction that calls an async precompile while omitting the matching `TxAsyncCommitment`, because the verifier validates commitments if present but does not appear to derive the set of required commitments from the whole block.

**Next verification:**

- Build or find a direct block test where a regular tx calls an async precompile but the matching commitment is omitted.
- Repeat for a delivery callback that calls an async precompile.
- Check whether any newer execution-layer hook outside `ritual-block-verification` already rejects this before `verify_block_concrete()`; I have not seen one yet.

### Finding 2 - Async payload validation is still stronger at RPC/shared admission than in verifier

**Status:** confirmed as a current-code drift pattern; exact exploitability depends on precompile behavior under malformed inputs.

**Category:** admission-only validation / constraint in one path but not another.

**Evidence:**

- `crates/ritual-async/src/validation.rs::validate_async_payload()` performs precompile-specific validation: HTTP URL scheme, LLM model/messages, Sovereign Agent prompt/model/type and deadline bounds, Persistent Agent model, DKMS owner, and media/FHE base decoding.
- `crates/rpc/rpc/src/async_tx_validator.rs::validate_async_payload()` delegates to that shared validator.
- `crates/ritual-block-verification/src/verifier.rs::verify_async_commitments()` does not call `validate_async_payload()`; it checks commitment structure, wallet/lock, selected phase-2 deadline rules, and re-simulation equality.
- `crates/ritual-async-commitment-validator/src/lib.rs::validate_commitment_with_state()` checks that re-simulation detects the same precompile address and input as the commitment. It does not apply the RPC/shared semantic validator to the detected input.

**Why it matters:**

Some checks may be intended as mempool hygiene, but if any are protocol validity rules then direct block verification can be weaker than RPC admission. This is the clearest new category from the current pass: **admission-only validity**. The audit question should be: for each RPC/shared payload check, is it merely local admission hygiene, or must it be replayed by block verification?

**Next verification:**

- For each precompile family, construct direct-block commitments that bypass RPC with payloads rejected by `validate_async_payload()` and see whether the verifier accepts.
- Start with simple cases: invalid HTTP URL scheme, empty LLM model/messages, unsupported Sovereign Agent type, zero DKMS owner.

### Finding 3 - Two-phase deadline extraction still has fail-open shape when extraction returns `None`

**Status:** confirmed fail-open shape in current Reth and contract code; exploitability still depends on whether malformed inputs can reach accepted commitment/settlement paths.

**Category:** malformed-input validity gap / consistency gap.

**Evidence:**

- `crates/ritual-block-verification/src/verifier.rs::is_two_phase_precompile()` includes long-running HTTP, ZK, FHE, Sovereign Agent, Image, Audio, Video, and Persistent Agent.
- `crates/ritual-block-verification/src/verifier.rs::extract_phase2_deadline()` returns `None` when input is too short or conversion fails.
- In `verify_async_commitments()`, the deadline checks are inside `if let Some(phase2_offset) = extract_phase2_deadline(...)`; if extraction returns `None`, the verifier does not reject.
- `crates/rpc/rpc/src/async_tx_validator.rs::validate_two_phase_deadline()` also returns `Ok(())` when shared deadline extraction returns `None`.
- `crates/ritual-async/src/detector.rs` validates deadline offsets for long-running HTTP, Sovereign Agent, ZK, and Persistent Agent when extraction succeeds. I have not yet seen equivalent detector-side checks for FHE/Image/Audio/Video, even though the verifier classifies them as two-phase.
- `ritual-sc-internal/src/async/AsyncJobTracker.sol::_extractPhase2Deadline()` returns `0` when `input.length < minLength`, and `markPhase1Settled()` only checks `phase2DeadlineOffset <= MAX_PHASE2_DEADLINE_OFFSET`. It does not require the offset to be extractable or greater than TTL.

**Why it matters:**

The comments say malformed two-phase input should fail closed, but current code paths still look like "validate only if extraction succeeds." This may be harmless if ABI decoding or precompile execution always fails before a commitment can be accepted, but that needs direct verification rather than assumption.

**Next verification:**

- Cross-check `ritual-sc-internal/src/async/AsyncJobTracker.sol` deadline extraction semantics on current `dev`.
- Test malformed/short inputs for each two-phase family and see whether builder, verifier, and contract all reject for the same reason.
- Pay special attention to FHE/Image/Audio/Video because current builder-side detector deadline checks appear narrower than verifier two-phase classification.

### Finding 4 - Sequencing-rights skip asymmetry still appears present

**Status:** confirmed current-code asymmetry; needs reproduction to determine how reachable under normal block building.

**Category:** consistency gap / builder-only timeout policy vs verifier hard rule.

**Evidence:**

- `crates/ethereum/payload/src/lib.rs` can skip sequencing-rights reordering when `build_policy.should_skip(WorkClass::SequencingRights)` is true or when the global build deadline is exceeded. In that case it logs that it is using tip-sorted order.
- `crates/ritual-block-verification/src/verifier.rs::verify_block_concrete()` always calls `verify_sequencing_rights()` unless `SKIP_VALIDITY_CONSTRAINTS` is enabled.
- `verify_sequencing_rights()` has no corresponding deterministic "builder was allowed to skip SR" acceptance condition. It reclassifies each tx and enforces monotonic priority per contract.

**Why it matters:**

This is the cleanest example of a "constraint in one path but not another path" category, but in reverse: the verifier enforces a hard constraint while the builder has a local timeout/policy escape hatch. If the builder actually emits a block after skipping SR and that block is not already priority-ordered, honest verifiers should reject it.

**Next verification:**

- Determine whether `build_policy.should_skip(SequencingRights)` or the global deadline can be reached in production-like payload building.
- Add a stress or unit test that forces SR skipping with two transactions that require SR reordering and confirms whether the produced block fails verification.
- Decide policy: either SR is hard-required and the builder must miss the slot instead of skipping, or skip acceptance must be a deterministic verifier rule.

### Finding 5 - Phase 2 delivery/settlement inclusion remains purity-only

**Status:** confirmed current-code shape; policy decision needed on whether any delivery or timeout/refund work is consensus-required.

**Category:** inclusion gap / optional-builder-work boundary.

**Evidence:**

- `crates/ritual-block-verification/src/verifier.rs::verify_settlement_payments()` returns `Ok(())` when there are no `TxAsyncSettlement` transactions in the block. It validates settlement jobs that are present, including parent-state job existence and expiry, input hash, phase-1 adjacency, and fee correctness.
- `crates/ethereum/payload/src/lib.rs` Phase B and Phase C collect fulfilled async and delivery-ready transactions from local pool state. Both phases can skip due build policy, global deadline, caps like `RETH_MAX_FULFILLED_ASYNC_PER_BLOCK` / `RETH_MAX_DELIVERY_PER_BLOCK`, missing pool metadata, stale contract state, expiry, or settlement construction failure.
- For delivery callbacks that trigger nested async, the builder attempts to create and execute a nested commitment. If that nested commitment cannot fit or execute, the code falls through to direct delivery execution, which is another instance of the async commitment coverage problem in Finding 1.

**Why it matters:**

The verifier currently treats delivery settlements as valid-if-present. That may be correct for executor-produced off-chain results, because availability is not purely chain-visible. But any chain-visible timeout/refund obligation after `expiryBlock`, or any expected phase transition that is deterministic from `AsyncJobTracker`, needs an explicit policy decision. Otherwise "builder skipped protocol work" remains indistinguishable from "no deliverable work existed."

**Next verification:**

- Confirm whether there is any on-chain timeout/refund settlement path for expired phase-2 jobs. I have not found one yet in this pass.
- If timeout/refund is intended, define a scheduler-style inclusion rule derived from `AsyncJobTracker` state.
- If delivery is intentionally best-effort/off-chain-availability dependent, document that it is not a validity constraint and keep verifier checks purity-only.

### Finding 6 - Heartbeat/revival inclusion gaps still appear present

**Status:** confirmed current-code shape; exact desired policy still needs product/protocol decision.

**Category:** inclusion gap / purity-only system transaction validation.

**Evidence:**

- `crates/ritual-block-verification/src/verifier.rs::verify_scheduled_transactions()` bifurcates heartbeat-routed scheduled txs and validates CH2-CH9 when heartbeat txs are present.
- Current CH checks include dummy signature, zero value, valid calldata, `checkAndRevive` system caller, at most one `checkAndRevive`, `checkAndRevive` only when `shouldCheck()` is true, `reviveAgent` target state/caller, and ordering.
- I do not see a verifier rule requiring `checkAndRevive` to be present when `heartbeat_has_agents()` or a stronger "expired agents exist" predicate is true.
- I also do not see a verifier rule requiring `reviveAgent` txs for FAILED agents. `reviveAgent` is validated if present, but omitted revivals are not rejected.
- `crates/ethereum/payload/src/lib.rs` builder code still treats heartbeat/revival as builder-injected work that can be skipped due thresholds, probabilistic skip, transaction cap, or build policy.

**Why it matters:**

This is the same problem type as scheduled anti-censorship, but for heartbeat/revival work: verifier checks "if present, must be valid," not "if due, must be present." If agent liveness/revival is intended to be protocol-guaranteed rather than best-effort builder behavior, current `dev` still needs a type-2 inclusion constraint.

**Next verification:**

- Decide the actual inclusion predicate: `shouldCheck()` alone, expired monitored agents, FAILED agents, or a gas/cap-bounded subset.
- Re-check current canonical revival executor selection. Prior notes suggest the old issue text was stale about `AUTONOMOUS_AGENT`; current canonical path may use HTTP-capable executors.
- If inclusion is required, model it after `verify_scheduled_censorship()` with explicit gas/cap carve-outs.

### Finding 7 - Consensus-critical parameters are still runtime-env configurable

**Status:** confirmed current-code pattern.

**Category:** determinism gap / hidden consensus parameter.

**Evidence:**

- `crates/ritual-async-inspector/src/lib.rs::max_ttl_blocks()` reads `ASYNC_MAX_TTL_BLOCKS` and explicitly notes all validators must use the same value.
- `crates/ritual-scheduled-verification/src/lib.rs` reads `SCHEDULER_ADDRESS`, `RITUAL_WALLET_ADDRESS`, `SYSTEM_ACCOUNT_ADDRESS`, and `AGENT_HEARTBEAT_ADDRESS`.
- `crates/ritual-async-registry/src/lib.rs` reads `ASYNC_JOB_TRACKER_ADDRESS` and `TEE_SERVICE_REGISTRY_CONTRACT_ADDRESS`.
- `crates/ritual-block-verification/src/verifier.rs` reads `SKIP_VALIDITY_CONSTRAINTS`, `MODEL_REGISTRY_CONTRACT_ADDRESS`, and `TEE_SERVICE_REGISTRY_CONTRACT_ADDRESS`.
- `crates/ethereum/payload/src/lib.rs` reads builder caps and deadlines such as `RETH_MAX_ASYNC_SIMS_PER_BLOCK`, `RETH_MAX_FULFILLED_ASYNC_PER_BLOCK`, `RETH_MAX_DELIVERY_PER_BLOCK`, `RETH_MAX_TRANSACTIONS_PER_BLOCK`, heartbeat/revival skip knobs, and build-policy timing knobs.

**Why it matters:**

Some env vars are clearly builder-local or operational. Others directly affect block validity, contract address reads, fee calculation, TTL acceptance, or whether verification is bypassed. Those should be chain/fork config, not process-local environment. The useful category is: **local runtime knob with consensus effect**.

**Next verification:**

- Inventory each env var into one of: consensus-critical, builder-local policy, observability-only, or dev/emergency bypass.
- Move consensus-critical values to chain config or hard fork config.
- Add a startup lint that rejects production mode if consensus-critical env overrides are set.

### Finding 8 - Precompile address centralization improved, but classification is still partly duplicated

**Status:** partially stale old concern; current code has improved centralization but still has local classification logic.

**Category:** consistency gap / duplicated source of truth.

**Evidence:**

- `crates/ritual-precompile-addresses/src/lib.rs` now provides canonical constants plus `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES`, `ALL_TWO_PHASE_PRECOMPILE_ADDRESSES`, and `is_two_phase_precompile()`.
- `crates/ritual-block-verification/src/constants.rs` re-exports those address constants.
- However, `crates/ritual-block-verification/src/verifier.rs::is_two_phase_precompile()` still manually enumerates the two-phase set instead of using `ritual_precompile_addresses::is_two_phase_precompile()` or the canonical list.
- `crates/ritual-async/src/detector.rs` still has per-precompile branching for deadline extraction/validation that does not obviously cover every address in the verifier's two-phase set.

**Why it matters:**

The old "duplicated address lists" finding is partly improved, but the audit category remains valid: **central constants are not sufficient if semantic classifications are manually reimplemented downstream**.

**Next verification:**

- Replace local two-phase classification with the canonical `ritual-precompile-addresses` helper where practical.
- Build a matrix test that compares detector, verifier, RPC validation, contract `isLongRunning`, and address crate two-phase membership for every async precompile.

### Finding 9 - Same-block nonce lock may not account for commitments created in the same block

**Status:** confirmed current-code concern; needs policy decision and adversarial block test.

**Category:** global block correctness gap / parent-state-only constraint.

**Evidence:**

- `crates/ritual-block-verification/src/nonce_lock.rs::verify_nonce_locks_internal()` first collects `originating_tx_hashes` from `TxAsyncCommitment` transactions and rejects multiple async commitments from the same sender.
- It then checks non-system transactions against `senderJobs` in parent state. Transactions whose own hash appears in `originating_tx_hashes` are exempt because they are the origin tx for a same-block commitment.
- It does not appear to reject an unrelated regular transaction from sender `S` when the same block also contains an async commitment from sender `S`. If parent state has no pending job for `S`, the unrelated tx passes the parent-state lock check.
- Builder Phase D similarly checks `should_skip_sender_locked_tx()` against parent-state contract storage, not a lock set augmented by commitments already selected into the block.

**Why it matters:**

If the nonce-lock invariant means "once an async commitment is included, that sender cannot include unrelated new transactions until the async job reaches the allowed phase," then same-block commitments should lock later unrelated transactions in that same block. Current code enforces cross-block locks and duplicate same-block commitments, but not this same-block follow-on case.

**Next verification:**

- Decide whether same-block locks are intended. This may be constrained by transaction nonce ordering in common mempool paths, but a malicious proposer can construct blocks directly.
- Add an adversarial block test: commitment for sender `S` plus unrelated non-system transaction from `S` in the same block.
- If the invariant is required, verifier should derive locked senders from parent-state jobs plus same-block commitments, then reject unrelated same-block txs from those senders.

## Chain-Halt Audit Springboard Findings

These findings come from a doc-by-doc current-code re-check of `/home/ritual/repos/sjs-agent-sessions/chain-halt-audit`. Treat the old chain-halt docs as hypothesis sources. The current-code checks were split by source doc across `chain-interaction-notes.md`, `reth-fork-diffs.md`, `misc-flagged-items.md`, `summit-fork-diffs.md`, `summit-panic-audit.md`, `reth-panic-targets.md`, `engine-client-fsm-delta.md`, and `chain-halt-audit.md`.

### Chain-Halt Finding 1 - Ritual block verifier hot-path wiring needs immediate confirmation

**Status:** high-impact uncertainty from current-code read.

**Category:** validity wiring gap / dead verifier risk / block-import correctness.

**Evidence:**

- The engine tree calls `validate_block_post_execution_with_hashed_state()` from `crates/engine/tree/src/tree/mod.rs`.
- The Ethereum payload validator path in `crates/ethereum/node/src/engine.rs` appears to implement only `ensure_well_formed_payload()`.
- The default trait implementation in `crates/engine/primitives/src/lib.rs` returns `Ok(())` for `validate_block_post_execution_with_hashed_state()`.
- The chain-halt doc agent did not find obvious external call sites for `ritual-block-verification::BlockVerifier::verify_block()` or `verify_nonce_locks()` outside the verifier crate.

**Why it matters:**

This can supersede several individual validity findings. If the Ritual block verifier is not wired into the `newPayload` / block import hot path, then rules documented above as verifier-side constraints may be dead on direct block import even if the verifier crate itself is correct.

**Next verification:**

- Trace the exact current `newPayload` path from engine API into post-execution validation and identify whether `verify_block_concrete()` runs for every imported block.
- If it does not run, classify all verifier-only constraints as missing hot-path validity checks.
- If it does run through a different adapter, document that adapter and add a regression test that a block violating a known Ritual constraint is rejected through engine import.

### Chain-Halt Finding 2 - P2P/pool async payload validation may still be weaker than RPC admission

**Status:** still relevant by current-code read.

**Category:** admission-only validation / P2P bypass / validity and availability overlap.

**Evidence:**

- RPC transaction submission calls shared async payload validation through `crates/rpc/rpc/src/eth/helpers/transaction.rs`.
- The transaction-pool validation path in `crates/transaction-pool/src/validate/eth.rs` gates async commitment transaction type support but does not obviously apply the same semantic payload checks to normal origin transactions that call async precompiles.
- Current commitment validation does reject `ttl == 0`, `ttl > max_ttl`, and zero executor address, so the old "zero executor at commitment" concern is stale for commitments.

**Why it matters:**

This is the same problem category as Finding 2 above, but from the chain-halt angle: open P2P or non-RPC propagation can admit malformed or resource-heavy transactions that RPC would reject. If those semantics are protocol rules, they need a shared verifier/pool path rather than RPC-only enforcement.

**Next verification:**

- Build a direct pool/P2P test for a malformed origin transaction targeting an async precompile and compare RPC, pool, builder, and block-import behavior.
- Decide which `validate_async_payload()` checks are consensus validity, mempool hygiene, or local DoS protection.

### Chain-Halt Finding 3 - FHE phase-2 output-size conversion can still panic

**Status:** still relevant chain-halt concern; narrow current-code lead.

**Category:** panic path / ABI conversion / malicious delivery payload.

**Evidence:**

- `crates/ritual-precompile-codecs/src/long_running.rs::extract_fhe_output_size()` still converts a decoded ABI integer with `as_u64()`.
- That conversion can panic when the decoded value is greater than `u64::MAX`.
- The function is used by payload construction and block verification paths for FHE phase-2 delivery handling.

**Why it matters:**

Unlike many stale panic findings, this one still looks like a real non-fallible conversion in a consensus-adjacent path. The likely trigger is malicious or compromised phase-2 delivery bytes, not ordinary phase-1 user calldata.

**Next verification:**

- Replace `as_u64()` with a checked conversion that returns a codec error.
- Audit nearby ABI integer conversions for `as_u64()` / `as_u32()` on decoded untrusted values.
- Add a test with an FHE output-size word greater than `u64::MAX`.

### Chain-Halt Finding 4 - Summit engine-client transport errors are still semantically dangerous

**Status:** still relevant chain-halt / liveness issue.

**Category:** CL/EL state-machine semantics / transport-vs-invalid collapse.

**Evidence:**

- `ritual-summit-internal/types/src/engine_client.rs::RethEngineClient::check_payload()` can map persistent transport failure after reconnect into `PayloadStatusEnum::Invalid`.
- Summit application voting treats any non-valid payload status as a no vote.
- Finalizer execution advances only on valid or syncing; `Invalid` is not handled as a retryable transport condition.
- A separate `RitualEngineClient` path returns `Err` for RPC failures, so engine-client semantics differ across crates.

**Why it matters:**

Execution-invalid payloads and local EL connectivity failures should not necessarily produce the same consensus vote. Treating transport failure as semantic invalidity can create liveness or quorum failures during EL flaps.

**Next verification:**

- Decide whether persistent transport failures should map to `Syncing`, abstain, or a retry/error path.
- Align `RethEngineClient` and `RitualEngineClient` semantics or document why both paths exist.
- Add integration coverage for EL disconnect during `check_payload()`.

### Chain-Halt Finding 5 - Summit `commit_hash` failure policy remains under-specified

**Status:** improved but still relevant.

**Category:** CL/EL agreement / recovery policy gap.

**Evidence:**

- `commit_hash()` now returns `Result`, so the old "no return value" issue is stale.
- Current finalizer paths can log a `commit_hash` error and continue.
- The chain-halt agents did not identify a clear rollback, retry queue, or recovery trigger tied to repeated forkchoice update failures.

**Why it matters:**

If Summit advances CL state while EL forkchoice update failed, CL/EL agreement depends on later recovery behavior. That may be acceptable, but it needs to be an explicit state-machine policy rather than log-only handling.

**Next verification:**

- Define whether `commit_hash` failure should abort finalization, retry, enter recovery, or mark the node unhealthy.
- Add metrics and alerts for repeated `commit_hash` failures.

### Chain-Halt Finding 6 - Summit syncer/finalizer/cache panic paths remain live liveness risks

**Status:** still relevant chain-halt / availability class.

**Category:** process halt / storage and channel failure handling.

**Evidence:**

- `ritual-summit-internal/syncer/src/actor.rs` still has panic paths for storage reads, finalization writes, missing/gapped blocks, and buffer subscriber closure.
- `ritual-summit-internal/syncer/src/cache.rs` still has cache operation panics.
- `ritual-summit-internal/node/src/args.rs` still has checkpoint read/parse and missing EL snapshot panic or `expect` paths.
- `ritual-summit-internal/types/src/engine_client.rs` still unwraps IPC connection at startup.

**Why it matters:**

Most of these are not malicious-block validity bugs, but they are credible node halt risks under storage corruption, restart, local archive inconsistency, EL unavailability, or operational misconfiguration.

**Next verification:**

- Split these into hot runtime paths versus startup/operator paths.
- Replace hot syncer/cache panics with explicit error propagation, retry, safe stall, or recovery.
- Keep startup panics only where process exit is intentionally the clearest operator signal.

### Chain-Halt Finding 7 - Summit finalizer CL/EL advancement needs a focused agreement audit

**Status:** still relevant validity / liveness concern.

**Category:** CL/EL agreement / state advancement after failed EL update.

**Evidence:**

- Chain-halt agents reported that finalizer `execute_block()` can skip EL forkchoice update on withdrawal or parent mismatch while Summit state/head advancement behavior needs close review.
- `finalizer/src/actor.rs` still has an epoch `assert_eq!` after CL state update in the relevant execution flow.
- Withdrawal handling contains invariant `expect` / `assert_eq` style checks that may be unreachable for bad EL payloads but remain important if CL invariants break.

**Why it matters:**

This is not a Reth verifier issue, but it is validity-adjacent: the CL must not finalize or advance state in a way that leaves the EL on a different canonical head without an explicit recovery path.

**Next verification:**

- Build a state-machine trace for valid payload, invalid payload, syncing, transport failure, withdrawal mismatch, and parent mismatch.
- Confirm where CL state/head is mutated relative to EL `newPayload` and forkchoice update.
- Add a regression test for the mismatch path that asserts the intended CL and EL state.

### Chain-Halt Finding 8 - Blocking refunds and scheduler cleanup remain contract-layer liveness leads

**Status:** still relevant availability issues; not direct Reth validity constraints.

**Category:** contract liveness / gas griefing / protocol work availability.

**Evidence:**

- `ritual-sc-internal/src/async/AsyncDelivery.sol::deliver()` calls `RITUAL_WALLET.refundGas()` before `markDelivered()` without an obvious non-blocking fallback.
- `ritual-sc-internal/src/scheduler/Scheduler.sol` stores scheduled call `data` without an obvious `data.length` cap on `_schedule()`, while cleanup still uses bounded batch cleanup and byte wiping.

**Why it matters:**

Refund reverts can block delivery terminal-state marking, and large scheduled calldata can make cleanup expensive enough to threaten scheduler liveness. These are not block-import validity gaps, but they can interfere with protocol progress.

**Next verification:**

- Consider non-blocking refunds: `try/catch`, escrow, or pull-based refunds.
- Model `MAX_CLEANUP_PER_EXECUTE * _wipeBytes` worst-case gas against chain block limits.
- Add a maximum scheduled calldata size if cleanup cost can exceed safe budgets.

### Chain-Halt Finding 9 - Runtime TTL/env parity remains a consensus-configuration foot-gun

**Status:** partially mitigated, still relevant.

**Category:** hidden consensus parameter / env-contract parity.

**Evidence:**

- `AsyncJobTracker.sol` now enforces `ttl >= 1 && ttl <= MAX_TTL_BLOCKS`, so the old "no Solidity bound" claim is stale.
- Reth still reads `ASYNC_MAX_TTL_BLOCKS` through `crates/ritual-async-inspector/src/lib.rs::max_ttl_blocks()`.
- Validators with different env values can disagree about admissible TTLs even when the contract cap is fixed.

**Why it matters:**

This is another instance of local runtime configuration affecting validity. The contract cap helps, but validator-local lower or higher caps can still create acceptance divergence unless the value is chain-configured or startup-validated.

**Next verification:**

- Ensure deployed `AsyncJobTracker.MAX_TTL_BLOCKS`, Reth default `DEFAULT_MAX_TTL_BLOCKS`, and validator env overrides are identical.
- Move TTL to chain/fork config or reject production startup when env overrides do not match configured network values.

### Stale Or Lower-Priority Chain-Halt Findings

- `AsyncJobTracker.onlySettlementSender` using `tx.origin` is stale for the cited pattern; current settlement-style access goes through `AsyncDelivery` and `msg.sender`.
- Multimodal UX `steps` / `fps` panic claims are stale as panic findings; current extraction uses `Result`, bounded reads, and clamp semantics. The ABI shape remains consensus-relevant for pricing/extraction.
- Expired settlement builder/verifier asymmetry is stale as stated; current builder skips expired settlements and verifier rejects expired jobs, with equivalence tests present.
- Several old Reth numeric conversion panics are fixed through checked conversions in async fee and model/LLM decoding paths.
- Production `RethEngineClient` panic-on-EL-error claims are mostly stale; bench or startup paths still have unwraps, but the default client now returns controlled outcomes for many runtime calls.
- Heartbeat registration existence checks and several RwLock poison cases are mostly operational or cosmetic unless the team wants a zero-panic posture for poisoned locks.
