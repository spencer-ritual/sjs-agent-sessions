# Coverage Review Queue

## File 0022: crates/chain-state/src/in_memory.rs

- Key: `file_index=22`, `source_path=crates/chain-state/src/in_memory.rs`, `record_id=file-0022-atom-0001`
  - Source hunk: `@@ -139,6 +140,8 @@ pub(crate) struct CanonicalInMemoryStateInner<N: NodePrimitives>`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chain-state/src/in_memory.rs`

- Key: `file_index=22`, `source_path=crates/chain-state/src/in_memory.rs`, `record_id=file-0022-atom-0003`
  - Source hunk: `@@ -513,8 +518,21 @@ impl<N: NodePrimitives> CanonicalInMemoryState<N>`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chain-state/src/in_memory.rs`

## File 0026: crates/chainspec/src/api.rs

- Key: `file_index=26`, `source_path=crates/chainspec/src/api.rs`, `record_id=file-0026-atom-0001`
  - Source hunk: `@@ -65,6 +65,10 @@ pub trait EthChainSpec`
  - Human question: Covered by chain spec and consensus focused tests in this pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chainspec/src/api.rs`

## File 0027: crates/chainspec/src/constants.rs

- Key: `file_index=27`, `source_path=crates/chainspec/src/constants.rs`, `record_id=file-0027-atom-0001`
  - Source hunk: `@@ -14,3 +14,9 @@ pub(crate) const MAINNET_DEPOSIT_CONTRACT`
  - Human question: No Reth code change needed for deposit-topic behavior; dependency is source of truth.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/eth/eip6110.rs`

## File 0028: crates/chainspec/src/spec.rs

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0001`
  - Source hunk: `@@ -326,11 +334,20 @@ pub struct ChainSpec`
  - Human question: Covered by chain spec and consensus focused tests in this pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chainspec/src/api.rs`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0002`
  - Source hunk: `@@ -746,7 +805,12 @@ impl From<Genesis> for ChainSpec`
  - Human question: No Reth code change needed for deposit-topic behavior; dependency is source of truth.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/eth/eip6110.rs`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0003`
  - Source hunk: `@@ -766,6 +825,9 @@ impl From<Genesis> for ChainSpec`
  - Human question: Covered by chain spec and consensus focused tests in this pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chainspec/src/api.rs`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0004`
  - Source hunk: `@@ -326,11 +334,20 @@ pub struct ChainSpec`
  - Human question: Covered by chain spec focused test in this pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chainspec/src/spec.rs`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0005`
  - Source hunk: `@@ -395,6 +420,37 @@ impl ChainSpec`
  - Human question: Covered by chain spec focused test in this pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chainspec/src/spec.rs`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0006`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Human question: Covered by chain spec and consensus focused tests in this pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chainspec/src/api.rs`

- Key: `file_index=28`, `source_path=crates/chainspec/src/spec.rs`, `record_id=file-0028-atom-0007`
  - Source hunk: `crates/chainspec/src/spec.rs:369-389`
  - Human question: Mapped to chainspec.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chainspec/src/spec.rs`

## File 0042: crates/cli/commands/src/stage/run.rs

- Key: `file_index=42`, `source_path=crates/cli/commands/src/stage/run.rs`, `record_id=file-0042-atom-0001`
  - Source hunk: `@@ -193 +193 @@ impl<C: ChainSpecParser<ChainSpec: EthChainSpec + Hardforks + EthereumHardforks>`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/cli/commands/src/stage/run.rs`

## File 0047: crates/consensus/common/Cargo.toml

- Key: `file_index=47`, `source_path=crates/consensus/common/Cargo.toml`, `record_id=file-0047-atom-0001`
  - Source hunk: `@@ -21,2 +21,3 @@`
  - Human question: None
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
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/engine/tree/Cargo.toml`

## File 0059: crates/engine/tree/src/download.rs

- Key: `file_index=59`, `source_path=crates/engine/tree/src/download.rs`, `record_id=file-0059-atom-0001`
  - Source hunk: `@@ -145 +145 @@ where`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/engine/tree/src/download.rs`

## File 0064: crates/engine/tree/src/tree/mod.rs

- Key: `file_index=64`, `source_path=crates/engine/tree/src/tree/mod.rs`, `record_id=file-0064-atom-0001`
  - Source hunk: `@@ -25,0 +26 @@ use reth_chain_state::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/engine/tree/src/tree/mod.rs`

## File 0072: crates/errors/Cargo.toml

