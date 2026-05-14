# Feature Coverage Map

Generated from current `files/file-*.json` atom records after the feature-ordered v2.2 pass.

| Feature | Atoms | High Risk | Review Required | Status Counts | Generic/Broad Atoms |
| --- | ---: | ---: | ---: | --- | ---: |
| Transaction identity, wire encoding, and storage codecs | 44 | 16 | 41 | `{'structural_equivalent': 35, 'blocked': 2, 'intentionally_absent': 4, 'moved_to_dependency': 1, 'covered_by_upstream': 1, 'exact': 1}` | 42 |
| Precompile dispatch, SPC, and executor registry | 65 | 60 | 55 | `{'structural_equivalent': 36, 'blocked': 6, 'exact': 19, 'intentionally_absent': 3, 'renamed_exact': 1}` | 24 |
| Transaction pool, admission, and ordering | 13 | 13 | 13 | `{'structural_equivalent': 12, 'exact': 1}` | 10 |
| Core async execution and settlement | 152 | 125 | 128 | `{'structural_equivalent': 96, 'blocked': 15, 'noise': 1, 'covered_by_upstream': 2, 'intentionally_absent': 19, 'moved_to_dependency': 4, 'exact': 15}` | 84 |
| Long-running async delivery FSM | 88 | 88 | 84 | `{'structural_equivalent': 71, 'blocked': 6, 'exact': 6, 'intentionally_absent': 5}` | 19 |
| Scheduled transactions and missed-obligation verification | 224 | 196 | 195 | `{'noise': 3, 'structural_equivalent': 74, 'exact': 49, 'intentionally_absent': 74, 'moved_to_dependency': 1, 'blocked': 23}` | 114 |
| Payload building, execution, and consensus validation | 54 | 39 | 51 | `{'structural_equivalent': 37, 'blocked': 4, 'moved_to_dependency': 2, 'intentionally_absent': 9, 'exact': 2}` | 38 |
| RPC and external API surface | 32 | 27 | 30 | `{'blocked': 10, 'structural_equivalent': 18, 'exact': 2, 'intentionally_absent': 2}` | 23 |
| Storage, provider, and database infrastructure | 19 | 11 | 17 | `{'blocked': 2, 'structural_equivalent': 13, 'noise': 1, 'moved_to_dependency': 1, 'exact': 2}` | 10 |
| Network and P2P compatibility | 28 | 1 | 22 | `{'structural_equivalent': 16, 'covered_by_upstream': 1, 'intentionally_absent': 5, 'noise': 3, 'blocked': 2, 'exact': 1}` | 26 |

## Transaction identity, wire encoding, and storage codecs

Custom transaction types, RLP/hash/signature identity, runtime-field boundaries, receipts, storage compact codecs, and persistent DB encoding rules.

- Counts: `44` atoms; `16` high-risk; `41` review-required; statuses `{'structural_equivalent': 35, 'blocked': 2, 'intentionally_absent': 4, 'moved_to_dependency': 1, 'covered_by_upstream': 1, 'exact': 1}`.

Actionable gaps:
- `file-0062-atom-0001` `blocked`: `crates/engine/tree/src/tree/cached_state.rs` — The downstream diff for crates/engine/tree/src/tree/cached_state.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0427-atom-0002` `blocked`: `crates/stages/api/src/pipeline/mod.rs` — PR preservation `#301` `fix-onnx-blocking-verification-download` keeps live downstream behavior: bounded pipeline retry for transient ONNX verification misses before unwind/escalation.

Representative atoms:
- `file-0048-atom-0001` `structural_equivalent`: `crates/consensus/common/src/validation.rs` — The downstream diff for crates/consensus/common/src/validation.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0078-atom-0001` `structural_equivalent`: `crates/ethereum/evm/src/build.rs` — The downstream diff for crates/ethereum/evm/src/build.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0097-atom-0001` `structural_equivalent`: `crates/ethereum/primitives/src/receipt.rs` — The downstream diff for crates/ethereum/primitives/src/receipt.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0458-atom-0001` `exact`: `crates/storage/codecs/src/alloy/mod.rs` — The alloy codec module exports the `passkey_signature` compact codec module alongside the existing alloy codec submodules.
- `file-0390-atom-0001` `moved_to_dependency`: `crates/rpc/rpc-eth-types/src/revm_utils.rs` — The downstream diff for crates/rpc/rpc-eth-types/src/revm_utils.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0455-atom-0001` `covered_by_upstream`: `crates/storage/codecs/derive/src/compact/mod.rs` — The downstream diff for crates/storage/codecs/derive/src/compact/mod.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0212-atom-0001` `intentionally_absent`: `crates/optimism/consensus/src/proof.rs` — The downstream diff for crates/optimism/consensus/src/proof.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0221-atom-0001` `intentionally_absent`: `crates/optimism/primitives/src/receipt.rs` — The downstream diff for crates/optimism/primitives/src/receipt.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0222-atom-0001` `intentionally_absent`: `crates/optimism/primitives/src/transaction/signed.rs` — The downstream diff for crates/optimism/primitives/src/transaction/signed.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0062-atom-0001` `blocked`: `crates/engine/tree/src/tree/cached_state.rs` — The downstream diff for crates/engine/tree/src/tree/cached_state.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0427-atom-0002` `blocked`: `crates/stages/api/src/pipeline/mod.rs` — PR preservation `#301` `fix-onnx-blocking-verification-download` keeps live downstream behavior: bounded pipeline retry for transient ONNX verification misses before unwind/escalation.

Trace IDs by status:

- `blocked`: file-0062-atom-0001, file-0427-atom-0002
- `covered_by_upstream`: file-0455-atom-0001
- `exact`: file-0458-atom-0001
- `intentionally_absent`: file-0212-atom-0001, file-0221-atom-0001, file-0222-atom-0001, file-0226-atom-0001
- `moved_to_dependency`: file-0390-atom-0001
- `structural_equivalent`: file-0048-atom-0001, file-0078-atom-0001, file-0097-atom-0001, file-0107-atom-0001, file-0115-atom-0001, file-0144-atom-0001, file-0164-atom-0001, file-0174-atom-0001, file-0175-atom-0001, file-0194-atom-0001, file-0204-atom-0001, file-0255-atom-0001, file-0261-atom-0001, file-0304-atom-0025, file-0372-atom-0001, file-0378-atom-0001, file-0384-atom-0001, file-0388-atom-0001, file-0391-atom-0001, file-0438-atom-0001, file-0444-atom-0001, file-0447-atom-0001, file-0449-atom-0001, file-0450-atom-0001, file-0452-atom-0001, file-0459-atom-0001, file-0470-atom-0001, file-0476-atom-0001, file-0483-atom-0001, file-0496-atom-0001, file-0546-atom-0001, file-0552-atom-0001, file-0555-atom-0001, file-0557-atom-0001, file-0559-atom-0001

## Precompile dispatch, SPC, and executor registry

Ritual precompile codecs and routing, SPC signature/verification support, block-verification helpers, TEE/executor registry reads, capability filtering, and executor-selection data.

- Counts: `65` atoms; `60` high-risk; `55` review-required; statuses `{'structural_equivalent': 36, 'blocked': 6, 'exact': 19, 'intentionally_absent': 3, 'renamed_exact': 1}`.

Actionable gaps:
- `file-0092-atom-0007` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 2 (Async Precompile Detection And Validation) preserves payload validation: Shared payload validation rejects bad TTL, oversized inputs, malformed ECIES/user keys, bad URLs/models/messages, invalid two-phase deadlines, and unsupported agent types; Preserve validation hardening: centralized invalid-payload errors (`#231`).
- `file-0092-atom-0008` `structural_equivalent`: `crates/ethereum/payload/src/ritual_async.rs` + `coverage-map/verify_async_precompile_cross_repo.py` — TEE registry executor `Capability` must equal `registry_capability_for_precompile` / ritual-precompile-addresses metadata (cross-repo static gate; split from broad 0008).
- `file-0092-atom-0036` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#83` `etherscan-investigation` keeps live downstream behavior: commitment/settlement flow.
- `file-0092-atom-0046` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#298` `fix-onnx-building-verification-divergence` keeps live downstream behavior: permanent invalid precompile requests remain evictable.
- `file-0357-atom-0005` `blocked`: `crates/ritual-tee-registry-reader/src/reader.rs` — PR preservation `#333` `agent_telemetry` keeps live downstream behavior: `TELEMETRY=12` as non-executor capabilities.
- `file-0468-atom-0003` `blocked`: `crates/storage/codecs/src/alloy/transaction/spc_call.rs` — SPC call fields: precompile address, input, output, proof, and block number.

