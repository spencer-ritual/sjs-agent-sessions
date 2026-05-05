# Reth PR Preservation Map

Source: first-parent merge history in `ritual-reth-internal` from upstream divergence base `6f8e7258f4733279080e4bd8345ce50538a40d6e` to `dev` at `851b5150035e92c3fbfc9a543fdb9049acfc1e3a`.

Method: inspect each merge as `git diff <merge>^1 <merge>`, then record product behavior that must survive the Reth `v2.2.0` port. This complements `feature-preservation-map.md`: that file groups by subsystem; this file groups by merged PR intent.

Coverage: 90 first-parent merge commits. Most product behavior lands through PR merges; a few early non-PR branch merges are included when they changed behavior.

## Batch Key

- Transaction formats/codecs: custom tx types, signatures, receipts, DB/static-file codecs.
- Async core: async detection, payload validation, parent-state simulation, TTL/deadline rules.
- EVM/SPC/precompiles: async context, precompile ABIs, SPC capture/signature/proof paths.
- Txpool lifecycle: async/scheduled pools, canonical cleanup, expiry, sender locks.
- Scheduling/heartbeat: scheduler storage, C1-C11, predicates, revival, liveness.
- Payload/verifier: block building, sequencing rights, verifier gates, censorship, atomicity.
- RPC/operator: `ritual_*`, txpool async RPC, debug/trace APIs.
- Fees/registries/economics: pricing, wallet locks, model registry, TEE registry.
- Chainspec/config/ops: genesis, rewards, payload deadlines, sync behavior.
- Observability: metrics, traces, incident buffers.
- No-port/noise: workflow, formatting, reverted/intermediate behavior.

## Early Async And Scheduling Foundation

- Early branch merge `3393e7a3`: preserve added tx verification-end metrics fields. Batch: observability.
- Early branch merge `ac25b7d7`: preserves first async execution prototype: custom async tx variant, async subpool, txpool RPC, detector-created system tx, payload handling. Batch: transaction formats/codecs, async core, txpool lifecycle, payload/verifier.
- `#32` `ritual_async-execution-checkpoint-12`: preserve detailed async txpool metadata exposed over RPC. Batch: RPC/operator, txpool lifecycle.
- Branch merge `8f7946e4` `ritual_move-scheduling-service`: preserve `crates/scheduling` singleton/service, contract reads, due-call tracking, scheduler state. Batch: scheduling/heartbeat.
- `#78` `async_scheduled_fix_bn_sim`: preserve scheduled async simulation block calculation from start/frequency/index. Batch: async core, scheduling/heartbeat.
- `#83` `etherscan-investigation`: preserve `AsyncCommitment`/`AsyncSettlement` codecs, SPC call codec, precompile codecs, wallet checks, commitment/settlement flow, block verifier, async pool. Batch: transaction formats/codecs, EVM/SPC/precompiles, txpool lifecycle, payload/verifier.
- `#84` `address-etherscan-feedback`: preserve non-overlapping tx type constants and async settlement compact codec coverage. Batch: transaction formats/codecs.
- `#85` `asyncpool-rpc-rename`: preserve async txpool RPC names and detailed async metadata access. Batch: RPC/operator.
- `#86` `blocking-state-updates`: preserve blocking canonical-state scheduling handlers for live updates/backfill. Batch: txpool lifecycle, scheduling/heartbeat.
- `#93` `executor-rs`: preserve parent/simulation context rewriting, settlement origin hashing, SPC verification batching, async-pool pruning. Do not preserve temporary permissive verification behavior unless behind explicit skip-validity config. Batch: EVM/SPC/precompiles, payload/verifier, txpool lifecycle.
- `#97` `async-onlyevent`: preserve payload/verification phase metrics, scheduler event handling, production ABI topics, `Complete` event support, retry-aligned scheduling, `FrequencyIndex`. Batch: scheduling/heartbeat, observability.
- `#99` `block-size-limit`: preserve `builder.max-block-size` and block byte/log-size checks for regular, scheduled, async commitment, fulfilled async, and settlement txs. Batch: payload/verifier, chainspec/config/ops.
- `#107` `remove-optimized-ws`: no product behavior to port; keep upstream/default pubsub unless later behavior depends on the reverted code. Batch: no-port/noise.
- `#115` `unified-gas-validation-fixes`: preserve sender address propagation, `secret_signature` decoding, original caller for scheduled txs, no double SPC injection, raw input for signature validation, time-based async/scheduled eviction. Batch: async core, EVM/SPC/precompiles, txpool lifecycle.
- `#122` `scheduling-eviction`: preserve dual-path scheduled eviction, chain-halt job eviction, and verification mode for all txs during block verification. Batch: scheduling/heartbeat, txpool lifecycle, EVM/SPC/precompiles.
- `#124` `teeda-policy`: preserve ExecutorRegistry event/storage migration for SPC executor data, capability, workload ID, public key, and registry address env/config. Batch: fees/registries/economics, EVM/SPC/precompiles.