- Key: `file_index=72`, `source_path=crates/errors/Cargo.toml`, `record_id=file-0072-atom-0002`
  - Source hunk: `@@ -19 +19,5 @@`
  - Human question: None
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
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/Cargo.toml`

- Key: `file_index=77`, `source_path=crates/ethereum/evm/Cargo.toml`, `record_id=file-0077-atom-0002`
  - Source hunk: `@@ -28,2 +29,5 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/src/build.rs`

- Key: `file_index=77`, `source_path=crates/ethereum/evm/Cargo.toml`, `record_id=file-0077-atom-0003`
  - Source hunk: `@@ -52 +56,2 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/Cargo.toml`

## File 0078: crates/ethereum/evm/src/build.rs

- Key: `file_index=78`, `source_path=crates/ethereum/evm/src/build.rs`, `record_id=file-0078-atom-0001`
  - Source hunk: `@@ -3 +3,2 @@ use alloy_consensus::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/evm/src/build.rs`

## File 0079: crates/ethereum/evm/src/execute.rs

- Key: `file_index=79`, `source_path=crates/ethereum/evm/src/execute.rs`, `record_id=file-0079-atom-0001`
  - Source hunk: `@@ -712,0 +713,3 @@ mod tests {`
  - Human question: Mapped to async-context feature propagation and payload integration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=79`, `source_path=crates/ethereum/evm/src/execute.rs`, `record_id=file-0079-atom-0002`
  - Source hunk: `crates/ethereum/evm/src/execute.rs:885-905`
  - Human question: Mapped to async-context feature propagation and payload integration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

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
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=81`, `source_path=crates/ethereum/node/Cargo.toml`, `record_id=file-0081-atom-0006`
  - Source hunk: `@@ -77,2 +84,3 @@`
  - Human question: None
  - Likely destination: `unknown`

## File 0082: crates/ethereum/node/src/lib.rs

- Key: `file_index=82`, `source_path=crates/ethereum/node/src/lib.rs`, `record_id=file-0082-atom-0001`
  - Source hunk: `@@ -25,5 +25,9 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/lib.rs`

- Key: `file_index=82`, `source_path=crates/ethereum/node/src/lib.rs`, `record_id=file-0082-atom-0002`
  - Source hunk: `@@ -25,5 +25,9 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/lib.rs`

## File 0083: crates/ethereum/node/src/node.rs

- Key: `file_index=83`, `source_path=crates/ethereum/node/src/node.rs`, `record_id=file-0083-atom-0001`
  - Source hunk: `@@ -4 +4 @@ pub use crate::{payload::EthereumPayloadBuilder, EthereumEngineValidator};`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/node.rs`

## File 0084: crates/ethereum/node/src/payload.rs

- Key: `file_index=84`, `source_path=crates/ethereum/node/src/payload.rs`, `record_id=file-0084-atom-0001`
  - Source hunk: `@@ -50,3 +50,8 @@ impl EthereumPayloadBuilder {`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=84`, `source_path=crates/ethereum/node/src/payload.rs`, `record_id=file-0084-atom-0002`
  - Source hunk: `@@ -50,3 +50,8 @@ impl EthereumPayloadBuilder {`
  - Human question: Fixed in the v2.2 port during the feature-ordered pass; focused crate checks passed.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/payload.rs`

## File 0085: crates/ethereum/node/src/spc.rs

- Key: `file_index=85`, `source_path=crates/ethereum/node/src/spc.rs`, `record_id=file-0085-atom-0001`
  - Source hunk: `@@ -0,0 +1,175 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0087: crates/ethereum/payload/Cargo.toml

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0002`
  - Source hunk: `@@ -32,2 +33,3 @@`
  - Human question: Confirm that converting the plain workspace `revm-context` dependency into an explicit path-plus-features edge is sufficient to preserve the downstream async payload context behavior.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/Cargo.toml`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0005`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0006`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0007`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0008`
  - Source hunk: `@@ -38,2 +40,17 @@`
  - Human question: Confirm that `ritual-scheduled-block-building` fully replaces the old payload-local `ritual-scheduling` dependency surface, including heartbeat-routed and predicate-gated orchestration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/src/lib.rs`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0010`
  - Source hunk: `@@ -41 +58,10 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0011`
  - Source hunk: `@@ -41 +58,10 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/Cargo.toml`

- Key: `file_index=87`, `source_path=crates/ethereum/payload/Cargo.toml`, `record_id=file-0087-atom-0013`
  - Source hunk: `@@ -41 +58,10 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0088: crates/ethereum/payload/src/bundle.rs

- Key: `file_index=88`, `source_path=crates/ethereum/payload/src/bundle.rs`, `record_id=file-0088-atom-0001`
  - Source hunk: `@@ -0,0 +1,194 @@`
  - Human question: Mapped to current payload module; old file split is not restored.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=88`, `source_path=crates/ethereum/payload/src/bundle.rs`, `record_id=file-0088-atom-0002`
  - Source hunk: `@@ -0,0 +1,194 @@`
  - Human question: Mapped to current payload module; old file split is not restored.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

## File 0089: crates/ethereum/payload/src/collector.rs

- Key: `file_index=89`, `source_path=crates/ethereum/payload/src/collector.rs`, `record_id=file-0089-atom-0001`
  - Source hunk: `@@ -0,0 +1,124 @@`
  - Human question: Mapped to current payload module; old file split is not restored.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=89`, `source_path=crates/ethereum/payload/src/collector.rs`, `record_id=file-0089-atom-0002`
  - Source hunk: `@@ -0,0 +1,124 @@`
  - Human question: Mapped to current payload module; old file split is not restored.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

## File 0090: crates/ethereum/payload/src/config.rs

- Key: `file_index=90`, `source_path=crates/ethereum/payload/src/config.rs`, `record_id=file-0090-atom-0001`
  - Source hunk: `@@ -2,0 +3,4 @@ use reth_primitives_traits::constants::GAS_LIMIT_BOUND_DIVISOR;`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

## File 0091: crates/ethereum/payload/src/execution.rs

- Key: `file_index=91`, `source_path=crates/ethereum/payload/src/execution.rs`, `record_id=file-0091-atom-0001`
  - Source hunk: `@@ -0,0 +1,311 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0092: crates/ethereum/payload/src/lib.rs

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0001`
  - Source hunk: `@@ -11,0 +12,5 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0003`
  - Source hunk: `@@ -194,132 +1255,5106 @@ where`
  - Human question: Mapped to current payload builder/verifier structure.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0013`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0020`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Human question: Fixed in the v2.2 port during the feature-ordered pass; focused crate checks passed.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/payload.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0022`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:430-451`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0023`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:1297-1318`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0024`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:1440-1461`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0025`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:1742-1763`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0027`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:2337-2358`
  - Human question: Mapped to current payload builder/verifier structure.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0028`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:2882-2903`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0029`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:2967-2988`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0030`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:2992-3013`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0031`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:1-19`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0032`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:5340-5361`
  - Required change: Split and port old multimodal/FHE Phase 2 pricing before marking this broad pricing branch atom green. Keep current fail-closed guards for unported families.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0033`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:5238-5259`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0034`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:2730-2751`
  - Human question: Mapped to current payload builder/verifier structure.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0035`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:3299-3320`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0038`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:3065-3085`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=92`, `source_path=crates/ethereum/payload/src/lib.rs`, `record_id=file-0092-atom-0044`
  - Source hunk: `crates/ethereum/payload/src/lib.rs:2967-2987`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

## File 0093: crates/ethereum/payload/src/unified_builder.rs

- Key: `file_index=93`, `source_path=crates/ethereum/payload/src/unified_builder.rs`, `record_id=file-0093-atom-0001`
  - Source hunk: `@@ -0,0 +1,341 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=93`, `source_path=crates/ethereum/payload/src/unified_builder.rs`, `record_id=file-0093-atom-0002`
  - Source hunk: `@@ -0,0 +1,341 @@`
  - Human question: Mapped to current payload module; old file split is not restored.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

## File 0094: crates/ethereum/payload/src/unified_execution.rs

- Key: `file_index=94`, `source_path=crates/ethereum/payload/src/unified_execution.rs`, `record_id=file-0094-atom-0001`
  - Source hunk: `@@ -0,0 +1,537 @@`
  - Human question: Mapped to current payload module; old file split is not restored.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

## File 0097: crates/ethereum/primitives/src/receipt.rs

- Key: `file_index=97`, `source_path=crates/ethereum/primitives/src/receipt.rs`, `record_id=file-0097-atom-0001`
  - Source hunk: `@@ -38,4 +38,4 @@ impl Receipt {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/primitives/src/receipt.rs`

## File 0098: crates/ethereum/primitives/src/transaction.rs

- Key: `file_index=98`, `source_path=crates/ethereum/primitives/src/transaction.rs`, `record_id=file-0098-atom-0002`
  - Source hunk: `crates/ethereum/primitives/src/transaction.rs:2046-2066`
  - Human question: Mapped to prior tx identity/codecs pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/ethereum.rs`

- Key: `file_index=98`, `source_path=crates/ethereum/primitives/src/transaction.rs`, `record_id=file-0098-atom-0003`
  - Source hunk: `crates/ethereum/primitives/src/transaction.rs:1-20`
  - Human question: Mapped to prior tx identity/codecs pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/ethereum.rs`

## File 0099: crates/ethereum/reth/Cargo.toml

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0001`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/reth/Cargo.toml`

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0002`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/reth/Cargo.toml`

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0003`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/reth/Cargo.toml`

- Key: `file_index=99`, `source_path=crates/ethereum/reth/Cargo.toml`, `record_id=file-0099-atom-0004`
  - Source hunk: `@@ -117,3 +117,4 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/reth/Cargo.toml`

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
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/evm/Cargo.toml`

- Key: `file_index=101`, `source_path=crates/evm/Cargo.toml`, `record_id=file-0101-atom-0004`
  - Source hunk: `@@ -72,3 +81,4 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/evm/Cargo.toml`

## File 0102: crates/evm/execution-errors/Cargo.toml

- Key: `file_index=102`, `source_path=crates/evm/execution-errors/Cargo.toml`, `record_id=file-0102-atom-0001`
  - Source hunk: `@@ -31,3 +31,4 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/execution-errors/Cargo.toml`

## File 0106: crates/evm/src/async_context_tests.rs

- Key: `file_index=106`, `source_path=crates/evm/src/async_context_tests.rs`, `record_id=file-0106-atom-0001`
  - Source hunk: `@@ -0,0 +1,99 @@`
  - Human question: Mapped to async-context feature propagation and payload integration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=106`, `source_path=crates/evm/src/async_context_tests.rs`, `record_id=file-0106-atom-0002`
  - Source hunk: `@@ -0,0 +1,99 @@`
  - Human question: Mapped to async-context feature propagation and payload integration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

## File 0107: crates/evm/src/execute.rs

- Key: `file_index=107`, `source_path=crates/evm/src/execute.rs`, `record_id=file-0107-atom-0001`
  - Source hunk: `@@ -256,0 +257,17 @@ pub trait BlockBuilder {`
  - Human question: First-pass review found the behavior split between the v2 Reth block-builder trait and Alloy EVM executor implementation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/evm/evm/src/execute.rs`

- Key: `file_index=107`, `source_path=crates/evm/src/execute.rs`, `record_id=file-0107-atom-0002`
  - Source hunk: `crates/evm/src/execute.rs:26-46`
  - Human question: Mapped to async-context feature propagation and payload integration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

## File 0110: crates/evm/src/pool_manager.rs

- Key: `file_index=110`, `source_path=crates/evm/src/pool_manager.rs`, `record_id=file-0110-atom-0001`
  - Source hunk: `@@ -0,0 +1,89 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

## File 0111: crates/evm/src/spc.rs

- Key: `file_index=111`, `source_path=crates/evm/src/spc.rs`, `record_id=file-0111-atom-0001`
  - Source hunk: `@@ -0,0 +1,151 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
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
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

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

- Key: `file_index=194`, `source_path=crates/node/builder/src/launch/engine.rs`, `record_id=file-0194-atom-0002`
  - Source hunk: `crates/node/builder/src/launch/engine.rs:444-457`
  - Human question: Mapped to core async blocking pubsub restoration.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/chain-state/src/in_memory.rs`

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

- Key: `file_index=200`, `source_path=crates/node/core/src/args/payload_builder.rs`, `record_id=file-0200-atom-0002`
  - Source hunk: `@@ -141,14 +152,16 @@ mod tests {`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
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
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0207: crates/optimism/cli/src/commands/import.rs

- Key: `file_index=207`, `source_path=crates/optimism/cli/src/commands/import.rs`, `record_id=file-0207-atom-0001`
  - Source hunk: `@@ -92 +92 @@ impl<C: ChainSpecParser<ChainSpec = OpChainSpec>> ImportOpCommand<C> {`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0211: crates/optimism/consensus/src/lib.rs

- Key: `file_index=211`, `source_path=crates/optimism/consensus/src/lib.rs`, `record_id=file-0211-atom-0001`
  - Source hunk: `@@ -95 +95 @@ impl<ChainSpec: EthChainSpec + OpHardforks, B: Block> Consensus<B>`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0212: crates/optimism/consensus/src/proof.rs

- Key: `file_index=212`, `source_path=crates/optimism/consensus/src/proof.rs`, `record_id=file-0212-atom-0001`
  - Source hunk: `@@ -22,2 +22,2 @@ pub(crate) fn calculate_receipt_root_optimism<R: DepositReceipt>(`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/MERGE_NOTES.md`

## File 0218: crates/optimism/payload/src/builder.rs

- Key: `file_index=218`, `source_path=crates/optimism/payload/src/builder.rs`, `record_id=file-0218-atom-0001`
  - Source hunk: `@@ -151 +151 @@ where`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0221: crates/optimism/primitives/src/receipt.rs

- Key: `file_index=221`, `source_path=crates/optimism/primitives/src/receipt.rs`, `record_id=file-0221-atom-0001`
  - Source hunk: `@@ -43,4 +43,4 @@ impl OpReceipt {`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/MERGE_NOTES.md`

## File 0222: crates/optimism/primitives/src/transaction/signed.rs

- Key: `file_index=222`, `source_path=crates/optimism/primitives/src/transaction/signed.rs`, `record_id=file-0222-atom-0001`
  - Source hunk: `@@ -115 +115 @@ impl SignedTransaction for OpTransactionSigned {`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0226: crates/optimism/rpc/src/eth/ext.rs

- Key: `file_index=226`, `source_path=crates/optimism/rpc/src/eth/ext.rs`, `record_id=file-0226-atom-0001`
  - Source hunk: `@@ -122,2 +122,4 @@ where`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

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

- Key: `file_index=236`, `source_path=crates/payload/builder/src/service.rs`, `record_id=file-0236-atom-0002`
  - Source hunk: `crates/payload/builder/src/service.rs:57-77`
  - Human question: Fixed in the v2.2 port during the feature-ordered pass; focused crate checks passed.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/node/src/payload.rs`

## File 0249: crates/primitives-traits/src/transaction/error.rs

- Key: `file_index=249`, `source_path=crates/primitives-traits/src/transaction/error.rs`, `record_id=file-0249-atom-0001`
  - Source hunk: `@@ -44,0 +45,4 @@ pub enum InvalidTransactionError {`
  - Human question: Restored at the payload and pending-block error boundary using the v2.2 upstream transaction-error surface. Guideline remediation: marked high-risk because Negative-path permanent precompile request eviction is high-risk because it affects txpool/payload rejection semantics.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/block/error.rs`

## File 0250: crates/primitives-traits/src/transaction/signed.rs

- Key: `file_index=250`, `source_path=crates/primitives-traits/src/transaction/signed.rs`, `record_id=file-0250-atom-0002`
  - Source hunk: `crates/primitives-traits/src/transaction/signed.rs:137-157`
  - Human question: Mapped to prior tx identity/codecs pass.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/ethereum.rs`

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

## File 0273: crates/ritual-async-commitment-validator/Cargo.toml

- Key: `file_index=273`, `source_path=crates/ritual-async-commitment-validator/Cargo.toml`, `record_id=file-0273-atom-0001`
  - Source hunk: `@@ -0,0 +1,25 @@`
  - Human question: Mapped to v2.2 verifier/payload validation split.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

## File 0274: crates/ritual-async-commitment-validator/src/lib.rs

- Key: `file_index=274`, `source_path=crates/ritual-async-commitment-validator/src/lib.rs`, `record_id=file-0274-atom-0001`
  - Source hunk: `@@ -0,0 +1,576 @@`
  - Human question: Mapped to v2.2 verifier/payload validation split.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=274`, `source_path=crates/ritual-async-commitment-validator/src/lib.rs`, `record_id=file-0274-atom-0002`
  - Source hunk: `@@ -0,0 +1,576 @@`
  - Human question: Mapped to v2.2 verifier/payload validation split.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=274`, `source_path=crates/ritual-async-commitment-validator/src/lib.rs`, `record_id=file-0274-atom-0003`
  - Source hunk: `crates/ritual-async-commitment-validator/src/lib.rs:6-26`
  - Human question: Mapped to v2.2 verifier/payload validation split.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

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

- Key: `file_index=276`, `source_path=crates/ritual-async-fees/src/constants.rs`, `record_id=file-0276-atom-0002`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=276`, `source_path=crates/ritual-async-fees/src/constants.rs`, `record_id=file-0276-atom-0003`
  - Source hunk: `crates/ritual-async-fees/src/constants.rs:317-337`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=276`, `source_path=crates/ritual-async-fees/src/constants.rs`, `record_id=file-0276-atom-0004`
  - Source hunk: `crates/ritual-async-fees/src/constants.rs:188-208`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0277: crates/ritual-async-fees/src/delivery.rs

- Key: `file_index=277`, `source_path=crates/ritual-async-fees/src/delivery.rs`, `record_id=file-0277-atom-0001`
  - Source hunk: `@@ -0,0 +1,252 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/delivery.rs`

## File 0278: crates/ritual-async-fees/src/gas.rs

- Key: `file_index=278`, `source_path=crates/ritual-async-fees/src/gas.rs`, `record_id=file-0278-atom-0001`
  - Source hunk: `@@ -0,0 +1,198 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/gas.rs`

- Key: `file_index=278`, `source_path=crates/ritual-async-fees/src/gas.rs`, `record_id=file-0278-atom-0002`
  - Source hunk: `@@ -0,0 +1,198 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=278`, `source_path=crates/ritual-async-fees/src/gas.rs`, `record_id=file-0278-atom-0003`
  - Source hunk: `@@ -0,0 +1,198 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=278`, `source_path=crates/ritual-async-fees/src/gas.rs`, `record_id=file-0278-atom-0004`
  - Source hunk: `crates/ritual-async-fees/src/gas.rs:3-23`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0279: crates/ritual-async-fees/src/http.rs

- Key: `file_index=279`, `source_path=crates/ritual-async-fees/src/http.rs`, `record_id=file-0279-atom-0001`
  - Source hunk: `@@ -0,0 +1,44 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/http.rs`

- Key: `file_index=279`, `source_path=crates/ritual-async-fees/src/http.rs`, `record_id=file-0279-atom-0002`
  - Source hunk: `@@ -0,0 +1,44 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0280: crates/ritual-async-fees/src/lib.rs

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0001`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Human question: The destination file still exists but lacks enough shared structure for a reliable automated equivalence claim.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0002`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0003`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0004`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0005`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0006`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0007`
  - Source hunk: `@@ -0,0 +1,1820 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0008`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0009`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0010`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0011`
  - Source hunk: `crates/ritual-async-fees/src/lib.rs:115-136`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0012`
  - Source hunk: `crates/ritual-async-fees/src/lib.rs:241-262`
  - Required change: Port old image Phase 2 model-specific per-pixel pricing and associated model-registry reads before enabling this family.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=280`, `source_path=crates/ritual-async-fees/src/lib.rs`, `record_id=file-0280-atom-0013`
  - Source hunk: `crates/ritual-async-fees/src/lib.rs:311-332`
  - Required change: Port old video/audio-style multimodal escrow/model-specific pricing and associated model-registry reads before enabling this family.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0281: crates/ritual-async-fees/src/llm.rs

- Key: `file_index=281`, `source_path=crates/ritual-async-fees/src/llm.rs`, `record_id=file-0281-atom-0001`
  - Source hunk: `@@ -0,0 +1,941 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/llm.rs`

- Key: `file_index=281`, `source_path=crates/ritual-async-fees/src/llm.rs`, `record_id=file-0281-atom-0002`
  - Source hunk: `@@ -0,0 +1,941 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0282: crates/ritual-async-fees/src/registry.rs

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0001`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/registry.rs`

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0002`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0003`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0004`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0005`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=282`, `source_path=crates/ritual-async-fees/src/registry.rs`, `record_id=file-0282-atom-0006`
  - Source hunk: `@@ -0,0 +1,1132 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0283: crates/ritual-async-fees/src/scheduled.rs

- Key: `file_index=283`, `source_path=crates/ritual-async-fees/src/scheduled.rs`, `record_id=file-0283-atom-0001`
  - Source hunk: `@@ -0,0 +1,373 @@`
  - Human question: filename/path similarity is not evidence of preserved behavior, guards, transitions, side effects, or failure paths.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=283`, `source_path=crates/ritual-async-fees/src/scheduled.rs`, `record_id=file-0283-atom-0002`
  - Source hunk: `@@ -0,0 +1,373 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=283`, `source_path=crates/ritual-async-fees/src/scheduled.rs`, `record_id=file-0283-atom-0003`
  - Source hunk: `@@ -0,0 +1,373 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0284: crates/ritual-async-fees/src/validators.rs

- Key: `file_index=284`, `source_path=crates/ritual-async-fees/src/validators.rs`, `record_id=file-0284-atom-0001`
  - Source hunk: `@@ -0,0 +1,106 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/validators.rs`

- Key: `file_index=284`, `source_path=crates/ritual-async-fees/src/validators.rs`, `record_id=file-0284-atom-0002`
  - Source hunk: `@@ -0,0 +1,106 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=284`, `source_path=crates/ritual-async-fees/src/validators.rs`, `record_id=file-0284-atom-0003`
  - Source hunk: `@@ -0,0 +1,106 @@`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0285: crates/ritual-async-fees/src/wallet.rs

- Key: `file_index=285`, `source_path=crates/ritual-async-fees/src/wallet.rs`, `record_id=file-0285-atom-0001`
  - Source hunk: `@@ -0,0 +1,540 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/wallet.rs`

- Key: `file_index=285`, `source_path=crates/ritual-async-fees/src/wallet.rs`, `record_id=file-0285-atom-0002`
  - Source hunk: `crates/ritual-async-fees/src/wallet.rs:19-39`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

- Key: `file_index=285`, `source_path=crates/ritual-async-fees/src/wallet.rs`, `record_id=file-0285-atom-0003`
  - Source hunk: `crates/ritual-async-fees/src/wallet.rs:291-311`
  - Human question: Mapped to shared fee crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-fees/src/lib.rs`

## File 0286: crates/ritual-async-inspector/Cargo.toml

- Key: `file_index=286`, `source_path=crates/ritual-async-inspector/Cargo.toml`, `record_id=file-0286-atom-0001`
  - Source hunk: `@@ -0,0 +1,14 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/Cargo.toml`

## File 0287: crates/ritual-async-inspector/src/inspector.rs

- Key: `file_index=287`, `source_path=crates/ritual-async-inspector/src/inspector.rs`, `record_id=file-0287-atom-0001`
  - Source hunk: `@@ -0,0 +1,224 @@`
  - Human question: filename/path similarity is not evidence of preserved behavior, guards, transitions, side effects, or failure paths.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

## File 0288: crates/ritual-async-inspector/src/lib.rs

- Key: `file_index=288`, `source_path=crates/ritual-async-inspector/src/lib.rs`, `record_id=file-0288-atom-0001`
  - Source hunk: `@@ -0,0 +1,59 @@`
  - Human question: The destination file still exists but lacks enough shared structure for a reliable automated equivalence claim.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

## File 0289: crates/ritual-async-inspector/src/utils.rs

- Key: `file_index=289`, `source_path=crates/ritual-async-inspector/src/utils.rs`, `record_id=file-0289-atom-0001`
  - Source hunk: `@@ -0,0 +1,4 @@`
  - Human question: Mapped to live inspector crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

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

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0002`
  - Source hunk: `@@ -0,0 +1,2223 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0003`
  - Source hunk: `@@ -0,0 +1,2223 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0004`
  - Source hunk: `@@ -0,0 +1,2223 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0005`
  - Source hunk: `@@ -0,0 +1,2223 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0006`
  - Source hunk: `@@ -0,0 +1,2223 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0007`
  - Source hunk: `@@ -0,0 +1,2223 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0009`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Human question: Mapped to ritual-async-registry.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

- Key: `file_index=292`, `source_path=crates/ritual-async-registry/src/lib.rs`, `record_id=file-0292-atom-0010`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Human question: Mapped to ritual-async-registry.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/lib.rs`

## File 0293: crates/ritual-async-registry/src/slots.rs

- Key: `file_index=293`, `source_path=crates/ritual-async-registry/src/slots.rs`, `record_id=file-0293-atom-0002`
  - Source hunk: `@@ -0,0 +1,155 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/slots.rs`

- Key: `file_index=293`, `source_path=crates/ritual-async-registry/src/slots.rs`, `record_id=file-0293-atom-0003`
  - Source hunk: `@@ -0,0 +1,155 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-registry/src/slots.rs`

## File 0294: crates/ritual-async/Cargo.toml

- Key: `file_index=294`, `source_path=crates/ritual-async/Cargo.toml`, `record_id=file-0294-atom-0001`
  - Source hunk: `@@ -0,0 +1,43 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

## File 0295: crates/ritual-async/src/detector.rs

- Key: `file_index=295`, `source_path=crates/ritual-async/src/detector.rs`, `record_id=file-0295-atom-0001`
  - Source hunk: `@@ -0,0 +1,1546 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=295`, `source_path=crates/ritual-async/src/detector.rs`, `record_id=file-0295-atom-0002`
  - Source hunk: `@@ -0,0 +1,1546 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=295`, `source_path=crates/ritual-async/src/detector.rs`, `record_id=file-0295-atom-0003`
  - Source hunk: `crates/ritual-async/src/detector.rs:595-615`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=295`, `source_path=crates/ritual-async/src/detector.rs`, `record_id=file-0295-atom-0004`
  - Source hunk: `crates/ritual-async/src/detector.rs:417-437`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

## File 0296: crates/ritual-async/src/lib.rs

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0001`
  - Source hunk: `@@ -0,0 +1,54 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0002`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0003`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=296`, `source_path=crates/ritual-async/src/lib.rs`, `record_id=file-0296-atom-0004`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

## File 0297: crates/ritual-async/src/validation.rs

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0001`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Human question: filename/path similarity is not evidence of preserved behavior, guards, transitions, side effects, or failure paths.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0002`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0003`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0004`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0005`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0006`
  - Source hunk: `@@ -0,0 +1,1496 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0007`
  - Source hunk: `crates/ritual-async/src/validation.rs:49-70`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0008`
  - Source hunk: `crates/ritual-async/src/validation.rs:208-229`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/validation.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0009`
  - Source hunk: `crates/ritual-async/src/validation.rs:316-337`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0010`
  - Source hunk: `crates/ritual-async/src/validation.rs:417-438`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/validation.rs`

- Key: `file_index=297`, `source_path=crates/ritual-async/src/validation.rs`, `record_id=file-0297-atom-0011`
  - Source hunk: `crates/ritual-async/src/validation.rs:441-462`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

## File 0298: crates/ritual-async/src/wallet.rs

- Key: `file_index=298`, `source_path=crates/ritual-async/src/wallet.rs`, `record_id=file-0298-atom-0001`
  - Source hunk: `@@ -0,0 +1,140 @@`
  - Human question: Mapped to decomposed v2.2 async modules.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-async-inspector/src/lib.rs`

## File 0299: crates/ritual-block-verification/Cargo.toml

- Key: `file_index=299`, `source_path=crates/ritual-block-verification/Cargo.toml`, `record_id=file-0299-atom-0001`
  - Source hunk: `@@ -0,0 +1,42 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/Cargo.toml`

## File 0300: crates/ritual-block-verification/src/constants.rs

- Key: `file_index=300`, `source_path=crates/ritual-block-verification/src/constants.rs`, `record_id=file-0300-atom-0001`
  - Source hunk: `@@ -0,0 +1,28 @@`
  - Human question: First-pass review found the constants in the v2.2 block-verification crate, with additional async bounds rather than a missing port.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/constants.rs`

## File 0301: crates/ritual-block-verification/src/error.rs

- Key: `file_index=301`, `source_path=crates/ritual-block-verification/src/error.rs`, `record_id=file-0301-atom-0001`
  - Source hunk: `@@ -0,0 +1,167 @@`
  - Human question: First-pass review found the verifier negative-path classification surface in the v2.2 destination crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/error.rs`

## File 0302: crates/ritual-block-verification/src/lib.rs

- Key: `file_index=302`, `source_path=crates/ritual-block-verification/src/lib.rs`, `record_id=file-0302-atom-0001`
  - Source hunk: `@@ -0,0 +1,12 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

## File 0303: crates/ritual-block-verification/src/nonce_lock.rs

- Key: `file_index=303`, `source_path=crates/ritual-block-verification/src/nonce_lock.rs`, `record_id=file-0303-atom-0001`
  - Source hunk: `@@ -0,0 +1,422 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

## File 0304: crates/ritual-block-verification/src/verifier.rs

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0002`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0003`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0004`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0005`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0006`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0007`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0008`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0009`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0010`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0011`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0012`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0013`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0014`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0015`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0016`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0017`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0018`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0019`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0020`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0021`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0022`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0023`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0024`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0025`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0026`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0027`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0028`
  - Source hunk: `@@ -0,0 +1,5303 @@`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0029`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0030`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0031`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Human question: No Reth code change needed for deposit-topic behavior; dependency is source of truth.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/eth/eip6110.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0032`
  - Source hunk: `crates/ritual-block-verification/src/verifier.rs:469-489`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

- Key: `file_index=304`, `source_path=crates/ritual-block-verification/src/verifier.rs`, `record_id=file-0304-atom-0033`
  - Source hunk: `crates/ritual-block-verification/src/verifier.rs:1632-1652`
  - Human question: Mapped to ritual-block-verification/src/lib.rs.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-block-verification/src/lib.rs`

## File 0309: crates/ritual-heartbeat-tracker/src/lib.rs

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0002`
  - Source hunk: `@@ -0,0 +1,436 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-heartbeat-tracker/src/lib.rs`

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0003`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0004`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=309`, `source_path=crates/ritual-heartbeat-tracker/src/lib.rs`, `record_id=file-0309-atom-0005`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0310: crates/ritual-metrics/Cargo.toml

- Key: `file_index=310`, `source_path=crates/ritual-metrics/Cargo.toml`, `record_id=file-0310-atom-0001`
  - Source hunk: `@@ -0,0 +1,50 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0311: crates/ritual-metrics/src/block.rs

- Key: `file_index=311`, `source_path=crates/ritual-metrics/src/block.rs`, `record_id=file-0311-atom-0001`
  - Source hunk: `@@ -0,0 +1,587 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0312: crates/ritual-metrics/src/lib.rs

- Key: `file_index=312`, `source_path=crates/ritual-metrics/src/lib.rs`, `record_id=file-0312-atom-0001`
  - Source hunk: `@@ -0,0 +1,20 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0313: crates/ritual-metrics/src/scheduling.rs

- Key: `file_index=313`, `source_path=crates/ritual-metrics/src/scheduling.rs`, `record_id=file-0313-atom-0001`
  - Source hunk: `@@ -0,0 +1,415 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0314: crates/ritual-metrics/src/tx.rs

- Key: `file_index=314`, `source_path=crates/ritual-metrics/src/tx.rs`, `record_id=file-0314-atom-0001`
  - Source hunk: `@@ -0,0 +1,651 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

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

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0002`
  - Source hunk: `@@ -0,0 +1,115 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-addresses/src/lib.rs`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0003`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0004`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Required change: Use the per-precompile cross-repo atoms and runtime delivery/fee atoms; do not satisfy this broad claim directly.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-addresses/src/lib.rs`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0005`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Human question: Mapped to canonical address crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-addresses/src/lib.rs`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0006`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0007`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Human question: Mapped to canonical address crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-addresses/src/lib.rs`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0008`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Human question: Mapped to canonical address crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-addresses/src/lib.rs`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0009`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=316`, `source_path=crates/ritual-precompile-addresses/src/lib.rs`, `record_id=file-0316-atom-0010`
  - Source hunk: `crates/ritual-precompile-addresses/src/lib.rs:48-69`
  - Human question: Mapped to canonical address crate.
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

- Key: `file_index=320`, `source_path=crates/ritual-precompile-codecs/src/executor.rs`, `record_id=file-0320-atom-0002`
  - Source hunk: `@@ -0,0 +1,260 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

## File 0321: crates/ritual-precompile-codecs/src/http_call.rs

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0001`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/http_call.rs`

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0002`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0003`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0004`
  - Source hunk: `@@ -0,0 +1,548 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=321`, `source_path=crates/ritual-precompile-codecs/src/http_call.rs`, `record_id=file-0321-atom-0005`
  - Source hunk: `crates/ritual-precompile-codecs/src/http_call.rs:48-69`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

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

- Key: `file_index=323`, `source_path=crates/ritual-precompile-codecs/src/llm_call.rs`, `record_id=file-0323-atom-0002`
  - Source hunk: `@@ -0,0 +1,361 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=323`, `source_path=crates/ritual-precompile-codecs/src/llm_call.rs`, `record_id=file-0323-atom-0003`
  - Source hunk: `@@ -0,0 +1,361 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=323`, `source_path=crates/ritual-precompile-codecs/src/llm_call.rs`, `record_id=file-0323-atom-0004`
  - Source hunk: `crates/ritual-precompile-codecs/src/llm_call.rs:16-37`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

## File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0001`
  - Source hunk: `@@ -0,0 +1,1172 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/long_running.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0002`
  - Source hunk: `@@ -0,0 +1,1172 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0003`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:12-33`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0004`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:50-71`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/long_running.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0005`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:202-223`
  - Human question: Non-exact high-risk async atom retained in review queue after first-principles audit; see notes for narrowed scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/validation.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0006`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:348-369`
  - Human question: Non-exact high-risk async atom retained in review queue after first-principles audit; see notes for narrowed scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0007`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:507-528`
  - Human question: Non-exact high-risk async atom retained in review queue after first-principles audit; see notes for narrowed scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/persistent_agent.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0008`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:661-682`
  - Human question: Non-exact high-risk async atom retained in review queue after first-principles audit; see notes for narrowed scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/long_running.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0009`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:852-873`
  - Required change: Port old `extract_fhe_output_size` and FHE Phase 2 fee/wallet logic, then enable FHE delivery; until then keep FHE fail-closed and do not mark runtime parity green.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/ritual_async.rs`

- Key: `file_index=324`, `source_path=crates/ritual-precompile-codecs/src/long_running.rs`, `record_id=file-0324-atom-0010`
  - Source hunk: `crates/ritual-precompile-codecs/src/long_running.rs:349-369`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/storage_ref.rs`

## File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0001`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/persistent_agent.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0002`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0003`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0004`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0005`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0006`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0007`
  - Source hunk: `@@ -0,0 +1,968 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0008`
  - Source hunk: `crates/ritual-precompile-codecs/src/persistent_agent.rs:118-139`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=325`, `source_path=crates/ritual-precompile-codecs/src/persistent_agent.rs`, `record_id=file-0325-atom-0009`
  - Source hunk: `crates/ritual-precompile-codecs/src/persistent_agent.rs:629-650`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

## File 0326: crates/ritual-precompile-codecs/src/sovereign_agent.rs

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0001`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0002`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0003`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0004`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0005`
  - Source hunk: `@@ -0,0 +1,543 @@`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

- Key: `file_index=326`, `source_path=crates/ritual-precompile-codecs/src/sovereign_agent.rs`, `record_id=file-0326-atom-0006`
  - Source hunk: `crates/ritual-precompile-codecs/src/sovereign_agent.rs:51-72`
  - Human question: Mapped to canonical codec crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-precompile-codecs/src/lib.rs`

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

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0002`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/src/lib.rs`

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0003`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Human question: Mapped to live builder helper crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/src/lib.rs`

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0004`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Human question: Mapped to live builder helper crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/src/lib.rs`

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0005`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Human question: Mapped to live builder helper crate.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-block-building/src/lib.rs`

- Key: `file_index=329`, `source_path=crates/ritual-scheduled-block-building/src/lib.rs`, `record_id=file-0329-atom-0006`
  - Source hunk: `@@ -0,0 +1,911 @@`
  - Human question: Mapped to live builder helper crate.
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

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0003`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0004`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0005`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0006`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0007`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0008`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0009`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0010`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0011`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0012`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0013`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0014`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0015`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0016`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0017`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0018`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0019`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0020`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0022`
  - Source hunk: `@@ -0,0 +1,3813 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0023`
  - Source hunk: `feature-preservation-map.md section 10: Fees, Registries, And Product Economics`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0025`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0026`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0027`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0028`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0029`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0030`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0031`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0032`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0033`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0035`
  - Source hunk: `feature-preservation-map.md section 9: Chainspec, Genesis, And Config`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0036`
  - Source hunk: `crates/ritual-scheduled-verification/src/lib.rs:1-21`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0037`
  - Source hunk: `crates/ritual-scheduled-verification/src/lib.rs:36-57`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0038`
  - Source hunk: `crates/ritual-scheduled-verification/src/lib.rs:403-424`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0039`
  - Source hunk: `crates/ritual-scheduled-verification/src/lib.rs:431-452`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0040`
  - Source hunk: `crates/ritual-scheduled-verification/src/lib.rs:821-842`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=332`, `source_path=crates/ritual-scheduled-verification/src/lib.rs`, `record_id=file-0332-atom-0041`
  - Source hunk: `crates/ritual-scheduled-verification/src/lib.rs:2170-2190`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

## File 0333: crates/ritual-scheduled-verification/src/predicate.rs

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0001`
  - Source hunk: `@@ -0,0 +1,235 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/predicate.rs`

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0002`
  - Source hunk: `@@ -0,0 +1,235 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/predicate.rs`

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0005`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0006`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

- Key: `file_index=333`, `source_path=crates/ritual-scheduled-verification/src/predicate.rs`, `record_id=file-0333-atom-0007`
  - Source hunk: `crates/ritual-scheduled-verification/src/predicate.rs:98-118`
  - Human question: Mapped to the live scheduled FSM source of truth.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/lib.rs`

## File 0334: crates/ritual-scheduled-verification/src/slots.rs

- Key: `file_index=334`, `source_path=crates/ritual-scheduled-verification/src/slots.rs`, `record_id=file-0334-atom-0002`
  - Source hunk: `@@ -0,0 +1,275 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/slots.rs`

- Key: `file_index=334`, `source_path=crates/ritual-scheduled-verification/src/slots.rs`, `record_id=file-0334-atom-0003`
  - Source hunk: `@@ -0,0 +1,275 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-scheduled-verification/src/slots.rs`

## File 0335: crates/ritual-sequencing-rights/Cargo.toml

- Key: `file_index=335`, `source_path=crates/ritual-sequencing-rights/Cargo.toml`, `record_id=file-0335-atom-0001`
  - Source hunk: `@@ -0,0 +1,35 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0336: crates/ritual-sequencing-rights/src/bucket.rs

- Key: `file_index=336`, `source_path=crates/ritual-sequencing-rights/src/bucket.rs`, `record_id=file-0336-atom-0001`
  - Source hunk: `@@ -0,0 +1,604 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=336`, `source_path=crates/ritual-sequencing-rights/src/bucket.rs`, `record_id=file-0336-atom-0002`
  - Source hunk: `@@ -0,0 +1,604 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0337: crates/ritual-sequencing-rights/src/classifier.rs

- Key: `file_index=337`, `source_path=crates/ritual-sequencing-rights/src/classifier.rs`, `record_id=file-0337-atom-0001`
  - Source hunk: `@@ -0,0 +1,763 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=337`, `source_path=crates/ritual-sequencing-rights/src/classifier.rs`, `record_id=file-0337-atom-0002`
  - Source hunk: `@@ -0,0 +1,763 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=337`, `source_path=crates/ritual-sequencing-rights/src/classifier.rs`, `record_id=file-0337-atom-0003`
  - Source hunk: `@@ -0,0 +1,763 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0338: crates/ritual-sequencing-rights/src/error.rs

- Key: `file_index=338`, `source_path=crates/ritual-sequencing-rights/src/error.rs`, `record_id=file-0338-atom-0001`
  - Source hunk: `@@ -0,0 +1,39 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0339: crates/ritual-sequencing-rights/src/lib.rs

- Key: `file_index=339`, `source_path=crates/ritual-sequencing-rights/src/lib.rs`, `record_id=file-0339-atom-0001`
  - Source hunk: `@@ -0,0 +1,244 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0340: crates/ritual-sequencing-rights/src/priority.rs

- Key: `file_index=340`, `source_path=crates/ritual-sequencing-rights/src/priority.rs`, `record_id=file-0340-atom-0001`
  - Source hunk: `@@ -0,0 +1,287 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=340`, `source_path=crates/ritual-sequencing-rights/src/priority.rs`, `record_id=file-0340-atom-0002`
  - Source hunk: `@@ -0,0 +1,287 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0341: crates/ritual-sequencing-rights/src/reader.rs

- Key: `file_index=341`, `source_path=crates/ritual-sequencing-rights/src/reader.rs`, `record_id=file-0341-atom-0001`
  - Source hunk: `@@ -0,0 +1,358 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=341`, `source_path=crates/ritual-sequencing-rights/src/reader.rs`, `record_id=file-0341-atom-0002`
  - Source hunk: `@@ -0,0 +1,358 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0342: crates/ritual-sequencing-rights/src/types.rs

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0001`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0002`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0003`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0004`
  - Source hunk: `@@ -0,0 +1,293 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=342`, `source_path=crates/ritual-sequencing-rights/src/types.rs`, `record_id=file-0342-atom-0005`
  - Source hunk: `feature-preservation-map.md section 6: Payload Building`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
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

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0002`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0003`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0004`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0005`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0006`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0007`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0008`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0009`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0010`
  - Source hunk: `@@ -0,0 +1,724 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0011`
  - Source hunk: `crates/ritual-spc-signature/src/lib.rs:15-36`
  - Human question: Mapped to current ritual-spc-signature implementation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0012`
  - Source hunk: `crates/ritual-spc-signature/src/lib.rs:199-220`
  - Human question: Mapped to current ritual-spc-signature implementation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

- Key: `file_index=344`, `source_path=crates/ritual-spc-signature/src/lib.rs`, `record_id=file-0344-atom-0013`
  - Source hunk: `crates/ritual-spc-signature/src/lib.rs:181-202`
  - Human question: Mapped to current ritual-spc-signature tests and implementation.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-spc-signature/src/lib.rs`

## File 0346: crates/ritual-spc-verification/Cargo.toml

- Key: `file_index=346`, `source_path=crates/ritual-spc-verification/Cargo.toml`, `record_id=file-0346-atom-0001`
  - Source hunk: `@@ -0,0 +1,76 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0348: crates/ritual-spc-verification/src/client.rs

- Key: `file_index=348`, `source_path=crates/ritual-spc-verification/src/client.rs`, `record_id=file-0348-atom-0001`
  - Source hunk: `@@ -0,0 +1,180 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=348`, `source_path=crates/ritual-spc-verification/src/client.rs`, `record_id=file-0348-atom-0002`
  - Source hunk: `@@ -0,0 +1,180 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=348`, `source_path=crates/ritual-spc-verification/src/client.rs`, `record_id=file-0348-atom-0003`
  - Source hunk: `@@ -0,0 +1,180 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0349: crates/ritual-spc-verification/src/error.rs

- Key: `file_index=349`, `source_path=crates/ritual-spc-verification/src/error.rs`, `record_id=file-0349-atom-0001`
  - Source hunk: `@@ -0,0 +1,64 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0350: crates/ritual-spc-verification/src/lib.rs

- Key: `file_index=350`, `source_path=crates/ritual-spc-verification/src/lib.rs`, `record_id=file-0350-atom-0001`
  - Source hunk: `@@ -0,0 +1,105 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0351: crates/ritual-spc-verification/src/types.rs

- Key: `file_index=351`, `source_path=crates/ritual-spc-verification/src/types.rs`, `record_id=file-0351-atom-0001`
  - Source hunk: `@@ -0,0 +1,380 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=351`, `source_path=crates/ritual-spc-verification/src/types.rs`, `record_id=file-0351-atom-0002`
  - Source hunk: `crates/ritual-spc-verification/src/types.rs:205-225`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0352: crates/ritual-spc-verification/src/verifier.rs

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0001`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0002`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0003`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=352`, `source_path=crates/ritual-spc-verification/src/verifier.rs`, `record_id=file-0352-atom-0004`
  - Source hunk: `@@ -0,0 +1,820 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0353: crates/ritual-tee-registry-reader/Cargo.toml

- Key: `file_index=353`, `source_path=crates/ritual-tee-registry-reader/Cargo.toml`, `record_id=file-0353-atom-0001`
  - Source hunk: `@@ -0,0 +1,28 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-tee-registry-reader/Cargo.toml`

## File 0357: crates/ritual-tee-registry-reader/src/reader.rs

- Key: `file_index=357`, `source_path=crates/ritual-tee-registry-reader/src/reader.rs`, `record_id=file-0357-atom-0002`
  - Source hunk: `@@ -0,0 +1,477 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ritual-tee-registry-reader/src/reader.rs`

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

## File 0390: crates/rpc/rpc-eth-types/src/revm_utils.rs

- Key: `file_index=390`, `source_path=crates/rpc/rpc-eth-types/src/revm_utils.rs`, `record_id=file-0390-atom-0001`
  - Source hunk: `@@ -114,2 +114,2 @@ impl CallFees {`
  - Human question: Reclassified after locating the moved fee helper in Alloy EVM and its Reth re-export path.
  - Likely destination: `/home/ritual/repos/ritual-alloy-evm-internal/crates/evm/src/rpc/fees.rs`

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

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0006`
  - Source hunk: `crates/rpc/rpc/src/async_tx_validator.rs:5-26`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0007`
  - Source hunk: `crates/rpc/rpc/src/async_tx_validator.rs:165-186`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0008`
  - Source hunk: `crates/rpc/rpc/src/async_tx_validator.rs:283-304`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=396`, `source_path=crates/rpc/rpc/src/async_tx_validator.rs`, `record_id=file-0396-atom-0009`
  - Source hunk: `crates/rpc/rpc/src/async_tx_validator.rs:361-382`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
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
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0415: crates/scheduling/src/canonical.rs

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0001`
  - Source hunk: `@@ -0,0 +1,544 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0002`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0003`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0004`
  - Source hunk: `feature-preservation-map.md section 5: Scheduling And Heartbeat`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0005`
  - Source hunk: `crates/scheduling/src/canonical.rs:143-163`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0006`
  - Source hunk: `crates/scheduling/src/canonical.rs:1-20`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0007`
  - Source hunk: `crates/scheduling/src/canonical.rs:387-407`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=415`, `source_path=crates/scheduling/src/canonical.rs`, `record_id=file-0415-atom-0008`
  - Source hunk: `crates/scheduling/src/canonical.rs:86-106`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0416: crates/scheduling/src/contract.rs

- Key: `file_index=416`, `source_path=crates/scheduling/src/contract.rs`, `record_id=file-0416-atom-0001`
  - Source hunk: `@@ -0,0 +1,1035 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=416`, `source_path=crates/scheduling/src/contract.rs`, `record_id=file-0416-atom-0002`
  - Source hunk: `crates/scheduling/src/contract.rs:5-25`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0417: crates/scheduling/src/events.rs

- Key: `file_index=417`, `source_path=crates/scheduling/src/events.rs`, `record_id=file-0417-atom-0001`
  - Source hunk: `@@ -0,0 +1,24 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0418: crates/scheduling/src/job.rs

- Key: `file_index=418`, `source_path=crates/scheduling/src/job.rs`, `record_id=file-0418-atom-0001`
  - Source hunk: `@@ -0,0 +1,10 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0419: crates/scheduling/src/lib.rs

- Key: `file_index=419`, `source_path=crates/scheduling/src/lib.rs`, `record_id=file-0419-atom-0001`
  - Source hunk: `@@ -0,0 +1,29 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0420: crates/scheduling/src/service.rs

- Key: `file_index=420`, `source_path=crates/scheduling/src/service.rs`, `record_id=file-0420-atom-0001`
  - Source hunk: `@@ -0,0 +1,58 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0421: crates/scheduling/src/singleton.rs

- Key: `file_index=421`, `source_path=crates/scheduling/src/singleton.rs`, `record_id=file-0421-atom-0001`
  - Source hunk: `@@ -0,0 +1,519 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=421`, `source_path=crates/scheduling/src/singleton.rs`, `record_id=file-0421-atom-0002`
  - Source hunk: `crates/scheduling/src/singleton.rs:1-18`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=421`, `source_path=crates/scheduling/src/singleton.rs`, `record_id=file-0421-atom-0003`
  - Source hunk: `crates/scheduling/src/singleton.rs:87-107`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0422: crates/scheduling/src/transaction.rs

- Key: `file_index=422`, `source_path=crates/scheduling/src/transaction.rs`, `record_id=file-0422-atom-0001`
  - Source hunk: `@@ -0,0 +1,212 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=422`, `source_path=crates/scheduling/src/transaction.rs`, `record_id=file-0422-atom-0002`
  - Source hunk: `@@ -0,0 +1,212 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0423: crates/scheduling/src/types.rs

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0001`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0002`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0003`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0004`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0005`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0006`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0007`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0008`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0009`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0010`
  - Source hunk: `@@ -0,0 +1,624 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0011`
  - Source hunk: `crates/scheduling/src/types.rs:158-178`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0012`
  - Source hunk: `crates/scheduling/src/types.rs:198-218`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=423`, `source_path=crates/scheduling/src/types.rs`, `record_id=file-0423-atom-0013`
  - Source hunk: `crates/scheduling/src/types.rs:217-237`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
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

## File 0455: crates/storage/codecs/derive/src/compact/mod.rs

- Key: `file_index=455`, `source_path=crates/storage/codecs/derive/src/compact/mod.rs`, `record_id=file-0455-atom-0001`
  - Source hunk: `@@ -151,4 +151,5 @@ fn load_field_from_segments(`
  - Human question: Reclassified after confirming the consumed upstream derive crate already includes `maybe_zero` handling and local transaction codec bitflag tests remain in place.
  - Likely destination: `/home/ritual/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/reth-codecs-derive-0.3.1/src/compact/mod.rs`

## File 0459: crates/storage/codecs/src/alloy/passkey_signature.rs

- Key: `file_index=459`, `source_path=crates/storage/codecs/src/alloy/passkey_signature.rs`, `record_id=file-0459-atom-0001`
  - Source hunk: `@@ -0,0 +1,148 @@`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/passkey_signature.rs`

- Key: `file_index=459`, `source_path=crates/storage/codecs/src/alloy/passkey_signature.rs`, `record_id=file-0459-atom-0002`
  - Source hunk: `@@ -0,0 +1,148 @@`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/passkey_signature.rs`

## File 0461: crates/storage/codecs/src/alloy/transaction/async_settlement.rs

- Key: `file_index=461`, `source_path=crates/storage/codecs/src/alloy/transaction/async_settlement.rs`, `record_id=file-0461-atom-0003`
  - Source hunk: `crates/storage/codecs/src/alloy/transaction/async_settlement.rs:37-58`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/storage/codecs/src/alloy/transaction/async_settlement.rs`

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
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

## File 0514: crates/transaction-pool/Cargo.toml

- Key: `file_index=514`, `source_path=crates/transaction-pool/Cargo.toml`, `record_id=file-0514-atom-0001`
  - Source hunk: `@@ -26,0 +27,5 @@ revm-primitives.workspace = true`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/Cargo.toml`

## File 0521: crates/transaction-pool/src/blocking_handlers.rs

- Key: `file_index=521`, `source_path=crates/transaction-pool/src/blocking_handlers.rs`, `record_id=file-0521-atom-0001`
  - Source hunk: `@@ -0,0 +1,284 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/mod.rs`

- Key: `file_index=521`, `source_path=crates/transaction-pool/src/blocking_handlers.rs`, `record_id=file-0521-atom-0002`
  - Source hunk: `crates/transaction-pool/src/blocking_handlers.rs:276-284`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

## File 0523: crates/transaction-pool/src/error.rs

- Key: `file_index=523`, `source_path=crates/transaction-pool/src/error.rs`, `record_id=file-0523-atom-0001`
  - Source hunk: `@@ -68,0 +69,4 @@ pub enum PoolErrorKind {`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/error.rs`

## File 0524: crates/transaction-pool/src/lib.rs

- Key: `file_index=524`, `source_path=crates/transaction-pool/src/lib.rs`, `record_id=file-0524-atom-0001`
  - Source hunk: `@@ -175 +175,9 @@ pub use crate::{`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/traits.rs`

## File 0525: crates/transaction-pool/src/maintain.rs

- Key: `file_index=525`, `source_path=crates/transaction-pool/src/maintain.rs`, `record_id=file-0525-atom-0001`
  - Source hunk: `@@ -12 +12 @@ use alloy_eips::BlockNumberOrTag;`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/maintain.rs`

- Key: `file_index=525`, `source_path=crates/transaction-pool/src/maintain.rs`, `record_id=file-0525-atom-0002`
  - Source hunk: `crates/transaction-pool/src/maintain.rs:57-77`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

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
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0002`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/ethereum/payload/src/lib.rs`

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0003`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0004`
  - Source hunk: `crates/transaction-pool/src/pool/async_pool.rs:28-49`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0005`
  - Source hunk: `crates/transaction-pool/src/pool/async_pool.rs:288-309`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0006`
  - Source hunk: `crates/transaction-pool/src/pool/async_pool.rs:335-356`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=528`, `source_path=crates/transaction-pool/src/pool/async_pool.rs`, `record_id=file-0528-atom-0007`
  - Source hunk: `crates/transaction-pool/src/pool/async_pool.rs:613-633`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

## File 0529: crates/transaction-pool/src/pool/async_pool_removal_tests.rs

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0001`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0002`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0003`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0004`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0005`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Required change: No code change in this v2 slice; behavior is intentionally inactive or out of scope.
  - Likely destination: `unknown`

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0006`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0007`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=529`, `source_path=crates/transaction-pool/src/pool/async_pool_removal_tests.rs`, `record_id=file-0529-atom-0008`
  - Source hunk: `@@ -0,0 +1,453 @@`
  - Human question: Mapped to async_pool and verifier.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

## File 0532: crates/transaction-pool/src/pool/mod.rs

- Key: `file_index=532`, `source_path=crates/transaction-pool/src/pool/mod.rs`, `record_id=file-0532-atom-0001`
  - Source hunk: `@@ -73,0 +74,2 @@ use crate::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/mod.rs`

## File 0535: crates/transaction-pool/src/pool/scheduled.rs

- Key: `file_index=535`, `source_path=crates/transaction-pool/src/pool/scheduled.rs`, `record_id=file-0535-atom-0001`
  - Source hunk: `@@ -0,0 +1,154 @@`
  - Human question: filename/path similarity is not evidence of preserved behavior, guards, transitions, side effects, or failure paths.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

## File 0536: crates/transaction-pool/src/pool/state.rs

- Key: `file_index=536`, `source_path=crates/transaction-pool/src/pool/state.rs`, `record_id=file-0536-atom-0001`
  - Source hunk: `@@ -77,6 +77,3 @@ pub enum SubPool {`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/state.rs`

## File 0537: crates/transaction-pool/src/pool/txpool.rs

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0001`
  - Source hunk: `@@ -12,0 +13 @@ use crate::{`
  - Human question: Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/txpool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0002`
  - Source hunk: `@@ -2326,6 +2719,22 @@ mod tests {`
  - Required change: Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/txpool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0003`
  - Source hunk: `feature-preservation-map.md section 1: Transaction Formats And Codecs`
  - Human question: Verify whether this absence/negative-preservation invariant is upheld in the v2.2 port and record evidence.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0004`
  - Source hunk: `feature-preservation-map.md section 2: Async Precompile Detection And Validation`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0005`
  - Source hunk: `feature-preservation-map.md section 3: EVM Context, Precompiles, And SPC`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0006`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0007`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0008`
  - Source hunk: `feature-preservation-map.md section 4: Txpool Async And Scheduled Lifecycle`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0009`
  - Source hunk: `feature-preservation-map.md section 7: Block Verification And Consensus Gates`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=537`, `source_path=crates/transaction-pool/src/pool/txpool.rs`, `record_id=file-0537-atom-0010`
  - Source hunk: `feature-preservation-map.md section 8: RPC And Operator Surfaces`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

## File 0538: crates/transaction-pool/src/test_utils/gen.rs

- Key: `file_index=538`, `source_path=crates/transaction-pool/src/test_utils/gen.rs`, `record_id=file-0538-atom-0001`
  - Source hunk: `@@ -154,0 +155,3 @@ impl TransactionBuilder {`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

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

- Key: `file_index=540`, `source_path=crates/transaction-pool/src/traits.rs`, `record_id=file-0540-atom-0002`
  - Source hunk: `crates/transaction-pool/src/traits.rs:371-391`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

- Key: `file_index=540`, `source_path=crates/transaction-pool/src/traits.rs`, `record_id=file-0540-atom-0003`
  - Source hunk: `crates/transaction-pool/src/traits.rs:722-742`
  - Human question: Mapped to transaction-pool async_pool.
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/async_pool.rs`

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

## File 0545: crates/transaction-pool/tests/it/async_exec.rs

- Key: `file_index=545`, `source_path=crates/transaction-pool/tests/it/async_exec.rs`, `record_id=file-0545-atom-0001`
  - Source hunk: `@@ -0,0 +1,57 @@`
  - Human question: None
  - Likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port/crates/transaction-pool/src/pool/mod.rs`

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

## First-Principles Async Precompile Audit Override

- Resolved: `file-0316-atom-0011` captures the 0x080C/0x0820 old-FSM contract as `HttpCall` / registry u8 0, backed by Reth metadata, traffic-gen HTTP executor selection, and node HTTP executor provisioning.
- Narrowed: `file-0092-atom-0008`, `file-0092-atom-0049`, and `file-0092-atom-0050` apply only to live supported families; they no longer imply multimodal/FHE runtime parity.
- Blocked, not punted: `file-0092-atom-0032`, `file-0280-atom-0012`, `file-0280-atom-0013`, and `file-0324-atom-0009` are concrete missing old-FSM runtime/fee parity for multimodal/FHE and must stay fail-closed until ported.
- Verification: `coverage-map/verify_async_precompile_cross_repo.py` is the static cross-repo gate for address -> capability -> traffic-gen -> node config consistency. It is capability proof only, not delivery/pricing proof for disabled families.