Representative atoms:
- `file-0092-atom-0003` `structural_equivalent`: `crates/ethereum/payload/src/lib.rs` — SPC verification accepts valid preloaded-context signatures and rejects wrong outputs, mismatched input hashes, or empty executor keys.
- `file-0150-atom-0001` `structural_equivalent`: `crates/net/eth-wire/src/multiplex.rs` — The downstream diff for crates/net/eth-wire/src/multiplex.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0178-atom-0001` `structural_equivalent`: `crates/net/network/tests/it/multiplex.rs` — The downstream diff for crates/net/network/tests/it/multiplex.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0292-atom-0004` `exact`: `crates/ritual-async-registry/src/lib.rs` — phase1 settled preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_settlement_data_fields, test_is_phase1_settled_true_when_slot_is_nonzero, diff_eq_no_pending_jobs, diff_eq_all_jobs_phase1_settled.
- `file-0292-atom-0005` `exact`: `crates/ritual-async-registry/src/lib.rs` — precompile address preserves the production behavior asserted by downstream tests: test_get_async_job_tracker_address_default, test_spc_verification_job_data_fields.
- `file-0316-atom-0002` `exact`: `crates/ritual-precompile-addresses/src/lib.rs` — precompile address preserves the production behavior asserted by downstream tests: precompile_addresses_are_nonzero_and_pairwise_distinct, two_phase_precompiles_are_subset_of_spc_verified_allowlist.
- `file-0316-atom-0011` `exact`: `crates/ritual-precompile-addresses/src/lib.rs` — cross-repo FSM: sovereign `0x080C` and persistent `0x0820` expected registry capability is HttpCall (u8 0), matching traffic-gen HTTP_CALL executor selection and ritual-node localnet HTTP sidecars; regression `sovereign_and_persistent_precompiles_expected_capability_is_http_call_for_downstream_parity`.
- `file-0316-atom-0012`–`file-0316-atom-0020` `exact`: per-precompile cross-repo contracts (`0x0801`–`0x081b` except `0x080C`/`0x0820` covered by 0011); static proof: `coverage-map/verify_async_precompile_cross_repo.py`.

- `file-0316-atom-0003` `intentionally_absent`: `crates/ritual-precompile-addresses/src/lib.rs` — Preserve: Do not reintroduce deprecated `AGENT_CALL_PRECOMPILE` in fee or registry paths (`#319`).
- `file-0316-atom-0006` `intentionally_absent`: `crates/ritual-precompile-addresses/src/lib.rs` — Preserve: Do not reintroduce deprecated `AGENT_CALL_PRECOMPILE`.
- `file-0316-atom-0009` `intentionally_absent`: `crates/ritual-precompile-addresses/src/lib.rs` — Preserve: Do not reintroduce `target_block`/`commit_block` (`#261`) or deprecated `AGENT_CALL_PRECOMPILE` (`#319`).
- `file-0092-atom-0007` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 2 (Async Precompile Detection And Validation) preserves payload validation: Shared payload validation rejects bad TTL, oversized inputs, malformed ECIES/user keys, bad URLs/models/messages, invalid two-phase deadlines, and unsupported agent types; Preserve validation hardening: centralized invalid-payload errors (`#231`).
- `file-0092-atom-0008` `structural_equivalent`: `crates/ethereum/payload/src/ritual_async.rs` + `coverage-map/verify_async_precompile_cross_repo.py` — TEE registry executor `Capability` must equal `registry_capability_for_precompile` / ritual-precompile-addresses metadata (cross-repo static gate; split from broad 0008).
- `file-0092-atom-0036` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#83` `etherscan-investigation` keeps live downstream behavior: commitment/settlement flow.

Trace IDs by status:

- `blocked`: file-0092-atom-0007, file-0092-atom-0036, file-0092-atom-0046, file-0357-atom-0005, file-0468-atom-0003
- `exact`: file-0292-atom-0004, file-0292-atom-0005, file-0316-atom-0002, file-0316-atom-0011, file-0316-atom-0012, file-0316-atom-0013, file-0316-atom-0014, file-0316-atom-0015, file-0316-atom-0016, file-0316-atom-0017, file-0316-atom-0018, file-0316-atom-0019, file-0316-atom-0020, file-0344-atom-0002, file-0344-atom-0003, file-0344-atom-0004, file-0344-atom-0005, file-0344-atom-0006, file-0344-atom-0009, file-0344-atom-0010, file-0354-atom-0001, file-0354-atom-0002, file-0354-atom-0003, file-0355-atom-0002, file-0355-atom-0003, file-0355-atom-0004, file-0356-atom-0001, file-0357-atom-0003, file-0357-atom-0004
- `intentionally_absent`: file-0316-atom-0003, file-0316-atom-0006, file-0316-atom-0009
- `renamed_exact`: file-0356-atom-0002
- `structural_equivalent`: file-0092-atom-0003, file-0092-atom-0008, file-0092-atom-0049, file-0092-atom-0050, file-0150-atom-0001, file-0178-atom-0001, file-0180-atom-0001, file-0249-atom-0001, file-0274-atom-0002, file-0280-atom-0003, file-0280-atom-0006, file-0295-atom-0002, file-0295-atom-0003, file-0297-atom-0006, file-0299-atom-0001, file-0300-atom-0001, file-0301-atom-0001, file-0302-atom-0001, file-0304-atom-0004, file-0304-atom-0009, file-0304-atom-0017, file-0316-atom-0004, file-0316-atom-0005, file-0316-atom-0008, file-0317-atom-0001, file-0318-atom-0001, file-0319-atom-0001, file-0320-atom-0001, file-0320-atom-0002, file-0321-atom-0002, file-0321-atom-0003, file-0321-atom-0004, file-0321-atom-0005, file-0322-atom-0001, file-0323-atom-0002, file-0323-atom-0003, file-0327-atom-0001, file-0344-atom-0012, file-0344-atom-0013

## Transaction pool, admission, and ordering

Txpool async/scheduled subpools, admission validation, pending/parked/blob behavior, sequencing rights, and candidate ordering.

- Counts: `13` atoms; `13` high-risk; `13` review-required; statuses `{'structural_equivalent': 12, 'exact': 1}`.

Actionable gaps:
- No unresolved `missing` atoms remain; intentionally absent atoms are scope decisions rather than code gaps.

Representative atoms:
- `file-0521-atom-0001` `structural_equivalent`: `crates/transaction-pool/src/blocking_handlers.rs` — The downstream diff for crates/transaction-pool/src/blocking_handlers.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0524-atom-0001` `structural_equivalent`: `crates/transaction-pool/src/lib.rs` — The downstream diff for crates/transaction-pool/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0525-atom-0002` `structural_equivalent`: `crates/transaction-pool/src/maintain.rs` — PR preservation `#300` `txpool-pending-eviction` keeps live downstream behavior: age eviction for pending pool in addition to queued/basefee pools.
- `file-0537-atom-0002` `exact`: `crates/transaction-pool/src/pool/txpool.rs` — fee preserves the fee/gas/accounting behavior covered by downstream tests: test_add_async_commitment_transaction, test_insert_pending.

Trace IDs by status:

- `exact`: file-0537-atom-0002
- `structural_equivalent`: file-0521-atom-0001, file-0524-atom-0001, file-0525-atom-0002, file-0529-atom-0007, file-0529-atom-0008, file-0536-atom-0001, file-0537-atom-0004, file-0537-atom-0005, file-0537-atom-0006, file-0537-atom-0007, file-0537-atom-0009, file-0545-atom-0001

## Core async execution and settlement

Short async transaction lifecycle: async-context feature plumbing, commitment/result state, settlement, fulfilled-original replay, pool/RPC/verifier hooks, SPC call handling, and async fee/wallet foundations.

- Counts: `152` atoms; `125` high-risk; `128` review-required; statuses `{'structural_equivalent': 96, 'blocked': 15, 'noise': 1, 'covered_by_upstream': 2, 'intentionally_absent': 19, 'moved_to_dependency': 4, 'exact': 15}`.

