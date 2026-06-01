# Scheduled Precompile Caller Plan

## Goal

Preserve the current non-scheduled async rule:

- async job owner is the immediate precompile caller

But introduce a narrow scheduled-only exception:

- when a scheduled system transaction executes a precompile through the protocol-owned scheduled execution path, use `TxScheduled.caller` as the effective async `JobSender`

This is intended to restore original-user ownership semantics for scheduled async precompile calls without reintroducing a broad `tx.origin`-style escape hatch.

## Design Direction

Refactor the scheduled execution path from:

- `SYSTEM_SENDER -> TxScheduled -> Scheduler.execute(...) -> ScheduledConsumer -> precompile`

to:

- `SYSTEM_SENDER -> TxScheduled -> Scheduler.execute(...) -> precompile`

Then add a small reth-side override at the async sender provenance boundary:

- default: use immediate precompile caller
- scheduled system path: use `TxScheduled.caller`

The exception should be tied to the unique protocol execution path, not to `TxScheduled` in general.

## Why This Shape

The current `ScheduledConsumer` wrapper creates two problems:

- it makes the scheduled async caller appear as `ScheduledConsumer`
- it exposes public helper methods that EOAs can call directly, which makes the caller shape less unique than it should be

Inlining the precompile execution logic into `Scheduler` gives one privileged entry path for scheduled execution. That makes the reth exception easier to reason about and much safer to scope.

## Scope

### Contracts

- Move the scheduled precompile execution logic out of `ScheduledConsumer` and into `Scheduler`
- Keep `Scheduler` responsible for:
  - call storage
  - timing / TTL / predicate checks
  - wallet deduction / refunds
  - scheduled execution dispatch
- Recreate the useful observability surface currently provided by `ScheduledConsumer`:
  - `PrecompileCalled`-style event
  - any typed scheduling helpers that are still needed

### Reth / Execution

- Add a scheduled-only override at the async sender provenance boundary in the detector path
- Default behavior remains:
  - `JobSender = immediate precompile caller`
- Scheduled system-path behavior becomes:
  - `JobSender = TxScheduled.caller`

### Downstream

- Update traffic-gen scheduled actions to schedule through the new contract surface
- Update E2E/localnet tests to assert original-user ownership for scheduled async precompile flows
- Update docs that describe scheduled async caller semantics

## Guard Conditions For The Override

The override should only apply when all of the following are true:

1. The transaction is `TxScheduled`
2. The recovered sender is the fixed scheduled system sender
3. The transaction target is the configured `Scheduler`
4. The calldata is the scheduler `execute(callId, executionIndex)` path
5. The async precompile call occurs directly in that scheduled execution path

Everything else must continue using the normal immediate-caller rule.

Specifically, do **not** apply the override:

- to arbitrary scheduled transactions
- to arbitrary contracts called by the scheduler
- to direct EOA calls into any public helper contract

## Implementation Plan

### Phase 1: Contract Refactor

1. Add precompile execution helper(s) and async-output unwrapping/event emission to `Scheduler`
2. Add a scheduler-owned event surface equivalent to the useful parts of `ScheduledConsumer.PrecompileCalled`
3. Change scheduled precompile scheduling helpers to encode direct scheduler execution of the precompile call
4. Remove `executeScheduledPrecompileCall` from the public scheduled execution path
5. Keep or trim `ScheduledConsumer` depending on whether any non-execution helper API still needs to survive

Deliverable:

- scheduled precompile execution no longer flows through `ScheduledConsumer`

### Phase 2: Reth Sender Override

1. Identify the sender provenance boundary in the async detector
2. Introduce a helper that computes the effective async sender:
   - normal tx: inspector-captured caller
   - scheduled system path: `TxScheduled.caller`
3. Use that helper when constructing `AsyncCallResult`
4. Leave `commitment_job_sender()` unchanged; it should continue decoding whatever sender the commitment already contains

Deliverable:

- scheduled async commitments encode the original scheduler/user as `Job.sender`

### Phase 3: Consistency Audit

