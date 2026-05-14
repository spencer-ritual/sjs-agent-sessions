# Fresh Restart Review Queue

Entries are added only after their per-file JSON has been persisted.

- `file-0026-atom-0001` (`file-0026`, `crates/chainspec/src/api.rs`, `structural_equivalent`)
  - Hunk: `@@ -65,6 +65,10 @@ pub trait EthChainSpec: Send + Sync + Unpin + Debug {`
  - Claim: EthChainSpec exposes a required chain-specific optional maximum header extra_data byte limit; None means the chain has no limit.
  - Required change: Destination callers receive the same API shape and ChainSpec overrides the method, so core ChainSpec behavior is covered. However, the destination trait default is not exact and not renamed_exact relative to the downstream abstract method: the downstream patch forced every EthChainSpec implementer to state its own limit, while the port silently assigns Some(MAXIMUM_EXTRA_DATA_SIZE) to any non-overriding implementer. This is structural equivalence only for implementers whose intended limit is the Ethereum default; it needs review for custom chains that require None or a custom size.

- `file-0047-atom-0001` (`file-0047`, `crates/consensus/common/Cargo.toml`, `missing`)
  - Hunk: `@@ -19,6 +19,7 @@ reth-consensus.workspace = true`
  - Claim: The consensus-common crate declares a tracing dependency so validation.rs can emit debug/error logs around transaction-root validation under the ritual::async target.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0048-atom-0001` (`file-0048`, `crates/consensus/common/src/validation.rs`, `missing`)
  - Hunk: `@@ -95,14 +94,39 @@ where`
  - Claim: Before comparing body and header transaction roots, validation emits a ritual::async debug event containing the header root, calculated root, and transaction count.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0048-atom-0002` (`file-0048`, `crates/consensus/common/src/validation.rs`, `missing`)
  - Hunk: `@@ -95,14 +94,39 @@ where`
  - Claim: Validation emits ritual::async debug events for the first three transaction indexes while diagnosing transaction-root validation.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0048-atom-0003` (`file-0048`, `crates/consensus/common/src/validation.rs`, `missing`)
  - Hunk: `@@ -95,14 +94,39 @@ where`
  - Claim: On transaction-root mismatch, validation emits a ritual::async error event with both roots before returning BodyTransactionRootDiff.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0056-atom-0001` (`file-0056`, `crates/engine/tree/Cargo.toml`, `missing`)
  - Hunk: `@@ -53,6 +53,7 @@ mini-moka = { workspace = true, features = ["sync"] }`
  - Claim: The engine-tree crate declares the Ritual metrics workspace dependency, enabling downstream engine/tree instrumentation that depends on the `ritual-metrics` crate.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0062-atom-0001` (`file-0062`, `crates/engine/tree/src/tree/cached_state.rs`, `missing`)
  - Hunk: `@@ -15,9 +15,97 @@`
  - Claim: State cache time-to-live and idle expiration are runtime-configurable through RETH_STATE_CACHE_TTL_SECS and RETH_STATE_CACHE_IDLE_SECS, with 2-hour and 1-hour defaults.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0062-atom-0002` (`file-0062`, `crates/engine/tree/src/tree/cached_state.rs`, `missing`)
  - Hunk: `@@ -15,9 +15,97 @@`
  - Claim: The cache builds a process-global set of pinned system contract addresses from Ritual env vars and optional RETH_PINNED_CONTRACTS additions, and uses it to identify contracts that should not be evicted by regular time-based cache policy.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0062-atom-0003` (`file-0062`, `crates/engine/tree/src/tree/cached_state.rs`, `missing`)
  - Hunk: `@@ -115,9 +203,23 @@ and @@ -350,16 +492,20 @@`
  - Claim: Pinned contract account reads and post-execution account updates use a separate pinned_account_cache so pinned accounts are cached without TTL but still invalidated or refreshed when block state changes destroy or modify them.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0062-atom-0004` (`file-0062`, `crates/engine/tree/src/tree/cached_state.rs`, `missing`)
  - Hunk: `@@ -296,20 +405,45 @@ and @@ -458,11 +611,57 @@`
  - Claim: Pinned contract storage uses a separate non-expiring pinned_storage_cache for reads, writes, invalidation, and metrics accounting so system-contract storage remains hot without bypassing correctness updates.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0002` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -89,7 +92,13 @@`
  - Claim: Backfill pipeline sync should not be triggered until the live-sync gap exceeds 64 blocks, replacing the epoch-slot threshold with a Ritual-tuned threshold and documented rationale.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0003` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2146,6 +2155,8 @@`
  - Claim: Every canonical-chain update records the execution-layer head hash, number, and timestamp through Ritual block metrics before notifications are emitted.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0004` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2173,6 +2184,24 @@`
  - Claim: Canonical commit and reorg updates emit Ritual transaction finalization metrics for the complete NewCanonicalChain update.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0005` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `missing`)
  - Hunk: `@@ -2173,6 +2184,24 @@`
  - Claim: Canonical updates emit per-block Ritual SPC provider debug evidence for each newly canonical block, even though the historical header cache has been removed.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0006` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2342,13 +2371,17 @@ and @@ -2357,6 +2390,18 @@`
  - Claim: Disconnected blocks with missing parent state emit a Ritual block-acceptance state-provider metric with skipped status and missing_parent_state reason before buffering the block.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0007` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2383,11 +2428,47 @@`
  - Claim: Parent-header consensus validation during block acceptance emits Ritual timing metrics for both success and failure outcomes.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0008` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2383,11 +2428,47 @@`
  - Claim: Successful state-provider construction during block acceptance emits a Ritual timing metric separate from the missing-parent skipped case.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0009` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `missing`)
  - Hunk: `@@ -2409,6 +2490,7 @@ through @@ -2432,6 +2525,18 @@`
  - Claim: Trie-input preparation during block acceptance emits Ritual timing metrics for computed and skipped paths, distinguishing parallel-state-root-disabled skips.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0010` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2446,12 +2551,24 @@`
  - Claim: Successful block execution during engine-tree block acceptance emits a Ritual block_accept_execution timing metric around the executor call.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0011` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2459,25 +2576,76 @@`
  - Claim: Post-execution consensus validation emits Ritual block-acceptance timing metrics for both valid output and invalid output error paths.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0012` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2459,25 +2576,76 @@`
  - Claim: Ritual post-execution payload validation emits explicit block-acceptance timing metrics for success and failure paths.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0013` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2529,6 +2697,7 @@ through @@ -2541,9 +2710,22 @@`
  - Claim: State-root calculation emits Ritual acceptance telemetry that distinguishes parallel state root success from serial fallback.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0064-atom-0014` (`file-0064`, `crates/engine/tree/src/tree/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -2725,6 +2907,27 @@`
  - Claim: Temporary ONNX model unavailability during verification is treated as SYNCING and is not cached as INVALID, allowing the block to be retried after model download/backfill.
  - Required change: Review destination evidence and either prove equivalence or restore behavior.

- `file-0107-atom-0001` (`file-0107`, `crates/evm/src/execute.rs`, `structural_equivalent`)
  - Hunk: `@@ -254,6 +254,23 @@ pub trait BlockBuilder`
  - Claim: The downstream Reth BlockBuilder API gained a system-transaction execution path where the caller supplies an explicit block/receipt gas contribution derived from the execution result, and the method returns both actual EVM gas used and the contribution used for block accounting.
  - Required change: The destination preserves the API-level behavior through a v2-shaped Reth BlockBuilder method and delegates the detailed explicit-gas contract to the internal Alloy EVM dependency. This is not exact because the original source text is split across the v2 Reth wrapper and the Alloy EVM executor trait, and the old ExecutorTx surface changed.

- `file-0414-atom-0001` (`file-0414`, `crates/scheduling/Cargo.toml`, `partial`)
  - Hunk: `@@ -0,0 +1,42 @@`
  - Claim: The old divergence introduced a standalone `ritual-scheduling` crate as the scheduling service boundary.
  - Required change: Non-exact ownership split: the old crate manifest is intentionally not present, while behavior-bearing scheduled code is split into verification and block-building crates. This proves broad ownership migration, not complete API compatibility for any stale `ritual-scheduling` consumers.

- `file-0415-atom-0001` (`file-0415`, `crates/scheduling/src/canonical.rs`, `partial`)
  - Hunk: `@@ -0,0 +1,544 @@`
  - Claim: The old file processes canonical state changes through a global scheduler singleton and submits due scheduled transactions to a callback.
  - Required change: The live scheduling path moved from canonical-event callback submission to payload-builder synthesis plus verifier censorship checks. This preserves the main obligation surface but is non-exact: there is no global event-driven `SynchronousScheduler` catch-up path in the destination.

- `file-0415-atom-0002` (`file-0415`, `crates/scheduling/src/canonical.rs`, `structural_equivalent`)
  - Hunk: `crates/scheduling/src/canonical.rs:143-183`
  - Claim: The old canonical path has a strict startup hydration gate before normal event processing.
  - Required change: Restart safety is achieved by reading Scheduler storage on demand rather than hydrating a singleton. This is a structural replacement, not an exact port of the one-time hydration gate.

- `file-0415-atom-0003` (`file-0415`, `crates/scheduling/src/canonical.rs`, `missing`)
  - Hunk: `crates/scheduling/src/canonical.rs:1-115 and heartbeat revival loop`
  - Claim: The old canonical path synthesizes heartbeat revival transactions, chooses an HTTP executor with parent-hash plus agent-address entropy, and uses owner-caller context.
  - Required change: Not equivalent based on current evidence: heartbeat state reading/tracking exists, but the old builder-side revival transaction synthesis and executor-selection entropy were not found in the v2.2 port.

- `file-0415-atom-0004` (`file-0415`, `crates/scheduling/src/canonical.rs`, `partial`)
  - Hunk: `feature-preservation-map section 5 / source PRs #331, #339, #342`
  - Claim: The grouped preservation claims attached to this file require hydration and heartbeat revival semantics to survive the v2.2 port.
  - Required change: Hydration/scheduled-obligation preservation is structurally covered, but heartbeat revival creation and executor entropy remain missing by search evidence; therefore the grouped claim is only partial.

