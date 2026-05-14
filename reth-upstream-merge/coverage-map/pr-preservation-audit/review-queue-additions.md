# PR-Preservation Review Queue Additions

### File 0540: crates/transaction-pool/src/traits.rs

- Source: `crates/transaction-pool/src/traits.rs:371-391`
- Claim: PR preservation `ac25b7d7` `Early branch merge` keeps live downstream behavior: first async execution prototype: custom async tx variant.
- PRs: `ac25b7d7`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by ac25b7d7 that exercises `first async execution prototype: custom async tx variant` and fail if the v2.2 port omits or changes it.

### File 0295: crates/ritual-async/src/detector.rs

- Source: `crates/ritual-async/src/detector.rs:595-615`
- Claim: PR preservation `ac25b7d7` `Early branch merge` keeps live downstream behavior: detector-created system tx.
- PRs: `ac25b7d7`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by ac25b7d7 that exercises `detector-created system tx` and fail if the v2.2 port omits or changes it.

### File 0412: crates/rpc/rpc/src/txpool.rs

- Source: `crates/rpc/rpc/src/txpool.rs:8-28`
- Claim: PR preservation `#32` `ritual_async-execution-checkpoint-12` keeps live downstream behavior: detailed async txpool metadata exposed over RPC.
- PRs: `#32`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #32 that exercises `detailed async txpool metadata exposed over RPC` and fail if the v2.2 port omits or changes it.

### File 0421: crates/scheduling/src/singleton.rs

- Source: `crates/scheduling/src/singleton.rs:1-18`
- Claim: PR preservation `8f7946e4` `ritual_move-scheduling-service` keeps live downstream behavior: `crates/scheduling` singleton/service.
- PRs: `8f7946e4`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by 8f7946e4 that exercises ``crates/scheduling` singleton/service` and fail if the v2.2 port omits or changes it.

### File 0098: crates/ethereum/primitives/src/transaction.rs

- Source: `crates/ethereum/primitives/src/transaction.rs:2046-2066`
- Claim: PR preservation `#83` `etherscan-investigation` keeps live downstream behavior: `AsyncCommitment`/`AsyncSettlement` codecs.
- PRs: `#83`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #83 that exercises ``AsyncCommitment`/`AsyncSettlement` codecs` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2310-2330`
- Claim: PR preservation `#83` `etherscan-investigation` keeps live downstream behavior: commitment/settlement flow.
- PRs: `#83`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #83 that exercises `commitment/settlement flow` and fail if the v2.2 port omits or changes it.

### File 0098: crates/ethereum/primitives/src/transaction.rs

- Source: `crates/ethereum/primitives/src/transaction.rs:1-20`
- Claim: PR preservation `#84` `address-etherscan-feedback` keeps live downstream behavior: non-overlapping tx type constants.
- PRs: `#84`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #84 that exercises `non-overlapping tx type constants` and fail if the v2.2 port omits or changes it.

### File 0366: crates/rpc/rpc-api/src/txpool.rs

- Source: `crates/rpc/rpc-api/src/txpool.rs:1-21`
- Claim: PR preservation `#85` `asyncpool-rpc-rename` keeps live downstream behavior: async txpool RPC names.
- PRs: `#85`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #85 that exercises `async txpool RPC names` and fail if the v2.2 port omits or changes it.

### File 0412: crates/rpc/rpc/src/txpool.rs

- Source: `crates/rpc/rpc/src/txpool.rs:62-82`
- Claim: PR preservation `#85` `asyncpool-rpc-rename` keeps live downstream behavior: detailed async metadata access.
- PRs: `#85`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #85 that exercises `detailed async metadata access` and fail if the v2.2 port omits or changes it.

### File 0194: crates/node/builder/src/launch/engine.rs

- Source: `crates/node/builder/src/launch/engine.rs:444-457`
- Claim: PR preservation `#86` `blocking-state-updates` keeps live downstream behavior: blocking canonical-state scheduling handlers for live updates/backfill.
- PRs: `#86`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #86 that exercises `blocking canonical-state scheduling handlers for live updates/backfill` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:1776-1796`
- Claim: PR preservation `#93` `executor-rs` keeps live downstream behavior: parent/simulation context rewriting.
- PRs: `#93`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #93 that exercises `parent/simulation context rewriting` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:3065-3085`
- Claim: PR preservation `#93` `executor-rs` keeps live downstream behavior: settlement origin hashing.
- PRs: `#93`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #93 that exercises `settlement origin hashing` and fail if the v2.2 port omits or changes it.

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Source: `crates/ritual-block-verification/src/verifier.rs:469-489`
- Claim: PR preservation `#93` `executor-rs` keeps live downstream behavior: async-pool pruning. Do not preserve temporary permissive verification behavior unless behind explicit skip-validity config.
- PRs: `#93`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #93 that exercises `async-pool pruning. Do not preserve temporary permissive verification behavior unless behind explicit skip-validity config` and fail if the v2.2 port omits or changes it.

