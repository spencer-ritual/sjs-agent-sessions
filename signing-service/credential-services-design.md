# Secure Credential Service Design

**Status:** Draft  
**Date:** 2026-04-03  
**References:** Turnkey OAuth credential and OAuth 2.0 reference material

## Objective

Move the highest-sensitivity credential operations out of the agent/executor runtime and into hardened external services, without trying to solve agent adherence inside the same design.

This doc proposes **one Go service**:

1. `credential-service`

The service is exposed to agents as an MCP server and owns all relevant API routes and data for OAuth delegation and EVM signing.

## Bottom Line

- The top-priority web2 credential flow we can design concretely today is **OAuth/OIDC-style delegation**, especially for providers like X/Twitter and similar integrations.
- **Generic API-key custody is out of scope for v1.** OAuth has a well-understood delegation and revocation model, while arbitrary API-key custody does not yet have a similarly bounded interface in this design.
- **Agent adherence is a perpendicular concern.** This service provides a safe path for signing and delegated auth, but it does not by itself guarantee that an agent will use it. Harness/orchestration/model-side controls must enforce that separately.
- MCP is the right transport surface for agent access, but the hard security boundary is the backend service authorization and policy engine, not MCP alone.

## Design Requirements

- Secrets must no longer be directly available on the executor/agent.
- The agent should be able to ask for actions such as:
  - "sign this EVM transaction"
  - "authorize against X/Twitter and act on my behalf"
- The design should assume we are building our own infrastructure, while taking inspiration from existing systems such as Turnkey.
- The design should cover the MCP-mediated flow.
- The design should enumerate sad paths and define how each is bounded.
- The design should stay decoupled from the separate problem of forcing agents to comply with the tool path.

## Non-Goals

- Enforcing that all agents always use this service
- Supporting arbitrary plaintext secret export to agents
- Supporting arbitrary generic API keys in v1
- Building a general-purpose OAuth identity provider from scratch
- Solving every provider-specific API integration in v1

## Why One Service

The primary goal is to remove sensitive credential operations from the agent, not to maximize service decomposition in v1.

A single `credential-service` is acceptable for the first version if it:

- owns all credential-related API routes in one place
- stores all relevant credential metadata and policy data in one service boundary
- exposes one MCP surface to the harness/agent
- keeps OAuth handling and EVM signing as separate internal modules

This gives us:

- a simpler deployment model
- one authn/authz boundary for agent access
- one audit pipeline
- one place to apply policy and observability

The tradeoff is a broader blast radius than a split-service design, but that is acceptable in v1 if we keep strong internal separation between the OAuth and EVM modules.

## Architecture Overview

```text
                         +----------------------+
                         |  User / Human Owner  |
                         +----------+-----------+
                                    |
                         browser redirect / consent
                                    |
                                    v
+-------------+    MCP     +----------------------+      HTTPS      +------------------+
| Agent /     +----------->+ credential-service   +---------------->+ OAuth Provider   |
| Harness     |            | Go MCP + HTTP API    |                 | X, Discord, etc. |
+------+------+            +----------+-----------+                 +------------------+
       |                              |
       |                              | JSON-RPC
       |                              v
       |                    +------------------+
       |                    | EVM RPC / Chain  |
       |                    | Ethereum, Base   |
       |                    +------------------+
```

## MCP Flow

This section captures the MCP flow that should be explicit in the design.

### Common MCP Service Flow

1. The harness gives the agent access to the `credential-service` MCP server.
2. The harness authenticates to the MCP server with a short-lived internal credential for the current run/session.
3. The agent calls MCP tools exposed by the service.
4. The service performs its own authorization and policy checks for the user, agent, run, and requested action.
5. The service either executes the action or returns a bounded denial/error.

Important distinction:

- **MCP auth** is the transport/session layer between agent-side runtime and service.
- **OAuth** is the downstream delegated authorization flow between end-user, provider, and the service's OAuth module.

These are separate layers and should not be conflated.

### OAuth Flow

```text
Agent -> MCP oauth.begin(provider, scopes, user_ref)
      <- auth_session_id, authorization_url

User browser -> provider authorize endpoint
Provider -> credential-service callback with auth_code
credential-service -> provider token endpoint
credential-service -> provider whoami/userinfo endpoint
credential-service stores encrypted access/refresh tokens

Agent -> MCP oauth.poll(auth_session_id)
      <- credential_handle ready

Agent -> MCP oauth.invoke(credential_handle, action, params)
credential-service performs approved provider API request using stored token
      <- action result
```

