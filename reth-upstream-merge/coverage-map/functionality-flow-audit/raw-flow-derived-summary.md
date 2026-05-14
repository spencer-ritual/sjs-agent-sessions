# Raw Functionality-Flow Atom Pass

- Source: `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/functionality-flow-traces.md`
- Raw candidates: 234

## By Flow Title

- `Persistent Agent `0x0820``: 16
- `Short-Running Async SPC Trace`: 12
- `Long-Running Two-Phase Trace`: 12
- `Scheduled Execution Trace`: 12
- `Secret, Private Output, And dKMS Trace`: 12
- `Sovereign Agent `0x080C``: 10
- `Sync Precompile Trace`: 8
- `1. Wire, Storage, And Receipt Compatibility`: 7
- ``llm_call``: 6
- ``llm_call_streaming``: 6
- ``scheduled_onnx_inference``: 6
- `3. Builder Obligation Compatibility`: 6
- ``http_call``: 5
- ``x402_dkms_http_call``: 5
- ``x402_dkms_long_running_http``: 5
- ``x402_dkms_scheduled``: 5
- ``delegate_secret``: 5
- ``zk_two_phase``: 5
- ``scheduled_zk_two_phase``: 5
- ``sequencing_rights_simple``: 5
- `Factory-Backed Agent Deployment`: 5
- `Multimodal Image/Audio/Video `0x0818`/`0x0819`/`0x081A``: 5
- `Passkey / P-256`: 5
- `dKMS Mode`: 5
- `2. Admission And Validation Compatibility`: 5
- `6. Product Economics Compatibility`: 5
- ``token_transfer``: 4
- ``onnx_inference``: 4
- ``jq_query``: 4
- ``private_io``: 4
- `FHE `0x0807``: 4
- `Summit And Chain-Driver Consensus`: 4
- ``swap``: 3
- ``ed25519_verify``: 3
- `4. Verifier Fail-Closed Compatibility`: 3
- `5. Executor And Operator Surface Compatibility`: 3
- `7. Agent Lifecycle Compatibility`: 3
- ``long_running_echo``: 2
- `Mock Proxy Mode`: 2
- `Shared GLM Proxy Mode`: 2
- `GCS DA`: 2
- `8. Deployment Reproducibility Compatibility`: 2
- `Agent Orchestrator Sidecar`: 1
- `Reth Env Gates`: 1

## By Source Path

- `crates/ritual-scheduled-verification/src/lib.rs`: 31
- `crates/ritual-precompile-codecs/src/long_running.rs`: 26
- `crates/ritual-precompile-addresses/src/lib.rs`: 23
- `crates/ritual-async/src/validation.rs`: 20
- `crates/ritual-precompile-codecs/src/persistent_agent.rs`: 20
- `crates/ritual-precompile-codecs/src/llm_call.rs`: 20
- `crates/ritual-spc-signature/src/lib.rs`: 17
- `crates/ritual-async-fees/src/lib.rs`: 14
- `crates/ethereum/payload/src/lib.rs`: 11
- `crates/ritual-precompile-codecs/src/sovereign_agent.rs`: 11
- `crates/storage/codecs/src/alloy/transaction/spc_call.rs`: 10
- `crates/ritual-block-verification/src/verifier.rs`: 6
- `crates/storage/codecs/src/alloy/passkey_signature.rs`: 6
- `crates/chainspec/src/spec.rs`: 4
- `crates/ritual-async-fees/src/gas.rs`: 3
- `crates/transaction-pool/src/pool/txpool.rs`: 3
- `crates/ritual-precompile-codecs/src/http_call.rs`: 2
- `crates/transaction-pool/src/pool/async_pool.rs`: 2
- `crates/ritual-tee-registry-reader/src/reader.rs`: 2
- `crates/ritual-sequencing-rights/src/types.rs`: 1
- `crates/rpc/rpc/src/async_tx_validator.rs`: 1
- `crates/ritual-async-registry/src/lib.rs`: 1
