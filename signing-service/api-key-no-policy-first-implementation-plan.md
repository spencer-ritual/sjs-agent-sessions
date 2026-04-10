# API Key Implementation Plan: No-Policy First

**Status:** Draft  
**Date:** 2026-04-10  
**Related:** `api-key-dkms-plan.md`, `api-key-via-shared-secrets-alternatives.md`

## Goal

Get the end-to-end API-key flow working first:

- user seals an API-key secret
- ciphertext is stored on-chain
- dKMS reads the ciphertext from chain
- dKMS decrypts it inside the TEE
- an agentic caller asks dKMS to make an outbound HTTP request
- dKMS injects the API key and returns the response

This plan explicitly **defers policy enforcement** to a later PR.

## Intentional Deferral

The existing shared-secrets infrastructure is still the right place to look for future policy work.

In particular, a later PR can reuse:

- `SecretsAccessControl`
- the shared-secrets HTTP restriction model
- the existing executor-side policy semantics

But none of that is required for the first implementation chunk. The first chunk should prioritize getting the storage, retrieval, decryption, and outbound-call path working.

## PR 1: End-to-End Secret Flow, No Policy

### Objective

Build the minimum working architecture with no allowlists or policy checks.

This PR should answer:

"Can dKMS read an API-key ciphertext from chain and use it to make a real outbound HTTP call?"

### Scope

Primary repos:

- `ritual-sc-internal`
- `dkms`

Likely support repos:

- `ritual-node-internal`
- `traffic-gen-internal`

### Required implementation

1. Add a ciphertext registry contract.

Recommended name:

- `APIKeySecretsRegistry`

Recommended interface:

```solidity
function postAPIKeyCiphertext(bytes32 credentialId, bytes calldata ciphertext) external;
function deleteAPIKeyCiphertext(bytes32 credentialId) external;
function getAPIKeyCiphertext(address owner, bytes32 credentialId) external view returns (bytes memory);
```

2. Keep the secret bundle minimal.

Recommended encrypted secret bundle:

```json
{
  "provider": "openai",
  "display_name": "OpenAI prod key",
  "api_key": "sk-..."
}
```

3. Add dKMS chain-read support for the new registry.

4. Add dKMS secret decryption support for the new bundle type.

Use the same DA-key direction as the current OAuth flow rather than inventing a separate sealing model.

5. Add a dKMS HTTP execution endpoint with no policy checks.

Recommended endpoints:

- `POST /v1/api_keys/http`

Behavior for this PR:

- dKMS loads ciphertext from chain
- dKMS decrypts the API-key bundle
- dKMS injects the API key into the request
- dKMS makes the outbound request
- dKMS returns the bounded upstream response

6. Keep auth model reuse, even though policy is deferred.

Use the same model as existing dKMS endpoints:

- reuse the same executor-scoped dKMS identity model as existing endpoints
- require mTLS when enabled
- when `TLS_ENABLED=false`, allow the endpoint to run in the normal development mode without blocking on client certs

7. Add local/dev tooling.

At minimum:

- helper to encrypt an API-key bundle
- helper to post ciphertext to the registry
- helper to call `POST /v1/api_keys/http` in local development

### Explicit non-goals for PR 1

Do not implement in this PR:

- host allowlists
- method allowlists
- path allowlists
- `SecretsAccessControl` lookups
- delegated shared-secrets policy enforcement
- secret-location or body-format restrictions

### Reviewer verification criteria

A reviewer should be able to verify all of the following:

1. The new contract stores ciphertext by `(owner, credentialId)`.
2. dKMS can read ciphertext from the contract and decrypt it successfully.
3. The encrypted bundle contains only secret material, not policy.
4. `POST /v1/api_keys/http` exists and uses the normal dKMS executor auth model.
5. There is at least one working end-to-end example that proves:
   - ciphertext can be posted
   - dKMS can load it
   - dKMS can inject the API key
   - dKMS can return an HTTP response
6. The same endpoint works in normal dKMS development mode when `TLS_ENABLED=false`.
7. No policy contract or policy schema was introduced in this PR.

### PR 1 complete when

All of the following are true:

- ciphertext storage works
- dKMS retrieval works
- dKMS decryption works
- outbound HTTP execution works
- dev tooling can demonstrate the full flow

## PR 2: Harden And Clean Up The Runtime Path

### Objective

Take the working end-to-end flow and make it stable enough for broader use, still without doing full policy integration yet.

This PR should answer:

"Can the no-policy path be made reliable, bounded, and reviewable before we add shared-secrets policy enforcement?"

### Scope

Primary repos:

- `dkms`
- `traffic-gen-internal`

Optional support repo:

- `ritual-node-internal`

### Required implementation

1. Tighten request and response bounds.

Add:

- request size limits
- response size limits
- timeout limits
- header filtering on returned responses
- redirect handling rules

2. Make auth injection support the minimum useful set.

Recommended first set:

- `authorization_bearer`
- `custom_header`

Optional if easy:

- `query_param`

3. Improve logging and observability.

Add:

- structured logs for credential lookup and outbound request status
- no plaintext API-key logging
- useful error messages for missing credential / decrypt failure / upstream failure

4. Add stronger tests.

Required tests:

- missing ciphertext
- invalid ciphertext
- decrypt failure
- auth header injection works
- custom header injection works
- response truncation works
- endpoint behaves correctly in `TLS_ENABLED=false` development mode

5. Keep the implementation policy-free on purpose.

This PR may mention future policy reuse, but it should still not wire:

- `SecretsAccessControl`
- shared-secrets enforcement

### Explicit non-goals for PR 2

Do not implement in this PR:

- policy lookups
- delegated secret access checks
- host/method/path restrictions from shared-secrets

### Reviewer verification criteria

A reviewer should be able to verify all of the following:

1. The runtime path is bounded and does not return unbounded responses.
2. The supported auth injection modes are clear and tested.
3. API keys are not logged in plaintext.
4. Failure modes are tested and understandable.
5. The code still does not introduce a second policy system.
6. The code still does not wire `SecretsAccessControl` yet.

### PR 2 complete when

All of the following are true:

- the runtime path is reliable and bounded
- tests cover success and core failure cases
- local tooling still demonstrates the flow
- the code is ready for a later policy-enforcement PR

## Future PR: Reuse Shared-Secrets Policy Infrastructure

This is intentionally not part of the first two chunks.

When we are ready, the next PR should:

- reuse `SecretsAccessControl`
- reuse shared-secrets HTTP policy semantics
- bind policy lookup to the stored ciphertext, likely via `secretsHash = keccak256(ciphertext)`
- add deny-path enforcement before and after injection

That future PR should explicitly avoid inventing a new API-key-specific policy model.

## Why This Split Is Better

This split is better for implementation because:

- PR 1 proves the core architecture works
- PR 2 makes the core architecture usable and testable
- the policy PR can then focus only on policy reuse and enforcement

This avoids mixing three kinds of work in one review:

- storage
- runtime secret use
- policy design and enforcement

## Final Acceptance Criteria

This no-policy-first plan is successful if:

- the first two PRs get the end-to-end secret flow working
- dKMS becomes the runtime secret-use boundary
- the code remains compatible with future shared-secrets policy reuse

This plan is unsuccessful if:

- the first PR tries to solve policy too
- the implementation invents a new policy model prematurely
- the no-policy path becomes the permanent answer instead of a stepping stone