Actionable gaps:
- `file-0064-atom-0002` `blocked`: `crates/engine/tree/src/tree/mod.rs` — PR preservation `#298` `fix-onnx-building-verification-divergence` keeps live downstream behavior: temporary ONNX model unavailability as retryable `SYNCING`.
- `file-0092-atom-0004` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve strict fee behavior: shared async fee crate and no fallback on HTTP/LLM/pricing failures (`#146`), model-registry pricing and fail-closed builder/verifier/wallet reads (`#252`).
- `file-0092-atom-0011` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve duplicate/nonce behavior: active AsyncJobTracker duplicates block builder/verifier commitments and prune stale pool entries (`#260`, `#268`).
- `file-0092-atom-0016` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve parity with builder: per-block async sender uniqueness and wallet locks (`#202`), shared per-block `ModelCache` (`#205`), optimized nonce-lock checks and same-block duplicate rejection (`#207`).
- `file-0092-atom-0018` `blocked`: `crates/ethereum/payload/src/lib.rs` — Error messages should stay descriptive for invalid async payloads and mismatched canonical context.
- `file-0092-atom-0026` `blocked`: `crates/ethereum/payload/src/lib.rs` — Fulfilled async collection is skipped when the global deadline has passed and capped by RETH_MAX_FULFILLED_ASYNC_PER_BLOCK, allowing settlements to roll to later blocks instead of overrunning payload construction.
- `file-0092-atom-0037` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#93` `executor-rs` keeps live downstream behavior: parent/simulation context rewriting.
- `file-0092-atom-0047` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#304` `async-atomicity-pair-precheck-dev` keeps live downstream behavior: fail-fast if settlement cannot execute after original.
- `file-0108-atom-0001` `blocked`: `crates/evm/src/lib.rs` — The downstream diff for crates/evm/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0281-atom-0003` `blocked`: `crates/ritual-async-fees/src/llm.rs` — PR preservation `#314` `llm-error-pricing` keeps live downstream behavior: encrypted-response fallback to plaintext error decode.
- `file-0365-atom-0001` `blocked`: `crates/rpc/rpc-api/src/ritual.rs` — The downstream diff for crates/rpc/rpc-api/src/ritual.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0396-atom-0001` `blocked`: `crates/rpc/rpc/src/async_tx_validator.rs` — The downstream diff for crates/rpc/rpc/src/async_tx_validator.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0410-atom-0001` `blocked`: `crates/rpc/rpc/src/ritual.rs` — The downstream diff for crates/rpc/rpc/src/ritual.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0466-atom-0002` `blocked`: `crates/storage/codecs/src/alloy/transaction/passkey.rs` — Passkey compact storage preserves chain id, nonce, gas, fees, kind, value, access list, settlement transaction, optional SPC calls, and trailing input for P-256 and WebAuthn transactions.
- `file-0468-atom-0002` `blocked`: `crates/storage/codecs/src/alloy/transaction/spc_call.rs` — proof preserves the encoding, decoding, storage, or proof boundary covered by downstream tests: test_spc_call_compact_roundtrip, test_spc_call_compact_empty_bytes, test_spc_call_compact_large_bytes, test_spc_call_wrapper_roundtrip.

Representative atoms:
- `file-0020-atom-0001` `structural_equivalent`: `crates/chain-state/Cargo.toml` — The chain-state crate depends on Ritual's blocking canonical-state pubsub helper.
- `file-0022-atom-0001` `structural_equivalent`: `crates/chain-state/src/in_memory.rs` — CanonicalInMemoryState stores a blocking notifier alongside the async broadcast sender.
- `file-0022-atom-0002` `structural_equivalent`: `crates/chain-state/src/in_memory.rs` — CanonicalInMemoryState exposes an API to register synchronous canonical-state handlers.
- `file-0292-atom-0002` `exact`: `crates/ritual-async-registry/src/lib.rs` — diff eq preserves the production behavior asserted by downstream tests: diff_eq_locked_and_not_fulfillment, diff_eq_mixed_settlement_status, diff_eq_mixed_settlement_fulfillment_of_settled, diff_eq_mixed_settlement_fulfillment_of_unsettled, diff_eq_many_jobs_all_settled.
- `file-0292-atom-0003` `exact`: `crates/ritual-async-registry/src/lib.rs` — job exists and active preserves the production behavior asserted by downstream tests: test_job_exists_and_active_no_job, test_job_exists_and_active_active_job, test_job_exists_and_active_expired_job, test_job_exists_and_active_boundary_exact, test_job_exists_and_active_boundary_one_before.
- `file-0292-atom-0006` `exact`: `crates/ritual-async-registry/src/lib.rs` — read jobs preserves the production behavior asserted by downstream tests: test_read_jobs_empty_list, test_read_jobs_for_spc_verification_empty_list, test_read_job_not_found, test_read_spc_job_not_found, test_builder_should_skip_phase1_settled_jobs.
- `file-0081-atom-0003` `moved_to_dependency`: `crates/ethereum/node/Cargo.toml` — The ethereum node crate directly links Ritual async-transaction support as a first-class dependency.
- `file-0081-atom-0004` `moved_to_dependency`: `crates/ethereum/node/Cargo.toml` — The ethereum node crate directly links Ritual scheduling support.
- `file-0101-atom-0001` `moved_to_dependency`: `crates/evm/Cargo.toml` — The core `reth-evm` crate directly depends on `revm-context` and `revm-precompile` so async-aware execution context and precompile dispatch are available from the EVM layer itself.
- `file-0073-atom-0001` `covered_by_upstream`: `crates/errors/src/error.rs` — The file documents that `RethError` and `BlockExecutionError` no longer have a stable exact size because `alloy-evm`'s `async-context` feature can enlarge them from 56 to 64 bytes.
- `file-0073-atom-0002` `covered_by_upstream`: `crates/errors/src/error.rs` — The file stops enforcing that `RethError` must be exactly 56 bytes on x86_64.
- `file-0077-atom-0002` `intentionally_absent`: `crates/ethereum/evm/Cargo.toml` — Adds the `tracing` dependency required by downstream debug logging in this crate.
- `file-0081-atom-0005` `intentionally_absent`: `crates/ethereum/node/Cargo.toml` — The ethereum node crate directly provides the SPC verification bridge through `ritual-spc-verification`.
- `file-0081-atom-0006` `intentionally_absent`: `crates/ethereum/node/Cargo.toml` — The crate exposes an `async-context` feature that forwards async execution support through `reth-evm-ethereum`.
- `file-0064-atom-0002` `blocked`: `crates/engine/tree/src/tree/mod.rs` — PR preservation `#298` `fix-onnx-building-verification-divergence` keeps live downstream behavior: temporary ONNX model unavailability as retryable `SYNCING`.

Trace IDs by status:

- `blocked`: file-0064-atom-0002, file-0092-atom-0004, file-0092-atom-0011, file-0092-atom-0016, file-0092-atom-0018, file-0092-atom-0026, file-0092-atom-0037, file-0092-atom-0047, file-0108-atom-0001, file-0281-atom-0003, file-0365-atom-0001, file-0396-atom-0001, file-0410-atom-0001, file-0466-atom-0002, file-0468-atom-0002
- `covered_by_upstream`: file-0073-atom-0001, file-0073-atom-0002
- `exact`: file-0292-atom-0002, file-0292-atom-0003, file-0292-atom-0006, file-0292-atom-0007, file-0292-atom-0008, file-0293-atom-0002, file-0293-atom-0003, file-0293-atom-0004, file-0359-atom-0001, file-0359-atom-0002, file-0359-atom-0003, file-0359-atom-0004, file-0460-atom-0001, file-0460-atom-0002, file-0466-atom-0001
- `intentionally_absent`: file-0077-atom-0002, file-0081-atom-0005, file-0081-atom-0006, file-0082-atom-0001, file-0082-atom-0002, file-0085-atom-0001, file-0111-atom-0001, file-0346-atom-0001, file-0348-atom-0001, file-0348-atom-0002, file-0348-atom-0003, file-0349-atom-0001, file-0350-atom-0001, file-0351-atom-0001, file-0351-atom-0002, file-0352-atom-0001, file-0352-atom-0002, file-0352-atom-0003, file-0352-atom-0004
- `moved_to_dependency`: file-0081-atom-0003, file-0081-atom-0004, file-0101-atom-0001, file-0101-atom-0002
- `noise`: file-0072-atom-0001
- `structural_equivalent`: file-0020-atom-0001, file-0022-atom-0001, file-0022-atom-0002, file-0022-atom-0003, file-0023-atom-0001, file-0024-atom-0001, file-0024-atom-0002, file-0025-atom-0001, file-0072-atom-0002, file-0077-atom-0001, file-0077-atom-0003, file-0079-atom-0001, file-0080-atom-0001, file-0081-atom-0001, file-0081-atom-0002, file-0083-atom-0001, file-0084-atom-0002, file-0099-atom-0001, file-0099-atom-0002, file-0099-atom-0003, file-0099-atom-0004, file-0101-atom-0003, file-0101-atom-0004, file-0102-atom-0001, file-0106-atom-0001, file-0106-atom-0002, file-0107-atom-0002, file-0110-atom-0001, file-0185-atom-0001, file-0186-atom-0001, file-0187-atom-0001, file-0188-atom-0001, file-0193-atom-0001, file-0236-atom-0002, file-0273-atom-0001, file-0274-atom-0001, file-0275-atom-0001, file-0276-atom-0001, file-0276-atom-0002, file-0278-atom-0001, file-0278-atom-0002, file-0279-atom-0001, file-0279-atom-0002, file-0280-atom-0001, file-0280-atom-0004, file-0280-atom-0007, file-0280-atom-0010, file-0281-atom-0001, file-0281-atom-0002, file-0282-atom-0002, file-0282-atom-0004, file-0282-atom-0006, file-0284-atom-0001, file-0284-atom-0002, file-0284-atom-0003, file-0286-atom-0001, file-0287-atom-0001, file-0288-atom-0001, file-0289-atom-0001, file-0290-atom-0001, file-0292-atom-0001, file-0292-atom-0009, file-0292-atom-0010, file-0294-atom-0001, file-0295-atom-0001, file-0296-atom-0001, file-0296-atom-0003, file-0296-atom-0004, file-0297-atom-0001, file-0297-atom-0002, file-0298-atom-0001, file-0303-atom-0001, file-0304-atom-0014, file-0304-atom-0029, file-0304-atom-0033, file-0315-atom-0001, file-0316-atom-0001, file-0321-atom-0001, file-0323-atom-0001, file-0325-atom-0001, file-0326-atom-0001, file-0343-atom-0001, file-0344-atom-0001, file-0395-atom-0001, file-0403-atom-0001, file-0424-atom-0001, file-0427-atom-0001, file-0462-atom-0001, file-0464-atom-0001, file-0468-atom-0001, file-0523-atom-0001, file-0529-atom-0001, file-0532-atom-0001, file-0538-atom-0001, file-0539-atom-0001, file-0540-atom-0001

