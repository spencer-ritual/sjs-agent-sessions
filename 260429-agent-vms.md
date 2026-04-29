# Agent VMs Instead of Containers

## Goal / Working Assumptions

### Goal

Map the current agent lifecycle and identify the mechanics that would need to change if agent runtimes move from Docker containers to TEE VMs.

This note is for enumeration, not resolution. The purpose is to make the moving pieces and uncertainty categories legible before any implementation plan. The curated context here will inform future design / implementation docs

- Both persistent and sovereign agents are Docker-backed today and launch through `claw-spawner`; the main difference is intended uptime, with persistent agents designed to stay up and sovereign agents designed to be short-lived exec containers.
- The target model under consideration is that the agent runtime becomes a first-class on-chain TEE citizen, analogous to existing registered services like HTTP executors or vLLM proxies.


## Current Migration View

This is the current best read on the migration shape, given the mechanics below. It is meant to connect the open questions to practical steps rather than replace the detailed inventory.

1. Define the long-term lifecycle API.
   Make the `executor-go` ↔ `claw-spawner` boundary describe the agent lifecycle we actually want: create a runtime, inspect it, stop it, recover it, and return gateway / health / attestation metadata. The specific thing to generalize is today's reliance on Docker operations such as file `inject` / `extract`, container `exec`, logs, stats, and kill/restart commands. If `claw-spawner` is going to be the VM provisioner, this is where its role should become stable rather than container-shaped. The API should also leave room for the sovereign lifecycle decision, such as cold-start VMs, warm blank VMs, or warm registered VMs, so the flow from `JobAdded -> launch -> stop/recover` can stabilize before the VM backend is built.

2. Decide service placement and packaging for agent helper services.
   Today agent runtimes get key derivation, the internal LLM gateway, telemetry, and health checks through the executor-local Docker environment. If the VM strategy is "boot the agent VM and run a local compose-style stack inside it," then these services may not need to be split out of `executor-go` as shared network services. The concrete task is to inspect each helper and decide whether it should be packaged into the VM-local stack, remain executor-owned, or become a shared service. Success means the VM packaging plan can say, for each of the four helpers, exactly where it runs, how the agent reaches it, how it authenticates, and what code/config delta is actually required.

3. Persistent VM milestone.
   Add VM provisioning for persistent agents as one end-to-end milestone, not as a degraded partial pilot. To count as working, the persistent VM path must register with the right agent capability, launch through the existing schedule / async job intake, claim and heartbeat under the agent identity, serve its gateway, sync DA state, and revive from DA after failure or recall. Internally this can still be implemented in slices, but the migration checkpoint should not be considered acceptable until it preserves the persistent-agent functionality containers have today.

4. Sovereign job API refactor.
   Before sovereign VMs, separate job orchestration from container `exec` mechanics. Define a runtime-neutral service API for request payloads, results, logs, cancellation, and artifacts.

5. Sovereign VM migration.
   Choose the lifecycle shape, implement one sovereign runtime VM backend, and migrate one CLI path first. Expand once artifact extraction, logs, cancellation, and delivery are stable.

6. Container retirement.
   Remove compatibility fields, Docker-only monitoring fallbacks, and container backend support when VM parity and localnet/prod verification are stable.


## Identified Mechanics / Affected Areas

This section is organized by mechanics affected by an agent-VM model change.

Each subsection can hold a mix of:
- open questions we still need to figure out
- working priors
- concrete answers, when we already know them

### Registration mechanics

- Agent TEEs need to register in `TEEServiceRegistry`, instead of only having the host executor TEE represented there.
- Agent VM registration needs to reuse the existing `ritual-go-common` registration path; the open question is how that path gets integrated into agent images or sidecars, and where that registration step lives operationally.
- Whether registration happens at VM boot vs Agent Boot 
- TEEServiceRegistry requires a key at registration time, is that key from each agent or some launcher service
- When addresses are in attestations, how does that get linked to the AgentIdentityRegistry system
- How will TEE whitelisting work - currently we whitelist individual executors as a bridge towards proof of cloud

### Capability and workload mechanics

