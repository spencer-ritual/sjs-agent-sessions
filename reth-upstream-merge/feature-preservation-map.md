# Reth Feature Preservation Map

Source: `ritual-reth-internal` diff `6f8e7258f4733279080e4bd8345ce50538a40d6e..851b5150035e92c3fbfc9a543fdb9049acfc1e3a`.

This is a starter map for port batches. Treat it as an invariant checklist, not a complete spec.

## How To Use This Map

Use this file as the merge agent's subsystem work queue. Use `pr-preservation-map.md` as the audit ledger.

For each section:

- Preserve the listed invariants.
- Use PR coverage to check historical intent, removals, constants, and hardening.
- Port into upstream Reth `v2.2.0` structure rather than old fork file layout.
- Mark every relevant PR as ported, intentionally dropped, or no-port/noise before the section is done.
- Prefer scoped checks per section, then builder/verifier replay and localnet gates at integration checkpoints.

## 1. Transaction Formats And Codecs

Preserve custom tx families and wire/storage identity:

- `Scheduled(0x10)`, `AsyncCommitment(0x11)`, `AsyncSettlement(0x12)`, `Passkey(0x77)`.
- Full passkey signature representation, including P256/WebAuthn and synthetic sender handling.
- SPC call fields: precompile address, input, output, proof, and block number.
- RLP/2718, compact codec, DB/static-file, receipt, and RPC transaction conversion compatibility.

Evidence:

- `crates/ethereum/primitives/src/transaction.rs`
- `crates/storage/codecs/src/alloy/transaction/mod.rs`
- `crates/storage/codecs/src/alloy/transaction/{scheduled,async_commitment,async_settlement,passkey,spc_call}.rs`

Port target: upstream Alloy/Reth transaction envelope, primitive, typed transaction, compact codec, storage codec, and receipt/RPC adapters.

Validation: round-trip fixtures for every custom tx type; transaction hash/root equality for blocks containing each type; DB decode of old fork data if available. Include wrapper and adapter coverage, not only concrete transaction structs:

- `Transaction` trait forwarding through `Signed<T>`, sealed transactions, typed envelopes, and generated envelope implementations must expose Ritual metadata such as `spc_calls`, `delivery_spc_calls`, `origin_tx_hash`, `commitment_tx`, and `settlement_tx`.
- Signed wire/storage/network encoding must preserve runtime SPC/async fields where they are part of persisted or transmitted identity, while transaction hash and signing preimage paths must continue to exclude runtime-populated fields when that is the established Ritual invariant.
- RPC and CL/EL adapter structs must round-trip optional Ritual-relevant fields. The Alloy `v2.0.4` checkpoint caught beacon `PayloadAttributes.extra_data` being dropped in the beacon adapter even though the engine type supported it.
- Request inference must honor explicit custom transaction type IDs (`0x10`, `0x11`, `0x12`, `0x77`) instead of silently falling back to legacy or EIP-1559 inference.
- Removed async fields such as `target_block` / `commit_block` must stay removed from RPC/txpool surfaces unless a deliberate old-data decode path is documented.

PR coverage:

- Port: first async tx variant and subpool metadata (`ac25b7d7`, `#32`), `AsyncCommitment`/`AsyncSettlement` and SPC codecs (`#83`), non-overlapping tx type constants (`#84`), scheduled tx codec/receipt integration (`#220`), passkey `0x77` (`#241`), Phase 2 `delivery_spc_calls` in receipts/codecs (`#270`), sovereign/persistent agent codecs and storage refs (`#286`).
- Preserve hardening: async settlement compact codec coverage (`#84`), passkey synthetic ECDSA fallback (`#241`), safe settlement/delivery selector offsets and Phase 1/Phase 2 input extraction (`#282`), LLM 30-field ABI with `convo_history: StorageRef` at index 29 (`#306`).
- Do not reintroduce removed fields: `target_block` and `commit_block` were intentionally removed from async flow/codecs/RPC/txpool/verifier in favor of parent-block simulation (`#261`), except for explicit old-data decode compatibility.

## 2. Async Precompile Detection And Validation

Preserve async transaction detection at parent state and shared validation semantics:

- Builder/verifier simulate against parent block state for deterministic async detection.
- RPC validation simulates pending txs for immediate user feedback but is not the authority.
- Shared payload validation rejects bad TTL, oversized inputs, malformed ECIES/user keys, bad URLs/models/messages, invalid two-phase deadlines, and unsupported agent types.
- TEE registry, model registry, and wallet lock checks must stay aligned with builder/verifier assumptions.

