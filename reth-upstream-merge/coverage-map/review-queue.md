# Coverage Review Queue

## File 0020: crates/chain-state/Cargo.toml

- Key: `file_index=20`, `source_path=crates/chain-state/Cargo.toml`, `record_id=file-0020-atom-0001`
  - Source hunk: `@@ -12,6 +12,7 @@ [dependencies]`
  - Required change: Decide whether the v2.2 port should restore a blocking canonical-state pubsub dependency or replace it with the current async notification architecture.
  - Likely destination: `unknown`

## File 0022: crates/chain-state/src/in_memory.rs

- Key: `file_index=22`, `source_path=crates/chain-state/src/in_memory.rs`, `record_id=file-0022-atom-0001`
  - Source hunk: `@@ -139,6 +140,8 @@ pub(crate) struct CanonicalInMemoryStateInner<N: NodePrimitives>`
  - Required change: Restore or intentionally replace storage for blocking canonical-state handlers in the v2.2 chain-state path.
  - Likely destination: `unknown`

- Key: `file_index=22`, `source_path=crates/chain-state/src/in_memory.rs`, `record_id=file-0022-atom-0002`
  - Source hunk: `@@ -513,8 +518,21 @@ impl<N: NodePrimitives> CanonicalInMemoryState<N>`
  - Required change: Decide whether the v2.2 chain-state API should expose blocking canonical-state subscription.
  - Likely destination: `unknown`

- Key: `file_index=22`, `source_path=crates/chain-state/src/in_memory.rs`, `record_id=file-0022-atom-0003`
  - Source hunk: `@@ -513,8 +518,21 @@ impl<N: NodePrimitives> CanonicalInMemoryState<N>`
  - Required change: Restore or explicitly reject the old blocking-before-async canonical notification ordering requirement.
  - Likely destination: `unknown`

## File 0023: crates/chain-state/src/noop.rs

- Key: `file_index=23`, `source_path=crates/chain-state/src/noop.rs`, `record_id=file-0023-atom-0001`
  - Source hunk: `@@ -12,6 +12,10 @@ impl<C: Send + Sync, N: NodePrimitives> CanonStateSubscriptions for NoopProvider`
  - Required change: If blocking canonical-state subscription is restored, update NoopProvider to satisfy the trait.
  - Likely destination: `unknown`

## File 0024: crates/chain-state/src/notifications.rs

- Key: `file_index=24`, `source_path=crates/chain-state/src/notifications.rs`, `record_id=file-0024-atom-0001`
  - Source hunk: `@@ -32,6 +32,14 @@ pub trait CanonStateSubscriptions`
  - Required change: Decide whether to restore the blocking subscription method on CanonStateSubscriptions in the v2.2 port.
  - Likely destination: `unknown`

- Key: `file_index=24`, `source_path=crates/chain-state/src/notifications.rs`, `record_id=file-0024-atom-0002`
  - Source hunk: `@@ -45,6 +53,13 @@ impl<T: CanonStateSubscriptions> CanonStateSubscriptions for &T`
  - Required change: If the trait method is restored, update the reference impl forwarding path.
  - Likely destination: `unknown`

## File 0025: crates/chain-state/src/test_utils.rs

- Key: `file_index=25`, `source_path=crates/chain-state/src/test_utils.rs`, `record_id=file-0025-atom-0001`
  - Source hunk: `@@ -341,8 +341,14 @@ impl CanonStateSubscriptions for TestCanonStateSubscriptions`
  - Required change: If blocking canonical-state subscription is restored, update chain-state test fixtures to satisfy the trait.
  - Likely destination: `unknown`

## File 0026: crates/chainspec/src/api.rs

- Key: `file_index=26`, `source_path=crates/chainspec/src/api.rs`, `record_id=file-0026-atom-0001`
  - Source hunk: `@@ -65,6 +65,10 @@ pub trait EthChainSpec`
  - Required change: Decide whether the v2.2 port should restore a per-chain max_extra_data_bytes accessor or use an equivalent chain-specific consensus config.
  - Likely destination: `unknown`

## File 0027: crates/chainspec/src/constants.rs

- Key: `file_index=27`, `source_path=crates/chainspec/src/constants.rs`, `record_id=file-0027-atom-0001`
  - Source hunk: `@@ -14,3 +14,9 @@ pub(crate) const MAINNET_DEPOSIT_CONTRACT`
  - Required change: Restore or intentionally replace the Summit deposit event topic constant in the v2.2 chain-spec path.
  - Likely destination: `unknown`

## File 0028: crates/chainspec/src/spec.rs

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0001`
  - Source hunk: `@@ -326,11 +334,20 @@ pub struct ChainSpec`
  - Required change: Restore or replace ChainSpec-level storage and builder support for per-chain max_extra_data_bytes.
  - Likely destination: `unknown`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0002`
  - Source hunk: `@@ -746,7 +805,12 @@ impl From<Genesis> for ChainSpec`
  - Required change: Restore or intentionally replace Summit deposit topic selection for genesis-derived deposit contracts.
  - Likely destination: `unknown`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0003`
  - Source hunk: `@@ -766,6 +825,9 @@ impl From<Genesis> for ChainSpec`
  - Required change: Restore or explicitly reject the old Ritual/Summit unbounded extra_data policy for genesis-derived chain specs.
  - Likely destination: `unknown`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0004`
  - Source hunk: `@@ -326,11 +334,20 @@ pub struct ChainSpec`
  - Required change: Restore or replace ChainSpec/base builder support for custom base_block_reward.
  - Likely destination: `unknown`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0005`
  - Source hunk: `@@ -395,6 +420,37 @@ impl ChainSpec`
  - Required change: Determine whether v2.2's alloy-evm block reward helpers are enough, or restore ChainSpec/EthExecutorSpec custom base reward plumbing.
  - Likely destination: `unknown`

## File 0042: crates/cli/commands/src/stage/run.rs

- Key: `file_index=42`, `source_path=crates/cli/commands/src/stage/run.rs`, `record_id=file-0042-atom-0001`
  - Source hunk: `@@ -193 +193 @@ impl<C: ChainSpecParser<ChainSpec: EthChainSpec + Hardforks + EthereumHardforks>`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/cli/commands/src/stage/run.rs`

## File 0047: crates/consensus/common/Cargo.toml

- Key: `file_index=47`, `source_path=crates/consensus/common/Cargo.toml`, `record_id=file-0047-atom-0001`
  - Source hunk: `@@ -21,2 +21,3 @@`
  - Human question: Confirm that the v2.2 port should continue omitting downstream-only consensus validation tracing, leaving this manifest dependency intentionally absent.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/consensus/common/Cargo.toml`

## File 0048: crates/consensus/common/src/validation.rs

- Key: `file_index=48`, `source_path=crates/consensus/common/src/validation.rs`, `record_id=file-0048-atom-0001`
  - Source hunk: `@@ -3,3 +3 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/consensus/common/src/validation.rs`

## File 0050: crates/e2e-test-utils/src/network.rs

- Key: `file_index=50`, `source_path=crates/e2e-test-utils/src/network.rs`, `record_id=file-0050-atom-0001`
  - Source hunk: `@@ -46,2 +46,2 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/e2e-test-utils/src/network.rs`

## File 0056: crates/engine/tree/Cargo.toml

- Key: `file_index=56`, `source_path=crates/engine/tree/Cargo.toml`, `record_id=file-0056-atom-0001`
  - Source hunk: `@@ -55,2 +55,3 @@ metrics.workspace = true`
  - Human question: Confirm that the v2.2 port should keep engine-tree Ritual metrics instrumentation dropped, leaving the `ritual-metrics` manifest dependency intentionally absent.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/engine/tree/Cargo.toml`

## File 0059: crates/engine/tree/src/download.rs

- Key: `file_index=59`, `source_path=crates/engine/tree/src/download.rs`, `record_id=file-0059-atom-0001`
  - Source hunk: `@@ -145 +145 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/engine/tree/src/download.rs`

## File 0062: crates/engine/tree/src/tree/cached_state.rs