- `file-0416-atom-0001` (`file-0416`, `crates/scheduling/src/contract.rs`, `partial`)
  - Hunk: `@@ -0,0 +1,1035 @@`
  - Claim: The old file decodes Scheduler event logs and updates in-memory scheduler state from CallScheduled/Cancelled/Executed/Completed/failure/skip events.
  - Required change: Non-exact replacement: scheduled correctness is driven by storage scans and verifier obligations rather than by preserving the old Scheduler event decoder and internal event length state.

- `file-0416-atom-0002` (`file-0416`, `crates/scheduling/src/contract.rs`, `structural_equivalent`)
  - Hunk: `crates/scheduling/src/contract.rs:5-80`
  - Claim: The old file adapts Scheduler API migration from `(initialBlock,maxBlockNumber)` to `(startBlock,numCalls)` and derives expiry bounds.
  - Required change: The API migration math is preserved structurally in the destination storage model, but not via the old event-derived compatibility fields.

- `file-0417-atom-0001` (`file-0417`, `crates/scheduling/src/events.rs`, `partial`)
  - Hunk: `@@ -0,0 +1,24 @@`
  - Claim: The old crate exposes a small internal event model for scheduling service block/call transitions.
  - Required change: The old service-event API is not preserved; its behavior-bearing purpose is partially replaced by storage-derived obligations and verifier checks.

