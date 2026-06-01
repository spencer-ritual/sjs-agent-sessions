## Implementation Plan

Status: implemented on `spencer/rpc-auth`. This file now records both the original
implementation plan and the deltas discovered while building and verifying it.

## Implemented PRs

- `ritual-go-common`: https://github.com/ritual-net/ritual-go-common/pull/58
- `executor-go-internal`: https://github.com/ritual-net/executor-go-internal/pull/174
- `dkms`: https://github.com/ritual-net/dkms/pull/32
- `ritual-streaming-service`: https://github.com/ritual-net/ritual-streaming-service/pull/22
- `ritual-agent-telemetry`: https://github.com/ritual-net/ritual-agent-telemetry/pull/8
- `ritual-vllm-proxy-go`: https://github.com/ritual-net/ritual-vllm-proxy-go/pull/44
- `claw-spawner`: https://github.com/ritual-net/claw-spawner/pull/65
- `ritual-node-internal`: https://github.com/ritual-net/ritual-node-internal/pull/362
- `chain-deployment-infra`: https://github.com/ritual-net/chain-deployment-infra/pull/387

## Plan Deviations and Final Decisions

- **No unauthenticated read fallback.** The original plan allowed dev/backward-compatible
  fallbacks when production auth was off. During implementation we removed that path:
  all TEE trusted reads now hard-fail when trusted-read config is missing or invalid.
- **Shared config validation moved to common.** The original plan centralized dialing
  but left some service-local config validation. After seeing duplicated
  `validateTrustedReadConfig` logic, validation moved into
  `ritual-go-common/trustedrpc.ValidateAuthenticatedReadConfig`.
- **Read-only registry clients are always authenticated.** `NewReadOnlyClient` was
  removed from `ritual-go-common/registry`; services must use
  `NewTrustedReadOnlyClient` for registry reads.
- **HAProxy was selected.** The off-the-shelf terminator path worked cleanly with
  HAProxy for both HTTP RPC and WS RPC, so no custom proxy repo/binary was needed.
- **Dead env aliases were removed.** `TEE_SERVICE_REGISTRY_RPC_URL`, `WS_URLS`, and
  `CHAIN_RPC_URL` fallback emissions were removed from service config, local configgen,
  and deploy templates/scripts where they were only read aliases.
- **Some stale call sites were only caught by full build/localnet.** The streaming
  service still referenced a removed `chain.NewTrustedClient` constructor, and some
  executor/dKMS registry verifier paths initially missed the cert hash. Local image
  rebuild + local-network startup caught these.

## Implementation Verification Summary

- Unit/focused tests passed across changed Go packages.
- Local service images were rebuilt after the `ritual-go-common` changes.
- `make restart-network` succeeded in `ritual-node-internal`.
- `make tee-registry` showed 12 registered TEE services, including 4 executors.
- `make run-http-call` in `traffic-gen-internal` completed `1/1` successfully.
- `make test-misconfigured-executor` rejected a raw reth endpoint wired as trusted TLS
  with the expected HTTPS/plain-RPC failure.
- Follow-up format/lint/test pass was run and pushed. Broad repo lint still exposes
  unrelated existing debt in `executor-go-internal`, `ritual-vllm-proxy-go`, and one
  unrelated Python test failure in `claw-spawner`.

1. `ritual-go-common`: add a reusable RPC dial package
   Objective: Create one shared place for plain and pinned chain RPC dialing so TEE
   services do not implement pinning locally.
   Change: Add a small common package that parses an optional static SPKI cert hash,
   builds the `mtls.NewCertPinningVerifier` / `NewClientTLSConfigWithPinning`
   transport, dials HTTP JSON-RPC through `ethclient.DialOptions`, and exposes a
   reusable TLS config for WS callers. Final policy: dialing helpers still support
   non-security-critical plain dials, but trusted-read config validation hard-requires
   a hash and HTTPS/WSS endpoint.
   Constraints: Reuse only the static pinning primitive; no registry lookup, refresh
   callback, TEE-address extraction, or client cert. Accept `0x`-prefixed and
   unprefixed hashes, normalize as `0x`-prefixed, reject malformed/all-zero hashes.
   Verification: Unit tests cover hash parsing, plain HTTP dial behavior, accepted
   pinned HTTPS, rejected wrong cert hash, and WS TLS config construction.