## Long-running async delivery FSM

Two-phase long-running async flow: Phase 1 commitment settlement, delivery readiness, delivery result validation, and final settlement/delivery bookkeeping.

- Counts: `88` atoms; `88` high-risk; `84` review-required; statuses `{'structural_equivalent': 71, 'blocked': 6, 'exact': 6, 'intentionally_absent': 5}`.

Actionable gaps:
- `file-0092-atom-0014` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 6 (Payload Building) preserves runtime fields hashing: Preserve active-job and Phase 2 behavior: parent-state duplicate active-job checks (`#260`, `#268`), build-time SPC reverification and metadata refresh (`#273`), Phase 2 delivery settlements and nested delivery (`#270`), atomic original+settlement size/gas precheck (`#304`); Preserve trace-facing payload metadata: payload attempt IDs/kinds, empty-payload fallback tracing, demotion capture, primary included tx count (`#329`, `#336`).
- `file-0092-atom-0019` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve RPC async validation behavior: precompile consumer decoding, executor capability/registration, ECIES/user keys, supported sovereign agent types `0/4/5/6`, Phase 2 offset bounds, rich invalid-payload errors (`#204`, `#231`, `#307`).
- `file-0092-atom-0043` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#270` `second-phase-valconstraint` keeps live downstream behavior: `delivery_spc_calls` in receipts/codecs.
- `file-0304-atom-0001` `blocked`: `crates/ritual-block-verification/src/verifier.rs` — The downstream diff for crates/ritual-block-verification/src/verifier.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0459-atom-0005` `blocked`: `crates/storage/codecs/src/alloy/passkey_signature.rs` — Feature section 1 (Transaction Formats And Codecs) preserves passkey signature: Full passkey signature representation, including P256/WebAuthn and synthetic sender handling; Preserve hardening: async settlement compact codec coverage (`#84`), passkey synthetic ECDSA fallback (`#241`), safe settlement/delivery selector offsets and Phase 1/Phase 2 input extraction (`#282`), LLM 30-field ABI with `convo_history: StorageRef` at index 29 (`#306`).
- `file-0459-atom-0006` `blocked`: `crates/storage/codecs/src/alloy/passkey_signature.rs` — Feature section 8 (RPC And Operator Surfaces) preserves passkey signature: Async result submission must preserve original tx/passkey context; Preserve: Preserve delivery result submission with original tx/passkey context and `delivery_spc_calls` compatibility (`#270`).

Representative atoms:
- `file-0092-atom-0013` `structural_equivalent`: `crates/ethereum/payload/src/lib.rs` — Fulfilled async settlement and delivery settlement inclusion.
- `file-0092-atom-0028` `structural_equivalent`: `crates/ethereum/payload/src/lib.rs` — Phase 2 delivery collection reads each delivery-ready job from AsyncJobTracker, defers jobs whose Phase 1 is not settled, and skips missing on-chain jobs instead of trusting pool state alone.
- `file-0092-atom-0029` `structural_equivalent`: `crates/ethereum/payload/src/lib.rs` — Phase 2 delivery settlement checks pool metadata against contract state for precompile input hash, commit block, and precompile address before constructing a delivery transaction.
- `file-0277-atom-0002` `exact`: `crates/ritual-async-fees/src/delivery.rs` — extract delivery gas preserves the fee/gas/accounting behavior covered by downstream tests: test_extract_delivery_gas_success, test_extract_delivery_gas_callback_failed, test_extract_delivery_gas_wrong_address, test_extract_delivery_gas_empty_logs.
- `file-0277-atom-0003` `exact`: `crates/ritual-async-fees/src/delivery.rs` — get delivery callback gas or fallback preserves the fee/gas/accounting behavior covered by downstream tests: test_get_delivery_callback_gas_or_fallback_delivered, test_get_delivery_callback_gas_or_fallback_failed, test_get_delivery_callback_gas_or_fallback_not_found.
- `file-0344-atom-0007` `exact`: `crates/ritual-spc-signature/src/lib.rs` — precompile address preserves the production behavior asserted by downstream tests: test_recovery_id_invalid_26, test_recovery_id_invalid_29.
- `file-0304-atom-0013` `intentionally_absent`: `crates/ritual-block-verification/src/verifier.rs` — metrics delivery preserves the production behavior asserted by downstream tests: prop_metrics_delivery_deterministic.
- `file-0324-atom-0006` `intentionally_absent`: `crates/ritual-precompile-codecs/src/long_running.rs` — Sovereign-agent delivery decoding uses the agent-specific ABI layout to extract max poll block and callback fields without depending on the long-HTTP field offsets.
- `file-0324-atom-0009` `intentionally_absent`: `crates/ritual-precompile-codecs/src/long_running.rs` — FHE Phase 2 result decoding extracts the encrypted output size from the delivery result, making output-size fee calculation depend on the delivered result struct rather than external metadata.
- `file-0092-atom-0014` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 6 (Payload Building) preserves runtime fields hashing: Preserve active-job and Phase 2 behavior: parent-state duplicate active-job checks (`#260`, `#268`), build-time SPC reverification and metadata refresh (`#273`), Phase 2 delivery settlements and nested delivery (`#270`), atomic original+settlement size/gas precheck (`#304`); Preserve trace-facing payload metadata: payload attempt IDs/kinds, empty-payload fallback tracing, demotion capture, primary included tx count (`#329`, `#336`).
- `file-0092-atom-0019` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve RPC async validation behavior: precompile consumer decoding, executor capability/registration, ECIES/user keys, supported sovereign agent types `0/4/5/6`, Phase 2 offset bounds, rich invalid-payload errors (`#204`, `#231`, `#307`).
- `file-0092-atom-0043` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#270` `second-phase-valconstraint` keeps live downstream behavior: `delivery_spc_calls` in receipts/codecs.

Trace IDs by status:

- `blocked`: file-0092-atom-0014, file-0092-atom-0019, file-0092-atom-0043, file-0304-atom-0001, file-0459-atom-0005, file-0459-atom-0006
- `exact`: file-0277-atom-0002, file-0277-atom-0003, file-0344-atom-0007, file-0357-atom-0002, file-0461-atom-0001, file-0461-atom-0002
- `intentionally_absent`: file-0304-atom-0013, file-0324-atom-0006, file-0324-atom-0009, file-0396-atom-0007, file-0396-atom-0009
- `structural_equivalent`: file-0092-atom-0013, file-0092-atom-0028, file-0092-atom-0029, file-0092-atom-0030, file-0092-atom-0031, file-0092-atom-0032, file-0092-atom-0033, file-0092-atom-0034, file-0092-atom-0038, file-0092-atom-0044, file-0276-atom-0003, file-0276-atom-0004, file-0277-atom-0001, file-0280-atom-0002, file-0280-atom-0005, file-0280-atom-0008, file-0280-atom-0009, file-0280-atom-0011, file-0280-atom-0012, file-0280-atom-0013, file-0282-atom-0003, file-0282-atom-0005, file-0285-atom-0002, file-0285-atom-0003, file-0295-atom-0004, file-0296-atom-0002, file-0297-atom-0003, file-0297-atom-0004, file-0297-atom-0005, file-0297-atom-0007, file-0297-atom-0008, file-0297-atom-0009, file-0297-atom-0010, file-0297-atom-0011, file-0304-atom-0008, file-0304-atom-0010, file-0304-atom-0012, file-0304-atom-0015, file-0304-atom-0030, file-0304-atom-0032, file-0316-atom-0007, file-0324-atom-0001, file-0324-atom-0002, file-0324-atom-0003, file-0324-atom-0004, file-0324-atom-0005, file-0324-atom-0007, file-0324-atom-0008, file-0324-atom-0010, file-0325-atom-0002, file-0325-atom-0003, file-0325-atom-0004, file-0325-atom-0005, file-0325-atom-0006, file-0325-atom-0007, file-0325-atom-0008, file-0325-atom-0009, file-0326-atom-0002, file-0326-atom-0003, file-0326-atom-0004, file-0326-atom-0005, file-0326-atom-0006, file-0461-atom-0003, file-0528-atom-0002, file-0528-atom-0003, file-0528-atom-0004, file-0528-atom-0005, file-0528-atom-0006, file-0528-atom-0007, file-0529-atom-0006, file-0537-atom-0008

