## invariant-0005 cur-daefd947f4-chain-halt-eviction-takes-priority-over-scheduled-eviction

- Title: Chain-halt eviction takes priority over scheduled age eviction
- Subsystem: scheduler
- Missing behavior: Missing transaction-pool maintenance rule that detects chain halt, evicts scheduled transactions as poisonous, records chain_halt_detected, and suppresses scheduled age eviction on the same tick.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Drive txpool maintenance with a stale latest header and scheduled tx present; current port exposes no chain-halt scheduled eviction path.
- Artifact: invariants/invariant-0005.json

## invariant-0012 cur-ca24e3812d-missed-canonical-scheduler-windows-caught

- Title: Missed canonical scheduler windows are not caught up
- Subsystem: scheduler
- Missing behavior: No audited repo preserves a canonical scheduler rule that suppresses missed historical windows and fires only the current/next execution index; the port catches up unexecuted due indices inside TTL.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create a schedule with missed earlier indices still inside TTL at block 130; current port due_index_bounds can return multiple indices, while the invariant expects no catch-up burst.
- Artifact: invariants/invariant-0012.json

## invariant-0018 cur-4a8b295707-scheduler-channel-size-configurable

- Title: Scheduler channel size is configurable
- Subsystem: scheduler
- Missing behavior: No audited repo implements ScheduledTxService event-processing channels whose capacity is parsed from RITUAL_SCHEDULER_CHANNEL_SIZE with a fallback of 1000 when absent or invalid.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Set RITUAL_SCHEDULER_CHANNEL_SIZE to unset, invalid, and a small valid value, then instantiate the current scheduled event-processing service; no such service/channel construction exists in the audited repo set, so the test cannot be written without restoring that surface.
- Artifact: invariants/invariant-0018.json

## invariant-0019 cur-c172a5245e-scheduler-monitor-share-state

- Title: Scheduler monitor can share state
- Subsystem: scheduler
- Missing behavior: No audited repo implements SchedulerContract construction with an externally supplied Arc for sharing one scheduler service-state instance.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Attempt to construct SchedulerContract::new_with_state with a shared Arc and observe mutations through another Arc clone; the required types/constructor are absent from the audited repo set.
- Artifact: invariants/invariant-0019.json

## invariant-0025 cur-c0b9273ca4-synchronousscheduler-singleton-initialized-once

- Title: SynchronousScheduler singleton is initialized once
- Subsystem: scheduler
- Missing behavior: No audited repo implements SynchronousScheduler one-time singleton initialization with instance() failing before initialize(), a single successful initialize(address), and repeated initialize returning already-initialized.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: API parity test for SynchronousScheduler::instance before/after initialize cannot be expressed because the type/surface is absent.
- Artifact: invariants/invariant-0025.json

## invariant-0026 cur-98669920ac-scheduler-adapter-honors-requested-state-height

- Title: Scheduler adapter honors requested state height
- Subsystem: scheduler
- Missing behavior: No audited repo implements canonical scheduling ClientAdapter get_storage_at(address, slot, Option) selecting historical vs latest state and converting storage to 32-byte Bytes or empty Bytes for missing storage.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Fake provider test for Some(block) vs None latest and missing storage returning empty Bytes cannot be instantiated because the adapter surface is absent.
- Artifact: invariants/invariant-0026.json

## invariant-0028 cur-580c866f4b-canonical-handler-processes-async-commitments-first

- Title: Canonical handler processes async commitments first
- Subsystem: scheduler
- Missing behavior: Missing blocking canonical-state handler that processes async commitment transactions and then scheduled canonical-state processing in the same handler/order.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instrument provider blocking canonical handler with async commitment and due scheduled work; current port lacks the scheduled callback after async processing.
- Artifact: invariants/invariant-0028.json

## invariant-0029 cur-6296489688-scheduler-observability-includes-timing-bounds

- Title: Scheduler observability includes timing and bounds
- Subsystem: scheduler
- Missing behavior: No audited repo actively emits scheduled verification start/end logs with max_block-equivalent bounds plus Scheduler processing ritual::scheduling storage/event/state/block timing logs.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Enable tracing through scheduled verification and due obligation processing; assert required tx_verify max_block and ritual::scheduling events exist. Expected to fail on audited revisions.
- Artifact: invariants/invariant-0029.json

## invariant-0031 cur-e6a6cb5e5f-scheduled-maintenance-event-bounds-defensive

- Title: Scheduled maintenance and event bounds are defensive
- Subsystem: scheduler
- Missing behavior: Missing txpool maintenance that reads CHAIN_HALT_THRESHOLD_SECS with default 10, compares latest-block wall-clock divergence, and evicts all scheduled transactions as poisonous only when threshold is exceeded.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Run txpool maintenance with raw scheduled tx and stale latest block timestamp >10 seconds; expected poisonous eviction path is absent.
- Artifact: invariants/invariant-0031.json

## invariant-0034 cur-fc5e70c5fd-scheduled-verification-parent-state-backed

- Title: Scheduled verification is parent-state backed
- Subsystem: scheduler
- Missing behavior: Missing full invariant: block verification does not hard-fail RitualWallet balance C9 failures unless skip mode is enabled; instead underfunded wallet cases are allowed for Scheduler.execute contract eviction.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Construct valid scheduled tx with insufficient RitualWallet balance and skip mode disabled; invariant expects verifier failure, current port tests/logic predict Ok.
- Artifact: invariants/invariant-0034.json

## invariant-0036 cur-ff06694da2-canonical-scheduling-fires-only-next-index

- Title: Canonical scheduling fires only the next index
- Subsystem: scheduler
- Missing behavior: No canonical scheduling path computes a single next/current execution index, compares it to fired_count, and skips missed catch-up indices; the port can synthesize multiple unexecuted due indices in one block/window.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Scheduler state with start_block=100, frequency=1, ttl=500, no executed bits at block 105 should produce 0..=5 in the port but invariant expects at most one next index.
- Artifact: invariants/invariant-0036.json

## invariant-0038 cur-73ef235e96-heartbeat-revival-validity-uses-parent-state

- Title: Heartbeat revival validity uses parent state
- Subsystem: scheduler
- Missing behavior: HeartbeatTracker::sync_from_storage does not skip individual agents whose address/state/liveness reads fail and does not initialize synced heartbeat_timeout_blocks from contract defaultTimeout when readable.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Mock heartbeat DB with multiple agents, one per-agent read failure, and defaultTimeout non-200; current port should return Err and use per-agent liveness timeout rather than defaultTimeout.
- Artifact: invariants/invariant-0038.json

## invariant-0039 cur-dfbd5158e5-chain-halt-poison-eviction-clears-scheduled-pool-scheduler

- Title: Chain-halt poison eviction clears scheduled pool and Scheduler calls
- Subsystem: scheduler
- Missing behavior: Missing chain-halt poison recovery path that reads threshold, detects temporal divergence, evicts scheduled pool transactions, and evicts each call_id from SynchronousScheduler state.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Populate due scheduled calls, make latest header stale beyond threshold, tick txpool maintenance, and assert scheduled pool entries/call IDs are evicted; current port lacks the path.
- Artifact: invariants/invariant-0039.json

## invariant-0041 cur-7835859c0a-chain-halt-threshold-precedes-lifetime

- Title: Chain-halt threshold precedes transaction lifetime
- Subsystem: scheduler
- Missing behavior: Missing startup rejection/panic when CHAIN_HALT_THRESHOLD_SECS >= txpool.max_tx_lifetime; no chain-halt threshold input or validation path exists in txpool maintenance.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Configure threshold >= --txpool.lifetime and start txpool maintenance; current port has no such threshold/validation path.
- Artifact: invariants/invariant-0041.json

## invariant-0044 cur-8678779d10-terminal-scheduler-events-retain-calls

- Title: Non-terminal scheduler events retain calls
- Subsystem: scheduler
- Missing behavior: No audited repo contains the old Scheduler event-processing lifecycle that retains calls on non-terminal failure/skip events and removes calls on cancel/complete/expire events.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Replay each Scheduler event status against the port; there is no event-state processor to retain ExecutionFailed/SkippedInsufficientFunds/SkippedTTLExpired calls or remove Cancel/Complete/Expired calls.
- Artifact: invariants/invariant-0044.json

## invariant-0045 cur-ee664f4d6d-pinned-contract-cache-entries-expire

- Title: Pinned contract cache entries do not TTL-expire
- Subsystem: scheduler
- Missing behavior: Missing separate pinned account and storage caches for pinned system contract reads/inserts, and missing distinction where non-pinned addresses continue using regular TTL/idle caches.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Configure one pinned and one non-pinned contract and advance beyond the regular cache idle time; current port has no pinned cache configuration or TTL/idle policy to make this behavior observable.
- Artifact: invariants/invariant-0045.json

## invariant-0047 cur-c4d7cbec77-scheduled-builder-filtering-remains-deterministic-around-parallel-simulation

- Title: Scheduled builder filtering remains deterministic around parallel simulation
- Subsystem: scheduler
- Missing behavior: Missing deterministic parallel-simulation pipeline for scheduled async candidates: no hash-deduped parallel simulation batch, revival-lane filtering before the global cap, max-simulation limiting, or sequential post-simulation async-cache insertion path was found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Provide duplicate scheduled candidates, unselected revival candidates, same-sender candidates, and cap overflow; current port has no parallel scheduled async simulation batch to enforce the specified ordering.
- Artifact: invariants/invariant-0047.json

## invariant-0048 cur-709c49673e-duplicate-async-jobs-prune-stale-pool

- Title: Duplicate async jobs prune stale pool transactions
- Subsystem: scheduler
- Missing behavior: Missing self-healing behavior: active duplicate scheduled or regular async jobs are not both cached as InvalidAsync and pruned from the transaction pool by original transaction hash.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Mock job_exists_and_active=true for scheduled and regular async candidates and assert each is skipped, cached InvalidAsync, and removed from txpool; current scheduled path only skips.
- Artifact: invariants/invariant-0048.json

## invariant-0049 cur-a48f14c25e-async-pool-derives-block-expiry

- Title: Async pool derives commit block from expiry
- Subsystem: scheduler
- Missing behavior: Async pool metadata insertion does not derive commit_block as expiry_block - ttl and does not compute two-phase deadlines from such a derived commit block.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Insert commitment with expiry_block=120, ttl=20, and divergent commitment commit_block; current port has no expiry_block input and stores canonical commit_block instead.
- Artifact: invariants/invariant-0049.json

## invariant-0051 cur-8504c8d14d-scheduled-removals-decrement-calldata-counters

- Title: Scheduled removals do not decrement calldata counters
- Subsystem: scheduler
- Missing behavior: Missing scheduled subpool insertion/removal accounting rule: no scheduled pool path exists that avoids incrementing calldata counters on insertion and therefore avoids decrementing them on removal/prune.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Add normal calldata-counted transactions plus a scheduled transaction through a scheduled subpool and remove the scheduled hash; current port has no scheduled subpool/counter path to satisfy the assertion.
- Artifact: invariants/invariant-0051.json

## invariant-0052 cur-c6aa75bc8f-duplicate-pending-reviveagent-submissions-skipped

- Title: Duplicate pending reviveAgent submissions are skipped
- Subsystem: scheduler
- Missing behavior: Missing canonical-state guard that scans the scheduled pool for an existing pending reviveAgent(agent) and skips submitting a duplicate for the same target agent while allowing distinct agents.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Put reviveAgent(A) in the scheduled pool then process another canonical update for A and B; current port lacks the scheduled pool scan needed to skip A and submit B.
- Artifact: invariants/invariant-0052.json

## invariant-0054 cur-bb612fd1fc-heartbeat-expiry-checks-read-only-during-payload-builds

- Title: Heartbeat expiry checks are read-only during payload builds
- Subsystem: scheduler
- Missing behavior: Missing payload-build heartbeat expiry check that calls get_expired_agents under a read-only tracker snapshot without sync_from_storage or mutable hydration.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instrument HeartbeatTracker::sync_from_storage and run payload building through heartbeat expiry; current port has no such payload path to exercise.
- Artifact: invariants/invariant-0054.json

## invariant-0055 cur-24eb469c36-payload-builder-enforces-block-count

- Title: Payload builder enforces a block transaction-count cap
- Subsystem: scheduler
- Missing behavior: Missing RETH_MAX_TRANSACTIONS_PER_BLOCK cap across heartbeat, scheduled, async commitment, settlement pair, delivery, and regular inclusion paths.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Set RETH_MAX_TRANSACTIONS_PER_BLOCK=1 and offer a two-transaction async settlement pair; current builder has no count cap to prevent overrun or partial-pair admission.
- Artifact: invariants/invariant-0055.json

## invariant-0056 cur-36c8699cd3-build-policy-demote-optional-payload-work

- Title: Build policy can demote optional payload work
- Subsystem: scheduler
- Missing behavior: Missing optional-work demotion behavior: no WorkClass::Obligations skip with empty obligation set and no unified execution break policy.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Configure a policy to skip obligations with due parent-state obligations; current payload builder has no policy object to bypass obligation scanning.
- Artifact: invariants/invariant-0056.json

## invariant-0057 cur-cd37f0ea99-block-build-traces-preserve-first-primary-cause

- Title: Block build traces preserve the first primary cause
- Subsystem: scheduler
- Missing behavior: Missing producer path that captures the first primary cause during payload building and records it into block-build traces.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Trigger multiple demotions/deadline breaches with trace enabled; current port exposes the field type but no payload-builder producer populates it.
- Artifact: invariants/invariant-0057.json

## invariant-0058 cur-08a616bb00-async-collection-traces-combined-phases-observations

- Title: Async collection traces use combined phases and cap observations
- Subsystem: scheduler
- Missing behavior: Missing combined async collection telemetry producer: no combined_parallel_simulation/combined_post_filter phases, scheduled/regular counts, aggregate async stats, or capObservations are emitted by payload building.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Build with scheduled and regular async candidates and query ritual_getBlockBuildTrace; current port has schema fields but no producer path to populate combined phases/cap observations.
- Artifact: invariants/invariant-0058.json

## invariant-0061 cur-af91dbee21-scheduled-execution-errors-record-full-incident-context

- Title: Scheduled execution errors record full incident context
- Subsystem: scheduler
- Missing behavior: Missing payload-builder incident recording hook for scheduled transaction execution errors, including scheduled-only filtering, decoded Scheduler calldata, full error/source chain, debug text, and revert selector classification.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Force scheduled tx BlockExecutionError in payload builder and assert an incident is recorded; current port has recorder structs but no payload callsite.
- Artifact: invariants/invariant-0061.json

## invariant-0063 cur-312da4fe92-async-simulation-caps-protect-regular-candidates