### File 0423: crates/scheduling/src/types.rs

- Source: `crates/scheduling/src/types.rs:158-178`
- Claim: PR preservation `#97` `async-onlyevent` keeps live downstream behavior: scheduler event handling.
- PRs: `#97`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #97 that exercises `scheduler event handling` and fail if the v2.2 port omits or changes it.

### File 0423: crates/scheduling/src/types.rs

- Source: `crates/scheduling/src/types.rs:198-218`
- Claim: PR preservation `#97` `async-onlyevent` keeps live downstream behavior: `Complete` event support.
- PRs: `#97`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #97 that exercises ``Complete` event support` and fail if the v2.2 port omits or changes it.

### File 0295: crates/ritual-async/src/detector.rs

- Source: `crates/ritual-async/src/detector.rs:417-437`
- Claim: PR preservation `#115` `unified-gas-validation-fixes` keeps live downstream behavior: `secret_signature` decoding.
- PRs: `#115`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #115 that exercises ``secret_signature` decoding` and fail if the v2.2 port omits or changes it.

### File 0528: crates/transaction-pool/src/pool/async_pool.rs

- Source: `crates/transaction-pool/src/pool/async_pool.rs:613-633`
- Claim: PR preservation `#115` `unified-gas-validation-fixes` keeps live downstream behavior: raw input for signature validation.
- PRs: `#115`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #115 that exercises `raw input for signature validation` and fail if the v2.2 port omits or changes it.

### File 0540: crates/transaction-pool/src/traits.rs

- Source: `crates/transaction-pool/src/traits.rs:722-742`
- Claim: PR preservation `#115` `unified-gas-validation-fixes` keeps live downstream behavior: time-based async/scheduled eviction.
- PRs: `#115`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #115 that exercises `time-based async/scheduled eviction` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:3471-3491`
- Claim: PR preservation `#122` `scheduling-eviction` keeps live downstream behavior: verification mode for all txs during block verification.
- PRs: `#122`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #122 that exercises `verification mode for all txs during block verification` and fail if the v2.2 port omits or changes it.

### File 0351: crates/ritual-spc-verification/src/types.rs

- Source: `crates/ritual-spc-verification/src/types.rs:205-225`
- Claim: PR preservation `#124` `teeda-policy` keeps live downstream behavior: ExecutorRegistry event/storage migration for SPC executor data.
- PRs: `#124`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #124 that exercises `ExecutorRegistry event/storage migration for SPC executor data` and fail if the v2.2 port omits or changes it.

### File 0274: crates/ritual-async-commitment-validator/src/lib.rs

- Source: `crates/ritual-async-commitment-validator/src/lib.rs:6-26`
- Claim: PR preservation `#145` `valconstraints-async-commitment` keeps live downstream behavior: verifier re-simulation of async origin tx at parent/commit context.
- PRs: `#145`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #145 that exercises `verifier re-simulation of async origin tx at parent/commit context` and fail if the v2.2 port omits or changes it.

### File 0107: crates/evm/src/execute.rs

- Source: `crates/evm/src/execute.rs:26-46`
- Claim: PR preservation `#149` `executor-migration` keeps live downstream behavior: direct registry storage reads for executor/SPC public key data.
- PRs: `#149`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #149 that exercises `direct registry storage reads for executor/SPC public key data` and fail if the v2.2 port omits or changes it.

### File 0416: crates/scheduling/src/contract.rs

- Source: `crates/scheduling/src/contract.rs:5-25`
- Claim: PR preservation `#150` `scheduling-refactor` keeps live downstream behavior: Scheduler API change to `startBlock/numCalls`.
- PRs: `#150`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #150 that exercises `Scheduler API change to `startBlock/numCalls`` and fail if the v2.2 port omits or changes it.

### File 0278: crates/ritual-async-fees/src/gas.rs

- Source: `crates/ritual-async-fees/src/gas.rs:3-23`
- Claim: PR preservation `#167` `async-fixes-revive-to-dev` keeps live downstream behavior: system tx gas accounting: async commitments charge zero block gas.
- PRs: `#167`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #167 that exercises `system tx gas accounting: async commitments charge zero block gas` and fail if the v2.2 port omits or changes it.

