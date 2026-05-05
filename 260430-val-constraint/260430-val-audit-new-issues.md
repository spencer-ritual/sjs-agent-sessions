# 260430 Validity Audit - New Unique Issues

## Overview

This document collects the remaining new issue candidates from the validity-constraints audit of `ritual-reth-internal`. The focus is on rules that should be enforced by block verification, execution, or closely adjacent consensus-critical code, not on general product cleanup or already-tracked work.

In this context, a "validity constraint" means an invariant that every accepted block must satisfy even if the block producer is malicious or bypasses the normal RPC/mempool path. Many of the issues below follow the same pattern: a check appears to exist in one path, such as RPC admission or builder-side construction, but the audit question is whether the same fact is enforced when another node verifies the block.

The list is intentionally narrower than the raw notes. Items that were already covered by the microsite or existing GitHub issues are not repeated unless the notes added a distinct attack shape, a stronger current-code reference, or a follow-up that would otherwise be easy to lose. Summit/chain-halt items and other non-Reth-validity concerns were moved out of this main document so the final list stays focused.

Each issue includes source notes, a confidence/status label, the suspected missing invariant, and why it is distinct from already-covered work. Some entries are confirmed enough to turn directly into implementation or test tasks; others are marked as candidates because they still need a targeted code or localnet check before being treated as production bugs.

The audit uses five working categories:

- **Validity gaps:** a block includes a protocol transaction or side effect that should be invalid.
- **Inclusion gaps:** a required protocol transaction is omitted even though the block had the obligation and capacity to include it.
- **Consistency and determinism gaps:** builder/verifier behavior can diverge, or verification depends on non-deterministic runtime behavior.
- **Global block correctness gaps:** validity depends on the block as a whole, such as forbidding multiple async calls in one transaction or enforcing sequencing rules over global block order.
- **Rule-placement gaps:** a check could plausibly live in the smart contract, Reth verifier, executor, or docs, but the current ownership is unclear or insufficiently justified.

Broad recommendation: for any validity or verification check that could live in a smart contract, prefer moving it on-chain or explicitly document why it remains in Reth or executor code. Custom off-chain verification increases attack surface and audit burden, while on-chain or consensus-level checks are easier to reason about and reuse. Some checks clearly need Reth-level global context, such as "max one SPC per transaction"; others, such as checks against `AsyncJobTracker` metadata, may be better enforced in contracts unless the intended invariant is stronger than "bad delivery cannot mutate state" and instead says "every included protocol delivery must be valid and successful."

## Scope

This file consolidates unique issue candidates from the markdown notes in this folder:

- `first-pass.md`
- `audit-loop-missed-findings.md`
- `pt1-sad-springboard.md`
- `second-pass.md`

I treated the microsite, GitHub issues `340`, `352`, and `353` as prior context. Items already captured there are only included when a later note adds a distinct new angle, a stronger current-code confirmation, or a concrete follow-up that should not be lost.

## Deduping Rules

- If two notes describe the same root issue, keep one entry and list all source notes.
- If one note describes a broader category and another identifies a concrete exploit shape, keep the concrete issue.
- If an item is only an audit method, documentation cleanup, or stale correction, do not list it as a new issue unless it implies a live implementation or protocol risk.
- If an item is still an uncertainty rather than a confirmed bug, keep it as a candidate and mark the required verification.

## Unique New Issue Candidates

### 1. Async precompile jobs use tx-origin-style sender attribution

