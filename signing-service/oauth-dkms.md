# OAuth integration for dKMS

**Status:** Draft (planning)  
**Date:** 2026-04-06  
**Related:** [credential-services-design.md](./credential-services-design.md) (OAuth / MCP / policy), [dkms-wallet-signing-integration.md](./dkms-wallet-signing-integration.md) (dKMS endpoints, executor flows)

## Purpose

This document scopes **adding OAuth (OIDC-style) concerns to the dKMS trust boundary**: how a **human-proven identity** (or delegated provider session) can gate or augment **dKMS operations** (`get_key`, `sign_transaction`, `get_address`, etc.) without collapsing OAuth into the same surface as TEE mTLS.

It is **not** a full OAuth provider design; it assumes we integrate with existing IdPs / social OAuth providers where needed, consistent with the credential-service direction.

**Storage direction (decided in plan):** OAuth **application** secrets (e.g. client secret) are **encrypted to a dKMS public key** and posted to a **smart contract** so the chain provides **replicated DA**; dKMS **decrypts in the TEE** when needed, reusing patterns from the existing **encrypted secrets** workflows elsewhere in the stack.

---

## Problem statement

Today, dKMS primarily trusts:

- **Executor identity:** mTLS client cert + on-chain **TEEServiceRegistry** (capability checks, attestation).
- **Key semantics:** `(keyId / owner address, index, format)` as the stable wallet identity for signing.

That model does not, by itself, answer:

- **Who is allowed to authorize use of keys tied to a given on-chain owner?** (Especially when the “owner” is a contract, a shared account, or recovery is required.)
- **When must a human re-confirm** high-risk actions (new executor, new index, large spend policy)?
- **How do we bind OAuth “login as user@provider”** to **“this chain address owns these keys in dKMS”** without exporting raw keys to browsers or agents?

OAuth is the usual tool for **user consent and refreshable delegation** at web scale; dKMS is the tool for **TEE-backed signing**. This doc is where those two meet.

---

## Goals

1. **Define authorization layers** clearly: transport (mTLS), registry (executor), **user/session** (OAuth), and optional **policy** (credential-service or dKMS-local).
2. **Prefer additive APIs** on dKMS (same principle as wallet-signing doc): new routes or headers for OAuth-bound sessions rather than breaking `POST /v1/get_key` for existing callers.
3. **Reuse the encrypted-secrets mental model** already used elsewhere in the stack (e.g. executor **delegated secrets** / encrypted payloads to a known recipient): users **seal** OAuth app credentials to a **dKMS public key**; **plaintext client secrets never sit in a single central DB** as the only copy—see **§Chain-backed OAuth secrets** below.
4. **Make binding explicit:** document how **OIDC `sub` + issuer** (or provider account id) maps to **owner `keyId`** / wallet identity, and what happens on mismatch or account merge.

---

## Chain-backed OAuth secrets (planned direction)

This is the **preferred plan** for where OAuth **client secrets** (and related app credentials) live, and how **dKMS** obtains them without becoming the sole replication point.

### dKMS public key

- dKMS exposes a **public key** (exact algorithm TBD: e.g. X25519 for ECIES-style sealing, or RSA-OAEP, or a hybrid aligned with existing **encrypted secrets** crypto in the repo).
- Users (or tooling) **encrypt** OAuth client credentials **to that public key** before anything hits the chain.
- Only the **dKMS TEE** (holding the matching private key) can **decrypt** for use at runtime (token exchange, refresh flows, etc.).

### Smart contract as DA for ciphertext

- Users **post ciphertext** (and minimal metadata: provider id, version, optional key id) to a **smart contract**—calldata, contract storage, or an approved L2/blob pattern depending on cost and availability requirements.
- **Replication / availability:** the chain acts as **data availability** for the encrypted blobs. Any **honest dKMS replica** that follows the chain can **read the same ciphertext** and decrypt with the dKMS private key when it needs to act. No reliance on a single operator’s disk for “the” copy of the encrypted secret.
- This **does not** put plaintext on-chain—only **encrypted** material is public to observers.

### Reuse of existing encrypted-secrets workflow

- Align **envelope format**, **key versioning**, and **owner authorization** patterns with the **encrypted secrets** flows already used in the product (e.g. how executors and users reason about “encrypt to X, submit Y”).
- Where helpful, the **same UX** can apply: user proves ownership (wallet tx), posts sealed payload, dKMS later consumes it—differing only in that the **recipient** of the encryption is **dKMS** and the **durability** layer is **on-chain** rather than off-chain storage only.