- Current launch / selection / revival paths still rely on `HTTP_CALL` capability today, even though `ITEECapabilityPolicy.Capability` already includes `AUTONOMOUS_AGENT` (11); see `Current State` section `Executor selection and capability gating today`.
- Do persistant & sovereign agents end up under the same capability, or different capabilities
- Do both migrate to their own VMs? Simultaneously or one at a time? Since staging to break up work is best practice, which is higher prio?

### Contract and chain mechanics

- Whether revival scheduling semantics change once the runtime is a registered TEE service
- Whether persistent heartbeat semantics bind to the executor TEE, the agent VM TEE, or both
- `AgentHeartbeat` liveness is still executor-keyed today: `heartbeat()` requires the recovered signer to equal `slot.boundExecutor`, even though `msg.sender` is `slot.agentAddress`
- Persistent launch currently threads an explicit executor address into DKMS extraction context on-chain, so executor identity is part of current contract calldata rather than only an off-chain policy assumption
- Sovereign dynamic executor resolution still hard-requires `HTTP_CALL`, so simply registering an agent VM as `AUTONOMOUS_AGENT` would not make the current harness path use it
- `ritual-dapp-skills` likely needs updates if launch / debug / recovery user flows change, but that repo is not present in this workspace snapshot.

### Launch and control-plane mechanics

- Who/What actually provisions the VM
- What edits `claw-spawner` needs if it evolves into the VM control plane, or whether it is replaced completely; see `Current State` sections `Runtime integration points today` and ``executor-go` ↔ `claw-spawner` / agent-container surfaces today` for relevant details
- What VM control-plane functionality needs to be stripped from `executor-go`; see `Current State` section ``executor-go` ↔ `claw-spawner` / agent-container surfaces today` for relevant details

### Lifecycle mechanics

- How persistent agent boot, restore, and revival work in a VM model; see `Current State` sections `Persistent agents`, `Persistent-agent revival path`, and `Runtime integration points today`
  - Whether the current host-local crash recovery layer in `claw-spawner` remains, is replaced, or is dropped; today that recovery path is separate from chain-driven revival and rebuilds containers from tracked instance state / `da_manifest_cid`
- How sovereign short-lived execution works in a VM model; see `Current State` sections `Sovereign agents`, `Runtime integration points today`, and ``executor-go` ↔ `claw-spawner` / agent-container surfaces today`
  - Whether the current executor-owned Phase 2 worker role for sovereign agents (polling, cancellation, container orchestration, delivery submission) stays on the HTTP executor, moves into the agent VM, or gets split across components
  - Whether sovereign jobs use cold-start VMs, warm pooled VMs, or another lifecycle shape
  - How VMs are automatically spun down, if needed
- What replaces container inject / extract and container-scoped execution semantics; see `Current State` sections `Runtime integration points today` and ``executor-go` ↔ `claw-spawner` / agent-container surfaces today`

### Persistence / DA mechanics

- DA for sovereign agents is an optional / convenient way to upload large prompts and/or store conversation history, while for persistent agents it is important to the revival flow.
Low likelihood the DA backend itself needs to change, but listed for completeness because the current restore integration is tied to container-specific filesystem paths and may need remapping in a VM runtime.

### Migration of executor-provided services

This section lists the executor-provided services that currently leak into agent runtime assumptions and would therefore need a migration story in an agent-VM model.

- Key derivation / DKMS interaction
  - Note: DKMS only gives out keys to HTTP capability right now, `KEY_DERIVATION_TOKEN` for agents is executor-derived secret material
- Internal LLM gateway access (for Ritual LLM provider)
- Telemetry relay
- Health/status checking
- Not a standalone service, but the executor also currently handles submission / delivery attribution for agent work
  - Async delivery attribution remains executor-centric today: `executor-go` `Submitter` uses the executor registration identity when submitting delivery results.

See `Current State` section `Executor-provided services consumed by agent runtimes today` for more detail. 

### Standby-capacity mechanics

- In a one-agent-per-VM world, what component is actually "up and waiting" to take work
- Whether that waiting layer is:
  - a host-side provisioner like `claw-spawner`
  - a pool of warm blank VMs
  - a pool of warm registered agent VMs
  - or nothing, with pure cold starts

### Economic mechanics

- How protocol economics should price standby time behind the waiting layer
- Do parameters in our current system in Reth need to be tuned

### Observability and operations mechanics

