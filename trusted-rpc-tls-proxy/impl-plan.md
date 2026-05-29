## Implementation Plan

1. `ritual-go-common`: add a reusable RPC dial package
   Objective: Create one shared place for plain and pinned chain RPC dialing so TEE
   services do not implement pinning locally.
   Change: Add a small common package that parses an optional static SPKI cert hash,
   builds the `mtls.NewCertPinningVerifier` / `NewClientTLSConfigWithPinning`
   transport, dials HTTP JSON-RPC through `ethclient.DialOptions`, and exposes a
   reusable TLS config for WS callers. Keep pinning disabled when no hash is supplied.
   Constraints: Reuse only the static pinning primitive; no registry lookup, refresh
   callback, TEE-address extraction, or client cert. Accept `0x`-prefixed and
   unprefixed hashes, normalize as `0x`-prefixed, reject malformed/all-zero hashes.
   Verification: Unit tests cover hash parsing, plain HTTP dial behavior, accepted
   pinned HTTPS, rejected wrong cert hash, and WS TLS config construction.

2. `ritual-go-common`: route registry clients through the shared dial package
   Objective: Preserve existing registry behavior while creating the durable seam for
   trusted read RPCs.
   Change: Refactor `registry.NewClient` and `registry.NewReadOnlyClient` to use the
   new common dialer for their default plain behavior, and add explicit constructors or
   options for pinned read clients and split read/write clients where needed.
   Constraints: Existing callers without trusted-read config must continue compiling
   and dialing the same URLs. Write methods must keep using the write/plain client;
   read methods must be able to use a pinned read client.
   Verification: Existing `ritual-go-common/registry` tests pass, plus focused tests
   prove read calls can use a different underlying endpoint than write calls.

3. `dkms`: split trusted reads from plain registration writes
   Objective: Make dKMS registry reads use the pinned trusted endpoint without changing
   its signed registration write behavior.
   Change: Add `TRUSTED_READ_RPC_URL` and `RPC_CERT_HASH` config fields; keep `RPC_URL`
   as the plain write/registration URL. Initialize the server read-only registry client
   with the trusted read config, and registration with the existing write URL.
   Constraints: Production mode must require trusted-read auth on; dev/unit tests may
   disable it. Preserve existing recovery-peer pinning semantics.
   Verification: dKMS config tests cover missing/invalid trusted-read settings in
   production, dev fallback behavior, and both hash formats. Server/registration tests
   show reads and writes consume the intended URLs.

4. `executor-go-internal`: wire trusted reads while preserving multicast writes
   Objective: Cover executor chain reads/subscriptions without weakening existing
   result-submission fanout.
   Change: Add trusted read URL/hash config for HTTP and WS read paths. Keep
   `FANOUT_URLS`/`MULTICAST_URLS` as the write/result-submission endpoints. Route
   registry discovery, contract event HTTP reads, and WS subscription dialing through
   the shared common helpers.
   Constraints: Executor should mostly wire config into common helpers; pinning logic
   should not be duplicated in executor packages. Existing multicast behavior remains
   unchanged.
   Verification: Config tests prove multicast URLs remain required for writes while
   trusted read settings are required in production. Focused monitor/discovery tests
   cover pinned HTTP and WS rejection on wrong cert.

5. Other Go TEE services: standardize trusted read config
   Objective: Apply the same authenticated-read boundary to vLLM proxy, streaming,
   telemetry, and claw-spawner agent-sidecar paths that read registry or chain state.
   Change: Add `TRUSTED_READ_RPC_URL` and `RPC_CERT_HASH` where those services
   currently use `REGISTRY_RPC_URL`, `TEE_SERVICE_REGISTRY_RPC_URL`, or
   `CHAIN_RPC_URL` for trusted reads. Preserve each service's current single write URL
   for registration or other signed writes.
   Constraints: Avoid per-service pinning logic; use the common helper. Keep legacy
   env names only as dev/backward-compatible fallback when production auth is off.
   Verification: Each service has config tests for production required settings,
   dev fallback, and successful construction of pinned registry/read clients.

6. `ritual-node-internal`: make local-network TLS proxy self-contained
   Objective: Local-network startup should generate or persist proxy cert material,
   mount it into an off-the-shelf TLS terminator, and wire the pinned hash into TEE
   services without relying on external deploy tooling.
   Change: Add local-network cert/key generation or reuse, add a TCP/stream TLS
   terminator service in front of reth if nginx stream or stunnel fits cleanly, expose
   trusted HTTP and WSS endpoints, and inject `TRUSTED_READ_RPC_URL`/`RPC_CERT_HASH`.
   Constraints: Prefer off-the-shelf config only if it is clean; if neither nginx stream
   nor stunnel fits HTTP+WS pass-through with stable mounting, stop and revisit the
   terminator choice. Keep reth untouched.
   Verification: A local network starts from `ritual-node-internal`; TEE services read
   through the trusted endpoint; replacing the cert/hash causes read startup or first
   read to fail.

7. `chain-deployment-infra`: mirror the trusted-read contract for deploy scripts
   Objective: Production and sim deploys should wire the same trusted-read contract as
   local-network.
   Change: Update relevant deploy/config generation scripts to provision or mount the
   proxy cert material, configure the TLS terminator, emit trusted read URLs and cert
   hashes, and preserve existing write endpoints including executor multicast lists.
   Constraints: Local correctness remains owned by `ritual-node-internal`; deploy infra
   should reuse the same env contract rather than inventing another one.
   Verification: Dry-run or generated config review shows trusted read URLs/hashes on
   all TEE services, write URLs preserved, and no direct plain read URL in production
   TEE service envs.

8. Integration verification and negative tests
   Objective: Prove the end-to-end trust boundary works and fails closed.
   Change: Run focused unit tests in changed Go repos, then restart a local network and
   exercise dKMS/executor/vLLM/streaming registry reads through the pinned proxy.
   Constraints: Final verification must include both success against the real proxy and
   failure on a wrong cert hash or alternate TLS server.
   Verification: Test logs show accepted reads through the legitimate proxy, rejected
   reads for a mismatched SPKI hash, executor multicast writes still submit to all
   configured endpoints, and production-mode guards reject auth-off configs.

## Structural Simplification Check (implementation pass)

- The implementation plan keeps one shared client-side pinning mechanism in
  `ritual-go-common`; service repos only wire URLs/hashes and should not duplicate TLS
  verification logic.
- The read/write split follows the real trust boundary: trusted reads use
  `TRUSTED_READ_RPC_URL`/`RPC_CERT_HASH`; writes preserve existing topology, including
  executor multicast submission.
- The first two subtasks are prep/refactor work that create the seam before service
  behavior changes, reducing the risk of scattered `if trusted` branches.
- The server-side proxy remains config-only unless an off-the-shelf TCP terminator
  cannot cleanly satisfy HTTP and WS pass-through.
