# Agent Harness Adherence in `ritual-node-internal`

**Status:** In-progress — pivoted from ZeroClaw runtime to Hermes runtime  
**Date:** 2026-04-16 (revised)  
**Source of truth:** This file

## Design Plan
- Goal:
  Integrate `agent-harness-adherence` into local `ritual-node-internal` so a local network can spawn at least one **Hermes** agent runtime with the AHA MCP server configured, pointed at the local dKMS/chain stack, and capable of completing one real gated dKMS-backed flow under a focused post-launch prompt.
- Main workstreams:
  1. Runtime packaging: make the AHA MCP executable available inside the Hermes runtime image (`hermes-instance`).
  2. Runtime config injection: add an `mcp_servers.agent-harness-adherence-gate` entry to `~/.hermes/config.yaml` at container startup, using Hermes' native MCP config schema.
  3. Environment wiring: provide `DKMS_HTTP` (and any other truly required runtime values) to the stdio MCP subprocess via the `env` key on the Hermes MCP server entry, using values consistent with local `ritual-node-internal` compose topology.
  4. Verification-driving prompt delivery: prefer a post-launch chat-completions request to the live Hermes agent gateway (port 8642) as the primary proof path; keep seeded heartbeat/system-prompt guidance only as a fallback or setup aid.
  5. Tiered verification: first prove ordered AHA usage plus real dKMS signing and capture the signed payload (Tier 1); only then add optional broadcast / on-chain effect verification (Tier 2) if the tool surface supports it cleanly.
  6. Local verification: document and automate a reproducible local path from `make restart-network` to a spawned Hermes agent that completes the AHA proof.
- Key decisions:
  1. The first (and only) integration target runtime is **Hermes** (`agent_runtime=2`). This is what `make launch-persistent-agent` launches by default, and Hermes has first-class native MCP support (`hermes mcp add`, `mcp_servers` key in `~/.hermes/config.yaml`, `StdioServerParameters`-based stdio transport with full `env`/`${VAR}` interpolation). Earlier plan pass targeted ZeroClaw; that path worked with a local patch to `zeroclaw-internal`'s `process_message_with_session`, but Hermes is the team's path forward and removes the need for that patch.
  2. For the first integration, keep AHA calling dKMS directly rather than adapting it to executor-go's proxy surface.
  3. Prefer packaging AHA into the Hermes runtime image instead of relying on a host path inside spawned containers.
  4. Prefer post-launch chat-completions prompting as the primary verification mechanism; seeded system prompt / `HEARTBEAT.md` is secondary.
  5. Do not assume the current AHA surface can both sign and broadcast; verification must distinguish "signed payload produced" from "transaction mined on-chain".
  6. Use `ritual-node-internal` as the final integration entrypoint even if changes span multiple repos.
- Risks and dependencies:
  1. Hermes' OpenAI-compatible gateway path (`API_SERVER_ENABLED=true` on port 8642) may or may not expose MCP-registered tools in a live chat-completions request, mirroring the architectural gap we hit in ZeroClaw. If it does not, the fallback options in order are: (a) drive the proof via `hermes chat` invoked inside the container (tool-aware CLI path), (b) drive it via a channel, or (c) patch Hermes' gateway locally, same shape as the ZeroClaw patch.
  2. AHA currently assumes a standalone dKMS URL shape (`127.0.0.1:8000`) that does not match local RNI defaults; we inject the correct value via the server's `env` block.
  3. AHA currently talks directly to dKMS HTTP endpoints; local RNI may prefer executor-go proxy surfaces for some agent flows. Out of scope for Tier 1.
  4. The gate-facing tool name is `evm_send_transaction`, but the current dKMS-backed implementation returns `signed_transaction_rlp` rather than a broadcast transaction hash. Tier 1 treats this as a signed-payload proof; Tier 2 broadcasts host-side.
  5. If Hermes' MCP loader discovery step (`hermes mcp add` performs a probe connect) requires live dKMS connectivity at container startup, ordering with the rest of the compose stack matters. Mitigation: seed `config.yaml` directly rather than invoking the interactive `hermes mcp add` command.
