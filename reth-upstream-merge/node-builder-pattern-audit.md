# Reth Node Builder Pattern Audit

Date: 2026-05-05

## Goal

Explain the upstream Reth node builder pattern, evaluate whether Ritual diverged before the relevant upstream architecture, and map how `ritual-reth-nodebuilder-internal` and `ritual-reth-internal` currently use or miss that pattern for the Reth `v2.2.0` upstream merge.

## Summary

Ritual is not before the existence of Reth's `NodeBuilder`; upstream had the node builder pattern by at least Reth `v1.3.12`, and the local `ritual-reth-nodebuilder-internal` repo already uses it at the high level.

The more important merge finding is that Ritual is on an older node builder API shape. The local code uses `Node`, `NodeTypes`, `ComponentsBuilder`, `ExecutorBuilder`, `PayloadBuilderBuilder`, and add-ons, but those interfaces match the older Reth `v1.3.12` family more closely than Reth `v2.2.0`. For the upstream merge, the right target is not to abandon node builder; it is to keep the node builder structure and port Ritual's custom EVM, payload, verifier, precompile, RPC, and pool hooks into the current `v2.2.0` extension points.

## Upstream Pattern

Upstream Reth's `NodeBuilder` is a type-safe assembly pipeline for a node:

- Start from CLI-derived `NodeConfig`.
- Configure static node types via `NodeTypes`: primitives, chain spec, engine payload types, storage, and related type families.
- Configure stateful components with `NodeComponentsBuilder`, typically through `ComponentsBuilder`.
- Launch the node and receive a typed `NodeHandle` / `FullNode`.
- Use add-ons and hooks for RPC modules, engine API wiring, lifecycle tasks, and other services around the core node.

The upstream docs describe the stateful component slots as:

- `ExecutorBuilder`: EVM configuration / execution configuration.
- `PoolBuilder`: transaction pool.
- `NetworkBuilder`: P2P network.
- `PayloadServiceBuilder` and `PayloadBuilderBuilder`: payload job service and concrete payload builder.
- `ConsensusBuilder`: consensus object.

Sources:

- Reth docs: https://reth.rs/docs/reth/builder/struct.NodeBuilder.html
- Reth `v2.2.0` `NodeBuilder` source: https://github.com/paradigmxyz/reth/blob/v2.2.0/crates/node/builder/src/builder/mod.rs
- Reth `v2.2.0` `ComponentsBuilder` source: https://github.com/paradigmxyz/reth/blob/v2.2.0/crates/node/builder/src/components/builder.rs
- Reth `v2.2.0` Ethereum node source: https://github.com/paradigmxyz/reth/blob/v2.2.0/crates/ethereum/node/src/node.rs

## Important `v1.3.12` To `v2.2.0` API Drift

The local code is already conceptually a node builder integration, but several local extension points line up with Reth `v1.3.12`, not `v2.2.0`.

### Executor

In Reth `v1.3.12`, `ExecutorBuilder` produced both an EVM config and a separate block executor provider:

```rust
type EVM: ConfigureEvm<...>;
type Executor: BlockExecutorProvider<...>;
fn build_evm(...) -> Result<(Self::EVM, Self::Executor)>;
```

In Reth `v2.2.0`, `ExecutorBuilder` only builds the EVM config:

```rust
type EVM: ConfigureEvm<...>;
fn build_evm(...) -> Result<Self::EVM>;
```

This matters because `ritual-reth-nodebuilder-internal/crates/node/src/executor.rs` still implements `type Executor = RitualBlockExecutorProvider<Self::EVM>` and returns `(evm_config, executor)`.

### Pool / Payload Ordering

In the local old-shape builder, `ComponentsBuilder` builds the pool first, then calls `build_evm_with_pool`, then starts network and payload:

```text
pool_builder.build_pool(context)
evm_builder.build_evm_with_pool(context, pool.clone())
network_builder.build_network(context, pool.clone())
payload_builder.spawn_payload_builder_service(context, pool.clone())
```