- Launch infrastructure needs changes in:
  - `ritual-node-internal` for local bring-up
  - `chain-deployment-infra` for production deployment and operations
- How operators inspect, restart, drain, and debug agent VMs
- What replaces current Docker-based logs / stats / kill flows
- What new runbooks, dashboards, and operational invariants are required
- Any IP gating ramifications (e.g. envoy mesh)

## Current State

### Executor selection and capability gating today

- `ITEECapabilityPolicy.Capability` already includes `AUTONOMOUS_AGENT` (11), but the current traffic-gen launch flows checked here still select `HTTP_CALL` executors today:
  - `traffic-gen-internal/src/action/launch_persistent_agent.py`
  - `traffic-gen-internal/src/action/launch_sovereign_agent.py`
  - `traffic-gen-internal/src/action/spawn_agent.py`
- `ritual-sc-internal/src/factory/SovereignAgentHarness.sol`: if the executor is not pinned, `_resolveExecutor()` calls `teeRegistry.pickServiceByCapability(...)` and currently gates on `HTTP_CALL`.
- `ritual-reth-internal/crates/scheduling/src/canonical.rs`: the revival path is involved in executor selection for revival submissions, and it currently filters to `HTTP_CALL` executors only.

### Persistent agents

1. User or tooling calls the factory-backed persistent launch flow.
   - Main entrypoints:
     - `traffic-gen-internal/src/action/launch_persistent_agent.py`
     - `ritual-sc-internal/src/factory/PersistentAgentFactory.sol`
2. `PersistentAgentFactory` predicts a launcher address, derives / prefunds DKMS context, deploys a `PersistentAgentLauncher`, then calls `configureFundAndArm(...)`.
3. `PersistentAgentLauncher` stores the persistent precompile input and schedules a one-shot launch through `Scheduler.schedule(...)`.
   - Main file:
     - `ritual-sc-internal/src/factory/PersistentAgentLauncher.sol`
4. On the scheduled block, the scheduler calls `PersistentAgentLauncher.executeLaunch(...)`, which calls the `0x0820` persistent-agent precompile.
5. In reth, async detection extracts the executor, TTL, input, and creates a system transaction that calls `AsyncJobTracker.addJob(...)`.
   - Main files:
     - `ritual-reth-internal/crates/ritual-async/src/detector.rs`
     - `ritual-reth-internal/crates/ritual-async/src/validation.rs`
6. `executor-go` watches `AsyncJobTracker` `JobAdded` events over WebSocket, decodes them into `PrecompileJob`s, and queues them for execution.
   - Main files:
     - `executor-go-internal/internal/monitor/contract_event_monitor.go`
     - `executor-go-internal/internal/service/service.go`
7. `PersistentAgentHandler.Execute(...)` decodes the `0x0820` request, validates the chain-issued `agent_id` against `AgentIdentityRegistry`, decrypts launch secrets, resolves DA config, and registers a phase-2 spawn job.
   - Main file:
     - `executor-go-internal/internal/handlers/persistentagent/handler.go`
8. After Phase 1 settles on-chain, `spawn.Service` activates the job and calls `claw-spawner` `POST /instances`.
   - Main file:
     - `executor-go-internal/internal/services/spawn/service.go`
9. `claw-spawner` allocates a per-agent Docker network, creates the runtime container, seeds workspace files, optionally restores from DA, starts the container, and health-checks the internal gateway.
   - Main files:
     - `claw-spawner/claw_spawner/service.py`
     - `claw-spawner/claw_spawner/docker/manager.py`
10. Inside the container, the runtime starts the agent process plus `agent-sidecar`.
    - Current images / entrypoints:
      - `claw-spawner/zeroclaw-instance/entrypoint.sh`
      - `claw-spawner/openclaw-instance/entrypoint.sh`
11. The sidecar claims / heartbeats against `AgentHeartbeat`, syncs encrypted state to DA, and persists the encrypted DA config used later for revival.
    - Main files:
      - `claw-spawner/agent-sidecar/pkg/heartbeat/heartbeat.go`
      - `ritual-sc-internal/src/heartbeat/AgentHeartbeat.sol`

### Persistent-agent revival path

1. Revival is still rooted in the persistent-agent async path, but the calldata is intentionally sparse.
2. The revival request carries:
   - empty or near-empty launch secrets
   - `restore_from_cid`
   - encrypted DA config containing recovered runtime metadata