2. `ritual-go-common`: route registry clients through the shared dial package
   Objective: Create the durable authenticated read seam for trusted read RPCs.
   Change: Keep `registry.NewClient` for transaction submission and require
   `registry.NewTrustedReadOnlyClient` for read-only registry access. Read-only
   clients must authenticate the RPC certificate with SPKI pinning before trusting
   returned chain data.
   Constraints: Write methods must keep using the write/plain client;
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
   Verification: dKMS config tests cover missing/invalid trusted-read settings in all
   modes and both hash formats. Server/registration tests show reads and writes
   consume the intended URLs.

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
   Verification: Config tests prove write URLs remain separate from authenticated
   reads while trusted read settings are always required. Focused monitor/discovery
   tests and local-network negative tests cover rejection on unauthenticated or wrong
   trusted endpoints.

5. Other Go TEE services: standardize trusted read config
   Objective: Apply the same authenticated-read boundary to vLLM proxy, streaming,
   telemetry, and claw-spawner agent-sidecar paths that read registry or chain state.
   Change: Add `TRUSTED_READ_RPC_URL` and `RPC_CERT_HASH` where those services used
   plain registry/chain RPC envs for trusted reads. Preserve each service's explicit
   write URL for registration or other signed writes.
   Constraints: Avoid per-service pinning logic; use the common helper. Do not keep
   legacy env fallback aliases for trusted reads.
   Verification: Each service has config tests for required trusted-read settings,
   hash canonicalization, invalid HTTP trusted-read rejection, and successful
   construction of pinned registry/read clients where applicable.

6. `ritual-node-internal`: make local-network TLS proxy self-contained
   Objective: Local-network startup should generate or persist proxy cert material,
   mount it into an off-the-shelf TLS terminator, and wire the pinned hash into TEE
   services without relying on external deploy tooling.
   Change: Add local-network cert/key generation or reuse, add an HAProxy TLS
   terminator service in front of reth, expose trusted HTTP and WSS endpoints, and
   inject `TRUSTED_READ_RPC_URL`, `TRUSTED_READ_WS_URL`, and `RPC_CERT_HASH`.
   Constraints: Keep reth untouched and keep local-network self-contained.
   Verification: A local network starts from `ritual-node-internal`; TEE services read
   through the trusted endpoint; replacing the cert/hash causes read startup or first
   read to fail.

7. `chain-deployment-infra`: mirror the trusted-read contract for deploy scripts
   Objective: Production and sim deploys should wire the same trusted-read contract as
   local-network.
   Change: Update relevant deploy/config generation scripts to provision or mount the
   proxy cert material, configure trusted read envs, emit trusted read URLs and cert
   hashes, and preserve existing write endpoints including executor multicast lists.
   Also remove stale env aliases from deploy templates/scripts.
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
   reads for a raw reth endpoint miswired as trusted TLS, executor write endpoints are
   preserved, and config validation rejects missing trusted-read auth.

## Structural Simplification Check (implementation pass)

- The implementation plan keeps one shared client-side pinning mechanism in
  `ritual-go-common`; service repos only wire URLs/hashes and should not duplicate TLS
  verification or trusted-read config validation logic.
- The read/write split follows the real trust boundary: trusted reads use
  `TRUSTED_READ_RPC_URL`/`RPC_CERT_HASH`; writes preserve existing topology, including
  executor multicast submission.
- The first two subtasks are prep/refactor work that create the seam before service
  behavior changes, reducing the risk of scattered `if trusted` branches.
- The server-side proxy is config-only HAProxy in local-network; no custom proxy binary
  was needed.
