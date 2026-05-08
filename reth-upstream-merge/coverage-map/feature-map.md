# Reth Coverage Feature Map

Generated from the completed coverage-map atom artifacts. This is a higher-level feature index over `coverage-map/files/file-####.json`; use the atom `record_id` values here to jump back to the authoritative per-file records.

## Source State

- File artifacts: `579/579`
- Atoms: `349` total, `216` high-risk, `310` non-exact
- Human-review queue entries: `294`
- Validation errors: `0`
- Atom status counts: `{'missing': 93, 'structural_equivalent': 174, 'intentionally_absent': 5, 'exact': 35, 'moved_to_dependency': 30, 'noise': 4, 'covered_by_upstream': 4, 'blocked': 4}`

## Reading Notes

- Each atom is assigned to one primary feature for navigation, even when it touches multiple domains such as async plus encoding.
- `generic` means the underlying atom record has broad placeholder wording like “introduces behavior or wiring”; treat those as traceability anchors that need source/destination inspection before implementation decisions.
- Features are ordered from transaction identity and execution foundations into async/scheduled behavior, payload validation, API/storage surfaces, and lower-level network compatibility.

## Feature Summary


| Feature                                                   | Atoms | High Risk | Review Required | Status Counts                                                                                                                                                       | Generic Atoms |
| --------------------------------------------------------- | ----- | --------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| Transaction identity, wire encoding, and storage codecs   | 42    | 14        | 38              | `{'structural_equivalent': 34, 'moved_to_dependency': 4, 'intentionally_absent': 2, 'covered_by_upstream': 1, 'exact': 1}`                                          | 41            |
| Precompile dispatch, SPC, and executor registry           | 21    | 15        | 10              | `{'structural_equivalent': 14, 'exact': 7}`                                                                                                                         | 14            |
| Transaction pool, admission, and ordering                 | 4     | 4         | 0               | `{'structural_equivalent': 4}`                                                                                                                                      | 4             |
| Core async execution and settlement                       | 105   | 81        | 95              | `{'missing': 44, 'noise': 1, 'covered_by_upstream': 2, 'intentionally_absent': 1, 'structural_equivalent': 37, 'moved_to_dependency': 9, 'blocked': 3, 'exact': 8}` | 65            |
| Long-running async delivery FSM                           | 4     | 4         | 3               | `{'missing': 1, 'moved_to_dependency': 1, 'structural_equivalent': 1, 'exact': 1}`                                                                                  | 3             |
| Scheduled transactions and missed-obligation verification | 81    | 61        | 67              | `{'noise': 3, 'structural_equivalent': 26, 'exact': 16, 'missing': 24, 'moved_to_dependency': 12}`                                                                  | 56            |
| Payload building, execution, and consensus validation     | 43    | 28        | 42              | `{'missing': 12, 'intentionally_absent': 2, 'exact': 1, 'structural_equivalent': 24, 'moved_to_dependency': 3, 'blocked': 1}`                                       | 32            |
| RPC and external API surface                              | 14    | 9         | 14              | `{'missing': 2, 'structural_equivalent': 12}`                                                                                                                       | 14            |
| Storage, provider, and database infrastructure            | 8     | 0         | 8               | `{'structural_equivalent': 7, 'missing': 1}`                                                                                                                        | 8             |
| Network and P2P compatibility                             | 27    | 0         | 25              | `{'structural_equivalent': 15, 'missing': 9, 'covered_by_upstream': 1, 'exact': 1, 'moved_to_dependency': 1}`                                                       | 25            |


## Transaction identity, wire encoding, and storage codecs

Custom transaction types, RLP/hash/signature identity, runtime-field boundaries, receipts, storage compact codecs, and persistent DB encoding rules.