3. `executor-go` detects revival mode, decrypts the escrowed DA config, reconstructs effective provider / model / runtime config, and passes `Bootstrap=true` into the spawn job.
4. `spawn.Service` forwards that recovery data to `claw-spawner`.
5. `claw-spawner` restores the workspace from DA, starts the container in bootstrap mode, and the sidecar resumes heartbeat / escrow behavior.
6. The core reference doc for this path is:
   - `chain-deployment-infra/docs/PERSISTENT_AGENT_REVIVAL_ARCHITECTURE.md`

### Sovereign agents

1. User or tooling calls the factory-backed sovereign launch path.
   - Main entrypoints:
     - `traffic-gen-internal/src/action/launch_sovereign_agent.py`
     - `ritual-sc-internal/src/factory/SovereignAgentFactory.sol`
2. `SovereignAgentFactory` predicts / deploys a `SovereignAgentHarness`, derives / funds DKMS context, then configures and arms a rolling scheduler window.
3. `SovereignAgentHarness` stores the `0x080C` precompile payload and either:
   - uses a pinned executor, or
   - resolves one at invocation time from `TEEServiceRegistry.pickServiceByCapability(...)`
   - Main file:
     - `ritual-sc-internal/src/factory/SovereignAgentHarness.sol`
4. On each scheduled wakeup, the scheduler calls into the harness, and the harness calls the sovereign-agent precompile at `0x080C`.
5. In reth, the async detector again builds a system transaction that writes the job into `AsyncJobTracker`.
6. `executor-go` consumes the `JobAdded` event and sends the job to `SovereignAgentHandler.Execute(...)`.
7. Phase 1 returns immediately with a task id and registers a phase-2 poll job.
   - Main file:
     - `executor-go-internal/internal/handlers/sovereignagent/handler.go`
8. In Phase 2, `executor-go` acquires an ephemeral exec container from the container registry, injects prompt / skills / history / artifacts, runs Crush / ZeroClaw / OpenClaw inside the container, extracts outputs, and destroys the container afterward.
   - Main files:
     - `executor-go-internal/internal/handlers/sovereignagent/handler.go`
     - `executor-go-internal/internal/services/clicontainer/client.go`
9. Results are delivered back through `AsyncDelivery`, which calls the harness callback surface.

### Runtime integration points today

#### Persistent agents

- What `claw-spawner` injects into the runtime container:
  - DA-restored files from HuggingFace / GCS / IPFS / Pinata manifests during restore
  - `workspace_config` files copied into the runtime workspace
  - `HEARTBEAT.md` synthesized from `openclaw_config.agents.defaults.heartbeat.prompt` when needed
  - generated `openclaw.json`
  - runtime env derived from request / config, including bootstrap, heartbeat-chain, Telegram, UAHI, key derivation, and RPC settings
- What `claw-spawner` extracts from the runtime:
  - there is not a host-driven post-run extract step analogous to sovereign execution
  - persistence is primarily sidecar-driven through encrypted DA sync, with later restore pulling files back from DA into a fresh container
- What `claw-spawner` causes to run in the runtime:
  - `claw-spawner` copies seeded / restored files into the container via `copy_files_to_container(...)`
  - `openclaw-instance/entrypoint.sh` runs:
    - `openclaw onboard ...`
    - `openclaw config set ...`
    - `openclaw hooks enable session-memory`
    - `openclaw plugins enable chain-tools`
    - `curl ... /v1/derive_key ...` to derive the runtime wallet and write `BLOCKCHAIN.md`
    - `agent-sidecar run-all`
    - optional `agent-sidecar escrow-decrypt` in bootstrap mode
    - `openclaw gateway`
  - `zeroclaw-instance/entrypoint.sh` runs:
    - `render-blockchain-md`
    - optional `agent-sidecar escrow-decrypt` in bootstrap mode
    - file copies from `.openclaw/workspace` into `.zeroclaw/workspace`
    - `agent-sidecar run-all`
    - `zeroclaw daemon`
  - `hermes-instance/entrypoint.sh` runs:
    - blockchain identity setup and optional `hermes chat -q "Store this in memory: ..."`
    - `agent-sidecar run-all`
    - optional `python3 -u /usr/local/bin/app_driver.py`
    - `hermes gateway run`