### EVM Signer Flow

```text
Agent -> MCP evm.send_transaction(signer_id, chain_id, tx)
credential-service -> signer ownership and request validation
credential-service -> optional simulation
credential-service -> sign
credential-service -> broadcast
      <- tx_hash or bounded denial
```

### MCP OAuth Flow Walkthrough

The `credential-service` acts as both:

- the **OAuth client** toward external providers such as X/Twitter
- the **authorization server** toward the agent, issuing MCP-scoped session credentials

These are two separate layers and should not be conflated.

#### 1. Initial Request Returns `401`

The agent calls a protected MCP tool endpoint without a valid token.

The service replies with:

- `401 Unauthorized`
- a `WWW-Authenticate: Bearer` hint
- a pointer to the RFC 8414 metadata document at `/.well-known/oauth-authorization-server`

This tells the agent that authorization is required and where to start.

#### 2. Discovery

The agent fetches the metadata document.

That document advertises:

- `authorization_endpoint`
- `token_endpoint`
- `registration_endpoint`
- supported scopes

This part of the MCP ecosystem is still somewhat fluid, but the core discovery and authorization flow is stable enough to design around.

#### 3. Redirect For User Consent

The agent, or its host process, opens the user's browser to the authorization URL:

```text
https://provider.example.com/authorize
  ?response_type=code
  &client_id=client123
  &redirect_uri=https://credential-service/oauth/callback/:provider
  &scope=tweet.read tweet.write
  &code_challenge=<hash>
  &code_challenge_method=S256
  &state=<random>
```

The user sees a consent screen and approves the requested access.

The provider redirects back to:

```text
https://credential-service/oauth/callback/:provider?code=xyz&state=<same>
```

#### 4. Code Exchange With PKCE

The service receives the callback, validates `state` against the stored `PendingAuthSession`, and exchanges the auth code at the provider token endpoint:

```text
POST https://provider.example.com/token
  grant_type=authorization_code
  code=xyz
  redirect_uri=https://credential-service/oauth/callback/:provider
  client_id=client123
  code_verifier=<original_secret>
```

The provider returns an access token and refresh token.

The service then:

- stores both encrypted at rest
- marks the `PendingAuthSession` as complete
- keeps the raw tokens inside the service boundary

The agent never sees the raw tokens.

#### 5. Agent Polls For Completion

The agent calls:

```text
oauth.get_authorization_status(auth_session_id)
```

Once the callback flow has completed, the service returns:

- `status: complete`
- `credential_handle`

#### 6. Authenticated MCP Tool Calls Via Handle

The agent calls:

```text
oauth.invoke(credential_handle, action, params)
```

The service:

- looks up the stored access token for that handle
- refreshes the token if needed
- performs the approved provider API call
- returns the result to the agent

The raw token never leaves the service boundary.

#### Built-In Safeguards

- PKCE binds the authorization code to the initiating client and blocks simple interception attacks.
- `state` validation on every callback blocks CSRF and confused-deputy failures.
- Short access-token lifetimes and refresh handling reduce the blast radius of token leakage.
- User revocation is naturally supported; the next refresh attempt fails and the credential can be marked unhealthy.
- The agent operates on handles, not tokens, so there is no normal path for the agent to exfiltrate the underlying OAuth credential.

## Service: `credential-service`

### Purpose

Provide delegated OAuth/OIDC credential management and bounded EVM signing without exposing provider client secrets, refresh tokens, long-lived bearer tokens, or EVM private keys to the agent.

### Alignment With Current Codebase

The current codebase mostly signs and submits **full EVM transactions** for on-chain actions.

- `executor-go` x402 settlement builds an EIP-1559 transaction, signs it with `types.SignTx`, and broadcasts it
- `claw-spawner` heartbeat similarly builds a full transaction after preparing the contract calldata
- generic message signing exists today primarily for heartbeat and registration attestation flows, not as the main pattern for ordinary on-chain actions

V1 should mirror that existing pattern. The EVM portion of this service should therefore focus on **full transaction execution** rather than a broad generic payload-signing API.

### Responsibilities

- Expose one MCP surface to the agent/harness
- Expose one HTTP API surface for browser callbacks and internal control-plane routes
- Register supported OAuth providers and their metadata
- Store provider app credentials
- Initiate authorization flows
- Track pending auth sessions
- Exchange auth codes for tokens
- Validate identity via `userinfo`/`whoami` or OIDC token claims
- Store delegated credentials encrypted at rest
- Refresh and revoke delegated credentials
- Execute approved provider actions on behalf of the user
- Hold or reference EVM keys via HSM/KMS/TEE-backed key material
- Build EVM transactions from structured requests
- Simulate transactions before signing when required
- Sign and broadcast EVM transactions
- Record auditable signing intent and outcome