Noise in this era: early empty merges `5625a9a7` and `28abafa3`; stray file `b`; design/helper docs/scripts are context only.

## Validation, Fees, Scheduling, Multimodal

- `#145` `valconstraints-async-commitment`: preserve verifier re-simulation of async origin tx at parent/commit context, TTL/precompile/input checks, and hard-fail invalid commitments. Batch: async core, payload/verifier.
- `#146` `unify-fees`: preserve shared async fee crate and strict no-fallback fee policy for HTTP/LLM/pricing failures. Batch: fees/registries/economics.
- `#149` `executor-migration`: preserve direct registry storage reads for executor/SPC public key data and deduped SPC key reads. Batch: fees/registries/economics, EVM/SPC/precompiles.
- `#150` `scheduling-refactor`: preserve Scheduler API change to `startBlock/numCalls` and scheduled async simulation block `startBlock + frequency * index - 1`. Batch: scheduling/heartbeat, async core.
- `#167` `async-fixes-revive-to-dev`: preserve system tx gas accounting: async commitments charge zero block gas, scheduled/settlement use calldata gas, EVM execution may use `u64::MAX`. Batch: payload/verifier, fees/registries/economics.
- `#202` `balance-check-valconstraint`: preserve per-block async sender uniqueness and wallet balance/lock duration checks in builder and verifier. Batch: fees/registries/economics, payload/verifier.
- `#204` `rpc-async-validate`: preserve RPC-level async payload validation, PrecompileConsumer decoding, executor registration/capability checks, and pool removal on failed validation. Batch: RPC/operator, async core.
- `#205` `per-block-model-cache-v2`: preserve per-block `ModelCache` shared by builder and verifier for model registry reads. Batch: fees/registries/economics, payload/verifier.
- `#207` `nonce-lock-valconstraint-perf-enhanced`: preserve optimized nonce-lock verification, pre-recovered senders, same-block duplicate commitment rejection, and pool hooks. Batch: payload/verifier, txpool lifecycle.
- `#208` `contract-optimization`: preserve deferred bytes storage: hash/size from AsyncJobTracker, full bytes from calldata, and hash checks for settlement/SPC verification. Batch: async core, payload/verifier.
- `#219` `junglejuice-01`: preserve contract state as async job source of truth, builder sender-lock checks, and settlement expiry parity. Batch: async core, txpool lifecycle, scheduling/heartbeat.
- `#220` `jungle-scheduled`: preserve scheduled block-building and verification crates, C1-C10 constraints, scheduled metrics, scheduled tx codec/receipt integration, pool filtering. Batch: scheduling/heartbeat, transaction formats/codecs, txpool lifecycle.
- `#230` `jungle-ass`: preserve unified payload collection/execution and sequencing-rights classification/reordering plus verifier checks. Batch: payload/verifier.
- `#231` `rpc-async-feedback`: preserve centralized async validation shared by RPC and builder, richer invalid-payload errors, parity across scheduled/sequencing/async paths. Batch: async core, RPC/operator.
- `#232` `phase2-deadline-offset-semantics`: preserve Phase 2 deadline offset semantics: offset must be `> ttl` and `<= MAX_PHASE2_DEADLINE_OFFSET`. Batch: async core, txpool lifecycle.
- `#241` `passkey-support`: preserve tx type `0x77`, passkey signatures, synthetic ECDSA fallback for sender encoding, storage codecs, RPC/pool support. Batch: transaction formats/codecs.
- `#242` `increase-ttl`: preserve shared TTL source `max_ttl_blocks()` / `ASYNC_MAX_TTL_BLOCKS`; note later default changes to 500 in `#265`. Batch: async core.
- `#243` `eager-payload`: preserve operational payload behavior only if still needed: wait for pending payload with empty fallback. Batch: chainspec/config/ops.
- `#246` `separate-capabilities`: preserve split image/audio/video executor capabilities and default model registry address. Batch: fees/registries/economics, EVM/SPC/precompiles.
- `#249` `embed-multisig`: preserve unbounded Ritual `extra_data`, dynamic CL-provided extra data, Summit deposit topic, max-extra-data plumbing. Batch: chainspec/config/ops.
- `#251` `mm-ux`: preserve multimodal UX/pricing params: image/video steps, FPS, output extraction. Batch: EVM/SPC/precompiles, fees/registries/economics.
- `#252` `mm-ux-dynamic-model-pricing`: preserve model-registry multimodal pricing and fail-closed builder/verifier/wallet reads. Batch: fees/registries/economics.
- `#258` `getDkmsAddr`: preserve DKMS precompile `0x081B`, codec, validation, SPC filtering support, block-time metrics. Batch: EVM/SPC/precompiles, observability.