## Scheduled transactions and missed-obligation verification

Scheduled transaction identity, Scheduler storage reads, predicate evaluation, missed-obligation synthesis, heartbeat/revival helpers, and builder/verifier parity for scheduled jobs.

- Counts: `224` atoms; `196` high-risk; `195` review-required; statuses `{'noise': 3, 'structural_equivalent': 74, 'exact': 49, 'intentionally_absent': 74, 'moved_to_dependency': 1, 'blocked': 23}`.

Actionable gaps:
- `file-0092-atom-0002` `blocked`: `crates/ethereum/payload/src/lib.rs` — Payload async simulation slot allocation preserves regular-lane anti-starvation, total-cap clamping, zero-cap disabling, and leftover redistribution across scheduled and regular candidates.
- `file-0092-atom-0005` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 11 (Observability And Agent Guardrails) preserves observability: Preserve early metrics: verification-end fields, payload/verification phase metrics, scheduler event visibility (`3393e7a3`, `#97`); Preserve structured block telemetry: block/tx phase logs, per-tx payload execution logs, payload attempt IDs/kinds, empty-payload fallback tracing, node/basic payload integration (`#325`, `#329`).
- `file-0092-atom-0009` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve validation hardening: async input/calldata caps and builder/verifier obligation consistency (`#292`).
- `file-0092-atom-0012` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 6 (Payload Building) preserves payload construction: Async detection and commitment insertion; Preserve DoS policy: build deadline default `300ms`, deadline guards, obligation/fulfilled/delivery caps, total/per-category async sim caps, regular-priority allocation, tx-count cap, local work-class demotion, near-deadline epsilon, optional-class short-circuit, and cap observations (`#292`, `#332`, `#330`, `#354`).
- `file-0092-atom-0015` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve: Avoid verifier-only obligation deadline logic that can diverge from builder membership (`#299`).
- `file-0092-atom-0021` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve payload deadline/sync policy: default `300ms`, obligation caps, async sim caps, builder/verifier policy boundary (`#282`, `#292`, `#332`), transient ONNX unavailability as retryable/`SYNCING` with bounded retry before unwind/escalation (`#298`, `#301`).
- `file-0092-atom-0039` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#122` `scheduling-eviction` keeps live downstream behavior: verification mode for all txs during block verification.
- `file-0092-atom-0040` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#230` `jungle-ass` keeps live downstream behavior: sequencing-rights classification/reordering plus verifier checks.
- `file-0092-atom-0041` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#231` `rpc-async-feedback` keeps live downstream behavior: parity across scheduled/sequencing/async paths.
- `file-0092-atom-0042` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#260` `single-node` keeps live downstream behavior: parent-state AsyncJobTracker duplicate checks in builder/verifier.
- `file-0092-atom-0045` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#292` `sadpaths-halt-protection` keeps live downstream behavior: DoS bounds: build deadline default.
- `file-0092-atom-0048` `blocked`: `crates/ethereum/payload/src/lib.rs` — PR preservation `#351` `scheduled-gas-extraction-recorder-realign` keeps live downstream behavior: broader scheduled incident capture after gas-extraction sad paths became structured 0-gas logs.
- `file-0248-atom-0001` `blocked`: `crates/primitives-traits/src/size.rs` — The downstream diff for crates/primitives-traits/src/size.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0313-atom-0002` `blocked`: `crates/ritual-metrics/src/scheduling.rs` — PR preservation `#345` `scheduled-incidents-debug-rpc` keeps live downstream behavior: `ritual_getScheduledIncidents`.
- `file-0332-atom-0024` `blocked`: `crates/ritual-scheduled-verification/src/lib.rs` — Feature section 11 (Observability And Agent Guardrails) preserves observability: Scheduled incident tracking; Preserve payload policy traceability: build attempts, demotion capture, primary-cause trace plumbing, cap observations, async sim deadlines, total/per-category caps, combined scheduled/regular sim phases (`#332`, `#336`, `#337`, `#354`); Preserve scheduled incident observability: bounded ring buffer, structured gas/scheduled sad-path capture, decoded call/index fields, continued capture after 0-gas structured logs (`#345`, `#351`).
- `file-0332-atom-0034` `blocked`: `crates/ritual-scheduled-verification/src/lib.rs` — Feature section 8 (RPC And Operator Surfaces) preserves heartbeat revival: `ritual_*` namespace for async result submission, batch submission, delivery result submission, pending jobs, async simulation traces, block-build traces, scheduled incidents, and heartbeat tracker state; Preserve operator APIs: `ritual_getHeartbeatTrackerState` (`#331`), scheduled incident debug RPC (`#345`, `#351`), block-build trace with demotions/caps/primary included count (`#336`, `#354`), async simulation trace.
- `file-0365-atom-0003` `blocked`: `crates/rpc/rpc-api/src/ritual.rs` — PR preservation `#345` `scheduled-incidents-debug-rpc` keeps live downstream behavior: gas/scheduled error capture.
- `file-0366-atom-0002` `blocked`: `crates/rpc/rpc-api/src/txpool.rs` — PR preservation `#85` `asyncpool-rpc-rename` keeps live downstream behavior: async txpool RPC names.
- `file-0410-atom-0002` `blocked`: `crates/rpc/rpc/src/ritual.rs` — PR preservation `#332` `payload-policy-checkpointing` keeps live downstream behavior: block-build attempts.
- `file-0412-atom-0002` `blocked`: `crates/rpc/rpc/src/txpool.rs` — PR preservation `#32` `ritual_async-execution-checkpoint-12` keeps live downstream behavior: detailed async txpool metadata exposed over RPC.
- `file-0412-atom-0003` `blocked`: `crates/rpc/rpc/src/txpool.rs` — PR preservation `#85` `asyncpool-rpc-rename` keeps live downstream behavior: detailed async metadata access.
- `file-0459-atom-0004` `blocked`: `crates/storage/codecs/src/alloy/passkey_signature.rs` — `Scheduled(0x10)`, `AsyncCommitment(0x11)`, `AsyncSettlement(0x12)`, `Passkey(0x77)`.
- `file-0469-atom-0002` `blocked`: `crates/storage/codecs/src/alloy/transaction/txtype.rs` — Compact transaction type encoding preserves extended identifiers for scheduled, async commitment, async settlement, and passkey transactions instead of collapsing them into upstream Ethereum transaction types.

Representative atoms:
- `file-0087-atom-0002` `structural_equivalent`: `crates/ethereum/payload/Cargo.toml` — The payload crate depends on `revm-context` for async execution context support.
- `file-0087-atom-0011` `structural_equivalent`: `crates/ethereum/payload/Cargo.toml` — The payload crate exposes an `async-context` feature gate that forwards async-context support to EVM dependencies.
- `file-0088-atom-0002` `structural_equivalent`: `crates/ethereum/payload/src/bundle.rs` — tx source preserves the production behavior asserted by downstream tests: test_tx_source_equality.
- `file-0087-atom-0003` `exact`: `crates/ethereum/payload/Cargo.toml` — The payload crate gains ABI encoding/decoding support via `alloy-sol-types`.
- `file-0087-atom-0004` `exact`: `crates/ethereum/payload/Cargo.toml` — The payload crate is wired to Ritual async, registry, SPC, precompile, and scheduled-execution helper crates needed for runtime payload behavior.
- `file-0291-atom-0001` `exact`: `crates/ritual-async-registry/src/error.rs` — AsyncJobTracker registry reads preserve a database-error variant for storage/provider failures.
- `file-0087-atom-0008` `moved_to_dependency`: `crates/ethereum/payload/Cargo.toml` — The payload crate depends on Ritual scheduling helpers for heartbeat and scheduled transaction orchestration.
- `file-0087-atom-0005` `intentionally_absent`: `crates/ethereum/payload/Cargo.toml` — The payload crate adds Ritual metrics/tracing instrumentation support.
- `file-0087-atom-0006` `intentionally_absent`: `crates/ethereum/payload/Cargo.toml` — The payload crate depends on sequencing-rights logic to classify and reorder candidate transactions before execution.
- `file-0087-atom-0007` `intentionally_absent`: `crates/ethereum/payload/Cargo.toml` — The payload crate keeps heartbeat revival/tracking state in-process while building payloads.
- `file-0092-atom-0002` `blocked`: `crates/ethereum/payload/src/lib.rs` — Payload async simulation slot allocation preserves regular-lane anti-starvation, total-cap clamping, zero-cap disabling, and leftover redistribution across scheduled and regular candidates.
- `file-0092-atom-0005` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 11 (Observability And Agent Guardrails) preserves observability: Preserve early metrics: verification-end fields, payload/verification phase metrics, scheduler event visibility (`3393e7a3`, `#97`); Preserve structured block telemetry: block/tx phase logs, per-tx payload execution logs, payload attempt IDs/kinds, empty-payload fallback tracing, node/basic payload integration (`#325`, `#329`).
- `file-0092-atom-0009` `blocked`: `crates/ethereum/payload/src/lib.rs` — Preserve validation hardening: async input/calldata caps and builder/verifier obligation consistency (`#292`).
- `file-0087-atom-0001` `noise`: `crates/ethereum/payload/Cargo.toml` — The payload crate adds a dependency on the umbrella `ritual-async` crate.
- `file-0087-atom-0009` `noise`: `crates/ethereum/payload/Cargo.toml` — The payload crate adds `once_cell` support.