- `file-0419-atom-0001` (`file-0419`, `crates/scheduling/src/lib.rs`, `partial`)
  - Hunk: `@@ -0,0 +1,29 @@`
  - Claim: The old crate root exposes a unified scheduling service API including canonical processing, contract monitoring, singleton state, transaction creation, and types.
  - Required change: The behavior-bearing surface is split across v2.2 crates and hooks; the old unified crate API is not exact-preserved.

- `file-0420-atom-0001` (`file-0420`, `crates/scheduling/src/service.rs`, `partial`)
  - Hunk: `@@ -0,0 +1,58 @@`
  - Claim: The old file wraps the scheduler contract monitor in a block-processing service loop.
  - Required change: The old service loop is not exact-preserved; its execution responsibility is absorbed by payload assembly and verification hooks.

- `file-0421-atom-0001` (`file-0421`, `crates/scheduling/src/singleton.rs`, `partial`)
  - Hunk: `@@ -0,0 +1,519 @@`
  - Claim: The old file implements a globally accessible in-memory scheduler singleton.
  - Required change: The state machine is non-exact: process-global memory is intentionally avoided, while storage-derived calls and obligation scans preserve the behavior needed for consensus scheduling.

- `file-0421-atom-0002` (`file-0421`, `crates/scheduling/src/singleton.rs`, `structural_equivalent`)
  - Hunk: `crates/scheduling/src/singleton.rs:87-150`
  - Claim: The old singleton can replace in-memory scheduler state from Scheduler contract storage on startup.
  - Required change: Hydration behavior is structurally preserved as direct parent-state reads; no exact state replacement API exists because the singleton is gone.

