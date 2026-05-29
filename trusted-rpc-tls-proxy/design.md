# Trusted RPC TLS Proxy — Design

Status: Phase 1 (design) complete. Ready for implementation planning.

## Context

### The current trust assumption

TEE services (all written in Go) read chain state through a "Trusted RPC" that is
configured purely by URL in the container environment:

- dKMS: `RPC_URL` (single URL), consumed via
  `registry.NewReadOnlyClient(cfg.RPCURL, cfg.RegistryAddress)` →
  `ethclient.Dial(rpcURL)` (`dkms/internal/config/config.go`, `dkms/internal/server/server.go`).
- Executor: `RPC_URLS` / `WS_URLS` plus `TEE_SERVICE_REGISTRY_RPC_URL`
  (`executor-go-internal/internal/config/config.go`), again via go-ethereum `ethclient`.
- Other TEE services (vLLM proxy, streaming, telemetry, heartbeat) get `*_RPC_URL`
  wired by `ritual-node-internal/configgen/docker.py` (e.g. `REGISTRY_RPC_URL`,
  `TEE_SERVICE_REGISTRY_RPC_URL`, `CHAIN_RPC_URL`), all plain `http://`.

  > TODO: The trusted-RPC env var name is inconsistent across services
  > (`RPC_URL`, `RPC_URLS`, `REGISTRY_RPC_URL`, `TEE_SERVICE_REGISTRY_RPC_URL`,
  > `CHAIN_RPC_URL`). Standardize on a single name `TRUSTED_READ_RPC_URL` for all of
  > these so the pinned-TLS endpoint + `RPC_CERT_HASH` are wired uniformly. Fold this
  > rename into the shared pinned-dial refactor (workstream 2) and the deployment
  > wiring (workstream 3).

The shared client is `ritual-go-common/registry.Client`, which dials with
`ethclient.Dial(rpcURL)` — plain HTTP, no transport authentication.

### The security gap

These chain reads are security-critical. The dKMS `handleGetKey` /`handleShareKey`
paths call `registryClient.GetService(...)` to decide whether a caller is a valid,
online, correctly-capable TEE before releasing key material. The executor uses the
same registry reads to discover and pin peer service certs.

Because transport is plain HTTP and the RPC endpoint is reachable only by IP/URL
with no server authentication, a malicious host (e.g. Phala) that controls
networking can:

- MitM the connection, or
- redirect the RPC URL to an attacker-controlled endpoint that returns forged
  registry responses (e.g. mark an attacker address as a `IsValid` executor with
  `HTTP_CALL` capability), causing dKMS to hand out keys.

### Reads need auth; writes do not

Only **reads** require an authenticated channel. A read (`eth_call` /
`GetService`, capability checks, cert-hash lookups) is a claim about chain state that
the client cannot independently verify, so a forged response is directly exploitable
— this is what the pinned proxy must protect.

**Writes** (e.g. submitting a registration tx via `RegisterDKMS` /
`RegisterExecutor` / `createTransactOpts`) are self-protecting: the tx is signed by
the TEE key, and its effect is validated by chain consensus. A malicious write RPC
can drop, delay, or reorder a submission (a liveness/censorship concern), but cannot
forge an accepted state change or extract secrets. So writes can continue over the
plain (unauthenticated) RPC.

Implication: the trust boundary is the **read** path, hence the
`TRUSTED_READ_RPC_URL` naming. `ritual-go-common/registry.Client` currently mixes
both reads (`GetService`, `GetCertPubKeyHash...`) and writes (`Register*`,
`MarkOffline`) on one dialed endpoint; the refactor should let the read path use the
pinned/authenticated endpoint while the write path may keep using a plain RPC URL.

### What already exists that we should reuse

The codebase already implements the one primitive this fix needs:
**static SHA256(SPKI) hash pinning of a self-signed server cert**. But `mtls`
bundles that primitive together with several heavier flows that we must NOT pull in.
Being explicit, because the existing call sites mix these concerns:

**The exact minimal client primitive we want (and nothing else):**