**Sources:** Asana task [Change precompile auth behavior from tx.origin to msg.sender](https://app.asana.com/1/1206274797081445/project/1212017194493012/task/1213627979634996)

**Reference files:**

- `ritual-reth-internal/crates/ritual-async/src/detector.rs` derives the job sender from the outer transaction envelope before constructing async job data.
- `ritual-reth-internal/crates/ritual-async-commitment-validator/src/lib.rs` re-simulates commitments using the recovered transaction signer or async-settlement system sender, not the call-site `msg.sender`.

**Status:** known security issue / paused implementation task.

The async system currently attributes jobs to a protocol-level sender derived from the transaction envelope, not from `msg.sender` at the precompile call site. For regular transactions, this sender is derived from the transaction signer; for scheduled transactions, it is derived from the scheduled transaction caller; for async-settlement callbacks, it is derived from the settlement user.

The Solidity documentation explicitly warns against this pattern. See the asana task for details. If the suggested change lands, relevant validity constraints will need to update their checks

**Why unique:** This is a source-of-truth issue for who owns or pays for an async job. It is related to the commitment-calldata binding issue below, but it is not the same bug: this issue asks "what should the canonical job sender be?"

### 2. Async commitment calldata is not bound to typed commitment fields

**Sources:** `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-async-commitment-validator/src/lib.rs` checks detected precompile address/input against typed commitment fields.
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` calls commitment structure/state validation but does not decode and bind the executable `addJob(...)` calldata.

**Status:** high-confidence candidate.

This issue starts after issue 1's sender policy is decided. Under the current invariant, the job sender is derived from the transaction signer for regular txs, from the scheduled transaction caller for scheduled txs, and from the settlement user for async-settlement callbacks; if the Asana task lands, that rule may change to `msg.sender` or an explicit delegated owner.

The current validity constraint appears to enforce that the `precompile_input` field of a `TxAsyncCommitment` is correct. The verifier re-simulates the origin transaction, sees the async precompile request `X`, and checks that the commitment's typed `precompile_input` field also says `X`.

The missing check is around the fields that actually make the job land in contract state. A `TxAsyncCommitment` also carries executable calldata received by `AsyncJobTracker.addJob(...)`; if that calldata is not decoded and compared against the typed commitment fields, the verifier may prove that `precompile_input = X` while `AsyncJobTracker` receives calldata for a different job shape.

In plain terms: the validator may correctly verify the commitment's typed `precompile_input`, but still fail to verify the surrounding `addJob(...)` calldata that stores the job. That calldata includes the executor, job id, precompile address, input bytes, TTL, previous-block hash/number/time, sender, fee recipient, origin hash, and origin RLP, so the missing validity constraint should prove that the calldata received by `AsyncJobTracker` matches the canonical values for the commitment.

**Why unique:** This is distinct from issue `353`, which covers missing commitments. This issue is about a commitment that exists, but whose executable side effects may not match the fields the verifier validated.

### 3. Settlement calldata is only partially bound to `AsyncJobTracker` state

**Sources:** `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-async-registry/src/lib.rs` exposes canonical stored job state such as `sender`, input hash, executor, fee, and validator fields.
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` verifies settlement payments and extracts settlement `precompileInput`, but does not bind every settlement calldata field back to stored job state.

**Status:** high-confidence candidate.

This is the settlement-side version of the same "verified facts vs executed calldata" problem. A job is created earlier in `AsyncJobTracker` with canonical stored facts: job id / origin transaction, original input hash, job sender or payer, executor information, expiry, and phase state.

Later, a settlement transaction arrives to settle Phase 1 or deliver Phase 2. The verifier appears to check important facts such as whether the job exists, whether it is expired, whether `keccak256(precompileInput)` matches `job.input_hash`, whether fee amounts are correct, and whether the executor payment address is correct.

The suspected gap is that settlement calldata also controls who pays and what callback executes. For example, the original job may belong to user `U`, while settlement calldata says `user = V`; if the verifier only checks job id, input hash, expiry, fees, and executor address, it may not notice that the settlement is trying to charge or attribute work to `V` instead of `job.sender = U`.

The Phase 2 version is callback mutation. The original async request may encode "when the result arrives, call target `T`, selector `S`, with gas `G`, and value `W`," while the delivery calldata says to call target `T2` or use value `W2`. If the verifier only checks that the supplied `precompileInput` hashes to the stored input hash, but does not decode the delivery config inside that input and compare it to the actual `deliver(...)` calldata, the settlement could deliver the right job with the wrong callback envelope.

In plain terms: the verifier may prove that this settlement belongs to a real job and has the right input hash and fee math, but may not prove that the settlement calldata's user and callback fields match the original job's canonical request.

**Why unique:** This is broader than the microsite coinbase/fee-recipient item. It concerns user billing and callback execution semantics, not only validator fee recipients.

### 4. Coinbase and validator fee recipients appear unbound to block beneficiary

**Sources:** `second-pass.md`, `first-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-async/src/detector.rs` treats the commitment validator as the block proposer's coinbase on the builder side.
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` ties settlements to stored job validator fields but does not bind the commitment validator to the block beneficiary.

**Status:** medium-high confidence candidate; prior microsite item promoted from "needs audit."

The builder uses the payload fee recipient as the commitment validator and Phase 1 inclusion validator, but the verifier may only check that settlements match stored job values and fee amounts. If the original job's validator fields are not bound to the block beneficiary, a proposer may be able to redirect validator-side async fees.

**Why unique:** The microsite listed this as a needs-audit row. `second-pass.md` reports a concrete read that did not find the binding, so this should be tracked as a candidate bug until disproven.

### 5. Full async payload validation appears RPC-only, not verifier-enforced

**Sources:** `audit-loop-missed-findings.md`, `pt1-sad-springboard.md`, `second-pass.md`; related Asana task [Revm Precompiles Should Verify Basic Input Formatting](https://app.asana.com/1/1206274797081445/project/1212017194493012/task/1213531999709377)

**Reference files:**

- `ritual-reth-internal/crates/rpc/rpc/src/eth/helpers/transaction.rs` calls `validate_async_payload(...)` during RPC transaction handling before running fuller async validation.
- `ritual-reth-internal/crates/rpc/rpc/src/async_tx_validator.rs` delegates static payload checks to the shared `ritual_async::validation::validate_async_payload(...)` path.
- `ritual-reth-internal/crates/ritual-async/src/validation.rs` contains the precompile-specific checks, including HTTP URL scheme, empty LLM model/messages, long-running HTTP URL fields, Sovereign Agent prompt/model/deadline fields, Persistent Agent model, and DKMS payload fields.
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` appears to validate async commitments through `validate_commitment_structure(...)` and `validate_commitment_with_state(...)`, but this pass did not find a call to the shared `validate_async_payload(...)` semantic validator in `verify_async_commitments(...)`.

**Status:** high-confidence drift pattern; exploitability depends on which checks are consensus rules.

RPC admission calls shared async payload validation for precompile-specific semantics such as HTTP URL scheme, LLM model/messages, Sovereign Agent fields, DKMS fields, and base media/FHE shape. Commitment verification appears to check structural commitment properties and re-simulation equality, but does not call the same semantic payload validator.

**Why unique:** This is an alternate-path issue: a direct block can bypass RPC admission. It should be classified check-by-check into consensus validity, mempool hygiene, or local DoS policy.

### 6. P2P and pool async payload validation may be weaker than RPC admission

**Sources:** `pt1-sad-springboard.md`

**Reference files:**

- `ritual-reth-internal/crates/rpc/rpc/src/eth/helpers/transaction.rs` runs RPC-specific async detection and `validate_async_payload(...)` before accepting a raw transaction from the RPC path.
- `ritual-reth-internal/crates/transaction-pool/src/validate/eth.rs` is the general transaction-pool validator; the reviewed path checks transaction type enablement, input size, gas limits, fee caps, chain id, nonce, and funds, but this pass did not find equivalent async-precompile semantic payload checks for normal origin transactions.
- `ritual-reth-internal/crates/ritual-async/src/validation.rs` is the shared async payload validator that the RPC path uses and the pool/P2P path should be compared against if these checks are meant to apply before builder selection.

**Status:** current-code lead.

RPC submission appears to apply shared async payload validation, while the transaction-pool validation path may only gate transaction type support and not semantic validation for normal origin transactions that call async precompiles. This can allow malformed or resource-heavy transactions through non-RPC propagation even if RPC would reject them.

**Why unique:** It is related to RPC-only validation, but it is a different entry path. Even if block verification eventually rejects a payload, weaker P2P/pool validation can create availability and builder-resource problems.

### 7. Async input-size limit drifts between RPC/shared validation and builder/contract limits

**Sources:** `audit-loop-missed-findings.md`, `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-async/src/validation.rs` defines the shared async input limit as 1MB.
- `ritual-reth-internal/crates/ritual-async/src/detector.rs` uses a 10KB async input limit in the builder/detection path.

**Status:** high-confidence consistency gap.

Shared async validation allows a 1MB async input, while builder detection, async fee constants, and `AsyncJobTracker` appear to use a 10KB protocol limit. That means a transaction can be accepted or presented as valid by one path while being impossible to commit or execute through another.

**Why unique:** This is a concrete parameter mismatch, not just a generic "validation differs" category.

### 8. Two-phase deadline extraction can fail open on malformed or short input

**Sources:** `audit-loop-missed-findings.md`, `pt1-sad-springboard.md`, `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` runs Phase 2 deadline checks only when `extract_phase2_deadline(...)` returns `Some`; short inputs return `None`.

**Status:** medium-high confidence candidate; verifier fail-open pattern confirmed, contract-side short-input behavior not re-verified in this repo.

Verifier deadline checks appear to run only when `extract_phase2_deadline(...)` returns `Some`, while malformed or short input can return `None`. The contract-side extractor may collapse too-short input to offset `0`, which can avoid the intended "extractable, greater than TTL, and within max offset" invariant.

**Why unique:** This is a malformed-input validity issue that can survive even if normal well-formed two-phase flows work correctly.

### 9. Builder validates Phase 2 deadlines for only a subset of two-phase precompiles

**Sources:** `audit-loop-missed-findings.md`, `pt1-sad-springboard.md`, `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` classifies HTTP, ZK, FHE, Sovereign Agent, Image, Audio, Video, and Persistent Agent as two-phase.
- `ritual-reth-internal/crates/ritual-async/src/detector.rs` performs builder-side Phase 2 deadline validation only in the long-running HTTP, Sovereign Agent, ZK, and Persistent Agent branches.

**Status:** medium-confidence consistency gap.

The verifier classifies long-running HTTP, ZK, FHE, Sovereign Agent, Image, Audio, Video, and Persistent Agent as two-phase. Builder detector-side deadline validation appears explicit for long-running HTTP, Sovereign Agent, ZK, and Persistent Agent, with less obvious coverage for FHE and media families.

**Why unique:** This is the builder/verifier consistency half of the deadline issue. Even if the verifier is fixed to fail closed, builders may still waste block-building work or produce invalid blocks if detector validation is incomplete.

### 10. Same-block nonce lock may not account for commitments created earlier in the block

**Sources:** `audit-loop-missed-findings.md`, `pt1-sad-springboard.md`, `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-block-verification/src/nonce_lock.rs` builds same-block commitment sender sets but checks ordinary transaction senders against parent-state pending jobs.

**Status:** medium-confidence candidate; policy decision needed.

Nonce-lock verification checks parent-state pending jobs and rejects duplicate same-block commitments, but may not reject an unrelated regular transaction from a sender that also creates a same-block async commitment. If nonce locking is meant to take effect immediately once a commitment is included, the verifier needs to augment parent-state locks with same-block commitment senders.

Concrete example:

```text
Block N:
  tx1 = async origin tx from S
  tx2 = TxAsyncCommitment for tx1, creating a pending job for S
  tx3 = unrelated normal tx from S
```

Current checks could miss this because `tx3` is checked against parent-state pending jobs, and before block `N` executes, `S` may have no pending job yet. The verifier correctly exempts `tx1` because it is the origin transaction for a same-block commitment, but it may not also reject `tx3`, even though `tx2` creates a same-block lock for the same sender.

**Why unique:** This is a global block correctness issue, not a single-transaction purity check.

### 11. `reviveAgent` purity checks may not validate canonical revival payload

**Sources:** `audit-loop-missed-findings.md`, `pt1-sad-springboard.md`, `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` decodes heartbeat `reviveAgent` calls to the agent address and checks ordering/state/caller constraints.
- `ritual-reth-internal/crates/scheduling/src/canonical.rs` builds canonical revival precompile input bytes that are not compared by the verifier path.

**Status:** medium-high confidence candidate.

Existing heartbeat checks validate `reviveAgent` signature/value/calldata shape, caller, target failed state, and ordering, but may not prove the `precompileInput` is the canonical revival request for that agent. A builder could potentially include a syntactically valid revival for the right failed agent with stale or arbitrary persistent-agent input.

**Why unique:** Issue `352` covers missing revival inclusion. This is a separate purity issue for revivals that are present.

### 12. Async commitments for reverted or halted origin transactions need explicit semantics

**Sources:** `audit-loop-missed-findings.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-async-commitment-validator/src/lib.rs` re-simulates the origin transaction and uses recorded async precompile calls without requiring the transaction result to be successful.
- `ritual-reth-internal/crates/ritual-async-inspector/src/inspector.rs` records the async call and returns `None`, allowing normal EVM execution to continue afterward.

**Status:** code behavior confirmed; semantic ambiguity remains.

Builder detection and commitment validation may record async precompile calls even when the simulated origin transaction later reverts or halts. The protocol needs to decide whether a reverted EVM transaction should still register an off-chain async job.

Example:

```solidity
function doThing() external {
    ASYNC_PRECOMPILE.call(...); // inspector records async request X
    revert("after async");      // transaction later reverts
}
```

The inspector records the async call, then returns `None`, which means "continue normal call execution." The comment says exactly that in `ritual-async-inspector/src/inspector.rs`: it records the first async call and lets the transaction keep running.

**Why unique:** This is not necessarily a bug, but it is consensus-visible behavior with user-facing fee and side-effect implications.

### 13. Consensus-critical addresses, limits, and validation modes remain runtime-env configurable

**Sources:** `audit-loop-missed-findings.md`, `pt1-sad-springboard.md`, `second-pass.md`, `first-pass.md`; related Asana task [Migrate Contract Addresses to Chain Configuration](https://app.asana.com/1/1206274797081445/project/1212017194493012/task/1212349522094290)

**Reference files:**

- `ritual-reth-internal/crates/ritual-scheduled-verification/src/lib.rs` reads consensus-relevant scheduler, wallet, system-account, and heartbeat addresses from environment variables.
- `ritual-reth-internal/crates/ritual-sequencing-rights/src/classifier.rs` reads `RITUAL_SEQUENCING_RIGHTS_FULL_CALL_GRAPH_ENABLED` to change sequencing-rights classification behavior.

**Status:** confirmed pattern; exact blast radius varies by variable.

Several verifier or shared validity paths read contract addresses, TTL caps, validation modes, registry addresses, and bypass flags from process environment or defaults. Values such as scheduler, wallet, system account, heartbeat, async job tracker, async delivery, TEE registry, model registry, async max TTL, and validity bypass flags can affect block validity or verifier behavior.

One concrete example is `RITUAL_SEQUENCING_RIGHTS_FULL_CALL_GRAPH_ENABLED`, which can change whether sequencing-rights classification uses only top-level calls or full EVM call-graph inspection. If validators run with different values, they can classify the same block differently and disagree on validity.

**Why unique:** Address migration work existed for a subset, but the notes identify a broader inventory beyond model/executor registry addresses. Any env-driven consensus parameter should be grouped here and moved to chain/fork config or rejected in production startup if overridden.

### 14. Verifier missing-dependency fallbacks should fail loudly

**Sources:** `second-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` returns `Ok(())` from async commitment verification when required verifier dependencies such as state provider or EVM environment factory are absent.

**Status:** medium-confidence high-impact hardening issue.

Some verifier phases return `Ok(())` when required dependencies such as the state provider, EVM config, or EVM environment factory are absent. That creates a silent fallback: the block appears to pass the phase, but the phase did not actually run its consensus-critical check.

The safer invariant is that production block verification should fail loudly when a required verifier dependency is missing. A no-state or no-EVM verifier may be useful for tests or diagnostics, but it should be impossible to use accidentally on the block-import path without an explicit, visible bypass mode.

**Why unique:** This is a wiring/configuration risk inside the verifier abstraction, not a missing individual constraint.

### 15. Precompile family classification is still partly duplicated

**Sources:** `pt1-sad-springboard.md`, `second-pass.md`

**Reference files / constants:**

- `ritual-reth-internal/crates/ritual-precompile-addresses/src/lib.rs` defines the canonical constants and lists, including `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES`, `ALL_TWO_PHASE_PRECOMPILE_ADDRESSES`, and `is_two_phase_precompile(...)`.
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` still has a local `is_two_phase_precompile(...)` helper that manually enumerates `LONG_RUNNING_HTTP_PRECOMPILE`, `ZK_TWO_PHASE_PRECOMPILE`, `FHE_PRECOMPILE`, `SOVEREIGN_AGENT_PRECOMPILE`, `IMAGE_CALL_PRECOMPILE`, `AUDIO_CALL_PRECOMPILE`, `VIDEO_CALL_PRECOMPILE`, and `PERSISTENT_AGENT_PRECOMPILE`.
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs::extract_phase2_deadline(...)` also hardcodes per-family ABI offsets: Sovereign Agent field 4, Persistent Agent field 5, FHE field 10, and the default field 6 path for HTTP/ZK/Image/Audio/Video.
- `ritual-reth-internal/crates/ritual-async/src/validation.rs::extract_two_phase_deadline(...)` reimplements similar deadline extraction logic, but the observed branch only treats long-running HTTP, ZK, and FHE as the generic two-phase set after the Sovereign Agent and Persistent Agent special cases.

**Status:** confirmed maintainability and consistency risk.

Canonical precompile address constants and family lists have improved, but downstream verifier and detector code still manually reimplements some semantic classifications such as two-phase membership and deadline offsets. Central address constants do not prevent drift if behavior tables are duplicated elsewhere.

**Why unique:** This is the structural cause behind several family-specific inconsistencies, including deadline extraction and validation differences.

### 16. AWS Nitro and other dead/pre-production precompile surfaces should be removed or explicitly de-scoped

**Sources:** `first-pass.md`

**Status:** not verified in current `ritual-reth-internal`; AWS Nitro appears outdated or out of repo scope.

**Verification note:** A current-code search did not find AWS Nitro precompile code or Nitro-named review surface in `ritual-reth-internal`. The broader "other dead/pre-production precompile surfaces" claim remains a scoping question, but this entry should not be treated as a confirmed current-code issue without a concrete inventory.

The notes flag AWS Nitro as likely dead or half-broken review surface, with similar ambiguity around ZK and FHE production readiness. Leaving unused precompile artifacts in place makes it hard to tell whether findings are live product risk or stale surface area.

**Why unique:** This is not a single verifier bug, but it drives audit noise and can hide real production scope.

### 17. FHE Phase 2 output-size conversion can still panic

**Sources:** `pt1-sad-springboard.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-precompile-codecs/src/long_running.rs` calls `as_u64()` while extracting FHE `output_size_bytes` from decoded ABI data.
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs` calls `extract_fhe_output_size(...)` while verifying FHE Phase 2 delivery handling.

**Status:** current-code chain-halt lead.

`extract_fhe_output_size()` reportedly converts decoded ABI integer data with `as_u64()`, which can panic for values greater than `u64::MAX`. The function is used in payload construction and block verification paths for FHE Phase 2 delivery handling.

**Why unique:** This is a concrete panic path in a consensus-adjacent delivery parser, not a broad "precompile readiness" concern.

### 18. Scheduled predicate docs should state enforcement is a Reth validity rule

**Sources:** `first-pass.md`

**Reference files:**

- `ritual-reth-internal/crates/ritual-scheduled-verification/src/lib.rs` documents and implements the Reth-side scheduled predicate verification table.
- `ritual-reth-internal/crates/ritual-scheduled-verification/src/predicate.rs` contains the predicate interface and evaluation helpers used by the Reth validity rule.

**Status:** documentation issue.

`Scheduler.execute()` does not enforce `IScheduledPredicate.shouldExecute(...)` as a smart-contract precondition. That can look like a missing contract check when reading only the smart contract, but the intended protocol design is that predicate enforcement is a consensus/execution-layer block validity rule in Reth: honest builders evaluate the predicate before inclusion, and verifiers reject blocks that include scheduled transactions whose predicate is false, invalid, reverted, halted, or over the predicate gas limit.

The smart contract docs and `IScheduledPredicate` docs should say this explicitly. Without that context, reviewers may keep rediscovering the same false-positive contract issue or misunderstand where the actual validity constraint lives.

**Why unique:** This is not a missing verifier check; it is a documentation gap about the ownership of an existing validity rule.

## Already-Covered Items Kept Out Of The Main List

These appeared in the folder but were not re-added as new unique issues because they are already represented by the microsite or GitHub issues unless a distinct angle was listed above:

- Async commitment coverage for every in-block async precompile call, including nested delivery callbacks: issue `353`.
- Heartbeat `checkAndRevive` inclusion: issue `352` and microsite.
- `reviveAgent` inclusion for failed agents: issue `352` and microsite.
- Delivery timeout/refund inclusion: issue `352` and microsite.
- Sequencing-rights deadline skip asymmetry: issue `352` and microsite.
- Scheduled Phase B expiry and scheduled C9/fee handling: microsite PR rows.
- ONNX scheduled-censorship probe handling and validity-observability RPCs: microsite PR rows.
- Broad Nitro/DKMS/media/ZK/FHE audit surface: microsite, except for the more specific issues called out above.
