# Cross-Repo PR Description: Remove Endpoint Cert Lookup

## PR Stack

This stack removes endpoint-authoritative mTLS certificate lookup from the TEE service registry flow and migrates callers to service-record-based verification. This matters because endpoint strings are self-asserted routing metadata, not authenticated identities.

- `ritual-sc-internal`: [PR 244](https://github.com/ritual-net/ritual-sc-internal/pull/244) - Remove endpoint cert lookup
- `ritual-go-common`: [PR 63](https://github.com/ritual-net/ritual-go-common/pull/63) - Remove endpoint cert lookup
- `executor-go-internal`: [PR 184](https://github.com/ritual-net/executor-go-internal/pull/184) - Remove endpoint cert lookup
- `ritual-vllm-proxy-go`: [PR 47](https://github.com/ritual-net/ritual-vllm-proxy-go/pull/47) - Remove endpoint cert lookup
- `ritual-node-internal`: [PR 381](https://github.com/ritual-net/ritual-node-internal/pull/381) - Remove endpoint cert lookup

All five PRs are on `spencer/sc-codex-audit-2` and target `spencer/sc-codex-audit`.

## Summary

This stack removes the old `endpoint -> mTlsSpkiHash` trust lookup. Endpoints remain service routing metadata, but they are no longer treated as a globally owned or authenticated namespace.

The new verification model is:

1. Select a registry `TEEServiceNode` using the strongest trusted input available for the call path: known TEE/service identity, capability discovery, or a constrained compatibility scan.
2. Dial the selected service record's `endpoint`.
3. Compute the presented TLS certificate's SPKI hash.
4. Accept the peer only if the presented SPKI hash matches the selected service record's `mTlsSpkiHash`, and the selected record also satisfies the expected validity, capability, and identity policy.

This makes the service record the source of verifier material. The endpoint is still needed to route traffic, but it does not decide which certificate hash the client should trust.

## Motivation

The previous registry flow allowed clients to start with only a raw endpoint URL and ask the contract for the certificate hash:

1. Client has an endpoint URL.
2. Client calls `getMTlsSpkiHashForEndpoint(endpoint)`.
3. The contract resolves `endpointToAddress[keccak256(endpoint)]`.
4. Client dials the endpoint and pins the certificate against the returned hash.

That made a self-asserted endpoint string part of the trust lookup. The endpoint is useful as "dial this URL" metadata, but it is not an authenticated identity. The authenticated peer identity is the presented TLS certificate's SPKI hash, checked against a service record registered by a TEE identity and validated by the registry's attestation and capability policy.

In the corrected model, duplicate or fake endpoints do not create a contract-level ownership problem. They may make a service unreachable, suspicious, or ambiguous to endpoint-only compatibility paths, but they should not create a global namespace conflict in the registry.

## Cross-Repo Changes

### `ritual-sc-internal`

- Removes `endpointToAddress` from `TEEServiceRegistry`.
- Removes `getMTlsSpkiHashForEndpoint` overloads from `ITEEServiceRegistry` and `TEEServiceRegistry`.
- Removes endpoint mapping writes/deletes from registration and offline flows.
- Keeps `endpoint` and `mTlsSpkiHash` as fields on `TEEServiceNode`.
- Keeps address/service-record-based lookup as the registry source of truth.
- Removes the duplicate-endpoint ownership behavior from the prior audit-fix direction.

### `ritual-go-common`

- Regenerates TEE service registry bindings without endpoint-based SPKI lookup.
- Removes endpoint hash lookup/cache APIs that made endpoint the trust primitive.
- Adds service-record selection helpers so callers can obtain endpoint, TEE address, capability, validity, and mTLS SPKI hash together.
- Keeps endpoint-only matching only as a compatibility bridge, and fails closed when a raw endpoint matches more than one service record without another trusted selector.

### `executor-go-internal`

- Migrates outbound mTLS clients away from `GetCertPubKeyHashForEndpoint`.
- Uses selected service records to create TLS config and pin against the selected record's `mTlsSpkiHash`.
- Applies the expected validity and capability checks for dKMS, vLLM, image, audio, video, FHE, media polling, and telemetry relay paths.
- Treats endpoint-only compatibility matches as ambiguous when duplicates exist.

### `ritual-vllm-proxy-go`

- Updates registration idempotence to look up the proxy's own TEE service record by `teeAddress`.
- Skips registration only when the existing service record is valid and matches expected capability, endpoint, `mTlsSpkiHash`, and payment address.
- No longer uses endpoint-authoritative lookup to decide whether this proxy is already registered.

### `ritual-node-internal`

- Refreshes local-network EL resources after the contract state/API change.
- Keeps generated genesis artifacts aligned with the updated TEE service registry.
- Provides the integration smoke surface for the full stack.

## Review Order

Recommended review order:

1. `ritual-sc-internal` PR 244: establishes the contract/API change.
2. `ritual-go-common` PR 63: regenerates bindings and introduces service-record-based helpers.
3. `executor-go-internal` PR 184 and `ritual-vllm-proxy-go` PR 47: migrate live Go callers.
4. `ritual-node-internal` PR 381: refreshes generated local-network artifacts and validates the stack in the integrated environment.

## Compatibility And Failure Behavior

The intended invariant is that no production path relies on `endpoint -> mTlsSpkiHash` as the trust lookup.

If a caller already knows the intended TEE or service identity, it should look up that service record directly. If it is doing service discovery, it should discover valid service records by capability and choose a record under the relevant policy. If legacy code only has a raw endpoint, it may scan service records as a compatibility bridge, but duplicate matches must fail closed unless another trusted identity or policy input selects exactly one service record.

## Test Plan

Per-repo test plans from the PRs:

- `ritual-sc-internal`: `forge test --match-path test/TEEServiceRegistry.t.sol`
- `ritual-go-common`: `make lint`; `go test ./registry ./mtls ./registration`
- `executor-go-internal`: `make lint`; `go test ./internal/dkms ./internal/handlers/llmcall ./internal/handlers/imagecall ./internal/handlers/audiocall ./internal/handlers/videocall ./internal/handlers/fhecall ./internal/vllm ./internal/services/poll ./internal/services/keyderivation`
- `ritual-vllm-proxy-go`: `make lint`; `go test ./internal/registration`
- `ritual-node-internal`: `make restart-network vllm_mode=local_mock`; `make tee-registry`; `make test-e2e TEST=test_async_llm_call`; `make test-e2e TEST=test_async_dkms_key`

Cross-repo smoke target:

- Start the local network with vLLM mock mode.
- Register TEE services against the updated registry.
- Exercise async LLM and dKMS E2E traffic.
- Confirm outbound clients pin TLS against selected service records rather than endpoint reverse lookup.

## Acceptance Criteria

- `TEEServiceRegistry` no longer stores or maintains `endpointToAddress`.
- Endpoint-based mTLS lookup functions are absent from the contract ABI and generated Go bindings.
- Endpoints remain non-authoritative routing metadata attached to service records.
- mTLS verification pins against the selected service record's `mTlsSpkiHash`.
- Callers select service records by identity or capability where available.
- Endpoint-only compatibility paths fail closed when duplicate endpoint matches are ambiguous.
- Registration idempotence uses service identity, not endpoint ownership.
- The old duplicate-endpoint rejection behavior is not part of the final audit fix.

## Risk Notes

- The largest behavioral risk is a caller path that still starts from only an endpoint and silently picks the wrong service record. The migrated compatibility paths should fail closed on ambiguity.
- Generated artifacts must stay in sync with the contract ABI. Reviewers should check the contract PR and binding regeneration together.
- Existing documentation or mental models may still describe endpoint lookup as the source of certificate hashes. That language should be treated as stale after this stack.
