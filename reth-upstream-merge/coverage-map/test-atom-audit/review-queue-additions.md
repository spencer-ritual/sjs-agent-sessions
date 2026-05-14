# Test-Derived Review Queue Additions

## file_index 79: `crates/ethereum/evm/src/execute.rs`

- new_atom: `test-file-0079-atom-0001`
- source hunk: `@@ -876,4 +882,122 @@ mod tests {`
- test/helper: `test_custom_block_reward_post_merge`
- invariant: custom block reward post merge preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/evm/src/execute.rs`

## file_index 79: `crates/ethereum/evm/src/execute.rs`

- new_atom: `test-file-0079-atom-0002`
- source hunk: `@@ -876,4 +882,122 @@ mod tests {`
- test/helper: `test_no_block_reward_post_merge_without_custom_reward`
- invariant: no block reward post merge without custom reward preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/evm/src/execute.rs`

## file_index 88: `crates/ethereum/payload/src/bundle.rs`

- new_atom: `test-file-0088-atom-0001`
- source hunk: `@@ -0,0 +1,194 @@`
- test/helper: `test_tx_source_equality`
- invariant: tx source equality preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/bundle.rs`

## file_index 89: `crates/ethereum/payload/src/collector.rs`

- new_atom: `test-file-0089-atom-0001`
- source hunk: `@@ -0,0 +1,124 @@`
- test/helper: `test_collected_bundles_new`
- invariant: collected bundles new preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/collector.rs`

## file_index 89: `crates/ethereum/payload/src/collector.rs`

- new_atom: `test-file-0089-atom-0002`
- source hunk: `@@ -0,0 +1,124 @@`
- test/helper: `test_can_fit_transaction`
- invariant: can fit transaction preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/collector.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0001`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_default_build_deadline`
- invariant: default build deadline preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0002`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_build_deadline_from_env`
- invariant: build deadline from env preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0003`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_build_deadline_invalid_env_falls_back`
- invariant: build deadline invalid env falls back is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0004`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_with_build_deadline_override`
- invariant: with build deadline override preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0005`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_builder_pattern_chaining`
- invariant: builder pattern chaining is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0006`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_zero_deadline_is_valid`
- invariant: zero deadline is valid is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0007`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_large_deadline_is_valid`
- invariant: large deadline is valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0008`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_config_clone_preserves_deadline`
- invariant: config clone preserves deadline preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 90: `crates/ethereum/payload/src/config.rs`

- new_atom: `test-file-0090-atom-0009`
- source hunk: `@@ -53,3 +88,80 @@ pub fn calculate_block_gas_limit(parent_gas_limit: u64, desired_gas_limit: u64)`
- test/helper: `test_gas_limit_calculation`
- invariant: gas limit calculation preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/config.rs`

## file_index 91: `crates/ethereum/payload/src/execution.rs`

- new_atom: `test-file-0091-atom-0001`
- source hunk: `@@ -0,0 +1,311 @@`
- test/helper: `test_execution_result_default`
- invariant: execution result default is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/execution.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0001`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `test_keypair`
- invariant: keypair is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0002`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `make_job`
- invariant: make job is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0003`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `test_verify_spc_valid_signature_passes`
- invariant: verify SPC valid signature passes is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0004`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `test_verify_spc_wrong_output_fails`
- invariant: verify SPC wrong output fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0005`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `test_verify_spc_wrong_input_hash_fails`
- invariant: verify SPC wrong input hash fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0006`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `test_verify_spc_empty_executor_key_fails`
- invariant: verify SPC empty executor key fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0007`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `fix_for_current_incident_regular_gets_at_least_its_cap`
- invariant: fix for current incident regular gets at least its cap preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0008`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `lots_of_scheduled_no_regular_uses_full_total_for_scheduled`
- invariant: lots of scheduled no regular uses full total for scheduled preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0009`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `lots_of_regular_no_scheduled_uses_full_total_for_regular`
- invariant: lots of regular no scheduled uses full total for regular preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0010`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `both_under_their_caps_no_truncation`
- invariant: both under their caps no truncation preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0011`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `both_at_cap_truncates_scheduled_first`
- invariant: both at cap truncates scheduled first preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0013`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `category_caps_above_total_are_clamped`
- invariant: category caps above total are clamped preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0014`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `zero_regular_cap_disables_regular_lane`
- invariant: zero regular cap disables regular lane is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0015`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `zero_scheduled_cap_disables_scheduled_lane`
- invariant: zero scheduled cap disables scheduled lane is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0016`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `leftover_after_regular_fills_into_scheduled`
- invariant: leftover after regular fills into scheduled preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0017`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `leftover_after_scheduled_cap_fills_into_regular`
- invariant: leftover after scheduled cap fills into regular preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0018`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `under_total_cap_with_unmet_demand_only_regular`
- invariant: under total cap with unmet demand only regular preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 92: `crates/ethereum/payload/src/lib.rs`

- new_atom: `test-file-0092-atom-0019`
- source hunk: `@@ -194,132 +1255,5106 @@ where`
- test/helper: `neither_category_exceeds_caps_or_total`
- invariant: neither category exceeds caps or total preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/lib.rs`

## file_index 93: `crates/ethereum/payload/src/unified_builder.rs`

- new_atom: `test-file-0093-atom-0001`
- source hunk: `@@ -0,0 +1,341 @@`
- test/helper: `test_can_fit_in_block`
- invariant: can fit in block preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/unified_builder.rs`

## file_index 93: `crates/ethereum/payload/src/unified_builder.rs`

- new_atom: `test-file-0093-atom-0002`
- source hunk: `@@ -0,0 +1,341 @@`
- test/helper: `test_extract_delivery_tip_short_input`
- invariant: extract delivery tip short input extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/unified_builder.rs`

## file_index 94: `crates/ethereum/payload/src/unified_execution.rs`

- new_atom: `test-file-0094-atom-0001`
- source hunk: `@@ -0,0 +1,537 @@`
- test/helper: `test_unified_execution_result_default`
- invariant: unified execution result default is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ethereum/payload/src/unified_execution.rs`

## file_index 106: `crates/evm/src/async_context_tests.rs`

- new_atom: `test-file-0106-atom-0001`
- source hunk: `@@ -0,0 +1,99 @@`
- test/helper: `test_async_context_default_values`
- invariant: async context default values is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/evm/src/async_context_tests.rs`

## file_index 106: `crates/evm/src/async_context_tests.rs`

- new_atom: `test-file-0106-atom-0002`
- source hunk: `@@ -0,0 +1,99 @@`
- test/helper: `test_async_context_execution_mode_setting`
- invariant: async context execution mode setting preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/evm/src/async_context_tests.rs`

## file_index 106: `crates/evm/src/async_context_tests.rs`

- new_atom: `test-file-0106-atom-0003`
- source hunk: `@@ -0,0 +1,99 @@`
- test/helper: `test_async_context_execution_results`
- invariant: async context execution results is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/evm/src/async_context_tests.rs`

## file_index 106: `crates/evm/src/async_context_tests.rs`

- new_atom: `test-file-0106-atom-0004`
- source hunk: `@@ -0,0 +1,99 @@`
- test/helper: `test_async_context_spc_call_index`
- invariant: async context SPC call index preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/evm/src/async_context_tests.rs`

## file_index 106: `crates/evm/src/async_context_tests.rs`

- new_atom: `test-file-0106-atom-0005`
- source hunk: `@@ -0,0 +1,99 @@`
- test/helper: `test_async_context_pending_spc_calls`
- invariant: async context pending SPC calls is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/evm/src/async_context_tests.rs`

## file_index 200: `crates/node/core/src/args/payload_builder.rs`

- new_atom: `test-file-0200-atom-0002`
- source hunk: `@@ -141,14 +152,16 @@ mod tests {`
- test/helper: `test_large_extra_data`
- invariant: large extra DAta preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/node/core/src/args/payload_builder.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0001`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_1_ttl_zero_rejected`
- invariant: commitment constraint 1 TTL zero rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0002`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_1_ttl_one_accepted`
- invariant: commitment constraint 1 TTL one accepted is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0003`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_2_ttl_max_accepted`
- invariant: commitment constraint 2 TTL max accepted is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0004`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_2_ttl_exceeds_max_rejected`
- invariant: commitment constraint 2 TTL exceeds max rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0005`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_3_valid_precompiles`
- invariant: commitment constraint 3 valid precompiles is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0006`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_3_invalid_precompile_rejected`
- invariant: commitment constraint 3 invalid precompile rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0007`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_4_zero_executor_rejected`
- invariant: commitment constraint 4 zero executor rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0008`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `test_c_ac_4_nonzero_executor_accepted`
- invariant: commitment constraint 4 nonzero executor accepted is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0009`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `prop_zero_executor_always_rejected`
- invariant: zero executor always rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0010`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `prop_invalid_ttl_always_rejected`
- invariant: invalid TTL always rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0011`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `prop_valid_commitment_accepted`
- invariant: valid commitment accepted is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0013`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `diff_eq_builder_commitment_passes_verifier`
- invariant: Builder and verifier decisions remain equivalent for diff eq builder commitment passes verifier.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 274: `crates/ritual-async-commitment-validator/src/lib.rs`

- new_atom: `test-file-0274-atom-0014`
- source hunk: `@@ -0,0 +1,576 @@`
- test/helper: `diff_eq_builder_cannot_produce_zero_executor`
- invariant: diff eq builder cannot produce zero executor is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-commitment-validator/src/lib.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0001`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_calculate_calldata_gas_empty`
- invariant: calculate callDAta gas empty is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0002`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_calculate_calldata_gas_zeros`
- invariant: calculate callDAta gas zeros is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0003`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_calculate_calldata_gas_non_zeros`
- invariant: calculate callDAta gas non zeros is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0004`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_calculate_calldata_gas_mixed`
- invariant: calculate callDAta gas mixed preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0005`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_calculate_calldata_gas_overflow_protection`
- invariant: calculate callDAta gas overflow protection is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0006`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_is_system_transaction`
- invariant: is system transaction preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0007`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_effective_gas_limit_for_block_commitment_tx`
- invariant: effective gas limit for block commitment tx preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0008`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_effective_gas_limit_for_block_settlement_tx`
- invariant: effective gas limit for block seTTLement tx preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0009`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_effective_gas_limit_for_block_scheduled_tx`
- invariant: effective gas limit for block scheduled tx preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 278: `crates/ritual-async-fees/src/gas.rs`

- new_atom: `test-file-0278-atom-0010`
- source hunk: `@@ -0,0 +1,198 @@`
- test/helper: `test_effective_gas_limit_for_block_regular_tx`
- invariant: effective gas limit for block regular tx preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/gas.rs`

## file_index 279: `crates/ritual-async-fees/src/http.rs`

- new_atom: `test-file-0279-atom-0001`
- source hunk: `@@ -0,0 +1,44 @@`
- test/helper: `test_http_executor_fee_zero_output`
- invariant: HTTP executor fee zero output is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/http.rs`

## file_index 279: `crates/ritual-async-fees/src/http.rs`

- new_atom: `test-file-0279-atom-0002`
- source hunk: `@@ -0,0 +1,44 @@`
- test/helper: `test_http_executor_fee_with_output`
- invariant: HTTP executor fee with output preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/http.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0001`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_http_fees_calculation`
- invariant: HTTP fees calculation is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0002`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_fees_total_calculation`
- invariant: fees total calculation preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0003`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_llm_fees_fail_without_output`
- invariant: LLM fees fail without output is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0004`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_dkms_explicit_pricing`
- invariant: DKMS explicit pricing is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0005`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_dkms_executor_fee_is_fixed`
- invariant: DKMS executor fee is fixed preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0006`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_unknown_precompile_fails_explicitly`
- invariant: unknown precompile fails explicitly is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0007`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_model_info_image`
- invariant: model info image preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0008`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_model_info_video`
- invariant: model info video preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0009`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_image_steps_multiplier_applies`
- invariant: image steps multiplier applies preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0010`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_video_steps_fps_multiplier_applies`
- invariant: video steps fps multiplier applies preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0011`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_extract_ux_params_legacy_fails`
- invariant: extract ux params legacy fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0012`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_extract_ux_params_too_short_fails`
- invariant: extract ux params too short fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0013`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_extract_ux_params_dynamic_output`
- invariant: extract ux params dynamic output preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0014`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_extract_ux_params_out_of_bounds_fails`
- invariant: extract ux params out of bounds fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0015`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_delivery_has_error_true`
- invariant: delivery has error true preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0016`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_delivery_has_error_false`
- invariant: delivery has error false preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0017`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_delivery_has_error_none`
- invariant: delivery has error none preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0018`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_delivery_has_error_too_short`
- invariant: delivery has error too short is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0019`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_da_error_fees_phase2_constant`
- invariant: DA error fees phase2 constant is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0020`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_da_error_fee_less_than_phase1_escrow`
- invariant: DA error fee less than phase1 escrow preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 280: `crates/ritual-async-fees/src/lib.rs`

- new_atom: `test-file-0280-atom-0021`
- source hunk: `@@ -0,0 +1,1820 @@`
- test/helper: `test_delivery_has_error_realistic_image_error`
- invariant: delivery has error realistic image error preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/lib.rs`

## file_index 281: `crates/ritual-async-fees/src/llm.rs`

- new_atom: `test-file-0281-atom-0001`
- source hunk: `@@ -0,0 +1,941 @@`
- test/helper: `test_llm_has_error_returns_constant_fee`
- invariant: LLM has error returns constant fee preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/llm.rs`

## file_index 281: `crates/ritual-async-fees/src/llm.rs`

- new_atom: `test-file-0281-atom-0002`
- source hunk: `@@ -0,0 +1,941 @@`
- test/helper: `test_llm_has_error_prefix_constant_used_in_decode`
- invariant: LLM has error prefix constant used in decode preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/llm.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0001`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_contract_not_deployed`
- invariant: contract not deployed preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0002`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_invalid_model_config_params_b_zero`
- invariant: invalid model config params b zero is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0003`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_invalid_model_config_theta_zero`
- invariant: invalid model config theta zero is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0004`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_model_exists_valid_config`
- invariant: model exists valid config preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0005`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_model_not_found`
- invariant: model not found is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0006`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_u256_to_f64_scaled`
- invariant: U256 to f64 scaled is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0007`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_u256_to_f64_scaled_overflow`
- invariant: U256 to f64 scaled overflow is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0008`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_compute_string_mapping_slot`
- invariant: compute string mapping slot is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0009`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_read_model_from_db_cached`
- invariant: read model from db cached preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0010`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_image_pricing_partial_config_rejected`
- invariant: image pricing partial config rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0011`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_audio_pricing_partial_config_rejected`
- invariant: audio pricing partial config rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0012`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_video_pricing_partial_config_rejected`
- invariant: video pricing partial config rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0013`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_text_only_model_no_multimodal_pricing_valid`
- invariant: text only model no multimoDAl pricing valid preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 282: `crates/ritual-async-fees/src/registry.rs`

- new_atom: `test-file-0282-atom-0014`
- source hunk: `@@ -0,0 +1,1132 @@`
- test/helper: `test_fully_configured_image_model_valid`
- invariant: fully configured image model valid preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/registry.rs`

## file_index 283: `crates/ritual-async-fees/src/scheduled.rs`

- new_atom: `test-file-0283-atom-0001`
- source hunk: `@@ -0,0 +1,373 @@`
- test/helper: `create_mock_call_executed_log`
- invariant: create mock call executed log preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## file_index 283: `crates/ritual-async-fees/src/scheduled.rs`

- new_atom: `test-file-0283-atom-0002`
- source hunk: `@@ -0,0 +1,373 @@`
- test/helper: `test_extract_callback_gas_success`
- invariant: extract callback gas success preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## file_index 283: `crates/ritual-async-fees/src/scheduled.rs`

- new_atom: `test-file-0283-atom-0003`
- source hunk: `@@ -0,0 +1,373 @@`
- test/helper: `test_extract_callback_gas_wrong_address`
- invariant: extract callback gas wrong address is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## file_index 283: `crates/ritual-async-fees/src/scheduled.rs`

- new_atom: `test-file-0283-atom-0004`
- source hunk: `@@ -0,0 +1,373 @@`
- test/helper: `test_extract_callback_gas_empty_logs`
- invariant: extract callback gas empty logs is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## file_index 283: `crates/ritual-async-fees/src/scheduled.rs`

- new_atom: `test-file-0283-atom-0005`
- source hunk: `@@ -0,0 +1,373 @@`
- test/helper: `test_get_callback_gas_or_fallback_success`
- invariant: get callback gas or fallback success preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## file_index 283: `crates/ritual-async-fees/src/scheduled.rs`

- new_atom: `test-file-0283-atom-0006`
- source hunk: `@@ -0,0 +1,373 @@`
- test/helper: `test_get_callback_gas_or_fallback_failed`
- invariant: get callback gas or fallback failed is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## file_index 283: `crates/ritual-async-fees/src/scheduled.rs`

- new_atom: `test-file-0283-atom-0007`
- source hunk: `@@ -0,0 +1,373 @@`
- test/helper: `test_get_callback_gas_or_fallback_not_found`
- invariant: get callback gas or fallback not found is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/scheduled.rs`

## file_index 284: `crates/ritual-async-fees/src/validators.rs`

- new_atom: `test-file-0284-atom-0001`
- source hunk: `@@ -0,0 +1,106 @@`
- test/helper: `test_async_commitment_fee`
- invariant: async commitment fee preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/validators.rs`

## file_index 284: `crates/ritual-async-fees/src/validators.rs`

- new_atom: `test-file-0284-atom-0002`
- source hunk: `@@ -0,0 +1,106 @@`
- test/helper: `test_async_inclusion_fee_is_zero`
- invariant: async inclusion fee is zero is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/validators.rs`

## file_index 284: `crates/ritual-async-fees/src/validators.rs`

- new_atom: `test-file-0284-atom-0003`
- source hunk: `@@ -0,0 +1,106 @@`
- test/helper: `test_commitment_fee_scales_with_data_size`
- invariant: commitment fee scales with DAta size preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/validators.rs`

## file_index 284: `crates/ritual-async-fees/src/validators.rs`

- new_atom: `test-file-0284-atom-0004`
- source hunk: `@@ -0,0 +1,106 @@`
- test/helper: `test_zero_input_commitment_fee`
- invariant: zero input commitment fee is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/validators.rs`

## file_index 284: `crates/ritual-async-fees/src/validators.rs`

- new_atom: `test-file-0284-atom-0005`
- source hunk: `@@ -0,0 +1,106 @@`
- test/helper: `test_inclusion_fee_always_zero`
- invariant: inclusion fee always zero is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async-fees/src/validators.rs`

## file_index 295: `crates/ritual-async/src/detector.rs`

- new_atom: `test-file-0295-atom-0001`
- source hunk: `@@ -0,0 +1,1546 @@`
- test/helper: `test_extract_precompile_data_valid`
- invariant: extract precompile DAta valid extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/detector.rs`

## file_index 295: `crates/ritual-async/src/detector.rs`

- new_atom: `test-file-0295-atom-0002`
- source hunk: `@@ -0,0 +1,1546 @@`
- test/helper: `test_extract_precompile_data_invalid_data`
- invariant: extract precompile DAta invalid DAta is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/detector.rs`

## file_index 295: `crates/ritual-async/src/detector.rs`

- new_atom: `test-file-0295-atom-0003`
- source hunk: `@@ -0,0 +1,1546 @@`
- test/helper: `test_extract_precompile_data_empty_data`
- invariant: extract precompile DAta empty DAta is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/detector.rs`

## file_index 295: `crates/ritual-async/src/detector.rs`

- new_atom: `test-file-0295-atom-0004`
- source hunk: `@@ -0,0 +1,1546 @@`
- test/helper: `test_extract_precompile_data_ttl_too_large`
- invariant: extract precompile DAta TTL too large is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-async/src/detector.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0001`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `create_http_request_payload`
- invariant: create HTTP request payload is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0002`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `create_llm_request_payload`
- invariant: create LLM request payload is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0003`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_http_payload_valid`
- invariant: valiDAte HTTP payload valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0004`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_http_payload_ttl_zero`
- invariant: valiDAte HTTP payload TTL zero is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0005`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_http_payload_ttl_exceeded`
- invariant: valiDAte HTTP payload TTL exceeded is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0006`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_http_payload_empty_url`
- invariant: valiDAte HTTP payload empty url is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0007`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_http_payload_invalid_scheme`
- invariant: valiDAte HTTP payload invalid scheme is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0008`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_llm_payload_valid`
- invariant: valiDAte LLM payload valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0009`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_llm_payload_empty_model`
- invariant: valiDAte LLM payload empty model is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0010`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_llm_payload_empty_messages`
- invariant: valiDAte LLM payload empty messages is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0011`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_llm_payload_convo_history_roundtrip`
- invariant: valiDAte LLM payload convo history roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0012`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `create_storage_ref_token`
- invariant: create storage ref token preserves deterministic storage slot or bitmap layout behavior.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0013`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `create_persistent_agent_payload`
- invariant: create persistent agent payload is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0014`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_persistent_agent_payload_valid`
- invariant: valiDAte persistent agent payload valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0015`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_persistent_agent_payload_zero_executor`
- invariant: valiDAte persistent agent payload zero executor is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0016`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_persistent_agent_payload_ttl_zero`
- invariant: valiDAte persistent agent payload TTL zero is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0017`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_persistent_agent_payload_ttl_exceeded`
- invariant: valiDAte persistent agent payload TTL exceeded is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0018`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_persistent_agent_payload_empty_model`
- invariant: valiDAte persistent agent payload empty model is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0019`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_persistent_agent_payload_garbage_rejected`
- invariant: valiDAte persistent agent payload garbage rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0020`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_extract_two_phase_deadline_persistent_agent`
- invariant: extract two phase deadline persistent agent extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0021`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_extract_two_phase_deadline_persistent_agent_short_input`
- invariant: extract two phase deadline persistent agent short input extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0022`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_try_decode_persistent_agent_uses_full_codec`
- invariant: try decode persistent agent uses full codec extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0023`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `create_sovereign_agent_payload`
- invariant: create sovereign agent payload is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0024`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_sovereign_agent_payload_valid`
- invariant: valiDAte sovereign agent payload valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0025`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_sovereign_agent_payload_zero_executor`
- invariant: valiDAte sovereign agent payload zero executor is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0026`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_sovereign_agent_payload_ttl_zero`
- invariant: valiDAte sovereign agent payload TTL zero is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0027`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_sovereign_agent_payload_empty_prompt`
- invariant: valiDAte sovereign agent payload empty prompt is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0028`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_sovereign_agent_payload_whitespace_prompt`
- invariant: valiDAte sovereign agent payload whitespace prompt is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0029`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_sovereign_agent_payload_garbage_rejected`
- invariant: valiDAte sovereign agent payload garbage rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0030`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_try_decode_sovereign_agent_uses_full_codec`
- invariant: try decode sovereign agent uses full codec extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0031`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `create_sovereign_agent_payload_custom`
- invariant: create sovereign agent payload custom is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0032`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `make_uncompressed_pubkey`
- invariant: make uncompressed pubkey is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0033`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `make_valid_ecies_blob`
- invariant: make valid ecies blob is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0034`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_encrypted_secrets_too_short`
- invariant: encrypted secrets too short is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0035`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_encrypted_secrets_invalid_prefix`
- invariant: encrypted secrets invalid prefix is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0036`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_invalid_user_public_key_wrong_length`
- invariant: invalid user public key wrong length is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0037`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_invalid_user_public_key_compressed_format`
- invariant: invalid user public key compressed format is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0038`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_unsupported_agent_type`
- invariant: unsupported agent type is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0039`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_unsupported_agent_type_aider`
- invariant: unsupported agent type aider is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0040`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_agent_type_out_of_enum_range_rejected_at_decode`
- invariant: agent type out of enum range rejected at decode is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0041`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_phase2_offset_too_small`
- invariant: phase2 offset too small is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0042`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_phase2_offset_too_small_less_than_ttl`
- invariant: phase2 offset too small less than TTL is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0043`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_phase2_offset_too_large`
- invariant: phase2 offset too large is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0044`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_phase2_offset_at_boundary_valid`
- invariant: phase2 offset at bounDAry valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0045`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_valid_with_ecies_secrets_and_pubkey`
- invariant: valid with ecies secrets and pubkey is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0046`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_two_phase_deadline_valid`
- invariant: valiDAte two phase deadline valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0047`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_two_phase_deadline_insufficient`
- invariant: valiDAte two phase deadline insufficient is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0048`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `test_validate_two_phase_deadline_equal`
- invariant: valiDAte two phase deadline equal is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0049`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `fuzz_validate_two_phase_deadline_property`
- invariant: fuzz valiDAte two phase deadline property is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 297: `crates/ritual-async/src/validation.rs`

- new_atom: `test-file-0297-atom-0050`
- source hunk: `@@ -0,0 +1,1496 @@`
- test/helper: `fuzz_ttl_bounds`
- invariant: fuzz TTL bounds is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-revm-internal:crates/handler/src/validation.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0001`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_is_two_phase_precompile`
- invariant: is two phase precompile preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0002`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_valid_input`
- invariant: extract phase2 deadline valid input extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0003`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_input_too_short`
- invariant: extract phase2 deadline input too short is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0004`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_various_values`
- invariant: extract phase2 deadline various values is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0005`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_sovereign_agent_reads_field_4`
- invariant: extract phase2 deadline sovereign agent reads field 4 extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0006`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_sovereign_agent_input_too_short`
- invariant: extract phase2 deadline sovereign agent input too short is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0007`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_persistent_agent_reads_field_5`
- invariant: extract phase2 deadline persistent agent reads field 5 extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0008`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_fhe_reads_field_10`
- invariant: extract phase2 deadline FHE reads field 10 extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0009`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_fhe_input_too_short`
- invariant: extract phase2 deadline FHE input too short is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0010`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_fhe_various_values`
- invariant: extract phase2 deadline FHE various values is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0011`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_extract_phase2_deadline_non_fhe_still_reads_field_6`
- invariant: extract phase2 deadline non FHE still reads field 6 extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0012`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_phase2_deadline_valid`
- invariant: Builder and verifier decisions remain equivalent for diff eq phase2 deadline valid.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0013`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_phase2_deadline_invalid_equal`
- invariant: Builder and verifier decisions remain equivalent for diff eq phase2 deadline invalid equal.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0014`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_phase2_deadline_invalid_less`
- invariant: Builder and verifier decisions remain equivalent for diff eq phase2 deadline invalid less.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0015`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_phase2_deadline_boundary`
- invariant: Builder and verifier decisions remain equivalent for diff eq phase2 deadline bounDAry.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0016`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_phase2_deadline_equivalence`
- invariant: phase2 deadline equivalence preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0017`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_phase2_deadline_correctness`
- invariant: phase2 deadline correctness preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0019`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_block_verifier_trait_object_safety`
- invariant: block verifier trait object safety preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0020`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `_accepts_trait_object`
- invariant: accepts trait object preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0021`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_sequencing_rights_priority_basics`
- invariant: sequencing rights priority basics preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0022`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_classification_variants`
- invariant: classification variants is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0023`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_sequencing_rights_reader`
- invariant: sequencing rights reader preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0024`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_sequencing_rights_error_variants`
- invariant: sequencing rights error variants preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0025`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_empty_selectors`
- invariant: empty selectors is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0026`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_empty_ordering`
- invariant: empty ordering is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0027`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_ttl_zero_rejected`
- invariant: Builder and verifier decisions remain equivalent for diff eq TTL zero rejected.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0028`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_ttl_one_accepted`
- invariant: Builder and verifier decisions remain equivalent for diff eq TTL one accepted.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0029`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_ttl_max_accepted`
- invariant: Builder and verifier decisions remain equivalent for diff eq TTL max accepted.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0030`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_ttl_exceeds_max_rejected`
- invariant: Builder and verifier decisions remain equivalent for diff eq TTL exceeds max rejected.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0031`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_ttl_large_value_rejected`
- invariant: Builder and verifier decisions remain equivalent for diff eq TTL large value rejected.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0032`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_executor_zero_rejected`
- invariant: Builder and verifier decisions remain equivalent for diff eq executor zero rejected.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0033`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_executor_nonzero_accepted`
- invariant: Builder and verifier decisions remain equivalent for diff eq executor nonzero accepted.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0034`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_executor_one_byte_accepted`
- invariant: Builder and verifier decisions remain equivalent for diff eq executor one byte accepted.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0035`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_ttl_equivalence`
- invariant: TTL equivalence preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0036`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_executor_equivalence`
- invariant: executor equivalence preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0037`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_valid_commitment_passes_both`
- invariant: Builder and verifier decisions remain equivalent for valid commitment passes both.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0038`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_settlement_expiry_equal`
- invariant: Builder and verifier decisions remain equivalent for diff eq seTTLement expiry equal.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0039`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_settlement_expiry_before`
- invariant: Builder and verifier decisions remain equivalent for diff eq seTTLement expiry before.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0040`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_settlement_expiry_after`
- invariant: Builder and verifier decisions remain equivalent for diff eq seTTLement expiry after.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0041`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_settlement_expiry_boundary_plus_one`
- invariant: Builder and verifier decisions remain equivalent for diff eq seTTLement expiry bounDAry plus one.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0043`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_settlement_expiry_correctness`
- invariant: seTTLement expiry correctness preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0044`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_sender_first_async_allowed`
- invariant: diff eq sender first async allowed preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0045`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_sender_duplicate_async_rejected`
- invariant: diff eq sender duplicate async rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0046`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_sender_dedup_deterministic`
- invariant: sender dedup deterministic preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0047`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_sr_empty_input_no_sr`
- invariant: diff eq sr empty input no sr is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0048`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_sr_contract_creation_no_sr`
- invariant: diff eq sr contract creation no sr preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0049`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_sr_ascending_order_passes`
- invariant: diff eq sr ascending order passes is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0050`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_sr_descending_order_fails`
- invariant: diff eq sr descending order fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0051`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_sr_same_priority_passes`
- invariant: diff eq sr same priority passes preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0052`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_sr_ordering_deterministic`
- invariant: sr ordering deterministic preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0053`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_sr_monotonic_passes`
- invariant: sr monotonic passes is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0054`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_spc_valid_proof_length`
- invariant: diff eq SPC valid proof length is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0055`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_spc_short_proof_rejected`
- invariant: diff eq SPC short proof rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0056`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_spc_multiple_calls_rejected`
- invariant: diff eq SPC multiple calls rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0057`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_spc_proof_length_equivalence`
- invariant: SPC proof length equivalence preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0058`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_fee_http_helpers_deterministic`
- invariant: diff eq fee HTTP helpers deterministic preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0059`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_fee_agent_phase2_deterministic`
- invariant: diff eq fee agent phase2 deterministic preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0060`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_fee_phase2_http_deterministic`
- invariant: diff eq fee phase2 HTTP deterministic preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0061`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_fee_agent_phase2_deterministic`
- invariant: fee agent phase2 deterministic preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0062`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_fee_phase2_http_deterministic`
- invariant: fee phase2 HTTP deterministic preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0063`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_nonce_lock_no_pending`
- invariant: diff eq nonce lock no pending preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0064`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_nonce_lock_has_pending`
- invariant: diff eq nonce lock has pending is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0065`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_nonce_lock_deterministic`
- invariant: diff eq nonce lock deterministic preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0066`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_nonce_lock_deterministic`
- invariant: Builder and verifier decisions remain equivalent for nonce lock deterministic.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0067`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c4_too_early`
- invariant: diff eq scheduled C4 too early is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0068`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c4_at_expected`
- invariant: diff eq scheduled C4 at expected preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0069`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c5_too_late`
- invariant: diff eq scheduled C5 too late is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0070`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c5_at_deadline`
- invariant: diff eq scheduled C5 at deadline preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0071`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c6_expired`
- invariant: diff eq scheduled C6 expired is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0072`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c3_out_of_bounds`
- invariant: diff eq scheduled C3 out of bounds is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0073`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c3_valid_index`
- invariant: diff eq scheduled C3 valid index is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0074`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c10_duplicate`
- invariant: diff eq scheduled C10 duplicate is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0075`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_scheduled_c4_equivalence`
- invariant: Builder and verifier decisions remain equivalent for scheduled C4 equivalence.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0076`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_scheduled_c5_equivalence`
- invariant: Builder and verifier decisions remain equivalent for scheduled C5 equivalence.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0077`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_scheduled_c6_equivalence`
- invariant: Builder and verifier decisions remain equivalent for scheduled C6 equivalence.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0078`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_scheduled_c3_equivalence`
- invariant: Builder and verifier decisions remain equivalent for scheduled C3 equivalence.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0079`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_scheduled_c10_deterministic`
- invariant: scheduled C10 deterministic preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0080`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c11_predicate_true`
- invariant: diff eq scheduled C11 predicate true preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0081`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c11_predicate_false_is_byzantine`
- invariant: diff eq scheduled C11 predicate false is byzantine preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0082`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c11_default_predicate`
- invariant: diff eq scheduled C11 default predicate preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0083`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c11_predicate_revert_is_byzantine`
- invariant: diff eq scheduled C11 predicate revert is byzantine preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0084`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_scheduled_c11_predicate_halt_is_byzantine`
- invariant: diff eq scheduled C11 predicate halt is byzantine preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0085`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_scheduled_c11_equivalence`
- invariant: Builder and verifier decisions remain equivalent for scheduled C11 equivalence.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0086`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_scheduled_c11_default_always_true`
- invariant: scheduled C11 default always true is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0087`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_metrics_delivery_result_len_valid`
- invariant: diff eq metrics delivery result len valid is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0088`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_metrics_delivery_result_len_short`
- invariant: diff eq metrics delivery result len short preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0089`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_metrics_agent_short_input`
- invariant: diff eq metrics agent short input preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0090`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `diff_eq_metrics_extraction_deterministic`
- invariant: diff eq metrics extraction deterministic extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0091`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_metrics_delivery_deterministic`
- invariant: metrics delivery deterministic preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0092`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `prop_metrics_agent_deterministic`
- invariant: metrics agent deterministic preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0093`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_onnx_unavailable_is_validation_error`
- invariant: onnx unavailable is valiDAtion error is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0094`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_validation_errors_are_classified_as_validation`
- invariant: valiDAtion errors are classified as valiDAtion is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 304: `crates/ritual-block-verification/src/verifier.rs`

- new_atom: `test-file-0304-atom-0095`
- source hunk: `@@ -0,0 +1,5303 @@`
- test/helper: `test_error_class_system_vs_block_local`
- invariant: error class system vs block local is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 320: `crates/ritual-precompile-codecs/src/executor.rs`

- new_atom: `test-file-0320-atom-0001`
- source hunk: `@@ -0,0 +1,260 @@`
- test/helper: `create_test_executor_request`
- invariant: create test executor request extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/executor.rs`

## file_index 320: `crates/ritual-precompile-codecs/src/executor.rs`

- new_atom: `test-file-0320-atom-0002`
- source hunk: `@@ -0,0 +1,260 @@`
- test/helper: `test_decode_base_fields_success`
- invariant: decode base fields success extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/executor.rs`

## file_index 320: `crates/ritual-precompile-codecs/src/executor.rs`

- new_atom: `test-file-0320-atom-0003`
- source hunk: `@@ -0,0 +1,260 @@`
- test/helper: `test_decode_base_fields_too_short`
- invariant: decode base fields too short is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/executor.rs`

## file_index 320: `crates/ritual-precompile-codecs/src/executor.rs`

- new_atom: `test-file-0320-atom-0004`
- source hunk: `@@ -0,0 +1,260 @@`
- test/helper: `test_from_base_fields`
- invariant: from base fields extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/executor.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0001`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `create_test_http_call_request`
- invariant: create test HTTP call request extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0002`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_extract_ttl_success`
- invariant: extract TTL success extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0003`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_extract_ttl_different_values`
- invariant: extract TTL different values extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0004`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_extract_executor_success`
- invariant: extract executor success extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0005`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_extract_executor_and_ttl`
- invariant: extract executor and TTL extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0006`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_from_abi_success`
- invariant: from abi success extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0007`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_extract_ttl_invalid_data`
- invariant: extract TTL invalid DAta is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0008`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_http_method_conversion`
- invariant: HTTP method conversion extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0009`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_header_length_mismatch`
- invariant: header length mismatch extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 321: `crates/ritual-precompile-codecs/src/http_call.rs`

- new_atom: `test-file-0321-atom-0010`
- source hunk: `@@ -0,0 +1,548 @@`
- test/helper: `test_decode_real_http_request_from_cast_run`
- invariant: decode real HTTP request from cast run extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/http_call.rs`

## file_index 323: `crates/ritual-precompile-codecs/src/llm_call.rs`

- new_atom: `test-file-0323-atom-0001`
- source hunk: `@@ -0,0 +1,361 @@`
- test/helper: `create_llm_request_payload`
- invariant: create LLM request payload extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`

## file_index 323: `crates/ritual-precompile-codecs/src/llm_call.rs`

- new_atom: `test-file-0323-atom-0002`
- source hunk: `@@ -0,0 +1,361 @@`
- test/helper: `test_valid_llm_request`
- invariant: valid LLM request extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`

## file_index 323: `crates/ritual-precompile-codecs/src/llm_call.rs`

- new_atom: `test-file-0323-atom-0003`
- source hunk: `@@ -0,0 +1,361 @@`
- test/helper: `test_empty_model`
- invariant: empty model is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`

## file_index 323: `crates/ritual-precompile-codecs/src/llm_call.rs`

- new_atom: `test-file-0323-atom-0004`
- source hunk: `@@ -0,0 +1,361 @@`
- test/helper: `test_empty_messages`
- invariant: empty messages is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`

## file_index 323: `crates/ritual-precompile-codecs/src/llm_call.rs`

- new_atom: `test-file-0323-atom-0005`
- source hunk: `@@ -0,0 +1,361 @@`
- test/helper: `test_malformed_abi`
- invariant: malformed abi extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`

## file_index 323: `crates/ritual-precompile-codecs/src/llm_call.rs`

- new_atom: `test-file-0323-atom-0006`
- source hunk: `@@ -0,0 +1,361 @@`
- test/helper: `test_convo_history_roundtrip`
- invariant: convo history roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/llm_call.rs`

## file_index 324: `crates/ritual-precompile-codecs/src/long_running.rs`

- new_atom: `test-file-0324-atom-0001`
- source hunk: `@@ -0,0 +1,1172 @@`
- test/helper: `test_decode_delivery_config`
- invariant: decode delivery config preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/long_running.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0001`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `create_storage_ref_token`
- invariant: create storage ref token is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0002`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `create_minimal_request_payload`
- invariant: create minimal request payload is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0003`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_roundtrip_request`
- invariant: roundtrip request round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0004`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_roundtrip_request_with_rpc_urls`
- invariant: roundtrip request with RPC urls round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0005`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_extract_ttl`
- invariant: extract TTL extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0007`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_get_required_secret_keys`
- invariant: get required secret keys extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0008`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_delivery_config_extraction`
- invariant: delivery config extraction preserves the expected fee, gas, reward, or escrow calculation.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0009`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_response_roundtrip`
- invariant: response roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0010`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_response_error`
- invariant: response error is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 325: `crates/ritual-precompile-codecs/src/persistent_agent.rs`

- new_atom: `test-file-0325-atom-0011`
- source hunk: `@@ -0,0 +1,968 @@`
- test/helper: `test_llm_provider_api_string`
- invariant: LLM provider api string extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/persistent_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0001`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `create_storage_ref_token`
- invariant: create storage ref token preserves deterministic storage slot or bitmap layout behavior.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0002`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `create_sovereign_agent_request_payload`
- invariant: create sovereign agent request payload extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0003`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `create_sovereign_agent_request_payload_with_type`
- invariant: create sovereign agent request payload with type extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0004`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_valid_sovereign_agent_request`
- invariant: valid sovereign agent request extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0005`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_valid_sovereign_agent_request_with_rpc_urls`
- invariant: valid sovereign agent request with RPC urls extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0006`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_22_field_payload_rejected`
- invariant: 22 field payload rejected is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0007`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_sovereign_agent_type_crush_roundtrip`
- invariant: sovereign agent type crush roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0008`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_sovereign_agent_type_zeroclaw_roundtrip`
- invariant: sovereign agent type zeroclaw roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0009`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_sovereign_agent_type_invalid_boundary`
- invariant: sovereign agent type invalid bounDAry is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0010`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_empty_prompt`
- invariant: empty prompt is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 326: `crates/ritual-precompile-codecs/src/sovereign_agent.rs`

- new_atom: `test-file-0326-atom-0011`
- source hunk: `@@ -0,0 +1,543 @@`
- test/helper: `test_malformed_abi`
- invariant: malformed abi extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-precompile-codecs/src/sovereign_agent.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0001`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_filtering_stats_from_results`
- invariant: filtering stats from results is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0002`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_filtering_stats_all_valid`
- invariant: filtering stats all valid preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0003`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_filtering_stats_empty`
- invariant: filtering stats empty is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0004`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_derive_max_block_number_regular_values`
- invariant: derive max block number regular values preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0005`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_derive_max_block_number_saturates_on_overflow`
- invariant: derive max block number saturates on overflow is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0006`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_compute_obligations_from_pool_skips_calls_above_protocol_ttl_bound`
- invariant: compute obligations from pool skips calls above protocol TTL bound is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0007`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_compute_obligations_from_pool_includes_underfunded_call_for_contract_eviction`
- invariant: compute obligations from pool includes underfunded call for contract eviction preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0008`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_compute_obligations_from_pool_skips_when_base_fee_exceeds_max_fee`
- invariant: compute obligations from pool skips when base fee exceeds max fee is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0009`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `test_compute_obligations_from_pool_includes_when_wallet_funded`
- invariant: compute obligations from pool includes when wallet funded preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0012`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `active_job_dispatch_proceeds_on_storage_error`
- invariant: active job dispatch proceeds on storage error preserves deterministic storage slot or bitmap layout behavior.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 329: `crates/ritual-scheduled-block-building/src/lib.rs`

- new_atom: `test-file-0329-atom-0013`
- source hunk: `@@ -0,0 +1,911 @@`
- test/helper: `active_job_dispatch_passes_through_arguments`
- invariant: active job dispatch passes through arguments preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-scheduled-block-building/src/lib.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0001`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `make_selector`
- invariant: make selector is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0003`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_bucket_sort`
- invariant: bucket sort is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0004`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_partition_reassemble`
- invariant: partition reassemble is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0005`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_empty_bucket_passes_verification`
- invariant: empty bucket passes verification is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0006`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_single_tx_bucket_passes`
- invariant: single tx bucket passes preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0007`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_ascending_order_passes`
- invariant: ascending order passes preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0008`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_same_priority_passes`
- invariant: same priority passes preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0009`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_descending_order_fails`
- invariant: descending order fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0010`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_mixed_order_fails`
- invariant: mixed order fails is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0011`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_partition_new`
- invariant: partition new is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0012`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_partition_default`
- invariant: partition default is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0013`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_bucket_manager_new`
- invariant: bucket manager new preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0014`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_large_bucket_construction`
- invariant: large bucket construction preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0015`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_bucket_sort_reorders`
- invariant: bucket sort reorders preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0016`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `test_ordering_violation_error_details`
- invariant: ordering violation error details preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 336: `crates/ritual-sequencing-rights/src/bucket.rs`

- new_atom: `test-file-0336-atom-0017`
- source hunk: `@@ -0,0 +1,604 @@`
- test/helper: `create_dummy_recovered_tx`
- invariant: create dummy recovered tx preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/bucket.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0001`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_inspector_single_contract`
- invariant: inspector single contract preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0002`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_inspector_multi_contract`
- invariant: inspector multi contract preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0003`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_inspector_into_classification`
- invariant: inspector into classification preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0004`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_selectors_for_contract`
- invariant: selectors for contract is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0005`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_inspector_reset`
- invariant: inspector reset is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0006`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_exactly_4_byte_selector`
- invariant: exactly 4 byte selector preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0007`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_input_boundary_cases`
- invariant: input bounDAry cases preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0008`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_multiple_selectors_same_contract`
- invariant: multiple selectors same contract preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0009`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_duplicate_selector_calls`
- invariant: duplicate selector calls is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0010`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_many_contracts_multi_contract_classification`
- invariant: many contracts multi contract classification preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0011`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_get_contracts`
- invariant: get contracts preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0012`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_call_depth_tracking`
- invariant: call depth tracking preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0013`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_empty_inspector_get_contracts`
- invariant: empty inspector get contracts is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0014`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `test_classification_enum_coverage`
- invariant: classification enum coverage is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0015`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `arb_address`
- invariant: arb address preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0016`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `arb_selector`
- invariant: arb selector preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0017`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `prop_classify_deterministic`
- invariant: classify deterministic preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0018`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `prop_into_classification_deterministic`
- invariant: into classification deterministic preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0019`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `prop_empty_is_simple_transfer`
- invariant: empty is simple transfer is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0020`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `prop_single_contract_classification`
- invariant: single contract classification preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0021`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `prop_multi_contract_classification`
- invariant: multi contract classification preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0022`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `prop_reset_clears_state`
- invariant: reset clears state is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 337: `crates/ritual-sequencing-rights/src/classifier.rs`

- new_atom: `test-file-0337-atom-0023`
- source hunk: `@@ -0,0 +1,763 @@`
- test/helper: `prop_selectors_for_contract`
- invariant: selectors for contract preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/classifier.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0001`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `make_selector`
- invariant: make selector preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0003`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_exact_match`
- invariant: exact match preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0004`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_no_match`
- invariant: no match preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0005`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_empty_ordering`
- invariant: empty ordering is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0006`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_subset_match`
- invariant: subset match preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0007`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_max_priority_no_overflow`
- invariant: max priority no overflow is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0008`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_empty_selector_set`
- invariant: empty selector set is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0009`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_empty_selector_set_empty_ordering`
- invariant: empty selector set empty ordering is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0010`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_overlapping_levels`
- invariant: overlapping levels preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0011`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_superset_uses_lowest_priority`
- invariant: superset uses lowest priority preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0012`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_partial_overlap`
- invariant: partial overlap preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0013`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_many_levels`
- invariant: many levels preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0015`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_selector_in_multiple_level_sets`
- invariant: selector in multiple level sets preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 340: `crates/ritual-sequencing-rights/src/priority.rs`

- new_atom: `test-file-0340-atom-0016`
- source hunk: `@@ -0,0 +1,287 @@`
- test/helper: `test_completely_disjoint`
- invariant: completely disjoint preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/net/p2p/src/priority.rs`

## file_index 341: `crates/ritual-sequencing-rights/src/reader.rs`

- new_atom: `test-file-0341-atom-0001`
- source hunk: `@@ -0,0 +1,358 @@`
- test/helper: `test_decode_empty_ordering`
- invariant: decode empty ordering is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-tee-registry-reader/src/reader.rs`

## file_index 341: `crates/ritual-sequencing-rights/src/reader.rs`

- new_atom: `test-file-0341-atom-0002`
- source hunk: `@@ -0,0 +1,358 @@`
- test/helper: `test_selector_constant`
- invariant: selector constant preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-tee-registry-reader/src/reader.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0002`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `test_selector_set_equality`
- invariant: selector set equality preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0003`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `test_sequencing_ordering_priority`
- invariant: sequencing ordering priority preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0004`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `arb_selector`
- invariant: arb selector preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0005`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `arb_selector_set`
- invariant: arb selector set preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0006`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `arb_ordering`
- invariant: arb ordering preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0007`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_priority_total_ordering`
- invariant: priority total ordering preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0008`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_priority_consistent_with_value`
- invariant: priority consistent with value preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0009`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_lowest_is_lowest`
- invariant: lowest is lowest preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0010`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_priority_value_roundtrip`
- invariant: priority value roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0011`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_selector_set_deterministic`
- invariant: selector set deterministic preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0012`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_get_priority_deterministic`
- invariant: get priority deterministic preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0013`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_get_priority_correctness`
- invariant: get priority correctness preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0014`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_empty_ordering_returns_none`
- invariant: empty ordering returns none is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0015`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `prop_is_empty_consistent`
- invariant: is empty consistent is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0016`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `test_priority_lowest_value`
- invariant: priority lowest value preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0017`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `test_priority_equality`
- invariant: priority equality preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0018`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `test_contract_interaction_new`
- invariant: contract interaction new preserves sequencing-rights classification, priority, or ordering semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0019`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `test_sequencing_ordering_is_empty`
- invariant: sequencing ordering is empty is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 342: `crates/ritual-sequencing-rights/src/types.rs`

- new_atom: `test-file-0342-atom-0020`
- source hunk: `@@ -0,0 +1,293 @@`
- test/helper: `test_sequencing_ordering_default`
- invariant: sequencing ordering default is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/ritual-sequencing-rights/src/types.rs`

## file_index 348: `crates/ritual-spc-verification/src/client.rs`

- new_atom: `test-file-0348-atom-0001`
- source hunk: `@@ -0,0 +1,180 @@`
- test/helper: `create_test_request`
- invariant: create test request preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/sidecar-client/src/client.rs`

## file_index 348: `crates/ritual-spc-verification/src/client.rs`

- new_atom: `test-file-0348-atom-0002`
- source hunk: `@@ -0,0 +1,180 @@`
- test/helper: `test_client_creation`
- invariant: client creation preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/sidecar-client/src/client.rs`

## file_index 348: `crates/ritual-spc-verification/src/client.rs`

- new_atom: `test-file-0348-atom-0003`
- source hunk: `@@ -0,0 +1,180 @@`
- test/helper: `test_verification_url_construction`
- invariant: verification url construction preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/sidecar-client/src/client.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0002`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_verifier`
- invariant: verifier preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0003`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_verifier_fast`
- invariant: verifier fast preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0004`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `create_test_request`
- invariant: create test request preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0005`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_verifier_creation`
- invariant: verifier creation preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0006`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_batch_verification_empty`
- invariant: batch verification empty is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0007`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_batch_verification_single`
- invariant: batch verification single is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0008`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_batch_verification_multiple`
- invariant: batch verification multiple is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0009`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_verify_parallel`
- invariant: verify parallel is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 352: `crates/ritual-spc-verification/src/verifier.rs`

- new_atom: `test-file-0352-atom-0010`
- source hunk: `@@ -0,0 +1,820 @@`
- test/helper: `test_batch_verification_request_creation`
- invariant: batch verification request creation preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-nodebuilder-internal:crates/ritual-nsm/src/verifier.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0001`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `create_http_request_payload`
- invariant: create HTTP request payload is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0002`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `test_valid_http_request`
- invariant: valid HTTP request is accepted on the expected valid path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0004`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `test_ttl_exceeded`
- invariant: TTL exceeded is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0005`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `test_zero_executor`
- invariant: zero executor is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0006`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `test_empty_url`
- invariant: empty url is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0007`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `test_invalid_url_scheme`
- invariant: invalid url scheme is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0008`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `test_malformed_abi`
- invariant: malformed abi is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 396: `crates/rpc/rpc/src/async_tx_validator.rs`

- new_atom: `test-file-0396-atom-0009`
- source hunk: `@@ -0,0 +1,550 @@`
- test/helper: `test_input_too_large`
- invariant: input too large is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/rpc/rpc/src/async_tx_validator.rs`

## file_index 421: `crates/scheduling/src/singleton.rs`

- new_atom: `test-file-0421-atom-0001`
- source hunk: `@@ -0,0 +1,519 @@`
- test/helper: `test_hydrate_from_storage_rebuilds_scheduler_state`
- invariant: hydrate from storage rebuilds scheduler state preserves deterministic storage slot or bitmap layout behavior.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/singleton.rs`

## file_index 422: `crates/scheduling/src/transaction.rs`

- new_atom: `test-file-0422-atom-0002`
- source hunk: `@@ -0,0 +1,212 @@`
- test/helper: `test_create_scheduled_transaction_rejects_max_fee_per_gas_overflow`
- invariant: create scheduled transaction rejects max fee per gas overflow is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-alloy-evm-internal:crates/evm/src/rpc/transaction.rs`

## file_index 422: `crates/scheduling/src/transaction.rs`

- new_atom: `test-file-0422-atom-0003`
- source hunk: `@@ -0,0 +1,212 @@`
- test/helper: `test_create_scheduled_transaction_rejects_max_priority_fee_overflow`
- invariant: create scheduled transaction rejects max priority fee overflow is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-alloy-evm-internal:crates/evm/src/rpc/transaction.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0001`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `create_test_call`
- invariant: create test call preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0002`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_fire_at_exact_target_blocks_frequency_5`
- invariant: fire at exact target blocks frequency 5 preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0003`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_fire_not_at_intermediate_blocks`
- invariant: fire not at intermediate blocks preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0004`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_fire_before_start_block`
- invariant: fire before start block preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0005`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_fire_frequency_1`
- invariant: fire frequency 1 preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0006`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_fire_num_calls_1`
- invariant: fire num calls 1 preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0007`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_fire_large_frequency`
- invariant: fire large frequency preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0008`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_fire_edge_case_examples_from_plan`
- invariant: fire edge case examples from plan preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0009`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_replace_calls_replaces_non_empty_state`
- invariant: replace calls replaces non empty state is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0010`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_startup_hydration_gate_runs_once`
- invariant: startup hydration gate runs once preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 423: `crates/scheduling/src/types.rs`

- new_atom: `test-file-0423-atom-0011`
- source hunk: `@@ -0,0 +1,624 @@`
- test/helper: `test_startup_hydration_abort_resets_gate`
- invariant: startup hydration abort resets gate preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/scheduling/src/types.rs`

## file_index 427: `crates/stages/api/src/pipeline/mod.rs`

- new_atom: `test-file-0427-atom-0001`
- source hunk: `@@ -1079,6 +1213,102 @@ mod tests {`
- test/helper: `run_pipeline_retries_onnx_unavailable_without_unwind`
- invariant: run pipeline retries onnx unavailable without unwind preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/stages/api/src/pipeline/mod.rs`

## file_index 427: `crates/stages/api/src/pipeline/mod.rs`

- new_atom: `test-file-0427-atom-0002`
- source hunk: `@@ -1079,6 +1213,102 @@ mod tests {`
- test/helper: `run_pipeline_limits_onnx_retries_then_unwinds`
- invariant: run pipeline limits onnx retries then unwinds preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/stages/api/src/pipeline/mod.rs`

## file_index 468: `crates/storage/codecs/src/alloy/transaction/spc_call.rs`

- new_atom: `test-file-0468-atom-0001`
- source hunk: `@@ -0,0 +1,349 @@`
- test/helper: `test_spc_call_compact_roundtrip`
- invariant: SPC call compact roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/spc_call.rs`

## file_index 468: `crates/storage/codecs/src/alloy/transaction/spc_call.rs`

- new_atom: `test-file-0468-atom-0002`
- source hunk: `@@ -0,0 +1,349 @@`
- test/helper: `test_spc_call_compact_empty_bytes`
- invariant: SPC call compact empty bytes round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/spc_call.rs`

## file_index 468: `crates/storage/codecs/src/alloy/transaction/spc_call.rs`

- new_atom: `test-file-0468-atom-0003`
- source hunk: `@@ -0,0 +1,349 @@`
- test/helper: `test_spc_call_compact_large_bytes`
- invariant: SPC call compact large bytes round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/spc_call.rs`

## file_index 468: `crates/storage/codecs/src/alloy/transaction/spc_call.rs`

- new_atom: `test-file-0468-atom-0004`
- source hunk: `@@ -0,0 +1,349 @@`
- test/helper: `test_spc_call_wrapper_roundtrip`
- invariant: SPC call wrapper roundtrip round-trips through the relevant encoding/decoding path without changing semantic fields.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/storage/codecs/src/alloy/transaction/spc_call.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0001`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `create_test_async_transaction`
- invariant: create test async transaction is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0002`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `create_test_normal_transaction`
- invariant: create test normal transaction is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0003`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_async_transaction_added_to_global_mapping`
- invariant: async transaction added to global mapping is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0004`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_async_transaction_removal_during_block_finalization`
- invariant: async transaction removal during block finalization is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0005`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_normal_transaction_unaffected`
- invariant: normal transaction unaffected preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0006`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_concurrent_async_transaction_operations`
- invariant: concurrent async transaction operations preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0007`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_extract_original_tx_hash_error_handling`
- invariant: extract original tx hash error handling extracts or encodes the expected fields and boundary values.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0008`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_expiry_check_not_expired`
- invariant: expiry check not expired is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0009`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_expiry_boundary_conditions`
- invariant: expiry bounDAry conditions is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0010`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_zero_ttl_expiry`
- invariant: zero TTL expiry is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0011`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_expiry_formula_documentation`
- invariant: expiry formula documentation preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0012`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_phase2_ttl_uses_max_poll_block`
- invariant: phase2 TTL uses max poll block is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0013`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_phase2_ttl_extends_beyond_original`
- invariant: phase2 TTL extends beyond original preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0014`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_mark_awaiting_delivery_updates_expiry`
- invariant: mark awaiting delivery upDAtes expiry preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0015`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_expiry_always_set_at_add_time`
- invariant: expiry always set at add time preserves scheduled-transaction scheduling, obligation, or predicate semantics.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0016`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_none_expiry_is_invariant_violation`
- invariant: none expiry is invariant violation is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 529: `crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

- new_atom: `test-file-0529-atom-0017`
- source hunk: `@@ -0,0 +1,453 @@`
- test/helper: `test_ttl_overflow_protection`
- invariant: TTL overflow protection is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/async_pool_removal_tests.rs`

## file_index 537: `crates/transaction-pool/src/pool/txpool.rs`

- new_atom: `test-file-0537-atom-0001`
- source hunk: `@@ -2326,6 +2719,22 @@ mod tests {`
- test/helper: `test_add_async_commitment_transaction`
- invariant: add async commitment transaction is rejected or classified on the expected negative path.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/src/pool/txpool.rs`

## file_index 545: `crates/transaction-pool/tests/it/async_exec.rs`

- new_atom: `test-file-0545-atom-0001`
- source hunk: `@@ -0,0 +1,57 @@`
- test/helper: `test_async_commitment_inclusion`
- invariant: async commitment inclusion preserves the behavior asserted by the downstream test or fixture.
- required change or question: Add a canonical per-file atom for this test-derived invariant and verify whether the v2.2 port preserves it; current supplemental mapping is `missing`.
- likely destination: `/home/ritual/repos/ritual-reth-internal-v2.2.0-port:crates/transaction-pool/tests/it/async_exec.rs`