- Counts: `42` atoms; `14` high-risk; `38` review-required; statuses `{'structural_equivalent': 34, 'moved_to_dependency': 4, 'intentionally_absent': 2, 'covered_by_upstream': 1, 'exact': 1}`.
- Precision note: `41` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0212-atom-0001` `intentionally_absent` (review, generic): `crates/optimism/consensus/src/proof.rs` — OP receipt-root compatibility remains outside the current Summit/Ethereum v2.2 port scope and needs human confirmation if OP support becomes in scope.
- `file-0221-atom-0001` `intentionally_absent` (review, generic): `crates/optimism/primitives/src/receipt.rs` — OP receipt enum compatibility remains outside the current Summit/Ethereum v2.2 port scope and needs human confirmation if OP support becomes in scope.

Representative atoms:

- `file-0107-atom-0001` `structural_equivalent` (high-risk, generic): `crates/evm/src/execute.rs` — Explicit-gas system transaction execution is preserved across `reth-evm` block-builder orchestration and Alloy EVM receipt gas accounting.
- `file-0390-atom-0001` `moved_to_dependency` (high-risk, generic): `crates/rpc/rpc-eth-types/src/revm_utils.rs` — The RPC zero-fee exception moved to Alloy EVM `CallFees::ensure_fees` and is consumed through Reth's rpc-convert layer.
- `file-0455-atom-0001` `covered_by_upstream` (high-risk, generic): `crates/storage/codecs/derive/src/compact/mod.rs` — The consumed upstream `reth-codecs-derive 0.3.1` already contains `maybe_zero` compact-field handling.
- `file-0212-atom-0001` `intentionally_absent` (review, generic): `crates/optimism/consensus/src/proof.rs` — OP receipt-root compatibility is out of scope for the current v2.2 port.
- `file-0221-atom-0001` `intentionally_absent` (review, generic): `crates/optimism/primitives/src/receipt.rs` — OP receipt enum compatibility is out of scope for the current v2.2 port.
- `file-0078-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ethereum/evm/src/build.rs` — The downstream diff for crates/ethereum/evm/src/build.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0226-atom-0001` `moved_to_dependency` (high-risk, review, generic): `crates/optimism/rpc/src/eth/ext.rs` — The downstream diff for crates/optimism/rpc/src/eth/ext.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0372-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-engine-api/src/engine_api.rs` — The downstream diff for crates/rpc/rpc-engine-api/src/engine_api.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0378-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-api/src/helpers/pending_block.rs` — The downstream diff for crates/rpc/rpc-eth-api/src/helpers/pending_block.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0384-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-types/src/error/mod.rs` — The downstream diff for crates/rpc/rpc-eth-types/src/error/mod.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0388-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-types/src/logs_utils.rs` — The downstream diff for crates/rpc/rpc-eth-types/src/logs_utils.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0391-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-types/src/utils.rs` — The downstream diff for crates/rpc/rpc-eth-types/src/utils.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0452-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/storage/codecs/Cargo.toml` — The downstream diff for crates/storage/codecs/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0459-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/storage/codecs/src/alloy/passkey_signature.rs` — The downstream diff for crates/storage/codecs/src/alloy/passkey_signature.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0470-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/storage/codecs/src/lib.rs` — The downstream diff for crates/storage/codecs/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0483-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/storage/libmdbx-rs/src/codec.rs` — The downstream diff for crates/storage/libmdbx-rs/src/codec.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- ... `26` more atoms in `feature-map.json`.

Trace IDs by status:

- `exact`: file-0458-atom-0001
- `covered_by_upstream`: file-0455-atom-0001
- `intentionally_absent`: file-0212-atom-0001, file-0221-atom-0001
- `moved_to_dependency`: file-0062-atom-0001, file-0222-atom-0001, file-0226-atom-0001, file-0390-atom-0001
- `structural_equivalent`: file-0048-atom-0001, file-0078-atom-0001, file-0097-atom-0001, file-0107-atom-0001, file-0115-atom-0001, file-0144-atom-0001, file-0164-atom-0001, file-0174-atom-0001, file-0175-atom-0001, file-0194-atom-0001, file-0204-atom-0001, file-0255-atom-0001, file-0261-atom-0001, file-0372-atom-0001, file-0378-atom-0001, file-0384-atom-0001, file-0388-atom-0001, file-0391-atom-0001, file-0438-atom-0001, file-0444-atom-0001, file-0447-atom-0001, file-0449-atom-0001, file-0450-atom-0001, file-0452-atom-0001, file-0459-atom-0001, file-0470-atom-0001, file-0476-atom-0001, file-0483-atom-0001, file-0496-atom-0001, file-0546-atom-0001, file-0552-atom-0001, file-0555-atom-0001, file-0557-atom-0001, file-0559-atom-0001

## Precompile dispatch, SPC, and executor registry

Ritual precompile codecs and routing, SPC signature/verification support, block-verification helpers, TEE/executor registry reads, capability filtering, and executor-selection data.

- Counts: `21` atoms; `15` high-risk; `10` review-required; statuses `{'structural_equivalent': 14, 'exact': 7}`.
- Precision note: `14` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- No unresolved `missing` or `blocked` atoms remain after the first-pass precompile/SPC/block-verification review.

Representative atoms:

- `file-0300-atom-0001` `structural_equivalent` (high-risk, generic): `crates/ritual-block-verification/src/constants.rs` — Block-verification constants are preserved in the v2.2 port and extended with shared short-async verifier bounds.
- `file-0301-atom-0001` `structural_equivalent` (high-risk, generic): `crates/ritual-block-verification/src/error.rs` — Block-verification error classification is preserved with v2.2 grouped verifier variants.
- `file-0302-atom-0001` `structural_equivalent` (high-risk, generic): `crates/ritual-block-verification/src/lib.rs` — The old block-verifier wrapper is replaced by v2.2 function-based verifier hooks plus nodebuilder-owned EVM replay integration.
- `file-0249-atom-0001` `structural_equivalent` (generic): `crates/primitives-traits/src/transaction/error.rs` — Permanent precompile request eviction is preserved through Alloy EVM validation errors and the v2.2 hard-invalid pool path.
- `file-0299-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-block-verification/Cargo.toml` — The downstream diff for crates/ritual-block-verification/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0317-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-precompile-codecs/Cargo.toml` — The downstream diff for crates/ritual-precompile-codecs/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0318-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-precompile-codecs/src/dkms_key.rs` — The downstream diff for crates/ritual-precompile-codecs/src/dkms_key.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0319-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-precompile-codecs/src/error.rs` — The downstream diff for crates/ritual-precompile-codecs/src/error.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0320-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-precompile-codecs/src/executor.rs` — The downstream diff for crates/ritual-precompile-codecs/src/executor.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0322-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-precompile-codecs/src/lib.rs` — The downstream diff for crates/ritual-precompile-codecs/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0327-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-precompile-codecs/src/storage_ref.rs` — The downstream diff for crates/ritual-precompile-codecs/src/storage_ref.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0354-atom-0001` `exact` (high-risk): `crates/ritual-tee-registry-reader/src/constants.rs` — TEE registry reads cap service count at 10,000 to prevent unbounded allocation from corrupted contract state.
- `file-0354-atom-0002` `exact` (high-risk): `crates/ritual-tee-registry-reader/src/constants.rs` — TEE registry reads cap public key bytes at 128 to prevent malformed registry state from causing unbounded allocation.
- `file-0355-atom-0002` `exact` (high-risk): `crates/ritual-tee-registry-reader/src/error.rs` — TEE registry reads expose a typed service-count limit violation for corrupted or malicious registry state.
- `file-0355-atom-0003` `exact` (high-risk): `crates/ritual-tee-registry-reader/src/error.rs` — TEE registry reads expose a typed public-key length violation with executor context.
- `file-0355-atom-0004` `exact` (high-risk): `crates/ritual-tee-registry-reader/src/error.rs` — TEE registry reads expose a typed not-found error for missing executor addresses.
- ... `5` more atoms in `feature-map.json`.

Trace IDs by status:

- `exact`: file-0354-atom-0001, file-0354-atom-0002, file-0354-atom-0003, file-0355-atom-0002, file-0355-atom-0003, file-0355-atom-0004, file-0356-atom-0001
- `structural_equivalent`: file-0150-atom-0001, file-0178-atom-0001, file-0180-atom-0001, file-0249-atom-0001, file-0299-atom-0001, file-0300-atom-0001, file-0301-atom-0001, file-0302-atom-0001, file-0317-atom-0001, file-0318-atom-0001, file-0319-atom-0001, file-0320-atom-0001, file-0322-atom-0001, file-0327-atom-0001

## Transaction pool, admission, and ordering

Txpool async/scheduled admission, canonical async commitment finalization, and candidate ordering. Formatting-only network/storage/txpool records previously grouped here were reclassified as noise. Sequencing-rights crate atoms remain tracked in their existing scheduled/payload feature groups rather than this narrowed first pass.

- Counts: `4` atoms; `4` high-risk; `0` review-required; statuses `{'structural_equivalent': 4}`.
- Precision note: all four remaining atoms use generic coverage wording but now have destination evidence and adversarial review records.

Actionable gaps:

- None in this feature group after the first pass.

Representative atoms:

- `file-0521-atom-0001` `structural_equivalent` (high-risk, generic): `crates/transaction-pool/src/blocking_handlers.rs` — Old blocking handler behavior is split across txpool canonical async lifecycle processing plus payload/verifier scheduled obligation handling; the dormant `ritual-scheduling` blocking callback was intentionally not restored.
- `file-0524-atom-0001` `structural_equivalent` (high-risk, generic): `crates/transaction-pool/src/lib.rs` — Async lifecycle pool APIs and sender-lock admission are preserved through current v2.2 traits and `Pool` wrappers; old direct scheduled/async subpool APIs are replaced by canonical metadata and payload-derived scheduling.
- `file-0536-atom-0001` `structural_equivalent` (high-risk, generic): `crates/transaction-pool/src/pool/state.rs` — Normal candidate ordering remains the upstream pending/basefee/blob/queued model, while Ritual async/scheduled lifecycle moved out of `SubPool` variants.
- `file-0545-atom-0001` `structural_equivalent` (high-risk, generic): `crates/transaction-pool/tests/it/async_exec.rs` — The stale old integration test is replaced by `canonical_async_commitment_moves_original_to_async_pool` and existing gold1p async/precompile traffic evidence.

Trace IDs by status:

- `structural_equivalent`: file-0521-atom-0001, file-0524-atom-0001, file-0536-atom-0001, file-0545-atom-0001

## Core async execution and settlement

Short async transaction lifecycle: async-context feature plumbing, commitment/result state, settlement, fulfilled-original replay, pool/RPC/verifier hooks, SPC call handling, and async fee/wallet foundations.

- Counts: `105` atoms; `81` high-risk; `95` review-required; statuses `{'missing': 44, 'blocked': 3, 'intentionally_absent': 1, 'structural_equivalent': 37, 'moved_to_dependency': 9, 'exact': 8, 'noise': 1, 'covered_by_upstream': 2}`.
- Precision note: `65` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0022-atom-0001` `missing` (high-risk, review): `crates/chain-state/src/in_memory.rs` — CanonicalInMemoryState stores a blocking notifier alongside the async broadcast sender.
- `file-0022-atom-0003` `missing` (high-risk, review): `crates/chain-state/src/in_memory.rs` — Blocking canonical-state handlers run synchronously before async canonical-state notifications are broadcast.
- `file-0072-atom-0002` `missing` (high-risk, review): `crates/errors/Cargo.toml` — Enabling `reth-errors/async-context` forwards the feature to `reth-execution-errors`, exposing async-context behavior through this crate's public feature surface.
- `file-0077-atom-0001` `missing` (high-risk, review): `crates/ethereum/evm/Cargo.toml` — Adds a direct dependency on `revm-context` so this crate can compile its async-context-aware ethereum EVM configuration against `revm_context` types.
- `file-0077-atom-0003` `missing` (high-risk, review): `crates/ethereum/evm/Cargo.toml` — Exposes an `async-context` feature from `reth-evm-ethereum` and forwards it into `reth-evm` so async-aware execution can be enabled transitively.
- `file-0079-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/evm/src/execute.rs` — The downstream diff for crates/ethereum/evm/src/execute.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0081-atom-0005` `missing` (high-risk, review): `crates/ethereum/node/Cargo.toml` — The ethereum node crate directly provides the SPC verification bridge through `ritual-spc-verification`.
- `file-0082-atom-0001` `missing` (high-risk, review): `crates/ethereum/node/src/lib.rs` — Expose and compile the new `spc` submodule from `reth_node_ethereum` so the SPC verifier bridge becomes part of the crate surface.
- `file-0082-atom-0002` `missing` (high-risk, review): `crates/ethereum/node/src/lib.rs` — Re-export `SpcVerifierImpl` at the crate root so downstream code can import `reth_node_ethereum::SpcVerifierImpl` directly.
- `file-0084-atom-0002` `missing` (high-risk, review): `crates/ethereum/node/src/payload.rs` — The Ethereum node forces missing-payload resolution to race an empty payload fallback instead of awaiting the first in-progress payload, preventing consensus-client crashes/stalls wh...
- `file-0099-atom-0001` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — `reth-ethereum` exposes a public `async-context` Cargo feature.
- `file-0099-atom-0002` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — Enabling `reth-ethereum/async-context` must also enable the crate's optional `evm` feature set.
- `file-0099-atom-0003` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — Enabling `reth-ethereum/async-context` must forward the `async-context` feature into `reth-evm`.
- `file-0099-atom-0004` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — Enabling `reth-ethereum/async-context` must forward the `async-context` feature into `reth-evm-ethereum`.
- `file-0101-atom-0003` `missing` (high-risk, review): `crates/evm/Cargo.toml` — Building `reth-evm` with default features enables the async-context execution path by default.
- `file-0101-atom-0004` `missing` (high-risk, review): `crates/evm/Cargo.toml` — The `reth-evm` crate exposes an `async-context` feature that forwards all required async execution feature gates through alloy, revm, ethereum primitives, and execution errors.
- `file-0102-atom-0001` `missing` (high-risk, review): `crates/evm/execution-errors/Cargo.toml` — `reth-execution-errors` exposes an `async-context` feature that forwards to `alloy-evm/async-context`, allowing downstream feature chains to enable async-only block execution error v...
- `file-0106-atom-0001` `missing` (high-risk, review, generic): `crates/evm/src/async_context_tests.rs` — The downstream diff for crates/evm/src/async_context_tests.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- ... `30` more gap atoms in `feature-map.json`.

Representative atoms:

- `file-0022-atom-0001` `missing` (high-risk, review): `crates/chain-state/src/in_memory.rs` — CanonicalInMemoryState stores a blocking notifier alongside the async broadcast sender.
- `file-0022-atom-0003` `missing` (high-risk, review): `crates/chain-state/src/in_memory.rs` — Blocking canonical-state handlers run synchronously before async canonical-state notifications are broadcast.
- `file-0072-atom-0002` `missing` (high-risk, review): `crates/errors/Cargo.toml` — Enabling `reth-errors/async-context` forwards the feature to `reth-execution-errors`, exposing async-context behavior through this crate's public feature surface.
- `file-0077-atom-0001` `missing` (high-risk, review): `crates/ethereum/evm/Cargo.toml` — Adds a direct dependency on `revm-context` so this crate can compile its async-context-aware ethereum EVM configuration against `revm_context` types.
- `file-0077-atom-0003` `missing` (high-risk, review): `crates/ethereum/evm/Cargo.toml` — Exposes an `async-context` feature from `reth-evm-ethereum` and forwards it into `reth-evm` so async-aware execution can be enabled transitively.
- `file-0079-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/evm/src/execute.rs` — The downstream diff for crates/ethereum/evm/src/execute.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0081-atom-0005` `missing` (high-risk, review): `crates/ethereum/node/Cargo.toml` — The ethereum node crate directly provides the SPC verification bridge through `ritual-spc-verification`.
- `file-0082-atom-0001` `missing` (high-risk, review): `crates/ethereum/node/src/lib.rs` — Expose and compile the new `spc` submodule from `reth_node_ethereum` so the SPC verifier bridge becomes part of the crate surface.
- `file-0082-atom-0002` `missing` (high-risk, review): `crates/ethereum/node/src/lib.rs` — Re-export `SpcVerifierImpl` at the crate root so downstream code can import `reth_node_ethereum::SpcVerifierImpl` directly.
- `file-0084-atom-0002` `missing` (high-risk, review): `crates/ethereum/node/src/payload.rs` — The Ethereum node forces missing-payload resolution to race an empty payload fallback instead of awaiting the first in-progress payload, preventing consensus-client crashes/stalls wh...
- `file-0099-atom-0001` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — `reth-ethereum` exposes a public `async-context` Cargo feature.
- `file-0099-atom-0002` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — Enabling `reth-ethereum/async-context` must also enable the crate's optional `evm` feature set.
- `file-0099-atom-0003` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — Enabling `reth-ethereum/async-context` must forward the `async-context` feature into `reth-evm`.
- `file-0099-atom-0004` `missing` (high-risk, review): `crates/ethereum/reth/Cargo.toml` — Enabling `reth-ethereum/async-context` must forward the `async-context` feature into `reth-evm-ethereum`.
- `file-0101-atom-0003` `missing` (high-risk, review): `crates/evm/Cargo.toml` — Building `reth-evm` with default features enables the async-context execution path by default.
- `file-0101-atom-0004` `missing` (high-risk, review): `crates/evm/Cargo.toml` — The `reth-evm` crate exposes an `async-context` feature that forwards all required async execution feature gates through alloy, revm, ethereum primitives, and execution errors.
- ... `89` more atoms in `feature-map.json`.

Trace IDs by status:

- `blocked`: file-0108-atom-0001, file-0280-atom-0001, file-0288-atom-0001
- `covered_by_upstream`: file-0073-atom-0001, file-0073-atom-0002
- `exact`: file-0359-atom-0001, file-0359-atom-0002, file-0359-atom-0003, file-0359-atom-0004, file-0460-atom-0001, file-0460-atom-0002, file-0461-atom-0002, file-0466-atom-0001
- `intentionally_absent`: file-0077-atom-0002
- `missing`: file-0020-atom-0001, file-0022-atom-0001, file-0022-atom-0002, file-0022-atom-0003, file-0023-atom-0001, file-0024-atom-0001, file-0024-atom-0002, file-0025-atom-0001, file-0072-atom-0002, file-0077-atom-0001, file-0077-atom-0003, file-0079-atom-0001, file-0081-atom-0005, file-0082-atom-0001, file-0082-atom-0002, file-0084-atom-0002, file-0085-atom-0001, file-0099-atom-0001, file-0099-atom-0002, file-0099-atom-0003, file-0099-atom-0004, file-0101-atom-0003, file-0101-atom-0004, file-0102-atom-0001, file-0106-atom-0001, file-0110-atom-0001, file-0111-atom-0001, file-0273-atom-0001, file-0274-atom-0001, file-0289-atom-0001, file-0294-atom-0001, file-0295-atom-0001, file-0296-atom-0001, file-0298-atom-0001, file-0303-atom-0001, file-0346-atom-0001, file-0349-atom-0001, file-0350-atom-0001, file-0351-atom-0001, file-0365-atom-0001, file-0396-atom-0001, file-0410-atom-0001, file-0529-atom-0001, file-0538-atom-0001
- `moved_to_dependency`: file-0081-atom-0003, file-0081-atom-0004, file-0081-atom-0006, file-0101-atom-0001, file-0101-atom-0002, file-0287-atom-0001, file-0297-atom-0001, file-0348-atom-0001, file-0352-atom-0001
- `noise`: file-0072-atom-0001
- `structural_equivalent`: file-0080-atom-0001, file-0081-atom-0001, file-0081-atom-0002, file-0083-atom-0001, file-0185-atom-0001, file-0186-atom-0001, file-0187-atom-0001, file-0188-atom-0001, file-0193-atom-0001, file-0275-atom-0001, file-0276-atom-0001, file-0278-atom-0001, file-0279-atom-0001, file-0281-atom-0001, file-0284-atom-0001, file-0286-atom-0001, file-0290-atom-0001, file-0292-atom-0001, file-0315-atom-0001, file-0316-atom-0001, file-0321-atom-0001, file-0323-atom-0001, file-0325-atom-0001, file-0326-atom-0001, file-0343-atom-0001, file-0344-atom-0001, file-0395-atom-0001, file-0403-atom-0001, file-0424-atom-0001, file-0427-atom-0001, file-0462-atom-0001, file-0464-atom-0001, file-0468-atom-0001, file-0523-atom-0001, file-0532-atom-0001, file-0539-atom-0001, file-0540-atom-0001

## Long-running async delivery FSM

Two-phase long-running async flow: Phase 1 commitment settlement, delivery readiness, delivery result validation, and final settlement/delivery bookkeeping.

- Counts: `4` atoms; `4` high-risk; `3` review-required; statuses `{'missing': 1, 'moved_to_dependency': 1, 'structural_equivalent': 1, 'exact': 1}`.
- Precision note: `3` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0277-atom-0001` `missing` (high-risk, review, generic): `crates/ritual-async-fees/src/delivery.rs` — The downstream diff for crates/ritual-async-fees/src/delivery.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Representative atoms:

- `file-0277-atom-0001` `missing` (high-risk, review, generic): `crates/ritual-async-fees/src/delivery.rs` — The downstream diff for crates/ritual-async-fees/src/delivery.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0304-atom-0001` `moved_to_dependency` (high-risk, review, generic): `crates/ritual-block-verification/src/verifier.rs` — The downstream diff for crates/ritual-block-verification/src/verifier.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0324-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/ritual-precompile-codecs/src/long_running.rs` — The downstream diff for crates/ritual-precompile-codecs/src/long_running.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0461-atom-0001` `exact` (high-risk): `crates/storage/codecs/src/alloy/transaction/async_settlement.rs` — Storage codecs preserve the TxAsyncSettlement field layout for async settlement transaction compact encoding, with the Bytes input field last for Compact derive handling.

Trace IDs by status:

- `exact`: file-0461-atom-0001
- `missing`: file-0277-atom-0001
- `moved_to_dependency`: file-0304-atom-0001
- `structural_equivalent`: file-0324-atom-0001

## Scheduled transactions and missed-obligation verification

Scheduled transaction identity, Scheduler storage reads, predicate evaluation, missed-obligation synthesis, heartbeat/revival helpers, and builder/verifier parity for scheduled jobs.

- Counts: `81` atoms; `61` high-risk; `67` review-required; statuses `{'missing': 24, 'structural_equivalent': 26, 'exact': 16, 'moved_to_dependency': 12, 'noise': 3}`.
- Precision note: `56` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0087-atom-0006` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate depends on sequencing-rights logic to classify and reorder candidate transactions before execution.
- `file-0087-atom-0007` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate keeps heartbeat revival/tracking state in-process while building payloads.
- `file-0087-atom-0010` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate enables parallel transaction classification/preparation work using Rayon.
- `file-0087-atom-0013` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate adds `secp256k1` as a dev-dependency to support local SPC signature verification tests.
- `file-0089-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/collector.rs` — The downstream diff for crates/ethereum/payload/src/collector.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0093-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/unified_builder.rs` — The downstream diff for crates/ethereum/payload/src/unified_builder.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0313-atom-0001` `missing` (high-risk, review, generic): `crates/ritual-metrics/src/scheduling.rs` — The downstream diff for crates/ritual-metrics/src/scheduling.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0414-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/Cargo.toml` — The downstream diff for crates/scheduling/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0415-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/canonical.rs` — The downstream diff for crates/scheduling/src/canonical.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0417-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/events.rs` — The downstream diff for crates/scheduling/src/events.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0418-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/job.rs` — The downstream diff for crates/scheduling/src/job.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0419-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/lib.rs` — The downstream diff for crates/scheduling/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0421-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/singleton.rs` — The downstream diff for crates/scheduling/src/singleton.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0423-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/types.rs` — The downstream diff for crates/scheduling/src/types.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0087-atom-0005` `missing` (review): `crates/ethereum/payload/Cargo.toml` — The payload crate adds Ritual metrics/tracing instrumentation support.
- `file-0307-atom-0001` `missing` (review, generic): `crates/ritual-heartbeat-tracker/Cargo.toml` — The downstream diff for crates/ritual-heartbeat-tracker/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0308-atom-0001` `missing` (review, generic): `crates/ritual-heartbeat-tracker/src/events.rs` — The downstream diff for crates/ritual-heartbeat-tracker/src/events.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0309-atom-0001` `missing` (review, generic): `crates/ritual-heartbeat-tracker/src/lib.rs` — The downstream diff for crates/ritual-heartbeat-tracker/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- ... `6` more gap atoms in `feature-map.json`.

Representative atoms:

- `file-0087-atom-0006` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate depends on sequencing-rights logic to classify and reorder candidate transactions before execution.
- `file-0087-atom-0007` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate keeps heartbeat revival/tracking state in-process while building payloads.
- `file-0087-atom-0010` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate enables parallel transaction classification/preparation work using Rayon.
- `file-0087-atom-0013` `missing` (high-risk, review): `crates/ethereum/payload/Cargo.toml` — The payload crate adds `secp256k1` as a dev-dependency to support local SPC signature verification tests.
- `file-0089-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/collector.rs` — The downstream diff for crates/ethereum/payload/src/collector.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0093-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/unified_builder.rs` — The downstream diff for crates/ethereum/payload/src/unified_builder.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0313-atom-0001` `missing` (high-risk, review, generic): `crates/ritual-metrics/src/scheduling.rs` — The downstream diff for crates/ritual-metrics/src/scheduling.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0414-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/Cargo.toml` — The downstream diff for crates/scheduling/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0415-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/canonical.rs` — The downstream diff for crates/scheduling/src/canonical.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0417-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/events.rs` — The downstream diff for crates/scheduling/src/events.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0418-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/job.rs` — The downstream diff for crates/scheduling/src/job.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0419-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/lib.rs` — The downstream diff for crates/scheduling/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0421-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/singleton.rs` — The downstream diff for crates/scheduling/src/singleton.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0423-atom-0001` `missing` (high-risk, review, generic): `crates/scheduling/src/types.rs` — The downstream diff for crates/scheduling/src/types.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0087-atom-0005` `missing` (review): `crates/ethereum/payload/Cargo.toml` — The payload crate adds Ritual metrics/tracing instrumentation support.
- `file-0307-atom-0001` `missing` (review, generic): `crates/ritual-heartbeat-tracker/Cargo.toml` — The downstream diff for crates/ritual-heartbeat-tracker/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- ... `65` more atoms in `feature-map.json`.

Trace IDs by status:

- `exact`: file-0087-atom-0003, file-0087-atom-0004, file-0291-atom-0001, file-0291-atom-0002, file-0291-atom-0003, file-0293-atom-0001, file-0331-atom-0001, file-0331-atom-0002, file-0334-atom-0001, file-0355-atom-0001, file-0358-atom-0001, file-0358-atom-0002, file-0358-atom-0003, file-0358-atom-0004, file-0467-atom-0001, file-0467-atom-0002
- `missing`: file-0087-atom-0005, file-0087-atom-0006, file-0087-atom-0007, file-0087-atom-0010, file-0087-atom-0013, file-0089-atom-0001, file-0093-atom-0001, file-0307-atom-0001, file-0308-atom-0001, file-0309-atom-0001, file-0313-atom-0001, file-0335-atom-0001, file-0336-atom-0001, file-0337-atom-0001, file-0338-atom-0001, file-0339-atom-0001, file-0342-atom-0001, file-0414-atom-0001, file-0415-atom-0001, file-0417-atom-0001, file-0418-atom-0001, file-0419-atom-0001, file-0421-atom-0001, file-0423-atom-0001
- `moved_to_dependency`: file-0087-atom-0008, file-0091-atom-0001, file-0098-atom-0001, file-0248-atom-0001, file-0250-atom-0001, file-0283-atom-0001, file-0340-atom-0001, file-0341-atom-0001, file-0416-atom-0001, file-0420-atom-0001, file-0422-atom-0001, file-0535-atom-0001
- `noise`: file-0087-atom-0001, file-0087-atom-0009, file-0087-atom-0012
- `structural_equivalent`: file-0087-atom-0002, file-0087-atom-0011, file-0163-atom-0001, file-0282-atom-0001, file-0285-atom-0001, file-0328-atom-0001, file-0329-atom-0001, file-0330-atom-0001, file-0332-atom-0001, file-0333-atom-0001, file-0366-atom-0001, file-0389-atom-0001, file-0401-atom-0001, file-0408-atom-0001, file-0412-atom-0001, file-0463-atom-0001, file-0465-atom-0001, file-0469-atom-0001, file-0514-atom-0001, file-0525-atom-0001, file-0526-atom-0001, file-0537-atom-0001, file-0541-atom-0001, file-0542-atom-0001, file-0543-atom-0001, file-0550-atom-0001