- `mtls.NewCertPinningVerifier(expectedHash)` with **no** refresh callback
  (`mtls/pinning.go`). `VerifyConnection` does only: compute
  `sha256.Sum256(serverCert.RawSubjectPublicKeyInfo)` and constant-time compare it to
  the baked-in `expectedHash`. No TEE-address extraction, no chain call.
- `mtls.NewClientTLSConfigWithPinning(PinningClientConfig{Verifier: verifier})` with
  **no** `ClientCert` → `InsecureSkipVerify: true` + that `VerifyConnection`, and no
  client certificate presented (server-auth only, not mTLS).

That's the whole client side: a static hash compare over TLS. The expected hash is
the baked-in `RPC_CERT_HASH`; there is no registry involvement on the read path.

**Steps in the existing `mtls` / recovery-peer flows we explicitly EXCLUDE:**

- On-chain cert-hash lookup: `NewClientTLSConfigWithVerifier` /
  `Manager.CreateClientTLSConfigWithVerifier` extract the server's TEE address from
  its cert and call `registry.GetCertPubKeyHashForAddress`. Not used here — the proxy
  is not a registered TEE and its hash is configured statically, not discovered.
- Refresh callback (`WithRefreshCallback`): would do a live registry lookup on
  mismatch. We pass none.
- TEE-address pinning: `keyshare/retriever.go::pinTLSConfigToPeer` /
  `ExtractTeeAddressFromCert` require a TEE address in the cert CN and compare it. The
  proxy cert has no meaningful TEE address; we pin the key hash only.
- Client-cert / mTLS: `Manager.CreateClientTLSConfig` presents the manager's own cert
  (`ClientConfig.ClientCert`). We present no client cert for reads.

**Server (proxy) side:** just a self-signed keypair; the pinned identity is
`sha256(SPKI)` (`mtls.ComputeCertPubKeyHash`, `cert.go`). `mtls.GenerateSelfSignedCert`
works but embeds a TEE address in the CN (`CertConfig.TeeAddress`) that is unused by
hash pinning, so the proxy can equally use a plain Go/`openssl` self-signed cert and
does not need `mtls.Manager` at all.

Net: reuse only `NewCertPinningVerifier` + `NewClientTLSConfigWithPinning` (no
callback, no client cert) and `ComputeCertPubKeyHash`. The minimal fix is: stand up a
TLS terminator in front of reth and dial it through this static pin.

### reth / nodebuilder feasibility (evaluated)

reth's RPC is built on jsonrpsee's HTTP server via `crates/rpc/rpc-builder`. There is
no TLS/rustls/certificate surface in `rpc-builder` (the only `https` hits in
`lib.rs` are doc-comment URLs) and no `--*-tls*` RPC args in node core. Adding TLS
termination inside reth would mean patching jsonrpsee server construction or the
reth RPC server builder. Given ritual-reth is a heavily-forked, upstream-merge-
sensitive codebase (per repo memory `ritual-reth/index.md`), adding a TLS feature
inside it is high-friction and a recurring merge cost.

Prior (high confidence): terminating TLS *outside* reth is the right call. The open
question is only whether the terminator is a small custom Go proxy or an
off-the-shelf TLS reverse proxy (see ambiguities).

Note: regardless of which terminator we pick, the **client-side change is
unavoidable** — go-ethereum's `ethclient.Dial` does not pin self-signed certs, so we
must dial via `ethclient.DialOptions(..., rpc.WithHTTPClient(customClient))` with a
pinning `tls.Config`. That client change lives in `ritual-go-common`.

## Design Plan

- Goal: Make every security-critical chain read from a TEE service run over an
  authenticated, encrypted channel whose server identity is pinned to a cert hash
  baked into the TEE image, eliminating host-level MitM / RPC-redirection forgery
  for the minimal-fix milestone. Success = a TEE service rejects any RPC server
  whose cert SPKI hash does not match the pinned value, and accepts the legitimate
  proxy; verified on local network.

