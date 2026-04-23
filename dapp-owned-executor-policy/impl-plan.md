## Implementation Plan
1. `ritual-sc-internal`: add `CUSTOM` capability and shared-registry support
   Objective:
   Introduce the smallest network-owned hook that lets dapp-owned executors register and remain queryable on the shared `TEEServiceRegistry` without granting dapp write access to network-owned policy state.
   Change:
   Extend `ITEECapabilityPolicy.Capability`, `TEEServiceRegistry`, and related registry interfaces/tests with a `CUSTOM` capability branch; update executor-capability checks, debug-path handling, stored capability/workload reads, and any capability-indexed lookups so `CUSTOM` executors can register and be returned by `getService(...)`.
   Constraints:
   Keep workload-ID derivation shared and deterministic; treat `CUSTOM` as operationally registered in the shared registry, not as a new dapp-governed branch inside the network policy contract; accept breaking enum/interface changes if they are cleaner than compatibility shims.
   Verification:
   Add/update Forge tests proving a `CUSTOM` executor can register in `ValidationMode.NONE`, that registry reads expose the expected capability/workload, and that non-`CUSTOM` flows still pass their existing tests.

2. `ritual-sc-internal`: add the dapp-owned policy contract
   Objective:
   Give `demoDapp` an independent governance surface for its allowed workload identity and executor policy.
   Change:
   Implement the dapp-owned policy contract as a `BasePolicy`-derived contract (with whatever ownership/access-control wrapper is appropriate) so the proof exercises the intended reusable downstream-dapp policy surface. The contract should still record the dapp's allowed `CUSTOM` workload ID and any per-executor allow/deny state the toy flow needs, and it should expose the validation surface the toy dapp calls before dispatching work.
   Constraints:
   Do not require this contract to mutate the network-owned `TEEServiceRegistry` or network-owned `TEECapabilityPolicy`. If adopting `BasePolicy` introduces extra registry/workload-deriver plumbing, approved-workload metadata management, or a broader validation API than the earlier minimal proof sketch, treat that as acceptable scope expansion and flag it explicitly rather than bypassing `BasePolicy`.
   Verification:
   Add Forge tests covering `BasePolicy`-backed workload management, owner-managed policy updates, rejection of wrong workload IDs/capabilities, and successful validation of a correctly registered `CUSTOM` executor.

3. `ritual-sc-internal`: build the toy dapp contract and callback binding checks
   Objective:
   Prove on-chain that a dapp can validate a chosen executor against both the shared registry and dapp-owned policy before creating work, then safely accept the callback.
   Change:
   Add the minimal toy dapp contract that accepts a caller-supplied executor, validates `TEEServiceRegistry.getService(...)` plus the dapp policy, submits the `CUSTOM` async request with a `bytes payload`, stores pending context keyed by `jobId`, and on callback verifies `msg.sender == AsyncDelivery`, checks stored context against canonical `AsyncJobTracker` job data, and only then accepts the echoed result.
   Constraints:
   Keep the contract narrowly focused on executor validation and async result binding; do not add unrelated app behavior or rely on on-chain executor discovery for milestone 1. Because the `CUSTOM` proof keeps flat Phase 2 pricing, the contract/request surface must also enforce a small payload bound instead of allowing arbitrary echoed bytes.
   Verification:
   Add Forge tests for happy-path submission/delivery, wrong-executor rejection, wrong-workload rejection, oversized-payload rejection, and callback spoof/replay/mismatched-job rejection.

4. `ritual-reth-internal`: add the `CUSTOM` async operation, validation, and fee plumbing
   Objective:
   Reuse the existing async transaction pipeline while routing `CUSTOM` work to `CUSTOM` executors instead of network-owned HTTP executors.
   Change:
   Add a dedicated `CUSTOM` async operation path in the relevant `ritual-async`, reader, RPC/builder/verifier, and `ritual-async-fees` code with a minimal codec: reuse the standard async envelope fields the stack already expects, replace HTTP-specific fields with a `bytes payload`, and charge the flat `CUSTOM` executor fee described in the design.
   Constraints:
   Reuse existing async serialization/lifecycle wherever possible; keep contract-side policy enforcement authoritative for executor/workload selection; do not make the entire request opaque if that would break shared extraction of executor, TTL, secrets, or delivery config. The flat-fee proof is only safe if validation also caps the `CUSTOM` payload size to a small, explicit bound shared with the other languages.
   Verification:
   Add/update Rust tests proving the new precompile/operation decodes, maps to `Capability::Custom`, extracts executor/TTL from the shared envelope, computes the expected fee, and passes/fails RPC/builder validation in the expected cases, including oversized-payload rejection.