### File 0250: crates/primitives-traits/src/transaction/signed.rs

- Source: `crates/primitives-traits/src/transaction/signed.rs:137-157`
- Claim: PR preservation `#220` `jungle-scheduled` keeps live downstream behavior: scheduled tx codec/receipt integration.
- PRs: `#220`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #220 that exercises `scheduled tx codec/receipt integration` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:397-417`
- Claim: PR preservation `#230` `jungle-ass` keeps live downstream behavior: sequencing-rights classification/reordering plus verifier checks.
- PRs: `#230`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #230 that exercises `sequencing-rights classification/reordering plus verifier checks` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:414-434`
- Claim: PR preservation `#231` `rpc-async-feedback` keeps live downstream behavior: parity across scheduled/sequencing/async paths.
- PRs: `#231`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #231 that exercises `parity across scheduled/sequencing/async paths` and fail if the v2.2 port omits or changes it.

### File 0236: crates/payload/builder/src/service.rs

- Source: `crates/payload/builder/src/service.rs:57-77`
- Claim: PR preservation `#243` `eager-payload` keeps live downstream behavior: operational payload behavior only if still needed: wait for pending payload with empty fallback.
- PRs: `#243`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #243 that exercises `operational payload behavior only if still needed: wait for pending payload with empty fallback` and fail if the v2.2 port omits or changes it.

### File 0276: crates/ritual-async-fees/src/constants.rs

- Source: `crates/ritual-async-fees/src/constants.rs:317-337`
- Claim: PR preservation `#246` `separate-capabilities` keeps live downstream behavior: default model registry address.
- PRs: `#246`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #246 that exercises `default model registry address` and fail if the v2.2 port omits or changes it.

### File 0402: crates/rpc/rpc/src/eth/helpers/pending_block.rs

- Source: `crates/rpc/rpc/src/eth/helpers/pending_block.rs:72-78`
- Claim: PR preservation `#249` `embed-multisig` keeps live downstream behavior: max-extra-data plumbing.
- PRs: `#249`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #249 that exercises `max-extra-data plumbing` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:4215-4235`
- Claim: PR preservation `#260` `single-node` keeps live downstream behavior: parent-state AsyncJobTracker duplicate checks in builder/verifier.
- PRs: `#260`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #260 that exercises `parent-state AsyncJobTracker duplicate checks in builder/verifier` and fail if the v2.2 port omits or changes it.

### File 0333: crates/ritual-scheduled-verification/src/predicate.rs

- Source: `crates/ritual-scheduled-verification/src/predicate.rs:98-118`
- Claim: PR preservation `#262` `predicate-implementation` keeps live downstream behavior: C11 `shouldExecute` predicate reads.
- PRs: `#262`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #262 that exercises `C11 `shouldExecute` predicate reads` and fail if the v2.2 port omits or changes it.

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Source: `crates/ritual-block-verification/src/verifier.rs:1632-1652`
- Claim: PR preservation `#268` `async-job-active-fix` keeps live downstream behavior: `job_exists_and_active()`: active jobs block duplicate commitments.
- PRs: `#268`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #268 that exercises ``job_exists_and_active()`: active jobs block duplicate commitments` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2741-2761`
- Claim: PR preservation `#270` `second-phase-valconstraint` keeps live downstream behavior: `delivery_spc_calls` in receipts/codecs.
- PRs: `#270`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #270 that exercises ``delivery_spc_calls` in receipts/codecs` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2967-2987`
- Claim: PR preservation `#270` `second-phase-valconstraint` keeps live downstream behavior: contract-derived delivery verification.
- PRs: `#270`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #270 that exercises `contract-derived delivery verification` and fail if the v2.2 port omits or changes it.

### File 0028: crates/chainspec/src/spec.rs

- Source: `crates/chainspec/src/spec.rs:369-389`
- Claim: PR preservation `#271` `min-stake-stuff` keeps live downstream behavior: configurable `base_block_reward` from genesis/chainspec.
- PRs: `#271`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #271 that exercises `configurable `base_block_reward` from genesis/chainspec` and fail if the v2.2 port omits or changes it.

### File 0079: crates/ethereum/evm/src/execute.rs

- Source: `crates/ethereum/evm/src/execute.rs:885-905`
- Claim: PR preservation `#271` `min-stake-stuff` keeps live downstream behavior: beneficiary reward application.
- PRs: `#271`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #271 that exercises `beneficiary reward application` and fail if the v2.2 port omits or changes it.

### File 0285: crates/ritual-async-fees/src/wallet.rs