- Title: Async simulation caps protect regular candidates
- Subsystem: scheduler
- Missing behavior: Missing phase-1 async simulation allocation policy: no hard total cap, soft scheduled/regular caps, regular-priority overcommit, overflow allocation, zero-cap lane disablement, warnings, or pre-cap cap pressure diagnostics.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call allocate_async_sim_slots-style cases from the invariant; current port has no allocator symbol or equivalent behavior to test.
- Artifact: invariants/invariant-0063.json

## invariant-0064 cur-d72383a35d-combined-async-simulation-preserves-ordered-post-filtering

- Title: Combined async simulation preserves ordered post-filtering
- Subsystem: scheduler
- Missing behavior: Missing combined parallel async simulation and ordered sequential post-filtering across scheduled and regular candidates, including proceed-on-storage-error and pool-only stale pruning semantics.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Provide scheduled and regular async candidates with same sender; current port has no combined parallel pass then ordered post-filter phase to test.
- Artifact: invariants/invariant-0064.json

## invariant-0065 cur-62de2eed59-scheduled-dedicated-managed-subpool

- Title: Scheduled transactions use a dedicated node-managed subpool
- Subsystem: scheduler
- Missing behavior: Missing dedicated node-managed Scheduled subpool with retrieval and hash pruning that avoids ordinary sender accounting.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Insert node-generated scheduled tx through scheduled insertion path and retrieve/remove it from Scheduled subpool; current port lacks this path.
- Artifact: invariants/invariant-0065.json

## invariant-0066 cur-3015bfcbed-payload-builder-filters-scheduled-pool-before-execution

- Title: Payload builder filters scheduled-pool transactions before execution
- Subsystem: scheduler
- Missing behavior: Missing the required scheduled-pool source and filter path; only normal-pool scheduled candidates are filtered inline.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Populate dedicated scheduled pool with valid/invalid scheduled txs; current port has no scheduled pool source to feed the filter.
- Artifact: invariants/invariant-0066.json

## invariant-0067 cur-1cff45af0b-canonical-scheduling-runs-blocking-pool-handler

- Title: Canonical scheduling runs in the blocking pool handler
- Subsystem: scheduler
- Missing behavior: Missing synchronous transaction-pool blocking canonical handler that replays Scheduler-origin events, updates scheduler state, removes mined async originals, and submits scheduled transactions before canonical update returns.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Apply canonical update with Scheduler Create/Cancel events and assert blocking handler updates scheduler state and submits due scheduled txs; current port lacks handler.
- Artifact: invariants/invariant-0067.json

## invariant-0068 cur-602c4265cc-scheduler-state-removes-only-terminal-explicitly-evicted-calls

- Title: Scheduler state removes only terminal or explicitly evicted calls
- Subsystem: scheduler
- Missing behavior: Missing Scheduler state cleanup semantics that remove calls and auxiliary indexes only for terminal/explicit eviction events and retain retryable failures/skips.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Process terminal and non-terminal Scheduler events against scheduler state; current port has no event-state processor.
- Artifact: invariants/invariant-0068.json

## invariant-0069 cur-e33e049f37-scheduled-async-pool-lanes-coordinate-without-duplicate-ownership

- Title: Scheduled and async pool lanes coordinate without duplicate ownership
- Subsystem: scheduler
- Missing behavior: Missing full cross-lane ownership coordination: no scheduled subpool ownership checks, no scheduled-or-async local-known verifier path, and no stale-pool pruning for duplicate active jobs.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Exercise all four lane-coordination cases from the invariant; current port only satisfies the scheduled async index/sender-lock subset.
- Artifact: invariants/invariant-0069.json

## invariant-0070 cur-4b080eecde-async-scheduled-pools-expire-block-time-chain-halt

- Title: Async and scheduled pools expire by block, time, and chain-halt rules
- Subsystem: scheduler
- Missing behavior: Missing scheduled-pool block expiry, scheduled stale lifetime expiry, and chain-halt eviction of scheduled pool plus Scheduler state; only async block/time expiry is present.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Run async and scheduled block/time/chain-halt expiry fixtures; current port can only satisfy async cleanup portions.
- Artifact: invariants/invariant-0070.json

## invariant-0071 cur-54a1846da8-specialized-subpools-remain-visible-pool-accounting

- Title: Specialized subpools remain visible in pool accounting
- Subsystem: scheduler
- Missing behavior: Missing specialized subpool visibility in size reporting, metrics, invariant accounting, and scheduled removal metrics.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Insert scheduled and awaiting-execution transactions and assert PoolSize/metrics include them; current port lacks scheduled subpool accounting.
- Artifact: invariants/invariant-0071.json

## invariant-0073 cur-d4acaf0d5e-scheduled-obligations-shared-bounded-parent-state-eligibility

- Title: Scheduled obligations use shared bounded parent-state eligibility
- Subsystem: scheduler
- Missing behavior: Missing full shared bounded eligibility rule: no env-controlled pool-vs-contract scan selection and no explicit max-obligations-per-block cap defaulting to 64.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create >64 due obligations plus env-controlled synced pool cases; current port has parent-state due-window logic but no cap/env selection to satisfy the full invariant.
- Artifact: invariants/invariant-0073.json

## invariant-0075 cur-9b782bd535-async-duplicate-checks-fail-closed-ignore-expired-jobs

- Title: Async duplicate checks fail closed and ignore expired jobs
- Subsystem: scheduler
- Missing behavior: Missing fail-closed duplicate handling: active-job reads that error are treated as Proceed rather than aborting block construction.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Inject an AsyncJobTracker storage-read error in scheduled async augmentation; current port proceeds instead of failing closed.
- Artifact: invariants/invariant-0075.json

## invariant-0076 cur-fd2fbb50e0-scheduled-async-sources-share-detection-path

- Title: Scheduled async sources share one detection path
- Subsystem: scheduler
- Missing behavior: Missing unified pre-simulation detection path with async_cache classification for pool-sourced and augmented scheduled async sources.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search for async_cache/classification in payload builder; current port lacks the shared cache and uses separate candidate arms.
- Artifact: invariants/invariant-0076.json

## invariant-0080 cur-52946ce7a0-zero-pool-scheduled-mode-ignores-pool-candidates-consistently

- Title: Zero-pool scheduled mode ignores pool candidates consistently
- Subsystem: scheduler
- Missing behavior: Missing RITUAL_ZERO_POOL_SCHEDULED payload-builder mode and transaction-hash de-duplication for merged scheduled candidates.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Current port has no RITUAL_ZERO_POOL_SCHEDULED payload code path to exercise.
- Artifact: invariants/invariant-0080.json

## invariant-0081 cur-2ffb9b030a-payload-verifier-deadlines-avoid-asymmetric-obligation-membership

- Title: Payload and verifier deadlines avoid asymmetric obligation membership
- Subsystem: scheduler
- Missing behavior: Missing the exact deadline invariant: default is 300ms instead of 500ms, scheduled obligation scanning is not deadline-threaded, and deterministic obligation caps required by the invariant are absent.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Unset RETH_BUILD_DEADLINE_MS and assert the required 500ms default; current port has DEFAULT_BUILD_DEADLINE_MS = 300.
- Artifact: invariants/invariant-0081.json

## invariant-0082 cur-c6695cdc28-async-simulation-bounded-policy-demotable

- Title: Async simulation is bounded but not policy demotable
- Subsystem: scheduler
- Missing behavior: Missing AsyncSims classification, shared scheduled-plus-regular simulation counter, async simulation deadline, and current-cycle async_cache gate.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search for RETH_MAX_ASYNC_SIMS_PER_BLOCK, RETH_ASYNC_SIM_DEADLINE_MS, and async_cache; current port has no implementation to satisfy the invariant.
- Artifact: invariants/invariant-0082.json

## invariant-0083 cur-1a59d83a46-async-collection-emits-detailed-lifecycle-stats

- Title: Async collection emits detailed lifecycle stats
- Subsystem: scheduler
- Missing behavior: Missing AsyncCollectionStats return/log record with scheduled/regular/total simulated counts, accepted count, deadline-skipped count, parallel mode, deadline fields, and fallback outcome.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search/build for AsyncCollectionStats and lifecycle fields; current port lacks the type and logs only generic payload/deadline events.
- Artifact: invariants/invariant-0083.json

## invariant-0084 cur-0e3374965f-heartbeat-revival-uses-hydrated-state-respects-build-deadline

- Title: Heartbeat revival uses hydrated state and respects build deadline
- Subsystem: scheduler
- Missing behavior: Missing end-to-end heartbeat revival/deadline invariant: payload building does not hydrate/use HeartbeatTracker state, does not run a direct checkAndRevive phase, and does not gate remaining build phases immediately after that system transaction.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Payload build with unsynced/expired heartbeat state; current port lacks tracker hydration and direct post-revival deadline gating.
- Artifact: invariants/invariant-0084.json

## invariant-0088 cur-edf229bd15-async-payload-collection-uses-cached-simulation-gates

- Title: Async payload collection uses cached simulation gates
- Subsystem: scheduler
- Missing behavior: Missing cached async payload collection model: no async_cache by tx hash, no current-cycle simulation gate, no pre-normal-loop async collection/execution of recovered async system txs, and no rule that skips unsimulated originals in normal loops.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search for async_cache/current-cycle simulation gates; current port lacks this collection model.
- Artifact: invariants/invariant-0088.json

## invariant-0092 cur-f675369d83-payload-byte-limits-estimated-plus-sizes

- Title: Payload byte limits use estimated transaction plus log sizes
- Subsystem: scheduler
- Missing behavior: Missing full estimated-size policy: CLI/config/limit propagation and skip checks exist, but transaction contribution is only RLP length plus a fixed 1024 overhead, with no tx.size() plus type-specific log estimates such as 1800/1024/0.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search for type-specific size/log-estimate constants; current port uses length plus fixed 1024 overhead.
- Artifact: invariants/invariant-0092.json

## invariant-0094 cur-03136a7c3e-payload-verification-phases-emit-timing-metrics

- Title: Payload and verification phases emit timing metrics
- Subsystem: scheduler
- Missing behavior: Missing end-to-end per-phase timing emission from payload building, block execution, and block verification. Metrics structs/log helpers exist, but local payload and verifier code do not call them for async/scheduled/regular/finalization/verification phases.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Enable block-build trace collection and build/verify a block; current code has trace types but no payload/verifier phase emission sites.
- Artifact: invariants/invariant-0094.json

## invariant-0095 cur-c8709563d1-settlement-building-uses-contract-live-async-state

- Title: Settlement building uses contract-live async job state
- Subsystem: scheduler
- Missing behavior: Missing accepted commit-block lookback bounds for fulfilled settlement building; the port reads live contract state and checks absent/settled/expired/mismatch cases, but no lookback-bound policy was found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: A too-old commit_block fixture should be skipped by payload building; no local lookback-bound implementation was found.
- Artifact: invariants/invariant-0095.json

## invariant-0097 cur-a08ea4a6b9-state-cache-defaults-long-environment-configurable

- Title: State cache defaults are long but environment configurable
- Subsystem: scheduler
- Missing behavior: Missing ProviderCacheBuilder TTL/idle configurability and restored 7200s/3600s defaults; local execution cache is fixed-size and created by ExecutionCache::new without time_to_live/time_to_idle configuration.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search for ProviderCacheBuilder and RETH_STATE_CACHE_* env vars; current port lacks this cache builder/configuration.
- Artifact: invariants/invariant-0097.json

## invariant-0099 cur-eef8a4838d-canonical-scheduler-skips-missed-windows-instead-catch-bursts

- Title: Canonical scheduler skips missed windows instead of catch-up bursts
- Subsystem: scheduler
- Missing behavior: Missing canonical scheduler exact-target no-catch-up processing. The old scheduling crate/path is absent locally, and the live parent-state due-window logic intentionally includes any execution index whose target block is within TTL rather than only exact target blocks.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Current port lacks the canonical scheduler service path and its exact-target modulo firing rule.
- Artifact: invariants/invariant-0099.json

## invariant-0100 cur-520cb2f3e1-scheduler-event-decoding-rejects-oversized-identifiers

- Title: Scheduler event decoding rejects oversized identifiers
- Subsystem: scheduler
- Missing behavior: Missing scheduler event decoder overflow rejection. The old scheduling event decoder is absent locally; storage-reading code converts U256 storage fields with to::() but does not implement event decoding rejection for oversized event identifiers.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Current port lacks crates/scheduling/src/contract.rs and the u256_to_u64 event-overflow rejection path.
- Artifact: invariants/invariant-0100.json

## invariant-0101 cur-b079b77929-scheduler-event-reject-overflow

- Title: Scheduler event IDs reject u64 overflow
- Subsystem: scheduler
- Missing behavior: Missing EnhancedCallEvent construction with u64 overflow rejection; no local scheduler event parser was found in port or dependency repos.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Current port lacks EnhancedCallEvent and u256_to_u64 overflow checks.
- Artifact: invariants/invariant-0101.json

## invariant-0104 cur-c5ee05ab6f-synchronousscheduler-exposes-configured-scheduler-address

- Title: SynchronousScheduler exposes configured scheduler address
- Subsystem: scheduler
- Missing behavior: Missing SynchronousScheduler/SchedulerContract instance API that exposes the constructed scheduler address. The port has a global/env get_scheduler_address helper and optional address parameters, but no SynchronousScheduler object returning its stored SchedulerContract address.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search for SynchronousScheduler and SchedulerContract::address in local repos; both are absent.
- Artifact: invariants/invariant-0104.json

## invariant-0107 cur-3b004525fc-scheduler-event-monitoring-receipt-driven-block

- Title: Scheduler event monitoring is receipt-log driven per block
- Subsystem: scheduler
- Missing behavior: Missing receipt-log-driven Scheduler event monitor. Local port uses parent-state Scheduler storage readers and does not include a SchedulerContract scanner that reads one block plus receipts, filters scheduler logs by address/topic, records fetch timing, and skips malformed scheduler logs.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search local repos for SchedulerContract/parse_event_log/CallScheduled receipt scanning; absent.
- Artifact: invariants/invariant-0107.json

## invariant-0109 cur-3ac8507412-scheduler-legacy-bounds-derive-saturating-contract-recurrence-fields

- Title: Scheduler legacy bounds derive saturating from contract recurrence fields
- Subsystem: scheduler
- Missing behavior: Missing scheduler event parser that derives legacy bounds from event recurrence fields and rejects oversized U256 event indices. Port has saturating block math for parent-state ScheduledCall, but no event parser or u256_to_u64 overflow-rejection path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: No local derive_execution_bounds/u256_to_u64 event parser exists.
- Artifact: invariants/invariant-0109.json