### Flow (sketch)

```text
  User / tool ──encrypt to dKMS pubkey──► ciphertext
       │
       └── tx ──► Smart contract (DA: replicated ciphertext + metadata)
                         │
                         │  read + decrypt inside TEE
                         v
                    dKMS ──► OAuth token exchange / refresh (uses decrypted client secret)
```

### Why chain DA here

| Goal | How this helps |
|------|----------------|
| **Replication** | Every dKMS instance that can read chain state + hold the private key sees the **same** sealed secret. |
| **Auditability** | Updates are **on-chain events** (who posted, when, which version)—without revealing plaintext. |
| **No single DB** | Avoids “credential-service is the only place ciphertext exists” if we want **dKMS-first** consumption. |

### New design work

- **Contract:** permissions (who may post/update for a given owner), versioning, revocation (e.g. mark a blob invalid without deleting history), gas and chain choice.
- **Key rotation:** dKMS pubkey rotation implies **re-wrap** or **multi-key** ciphertext support so old blobs remain decryptable during migration.
- **Threat model:** ciphertext is **public**; security rests on **dKMS private key** protection and **mTLS/registry** for who may trigger use of those secrets.

## Non-goals (v1)

- Replacing mTLS + registry verification for **executor → dKMS** transport trust.
- Implementing a **public OAuth authorization server** from scratch (use hosted IdP / credential-service flows).
- Solving **every** provider’s OAuth quirks inside dKMS (delegate to credential-service where possible).
- **Arbitrary API-key custody** (see credential-services-design).

---

## Conceptual model

```text
  Human ──browser OAuth──► IdP / credential-service
                              │
                              │  short-lived or step-up token
                              ▼
  Executor (TEE) ──mTLS──► dKMS ──► signing / get_key
       ▲                        ▲
       │                        └── reads: on-chain ciphertext (OAuth app secrets)
       └── policy: "this OAuth session may request index N for owner 0x…"

  User ──encrypt to dKMS pubkey──► Smart contract (DA) ──► dKMS decrypts when needed
```

**Separation of concerns:**

| Concern | Typical owner |
|--------|----------------|
| “Is this executor a registered TEE that may call dKMS?” | Registry + mTLS |
| “Did a human consent for *this* wallet operation?” | OAuth / credential-service |
| “What bytes are we signing?” | Executor (tx construction) + dKMS (HSM/TEE sign) |
| “Where do **OAuth client secrets** live, replicated?” | **Encrypted** blobs on-chain (see §Chain-backed OAuth secrets); dKMS holds decryption key |

---

## Runtime flow: provision → 401 → dKMS → retry

This section turns the high-level idea into a **concrete sequence**. The steps below match the mental model you described, with terminology tightened so we do **not** ship **client secrets** to agents.

### Terminology (important)

| Term | Who holds it | Agent sees it? |
|------|----------------|----------------|
| **Client ID** | Public OAuth app identifier | **Yes** (often harmless to expose) |
| **Client secret** | Confidential; used at token endpoint | **No** — stays in dKMS TEE after decrypt from chain |
| **Access token** (OAuth 2.0) | Short-lived bearer for APIs | **Yes** — this is what the agent retries with |
| **OIDC ID token** | JWT about the user/session (when using OIDC) | **Sometimes** — depends on provider flow; not the same as client secret |

**Rule:** After step 3, the agent receives an **access token** (and optional OIDC artifacts), **not** the **client secret**.

### When this linear flow applies

- Best fit: **machine-oriented** token acquisition (e.g. **OAuth 2.0 client credentials** against the provider, or **refresh token** rotation where the **refresh token** was obtained earlier and also stored sealed-on-chain or in credential-service—not shown here).
- **User login** flows (authorization code + browser) insert extra steps: redirect to IdP, user consent, then callback—dKMS or credential-service completes the code exchange. The **401 → get token → retry** pattern still applies to the **agent → resource** leg once a **user delegation** exists.

### Step 0 — User provisions OAuth app material (once per app / rotation)

**Actor:** wallet owner (or admin tooling).

