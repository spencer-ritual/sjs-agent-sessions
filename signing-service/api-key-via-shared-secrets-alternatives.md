# API Keys vs Shared Secrets

**Status:** Draft comparison  
**Date:** 2026-04-10  
**Related:** `api-key-dkms-plan.md`

## Bottom Line

We are at risk of reinventing part of the existing encrypted/delegated secrets stack.

The current "shared secrets" path already gives us:

- encrypted secret transport
- delegate authorization
- on-chain HTTP usage policy
- off-chain request validation before secret injection
- off-chain request validation after secret injection

What it does **not** give us by default is the exact architecture described in `api-key-dkms-plan.md`, where:

- dKMS itself is the component that reads the secret from chain
- dKMS itself injects the secret
- dKMS itself performs the outbound HTTP request

So the real choice is not "shared secrets or new work." The real choice is:

1. use the existing shared-secrets architecture directly
2. keep the new dKMS-centric architecture
3. do a hybrid: reuse the existing shared-secrets policy model, but keep dKMS as the runtime secret boundary

## Existing Shared-Secrets Flow

There are two closely related things in the current stack:

1. **encrypted secrets payloads**
2. **delegated secrets access control**

### Contract-side pieces

The main policy contract is `ritual-sc-internal/src/wallet/SecretsAccessControl.sol`.

It stores:

- `owner -> delegate -> secretsHash -> AccessGrant`

Each grant includes:

- expiry
- `SecretsAccessPolicy`

That policy already models the key exfiltration controls we care about for API keys:

- allowed destinations
- allowed methods
- allowed paths
- allowed query params
- allowed headers
- where the secret may appear
- required body format

There is also an OAuth-specific ciphertext registry in `ritual-sc-internal/src/oauth/OAuthAppSecretsRegistry.sol`, but that contract is only a simple ciphertext DA store. It is not the general delegated-secrets policy system.

### Runtime-side pieces

The main runtime path is in `executor-go-internal/internal/handlers/httpcall/handler.go` plus `executor-go-internal/internal/delegatedsecrets/`.

The existing HTTP flow already does this:

1. caller submits `encrypted_secrets`
2. executor validates secret signatures and delegation policy
3. executor validates the request against the on-chain policy before decrypting
4. executor decrypts secrets
5. executor injects the secrets into the request
6. executor validates the final injected request again
7. executor makes the outbound HTTP call

That is already very close to "use API keys safely in outbound HTTP."

## Comparison To The New API-Key dKMS Plan

### What the current shared-secrets stack already covers well

- policy-based prevention of secret exfiltration
- delegated access
- on-chain source of truth for policy
- HTTP request enforcement in the runtime
- support for header/query/body/path placement rules

### What the new API-key dKMS plan adds

- chain-backed ciphertext retrieval by dKMS itself
- dKMS as the decrypt-and-inject runtime
- potential reuse of the newer DA-key sealing direction used by OAuth
- a cleaner story where the secret never needs to be handed to executor-side secret decryption logic

### What the new plan duplicates

- policy schema
- allowlist logic
- request validation concepts
- secret injection concepts

That duplication is the main architectural smell.

## The Three Real Options

## Option A: Reuse Shared Secrets Directly

Do not build a new dKMS HTTP injection path.

Instead:

- treat API keys as ordinary `encrypted_secrets`
- keep using `SecretsAccessControl`
- use the existing executor HTTP handler to inject the key and make the request

### Pros

- smallest amount of new infrastructure
- reuses the existing policy contract exactly
- reuses the existing executor validation logic exactly
- no new dKMS HTTP proxy surface

### Cons

- does not match the stated dKMS-centric direction
- executor remains the runtime secret consumer
- no chain-backed ciphertext registry by default unless we add one separately
- not aligned with the newer OAuth "dKMS reads sealed secret from chain" mental model

### When this is the right answer

This is the best option if the real goal is simply:

"let agents use API keys safely for HTTP calls"