- `file-0421-atom-0003` (`file-0421`, `crates/scheduling/src/singleton.rs`, `structural_equivalent`)
  - Hunk: `feature-preservation-map / PR #341`
  - Claim: The preservation atom requires no stale or partially hydrated scheduled state during startup.
  - Required change: The one-time gate is not exact-preserved, but stale-memory risk is mitigated by eliminating the memory dependency for builder/verifier decisions.

- `file-0422-atom-0001` (`file-0422`, `crates/scheduling/src/transaction.rs`, `structural_equivalent`)
  - Hunk: `@@ -0,0 +1,112 @@`
  - Claim: The old file creates protocol `TxScheduled` transactions for Scheduler execution.
  - Required change: The transaction synthesis behavior is structurally preserved under the split block-building crate and verifier hash reconstruction, though the old API and singleton scheduler address lookup are gone.

- `file-0422-atom-0002` (`file-0422`, `crates/scheduling/src/transaction.rs`, `partial`)
  - Hunk: `@@ -0,0 +113,157 @@`
  - Claim: The old file creates heartbeat system transactions that bypass Scheduler and target AgentHeartbeat.
  - Required change: Only recognition/allowance of heartbeat scheduled transactions was found; builder-side heartbeat transaction construction was not found, so synthesis is partial at best.

- `file-0422-atom-0003` (`file-0422`, `crates/scheduling/src/transaction.rs`, `missing`)
  - Hunk: `transaction.rs tests: fee overflow rejection`
  - Claim: The old helper rejects scheduled transaction creation when fee fields exceed `u128::MAX`.
  - Required change: Not exact: the old explicit overflow rejection is absent. This may be acceptable if the current Alloy scheduled transaction model supports `U256` fee fields end-to-end, but the negative path is not preserved as written.

- `file-0423-atom-0001` (`file-0423`, `crates/scheduling/src/types.rs`, `partial`)
  - Hunk: `@@ -0,0 +1,90 @@`
  - Claim: The old file defines Scheduler service event statuses, scheduling errors, and block info for the event-driven service.
  - Required change: The old service event/error taxonomy is not exact-preserved; destination errors and states are organized around storage verification and block validation.

- `file-0423-atom-0002` (`file-0423`, `crates/scheduling/src/types.rs`, `structural_equivalent`)
  - Hunk: `@@ -0,0 +80,158 @@`
  - Claim: The old scheduled call model carries Scheduler call fields plus calldata and origin_hash for deterministic transaction creation.
  - Required change: The field model is structurally equivalent for consensus-critical scheduled execution, with origin_hash split out of the call struct and callback calldata represented by Scheduler.execute input construction.

- `file-0423-atom-0003` (`file-0423`, `crates/scheduling/src/types.rs`, `partial`)
  - Hunk: `Call::should_fire_at_block and related tests`
  - Claim: The old type-level firing logic only fires on exact modulo-aligned target blocks.
  - Required change: Not exact by design: v2.2 uses TTL-window obligations instead of the old exact-block modulo helper. This likely aligns better with Scheduler semantics but does not preserve the old tests literally.

- `file-0423-atom-0004` (`file-0423`, `crates/scheduling/src/types.rs`, `partial`)
  - Hunk: `SchedulerServiceState, FrequencyIndex, replace_calls tests`
  - Claim: The old file maintains lock-free in-memory scheduler state with frequency indexing and replacement semantics.
  - Required change: The old in-memory data structure is not exact-preserved. Its externally important result, a set of due non-executed obligations, is recomputed from parent state.

