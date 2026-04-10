# API Key Hybrid Implementation Plan

**Status:** Draft  
**Date:** 2026-04-10  
**Related:** `api-key-dkms-plan.md`, `api-key-via-shared-secrets-alternatives.md`

## Goal

Implement API-key support using the hybrid architecture:

- keep dKMS as the runtime secret boundary
- reuse `SecretsAccessControl` for policy semantics and storage
- add chain-backed ciphertext storage for API-key material

This plan is intentionally split into **two weak-agent-friendly steps**. Each step should be reviewable on its own and should not require the implementing agent to make major architectural decisions mid-flight.

## Non-Goal

Do not ask the implementing agent to redesign policy semantics.

The agent should **reuse the existing shared-secrets policy model**:

- `allowedDestinations`
- `allowedMethods`
- `allowedPaths`
- `allowedQueryParams`
- `allowedHeaders`
- `secretLocation`
- `bodyFormat`

## Step 1: Add Chain-Backed Ciphertext Storage

### Objective

Add the on-chain storage path for API-key ciphertext, without yet building the full dKMS HTTP execution flow.

This step should answer:

"Can we store and retrieve sealed API-key ciphertext in a way that dKMS can consume later, while reusing the existing shared-secrets policy model?"

### Scope

Primary repo:

- `ritual-sc-internal`

Possible follow-up plumbing if needed:

- state artifact generation in `ritual-sc-internal`
- local deployment wiring in `ritual-node-internal`

### Required implementation

1. Add a dedicated ciphertext registry contract.

Recommended name:

- `APIKeySecretsRegistry`

Recommended interface:

```solidity
function postAPIKeyCiphertext(bytes32 credentialId, bytes calldata ciphertext) external;
function deleteAPIKeyCiphertext(bytes32 credentialId) external;
function getAPIKeyCiphertext(address owner, bytes32 credentialId) external view returns (bytes memory);
```

2. Make the contract narrowly scoped to ciphertext storage only.

It should:

- store ciphertext
- support replacement
- support deletion
- emit clear events

It should not:

- duplicate `SecretsAccessControl`
- duplicate policy fields
- enforce delegate logic itself

3. Keep the policy binding model compatible with `SecretsAccessControl`.

The intended lookup model is:

- ciphertext is stored by `(owner, credentialId)`
- policy is still keyed by `secretsHash`
- reviewer should be able to see how `secretsHash = keccak256(ciphertext)` would be used later

The agent does not need to wire that full runtime lookup yet, but the contract and docs must not make it impossible.

4. Add tests.

Required tests:

- post/get works
- replace works
- delete works
- sender isolation works
- multiple `credentialId`s per owner work
- event emission is correct

5. Update deploy/state artifacts if this repo already tracks them for new contracts.

### Explicit instructions for weak agent

- Reuse `OAuthAppSecretsRegistry` as the starting shape for ciphertext storage.
- Do **not** modify `SecretsAccessControl` in this step unless absolutely necessary.
- Do **not** invent an API-key-specific policy contract.
- Do **not** add runtime semantics to the contract beyond storage and events.

### Reviewer verification criteria

A reviewer should be able to verify all of the following:

1. There is a new ciphertext registry contract, and it is clearly separate from `SecretsAccessControl`.
2. The contract stores ciphertext by `(owner, credentialId)` rather than only by owner.
3. No new policy schema was introduced in the contract layer.
4. Foundry tests cover post, replace, delete, owner isolation, and multiple credential IDs.
5. The contract surface is storage-only and does not try to reimplement delegated access control.
6. Any generated state artifacts or deployment wiring are updated consistently.

### Step 1 complete when

All of the following are true:

- the new contract exists
- tests pass for the contract
- deployment/state outputs are updated if required by repo conventions
- reviewer confirms this step did not create a second policy system

## Step 2: Add dKMS Runtime Support Using Shared-Secrets Policy

### Objective

Add the dKMS runtime path that:

- reads API-key ciphertext from chain
- derives `secretsHash`
- fetches policy from `SecretsAccessControl`
- enforces the same shared-secrets HTTP policy semantics
- injects the API key
- performs the outbound HTTP call

This step should answer:

"Can dKMS execute API-key-backed HTTP calls without inventing a new policy model?"

### Scope

Primary repo:

- `dkms`

Likely supporting repo:

- `traffic-gen-internal` for dev/e2e harness