#### Sovereign agents

- What `claw-spawner` injects into the exec container:
  - `skill_<n>.md` files downloaded from storage refs
  - `skill_chain.md`
  - `convo_history.jsonl`
  - prior artifacts under `/workspace/artifacts/...`
  - ZeroClaw `config.toml` under `/workspace/.zeroclaw/config.toml`
  - Claude prompt text at `/workspace/.claude_prompt.txt`
  - execution env such as provider API keys, `OPENAI_API_BASE`, `KEY_DERIVATION_URL`, `KEY_DERIVATION_TOKEN`, `AGENT_OWNER_ADDRESS`, and `RPC_URLS`
- What `claw-spawner` extracts from the exec container:
  - `/workspace/artifacts`
  - `/workspace/convo_history.jsonl`
  - run logs are also persisted separately into `/workspace/.logs/...`
- What `claw-spawner` causes to run in the exec container:
  - pre-run setup commands such as:
    - `touch /workspace/.logs/<tx>.log`
    - `mkdir -p /workspace/.zeroclaw`
    - `bash -c <logRotateCommand()>`
  - Claude path:
    - `bash -lc '... cd /workspace && cat /workspace/.claude_prompt.txt | claude ... | tee -a /workspace/.debug/live.log'`
  - Crush path:
    - `bash -lc '... cd /workspace && crush run --quiet --cwd /workspace ... "<prompt>" 2>&1 | tee -a /workspace/.debug/live.log'`
  - ZeroClaw path:
    - `bash -lc '... cd /workspace && zeroclaw agent --config-dir /workspace/.zeroclaw -m "<prompt>" ... 2>&1 | tee -a /workspace/.debug/live.log'`
  - OpenClaw path:
    - `bash -lc 'mkdir -p /workspace/.logs && cd /workspace && ... openclaw agent --local --json --session-id ... --message "<prompt>"'`

### `executor-go` ↔ `claw-spawner` / agent-container surfaces today

#### Persistent path

- For persistent agents, the `executor-go` ↔ `claw-spawner` boundary is mostly a launch-time configuration handoff plus spawn result return; ongoing persistence and runtime behavior are then handled by the launched agent container and sidecar.
- `executor-go` → `claw-spawner` control-plane surface:
  - `executor-go-internal/internal/services/spawn/service.go` sends `POST /instances`
  - request shape is `ClawSpawnerRequest`
  - key agent config fields passed to `claw-spawner`, such as:
    - provider / model / API key
    - runtime identity fields
    - DA fields
    - persistence / restore fields
    - extra env
- Important `extra_env` that `executor-go` passes through toward the runtime:
  - `KEY_DERIVATION_URL`
  - `KEY_DERIVATION_TOKEN`
  - `AGENT_ID`
  - `AGENT_OWNER_ADDRESS`
  - `RITUAL_DKMS_OWNER_ADDRESS`
  - `RPC_URLS`
  - `AGENT_RUNTIME`
  - `AGENT_MODEL_QUALIFIED`
  - `AGENT_PROVIDER`
  - `EXECUTOR_ADDRESS`
  - `RITUAL_ORIGIN_TX_HASH`
  - `RITUAL_ASYNC_JOB_ID`
  - `AGENT_DKMS_INDEX`
  - `AGENT_NAMESPACE`
  - optional MCP telemetry env when enabled
- `claw-spawner` → `executor-go` response surface:
  - `ClawSpawnerResponse`
  - returned fields include:
    - `instance_id`
    - `container_id`
    - `gateway_url`
    - `gateway_token`
    - `status`
    - `da_manifest_cid`
    - `detail`
- `executor-go` uses that response to build the Phase 2 delivery payload back on-chain.

#### Sovereign path

- For sovereign agents, the `executor-go` ↔ `claw-spawner` boundary is a much more active Phase 2 execution surface: `executor-go` uses `claw-spawner` to create or reuse an exec container, inject inputs, run commands inside it, extract outputs, and then release or destroy that container.
- `executor-go` → `claw-spawner` control-plane surface:
  - `executor-go-internal/internal/services/clicontainer/client.go`
  - `executor-go-internal/internal/services/clicontainer/registry.go`
  - HTTP endpoints used:
    - `POST /exec-containers`
    - `GET /exec-containers/{id}`
    - `DELETE /exec-containers/{id}`
    - `POST /exec-containers/{id}/exec`
    - `POST /exec-containers/{id}/inject`
    - `POST /exec-containers/{id}/extract`