- `file-0423-atom-0005` (`file-0423`, `crates/scheduling/src/types.rs`, `structural_equivalent`)
  - Hunk: `startup hydration gate methods and tests`
  - Claim: The old type-level startup hydration gate prevents concurrent or partially failed singleton hydration.
  - Required change: The exact gate is absent because there is no singleton hydration. The safety property is structurally replaced by avoiding process-local hydrated state for consensus decisions.

- `file-0424-atom-0001` (`file-0424`, `crates/stages/api/Cargo.toml`, `missing`)
  - Hunk: `@@ -48,6 +48,7 @@ [features]`
  - Claim: The downstream fork exposes an `async-context` feature on `reth-stages-api` and forwards it to `reth-errors/async-context`, allowing stages pipeline code to compile async-context-specific error handling.
  - Required change: Add `async-context = ["reth-errors/async-context"]` to `crates/stages/api/Cargo.toml` if the pipeline ONNX retry path is intended to remain live in the v2.2 port, or record an explicit scope decision that stages pipeline async-context handling is intentionally omitted.

- `file-0427-atom-0001` (`file-0427`, `crates/stages/api/src/pipeline/mod.rs`, `missing`)
  - Hunk: `@@ -31,6 +31,11 @@; @@ -385,6 +391,8 @@; @@ -423,6 +431,55 @@; @@ -474,17 +537,66 @@; @@ -537,6 +649,28 @@; @@ -1079,6 +1213,102 @@`
  - Claim: Temporary ONNX model unavailability during staged pipeline execution should receive three bounded one-second retries before the normal unwind/bad-block path, preserving transient verifier download tolerance.
  - Required change: Port the bounded ONNX-unavailable retry handling and tests into the v2.2 `Pipeline` path, or record an explicit scope decision that staged sync may unwind immediately for transient ONNX model unavailability.

- `file-0431-atom-0001` (`file-0431`, `crates/stages/stages/src/stages/execution.rs`, `missing`)
  - Hunk: `@@ -65,7 +65,6 @@; @@ -94,6 +93,27 @@; @@ -117,9 +137,19 @@; @@ -352,8 +382,25 @@`
  - Claim: ExecutionStage supports an optional blocking handler that observes canonical state updates during backfill block execution.
  - Required change: Port `ExecutionStage::with_blocking_handler` and its per-block backfill invocation if consumers still depend on this hook, or document that the v2.2 port intentionally replaced it with another canonical-state notification path.

- `file-0452-atom-0001` (`file-0452`, `crates/storage/codecs/Cargo.toml`, `missing`)
  - Hunk: `@@ -30,12 +30,13 @@ bytes.workspace = true`
  - Claim: The old storage-codecs crate added a direct `tracing` dependency so compact codec instrumentation in the transaction codec files could compile.
  - Required change: Not equivalent as an observability/build surface: the destination removed the old codec debug logging and therefore does not require or provide this dependency.

- `file-0463-atom-0005` (`file-0463`, `crates/storage/codecs/src/alloy/transaction/ethereum.rs`, `missing`)
  - Hunk: `@@ -94,22 +134,50 @@ TxType::Passkey fallback`
  - Claim: The old divergence allowed the non-passkey envelope decode path to rebuild `TxType::Passkey` using a standard secp256k1 signature as a compatibility fallback.
  - Required change: Not equivalent for compact bytes that identify `TxType::Passkey` without the dedicated passkey flag. The destination intentionally requires the passkey-signature path, but old fallback compatibility is not preserved.

- `file-0468-atom-0004` (`file-0468`, `crates/storage/codecs/src/alloy/transaction/spc_call.rs`, `missing`)
  - Hunk: `@@ -0,0 +1,349 @@ #[cfg(test)] mod tests`
  - Claim: The old downstream file carried focused SPC compact round-trip tests for normal, empty, large, and wrapper cases.
  - Required change: Production codec behavior is structurally preserved, but the old focused test coverage is not present in this file.