Trace IDs by status:

- `blocked`: file-0092-atom-0002, file-0092-atom-0005, file-0092-atom-0009, file-0092-atom-0012, file-0092-atom-0015, file-0092-atom-0021, file-0092-atom-0039, file-0092-atom-0040, file-0092-atom-0041, file-0092-atom-0042, file-0092-atom-0045, file-0092-atom-0048, file-0248-atom-0001, file-0313-atom-0002, file-0332-atom-0024, file-0332-atom-0034, file-0365-atom-0003, file-0366-atom-0002, file-0410-atom-0002, file-0412-atom-0002, file-0412-atom-0003, file-0459-atom-0004, file-0469-atom-0002
- `exact`: file-0087-atom-0003, file-0087-atom-0004, file-0291-atom-0001, file-0291-atom-0002, file-0291-atom-0003, file-0293-atom-0001, file-0307-atom-0001, file-0308-atom-0001, file-0309-atom-0001, file-0309-atom-0002, file-0329-atom-0002, file-0329-atom-0007, file-0331-atom-0001, file-0331-atom-0002, file-0332-atom-0002, file-0332-atom-0003, file-0332-atom-0004, file-0332-atom-0005, file-0332-atom-0006, file-0332-atom-0007, file-0332-atom-0008, file-0332-atom-0009, file-0332-atom-0010, file-0332-atom-0011, file-0332-atom-0012, file-0332-atom-0013, file-0332-atom-0014, file-0332-atom-0015, file-0332-atom-0016, file-0332-atom-0017, file-0332-atom-0018, file-0332-atom-0019, file-0332-atom-0020, file-0332-atom-0021, file-0332-atom-0022, file-0333-atom-0002, file-0333-atom-0003, file-0333-atom-0004, file-0334-atom-0001, file-0334-atom-0002, file-0334-atom-0003, file-0344-atom-0008, file-0355-atom-0001, file-0358-atom-0001, file-0358-atom-0002, file-0358-atom-0003, file-0358-atom-0004, file-0467-atom-0001, file-0467-atom-0002
- `intentionally_absent`: file-0087-atom-0005, file-0087-atom-0006, file-0087-atom-0007, file-0087-atom-0010, file-0087-atom-0013, file-0091-atom-0001, file-0092-atom-0022, file-0092-atom-0023, file-0092-atom-0024, file-0092-atom-0025, file-0092-atom-0035, file-0093-atom-0001, file-0304-atom-0002, file-0304-atom-0016, file-0304-atom-0024, file-0304-atom-0026, file-0309-atom-0003, file-0309-atom-0004, file-0309-atom-0005, file-0313-atom-0001, file-0332-atom-0032, file-0332-atom-0033, file-0332-atom-0035, file-0335-atom-0001, file-0336-atom-0001, file-0336-atom-0002, file-0337-atom-0001, file-0337-atom-0002, file-0337-atom-0003, file-0338-atom-0001, file-0339-atom-0001, file-0340-atom-0001, file-0340-atom-0002, file-0341-atom-0001, file-0341-atom-0002, file-0342-atom-0001, file-0342-atom-0002, file-0342-atom-0003, file-0342-atom-0004, file-0342-atom-0005, file-0414-atom-0001, file-0415-atom-0001, file-0415-atom-0002, file-0415-atom-0003, file-0415-atom-0004, file-0415-atom-0005, file-0415-atom-0006, file-0415-atom-0007, file-0415-atom-0008, file-0416-atom-0001, file-0416-atom-0002, file-0417-atom-0001, file-0418-atom-0001, file-0419-atom-0001, file-0420-atom-0001, file-0421-atom-0001, file-0421-atom-0002, file-0421-atom-0003, file-0422-atom-0001, file-0422-atom-0002, file-0423-atom-0001, file-0423-atom-0002, file-0423-atom-0003, file-0423-atom-0004, file-0423-atom-0005, file-0423-atom-0006, file-0423-atom-0007, file-0423-atom-0008, file-0423-atom-0009, file-0423-atom-0010, file-0423-atom-0011, file-0423-atom-0012, file-0423-atom-0013, file-0529-atom-0005
- `moved_to_dependency`: file-0087-atom-0008
- `noise`: file-0087-atom-0001, file-0087-atom-0009, file-0087-atom-0012
- `structural_equivalent`: file-0087-atom-0002, file-0087-atom-0011, file-0088-atom-0002, file-0089-atom-0001, file-0098-atom-0001, file-0098-atom-0002, file-0098-atom-0003, file-0163-atom-0001, file-0194-atom-0002, file-0250-atom-0001, file-0250-atom-0002, file-0278-atom-0003, file-0278-atom-0004, file-0282-atom-0001, file-0283-atom-0001, file-0283-atom-0002, file-0283-atom-0003, file-0285-atom-0001, file-0304-atom-0011, file-0304-atom-0018, file-0304-atom-0019, file-0304-atom-0020, file-0304-atom-0021, file-0304-atom-0022, file-0304-atom-0023, file-0316-atom-0010, file-0328-atom-0001, file-0329-atom-0001, file-0329-atom-0003, file-0329-atom-0004, file-0329-atom-0005, file-0329-atom-0006, file-0330-atom-0001, file-0332-atom-0001, file-0332-atom-0023, file-0332-atom-0025, file-0332-atom-0026, file-0332-atom-0027, file-0332-atom-0028, file-0332-atom-0029, file-0332-atom-0030, file-0332-atom-0031, file-0332-atom-0036, file-0332-atom-0037, file-0332-atom-0038, file-0332-atom-0039, file-0332-atom-0040, file-0332-atom-0041, file-0333-atom-0001, file-0333-atom-0005, file-0333-atom-0006, file-0333-atom-0007, file-0366-atom-0001, file-0389-atom-0001, file-0401-atom-0001, file-0408-atom-0001, file-0412-atom-0001, file-0463-atom-0001, file-0465-atom-0001, file-0469-atom-0001, file-0514-atom-0001, file-0521-atom-0002, file-0525-atom-0001, file-0526-atom-0001, file-0529-atom-0002, file-0529-atom-0003, file-0529-atom-0004, file-0535-atom-0001, file-0537-atom-0001, file-0540-atom-0003, file-0541-atom-0001, file-0542-atom-0001, file-0543-atom-0001, file-0550-atom-0001

## Payload building, execution, and consensus validation

Payload builder/execution hooks, block verification, engine-tree behavior, consensus validation, chain-spec constants, extra_data policy, block rewards, and genesis-derived behavior.

- Counts: `54` atoms; `39` high-risk; `51` review-required; statuses `{'structural_equivalent': 37, 'blocked': 4, 'moved_to_dependency': 2, 'intentionally_absent': 9, 'exact': 2}`.

Actionable gaps:
- `file-0026-atom-0002` `blocked`: `crates/chainspec/src/api.rs` — Environment-gated consensus constants only where already shipped.
- `file-0090-atom-0002` `blocked`: `crates/ethereum/payload/src/config.rs` — Payload builder config preserves the default build deadline, environment override, invalid-env fallback, and explicit override semantics.
- `file-0092-atom-0010` `blocked`: `crates/ethereum/payload/src/lib.rs` — Pool manager / EVM integration remains available to nodebuilder and payload code.
- `file-0092-atom-0017` `blocked`: `crates/ethereum/payload/src/lib.rs` — Builder-produced blocks must replay under verifier rules.

