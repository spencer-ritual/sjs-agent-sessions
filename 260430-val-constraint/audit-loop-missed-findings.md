# Validity Constraint Audit Loop - Missed Findings

## Scope

## Original Prompt Shape

The task was: take the proposed "strongest audit loop" and actually apply it to the Ritual
validity-constraint surface, looking for issues that had not already been captured in the prior
matrix/issues. The instruction was explicitly read-only for code: do not edit implementation code
yet, but create a new markdown document in this folder with findings and TODOs.

The reusable prompt pattern was roughly:

> Try to do this audit loop and find issues that were missed so far. Do not edit code yet, but make
> a new markdown doc in `sjs-agent-sessions/260430-val-constraint` with findings/todos.

The inputs were the validity-constraint matrix, GitHub issues 340/352/353, and the manual review
notes in `first-pass.md`.

## How The Loop Was Applied

This is a first application of the audit loop:

1. Enumerate builder behavior and the semantic obligation it creates.
2. Identify the authoritative source of truth.
3. Decide whether the rule belongs in contract, Reth verifier, executor, or docs.
4. Check both directions: purity and inclusion.
5. Search alternate paths: RPC, mempool, builder, scheduled, delivery callback, verifier, replay/import.
6. Kill or explicitly de-scope dead surfaces.

Operationally, I used the loop as a repeated pass over protocol surfaces rather than as one linear
grep:

1. **Builder obligation pass:** read `crates/ethereum/payload/src/lib.rs` and related scheduling /
   async collection paths, then asked what each builder phase is promising the protocol.
2. **Verifier symmetry pass:** checked `crates/ritual-block-verification/src/verifier.rs`,
   `nonce_lock.rs`, scheduled verification, async commitment validation, and sequencing-related
   paths to see whether the verifier independently re-derives or merely trusts those builder
   decisions.
3. **Alternate-path pass:** compared RPC/shared validation, builder detector behavior, mempool/pool
   behavior, contract execution, and verifier/import behavior to find checks that exist in one path
   but not another.
4. **Contract-placement pass:** compared Reth-side assumptions against `AsyncJobTracker`,
   `AgentHeartbeat`, and Scheduler-style contract logic to identify checks that could be moved
   on-chain or need explicit docs.
5. **Duplicate-pruning pass:** filtered out known findings already covered by the microsite/issues,
   such as async commitment coverage, revival inclusion, sequencing-rights skip symmetry,
   scheduled C9/expiry, and broad Nitro/ZK/FHE/media de-scope concerns.

This note intentionally avoids code edits. Items below are candidate findings/TODOs, not final exploit writeups.

## Candidate Findings

### 1. Full async payload validation appears RPC-only, not verifier-enforced

**Confidence:** high

**Category:** validity gap / alternate-path gap

**Observed shape:**

- RPC uses `ritual_async::validation::validate_async_payload()` via `crates/rpc/rpc/src/async_tx_validator.rs` and `crates/rpc/rpc/src/eth/helpers/transaction.rs`.
- That validation checks precompile-specific semantics such as HTTP URL scheme, LLM non-empty model/messages, Sovereign Agent prompt/model/type, DKMS owner, key format-related shape, and basic media/FHE structure.
- Block verification for `TxAsyncCommitment` in `crates/ritual-block-verification/src/verifier.rs` appears to enforce TTL, precompile allowlist, executor non-zero, wallet balance, some Phase 2 deadline checks, active-job uniqueness, and re-simulation equality.
- I did not find a verifier call to the shared `validate_async_payload()` path.

**Why this matters:**

A malicious proposer may be able to include a commitment for a payload that would be rejected at RPC admission but still passes block verification. That turns RPC validation into a local hygiene check rather than a validity rule. Examples to verify:

- HTTP async request with invalid URL scheme.
- LLM async request with empty model/messages.
- Sovereign Agent request with unsupported agent type.
- DKMS request with bad semantic fields.

**Source of truth:** shared ABI/codecs plus protocol-level payload validity policy.

**Likely placement:** Reth verifier. Some checks may also belong in contracts if they can be enforced cheaply from calldata, but verifier is the minimum because commitment validity is currently Reth-mediated.

**TODO:**