- Source: `crates/ritual-async-fees/src/wallet.rs:19-39`
- Claim: PR preservation `#286` `agentic-latest` keeps live downstream behavior: precompile constants.
- PRs: `#286`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #286 that exercises `precompile constants` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:1240-1260`
- Claim: PR preservation `#292` `sadpaths-halt-protection` keeps live downstream behavior: DoS bounds: build deadline default.
- PRs: `#292`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #292 that exercises `DoS bounds: build deadline default` and fail if the v2.2 port omits or changes it.

### File 0064: crates/engine/tree/src/tree/mod.rs

- Source: `crates/engine/tree/src/tree/mod.rs:2907-2927`
- Claim: PR preservation `#298` `fix-onnx-building-verification-divergence` keeps live downstream behavior: temporary ONNX model unavailability as retryable `SYNCING`.
- PRs: `#298`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #298 that exercises `temporary ONNX model unavailability as retryable `SYNCING`` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:3461-3481`
- Claim: PR preservation `#298` `fix-onnx-building-verification-divergence` keeps live downstream behavior: permanent invalid precompile requests remain evictable.
- PRs: `#298`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #298 that exercises `permanent invalid precompile requests remain evictable` and fail if the v2.2 port omits or changes it.

### File 0525: crates/transaction-pool/src/maintain.rs

- Source: `crates/transaction-pool/src/maintain.rs:57-77`
- Claim: PR preservation `#300` `txpool-pending-eviction` keeps live downstream behavior: age eviction for pending pool in addition to queued/basefee pools.
- PRs: `#300`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #300 that exercises `age eviction for pending pool in addition to queued/basefee pools` and fail if the v2.2 port omits or changes it.

### File 0427: crates/stages/api/src/pipeline/mod.rs

- Source: `crates/stages/api/src/pipeline/mod.rs:454-474`
- Claim: PR preservation `#301` `fix-onnx-blocking-verification-download` keeps live downstream behavior: bounded pipeline retry for transient ONNX verification misses before unwind/escalation.
- PRs: `#301`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #301 that exercises `bounded pipeline retry for transient ONNX verification misses before unwind/escalation` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:3808-3828`
- Claim: PR preservation `#304` `async-atomicity-pair-precheck-dev` keeps live downstream behavior: fail-fast if settlement cannot execute after original.
- PRs: `#304`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #304 that exercises `fail-fast if settlement cannot execute after original` and fail if the v2.2 port omits or changes it.

### File 0281: crates/ritual-async-fees/src/llm.rs

- Source: `crates/ritual-async-fees/src/llm.rs:8-28`
- Claim: PR preservation `#314` `llm-error-pricing` keeps live downstream behavior: encrypted-response fallback to plaintext error decode.
- PRs: `#314`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #314 that exercises `encrypted-response fallback to plaintext error decode` and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:349-369`
- Claim: PR preservation `#315` `da-standard` keeps live downstream behavior: DA `StorageRef` tuple ABI for FHE.
- PRs: `#315`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #315 that exercises `DA `StorageRef` tuple ABI for FHE` and fail if the v2.2 port omits or changes it.

### File 0285: crates/ritual-async-fees/src/wallet.rs

- Source: `crates/ritual-async-fees/src/wallet.rs:291-311`
- Claim: PR preservation `#321` `add-hermes` keeps live downstream behavior: stricter callback-cost decoding.
- PRs: `#321`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #321 that exercises `stricter callback-cost decoding` and fail if the v2.2 port omits or changes it.

### File 0410: crates/rpc/rpc/src/ritual.rs

- Source: `crates/rpc/rpc/src/ritual.rs:780-800`
- Claim: PR preservation `#332` `payload-policy-checkpointing` keeps live downstream behavior: block-build attempts.
- PRs: `#332`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #332 that exercises `block-build attempts` and fail if the v2.2 port omits or changes it.

### File 0415: crates/scheduling/src/canonical.rs

- Source: `crates/scheduling/src/canonical.rs:143-163`
- Claim: PR preservation `#331` `heartbeat-static-batch-hydration-pr` keeps live downstream behavior: `hydrated`/`is_synced`.
- PRs: `#331`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #331 that exercises ``hydrated`/`is_synced`` and fail if the v2.2 port omits or changes it.

### File 0357: crates/ritual-tee-registry-reader/src/reader.rs

- Source: `crates/ritual-tee-registry-reader/src/reader.rs:180-200`
- Claim: PR preservation `#333` `agent_telemetry` keeps live downstream behavior: `TELEMETRY=12` as non-executor capabilities.
- PRs: `#333`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #333 that exercises ``TELEMETRY=12` as non-executor capabilities` and fail if the v2.2 port omits or changes it.

