# API Key Injection via dKMS

**Status:** Draft plan  
**Date:** 2026-04-10  
**Related:** `oauth-dkms.md`, `credential-services-design.md`, `dkms/docs/ARCHITECTURE.md`

## Goal

Add an OAuth-like flow for API keys:

1. A user encrypts an API-key bundle to dKMS.
2. The ciphertext is posted on-chain for replicated availability.
3. dKMS fetches and decrypts the bundle inside the TEE.
4. An agent asks dKMS to make an outbound HTTP request using that credential.
5. dKMS injects the API key, performs the HTTP call, and returns the upstream response without ever exposing the raw API key to the agent.

This should intentionally mirror the current OAuth direction:

- sealed secret material lives on-chain as ciphertext
- dKMS is the trust boundary that decrypts and uses it
- agent-facing integration can start with a temporary mock path before full executor/agent wiring

## Important Constraint

This feature must **not** become a generic arbitrary secret exfiltration proxy.

If the agent can say "send this secret to any URL I want", the agent can leak the API key by pointing dKMS at an attacker-controlled host. Because of that, the v1 design must bind each stored API key to an allowlisted outbound target shape.

This should also inherit the **existing dKMS caller-identity policy** rather than introducing a brand-new agent auth model in v1. Today, agents typically reach dKMS through an executor-local service using an owner-scoped bearer token on the internal network, and the executor then reaches dKMS under its own authenticated executor identity. At the public dKMS boundary, access is still fundamentally executor-scoped: mTLS identifies the caller, dKMS verifies the executor is online and has `HTTP_CALL` capability, and endpoints that take `executorId` require it to match the authenticated cert identity.

So the meta-constraint for this feature is:

- preserve the current executor-scoped dKMS access policy
- keep any agent-facing API-key flow bound to the same owner/executor path we already trust today
- do not make raw API-key use available through a new unauthenticated or agent-direct production path
- if we add a temporary mock route for development, keep it explicitly dev-only and outside the long-term auth model

That is the main difference between "store an API key" and "store OAuth client secrets":

- OAuth is naturally bounded by provider token endpoints and callback flows.
- Generic API keys are dangerous unless we add request policy around where and how the key may be used.

## Recommended v1 Scope

Build a narrow v1 with:

- on-chain encrypted storage for API-key bundles
- dKMS retrieval + TEE decryption
- dKMS outbound HTTP proxying with injected auth
- strict allowlisting of target hosts and injection mode
- one temporary dev/mock endpoint that bypasses mTLS when `TLS_ENABLED=false`

Do **not** build in v1:

- arbitrary open proxying
- raw API-key export back to callers
- agent-side secret handling
- multi-step browser flows
- full agent authorization policy beyond the temporary mock/dev path

## Why A Separate Contract

Use a separate contract for API keys.

The current `OAuthAppSecretsRegistry` is keyed as `owner -> ciphertext`. That is fine for one OAuth app bundle per owner, but it is the wrong shape for API keys:

- one owner may have multiple API keys
- keys may represent different providers
- keys may represent different environments or scopes
- deletion/rotation should happen per credential, not per owner

Do not overload the OAuth registry for this.

Contract name:

- `APIKeySecretsRegistry`

Recommended keying model:

- `(owner, credentialId) -> ciphertext`

Where `credentialId` is an app-defined stable identifier such as:

- `bytes32 credentialId = keccak256("openai-prod")`

This keeps the rollout isolated from the OAuth contract and avoids migration risk while we learn what the generic credential model should be.

## Recommended Secret Bundle Shape

Do not entangle the secret with the usage policy.

The encrypted bundle should contain the secret material and only the minimal metadata needed to identify it.

Example encrypted secret bundle:

```json
{
  "provider": "openai",
  "display_name": "OpenAI prod key",
  "api_key": "sk-..."
}
```

### Required fields

- `api_key`

### Optional fields

- `provider`
- `display_name`

## Usage Policy Shape

The routing and injection policy should be a separate object.

Example policy object:

```json
{
  "injection_mode": "authorization_bearer",
  "header_name": "Authorization",
  "query_param": "",
  "allowed_hosts": ["api.openai.com"],
  "allowed_methods": ["GET", "POST"],
  "allowed_path_prefixes": ["/v1/"],
  "base_url": "https://api.openai.com",
  "additional_headers": {
    "OpenAI-Beta": "assistants=v2"
  },
  "strip_agent_headers": ["Authorization", "X-API-Key"],
  "max_response_bytes": 1048576,
  "connect_timeout_ms": 5000,
  "request_timeout_ms": 30000
}
```

This can be handled in two ways:

- a convenience flow that uploads secret + policy together
- a secret-only flow where the policy is attached later or supplied separately

The logical model should still stay split even if one endpoint accepts both at once.

### Supported injection modes for v1

- `authorization_bearer`
- `x_api_key`
- `custom_header`
- `query_param`