- Main workstreams:
  1. **TLS terminator in front of reth** (likely a new repo): listens on a TLS
     port with a self-signed cert, reverse-proxies JSON-RPC to reth's local
     `http://` RPC, exposes the same endpoints as reth (transparent pass-through of
     `eth_call`, etc.). Publishes/derives the cert SPKI hash for baking into images.
  2. **Pinned RPC dial in `ritual-go-common`** (one shared helper): a single dial
     path that dials via `ethclient.DialOptions(ctx, url, rpc.WithHTTPClient(...))`
     where the HTTP client's transport uses
     `mtls.NewClientTLSConfigWithPinning(PinningClientConfig{Verifier:
     NewCertPinningVerifier(hash)})` — no refresh callback, no client cert. Used by
     `registry.Client` (`NewReadOnlyClient`/`NewClient`) and by executor RPC
     dialing — not duplicated per repo.
  3. **Config + deployment wiring**: new env (e.g. `RPC_URL=https://...` +
     `RPC_CERT_HASH=0x...`) in dKMS / executor / other consumers; production-mode
     validation (https + non-empty pinned hash); `configgen/docker.py` and deploy
     scripts (`gold_standard.sh`) emit the proxy service and the pinned env.
  4. **Cert provisioning + lifecycle**: how the proxy's keypair is generated/stored,
     how its hash reaches the TEE image env, and how rotation works.
  5. **Local-network integration test** via `ritual-node-internal`.

- Key decisions (proposed defaults, open ones tracked below):
  - **Full TLS encryption in all variants.** "Server-auth-only" below refers to the
    *authentication direction* (one-way, like every HTTPS site), NOT to dropping
    encryption. The channel is always encrypted with standard Go `crypto/tls`. mTLS
    (also requiring a client cert) is the thing we decline, because chain reads are
    public and the threat is *server* impersonation/MitM; requiring every TEE service
    to hold a registered client cert just to read adds deployment cost for no
    read-integrity gain.
  - **Server-cert verification model: DECIDED = A.a (self-signed + SPKI pin).** Full
    encryption + server auth via audited `crypto/tls`; client pins the baked-in
    `RPC_CERT_HASH`. Chosen over CA/hostname (A.b) because it keeps each network
    self-contained (no per-deployment DNS name or CA issuance/renewal), which suits
    `chain-deployment-infra` launching repeated/simultaneous sims, and keeps DNS out
    of the TEE security analysis entirely. See Baseline Decisions.
  - Keep reth untouched.

- Risks and dependencies:
  - **Cert provisioning chicken-and-egg**: if the proxy mints a fresh cert per
    start, the baked-in hash goes stale. Needs a persistent/deterministic keypair
    and a defined rotation story.
  - **Trust delegation, acknowledged**: this gives Ritual (proxy operator) the power
    to forge reads. This is the explicit shortcut vs. the light-client long-term
    plan; it removes the *host* from the trust set but not Ritual.
  - **Scope creep across services**: dKMS is the urgent path, but executor/vLLM/
    streaming rely on the same trusted reads. Doing only dKMS leaves a partial fix.
  - **WS path**: executor uses `WS_URLS` (`ws://`) for subscriptions; TLS-for-HTTP
    only does not cover WS unless we also terminate `wss://`.
  - **Client dial refactor blast radius**: changing `registry.Client` dialing
    touches every TEE service that imports `ritual-go-common/registry`.

## Structural Simplification Check (pre-implementation pass)

- Are we adding a second parallel path? The real risk is the **client RPC dial**: a
  pinned-TLS dial alongside the existing plain `ethclient.Dial`. Mitigation: add one
  shared pinned-dial helper in `ritual-go-common` and route all consumers through it
  (including the non-pinned/dev case via the same helper with pinning disabled),
  rather than `if https { ... } else { ... }` branches scattered per repo.
- Can a behavior-preserving prep refactor create a cleaner seam first? Yes: before
  adding pinning, refactor `registry.NewClient`/`NewReadOnlyClient` to dial through
  an injectable HTTP client / transport (no behavior change). Pinning then becomes a
  config of that seam. Recommend making this the first implementation step.
- Do we need a custom proxy at all, or does an off-the-shelf TLS terminator (nginx/
  caddy/stunnel) suffice on the server side? The server only needs to terminate TLS
  with a self-signed cert and pass JSON-RPC through; all the *pinning* logic is
  client-side. This is a genuine fork (see ambiguities) — a config-only terminator
  could avoid a whole new repo/binary.