In Reth `v2.2.0`, the EVM config is built first, then passed into the pool and payload builders:

```text
executor_builder.build_evm(context)
pool_builder.build_pool(context, evm_config.clone())
network_builder.build_network(context, pool.clone())
payload_builder.spawn_payload_builder_service(context, pool.clone(), evm_config.clone())
```

This is a major porting point for Ritual because local `build_evm_with_pool` was added specifically to give block verification access to the transaction pool.

### Add-ons And Engine Validation

In the older shape, `EngineValidatorAddOn` directly provides a validator:

```rust
type Validator = EthereumEngineValidator;
async fn engine_validator(&self, ctx: &AddOnsContext<'_, N>) -> Result<Self::Validator>;
```

In Reth `v2.2.0`, add-ons expose a validator builder:

```rust
type ValidatorBuilder: EngineValidatorBuilder;
fn engine_validator_builder(&self) -> Self::ValidatorBuilder;
```

Reth `v2.2.0` also separates payload validation and tree validation through `PayloadValidatorBuilder`, `EngineValidatorBuilder`, `BasicEngineApiBuilder`, and `BasicEngineValidatorBuilder` in the RPC/add-on stack. Ritual's current add-on wrapper needs to move to that model.

### Node Types

The local `NodeTypes` implementations still include `type StateCommitment = MerklePatriciaTrie`, matching the older local/Reth shape. Upstream `v2.2.0` `EthereumNode` no longer declares `StateCommitment` in its `NodeTypes` implementation.

## Evidence For Or Against "We Diverged Before This"

### Evidence Against "Before NodeBuilder Existed"

- Upstream Reth introduced `NodeBuilder` before the local nodebuilder integration was created. Local `ritual-reth-internal` history includes upstream commits such as `feat: Introduce NodeBuilder` from 2023-12 and later node builder refactors.
- Upstream Reth `v1.3.12` has `NodeBuilder`, `Node`, `ComponentsBuilder`, `ExecutorBuilder`, `PoolBuilder`, `PayloadServiceBuilder`, and `EthereumNode`.
- `ritual-reth-nodebuilder-internal` already uses those concepts. The binary calls `builder.node(RitualNode::default()).launch()`, and `RitualNode` implements `NodeTypes` and `Node`.

### Evidence For "Before The Current `v2.2.0` Pattern Shape"

- `ritual-reth-nodebuilder-internal` has a remote branch named `origin/upstream/v1.3.12`. Locally, that ref points at the repo's initial commit `4e4c25e` from 2025-04-26 and contains only `README.md`; it is not a normal public upstream branch, but it is still a strong naming clue for the intended base.
- The `ritual-reth-nodebuilder-internal` git history begins with Ritual-authored commits:
  - `4e4c25e` `initial commit`
  - `ae93973` `fix: minimal rust project with the node builder pattern`
  - `40aefda` `fix: minimal nodebuilder implementatio`
  - `c23c9a9` `fix: README describing the nodebuilder pattern & implementation`
- The current local code matches older Reth interfaces:
  - `ExecutorBuilder` has an associated `Executor` type.
  - `ComponentsBuilder` stores `ExecB::Executor` in node components.
  - `PoolBuilder` builds without receiving `evm_config`.
  - `PayloadServiceBuilder` starts without receiving `evm_config`.
  - `EngineValidatorAddOn` builds a validator directly instead of returning a validator builder.
- Reth `v2.2.0` changed each of those interfaces.

Conclusion: Ritual did not diverge before Reth's node builder pattern existed. Ritual did diverge before the current `v2.2.0` node builder API shape, then partially integrated the older pattern by creating `ritual-reth-nodebuilder-internal`.

## Current Local Usage

### `ritual-reth-nodebuilder-internal`

`bin/src/main.rs` is the executable entrypoint. It parses `reth::cli::Cli<RitualChainSpecParser, NoArgs>`, initializes the synchronous scheduler singleton, then launches:

```rust
let handle = builder
    .node(RitualNode::default())
    .launch()
    .await?;
```