Representative atoms:
- `file-0026-atom-0001` `structural_equivalent`: `crates/chainspec/src/api.rs` — EthChainSpec exposes an optional per-chain maximum header extra_data size, with None meaning unbounded.
- `file-0028-atom-0001` `structural_equivalent`: `crates/chainspec/src/spec.rs` — ChainSpec stores a per-chain optional header extra_data size limit, defaulting Ethereum networks to MAXIMUM_EXTRA_DATA_SIZE.
- `file-0028-atom-0003` `structural_equivalent`: `crates/chainspec/src/spec.rs` — Chain specs built from genesis files disable the Ethereum extra_data size cap so Ritual/Summit chains can embed CL snapshots for recovery.
- `file-0054-atom-0001` `exact`: `crates/engine/local/src/payload.rs` — The local Ethereum payload attributes builder must explicitly set `EthPayloadAttributes.extra_data` to `None` when constructing payload attributes.
- `file-0200-atom-0002` `exact`: `crates/node/core/src/args/payload_builder.rs` — Payload-builder extra_data argument handling accepts large Ritual extra_data values while rejecting invalid extra_data input.
- `file-0027-atom-0001` `moved_to_dependency`: `crates/chainspec/src/constants.rs` — Summit chains use a custom 7-field deposit event topic for Ed25519 node keys plus BLS consensus keys.
- `file-0028-atom-0002` `moved_to_dependency`: `crates/chainspec/src/spec.rs` — Genesis-derived deposit contracts use the Summit deposit event topic instead of the Ethereum mainnet deposit topic.
- `file-0047-atom-0001` `intentionally_absent`: `crates/consensus/common/Cargo.toml` — `reth-consensus-common` adds a direct workspace dependency on `tracing` so the crate can compile downstream-only tracing macros used in its validation code.
- `file-0056-atom-0001` `intentionally_absent`: `crates/engine/tree/Cargo.toml` — The downstream engine-tree crate adds a workspace dependency on `ritual-metrics` so Ritual-specific metrics instrumentation in this crate can compile.
- `file-0084-atom-0001` `intentionally_absent`: `crates/ethereum/node/src/payload.rs` — The Ethereum node propagates the configured maximum block tx-list size cap into the payload builder so block construction enforces `max_block_size_bytes`.
- `file-0026-atom-0002` `blocked`: `crates/chainspec/src/api.rs` — Environment-gated consensus constants only where already shipped.
- `file-0090-atom-0002` `blocked`: `crates/ethereum/payload/src/config.rs` — Payload builder config preserves the default build deadline, environment override, invalid-env fallback, and explicit override semantics.
- `file-0092-atom-0010` `blocked`: `crates/ethereum/payload/src/lib.rs` — Pool manager / EVM integration remains available to nodebuilder and payload code.

Trace IDs by status:

- `blocked`: file-0026-atom-0002, file-0090-atom-0002, file-0092-atom-0010, file-0092-atom-0017
- `exact`: file-0054-atom-0001, file-0200-atom-0002
- `intentionally_absent`: file-0047-atom-0001, file-0056-atom-0001, file-0084-atom-0001, file-0090-atom-0001, file-0206-atom-0001, file-0211-atom-0001, file-0218-atom-0001, file-0311-atom-0001, file-0314-atom-0001
- `moved_to_dependency`: file-0027-atom-0001, file-0028-atom-0002
- `structural_equivalent`: file-0026-atom-0001, file-0028-atom-0001, file-0028-atom-0003, file-0028-atom-0004, file-0028-atom-0005, file-0028-atom-0006, file-0028-atom-0007, file-0059-atom-0001, file-0064-atom-0001, file-0074-atom-0001, file-0076-atom-0001, file-0079-atom-0002, file-0088-atom-0001, file-0089-atom-0002, file-0092-atom-0001, file-0092-atom-0020, file-0093-atom-0002, file-0094-atom-0001, file-0136-atom-0001, file-0189-atom-0001, file-0190-atom-0001, file-0191-atom-0001, file-0192-atom-0001, file-0196-atom-0001, file-0197-atom-0001, file-0200-atom-0001, file-0201-atom-0001, file-0231-atom-0001, file-0232-atom-0001, file-0233-atom-0001, file-0236-atom-0001, file-0364-atom-0001, file-0370-atom-0001, file-0402-atom-0001, file-0407-atom-0001, file-0527-atom-0001, file-0528-atom-0001

## RPC and external API surface

Ritual RPC namespace, async result submission, txpool/RPC API extensions, pubsub surfaces, and externally visible request/response compatibility.

- Counts: `32` atoms; `27` high-risk; `30` review-required; statuses `{'blocked': 10, 'structural_equivalent': 18, 'exact': 2, 'intentionally_absent': 2}`.

Actionable gaps:
- `file-0092-atom-0006` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 2 (Async Precompile Detection And Validation) preserves parent state detection: Builder/verifier simulate against parent block state for deterministic async detection; Port authority model: RPC provides early feedback (`#204`, `#231`, `#307`), while builder/verifier re-simulate async origin txs and hard-fail invalid commitments (`#145`).
- `file-0365-atom-0002` `blocked`: `crates/rpc/rpc-api/src/ritual.rs` — No-port unless later behavior depends on it: reverted optimized WS/pubsub behavior (`#107`).
- `file-0385-atom-0001` `blocked`: `crates/rpc/rpc-eth-types/src/fee_history.rs` — Fee-history behavior changed in the downstream diff, but the current same-path/overlapping-symbol evidence does not establish the exact fee-history behavior preserved by the v2.2 port.
- `file-0396-atom-0002` `blocked`: `crates/rpc/rpc/src/async_tx_validator.rs` — validate async payload preserves the production behavior asserted by downstream tests: test_valid_http_request, test_ttl_zero, test_ttl_exceeded, test_zero_executor, test_empty_url.
- `file-0396-atom-0003` `blocked`: `crates/rpc/rpc/src/async_tx_validator.rs` — RLP/2718, compact codec, DB/static-file, receipt, and RPC transaction conversion compatibility.
- `file-0396-atom-0004` `blocked`: `crates/rpc/rpc/src/async_tx_validator.rs` — RPC validation simulates pending txs for immediate user feedback but is not the authority.
- `file-0396-atom-0005` `blocked`: `crates/rpc/rpc/src/async_tx_validator.rs` — Async context mode distinguishes build, verify, and RPC simulation.
- `file-0402-atom-0002` `blocked`: `crates/rpc/rpc/src/eth/helpers/pending_block.rs` — PR preservation `#249` `embed-multisig` keeps live downstream behavior: max-extra-data plumbing.
- `file-0513-atom-0002` `blocked`: `crates/tracing/src/ritual_router.rs` — Bounded block-build traces and demotion/cap observations.
- `file-0513-atom-0003` `blocked`: `crates/tracing/src/ritual_router.rs` — Bounded async simulation traces.

Representative atoms:
- `file-0092-atom-0027` `structural_equivalent`: `crates/ethereum/payload/src/lib.rs` — Fulfilled async processing batch-reads SPC verification data before per-transaction processing and falls back to per-tx verification only if the batch read fails.
- `file-0274-atom-0003` `structural_equivalent`: `crates/ritual-async-commitment-validator/src/lib.rs` — PR preservation `#145` `valconstraints-async-commitment` keeps live downstream behavior: verifier re-simulation of async origin tx at parent/commit context.
- `file-0323-atom-0004` `structural_equivalent`: `crates/ritual-precompile-codecs/src/llm_call.rs` — LLM async payload decoding preserves the 30-field request shape while extracting executor, encrypted secrets, TTL, user public key, messages JSON, and model for shared RPC and builder validation.
- `file-0305-atom-0001` `exact`: `crates/ritual-blocking-pubsub/Cargo.toml` — The downstream diff for crates/ritual-blocking-pubsub/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0306-atom-0001` `exact`: `crates/ritual-blocking-pubsub/src/lib.rs` — The downstream diff for crates/ritual-blocking-pubsub/src/lib.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0396-atom-0006` `intentionally_absent`: `crates/rpc/rpc/src/async_tx_validator.rs` — RPC async validation is explicitly a user-feedback layer that delegates consensus-relevant payload checks to shared validation so invalid async traffic receives descriptive errors without becoming the authority over builder or verifier behavior.
- `file-0396-atom-0008` `intentionally_absent`: `crates/rpc/rpc/src/async_tx_validator.rs` — RPC wallet validation calls the same commitment wallet verifier as the builder and translates insufficient balance, lock duration, and model failures into user-facing async validation errors.
- `file-0092-atom-0006` `blocked`: `crates/ethereum/payload/src/lib.rs` — Feature section 2 (Async Precompile Detection And Validation) preserves parent state detection: Builder/verifier simulate against parent block state for deterministic async detection; Port authority model: RPC provides early feedback (`#204`, `#231`, `#307`), while builder/verifier re-simulate async origin txs and hard-fail invalid commitments (`#145`).
- `file-0365-atom-0002` `blocked`: `crates/rpc/rpc-api/src/ritual.rs` — No-port unless later behavior depends on it: reverted optimized WS/pubsub behavior (`#107`).
- `file-0385-atom-0001` `blocked`: `crates/rpc/rpc-eth-types/src/fee_history.rs` — Fee-history behavior changed in the downstream diff, but the current same-path/overlapping-symbol evidence does not establish the exact fee-history behavior preserved by the v2.2 port.