- Key: `file_index=62`, `source_path=crates/engine/tree/src/tree/cached_state.rs`, `record_id=file-0062-atom-0001`
  - Source hunk: `@@ -18 +18 @@ use revm_primitives::map::DefaultHashBuilder;`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/engine/execution-cache/src/cached_state.rs`

## File 0064: crates/engine/tree/src/tree/mod.rs

- Key: `file_index=64`, `source_path=crates/engine/tree/src/tree/mod.rs`, `record_id=file-0064-atom-0001`
  - Source hunk: `@@ -25,0 +26 @@ use reth_chain_state::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/engine/tree/src/tree/mod.rs`

## File 0071: crates/era/src/era1_file.rs

- Key: `file_index=71`, `source_path=crates/era/src/era1_file.rs`, `record_id=file-0071-atom-0001`
  - Source hunk: `@@ -115 +115,3 @@ impl<R: Read + Seek> Era1Reader<R> {`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/era/src/era1_file.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0072: crates/errors/Cargo.toml

- Key: `file_index=72`, `source_path=crates/errors/Cargo.toml`, `record_id=file-0072-atom-0002`
  - Source hunk: `@@ -19 +19,5 @@`
  - Required change: Restore or intentionally replace the `reth-errors` async-context feature passthrough so downstream manifests can enable async-context through this crate boundary.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/errors/Cargo.toml`

## File 0074: crates/ethereum/consensus/src/lib.rs

- Key: `file_index=74`, `source_path=crates/ethereum/consensus/src/lib.rs`, `record_id=file-0074-atom-0001`
  - Source hunk: `@@ -57,2 +57,2 @@ impl<ChainSpec: EthChainSpec + EthereumHardforks> EthBeaconConsensus<ChainSpec>`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/consensus/src/lib.rs`

## File 0076: crates/ethereum/engine-primitives/src/payload.rs

- Key: `file_index=76`, `source_path=crates/ethereum/engine-primitives/src/payload.rs`, `record_id=file-0076-atom-0001`
  - Source hunk: `@@ -5 +5 @@ use alloy_eips::{eip4844::BlobTransactionSidecar, eip4895::Withdrawals, eip7685:`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/engine-primitives/src/payload.rs`

## File 0077: crates/ethereum/evm/Cargo.toml

- Key: `file_index=77`, `source_path=crates/ethereum/evm/Cargo.toml`, `record_id=file-0077-atom-0001`
  - Source hunk: `@@ -20,2 +20,3 @@`
  - Required change: Restore or intentionally replace the direct `revm-context` dependency for async-context-aware ethereum EVM wiring in the port crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/Cargo.toml`

- Key: `file_index=77`, `source_path=crates/ethereum/evm/Cargo.toml`, `record_id=file-0077-atom-0002`
  - Source hunk: `@@ -28,2 +29,5 @@`
  - Human question: Confirm that the v2.2 port should keep the downstream-only `tracing` diagnostics dropped in `reth-evm-ethereum`, leaving this manifest dependency intentionally absent.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/src/build.rs`

- Key: `file_index=77`, `source_path=crates/ethereum/evm/Cargo.toml`, `record_id=file-0077-atom-0003`
  - Source hunk: `@@ -52 +56,2 @@`
  - Required change: Restore or intentionally replace the `reth-evm-ethereum` async-context feature exposure so callers can enable async-aware execution transitively from this crate boundary.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/Cargo.toml`

## File 0078: crates/ethereum/evm/src/build.rs

- Key: `file_index=78`, `source_path=crates/ethereum/evm/src/build.rs`, `record_id=file-0078-atom-0001`
  - Source hunk: `@@ -3 +3,2 @@ use alloy_consensus::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/src/build.rs`

## File 0079: crates/ethereum/evm/src/execute.rs

- Key: `file_index=79`, `source_path=crates/ethereum/evm/src/execute.rs`, `record_id=file-0079-atom-0001`
  - Source hunk: `@@ -712,0 +713,3 @@ mod tests {`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ethereum/evm/src/execute.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0080: crates/ethereum/evm/src/lib.rs

- Key: `file_index=80`, `source_path=crates/ethereum/evm/src/lib.rs`, `record_id=file-0080-atom-0001`
  - Source hunk: `@@ -25 +25 @@ use alloy_evm::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/src/lib.rs`

## File 0081: crates/ethereum/node/Cargo.toml

- Key: `file_index=81`, `source_path=crates/ethereum/node/Cargo.toml`, `record_id=file-0081-atom-0003`
  - Source hunk: `@@ -46,2 +48,7 @@`
  - Human question: Confirm that splitting the old `ritual-async` dependency across payload and RPC crates fully preserves the downstream async-node behavior that used to hang off `reth-node-ethereum`.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/Cargo.toml`

- Key: `file_index=81`, `source_path=crates/ethereum/node/Cargo.toml`, `record_id=file-0081-atom-0004`
  - Source hunk: `@@ -46,2 +48,7 @@`
  - Human question: Confirm that scheduled-block-building plus nodebuilder integration fully replaces the old direct `ritual-scheduling` dependency edge from `reth-node-ethereum`.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/Cargo.toml`

- Key: `file_index=81`, `source_path=crates/ethereum/node/Cargo.toml`, `record_id=file-0081-atom-0005`
  - Source hunk: `@@ -46,2 +48,7 @@`
  - Required change: Restore or intentionally replace the `ritual-spc-verification` dependency edge together with the missing `SpcVerifierImpl` bridge surface in `reth-node-ethereum`.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal/crates/ethereum/node/src/spc.rs`

- Key: `file_index=81`, `source_path=crates/ethereum/node/Cargo.toml`, `record_id=file-0081-atom-0006`
  - Source hunk: `@@ -77,2 +84,3 @@`
  - Human question: Confirm that removing the public `reth-node-ethereum/async-context` feature is acceptable because async-context enablement moved to Ritual nodebuilder and payload crates.
  - Likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal/crates/node/Cargo.toml`

## File 0082: crates/ethereum/node/src/lib.rs

- Key: `file_index=82`, `source_path=crates/ethereum/node/src/lib.rs`, `record_id=file-0082-atom-0001`
  - Source hunk: `@@ -25,5 +25,9 @@`
  - Required change: Restore or intentionally replace the `spc` module wiring in `reth_node_ethereum` so the SPC verifier bridge is compiled into the crate surface.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/lib.rs`

- Key: `file_index=82`, `source_path=crates/ethereum/node/src/lib.rs`, `record_id=file-0082-atom-0002`
  - Source hunk: `@@ -25,5 +25,9 @@`
  - Required change: Restore or intentionally replace the crate-root `SpcVerifierImpl` re-export expected by downstream nodebuilder consumers.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/lib.rs`

## File 0083: crates/ethereum/node/src/node.rs

- Key: `file_index=83`, `source_path=crates/ethereum/node/src/node.rs`, `record_id=file-0083-atom-0001`
  - Source hunk: `@@ -4 +4 @@ pub use crate::{payload::EthereumPayloadBuilder, EthereumEngineValidator};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/node.rs`

## File 0084: crates/ethereum/node/src/payload.rs

- Key: `file_index=84`, `source_path=crates/ethereum/node/src/payload.rs`, `record_id=file-0084-atom-0001`
  - Source hunk: `@@ -50,3 +50,8 @@ impl EthereumPayloadBuilder {`
  - Required change: Restore or intentionally replace the node-to-payload-builder `max_block_size_bytes` propagation so payload construction enforces the downstream transaction-list size cap.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/payload.rs`

- Key: `file_index=84`, `source_path=crates/ethereum/node/src/payload.rs`, `record_id=file-0084-atom-0002`
  - Source hunk: `@@ -50,3 +50,8 @@ impl EthereumPayloadBuilder {`
  - Required change: Restore or intentionally replace the node-level `with_await_payload_on_missing(false)` wiring so missing payloads race an empty fallback instead of awaiting in-progress payloads.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/payload.rs`

## File 0085: crates/ethereum/node/src/spc.rs

- Key: `file_index=85`, `source_path=crates/ethereum/node/src/spc.rs`, `record_id=file-0085-atom-0001`
  - Source hunk: `@@ -0,0 +1,175 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ethereum/node/src/spc.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0087: crates/ethereum/payload/Cargo.toml

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0002`
  - Source hunk: `@@ -32,2 +33,3 @@`
  - Human question: Confirm that converting the plain workspace `revm-context` dependency into an explicit path-plus-features edge is sufficient to preserve the downstream async payload context behavior.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/Cargo.toml`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0005`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Required change: Restore or intentionally reject payload-local `ritual-metrics` instrumentation for the downstream Ritual payload paths that currently have no counterpart in the port crate.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0006`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Required change: Restore or intentionally replace sequencing-rights-based transaction classification and reordering in the payload build path.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0007`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Required change: Restore or intentionally replace payload-local heartbeat tracking and hydration behavior used during scheduled or async execution.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0008`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Human question: Confirm that `ritual-scheduled-block-building` fully replaces the old payload-local `ritual-scheduling` dependency surface, including heartbeat-routed and predicate-gated orchestration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/src/lib.rs`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0010`
  - Source hunk: `@@ -41 +58,10 @@`
  - Required change: Restore or intentionally reject the downstream Rayon-backed payload preparation path used for scheduled and async transaction handling.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0011`
  - Source hunk: `@@ -41 +58,10 @@`
  - Human question: Confirm that making async-context always-on in the payload crate is an acceptable replacement for the old opt-in `async-context` feature surface.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/Cargo.toml`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0013`
  - Source hunk: `@@ -41 +58,10 @@`
  - Required change: Restore or intentionally replace the payload-crate SPC signature test support that depended on `secp256k1`, including wrong-output and wrong-signature regression coverage.
  - Likely destination: `unknown`

## File 0088: crates/ethereum/payload/src/bundle.rs

- Key: `file_index=88`, `source_path=crates/ethereum/payload/src/bundle.rs`, `record_id=file-0088-atom-0001`
  - Source hunk: `@@ -0,0 +1,194 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ethereum/payload/src/bundle.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0089: crates/ethereum/payload/src/collector.rs

- Key: `file_index=89`, `source_path=crates/ethereum/payload/src/collector.rs`, `record_id=file-0089-atom-0001`
  - Source hunk: `@@ -0,0 +1,124 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ethereum/payload/src/collector.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0090: crates/ethereum/payload/src/config.rs

- Key: `file_index=90`, `source_path=crates/ethereum/payload/src/config.rs`, `record_id=file-0090-atom-0001`
  - Source hunk: `@@ -2,0 +3,4 @@ use reth_primitives_traits::constants::GAS_LIMIT_BOUND_DIVISOR;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/config.rs`

## File 0091: crates/ethereum/payload/src/execution.rs

- Key: `file_index=91`, `source_path=crates/ethereum/payload/src/execution.rs`, `record_id=file-0091-atom-0001`
  - Source hunk: `@@ -0,0 +1,311 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-revm-internal/crates/handler/src/execution.rs`

## File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0001`
  - Source hunk: `@@ -11,0 +12,5 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

## File 0093: crates/ethereum/payload/src/unified_builder.rs

- Key: `file_index=93`, `source_path=crates/ethereum/payload/src/unified_builder.rs`, `record_id=file-0093-atom-0001`
  - Source hunk: `@@ -0,0 +1,341 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ethereum/payload/src/unified_builder.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0094: crates/ethereum/payload/src/unified_execution.rs

- Key: `file_index=94`, `source_path=crates/ethereum/payload/src/unified_execution.rs`, `record_id=file-0094-atom-0001`
  - Source hunk: `@@ -0,0 +1,537 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ethereum/payload/src/unified_execution.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0097: crates/ethereum/primitives/src/receipt.rs

- Key: `file_index=97`, `source_path=crates/ethereum/primitives/src/receipt.rs`, `record_id=file-0097-atom-0001`
  - Source hunk: `@@ -38,4 +38,4 @@ impl Receipt {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/primitives/src/receipt.rs`

## File 0098: crates/ethereum/primitives/src/transaction.rs

- Key: `file_index=98`, `source_path=crates/ethereum/primitives/src/transaction.rs`, `record_id=file-0098-atom-0001`
  - Source hunk: `@@ -2 +1,0 @@ use alloc::vec::Vec;`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/rpc/transaction.rs`

## File 0099: crates/ethereum/reth/Cargo.toml

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0001`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Required change: Restore or intentionally replace the public `reth-ethereum/async-context` Cargo feature so the port preserves the downstream feature surface.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/reth/Cargo.toml`

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0002`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Required change: If `reth-ethereum/async-context` is restored, ensure it still enables the crate's optional `evm` feature set transitively.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/reth/Cargo.toml`

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0003`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Required change: Restore or intentionally replace `reth-evm` async-context feature propagation before reintroducing the top-level alias.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/evm/Cargo.toml`

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0004`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Required change: Restore or intentionally replace `reth-evm-ethereum` async-context feature propagation before reintroducing the top-level alias.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/Cargo.toml`

## File 0101: crates/evm/Cargo.toml

- Key: `file_index=101`, `source_path=crates/evm/Cargo.toml`, `record_id=file-0101-atom-0001`
  - Source hunk: `@@ -23,8 +23,11 @@`
  - Human question: Confirm that moving async context and precompile ownership out of core `reth-evm` and into Ritual payload/verifier crates is an acceptable API-surface change for downstream consumers.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/Cargo.toml`

- Key: `file_index=101`, `source_path=crates/evm/Cargo.toml`, `record_id=file-0101-atom-0002`
  - Source hunk: `@@ -35,7 +38,13 @@`
  - Human question: Confirm that rehoming txpool, registry, metrics, and async runtime support out of core `reth-evm` preserves the downstream Ritual execution path sufficiently for all consumers that previously depended on `reth-evm` directly.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/Cargo.toml`

- Key: `file_index=101`, `source_path=crates/evm/Cargo.toml`, `record_id=file-0101-atom-0003`
  - Source hunk: `@@ -45,7 +54,7 @@`
  - Required change: Restore or intentionally reject the downstream `reth-evm` default async-context contract so consumers know whether async execution is enabled by default.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/evm/Cargo.toml`

- Key: `file_index=101`, `source_path=crates/evm/Cargo.toml`, `record_id=file-0101-atom-0004`
  - Source hunk: `@@ -72,3 +81,4 @@`
  - Required change: Restore or intentionally replace the `reth-evm` async-context feature surface and its forwarding chain through alloy, revm precompile, ethereum primitives, and execution errors.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/evm/Cargo.toml`

## File 0102: crates/evm/execution-errors/Cargo.toml

- Key: `file_index=102`, `source_path=crates/evm/execution-errors/Cargo.toml`, `record_id=file-0102-atom-0001`
  - Source hunk: `@@ -31,3 +31,4 @@`
  - Required change: Restore or intentionally replace the `reth-execution-errors` async-context feature re-export so downstream async error-feature propagation can traverse this crate boundary.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/execution-errors/Cargo.toml`

## File 0106: crates/evm/src/async_context_tests.rs

- Key: `file_index=106`, `source_path=crates/evm/src/async_context_tests.rs`, `record_id=file-0106-atom-0001`
  - Source hunk: `@@ -0,0 +1,99 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/evm/src/async_context_tests.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0108: crates/evm/src/lib.rs

- Key: `file_index=108`, `source_path=crates/evm/src/lib.rs`, `record_id=file-0108-atom-0001`
  - Source hunk: `@@ -24 +24 @@ use alloy_evm::block::{BlockExecutorFactory, BlockExecutorFor};`
  - Required change: Resolve whether the downstream crates/evm/src/lib.rs behavior is still implemented in the destination module at the same relative path or whether it must be restored explicitly.
  - Likely destination: `unknown`

## File 0110: crates/evm/src/pool_manager.rs

- Key: `file_index=110`, `source_path=crates/evm/src/pool_manager.rs`, `record_id=file-0110-atom-0001`
  - Source hunk: `@@ -0,0 +1,89 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/evm/src/pool_manager.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0111: crates/evm/src/spc.rs

- Key: `file_index=111`, `source_path=crates/evm/src/spc.rs`, `record_id=file-0111-atom-0001`
  - Source hunk: `@@ -0,0 +1,151 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/evm/src/spc.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0115: crates/exex/exex/src/notifications.rs

- Key: `file_index=115`, `source_path=crates/exex/exex/src/notifications.rs`, `record_id=file-0115-atom-0001`
  - Source hunk: `@@ -319,2 +319,2 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/exex/exex/src/notifications.rs`

## File 0131: crates/net/downloaders/src/bodies/bodies.rs

- Key: `file_index=131`, `source_path=crates/net/downloaders/src/bodies/bodies.rs`, `record_id=file-0131-atom-0001`
  - Source hunk: `@@ -106 +106 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/downloaders/src/bodies/bodies.rs`

## File 0136: crates/net/downloaders/src/headers/reverse_headers.rs

- Key: `file_index=136`, `source_path=crates/net/downloaders/src/headers/reverse_headers.rs`, `record_id=file-0136-atom-0001`
  - Source hunk: `@@ -163 +163 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/downloaders/src/headers/reverse_headers.rs`

## File 0144: crates/net/eth-wire-types/src/message.rs

- Key: `file_index=144`, `source_path=crates/net/eth-wire-types/src/message.rs`, `record_id=file-0144-atom-0001`
  - Source hunk: `@@ -105 +105 @@ impl<N: NetworkPrimitives> ProtocolMessage<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/eth-wire-types/src/message.rs`

## File 0150: crates/net/eth-wire/src/multiplex.rs

- Key: `file_index=150`, `source_path=crates/net/eth-wire/src/multiplex.rs`, `record_id=file-0150-atom-0001`
  - Source hunk: `@@ -83 +83 @@ impl<St> RlpxProtocolMultiplexer<St> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/eth-wire/src/multiplex.rs`

## File 0157: crates/net/network/Cargo.toml

- Key: `file_index=157`, `source_path=crates/net/network/Cargo.toml`, `record_id=file-0157-atom-0001`
  - Source hunk: `@@ -33,6 +33,7 @@`
  - Required change: Restore or intentionally reject the `ritual-metrics` dependency in `reth-network` together with the downstream network metrics call sites that depend on it.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/Cargo.toml`

## File 0159: crates/net/network/src/error.rs

- Key: `file_index=159`, `source_path=crates/net/network/src/error.rs`, `record_id=file-0159-atom-0001`
  - Source hunk: `@@ -75 +75 @@ impl NetworkError {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/error.rs`

## File 0163: crates/net/network/src/metrics.rs

- Key: `file_index=163`, `source_path=crates/net/network/src/metrics.rs`, `record_id=file-0163-atom-0001`
  - Source hunk: `@@ -351,0 +352,9 @@ pub struct AnnouncedTxTypesMetrics {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/metrics.rs`

## File 0164: crates/net/network/src/network.rs

- Key: `file_index=164`, `source_path=crates/net/network/src/network.rs`, `record_id=file-0164-atom-0001`
  - Source hunk: `@@ -26,0 +27 @@ use reth_tokio_util::{EventSender, EventStream};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/network.rs`

## File 0165: crates/net/network/src/peers.rs

- Key: `file_index=165`, `source_path=crates/net/network/src/peers.rs`, `record_id=file-0165-atom-0001`
  - Source hunk: `@@ -245 +245 @@ impl PeersManager {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/peers.rs`

## File 0169: crates/net/network/src/state.rs

- Key: `file_index=169`, `source_path=crates/net/network/src/state.rs`, `record_id=file-0169-atom-0001`
  - Source hunk: `@@ -203 +203 @@ impl<N: NetworkPrimitives> NetworkState<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/state.rs`

## File 0172: crates/net/network/src/test_utils/testnet.rs

- Key: `file_index=172`, `source_path=crates/net/network/src/test_utils/testnet.rs`, `record_id=file-0172-atom-0001`
  - Source hunk: `@@ -362 +362 @@ impl<C, Pool> TestnetHandle<C, Pool> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/test_utils/testnet.rs`

## File 0174: crates/net/network/src/transactions/fetcher.rs

- Key: `file_index=174`, `source_path=crates/net/network/src/transactions/fetcher.rs`, `record_id=file-0174-atom-0001`
  - Source hunk: `@@ -170 +170 @@ impl<N: NetworkPrimitives> TransactionFetcher<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/transactions/fetcher.rs`

## File 0175: crates/net/network/src/transactions/mod.rs

- Key: `file_index=175`, `source_path=crates/net/network/src/transactions/mod.rs`, `record_id=file-0175-atom-0001`
  - Source hunk: `@@ -63,0 +64 @@ use reth_transaction_pool::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/src/transactions/mod.rs`

## File 0178: crates/net/network/tests/it/multiplex.rs

- Key: `file_index=178`, `source_path=crates/net/network/tests/it/multiplex.rs`, `record_id=file-0178-atom-0001`
  - Source hunk: `@@ -106,2 +106,2 @@ mod proto {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/network/tests/it/multiplex.rs`

## File 0180: crates/net/p2p/src/error.rs

- Key: `file_index=180`, `source_path=crates/net/p2p/src/error.rs`, `record_id=file-0180-atom-0001`
  - Source hunk: `@@ -37 +37 @@ impl<H: BlockHeader> EthResponseValidator for RequestResult<Vec<H>> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/p2p/src/error.rs`

## File 0185: crates/node/api/Cargo.toml

- Key: `file_index=185`, `source_path=crates/node/api/Cargo.toml`, `record_id=file-0185-atom-0001`
  - Source hunk: `@@ -30,0 +31,4 @@ reth-tokio-util.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/api/Cargo.toml`

## File 0186: crates/node/api/src/node.rs

- Key: `file_index=186`, `source_path=crates/node/api/src/node.rs`, `record_id=file-0186-atom-0001`
  - Source hunk: `@@ -18 +18,2 @@ use reth_transaction_pool::{PoolTransaction, TransactionPool};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/api/src/node.rs`

## File 0187: crates/node/builder/Cargo.toml

- Key: `file_index=187`, `source_path=crates/node/builder/Cargo.toml`, `record_id=file-0187-atom-0001`
  - Source hunk: `@@ -30,0 +31 @@ reth-evm.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/Cargo.toml`

## File 0188: crates/node/builder/src/builder/mod.rs

- Key: `file_index=188`, `source_path=crates/node/builder/src/builder/mod.rs`, `record_id=file-0188-atom-0001`
  - Source hunk: `@@ -38,0 +39 @@ use reth_transaction_pool::{PoolConfig, PoolTransaction, TransactionPool};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/builder/mod.rs`

## File 0189: crates/node/builder/src/components/builder.rs

- Key: `file_index=189`, `source_path=crates/node/builder/src/components/builder.rs`, `record_id=file-0189-atom-0001`
  - Source hunk: `@@ -14,0 +15 @@ use reth_transaction_pool::{PoolTransaction, TransactionPool};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/components/builder.rs`

## File 0190: crates/node/builder/src/components/execute.rs

- Key: `file_index=190`, `source_path=crates/node/builder/src/components/execute.rs`, `record_id=file-0190-atom-0001`
  - Source hunk: `@@ -21,0 +22,13 @@ pub trait ExecutorBuilder<Node: FullNodeTypes>: Send {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/components/execute.rs`

## File 0191: crates/node/builder/src/components/payload.rs

- Key: `file_index=191`, `source_path=crates/node/builder/src/components/payload.rs`, `record_id=file-0191-atom-0001`
  - Source hunk: `@@ -86,0 +87 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/components/payload.rs`

## File 0192: crates/node/builder/src/components/pool.rs

- Key: `file_index=192`, `source_path=crates/node/builder/src/components/pool.rs`, `record_id=file-0192-atom-0001`
  - Source hunk: `@@ -13,0 +14 @@ pub trait PoolBuilder<Node: FullNodeTypes>: Send {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/components/pool.rs`

## File 0193: crates/node/builder/src/launch/common.rs

- Key: `file_index=193`, `source_path=crates/node/builder/src/launch/common.rs`, `record_id=file-0193-atom-0001`
  - Source hunk: `@@ -55,0 +56 @@ use reth_transaction_pool::TransactionPool;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/launch/common.rs`

## File 0194: crates/node/builder/src/launch/engine.rs

- Key: `file_index=194`, `source_path=crates/node/builder/src/launch/engine.rs`, `record_id=file-0194-atom-0001`
  - Source hunk: `@@ -18,2 +18,2 @@ use reth_node_api::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/launch/engine.rs`

## File 0196: crates/node/builder/src/rpc.rs

- Key: `file_index=196`, `source_path=crates/node/builder/src/rpc.rs`, `record_id=file-0196-atom-0001`
  - Source hunk: `@@ -459 +459,8 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/rpc.rs`

## File 0197: crates/node/builder/src/setup.rs

- Key: `file_index=197`, `source_path=crates/node/builder/src/setup.rs`, `record_id=file-0197-atom-0001`
  - Source hunk: `@@ -13,0 +14 @@ use reth_evm::execute::BlockExecutorProvider;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/builder/src/setup.rs`

## File 0199: crates/node/core/src/args/log.rs

- Key: `file_index=199`, `source_path=crates/node/core/src/args/log.rs`, `record_id=file-0199-atom-0001`
  - Source hunk: `@@ -7 +7 @@ use reth_tracing::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/core/src/args/log.rs`

## File 0200: crates/node/core/src/args/payload_builder.rs

- Key: `file_index=200`, `source_path=crates/node/core/src/args/payload_builder.rs`, `record_id=file-0200-atom-0001`
  - Source hunk: `@@ -2 +1,0 @@ use crate::{cli::config::PayloadBuilderConfig, version::default_extra_data};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/core/src/args/payload_builder.rs`

## File 0201: crates/node/core/src/cli/config.rs

- Key: `file_index=201`, `source_path=crates/node/core/src/cli/config.rs`, `record_id=file-0201-atom-0001`
  - Source hunk: `@@ -26,0 +27,3 @@ pub trait PayloadBuilderConfig {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/core/src/cli/config.rs`

## File 0204: crates/node/events/src/node.rs

- Key: `file_index=204`, `source_path=crates/node/events/src/node.rs`, `record_id=file-0204-atom-0001`
  - Source hunk: `@@ -223,2 +223,2 @@ impl NodeState {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/node/events/src/node.rs`

## File 0206: crates/optimism/chainspec/src/lib.rs

- Key: `file_index=206`, `source_path=crates/optimism/chainspec/src/lib.rs`, `record_id=file-0206-atom-0001`
  - Source hunk: `@@ -258,0 +259,4 @@ impl EthChainSpec for OpChainSpec {`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/optimism/chainspec/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0207: crates/optimism/cli/src/commands/import.rs

- Key: `file_index=207`, `source_path=crates/optimism/cli/src/commands/import.rs`, `record_id=file-0207-atom-0001`
  - Source hunk: `@@ -92 +92 @@ impl<C: ChainSpecParser<ChainSpec = OpChainSpec>> ImportOpCommand<C> {`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/optimism/cli/src/commands/import.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0211: crates/optimism/consensus/src/lib.rs

- Key: `file_index=211`, `source_path=crates/optimism/consensus/src/lib.rs`, `record_id=file-0211-atom-0001`
  - Source hunk: `@@ -95 +95 @@ impl<ChainSpec: EthChainSpec + OpHardforks, B: Block> Consensus<B>`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/optimism/consensus/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0212: crates/optimism/consensus/src/proof.rs

- Key: `file_index=212`, `source_path=crates/optimism/consensus/src/proof.rs`, `record_id=file-0212-atom-0001`
  - Source hunk: `@@ -22,2 +22,2 @@ pub(crate) fn calculate_receipt_root_optimism<R: DepositReceipt>(`
  - Human question: Confirm that OP receipt-root compatibility remains outside the current Reth v2.2/Summit merge scope. If OP support becomes in scope, this atom requires a dedicated OP stack port rather than a local one-file fix.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/MERGE_NOTES.md`

## File 0218: crates/optimism/payload/src/builder.rs

- Key: `file_index=218`, `source_path=crates/optimism/payload/src/builder.rs`, `record_id=file-0218-atom-0001`
  - Source hunk: `@@ -151 +151 @@ where`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-revm-internal/crates/op-revm/src/api/builder.rs`

## File 0221: crates/optimism/primitives/src/receipt.rs

- Key: `file_index=221`, `source_path=crates/optimism/primitives/src/receipt.rs`, `record_id=file-0221-atom-0001`
  - Source hunk: `@@ -43,4 +43,4 @@ impl OpReceipt {`
  - Human question: Confirm that OP receipt enum compatibility remains outside the current Reth v2.2/Summit merge scope. If OP support becomes in scope, this atom belongs to a dedicated OP primitives port.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/MERGE_NOTES.md`

## File 0222: crates/optimism/primitives/src/transaction/signed.rs

- Key: `file_index=222`, `source_path=crates/optimism/primitives/src/transaction/signed.rs`, `record_id=file-0222-atom-0001`
  - Source hunk: `@@ -115 +115 @@ impl SignedTransaction for OpTransactionSigned {`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-alloy-internal/crates/consensus/src/signed.rs`

## File 0226: crates/optimism/rpc/src/eth/ext.rs

- Key: `file_index=226`, `source_path=crates/optimism/rpc/src/eth/ext.rs`, `record_id=file-0226-atom-0001`
  - Source hunk: `@@ -122,2 +122,4 @@ where`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-api/src/ext.rs`

## File 0231: crates/payload/basic/src/better_payload_emitter.rs

- Key: `file_index=231`, `source_path=crates/payload/basic/src/better_payload_emitter.rs`, `record_id=file-0231-atom-0001`
  - Source hunk: `@@ -1 +1 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/payload/basic/src/better_payload_emitter.rs`

## File 0232: crates/payload/basic/src/lib.rs

- Key: `file_index=232`, `source_path=crates/payload/basic/src/lib.rs`, `record_id=file-0232-atom-0001`
  - Source hunk: `@@ -29 +29,4 @@ use std::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/payload/basic/src/lib.rs`

## File 0233: crates/payload/basic/src/stack.rs

- Key: `file_index=233`, `source_path=crates/payload/basic/src/stack.rs`, `record_id=file-0233-atom-0001`
  - Source hunk: `@@ -2,2 +2,2 @@ use crate::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/payload/basic/src/stack.rs`

## File 0236: crates/payload/builder/src/service.rs

- Key: `file_index=236`, `source_path=crates/payload/builder/src/service.rs`, `record_id=file-0236-atom-0001`
  - Source hunk: `@@ -58,0 +59,3 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/payload/builder/src/service.rs`

## File 0242: crates/primitives-traits/Cargo.toml

- Key: `file_index=242`, `source_path=crates/primitives-traits/Cargo.toml`, `record_id=file-0242-atom-0001`
  - Source hunk: `@@ -43,0 +44 @@ thiserror.workspace = true`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/primitives-traits/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0248: crates/primitives-traits/src/size.rs

- Key: `file_index=248`, `source_path=crates/primitives-traits/src/size.rs`, `record_id=file-0248-atom-0001`
  - Source hunk: `@@ -2,0 +3 @@ use alloy_consensus::{`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/size.rs`

## File 0250: crates/primitives-traits/src/transaction/signed.rs

- Key: `file_index=250`, `source_path=crates/primitives-traits/src/transaction/signed.rs`, `record_id=file-0250-atom-0001`
  - Source hunk: `@@ -9,2 +9,5 @@ use alloy_consensus::{`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-alloy-internal/crates/consensus/src/signed.rs`

## File 0253: crates/prune/prune/src/pruner.rs

- Key: `file_index=253`, `source_path=crates/prune/prune/src/pruner.rs`, `record_id=file-0253-atom-0001`
  - Source hunk: `@@ -123 +123 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/prune/prune/src/pruner.rs`

## File 0255: crates/prune/prune/src/segments/receipts.rs

- Key: `file_index=255`, `source_path=crates/prune/prune/src/segments/receipts.rs`, `record_id=file-0255-atom-0001`
  - Source hunk: `@@ -32 +32 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/prune/prune/src/segments/receipts.rs`

## File 0257: crates/prune/prune/src/segments/static_file/headers.rs

- Key: `file_index=257`, `source_path=crates/prune/prune/src/segments/static_file/headers.rs`, `record_id=file-0257-atom-0001`
  - Source hunk: `@@ -57 +57 @@ impl<Provider: StaticFileProviderFactory + DBProvider<Tx: DbTxMut>> Segment<Prov`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/prune/prune/src/segments/static_file/headers.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0258: crates/prune/prune/src/segments/static_file/transactions.rs

- Key: `file_index=258`, `source_path=crates/prune/prune/src/segments/static_file/transactions.rs`, `record_id=file-0258-atom-0001`
  - Source hunk: `@@ -55 +55 @@ where`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/prune/prune/src/segments/static_file/transactions.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0259: crates/prune/prune/src/segments/user/account_history.rs

- Key: `file_index=259`, `source_path=crates/prune/prune/src/segments/user/account_history.rs`, `record_id=file-0259-atom-0001`
  - Source hunk: `@@ -54 +54 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/prune/prune/src/segments/user/account_history.rs`

## File 0261: crates/prune/prune/src/segments/user/receipts_by_logs.rs

- Key: `file_index=261`, `source_path=crates/prune/prune/src/segments/user/receipts_by_logs.rs`, `record_id=file-0261-atom-0001`
  - Source hunk: `@@ -144 +144 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/prune/prune/src/segments/user/receipts_by_logs.rs`

## File 0262: crates/prune/prune/src/segments/user/sender_recovery.rs

- Key: `file_index=262`, `source_path=crates/prune/prune/src/segments/user/sender_recovery.rs`, `record_id=file-0262-atom-0001`
  - Source hunk: `@@ -46 +46 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/prune/prune/src/segments/user/sender_recovery.rs`

## File 0263: crates/prune/prune/src/segments/user/storage_history.rs

- Key: `file_index=263`, `source_path=crates/prune/prune/src/segments/user/storage_history.rs`, `record_id=file-0263-atom-0001`
  - Source hunk: `@@ -56 +56 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/prune/prune/src/segments/user/storage_history.rs`

## File 0264: crates/prune/prune/src/segments/user/transaction_lookup.rs

- Key: `file_index=264`, `source_path=crates/prune/prune/src/segments/user/transaction_lookup.rs`, `record_id=file-0264-atom-0001`
  - Source hunk: `@@ -46 +46 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/prune/prune/src/segments/user/transaction_lookup.rs`

## File 0268: crates/ress/protocol/src/provider.rs

- Key: `file_index=268`, `source_path=crates/ress/protocol/src/provider.rs`, `record_id=file-0268-atom-0001`
  - Source hunk: `@@ -24,3 +24,3 @@ pub trait RessProtocolProvider: Send + Sync {`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ress/protocol/src/provider.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0273: crates/ritual-async-commitment-validator/Cargo.toml

- Key: `file_index=273`, `source_path=crates/ritual-async-commitment-validator/Cargo.toml`, `record_id=file-0273-atom-0001`
  - Source hunk: `@@ -0,0 +1,25 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async-commitment-validator/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0274: crates/ritual-async-commitment-validator/src/lib.rs

- Key: `file_index=274`, `source_path=crates/ritual-async-commitment-validator/src/lib.rs`, `record_id=file-0274-atom-0001`
  - Source hunk: `@@ -0,0 +1,576 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async-commitment-validator/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0275: crates/ritual-async-fees/Cargo.toml

- Key: `file_index=275`, `source_path=crates/ritual-async-fees/Cargo.toml`, `record_id=file-0275-atom-0001`
  - Source hunk: `@@ -0,0 +1,39 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/Cargo.toml`

## File 0276: crates/ritual-async-fees/src/constants.rs

- Key: `file_index=276`, `source_path=crates/ritual-async-fees/src/constants.rs`, `record_id=file-0276-atom-0001`
  - Source hunk: `@@ -0,0 +1,443 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/constants.rs`

## File 0277: crates/ritual-async-fees/src/delivery.rs

- Key: `file_index=277`, `source_path=crates/ritual-async-fees/src/delivery.rs`, `record_id=file-0277-atom-0001`
  - Source hunk: `@@ -0,0 +1,252 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async-fees/src/delivery.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0278: crates/ritual-async-fees/src/gas.rs

- Key: `file_index=278`, `source_path=crates/ritual-async-fees/src/gas.rs`, `record_id=file-0278-atom-0001`
  - Source hunk: `@@ -0,0 +1,198 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/gas.rs`

## File 0279: crates/ritual-async-fees/src/http.rs

- Key: `file_index=279`, `source_path=crates/ritual-async-fees/src/http.rs`, `record_id=file-0279-atom-0001`
  - Source hunk: `@@ -0,0 +1,44 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/http.rs`

## File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0001`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Required change: Resolve whether the downstream crates/ritual-async-fees/src/lib.rs behavior is still implemented in the destination module at the same relative path or whether it must be restored explicitly.
  - Likely destination: `unknown`

## File 0281: crates/ritual-async-fees/src/llm.rs

- Key: `file_index=281`, `source_path=crates/ritual-async-fees/src/llm.rs`, `record_id=file-0281-atom-0001`
  - Source hunk: `@@ -0,0 +1,941 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/llm.rs`

## File 0282: crates/ritual-async-fees/src/registry.rs

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0001`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/registry.rs`

## File 0283: crates/ritual-async-fees/src/scheduled.rs

- Key: `file_index=283`, `source_path=crates/ritual-async-fees/src/scheduled.rs`, `record_id=file-0283-atom-0001`
  - Source hunk: `@@ -0,0 +1,373 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## File 0284: crates/ritual-async-fees/src/validators.rs

- Key: `file_index=284`, `source_path=crates/ritual-async-fees/src/validators.rs`, `record_id=file-0284-atom-0001`
  - Source hunk: `@@ -0,0 +1,106 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/validators.rs`

## File 0285: crates/ritual-async-fees/src/wallet.rs

- Key: `file_index=285`, `source_path=crates/ritual-async-fees/src/wallet.rs`, `record_id=file-0285-atom-0001`
  - Source hunk: `@@ -0,0 +1,540 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/wallet.rs`

## File 0286: crates/ritual-async-inspector/Cargo.toml

- Key: `file_index=286`, `source_path=crates/ritual-async-inspector/Cargo.toml`, `record_id=file-0286-atom-0001`
  - Source hunk: `@@ -0,0 +1,14 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/Cargo.toml`

## File 0287: crates/ritual-async-inspector/src/inspector.rs

- Key: `file_index=287`, `source_path=crates/ritual-async-inspector/src/inspector.rs`, `record_id=file-0287-atom-0001`
  - Source hunk: `@@ -0,0 +1,224 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-revm-internal/crates/inspector/src/inspector.rs`

## File 0288: crates/ritual-async-inspector/src/lib.rs

- Key: `file_index=288`, `source_path=crates/ritual-async-inspector/src/lib.rs`, `record_id=file-0288-atom-0001`
  - Source hunk: `@@ -0,0 +1,59 @@`
  - Required change: Resolve whether the downstream crates/ritual-async-inspector/src/lib.rs behavior is still implemented in the destination module at the same relative path or whether it must be restored explicitly.
  - Likely destination: `unknown`

## File 0289: crates/ritual-async-inspector/src/utils.rs

- Key: `file_index=289`, `source_path=crates/ritual-async-inspector/src/utils.rs`, `record_id=file-0289-atom-0001`
  - Source hunk: `@@ -0,0 +1,4 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async-inspector/src/utils.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0290: crates/ritual-async-registry/Cargo.toml

- Key: `file_index=290`, `source_path=crates/ritual-async-registry/Cargo.toml`, `record_id=file-0290-atom-0001`
  - Source hunk: `@@ -0,0 +1,27 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/Cargo.toml`

## File 0292: crates/ritual-async-registry/src/lib.rs

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0001`
  - Source hunk: `@@ -0,0 +1,2223 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

## File 0294: crates/ritual-async/Cargo.toml

- Key: `file_index=294`, `source_path=crates/ritual-async/Cargo.toml`, `record_id=file-0294-atom-0001`
  - Source hunk: `@@ -0,0 +1,43 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0295: crates/ritual-async/src/detector.rs

- Key: `file_index=295`, `source_path=crates/ritual-async/src/detector.rs`, `record_id=file-0295-atom-0001`
  - Source hunk: `@@ -0,0 +1,1546 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async/src/detector.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0296: crates/ritual-async/src/lib.rs

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0001`
  - Source hunk: `@@ -0,0 +1,54 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0297: crates/ritual-async/src/validation.rs

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0001`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-revm-internal/crates/handler/src/validation.rs`

## File 0298: crates/ritual-async/src/wallet.rs

- Key: `file_index=298`, `source_path=crates/ritual-async/src/wallet.rs`, `record_id=file-0298-atom-0001`
  - Source hunk: `@@ -0,0 +1,140 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-async/src/wallet.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0299: crates/ritual-block-verification/Cargo.toml

- Key: `file_index=299`, `source_path=crates/ritual-block-verification/Cargo.toml`, `record_id=file-0299-atom-0001`
  - Source hunk: `@@ -0,0 +1,42 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/Cargo.toml`

## File 0303: crates/ritual-block-verification/src/nonce_lock.rs

- Key: `file_index=303`, `source_path=crates/ritual-block-verification/src/nonce_lock.rs`, `record_id=file-0303-atom-0001`
  - Source hunk: `@@ -0,0 +1,422 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-block-verification/src/nonce_lock.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0001`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal/crates/ritual-nsm/src/verifier.rs`

## File 0305: crates/ritual-blocking-pubsub/Cargo.toml

- Key: `file_index=305`, `source_path=crates/ritual-blocking-pubsub/Cargo.toml`, `record_id=file-0305-atom-0001`
  - Source hunk: `@@ -0,0 +1,13 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-blocking-pubsub/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0306: crates/ritual-blocking-pubsub/src/lib.rs

- Key: `file_index=306`, `source_path=crates/ritual-blocking-pubsub/src/lib.rs`, `record_id=file-0306-atom-0001`
  - Source hunk: `@@ -0,0 +1,38 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-blocking-pubsub/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0307: crates/ritual-heartbeat-tracker/Cargo.toml

- Key: `file_index=307`, `source_path=crates/ritual-heartbeat-tracker/Cargo.toml`, `record_id=file-0307-atom-0001`
  - Source hunk: `@@ -0,0 +1,13 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-heartbeat-tracker/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0308: crates/ritual-heartbeat-tracker/src/events.rs

- Key: `file_index=308`, `source_path=crates/ritual-heartbeat-tracker/src/events.rs`, `record_id=file-0308-atom-0001`
  - Source hunk: `@@ -0,0 +1,38 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-heartbeat-tracker/src/events.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0309: crates/ritual-heartbeat-tracker/src/lib.rs

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0001`
  - Source hunk: `@@ -0,0 +1,436 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-heartbeat-tracker/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0310: crates/ritual-metrics/Cargo.toml

- Key: `file_index=310`, `source_path=crates/ritual-metrics/Cargo.toml`, `record_id=file-0310-atom-0001`
  - Source hunk: `@@ -0,0 +1,50 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-metrics/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0311: crates/ritual-metrics/src/block.rs

- Key: `file_index=311`, `source_path=crates/ritual-metrics/src/block.rs`, `record_id=file-0311-atom-0001`
  - Source hunk: `@@ -0,0 +1,587 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/eth/block.rs`

## File 0312: crates/ritual-metrics/src/lib.rs

- Key: `file_index=312`, `source_path=crates/ritual-metrics/src/lib.rs`, `record_id=file-0312-atom-0001`
  - Source hunk: `@@ -0,0 +1,20 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-metrics/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0313: crates/ritual-metrics/src/scheduling.rs

- Key: `file_index=313`, `source_path=crates/ritual-metrics/src/scheduling.rs`, `record_id=file-0313-atom-0001`
  - Source hunk: `@@ -0,0 +1,415 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-metrics/src/scheduling.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0314: crates/ritual-metrics/src/tx.rs

- Key: `file_index=314`, `source_path=crates/ritual-metrics/src/tx.rs`, `record_id=file-0314-atom-0001`
  - Source hunk: `@@ -0,0 +1,651 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/db/src/implementation/mdbx/tx.rs`

## File 0315: crates/ritual-precompile-addresses/Cargo.toml

- Key: `file_index=315`, `source_path=crates/ritual-precompile-addresses/Cargo.toml`, `record_id=file-0315-atom-0001`
  - Source hunk: `@@ -0,0 +1,10 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-addresses/Cargo.toml`

## File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0001`
  - Source hunk: `@@ -0,0 +1,115 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-addresses/src/lib.rs`

## File 0317: crates/ritual-precompile-codecs/Cargo.toml

- Key: `file_index=317`, `source_path=crates/ritual-precompile-codecs/Cargo.toml`, `record_id=file-0317-atom-0001`
  - Source hunk: `@@ -0,0 +1,18 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/Cargo.toml`

## File 0318: crates/ritual-precompile-codecs/src/dkms_key.rs

- Key: `file_index=318`, `source_path=crates/ritual-precompile-codecs/src/dkms_key.rs`, `record_id=file-0318-atom-0001`
  - Source hunk: `@@ -0,0 +1,272 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/dkms_key.rs`

## File 0319: crates/ritual-precompile-codecs/src/error.rs

- Key: `file_index=319`, `source_path=crates/ritual-precompile-codecs/src/error.rs`, `record_id=file-0319-atom-0001`
  - Source hunk: `@@ -0,0 +1,22 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/error.rs`

## File 0320: crates/ritual-precompile-codecs/src/executor.rs

- Key: `file_index=320`, `source_path=crates/ritual-precompile-codecs/src/executor.rs`, `record_id=file-0320-atom-0001`
  - Source hunk: `@@ -0,0 +1,260 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/executor.rs`

## File 0321: crates/ritual-precompile-codecs/src/http_call.rs

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0001`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/http_call.rs`

## File 0322: crates/ritual-precompile-codecs/src/lib.rs

- Key: `file_index=322`, `source_path=crates/ritual-precompile-codecs/src/lib.rs`, `record_id=file-0322-atom-0001`
  - Source hunk: `@@ -0,0 +1,31 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

## File 0323: crates/ritual-precompile-codecs/src/llm_call.rs

- Key: `file_index=323`, `source_path=crates/ritual-precompile-codecs/src/llm_call.rs`, `record_id=file-0323-atom-0001`
  - Source hunk: `@@ -0,0 +1,361 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/llm_call.rs`

## File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0001`
  - Source hunk: `@@ -0,0 +1,1172 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/long_running.rs`

## File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0001`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/persistent_agent.rs`

## File 0326: crates/ritual-precompile-codecs/src/sovereign_agent.rs

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0001`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## File 0327: crates/ritual-precompile-codecs/src/storage_ref.rs

- Key: `file_index=327`, `source_path=crates/ritual-precompile-codecs/src/storage_ref.rs`, `record_id=file-0327-atom-0001`
  - Source hunk: `@@ -0,0 +1,93 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/storage_ref.rs`

## File 0328: crates/ritual-scheduled-block-building/Cargo.toml

- Key: `file_index=328`, `source_path=crates/ritual-scheduled-block-building/Cargo.toml`, `record_id=file-0328-atom-0001`
  - Source hunk: `@@ -0,0 +1,46 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/Cargo.toml`

## File 0329: crates/ritual-scheduled-block-building/src/lib.rs

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0001`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/src/lib.rs`

## File 0330: crates/ritual-scheduled-verification/Cargo.toml

- Key: `file_index=330`, `source_path=crates/ritual-scheduled-verification/Cargo.toml`, `record_id=file-0330-atom-0001`
  - Source hunk: `@@ -0,0 +1,23 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/Cargo.toml`

## File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0001`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

## File 0333: crates/ritual-scheduled-verification/src/predicate.rs

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0001`
  - Source hunk: `@@ -0,0 +1,235 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/predicate.rs`

## File 0335: crates/ritual-sequencing-rights/Cargo.toml

- Key: `file_index=335`, `source_path=crates/ritual-sequencing-rights/Cargo.toml`, `record_id=file-0335-atom-0001`
  - Source hunk: `@@ -0,0 +1,35 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-sequencing-rights/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0336: crates/ritual-sequencing-rights/src/bucket.rs

- Key: `file_index=336`, `source_path=crates/ritual-sequencing-rights/src/bucket.rs`, `record_id=file-0336-atom-0001`
  - Source hunk: `@@ -0,0 +1,604 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-sequencing-rights/src/bucket.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0337: crates/ritual-sequencing-rights/src/classifier.rs

- Key: `file_index=337`, `source_path=crates/ritual-sequencing-rights/src/classifier.rs`, `record_id=file-0337-atom-0001`
  - Source hunk: `@@ -0,0 +1,763 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-sequencing-rights/src/classifier.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0338: crates/ritual-sequencing-rights/src/error.rs

- Key: `file_index=338`, `source_path=crates/ritual-sequencing-rights/src/error.rs`, `record_id=file-0338-atom-0001`
  - Source hunk: `@@ -0,0 +1,39 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-sequencing-rights/src/error.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0339: crates/ritual-sequencing-rights/src/lib.rs

- Key: `file_index=339`, `source_path=crates/ritual-sequencing-rights/src/lib.rs`, `record_id=file-0339-atom-0001`
  - Source hunk: `@@ -0,0 +1,244 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-sequencing-rights/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0340: crates/ritual-sequencing-rights/src/priority.rs

- Key: `file_index=340`, `source_path=crates/ritual-sequencing-rights/src/priority.rs`, `record_id=file-0340-atom-0001`
  - Source hunk: `@@ -0,0 +1,287 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/net/p2p/src/priority.rs`

## File 0341: crates/ritual-sequencing-rights/src/reader.rs

- Key: `file_index=341`, `source_path=crates/ritual-sequencing-rights/src/reader.rs`, `record_id=file-0341-atom-0001`
  - Source hunk: `@@ -0,0 +1,358 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-tee-registry-reader/src/reader.rs`

## File 0342: crates/ritual-sequencing-rights/src/types.rs

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0001`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-sequencing-rights/src/types.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0343: crates/ritual-spc-signature/Cargo.toml

- Key: `file_index=343`, `source_path=crates/ritual-spc-signature/Cargo.toml`, `record_id=file-0343-atom-0001`
  - Source hunk: `@@ -0,0 +1,16 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/Cargo.toml`

## File 0344: crates/ritual-spc-signature/src/lib.rs

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0001`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

## File 0346: crates/ritual-spc-verification/Cargo.toml

- Key: `file_index=346`, `source_path=crates/ritual-spc-verification/Cargo.toml`, `record_id=file-0346-atom-0001`
  - Source hunk: `@@ -0,0 +1,76 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-spc-verification/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0348: crates/ritual-spc-verification/src/client.rs

- Key: `file_index=348`, `source_path=crates/ritual-spc-verification/src/client.rs`, `record_id=file-0348-atom-0001`
  - Source hunk: `@@ -0,0 +1,180 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal/crates/sidecar-client/src/client.rs`

## File 0349: crates/ritual-spc-verification/src/error.rs

- Key: `file_index=349`, `source_path=crates/ritual-spc-verification/src/error.rs`, `record_id=file-0349-atom-0001`
  - Source hunk: `@@ -0,0 +1,64 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-spc-verification/src/error.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0350: crates/ritual-spc-verification/src/lib.rs

- Key: `file_index=350`, `source_path=crates/ritual-spc-verification/src/lib.rs`, `record_id=file-0350-atom-0001`
  - Source hunk: `@@ -0,0 +1,105 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-spc-verification/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0351: crates/ritual-spc-verification/src/types.rs

- Key: `file_index=351`, `source_path=crates/ritual-spc-verification/src/types.rs`, `record_id=file-0351-atom-0001`
  - Source hunk: `@@ -0,0 +1,380 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/ritual-spc-verification/src/types.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0352: crates/ritual-spc-verification/src/verifier.rs

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0001`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal/crates/ritual-nsm/src/verifier.rs`

## File 0353: crates/ritual-tee-registry-reader/Cargo.toml

- Key: `file_index=353`, `source_path=crates/ritual-tee-registry-reader/Cargo.toml`, `record_id=file-0353-atom-0001`
  - Source hunk: `@@ -0,0 +1,28 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-tee-registry-reader/Cargo.toml`

## File 0363: crates/rpc/rpc-api/Cargo.toml

- Key: `file_index=363`, `source_path=crates/rpc/rpc-api/Cargo.toml`, `record_id=file-0363-atom-0001`
  - Source hunk: `@@ -19,0 +20,3 @@ reth-network-peers.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-api/Cargo.toml`

## File 0364: crates/rpc/rpc-api/src/lib.rs

- Key: `file_index=364`, `source_path=crates/rpc/rpc-api/src/lib.rs`, `record_id=file-0364-atom-0001`
  - Source hunk: `@@ -27,0 +28 @@ mod reth;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-api/src/lib.rs`

## File 0365: crates/rpc/rpc-api/src/ritual.rs

- Key: `file_index=365`, `source_path=crates/rpc/rpc-api/src/ritual.rs`, `record_id=file-0365-atom-0001`
  - Source hunk: `@@ -0,0 +1,676 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/rpc/rpc-api/src/ritual.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0366: crates/rpc/rpc-api/src/txpool.rs

- Key: `file_index=366`, `source_path=crates/rpc/rpc-api/src/txpool.rs`, `record_id=file-0366-atom-0001`
  - Source hunk: `@@ -3 +3,4 @@ use alloy_primitives::Address;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-api/src/txpool.rs`

## File 0370: crates/rpc/rpc-builder/src/lib.rs

- Key: `file_index=370`, `source_path=crates/rpc/rpc-builder/src/lib.rs`, `record_id=file-0370-atom-0001`
  - Source hunk: `@@ -1263,0 +1264,3 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-builder/src/lib.rs`

## File 0372: crates/rpc/rpc-engine-api/src/engine_api.rs

- Key: `file_index=372`, `source_path=crates/rpc/rpc-engine-api/src/engine_api.rs`, `record_id=file-0372-atom-0001`
  - Source hunk: `@@ -740 +740 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-engine-api/src/engine_api.rs`

## File 0375: crates/rpc/rpc-eth-api/src/helpers/call.rs

- Key: `file_index=375`, `source_path=crates/rpc/rpc-eth-api/src/helpers/call.rs`, `record_id=file-0375-atom-0001`
  - Source hunk: `@@ -75 +75 @@ pub trait EthCall: EstimateCall + Call + LoadPendingBlock + LoadBlock + FullEthA`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-api/src/helpers/call.rs`

## File 0376: crates/rpc/rpc-eth-api/src/helpers/estimate.rs

- Key: `file_index=376`, `source_path=crates/rpc/rpc-eth-api/src/helpers/estimate.rs`, `record_id=file-0376-atom-0001`
  - Source hunk: `@@ -99 +99 @@ pub trait EstimateCall: Call {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-api/src/helpers/estimate.rs`

## File 0377: crates/rpc/rpc-eth-api/src/helpers/fee.rs

- Key: `file_index=377`, `source_path=crates/rpc/rpc-eth-api/src/helpers/fee.rs`, `record_id=file-0377-atom-0001`
  - Source hunk: `@@ -60 +60 @@ pub trait EthFees: LoadFee {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-api/src/helpers/fee.rs`

## File 0378: crates/rpc/rpc-eth-api/src/helpers/pending_block.rs

- Key: `file_index=378`, `source_path=crates/rpc/rpc-eth-api/src/helpers/pending_block.rs`, `record_id=file-0378-atom-0001`
  - Source hunk: `@@ -157,3 +157,3 @@ pub trait LoadPendingBlock:`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-api/src/helpers/pending_block.rs`

## File 0384: crates/rpc/rpc-eth-types/src/error/mod.rs

- Key: `file_index=384`, `source_path=crates/rpc/rpc-eth-types/src/error/mod.rs`, `record_id=file-0384-atom-0001`
  - Source hunk: `@@ -49,2 +49,2 @@ pub enum EthApiError {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-types/src/error/mod.rs`

## File 0385: crates/rpc/rpc-eth-types/src/fee_history.rs

- Key: `file_index=385`, `source_path=crates/rpc/rpc-eth-types/src/fee_history.rs`, `record_id=file-0385-atom-0001`
  - Source hunk: `@@ -109 +109 @@ impl FeeHistoryCache {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-types/src/fee_history.rs`

## File 0388: crates/rpc/rpc-eth-types/src/logs_utils.rs

- Key: `file_index=388`, `source_path=crates/rpc/rpc-eth-types/src/logs_utils.rs`, `record_id=file-0388-atom-0001`
  - Source hunk: `@@ -148,5 +148,5 @@ pub fn log_matches_filter(`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-types/src/logs_utils.rs`

## File 0389: crates/rpc/rpc-eth-types/src/receipt.rs

- Key: `file_index=389`, `source_path=crates/rpc/rpc-eth-types/src/receipt.rs`, `record_id=file-0389-atom-0001`
  - Source hunk: `@@ -78,0 +79,98 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-types/src/receipt.rs`

## File 0391: crates/rpc/rpc-eth-types/src/utils.rs

- Key: `file_index=391`, `source_path=crates/rpc/rpc-eth-types/src/utils.rs`, `record_id=file-0391-atom-0001`
  - Source hunk: `@@ -15 +15 @@ pub fn recover_raw_transaction<T: SignedTransaction>(mut data: &[u8]) -> EthResu`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-eth-types/src/utils.rs`

## File 0393: crates/rpc/rpc-server-types/src/module.rs

- Key: `file_index=393`, `source_path=crates/rpc/rpc-server-types/src/module.rs`, `record_id=file-0393-atom-0001`
  - Source hunk: `@@ -207 +207 @@ impl FromStr for RpcModuleSelection {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc-server-types/src/module.rs`

## File 0395: crates/rpc/rpc/Cargo.toml

- Key: `file_index=395`, `source_path=crates/rpc/rpc/Cargo.toml`, `record_id=file-0395-atom-0001`
  - Source hunk: `@@ -40,0 +41,10 @@ reth-node-api.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/Cargo.toml`

## File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0001`
  - Source hunk: `@@ -0,0 +1,550 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/rpc/rpc/src/async_tx_validator.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0398: crates/rpc/rpc/src/eth/bundle.rs

- Key: `file_index=398`, `source_path=crates/rpc/rpc/src/eth/bundle.rs`, `record_id=file-0398-atom-0001`
  - Source hunk: `@@ -69 +69 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/eth/bundle.rs`

## File 0399: crates/rpc/rpc/src/eth/filter.rs

- Key: `file_index=399`, `source_path=crates/rpc/rpc/src/eth/filter.rs`, `record_id=file-0399-atom-0001`
  - Source hunk: `@@ -200 +200 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/eth/filter.rs`

## File 0401: crates/rpc/rpc/src/eth/helpers/call.rs

- Key: `file_index=401`, `source_path=crates/rpc/rpc/src/eth/helpers/call.rs`, `record_id=file-0401-atom-0001`
  - Source hunk: `@@ -57 +57 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/eth/helpers/call.rs`

## File 0402: crates/rpc/rpc/src/eth/helpers/pending_block.rs

- Key: `file_index=402`, `source_path=crates/rpc/rpc/src/eth/helpers/pending_block.rs`, `record_id=file-0402-atom-0001`
  - Source hunk: `@@ -74,0 +75 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/eth/helpers/pending_block.rs`

## File 0403: crates/rpc/rpc/src/eth/helpers/transaction.rs

- Key: `file_index=403`, `source_path=crates/rpc/rpc/src/eth/helpers/transaction.rs`, `record_id=file-0403-atom-0001`
  - Source hunk: `@@ -1,0 +2,9 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/eth/helpers/transaction.rs`

## File 0407: crates/rpc/rpc/src/lib.rs

- Key: `file_index=407`, `source_path=crates/rpc/rpc/src/lib.rs`, `record_id=file-0407-atom-0001`
  - Source hunk: `@@ -35,0 +36 @@ mod admin;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/lib.rs`

## File 0408: crates/rpc/rpc/src/otterscan.rs

- Key: `file_index=408`, `source_path=crates/rpc/rpc/src/otterscan.rs`, `record_id=file-0408-atom-0001`
  - Source hunk: `@@ -229 +229 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/otterscan.rs`

## File 0410: crates/rpc/rpc/src/ritual.rs

- Key: `file_index=410`, `source_path=crates/rpc/rpc/src/ritual.rs`, `record_id=file-0410-atom-0001`
  - Source hunk: `@@ -0,0 +1,1153 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/rpc/rpc/src/ritual.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0412: crates/rpc/rpc/src/txpool.rs

- Key: `file_index=412`, `source_path=crates/rpc/rpc/src/txpool.rs`, `record_id=file-0412-atom-0001`
  - Source hunk: `@@ -2 +2 @@ use core::fmt;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/txpool.rs`

## File 0413: crates/rpc/rpc/src/validation.rs

- Key: `file_index=413`, `source_path=crates/rpc/rpc/src/validation.rs`, `record_id=file-0413-atom-0001`
  - Source hunk: `@@ -126 +126 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/rpc/rpc/src/validation.rs`

## File 0414: crates/scheduling/Cargo.toml

- Key: `file_index=414`, `source_path=crates/scheduling/Cargo.toml`, `record_id=file-0414-atom-0001`
  - Source hunk: `@@ -0,0 +1,42 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/scheduling/Cargo.toml; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0415: crates/scheduling/src/canonical.rs

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0001`
  - Source hunk: `@@ -0,0 +1,544 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/scheduling/src/canonical.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0416: crates/scheduling/src/contract.rs

- Key: `file_index=416`, `source_path=crates/scheduling/src/contract.rs`, `record_id=file-0416-atom-0001`
  - Source hunk: `@@ -0,0 +1,1035 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-revm-internal/crates/interpreter/src/instructions/contract.rs`

## File 0417: crates/scheduling/src/events.rs

- Key: `file_index=417`, `source_path=crates/scheduling/src/events.rs`, `record_id=file-0417-atom-0001`
  - Source hunk: `@@ -0,0 +1,24 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/scheduling/src/events.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0418: crates/scheduling/src/job.rs

- Key: `file_index=418`, `source_path=crates/scheduling/src/job.rs`, `record_id=file-0418-atom-0001`
  - Source hunk: `@@ -0,0 +1,10 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/scheduling/src/job.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0419: crates/scheduling/src/lib.rs

- Key: `file_index=419`, `source_path=crates/scheduling/src/lib.rs`, `record_id=file-0419-atom-0001`
  - Source hunk: `@@ -0,0 +1,29 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/scheduling/src/lib.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0420: crates/scheduling/src/service.rs

- Key: `file_index=420`, `source_path=crates/scheduling/src/service.rs`, `record_id=file-0420-atom-0001`
  - Source hunk: `@@ -0,0 +1,58 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-alloy-internal/crates/pubsub/src/service.rs`

## File 0421: crates/scheduling/src/singleton.rs

- Key: `file_index=421`, `source_path=crates/scheduling/src/singleton.rs`, `record_id=file-0421-atom-0001`
  - Source hunk: `@@ -0,0 +1,519 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/scheduling/src/singleton.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0422: crates/scheduling/src/transaction.rs

- Key: `file_index=422`, `source_path=crates/scheduling/src/transaction.rs`, `record_id=file-0422-atom-0001`
  - Source hunk: `@@ -0,0 +1,212 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/rpc/transaction.rs`

## File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0001`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/scheduling/src/types.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0424: crates/stages/api/Cargo.toml

- Key: `file_index=424`, `source_path=crates/stages/api/Cargo.toml`, `record_id=file-0424-atom-0001`
  - Source hunk: `@@ -50,0 +51 @@ reth-testing-utils.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/stages/api/Cargo.toml`

## File 0427: crates/stages/api/src/pipeline/mod.rs

- Key: `file_index=427`, `source_path=crates/stages/api/src/pipeline/mod.rs`, `record_id=file-0427-atom-0001`
  - Source hunk: `@@ -33,0 +34,5 @@ pub use set::*;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/stages/api/src/pipeline/mod.rs`

## File 0431: crates/stages/stages/src/stages/execution.rs

- Key: `file_index=431`, `source_path=crates/stages/stages/src/stages/execution.rs`, `record_id=file-0431-atom-0001`
  - Source hunk: `@@ -68 +67,0 @@ use super::missing_static_data_error;`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-revm-internal/crates/handler/src/execution.rs`

## File 0438: crates/stages/stages/src/stages/merkle.rs

- Key: `file_index=438`, `source_path=crates/stages/stages/src/stages/merkle.rs`, `record_id=file-0438-atom-0001`
  - Source hunk: `@@ -110 +110 @@ impl MerkleStage {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/stages/stages/src/stages/merkle.rs`

## File 0444: crates/stages/stages/src/stages/tx_lookup.rs

- Key: `file_index=444`, `source_path=crates/stages/stages/src/stages/tx_lookup.rs`, `record_id=file-0444-atom-0001`
  - Source hunk: `@@ -245,2 +245,2 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/stages/stages/src/stages/tx_lookup.rs`

## File 0447: crates/stages/types/src/checkpoints.rs

- Key: `file_index=447`, `source_path=crates/stages/types/src/checkpoints.rs`, `record_id=file-0447-atom-0001`
  - Source hunk: `@@ -166 +166 @@ impl EntitiesCheckpoint {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/stages/types/src/checkpoints.rs`

## File 0449: crates/static-file/static-file/src/static_file_producer.rs

- Key: `file_index=449`, `source_path=crates/static-file/static-file/src/static_file_producer.rs`, `record_id=file-0449-atom-0001`
  - Source hunk: `@@ -119 +119 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/static-file/static-file/src/static_file_producer.rs`

## File 0450: crates/static-file/types/src/lib.rs

- Key: `file_index=450`, `source_path=crates/static-file/types/src/lib.rs`, `record_id=file-0450-atom-0001`
  - Source hunk: `@@ -97,4 +97,4 @@ impl StaticFileTargets {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/static-file/types/src/lib.rs`

## File 0452: crates/storage/codecs/Cargo.toml

- Key: `file_index=452`, `source_path=crates/storage/codecs/Cargo.toml`, `record_id=file-0452-atom-0001`
  - Source hunk: `@@ -32,0 +33 @@ serde.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/Cargo.toml`

## File 0459: crates/storage/codecs/src/alloy/passkey_signature.rs

- Key: `file_index=459`, `source_path=crates/storage/codecs/src/alloy/passkey_signature.rs`, `record_id=file-0459-atom-0001`
  - Source hunk: `@@ -0,0 +1,148 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/passkey_signature.rs`

## File 0462: crates/storage/codecs/src/alloy/transaction/eip1559.rs

- Key: `file_index=462`, `source_path=crates/storage/codecs/src/alloy/transaction/eip1559.rs`, `record_id=file-0462-atom-0001`
  - Source hunk: `@@ -4 +4 @@ use crate::Compact;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/eip1559.rs`

## File 0463: crates/storage/codecs/src/alloy/transaction/ethereum.rs

- Key: `file_index=463`, `source_path=crates/storage/codecs/src/alloy/transaction/ethereum.rs`, `record_id=file-0463-atom-0001`
  - Source hunk: `@@ -3,2 +3,2 @@ use alloy_consensus::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/ethereum.rs`

## File 0464: crates/storage/codecs/src/alloy/transaction/legacy.rs

- Key: `file_index=464`, `source_path=crates/storage/codecs/src/alloy/transaction/legacy.rs`, `record_id=file-0464-atom-0001`
  - Source hunk: `@@ -4 +4 @@ use crate::Compact;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/legacy.rs`

## File 0465: crates/storage/codecs/src/alloy/transaction/mod.rs

- Key: `file_index=465`, `source_path=crates/storage/codecs/src/alloy/transaction/mod.rs`, `record_id=file-0465-atom-0001`
  - Source hunk: `@@ -4 +4 @@ use alloy_consensus::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/mod.rs`

## File 0468: crates/storage/codecs/src/alloy/transaction/spc_call.rs

- Key: `file_index=468`, `source_path=crates/storage/codecs/src/alloy/transaction/spc_call.rs`, `record_id=file-0468-atom-0001`
  - Source hunk: `@@ -0,0 +1,349 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/spc_call.rs`

## File 0469: crates/storage/codecs/src/alloy/transaction/txtype.rs

- Key: `file_index=469`, `source_path=crates/storage/codecs/src/alloy/transaction/txtype.rs`, `record_id=file-0469-atom-0001`
  - Source hunk: `@@ -4,0 +5,2 @@ use alloy_consensus::constants::{EIP4844_TX_TYPE_ID, EIP7702_TX_TYPE_ID};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/txtype.rs`

## File 0470: crates/storage/codecs/src/lib.rs

- Key: `file_index=470`, `source_path=crates/storage/codecs/src/lib.rs`, `record_id=file-0470-atom-0001`
  - Source hunk: `@@ -239 +239,2 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/lib.rs`

## File 0475: crates/storage/db-common/src/db_tool/mod.rs

- Key: `file_index=475`, `source_path=crates/storage/db-common/src/db_tool/mod.rs`, `record_id=file-0475-atom-0001`
  - Source hunk: `@@ -53 +53 @@ impl<N: NodeTypesWithDB> DbTool<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/db-common/src/db_tool/mod.rs`

## File 0476: crates/storage/db-common/src/init.rs

- Key: `file_index=476`, `source_path=crates/storage/db-common/src/init.rs`, `record_id=file-0476-atom-0001`
  - Source hunk: `@@ -105 +105 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/db-common/src/init.rs`

## File 0483: crates/storage/libmdbx-rs/src/codec.rs

- Key: `file_index=483`, `source_path=crates/storage/libmdbx-rs/src/codec.rs`, `record_id=file-0483-atom-0001`
  - Source hunk: `@@ -44,2 +44,2 @@ impl TableObject for Cow<'_, [u8]> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/libmdbx-rs/src/codec.rs`

## File 0494: crates/storage/provider/Cargo.toml

- Key: `file_index=494`, `source_path=crates/storage/provider/Cargo.toml`, `record_id=file-0494-atom-0001`
  - Source hunk: `@@ -35,0 +36 @@ reth-node-types.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/Cargo.toml`

## File 0495: crates/storage/provider/src/providers/blockchain_provider.rs

- Key: `file_index=495`, `source_path=crates/storage/provider/src/providers/blockchain_provider.rs`, `record_id=file-0495-atom-0001`
  - Source hunk: `@@ -709,0 +710,7 @@ impl<N: ProviderNodeTypes> CanonStateSubscriptions for BlockchainProvider<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/src/providers/blockchain_provider.rs`

## File 0496: crates/storage/provider/src/providers/consistent.rs

- Key: `file_index=496`, `source_path=crates/storage/provider/src/providers/consistent.rs`, `record_id=file-0496-atom-0001`
  - Source hunk: `@@ -151 +151 @@ impl<N: ProviderNodeTypes> ConsistentProvider<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/src/providers/consistent.rs`

## File 0498: crates/storage/provider/src/providers/database/provider.rs

- Key: `file_index=498`, `source_path=crates/storage/provider/src/providers/database/provider.rs`, `record_id=file-0498-atom-0001`
  - Source hunk: `@@ -171,2 +171,2 @@ impl<TX: DbTx + 'static, N: NodeTypes> DatabaseProvider<TX, N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/src/providers/database/provider.rs`

## File 0499: crates/storage/provider/src/providers/state/historical.rs

- Key: `file_index=499`, `source_path=crates/storage/provider/src/providers/state/historical.rs`, `record_id=file-0499-atom-0001`
  - Source hunk: `@@ -83 +83 @@ impl<'b, Provider: DBProvider + BlockNumReader + StateCommitmentProvider>`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/src/providers/state/historical.rs`

## File 0502: crates/storage/provider/src/providers/static_file/manager.rs

- Key: `file_index=502`, `source_path=crates/storage/provider/src/providers/static_file/manager.rs`, `record_id=file-0502-atom-0001`
  - Source hunk: `@@ -158,3 +158,3 @@ impl<N: NodePrimitives> StaticFileProvider<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/src/providers/static_file/manager.rs`

## File 0503: crates/storage/provider/src/providers/static_file/writer.rs

- Key: `file_index=503`, `source_path=crates/storage/provider/src/providers/static_file/writer.rs`, `record_id=file-0503-atom-0001`
  - Source hunk: `@@ -380 +380 @@ impl<N: NodePrimitives> StaticFileProviderRW<N> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/src/providers/static_file/writer.rs`

## File 0504: crates/storage/provider/src/test_utils/mock.rs

- Key: `file_index=504`, `source_path=crates/storage/provider/src/test_utils/mock.rs`, `record_id=file-0504-atom-0001`
  - Source hunk: `@@ -404 +404 @@ impl<ChainSpec: EthChainSpec + 'static> TransactionsProvider`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/provider/src/test_utils/mock.rs`

## File 0511: crates/tracing/Cargo.toml

- Key: `file_index=511`, `source_path=crates/tracing/Cargo.toml`, `record_id=file-0511-atom-0001`
  - Source hunk: `@@ -22,0 +23 @@ clap = { workspace = true, features = ["derive"] }`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/tracing/Cargo.toml`

## File 0512: crates/tracing/src/lib.rs

- Key: `file_index=512`, `source_path=crates/tracing/src/lib.rs`, `record_id=file-0512-atom-0001`
  - Source hunk: `@@ -53,0 +54 @@ pub use layers::{FileInfo, FileWorkerGuard};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/tracing/src/lib.rs`

## File 0513: crates/tracing/src/ritual_router.rs

- Key: `file_index=513`, `source_path=crates/tracing/src/ritual_router.rs`, `record_id=file-0513-atom-0001`
  - Source hunk: `@@ -0,0 +1,147 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/tracing/src/ritual_router.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0514: crates/transaction-pool/Cargo.toml

- Key: `file_index=514`, `source_path=crates/transaction-pool/Cargo.toml`, `record_id=file-0514-atom-0001`
  - Source hunk: `@@ -26,0 +27,5 @@ revm-primitives.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/Cargo.toml`

## File 0523: crates/transaction-pool/src/error.rs

- Key: `file_index=523`, `source_path=crates/transaction-pool/src/error.rs`, `record_id=file-0523-atom-0001`
  - Source hunk: `@@ -68,0 +69,4 @@ pub enum PoolErrorKind {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/error.rs`

## File 0525: crates/transaction-pool/src/maintain.rs

- Key: `file_index=525`, `source_path=crates/transaction-pool/src/maintain.rs`, `record_id=file-0525-atom-0001`
  - Source hunk: `@@ -12 +12 @@ use alloy_eips::BlockNumberOrTag;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/maintain.rs`

## File 0526: crates/transaction-pool/src/metrics.rs

- Key: `file_index=526`, `source_path=crates/transaction-pool/src/metrics.rs`, `record_id=file-0526-atom-0001`
  - Source hunk: `@@ -39 +39,10 @@ pub struct TxPoolMetrics {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/metrics.rs`

## File 0527: crates/transaction-pool/src/noop.rs

- Key: `file_index=527`, `source_path=crates/transaction-pool/src/noop.rs`, `record_id=file-0527-atom-0001`
  - Source hunk: `@@ -9 +9,5 @@ use crate::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/noop.rs`

## File 0528: crates/transaction-pool/src/pool/async_pool.rs

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0001`
  - Source hunk: `@@ -0,0 +1,1471 @@`
  - Required change: Resolve whether the downstream crates/transaction-pool/src/pool/async_pool.rs behavior is still implemented in the destination module at the same relative path or whether it must be restored explicitly.
  - Likely destination: `unknown`

## File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0001`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/transaction-pool/src/pool/async_pool_removal_tests.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0532: crates/transaction-pool/src/pool/mod.rs

- Key: `file_index=532`, `source_path=crates/transaction-pool/src/pool/mod.rs`, `record_id=file-0532-atom-0001`
  - Source hunk: `@@ -73,0 +74,2 @@ use crate::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/mod.rs`

## File 0535: crates/transaction-pool/src/pool/scheduled.rs

- Key: `file_index=535`, `source_path=crates/transaction-pool/src/pool/scheduled.rs`, `record_id=file-0535-atom-0001`
  - Source hunk: `@@ -0,0 +1,154 @@`
  - Human question: Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0001`
  - Source hunk: `@@ -12,0 +13 @@ use crate::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/txpool.rs`

## File 0538: crates/transaction-pool/src/test_utils/gen.rs

- Key: `file_index=538`, `source_path=crates/transaction-pool/src/test_utils/gen.rs`, `record_id=file-0538-atom-0001`
  - Source hunk: `@@ -154,0 +155,3 @@ impl TransactionBuilder {`
  - Required change: Restore or intentionally replace the downstream behavior carried by crates/transaction-pool/src/test_utils/gen.rs; no reliable destination evidence was found in the configured search scope.
  - Likely destination: `unknown`

## File 0539: crates/transaction-pool/src/test_utils/mock.rs

- Key: `file_index=539`, `source_path=crates/transaction-pool/src/test_utils/mock.rs`, `record_id=file-0539-atom-0001`
  - Source hunk: `@@ -15 +15 @@ use alloy_consensus::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/test_utils/mock.rs`

## File 0540: crates/transaction-pool/src/traits.rs

- Key: `file_index=540`, `source_path=crates/transaction-pool/src/traits.rs`, `record_id=file-0540-atom-0001`
  - Source hunk: `@@ -5,2 +5,3 @@ use crate::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/traits.rs`

## File 0541: crates/transaction-pool/src/validate/constants.rs

- Key: `file_index=541`, `source_path=crates/transaction-pool/src/validate/constants.rs`, `record_id=file-0541-atom-0001`
  - Source hunk: `@@ -10,3 +10,4 @@ pub const TX_SLOT_BYTE_SIZE: usize = 32 * 1024;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/validate/constants.rs`

## File 0542: crates/transaction-pool/src/validate/eth.rs

- Key: `file_index=542`, `source_path=crates/transaction-pool/src/validate/eth.rs`, `record_id=file-0542-atom-0001`
  - Source hunk: `@@ -17,2 +17,2 @@ use alloy_consensus::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/validate/eth.rs`

## File 0543: crates/transaction-pool/src/validate/mod.rs

- Key: `file_index=543`, `source_path=crates/transaction-pool/src/validate/mod.rs`, `record_id=file-0543-atom-0001`
  - Source hunk: `@@ -275,0 +276,54 @@ impl<T: PoolTransaction> ValidPoolTransaction<T> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/validate/mod.rs`

## File 0546: crates/trie/common/Cargo.toml

- Key: `file_index=546`, `source_path=crates/trie/common/Cargo.toml`, `record_id=file-0546-atom-0001`
  - Source hunk: `@@ -45,0 +46 @@ rayon = { workspace = true, optional = true }`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/trie/common/Cargo.toml`

## File 0550: crates/trie/common/src/proofs.rs

- Key: `file_index=550`, `source_path=crates/trie/common/src/proofs.rs`, `record_id=file-0550-atom-0001`
  - Source hunk: `@@ -182,4 +182,4 @@ impl MultiProof {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/trie/common/src/proofs.rs`

## File 0552: crates/trie/db/tests/witness.rs

- Key: `file_index=552`, `source_path=crates/trie/db/tests/witness.rs`, `record_id=file-0552-atom-0001`
  - Source hunk: `@@ -92,10 +92,6 @@ fn includes_nodes_for_destroyed_storage_nodes() {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/trie/db/tests/witness.rs`

## File 0555: crates/trie/sparse/src/trie.rs

- Key: `file_index=555`, `source_path=crates/trie/sparse/src/trie.rs`, `record_id=file-0555-atom-0001`
  - Source hunk: `@@ -398 +398 @@ impl<P> RevealedSparseTrie<P> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/trie/sparse/src/trie.rs`

## File 0557: crates/trie/trie/src/node_iter.rs

- Key: `file_index=557`, `source_path=crates/trie/trie/src/node_iter.rs`, `record_id=file-0557-atom-0001`
  - Source hunk: `@@ -186 +186 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/trie/trie/src/node_iter.rs`

## File 0559: crates/trie/trie/src/trie.rs

- Key: `file_index=559`, `source_path=crates/trie/trie/src/trie.rs`, `record_id=file-0559-atom-0001`
  - Source hunk: `@@ -232,3 +232,3 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/trie/trie/src/trie.rs`

## File 0561: crates/trie/trie/src/walker.rs

- Key: `file_index=561`, `source_path=crates/trie/trie/src/walker.rs`, `record_id=file-0561-atom-0001`
  - Source hunk: `@@ -205 +205 @@ impl<C: TrieCursor> TrieWalker<C> {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/trie/trie/src/walker.rs`

## Test-Derived Atom Insertions (Curated 2026-05-08)

These entries were appended by the curated test-atom insertion pass. They group behavior-bearing downstream tests and omit helper/no-assert/default-only noise.

### File 0088: crates/ethereum/payload/src/bundle.rs

- Key: `file_index=88`, `source_path=crates/ethereum/payload/src/bundle.rs`, `record_id=file-0088-atom-0002`
  - Source hunk: `@@ -0,0 +1,194 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: tx source preserves the production behavior asserted by downstream tests: test_tx_source_equality.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/bundle.rs`
  - Grouped tests: `test_tx_source_equality`

### File 0089: crates/ethereum/payload/src/collector.rs

- Key: `file_index=89`, `source_path=crates/ethereum/payload/src/collector.rs`, `record_id=file-0089-atom-0002`
  - Source hunk: `@@ -0,0 +1,124 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: can fit preserves the production behavior asserted by downstream tests: test_can_fit_transaction.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/collector.rs`
  - Grouped tests: `test_can_fit_transaction`

### File 0090: crates/ethereum/payload/src/config.rs

- Key: `file_index=90`, `source_path=crates/ethereum/payload/src/config.rs`, `record_id=file-0090-atom-0002`
  - Source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Payload builder config preserves the default build deadline, environment override, invalid-env fallback, and explicit override semantics.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`
  - Grouped tests: `test_default_build_deadline, test_build_deadline_from_env, test_build_deadline_invalid_env_falls_back, test_with_build_deadline_override, test_gas_limit_calculation`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0002`
  - Source hunk: `@@ -194,132 +1255,5106 @@ where`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Payload async simulation slot allocation preserves regular-lane anti-starvation, total-cap clamping, zero-cap disabling, and leftover redistribution across scheduled and regular candidates.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Grouped tests: `fix_for_current_incident_regular_gets_at_least_its_cap, lots_of_scheduled_no_regular_uses_full_total_for_scheduled, lots_of_regular_no_scheduled_uses_full_total_for_regular, both_under_their_caps_no_truncation, both_at_cap_truncates_scheduled_first, empty_pool, category_caps_above_total_are_clamped, zero_regular_cap_disables_regular_lane, zero_scheduled_cap_disables_scheduled_lane, leftover_after_regular_fills_into_scheduled`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0003`
  - Source hunk: `@@ -194,132 +1255,5106 @@ where`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: SPC verification accepts valid preloaded-context signatures and rejects wrong outputs, mismatched input hashes, or empty executor keys.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Grouped tests: `test_verify_spc_valid_signature_passes, test_verify_spc_wrong_output_fails, test_verify_spc_wrong_input_hash_fails, test_verify_spc_empty_executor_key_fails`

### File 0093: crates/ethereum/payload/src/unified_builder.rs

- Key: `file_index=93`, `source_path=crates/ethereum/payload/src/unified_builder.rs`, `record_id=file-0093-atom-0002`
  - Source hunk: `@@ -0,0 +1,341 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: can fit preserves the production behavior asserted by downstream tests: test_can_fit_in_block, test_extract_delivery_tip_short_input.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/unified_builder.rs`
  - Grouped tests: `test_can_fit_in_block, test_extract_delivery_tip_short_input`

### File 0106: crates/evm/src/async_context_tests.rs

- Key: `file_index=106`, `source_path=crates/evm/src/async_context_tests.rs`, `record_id=file-0106-atom-0002`
  - Source hunk: `@@ -0,0 +1,99 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Async EVM context preserves default building mode, execution-mode switching, SPC call index progression, pending SPC calls, and execution-result storage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/evm/src/async_context_tests.rs`
  - Grouped tests: `test_async_context_default_values, test_async_context_execution_mode_setting, test_async_context_execution_results, test_async_context_spc_call_index, test_async_context_pending_spc_calls`

### File 0274: crates/ritual-async-commitment-validator/src/lib.rs

- Key: `file_index=274`, `source_path=crates/ritual-async-commitment-validator/src/lib.rs`, `record_id=file-0274-atom-0002`
  - Source hunk: `@@ -0,0 +1,576 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Async commitment validation accepts only valid TTL, precompile, and executor structure and rejects TTL=0, TTL>max, invalid precompile addresses, and zero executors.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`
  - Grouped tests: `test_c_ac_1_ttl_zero_rejected, test_c_ac_1_ttl_one_accepted, test_c_ac_2_ttl_max_accepted, test_c_ac_2_ttl_exceeds_max_rejected, test_c_ac_3_valid_precompiles, test_c_ac_3_invalid_precompile_rejected, test_c_ac_4_zero_executor_rejected, test_c_ac_4_nonzero_executor_accepted, prop_zero_executor_always_rejected, prop_invalid_ttl_always_rejected`

### File 0278: crates/ritual-async-fees/src/gas.rs

- Key: `file_index=278`, `source_path=crates/ritual-async-fees/src/gas.rs`, `record_id=file-0278-atom-0002`
  - Source hunk: `@@ -0,0 +1,198 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: calculate calldata gas preserves the fee/gas/accounting behavior covered by downstream tests: test_calculate_calldata_gas_empty, test_calculate_calldata_gas_zeros, test_calculate_calldata_gas_non_zeros, test_calculate_calldata_gas_mixed.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`
  - Grouped tests: `test_calculate_calldata_gas_empty, test_calculate_calldata_gas_zeros, test_calculate_calldata_gas_non_zeros, test_calculate_calldata_gas_mixed, test_calculate_calldata_gas_overflow_protection`

### File 0278: crates/ritual-async-fees/src/gas.rs

- Key: `file_index=278`, `source_path=crates/ritual-async-fees/src/gas.rs`, `record_id=file-0278-atom-0003`
  - Source hunk: `@@ -0,0 +1,198 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: effective gas limit for block preserves the fee/gas/accounting behavior covered by downstream tests: test_is_system_transaction, test_effective_gas_limit_for_block_commitment_tx, test_effective_gas_limit_for_block_settlement_tx, test_effective_gas_limit_for_block_scheduled_tx.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`
  - Grouped tests: `test_is_system_transaction, test_effective_gas_limit_for_block_commitment_tx, test_effective_gas_limit_for_block_settlement_tx, test_effective_gas_limit_for_block_scheduled_tx, test_effective_gas_limit_for_block_regular_tx`

### File 0279: crates/ritual-async-fees/src/http.rs

- Key: `file_index=279`, `source_path=crates/ritual-async-fees/src/http.rs`, `record_id=file-0279-atom-0002`
  - Source hunk: `@@ -0,0 +1,44 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: http executor fee preserves the fee/gas/accounting behavior covered by downstream tests: test_http_executor_fee_zero_output, test_http_executor_fee_with_output.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/http.rs`
  - Grouped tests: `test_http_executor_fee_zero_output, test_http_executor_fee_with_output`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0002`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: delivery has error preserves the fee/gas/accounting behavior covered by downstream tests: test_delivery_has_error_true, test_delivery_has_error_false, test_delivery_has_error_none, test_delivery_has_error_too_short.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Grouped tests: `test_delivery_has_error_true, test_delivery_has_error_false, test_delivery_has_error_none, test_delivery_has_error_too_short, test_da_error_fees_phase2_constant, test_da_error_fee_less_than_phase1_escrow, test_delivery_has_error_realistic_image_error`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0003`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: dkms preserves the fee/gas/accounting behavior covered by downstream tests: test_dkms_explicit_pricing, test_dkms_executor_fee_is_fixed, test_unknown_precompile_fails_explicitly.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Grouped tests: `test_dkms_explicit_pricing, test_dkms_executor_fee_is_fixed, test_unknown_precompile_fails_explicitly`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0004`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract ux preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_extract_ux_params_too_short_fails, test_extract_ux_params_dynamic_output, test_extract_ux_params_out_of_bounds_fails.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Grouped tests: `test_extract_ux_params_too_short_fails, test_extract_ux_params_dynamic_output, test_extract_ux_params_out_of_bounds_fails`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0005`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fee preserves the fee/gas/accounting behavior covered by downstream tests: test_model_info_image, test_image_steps_multiplier_applies, test_video_steps_fps_multiplier_applies.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Grouped tests: `test_model_info_image, test_image_steps_multiplier_applies, test_video_steps_fps_multiplier_applies`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0006`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fees preserves the fee/gas/accounting behavior covered by downstream tests: test_fees_total_calculation, test_llm_fees_fail_without_output.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Grouped tests: `test_fees_total_calculation, test_llm_fees_fail_without_output`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0007`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: pricing preserves the fee/gas/accounting behavior covered by downstream tests: test_extract_ux_params_legacy_fails.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Grouped tests: `test_extract_ux_params_legacy_fails`

### File 0281: crates/ritual-async-fees/src/llm.rs

- Key: `file_index=281`, `source_path=crates/ritual-async-fees/src/llm.rs`, `record_id=file-0281-atom-0002`
  - Source hunk: `@@ -0,0 +1,941 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: llm has error preserves the production behavior asserted by downstream tests: test_llm_has_error_returns_constant_fee, test_llm_has_error_prefix_constant_used_in_decode.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/llm.rs`
  - Grouped tests: `test_llm_has_error_returns_constant_fee, test_llm_has_error_prefix_constant_used_in_decode`

### File 0282: crates/ritual-async-fees/src/registry.rs

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0002`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: compute string mapping slot preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_model_exists_valid_config, test_model_not_found, test_compute_string_mapping_slot.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`
  - Grouped tests: `test_model_exists_valid_config, test_model_not_found, test_compute_string_mapping_slot`

### File 0282: crates/ritual-async-fees/src/registry.rs

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0003`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fee preserves the fee/gas/accounting behavior covered by downstream tests: test_audio_pricing_partial_config_rejected, test_video_pricing_partial_config_rejected, test_fully_configured_image_model_valid.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`
  - Grouped tests: `test_audio_pricing_partial_config_rejected, test_video_pricing_partial_config_rejected, test_fully_configured_image_model_valid`

### File 0282: crates/ritual-async-fees/src/registry.rs

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0004`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: model config preserves the production behavior asserted by downstream tests: test_contract_not_deployed, test_invalid_model_config_params_b_zero, test_invalid_model_config_theta_zero.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`
  - Grouped tests: `test_contract_not_deployed, test_invalid_model_config_params_b_zero, test_invalid_model_config_theta_zero`

### File 0282: crates/ritual-async-fees/src/registry.rs

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0005`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: pricing preserves the fee/gas/accounting behavior covered by downstream tests: test_text_only_model_no_multimodal_pricing_valid.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`
  - Grouped tests: `test_text_only_model_no_multimodal_pricing_valid`

### File 0282: crates/ritual-async-fees/src/registry.rs

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0006`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: u256 to f64 preserves the production behavior asserted by downstream tests: test_u256_to_f64_scaled, test_u256_to_f64_scaled_overflow.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`
  - Grouped tests: `test_u256_to_f64_scaled, test_u256_to_f64_scaled_overflow`

### File 0283: crates/ritual-async-fees/src/scheduled.rs

- Key: `file_index=283`, `source_path=crates/ritual-async-fees/src/scheduled.rs`, `record_id=file-0283-atom-0002`
  - Source hunk: `@@ -0,0 +1,373 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract callback gas preserves the fee/gas/accounting behavior covered by downstream tests: test_extract_callback_gas_success, test_extract_callback_gas_wrong_address, test_extract_callback_gas_empty_logs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/scheduled.rs`
  - Grouped tests: `test_extract_callback_gas_success, test_extract_callback_gas_wrong_address, test_extract_callback_gas_empty_logs`

### File 0283: crates/ritual-async-fees/src/scheduled.rs

- Key: `file_index=283`, `source_path=crates/ritual-async-fees/src/scheduled.rs`, `record_id=file-0283-atom-0003`
  - Source hunk: `@@ -0,0 +1,373 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: get callback gas or fallback preserves the fee/gas/accounting behavior covered by downstream tests: test_get_callback_gas_or_fallback_success, test_get_callback_gas_or_fallback_failed, test_get_callback_gas_or_fallback_not_found.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/scheduled.rs`
  - Grouped tests: `test_get_callback_gas_or_fallback_success, test_get_callback_gas_or_fallback_failed, test_get_callback_gas_or_fallback_not_found`

### File 0284: crates/ritual-async-fees/src/validators.rs

- Key: `file_index=284`, `source_path=crates/ritual-async-fees/src/validators.rs`, `record_id=file-0284-atom-0002`
  - Source hunk: `@@ -0,0 +1,106 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fee preserves the fee/gas/accounting behavior covered by downstream tests: test_commitment_fee_scales_with_data_size, test_zero_input_commitment_fee, test_inclusion_fee_always_zero.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/validators.rs`
  - Grouped tests: `test_commitment_fee_scales_with_data_size, test_zero_input_commitment_fee, test_inclusion_fee_always_zero`

### File 0284: crates/ritual-async-fees/src/validators.rs

- Key: `file_index=284`, `source_path=crates/ritual-async-fees/src/validators.rs`, `record_id=file-0284-atom-0003`
  - Source hunk: `@@ -0,0 +1,106 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fees preserves the fee/gas/accounting behavior covered by downstream tests: test_async_commitment_fee, test_async_inclusion_fee_is_zero.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/validators.rs`
  - Grouped tests: `test_async_commitment_fee, test_async_inclusion_fee_is_zero`

### File 0295: crates/ritual-async/src/detector.rs

- Key: `file_index=295`, `source_path=crates/ritual-async/src/detector.rs`, `record_id=file-0295-atom-0002`
  - Source hunk: `@@ -0,0 +1,1546 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract precompile data preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_extract_precompile_data_valid, test_extract_precompile_data_invalid_data, test_extract_precompile_data_empty_data, test_extract_precompile_data_ttl_too_large.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/detector.rs`
  - Grouped tests: `test_extract_precompile_data_valid, test_extract_precompile_data_invalid_data, test_extract_precompile_data_empty_data, test_extract_precompile_data_ttl_too_large`

### File 0297: crates/ritual-async/src/validation.rs

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0002`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fuzz ttl preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: fuzz_ttl_bounds.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/validation.rs`
  - Grouped tests: `fuzz_ttl_bounds`

### File 0297: crates/ritual-async/src/validation.rs

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0003`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: try decode preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_try_decode_persistent_agent_uses_full_codec.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/validation.rs`
  - Grouped tests: `test_try_decode_persistent_agent_uses_full_codec`

### File 0297: crates/ritual-async/src/validation.rs

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0004`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: two phase deadline preserves the production behavior asserted by downstream tests: test_extract_two_phase_deadline_persistent_agent, test_extract_two_phase_deadline_persistent_agent_short_input, test_validate_two_phase_deadline_valid, test_validate_two_phase_deadline_insufficient, test_validate_two_phase_deadline_equal.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/validation.rs`
  - Grouped tests: `test_extract_two_phase_deadline_persistent_agent, test_extract_two_phase_deadline_persistent_agent_short_input, test_validate_two_phase_deadline_valid, test_validate_two_phase_deadline_insufficient, test_validate_two_phase_deadline_equal, fuzz_validate_two_phase_deadline_property`

### File 0297: crates/ritual-async/src/validation.rs

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0005`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: user public key preserves the production behavior asserted by downstream tests: test_try_decode_sovereign_agent_uses_full_codec.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/validation.rs`
  - Grouped tests: `test_try_decode_sovereign_agent_uses_full_codec`

### File 0297: crates/ritual-async/src/validation.rs

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0006`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: validate async payload preserves the production behavior asserted by downstream tests: test_validate_http_payload_valid, test_validate_http_payload_ttl_zero, test_validate_http_payload_ttl_exceeded, test_validate_http_payload_empty_url, test_validate_http_payload_invalid_scheme.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/validation.rs`
  - Grouped tests: `test_validate_http_payload_valid, test_validate_http_payload_ttl_zero, test_validate_http_payload_ttl_exceeded, test_validate_http_payload_empty_url, test_validate_http_payload_invalid_scheme, test_validate_llm_payload_valid, test_validate_llm_payload_empty_model, test_validate_llm_payload_empty_messages, test_validate_persistent_agent_payload_valid, test_validate_persistent_agent_payload_zero_executor`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0002`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: classification preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: prop_metrics_agent_deterministic, test_validation_errors_are_classified_as_validation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_metrics_agent_deterministic, test_validation_errors_are_classified_as_validation`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0003`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: commitment passes preserves the production behavior asserted by downstream tests: prop_valid_commitment_passes_both.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_valid_commitment_passes_both`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0004`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Async commitment validation accepts only valid TTL, precompile, and executor structure and rejects TTL=0, TTL>max, invalid precompile addresses, and zero executors.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_ttl_large_value_rejected`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0005`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: diff eq preserves the production behavior asserted by downstream tests: diff_eq_ttl_zero_rejected, diff_eq_ttl_one_accepted, diff_eq_ttl_max_accepted, diff_eq_ttl_exceeds_max_rejected, diff_eq_executor_zero_rejected.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_ttl_zero_rejected, diff_eq_ttl_one_accepted, diff_eq_ttl_max_accepted, diff_eq_ttl_exceeds_max_rejected, diff_eq_executor_zero_rejected, diff_eq_executor_nonzero_accepted, diff_eq_executor_one_byte_accepted, diff_eq_settlement_expiry_equal, diff_eq_settlement_expiry_before, diff_eq_settlement_expiry_after`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0006`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: error class preserves the production behavior asserted by downstream tests: test_error_class_system_vs_block_local.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `test_error_class_system_vs_block_local`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0007`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: executor equivalence preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: prop_executor_equivalence.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_executor_equivalence`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0008`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract phase2 deadline preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_is_two_phase_precompile, test_extract_phase2_deadline_valid_input, test_extract_phase2_deadline_input_too_short, test_extract_phase2_deadline_various_values.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `test_is_two_phase_precompile, test_extract_phase2_deadline_valid_input, test_extract_phase2_deadline_input_too_short, test_extract_phase2_deadline_various_values, test_extract_phase2_deadline_sovereign_agent_reads_field_4, test_extract_phase2_deadline_sovereign_agent_input_too_short, test_extract_phase2_deadline_persistent_agent_reads_field_5, test_extract_phase2_deadline_fhe_reads_field_10, test_extract_phase2_deadline_fhe_input_too_short, test_extract_phase2_deadline_fhe_various_values`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0009`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fee preserves the fee/gas/accounting behavior covered by downstream tests: prop_spc_proof_length_equivalence.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_spc_proof_length_equivalence`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0010`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fees preserves the fee/gas/accounting behavior covered by downstream tests: diff_eq_fee_agent_phase2_deterministic, prop_fee_agent_phase2_deterministic.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_fee_agent_phase2_deterministic, prop_fee_agent_phase2_deterministic`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0011`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: filter  preserves scheduled-transaction obligation/filtering behavior covered by downstream tests: prop_nonce_lock_deterministic.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_nonce_lock_deterministic`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0012`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: http executor fee preserves the fee/gas/accounting behavior covered by downstream tests: diff_eq_fee_http_helpers_deterministic.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_fee_http_helpers_deterministic`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0013`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: metrics delivery preserves the production behavior asserted by downstream tests: prop_metrics_delivery_deterministic.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_metrics_delivery_deterministic`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0014`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: onnx unavailable preserves the production behavior asserted by downstream tests: test_onnx_unavailable_is_validation_error.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `test_onnx_unavailable_is_validation_error`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0015`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: phase2 preserves the production behavior asserted by downstream tests: diff_eq_phase2_deadline_valid, diff_eq_phase2_deadline_invalid_equal, diff_eq_phase2_deadline_invalid_less, diff_eq_phase2_deadline_boundary, prop_phase2_deadline_equivalence.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_phase2_deadline_valid, diff_eq_phase2_deadline_invalid_equal, diff_eq_phase2_deadline_invalid_less, diff_eq_phase2_deadline_boundary, prop_phase2_deadline_equivalence, prop_phase2_deadline_correctness`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0016`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: priority preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_sequencing_rights_error_variants, test_empty_selectors, test_empty_ordering, diff_eq_sr_contract_creation_no_sr.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `test_sequencing_rights_error_variants, test_empty_selectors, test_empty_ordering, diff_eq_sr_contract_creation_no_sr, diff_eq_sr_ascending_order_passes, diff_eq_sr_descending_order_fails, diff_eq_sr_same_priority_passes`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0017`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: proof preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: diff_eq_spc_valid_proof_length, diff_eq_spc_short_proof_rejected, diff_eq_spc_multiple_calls_rejected.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_spc_valid_proof_length, diff_eq_spc_short_proof_rejected, diff_eq_spc_multiple_calls_rejected`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0018`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduled transaction verification preserves C10 validation behavior and the matching filter/result classification asserted by downstream tests.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_scheduled_c10_duplicate, prop_scheduled_c10_deterministic`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0019`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduled transaction verification preserves C11 validation behavior and the matching filter/result classification asserted by downstream tests.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_scheduled_c11_predicate_true, diff_eq_scheduled_c11_predicate_false_is_byzantine, diff_eq_scheduled_c11_default_predicate, diff_eq_scheduled_c11_predicate_revert_is_byzantine, diff_eq_scheduled_c11_predicate_halt_is_byzantine, prop_scheduled_c11_equivalence, prop_scheduled_c11_default_always_true`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0020`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduled transaction verification preserves C3 validation behavior and the matching filter/result classification asserted by downstream tests.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_scheduled_c3_out_of_bounds, diff_eq_scheduled_c3_valid_index, prop_scheduled_c3_equivalence`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0021`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduled transaction verification preserves C4 validation behavior and the matching filter/result classification asserted by downstream tests.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_scheduled_c4_too_early, diff_eq_scheduled_c4_at_expected, prop_scheduled_c4_equivalence`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0022`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduled transaction verification preserves C5 validation behavior and the matching filter/result classification asserted by downstream tests.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_scheduled_c5_too_late, diff_eq_scheduled_c5_at_deadline, prop_scheduled_c5_equivalence`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0023`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduled transaction verification preserves C6 validation behavior and the matching filter/result classification asserted by downstream tests.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_scheduled_c6_expired, prop_scheduled_c6_equivalence`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0024`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: selector preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: diff_eq_sr_empty_input_no_sr, diff_eq_metrics_delivery_result_len_valid, diff_eq_metrics_delivery_result_len_short, diff_eq_metrics_agent_short_input.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `diff_eq_sr_empty_input_no_sr, diff_eq_metrics_delivery_result_len_valid, diff_eq_metrics_delivery_result_len_short, diff_eq_metrics_agent_short_input`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0025`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: sender dedup preserves the production behavior asserted by downstream tests: prop_sender_dedup_deterministic.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_sender_dedup_deterministic`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0026`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: sequencing rights preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_classification_variants, test_sequencing_rights_reader.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `test_classification_variants, test_sequencing_rights_reader`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0027`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: settlement expiry preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: prop_settlement_expiry_equivalence, prop_settlement_expiry_correctness.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_settlement_expiry_equivalence, prop_settlement_expiry_correctness`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0028`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: ttl equivalence preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: prop_ttl_equivalence.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Grouped tests: `prop_ttl_equivalence`

### File 0320: crates/ritual-precompile-codecs/src/executor.rs

- Key: `file_index=320`, `source_path=crates/ritual-precompile-codecs/src/executor.rs`, `record_id=file-0320-atom-0002`
  - Source hunk: `@@ -0,0 +1,260 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: encrypted secrets preserves the production behavior asserted by downstream tests: test_decode_base_fields_success, test_decode_base_fields_too_short, test_from_base_fields.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/executor.rs`
  - Grouped tests: `test_decode_base_fields_success, test_decode_base_fields_too_short, test_from_base_fields`

### File 0321: crates/ritual-precompile-codecs/src/http_call.rs

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0002`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: encrypted secrets preserves the production behavior asserted by downstream tests: test_extract_executor_and_ttl, test_from_abi_success, test_http_method_conversion, test_header_length_mismatch.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`
  - Grouped tests: `test_extract_executor_and_ttl, test_from_abi_success, test_http_method_conversion, test_header_length_mismatch`

### File 0321: crates/ritual-precompile-codecs/src/http_call.rs

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0003`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract executor preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_extract_executor_success.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`
  - Grouped tests: `test_extract_executor_success`

### File 0321: crates/ritual-precompile-codecs/src/http_call.rs

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0004`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract ttl preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_extract_ttl_success, test_extract_ttl_different_values, test_extract_ttl_invalid_data.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`
  - Grouped tests: `test_extract_ttl_success, test_extract_ttl_different_values, test_extract_ttl_invalid_data`

### File 0323: crates/ritual-precompile-codecs/src/llm_call.rs

- Key: `file_index=323`, `source_path=crates/ritual-precompile-codecs/src/llm_call.rs`, `record_id=file-0323-atom-0002`
  - Source hunk: `@@ -0,0 +1,361 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: convo history preserves the production behavior asserted by downstream tests: test_convo_history_roundtrip.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`
  - Grouped tests: `test_convo_history_roundtrip`

### File 0323: crates/ritual-precompile-codecs/src/llm_call.rs

- Key: `file_index=323`, `source_path=crates/ritual-precompile-codecs/src/llm_call.rs`, `record_id=file-0323-atom-0003`
  - Source hunk: `@@ -0,0 +1,361 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: from abi preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_valid_llm_request, test_empty_model, test_empty_messages, test_malformed_abi.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`
  - Grouped tests: `test_valid_llm_request, test_empty_model, test_empty_messages, test_malformed_abi`

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0002`
  - Source hunk: `@@ -0,0 +1,1172 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fee preserves the fee/gas/accounting behavior covered by downstream tests: test_decode_delivery_config.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/long_running.rs`
  - Grouped tests: `test_decode_delivery_config`

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0002`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: delivery config preserves the production behavior asserted by downstream tests: test_delivery_config_extraction.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`
  - Grouped tests: `test_delivery_config_extraction`

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0003`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract executor preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_extract_executor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`
  - Grouped tests: `test_extract_executor`

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0004`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: extract ttl preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_extract_ttl.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`
  - Grouped tests: `test_extract_ttl`

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0005`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: from abi preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_roundtrip_request, test_get_required_secret_keys, test_response_roundtrip.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`
  - Grouped tests: `test_roundtrip_request, test_get_required_secret_keys, test_response_roundtrip`

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0006`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: response preserves the production behavior asserted by downstream tests: test_response_error, test_llm_provider_api_string.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`
  - Grouped tests: `test_response_error, test_llm_provider_api_string`

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0007`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: roundtrip request preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_roundtrip_request_with_rpc_urls.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`
  - Grouped tests: `test_roundtrip_request_with_rpc_urls`

### File 0326: crates/ritual-precompile-codecs/src/sovereign_agent.rs

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0002`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: 22 field payload preserves the production behavior asserted by downstream tests: test_22_field_payload_rejected.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`
  - Grouped tests: `test_22_field_payload_rejected`

### File 0326: crates/ritual-precompile-codecs/src/sovereign_agent.rs

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0003`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: agent type preserves the production behavior asserted by downstream tests: test_valid_sovereign_agent_request, test_sovereign_agent_type_crush_roundtrip, test_sovereign_agent_type_zeroclaw_roundtrip, test_sovereign_agent_type_invalid_boundary.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`
  - Grouped tests: `test_valid_sovereign_agent_request, test_sovereign_agent_type_crush_roundtrip, test_sovereign_agent_type_zeroclaw_roundtrip, test_sovereign_agent_type_invalid_boundary`

### File 0326: crates/ritual-precompile-codecs/src/sovereign_agent.rs

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0004`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: from abi preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_empty_prompt, test_malformed_abi.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`
  - Grouped tests: `test_empty_prompt, test_malformed_abi`

### File 0326: crates/ritual-precompile-codecs/src/sovereign_agent.rs

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0005`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: valid sovereign agent request preserves the production behavior asserted by downstream tests: test_valid_sovereign_agent_request_with_rpc_urls.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`
  - Grouped tests: `test_valid_sovereign_agent_request_with_rpc_urls`

### File 0329: crates/ritual-scheduled-block-building/src/lib.rs

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0003`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: compute obligations preserves scheduled-transaction obligation/filtering behavior covered by downstream tests: test_compute_obligations_from_pool_includes_when_wallet_funded.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`
  - Grouped tests: `test_compute_obligations_from_pool_includes_when_wallet_funded`

### File 0329: crates/ritual-scheduled-block-building/src/lib.rs

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0004`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: derive max block number preserves the production behavior asserted by downstream tests: test_derive_max_block_number_regular_values, test_derive_max_block_number_saturates_on_overflow.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`
  - Grouped tests: `test_derive_max_block_number_regular_values, test_derive_max_block_number_saturates_on_overflow`

### File 0329: crates/ritual-scheduled-block-building/src/lib.rs

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0005`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fee preserves the fee/gas/accounting behavior covered by downstream tests: test_compute_obligations_from_pool_skips_calls_above_protocol_ttl_bound, test_compute_obligations_from_pool_includes_underfunded_call_for_contract_eviction, test_compute_obligations_from_pool_skips_when_base_fee_exceeds_max_fee.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`
  - Grouped tests: `test_compute_obligations_from_pool_skips_calls_above_protocol_ttl_bound, test_compute_obligations_from_pool_includes_underfunded_call_for_contract_eviction, test_compute_obligations_from_pool_skips_when_base_fee_exceeds_max_fee`

### File 0329: crates/ritual-scheduled-block-building/src/lib.rs

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0006`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: filtering stats preserves scheduled-transaction obligation/filtering behavior covered by downstream tests: test_filtering_stats_from_results, test_filtering_stats_all_valid, test_filtering_stats_empty.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`
  - Grouped tests: `test_filtering_stats_from_results, test_filtering_stats_all_valid, test_filtering_stats_empty`

### File 0336: crates/ritual-sequencing-rights/src/bucket.rs

- Key: `file_index=336`, `source_path=crates/ritual-sequencing-rights/src/bucket.rs`, `record_id=file-0336-atom-0002`
  - Source hunk: `@@ -0,0 +1,604 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: bucket preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_bucket_sort, test_partition_reassemble, test_empty_bucket_passes_verification, test_single_tx_bucket_passes.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`
  - Grouped tests: `test_bucket_sort, test_partition_reassemble, test_empty_bucket_passes_verification, test_single_tx_bucket_passes, test_same_priority_passes, test_large_bucket_construction`

### File 0337: crates/ritual-sequencing-rights/src/classifier.rs

- Key: `file_index=337`, `source_path=crates/ritual-sequencing-rights/src/classifier.rs`, `record_id=file-0337-atom-0002`
  - Source hunk: `@@ -0,0 +1,763 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: inspector preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_inspector_single_contract, test_inspector_multi_contract, test_inspector_into_classification, test_selectors_for_contract.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`
  - Grouped tests: `test_inspector_single_contract, test_inspector_multi_contract, test_inspector_into_classification, test_selectors_for_contract, test_inspector_reset, test_exactly_4_byte_selector, test_input_boundary_cases, test_multiple_selectors_same_contract, test_duplicate_selector_calls, test_many_contracts_multi_contract_classification`

### File 0337: crates/ritual-sequencing-rights/src/classifier.rs

- Key: `file_index=337`, `source_path=crates/ritual-sequencing-rights/src/classifier.rs`, `record_id=file-0337-atom-0003`
  - Source hunk: `@@ -0,0 +1,763 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: selector preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_classification_enum_coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`
  - Grouped tests: `test_classification_enum_coverage`

### File 0340: crates/ritual-sequencing-rights/src/priority.rs

- Key: `file_index=340`, `source_path=crates/ritual-sequencing-rights/src/priority.rs`, `record_id=file-0340-atom-0002`
  - Source hunk: `@@ -0,0 +1,287 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: priority preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_exact_match, test_no_match, test_empty_ordering, test_subset_match.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/priority.rs`
  - Grouped tests: `test_exact_match, test_no_match, test_empty_ordering, test_subset_match, test_max_priority_no_overflow, test_empty_selector_set, test_empty_selector_set_empty_ordering, test_overlapping_levels, test_superset_uses_lowest_priority, test_partial_overlap`

### File 0341: crates/ritual-sequencing-rights/src/reader.rs

- Key: `file_index=341`, `source_path=crates/ritual-sequencing-rights/src/reader.rs`, `record_id=file-0341-atom-0002`
  - Source hunk: `@@ -0,0 +1,358 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: selector preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_decode_empty_ordering.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/reader.rs`
  - Grouped tests: `test_decode_empty_ordering`

### File 0342: crates/ritual-sequencing-rights/src/types.rs

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0002`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: ordering preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_sequencing_ordering_default.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`
  - Grouped tests: `test_sequencing_ordering_default`

### File 0342: crates/ritual-sequencing-rights/src/types.rs

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0003`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: priority preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_priority_ordering, test_selector_set_equality, test_sequencing_ordering_priority, prop_priority_total_ordering.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`
  - Grouped tests: `test_priority_ordering, test_selector_set_equality, test_sequencing_ordering_priority, prop_priority_total_ordering, prop_priority_consistent_with_value, prop_lowest_is_lowest, prop_priority_value_roundtrip, prop_selector_set_deterministic, prop_get_priority_deterministic, prop_get_priority_correctness`

### File 0342: crates/ritual-sequencing-rights/src/types.rs

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0004`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: selector preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_contract_interaction_new, test_sequencing_ordering_is_empty.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`
  - Grouped tests: `test_contract_interaction_new, test_sequencing_ordering_is_empty`

### File 0348: crates/ritual-spc-verification/src/client.rs

- Key: `file_index=348`, `source_path=crates/ritual-spc-verification/src/client.rs`, `record_id=file-0348-atom-0002`
  - Source hunk: `@@ -0,0 +1,180 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: client creation preserves the production behavior asserted by downstream tests: test_client_creation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-spc-verification/src/client.rs`
  - Grouped tests: `test_client_creation`

### File 0348: crates/ritual-spc-verification/src/client.rs

- Key: `file_index=348`, `source_path=crates/ritual-spc-verification/src/client.rs`, `record_id=file-0348-atom-0003`
  - Source hunk: `@@ -0,0 +1,180 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: verification url preserves the production behavior asserted by downstream tests: test_verification_url_construction.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-spc-verification/src/client.rs`
  - Grouped tests: `test_verification_url_construction`

### File 0352: crates/ritual-spc-verification/src/verifier.rs

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0002`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: batch verification preserves the production behavior asserted by downstream tests: test_batch_verification_empty, test_batch_verification_single, test_batch_verification_multiple, test_batch_verification_request_creation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-spc-verification/src/verifier.rs`
  - Grouped tests: `test_batch_verification_empty, test_batch_verification_single, test_batch_verification_multiple, test_batch_verification_request_creation`

### File 0352: crates/ritual-spc-verification/src/verifier.rs

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0003`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: verifier creation preserves the production behavior asserted by downstream tests: test_verifier_creation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-spc-verification/src/verifier.rs`
  - Grouped tests: `test_verifier_creation`

### File 0352: crates/ritual-spc-verification/src/verifier.rs

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0004`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: verify parallel preserves the production behavior asserted by downstream tests: test_verify_parallel.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-spc-verification/src/verifier.rs`
  - Grouped tests: `test_verify_parallel`

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0002`
  - Source hunk: `@@ -0,0 +1,550 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: validate async payload preserves the production behavior asserted by downstream tests: test_valid_http_request, test_ttl_zero, test_ttl_exceeded, test_zero_executor, test_empty_url.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`
  - Grouped tests: `test_valid_http_request, test_ttl_zero, test_ttl_exceeded, test_zero_executor, test_empty_url, test_invalid_url_scheme, test_malformed_abi, test_input_too_large`

### File 0422: crates/scheduling/src/transaction.rs

- Key: `file_index=422`, `source_path=crates/scheduling/src/transaction.rs`, `record_id=file-0422-atom-0002`
  - Source hunk: `@@ -0,0 +1,212 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fee preserves the fee/gas/accounting behavior covered by downstream tests: test_create_scheduled_transaction_rejects_max_fee_per_gas_overflow, test_create_scheduled_transaction_rejects_max_priority_fee_overflow.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/transaction.rs`
  - Grouped tests: `test_create_scheduled_transaction_rejects_max_fee_per_gas_overflow, test_create_scheduled_transaction_rejects_max_priority_fee_overflow`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0002`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fire at preserves the production behavior asserted by downstream tests: test_fire_at_exact_target_blocks_frequency_5.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_fire_at_exact_target_blocks_frequency_5`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0003`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fire before preserves the production behavior asserted by downstream tests: test_fire_before_start_block.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_fire_before_start_block`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0004`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fire edge preserves the production behavior asserted by downstream tests: test_fire_edge_case_examples_from_plan.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_fire_edge_case_examples_from_plan`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0005`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fire frequency preserves the production behavior asserted by downstream tests: test_fire_frequency_1.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_fire_frequency_1`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0006`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fire large preserves the production behavior asserted by downstream tests: test_fire_large_frequency.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_fire_large_frequency`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0007`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fire not preserves the production behavior asserted by downstream tests: test_fire_not_at_intermediate_blocks.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_fire_not_at_intermediate_blocks`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0008`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: fire num preserves the production behavior asserted by downstream tests: test_fire_num_calls_1.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_fire_num_calls_1`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0009`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: replace calls preserves the production behavior asserted by downstream tests: test_replace_calls_replaces_non_empty_state.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_replace_calls_replaces_non_empty_state`

### File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0010`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: startup hydration preserves the production behavior asserted by downstream tests: test_startup_hydration_gate_runs_once, test_startup_hydration_abort_resets_gate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`
  - Grouped tests: `test_startup_hydration_gate_runs_once, test_startup_hydration_abort_resets_gate`

### File 0468: crates/storage/codecs/src/alloy/transaction/spc_call.rs

- Key: `file_index=468`, `source_path=crates/storage/codecs/src/alloy/transaction/spc_call.rs`, `record_id=file-0468-atom-0002`
  - Source hunk: `@@ -0,0 +1,349 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: proof preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_spc_call_compact_roundtrip, test_spc_call_compact_empty_bytes, test_spc_call_compact_large_bytes, test_spc_call_wrapper_roundtrip.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/spc_call.rs`
  - Grouped tests: `test_spc_call_compact_roundtrip, test_spc_call_compact_empty_bytes, test_spc_call_compact_large_bytes, test_spc_call_wrapper_roundtrip`

### File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0002`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: expiry always preserves scheduled-transaction obligation/filtering behavior covered by downstream tests: test_expiry_always_set_at_add_time.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`
  - Grouped tests: `test_expiry_always_set_at_add_time`

### File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0003`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: expiry boundary preserves scheduled-transaction obligation/filtering behavior covered by downstream tests: test_expiry_boundary_conditions.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`
  - Grouped tests: `test_expiry_boundary_conditions`

### File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0004`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: expiry check preserves scheduled-transaction obligation/filtering behavior covered by downstream tests: test_expiry_check_not_expired.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`
  - Grouped tests: `test_expiry_check_not_expired`

### File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0005`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: ordering preserves sequencing-rights classification, priority, bucket, or ordering behavior covered by downstream tests: test_concurrent_async_transaction_operations, test_extract_original_tx_hash_error_handling.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`
  - Grouped tests: `test_concurrent_async_transaction_operations, test_extract_original_tx_hash_error_handling`

### File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0006`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: phase2 preserves the production behavior asserted by downstream tests: test_phase2_ttl_uses_max_poll_block, test_phase2_ttl_extends_beyond_original, test_mark_awaiting_delivery_updates_expiry.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`
  - Grouped tests: `test_phase2_ttl_uses_max_poll_block, test_phase2_ttl_extends_beyond_original, test_mark_awaiting_delivery_updates_expiry`

### File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0007`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: ttl overflow preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_ttl_overflow_protection.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`
  - Grouped tests: `test_ttl_overflow_protection`

### File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0008`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: Verify and restore this grouped test-derived invariant in the v2.2 port, or provide precise destination evidence and update the mapping: zero ttl preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_zero_ttl_expiry.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`
  - Grouped tests: `test_zero_ttl_expiry`

## Feature-Preservation Atom Insertions (Curated 2026-05-08)

These entries were appended from `feature-preservation-map.md` after pruning validation-only, broad inventory, and already-covered claims.

### File 0026: crates/chainspec/src/api.rs

- Key: `file_index=26`, `source_path=crates/chainspec/src/api.rs`, `record_id=file-0026-atom-0002`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Environment-gated consensus constants only where already shipped.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/chainspec/src/api.rs`
  - Feature source IDs: `feature-raw-0103`

### File 0028: crates/chainspec/src/spec.rs

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0006`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Preserve unbounded/dynamic Ritual `extra_data`, CL-provided extra data, Summit deposit topic, and max-extra-data validation (`#249`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/chainspec/src/spec.rs`
  - Feature source IDs: `feature-raw-0106`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0004`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve strict fee behavior: shared async fee crate and no fallback on HTTP/LLM/pricing failures (`#146`), model-registry pricing and fail-closed builder/verifier/wallet reads (`#252`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0116`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0005`
  - Source hunk: `feature-preservation-map.md section 11: Observability And Agent Guardrails`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 11 (Observability And Agent Guardrails) preserves observability: Preserve early metrics: verification-end fields, payload/verification phase metrics, scheduler event visibility (`3393e7a3`, `#97`); Preserve structured block telemetry: block/tx phase logs, per-tx payload execution logs, payload attempt IDs/kinds, empty-payload fallback tracing, node/basic payload integration (`#325`, `#329`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0128, feature-raw-0129`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0006`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 2 (Async Precompile Detection And Validation) preserves parent state detection: Builder/verifier simulate against parent block state for deterministic async detection; Port authority model: RPC provides early feedback (`#204`, `#231`, `#307`), while builder/verifier re-simulate async origin txs and hard-fail invalid commitments (`#145`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0011, feature-raw-0016`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0007`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 2 (Async Precompile Detection And Validation) preserves payload validation: Shared payload validation rejects bad TTL, oversized inputs, malformed ECIES/user keys, bad URLs/models/messages, invalid two-phase deadlines, and unsupported agent types; Preserve validation hardening: centralized invalid-payload errors (`#231`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0013, feature-raw-0019`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0008`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: TEE registry, model registry, and wallet lock checks must stay aligned with builder/verifier assumptions.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0014`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0009`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve validation hardening: async input/calldata caps and builder/verifier obligation consistency (`#292`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0021`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0010`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Pool manager / EVM integration remains available to nodebuilder and payload code.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0027`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0011`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve duplicate/nonce behavior: active AsyncJobTracker duplicates block builder/verifier commitments and prune stale pool entries (`#260`, `#268`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0048`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0012`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 6 (Payload Building) preserves payload construction: Async detection and commitment insertion; Preserve DoS policy: build deadline default `300ms`, deadline guards, obligation/fulfilled/delivery caps, total/per-category async sim caps, regular-priority allocation, tx-count cap, local work-class demotion, near-deadline epsilon, optional-class short-circuit, and cap observations (`#292`, `#332`, `#330`, `#354`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0064, feature-raw-0074`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0013`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Fulfilled async settlement and delivery settlement inclusion.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0065`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0014`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 6 (Payload Building) preserves runtime fields hashing: Preserve active-job and Phase 2 behavior: parent-state duplicate active-job checks (`#260`, `#268`), build-time SPC reverification and metadata refresh (`#273`), Phase 2 delivery settlements and nested delivery (`#270`), atomic original+settlement size/gas precheck (`#304`); Preserve trace-facing payload metadata: payload attempt IDs/kinds, empty-payload fallback tracing, demotion capture, primary included tx count (`#329`, `#336`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0073, feature-raw-0075`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0015`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Avoid verifier-only obligation deadline logic that can diverge from builder membership (`#299`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0076`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0016`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve parity with builder: per-block async sender uniqueness and wallet locks (`#202`), shared per-block `ModelCache` (`#205`), optimized nonce-lock checks and same-block duplicate rejection (`#207`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0086`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0017`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Builder-produced blocks must replay under verifier rules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0083`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0018`
  - Source hunk: `feature-preservation-map.md section 8: RPC And Operator Surfaces`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Error messages should stay descriptive for invalid async payloads and mismatched canonical context.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0093`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0019`
  - Source hunk: `feature-preservation-map.md section 8: RPC And Operator Surfaces`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve RPC async validation behavior: precompile consumer decoding, executor capability/registration, ECIES/user keys, supported sovereign agent types `0/4/5/6`, Phase 2 offset bounds, rich invalid-payload errors (`#204`, `#231`, `#307`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0096`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0020`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Preserve eager-payload wait-with-empty-fallback behavior only if still operationally required (`#243`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0107`

### File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0021`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve payload deadline/sync policy: default `300ms`, obligation caps, async sim caps, builder/verifier policy boundary (`#282`, `#292`, `#332`), transient ONNX unavailability as retryable/`SYNCING` with bounded retry before unwind/escalation (`#298`, `#301`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`
  - Feature source IDs: `feature-raw-0109`

### File 0108: crates/evm/src/lib.rs

- Key: `file_index=108`, `source_path=crates/evm/src/lib.rs`, `record_id=file-0108-atom-0002`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Do not preserve temporary permissive verification from `#93` unless explicitly gated by skip-validity config.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/evm/src/lib.rs`
  - Feature source IDs: `feature-raw-0037`

### File 0276: crates/ritual-async-fees/src/constants.rs

- Key: `file_index=276`, `source_path=crates/ritual-async-fees/src/constants.rs`, `record_id=file-0276-atom-0002`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Wallet balance and lock-duration requirements.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/constants.rs`
  - Feature source IDs: `feature-raw-0112`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0008`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 10 (Fees, Registries, And Product Economics) preserves fees economics: Per-call min funding and spawn/day fee calibration; Preserve wallet/economics: balance and lock-duration checks, per-block async sender uniqueness (`#202`), sovereign/persistent escrow and work/spawn fee models (`#286`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Feature source IDs: `feature-raw-0114, feature-raw-0118`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0009`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 10 (Fees, Registries, And Product Economics) preserves payload validation: Preserve changed constants: ZK Phase 1 fee (`#266`), async TTL default `500` (`#265`), capability IDs `AUTONOMOUS_AGENT=11` and `TELEMETRY=12` (`#333`), persistent spawn fee `0.10 RIT` and sovereign iteration/tool fees (`#356`); Preserve multimodal/DA/error pricing: image/video steps, FPS, output extraction (`#251`), FHE output-size Phase 2 pricing (`#264`), LLM error settlement fee (`#314`), constant DA-error settlements (`#315`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Feature source IDs: `feature-raw-0119, feature-raw-0120`

### File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0010`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Settlement, delivery, and executor fee verification.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`
  - Feature source IDs: `feature-raw-0078`

### File 0292: crates/ritual-async-registry/src/lib.rs

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0009`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve registry migrations: ExecutorRegistry/SPC public key reads, workload IDs, capabilities, registry address config (`#124`, `#149`), upgraded storage slots and ERC-7201 owner caveat (`#269`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-registry/src/lib.rs`
  - Feature source IDs: `feature-raw-0117`

### File 0292: crates/ritual-async-registry/src/lib.rs

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0010`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Model registry reads and cache behavior.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-registry/src/lib.rs`
  - Feature source IDs: `feature-raw-0111`

### File 0296: crates/ritual-async/src/lib.rs

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0002`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve validation hardening: ECIES/user-key checks, supported sovereign agent types `0/4/5/6`, and Phase 2 bounds (`#307`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/lib.rs`
  - Feature source IDs: `feature-raw-0020`

### File 0296: crates/ritual-async/src/lib.rs

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0003`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve active-job semantics: contract state / AsyncJobTracker is source of truth (`#219`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/lib.rs`
  - Feature source IDs: `feature-raw-0022`

### File 0296: crates/ritual-async/src/lib.rs

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0004`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve active-job semantics: duplicate active jobs block commitments while expired jobs may be recommitted (`#260`, `#268`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/lib.rs`
  - Feature source IDs: `feature-raw-0023`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0029`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Nonce-lock validation from parent async job state.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Feature source IDs: `feature-raw-0081`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0030`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve delivery/DA verification: Phase 2 delivery settlements, `delivery_spc_calls`, nested async delivery (`#270`), DA-error Phase 2 settlement handling (`#315`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Feature source IDs: `feature-raw-0089`

### File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0031`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Summit validator deposit behavior.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-block-verification/src/verifier.rs`
  - Feature source IDs: `feature-raw-0100`

### File 0309: crates/ritual-heartbeat-tracker/src/lib.rs

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0003`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Canonical-state cleanup, reorg behavior, and heartbeat revival dedup.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-heartbeat-tracker/src/lib.rs`
  - Feature source IDs: `feature-raw-0042`

### File 0309: crates/ritual-heartbeat-tracker/src/lib.rs

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0004`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Heartbeat contract liveness, failed-agent revival, cooldown, owner/executor data, and revive dedup.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-heartbeat-tracker/src/lib.rs`
  - Feature source IDs: `feature-raw-0053`

### File 0309: crates/ritual-heartbeat-tracker/src/lib.rs

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0005`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve heartbeat/revival policy: heartbeat hydration and `ritual_getHeartbeatTrackerState` (`#331`), deterministic Phase 0b skip after slow runs (`#337`), revival-lane filtering and `RETH_REVIVAL_*` knobs (`#338`), single `reviveAgent(address,bytes)` path and owner pending-job dedup (`#339`), parent-hash-plus-agent entropy (`#342`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-heartbeat-tracker/src/lib.rs`
  - Feature source IDs: `feature-raw-0059`

### File 0311: crates/ritual-metrics/src/block.rs

- Key: `file_index=311`, `source_path=crates/ritual-metrics/src/block.rs`, `record_id=file-0311-atom-0002`
  - Source hunk: `feature-preservation-map.md section 11: Observability And Agent Guardrails`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Ritual JSON tracing router for selected lifecycle targets.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-metrics/src/block.rs`
  - Feature source IDs: `feature-raw-0126`

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0003`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Do not reintroduce deprecated `AGENT_CALL_PRECOMPILE` in fee or registry paths (`#319`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-addresses/src/lib.rs`
  - Feature source IDs: `feature-raw-0121`

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0004`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: TEE registry capability matching for each precompile.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-addresses/src/lib.rs`
  - Feature source IDs: `feature-raw-0113`

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0005`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Async precompile calls are captured with enough data to build commitments and verify SPC results.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-addresses/src/lib.rs`
  - Feature source IDs: `feature-raw-0025`

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0006`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Do not reintroduce deprecated `AGENT_CALL_PRECOMPILE`.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-addresses/src/lib.rs`
  - Feature source IDs: `feature-raw-0035`

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0007`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve precompile/address surface: DKMS `0x081B` (`#258`), FHE `0x0807` (`#264`), canonical `0x08xx` address crate and shared SPC allowlist (`#317`), split image/audio/video capabilities (`#246`), persistent-agent runtime enum `zeroclaw/openclaw/hermes` with 26-field layout (`#321`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-addresses/src/lib.rs`
  - Feature source IDs: `feature-raw-0034`

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0008`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: SPC proof/signature paths preserve original transaction context, precompile input/output, executor, and previous-block context.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-addresses/src/lib.rs`
  - Feature source IDs: `feature-raw-0026`

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0009`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Do not reintroduce `target_block`/`commit_block` (`#261`) or deprecated `AGENT_CALL_PRECOMPILE` (`#319`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-addresses/src/lib.rs`
  - Feature source IDs: `feature-raw-0090`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0023`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Async inclusion, commitment, settlement, delivery, LLM, multimodal, sovereign agent, persistent agent, and scheduled fees.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0110`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0024`
  - Source hunk: `feature-preservation-map.md section 11: Observability And Agent Guardrails`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 11 (Observability And Agent Guardrails) preserves observability: Scheduled incident tracking; Preserve payload policy traceability: build attempts, demotion capture, primary-cause trace plumbing, cap observations, async sim deadlines, total/per-category caps, combined scheduled/regular sim phases (`#332`, `#336`, `#337`, `#354`); Preserve scheduled incident observability: bounded ring buffer, structured gas/scheduled sad-path capture, decoded call/index fields, continued capture after 0-gas structured logs (`#345`, `#351`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0124, feature-raw-0130, feature-raw-0131`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0025`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve timing semantics: scheduled async simulation block is `startBlock + frequency * index - 1` (`#78`, `#150`), Phase 2 offset must be `> ttl` and `<= MAX_PHASE2_DEADLINE_OFFSET` (`#232`), shared TTL source is `max_ttl_blocks()` / `ASYNC_MAX_TTL_BLOCKS` (`#242`), default TTL is `500` (`#265`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0017`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0026`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve sender/expiry hardening: sender address propagation and original scheduled caller (`#115`), dual-path scheduled eviction and chain-halt job eviction (`#122`), sender-lock checks and settlement expiry parity (`#219`), stale duplicate pool pruning (`#260`), pending-pool age eviction (`#300`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0046`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0027`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduled subpool and scheduled system tx insertion.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0038`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0028`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: System/scheduled tx exemptions from normal nonce/balance rules where intended.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0043`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0029`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Preserve overflow-safe scheduled fee/gas conversion (`#305`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0060`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0030`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 5 (Scheduling And Heartbeat) preserves scheduled due constraints: C1-C11 scheduled constraints, including predicate `shouldExecute`; Scheduled async calls should not be double-counted as missed obligations when an active async job exists; Preserve censorship and active-job rules: predicate-filtered obligations, capacity-based omission rejection, active-async-job exemption (`#278`), active-job filtering for augmented scheduled obligations (`#354`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0052, feature-raw-0054, feature-raw-0058`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0031`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 6 (Payload Building) preserves payload construction: Scheduled obligation augmentation before final ordering; Unified collection across regular, scheduled, fulfilled async, and delivery txs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0063, feature-raw-0066`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0032`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve block limits/gas policy: `builder.max-block-size` (`#99`), async commitments charge zero block gas while scheduled/settlement use calldata gas and EVM execution may use `u64::MAX` (`#167`), payload deadline and safe selector/input extraction (`#282`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0072`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0033`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 7 (Block Verification And Consensus Gates) preserves scheduled due constraints: Scheduled C1-C11 constraints and heartbeat constraints; Sequencing-rights validation and scheduled censorship checks; Preserve scheduled verifier hardening: C11 rejection (`#262`), censorship checks and capacity-based omission rejection (`#278`), builder/verifier obligation consistency and active-job filtering (`#292`, `#354`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0080, feature-raw-0082, feature-raw-0088`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0034`
  - Source hunk: `feature-preservation-map.md section 8: RPC And Operator Surfaces`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 8 (RPC And Operator Surfaces) preserves heartbeat revival: `ritual_*` namespace for async result submission, batch submission, delivery result submission, pending jobs, async simulation traces, block-build traces, scheduled incidents, and heartbeat tracker state; Preserve operator APIs: `ritual_getHeartbeatTrackerState` (`#331`), scheduled incident debug RPC (`#345`, `#351`), block-build trace with demotions/caps/primary included count (`#336`, `#354`), async simulation trace.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0091, feature-raw-0098`

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0035`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Preserve `builder.max-block-size` and byte/log-size enforcement across regular, scheduled, async commitment, fulfilled async, and settlement txs (`#99`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/lib.rs`
  - Feature source IDs: `feature-raw-0105`

### File 0333: crates/ritual-scheduled-verification/src/predicate.rs

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0005`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve predicate/due-window hardening: C11 `shouldExecute`, parent-state staticcalls, predicate gas budgets (`#262`), constant-time due-window math, TTL cap `500`, saturating max-block arithmetic, zero-`num_calls` handling (`#313`), overflow bitmap slot derivation using packed `callId` and bucket (`#357`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/predicate.rs`
  - Feature source IDs: `feature-raw-0057`

### File 0333: crates/ritual-scheduled-verification/src/predicate.rs

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0006`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Due-call selection by start block, frequency, TTL, state, funds, uniqueness, and predicate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-verification/src/predicate.rs`
  - Feature source IDs: `feature-raw-0051`

### File 0342: crates/ritual-sequencing-rights/src/types.rs

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0005`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 6 (Payload Building) preserves payload construction: Tip-maximizing order with sequencing-rights reordering; Port ordering model: unified collection/execution and sequencing-rights classification/reordering (`#230`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`
  - Feature source IDs: `feature-raw-0067, feature-raw-0071`

### File 0365: crates/rpc/rpc-api/src/ritual.rs

- Key: `file_index=365`, `source_path=crates/rpc/rpc-api/src/ritual.rs`, `record_id=file-0365-atom-0002`
  - Source hunk: `feature-preservation-map.md section 8: RPC And Operator Surfaces`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: No-port unless later behavior depends on it: reverted optimized WS/pubsub behavior (`#107`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc-api/src/ritual.rs`
  - Feature source IDs: `feature-raw-0099`

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0003`
  - Source hunk: `feature-preservation-map.md section 1: Transaction Formats And Codecs`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: RLP/2718, compact codec, DB/static-file, receipt, and RPC transaction conversion compatibility.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`
  - Feature source IDs: `feature-raw-0004`

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0004`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: RPC validation simulates pending txs for immediate user feedback but is not the authority.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`
  - Feature source IDs: `feature-raw-0012`

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0005`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Async context mode distinguishes build, verify, and RPC simulation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`
  - Feature source IDs: `feature-raw-0024`

### File 0415: crates/scheduling/src/canonical.rs

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0002`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Do not preserve intermediate conflict-marker artifacts from `#337`.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/canonical.rs`
  - Feature source IDs: `feature-raw-0061`

### File 0415: crates/scheduling/src/canonical.rs

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0003`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: use final behavior from `#338`.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/canonical.rs`
  - Feature source IDs: `feature-raw-0062`

### File 0415: crates/scheduling/src/canonical.rs

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0004`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Scheduler contract storage hydration on canonical updates/startup.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/canonical.rs`
  - Feature source IDs: `feature-raw-0050`

### File 0459: crates/storage/codecs/src/alloy/passkey_signature.rs

- Key: `file_index=459`, `source_path=crates/storage/codecs/src/alloy/passkey_signature.rs`, `record_id=file-0459-atom-0004`
  - Source hunk: `feature-preservation-map.md section 1: Transaction Formats And Codecs`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: `Scheduled(0x10)`, `AsyncCommitment(0x11)`, `AsyncSettlement(0x12)`, `Passkey(0x77)`.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/passkey_signature.rs`
  - Feature source IDs: `feature-raw-0001`

### File 0459: crates/storage/codecs/src/alloy/passkey_signature.rs

- Key: `file_index=459`, `source_path=crates/storage/codecs/src/alloy/passkey_signature.rs`, `record_id=file-0459-atom-0005`
  - Source hunk: `feature-preservation-map.md section 1: Transaction Formats And Codecs`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 1 (Transaction Formats And Codecs) preserves passkey signature: Full passkey signature representation, including P256/WebAuthn and synthetic sender handling; Preserve hardening: async settlement compact codec coverage (`#84`), passkey synthetic ECDSA fallback (`#241`), safe settlement/delivery selector offsets and Phase 1/Phase 2 input extraction (`#282`), LLM 30-field ABI with `convo_history: StorageRef` at index 29 (`#306`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/passkey_signature.rs`
  - Feature source IDs: `feature-raw-0002, feature-raw-0009`

### File 0459: crates/storage/codecs/src/alloy/passkey_signature.rs

- Key: `file_index=459`, `source_path=crates/storage/codecs/src/alloy/passkey_signature.rs`, `record_id=file-0459-atom-0006`
  - Source hunk: `feature-preservation-map.md section 8: RPC And Operator Surfaces`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Feature section 8 (RPC And Operator Surfaces) preserves passkey signature: Async result submission must preserve original tx/passkey context; Preserve: Preserve delivery result submission with original tx/passkey context and `delivery_spc_calls` compatibility (`#270`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/passkey_signature.rs`
  - Feature source IDs: `feature-raw-0092, feature-raw-0097`

### File 0468: crates/storage/codecs/src/alloy/transaction/spc_call.rs

- Key: `file_index=468`, `source_path=crates/storage/codecs/src/alloy/transaction/spc_call.rs`, `record_id=file-0468-atom-0003`
  - Source hunk: `feature-preservation-map.md section 1: Transaction Formats And Codecs`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: SPC call fields: precompile address, input, output, proof, and block number.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/spc_call.rs`
  - Feature source IDs: `feature-raw-0003`

### File 0513: crates/tracing/src/ritual_router.rs

- Key: `file_index=513`, `source_path=crates/tracing/src/ritual_router.rs`, `record_id=file-0513-atom-0002`
  - Source hunk: `feature-preservation-map.md section 11: Observability And Agent Guardrails`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Bounded block-build traces and demotion/cap observations.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/tracing/src/ritual_router.rs`
  - Feature source IDs: `feature-raw-0123`

### File 0513: crates/tracing/src/ritual_router.rs

- Key: `file_index=513`, `source_path=crates/tracing/src/ritual_router.rs`, `record_id=file-0513-atom-0003`
  - Source hunk: `feature-preservation-map.md section 11: Observability And Agent Guardrails`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Bounded async simulation traces.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/tracing/src/ritual_router.rs`
  - Feature source IDs: `feature-raw-0122`

### File 0528: crates/transaction-pool/src/pool/async_pool.rs

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0002`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Fulfilled async tx conversion into settlement/delivery transactions.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool.rs`
  - Feature source IDs: `feature-raw-0041`

### File 0528: crates/transaction-pool/src/pool/async_pool.rs

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0003`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Phase 1 sender locks, release rules, expiry filtering, and delivery-ready Phase 2 state.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool.rs`
  - Feature source IDs: `feature-raw-0040`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0003`
  - Source hunk: `feature-preservation-map.md section 1: Transaction Formats And Codecs`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Do not reintroduce removed fields: `target_block` and `commit_block` were intentionally removed from async flow/codecs/RPC/txpool/verifier in favor of parent-block simulation (`#261`), except for explicit old-data decode compatibility.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0010`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0004`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve validation hardening: PrecompileConsumer decoding, executor registration/capability checks, and pool removal on failed validation (`#204`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0018`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0005`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: it was intentionally removed from detection, validation, pool, verifier, fee, and registry paths (`#319`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0036`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0006`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve duplicate/nonce behavior: optimized nonce-lock verification, pre-recovered senders, same-block duplicate commitment rejection, and pool hooks (`#207`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0047`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0007`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Async commitment pool keyed by original tx hash.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0039`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0008`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve Phase 2 and lifetime behavior: Phase 2 deadline offset semantics (`#232`), async pool metadata refresh after canonical SPC context fixes (`#273`), sovereign-agent Phase 1 async tx pool lifetime of `200` seconds (`#308`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0049`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0009`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve deferred-bytes and canonical context checks: hash/size from AsyncJobTracker, full bytes from calldata (`#208`), canonical tracker-derived SPC context and pool/contract consistency (`#273`).
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0087`

### File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0010`
  - Source hunk: `feature-preservation-map.md section 8: RPC And Operator Surfaces`
  - Required change: Verify and restore this feature-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping: Preserve: Preserve async txpool metadata RPC coverage (`#32`, `#85`), not just submission endpoints.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`
  - Feature source IDs: `feature-raw-0095`