## invariant-0120 cur-c31c7402a3-regular-state-cache-expiry-environment-configurable

- Title: Regular state cache expiry is environment-configurable
- Subsystem: scheduler
- Missing behavior: Missing regular provider cache TTL/idle environment configuration. The port uses ExecutionCache/CachedStateProvider fixed-size caches and has no RETH_STATE_CACHE_TTL_SECS/RETH_STATE_CACHE_IDLE_SECS handling or 7200s/3600s defaults.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search and unit test for cache env configuration; currently absent.
- Artifact: invariants/invariant-0120.json

## invariant-0121 cur-871e1b84d8-startup-scheduler-hydration-single-owner-fail-fast

- Title: Startup scheduler hydration is single-owner and fail-fast
- Subsystem: scheduler
- Missing behavior: Missing startup scheduler-memory hydration gate and fail-fast canonical scheduler handler. The old scheduling singleton/canonical/blocking_handlers paths are absent; the port reads Scheduler parent state directly for obligations instead of hydrating a shared scheduler memory owner.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: No local SynchronousScheduler startup hydration gate exists to test.
- Artifact: invariants/invariant-0121.json

## invariant-0122 cur-d36ea9772d-hydration-strictly-rebuilds-memory-active-scheduler-storage

- Title: Hydration strictly rebuilds memory from active Scheduler storage
- Subsystem: scheduler
- Missing behavior: Missing strict scheduler memory rebuild. The port can scan active Scheduler storage and uses saturating max-block helpers, but it does not hydrate/rebuild a scheduler-memory map, preserve origin_hash in that memory, reject duplicate call IDs during hydration, or set scheduler last_synced_block.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: No local scheduler-memory hydration surface exists; only parent-state scans are present.
- Artifact: invariants/invariant-0122.json

## invariant-0123 cur-ab97cc117d-revival-active-helper-guards-remain-independent

- Title: Revival and active-job helper guards remain independent
- Subsystem: scheduler
- Missing behavior: Missing revival pending-transaction dedup helper for AgentHeartbeat reviveAgentPrepared(address,bytes) with padded address validation. The active-job helper does pass the synthesized tx hash and building block to job_exists_and_active, but the revival dedup half was not found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Active-job helper can be unit-tested today; revival pending-tx dedup helper is absent.
- Artifact: invariants/invariant-0123.json

## invariant-0124 cur-02bf47c51d-system-validation-bypasses-user-nonce-balance-checks

- Title: System transaction validation bypasses user nonce and balance checks
- Subsystem: scheduler
- Missing behavior: Missing full system-validation bypass surface in the port. Alloy recovers scheduled/async system senders and txpool has generic disable_balance_check, but local pool validation still calls requires_nonce_check defaulting to true and no scheduled-specific validation bypass/feature-disable/set_nonce placeholder path was found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Pool validation tests for scheduled/async system transactions.
- Artifact: invariants/invariant-0124.json

## invariant-0125 cur-8ef1204264-scheduler-address-initialization-parsed-fail-fast

- Title: Scheduler address initialization is parsed and fail-fast
- Subsystem: scheduler
- Missing behavior: Missing startup SynchronousScheduler initialization and initialization-failure abort. Nodebuilder add-ons parse SCHEDULER_ADDRESS with expect and default fallback, but no local SynchronousScheduler startup path was found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Startup integration test for scheduler address parsing and scheduler initialization.
- Artifact: invariants/invariant-0125.json

## invariant-0129 cur-6946e1a647-operational-validation-guardrails-remain-current

- Title: Operational validation guardrails remain current
- Subsystem: scheduler
- Missing behavior: Missing at least one guardrail: regular state-cache TTL/idle environment configuration is absent. Other related guardrails exist, including zero-frequency scheduled call skip and scheduled incident trace bounded capacity, but the full compound invariant is not satisfied.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Compound guardrail test suite; currently fails on state-cache TTL/idle config.
- Artifact: invariants/invariant-0129.json

## invariant-0132 cur-5167b41507-canonical-scheduled-firing-requires-real-stored-origin-hashes

- Title: Canonical scheduled firing requires real stored origin hashes
- Subsystem: scheduler
- Missing behavior: Missing skip-on-missing origin hash behavior. The port attaches an origin hash from Scheduler storage, but read_origin_hash falls back to B256::ZERO on storage read failure, so transaction creation is not skipped when origin hash is missing/unreadable.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Origin-hash missing/unreadable scheduled firing test.
- Artifact: invariants/invariant-0132.json

## invariant-0134 cur-8f90f3deb9-asyncexec-participates-typing-metrics

- Title: AsyncExec participates in transaction typing and metrics
- Subsystem: scheduler
- Missing behavior: Missing AsyncExec as a first-class transaction type/storage codec variant/network announcement metric. Searches found no AsyncExec, TxAsyncExec, or asyncexec support in the audited repos.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: AsyncExec codec round-trip and announcement metrics regression tests.
- Artifact: invariants/invariant-0134.json

## invariant-0136 cur-4b6d786787-assorted-current-scheduler-adjacent-guards-remain-distinct

- Title: Assorted current scheduler-adjacent guards remain distinct
- Subsystem: scheduler
- Missing behavior: Missing blocking scheduler async-pool dedup. Finalized scheduled logs and heartbeat shape validation exist, but no crates/transaction-pool/src/blocking_handlers.rs path and no add_scheduled_transaction/derived scheduled async_pool dedup behavior were found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Scheduled finalization metrics, heartbeat verifier, and async-pool duplicate suppression tests.
- Artifact: invariants/invariant-0136.json

## invariant-0137 cur-eeb164b3a4-scheduled-commitment-sender-uniqueness-uses-caller-identity

- Title: Scheduled commitment sender uniqueness uses caller identity
- Subsystem: scheduler
- Missing behavior: verify_nonce_locks does not use scheduled_tx.caller for async commitment sender uniqueness. It identifies scheduled origins and continues before commitment_senders insertion; OriginalTransaction::sender for Scheduled recovers the signer/system sender rather than the embedded caller.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-alloy-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Async commitment nonce-lock tests for scheduled origins sharing caller identity.
- Artifact: invariants/invariant-0137.json

## invariant-0139 cur-c1e13e6b63-agent-commitments-expose-phase-deadline

- Title: CLI agent commitments expose Phase 2 deadline
- Subsystem: precompile pricing
- Missing behavior: Missing CLI_AGENT_PRECOMPILE Phase 2 deadline support. phase2_deadline_offset handles FHE, SOVEREIGN_AGENT_PRECOMPILE, PERSISTENT_AGENT_PRECOMPILE, LONG_RUNNING_HTTP, ZK, IMAGE/AUDIO/VIDEO, but no CLI_AGENT_PRECOMPILE branch was found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Async pool Phase 2 deadline tests for CLI_AGENT_PRECOMPILE commitments.
- Artifact: invariants/invariant-0139.json

## invariant-0140 cur-8a5490d454-agent-escrow-uses-specific-limits

- Title: CLI agent escrow uses CLI-specific limits
- Subsystem: executor delivery
- Missing behavior: Missing CLI-agent-specific escrow pricing. wallet.rs prices SOVEREIGN_AGENT_PRECOMPILE with SOVEREIGN_AGENT_MAX_ITERATIONS and SOVEREIGN_AGENT_MAX_TOOL_CALLS plus persistent-agent handling, but no CLI_AGENT_PRECOMPILE branch or CLI_AGENT_MAX constants were found.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Wallet fee verification tests for standard agent versus CLI agent precompiles.
- Artifact: invariants/invariant-0140.json

## invariant-0179 cur-f9ff9c44b5-async-precompile-metadata-carried-detection-through-fulfilled-execution

- Title: Async precompile metadata is carried from detection through fulfilled execution
- Subsystem: precompile pricing
- Missing behavior: Missing end-to-end preservation of caller address and program counter from detection through commitment/SPC metadata and fulfilled execution; address, input, result/proof, and commit block are partially preserved, but the full callsite metadata required by the invariant is dropped.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Execute an async call from a known contract and program counter, then inspect the produced commitment, txpool metadata, fulfilled original transaction, and pending SPC call; current local structures should lack caller_address and program_counter after the inspector stage.
- Artifact: invariants/invariant-0179.json

## invariant-0180 cur-8bbad6e2b0-async-commitment-validation-binds-supported-precompile-metadata-replay

- Title: Async commitment validation binds supported precompile metadata to replay
- Subsystem: precompile pricing
- Missing behavior: Missing the full bounded static commitment envelope for commit block, expiry, and historical lookback, and no stored commitment block/target-block comparison is available for the verifier to enforce.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Construct a commitment whose origin transaction would only match outside the allowed historical window or with a future/stale commit block; current local commitment format and verifier lack the fields/checks needed to reject on that basis alone.
- Artifact: invariants/invariant-0180.json

## invariant-0181 cur-1bd607be3c-agent-settlement-uses-work-based-pricing-delivery-fields

- Title: CLI Agent settlement uses work-based pricing and CLI delivery fields
- Subsystem: executor delivery
- Missing behavior: Missing a CLI/0x080C delivery decoder that uses fields 6-10 and forces delivery value to zero; current shared two-phase decoder consumes field 11 as callback_value, which is the agent type field in the 0x080C ABI.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Build a 0x080C delivery request with sovereign_agent_type=1 and otherwise zero callback value semantics; current decode_delivery_config_at(input, 6) will treat field 11 as a nonzero callback_value instead of forcing zero.
- Artifact: invariants/invariant-0181.json

## invariant-0183 cur-a73145efc8-builder-verifier-active-duplicate-checks

- Title: Builder and verifier use active-job duplicate checks
- Subsystem: executor delivery
- Missing behavior: Missing regular async builder duplicate checking with job_exists_and_active; scheduled builder and verifier active-job checks are present, but the regular short-async collection path does not reject duplicate commitments only on active jobs.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Put an active AsyncJobTracker job for a regular async origin tx hash, then build a payload with the same original transaction; current local code should reach commitment construction because the regular path has no origin-hash job_exists_and_active precheck.
- Artifact: invariants/invariant-0183.json

## invariant-0185 cur-0341c4ea4c-builder-verifier-share-delivery-extraction-semantics

- Title: Builder and verifier share delivery extraction semantics
- Subsystem: executor delivery
- Missing behavior: Missing shared ritual-async-fees extraction semantics for image, audio, and video Phase 2 delivery metadata, and the local builder/verifier reject those two-phase families instead of using common offsets and helpers.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Encode Phase 2 delivery results for image, audio, and video with known dimensions/durations and attempt builder/verifier settlement fee calculation; current local code should reject the families as unsupported or fail fee calculation instead of extracting shared metrics.
- Artifact: invariants/invariant-0185.json

## invariant-0189 cur-f005814a67-delivery-callbacks-defer-into-nested-async

- Title: Delivery callbacks can defer into nested async
- Subsystem: executor delivery
- Missing behavior: Missing builder logic that simulates delivery callbacks, detects nested async precompile calls, checks the original user wallet for the nested job, executes a nested commitment transaction, and defers direct delivery execution.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Use a Phase 2 delivery callback that invokes an async precompile with sufficient user wallet balance; current local builder should execute the delivery settlement directly rather than replacing it with a nested commitment and deferring delivery.
- Artifact: invariants/invariant-0189.json

## invariant-0191 cur-47c5879830-delivery-calls-verified-using-original-hash

- Title: Delivery SPC calls are verified using original transaction hash
- Subsystem: executor delivery
- Missing behavior: Missing verifier enforcement that a delivery settlement contains at most one delivery_spc_call; extra calls can be ignored if one matching valid call is present.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create a delivery settlement containing one valid matching delivery_spc_call plus a second extra call; current verifier should find and verify the matching call instead of rejecting the transaction for cardinality.
- Artifact: invariants/invariant-0191.json

## invariant-0192 cur-fe7502f434-agentruntime-values-explicit-validated

- Title: AgentRuntime values are explicit and validated
- Subsystem: precompile pricing
- Missing behavior: Missing AgentRuntime API string mapping from ZeroClaw/OpenClaw/Hermes to zeroclaw/openclaw/hermes in the audited port/dependency repos.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Decode agent_runtime values 0, 1, 2, and 3; the first three decode and value 3 rejects, but any code requiring runtime.to_api_string() or equivalent string emission is absent in the audited repos.
- Artifact: invariants/invariant-0192.json

## invariant-0193 cur-6a98ac759a-delivery-config-uses-decoder

- Title: FHE delivery config uses FHE ABI decoder
- Subsystem: executor delivery
- Missing behavior: Missing reachable FHE Phase 2 delivery settlement decoding via DeliveryConfig::from_fhe_abi; the local builder/verifier reject FHE before delivery settlement construction/verification.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit an FHE delivery-ready job with FHE-layout callback fields; current local prepare_delivery_settlement_transaction should reject the precompile as unsupported before a DeliveryConfig::from_fhe_abi-style decode can occur.
- Artifact: invariants/invariant-0193.json

## invariant-0196 cur-111f55932f-delivery-result-submission-retries-pool-lookup

- Title: Delivery result submission retries pool lookup
- Subsystem: executor delivery
- Missing behavior: Missing submitDeliveryResult retry loop of 10 pool lookups with 100 ms sleeps before not-found failure.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Mock an initially absent async pool entry that appears after several lookups; current local submitDeliveryResult should still fail after the first pool submission path.
- Artifact: invariants/invariant-0196.json

## invariant-0198 cur-c0e00637b2-delivery-settlement-collection-bounded

- Title: Delivery settlement collection is bounded
- Subsystem: executor delivery
- Missing behavior: Missing Phase C skip when the build deadline has already elapsed and missing configurable cap/default 64 on delivery-ready transaction collection.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Set RETH_MAX_DELIVERY_PER_BLOCK=1 with multiple DeliveryReady jobs; current local collection has no env-var cap to enforce one entry.
- Artifact: invariants/invariant-0198.json

## invariant-0199 cur-31accf23aa-delivery-settlements-capped

- Title: Delivery settlements are capped
- Subsystem: executor delivery
- Missing behavior: Missing default-64/environment cap and deadline-expired skip for Phase C delivery settlement collection.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Force the builder deadline into the past before Phase C and observe that current code still calls get_delivery_ready_original_async_transactions before the later execution deadline check.
- Artifact: invariants/invariant-0199.json

## invariant-0202 cur-c49a706fb2-delivery-submit-recovers-missed-awaiting-transition

- Title: Delivery submit recovers missed awaiting transition
- Subsystem: executor delivery
- Missing behavior: Missing recovery path that accepts delivery while Fulfilled, releases the sender lock, transitions to AwaitingDelivery, stores delivery data, and then moves to DeliveryReady.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Place a two-phase async entry in Fulfilled and call submit_delivery_result_with_context; current code should return InvalidState(Fulfilled), not recover to DeliveryReady.
- Artifact: invariants/invariant-0202.json