- `file-0469-atom-0006` (`file-0469`, `crates/storage/codecs/src/alloy/transaction/txtype.rs`, `missing`)
  - Hunk: `@@ -66,6 +89,12 @@ mod tests`
  - Claim: The old downstream tests asserted scheduled, async commitment, and async settlement TxType compact identifiers in both encode and decode directions.
  - Required change: Production TxType behavior is present, but the old focused test cases for three custom identifiers are missing.

- `file-0470-atom-0001` (`file-0470`, `crates/storage/codecs/src/lib.rs`, `missing`)
  - Hunk: `@@ -236,12 +236,14 @@ impl<T> Compact for &[T]`
  - Claim: The old divergence changed `Compact for &[T]::to_compact` to return the number of bytes written, which is needed when `Vec<T>` is nested in `Option<T>` and the outer option records element length.
  - Required change: Not equivalent: destination keeps upstream zero-length reporting for slices, so an `Option<Vec<T>>` can encode bytes while reporting length 0 to the enclosing option.

- `file-0511-atom-0001` (`file-0511`, `crates/tracing/Cargo.toml`, `missing`)
  - Hunk: `@@ -20,3 +20,4 @@ tracing-logfmt.workspace = true`
  - Claim: The old divergence adds `serde_json` to the tracing crate for a custom Ritual JSON router.
  - Required change: Not equivalent: the dependency needed by the old custom JSON router is not present. Current `reth-tracing-otlp` is not a behavioral replacement for the old target-specific Ritual JSON router.

- `file-0512-atom-0001` (`file-0512`, `crates/tracing/src/lib.rs`, `missing`)
  - Hunk: `@@ -51,10 +51,12 @@ pub use tracing_subscriber;`
  - Claim: The old divergence adds `RethTracer::with_json_targets`, `json_targets` state, and initialization through `RitualRouter`.
  - Required change: Not equivalent: callers cannot request target-specific Ritual JSON routing through the tracing crate. Current `reth-tracing-otlp` is not a behavioral replacement for the old target-specific Ritual JSON router.

- `file-0513-atom-0001` (`file-0513`, `crates/tracing/src/ritual_router.rs`, `missing`)
  - Hunk: `@@ -0,0 +1,147 @@`
  - Claim: The old divergence adds `crates/tracing/src/ritual_router.rs` with `RitualRouter` and `RitualJsonLayer` for target-specific JSON log output.
  - Required change: Not equivalent: the old custom JSON routing implementation is absent. Current `reth-tracing-otlp` is not a behavioral replacement for the old target-specific Ritual JSON router.

- `file-0514-atom-0001` (`file-0514`, `crates/transaction-pool/Cargo.toml`, `missing`)
  - Hunk: `@@ -24,12 +24,19 @@ reth-storage-api.workspace = true`
  - Claim: The old transaction-pool manifest wires several Ritual crates, k256 support, sol macro/types, and dashmap for async/scheduled pool behavior.
  - Required change: Partially equivalent: the active v2.2 txpool async slice is wired through a narrower dependency set, but the old scheduled/metrics/router dependencies are not exact-port preserved here.

- `file-0521-atom-0001` (`file-0521`, `crates/transaction-pool/src/blocking_handlers.rs`, `missing`)
  - Hunk: `@@ -0,0 +1,284 @@`
  - Claim: The old divergence adds `blocking_handlers.rs` to process canonical state synchronously for scheduled transactions, async pool updates, heartbeat revival routing, and Scheduler cleanup.
  - Required change: Not exact: v2.2 moved scheduled execution toward parent-state synthesis and canonical verification, while the old txpool blocking handler surface is absent.

- `file-0523-atom-0002` (`file-0523`, `crates/transaction-pool/src/error.rs`, `missing`)
  - Hunk: `@@ -66,6 +66,10 @@ pub enum PoolErrorKind {`
  - Claim: The old divergence classifies `InvalidTransactionError::PrecompileRequestPermanentlyInvalid` as a bad transaction.
  - Required change: Not equivalent: the permanent precompile invalidity classification is absent from destination txpool errors.

- `file-0524-atom-0001` (`file-0524`, `crates/transaction-pool/src/lib.rs`, `structural_equivalent`)
  - Hunk: `@@ -172,15 +172,25 @@ pub use crate::{`
  - Claim: The old diff expands `Pool`/`TransactionPool` with async result submission, async metadata queries, and fulfilled original transaction replay helpers.
  - Required change: Behavior is carried by a refactored v2.2 API centered on canonical async metadata and result submissions, not by exact old trait methods.