### V1 Scope

- Concrete initial web2 target: **OAuth/OIDC providers**, with X/Twitter as the clearest initial example
- Support both:
  - OIDC-native providers
  - OAuth 2.0-only providers where we must perform the code exchange and then identify the user via provider APIs
- Return **credential handles**, not raw secrets
- Support a small allowlisted action surface per provider
- EVM transaction execution using full transaction build/sign/broadcast
- Optional simulation before signing
- Broadcast through approved RPC providers

### V1 Non-Scope

- Arbitrary third-party HTTP proxying
- Arbitrary provider onboarding by end users
- Returning plaintext refresh tokens, client secrets, or private keys
- Generic API-key storage for services like OpenRouter
- Preconfigured signing policy profiles such as contract allowlists, method allowlists, or spend-limit handles
- Generic `sign_message` or arbitrary payload-signing endpoints
- Returning signed but unbroadcast transactions as a primary v1 flow

### External Inspiration

Turnkey is a useful reference for:

- treating provider credentials as first-class stored objects
- storing encrypted client secrets
- distinguishing between provider metadata and delegated end-user credentials
- supporting OAuth 2.0-only providers via a brokered server-side exchange
- optionally returning encrypted tokens only when there is a specific secure recipient

We should copy the shape of that system more than the exact API.

### Interface Sketch

### MCP tools

- `oauth.begin_authorization`
  - input: `provider`, `user_ref`, `requested_scopes`, `redirect_context`
  - output: `auth_session_id`, `authorization_url`, `expires_at`
- `oauth.get_authorization_status`
  - input: `auth_session_id`
  - output: `pending | complete | failed`, optional `credential_handle`
- `oauth.invoke`
  - input: `credential_handle`, `action`, `params`, `idempotency_key`
  - output: provider action result
- `oauth.revoke_credential`
  - input: `credential_handle`
  - output: revocation status
- `oauth.describe_credential`
  - input: `credential_handle`
  - output: provider, subject, granted scopes, expiry, status
- `evm.get_address`
  - input: `signer_id`, `chain_id`
  - output: address
- `evm.send_transaction`
  - input: `signer_id`, `chain_id`, `transaction`, `idempotency_key`
  - output: `tx_hash`, optional simulation summary

### Internal HTTP endpoints

- `POST /oauth/providers`
- `POST /oauth/authorize/start`
- `GET /oauth/callback/:provider`
- `GET /oauth/sessions/:id`
- `POST /oauth/credentials/:id/invoke`
- `POST /oauth/credentials/:id/revoke`
- `POST /signers/:id/send-transaction`
- `GET /signers/:id/address`

### Data Model

### Signer

- `signer_id`
- `user_ref`
- `key_ref`
- `curve`
- `address`
- `allowed_chains`
- `simulation_required`
- `broadcast_allowed`
- `created_at`

### SigningRequest

- `request_id`
- `signer_id`
- `chain_id`
- `tx_hash_pre_sign`
- `idempotency_key`
- `decision`
- `decision_reason`
- `created_at`

### ProviderCredential

- `provider_credential_id`
- `provider`
- `client_id`
- `encrypted_client_secret`
- `redirect_uris`
- `allowed_scopes`
- `created_at`
- `updated_at`

### PendingAuthSession

- `auth_session_id`
- `provider`
- `user_ref`
- `state`
- `pkce_verifier`
- `requested_scopes`
- `redirect_uri`
- `expires_at`
- `status`

### DelegatedOAuthCredential

- `credential_handle`
- `provider`
- `provider_subject`
- `provider_user_ref`
- `granted_scopes`
- `encrypted_access_token`
- `encrypted_refresh_token`
- `access_token_expires_at`
- `refresh_state`
- `revoked_at`
- `created_at`
- `updated_at`

### Security Model

- Provider client secrets are encrypted at rest with service-managed envelope encryption backed by KMS/HSM/TEE key material.
- Refresh tokens are never exposed to MCP callers.
- Access tokens are not returned in plaintext in the normal flow.
- Private keys never leave the signer boundary.
- Every request is tied to:
  - authenticated MCP caller
  - user reference
  - signer
  - idempotency key