## invariant-0203 cur-71b2e7f108-delivery-uses-field-deadline-delivery-config

- Title: FHE delivery ABI uses field 10 deadline and FHE delivery config
- Subsystem: executor delivery
- Missing behavior: Missing reachable FHE Phase 2 delivery settlement support that uses field-10 deadline and field-11-through-16 callback config in both builder and verifier.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit an FHE two-phase job with field 10 and fields 11-16 populated; current local builder/verifier should reject FHE as unsupported before creating/verifying a delivery settlement.
- Artifact: invariants/invariant-0203.json

## invariant-0207 cur-bbd1426b56-error-deliveries-constant

- Title: DA error deliveries use constant fee
- Subsystem: executor delivery
- Missing behavior: Missing canonical hasError=true detection and deterministic DA error Phase 2 fee calculation in both payload builder and verifier.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Construct an image/audio/video/FHE Phase 2 delivery result with ABI slot 0 set true; current audited code has no DA error path and should reject these families or use normal fee logic if made reachable.
- Artifact: invariants/invariant-0207.json

## invariant-0208 cur-67b8ed9708-error-deliveries-have-covered-constant

- Title: DA error deliveries have covered constant fee
- Subsystem: executor delivery
- Missing behavior: Missing deterministic 500,000,000,000 wei DA error Phase 2 fee constant and assertions that it is covered by all relevant Phase 1 fees.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Add a unit check for DA_ERROR_PHASE2_FEE_WEI <= image/audio/video/FHE Phase 1 fees; it cannot be written against current audited code because the constant is absent.
- Artifact: invariants/invariant-0208.json

## invariant-0209 cur-2899238095-ethereum-launches-async-detection

- Title: Ethereum node launches async detection
- Subsystem: executor delivery
- Missing behavior: Missing construction of AsyncDetectionService from node provider and pool and missing task_executor spawn of async_detection_service.start().
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instrument EthereumAddOns::launch_add_ons with a recording task executor; current local code should spawn no AsyncDetectionService task.
- Artifact: invariants/invariant-0209.json

## invariant-0210 cur-1bd05853c6-binary-launches-ritualnode-wrapper

- Title: Ritual binary launches RitualNode wrapper
- Subsystem: executor delivery
- Missing behavior: Missing binary launch path that instantiates RitualNode rather than EthereumNode and exposes the wrapper add-ons as the node runtime.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Start or compile the binary launch path and assert its NodeBuilder type is RitualNode; current code selects EthereumNode instead.
- Artifact: invariants/invariant-0210.json

## invariant-0211 cur-897b017820-ritualnode-uses-ethereum-builders

- Title: RitualNode uses Ethereum builders
- Subsystem: executor delivery
- Missing behavior: Missing RitualNode::components configuration that uses EthereumPayloadBuilder and EthereumExecutorBuilder directly with no Ritual wrapper builders.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instantiate RitualNode::components in a compile-time assertion expecting EthereumPayloadBuilder/EthereumExecutorBuilder; current code should fail because it selects RitualPayloadBuilderBuilder/RitualExecutorBuilder.
- Artifact: invariants/invariant-0211.json

## invariant-0214 cur-b9d049ee8d-start-scheduling-service

- Title: Add-ons start scheduling service
- Subsystem: executor delivery
- Missing behavior: Missing creation of ScheduledTxService with node provider, pool, and configured scheduler address, and missing task executor spawn of service.start().
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Launch RitualAddOns with a recording task executor; current audited nodebuilder code should not spawn ScheduledTxService::start.
- Artifact: invariants/invariant-0214.json

## invariant-0215 cur-be463ed668-async-lifecycle-states-explicit

- Title: Async lifecycle states are explicit
- Subsystem: executor delivery
- Missing behavior: Missing explicit PreCommit async lifecycle state and transition from PreCommit to AwaitingExecution after the generated system transaction becomes canonical.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Exercise pool admission before a commitment transaction is canonical; current code has no PreCommit state to assert and add_metadata requires commitment_tx.
- Artifact: invariants/invariant-0215.json

## invariant-0218 cur-be7237b584-async-results-require-external-verification

- Title: Async results require external verification
- Subsystem: executor delivery
- Missing behavior: Missing unconditional external verification-service POST for every known async result before pool update.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit a result for an SPC block-verified precompile and assert no VerificationClient POST occurs; the current verifier can accept via local signature verification instead.
- Artifact: invariants/invariant-0218.json

## invariant-0220 cur-dbd3c02b99-verification-request-includes-execution-context

- Title: Verification request includes execution context
- Subsystem: executor delivery
- Missing behavior: Missing serialized maxTimeUntilTimeoutMs in the verification request context.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Serialize the current rpc-api VerificationRequest and SpcVerificationRequest and assert maxTimeUntilTimeoutMs is absent.
- Artifact: invariants/invariant-0220.json

## invariant-0221 cur-f233363780-executed-persist-pending-calls

- Title: Executed transactions persist pending SPC calls
- Subsystem: executor delivery
- Missing behavior: Missing async-context-gated extraction and injection of pending SPC calls into executed recovered transactions in the block executor storage path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Execute a Legacy/EIP-1559 transaction that records pending SPC calls in async context and inspect the block executor stored transaction; current execute.rs has no injection path to populate spc_calls.
- Artifact: invariants/invariant-0221.json

## invariant-0222 cur-9be3c0f8b0-async-http-calls-require-executor-address

- Title: Async HTTP calls require RLP executor address
- Subsystem: executor delivery
- Missing behavior: Missing RLP input decoding that treats the first item as executor address and rejects invalid/non-address RLP for HTTP async detection.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Pass an RLP-list HTTP_CALL input with a first Address and otherwise non-ABI payload; current ABI decoder should reject it instead of producing AsyncCallResult.executor_address.
- Artifact: invariants/invariant-0222.json

## invariant-0227 cur-1bcb8db91d-executor-verification-bypass

- Title: RPC executor verification bypass
- Subsystem: executor delivery
- Missing behavior: Missing unconditional verification bypass that returns success for arbitrary transaction hash and executor without metadata/proof validation.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call submitAsyncResult with a nonexistent tx hash or invalid executor; current code should fail while loading job context or verifier registry instead of returning success.
- Artifact: invariants/invariant-0227.json

## invariant-0229 cur-5f5ea62927-single-slot-registry-service-ignores-reorg-notifications

- Title: Single-slot registry service ignores reorg notifications
- Subsystem: executor delivery
- Missing behavior: Missing single-slot ExecutorRegistryService behavior that receives Reorg notifications and ignores them without mutating the registry.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instantiate the expected registry service with a mock canonical notification stream emitting Reorg; current audited code has no service type to construct or exercise.
- Artifact: invariants/invariant-0229.json

## invariant-0232 cur-e76bc78774-registry-cleanup-preserves-active-executors

- Title: Registry cleanup preserves active executors
- Subsystem: executor delivery
- Missing behavior: Missing cleanup behavior that removes expired inactive executors after a cleanup interval while retaining active executors older than TTL.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create old active and inactive executor records and trigger the expected cleanup path; current registry has no cleanup API or TTL setting to exercise.
- Artifact: invariants/invariant-0232.json

## invariant-0236 cur-6843f93f7e-executor-registry-apis-remain-public

- Title: Executor registry APIs remain public
- Subsystem: executor delivery
- Missing behavior: The crate root does not publicly expose a service module or ExecutorRegistryService, so downstream users cannot import the full API named by the invariant.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Add a downstream compile test importing ritual_spc_verification::{service, ExecutorRegistryService, ExecutorRegistry, ExecutorRegistryConfig, ExecutorRegistryStats, ExecutorInfo}; it should currently fail on service and ExecutorRegistryService.
- Artifact: invariants/invariant-0236.json

## invariant-0238 cur-41bd576139-configured-verifier-gates-block-execution

- Title: Configured SPC verifier gates block execution
- Subsystem: executor delivery
- Missing behavior: No audited executor path runs configured SPC batch verification before pre-execution changes and transaction execution, and no verifier failure can stop the block at that pre-execution point.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Configure a verifier that always fails, execute a block with SPC calls, and assert execution stops before apply_pre_execution_changes; the current executor reaches setup without such a verifier call.
- Artifact: invariants/invariant-0238.json

## invariant-0239 cur-7da36707fa-calls-batched-block

- Title: SPC calls are batched from block transactions
- Subsystem: executor delivery
- Missing behavior: The block executor does not aggregate all transaction SPC calls into SpcVerificationRequest values or submit them to one verifier batch.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instrument SpcVerifier::verify_batch and execute a block with two SPC-bearing transactions; assert one batch receives both requests. The current audited code has no such call site.
- Artifact: invariants/invariant-0239.json

## invariant-0240 cur-995ceb6781-builder-injects-verifier

- Title: Node builder injects SPC verifier
- Subsystem: executor delivery
- Missing behavior: Ethereum node component construction does not create and inject a verifier-backed executor provider.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instantiate Ethereum node components and assert the executor provider contains an SPC verifier; the current port only wires a verifier into the RPC module.
- Artifact: invariants/invariant-0240.json

## invariant-0241 cur-5ad9d3de66-verifier-registry-starts-bounded

- Title: SPC verifier registry starts bounded
- Subsystem: executor delivery
- Missing behavior: The verifier-created registry does not initialize or preserve executor_ttl=3600 seconds.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Inspect the node-created verifier registry config and assert max_executors=100 plus executor_ttl=3600; current registry has no TTL field.
- Artifact: invariants/invariant-0241.json

## invariant-0242 cur-92e2da6790-both-execution-paths-batch-verification

- Title: Both execution paths run SPC batch verification
- Subsystem: executor delivery
- Missing behavior: Both block execution paths lack the configured pre-strategy SPC batch verification step.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Invoke execute_one and execute_one_with_state_hook with a failing SPC batch verifier and assert both fail before strategy construction; current paths do not call the batch verifier.
- Artifact: invariants/invariant-0242.json

## invariant-0244 cur-6f2726fe02-builder-context-shares-verifier

- Title: Builder context shares SPC verifier
- Subsystem: executor delivery
- Missing behavior: BuilderContext does not allocate, store, expose, or share a single SPC verifier instance.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Compile a BuilderContext test that calls ctx.spc_verifier() and verifies pointer equality across RPC/executor users; the current port BuilderContext has no such accessor.
- Artifact: invariants/invariant-0244.json

## invariant-0250 cur-7ed9647c89-http-calls-verified-here

- Title: Non-HTTP SPC calls are not verified here
- Subsystem: executor delivery
- Missing behavior: There is no block execution pass that skips non-HTTP SPC calls before HTTP verifier submission; the current verifier treats non-HTTP SPC block-verified precompiles as verification candidates.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Include a non-HTTP SPC block-verified precompile in a settlement block and assert the old HTTP-only execution verifier skips it; current verification treats non-HTTP precompiles as candidates.
- Artifact: invariants/invariant-0250.json

## invariant-0251 cur-93f32a2f94-executor-registry-config-honors-defaults

- Title: Executor registry config honors env defaults
- Subsystem: executor delivery
- Missing behavior: from_env does not read TEEDA_CONTRACT_ADDRESS, EXECUTOR_REGISTRY_MAX_SIZE, or EXECUTOR_REGISTRY_TTL with the required Address::ZERO/1000/3600 fallback behavior.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Run from_env with TEEDA_CONTRACT_ADDRESS, EXECUTOR_REGISTRY_MAX_SIZE, and EXECUTOR_REGISTRY_TTL unset/invalid/valid and assert Address::ZERO/1000/3600 fallback semantics; current code uses different variables and no TTL.
- Artifact: invariants/invariant-0251.json

## invariant-0252 cur-f2d9727ec8-teeda-logs-detected-block-receipts

- Title: TeeDA logs are detected from block receipts
- Subsystem: executor delivery
- Missing behavior: ExecutorRegistryService does not fetch block receipts or identify TeeDA-address logs.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Provide a mock provider with TeeDA and non-TeeDA receipt logs and assert ExecutorRegistryService detects only TeeDA logs; the service type is absent.
- Artifact: invariants/invariant-0252.json

## invariant-0253 cur-10e602d8c4-builder-startup-launches-executor-registry-service

- Title: Builder startup launches executor registry service
- Subsystem: executor delivery
- Missing behavior: Builder startup does not create or spawn a background ExecutorRegistryService with the shared registry.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Construct BuilderContext::new with an instrumented TaskExecutor and assert it spawns ExecutorRegistryService with the shared registry; current construction performs no spawn.
- Artifact: invariants/invariant-0253.json

## invariant-0254 cur-160ad82643-registry-service-failures-abort-builder-construction

- Title: Registry service failures do not abort builder construction
- Subsystem: executor delivery
- Missing behavior: There is no registry service startup failure path that logs errors without aborting BuilderContext construction.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Force ExecutorRegistryService::start to return an error and assert BuilderContext::new still returns while logging; current code lacks the service and error-handling path.
- Artifact: invariants/invariant-0254.json

## invariant-0257 cur-f5b2f3d0ce-teeda-logs-dispatch-event-signature

- Title: TeeDA logs dispatch by event signature
- Subsystem: executor delivery
- Missing behavior: No audited repo contains a TeeDA log service that inspects topic[0] and dispatches ExecutorRegistered, ExecutorDeactivated, and ExecutorUpdated handlers while debug-logging unknown signatures.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Feed TeeDA receipt logs with registered, deactivated, updated, and unknown signatures to a service handler; current audited code has no handler to exercise.
- Artifact: invariants/invariant-0257.json

## invariant-0258 cur-80e8771e35-register-update-events-activate-payment-address

- Title: Register and update events activate payment address
- Subsystem: executor delivery
- Missing behavior: No audited repo handles ExecutorRegistered or ExecutorUpdated logs by extracting owner and paymentAddress topics and registering an active ExecutorInfo keyed by paymentAddress.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit registered and updated TeeDA logs with distinct owner and paymentAddress topics; current code has no event handler that would update the in-memory registry from those logs.
- Artifact: invariants/invariant-0258.json

## invariant-0259 cur-2cd055f454-deactivate-events-mark-owner-inactive

- Title: Deactivate events mark owner inactive
- Subsystem: executor delivery
- Missing behavior: No audited repo handles ExecutorDeactivated logs by extracting topic[1], deactivating that owner, and rejecting missing owner topics as InvalidEventData.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Feed an ExecutorDeactivated log with and without topic[1]; current code has no log handler that deactivates the owner or returns InvalidEventData.
- Artifact: invariants/invariant-0259.json

