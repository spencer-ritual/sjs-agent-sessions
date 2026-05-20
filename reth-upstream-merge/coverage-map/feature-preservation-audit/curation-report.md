# Curated Feature-Preservation Atom Insertion Report

- Raw feature candidates: 132
- Promoted raw rows: 101
- Canonical grouped atoms inserted: 83
- Dropped/demoted rows: 31
- covered_by_existing_atom: 7
- drop_noise: 1
- drop_port_inventory: 8
- drop_validation_gate: 15
- promote: 101

## Inserted Files

- `coverage-map/files/file-0026.json` `crates/chainspec/src/api.rs`: 1 feature atom(s)
- `coverage-map/files/file-0028.json` `crates/chainspec/src/spec.rs`: 1 feature atom(s)
- `coverage-map/files/file-0092.json` `crates/ethereum/payload/src/lib.rs`: 18 feature atom(s)
- `coverage-map/files/file-0108.json` `crates/evm/src/lib.rs`: 1 feature atom(s)
- `coverage-map/files/file-0276.json` `crates/ritual-async-fees/src/constants.rs`: 1 feature atom(s)
- `coverage-map/files/file-0280.json` `crates/ritual-async-fees/src/lib.rs`: 3 feature atom(s)
- `coverage-map/files/file-0292.json` `crates/ritual-async-registry/src/lib.rs`: 2 feature atom(s)
- `coverage-map/files/file-0296.json` `crates/ritual-async/src/lib.rs`: 3 feature atom(s)
- `coverage-map/files/file-0304.json` `crates/ritual-block-verification/src/verifier.rs`: 3 feature atom(s)
- `coverage-map/files/file-0309.json` `crates/ritual-heartbeat-tracker/src/lib.rs`: 3 feature atom(s)
- `coverage-map/files/file-0311.json` `crates/ritual-metrics/src/block.rs`: 1 feature atom(s)
- `coverage-map/files/file-0316.json` `crates/ritual-precompile-addresses/src/lib.rs`: 7 feature atom(s)
- `coverage-map/files/file-0332.json` `crates/ritual-scheduled-verification/src/lib.rs`: 13 feature atom(s)
- `coverage-map/files/file-0333.json` `crates/ritual-scheduled-verification/src/predicate.rs`: 2 feature atom(s)
- `coverage-map/files/file-0342.json` `crates/ritual-sequencing-rights/src/types.rs`: 1 feature atom(s)
- `coverage-map/files/file-0365.json` `crates/rpc/rpc-api/src/ritual.rs`: 1 feature atom(s)
- `coverage-map/files/file-0396.json` `crates/rpc/rpc/src/async_tx_validator.rs`: 3 feature atom(s)
- `coverage-map/files/file-0415.json` `crates/scheduling/src/canonical.rs`: 3 feature atom(s)
- `coverage-map/files/file-0459.json` `crates/storage/codecs/src/alloy/passkey_signature.rs`: 3 feature atom(s)
- `coverage-map/files/file-0468.json` `crates/storage/codecs/src/alloy/transaction/spc_call.rs`: 1 feature atom(s)
- `coverage-map/files/file-0513.json` `crates/tracing/src/ritual_router.rs`: 2 feature atom(s)
- `coverage-map/files/file-0528.json` `crates/transaction-pool/src/pool/async_pool.rs`: 2 feature atom(s)
- `coverage-map/files/file-0537.json` `crates/transaction-pool/src/pool/txpool.rs`: 8 feature atom(s)

## Heuristic

- Start from `feature-preservation-map.md` preserve and PR-preserve/do-not-preserve claims; validation-only lines are evidence, not canonical behavior atoms.
- Drop broad port-inventory bullets and claims already covered by specific canonical atoms.
- Group related feature claims by subsystem behavior family and source path before insertion.
- Mark inserted feature atoms as `missing` unless the claim is a negative/absence invariant, which is `blocked` until absence evidence is attached.