## Payload building, execution, and consensus validation

Payload builder/execution hooks, block verification, engine-tree behavior, consensus validation, chain-spec constants, extra_data policy, block rewards, and genesis-derived behavior.

- Counts: `43` atoms; `28` high-risk; `42` review-required; statuses `{'missing': 12, 'blocked': 1, 'intentionally_absent': 2, 'exact': 1, 'structural_equivalent': 24, 'moved_to_dependency': 3}`.
- Precision note: `32` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0026-atom-0001` `missing` (high-risk, review): `crates/chainspec/src/api.rs` — EthChainSpec exposes an optional per-chain maximum header extra_data size, with None meaning unbounded.
- `file-0027-atom-0001` `missing` (high-risk, review): `crates/chainspec/src/constants.rs` — Summit chains use a custom 7-field deposit event topic for Ed25519 node keys plus BLS consensus keys.
- `file-0028-atom-0001` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — ChainSpec stores a per-chain optional header extra_data size limit, defaulting Ethereum networks to MAXIMUM_EXTRA_DATA_SIZE.
- `file-0028-atom-0002` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — Genesis-derived deposit contracts use the Summit deposit event topic instead of the Ethereum mainnet deposit topic.
- `file-0028-atom-0003` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — Chain specs built from genesis files disable the Ethereum extra_data size cap so Ritual/Summit chains can embed CL snapshots for recovery.
- `file-0028-atom-0004` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — ChainSpec stores an optional post-merge validator/proposer base block reward parsed from genesis and builder configuration.
- `file-0028-atom-0005` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — ChainSpec computes effective block rewards: standard pre-merge rewards and configured custom post-merge rewards, and exposes the custom reward via EthExecutorSpec.
- `file-0084-atom-0001` `missing` (high-risk, review): `crates/ethereum/node/src/payload.rs` — The Ethereum node propagates the configured maximum block tx-list size cap into the payload builder so block construction enforces `max_block_size_bytes`.
- `file-0088-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/bundle.rs` — The downstream diff for crates/ethereum/payload/src/bundle.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0094-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/unified_execution.rs` — The downstream diff for crates/ethereum/payload/src/unified_execution.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0528-atom-0001` `blocked` (high-risk, review, generic): `crates/transaction-pool/src/pool/async_pool.rs` — The downstream diff for crates/transaction-pool/src/pool/async_pool.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0047-atom-0001` `intentionally_absent` (review): `crates/consensus/common/Cargo.toml` — `reth-consensus-common` adds a direct workspace dependency on `tracing` so the crate can compile downstream-only tracing macros used in its validation code.
- `file-0056-atom-0001` `intentionally_absent` (review): `crates/engine/tree/Cargo.toml` — The downstream engine-tree crate adds a workspace dependency on `ritual-metrics` so Ritual-specific metrics instrumentation in this crate can compile.
- `file-0206-atom-0001` `missing` (review, generic): `crates/optimism/chainspec/src/lib.rs` — The downstream diff for crates/optimism/chainspec/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0211-atom-0001` `missing` (review, generic): `crates/optimism/consensus/src/lib.rs` — The downstream diff for crates/optimism/consensus/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Representative atoms:

- `file-0026-atom-0001` `missing` (high-risk, review): `crates/chainspec/src/api.rs` — EthChainSpec exposes an optional per-chain maximum header extra_data size, with None meaning unbounded.
- `file-0027-atom-0001` `missing` (high-risk, review): `crates/chainspec/src/constants.rs` — Summit chains use a custom 7-field deposit event topic for Ed25519 node keys plus BLS consensus keys.
- `file-0028-atom-0001` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — ChainSpec stores a per-chain optional header extra_data size limit, defaulting Ethereum networks to MAXIMUM_EXTRA_DATA_SIZE.
- `file-0028-atom-0002` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — Genesis-derived deposit contracts use the Summit deposit event topic instead of the Ethereum mainnet deposit topic.
- `file-0028-atom-0003` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — Chain specs built from genesis files disable the Ethereum extra_data size cap so Ritual/Summit chains can embed CL snapshots for recovery.
- `file-0028-atom-0004` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — ChainSpec stores an optional post-merge validator/proposer base block reward parsed from genesis and builder configuration.
- `file-0028-atom-0005` `missing` (high-risk, review): `crates/chainspec/src/spec.rs` — ChainSpec computes effective block rewards: standard pre-merge rewards and configured custom post-merge rewards, and exposes the custom reward via EthExecutorSpec.
- `file-0084-atom-0001` `missing` (high-risk, review): `crates/ethereum/node/src/payload.rs` — The Ethereum node propagates the configured maximum block tx-list size cap into the payload builder so block construction enforces `max_block_size_bytes`.
- `file-0088-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/bundle.rs` — The downstream diff for crates/ethereum/payload/src/bundle.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0094-atom-0001` `missing` (high-risk, review, generic): `crates/ethereum/payload/src/unified_execution.rs` — The downstream diff for crates/ethereum/payload/src/unified_execution.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0528-atom-0001` `blocked` (high-risk, review, generic): `crates/transaction-pool/src/pool/async_pool.rs` — The downstream diff for crates/transaction-pool/src/pool/async_pool.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0047-atom-0001` `intentionally_absent` (review): `crates/consensus/common/Cargo.toml` — `reth-consensus-common` adds a direct workspace dependency on `tracing` so the crate can compile downstream-only tracing macros used in its validation code.
- `file-0056-atom-0001` `intentionally_absent` (review): `crates/engine/tree/Cargo.toml` — The downstream engine-tree crate adds a workspace dependency on `ritual-metrics` so Ritual-specific metrics instrumentation in this crate can compile.
- `file-0206-atom-0001` `missing` (review, generic): `crates/optimism/chainspec/src/lib.rs` — The downstream diff for crates/optimism/chainspec/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0211-atom-0001` `missing` (review, generic): `crates/optimism/consensus/src/lib.rs` — The downstream diff for crates/optimism/consensus/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0054-atom-0001` `exact` (high-risk): `crates/engine/local/src/payload.rs` — The local Ethereum payload attributes builder must explicitly set `EthPayloadAttributes.extra_data` to `None` when constructing payload attributes.
- ... `27` more atoms in `feature-map.json`.