## invariant-0262 cur-e944167789-executor-events-populate-full-registry-metadata

- Title: Executor events populate full registry metadata
- Subsystem: executor delivery
- Missing behavior: No audited repo handles TeeDA ExecutorRegistered or ExecutorUpdated logs with non-indexed publicKey/capabilities/teeType/attestation fields and populates an in-memory registry entry from those emitted fields.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Feed new-signature TeeDA registered/updated logs with known public key and metadata; current code has no event handler to populate the registry from those logs.
- Artifact: invariants/invariant-0262.json

## invariant-0265 cur-97ef244d57-verifier-logs-specific-failure-labels

- Title: SPC verifier logs specific failure labels
- Subsystem: executor delivery
- Missing behavior: The verifier does not call log_tx_error with spc_invalid_signature_length, spc_json_serialization_failed, spc_signature_parsing_failed, or spc_pubkey_recovery_failed on the corresponding failure branches.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Exercise invalid signature length, JSON serialization failure, signature parsing failure, and public-key recovery failure with a tracing/metrics subscriber and assert the specific labels are absent.
- Artifact: invariants/invariant-0265.json

## invariant-0267 cur-642dee4507-pending-async-jobs-discoverable

- Title: Pending async jobs discoverable by RPC
- Subsystem: executor delivery
- Missing behavior: The endpoint does not simulate pending pool transactions against the best block header and does not return the discovered executor field required by the invariant.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Add a pending transaction that has not yet produced async metadata, call ritual_getPendingAsyncJobs, and assert the current endpoint cannot discover it by simulation or return an executor field.
- Artifact: invariants/invariant-0267.json

## invariant-0269 cur-b5ac3b002a-http-call-requests-validated-typed-decoding

- Title: HTTP call requests use validated typed ABI decoding
- Subsystem: executor delivery
- Missing behavior: HTTP method validation does not accept method value 0 and does accept method value 7, instead of accepting only values 0 through 6.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Decode HTTP call payloads with method 0, 6, and 7; current code rejects 0 and accepts 7, contrary to the invariant.
- Artifact: invariants/invariant-0269.json

## invariant-0274 cur-01892753fa-async-settlement-encodes-executor-validator-recipients

- Title: Async settlement encodes executor and validator recipients
- Subsystem: executor delivery
- Missing behavior: No audited repo reads VALIDATOR_ADDRESS or applies a non-zero fallback for inclusion validator when encoding async settlement calldata; the builder uses payload attributes.suggested_fee_recipient instead.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-alloy-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Unset and set VALIDATOR_ADDRESS while building an async settlement; current code has no env read, so inclusion_validator follows suggested_fee_recipient rather than the documented fallback rule.
- Artifact: invariants/invariant-0274.json

## invariant-0276 cur-e2283b96b7-block-verifier-receives-pool

- Title: Block verifier receives transaction pool
- Subsystem: executor delivery
- Missing behavior: The audited port does not build the transaction pool before EVM construction or invoke a pool-aware executor builder from the component construction path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Instantiate RitualNode components and assert the component builder calls a pool-aware executor construction path; current code should fail because build_evm runs before build_pool.
- Artifact: invariants/invariant-0276.json

## invariant-0279 cur-9a1c0fb822-async-settlements-match-pool-metadata-fixed-fees

- Title: Async settlements match pool metadata and fixed fees
- Subsystem: executor delivery
- Missing behavior: No audited implementation finds the original async execution metadata in the async pool for each settlement or enforces executor_fee, commitment_fee, and inclusion_fee as fixed 0.01 ETH values.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create a settlement with AsyncJobTracker-compatible dynamic fees that differ from 0.01 ETH; the current verifier follows calculated fees rather than rejecting solely because the three fees are not fixed 0.01 ETH.
- Artifact: invariants/invariant-0279.json

## invariant-0287 cur-bbee351c4c-async-commitment-codec-preserves-fields

- Title: Async commitment codec preserves all fields
- Subsystem: executor delivery
- Missing behavior: TxAsyncCommitment compact encoding cannot preserve program_counter or caller_address because those fields are absent from the current transaction type and codec.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Attempt to construct a TxAsyncCommitment with distinct program_counter and caller_address and round-trip through the compact codec; current types have no fields to encode or assert.
- Artifact: invariants/invariant-0287.json

## invariant-0290 cur-ba3aebc329-requests-real-previous-headers

- Title: SPC requests use real previous headers
- Subsystem: executor delivery
- Missing behavior: No audited block-execution path converts block SPC calls into verification requests using freshly fetched previous-header hash/timestamp data or fails block execution when that header lookup is missing.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Mock SpcVerifier::get_previous_block_data to fail for an SPC call referenced block and execute a block; current code has no extraction path that would call the mock and abort execution for the missing header.
- Artifact: invariants/invariant-0290.json

## invariant-0299 cur-c40724167f-block-execution-emits-phase-timings

- Title: Block execution emits phase timings
- Subsystem: executor delivery
- Missing behavior: No audited repo emits the required block_execute_spc_batch lifecycle phase in normal and state-hook block execution paths.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Execute blocks through execute_one and execute_one_with_state_hook and assert lifecycle logs include block_execute_spc_batch; current code emits registry_update/setup/transactions/consensus/finalization but no SPC batch phase.
- Artifact: invariants/invariant-0299.json

## invariant-0303 cur-5d024cd2a2-executor-request-base-fields-extensibly-decoded

- Title: Executor request base fields are extensibly decoded
- Subsystem: executor delivery
- Missing behavior: The audited code does not implement a manual extensible base-prefix decoder that recovers only executor/encrypted_secrets/ttl from the first ABI words while tolerating arbitrary trailing request-specific fields.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: ABI-encode executor/encrypted_secrets/ttl followed by extra request-specific fields without the port-required five-field tuple and assert current decode_base_fields fails instead of recovering the base prefix.
- Artifact: invariants/invariant-0303.json

## invariant-0305 cur-4ccbfd9dd5-executor-requests-decode-fields-manually

- Title: Executor requests decode ABI fields manually
- Subsystem: executor delivery
- Missing behavior: The audited code does not manually read executor from word 0, encrypted_secrets from word 1 offset, and ttl from word 2 with explicit zero-offset empty-secrets and bounds/overflow errors.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Feed a zero-offset empty-secrets payload and malformed offset/length cases to the current decoder; it should not exercise the invariant-specified manual parsing behavior.
- Artifact: invariants/invariant-0305.json

## invariant-0306 cur-67a93af110-executor-requests-carry-secret-signatures

- Title: Executor requests carry secret signatures
- Subsystem: executor delivery
- Missing behavior: The base executor request ABI is no longer exactly executor/encrypted_secrets/ttl/secret_signature, and decode_base_fields does not return only the secret_signature bytes as the fourth and final decoded value with a four-field minimum size.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: ABI-encode exactly executor, encrypted_secrets, ttl, and secret_signature and assert current decode_base_fields rejects it or requires user_public_key, contrary to the invariant.
- Artifact: invariants/invariant-0306.json

## invariant-0308 cur-3d120240fc-http-executor-prices-normalized-constants

- Title: HTTP executor prices use normalized constants
- Subsystem: executor delivery
- Missing behavior: HTTP executor fee calculation does not use the required normalized constants: base 25,000,000,000,000 wei and 3,500,000,000 wei per input/output byte.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Compute http_executor_fee for known input/output lengths and assert current output uses 2_500_000_000_000 + 350_000_000 per byte, not the invariant-required values.
- Artifact: invariants/invariant-0308.json

## invariant-0311 cur-e38bfc329c-http-executor-fees-revised-byte-pricing

- Title: HTTP executor fees use revised byte pricing
- Subsystem: executor delivery
- Missing behavior: HTTP executor fee calculation does not use the revised byte pricing values 25,000,000,000,000 wei base and 3,500,000,000 wei per input/output byte.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Assert http_executor_fee(input_len, output_len) equals 25_000_000_000_000 + 3_500_000_000*(input_len+output_len); current code should fail.
- Artifact: invariants/invariant-0311.json

## invariant-0316 cur-08eabe0c5f-registry-service-watches-executorregistry-contract

- Title: Registry service watches ExecutorRegistry contract
- Subsystem: executor delivery
- Missing behavior: No local audited repo contains an SPC registry service that watches EXECUTOR_REGISTRY_CONTRACT_ADDRESS, applies the new ExecutorRegistry default address, or ignores old TeeDA/TEE service configuration by using the ExecutorRegistry log source.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Set EXECUTOR_REGISTRY_CONTRACT_ADDRESS to a test contract and emit ExecutorRegistry logs; the current local code has no service/log path expected to consume them.
- Artifact: invariants/invariant-0316.json

## invariant-0317 cur-02fe890f0a-registration-events-store-executorregistry-fields

- Title: Registration events store ExecutorRegistry fields
- Subsystem: executor delivery
- Missing behavior: No local audited repo decodes ExecutorRegistered or ExecutorUpdated logs into paymentAddress/teeAddress indexed fields plus teeType, workloadId, capability, and publicKey, nor rejects capability values outside 0..=1 in that event path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Feed a valid new ExecutorRegistered log to the local port; no log handler exists to populate ExecutorInfo from it.
- Artifact: invariants/invariant-0317.json

## invariant-0318 cur-36256e288c-executorwentoffline-deactivates-payment-address

- Title: ExecutorWentOffline deactivates payment address
- Subsystem: executor delivery
- Missing behavior: No local audited repo handles ExecutorWentOffline(address indexed paymentAddress) logs or rejects malformed logs missing topic[1]; the only deactivation method is an in-memory helper with no event dispatch caller.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Register an executor then process an ExecutorWentOffline log; the current local code has no handler to process that log or deactivate by payment address.
- Artifact: invariants/invariant-0318.json

## invariant-0320 cur-f4c9303fca-executor-events-decode-data-bytes

- Title: Executor events decode from log data bytes
- Subsystem: executor delivery
- Missing behavior: No local audited repo contains ExecutorRegistered or ExecutorUpdated log decoding from log.data.as_ref(), nor any payload-length reporting path for those event payload bytes.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create Alloy logs with ABI data for ExecutorRegistered/Updated; no local handler exists to decode log.data.as_ref() or report payload length.
- Artifact: invariants/invariant-0320.json

## invariant-0321 cur-c60b71f77f-executor-events-decode-registry-payload

- Title: Executor events decode new registry payload
- Subsystem: executor delivery
- Missing behavior: No local audited repo decodes ExecutorRegistered/ExecutorUpdated logs as indexed paymentAddress/teeAddress topics plus non-indexed teeType, workloadId, capability, and dynamic publicKey fields into the in-memory registry.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Feed a valid new registry event and assert no local log handler updates the in-memory registry.
- Artifact: invariants/invariant-0321.json

## invariant-0322 cur-34be1f8359-malformed-executor-event-payloads-rejected

- Title: Malformed executor event payloads are rejected
- Subsystem: executor delivery
- Missing behavior: No local audited repo has an ExecutorRegistry event handler that rejects short event data, a non-128 publicKey offset, publicKey overrun, or capability outside 0..=1 before mutating registry state.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit malformed ExecutorRegistry event payloads; there is no local event handler expected to return InvalidEventData or prevent event-based mutation.
- Artifact: invariants/invariant-0322.json

## invariant-0323 cur-25bb845264-executorregistry-logs-replace-teeda-logs

- Title: ExecutorRegistry logs replace TeeDA logs
- Subsystem: executor delivery
- Missing behavior: No local audited repo monitors configured ExecutorRegistry logs or recognizes ExecutorRegistered, ExecutorWentOffline, and ExecutorUpdated event signatures in place of old TeeDA signatures.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Feed new and old event signatures into the current local node; no registry log service exists to distinguish or apply them.
- Artifact: invariants/invariant-0323.json

## invariant-0324 cur-fd8eba7c32-executor-events-decode-identity-fields

- Title: Executor events decode new identity fields
- Subsystem: executor delivery
- Missing behavior: No local audited repo has event handling that decodes paymentAddress/teeAddress from topics, validates the dynamic publicKey layout, rejects capability > 1, and stores those decoded identity fields from ExecutorRegistry logs.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Construct valid and invalid ExecutorRegistry logs and assert the current local code has no handler to store or reject them.
- Artifact: invariants/invariant-0324.json

## invariant-0325 cur-1cd8d8cf9b-offline-events-deactivate-payment-address

- Title: Offline events deactivate payment address
- Subsystem: executor delivery
- Missing behavior: No local audited repo handles ExecutorWentOffline logs to deactivate the executor keyed by indexed paymentAddress; the old/new offline event dispatch path is missing entirely.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: After registering an executor, emit ExecutorWentOffline and assert the current local code has no event path that deactivates it.
- Artifact: invariants/invariant-0325.json

## invariant-0328 cur-d305810a56-secure-deployment-addresses-defaults

- Title: Secure deployment addresses are the defaults
- Subsystem: executor delivery
- Missing behavior: The audited local code does not default executor registry/SPC components to ExecutorRegistry 0xE7fb2698439326890ae9c8d2fd51D11F461D1c28 when env overrides are absent or invalid; it uses the older TEE service registry default/env var instead.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Unset EXECUTOR_REGISTRY_CONTRACT_ADDRESS and TEE_SERVICE_REGISTRY_CONTRACT_ADDRESS, then call the local registry address helpers and assert they return 0xE7fb...; current code would return 0x9644... for the executor/TEE registry path.
- Artifact: invariants/invariant-0328.json

## invariant-0342 cur-7634162bc7-verification-uses-unified-registry-reader

- Title: SPC verification uses unified registry reader
- Subsystem: executor delivery
- Missing behavior: SPC block verification does not call the unified read_executor_public_keys helper for the specific executor set and does not map registry-reader failures into SpcExecutorRegistryReadFailed.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Force a registry read failure during verify_spc_calls and assert the current code returns InvalidSpc rather than SpcExecutorRegistryReadFailed, demonstrating the missing mapping.
- Artifact: invariants/invariant-0342.json

## invariant-0348 cur-8aa44d074c-registry-exposes-context

- Title: Registry exposes SPC job context
- Subsystem: executor delivery
- Missing behavior: read_jobs_for_spc_verification returns an error for a zero executor slot instead of skipping that requested job id while returning entries for existing jobs.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call read_jobs_for_spc_verification with one existing job and one job whose executor slot is zero; the invariant expects one returned entry, but current code errors.
- Artifact: invariants/invariant-0348.json

## invariant-0351 cur-44b85680c5-pricing-failures-fall-back