Noise in this era: broad manifest/lockfile churn is supporting compile noise unless tied to a preserved crate/API; `PR183_REIMPLEMENTATION.md` is context only.

## Late Winter Hardening

- `#260` `single-node`: preserve parent-state AsyncJobTracker duplicate checks in builder/verifier and stale duplicate pool pruning. Batch: payload/verifier, txpool lifecycle.
- `#261` `remove-block-target`: preserve parent-block simulation model and removal of `target_block`/`commit_block` from async flow, codecs, RPC, txpool, verifier. Batch: async core, transaction formats/codecs.
- `#262` `predicate-implementation`: preserve C11 `shouldExecute` predicate reads, parent-state staticcalls, predicate gas budgets, builder skip, verifier rejection. Batch: scheduling/heartbeat, payload/verifier.
- `#264` `ckks-merge-dev`: preserve FHE precompile `0x0807`, FHE capability, input size limit, ABI/deadline extraction, delivery config decoding, output-size Phase 2 pricing. Batch: EVM/SPC/precompiles, fees/registries/economics.
- `#265` `second-phase-delivery`: preserve default async TTL of 500 blocks. Batch: async core.
- `#266` `zk-delegate-bugfixes`: preserve ZK Phase 1 fee constant and fee calculation. Batch: fees/registries/economics.
- `#268` `async-job-active-fix`: preserve `job_exists_and_active()`: active jobs block duplicate commitments, expired jobs can be recommitted. Batch: async core, payload/verifier.
- `#269` `upgradeable-contracts`: preserve upgraded registry storage slots and ERC-7201 owner caveat. Batch: fees/registries/economics.
- `#270` `second-phase-valconstraint`: preserve Phase 2 delivery settlements, `delivery_spc_calls` in receipts/codecs, nested async delivery, contract-derived delivery verification, RPC delivery submission. Batch: async core, transaction formats/codecs, RPC/operator, payload/verifier.
- `#271` `min-stake-stuff`: preserve configurable `base_block_reward` from genesis/chainspec and beneficiary reward application. Batch: chainspec/config/ops, fees/registries/economics.
- `#273` `fix-second-phase-delivery`: preserve canonical AsyncJobTracker-derived SPC context, pool/contract context consistency, build-time SPC reverification, async pool metadata refresh. Batch: payload/verifier, txpool lifecycle.
- `#278` `scheduled-censorship`: preserve scheduled obligation censorship checks, predicate-filtered obligations, capacity-based omission rejection, active-async-job exemption, heartbeat revival support. Batch: scheduling/heartbeat, payload/verifier.
- `#282` `el-build-timelimit`: preserve payload build deadline config, block-size enforcement, settlement/delivery selector offsets, safe Phase 1/Phase 2 input extraction. Batch: payload/verifier, chainspec/config/ops.
- `#286` `agentic-latest`: preserve sovereign/persistent agent codecs, storage refs, precompile constants, Phase 2 deadline offsets, work/spawn fee models, wallet escrow behavior. Batch: EVM/SPC/precompiles, fees/registries/economics.
- `#292` `sadpaths-halt-protection`: preserve DoS bounds: build deadline default, obligation cap, async simulation cap, tx input/calldata limits, builder/verifier obligation consistency. Batch: payload/verifier, async core, txpool lifecycle.
- `#298` `fix-onnx-building-verification-divergence`: preserve temporary ONNX model unavailability as retryable `SYNCING`; permanent invalid precompile requests remain evictable. Batch: chainspec/config/ops.
- `#300` `txpool-pending-eviction`: preserve age eviction for pending pool in addition to queued/basefee pools. Batch: txpool lifecycle.
- `#301` `fix-onnx-blocking-verification-download`: preserve bounded pipeline retry for transient ONNX verification misses before unwind/escalation. Batch: chainspec/config/ops.
- `#304` `async-atomicity-pair-precheck-dev`: preserve atomic original+settlement size/gas precheck and fail-fast if settlement cannot execute after original. Batch: payload/verifier.
- `#299` `post-292-sequencing-rights-deadline`: preserve Phase B/C caps and deadline guards, sequencing-rights deadline skip, and no verifier-side obligation deadline that can diverge from builder membership. Batch: payload/verifier.
- `#305` `schuled-prioriy-overflow`: preserve overflow-safe scheduled fee/gas conversion before tx/obligation creation. Batch: scheduling/heartbeat.
- `#306` `llm-multi-turn-gcs-da`: preserve LLM 30-field ABI decoding and `convo_history: StorageRef` at index 29. Batch: EVM/SPC/precompiles.
- `#307` `sovereign-agent-rpc-validation`: preserve ECIES/user-key validation, supported sovereign agent types `0/4/5/6`, and Phase 2 offset bounds. Batch: async core, RPC/operator.
- `#308` `sovereign-da-support`: preserve async tx pool lifetime of 200 seconds for sovereign-agent Phase 1 processing. Batch: txpool lifecycle.