Audit and adjust any scheduled-specific code that currently bypasses `JobSender`:

- wallet billing helpers
- block verification
- same-block duplicate sender logic
- RPC field surfacing
- async pool sender locks

Expected outcome:

- most downstream behavior should follow automatically once the detector emits the right `JobSender`
- any remaining scheduled special cases should be reduced, not expanded

### Phase 4: Test Migration

Update:

- contract tests for scheduler execution
- reth unit/regression tests around sender provenance
- localnet scheduled async E2Es
- traffic-gen scheduled HTTP / LLM / ONNX / ZK flows

Important assertions:

- non-scheduled direct precompile calls still use immediate `msg.sender`
- scheduled async precompile calls use original scheduler/user as `Job.sender`
- direct EOA calls to any remaining helper surface do not trigger the override

## Risk Areas

### Scheduler Genericity

Moving precompile logic into `Scheduler` makes it less generic. That is acceptable if scheduled precompile execution is treated as protocol functionality rather than generic callback infrastructure.

### Observability Drift

A lot of existing tooling parses `ScheduledConsumer` events. Equivalent scheduler-side events must be provided before removing that path.

### Over-Broad Override

The main failure mode is turning `TxScheduled` into a broad provenance escape hatch. The fix must be gated by the system-only scheduler execution path, not by transaction type alone.

### Hidden Scheduled Special Cases

There is already scheduled-specific wallet logic in reth. After the sender override lands, that code should be audited to ensure it still agrees with the new source of truth and does not create double-special-casing.

## Validation Plan

### Local Network Testing

Use the local-network skill as the source of truth for localnet bring-up, image rebuild scope, and genesis/export handling:

- `/home/ritual/repos/.cursor/skills/local-network/SKILL.md`

This work should explicitly follow that skill's guidance for:

- determining the smallest necessary rebuild
- restarting the network correctly
- and, if `ritual-sc-internal` changes, making sure updated genesis/exported contract state is actually propagated before trusting test results

### Unit / Integration

- scheduled contract execution emits the expected event payloads
- detector produces `JobSender == TxScheduled.caller` only for the guarded scheduled path
- detector still produces `JobSender == immediate caller` for all non-scheduled flows

### Localnet / E2E

- scheduled HTTP call
- scheduled OpenAI / LLM call
- scheduled ONNX inference
- scheduled ZK two-phase
- scheduled long-running async flows

### Traffic Validation

Use the serial workload list in:

- `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/gold1p-batch-results.json`

Required checks:

1. Confirm each listed serial command still succeeds individually after the refactor.
2. Then validate the parallel traffic path with:
   - `make run-api`
   - `make start-traffic FILE=gold-1p.json`
   - `make watch-traffic-status`
3. Treat parallel validation as incomplete unless the resulting success rate is near 100%, not just "actions started" or "running."

For each:

- `Job.sender` should equal original user / scheduler caller
- wallet billing should hit the original user slot
- duplicate sender locks should operate on the original user

### Negative Tests

- direct EOA call to any remaining public helper contract must not get the scheduled override
- non-precompile scheduled callbacks must not get the override
- arbitrary scheduler-routed contract calls must not get the override unless they are the blessed direct scheduled-precompile path

## Repo Impact

- `ritual-sc-internal`
  - main contract refactor
- `ritual-reth-internal`
  - detector/provenance override and consistency audit
- `ritual-reth-nodebuilder-internal`
  - likely minor verification / test fallout only
- `traffic-gen-internal`
  - scheduled action contract interface and verification updates
- `ritual-node-internal`
  - localnet/E2E expectation updates
- `ritual-dapp-skills`
  - docs if scheduled semantics are user-visible

## Recommendation

If we are going to support original-user semantics for scheduled async precompile calls, do it with both pieces:

1. inline scheduled precompile execution into `Scheduler`
2. add one narrow reth-side sender override at the async provenance boundary

Doing only the override is possible, but it leaves an unnecessarily entangled public-wrapper path in place. Doing only the contract refactor simplifies architecture, but does not change caller ownership semantics by itself.