- Title: LLM pricing failures do not fall back
- Subsystem: executor delivery
- Missing behavior: LLM executor outputs that report has_error=true are priced with a constant fee instead of returning Err and causing builder skip/verifier rejection.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call calculate_async_fees for LLM output with has_error=true and assert the invariant expects Err; current code returns Ok(LLM_ERROR_EXECUTOR_FEE_WEI).
- Artifact: invariants/invariant-0351.json

## invariant-0354 cur-09fe4dfa20-pricing-fails-closed-without-fallback

- Title: LLM pricing fails closed without fallback
- Subsystem: executor delivery
- Missing behavior: The LLM no-fallback policy is incomplete: at least one unpriceable/error output path returns a constant fee instead of Err, so payload construction and verification do not fail closed for that case.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit LLM executor output with has_error=true through calculate_async_fees and assert the invariant expects Err/no settlement; current code returns a constant fee.
- Artifact: invariants/invariant-0354.json

## invariant-0355 cur-fec4cbcdb7-floating-point-conversion-rejects-invalid-totals

- Title: LLM floating-point conversion rejects invalid totals
- Subsystem: executor delivery
- Missing behavior: LLM runtime fee conversion does not reject non-finite, negative, or u128-overflowing total_wei values and successful runtime conversions are not floored at HTTP_EXECUTOR_BASE_FEE_WEI.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Drive compute_llm_executor_fee with model data/token counts that produce NaN, infinity, negative, and >u128::MAX total_wei, plus a tiny valid total; the invariant expects Err for invalid totals and at least HTTP_EXECUTOR_BASE_FEE_WEI for the valid total, while current code clamps.
- Artifact: invariants/invariant-0355.json

## invariant-0362 cur-94e6d998d2-async-settlement-fees-exact-pricing-without-fallback

- Title: Async settlement fees use exact LLM pricing without fallback
- Subsystem: executor delivery
- Missing behavior: Async settlement creation/verification does not fail closed for LLM executor outputs with has_error=true; those outputs receive a constant executor fee instead of exact LLM pricing failure.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Build a fulfilled LLM settlement whose executor output sets has_error=true and assert the invariant expects settlement creation to fail or verification to reject; current compute_llm_executor_fee returns Ok(LLM_ERROR_EXECUTOR_FEE_WEI).
- Artifact: invariants/invariant-0362.json

## invariant-0375 cur-a476fe7189-delivery-results-require-block-proof-verification

- Title: Delivery results require block and proof verification
- Subsystem: executor delivery
- Missing behavior: ritual_submitDeliveryResult accepts the request fields but does not validate supplied block_number, block_hash, or executor and does not verify the delivery proof before moving the pool entry to DeliveryReady.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call ritual_submitDeliveryResult with a mismatched blockHash or invalid delivery proof and assert the current port accepts it once the pool entry is AwaitingDelivery.
- Artifact: invariants/invariant-0375.json

## invariant-0376 cur-495bd404f2-phase-pricing-polling-plus-payload

- Title: Phase 2 pricing is polling plus payload
- Subsystem: executor delivery
- Missing behavior: Long-running HTTP Phase 2 pricing ignores delivery_result_len and charges only FEE_PER_POLL_BLOCK_WEI * blocks_polled instead of polling_fee plus http_executor_fee(0, delivery_result_len).
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: For a 0x0805 delivery with a non-empty delivery result, compare expected polling + http_executor_fee(0, len) against current calculate_async_fees_phase2 output; current output omits the payload fee.
- Artifact: invariants/invariant-0376.json

## invariant-0377 cur-45436e2824-long-running-phase-aware

- Title: Long-running TTL is Phase-aware
- Subsystem: executor delivery
- Missing behavior: The pool extracts max_poll_block and uses settlement_block + max_poll_block as the Phase 2 deadline, but no 100-block buffer constant or addition is present.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Set max_poll_block to N, mark Phase 1 settled at block B, and assert current contract_expiry_block is B+N rather than the invariant-required B+N+100.
- Artifact: invariants/invariant-0377.json

## invariant-0385 cur-f7a09116c5-malformed-phase-settlement-data-rejects-blocks

- Title: Malformed SPC and Phase 2 settlement data rejects blocks
- Subsystem: executor delivery
- Missing behavior: Block verification rejects malformed delivery-result extraction and short SPC proofs, but no local verifier path rejects a transaction merely because it carries more than one SPC call; the current code selects a matching call with any/find.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create a settlement/original transaction with two SPC calls where one matches; the invariant expects rejection, while current verification can select the matching call and continue.
- Artifact: invariants/invariant-0385.json

## invariant-0389 cur-34a1822c2c-agent-calls-long-running-async-work

- Title: Agent calls are long-running async work
- Subsystem: executor delivery
- Missing behavior: The audited local code has no 0x0808 AGENT_CALL_PRECOMPILE accepted as async/two-phase/SPC-verified work, and the related sovereign agent path at 0x080C uses HttpCall capability rather than LLM.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit a 0x0808 agent-call commitment with an LLM executor; current metadata lookup treats 0x0808 as unsupported, exposing the missing invariant behavior.
- Artifact: invariants/invariant-0389.json

## invariant-0390 cur-3a8aeeff79-agent-fees-work-based-phase

- Title: Agent fees are work-based in Phase 2
- Subsystem: executor delivery
- Missing behavior: The exact 0x0808 agent-call fee path is absent: Phase 1 calculate_async_fees does not accept 0x0808, the generic Phase 2 helper rejects it as unsupported, and builder/verifier special-case only SOVEREIGN_AGENT_PRECOMPILE at 0x080C.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call calculate_async_fees for precompile 0x0808 and expect agent Phase 1 fees; current code returns unsupported. Also verify payload/verifier only special-case 0x080C.
- Artifact: invariants/invariant-0390.json

## invariant-0391 cur-7d473f9dd4-agent-wallet-escrow-uses-worst-case-work

- Title: Agent wallet escrow uses worst-case work
- Subsystem: executor delivery
- Missing behavior: Wallet validation does not recognize a 0x0808 agent-call precompile and therefore cannot require AGENT_MAX_ITERATIONS/AGENT_MAX_TOOL_CALLS escrow for that invariant path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Run verify_wallet_for_commitment for address 0x0808 with otherwise sufficient wallet state; the current code should return unsupported instead of applying worst-case agent escrow.
- Artifact: invariants/invariant-0391.json

## invariant-0395 cur-8887904fbb-pricing-split-across-phases

- Title: FHE pricing is split across phases
- Subsystem: executor delivery
- Missing behavior: The audited port has no FHE-specific Phase 1 fixed fee helper and no Phase 2 base-plus-per-layer FHE pricing with zero validator fees.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call the port fee APIs for FHE Phase 1 and Phase 2 layer counts; the current port has no FHE pricing entrypoint and generic Phase 2 fee calculation rejects 0x0807.
- Artifact: invariants/invariant-0395.json

## invariant-0397 cur-7d3cefb063-verifier-includes-phase-callback-escrow-long-running-http

- Title: Verifier includes Phase 2 callback escrow for long-running HTTP
- Subsystem: executor delivery
- Missing behavior: Long-running HTTP wallet verification includes callback cost when it can decode it, but decode failure is fail-closed rather than the required zero callback cost path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Verify a long-running HTTP commitment with malformed DeliveryConfig fields; the invariant expects zero callback cost, while current wallet verification returns an error.
- Artifact: invariants/invariant-0397.json

## invariant-0399 cur-6948899626-capability-value-recognized-executor-service

- Title: FHE capability value is recognized as executor service
- Subsystem: executor delivery
- Missing behavior: Capability::try_from(6) does not return Capability::Fhe and Capability::try_from(7) is not invalid; the audited code maps Fhe to value 10.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Assert Capability::try_from(6) == Capability::Fhe and Capability::try_from(7).is_err(); current code returns Dkms and ImageCall respectively.
- Artifact: invariants/invariant-0399.json

## invariant-0400 cur-e876a2d713-async-payload-constraints-enforced

- Title: Async payload constraints enforced
- Subsystem: executor delivery
- Missing behavior: RPC async payload validation does not enforce the invariant-required 5KB input ceiling or 30-block TTL ceiling.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit an async HTTP payload of 6KB or TTL 31; the invariant expects InvalidParams, while the current validator accepts those bounds if other fields are valid.
- Artifact: invariants/invariant-0400.json

## invariant-0407 cur-7777516d23-wallet-escrow-uses-layer-lockup

- Title: FHE wallet escrow uses max-layer lockup
- Subsystem: executor delivery
- Missing behavior: Verifier wallet checks do not recognize FHE and therefore cannot require max-layer FHE escrow.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Run verify_wallet_for_commitment for FHE_PRECOMPILE with otherwise sufficient state; current code returns unsupported instead of applying max-layer FHE escrow.
- Artifact: invariants/invariant-0407.json

## invariant-0408 cur-23b61fad34-image-call-fees-tiered-output-dimensions

- Title: Image Call fees are tiered by output dimensions
- Subsystem: executor delivery
- Missing behavior: The audited repo set has no Reth async fee calculation that tiers Image Call Phase 2 executor fees by delivered output dimensions.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Build/verify Image Call Phase 2 settlements with representative width/height tiers; the current port has no image fee function and cannot price them by output dimensions.
- Artifact: invariants/invariant-0408.json

## invariant-0414 cur-2cbf9cff7d-async-capability-requirements-follow-precompile-type

- Title: Async RPC capability requirements follow precompile type
- Subsystem: executor delivery
- Missing behavior: RPC capability requirements do not include an Agent->Llm rule, and unknown detected async precompile addresses are rejected rather than explicitly skipping capability checks.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit or directly validate a detected 0x0808 agent async call and an unknown async precompile address; the invariant expects Llm capability for agent and no capability check for unknown, while the current port has no 0x0808 metadata and rejects unknown metadata.
- Artifact: invariants/invariant-0414.json

## invariant-0416 cur-dc90761a2c-wallet-escrow-covers-audio-video

- Title: Wallet escrow covers audio and video
- Subsystem: executor delivery
- Missing behavior: The audited v2.2 port lacks audio_escrow_lockup/video_escrow_lockup and does not require worst-case audio/video executor escrow plus commitment, inclusion, and callback costs during wallet validation.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: For audio and video async calls, run wallet validation with balances just below and just above the sum of modality escrow, commitment fee, inclusion fee, and decoded delivery callback cost; assert only the sufficient balance case is accepted.
- Artifact: invariants/invariant-0416.json

## invariant-0417 cur-6e7ccf4c8f-video-phase-pricing-uses-resolution-duration

- Title: Video Phase 2 pricing uses resolution and duration
- Subsystem: executor delivery
- Missing behavior: The audited v2.2 port lacks video Phase 2 settlement pricing that extracts width, height, and outputDurationMs and fails malformed delivery data rather than using a fallback.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create audio Phase 2 delivery results with durations in each tier and assert payload settlement creation and block verification compute matching calculate_audio_fees_phase2 values; provide too-short delivery data and assert pricing/verification fails.
- Artifact: invariants/invariant-0417.json

## invariant-0418 cur-97a7e1c0ee-audio-phase-includes-executor-commitment-minimal-inclusion-fees

- Title: Audio Phase 1 fee includes executor, commitment, and minimal inclusion fees
- Subsystem: executor delivery
- Missing behavior: The audited v2.2 port lacks calculate_audio_fees_phase1(input_len) returning executor, commitment, and zero/minimal inclusion fee for audio Phase 1.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call calculate_audio_fees_phase1 with a representative input length and assert the returned AsyncFees fields exactly match AUDIO_PHASE1_SETTLEMENT_FEE_WEI, async_commitment_fee(input_len), and async_inclusion_fee(input_len, 64).
- Artifact: invariants/invariant-0418.json

## invariant-0419 cur-12a06561cd-audio-phase-pays-executor-only

- Title: Audio Phase 2 pays executor only
- Subsystem: executor delivery
- Missing behavior: The audited v2.2 port lacks calculate_audio_fees_phase2(duration_seconds) that charges executor-only audio completion fees and zero validator fees.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call calculate_audio_fees_phase2 for several durations and assert executor_fee equals audio_phase2_execution_fee(duration) while commitment_fee and inclusion_fee are U256::ZERO.
- Artifact: invariants/invariant-0419.json

## invariant-0437 cur-3aaeab8aa4-commitment-input-stores-resolved-deadline

- Title: Commitment input stores resolved deadline
- Subsystem: executor delivery
- Missing behavior: No audited v2.2-port path writes the resolved absolute Phase 2 deadline back into field 6 of precompile_input before creating the async commitment; the port continues to treat that field as an offset.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create a scheduled two-phase commitment from input whose field 6 is an offset; inspect the commitment's precompile_input and assert field 6 contains commit_block + offset, then verify the block verifier and async pool read that field directly as the absolute deadline.
- Artifact: invariants/invariant-0437.json

## invariant-0443 cur-e4bea590db-dkms-capability-decodes-executor

- Title: DKMS capability decodes as non-executor
- Subsystem: executor delivery
- Missing behavior: Capability value 7 no longer remains unknown in the audited port; it decodes as ImageCall.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Unit-test the registry reader capability conversion and classification: bytes 0-6 map to known capabilities with 6 as Dkms, byte 7 errors, and is_executor_capability returns false for Dkms while remaining true for executor capabilities.
- Artifact: invariants/invariant-0443.json

## invariant-0445 cur-c5267c83f4-validation-task-covers-simulation-state-checks

- Title: Validation task covers simulation and state checks
- Subsystem: executor delivery
- Missing behavior: The current RPC validation task lacks the invariant-required target-block validation/current-block lookup portion of the full simulation-plus-state validation sequence.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit a regular transaction and assert `run_validation` returns `Ok(())` after simulation reports no async call; submit an async transaction with invalid target block, invalid payload, or failing state validation and assert the corresponding formatted validation error is returned.
- Artifact: invariants/invariant-0445.json

## invariant-0447 cur-4e0f3b009d-dkms-capability-recognized-executor

- Title: DKMS capability is recognized but non-executor
- Subsystem: executor delivery
- Missing behavior: Capability value 7 is recognized as ImageCall instead of being rejected as unknown.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Unit test Capability::try_from for 5, 6, and 7 and assert ZkCall, Dkms, and Err respectively; assert Dkms.is_executor_capability() is false while HTTP/LLM/ZK executor capabilities remain true.
- Artifact: invariants/invariant-0447.json

## invariant-0448 cur-9fcaa16e58-shared-async-payload-rules-gate-builder