- Current-system model:
  1. `ritual-node-internal` owns local stack bring-up, compose generation, local dKMS wiring, and claw-spawner launch.
  2. `claw-spawner` owns spawned runtime images (including `hermes-instance`), seeding of `workspace_config`, heartbeat prompt injection, and runtime environment plumbing.
  3. `agent-harness-adherence` owns the MCP gate server, dKMS-backed credential server, and optional `AdherenceRegistry` attestation path.
  4. `dkms` owns the direct signing and OAuth HTTP endpoints that AHA currently expects.
  5. `executor-go-internal` owns the agent-facing key-derivation proxy and already-implemented remote-signing surfaces used by existing sidecar flows.
  6. Hermes (Nous Research `hermes-agent`) owns native MCP configuration, stdio MCP transport, and a `hermes gateway` OpenAI-compatible HTTP server on port 8642 inside the container.
  7. The authoritative existing chain-heartbeat transaction path is sidecar-managed remote signing. For this project, that path is background context, not the primary integration target.
  8. Generated/deployment artifacts that can change runtime behavior include `ritual-node-internal` compose output, runtime image contents in `claw-spawner`, and any local contract/resource addresses surfaced by `ritual-node-internal`.

- Historical context: how the pre-sidecar runtime-owned wallet flow worked
  1. Before the sidecar-owned heartbeat path, the runtime itself was expected to reach dKMS, export a derived private key, and submit chain transactions directly.
  2. The runtime learned how to reach dKMS from `KEY_DERIVATION_URL`, `KEY_DERIVATION_TOKEN`, and `AGENT_OWNER_ADDRESS`. In that older model, `/v1/derive_key` returned both `address` and `private_key`, so the runtime had the signing key material locally for the duration of the operation.
  3. The runtime learned how to reach chain RPC from `HEARTBEAT_CHAIN_RPC` or `RPC_URLS`.
  4. Direct transaction submission happened inside the runtime. Hermes-side flows called `cast send` after deriving the key.
  5. The newer sidecar path intentionally changed that trust boundary. Instead of exporting the private key into the runtime, the sidecar resolves the agent address with `get_address`, asks dKMS/executor-go to sign registration, heartbeat payloads, and unsigned transaction RLP remotely, and only broadcasts the already-signed transaction from the sidecar.
  6. That distinction matters for this AHA plan: AHA's first integration is conceptually closer to the older runtime-owned dKMS/RPC model than to the newer sidecar-managed heartbeat signer. That is why this plan treats the missing seam as runtime MCP/config/env wiring rather than reworking the existing sidecar heartbeat code path.

- Runtime-specific context: what Hermes exposes natively
  1. `hermes mcp add/remove/list/test/configure` subcommands manage MCP servers interactively, storing config under `mcp_servers.<name>` in `~/.hermes/config.yaml`.
  2. Supported server-config keys include `command`, `args`, `env`, `url`, `headers`, `auth`, `tools.include`, `enabled`. The `env` key is a dict passed directly to the stdio subprocess, and values support `${VAR}` interpolation from `os.environ` and `~/.hermes/.env`.
  3. Hermes' `tools/mcp_tool.py` uses `mcp.StdioServerParameters` to spawn stdio servers, so the stdin/stdout JSON-RPC contract is identical to what AHA's `aha-gate-mcp` already implements. No wrapper-script changes are required relative to the ZeroClaw attempt (the stdin-safe `python -c '...'` form continues to apply).
  4. Hermes' `hermes gateway run` binds on `API_SERVER_PORT` (default 8642) and is controlled by `API_SERVER_ENABLED=true`. The equivalent of ZeroClaw's `/v1/chat/completions` is provided by the Hermes gateway.

## Ambiguities To Resolve
- None currently blocking implementation of Tier 1 on Hermes.
- Resolved decisions:
  1. First (and only) target runtime is Hermes (`agent_runtime=2`).
  2. AHA should keep calling dKMS directly in the first local integration.
  3. AHA should be baked into the Hermes runtime image (`hermes-instance`) for the first implementation pass.
  4. The first proof is local-only and does not include on-chain `AdherenceRegistry` anchoring.
  5. The primary verification path should be a focused post-launch prompt to the live Hermes gateway, not only a seeded heartbeat file.
  6. The proof should distinguish Tier 1 (agent uses AHA and reaches real signing) from Tier 2 (signed transaction is broadcast and verified on-chain).
  7. Seed Hermes' `mcp_servers` config by writing `config.yaml` directly in the entrypoint rather than invoking the interactive `hermes mcp add` CLI. This avoids the discovery-time probe connect and interactive prompts.