- `executor-go` creates / reuses sovereign exec containers with `CreateContainerRequest` fields including:
  - `container_id`
  - `image`
  - `user_address`
  - `cli_type`
  - `env`
  - `labels`
  - `command`
  - `working_dir`
  - `user`
  - memory / CPU settings
- `executor-go` → agent-container file / env surfaces:
  - injects files through `InjectFiles(...)`
  - remotely executes setup and agent CLI commands inside the exec container via `Exec(...)`, e.g. `mkdir -p ...`, `claude ...`, `zeroclaw agent ...`,
  - extracts files through `ExtractFiles(...)`
  - passes runtime env such as:
    - provider API keys
    - `OPENAI_API_BASE` / `OPENAI_API_KEY`
    - `KEY_DERIVATION_URL`
    - `KEY_DERIVATION_TOKEN`
    - `AGENT_OWNER_ADDRESS`
    - `RPC_URLS`
- `executor-go` ↔ agent-container data surfaces specifically include:
  - injected skills
  - injected conversation history
  - injected prior artifacts
  - injected ZeroClaw config
  - injected Claude prompt file
  - extracted artifacts directory
  - extracted `convo_history.jsonl`
  - persisted run logs

### Executor-provided services consumed by agent runtimes today

- The current Docker model has a few distinct executor-local dependencies:
  - key derivation is an executor-local HTTP service that agent runtimes call directly
  - MCP telemetry relay is an executor-local HTTP service that persistent-agent sidecars can call directly when enabled
  - the internal LLM gateway is an executor-local HTTP service used by the sovereign `ritual` provider path
  - health checking is mostly the opposite direction today: `claw-spawner` calls the runtime gateway's `/health`, rather than the runtime calling an executor-local health service
- Key derivation:
  - persistent path: `executor-go-internal/internal/handlers/persistentagent/handler.go` generates an agent-scoped token and `executor-go-internal/internal/services/spawn/service.go` passes `KEY_DERIVATION_URL` / `KEY_DERIVATION_TOKEN` through `extra_env`
  - persistent runtimes and sidecars then call the executor-local DKMS surface for wallet derivation, heartbeat signing, and escrow operations; see `claw-spawner/openclaw-instance/entrypoint.sh` and `claw-spawner/agent-sidecar/cmd/agent-sidecar/main.go`
  - sovereign path: `executor-go-internal/internal/handlers/sovereignagent/handler.go` injects `KEY_DERIVATION_URL` / `KEY_DERIVATION_TOKEN` into the exec container when the key-derivation server is available
  - on the DKMS side, the current mTLS / registry authorization path checks the requestor's on-chain service record and rejects the request unless that service has `HTTP_CALL` capability
- Internal LLM gateway:
  - in the checked current paths, this is primarily a sovereign-agent dependency
  - when the sovereign request uses provider `ritual`, `executor-go-internal/internal/handlers/sovereignagent/handler.go` rewrites `OPENAI_API_BASE` to `http://<executor-internal-hostname>:<port>/v1`
  - that means the sovereign exec container is depending on an executor-local OpenAI-compatible gateway on the shared Docker network
- MCP telemetry relay:
  - `executor-go-internal/internal/services/spawn/service.go` only advertises telemetry env when the executor has actually registered the relay
  - when enabled, persistent-agent sidecars get `MCP_TELEMETRY_ENDPOINT=<key-derivation-base>/v1/mcp/events` and post telemetry back to the executor-local relay; see `claw-spawner/agent-sidecar/cmd/agent-sidecar/main.go`
- Health checking:
  - `claw-spawner/claw_spawner/service.py` waits for the runtime container's internal gateway `/health` to return success before considering the instance healthy
  - so the current health-check dependency is mostly a Docker-network control-plane assumption, not an executor-local helper API that the runtime itself consumes
- Reachability assumption:
  - both persistent and sovereign paths default to an internal hostname like `executor-go-http-1` when constructing executor-local URLs
  - so today these helper surfaces assume shared Docker DNS / networking between the runtime container and executor-local services