### File 0415: crates/scheduling/src/canonical.rs

- Source: `crates/scheduling/src/canonical.rs:1-20`
- Claim: PR preservation `#339` `factory-launch-pass2-sync` keeps live downstream behavior: owner-caller heartbeat scheduled txs.
- PRs: `#339`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #339 that exercises `owner-caller heartbeat scheduled txs` and fail if the v2.2 port omits or changes it.

### File 0415: crates/scheduling/src/canonical.rs

- Source: `crates/scheduling/src/canonical.rs:387-407`
- Claim: PR preservation `#339` `factory-launch-pass2-sync` keeps live downstream behavior: last-executor-aware selection.
- PRs: `#339`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #339 that exercises `last-executor-aware selection` and fail if the v2.2 port omits or changes it.

### File 0423: crates/scheduling/src/types.rs

- Source: `crates/scheduling/src/types.rs:217-237`
- Claim: PR preservation `#341` `strict-scheduler-startup-hydration` keeps live downstream behavior: one-time hydration gate.
- PRs: `#341`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #341 that exercises `one-time hydration gate` and fail if the v2.2 port omits or changes it.

### File 0421: crates/scheduling/src/singleton.rs

- Source: `crates/scheduling/src/singleton.rs:87-107`
- Claim: PR preservation `#341` `strict-scheduler-startup-hydration` keeps live downstream behavior: in-memory state replacement.
- PRs: `#341`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #341 that exercises `in-memory state replacement` and fail if the v2.2 port omits or changes it.

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Source: `crates/ritual-scheduled-verification/src/lib.rs:2170-2190`
- Claim: PR preservation `#341` `strict-scheduler-startup-hydration` keeps live downstream behavior: shared max-block helpers.
- PRs: `#341`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #341 that exercises `shared max-block helpers` and fail if the v2.2 port omits or changes it.

### File 0521: crates/transaction-pool/src/blocking_handlers.rs

- Source: `crates/transaction-pool/src/blocking_handlers.rs:276-284`
- Claim: PR preservation `#341` `strict-scheduler-startup-hydration` keeps live downstream behavior: fail-fast on hydration failure.
- PRs: `#341`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #341 that exercises `fail-fast on hydration failure` and fail if the v2.2 port omits or changes it.

### File 0415: crates/scheduling/src/canonical.rs

- Source: `crates/scheduling/src/canonical.rs:86-106`
- Claim: PR preservation `#342` `revival-executor-agent-entropy` keeps live downstream behavior: executor-selection entropy mixing parent hash with agent address for same-block revivals.
- PRs: `#342`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #342 that exercises `executor-selection entropy mixing parent hash with agent address for same-block revivals` and fail if the v2.2 port omits or changes it.

### File 0365: crates/rpc/rpc-api/src/ritual.rs

- Source: `crates/rpc/rpc-api/src/ritual.rs:343-363`
- Claim: PR preservation `#345` `scheduled-incidents-debug-rpc` keeps live downstream behavior: gas/scheduled error capture.
- PRs: `#345`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #345 that exercises `gas/scheduled error capture` and fail if the v2.2 port omits or changes it.

### File 0313: crates/ritual-metrics/src/scheduling.rs

- Source: `crates/ritual-metrics/src/scheduling.rs:27-47`
- Claim: PR preservation `#345` `scheduled-incidents-debug-rpc` keeps live downstream behavior: `ritual_getScheduledIncidents`.
- PRs: `#345`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #345 that exercises ``ritual_getScheduledIncidents`` and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:167-187`
- Claim: PR preservation `#351` `scheduled-gas-extraction-recorder-realign` keeps live downstream behavior: broader scheduled incident capture after gas-extraction sad paths became structured 0-gas logs.
- PRs: `#351`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #351 that exercises `broader scheduled incident capture after gas-extraction sad paths became structured 0-gas logs` and fail if the v2.2 port omits or changes it.

### File 0276: crates/ritual-async-fees/src/constants.rs

- Source: `crates/ritual-async-fees/src/constants.rs:188-208`
- Claim: PR preservation `#356` `agent-spawn-fee-cap` keeps live downstream behavior: sovereign-agent iteration/tool fee calibration.
- PRs: `#356`
- Negative test: Replay or unit-test the smallest downstream scenario introduced by #356 that exercises `sovereign-agent iteration/tool fee calibration` and fail if the v2.2 port omits or changes it.