Trace IDs by status:

- `blocked`: file-0092-atom-0006, file-0365-atom-0002, file-0385-atom-0001, file-0396-atom-0002, file-0396-atom-0003, file-0396-atom-0004, file-0396-atom-0005, file-0402-atom-0002, file-0513-atom-0002, file-0513-atom-0003
- `exact`: file-0305-atom-0001, file-0306-atom-0001
- `intentionally_absent`: file-0396-atom-0006, file-0396-atom-0008
- `structural_equivalent`: file-0092-atom-0027, file-0274-atom-0003, file-0323-atom-0004, file-0344-atom-0011, file-0363-atom-0001, file-0375-atom-0001, file-0376-atom-0001, file-0377-atom-0001, file-0393-atom-0001, file-0398-atom-0001, file-0399-atom-0001, file-0413-atom-0001, file-0494-atom-0001, file-0495-atom-0001, file-0504-atom-0001, file-0537-atom-0003, file-0537-atom-0010, file-0540-atom-0002

## Storage, provider, and database infrastructure

Provider traits, database/static-file surfaces, MDBX/nippy/db-api changes, state provider plumbing, and canonical-state subscription infrastructure.

- Counts: `19` atoms; `11` high-risk; `17` review-required; statuses `{'blocked': 2, 'structural_equivalent': 13, 'noise': 1, 'moved_to_dependency': 1, 'exact': 2}`.

Actionable gaps:
- `file-0108-atom-0002` `blocked`: `crates/evm/src/lib.rs` — Preserve: Do not preserve temporary permissive verification from `#93` unless explicitly gated by skip-validity config.
- `file-0108-atom-0003` `blocked`: `crates/evm/src/lib.rs` — Coverage accounting for this merge cannot attach per-file atoms to crates/evm/src/registry_db.rs or historical_header_cache.rs because those paths are not queue rows; catalog hints may be stale, renamed, or refer to unchanged modules. Confirm on downstream HEAD whether those files exist, were removed, or were merged into other modules; generic registry DB state may appear inline (e.g. StateProviderDatabase locals) elsewhere in the evm/execute path.

Representative atoms:
- `file-0253-atom-0001` `structural_equivalent`: `crates/prune/prune/src/pruner.rs` — The downstream diff for crates/prune/prune/src/pruner.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0263-atom-0001` `structural_equivalent`: `crates/prune/prune/src/segments/user/storage_history.rs` — The downstream diff for crates/prune/prune/src/segments/user/storage_history.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0304-atom-0003` `structural_equivalent`: `crates/ritual-block-verification/src/verifier.rs` — commitment passes preserves the production behavior asserted by downstream tests: prop_valid_commitment_passes_both.
- `file-0459-atom-0002` `exact`: `crates/storage/codecs/src/alloy/passkey_signature.rs` — compact p256 preserves the production behavior asserted by downstream tests: test_compact_p256_signature.
- `file-0459-atom-0003` `exact`: `crates/storage/codecs/src/alloy/passkey_signature.rs` — compact secp256k1 preserves the production behavior asserted by downstream tests: test_compact_secp256k1_signature.
- `file-0304-atom-0031` `moved_to_dependency`: `crates/ritual-block-verification/src/verifier.rs` — Summit validator deposit behavior.
- `file-0108-atom-0002` `blocked`: `crates/evm/src/lib.rs` — Preserve: Do not preserve temporary permissive verification from `#93` unless explicitly gated by skip-validity config.
- `file-0108-atom-0003` `blocked`: `crates/evm/src/lib.rs` — Coverage accounting for this merge cannot attach per-file atoms to crates/evm/src/registry_db.rs or historical_header_cache.rs because those paths are not queue rows; catalog hints may be stale, renamed, or refer to unchanged modules. Confirm on downstream HEAD whether those files exist, were removed, or were merged into other modules; generic registry DB state may appear inline (e.g. StateProviderDatabase locals) elsewhere in the evm/execute path.
- `file-0268-atom-0001` `noise`: `crates/ress/protocol/src/provider.rs` — The downstream diff for crates/ress/protocol/src/provider.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Trace IDs by status:

- `blocked`: file-0108-atom-0002, file-0108-atom-0003
- `exact`: file-0459-atom-0002, file-0459-atom-0003
- `moved_to_dependency`: file-0304-atom-0031
- `noise`: file-0268-atom-0001
- `structural_equivalent`: file-0253-atom-0001, file-0263-atom-0001, file-0304-atom-0003, file-0304-atom-0005, file-0304-atom-0006, file-0304-atom-0007, file-0304-atom-0027, file-0304-atom-0028, file-0475-atom-0001, file-0498-atom-0001, file-0499-atom-0001, file-0502-atom-0001, file-0503-atom-0001

## Network and P2P compatibility

P2P/discovery/network/download/wire compatibility changes and any network test fixture behavior retained or refactored by v2.2.

- Counts: `28` atoms; `1` high-risk; `22` review-required; statuses `{'structural_equivalent': 16, 'covered_by_upstream': 1, 'intentionally_absent': 5, 'noise': 3, 'blocked': 2, 'exact': 1}`.

Actionable gaps:
- `file-0311-atom-0002` `blocked`: `crates/ritual-metrics/src/block.rs` — Ritual JSON tracing router for selected lifecycle targets.
- `file-0431-atom-0001` `blocked`: `crates/stages/stages/src/stages/execution.rs` — The downstream diff for crates/stages/stages/src/stages/execution.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Representative atoms:
- `file-0042-atom-0001` `structural_equivalent`: `crates/cli/commands/src/stage/run.rs` — The downstream diff for crates/cli/commands/src/stage/run.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0050-atom-0001` `structural_equivalent`: `crates/e2e-test-utils/src/network.rs` — The downstream diff for crates/e2e-test-utils/src/network.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0071-atom-0001` `structural_equivalent`: `crates/era/src/era1_file.rs` — The downstream diff for crates/era/src/era1_file.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0357-atom-0001` `exact`: `crates/ritual-tee-registry-reader/src/reader.rs` — The downstream diff for crates/ritual-tee-registry-reader/src/reader.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0073-atom-0003` `covered_by_upstream`: `crates/errors/src/error.rs` — The file stops enforcing that `BlockExecutionError` must be exactly 56 bytes on x86_64.
- `file-0157-atom-0001` `intentionally_absent`: `crates/net/network/Cargo.toml` — The downstream `reth-network` crate adds a direct workspace dependency on `ritual-metrics` so Ritual-specific network transaction metric/logging hooks can compile and link.
- `file-0207-atom-0001` `intentionally_absent`: `crates/optimism/cli/src/commands/import.rs` — The downstream diff for crates/optimism/cli/src/commands/import.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0310-atom-0001` `intentionally_absent`: `crates/ritual-metrics/Cargo.toml` — The downstream diff for crates/ritual-metrics/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0311-atom-0002` `blocked`: `crates/ritual-metrics/src/block.rs` — Ritual JSON tracing router for selected lifecycle targets.
- `file-0431-atom-0001` `blocked`: `crates/stages/stages/src/stages/execution.rs` — The downstream diff for crates/stages/stages/src/stages/execution.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0242-atom-0001` `noise`: `crates/primitives-traits/Cargo.toml` — The downstream diff for crates/primitives-traits/Cargo.toml introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0257-atom-0001` `noise`: `crates/prune/prune/src/segments/static_file/headers.rs` — The downstream diff for crates/prune/prune/src/segments/static_file/headers.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.
- `file-0258-atom-0001` `noise`: `crates/prune/prune/src/segments/static_file/transactions.rs` — The downstream diff for crates/prune/prune/src/segments/static_file/transactions.rs introduces behavior or wiring that must be accounted for in the v2.2 merge target.

Trace IDs by status:

- `blocked`: file-0311-atom-0002, file-0431-atom-0001
- `covered_by_upstream`: file-0073-atom-0003
- `exact`: file-0357-atom-0001
- `intentionally_absent`: file-0157-atom-0001, file-0207-atom-0001, file-0310-atom-0001, file-0312-atom-0001, file-0513-atom-0001
- `noise`: file-0242-atom-0001, file-0257-atom-0001, file-0258-atom-0001
- `structural_equivalent`: file-0042-atom-0001, file-0050-atom-0001, file-0071-atom-0001, file-0131-atom-0001, file-0159-atom-0001, file-0165-atom-0001, file-0169-atom-0001, file-0172-atom-0001, file-0199-atom-0001, file-0259-atom-0001, file-0262-atom-0001, file-0264-atom-0001, file-0353-atom-0001, file-0511-atom-0001, file-0512-atom-0001, file-0561-atom-0001