### `TEEServiceRegistry` today

- `TEEServiceRegistry` is currently the registry for TEE-backed services such as executors, streaming services, proxies, and DKMS-related services.
- Executors register today through functions like `registerTdxExecutorWithPermit(...)`.
- Registration stores:
  - TEE address
  - payment address
  - endpoint
  - capability
  - workload id
- Main files:
  - `ritual-sc-internal/src/async/TEEServiceRegistry.sol`
  - `ritual-sc-internal/src/async/ITEEServiceRegistry.sol`
- Important current-state observation: the agent runtime is not the main on-chain TEE service in the current design. The executor host is.

## Analysis By Layer


### Contract / async lifecycle layer

- The existing async chain path already gives a useful baseline:
  - factory / harness / launcher
  - scheduler
  - async detection
  - `AsyncJobTracker`
  - `AsyncDelivery`
- The likely change is not replacing that lifecycle wholesale, but deciding which parts stay executor-centric and which parts become agent-TEE-centric.
- Relevant areas:
  - `ritual-sc-internal/src/factory/`
  - `ritual-reth-internal/crates/ritual-async/`

### Executor layer

- `executor-go` is currently the key bridge from on-chain async jobs to runtime launch.
- Persistent and sovereign diverge here:
  - persistent uses `spawn.Service` plus `POST /instances`
  - sovereign uses `clicontainer` exec-container acquisition
- A VM model likely changes this layer more than the on-chain async flow.
- Relevant areas:
  - `executor-go-internal/internal/handlers/persistentagent/`
  - `executor-go-internal/internal/handlers/sovereignagent/`
  - `executor-go-internal/internal/services/spawn/`
  - `executor-go-internal/internal/services/clicontainer/`

### Runtime control-plane layer

- `claw-spawner` is the current control plane for long-lived persistent containers, and is also part of the sovereign short-lived container story through the exec-container API.
- This is the clearest current embodiment of the "something is up and waiting to launch agent work" concept.
- The open mechanical question is whether VM provisioning remains centered here or moves elsewhere.
- Relevant areas:
  - `claw-spawner/claw_spawner/service.py`
  - `claw-spawner/claw_spawner/docker/manager.py`

### Runtime / sidecar layer

- Persistent agents today rely on the agent-sidecar module for heartbeat, DA sync, and recovery-state persistence.
- That sidecar behavior is a likely carry-forward conceptually, but its assumptions about local networking, bootstrap, and registration need re-evaluation in a VM model.
- Relevant areas:
  - `claw-spawner/agent-sidecar/pkg/heartbeat/heartbeat.go`
  - `ritual-sc-internal/src/heartbeat/AgentHeartbeat.sol`

### Networking / local-service layer

- Current assumptions are deeply Docker-shaped:
  - per-instance Docker networks
  - local service reachability over container networking
  - container-scoped health checks
  - executor-local key derivation and internal gateway surfaces
- This is one of the densest unknown clusters for a VM model.

### Local infra layer

- `ritual-node-internal` currently assumes Docker Compose, sidecars, image wiring, and Docker-based agent infrastructure for local bring-up.
- Relevant areas:
  - `ritual-node-internal/Makefile`
  - `ritual-node-internal/configgen/docker.py`

### Production infra layer

- `chain-deployment-infra` currently assumes TDX VMs that host Docker-based workload stacks.
- Relevant areas:
  - `chain-deployment-infra/docs/AGENT_INFRA_RUNBOOK.md`
  - `chain-deployment-infra/docs/PERSISTENT_AGENT_REVIVAL_ARCHITECTURE.md`
  - `chain-deployment-infra/src/7_chain_deploy/tee_deployments/`
  - `chain-deployment-infra/scripts/tee/`

### Observability / operations layer

- Current operational tooling is strongly coupled to Docker:
  - logs
  - stats
  - kill / restart flows
  - health inspection
- Moving to VMs means the operational surface itself needs to be redefined, not just the launch path.

### UX / external workflow layer

- `ritual-dapp-skills` is not present in this workspace, but likely changes if:
  - launch UX changes
  - returned metadata changes
  - agent selection semantics change
  - lifecycle / recovery semantics become more explicit to users
