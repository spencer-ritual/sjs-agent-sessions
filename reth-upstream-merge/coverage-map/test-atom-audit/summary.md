# Test Atom Audit Summary

- Total files scanned: 579
- Total test cases/helpers found: 654
- Test cases covered by existing atoms: 5
- New atoms created: 649
- Noise test changes: 41
- Blocked cases: 0

## New Atom Mapping Status

- exact: 200
- missing: 449

## Highest-Risk Missing Test-Derived Invariants

- `test-file-0281-atom-0002` `crates/ritual-async-fees/src/llm.rs` `test_llm_has_error_prefix_constant_used_in_decode`: LLM has error prefix constant used in decode preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, encoding, gas, fees, rewards, consensus-constant, negative-path)
- `test-file-0281-atom-0001` `crates/ritual-async-fees/src/llm.rs` `test_llm_has_error_returns_constant_fee`: LLM has error returns constant fee preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, gas, fees, rewards, consensus-constant, negative-path)
- `test-file-0283-atom-0003` `crates/ritual-async-fees/src/scheduled.rs` `test_extract_callback_gas_wrong_address`: extract callback gas wrong address is rejected or classified on the expected negative path. (risk: async-fsm, scheduled, gas, fees, consensus-constant, negative-path)
- `test-file-0092-atom-0005` `crates/ethereum/payload/src/lib.rs` `test_verify_spc_wrong_input_hash_fails`: verify SPC wrong input hash fails is rejected or classified on the expected negative path. (risk: async-fsm, payload, encoding, verifier, negative-path)
- `test-file-0278-atom-0009` `crates/ritual-async-fees/src/gas.rs` `test_effective_gas_limit_for_block_scheduled_tx`: effective gas limit for block scheduled tx preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, scheduled, gas, fees, rewards)
- `test-file-0280-atom-0015` `crates/ritual-async-fees/src/lib.rs` `test_delivery_has_error_true`: delivery has error true preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, gas, fees, rewards, negative-path)
- `test-file-0280-atom-0016` `crates/ritual-async-fees/src/lib.rs` `test_delivery_has_error_false`: delivery has error false preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, gas, fees, rewards, negative-path)
- `test-file-0280-atom-0017` `crates/ritual-async-fees/src/lib.rs` `test_delivery_has_error_none`: delivery has error none preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, gas, fees, rewards, negative-path)
- `test-file-0280-atom-0020` `crates/ritual-async-fees/src/lib.rs` `test_da_error_fee_less_than_phase1_escrow`: DA error fee less than phase1 escrow preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, gas, fees, rewards, negative-path)
- `test-file-0280-atom-0021` `crates/ritual-async-fees/src/lib.rs` `test_delivery_has_error_realistic_image_error`: delivery has error realistic image error preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, gas, fees, rewards, negative-path)
- `test-file-0283-atom-0001` `crates/ritual-async-fees/src/scheduled.rs` `create_mock_call_executed_log`: create mock call executed log preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, scheduled, gas, fees, rewards)
- `test-file-0283-atom-0002` `crates/ritual-async-fees/src/scheduled.rs` `test_extract_callback_gas_success`: extract callback gas success preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, scheduled, gas, fees, rewards)
- `test-file-0283-atom-0004` `crates/ritual-async-fees/src/scheduled.rs` `test_extract_callback_gas_empty_logs`: extract callback gas empty logs is rejected or classified on the expected negative path. (risk: async-fsm, scheduled, gas, fees, negative-path)
- `test-file-0283-atom-0005` `crates/ritual-async-fees/src/scheduled.rs` `test_get_callback_gas_or_fallback_success`: get callback gas or fallback success preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, scheduled, gas, fees, rewards)
- `test-file-0283-atom-0006` `crates/ritual-async-fees/src/scheduled.rs` `test_get_callback_gas_or_fallback_failed`: get callback gas or fallback failed is rejected or classified on the expected negative path. (risk: async-fsm, scheduled, gas, fees, negative-path)
- `test-file-0283-atom-0007` `crates/ritual-async-fees/src/scheduled.rs` `test_get_callback_gas_or_fallback_not_found`: get callback gas or fallback not found is rejected or classified on the expected negative path. (risk: async-fsm, scheduled, gas, fees, negative-path)
- `test-file-0304-atom-0059` `crates/ritual-block-verification/src/verifier.rs` `diff_eq_fee_agent_phase2_deterministic`: diff eq fee agent phase2 deterministic preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, verifier, gas, fees, rewards)
- `test-file-0304-atom-0060` `crates/ritual-block-verification/src/verifier.rs` `diff_eq_fee_phase2_http_deterministic`: diff eq fee phase2 HTTP deterministic preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, verifier, gas, fees, rewards)
- `test-file-0304-atom-0061` `crates/ritual-block-verification/src/verifier.rs` `prop_fee_agent_phase2_deterministic`: fee agent phase2 deterministic preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, verifier, gas, fees, rewards)
- `test-file-0304-atom-0062` `crates/ritual-block-verification/src/verifier.rs` `prop_fee_phase2_http_deterministic`: fee phase2 HTTP deterministic preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, verifier, gas, fees, rewards)
- `test-file-0325-atom-0008` `crates/ritual-precompile-codecs/src/persistent_agent.rs` `test_delivery_config_extraction`: delivery config extraction preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, encoding, gas, fees, rewards)
- `test-file-0092-atom-0006` `crates/ethereum/payload/src/lib.rs` `test_verify_spc_empty_executor_key_fails`: verify SPC empty executor key fails is rejected or classified on the expected negative path. (risk: async-fsm, payload, verifier, executor-selection, negative-path)
- `test-file-0278-atom-0008` `crates/ritual-async-fees/src/gas.rs` `test_effective_gas_limit_for_block_settlement_tx`: effective gas limit for block seTTLement tx preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, gas, fees, rewards, consensus-constant)
- `test-file-0279-atom-0002` `crates/ritual-async-fees/src/http.rs` `test_http_executor_fee_with_output`: HTTP executor fee with output preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, executor-selection, gas, fees, rewards)
- `test-file-0280-atom-0005` `crates/ritual-async-fees/src/lib.rs` `test_dkms_executor_fee_is_fixed`: DKMS executor fee is fixed preserves the expected fee, gas, reward, or escrow calculation. (risk: async-fsm, executor-selection, gas, fees, rewards)