- OAuth provider actions are constrained by:
  - provider allowlist
  - scope allowlist
  - action allowlist
  - per-user credential ownership
  - per-agent session authorization
- All callback endpoints validate `state`.
- PKCE is required where provider supports it.
- Signer ownership and basic request validation happen before signing.
- `send_transaction` should default to simulate-then-sign-then-broadcast.
- Network egress is limited to approved OAuth providers and approved RPC endpoints.
- High-risk chains, contracts, or methods can require explicit human approval later, but that is not required for the base design.
- The service emits immutable audit events for every auth start, completion, refresh, invoke, revoke, sign, send, and denial.

### Internal Module Boundaries

Even though this is one service, it should have separate internal modules for:

- MCP server plumbing
- service authn/authz
- OAuth provider integration
- EVM signing
- envelope encryption helpers
- audit event emission
- idempotency handling
- structured error types

The runtime process is shared, but token storage and signing-key metadata should remain logically separated in the data model.

## Authorization Model

Each MCP request should carry a short-lived service credential representing:

- `agent_run_id`
- `agent_id`
- `user_ref`
- `session_id`
- expiry

The backend service must still evaluate whether that caller is allowed to use the requested `credential_handle` or `signer_id`.

Recommended checks on every call:

1. Is the MCP caller authenticated?
2. Is the token/session still valid?
3. Is the caller bound to the same `user_ref` as the credential or signer?
4. Is the requested action allowed for this tool and handle?
5. Is the request inside configured quotas and TTL bounds?

## Authentication

For the near-term authentication path, the service should **re-use the existing chain-based authentication code from `ritual-go-common`** and verify executors the same way the current vLLM proxy pattern does.

Concretely, that means:

- authenticate the calling executor using the existing Ritual executor auth flow rather than inventing a new service-specific scheme
- verify the executor against on-chain registry state using the shared `ritual-go-common` primitives already used across Ritual services
- treat executor identity as the authenticated caller identity until agent identity is stable enough to rely on directly

This keeps the service aligned with the rest of the stack and avoids introducing a parallel authentication system for credential access.

### Future Authentication Path

Once we have a stable notion of agent identity, the service can support a more direct caller authentication mode:

- the request is signed by the agent's primary account key
- the service verifies that signature directly
- the verified primary account identity becomes the caller identity for authorization and audit

At that point, executor-authenticated access can remain as a compatibility path, but the cleaner long-term model is to authorize based on the agent's own stable primary account identity rather than only the hosting executor.

## Observability

The service should emit:

- request ID
- agent run ID
- user ref
- provider or chain ID
- tool/action name
- allow/deny outcome
- denial reason class
- latency

The service should avoid logging:

- plaintext access tokens
- refresh tokens
- client secrets
- raw private keys
- full transaction payloads when they may contain sensitive calldata unless explicitly redacted

## Sad Paths And How To Bound Them

### Cross-Cutting Sad Paths

| Sad path | Risk | Bound |
|----------|------|-------|
| Agent bypasses the service entirely | Design is unused | Explicitly out of scope here; must be handled in harness/orchestration/model-side adherence work |
| MCP caller token is stolen | Unauthorized service use | Very short session TTL, audience binding, mTLS inside infra, revoke-on-run-end |
| Service outage | Agents blocked from sensitive actions | Fail closed, expose health, make outages observable, no fallback to raw secrets on agent |
| Duplicate requests due to retries | Double side effects | Require idempotency keys for all mutating actions |
| Audit log pipeline is down | Loss of traceability | Local durable queue with bounded backpressure; fail closed only for high-risk actions if queue overflows |
| Database unavailable | Inability to resolve signer or credential state | Fail closed for sign/invoke; do not cache secrets client-side |

### OAuth Sad Paths