- `file-0525-atom-0001` (`file-0525`, `crates/transaction-pool/src/maintain.rs`, `missing`)
  - Hunk: `@@ -9,7 +9,7 @@ use crate::{`
  - Claim: The old txpool maintenance loop adds chain-halt threshold validation, poisonous scheduled-job detection, and a 200 second async transaction lifetime.
  - Required change: Not equivalent in this file: v2.2 has contract-expiry async cleanup, but not the old wall-clock chain halt/poisonous scheduled-job maintenance policy.

- `file-0526-atom-0001` (`file-0526`, `crates/transaction-pool/src/metrics.rs`, `missing`)
  - Hunk: `@@ -36,7 +36,16 @@ pub struct TxPoolMetrics {`
  - Claim: The old diff adds txpool gauges for scheduled pool count/bytes, async commitment pool count/bytes, and total scheduled transactions.
  - Required change: Not equivalent for txpool-local metrics; broader Ritual metrics exist elsewhere but not these pool gauges.

- `file-0528-atom-0001` (`file-0528`, `crates/transaction-pool/src/pool/async_pool.rs`, `structural_equivalent`)
  - Hunk: `@@ -0,0 +1,1471 @@`
  - Claim: The old added async pool tracks awaiting execution, fulfilled, awaiting delivery, delivery-ready states, sender locks, expiry cleanup, original transaction replay, and two-phase delivery results.
  - Required change: Structurally equivalent for the active v2.2 async lifecycle, but not textually exact to the old broad async_pool.rs implementation.

- `file-0532-atom-0001` (`file-0532`, `crates/transaction-pool/src/pool/mod.rs`, `structural_equivalent`)
  - Hunk: `@@ -71,6 +71,8 @@ use crate::{`
  - Claim: The old pool module wires async commitment processing, original transaction hash extraction, scheduled subpool modules, and async metadata APIs into PoolInner.
  - Required change: Async behavior is structurally preserved in a refactored form; old raw scheduled subpool integration is intentionally not exact in v2.2.

- `file-0537-atom-0001` (`file-0537`, `crates/transaction-pool/src/pool/txpool.rs`, `structural_equivalent`)
  - Hunk: `@@ -10,24 +10,32 @@ use crate::{`
  - Claim: The old txpool internals add scheduled pool storage, calldata caps, scheduled expiry methods, and async transaction insertion/removal hooks.
  - Required change: Partial structural equivalence: async lifecycle hooks are preserved in refactored APIs, while old raw scheduled pool and calldata cap behavior are absent.

- `file-0540-atom-0001` (`file-0540`, `crates/transaction-pool/src/traits.rs`, `structural_equivalent`)
  - Hunk: `@@ -2,13 +2,17 @@ use crate::{`
  - Claim: The old trait adds direct scheduled/async insertion, metadata queries, result submission, delivery readiness, and async containment APIs.
  - Required change: Structurally equivalent for active async lifecycle callers after refactor; not exact for raw scheduled insertion APIs.

- `file-0541-atom-0001` (`file-0541`, `crates/transaction-pool/src/validate/constants.rs`, `missing`)
  - Hunk: `@@ -7,9 +7,10 @@ pub const TX_SLOT_BYTE_SIZE: usize = 32 * 1024;`
  - Claim: The old diff lowers `DEFAULT_MAX_TX_INPUT_BYTES` from four tx slots/128KB to two tx slots/64KB and documents `RETH_MAX_TX_INPUT_BYTES` override.
  - Required change: Not equivalent: the old stricter default transaction input cap is not preserved.

- `file-0542-atom-0001` (`file-0542`, `crates/transaction-pool/src/validate/eth.rs`, `structural_equivalent`)
  - Hunk: `@@ -14,8 +14,8 @@ use crate::{`
  - Claim: The old validator explicitly accepts or rejects scheduled, async commitment, and passkey transaction types based on feature booleans.
  - Required change: Potentially equivalent when chain config marks custom tx types in `other_tx_types`, but not exact to the old explicit gates.