- Add negative tests that construct blocks directly, bypassing RPC, with invalid async payloads and matching commitments.
- Decide whether every RPC payload validation is consensus-critical or only admission hygiene.
- If consensus-critical, call a shared validation crate from commitment verification and builder detection.

### 2. Async input-size limit drifts between RPC/shared validation and builder/contract limits

**Confidence:** high

**Category:** consistency gap

**Observed shape:**

- `crates/ritual-async/src/validation.rs` defines `MAX_ASYNC_INPUT_SIZE = 1_048_576` and RPC tests import that value.
- `crates/ritual-async/src/detector.rs` enforces a local `10 * 1024` input/RLP limit before creating a commitment.
- `crates/ritual-async-fees/src/constants.rs` also says async input size is `10 * 1024`.
- `ritual-sc-internal/src/async/AsyncJobTracker.sol` enforces `MAX_INPUT_SIZE = 10 * 1024` in `addJob()`.

**Why this matters:**

The comment in `validation.rs` says the module is shared by RPC and builder, but the effective builder/contract limit is 10KB while RPC validation allows 1MB. This can cause transactions to be admitted or presented as valid by one path but impossible to commit by another. Combined with missing async-commitment coverage, oversized async calls may degrade into “included as regular / no commitment” behavior unless all paths explicitly skip them.

**Source of truth:** `AsyncJobTracker.MAX_INPUT_SIZE` or a chain-config constant mirrored from it.

**Likely placement:** shared constant used by RPC, builder detection, verifier, fee logic, and contract docs.

**TODO:**

- Replace the 1MB shared validation limit or rename it if it is not meant to be the protocol limit.
- Add a verifier-side explicit commitment input/RLP size check matching the contract limit, rather than relying only on `addJob()` execution failure.
- Add a differential test: RPC validation, builder detection, contract addJob, and verifier all agree on 10KB, 10KB+1.

### 3. Two-phase deadline extraction may fail open on malformed/short input

**Confidence:** medium-high

**Category:** validity gap / contract-Reth consistency gap

**Observed shape:**

- `crates/ritual-block-verification/src/verifier.rs` calls `extract_phase2_deadline()` for two-phase precompiles.
- The comment says extraction should fail closed, but the code only validates when `Some(phase2_offset)` is returned.
- If extraction returns `None`, the verifier appears to continue rather than reject.
- `ritual-sc-internal/src/async/AsyncJobTracker.sol::_extractPhase2Deadline()` returns `0` when input is too short.
- `markPhase1Settled()` only checks `phase2DeadlineOffset <= MAX_PHASE2_DEADLINE_OFFSET`, so a malformed/too-short input can collapse to offset `0` at the contract layer.

**Why this matters:**

The intended invariant seems to be:

> two-phase offset must be extractable, greater than TTL, and less than or equal to max offset.

Today the verifier may not enforce extractability, and the contract treats missing offset as zero. That can produce jobs whose Phase 2 deadline is not the one the request was supposed to encode.

**Source of truth:** two-phase ABI layout plus `AsyncJobTracker` deadline semantics.

**Likely placement:** both contract and Reth verifier. Contract should reject malformed two-phase deadline fields if these are protocol-required; verifier should reject `None` extraction for all two-phase precompiles.

**TODO:**

- Confirm whether every precompile marked two-phase must have a deadline field.
- Add tests for malformed/short inputs for HTTP long-running, ZK, FHE, Sovereign Agent, Persistent Agent, Image, Audio, and Video.
- Change verifier semantics from `if let Some(offset)` to fail-closed for two-phase precompiles.
- Consider making `_extractPhase2Deadline()` revert on too-short input instead of returning `0`.

### 4. Builder validates Phase 2 deadline offsets for only a subset of two-phase precompiles

**Confidence:** medium

**Category:** builder/verifier consistency gap

**Observed shape:**

- `crates/ritual-block-verification/src/verifier.rs::is_two_phase_precompile()` includes long-running HTTP, ZK, FHE, Sovereign Agent, Image, Audio, Video, and Persistent Agent.
- `crates/ritual-async/src/detector.rs` explicitly validates deadline offset for long-running HTTP, Sovereign Agent, ZK, and Persistent Agent.
- I did not see equivalent detector-side validation for FHE/Image/Audio/Video, even though verifier and contract classify them as two-phase.

