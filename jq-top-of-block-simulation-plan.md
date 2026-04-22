## Design Plan
- Goal: make top-of-block / parent-state simulation execute `jq` correctly, preserve correct behavior when `jq` composes into an async precompile call, and avoid turning parallel simulation into a single-file queue behind the current `jq` worker lock.
- Explicit PR goal: align `jq` with the same class of context-aware simulation behavior already used by `ONNX`, so simulation handling is explicit and mode-aware rather than silently degrading to empty or incorrect values.
- Problem definition: the failing pipeline shape is `sync_precompile -> async_operation`, specifically `jq -> http`, where the synchronous precompile output is expected to become the async operation input during simulation / transaction construction.
- Observed behavior: when `jq` executes before an async operation, the `jq` output is not propagated correctly and the downstream async operation can receive empty or otherwise incorrect input, which then causes request failure or invalid downstream behavior.
- Hypothesized root cause: the input-generation / simulation path used for async operations is not executing `jq` in the same effective execution context as real transaction execution, so `jq` is either skipped, evaluated too early/late, or collapsed to empty output.
- Failure mode: `onchain_data -> jq -> async_call(input)` becomes `onchain_data -> (jq not applied correctly) -> async_call(empty_or_bad_input)`.
- Required invariant: for any pipeline `sync_precompile -> async_operation`, the system must guarantee `async_operation.input == output(sync_precompile)` under simulation as well as under actual execution.
- System boundary: the affected surface includes synchronous precompiles (`jq` confirmed, others possible), async precompiles / external-call paths such as HTTP, and the simulation / input-generation layer that constructs async payloads before inclusion.
- Primary fix direction: ensure synchronous precompiles are executed during simulation / input construction, their outputs are materialized, and those outputs are passed forward into downstream async input construction.
- Primary implementation targets: the simulation engine, the precompile execution hooks/dispatch used by simulation, and the input builder that constructs payloads for async calls.
- Main workstreams: align simulation EVM wiring with the same Ritual precompile set used in real execution; make `jq` return real simulated outputs in jq-before-async flows; decide whether simulation should keep using the single worker or use a simulation-specific execution path; add regression coverage at unit/integration/e2e layers.
- Key decisions: treat `jq` as a normal precompile that must execute during simulation, not as an async precompile to be detected by `AsyncPrecompileInspector`; keep parent-block simulation semantics unchanged; align `jq` with `ONNX` at the policy level by making simulation behavior explicit and context-aware; keep consensus execution and simulation execution policy separable if that is the cleanest way to preserve both correctness and throughput.
- Prioritization: Phase 1 is correctness of simulation execution and output propagation; Phase 2 is preserving or improving simulation parallelism once correctness is restored.
- Required regression matrix:
  - Case A: `jq -> http`, where HTTP input must equal JQ output.
  - Case B: `jq -> onyx -> http`, where HTTP input must reflect the full upstream transformation chain.
  - Case C: `http -> jq`, used as a control / baseline case.
  - Case D: `jq -> jq -> http`, where chained synchronous transformations must compose before the async call.
- Dynamic verification gate:
  - Verification must be demonstrated dynamically, not just by static code inspection.
  - First prove the bug on untouched `dev` using either a focused test harness or a live local-network run.
  - Then switch to the candidate fix branch and rerun the exact same procedure.
  - Success requires an observed behavior change under the same transaction shape, same verification method, and same interpretation criteria.
- Old-`dev` reproduction criteria:
  - Preferred reproduction shape is the real `jq -> http` composition used by the traffic-gen harness.
  - Acceptable proof on old `dev` is either:
    - a deterministic automated test that exercises the builder/detector path and the validator re-simulation path, or
    - a deterministic local-network procedure that submits the composition transaction and captures node logs for both paths.
  - The old-version run must show a mismatch for the same origin transaction: detector / top-of-block-style simulation identifies the async HTTP call, while validator-side re-simulation fails to observe the equivalent async call or equivalent propagated input.
  - The reproduction notes must record the exact branch, tx shape, commands used, relevant tx hash(es), and the log or test assertions that prove the mismatch.
- Primary dynamic verification procedure:
  - Use the local-network reproduction as the main verification path unless a smaller automated test proves the same detector-versus-validator mismatch.
  - On untouched `dev`, run:
    - in `ritual-node-internal`: `make build-reth`
    - in `ritual-node-internal`: `make restart-network`
    - in `traffic-gen-internal`: `make run-jq-then-http`
  - After the transaction is submitted, inspect the exact live-chain replay context with:
    - `cast tx 0x4d7ce20afcc215152fdb3c660c7625207f2a5e0bd2e87d6ae79a50ced4d9596b --rpc-url http://127.0.0.1:8545 --json`
    - `cast rpc eth_getRawTransactionByHash 0x4d7ce20afcc215152fdb3c660c7625207f2a5e0bd2e87d6ae79a50ced4d9596b --rpc-url http://127.0.0.1:8545`
    - `cast block 0x51 --rpc-url http://127.0.0.1:8545 --json`
    - `cast code 0x84739894B41477fF6849621bB4C275A4C138E39C --rpc-url http://127.0.0.1:8545`
  - Then trace the node logs for the exact origin transaction and generated commitment tx hashes. Search for:
    - `0x4d7ce20afcc215152fdb3c660c7625207f2a5e0bd2e87d6ae79a50ced4d9596b`
    - validator messages like `Validating async commitment at parent block`
    - failure messages like `No async call detected in simulation`
  - The old-`dev` run is considered a bug reproduction only if it shows both:
    - detector / top-of-block-style simulation identified the async HTTP call for the origin tx, and
    - validator-side re-simulation for the same origin tx logged `Transaction simulation completed success=false` and `No async call detected in simulation`, or an equivalent mismatch in propagated async input.