- Title: Shared async payload rules gate RPC and builder
- Subsystem: executor delivery
- Missing behavior: Shared async validation lacks target-block extraction/range enforcement and uses a 10 KiB MAX_ASYNC_INPUT_SIZE rather than the stated 1 MiB rule.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: For each supported async precompile, submit malformed RPC payloads covering future/too-old target block, oversized input, zero executor, ttl 0, ttl above MAX_TTL_BLOCKS, invalid URL scheme, empty LLM model/messages, and empty Agent prompt; assert RPC rejects them and the shared validator returns matching errors.
- Artifact: invariants/invariant-0448.json

## invariant-0449 cur-da12d6590f-performs-full-async-state-validation

- Title: RPC performs full async state validation
- Subsystem: executor delivery
- Missing behavior: RPC async admission does not perform the invariant-required target-block validation as part of full async state validation.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit async RPC transactions with an unregistered executor, missing LLM model, insufficient wallet balance/lock duration, and invalid two-phase deadline, and assert each is rejected and removed from the pool even when static payload decoding succeeds.
- Artifact: invariants/invariant-0449.json

## invariant-0450 cur-23bae1f472-video-phase-pixel-second

- Title: Video Phase 2 is per pixel-second
- Subsystem: executor delivery
- Missing behavior: The audited v2.2 port lacks Video Phase 2 pricing that extracts width, height, and duration and charges executor fees by rounded-up pixel-seconds with zero validator fees.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Verify an image Phase 2 settlement whose delivery result encodes width and height; assert expected executor fee changes with `width * height` and malformed/missing dimensions reject the settlement.
- Artifact: invariants/invariant-0450.json

## invariant-0451 cur-6297d3b720-wallet-escrow-uses-layers

- Title: FHE wallet escrow uses max layers
- Subsystem: executor delivery
- Missing behavior: Wallet verification for FHE does not include fhe_escrow_lockup(FHE_MAX_LAYERS); FHE reaches the unsupported-precompile path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Run wallet fee verification for an FHE async request and assert total_required_fees includes fhe_escrow_lockup(FHE_MAX_LAYERS) plus commitment/inclusion/callback components.
- Artifact: invariants/invariant-0451.json

## invariant-0452 cur-772b1c47d7-awaitingexecution-move-awaiting-delivery

- Title: AwaitingExecution can move to awaiting delivery
- Subsystem: executor delivery
- Missing behavior: mark_async_awaiting_delivery does not accept AwaitingExecution; it only transitions Fulfilled entries to AwaitingDelivery.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Insert a two-phase async pool entry in AwaitingExecution and call mark_async_awaiting_delivery for its hash. Assert the transition succeeds. Repeat with an unrelated invalid state and assert InvalidState is returned.
- Artifact: invariants/invariant-0452.json

## invariant-0455 cur-fb34ce289c-multimodal-executors-require-capability

- Title: Multimodal executors require LLM capability
- Subsystem: executor delivery
- Missing behavior: The current port does not require Capability::Llm for image, audio, or video precompile executor validation; it requires ImageCall, AudioCall, and VideoCall respectively.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Validate executor registration for each multimodal precompile against a registry entry with Capability::Llm and one without it; assert only the Llm-capable executor passes under this rule.
- Artifact: invariants/invariant-0455.json

## invariant-0456 cur-d1fec9884c-multimodal-phase-uses-constant-async-fees

- Title: Multimodal Phase 1 uses constant async fees
- Subsystem: executor delivery
- Missing behavior: Phase 1 fee calculation does not return dedicated image/audio/video Phase 1 calculators; calculate_async_fees rejects those precompile addresses instead of pricing them.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call calculate_async_fees for 0x0818, 0x0819, and 0x081A with representative input lengths and assert each returns Ok from the corresponding Phase 1 fee calculator rather than an unsupported-precompile error.
- Artifact: invariants/invariant-0456.json

## invariant-0457 cur-19507e8575-multimodal-phase-fees-delivered-output-attributes

- Title: Multimodal Phase 2 fees use delivered output attributes
- Subsystem: executor delivery
- Missing behavior: Dedicated delivered-output Phase 2 pricing is absent for image and video, and the generic Phase 2 calculator rejects media addresses; only audio duration-based Phase 2 pricing is present.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Provide Phase 2 delivery results for image, audio, and video with known dimensions/duration and assert payload fee calculation uses the dedicated calculators; call the generic calculate_async_fees_phase2 with these precompile addresses and assert it returns the guidance error.
- Artifact: invariants/invariant-0457.json

## invariant-0458 cur-1eb9f518c9-verifier-mirrors-multimodal-phase-pricing

- Title: Verifier mirrors multimodal Phase 2 pricing
- Subsystem: executor delivery
- Missing behavior: Block verification does not support image/video Phase 2 settlement fee extraction and therefore cannot mirror multimodal Phase 2 pricing for all three media precompiles.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Construct Phase 2 settlement verification cases for image/audio/video where delivery results are valid and malformed; assert valid cases compute the same fees as the payload builder and malformed cases reject verification.
- Artifact: invariants/invariant-0458.json

## invariant-0459 cur-3c48364012-multimodal-precompiles-participate-async-lifecycle

- Title: Multimodal precompiles participate in async lifecycle
- Subsystem: executor delivery
- Missing behavior: Image and video do not participate through the full async lifecycle because block-verification commitment/delivery support rejects unsupported two-phase precompiles; audio is only partially supported.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit image, audio, and video async calls and assert the inspector detects them, RPC registration validation maps them to the expected capability, commitment validation accepts their precompile addresses, the pool treats them as long-running, and the verifier accepts their Phase 2 settlement path when other data is valid.
- Artifact: invariants/invariant-0459.json

## invariant-0467 cur-54e67c64a3-agent-accepts-http-executors

- Title: CLI Agent accepts HTTP or LLM executors
- Subsystem: executor delivery
- Missing behavior: The 0x080C agent precompile accepts only the HttpCall capability in current metadata/RPC validation; there is no allowed-capabilities list that also accepts Llm for CLI_AGENT_PRECOMPILE.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create executor registry entries for CLI Agent jobs with HttpCall, Llm, and ImageCall capabilities; validate_executor_registration should accept the first two and reject the third, while HTTP, LLM, image, audio, video, and ZK precompiles should still require their single mapped capability.
- Artifact: invariants/invariant-0467.json

## invariant-0468 cur-ee32a03920-video-pricing-scales-steps

- Title: Video pricing scales with steps and FPS
- Subsystem: executor delivery
- Missing behavior: Video Phase 2 executor fees are not calculated from pixel-seconds with inference-step and FPS multipliers; the port lacks video Phase 2 fee calculators and baseline constants.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Compute image Phase 2 fees for the same width and height with num_inference_steps 0, baseline, and 2x baseline; assert the first two equal the base fee and the 2x case doubles the executor fee. Compute video Phase 2 fees for identical width, height, and duration with default UX params, 2x baseline steps, 2x baseline fps, and both; assert fees scale by the expected multiplicative factors.
- Artifact: invariants/invariant-0468.json

## invariant-0469 cur-fa7cb34831-dkms-request-five-fields-secrets

- Title: DKMS request ABI has five fields and no secrets
- Subsystem: executor delivery
- Missing behavior: DkmsKeyRequest no longer has the five-field no-secrets ABI; the local codec requires eight fields including encrypted_secrets, secret_signature, and user_public_key.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Round-trip a DkmsKeyRequest through to_abi/from_abi and assert every field is preserved; then feed malformed ABI data, wrong token types, and a key_format uint256 above 255 and assert from_abi returns CodecError.
- Artifact: invariants/invariant-0469.json

## invariant-0471 cur-5d817cc607-dkms-validation-enforces-executor-only

- Title: DKMS RPC validation enforces executor and TTL only
- Subsystem: executor delivery
- Missing behavior: validate_dkms_key_payload does more than executor/TTL-only validation: it validates base encrypted secret/public key fields and rejects zero owner.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call validate_dkms_key_payload with a valid DKMS request and assert Ok; then test zero executor, ttl zero, ttl max_ttl_blocks()+1, and malformed ABI and assert ExecutorZeroAddress, TTLZero, TTLExceeded, and DecodeFailed respectively. Also assert owner zero and arbitrary key_index pass when ABI decoding succeeds.
- Artifact: invariants/invariant-0471.json

## invariant-0472 cur-0824aa0984-dkms-uses-http-style-fees-capability

- Title: DKMS uses HTTP-style fees and capability
- Subsystem: executor delivery
- Missing behavior: DKMS RPC capability validation requires HttpCall, but DKMS wallet/fee pricing uses a fixed DKMS executor fee rather than http_executor_fee(input_len, 20).
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: For DKMS_KEY_PRECOMPILE, assert wallet fee verification calculates executor_fee with http_executor_fee(input_len, 20), and assert executor registration validation accepts an executor with HttpCall capability and rejects one lacking it under this capability rule.
- Artifact: invariants/invariant-0472.json

## invariant-0476 cur-5dac64b7da-dkms-precompile-uses-http-style-executor

- Title: DKMS key precompile uses HTTP-style executor fee
- Subsystem: executor delivery
- Missing behavior: Wallet fee calculation for DKMS_KEY_PRECOMPILE does not use http_executor_fee(input_len, 20); it uses the fixed DKMS executor fee and dkms_escrow_lockup.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Validate a DKMS key async request and assert required fee/lockup equals http_executor_fee(input_len, 20), and that the DKMS codec round-trips the request format used by that precompile.
- Artifact: invariants/invariant-0476.json

## invariant-0478 cur-dee63ab7c4-multimodal-pricing-model-specific-erroring

- Title: Multimodal pricing is model-specific and erroring
- Subsystem: executor delivery
- Missing behavior: Image and video escrow/Phase 2 fee functions do not calculate from ModelInfo pricing fields or error on missing model pricing; only audio has model-specific erroring fee helpers.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: For each image, audio, and video model, call escrow and Phase 2 fee functions with valid ModelInfo and assert the fee uses that model's modality pricing; then call with zeroed pricing fields and assert an error is returned and no fallback fee is produced.
- Artifact: invariants/invariant-0478.json

## invariant-0483 cur-4d49c6d9e1-wallet-validation-uses-escrow-delivery-config

- Title: FHE wallet validation uses FHE escrow and delivery config
- Subsystem: executor delivery
- Missing behavior: Wallet validation does not support FHE_PRECOMPILE and no fhe_escrow_lockup helper exists, so FHE Phase 1 wallet escrow is not enforced through the FHE-specific escrow path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Run wallet validation for an FHE async request and assert required Phase 1 escrow is fhe_escrow_lockup; then provide FHE delivery fields at indices 11-16 and assert callback gas/value are decoded from the FHE layout, while malformed FHE delivery config returns an error.
- Artifact: invariants/invariant-0483.json

## invariant-0484 cur-6d434e854a-autonomous-agent-fees-fixed-plus-payload

- Title: Autonomous Agent fees are fixed plus payload
- Subsystem: executor delivery
- Missing behavior: No autonomous-agent fixed Phase 1 fee helper or Phase 2 AUTONOMOUS_AGENT_SPAWN_FEE_WEI plus payload-length fee calculation exists in the audited repo set.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: For an autonomous agent request of known input length and a settlement delivery result of known byte length, assert wallet validation uses calculate_autonomous_agent_fees for Phase 1 and builder/verifier both use calculate_autonomous_agent_fees_phase2 with identical totals. Mutate delivery result length and assert the payload component changes consistently.
- Artifact: invariants/invariant-0484.json

## invariant-0490 cur-3c1f46245d-missing-async-jobs-fail-registry-reads

- Title: Missing async jobs fail registry reads
- Subsystem: executor delivery
- Missing behavior: read_jobs_for_settlement does not return RegistryError when jobExecutor[job_id] is zero; it logs and continues, returning partial/empty results. Only read_jobs_for_spc_verification fails closed.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call each reader with a job ID whose jobExecutor storage slot is zero and assert the function returns RegistryError rather than omitting the job from the returned vector; call with multiple IDs and one missing job to assert no partial success is returned.
- Artifact: invariants/invariant-0490.json

## invariant-0497 cur-2b65ea452d-delivery-settlement-origins-calldata-accounting

- Title: Delivery settlement origins use calldata gas accounting
- Subsystem: executor delivery
- Missing behavior: AsyncSettlement block gas counters use calldata gas, but fee accounting still multiplies settlement gas price by actual EVM gas used rather than calldata gas.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Execute an AsyncSettlement where actual EVM gas differs from calldata gas and assert total_fees is based on calldata gas; current code would charge actual EVM gas.
- Artifact: invariants/invariant-0497.json

## invariant-0499 cur-c9941368c5-phase-delivery-proofs-cryptographically-verified

- Title: Phase 2 delivery proofs are cryptographically verified
- Subsystem: executor delivery
- Missing behavior: RPC Phase 2 delivery result submission does not cryptographically verify the delivery proof before accepting it into the async pool.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit a delivery result with a 65-byte invalid proof and assert RPC returns failure and leaves the pool state unchanged; current code would accept it if pool state permits.
- Artifact: invariants/invariant-0499.json

## invariant-0500 cur-d47655a1ad-block-verifier-validates-delivery-calls

- Title: Block verifier validates delivery SPC calls
- Subsystem: executor delivery
- Missing behavior: Block verification verifies a matching delivery SPC call but does not reject settlements containing more than one delivery_spc_call.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Build a delivery settlement with two delivery_spc_calls where one matches and assert block verification rejects the block; current verifier has no such cardinality guard.
- Artifact: invariants/invariant-0500.json

## invariant-0501 cur-222623b8ac-delivery-proofs-verified

- Title: Delivery SPC proofs are verified
- Subsystem: executor delivery
- Missing behavior: Delivery SPC calls are exposed through transaction, receipt, and storage paths and are verified, but the verifier does not enforce the required at-most-one delivery_spc_call rule.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Persist and verify a delivery settlement containing two delivery_spc_calls and assert verification fails even if one proof is valid.
- Artifact: invariants/invariant-0501.json

## invariant-0504 cur-dba2af55cc-result-verification-uses-asyncjobtracker-context

- Title: RPC result verification uses AsyncJobTracker context
- Subsystem: executor delivery
- Missing behavior: RPC delivery result submission does not load the canonical AsyncJobTracker job, compare pool/request metadata to contract data, or verify the delivery SPC proof before updating the pool.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit a delivery result after mutating AsyncJobTracker precompile, commit block, input hash, or executor and assert RPC rejects it without pool mutation.
- Artifact: invariants/invariant-0504.json

## invariant-0506 cur-d569e9b7ca-precompile-specific-delivery-config-decoders-used

- Title: Precompile-specific delivery config decoders are used
- Subsystem: executor delivery
- Missing behavior: The port has precompile-specific delivery config offsets for ZK, FHE, sovereign, and persistent agents, but no CLI-agent or autonomous-agent delivery config decoder symbols or branches are present in the audited repo set.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Encode CLI-agent and autonomous-agent Phase 2 inputs with distinct delivery-config locations and assert settlement creation uses the matching decoder; no such branches exist locally.
- Artifact: invariants/invariant-0506.json

