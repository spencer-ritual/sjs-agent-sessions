# Reth Upstream Merge Implementation Plan

Date: 2026-05-05

Use this as the phase-2 execution artifact. Keep `design.md`, `feature-preservation-map.md`,
`pr-preservation-map.md`, `functionality-flow-traces.md`, and repo-local `MERGE_NOTES.md` as
the source material for each batch.

## Implementation Plan

1. Finish dependency repo checkpoints
   Objective: make the lower-level repos coherent before Reth/nodebuilder depend on them.
   Change: Complete and commit/checkpoint `ritual-alloy-internal`, `ritual-revm-internal`,
   `ritual-alloy-evm-internal`, and `ritual-revm-inspectors-internal` in the documented order.
   Constraints: Each repo needs its own `MERGE_NOTES.md`; do not carry unresolved merge paths,
   empty deleted workspace directories, or behavior-weakening TODOs into downstream checks.
   Verification: `git diff --check`, package formatting, and the narrowest useful package check per
   repo. `ritual-alloy-internal` has a committed `v2.0.4` checkpoint (`4f808053`) after focused
   consensus/RPC/beacon tests for Ritual metadata forwarding, runtime-field encoding, `extra_data`,
   txpool async fields, and custom tx inference. For `ritual-alloy-evm-internal`,
   `cargo check -p alloy-evm` has passed for the first `v0.34.0` checkpoint.

2. Audit downstream dependency manifests
   Objective: prevent stale crates.io or deleted local crates from confusing the Reth port.
   Change: Inspect `ritual-reth-internal` and `ritual-reth-nodebuilder-internal` manifests after
   dependency repos land; align Alloy, revm, Alloy EVM, and inspector dependencies with the intended
   sibling repos.
   Constraints: `alloy-op-evm` should be considered deleted after the Alloy EVM checkpoint unless a
   live downstream consumer proves otherwise. `op-revm` policy remains a separate Reth/nodebuilder
   decision.
   Verification: Cargo metadata/check output resolves the intended sibling paths and no deleted
   workspace member is referenced.

3. Build the Reth v2.2 integration skeleton
   Objective: get the primary Reth repo onto the upstream architecture before porting behavior.
   Change: Start from clean upstream Reth `v2.2.0` shape and map Ritual node, EVM, payload, RPC,
   verifier, and txpool hooks into current extension points.
   Constraints: Do not preserve `build_evm_with_pool` or old nodebuilder APIs by default. The same
   `EthEvmConfig<RitualEvmFactory>` must reach payload building, RPC simulation, and block
   validation, with async-context capable execution where Ritual async precompiles can run.
   Verification: Reth compiles far enough to expose node builder, payload, RPC, and verifier
   extension points; `ritual-reth-nodebuilder-internal` can start compiling against the new trait
   shapes.

4. Port wire, storage, receipt, and transaction identity
   Objective: preserve shipped data identity before behavior depends on it.
   Change: Port `TxScheduled(0x10)`, `TxAsyncCommitment(0x11)`, `TxAsyncSettlement(0x12)`,
   `TxPasskey(0x77)`, SPC receipt fields, and DB/static-file codecs.
   Constraints: Do not reintroduce intentionally removed `target_block` / `commit_block` fields
   except for explicit old-data decode compatibility. Preserve Ritual metadata through wrapper and
   adapter paths (`Signed<T>`, sealed transactions, typed envelopes, RPC receipts/requests), not only
   through concrete transaction structs. Keep wire/storage encoding separate from hash/signing
   preimages for runtime fields where Ritual semantics require that split.
   Verification: Round-trip fixtures, transaction hash/root equality, and old-data decode where
   fixtures exist. Add adapter-specific tests for explicit custom tx type inference and CL/EL
   payload attributes that carry Ritual-relevant data such as `extra_data`.

5. Port execution and async admission foundation
   Objective: prove plain execution, sync precompiles, and async classification before settlement.
   Change: Port Ritual precompile registration, `AsyncContextTr` propagation, parent-state async
   detection, RPC UX validation, and builder/verifier classification.
   Constraints: RPC validation is early feedback only; builder/verifier parent-state checks remain
   the authority. Explicit gas limits and `tx_hash`/SPC metadata must not become advisory.
   Verification: sync precompile fixtures; one valid async detection fixture; negative tests for TTL,
   phase-two offset, malformed payload, missing registry/model/executor data, and oversized inputs.

6. Port pool, payload, verifier, scheduling, and operator surfaces by feature gate
   Objective: move from isolated invariants to composed Ritual behavior.
   Change: Follow `functionality-flow-traces.md` step gates for async pool lifecycle, short async
   settlement, secrets/dKMS, long-running delivery, scheduling/heartbeat, scheduled async
   combinations, mixed payload policy, RPC, traces, and incidents.
   Constraints: Keep builder/verifier checks symmetric. Every skipped validation must name the later
   gate that covers it.
   Verification: Use the gate-specific fixtures and localnet handoff table in
   `functionality-flow-traces.md`.

7. Reconcile `ritual-reth-nodebuilder-internal`
   Objective: prove the dependency repos and Reth port compose into the actual execution-layer image.
   Change: Port `RitualNode`, executor, payload builder, add-ons, RPC registration, and any custom
   pool/validator wiring to the Reth `v2.2.0` node builder APIs.
   Constraints: Use current upstream node builder extension points rather than preserving old
   compatibility shims unless no current hook exists.
   Verification: nodebuilder package check, execution-layer image build, and confirmation that the
   same EVM config reaches payload, RPC simulation, and validation.

8. Run localnet and acceptance gates
   Objective: turn compile and fixture confidence into product evidence.
   Change: Use `ritual-node-internal` to build the execution-layer image, start a localnet, generate
   gold-standard config, and run the traffic order from `functionality-flow-traces.md`.
   Constraints: Start with mock proxy mode before shared proxy mode. Add explicit sovereign/persistent
   agent traffic if gold standard still does not exercise `0x080C` or `0x0820`.
   Verification: localnet status, gold-standard traffic results, Reth payload/verifier logs, executor
   and orchestrator logs, Scheduler state, AsyncJobTracker state, and HeartbeatTracker state.