- Fix-branch verification criteria:
  - Rerun the same dynamic reproduction on the fix branch without changing the transaction shape or success criteria.
  - The fix is verified only if the old mismatch disappears: the relevant simulation entry points agree on async detection and the downstream HTTP input reflects the upstream `jq` output.
- Risks and dependencies: the relevant behavior is split across `ritual-reth-nodebuilder-internal` for `jq` and custom precompiles, `ritual-reth-internal` for async/top-of-block simulation, and likely `ritual-node-internal` for end-to-end validation; any simulation-only fast path must preserve observable semantics for success, revert, timeout, and verification-unavailable cases.

## Ambiguities To Resolve
- None blocking for a jq-first implementation plan. Assumption: phase 1 fixes `jq` first, then audits other similar precompiles for parity rather than broadening the initial code change.

## Implementation Plan
1. `ritual-reth-internal`: trace and fix simulation precompile parity
   Objective:
   ensure every top-of-block / async simulation entry point executes against the same Ritual precompile registration used by the node at runtime.
   Change:
   audit the simulation engine callers in `ritual_async::detector`, payload-builder async collection, and any verifier path that re-simulates transactions; confirm they are all using the nodebuilder-backed `EthEvmConfig<RitualEvmFactory>` path rather than a plain `EthEvmConfig` that would miss `RitualPrecompiles`, and fix any mismatched constructor or generic wiring so sync precompiles execute during simulation.
   Constraints:
   preserve parent-header state simulation and do not touch the duplicate `ritual-reth-internal-pr341` tree unless explicitly requested.
   Verification:
   add a focused test that simulates a transaction touching `0x...0803` and proves the `jq` precompile is actually invoked during simulation instead of being skipped or treated as empty output.

2. `ritual-reth-nodebuilder-internal`: make `jq` simulation semantics match real execution
   Objective:
   remove the dummy/zero-output behavior for jq-before-async compositions during simulation.
   Change:
   update the precompile execution hooks/dispatch used by simulation so the real `jq` logic runs, materialize the resulting sync-precompile outputs, and ensure the async input builder consumes those materialized values when constructing downstream async-precompile inputs; make this mode-aware and explicit in the same way `ONNX` is mode-aware today, while keeping jq-specific execution mechanics; explicitly cover `jq -> http`, `jq -> onyx -> http`, `jq -> jq -> http`, plus control cases where async work happens first, so simulation and execution agree on outputs and classification.
   Constraints:
   `jq` should execute during simulation without being added to the async-precompile detector list unless a separate product requirement says it should produce an async commitment itself.
   Verification:
   add unit or integration tests showing that a transaction whose async payload depends on prior `jq` output simulates with the same non-zero decoded value that real execution sees.

3. `ritual-reth-nodebuilder-internal` and `ritual-reth-internal`: decide the simulation-only `jq` execution path
   Objective:
   Phase 2: keep parallel top-of-block simulation meaningfully parallel once correctness is fixed.
   keep parallel top-of-block simulation meaningfully parallel even when many candidate transactions call `jq`.
   Change:
   compare two designs and pick one: simulation-only local in-process `jaq` execution, or a dedicated simulation worker pool with more than one slot and no shared single-slot bottleneck; document the chosen policy and wire it only into simulation if consensus execution must remain isolated behind the worker.
   Constraints:
   do not weaken the safety/isolation guarantees of real block execution; simulation-only behavior must still preserve the same functional outputs and timeout/error surface expected by builder, RPC, and verifier code.
   Verification:
   benchmark N parallel simulated `jq` transactions and show measurable wall-clock improvement over the current `slots[0]`-serialized path, with no regression in timeout/error handling tests.

4. `ritual-reth-internal`: keep builder, RPC, and verification behavior aligned
   Objective:
   avoid fixing one simulation entry point while another still returns stale or zeroed behavior.
   Change:
   add a shared regression matrix around the existing async simulation APIs so payload builder async collection, RPC validation, and any verification re-simulation all agree on `jq`-composed transactions.
   Constraints:
   keep the test surface focused on the behavior that actually regressed instead of introducing broad low-signal coverage.
   Verification:
   one test per entry point showing identical classification and payload extraction for each required pipeline shape: `jq -> http`, `jq -> onyx -> http`, `http -> jq`, and `jq -> jq -> http`.

5. `ritual-node-internal`: add local-network regression coverage
   Objective:
   prove the end-to-end workflow works in the real node configuration.
   Change:
   add an e2e that submits a transaction where `jq` runs before an async precompile, then validates that admission/top-of-block simulation and eventual block execution agree on the derived async payload/result; use this same flow as the branch-to-branch comparison harness so old `dev` and the fix branch are evaluated with the same dynamic procedure.
   Constraints:
   keep it deterministic and runnable through the normal local-network flow.
   Verification:
   run the local-network test from `ritual-node-internal` on untouched `dev`, capture the tx hash, raw tx, parent block, deployed harness code, and detector/validator log evidence showing the mismatch, then rerun unchanged on the fix branch and confirm the mismatch is gone and the propagated HTTP input matches the `jq` output.

6. PT1 fallback documentation
   Objective:
   keep users unblocked if the full code fix or simulation parallelism work slips.
   Change:
   document the temporary guidance discussed in eng sync: place `jq` after the async operation, or assume zero-valued precompile outputs during simulation.
   Constraints:
   mark it as a workaround and remove or narrow it once the fix is merged.
   Verification:
   docs note is present in the relevant operator/developer docs and references the limitation clearly.