Evidence:

- `crates/ritual-async/src/lib.rs`
- `crates/ritual-async/src/detector.rs`
- `crates/ritual-async/src/validation.rs`
- `crates/rpc/rpc/src/async_tx_validator.rs`

Port target: upstream RPC transaction submission, EVM simulation hooks, payload-builder async classification, and verifier pre-execution checks.

Validation: targeted RPC rejection tests plus one valid async tx path proving RPC, builder, and verifier agree on detection and deadlines.

PR coverage:

- Port authority model: RPC provides early feedback (`#204`, `#231`, `#307`), while builder/verifier re-simulate async origin txs and hard-fail invalid commitments (`#145`).
- Preserve timing semantics: scheduled async simulation block is `startBlock + frequency * index - 1` (`#78`, `#150`), Phase 2 offset must be `> ttl` and `<= MAX_PHASE2_DEADLINE_OFFSET` (`#232`), shared TTL source is `max_ttl_blocks()` / `ASYNC_MAX_TTL_BLOCKS` (`#242`), default TTL is `500` (`#265`).
- Preserve validation hardening: PrecompileConsumer decoding, executor registration/capability checks, and pool removal on failed validation (`#204`); centralized invalid-payload errors (`#231`); ECIES/user-key checks, supported sovereign agent types `0/4/5/6`, and Phase 2 bounds (`#307`); async input/calldata caps and builder/verifier obligation consistency (`#292`).
- Preserve active-job semantics: contract state / AsyncJobTracker is source of truth (`#219`); duplicate active jobs block commitments while expired jobs may be recommitted (`#260`, `#268`).

## 3. EVM Context, Precompiles, And SPC

Preserve the Ritual EVM execution context:

- Async context mode distinguishes build, verify, and RPC simulation.
- Async precompile calls are captured with enough data to build commitments and verify SPC results.
- SPC proof/signature paths preserve original transaction context, precompile input/output, executor, and previous-block context.
- Pool manager / EVM integration remains available to nodebuilder and payload code.

Evidence:

- `crates/evm/src/lib.rs`
- `crates/evm/src/spc.rs`
- `crates/evm/src/pool_manager.rs`
- `crates/evm/src/async_context_tests.rs`
- `crates/ritual-spc-signature/src/lib.rs`
- `crates/ritual-spc-verification/src/verifier.rs`

Port target: upstream `reth-evm`, `alloy-evm`, revm context/precompile integration, and node EVM factory wiring.

Validation: async context unit tests; local SPC precompile execution proving capture, submission, and verification still line up.

Revm `v107` follow-up checks:

- Preserve `async-context` feature wiring across `revm-context`, `revm-handler`, `revm-precompile`, and `revm`; Reth/nodebuilder execution contexts used for payload building, verifier/import, and RPC simulation must implement `AsyncContextTr` when Ritual async precompiles can execute.
- Keep upstream `CallInputs` / EIP-7702 authorization-list shape while preserving Ritual `TxEnv` metadata: `commitment_tx`, `settlement_tx`, `spc_calls`, and deterministic `tx_hash` propagation.
- Verify async-aware precompile dispatch for HTTP `0x0801`, LLM `0x0802`, long-running HTTP `0x0805`, ZK two-phase `0x0806`, FHE `0x0807`, sovereign agent `0x080C`, image/audio/video `0x0818`/`0x0819`/`0x081A`, dKMS `0x081B`, and persistent agent `0x0820`; the actual node path must not fall back to non-context precompile execution for these addresses.
- Preserve system transaction accounting in revm and downstream callers: scheduled, async commitment, and async settlement transactions intentionally skip selected nonce, balance, gas deduction/reimbursement, and block gas-limit checks while block gas accounting remains enforced separately in Reth payload/verifier policy.
- Preserve post-execution fund sinks: scheduled transactions burn the Scheduler contract balance, and Phase 2 async settlements burn only the AsyncDelivery contract balance, not RitualWallet.
- Decide the `op-revm` scope before E2E: either prove Ritual async execution does not route through OP precompile dispatch, or add equivalent async-context validation for OP paths.

PR coverage:

- Port executor/SPC intent: parent/simulation context rewriting, settlement origin hashing, SPC verification batching, and async-pool pruning (`#93`); direct registry storage reads and deduped SPC key reads (`#149`); deferred bytes verification with hash/size from AsyncJobTracker and full bytes from calldata (`#208`); canonical AsyncJobTracker-derived SPC context and build-time SPC reverification (`#273`).
- Preserve precompile/address surface: DKMS `0x081B` (`#258`), FHE `0x0807` (`#264`), canonical `0x08xx` address crate and shared SPC allowlist (`#317`), split image/audio/video capabilities (`#246`), persistent-agent runtime enum `zeroclaw/openclaw/hermes` with 26-field layout (`#321`).
- Do not reintroduce deprecated `AGENT_CALL_PRECOMPILE`; it was intentionally removed from detection, validation, pool, verifier, fee, and registry paths (`#319`).
- Do not preserve temporary permissive verification from `#93` unless explicitly gated by skip-validity config.

## 4. Txpool Async And Scheduled Lifecycle

Preserve pool state machines:

- Scheduled subpool and scheduled system tx insertion.
- Async commitment pool keyed by original tx hash.
- Phase 1 sender locks, release rules, expiry filtering, and delivery-ready Phase 2 state.
- Fulfilled async tx conversion into settlement/delivery transactions.
- Canonical-state cleanup, reorg behavior, and heartbeat revival dedup.
- System/scheduled tx exemptions from normal nonce/balance rules where intended.

Evidence:

- `crates/transaction-pool/src/pool/async_pool.rs`
- `crates/transaction-pool/src/pool/scheduled.rs`
- `crates/transaction-pool/src/pool/mod.rs`
- `crates/transaction-pool/src/blocking_handlers.rs`
- `crates/transaction-pool/src/traits.rs`
- `crates/transaction-pool/src/validate/eth.rs`

Port target: upstream transaction-pool trait, subpool, validator, maintenance, and canonical notification extension points.

Validation: async pool FSM tests, scheduled insertion tests, expiry/removal tests, sender-lock release tests, and canonical/reorg tests.

PR coverage:

- Port lifecycle surface: async subpool, txpool RPC metadata, detector-created system txs (`ac25b7d7`, `#32`), async pool pruning (`#83`, `#93`), scheduled pool filtering (`#220`), blocking canonical-state handlers for live updates/backfill (`#86`).
- Preserve sender/expiry hardening: sender address propagation and original scheduled caller (`#115`), dual-path scheduled eviction and chain-halt job eviction (`#122`), sender-lock checks and settlement expiry parity (`#219`), stale duplicate pool pruning (`#260`), pending-pool age eviction (`#300`).
- Preserve duplicate/nonce behavior: optimized nonce-lock verification, pre-recovered senders, same-block duplicate commitment rejection, and pool hooks (`#207`); active AsyncJobTracker duplicates block builder/verifier commitments and prune stale pool entries (`#260`, `#268`).
- Preserve Phase 2 and lifetime behavior: Phase 2 deadline offset semantics (`#232`), async pool metadata refresh after canonical SPC context fixes (`#273`), sovereign-agent Phase 1 async tx pool lifetime of `200` seconds (`#308`).

## 5. Scheduling And Heartbeat

Preserve scheduled execution semantics:

- Scheduler contract storage hydration on canonical updates/startup.
- Due-call selection by start block, frequency, TTL, state, funds, uniqueness, and predicate.
- C1-C11 scheduled constraints, including predicate `shouldExecute`.
- Heartbeat contract liveness, failed-agent revival, cooldown, owner/executor data, and revive dedup.
- Scheduled async calls should not be double-counted as missed obligations when an active async job exists.

Evidence:

- `crates/scheduling/src/{canonical,contract,singleton,transaction,types}.rs`
- `crates/ritual-scheduled-verification/src/lib.rs`
- `crates/ritual-scheduled-verification/src/predicate.rs`
- `crates/ritual-heartbeat-tracker/src/lib.rs`
- `crates/ritual-block-verification/src/verifier.rs`

Port target: upstream canonical state notifications, payload-builder scheduled augmentation, txpool system transaction handling, and verifier hooks.

Validation: localnet or fixture flow with one due scheduled tx, one false predicate, one expired tx, and one heartbeat revival.

PR coverage:

- Port scheduling model: scheduled async simulation block math (`#78`, `#150`), `FrequencyIndex`, production ABI topics, `Complete` events, retry-aligned scheduling (`#97`), startup/canonical hydration from Scheduler storage (`#86`, `#341`).
- Preserve predicate/due-window hardening: C11 `shouldExecute`, parent-state staticcalls, predicate gas budgets (`#262`), constant-time due-window math, TTL cap `500`, saturating max-block arithmetic, zero-`num_calls` handling (`#313`), overflow bitmap slot derivation using packed `callId` and bucket (`#357`).
- Preserve censorship and active-job rules: predicate-filtered obligations, capacity-based omission rejection, active-async-job exemption (`#278`), active-job filtering for augmented scheduled obligations (`#354`).
- Preserve heartbeat/revival policy: heartbeat hydration and `ritual_getHeartbeatTrackerState` (`#331`), deterministic Phase 0b skip after slow runs (`#337`), revival-lane filtering and `RETH_REVIVAL_*` knobs (`#338`), single `reviveAgent(address,bytes)` path and owner pending-job dedup (`#339`), parent-hash-plus-agent entropy (`#342`).
- Preserve overflow-safe scheduled fee/gas conversion (`#305`).
- Do not preserve intermediate conflict-marker artifacts from `#337`; use final behavior from `#338`.

## 6. Payload Building

Preserve block construction behavior:

- Scheduled obligation augmentation before final ordering.
- Async detection and commitment insertion.
- Fulfilled async settlement and delivery settlement inclusion.
- Unified collection across regular, scheduled, fulfilled async, and delivery txs.
- Tip-maximizing order with sequencing-rights reordering.
- Gas, size, cap/demotion, and trace behavior.

Evidence:

- `crates/ethereum/payload/src/lib.rs`
- `crates/ethereum/payload/src/{bundle,collector,execution,unified_builder,unified_execution}.rs`
- `crates/ritual-scheduled-block-building/src/lib.rs`
- `crates/ritual-sequencing-rights/src/*`

Port target: upstream Reth v2.2 payload-builder service, basic payload pipeline, transaction selection, and execution hooks.

Validation: builder scenarios for scheduled-only, async-only, fulfilled async, delivery, and mixed regular tx blocks; compare block-build trace phases.

PR coverage:

- Port ordering model: unified collection/execution and sequencing-rights classification/reordering (`#230`).
- Preserve block limits/gas policy: `builder.max-block-size` (`#99`), async commitments charge zero block gas while scheduled/settlement use calldata gas and EVM execution may use `u64::MAX` (`#167`), payload deadline and safe selector/input extraction (`#282`).
- Preserve active-job and Phase 2 behavior: parent-state duplicate active-job checks (`#260`, `#268`), build-time SPC reverification and metadata refresh (`#273`), Phase 2 delivery settlements and nested delivery (`#270`), atomic original+settlement size/gas precheck (`#304`).
- Preserve DoS policy: build deadline default `300ms`, deadline guards, obligation/fulfilled/delivery caps, total/per-category async sim caps, regular-priority allocation, tx-count cap, local work-class demotion, near-deadline epsilon, optional-class short-circuit, and cap observations (`#292`, `#332`, `#330`, `#354`).
- Preserve trace-facing payload metadata: payload attempt IDs/kinds, empty-payload fallback tracing, demotion capture, primary included tx count (`#329`, `#336`).
- Avoid verifier-only obligation deadline logic that can diverge from builder membership (`#299`).

## 7. Block Verification And Consensus Gates

Preserve fail-closed verifier behavior:

- Async commitment structure and parent-state validation.
- Settlement, delivery, and executor fee verification.
- SPC proof/signature verification.
- Scheduled C1-C11 constraints and heartbeat constraints.
- Nonce-lock validation from parent async job state.
- Sequencing-rights validation and scheduled censorship checks.
- Builder-produced blocks must replay under verifier rules.

Evidence:

- `crates/ritual-block-verification/src/verifier.rs`
- `crates/ritual-block-verification/src/nonce_lock.rs`
- `crates/ethereum/consensus/src/validation.rs`
- `crates/engine/tree/src/tree/mod.rs`

Port target: upstream engine tree, new-payload validation, consensus validation, and block execution/verifier hooks.

Validation: invalid-block fixtures per verifier phase plus one builder-produced block replay/import test.

PR coverage:

- Port async verifier gates: parent-state verifier re-simulation, settlement origin hashing, batched SPC verification, TTL/precompile/input checks, and hard-fail invalid commitments (`#93`, `#145`).
- Preserve parity with builder: per-block async sender uniqueness and wallet locks (`#202`), shared per-block `ModelCache` (`#205`), optimized nonce-lock checks and same-block duplicate rejection (`#207`).
- Preserve deferred-bytes and canonical context checks: hash/size from AsyncJobTracker, full bytes from calldata (`#208`), canonical tracker-derived SPC context and pool/contract consistency (`#273`).
- Preserve scheduled verifier hardening: C11 rejection (`#262`), censorship checks and capacity-based omission rejection (`#278`), builder/verifier obligation consistency and active-job filtering (`#292`, `#354`).
- Preserve delivery/DA verification: Phase 2 delivery settlements, `delivery_spc_calls`, nested async delivery (`#270`), DA-error Phase 2 settlement handling (`#315`).
- Do not reintroduce `target_block`/`commit_block` (`#261`) or deprecated `AGENT_CALL_PRECOMPILE` (`#319`).

## 8. RPC And Operator Surfaces

Preserve external/operator APIs:

- `ritual_*` namespace for async result submission, batch submission, delivery result submission, pending jobs, async simulation traces, block-build traces, scheduled incidents, and heartbeat tracker state.
- Async result submission must preserve original tx/passkey context.
- Error messages should stay descriptive for invalid async payloads and mismatched canonical context.

Evidence:

- `crates/rpc/rpc-api/src/ritual.rs`
- `crates/rpc/rpc/src/ritual.rs`
- `crates/rpc/rpc/src/async_tx_validator.rs`
- `crates/rpc/rpc/src/eth/helpers/transaction.rs`
- `crates/ethereum/node/src/node.rs`

Port target: upstream RPC module registration, node add-ons, typed RPC API crates, and transaction submission helpers.

Validation: JSON-RPC smoke tests for every `ritual_*` method and negative submission cases.

PR coverage:

- Preserve async txpool metadata RPC coverage (`#32`, `#85`), not just submission endpoints.
- Preserve RPC async validation behavior: precompile consumer decoding, executor capability/registration, ECIES/user keys, supported sovereign agent types `0/4/5/6`, Phase 2 offset bounds, rich invalid-payload errors (`#204`, `#231`, `#307`).
- Preserve delivery result submission with original tx/passkey context and `delivery_spc_calls` compatibility (`#270`).
- Preserve operator APIs: `ritual_getHeartbeatTrackerState` (`#331`), scheduled incident debug RPC (`#345`, `#351`), block-build trace with demotions/caps/primary included count (`#336`, `#354`), async simulation trace.
- No-port unless later behavior depends on it: reverted optimized WS/pubsub behavior (`#107`).

## 9. Chainspec, Genesis, And Config

Preserve Ritual network assumptions:

- Summit validator deposit behavior.
- Large/unbounded `extra_data` where Ritual CL snapshots require it.
- `base_block_reward` genesis/config path and reward application.
- Environment-gated consensus constants only where already shipped.

Evidence:

- `crates/chainspec/src/{api,constants,spec}.rs`
- `crates/ethereum/evm/src/execute.rs`
- `crates/consensus/common/src/validation.rs`

Port target: upstream chainspec/genesis parsing, header validation, and executor reward logic.

Validation: genesis parse test, large `extra_data` header validation, and block reward execution test.

PR coverage:

- Preserve `builder.max-block-size` and byte/log-size enforcement across regular, scheduled, async commitment, fulfilled async, and settlement txs (`#99`).
- Preserve unbounded/dynamic Ritual `extra_data`, CL-provided extra data, Summit deposit topic, and max-extra-data validation (`#249`).
- Preserve eager-payload wait-with-empty-fallback behavior only if still operationally required (`#243`).
- Preserve configurable `base_block_reward` from genesis/chainspec and beneficiary reward application (`#271`).
- Preserve payload deadline/sync policy: default `300ms`, obligation caps, async sim caps, builder/verifier policy boundary (`#282`, `#292`, `#332`), transient ONNX unavailability as retryable/`SYNCING` with bounded retry before unwind/escalation (`#298`, `#301`).

## 10. Fees, Registries, And Product Economics

Preserve pricing and registry rules:

- Async inclusion, commitment, settlement, delivery, LLM, multimodal, sovereign agent, persistent agent, and scheduled fees.
- Model registry reads and cache behavior.
- Wallet balance and lock-duration requirements.
- TEE registry capability matching for each precompile.
- Per-call min funding and spawn/day fee calibration.

Evidence:

- `crates/ritual-async-fees/src/*`
- `crates/ritual-async-registry/src/lib.rs`
- `crates/ritual-tee-registry-reader/src/*`
- `docs/design/model-pricing-registry.md`

Port target: support crates first, then RPC/builder/verifier call sites.

Validation: formula unit tests, registry storage-layout tests, and one end-to-end async fee settlement case.

PR coverage:

- Preserve strict fee behavior: shared async fee crate and no fallback on HTTP/LLM/pricing failures (`#146`), model-registry pricing and fail-closed builder/verifier/wallet reads (`#252`).
- Preserve registry migrations: ExecutorRegistry/SPC public key reads, workload IDs, capabilities, registry address config (`#124`, `#149`), upgraded storage slots and ERC-7201 owner caveat (`#269`).
- Preserve wallet/economics: balance and lock-duration checks, per-block async sender uniqueness (`#202`), sovereign/persistent escrow and work/spawn fee models (`#286`).
- Preserve changed constants: ZK Phase 1 fee (`#266`), async TTL default `500` (`#265`), capability IDs `AUTONOMOUS_AGENT=11` and `TELEMETRY=12` (`#333`), persistent spawn fee `0.10 RIT` and sovereign iteration/tool fees (`#356`).
- Preserve multimodal/DA/error pricing: image/video steps, FPS, output extraction (`#251`), FHE output-size Phase 2 pricing (`#264`), LLM error settlement fee (`#314`), constant DA-error settlements (`#315`).
- Do not reintroduce deprecated `AGENT_CALL_PRECOMPILE` in fee or registry paths (`#319`).

## 11. Observability And Agent Guardrails

Preserve operational visibility:

- Bounded async simulation traces.
- Bounded block-build traces and demotion/cap observations.
- Scheduled incident tracking.
- Txpool scheduled/async metrics.
- Ritual JSON tracing router for selected lifecycle targets.

Evidence:

- `crates/ritual-metrics/src/{block,scheduling,tx}.rs`
- `crates/tracing/src/ritual_router.rs`
- `crates/rpc/rpc-api/src/ritual.rs`
- `crates/rpc/rpc/src/ritual.rs`

Port target: upstream metrics registry, tracing layer, and RPC debug DTOs.

Validation: enable trace envs, build a capped/demoted block, and verify trace/RPC output plus metric names.

PR coverage:

- Preserve early metrics: verification-end fields, payload/verification phase metrics, scheduler event visibility (`3393e7a3`, `#97`).
- Preserve structured block telemetry: block/tx phase logs, per-tx payload execution logs, payload attempt IDs/kinds, empty-payload fallback tracing, node/basic payload integration (`#325`, `#329`).
- Preserve payload policy traceability: build attempts, demotion capture, primary-cause trace plumbing, cap observations, async sim deadlines, total/per-category caps, combined scheduled/regular sim phases (`#332`, `#336`, `#337`, `#354`).
- Preserve scheduled incident observability: bounded ring buffer, structured gas/scheduled sad-path capture, decoded call/index fields, continued capture after 0-gas structured logs (`#345`, `#351`).
- Preserve guardrail knobs and visible evidence: build deadline, obligation cap, async sim cap, tx input/calldata limits (`#292`), `RETH_REVIVAL_*` revival-lane controls (`#338`), cap observations aligned with builder/verifier obligation consistency (`#354`).

## PR Audit Checklist

- Every non-noise PR in `pr-preservation-map.md` is referenced by at least one feature section or explicitly marked no-port/noise.
- Every intentional removal remains removed unless there is an explicit compatibility reason to restore it.
- Every changed constant has one source of truth and a validation gate.
- Every high-risk path has both a builder-side and verifier/import-side check.
- Every RPC validation path is classified as UX feedback, not consensus authority.
- Every skipped validation records the later gate that will cover it.

## Open Follow-Up

- Turn each batch into an FSM/spec page before porting high-risk behavior.
- Add old-branch fixtures for transaction encoding and block verification where unit tests do not exist.
- Decide which end-to-end localnet scenarios are final gates versus per-batch gates.
- Check for features hidden outside the obvious Ritual crates, especially in net, storage provider, stages, and engine tree changes.