1. Create or select an OAuth/OIDC **application** at the provider; obtain **client_id** and **client_secret** (and any provider-specific fields: token endpoint URL, issuer, scopes, PKCE requirements, etc.).
2. Build a **plaintext bundle** for dKMS to use later at the token endpoint—at minimum **client_id** + **client_secret**; typically also **token endpoint**, **issuer** or provider id, **default scopes**, and optional **redirect URI** metadata if flows need it.
3. **Encrypt** the bundle to the **dKMS public key** (envelope format TBD).
4. **Submit** the ciphertext (+ indexing metadata: owner, provider key, version) to the **smart contract** so it is **DA-replicated** (see [§Chain-backed OAuth secrets](#chain-backed-oauth-secrets-planned-direction)).

Until step 0 completes for a given `(owner, provider)`, dKMS cannot mint tokens for that app.

### Step 1 — Agent calls protected endpoint, receives **401 Unauthorized**

**Actor:** agent (via harness / MCP / HTTP).

1. Agent calls a **resource** (HTTP API, MCP tool backend, etc.) that requires OAuth.
2. Server responds **401** (or **403** with `insufficient_scope`—product decision). Response should include a **machine-readable** hint: e.g. `WWW-Authenticate: Bearer`, `resource_metadata` URL, or application JSON with `error: "invalid_token"` / `"login_required"` so the client knows to **obtain a bearer token** rather than guessing.

This mirrors common **OAuth-protected resource** behavior: no valid `Authorization: Bearer` header yet.

### Step 2 — Agent requests an **access token** from dKMS (logical; transport may be brokered)

**Actor:** agent → **dKMS** (directly or via **executor / credential-service**).

1. Agent sends a **token request** identifying:
   - **Which owner** (on-chain identity / `keyId`) the OAuth app belongs to,
   - **Which provider** (or ciphertext pointer / version on-chain),
   - **What for** (scopes, audience, or opaque “intent” string tied to the 401’d resource).
2. **Transport trust** still follows deployment rules: often **executor mTLS** to dKMS, or **credential-service** first—see [integration patterns](#integration-patterns-options-to-decide). The doc’s **logical** step is “agent causes a dKMS token issuance request.”

### Step 3 — dKMS **mints** usable credentials using the **client secret** (inside TEE only)

**Actor:** dKMS.

1. Load **ciphertext** from chain (or cache), **decrypt** with dKMS private key → recover **client_id**, **client_secret**, endpoints.
2. Call the provider’s **OAuth token endpoint** (HTTPS from TEE):
   - e.g. **client credentials** grant with `client_id` / `client_secret`, or
   - **refresh grant** if a refresh token is part of the sealed bundle or stored elsewhere under policy.
3. Provider returns **access_token** (+ optional **expires_in**, **token_type**, OIDC **id_token**).
4. dKMS returns to the caller **only non-secret artifacts**: typically **access_token**, **expiry**, and optionally **id_token**—**never** the client secret.

### Step 4 — Agent retries the original request with **Bearer** access token

**Actor:** agent.

1. Agent repeats the call from step 1 with header: `Authorization: Bearer <access_token>`.
2. Resource validates token (issuer signature, audience, scopes) or accepts as opaque if it trusts the provider’s API.
3. Optional: **cache** the access token in the harness until `expires_in` to avoid hammering dKMS; on expiry, repeat steps 2–4 (refresh path TBD).

### ASCII summary

```text
  [0] Owner: encrypt(client_id, client_secret, …) → chain (DA)

  [1] Agent → Resource     → 401 (need Bearer)
  [2] Agent → dKMS         → "give me token for owner+provider+scope"
  [3] dKMS: decrypt chain; token endpoint HTTPS; access_token
  [4] Agent → Resource     → 200 (Authorization: Bearer access_token)
```

### Does this sequence “make sense”?

**Yes**, with the corrections above: step 4 is **access token**, not **client secret**. The **401** is a clean trigger for **lazy token fetch**; step 0 ensures dKMS has **confidential** material without a single off-chain DB. Gaps to close in implementation: **exact dKMS HTTP API** for step 2, **scope / audience** negotiation from the 401 response, and **rate limits** on token issuance.

---

## Integration patterns (options to decide)

These are **mutually combinable** in later phases; v1 should pick one primary path.

### A. OAuth only at **credential-service**; dKMS unchanged

- User completes OAuth in browser; credential-service issues **internal session** to the harness/agent.
- When chain signing is needed, **credential-service** (or executor on behalf of user) still calls dKMS with **existing** executor mTLS—OAuth never hits dKMS directly.
- **Pros:** Smallest dKMS change; aligns with [credential-services-design.md](./credential-services-design.md).
- **Cons:** Centralizes trust in credential-service; dKMS cannot enforce user-level policy without that service.

### B. **Step-up token** presented to dKMS (OAuth-derived)

- After OAuth, user (or credential-service) obtains a **signed JWT or macaroon** that dKMS verifies (JWKS, audience, expiry) before `sign_transaction` / sensitive `get_key` paths.
- Executor mTLS remains required; OAuth material is an **additional** header or body field.
- **Pros:** dKMS can log and enforce per-request user consent; clearer audit (“which OIDC subject approved this sign?”).
- **Cons:** Key management for verifying tokens inside dKMS TEE; rotation and clock skew handling.

### C. **Owner binding registry** (off-chain or on-chain pointer)

- Store `hash(issuer, sub) → allowed keyId` (or Merkle root) updated only after OAuth proof.
- dKMS checks binding before signing for **non-custodial** workflows where owner address must match OAuth identity.
- **Pros:** Strong coupling between “login” and “wallet.”
- **Cons:** Operational overhead; privacy considerations for storing provider ids.

### D. **On-chain encrypted OAuth app secrets + dKMS public key** (preferred for **secret durability**)

- **Full detail:** [§Chain-backed OAuth secrets](#chain-backed-oauth-secrets-planned-direction) above.
- **Summary:** Users seal provider **client_id / client_secret** (or equivalent) to the **dKMS public key**, post ciphertext to a **smart contract**, and dKMS **fetches and decrypts** inside the TEE when it must run token exchange or refresh. **Chain = DA** so every replica sees the same sealed material.
- **Orthogonal to A–C:** you can still use **credential-service** for browser OAuth UX while **storing** app credentials on-chain encrypted to dKMS, or use **step-up tokens** (B) for per-request approval on top of this storage layer.

---

## Security considerations

- **On-chain ciphertext is public:** assume world-readable; **only** dKMS’s private key material must provide confidentiality. Size and metadata leak **which** provider/app version a user configured—evaluate privacy vs audit tradeoffs.
- **Token leakage:** OAuth access tokens must not be logged by dKMS in plaintext; prefer opaque step-up tokens with short TTL.
- **Confused deputy:** If both executor mTLS and OAuth are present, dKMS must validate that the **OAuth identity is authorized for the `keyId` in the request**—not only that some user consented.
- **Replay:** step-up tokens must be **single-use or narrowly scoped** (e.g. bind to tx hash or request id) for high-risk operations.
- **Revocation:** OAuth refresh revocation should **invalidate** future step-up tokens; define whether dKMS checks revocation online or relies on short TTL only.

---

## Open questions

1. **Which operations require OAuth** vs executor-only? (e.g. `get_address` public-ish vs `sign_transaction` always sensitive.)
2. **Is `keyId` always an EOA address**, or do we need OAuth for **smart wallet / session key** models?
3. **Do we require OAuth for all agent-mediated signing**, or only when a **browser user** is in the loop?
4. **Deployment:** Is dKMS ever called **without** executor-go (direct from credential-service)? That changes token transport.
5. **Compliance / audit:** What identity fields are retained (issuer, `sub`, hashed only)?
6. **Contract design:** one contract vs per-network deployments; **update** vs **append-only** history; maximum blob size; **revocation** semantics.
7. **dKMS pubkey distribution:** on-chain registry entry, well-known URL, or both; **rotation** cadence and overlap with multi-key decrypt.
8. **Interaction with [credential-services-design.md](./credential-services-design.md):** does credential-service hold **no** provider client secrets and only orchestrate UX, with **all** long-lived sealed material on-chain—or a hybrid?

---

## Next steps

1. Specify **dKMS public-key** format and publishing channel; align envelope crypto with existing **encrypted secrets** implementations.
2. Draft **smart contract** interface for posting encrypted OAuth credentials (events, access control, versioning).
3. Choose **pattern A/B/C** for **session / consent** and combine with **pattern D** for **where ciphertext lives** (not mutually exclusive).
4. Align with **dkms** repo on **chain read + decrypt** path and additive HTTP if needed (see [dkms-wallet-signing-integration.md](./dkms-wallet-signing-integration.md)).
5. Prototype **encrypt → post → dKMS read/decrypt** on a testnet before production OAuth apps.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-06 | Initial draft |
| 2026-04-06 | Added **chain-backed OAuth secrets**: dKMS public key, encrypted client secrets on-chain as DA, reuse of encrypted-secrets workflow; pattern **D**; diagram and open questions updated |
| 2026-04-06 | Added **Runtime flow: provision → 401 → dKMS → retry** (steps 0–4, access token vs client secret, when user-login flows differ) |