## invariant-0507 cur-29d56e1b7a-agent-decodes-codec

- Title: CLI agent decodes with its own codec
- Subsystem: executor delivery
- Missing behavior: No CLI_AGENT_PRECOMPILE or CLIAgentRequest codec path exists locally, so CLI agent extraction cannot decode its own codec instead of DKMS input.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Encode a CLIAgentRequest and assert detector/RPC validation extract executor and TTL without DKMS decoding; no local CLI-agent codec is available to run this path.
- Artifact: invariants/invariant-0507.json

## invariant-0509 cur-74fda6fd4f-heartbeat-commitments-protocol-exempt

- Title: Heartbeat commitments are protocol-fee exempt
- Subsystem: executor delivery
- Missing behavior: Heartbeat revival scheduling is present, but no local builder/verifier path zeroes executor fee, total amount, or all settlement fees specifically for heartbeat async settlements.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Build a heartbeat revival through async settlement and assert executor_fee, total_amount, commitment_fee, inclusion_fee, and validator addresses are all zero.
- Artifact: invariants/invariant-0509.json

## invariant-0512 cur-93a3e077ff-persistent-agent-payloads-fully-decoded

- Title: Persistent agent payloads are fully decoded
- Subsystem: executor delivery
- Missing behavior: Persistent-agent payload validation decodes the full ABI and validates executor/TTL, but it permits an empty model when restore_from_cid is non-empty.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit a persistent-agent payload with nonzero executor, valid TTL, empty model, and non-empty restore_from_cid and assert validation rejects EmptyModel; current tests assert acceptance.
- Artifact: invariants/invariant-0512.json

## invariant-0513 cur-1e8f03e282-persistent-agent-uses-http-executors

- Title: Persistent agent uses HTTP or LLM executors
- Subsystem: executor delivery
- Missing behavior: Persistent-agent executor admission accepts only the metadata expected capability tag, which is HttpCall, and has no alternate Llm acceptance path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Validate persistent-agent admission with registry fixtures for HttpCall-only, Llm-only, and neither; current code only accepts HttpCall-only.
- Artifact: invariants/invariant-0513.json

## invariant-0517 cur-3aa9c37830-persistent-agent-0x0820-uses-persistent-agent-validation-fees

- Title: Persistent Agent 0x0820 uses persistent-agent validation and fees
- Subsystem: executor delivery
- Missing behavior: Persistent-agent validation does not require model to be non-empty when restore_from_cid is present, so the full invariant is not enforced.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Submit a persistent-agent payload with valid executor/TTL, empty model, and non-empty restore_from_cid; the invariant expects rejection, while current validation accepts it.
- Artifact: invariants/invariant-0517.json

## invariant-0526 cur-21e22326d9-error-responses-constant

- Title: LLM error responses use constant fee
- Subsystem: executor delivery
- Missing behavior: The port returns only U256 from compute_llm_executor_fee and has no fallback_reason/LlmPricingTrace result path for has_error=true responses.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call compute_llm_executor_fee on a has_error=true response and assert the API returns a trace/fallback object with fallback_reason plus zero token metrics; no such returned metadata exists locally.
- Artifact: invariants/invariant-0526.json

## invariant-0528 cur-c632bb5e0f-error-responses-constant

- Title: LLM error responses use constant fee
- Subsystem: executor delivery
- Missing behavior: The port returns only U256 from compute_llm_executor_fee and has no fallback_reason/LlmPricingTrace result path for has_error=true responses.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call compute_llm_executor_fee on a has_error=true response and assert the API returns a trace/fallback object with fallback_reason plus zero token metrics; no such returned metadata exists locally.
- Artifact: invariants/invariant-0528.json

## invariant-0530 cur-cfe4309d44-error-deliveries-settle-constant

- Title: DA error deliveries settle with constant fee
- Subsystem: executor delivery
- Missing behavior: Image, Audio, Video, and FHE Phase 2 delivery result handling has no hasError=true short-circuit that bypasses normal output extraction and applies a DA_ERROR_PHASE2_FEE_WEI executor fee.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Encode Image/Audio/Video/FHE Phase 2 delivery results with hasError=true and malformed normal output fields; builder/verifier should settle with DA_ERROR_PHASE2_FEE_WEI, but the local port has no such branch.
- Artifact: invariants/invariant-0530.json

## invariant-0531 cur-4cd93a1a20-error-settlement-fees-bounded-compile-time

- Title: Error settlement fees are bounded at compile time
- Subsystem: executor delivery
- Missing behavior: The port defines and compile-time-bounds LLM_ERROR_EXECUTOR_FEE_WEI, but does not define DA_ERROR_PHASE2_FEE_WEI or assert it is bounded by image/audio/video Phase 1 fees.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Temporarily add or mutate DA_ERROR_PHASE2_FEE_WEI above image/audio/video Phase 1 fee values and assert compilation fails; current code has no DA error constant or compile-time assertion to exercise.
- Artifact: invariants/invariant-0531.json

## invariant-0539 cur-32d210c6b1-phase-precompiles-escrow-callback-cost

- Title: All two-phase precompiles escrow callback cost
- Subsystem: executor delivery
- Missing behavior: verify_wallet_for_commitment does not include Phase 2 callback cost for every registered two-phase precompile; image, video, and FHE are not covered by the v2 port wallet callback-cost path.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Encode image, video, and FHE two-phase inputs with nonzero delivery gas/max fee/value and assert wallet verification includes that callback cost; current port lacks those branches.
- Artifact: invariants/invariant-0539.json

## invariant-0543 cur-9393fb5c50-heartbeat-revival-uses-prepared-payloads

- Title: Heartbeat revival uses prepared payloads
- Subsystem: executor delivery
- Missing behavior: Canonical heartbeat revival does not submit reviveAgentPrepared(agent, precompileInput); the local port uses reviveAgent(address,bytes) and has no reviveAgentPrepared symbol or selector.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Search for and call a reviveAgentPrepared selector in canonical heartbeat processing; current code only exposes reviveAgent(address,bytes).
- Artifact: invariants/invariant-0543.json

## invariant-0546 cur-2f077d909d-revival-executor-selection-avoids-last-executor

- Title: Revival executor selection avoids last executor
- Subsystem: executor delivery
- Missing behavior: The audited port does not select the revival executor by block-number modulo over the current executor list; the local selector uses parent-hash and agent-address entropy instead.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Call select_revival_executor with two different block numbers and identical parent hash/agent; current function has no block-number input, so the selected executor cannot change by block-number modulo.
- Artifact: invariants/invariant-0546.json

## invariant-0547 cur-b14bcc0200-revival-executor-selection-uses-parent-hash

- Title: Revival executor selection uses parent hash
- Subsystem: executor delivery
- Missing behavior: The start index is not computed solely as u16::from_be_bytes([hash[30], hash[31]]) % len; it is XORed with the revived agent address tail bytes.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: With a nonzero agent tail, assert the selected index equals u16::from_be_bytes([hash[30], hash[31]]) % len; current code uses XOR with agent bytes.
- Artifact: invariants/invariant-0547.json

## invariant-0551 cur-cdf37afeed-block-build-trace-includes-demotions-included-count

- Title: Block build trace includes demotions and included count
- Subsystem: block building
- Missing behavior: Block build attempts are not actually recorded with demotion events and included transaction counts by the payload builder; the schema exists but the producer path is absent.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Enable block build trace, build a payload with a policy demotion, and assert ritual_getBlockBuildTrace contains that demotion and includedTxCount; current producer wiring is absent.
- Artifact: invariants/invariant-0551.json

## invariant-0553 cur-08304a6882-block-lifecycle-events-include-block-time

- Title: Block lifecycle events include block_time
- Subsystem: block building
- Missing behavior: The local port does not wire payload-building start/end or block-verification-end events that emit block_time from the block header; only EL head update is wired with block_time.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Capture lifecycle tracing during payload build and block verification and assert start/end/verification events contain block_time; current calls are absent.
- Artifact: invariants/invariant-0553.json

## invariant-0554 cur-488e5ba86f-block-lifecycle-logs-carry-structured-phase-fields

- Title: Block lifecycle logs carry structured phase fields
- Subsystem: block building
- Missing behavior: Payload lifecycle logs with attempt metadata are not wired into the payload builder; the port only has helper definitions and block-accept phase logging.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Capture payload build tracing and assert payload phases include block_phase, path, outcome, timing/count, payload_id, attempt_id, and attempt_kind; current payload calls are absent.
- Artifact: invariants/invariant-0554.json

## invariant-0555 cur-1646306e47-block-lifecycle-metrics-include-header-block-time

- Title: Block lifecycle metrics include header block time
- Subsystem: block building
- Missing behavior: Payload build start/end and verified-block metric events are not produced with header block_time; only EL head update is wired with the canonical header timestamp.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Capture block lifecycle metrics during payload build, block verification, and EL head update; current code should only show EL head block_time while payload/verified-block producers are absent.
- Artifact: invariants/invariant-0555.json

## invariant-0557 cur-a68de514e1-build-attempts-flush-demotions-every-outcome

- Title: Build attempts flush demotions on every outcome
- Subsystem: block building
- Missing behavior: Payload build attempts do not snapshot policy demotions before success, abort, or cancellation outcomes, because the attempt recorder/producer path is absent.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Force cancelled, not-better, and better-payload exits after a demotion and assert ritual_getBlockBuildTrace contains the demotion for each; current producer wiring is absent.
- Artifact: invariants/invariant-0557.json

## invariant-0560 cur-b8b495a4de-builder-applies-sequencing-rights-ordering

- Title: Builder applies sequencing-rights ordering
- Subsystem: block building
- Missing behavior: Payload building does not classify transactions by simulated contract call graph before sequencing-rights reordering.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create a transaction whose top-level target lacks sequencingRights but an internal call reaches an SR contract; the current builder will not classify it as the SR contract bucket.
- Artifact: invariants/invariant-0560.json

## invariant-0562 cur-db1cfee895-builder-skips-validation-errors

- Title: Builder skips validation errors
- Subsystem: block building
- Missing behavior: Arbitrary BlockExecutionError::Validation values not matched by the specific branches still abort payload building instead of being logged and skipped.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Inject an unrecognized BlockExecutionError::Validation from transaction execution and assert payload building returns an EVM error rather than skipping the transaction.
- Artifact: invariants/invariant-0562.json

## invariant-0565 cur-717a7fcd54-chainspec-extra-data-byte

- Title: Ritual chainspec has no extra-data byte cap
- Subsystem: block building
- Missing behavior: RITUAL_MAINNET and RitualChainSpecBuilder::ritual_mainnet do not explicitly set max_extra_data_bytes(None), and RitualChainSpec does not expose a max_extra_data_bytes EthChainSpec override/delegation in nodebuilder.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-nodebuilder-internal
- Falsification candidate: Construct nodebuilder RITUAL_MAINNET and RitualChainSpecBuilder::ritual_mainnet().build() and assert max_extra_data_bytes() returns None; current source lacks the setter/delegation.
- Artifact: invariants/invariant-0565.json

## invariant-0566 cur-e4e57a01d7-classification-counts-only-contracts

- Title: Classification counts only SR contracts
- Subsystem: block building
- Missing behavior: Builder/verifier classification is not based on the set of call-graph addresses with non-bottom sequencingRights ordering.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Simulate a transaction touching one SR contract and multiple non-SR helper contracts through internal calls; current production classification will not use the call graph to return SingleContract for the SR contract.
- Artifact: invariants/invariant-0566.json

## invariant-0567 cur-f6636ebd19-compact-signatures-include-ecdsa-passkey-type-markers

- Title: Compact signatures include ECDSA and passkey type markers
- Subsystem: block building
- Missing behavior: Compact TransactionSignature encoding does not distinguish ECDSA and passkey signatures with the required 0xEC and 0x77 markers plus passkey RLP length framing.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-alloy-internal
- Falsification candidate: Compact-encode ECDSA and passkey signatures and assert first bytes 0xEC/0x77 with passkey length framing; no such compact encoder is present locally.
- Artifact: invariants/invariant-0567.json

## invariant-0570 cur-bb97305ba1-earliest-fallback-waits-before-empty-payload

- Title: Earliest fallback waits before empty payload
- Subsystem: block building
- Missing behavior: Earliest empty-payload fallback does not wait a configured grace duration before building an empty payload.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Trigger RaceEmptyPayload with no best payload and assert build_empty_payload can start immediately; there is no grace timer to configure or observe.
- Artifact: invariants/invariant-0570.json

## invariant-0571 cur-d3c5a53a07-empty-payload-fallback-does-race-waitforpending-full-builds

- Title: Empty payload fallback does not race WaitForPending full builds
- Subsystem: block building
- Missing behavior: The port prevents WaitForPending empty-payload racing but does not implement the configured grace delay for Earliest fallback, so the full invariant is not enforced.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Issue Earliest/RaceEmptyPayload while a full build is about to finish and assert empty fallback is delayed by configured grace; current source has no delay.
- Artifact: invariants/invariant-0571.json

## invariant-0573 cur-3e1d856ec4-error-chain-capture-bounded

- Title: Error-chain capture is bounded
- Subsystem: block building
- Missing behavior: Payload-builder error chain capture is not bounded to 32 entries and does not append the required truncation marker because the collector is absent.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create an execution error with more than 32 sources and call the expected collector; no bounded collector/truncation marker exists locally.
- Artifact: invariants/invariant-0573.json

## invariant-0574 cur-246-01-cli-agent-uses-agent-phase-2-pricing

- Title: CLI agent uses agent Phase 2 pricing
- Subsystem: executor delivery
- Missing behavior: Both AGENT_CALL_PRECOMPILE and CLI_AGENT_PRECOMPILE are not routed to work-based agent Phase 2 pricing; the CLI-agent address/symbol is absent from the audited code.
- Checked repos: /home/ritual/repos/ritual-reth-internal-v2.2.0-port, /home/ritual/repos/ritual-reth-nodebuilder-internal, /home/ritual/repos/ritual-alloy-internal, /home/ritual/repos/ritual-alloy-evm-internal, /home/ritual/repos/ritual-revm-internal, /home/ritual/repos/ritual-revm-inspectors-internal, /home/ritual/repos/ritual-node-internal
- Likely owner: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- Falsification candidate: Create Phase 2 settlements for the expected agent and CLI-agent precompile addresses and assert both use calculate_agent_fees_phase2_work; the CLI-agent branch is absent locally.
- Artifact: invariants/invariant-0574.json