Do not support body-template injection in v1 unless there is a concrete need. Header and query injection cover most API-key providers and are much easier to validate safely.

## Contract Design

Create `APIKeySecretsRegistry` in `ritual-sc-internal`.

Suggested interface:

```solidity
function postAPIKeyCiphertext(bytes32 credentialId, bytes calldata ciphertext) external;
function deleteAPIKeyCiphertext(bytes32 credentialId) external;
function getAPIKeyCiphertext(address owner, bytes32 credentialId) external view returns (bytes memory);
```

Suggested events:

```solidity
event APIKeyCiphertextPosted(address indexed owner, bytes32 indexed credentialId, uint256 ownerNonce, uint256 globalVersion);
event APIKeyCiphertextDeleted(address indexed owner, bytes32 indexed credentialId, uint256 globalVersion);
```

Suggested state:

- `mapping(address => mapping(bytes32 => bytes))`
- `mapping(address => uint256) ownerNonce`
- `uint256 version`

This mirrors the OAuth registry semantics while adding credential-level addressing.

## dKMS Runtime Design

### New internal model

Add separate secret and policy types in `dkms/internal/server`.

Suggested Go shape:

```go
type apiKeySecretBundle struct {
    Provider    string `json:"provider,omitempty"`
    DisplayName string `json:"display_name,omitempty"`
    APIKey      string `json:"api_key"`
}

type apiKeyUsagePolicy struct {
    InjectionMode       string            `json:"injection_mode"`
    HeaderName          string            `json:"header_name,omitempty"`
    QueryParam          string            `json:"query_param,omitempty"`
    AllowedHosts        []string          `json:"allowed_hosts"`
    AllowedMethods      []string          `json:"allowed_methods,omitempty"`
    AllowedPathPrefixes []string          `json:"allowed_path_prefixes,omitempty"`
    BaseURL             string            `json:"base_url,omitempty"`
    AdditionalHeaders   map[string]string `json:"additional_headers,omitempty"`
    StripAgentHeaders   []string          `json:"strip_agent_headers,omitempty"`
    MaxResponseBytes    int64             `json:"max_response_bytes,omitempty"`
    ConnectTimeoutMS    int               `json:"connect_timeout_ms,omitempty"`
    RequestTimeoutMS    int               `json:"request_timeout_ms,omitempty"`
}
```

### Core dKMS flow

1. Agentic caller sends `ownerAddress`, `credentialId`, and the outbound request description.
2. dKMS loads both the ciphertext and the usage policy for that credential together.
3. dKMS decrypts inside the TEE using the same DA-key pattern as the new OAuth path.
5. dKMS validates:
   - host is allowlisted
   - method is allowlisted
   - path matches allowlisted prefixes
   - agent is not overriding auth headers
6. dKMS injects the API key according to `injection_mode`.
7. dKMS executes the outbound HTTP request.
8. dKMS returns sanitized response fields:
   - status
   - headers allowlist or filtered headers
   - body bytes/text up to a max size

### New endpoint surface

Recommended final endpoint:

- `POST /v1/api_keys/http`

Recommended temporary dev/mock endpoint:

- `POST /v1/api_keys/mock_http`

Behavior:

- `/v1/api_keys/http`
  - same auth policy as existing dKMS executor endpoints
  - requires mTLS when `TLS_ENABLED=true`
- `/v1/api_keys/mock_http`
  - only enabled when `TLS_ENABLED=false`
  - bypasses executor auth entirely
  - exists only to unblock end-to-end development before real agent wiring lands

Do **not** allow the mock endpoint in production.

## Request / Response Shape

Suggested request:

```json
{
  "ownerAddress": "0x...",
  "credentialId": "0x...",
  "request": {
    "method": "POST",
    "url": "https://api.openai.com/v1/chat/completions",
    "headers": {
      "Content-Type": "application/json"
    },
    "body": "{\"model\":\"gpt-4.1-mini\",\"messages\":[...]}"
  }
}
```

Suggested response:

```json
{
  "status": 200,
  "headers": {
    "content-type": "application/json"
  },
  "body": "...",
  "truncated": false
}
```

Notes:

- dKMS should strip hop-by-hop headers and sensitive upstream headers before returning.
- dKMS should cap response size.
- dKMS should reject redirects in v1 unless the redirected host is still allowlisted.

## Crypto / Keying Direction

The safest path is to follow the new OAuth direction:

- users encrypt API-key bundles to the owner-derived DA public key
- dKMS derives the matching DA private key for `(owner, index=0)` inside the TEE
- dKMS decrypts the bundle locally

That keeps API-key storage aligned with the newer OAuth model instead of reintroducing the old static sealing pubkey shape.

If we want multiple credential namespaces later, we can either:

- keep one DA key per owner and distinguish records only at the contract layer, or
- derive credential-specific wrapping keys later

