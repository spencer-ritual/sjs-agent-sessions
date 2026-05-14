# Functionality-Flow Atom Curation Report

- Method: retraced documented flows against downstream source files; markdown sections were used only as flow labels.
- Existing functionality-flow atoms replaced: 0
- Raw grounded candidates: 53
- Promoted raw rows: 53
- Curated grouped atoms: 53
- Inserted atoms: 53

## Dropped Or Covered By Reason
- `promote`: 53

## Inserted By Source Path
- `crates/ethereum/payload/src/lib.rs`: 14
- `crates/ritual-precompile-codecs/src/long_running.rs`: 7
- `crates/ritual-async/src/validation.rs`: 5
- `crates/ritual-scheduled-verification/src/lib.rs`: 5
- `crates/rpc/rpc/src/async_tx_validator.rs`: 4
- `crates/ritual-async-fees/src/lib.rs`: 3
- `crates/ritual-spc-signature/src/lib.rs`: 3
- `crates/transaction-pool/src/pool/async_pool.rs`: 3
- `crates/ritual-precompile-codecs/src/persistent_agent.rs`: 2
- `crates/ritual-precompile-addresses/src/lib.rs`: 1
- `crates/ritual-precompile-codecs/src/http_call.rs`: 1
- `crates/ritual-precompile-codecs/src/llm_call.rs`: 1
- `crates/ritual-precompile-codecs/src/sovereign_agent.rs`: 1
- `crates/storage/codecs/src/alloy/transaction/async_settlement.rs`: 1
- `crates/storage/codecs/src/alloy/transaction/txtype.rs`: 1
- `crates/storage/codecs/src/alloy/transaction/passkey.rs`: 1

## Grounding Rule
Every promoted atom includes a `source_snippet` read from `/home/ritual/repos/ritual-reth-internal` at the owning downstream `source_path`; no promoted atom uses the markdown body as its evidence snippet.