5. `ritual-go-common`, `ritual-common-internal`, and any shared capability readers: propagate the new capability/precompile constants
   Objective:
   Keep shared enums, address constants, and client-side codecs aligned across Go, Rust, Python, and Solidity call sites.
   Change:
   Update shared registry capability enums/parsers, precompile address constants, and any typed request/response helpers used by executor services or Python tooling so `CUSTOM` is a first-class supported capability/operation everywhere the stack decodes registry or async data; include the new minimal `CUSTOM` request codec and the simple echoed-bytes response shape.
   Constraints:
   Treat ABI/interface drift as a first-class risk; update all consumer libraries that hardcode capability ordinals or precompile addresses before relying on localnet integration results.
   Verification:
   Run the relevant shared-library unit tests and add focused cases showing `CUSTOM` round-trips through string parsing, enum conversion, and typed request construction.

6. `executor-go-internal`: register and serve `CUSTOM` work
   Objective:
   Make a normal executor-go instance able to register as a `CUSTOM` executor and execute the new minimal bytes-payload flow.
   Change:
   Update configuration, registration, and request routing so an executor can advertise `CUSTOM`, survive the local debug registration path, decode the new `CUSTOM` request codec, and return the supplied `bytes payload` back as the async result with no additional business logic.
   Constraints:
   Keep the first implementation intentionally trivial: exercise the codec and async plumbing, not application logic. Keep local testing compatible with `TEE_TYPE=NONE` and the debug capability byte path. Even in the proof slice, the service must still respect the Phase 2 deadline offset and reject payloads above the shared bound so the state machine cannot drift from the validator assumptions.
   Verification:
   Add/update Go tests for capability parsing, codec decode, oversized-payload rejection, deadline-aware Phase 2 activation/expiry, and echo-handler dispatch, then verify an executor started with `CUSTOM` reports itself as registered and returns the same payload bytes through localnet.

7. `ritual-node-internal`: teach localnet bootstrap about the `CUSTOM` demo path
   Objective:
   Ensure localnet can boot, fund, discover, and expose at least one `CUSTOM` executor without manual post-start surgery beyond the intended bootstrap actions.
   Change:
   Update config generation, service discovery, network setup scripts, and any repo-export assumptions so a `CUSTOM` executor instance can be started, funded, discovered, and left registered after `make restart-network`; include the required contract export refresh when `ritual-sc-internal` changes.
   Constraints:
   Follow the existing `ritual-node-internal` workflow: export contract state from `ritual-sc-internal`, rebuild the narrowest needed images, then use `make restart-network` rather than ad hoc container restarts.
   Verification:
   After export/build/restart, confirm `make tee-registry` shows at least one `CUSTOM` executor with the expected workload/capability and that the network setup scripts complete without manual intervention.

8. `traffic-gen-internal` or the chosen thin demo client: implement off-chain discovery and submission
   Objective:
   Reuse the existing client-side executor selection precedent to pick a policy-compliant `CUSTOM` executor and drive the toy dapp end to end.
   Change:
   Add a focused demo flow that queries the shared registry for `CUSTOM` executors, filters them by the dapp-owned workload/policy, submits the toy dapp request with the chosen executor and a test `bytes payload`, and waits for the async callback/result.
   Constraints:
   Keep discovery off-chain for milestone 1; do not turn this into a generalized routing layer or model-pricing integration. The demo should fail fast if the requested payload exceeds the shared proof bound instead of relying on a later on-chain/runtime rejection.
   Verification:
   Add a focused integration script/test that shows candidate discovery, successful request submission, receipt of the same payload bytes back from a valid `CUSTOM` executor, and local rejection of oversized demo payloads.

9. Full local-network proof across the stack
   Objective:
   Validate the intended milestone claim on a fresh localnet, not just in unit tests.
   Change:
   Run the end-to-end sequence: export updated contracts from `ritual-sc-internal`, rebuild affected images/repos, restart from `ritual-node-internal` (prefer `make restart-network vllm_mode=local_mock` unless a different mode is required), deploy/configure the dapp-owned policy and toy dapp, register a `CUSTOM` executor, submit a demo `bytes payload`, and confirm the echoed callback/result is accepted only for policy-compliant executors.
   Constraints:
   Use a fresh network bring-up rather than piecemeal restarts; explicitly check for cross-repo ABI drift if any step returns empty data or capability mismatches.
   Verification:
   Capture the proof with repo-level test output plus localnet checks such as `make status` and `make tee-registry`, and treat the feature as verified only if the runtime proof shows all of the following:
   - invalid executor selection is rejected for policy reasons before a successful callback path can complete
   - a valid executor selection produces a successful submit transaction and emits `CustomJobSubmitted`
   - Phase 1 settles on-chain for that job
   - the executor submits Phase 2 before expiry and the callback transaction is mined
   - the toy dapp emits `CustomResultAccepted`
   - `getDeliveredResult(jobId)` matches the original submitted payload bytes
   - the job is no longer pending after delivery
