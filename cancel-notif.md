Work in `/home/ritual/repos/executor-go-internal`.

Goal: fix the real bug we reproduced in Sovereign Agent Phase 2 execution: the executor->claw-spawner HTTP timeout currently acts as the true runtime cap for agent work, which makes `max_poll_block` largely meaningless in practice for long-running jobs.

What we discovered:
- The relevant timeout is `SOVEREIGN_AGENT_CONTAINER_HTTP_TIMEOUT_SECONDS`.
- Its default is 120 seconds in `internal/config/config.go`.
- That timeout is used to configure the executor's HTTP client for claw-spawner in `internal/services/clicontainer/client.go`, specifically for the HTTP API claw-spawner exposes to manage and exec commands inside agent/exec containers.
- Phase 2 execution currently uses a single blocking HTTP call to claw-spawner: `POST /exec-containers/{id}/exec`.
- Claw-spawner does not stream progress, heartbeat partial status, or provide a pollable exec-job handle for that call. It waits for the Docker exec to finish and then returns stdout/stderr/exit code.
- Because of that architecture, the 120s HTTP timeout is not just a transport timeout. It becomes a hard cap on useful Claude runtime.
- In contrast, `max_poll_block` is supposed to be the chain-level ceiling for how long the Phase 2 job may remain valid before delivery is too late.
- Therefore the layering is backwards today: infrastructure timeout fires before the protocol deadline, even when the agent is still doing useful work.

Concrete reproduction evidence:
- On localnet, we restarted the network, deployed `ritual-rep`, configured `cliType=0`, and lowered `MAX_TURNS` from 12 to 4.
- Even with `maxTurns=4`, the job still hit the 120s boundary.
- The request/job id was:
  `0x6c323787746f315d3315e6a172db7f5836d282abde192e69e2c78ab6c07cee62`
- Phase 2 started at `2026-04-21T15:25:08Z`.
- Executor failed at `2026-04-21T15:27:09Z` with:
  `sovereign agent execution failed: request failed: Post "http://claw-spawner:8000/exec-containers/sovereign-91d29b25fcd6e0bb/exec": context deadline exceeded (Client.Timeout exceeded while awaiting headers)`
- The agent was still actively working inside the container during that interval. It was not dead or stuck before first output.
- The failure was delivered on-chain and surfaced in `ritual-rep` as a `ScanFailed` event in tx:
  `0xb2c18c9b7de7bbbc10a54eba2b2ccaaa8c74fb84a15956db1de4e87087971b4d`
- That means the HTTP-timeout error path is already user-visible on-chain. The deeper problem is that this timeout prevents `max_poll_block` from being the real limit.

Why this is a bug:
- `max_poll_block` is intended to define the maximum allowed job lifetime from the chain/protocol perspective.
- But in practice, long-running agents never get close to that ceiling because the 120s executor->spawner timeout kills them first.
- There does not appear to be a useful long-running-job purpose for this timeout in its current form, because there is no multi-call monitoring design behind it.
- If the system had async exec plus status polling, or streaming/heartbeat support, then an HTTP timeout on any single call would make sense.
- But with one blocking `/exec` call, this timeout just truncates valid work.

Preferred direction:
1. Remove or neutralize the executor->spawner HTTP timeout as the effective Phase 2 runtime cap.
2. Make `max_poll_block` the real deadline for long-running Sovereign Agent work.
3. Preserve timeout protection only where it is actually useful:
   - short control-plane calls like create/get/inject/delete
   - not the long-running Phase 2 exec itself
4. If there is a strong reason to keep a timeout on Phase 2 exec, it must no longer be shorter than the intended useful-runtime window, and it must not silently override `max_poll_block`.

Suggested implementation direction:
- Start in:
  - `internal/services/clicontainer/client.go`
  - `internal/services/clicontainer/registry.go`
  - `internal/handlers/sovereignagent/handler.go`
  - `internal/services/sovereignexec/service.go`
- Inspect how `SOVEREIGN_AGENT_CONTAINER_HTTP_TIMEOUT_SECONDS` is wired into the claw-spawner client.
- Change the long-running exec path so Phase 2 is not capped by that HTTP client timeout.
- A reasonable first implementation is to stop applying the short HTTP timeout to the blocking `/exec` request and rely on the existing Sovereign Agent runtime / chain deadline controls instead.
- If needed, split timeouts by operation type:
  - keep short HTTP timeouts for create/get/inject/delete
  - allow long-running or no client timeout for `/exec`
- Do not change contract ABI unless absolutely necessary.

Secondary note:
- There is still a separate bug where pure `max_poll_block` cancellation currently returns silently instead of delivering an on-chain error.
- But that is no longer the primary issue for this task.
- First fix the architectural bug where the 120s HTTP timeout prevents long-running jobs from ever reaching the intended chain-level deadline behavior.

Acceptance criteria:
- A Sovereign Agent Phase 2 run is no longer effectively capped at 120s by the executor->spawner HTTP client timeout.
- `max_poll_block` becomes the real practical ceiling for long-running jobs, or at minimum the exec path no longer times out earlier for normal healthy runs.
- The existing reproduced localnet flow can run past 120s without failing at the HTTP boundary.
- Existing error delivery for true execution failures is not regressed.
- Add focused tests if there is a reasonable place to do so. At minimum, document the timeout separation clearly in code comments or config naming if behavior changes.