Noise in this era: `#293` only changes GitHub review workflows; no product behavior to port.

## Spring Policy, Heartbeat, Telemetry, Economics

- `#313` `dev-o1-scheduled-due-window`: preserve constant-time scheduled due-window math, TTL cap 500, saturating max-block arithmetic, zero-`num_calls` handling. Batch: scheduling/heartbeat.
- `#314` `llm-error-pricing`: preserve LLM error settlements with constant fee and encrypted-response fallback to plaintext error decode. Batch: fees/registries/economics.
- `#317` `spc-addr-consts`: preserve canonical `0x08xx` precompile address crate and shared SPC allowlist across builder/verifier/RPC. Batch: EVM/SPC/precompiles.
- `#315` `da-standard`: preserve DA `StorageRef` tuple ABI for FHE and constant DA-error Phase 2 settlements for image/audio/video/FHE. Batch: EVM/SPC/precompiles, fees/registries/economics, payload/verifier.
- `#319` `remove-agent-call`: preserve removal of deprecated `AGENT_CALL_PRECOMPILE` from detection, validation, pool, verifier, fee, and registry paths. Batch: EVM/SPC/precompiles.
- `#321` `add-hermes`: preserve persistent-agent ABI runtime enum `zeroclaw/openclaw/hermes`, 26-field layout, two-phase classifier, stricter callback-cost decoding. Batch: EVM/SPC/precompiles, fees/registries/economics.
- `#325` `block-telemetry`: preserve structured block/tx phase telemetry and per-tx payload execution logs. Batch: observability.
- `#329` `block-telemetry-2`: preserve payload attempt IDs/kinds, empty-payload fallback tracing, and node/basic payload integration. Batch: observability, payload/verifier.
- `#332` `payload-policy-checkpointing`: preserve 300ms build deadline default, deadline guards, obligation/fulfilled/delivery caps, block-build attempts, async sim deadlines, batched SPC reads, C11 filtering. Batch: payload/verifier, observability.
- `#330` `payload-policy-checkpointing-pr`: preserve `BuildPolicyState`, local work-class demotion, near-deadline epsilon, loop check interval, tx-count cap, optional-class short-circuit. Batch: payload/verifier.
- `#331` `heartbeat-static-batch-hydration-pr`: preserve heartbeat tracker hydration from contract storage, `hydrated`/`is_synced`, liveness/revival readers, and `ritual_getHeartbeatTrackerState`. Batch: scheduling/heartbeat, RPC/operator.
- `#336` `block-build-demotion-trace`: preserve demotion capture, primary included tx count, RPC block-build trace exposure. Batch: observability, RPC/operator.
- `#337` `phase0b-probabilistic-skip`: preserve deterministic parent-hash lottery for skipping expensive heartbeat Phase 0b after slow runs, plus primary-cause trace plumbing. Batch: scheduling/heartbeat, payload/verifier, observability.
- `#338` `revival-lane-skip-fifo`: preserve revival-lane filtering, deterministic subset under pressure, `RETH_REVIVAL_*` knobs. Batch: scheduling/heartbeat, payload/verifier.
- `#333` `agent_telemetry`: preserve TEE registry capability IDs `AUTONOMOUS_AGENT=11` and `TELEMETRY=12` as non-executor capabilities. Batch: fees/registries/economics.
- `#339` `factory-launch-pass2-sync`: preserve single `reviveAgent(address,bytes)` scheduling path, owner-caller heartbeat scheduled txs, last-executor-aware selection, on-chain pending-job dedup by owner. Batch: scheduling/heartbeat, payload/verifier.
- `#341` `strict-scheduler-startup-hydration`: preserve startup scan of Scheduler storage, one-time hydration gate, in-memory state replacement, shared max-block helpers, fail-fast on hydration failure. Batch: scheduling/heartbeat.
- `#342` `revival-executor-agent-entropy`: preserve executor-selection entropy mixing parent hash with agent address for same-block revivals. Batch: scheduling/heartbeat.
- `#345` `scheduled-incidents-debug-rpc`: preserve scheduled incident ring buffer, gas/scheduled error capture, decoded call/index fields, `ritual_getScheduledIncidents`. Batch: observability, RPC/operator.
- `#351` `scheduled-gas-extraction-recorder-realign`: preserve broader scheduled incident capture after gas-extraction sad paths became structured 0-gas logs. Batch: observability.
- `#354` `per-category-async-sim-caps`: preserve total/per-category async sim caps, regular-priority allocation, cap observations, combined scheduled/regular sim phases, batched pruning, active-job filter for augmented scheduled obligations. Batch: payload/verifier, scheduling/heartbeat, observability.
- `#356` `agent-spawn-fee-cap`: preserve persistent spawn fee `0.10 RIT` and sovereign-agent iteration/tool fee calibration. Batch: fees/registries/economics.
- `#357` `scheduler-overflow-bitmap-key`: preserve `executedBitmapOverflow` slot derivation using packed `callId` and bucket, including `>=256` tests. Batch: scheduling/heartbeat.

Noise in this era: `#337` contains intermediate conflict-marker artifacts that `#338` resolves; preserve final behavior from `#338`. Manifest, import, formatting, and lockfile churn are supporting noise unless needed to compile a preserved batch.

## Cross-Check Against Feature Map

PR history adds detail that the aggregate map can miss:

- Which behavior was intentionally removed: optimized WS pubsub, deprecated `AGENT_CALL_PRECOMPILE`, `target_block`/`commit_block`.
- Which values changed over time: TTL default 60 to 500, async pool lifetime 200s, build deadline 300ms, agent fee calibration.
- Which behavior is hardening rather than feature creation: duplicate active-job checks, nonce locks, C11 predicates, censorship detection, scheduled overflow bitmap, ONNX retry/sync handling.
- Which APIs are operator/debug surfaces rather than consensus: block-build trace, async sim trace, scheduled incidents, heartbeat tracker state.

Use this file during migration planning to ensure each PR-introduced behavior is either ported, intentionally dropped, or marked no-port with a reason.