**Why this matters:**

Honest builder selection and verifier acceptance may diverge by precompile family. Even if the verifier eventually rejects bad FHE/media commitments, the builder may waste block-building work or produce invalid blocks. If the verifier fail-open in finding 3 is confirmed, then some malformed FHE/media deadlines may not be rejected either.

**Source of truth:** the two-phase precompile set and ABI deadline offsets.

**Likely placement:** shared two-phase metadata table or shared codec function used by RPC, detector, verifier, and contract tests.

**TODO:**

- Build a matrix of two-phase precompile families vs. RPC validation, detector validation, verifier validation, and contract validation.
- Remove hardcoded duplicated offset logic where possible.
- Add differential tests for each two-phase family.

### 5. Same-block nonce-lock semantics may not account for new commitments created earlier in the block

**Confidence:** medium

**Category:** global block correctness gap

**Observed shape:**

- `crates/ritual-block-verification/src/nonce_lock.rs` checks parent-state pending jobs for non-system transactions.
- It skips the originating tx hash for commitments in the same block and rejects duplicate commitments by sender.
- It does not obviously reject a block containing:
  - a same-block async commitment for sender `S`, and
  - an unrelated non-system transaction from sender `S` in the same block.
- Builder regular collection uses `should_skip_sender_locked_tx()` against a parent-state database, so it also may not see jobs created by same-block commitment execution.

**Why this matters:**

If nonce locking is meant to prevent user follow-up transactions while an async job is pending, then a commitment created earlier in the same block should lock later regular transactions from the same sender. Parent-state-only checks do not capture this. This may be constrained by mempool nonce ordering in common cases, so it needs a focused reproduction rather than immediate classification as exploitable.

**Source of truth:** intended nonce-lock invariant plus block order.

**Likely placement:** verifier global block check and builder collection logic.

**TODO:**

- Write an adversarial block test with an async commitment and a second non-system tx from the same sender in the same block.
- Decide whether same-block locks are required by protocol semantics or only cross-block locks.
- If required, verifier should derive locked senders from both parent-state jobs and same-block commitments, then reject unrelated same-block txs from those senders.

### 6. `reviveAgent` purity checks do not appear to validate the revival payload

**Confidence:** medium-high

**Category:** validity gap / contract-placement issue

**Observed shape:**

- `crates/ritual-block-verification/src/verifier.rs` CH checks validate heartbeat tx signature/value/calldata shape, `checkAndRevive` caller, duplicate check, ordering, agent state, and owner caller.
- For `reviveAgent(agentId, precompileInput)`, CH8 checks the target agent state and caller owner but does not appear to validate that `precompileInput` is the canonical revival request for that `agentId`.
- `crates/scheduling/src/canonical.rs::build_revival_precompile_input()` does construct a canonical request from `agent_id`, `latest_manifest_cid`, and `encrypted_da_config`, and `select_revival_executor()` picks a deterministic HTTP-capable executor.
- `ritual-sc-internal/src/heartbeat/AgentHeartbeat.sol::_attemptRevival()` only extracts the executor from the first word of `precompileInput` and calls the persistent-agent precompile. It does not appear to bind `precompileInput.agent_id`, manifest CID, DA config, or selected executor to the failed assignment.

**Why this matters:**

Issue 352 covers missing inclusion of revival obligations. This is a separate purity issue: even when `reviveAgent` is present, a malicious builder may be able to include a syntactically valid revival for the right failed agent but with arbitrary or stale persistent-agent input.

**Source of truth:** AgentHeartbeat assignment state plus canonical revival input construction.

**Likely placement:** split:

- Contract can likely enforce `precompileInput.agent_id == agentId` if that field is stable and cheaply decoded.
- Reth verifier may need to enforce canonical input construction if it depends on registry executor selection or other global policy.
- Docs should state which fields are contract-enforced vs. Reth-enforced vs. executor-trusted.

**TODO:**

- Confirm canonical revival input fields in `crates/scheduling/src/canonical.rs`.
- Add a negative test: failed agent `A`, `reviveAgent(A, precompileInput for B or arbitrary agent_id)`.
- Decide the minimal contract-level binding worth enforcing.