| Sad path | Risk | Bound |
|----------|------|-------|
| Provider client secret misconfigured | All auth attempts fail | Provider health check and startup validation; bounded to provider, not whole service |
| Callback `state` mismatch | CSRF or confused-deputy risk | Reject callback, expire session, require restart |
| PKCE verifier lost | Auth code unusable | Store verifier with auth session and TTL |
| Auth code replay | Token theft | One-time auth session state, mark consumed atomically |
| Provider token endpoint unavailable | Login stalls | Short retries with absolute timeout; surface `pending_failed` not indefinite hang |
| Provider returns broader scopes than expected | Over-privileged credential | Intersect granted scopes with allowlist and reject unexpected scope expansion |
| Provider returns no refresh token | Credential quickly expires | Mark credential as non-refreshable and force re-auth |
| Refresh token revoked or expired | Credential silently degrades | Track refresh failures, mark credential unhealthy after bounded retries |
| Provider rate limits requests | Agent loops or degraded UX | Per-provider concurrency/rate limits and exponential backoff |
| Arbitrary API proxying becomes exfil path | Token misuse | Do not support arbitrary outbound requests in v1; only allowlisted provider actions |
| Provider identity is ambiguous across clients | User account fragmentation | Standardize one client ID per provider/app surface where identity continuity matters |
| Callback replay after completion | Duplicate credential creation | Persist final auth session state and reject second completion |
| User abandons browser flow | Leaked pending sessions | TTL and garbage collection on `PendingAuthSession` |
| Token accidentally returned to agent logs | Secret exfiltration | Default to handle-based invocation only; sensitive fields redacted everywhere |

### EVM Sad Paths

| Sad path | Risk | Bound |
|----------|------|-------|
| Malformed transaction request | Undefined signer behavior | Strict schema validation before signing |
| Unsupported chain ID | Wrong-chain signing | Explicit allowlist on the signer record |
| Nonce drift between simulation and broadcast | Failed or unexpected tx | Keep simulation window short, refresh nonce before sign, classify as retriable failure |
| RPC returns stale state | Bad simulation | Approved RPC set, optional quorum/read redundancy for critical flows |
| Agent retries same send | Duplicate submission | Idempotency keys persisted with request outcome |
| Signer key unavailable | Hard failure | Bound to signer; fail closed, no key export fallback |
| Chain reorg after simulation | Unexpected final state | Simulation is advisory; record pre-state and surface reorg-class errors separately |
| Broadcast succeeds but response is lost | Uncertain outcome | Persist signed raw tx and lookup by tx hash/idempotency key |
| Gas estimates spike after simulation | Failed tx or overspend | Service-side max fee / gas limits; optionally require caller-supplied fee bounds |
| Service receives enormous calldata | Resource exhaustion | Max request size, parse limits, bounded simulation concurrency |

## Bounding Principles

Across the service, the design should follow these bounding rules:

1. **No plaintext secret export by default.**
2. **Every side-effecting call must be idempotent.**
3. **Every credential and signing action must be attached to a specific user and agent session.**
4. **Every external dependency is allowlisted.**
5. **Every pending workflow has a TTL and terminal failure state.**
6. **Every denial is explicit and auditable.**
7. **If signer, credential, or storage state cannot be resolved, fail closed.**

## Build vs Buy

This design resembles Turnkey in shape.

That does not force a buy decision, but it does suggest a good evaluation frame:

- If we build, we should copy the separation between provider credential objects, delegated credential objects, encrypted storage, and brokered OAuth 2.0-only flows.
- If we buy, the likely fit is stronger on the OAuth side than on the agent-specific adherence side.
- Building our own OAuth infrastructure all the way down is likely materially more complex than adding the EVM signing routes to the same service.

## Open Questions

1. Which exact providers are in v1: X only, X plus Discord, or a broader OIDC set?
2. Do we ever need to return encrypted bearer tokens to another trusted service, or can all provider use stay inside `credential-service`?
3. Is OpenRouter actually in scope for this system, or is it a separate generic API-key custody problem?
4. Do we want the services in TEEs from day one, or only on otherwise hardened infra initially?
5. What is the source of truth for `user_ref` and MCP caller identity?

## Recommended V1 Decision

Build the first version as one `credential-service` with:

- OAuth/OIDC delegation with handle-based invocation
- signer-based EVM transaction execution using full tx build/sign/broadcast
- one MCP surface
- one HTTP API surface for callbacks and internal control routes
- no generic API-key vault yet
- no preconfigured signing-policy handle system yet
- no generic payload-signing or `sign_message` API yet
- no attempt to solve adherence in the service design

That is the smallest design that covers the top-priority credential flow and keeps the architecture bounded while avoiding extra service split complexity in v1.

## Future Phases

The following can be added in later phases once the base service is stable:

- `sign_transaction` for workflows that need a signed-but-unbroadcast tx
- `sign_message` or other attestation-style payload-signing endpoints
- preconfigured signing-policy handles or authorization profiles
- contract and method allowlists per signer
- spend limits, rate limits, and daily budget enforcement
- explicit human approval gates for high-risk signing actions
- richer signer policy composition beyond basic signer ownership and chain allowlists