## Baseline Decisions and Requirements

- **Fork A — server-cert verification: A.a (self-signed + SPKI hash pinning).**
  Client pins a baked-in `RPC_CERT_HASH` via `mtls.NewClientTLSConfigWithPinning`
  over a custom dial transport. No WebPKI, no DNS dependency. Rationale: keeps each
  network self-contained for repeated/simultaneous `chain-deployment-infra` sims, and
  removes DNS from the TEE security analysis. Accepted cost: baked-hash provisioning
  + rotation (stale hash breaks all reads) — handled in workstream 4 / ambiguity 3.
  Rejected A.b (CA-signed + hostname verify) despite less client code, because it adds
  a public DNS name + CA issuance/renewal per deployment and pulls WebPKI + DNS into
  the trust base.
- This confirms the "minimal primitive" section and the custom-dial transport in
  workstream 2 are in scope.

- **Scope = all TEE services** that do trusted chain reads (dKMS, executor, vLLM
  proxy, streaming, telemetry, claw-spawner agent-sidecar heartbeat). Not just dKMS.
  → the client change is a `ritual-go-common`-wide shared helper plus per-service
  dial-site wiring. (`ritual-halo-internal` is the Omni/Halo bridge, not a Ritual-chain
  registry reader — explicitly out of scope.)

- **Terminator = off-the-shelf if it works cleanly.** Use a TCP/stream TLS
  terminator (nginx `stream` module or stunnel) in front of reth rather than a new
  custom Go proxy binary, provided it supports HTTP and WS pass-through with stable
  cert mounting in the deploy stack. Rationale: zero custom server code to maintain,
  and TCP-level termination is protocol-agnostic so it covers HTTP-RPC and WS
  uniformly with one mechanism. If neither off-the-shelf option fits cleanly, revisit
  the terminator choice rather than forcing a brittle config.

- **WS is in scope.** The executor (and heartbeat) subscribe over `WS_URLS`
  (`ws://`); the fix must cover `wss://` + pinning, not just HTTP JSON-RPC. TCP-level
  termination handles this server-side; client-side, gorilla `websocket.Dialer`
  exposes `TLSClientConfig` directly, and go-ethereum WS dials must use reusable
  `ritual-go-common` helpers so TEE services mostly only wire URLs and hashes rather
  than owning pinning details locally.

- **Topology = single reth node runs the proxy for now.** One terminator, one cert,
  therefore a single pinned hash (no allowed-set / multi-hash config needed yet).

- **Server-auth-only (no client cert / no mTLS).** Confirmed.

- **Auth toggle: off-switch allowed, but ON by default on local-network.** A flag may
  disable read-path pinning for dev/unit tests, but `ritual-node-internal`
  local-network must default to auth ON, and production mode must hard-require it
  (production guard rejects auth-off, mirroring existing `TLS_ENABLED` guards).

- **Cert lifecycle location = `ritual-node-internal` for local network.**
  `ritual-node-internal` must be self-contained for local-network verification: it
  owns local cert/key generation or persistence, proxy cert mounting, and hash wiring
  into local TEE service envs. `chain-deployment-infra` can reuse the same contract for
  deploy scripts, but local correctness must not depend on external deploy tooling.

- **Hash format contract = accept both, canonicalize one.** Config should accept both
  `0x`-prefixed and unprefixed hex to reduce operator footguns, validate length and
  hex encoding strictly, and normalize internally/log output as `0x`-prefixed hex.

- **Read/write endpoint split = explicit trusted read URL plus existing write shape.**
  Security-critical reads should move to `TRUSTED_READ_RPC_URL` + `RPC_CERT_HASH`.
  Writes should stay plain and preserve each service's current write topology:
  executor keeps `FANOUT_URLS`/`MULTICAST_URLS` for multicast result submission, while
  services that already have one registration/write RPC can keep a single plain write
  URL. This avoids weakening executor's existing fanout behavior while making the
  authenticated-read boundary explicit across TEE services.

## Ambiguities To Resolve

- None.