For v1, keep the contract responsible for `credentialId` addressing and keep dKMS decryption owner-based.

## Authz Model For v1

### Temporary mock/dev mode

In the short term, the mock endpoint is enough to prove:

- ciphertext posting
- dKMS retrieval
- decryption
- auth injection
- outbound call execution

It is acceptable that this path does not yet prove "the calling agent really has access", as long as:

- it is only available when `TLS_ENABLED=false`
- the plan treats it as temporary

### Real authenticated mode

When we move past the mock path, `POST /v1/api_keys/http` should reuse the same executor validation used by:

- `/v1/get_key`
- `/v1/get_address`
- `/v1/sign_transaction`
- `/v1/oauth/*`

Longer term, the authz check should bind:

- authenticated executor
- owner address
- credential id
- agent/session context

But that can be a follow-on PR once the runtime path exists.

## Main Security Risks

### 1. Arbitrary-host exfiltration

If the agent can choose any URL, it can leak the API key.

Mitigation:

- require `allowed_hosts`
- require host validation after URL parsing
- optionally require `base_url`
- reject mismatched scheme/host/path

### 2. Header override

If the agent can supply its own `Authorization` or `X-API-Key` header, it may break policy or confuse auditing.

Mitigation:

- strip conflicting auth headers from agent input
- have dKMS own the injected auth header

### 3. Response-based secret reflection

Some upstreams may echo request headers or bodies back.

Mitigation:

- never include injected secret material in returned debug logs
- avoid request dumps in logs
- optionally redact exact known secret value from response bodies in debug/test mode

### 4. Open proxy abuse

dKMS could become a general outbound HTTP proxy.

Mitigation:

- narrow endpoint purpose
- per-request limits
- allowlisted hosts only
- bounded body/response sizes
- explicit timeout limits

## Rollout Plan By Repo

### 1. `ritual-sc-internal`

Add the new registry contract and tests.

Deliverables:

- `src/api-keys/APIKeySecretsRegistry.sol` or similar
- Foundry tests for:
  - post/get
  - replace
  - delete
  - sender isolation
  - multiple `credentialId`s per owner
  - event/version semantics

### 2. `dkms`

Add the runtime support.

Deliverables:

- new secret-bundle parsing + validation
- new usage-policy parsing + validation
- chain fetch helper for `APIKeySecretsRegistry`
- TEE decrypt path using owner-derived DA key
- outbound HTTP executor with strict validation
- `POST /v1/api_keys/http`
- `POST /v1/api_keys/mock_http`
- unit tests for:
  - bundle validation
  - allowlist enforcement
  - header/query injection modes
  - response truncation
  - mock endpoint only when TLS disabled

### 3. `traffic-gen-internal`

Add a dev/e2e harness similar to the OAuth scripts.

Deliverables:

- helper to encrypt an API-key secret bundle
- helper to post ciphertext to the new contract
- script to call the mock dKMS endpoint
- one reproducible example against a simple echo service or approved external API

### 4. `ritual-node-internal`

Wire local network support.

Deliverables:

- deploy the new registry in genesis/dev flows
- export generated state/resource files
- expose any needed env vars for local dKMS testing

### 5. Future repos

Later PRs can wire real agent usage in:

- `executor-go-internal`
- `claw-spawner`
- agent tool surfaces

That is intentionally not required for the first implementation PR.

## Suggested PR Breakdown

### PR 1: contracts

- add `APIKeySecretsRegistry`
- add tests
- export state artifacts

### PR 2: dKMS core

- add bundle type
- add on-chain fetch + decrypt
- add authenticated and mock proxy endpoints
- add tests

### PR 3: local dev / e2e

- add encryption and posting helpers
- add mock endpoint exercise script
- wire local deployment/config

### PR 4: real agent integration

- replace mock caller with authenticated executor/agent path

## Open Questions

1. Should v1 support only header injection, or do we need query-param providers immediately?
2. Should `credentialId` be `bytes32` or `string` at the contract surface?
3. Do we want one contract for API keys only, or should we jump straight to a generic `CredentialSecretsRegistry`?
4. Should dKMS return raw bytes, base64, or text for upstream responses?
5. Do we need streaming responses in v1? Recommendation: no.
6. Do we want to allow more than one host per credential in v1? Recommendation: yes, but keep it small and explicit.

## Recommended First Slice

The smallest useful first slice is:

1. Add `APIKeySecretsRegistry`.
2. Define a sealed secret bundle with only:
   - `api_key`
3. Define a separate usage policy with at least:
   - `injection_mode`
   - `header_name`
   - `allowed_hosts`
4. Add `POST /v1/api_keys/mock_http` in dKMS.
5. Support only:
   - `authorization_bearer`
   - `custom_header`
6. Exercise it with a local test target or simple external API.

That proves the end-to-end architecture without overcommitting to the long-term agent authz model.