### 7. Async commitments for reverted/halted origin transactions need an explicit design decision

**Confidence:** medium

**Category:** semantic ambiguity / possible validity gap

**Observed shape:**

- Builder detection in `crates/ritual-async/src/detector.rs` continues inspecting async precompile calls even when EVM simulation returns `Revert` or `Halt`.
- Commitment validation in `crates/ritual-async-commitment-validator/src/lib.rs` re-simulates and checks the inspector result, but does not appear to require the origin transaction simulation result to be successful.

**Why this matters:**

This may be intentional, but it is surprising. In normal EVM semantics, a reverting transaction rolls back state effects. If a transaction calls an async precompile and then reverts, the protocol must decide whether the off-chain job should still be registered. If yes, document it clearly. If no, builder and verifier should require a successful origin simulation before accepting the commitment.

**Source of truth:** protocol semantics for async precompile calls under EVM revert/halt.

**Likely placement:** Reth verifier and builder detector, plus docs.

**TODO:**

- Create a contract that calls an async precompile and then reverts.
- Observe whether the builder emits a commitment and whether verifier accepts it.
- Decide whether this is intended. If intended, document user-visible behavior and fee implications.

### 8. Consensus-critical addresses and limits remain runtime-env configurable; address-migration work exists and should be merged

**Confidence:** medium-high

**Category:** consistency gap / production-hardening TODO / existing work to merge

**Observed shape:**

- `ritual-scheduled-verification` reads `SCHEDULER_ADDRESS`, `RITUAL_WALLET_ADDRESS`, `SYSTEM_ACCOUNT_ADDRESS`, and `AGENT_HEARTBEAT_ADDRESS` from env vars with defaults.
- `ritual-async-inspector::max_ttl_blocks()` reads `ASYNC_MAX_TTL_BLOCKS` from env.
- `BlockVerifier::new()` reads `MODEL_REGISTRY_CONTRACT_ADDRESS` and `TEE_SERVICE_REGISTRY_CONTRACT_ADDRESS` from env/defaults.
- Existing Asana work exists for the contract-address subset: `1212349522094290` ("Migrate Contract Addresses to Chain Configuration"). That task already identifies the model/executor registry address risk and proposes moving protocol addresses into chain configuration.

**Why this matters:**

These are not merely local builder preferences. They affect block validity. If any validator can run with different values, the network can split on otherwise identical blocks.

**Source of truth:** chain config / genesis / fork config, not local process env.

**Likely placement:** chain config with explicit fork activation, plus startup lint that refuses production mode when env overrides are set.

**TODO:**

- Merge the existing chain-config address migration work from Asana task `1212349522094290`.
- Inventory every env var consumed by verifier or shared validity crates.
- Classify each as consensus-critical, builder-local, observability-only, or emergency bypass.
- Extend the address-migration work, if needed, to cover scheduler/wallet/system/heartbeat addresses and non-address validity parameters such as `ASYNC_MAX_TTL_BLOCKS`.

## Strong Non-Issues / Already-Covered Items

- Scheduled `shouldExecute` not being checked in `Scheduler.execute()` is not itself a bug if C11 remains a Reth consensus rule. The docs still need to say this explicitly.
- Async commitment coverage for in-block async calls is already captured by issue 353; this note only adds related edge cases such as payload validity, oversized inputs, revert semantics, and same-block nonce-lock effects.
- Revival inclusion is already captured by issue 352. This note separates the additional `reviveAgent` payload-purity question.
- Broad Nitro/ZK/FHE/media production-readiness concerns are already known. The actionable meta-TODO is to explicitly de-scope or delete dead surfaces.

## Immediate Test Backlog

1. Direct-block invalid HTTP URL commitment: bypass RPC and verify whether block verification rejects.
2. Direct-block empty LLM model/messages commitment.
3. 10KB and 10KB+1 async input differential across RPC, detector, contract, verifier.
4. Short two-phase input where deadline extraction returns `None` / contract offset `0`.
5. FHE/Image/Audio/Video two-phase deadline offset matrix.
6. Same-block commitment plus unrelated regular tx from same sender.
7. `reviveAgent(agentId, precompileInput with mismatched agent_id)`.
8. Async precompile call followed by revert/halt.