## Canonical Artifacts Recommended For Patching

- `coverage-map/files/file-0079.json`
- `coverage-map/files/file-0088.json`
- `coverage-map/files/file-0089.json`
- `coverage-map/files/file-0090.json`
- `coverage-map/files/file-0091.json`
- `coverage-map/files/file-0092.json`
- `coverage-map/files/file-0093.json`
- `coverage-map/files/file-0094.json`
- `coverage-map/files/file-0106.json`
- `coverage-map/files/file-0200.json`
- `coverage-map/files/file-0274.json`
- `coverage-map/files/file-0277.json`
- `coverage-map/files/file-0278.json`
- `coverage-map/files/file-0279.json`
- `coverage-map/files/file-0280.json`
- `coverage-map/files/file-0281.json`
- `coverage-map/files/file-0282.json`
- `coverage-map/files/file-0283.json`
- `coverage-map/files/file-0284.json`
- `coverage-map/files/file-0292.json`
- `coverage-map/files/file-0293.json`
- `coverage-map/files/file-0295.json`
- `coverage-map/files/file-0297.json`
- `coverage-map/files/file-0304.json`
- `coverage-map/files/file-0309.json`
- `coverage-map/files/file-0316.json`
- `coverage-map/files/file-0320.json`
- `coverage-map/files/file-0321.json`
- `coverage-map/files/file-0323.json`
- `coverage-map/files/file-0324.json`
- `coverage-map/files/file-0325.json`
- `coverage-map/files/file-0326.json`
- `coverage-map/files/file-0329.json`
- `coverage-map/files/file-0332.json`
- `coverage-map/files/file-0333.json`
- `coverage-map/files/file-0334.json`
- `coverage-map/files/file-0336.json`
- `coverage-map/files/file-0337.json`
- `coverage-map/files/file-0340.json`
- `coverage-map/files/file-0341.json`
- `coverage-map/files/file-0342.json`
- `coverage-map/files/file-0344.json`
- `coverage-map/files/file-0348.json`
- `coverage-map/files/file-0352.json`
- `coverage-map/files/file-0357.json`
- `coverage-map/files/file-0396.json`
- `coverage-map/files/file-0421.json`
- `coverage-map/files/file-0422.json`
- `coverage-map/files/file-0423.json`
- `coverage-map/files/file-0427.json`
- `coverage-map/files/file-0459.json`
- `coverage-map/files/file-0468.json`
- `coverage-map/files/file-0469.json`
- `coverage-map/files/file-0529.json`
- `coverage-map/files/file-0537.json`
- `coverage-map/files/file-0540.json`
- `coverage-map/files/file-0545.json`

## Notes

- The original downstream diff sidecars were absent from the session directory at audit start, so they were regenerated from the commit range in the orchestrator prompt before this supplemental pass.
- Exact destination test/helper-name matches were treated as exact evidence for the test-derived atom, but they do not replace production behavior review when the canonical production atom is generic, missing, or non-exact.