This is node-builder-style launch. The missing part is not the launch pattern; it is the API-version alignment and which extension points own each Ritual behavior.

`crates/node/src/lib.rs` defines `RitualNode`:

- Implements `NodeTypes` using Ethereum primitives, local `ChainSpec`, `EthStorage`, `MerklePatriciaTrie`, and `EthEngineTypes`.
- Implements `Node<N>` and returns a `ComponentsBuilder`.
- Reuses upstream/default Ethereum builders for pool, network, and consensus.
- Overrides executor with `RitualExecutorBuilder`.
- Overrides payload builder with `RitualPayloadBuilderBuilder`.
- Overrides add-ons with `RitualAddOns`.

`crates/node/src/executor.rs` is the main local execution hook:

- Defines `RitualEvmFactory`.
- Constructs `RitualEvm` with `RitualPrecompiles`.
- Defines `RitualExecutorBuilder`.
- Implements the old-style `ExecutorBuilder` with `type EVM = EthEvmConfig<RitualEvmFactory>` and `type Executor = RitualBlockExecutorProvider<Self::EVM>`.
- Uses `build_evm_with_pool` to construct a `BlockVerifier` with pool/provider/EVM access.
- Runs `ritual_precompiles::jq::ensure_jq_worker_available()` at startup.

`crates/node/src/payload.rs` is the payload hook:

- Defines `RitualPayloadBuilderBuilder`.
- Builds `EthPayloadBuilder<Pool, Node::Provider, EthEvmConfig<RitualEvmFactory>>`.
- Constructs a fresh `EthEvmConfig::new_with_evm_factory(..., RitualEvmFactory::default())` instead of receiving the builder-level EVM config from `ComponentsBuilder`.

`crates/node/src/addons.rs` is the add-on hook:

- Wraps `EthereumAddOns`.
- Adds `--debug.rpc-consensus-ws` follower-mode support through `DebugConsensusClient`.
- Delegates RPC hooks to the inner Ethereum add-ons.
- Implements the old direct `EngineValidatorAddOn` style with `type Validator = EthereumEngineValidator`.

`Cargo.toml` shows that this repo is an integration workspace over local sibling repos, not a self-contained fork of upstream Reth:

- `reth-*` crates point at `../ritual-reth-internal`.
- `revm-*` crates point at `../ritual-revm-internal`.
- `alloy-*` crates point at `../ritual-alloy-internal`.
- `alloy-evm` points at `../ritual-alloy-evm-internal`.
- `revm-inspectors` points at `../ritual-revm-inspectors-internal`.

### `ritual-reth-internal`

`ritual-reth-internal` itself has a locally modified node builder layer:

- `crates/node/builder/src/components/execute.rs` adds `build_evm_with_pool`.
- `crates/node/builder/src/components/builder.rs` calls `build_evm_with_pool` after building the pool.
- `crates/ethereum/node/src/node.rs` includes Ritual-specific changes around SPC verifier wiring, Ritual RPC registration, async/scheduling behavior, and pool/EVM integration.

This means the current Ritual stack is not simply "upstream Reth plus a downstream nodebuilder crate." The nodebuilder repo depends on local changes inside `ritual-reth-internal`'s builder APIs.

## What We Are Not Using Yet

The current stack does not yet use the `v2.2.0` node builder shape in these places:

- Pool builders do not receive `evm_config` as an input.
- Payload builders do not receive the canonical builder-created `evm_config`; `RitualPayloadBuilderBuilder` recreates it.
- Executor builders still return an executor provider separately from EVM config.
- Add-ons still use the older direct engine-validator interface.
- The custom `build_evm_with_pool` hook is local to Ritual's old builder layer and has no direct upstream `v2.2.0` equivalent.
- Ritual pool behavior is not isolated as a `RitualPoolBuilder`; the nodebuilder crate currently uses `EthereumPoolBuilder`, while much async/scheduled pool behavior lives in `ritual-reth-internal`.

## Merge Implications

For the Reth `v2.2.0` merge, the clean target should be:

1. Keep the upstream `NodeBuilder` / `Node` / `ComponentsBuilder` architecture.
2. Port `RitualNode` to the `v2.2.0` trait signatures.
3. Make `RitualExecutorBuilder` return only `EthEvmConfig<RitualEvmFactory>` under the current `ExecutorBuilder` API.
4. Make `RitualPayloadBuilderBuilder` accept the EVM config passed by `BasicPayloadServiceBuilder` instead of constructing its own parallel config.
5. Decide where the current pool-dependent `BlockVerifier` construction belongs in `v2.2.0`:
   - likely in the `EngineValidatorBuilder` / tree-validator path if it is block import / engine validation policy;
   - possibly in a custom pool or payload builder if the behavior is builder-side selection/classification;
   - not as a carried-forward `build_evm_with_pool` shim unless there is no upstream-compatible extension point.
6. Consider whether scheduled/async txpool behavior should become an explicit `RitualPoolBuilder` instead of remaining hidden inside `ritual-reth-internal`'s modified Ethereum pool.
7. Port `RitualAddOns` to the `v2.2.0` add-on stack:
   - `RethRpcAddOns`
   - `PayloadValidatorBuilder`
   - `EngineApiBuilder`
   - `EngineValidatorBuilder`
   - `EngineValidatorAddOn::engine_validator_builder`
8. Treat `ritual-reth-nodebuilder-internal` as the integration test for whether the Reth, revm, Alloy, Alloy EVM, and inspector ports compose.

## Recommended Port Checklist

- `RitualNode` compiles against upstream `v2.2.0` `NodeTypes` and `Node`.
- `RitualExecutorBuilder` compiles against upstream `v2.2.0` `ExecutorBuilder`.
- The same `EthEvmConfig<RitualEvmFactory>` reaches payload building, RPC simulation, and block validation, and those paths use `AsyncContextTr`-capable execution when Ritual async precompiles can run.
- `RitualPrecompiles` are installed through `RitualEvmFactory` in all execution modes.
- Upstream revm `v107` `CallInputs` plumbing still routes Ritual async precompile addresses through context-aware dispatch rather than a non-context fallback.
- `RitualPayloadBuilderBuilder` uses the builder-provided EVM config and preserves async/SPC payload behavior.
- Block verification, SPC verification, and sequencing-rights checks are mapped to the current upstream engine/tree validation path.
- Debug follower mode from `--debug.rpc-consensus-ws` is either preserved in add-ons or intentionally moved to the current upstream hook.
- Ritual RPC registration is ported to the current RPC add-on/module API.
- Scheduled and async txpool invariants from `feature-preservation-map.md` are mapped to either `RitualPoolBuilder`, payload-builder logic, or upstream txpool hooks.
- If any downstream manifest still references `alloy-op-evm`, remove or remap it deliberately. The `ritual-alloy-evm-internal` `v0.34.0` checkpoint accepted upstream's deletion of `crates/op-evm` after checking target Reth `v2.2.0` has no `alloy-op-evm` / `op-revm` references.
- If OP execution remains in scope, `op-revm` dependency resolution and OP precompile dispatch are verified for the same async/SPC context guarantees; otherwise OP async execution is explicitly out of scope for this merge gate.
- Final validation includes `ritual-reth-nodebuilder-internal` image build and `ritual-node-internal` localnet startup, because `ritual-node-internal` consumes the nodebuilder image.

## Open Questions

- Should the `BlockVerifier` live in the `v2.2.0` `EngineValidatorBuilder` path, or should parts of it split between payload selection and engine/tree validation?
- Should `RitualPoolBuilder` be introduced during this merge to make async/scheduled pool behavior explicit in the node builder graph?
- Should `ritual-reth-nodebuilder-internal` stay as a separate integration repo after the merge, or should it become a temporary compatibility layer over a more complete `RitualNode` inside `ritual-reth-internal`?
- How much of `ritual-reth-internal/crates/ethereum/node/src/node.rs` should be preserved after `RitualNode` owns the custom node composition?