If that is the goal, the existing shared-secrets system is already the native solution.

## Option B: Keep The New dKMS-Centric Plan

Build the new `APIKeySecretsRegistry` and new dKMS HTTP injection route exactly as proposed.

### Pros

- fully aligned with the newer OAuth storage/runtime model
- dKMS becomes the secret-use boundary
- clearer long-term convergence around dKMS-owned credential operations

### Cons

- duplicates policy concepts already present in `SecretsAccessControl`
- duplicates executor-side HTTP policy semantics
- more implementation work
- higher risk of policy drift between dKMS and executor paths

### When this is the right answer

This is the right option only if we are intentionally moving credential use into dKMS as a platform boundary, not just solving API-key support.

## Option C: Hybrid

Keep dKMS as the runtime secret boundary, but reuse the existing shared-secrets policy model.

This is the strongest option.

### Shape of the hybrid

1. Store API-key ciphertext in a dedicated registry or generic sealed-secret registry.
2. Reuse `SecretsAccessControl` as the policy source of truth.
3. Make dKMS load:
   - ciphertext from the registry
   - policy from `SecretsAccessControl`
4. Make dKMS enforce the same policy semantics the executor already uses for HTTP calls.

### What this avoids

- inventing a second policy schema
- inventing a second set of allowlist concepts
- inventing a second policy storage contract

### What still needs to be built

- a ciphertext store that dKMS can read from chain
- dKMS-side policy enforcement logic, likely ported or shared from executor
- a way to identify the relevant `secretsHash` or credential mapping for policy lookup

## Recommendation

I recommend **Option C: Hybrid**.

That means:

- **do not** invent a brand-new API-key policy model
- **do not** invent a brand-new set of HTTP restriction fields
- **do** reuse `SecretsAccessControl` as the policy contract
- **do** keep a separate ciphertext registry if we want chain-backed DA and dKMS-side retrieval

## Recommended Design Adjustment

The current `api-key-dkms-plan.md` should be adjusted in one important way:

- the API-key feature should **reuse the shared-secrets policy schema and semantics**

More concretely:

### Reuse from existing stack

- `allowedDestinations`
- `allowedMethods`
- `allowedPaths`
- `allowedQueryParams`
- `allowedHeaders`
- `secretLocation`
- `bodyFormat`

These should become the policy model for API-key use too.

### New work that still makes sense

- an API-key ciphertext registry, if we want dKMS to load secrets from chain
- dKMS endpoint(s) for secret-backed outbound HTTP
- a convenience upload flow for secret + policy together

## What To Reuse Exactly

### Reuse the contract

Reuse `SecretsAccessControl` directly for policy.

Do not create a second API-key-specific policy contract unless there is a truly different auth model.

### Reuse the policy semantics

dKMS should match the executor semantics as closely as possible:

- exact host matching
- method allowlists
- path allowlists
- query-param allowlists
- header allowlists
- secret-location restrictions
- post-injection validation

### Reuse the delegated-access mental model

The existing model already answers:

"who may use this secret, under what restrictions?"

That is the right question for API keys too.

## Open Design Question

The main unresolved piece is how to bind policy to chain-stored ciphertext.

Today `SecretsAccessControl` keys grants by `secretsHash`.

If dKMS loads ciphertext from a registry, then we need a stable way to derive the policy lookup key. The cleanest options are:

1. `secretsHash = keccak256(ciphertext)`
2. store `credentialId -> ciphertext`, but still use `keccak256(ciphertext)` for policy lookup
3. later introduce a more generic secret registry that exposes both `credentialId` and canonical ciphertext hash

For now, option 1 is the simplest.

## Concrete Next Step

Before implementing the API-key feature, update the main plan so it says:

1. ciphertext storage may be new
2. policy storage should reuse `SecretsAccessControl`
3. dKMS should enforce the same shared-secrets HTTP policy model rather than inventing a new one

That keeps the new feature aligned with the stack we already have, while still allowing a dKMS-centric runtime design.