## Implementation Plan
1. Hermes image packaging in `claw-spawner`
   Objective:
   Bake `agent-harness-adherence` into the `hermes-instance` runtime image so the container has a runnable `aha-gate-mcp` entrypoint without relying on host-only paths.
   Change:
   Update `claw-spawner/hermes-instance/Dockerfile` to install the `agent-harness-adherence` Python package into a dedicated venv (or the image's default Python env) and copy in the stdin-safe `aha-gate-mcp` wrapper script already used for the ZeroClaw attempt. Hermes' base image is already `python:3.11-bookworm`, so no separate Python stage is required.
   Constraints:
   Keep the first pass local-dev oriented, but do not depend on bind mounts or host repo paths inside spawned containers. Do not disturb existing non-AHA Hermes startup behavior.
   Verification:
   Build the image successfully, start a container from it, confirm `aha-gate-mcp` is present on PATH (or at a known absolute path) and produces a well-formed MCP banner when stdin is provided.

2. Hermes MCP config injection at container startup
   Objective:
   Ensure each spawned Hermes runtime ships with an `mcp_servers.agent-harness-adherence-gate` entry pointing at the baked `aha-gate-mcp` and passing the correct `DKMS_HTTP` (via the server-entry `env` map).
   Change:
   Extend `claw-spawner/hermes-instance/entrypoint.sh` so that, after the existing workspace-seeding block and before `hermes gateway run`, it writes an entry into `$HERMES_HOME/config.yaml` under `mcp_servers`. Do this unconditionally for now (Tier 1 integration scope) but gate it behind a runtime-aware env (e.g. `AHA_ENABLED=true`) so non-AHA spawns remain untouched. Seed the config file directly in YAML rather than invoking `hermes mcp add`, to avoid the interactive discovery probe and to keep startup deterministic.
   Constraints:
   Preserve any existing `mcp_servers` entries if present (merge rather than overwrite). Preserve existing `hermes-instance` startup behavior for agents that do not opt into AHA.
   Verification:
   Spawn an agent, `docker exec` into it, inspect `~/.hermes/config.yaml`, confirm `hermes mcp list` shows `agent-harness-adherence-gate` with the expected command and `env`, and confirm `hermes mcp test agent-harness-adherence-gate` reports a successful tool-discovery connect.

3. Local endpoint and identity wiring in `ritual-node-internal` / `executor-go-internal`
   Objective:
   Provide the spawned Hermes runtime with the correct local-network values for direct dKMS access, specifically the executor-registration identity that dKMS uses to resolve a TEE service.
   Change:
   Wire local defaults for `DKMS_HTTP` (the in-network dKMS URL) and for `AHA_EXECUTOR_ID`, which AHA's `dkms_credential_server` reads when calling `/v1/get_address`, `/v1/sign_transaction`, etc. `AHA_EXECUTOR_ID` MUST be the executor's on-chain registration address (same value dKMS logs as `registration_address` and that executor-go registers into `TEEServiceRegistry`) — **not** the secrets EOA that `EXECUTOR_ADDRESS` already exposes. Implemented as:
   - `executor-go-internal/internal/services/spawn/service.NewService(...)` now takes the registration address; `cmd/executor/main.go` passes `cryptoCtx.RegistrationAddress`; the spawn path sets `extraEnv["AHA_EXECUTOR_ID"] = s.registrationAddress` alongside `EXECUTOR_ADDRESS`.
   - `claw-spawner/claw_spawner/docker/manager.py` already does `env.update(config.extra_env)` (no allowlist at the Docker manager layer), so one more `extra_env` key propagates into the Hermes container env with no further plumbing.
   - `claw-spawner/hermes-instance/entrypoint.sh` reads `AHA_EXECUTOR_ID` from env and writes it into the `mcp_servers.agent-harness-adherence-gate.env` block of `~/.hermes/config.yaml` alongside `DKMS_HTTP`, so Hermes spawns the stdio MCP subprocess with the right identity.
   Constraints:
   Do not rely on forwarding env through `secrets_dict` from `traffic-gen-internal` — `executor-go`'s `SpawnJobConfig` uses a small allowlist for `secrets_dict` and silently drops arbitrary keys. Use `extraEnv` on the Go side instead. Keep `AGENT_OWNER_ADDRESS`/`RITUAL_DKMS_OWNER_ADDRESS` flowing through the existing owner-address path. Tier 1 is local-only and not anchoring to `AdherenceRegistry`, so do not require chain-attestation envs.
   Verification:
   After `make restart-network`:
   - `docker logs executor-go-http-1 | grep registration_address` prints e.g. `0xEe670f8901…`.
   - Run `make run-aha-persistent-agent` from `traffic-gen-internal`. Inside the spawned agent container:
     - `env | grep AHA_EXECUTOR_ID` shows the same value as the logged `registration_address`.
     - `~/.hermes/config.yaml` contains `mcp_servers.agent-harness-adherence-gate.env.AHA_EXECUTOR_ID` equal to that value.
   - `docker logs dkms` shows `executorId=<registration_address>` (non-zero) in `resolved address` / `signed transaction` entries, instead of the earlier `failed to query executor registry` 500 with `executorId=0x00…00`.

4. AHA-aware spawn path in `traffic-gen-internal`
   Objective:
   Make the local spawn path able to launch an AHA-enabled Hermes agent intentionally.
   Change:
   Ensure `AhaPersistentAgentAction` sets `agent_runtime=2` unconditionally (not relying on the `SpawnAgentAction` default of 0), sets `enable_aha=True` (already done), and that downstream the correct Hermes gateway port (8642) is used when the driver talks to the live agent. Keep the recipe (`make run-aha-persistent-agent`) as the single entrypoint.
   Constraints:
   Keep the first proof narrow and deterministic. Avoid expanding the first pass into OAuth or optional chain anchoring. Prefer an additive dedicated recipe over changing unrelated generic spawn behavior.
   Verification:
   Run the local spawn flow, confirm the spawned runtime image is `hermes-instance`, confirm the gateway is reachable via `docker exec curl http://127.0.0.1:8642/...`.

5. Post-launch prompt-driven verification action in `traffic-gen-internal`
   Objective:
   Prove that a live spawned Hermes agent can be steered through the AHA path by an ordinary post-launch chat-completions request.
   Change:
   Keep the two-stage driver we already have (`_build_address_prompt`, `_build_sign_prompt`), sending stage A then stage B over the Hermes gateway. Add a probe that confirms the Hermes gateway lists MCP tools in the prompt before asserting failure. If Hermes' gateway does not expose MCP tools to a chat-completions request, fall back in this order: (a) use `docker exec hermes chat -q '<prompt>'` which is confirmed tool-aware, (b) drive via a channel, (c) patch Hermes' gateway with the same shape as the ZeroClaw `process_message_with_session` patch.
   Constraints:
   Treat the current AHA surface honestly: if the tool returns signed payload rather than a mined tx hash, record that as a successful Tier 1 proof instead of pretending broadcast happened inside AHA. Prefer direct evidence from the agent response and runtime traces.
   Verification:
   From a local run, show that the prompt reaches the agent, the agent calls AHA tools in order, and the AHA/dKMS layers produce a real signing result tied to the local stack. Concretely: agent log shows `Processing request of type CallToolRequest` for `evm_get_address`, `evm_send_transaction`, and `adherence_status`; gate's `status_after_send` shows `complete: true`; `signed_transaction_rlp` is present and parses as a valid signed legacy transaction with the expected `from`/`chainId`/`to`.

6. Optional broadcast and on-chain effect verification
   Objective:
   Extend the proof from "agent reached real signing" to "the signed result produced a real chain artifact" when the surface supports it cleanly.
   Change:
   Keep the existing host-side broadcast path (`--aha-broadcast-signed-tx`) that sends the captured RLP to `localhost:8545` and waits for a receipt, then verify recipient balance delta and/or `eth_getTransactionByHash` fields.
   Constraints:
   Do not blur this with Tier 1. Only claim on-chain effect when the implementation truly broadcasts the signed transaction and the evidence is collected.
   Verification:
   Show a concrete tx hash and matching chain evidence, or explicitly leave this step incomplete if only Tier 1 is implemented.

7. Local-network integration verification from `ritual-node-internal`
   Objective:
   Prove the full stack works from the actual local entrypoint the team uses.
   Change:
   Run the stack through `ritual-node-internal`, bring up the local network, use the AHA-enabled spawn path plus the post-launch verification flow, and capture the exact reproduction steps in the plan or supporting docs.
   Constraints:
   Use the real local workflow rather than a standalone AHA-only smoke test. The runtime selected by `make run-aha-persistent-agent` must be Hermes.
   Verification:
   From a clean local run, show that `make restart-network` succeeds, the AHA-enabled Hermes agent is spawned through the standard path, `hermes mcp list` shows the AHA entry, and at least Tier 1 completes against the local dKMS-backed setup. Tier 2 is additive when implemented.

## Appendix: what carries over from the ZeroClaw attempt
- Kept:
  - `aha-gate-mcp` wrapper script (stdin-safe `python -c` bootstrap). Works identically under Hermes' `StdioServerParameters`.
  - The `AhaPersistentAgentAction` driver skeleton (tiered verification, host-side broadcast, gateway-resolve-via-`docker inspect`).
  - The hostname/loopback pattern in the driver (`docker exec curl http://127.0.0.1:<port>/...`) — only the port changes (18789 → 8642).
  - Genesis artifact refresh and dKMS/executor-go rebuilds performed during baseline debugging.
- Dropped as unnecessary on the Hermes path:
  - The `zeroclaw-internal` `process_message_with_session` MCP-tools patch (still preserved on-branch at `spencer/dkms-oauth-2604`, one commit to revert cleanly if desired).
  - The `[mcp]` TOML injection in `claw-spawner/zeroclaw-instance/entrypoint.sh` and the corresponding Python-based renderer (ZeroClaw-only path).

## Appendix: Tier 1 evidence of end-to-end AHA->Hermes->dKMS wiring (2026-04-16)
From a clean `make restart-network` followed by `make run-aha-persistent-agent`:
- `docker logs executor-go-http-1` → `"registration_address":"0xEe670f890141314F9C5abEB97D6D03DeCBFE61ac"`.
- Spawned container (`agent-<instance_id>`) env: `AHA_EXECUTOR_ID=0xEe670f890141314F9C5abEB97D6D03DeCBFE61ac`.
- Spawned container `~/.hermes/config.yaml`:
  ```
  mcp_servers:
    agent-harness-adherence-gate:
      command: /usr/local/bin/aha-gate-mcp
      env:
        DKMS_HTTP: http://dkms:8080
        AHA_EXECUTOR_ID: '0xEe670f890141314F9C5abEB97D6D03DeCBFE61ac'
      enabled: true
  ```
- `dkms` logs during the AHA proof window: `msg="resolved address" ... executorId=0xEe670f890141314F9C5abEB97D6D03DeCBFE61ac endpoint=get_address address=0xB3e90afe...` and `msg="signed transaction" ... endpoint=sign_transaction` — no more 500s with `executorId=0x00…00`.
- `AhaPersistentAgentAction` driver observes:
  - address stage: `adherence_ok: true`, `progress: 1/2`, real dKMS address returned, `status_after_get.cursor: 1`.
  - sign stage: `adherence_ok: true`, `progress: 2/2`, `signed_transaction_rlp` is a valid 208-byte legacy RLP, `status_after_send.complete: true`.
  - action result classification: `PARTIAL_SUCCESS` from `_verify_signed_transaction`'s strict field match (Tier-1 signing-check semantics, separate from the AHA plumbing — see "Known follow-ups" below).

### Known follow-ups (not Tier 1 plumbing blockers)
- `_verify_signed_transaction` in `aha_persistent_agent.py` recovers the signer and compares nonce/to/value/chainId to the unsigned tx it built. In the current dKMS signing flow, the returned signed tx's nonce does not necessarily match `eth_getTransactionCount(aha_address, "pending")` because dKMS is signing an internally-derived tx, not the exact unsigned RLP we hand it. Decide whether to (a) relax the verifier to only require signer recovery + structural correctness, or (b) change AHA/dKMS so `sign_transaction` signs the provided unsigned RLP byte-for-byte. This is the gating question for Tier 2 broadcast.

## Appendix: Tier 2 enablement — Option A (explicit chain id) + EIP-1559 unsigned RLP (2026-04-16)

### Motivation
After Tier 1 went green, Tier 2 (host-side broadcast) still failed. Two distinct bugs were unmasked in sequence.

### Bug 1: dKMS misinferred the chain id from the unsigned RLP's `v` placeholder
- `traffic-gen-internal` originally built the unsigned RLP via `cast mktx --raw-unsigned --legacy --chain 1979`, which emits a legacy EIP-155 unsigned payload whose `v` field is the chain id (1979) with `r=s=0` — the canonical EIP-155 pre-hash placeholder.
- `dkms/internal/server/signing.go` then called `tx.UnmarshalBinary(raw)` followed by `chainID := tx.ChainId()`. go-ethereum has no way to distinguish a legacy pre-hash RLP from a real signed legacy tx where `v` happens to equal the chain id, so it ran `deriveChainId(v) = (v-35)/2 = 972` and signed for the wrong chain. The resulting signed tx decoded as chain id 972, not 1979, and Reth rejected it during broadcast.

### Fix — Option A
Plumb an explicit `chainId` end-to-end so dKMS never has to infer it:
1. `dkms/internal/server/signing.go` — add optional `ChainID *uint64` to `SignTransactionRequest`; when non-nil, use it to construct the signer; otherwise fall back to `tx.ChainId()` for backwards compatibility. Also widened the fallback error to `"Transaction must include chain id (EIP-155) or explicit chainId field"`.
2. `agent-harness-adherence/aha_mcp/dkms_client.py` — `sign_transaction` takes an optional `chain_id` kwarg and forwards it as `chainId` in the JSON body.
3. `agent-harness-adherence/aha_mcp/dkms_credential_server.py` — `evm_sign_transaction` forwards its `chain_id` parameter into `dkms_client.sign_transaction`.
4. `dkms/internal/server/signing_test.go` — new `TestSignTransactionExplicitChainIDBeatsVPlaceholder` characterization test pins down that with `v=1979, r=s=0` the naïve `tx.ChainId()` returns 972, while `LatestSignerForChainID(1979).SignTx(...)` produces a signed tx with `ChainId()==1979` and correct sender recovery.

Backwards-compat: an old AHA that does not send `chainId` still works (falls back to `tx.ChainId()`); a new AHA talking to an old dKMS still works (dKMS's JSON decoder ignores unknown fields).

### Bug 2: Reth rejects legacy (type 0) transactions with `transaction type not supported`
After the chain-id fix, the signed tx encoded for chain 1979 (confirmed: `v=0x0f99 → (3993-35)/2 = 1979`), but `eth_sendRawTransaction` returned `-32003 "transaction type not supported"`. The local Ritual chain is configured to only accept EIP-1559 (type 2) transactions — verified by inspecting the `spawn_agent_heartbeat_funding` tx which is `type: 0x2` with `maxFeePerGas`/`maxPriorityFeePerGas`.

### Fix
`traffic-gen-internal/src/action/aha_persistent_agent.py`:
- Drop the `cast mktx --legacy` subprocess and build the unsigned RLP inline with `rlp.encode(...)` as an EIP-1559 envelope: `0x02 || rlp([chain_id, nonce, maxPriorityFee, maxFee, gas, to, value, data, access_list, v, r, s])` with `v=r=s=0`. The 12-field shape is required because go-ethereum's `types.Transaction.UnmarshalBinary` decodes a `DynamicFeeTx` via its full struct; a 9-field body would fail to decode.
- Surface EIP-1559 fee fields (`maxFeePerGas`, `maxPriorityFeePerGas`) as advisories in `_verify_signed_transaction`; keep legacy `gasPrice` as a fallback advisory.
- Why this is unambiguous: in EIP-1559 the chain id is the first explicit RLP field rather than an EIP-155 `v` placeholder, so `tx.ChainId()` recovers it directly with no `(v-35)/2` inference. We still forward the explicit `ChainID` to dKMS so the contract stays symmetric across legacy and typed callers.

### Evidence
A post-fix run of `make run-aha-persistent-agent` produced:
- `signed_transaction_rlp = 0x02f86d8207bb38...c080a0...a0...` — EIP-1559 type-2 RLP with `chain_id = 0x7bb = 1979` in the canonical first field.
- Tier 1 `_verify_signed_transaction` passes: sender recovers to the dKMS-derived address; `to`, `value`, `data` match the requested transfer; `chainId==1979`.
- Broadcast via `eth_sendRawTransaction` no longer returns `transaction type not supported`; Reth now runs the full validation pipeline against the tx.

### Remaining Tier 2 gate — nonce race with the agent's autonomous activity
With chain id and tx type correct, the last observed broadcast failure is `-32003 "nonce too low: next nonce 57, tx nonce 56"`. The dKMS-derived EOA is shared with the Hermes agent itself, which submits autonomous heartbeat/onboarding transactions to a scheduler contract (observed at e.g. nonces 59 and 60 on `0xef505e...3aca`) during the AHA proof window. Between the driver's `eth_getTransactionCount(..., "pending")` call and the post-sign broadcast, several of the agent's own txs mine and drain the nonce counter, leaving the AHA-signed tx stale.

Candidate fixes, in order of cost:
1. Retry the sign stage with a freshly fetched `pending` nonce on `nonce too low` (narrow driver change, up to 2–3 retries; still racy against a busy agent).
2. Use a dedicated dKMS-derived key for AHA proofs that isn't also the agent's hot-wallet identity (isolates nonce space; cleanest).
3. Pause the agent's autonomous tx loop for the duration of the AHA proof (needs Hermes runtime hook).

Choice of fix is outside the scope of Option A and should be tracked separately.

## Appendix: Tier 2 nonce race — Option 2 (dedicated AHA dKMS leaf at index=1)

### Decision
Adopt candidate fix (2) from the previous appendix: derive the AHA-proof EOA at a non-zero dKMS index so the AHA-signed tx owns its own nonce space, disjoint from the Hermes hot wallet at index=0. Option 1 (retry on `nonce too low`) was rejected because Hermes keeps submitting heartbeats inside the proof window, so any fixed retry count can still lose. Option 3 (pause the heartbeat loop) requires a runtime hook we do not own and bleeds test infrastructure into the agent runtime.

### Why this is the right shape
- Hermes' heartbeat posting uses the dKMS leaf at index=0 (see `spawn_agent.py` → `get_dkms_payment_address_via_precompile(..., key_index=0)` and the funding block directly below it). That EOA is by design "live" — its pending nonce advances as long as the agent is up.
- The AHA proof only needs "dKMS signed a transaction the adherence gate ordered", which is independent of which owner-root leaf signs. Picking a different leaf keeps the cryptographic proof intact while decoupling nonce spaces.
- Both leaves are derived from the same owner address through the same precompile path, so the AHA sender recovery still lands on an address that provably belongs to the owner — the isolation is purely at the transaction-ordering layer.

### Change set
1. `agent-harness-adherence/aha_mcp/dkms_credential_server.py` — `evm_get_address` and `evm_sign_transaction` now take an optional `key_index: int = 0` and forward it to `dkms_client`. Added a module-level alias `evm_send_transaction = evm_sign_transaction` so the gate's `_backend.evm_send_transaction` lookup resolves against the dKMS backend (previously only the stub defined that name, which would have AttributeError'd against real dKMS the moment the gate invoked the tool — a latent bug the index-1 refactor surfaced).
2. `agent-harness-adherence/aha_mcp/gate_server.py` — `evm_get_address` and `evm_send_transaction` MCP tools expose an optional `key_index: int = 0` kwarg and forward it to the backend via `_gate_then_call(..., key_index=key_index)`.
3. `agent-harness-adherence/aha_mcp/stub_impl.py` — matched signatures; stub folds `key_index` into its deterministic address digest so two indices produce two distinct stub addresses (keeps unit tests honest).
4. `traffic-gen-internal/src/action/spawn_agent.py` — success context now exposes `executor_address` so downstream verification flows can reuse the same TEE executor for follow-up precompile derivations without re-running `ExecutorSelector`.
5. `traffic-gen-internal/src/action/aha_persistent_agent.py`:
   - Constant `AHA_KEY_INDEX = 1` plus `AHA_PROOF_EOA_MIN_BALANCE_WEI` / `AHA_PROOF_EOA_FUND_AMOUNT_WEI` (sized against `DEFAULT_MAX_FEE_WEI * DEFAULT_GAS_LIMIT`).
   - Before the address-stage prompt, the driver now calls `get_dkms_payment_address_via_precompile(..., key_index=AHA_KEY_INDEX)` using the reused `executor_address`, asserts the returned address is not the index-0 hot wallet, and funds it via `ensure_eth_balance` from the owner's private key. `expected_address` for the sender-recovery check is the index-1 address, not the spawn-time heartbeat address.
   - `_build_address_prompt` and `_build_sign_prompt` now render an explicit `key_index: <int>` argument into the MCP call stanza so the agent passes it through the gate to dKMS.

### Invariants and failure modes
- If the executor ever returns the same address for index=0 and index=1 the whole isolation story collapses, so the driver fails loudly with a dedicated error instead of proceeding to race.
- If funding fails the proof aborts before any prompt is sent — we never end up with a broadcast attempt from an unfunded dKMS leaf.
- Backwards compat: all MCP/server signatures default `key_index=0`, so existing callers that don't pass the kwarg continue to derive the historical address.

### Verification plan
1. Rebuild `dkms` and `hermes-instance` images so the new AHA source is inside the Hermes container.
2. `make restart-network` from `ritual-node-internal`.
3. `make run-aha-persistent-agent` and confirm:
   - Driver logs an `AHA-proof EOA: index=1 address=0x...` line distinct from the index=0 heartbeat address.
   - `ensure_eth_balance` funding tx mines.
   - Hermes calls `evm_get_address` and `evm_send_transaction` with `key_index=1`; dKMS logs `endpoint=get_address` / `endpoint=sign_transaction` for that address.
   - `_verify_signed_transaction` sender-recovery matches the index-1 derivation.
   - Host-side broadcast lands (no `nonce too low`) and the recipient balance delta matches `DEFAULT_TRANSFER_AMOUNT_WEI`.
4. Record the final tx hash plus `eth_getTransactionByHash` snippet in this appendix as Tier 2 evidence.

### Additional fix unmasked during verification: EIP-1559 decode in `_verify_signed_transaction`
Running the above verification plan produced a clean sign stage but the Tier 1 verifier itself aborted with:

> `Could not verify signed transaction: RLP string ends with 111 superfluous bytes`

Root cause: `TypedTransaction.from_bytes` (from `eth_account._utils.typed_transactions`) explicitly requires a `HexBytes` instance and raises `TypeError` on a plain `bytes` object. The helper was passing `bytes.fromhex(...)`, so the `except Exception` branch silently fell through to `Transaction.from_bytes` (the legacy decoder) on an EIP-1559 (`0x02`-prefixed) payload; the legacy RLP decoder then reported the trailing typed-tx bytes as superfluous.

Fix: wrap in `HexBytes` before trying the typed path so a real EIP-1559 tx is decoded, and only fall back to the legacy decoder for legacy payloads. Minimal, local to `_decode_signed_transaction`.

### Evidence — Tier 2 green on the local chain (2026-04-16)
Final run of `make run-aha-persistent-agent`:
- `AHA-proof EOA: index=1 address=0x104D50E12088800431cF59f2373A54Ab8D3E3aa3 (hot-wallet index=0 address=0x39D668aD94FF8A241fC9f39647dF1Baaa1da5507)` — indices resolve to distinct addresses.
- `AHA Tier 1 signed-tx verification PASSED: {'sender': '0x104D50E1...', 'to': '0x...dEaD', 'value': 1, 'nonce': 0, 'expected_nonce': 0, 'gas': 21000, 'max_fee_per_gas': 20000000000, 'max_priority_fee_per_gas': 1000000000, 'chain_id': 1979, 'data': '0x', 'advisories': []}` — no advisories, recovered signer equals the index=1 derivation, EIP-1559 fields round-trip.
- `AHA Tier 2 broadcast PASSED: tx=0x669fc8a4f8c2b352aa550e630ef40afb8ec312549ddabca39f1c410ee1e37a71 balance_delta=1` and `Action completed: 1/1 successful`.
- `eth_getTransactionByHash(0x669fc8a4...)` reports `type=0x2`, `chainId=0x7bb` (1979), `nonce=0`, `gas=0x5208`, `from=0x104d50e1...`, `to=0x...dead`, `value=0x1`, mined in block `0x950`. `eth_getBalance(0x...dEaD)` returns exactly `1` (first-ever transfer to the burn address on this chain), matching `DEFAULT_TRANSFER_AMOUNT_WEI`.

This closes the Tier 2 gate: the Hermes agent obtained a dKMS-backed address via the adherence-gated `evm_get_address`, signed an EIP-1559 transfer via the gated `evm_send_transaction`, and the host-broadcast tx mined on the local Ritual chain with the expected balance delta and the expected recovered sender — all with the AHA-proof key isolated from the autonomous heartbeat's nonce space.