Trace IDs by status:

- `blocked`: file-0528-atom-0001
- `exact`: file-0054-atom-0001
- `intentionally_absent`: file-0047-atom-0001, file-0056-atom-0001
- `missing`: file-0026-atom-0001, file-0027-atom-0001, file-0028-atom-0001, file-0028-atom-0002, file-0028-atom-0003, file-0028-atom-0004, file-0028-atom-0005, file-0084-atom-0001, file-0088-atom-0001, file-0094-atom-0001, file-0206-atom-0001, file-0211-atom-0001
- `moved_to_dependency`: file-0218-atom-0001, file-0311-atom-0001, file-0314-atom-0001
- `structural_equivalent`: file-0059-atom-0001, file-0064-atom-0001, file-0074-atom-0001, file-0076-atom-0001, file-0090-atom-0001, file-0092-atom-0001, file-0136-atom-0001, file-0189-atom-0001, file-0190-atom-0001, file-0191-atom-0001, file-0192-atom-0001, file-0196-atom-0001, file-0197-atom-0001, file-0200-atom-0001, file-0201-atom-0001, file-0231-atom-0001, file-0232-atom-0001, file-0233-atom-0001, file-0236-atom-0001, file-0364-atom-0001, file-0370-atom-0001, file-0402-atom-0001, file-0407-atom-0001, file-0527-atom-0001

## RPC and external API surface

Ritual RPC namespace, async result submission, txpool/RPC API extensions, pubsub surfaces, and externally visible request/response compatibility.

- Counts: `14` atoms; `9` high-risk; `14` review-required; statuses `{'missing': 2, 'structural_equivalent': 12}`.
- Precision note: `14` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0305-atom-0001` `missing` (review, generic): `crates/ritual-blocking-pubsub/Cargo.toml` — The downstream diff for crates/ritual-blocking-pubsub/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0306-atom-0001` `missing` (review, generic): `crates/ritual-blocking-pubsub/src/lib.rs` — The downstream diff for crates/ritual-blocking-pubsub/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Representative atoms:

- `file-0305-atom-0001` `missing` (review, generic): `crates/ritual-blocking-pubsub/Cargo.toml` — The downstream diff for crates/ritual-blocking-pubsub/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0306-atom-0001` `missing` (review, generic): `crates/ritual-blocking-pubsub/src/lib.rs` — The downstream diff for crates/ritual-blocking-pubsub/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0363-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-api/Cargo.toml` — The downstream diff for crates/rpc/rpc-api/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0375-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-api/src/helpers/call.rs` — The downstream diff for crates/rpc/rpc-eth-api/src/helpers/call.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0376-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-api/src/helpers/estimate.rs` — The downstream diff for crates/rpc/rpc-eth-api/src/helpers/estimate.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0377-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-api/src/helpers/fee.rs` — The downstream diff for crates/rpc/rpc-eth-api/src/helpers/fee.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0385-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-eth-types/src/fee_history.rs` — The downstream diff for crates/rpc/rpc-eth-types/src/fee_history.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0393-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc-server-types/src/module.rs` — The downstream diff for crates/rpc/rpc-server-types/src/module.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0398-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc/src/eth/bundle.rs` — The downstream diff for crates/rpc/rpc/src/eth/bundle.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0399-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc/src/eth/filter.rs` — The downstream diff for crates/rpc/rpc/src/eth/filter.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0413-atom-0001` `structural_equivalent` (high-risk, review, generic): `crates/rpc/rpc/src/validation.rs` — The downstream diff for crates/rpc/rpc/src/validation.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0494-atom-0001` `structural_equivalent` (review, generic): `crates/storage/provider/Cargo.toml` — The downstream diff for crates/storage/provider/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0495-atom-0001` `structural_equivalent` (review, generic): `crates/storage/provider/src/providers/blockchain_provider.rs` — The downstream diff for crates/storage/provider/src/providers/blockchain_provider.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0504-atom-0001` `structural_equivalent` (review, generic): `crates/storage/provider/src/test_utils/mock.rs` — The downstream diff for crates/storage/provider/src/test_utils/mock.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Trace IDs by status:

- `missing`: file-0305-atom-0001, file-0306-atom-0001
- `structural_equivalent`: file-0363-atom-0001, file-0375-atom-0001, file-0376-atom-0001, file-0377-atom-0001, file-0385-atom-0001, file-0393-atom-0001, file-0398-atom-0001, file-0399-atom-0001, file-0413-atom-0001, file-0494-atom-0001, file-0495-atom-0001, file-0504-atom-0001

## Storage, provider, and database infrastructure

Provider traits, database/static-file surfaces, MDBX/nippy/db-api changes, state provider plumbing, and canonical-state subscription infrastructure.

- Counts: `8` atoms; `0` high-risk; `8` review-required; statuses `{'missing': 1, 'structural_equivalent': 7}`.
- Precision note: `8` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0268-atom-0001` `missing` (review, generic): `crates/ress/protocol/src/provider.rs` — The downstream diff for crates/ress/protocol/src/provider.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Representative atoms:

- `file-0268-atom-0001` `missing` (review, generic): `crates/ress/protocol/src/provider.rs` — The downstream diff for crates/ress/protocol/src/provider.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0253-atom-0001` `structural_equivalent` (review, generic): `crates/prune/prune/src/pruner.rs` — The downstream diff for crates/prune/prune/src/pruner.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0263-atom-0001` `structural_equivalent` (review, generic): `crates/prune/prune/src/segments/user/storage_history.rs` — The downstream diff for crates/prune/prune/src/segments/user/storage_history.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0475-atom-0001` `structural_equivalent` (review, generic): `crates/storage/db-common/src/db_tool/mod.rs` — The downstream diff for crates/storage/db-common/src/db_tool/mod.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0498-atom-0001` `structural_equivalent` (review, generic): `crates/storage/provider/src/providers/database/provider.rs` — The downstream diff for crates/storage/provider/src/providers/database/provider.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0499-atom-0001` `structural_equivalent` (review, generic): `crates/storage/provider/src/providers/state/historical.rs` — The downstream diff for crates/storage/provider/src/providers/state/historical.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0502-atom-0001` `structural_equivalent` (review, generic): `crates/storage/provider/src/providers/static_file/manager.rs` — The downstream diff for crates/storage/provider/src/providers/static_file/manager.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0503-atom-0001` `structural_equivalent` (review, generic): `crates/storage/provider/src/providers/static_file/writer.rs` — The downstream diff for crates/storage/provider/src/providers/static_file/writer.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Trace IDs by status:

- `missing`: file-0268-atom-0001
- `structural_equivalent`: file-0253-atom-0001, file-0263-atom-0001, file-0475-atom-0001, file-0498-atom-0001, file-0499-atom-0001, file-0502-atom-0001, file-0503-atom-0001

## Network and P2P compatibility

P2P/discovery/network/download/wire compatibility changes and any network test fixture behavior retained or refactored by v2.2.

- Counts: `27` atoms; `0` high-risk; `25` review-required; statuses `{'missing': 9, 'structural_equivalent': 15, 'covered_by_upstream': 1, 'exact': 1, 'moved_to_dependency': 1}`.
- Precision note: `25` atoms in this group use generic coverage wording and should be refined from source/destination evidence before code changes.

Actionable gaps:

- `file-0071-atom-0001` `missing` (review, generic): `crates/era/src/era1_file.rs` — The downstream diff for crates/era/src/era1_file.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0157-atom-0001` `missing` (review): `crates/net/network/Cargo.toml` — The downstream `reth-network` crate adds a direct workspace dependency on `ritual-metrics` so Ritual-specific network transaction metric/logging hooks can compile and link.
- `file-0207-atom-0001` `missing` (review, generic): `crates/optimism/cli/src/commands/import.rs` — The downstream diff for crates/optimism/cli/src/commands/import.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0242-atom-0001` `missing` (review, generic): `crates/primitives-traits/Cargo.toml` — The downstream diff for crates/primitives-traits/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0257-atom-0001` `missing` (review, generic): `crates/prune/prune/src/segments/static_file/headers.rs` — The downstream diff for crates/prune/prune/src/segments/static_file/headers.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0258-atom-0001` `missing` (review, generic): `crates/prune/prune/src/segments/static_file/transactions.rs` — The downstream diff for crates/prune/prune/src/segments/static_file/transactions.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0310-atom-0001` `missing` (review, generic): `crates/ritual-metrics/Cargo.toml` — The downstream diff for crates/ritual-metrics/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0312-atom-0001` `missing` (review, generic): `crates/ritual-metrics/src/lib.rs` — The downstream diff for crates/ritual-metrics/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0513-atom-0001` `missing` (review, generic): `crates/tracing/src/ritual_router.rs` — The downstream diff for crates/tracing/src/ritual_router.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Representative atoms:

- `file-0071-atom-0001` `missing` (review, generic): `crates/era/src/era1_file.rs` — The downstream diff for crates/era/src/era1_file.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0157-atom-0001` `missing` (review): `crates/net/network/Cargo.toml` — The downstream `reth-network` crate adds a direct workspace dependency on `ritual-metrics` so Ritual-specific network transaction metric/logging hooks can compile and link.
- `file-0207-atom-0001` `missing` (review, generic): `crates/optimism/cli/src/commands/import.rs` — The downstream diff for crates/optimism/cli/src/commands/import.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0242-atom-0001` `missing` (review, generic): `crates/primitives-traits/Cargo.toml` — The downstream diff for crates/primitives-traits/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0257-atom-0001` `missing` (review, generic): `crates/prune/prune/src/segments/static_file/headers.rs` — The downstream diff for crates/prune/prune/src/segments/static_file/headers.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0258-atom-0001` `missing` (review, generic): `crates/prune/prune/src/segments/static_file/transactions.rs` — The downstream diff for crates/prune/prune/src/segments/static_file/transactions.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0310-atom-0001` `missing` (review, generic): `crates/ritual-metrics/Cargo.toml` — The downstream diff for crates/ritual-metrics/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0312-atom-0001` `missing` (review, generic): `crates/ritual-metrics/src/lib.rs` — The downstream diff for crates/ritual-metrics/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0513-atom-0001` `missing` (review, generic): `crates/tracing/src/ritual_router.rs` — The downstream diff for crates/tracing/src/ritual_router.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0042-atom-0001` `structural_equivalent` (review, generic): `crates/cli/commands/src/stage/run.rs` — The downstream diff for crates/cli/commands/src/stage/run.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0050-atom-0001` `structural_equivalent` (review, generic): `crates/e2e-test-utils/src/network.rs` — The downstream diff for crates/e2e-test-utils/src/network.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0073-atom-0003` `covered_by_upstream`: `crates/errors/src/error.rs` — The file stops enforcing that `BlockExecutionError` must be exactly 56 bytes on x86_64.
- `file-0131-atom-0001` `structural_equivalent` (review, generic): `crates/net/downloaders/src/bodies/bodies.rs` — The downstream diff for crates/net/downloaders/src/bodies/bodies.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0159-atom-0001` `structural_equivalent` (review, generic): `crates/net/network/src/error.rs` — The downstream diff for crates/net/network/src/error.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0165-atom-0001` `structural_equivalent` (review, generic): `crates/net/network/src/peers.rs` — The downstream diff for crates/net/network/src/peers.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0169-atom-0001` `structural_equivalent` (review, generic): `crates/net/network/src/state.rs` — The downstream diff for crates/net/network/src/state.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- ... `11` more atoms in `feature-map.json`.

Trace IDs by status:

- `covered_by_upstream`: file-0073-atom-0003
- `exact`: file-0357-atom-0001
- `missing`: file-0071-atom-0001, file-0157-atom-0001, file-0207-atom-0001, file-0242-atom-0001, file-0257-atom-0001, file-0258-atom-0001, file-0310-atom-0001, file-0312-atom-0001, file-0513-atom-0001
- `moved_to_dependency`: file-0431-atom-0001
- `structural_equivalent`: file-0042-atom-0001, file-0050-atom-0001, file-0131-atom-0001, file-0159-atom-0001, file-0165-atom-0001, file-0169-atom-0001, file-0172-atom-0001, file-0199-atom-0001, file-0259-atom-0001, file-0262-atom-0001, file-0264-atom-0001, file-0353-atom-0001, file-0511-atom-0001, file-0512-atom-0001, file-0561-atom-0001