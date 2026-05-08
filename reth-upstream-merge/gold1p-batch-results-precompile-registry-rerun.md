# Gold1p Traffic Rerun

Source workload JSON: `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/gold1p-batch-results.json`

## Summary

- Result: `15/15` workloads passed; `0` failed.
- Total runtime: `258.6s`.

## Workloads

| Row | Workload | Status | Runtime | Attempts | Command | Note |
| --- | --- | --- | ---: | ---: | --- | --- |
| 1 | `llm_call` | `PASS` | `8.8s` | `1` | `make run-llm-call ARGS='--agent-count 1 --start-agent-index 2210 --model mock-model'` | Action completed: 1/1 successful. |
| 2 | `llm_call_pii` | `PASS` | `6.4s` | `1` | `make run-llm-call-pii ARGS='--agent-count 1 --start-agent-index 2220 --model mock-model'` | Action completed: 1/1 successful. |
| 4 | `http_call` | `PASS` | `5.3s` | `1` | `make run-http-call ARGS='--agent-count 1 --start-agent-index 2230 --timeout 60'` | Action completed: 1/1 successful. |
| 5 | `http_call_pii` | `PASS` | `10.3s` | `1` | `make run-http-call-pii ARGS='--agent-count 1 --start-agent-index 2240'` | Action completed: 1/1 successful. |
| 6 | `onnx_inference` | `PASS` | `3.9s` | `1` | `make run-onnx ARGS='--agent-count 1 --start-agent-index 2250'` | Action completed: 1/1 successful. |
| 8 | `jq_query` | `PASS` | `3.7s` | `1` | `make run-jq ARGS='--agent-count 1 --start-agent-index 2260'` | Action completed: 1/1 successful. |
| 9 | `ed25519_verify` | `PASS` | `4.6s` | `1` | `make run-ed25519 ARGS='--agent-count 1 --start-agent-index 2270'` | Action completed: 1/1 successful. |
| 15 | `private_io` | `PASS` | `3.9s` | `1` | `make run-private-io ARGS='--agent-count 1 --start-agent-index 2280'` | Action completed: 1/1 successful. |
| 16 | `delegate_secret` | `PASS` | `4.4s` | `1` | `make run-delegate-secret ARGS='--agent-count 1 --start-agent-index 2290 --scenario domain_match'` | Action completed: 1/1 successful. |
| 18 | `x402_http_call` | `PASS` | `5.1s` | `1` | `make run-x402-http-call ARGS='--agent-count 1 --start-agent-index 2300'` | Action completed: 1/1 successful. |
| 19 | `x402_dkms_http_call` | `PASS` | `68.6s` | `1` | `make run-x402-dkms-http-call ARGS='--agent-count 1 --start-agent-index 2310 --dkms-key-index 0 --timeout 90'` | Action completed: 1/1 successful. |
| 21 | `x402_dkms_http_call_private` | `PASS` | `20.8s` | `1` | `make run-x402-dkms-http-call ARGS='--agent-count 1 --start-agent-index 2320 --use-private-input --dkms-key-index 0 --timeout 90'` | Action completed: 1/1 successful. |
| 22 | `x402_dkms_long_running_http` | `PASS` | `33.5s` | `1` | `make run-x402-dkms-long-running-http ARGS='--agent-count 1 --start-agent-index 2330 --use-private-input --dkms-key-index 0 --timeout 120'` | Action completed: 1/1 successful. |
| 23 | `zk_two_phase` | `PASS` | `25.7s` | `1` | `make run-zk-two-phase ARGS='--agent-count 1 --start-agent-index 2340 --phase2-timeout 120'` | Action completed: 1/1 successful. |
| 24 | `scheduled_zk_two_phase` | `PASS` | `53.7s` | `1` | `make run-scheduled-zk-two-phase ARGS='--agent-count 1 --start-agent-index 2350 --phase2-timeout 120'` | Action completed: 1/1 successful. |