### Required implementation

1. Add chain-read support in dKMS for:

- `APIKeySecretsRegistry`
- `SecretsAccessControl`

2. Add an API-key secret bundle type in dKMS.

Keep it minimal:

```json
{
  "provider": "openai",
  "display_name": "OpenAI prod key",
  "api_key": "sk-..."
}
```

Do not put policy fields into the encrypted secret bundle.

3. Reuse shared-secrets policy semantics instead of inventing a new API-key policy shape.

The dKMS runtime should use the same concepts already used by executor shared secrets:

- destination allowlist
- method allowlist
- path allowlist
- query-param allowlist
- header allowlist
- secret-location restriction
- body-format restriction

4. Add a dKMS HTTP execution endpoint.

Recommended endpoints:

- production path: `POST /v1/api_keys/http`
- dev-only path: `POST /v1/api_keys/mock_http`

5. Make the production endpoint inherit existing dKMS caller identity policy.

That means:

- same executor-scoped auth model
- mTLS when enabled
- same executor validation pattern used by existing dKMS endpoints

6. Keep the mock endpoint dev-only.

It must:

- only exist when `TLS_ENABLED=false`
- be clearly documented as temporary
- not become the production auth model

7. Add runtime validation in the correct order.

Required order:

1. parse request
2. load ciphertext and policy
3. decrypt ciphertext
4. derive `secretsHash = keccak256(ciphertext)` and confirm the policy lookup path is consistent
5. validate request against policy before injection where applicable
6. inject secret
7. validate final injected request against policy where applicable
8. execute outbound HTTP request
9. return bounded response

8. Add tests.

Required tests:

- ciphertext retrieval works
- policy retrieval works
- request is rejected when host is not allowed
- request is rejected when method is not allowed
- request is rejected when header/query placement violates policy
- conflicting auth headers from caller are rejected or stripped
- response size is bounded
- mock endpoint is unavailable when TLS is enabled

9. Add a small dev harness.

In `traffic-gen-internal` or equivalent:

- helper to encrypt an API-key secret bundle
- helper to post ciphertext to the registry
- helper to exercise the mock endpoint

### Explicit instructions for weak agent

- Reuse executor shared-secrets policy semantics as the source of truth.
- Do **not** invent new policy field names in dKMS.
- Do **not** add API-key-specific policy storage in dKMS.
- Do **not** combine secret and policy into one encrypted object.
- Keep the first implementation narrow: one secret, one credential, one outbound request.

### Reviewer verification criteria

A reviewer should be able to verify all of the following:

1. dKMS reads ciphertext from the new registry and policy from `SecretsAccessControl`.
2. The policy model in dKMS matches the shared-secrets model rather than introducing new API-key-specific fields.
3. The encrypted bundle contains only secret material, not policy.
4. The production endpoint uses the same executor-scoped identity model as existing dKMS endpoints.
5. The mock endpoint is only available in dev mode.
6. Requests to disallowed hosts/methods/paths/locations are rejected.
7. The implementation clearly derives or uses `secretsHash` compatibly with `SecretsAccessControl`.
8. There are tests for policy enforcement and for mock-endpoint gating.
9. The dev harness can demonstrate one end-to-end successful request.

### Step 2 complete when

All of the following are true:

- dKMS can read ciphertext and policy from chain
- dKMS can decrypt and inject an API key into an outbound HTTP request
- policy enforcement matches the shared-secrets model
- tests cover the main deny paths
- reviewer confirms no second policy system was introduced

## Delegation Guidance

These two steps are intentionally split so they can be delegated separately:

- **Step 1** is mostly contract/storage work
- **Step 2** is mostly runtime/policy-enforcement work

That means a weaker agent can succeed if given only one step at a time, with strict instructions not to expand scope.

## Recommended Review Order

1. Review Step 1 first and confirm that ciphertext storage is correct and policy was not duplicated.
2. Only after Step 1 is accepted, start Step 2.
3. In Step 2 review, focus first on policy reuse and auth model reuse, then on the HTTP mechanics.

## Final Acceptance Criteria

This implementation plan is successful if the final result has:

- one ciphertext storage path
- one policy storage path
- one set of HTTP restriction semantics
- dKMS as the runtime secret-use boundary

It is unsuccessful if the implementation introduces:

- a second policy contract
- a second set of policy field names
- a production path that bypasses the existing dKMS identity model
