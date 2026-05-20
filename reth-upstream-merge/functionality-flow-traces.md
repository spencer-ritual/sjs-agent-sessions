# Ritual Functionality Flow Traces For Upstream Merge

Date: 2026-05-05

Purpose: turn product-facing deployment traffic and dApp guide behavior into an explicit retention checklist for the Reth v2.2.0 upstream port. Treat this as working context, not a replacement for source-level audit.

Sources:

- `design.md`: merge working set, upstream target versions, and repo strategy.
- `feature-preservation-map.md`: existing invariant batches and likely code surfaces.
- `merge-principles.md`: port behavior onto upstream architecture; do not preserve old file layout for its own sake.
- `chain-deployment-infra/quick_deploys/gold_standard.sh`: main deployment and traffic inventory.
- `https://github.com/ritual-foundation/ritual-dapp-skills`: user-facing guide, especially agent, async, scheduler, secrets, X402, and precompile semantics.

## How To Use This File

For each flow, preserve four things:

1. The user-visible behavior and API contract.
2. The internal work trace through transaction admission, block building, execution, settlement, verification, and operator/RPC surfaces.
3. The consensus or persistence boundary where compatibility matters.
4. A focused validation that proves the behavior survived the port.

During the upstream merge, use this file to ask:

- Which upstream v2.2.0 extension point should own this behavior now?
- Which Ritual invariant must be re-applied there?
- Which cheap test proves the invariant before wider localnet validation?
- Which end-to-end traffic item in the gold standard should cover the final integration gate?

## Source Inventory

The gold standard traffic config currently describes these workloads:

- `llm_call`
- `token_transfer`
- `http_call`
- `onnx_inference`
- `swap`
- `jq_query`
- `ed25519_verify`
- `scheduled_onnx_inference`
- `long_running_echo`
- `x402_dkms_scheduled`
- `private_io`
- `delegate_secret`
- `llm_call_streaming`
- `x402_dkms_http_call`
- `x402_dkms_long_running_http`
- `zk_two_phase`
- `scheduled_zk_two_phase`
- `sequencing_rights_simple`

Note: the script banner says "19 standard workloads", but the `my_traffic.json` workload array currently lists 18 entries. Treat that as a small deployment-doc drift to resolve separately, not as evidence of a missing Reth feature by itself.

The script also enables or configures:

- Summit consensus by default, with chain-driver as an alternate path.
- `NUM_PHALA_EXECUTOR=1` for LLM/agent calls and `NUM_PHALA_ZK_EXECUTOR=1` for ZK.
- GCP TDX executor capacity.
- Mock proxy mode by default, with shared real GLM proxy mode available.
- dKMS mode.
- GCS data availability for LLM multi-turn history and multimodal/persistent data.
- Reth env vars: `SKIP_VALIDITY_CONSTRAINTS` and `RITUAL_FORCE_CONTRACT_SCAN`.
- Streaming service.
- Agent orchestrator sidecar.

The dApp guide adds important functionality that is not obvious from the gold standard traffic names:

- Persistent Agent precompile `0x0820`.
- Sovereign Agent precompile `0x080C`.
- Factory-backed agent deployment through deterministic child harnesses/launchers.
- Persistent-agent heartbeat, revival, DA-backed state, DKMS-derived identity, and operator channels.
- Multimodal precompiles `0x0818`, `0x0819`, `0x081A`.
- Passkey / P-256 behavior through `SECP256R1` and TxPasskey `0x77`.
- Frontend/backend expectations around `spcCalls`, sender locks, long-running callbacks, and async state machines.

## Base Execution Traces

These are the reusable flow skeletons. The workload traces below should reduce to one or more of these.

### Sync Precompile Trace

Applies to: ONNX, JQ, Ed25519, SECP256R1, TX Hash.

Work trace:

1. User transaction enters RPC/txpool as a normal EVM transaction.
2. Block builder includes it like any other transaction.
3. EVM execution calls the native precompile inline.
4. Result is returned inside the same EVM frame.
5. Verifier re-executes the block and must get the same result.
6. Receipt/log/storage effects are normal EVM effects.

Retain:

- No async commitment or settlement transaction.
- Multiple sync precompile calls per transaction remain allowed.
- Deterministic gas/accounting and output encoding remain stable.
- Any custom JQ output wrapping and ONNX/Ed25519 ABI formats remain compatible with shipped dApps.

Merge pressure points:

- `ritual-revm-internal` precompile registration and execution.
- `ritual-alloy-evm-internal` EVM interface and env conversion.
- `ritual-reth-internal` EVM factory wiring and block verification.

Validation:

- One unit or integration fixture per sync precompile.
- Builder-produced block imported by verifier with the same outputs.

### Short-Running Async SPC Trace

Applies to: HTTP, LLM, DKMS, X402 over HTTP.

Work trace:

1. User submits a transaction containing one short-running async precompile call.
2. RPC may simulate pending state for user feedback, but builder/verifier authority is parent-state validation.
3. Builder simulates the transaction against parent state and detects the async call.
4. Builder inserts `TxAsyncCommitment` (`0x11`) and records the job in `AsyncJobTracker`.
5. Original user tx is deferred rather than executed normally.
6. Executor sees the job, runs in TEE, signs/submits result through Ritual RPC.
7. Builder with the result re-executes the original tx with SPC output injected.
8. Same block includes the fulfilled user tx plus `TxAsyncSettlement` (`0x12`).
9. Fees are distributed and job state is removed.
10. Receipt exposes Ritual `spcCalls` so clients can decode settled output.

Retain:

- At most one short-running async precompile per user transaction.
- SPC capture contains original precompile address, input, output, proof/signature context, and block context.
- The fulfilled user tx and settlement are in the same block.
- RPC, builder, and verifier agree on validation, TTL, model/registry, wallet lock, sender lock, and payload-size rules.
- User-facing errors remain descriptive enough for invalid payloads.

Merge pressure points:

- Async detection and validation.
- EVM async context and SPC capture.
- Txpool async pool and sender locks.
- Payload builder commitment/fulfilled ordering.
- Block verifier fail-closed checks.
- RPC submission methods and receipt extensions.

Validation:

- One valid short async flow for HTTP and LLM.
- One invalid case each for TTL, sender lock, insufficient wallet, malformed payload, and unavailable registry/model/executor.
- Receipt check proving `spcCalls` survives the port.

### Long-Running Two-Phase Trace

Applies to: Long HTTP, ZK, sovereign agent, persistent agent, multimodal.

Work trace:

1. User submits a transaction containing a long-running async precompile call.
2. Phase 1 mines the user transaction and returns a task/job id, not final output.
3. Builder inserts `TxAsyncCommitment` (`0x11`).
4. Executor runs/polls/generates off-chain in TEE.
5. Sender lock is released after Phase 1 settlement, so user can submit later work.
6. Executor submits delivery result.
7. Chain includes `TxAsyncSettlement` (`0x12`) or delivery transaction that calls `AsyncDelivery.deliver`.
8. `AsyncDelivery` invokes the configured callback on `deliveryTarget` using `deliverySelector`.
9. `AsyncJobTracker` marks delivered or removes/expires the job.

Retain:

- Phase 1 receipt is not final result.
- Callback `msg.sender` is `AsyncDelivery`, not the original executor or user.
- Callback ABI is `(bytes32 jobId, bytes result)` for long-running consumer patterns.
- TTL, delivery gas, delivery fee, max poll/spawn/deadline, and wallet lock validation remain fail-closed.
- Job id semantics remain stable; clients must not need to derive callback ids from external task ids.

Merge pressure points:

- Long-running payload validation.
- Async pool Phase 1/Phase 2 state transitions.
- Delivery-ready pool and settlement inclusion.
- `AsyncDelivery` system contract interactions and verifier checks.
- RPC/operator result submission.

Validation:

- Happy path callback test.
- Missing/incorrect callback selector test.
- Delivery gas too low or callback revert test.
- Expiry path where no callback is delivered and state is cleaned up.

### Scheduled Execution Trace

Applies to: scheduled ONNX, scheduled ZK, scheduled X402, recurring sovereign harness windows, heartbeat/revival triggers.

Work trace:

1. Contract schedules a call through the Scheduler; EOAs cannot schedule directly.
2. Scheduler stores call metadata: target, calldata, start block, frequency, TTL, num calls, payer, predicate.
3. At eligible block, builder hydrates scheduled state and evaluates due calls.
4. If predicate exists, builder `staticcall`s `shouldExecute`; false/revert/out-of-gas skips the call for that block.
5. Builder injects real `executionIndex` into calldata bytes 4-35.
6. Builder inserts `TxScheduled` (`0x10`) from system sender.
7. If the scheduled call triggers async work, the normal async lifecycle starts from that scheduled transaction.
8. Verifier enforces the same C1-C11 scheduled constraints and predicate outcome.
9. Scheduler marks execution consumed/completed/expired as appropriate.

Retain:

- Scheduler TTL for scheduled async covers the replayed scheduled execution at settlement time.
- For long-running two-phase precompiles, Scheduler TTL constrains Phase 1 replay, not Phase 2 delivery.
- Scheduled async bypasses the normal EOA sender lock but still has per-block duplicate controls.
- Predicate behavior is builder/verifier consensus behavior, not best-effort local logic.
- `frequency * numCalls <= MAX_LIFESPAN` remains enforced where shipped.

Merge pressure points:

- Scheduler canonical hydration.
- Payload-builder scheduled augmentation.
- Scheduled tx validation/exemptions in txpool and verifier.
- Predicate evaluation gas limits and fail-closed semantics.

Validation:

- One due scheduled sync tx.
- One false predicate skip.
- One scheduled async settlement inside Scheduler TTL.
- One scheduled async settlement after Scheduler TTL that is rejected.
- One scheduled long-running Phase 2 delivery after Phase 1 succeeds.

### Secret, Private Output, And dKMS Trace

Applies to: X402, private I/O, delegated secrets, persistent-agent DA/state, DKMS scheduled flows.

Work trace:

1. Client selects executor from `TEEServiceRegistry` and gets the executor public key.
2. Client ECIES-encrypts JSON secrets to the executor key using Ritual's 12-byte nonce format.
3. Client signs each encrypted blob.
4. Transaction includes `encryptedSecrets`, `secretSignatures`, and optionally `userPublicKey`.
5. Executor decrypts inside TEE.
6. Executor substitutes secret placeholders into URL/header/body/runtime config, or uses dKMS-derived material.
7. Optional private output is encrypted to `userPublicKey`.
8. Delegated flows check `SecretsAccessControl` when signer does not match the transaction origin.
9. Result is settled via short async SPC or long-running callback, depending on precompile.

Retain:

- 12-byte ECIES nonce compatibility.
- Secret signature verification and delegation checks.
- Template substitution behavior when `encryptedSecrets` is non-empty.
- `userPublicKey` output encryption behavior.
- `SecretsAccessControl` grant/revoke/check semantics.
- DKMS key derivation and payment-address funding behavior used by X402 and persistent agents.

Merge pressure points:

- Async payload validation.
- Executor-facing ABI compatibility.
- Registry/wallet checks.
- Fee settlement and secret-related error propagation.

Validation:

- Secret substitution in HTTP request.
- Wrong signature/delegation denied path.
- Private output decryptable only by user key.
- dKMS-derived address funded and used by a dependent flow.

## Workload Traces

### `token_transfer`

Work trace: standard value or ERC20-style transaction enters RPC/txpool, is ordered by builder, executes in EVM, updates balances/storage/logs, and replays under verifier.

Retain:

- Standard EVM transaction semantics must not be disturbed by custom async/scheduled pool changes.
- Nonce, balance, gas, receipt, and storage behavior remain upstream-compatible except where Ritual explicitly changes economics.
- Async sender locks or scheduled exemptions must not accidentally affect plain transfers.

Merge surfaces:

- Txpool validation.
- Payload ordering.
- EVM execution.
- Receipt/storage codecs.

Validation:

- Plain transfer localnet smoke test before and after async-heavy blocks.

### `swap`

Work trace: standard contract interaction uses normal calldata, storage, events, token transfers, and possibly external router/pool contracts. It should be unaffected by Ritual precompile machinery unless the swap contract itself calls a precompile.

Retain:

- Normal contract calls stay compatible with upstream Reth execution.
- Logs and receipts remain indexer-compatible.
- Payload builder ordering/demotion does not break regular tx inclusion around system transactions.

Merge surfaces:

- EVM execution/gas accounting.
- Payload collection and ordering.
- Receipt/log encoding.

Validation:

- Swap tx succeeds in a mixed block containing regular, scheduled, and async system txs.

### `http_call`

Work trace: short-running async HTTP precompile `0x0801`; executor performs HTTP request in TEE; fulfilled replay injects HTTP response; result appears in `spcCalls`.

Retain:

- HTTP ABI layout and method enums.
- Executor selection by `HTTP_CALL` capability.
- URL/header/body validation, input-size limits, TTL, wallet lock, and sender lock.
- SPC result encoding for `(status, headers, body, errorMessage)`.

Merge surfaces:

- Async detector/validation.
- EVM precompile dispatch.
- Txpool async state.
- Payload builder fulfilled replay.
- RPC receipt extension.

Validation:

- Simple GET/POST response decoded from `spcCalls`.
- Invalid URL and expired TTL rejected before/at commitment as expected.

### `llm_call`

Work trace: short-running async LLM precompile `0x0802`; builder detects LLM request; executor routes to mock or shared GLM proxy; fulfilled replay injects response; receipt exposes `spcCalls`.

Retain:

- Model registry and pricing checks.
- Current production model path for `zai-org/GLM-4.7-FP8`, plus mock-model behavior in mock proxy deployments.
- Error envelope semantics: `has_error` can be true even when chain settlement succeeds.
- Conversation history DA refs and model metadata encoding.
- PII and streaming incompatibility constraints where applicable.

Merge surfaces:

- Async validation.
- Model pricing/registry readers.
- Wallet fee escrow and settlement.
- SPC receipt format.
- Deployment proxy wiring in `chain-deployment-infra` and executor services.

Validation:

- Mock LLM call in gold standard.
- Shared proxy mode call with proxy health/registration when `USE_MOCK_PROXY=false`.
- Overlarge/invalid model request returns expected error envelope without corrupting chain state.

### `llm_call_streaming`

Work trace: LLM precompile request sets `stream=true`; on-chain async settlement proceeds normally; streaming service separately authenticates an SSE request by transaction hash/signature and streams tokens while final result still settles on-chain.

Retain:

- Streaming is additive; final on-chain result still arrives if SSE fails.
- SSE auth is tied to submitted transaction and EIP-712 stream request.
- `stream=true` must be set in ABI before clients connect.
- PII mode is incompatible with streaming.
- Executor capability/config errors surface in on-chain LLM result even if SSE hangs.

Merge surfaces:

- LLM ABI validation.
- Receipt `spcCalls`.
- Streaming service deployment flag and executor/proxy path.
- RPC/receipt availability for stream auth.

Validation:

- Stream tokens from service and also decode final receipt result.
- Verify non-stream request does not produce a useful SSE stream.

### `onnx_inference`

Work trace: synchronous ONNX precompile `0x0800` executes inline inside the user's transaction and returns deterministic model inference output.

Retain:

- ONNX ABI field layout.
- Deterministic execution/gas behavior.
- No executor, commitment, settlement, sender lock, or callback.

Merge surfaces:

- revm precompile registration.
- EVM factory wiring.
- Block verification replay.

Validation:

- Known input/output fixture in a block imported by verifier.

### `jq_query`

Work trace: synchronous JQ precompile `0x0803` transforms JSON inline, often as post-processing for HTTP/long-running results.

Retain:

- JQ ABI and output unwrapping/double-indirection behavior expected by dApps.
- Multiple sync calls can execute in the same transaction.
- JQ can run during fulfilled replay after a short-running async result is injected.

Merge surfaces:

- revm precompile registration.
- SPC fulfilled replay EVM context.
- Gas/accounting consistency.

Validation:

- Plain JQ fixture and HTTP-plus-JQ fulfilled replay fixture.

### `ed25519_verify`

Work trace: synchronous Ed25519 precompile `0x0009` verifies signature inline and returns boolean/result bytes.

Retain:

- ABI field order and accepted key/signature/message formats.
- Determinism and gas accounting.

Merge surfaces:

- revm precompile registration.
- EVM execution and verifier replay.

Validation:

- Valid and invalid signature fixtures.

### `scheduled_onnx_inference`

Work trace: Scheduler creates a future/recurring call; builder inserts `TxScheduled`; scheduled callback invokes sync ONNX; verifier enforces the same scheduled constraints.

Retain:

- Contract-only scheduling.
- `executionIndex` calldata injection.
- Payer/RitualWallet semantics for scheduled execution.
- Scheduler state transitions and C1-C11 constraints.
- Predicate skip behavior if the workload adds predicates.

Merge surfaces:

- Scheduling crate.
- Txpool scheduled subpool.
- Payload scheduled augmentation.
- Block verifier scheduled checks.

Validation:

- One due ONNX scheduled tx executes.
- One expired or predicate-false scheduled tx is skipped.

### `long_running_echo`

Work trace: Long HTTP precompile `0x0805` submits an external echo job, returns task id in Phase 1, executor polls until complete, then delivers result to contract callback through `AsyncDelivery`.

Retain:

- 35-field ABI layout.
- Poll interval, max poll block, task-id marker, status JQ, result JQ, and delivery config.
- Callback authorization by `AsyncDelivery`.
- Delivery failure/lost-result behavior if callback reverts.

Merge surfaces:

- Long-running validation.
- Async delivery pool.
- Result submission RPC.
- Verifier settlement checks.

Validation:

- Echo callback received.
- Wrong selector or low delivery gas produces expected delivery failure event.

### `x402_dkms_http_call`

Work trace: X402 uses HTTP precompile `0x0801` with encrypted payment credentials; executor decrypts in TEE, substitutes secret placeholders, calls paid API, and settles inline through SPC.

Retain:

- Same HTTP ABI plus populated `encryptedSecrets`, `secretSignatures`, and PII/template-substitution flag.
- Payment credentials never appear on-chain.
- dKMS/shared credential path remains compatible where deployment uses `--dkms-mode enabled`.
- HTTP 401/402/API errors settle as response payloads, not consensus failures.

Merge surfaces:

- Secret validation/delegation.
- HTTP async validation.
- Wallet fees and executor fee settlement.
- DKMS precompile/service availability.

Validation:

- Placeholder substitution success.
- Missing secret placeholder returns expected error response.
- Wallet underfunded path rejected.

### `x402_dkms_long_running_http`

Work trace: X402 credential handling plus Long HTTP `0x0805`; Phase 1 submits paid/polling job; Phase 2 delivers callback after executor polling and result extraction.

Retain:

- All X402 secret rules.
- All long-running callback and timeout rules.
- No on-chain retry if credentials expire or poll endpoint fails.
- Duplicate external job risk on resubmission after timeout remains understood.

Merge surfaces:

- Long-running validation.
- Secret/delegation validation.
- Delivery settlement.
- Operator result submission.

Validation:

- Paid long-running callback received.
- Expired credentials or bad placeholder results in no/dropped delivery as currently specified.

### `x402_dkms_scheduled`

Work trace: Scheduler triggers a contract callback that invokes an X402 HTTP/long-running path. If short async, Scheduler TTL must cover the replayed scheduled execution at settlement. If long-running, Scheduler TTL covers Phase 1 replay while Phase 2 delivery is separate.

Retain:

- Scheduled payer approval and wallet funding.
- Scheduled async sender-lock exemption.
- Secret access/delegation checked for scheduled caller/origin semantics as shipped.
- Scheduler TTL vs async TTL distinction.

Merge surfaces:

- Scheduler builder/verifier hooks.
- Async validation for scheduled txs.
- Secret signer/delegate semantics.
- Wallet/payer accounting.

Validation:

- Scheduled X402 fires and settles.
- Tight Scheduler TTL failure.
- Delegate or secret access denied path.

### `private_io`

Work trace: client supplies `userPublicKey`; executor encrypts output so only holder of the corresponding private key can decrypt; result is delivered through SPC or callback depending on precompile.

Retain:

- User public-key field behavior.
- Private output encryption format.
- Interaction with `encryptedSecrets` and PII/template substitution.
- Clients can detect encrypted payloads and decrypt off-chain.

Merge surfaces:

- Async payload validation.
- Executor-facing ABI compatibility.
- Result encoding in SPC/callback.

Validation:

- User key decrypts result.
- Wrong key cannot decrypt result.

### `delegate_secret`

Work trace: secret owner encrypts credentials and grants delegate access through `SecretsAccessControl`; delegate submits request with encrypted secret; executor recovers signature signer, checks delegation if signer differs from tx origin, and either decrypts or denies.

Retain:

- `SecretsAccessControl` grant/revoke/check contract address and ABI expectations.
- Secret hash calculation over encrypted blob.
- Signature over raw encrypted bytes.
- Denied access produces the shipped executor response behavior, not silent success.

Merge surfaces:

- Secret validation and executor request payload.
- RPC/tx origin context preservation for async precompile validation.
- System contract deployment assumptions.

Validation:

- Grant allows delegate call.
- Revoke blocks delegate call.
- Incorrect signature denied.

### `zk_two_phase`

Work trace: ZK long-running precompile `0x0806`; Phase 1 registers job and commitment; ZK-capable executor generates proof; Phase 2 settlement/delivery reports result.

Retain:

- ZK capability routing (`ZK_CALL`).
- Phase 1/Phase 2 lifecycle and deadline validation.
- ZK executor separation from LLM/HTTP executor in deployment.
- Callback/result encoding and verifier checks.

Merge surfaces:

- Long-running async validation.
- Executor registry capability matching.
- Payload builder and verifier settlement rules.
- `chain-deployment-infra` deployment of `NUM_PHALA_ZK_EXECUTOR`.

Validation:

- ZK proof happy path callback.
- Missing ZK executor or expired deadline path.

### `scheduled_zk_two_phase`

Work trace: Scheduler triggers a ZK precompile call; builder inserts `TxScheduled` and `TxAsyncCommitment`; Phase 1 settlement must satisfy Scheduler TTL; proof generation and Phase 2 delivery happen later through long-running delivery.

Retain:

- Scheduler/long-running TTL split.
- Scheduled async sender-lock exemption.
- ZK capability routing.
- Verifier enforces scheduled and async constraints.

Merge surfaces:

- Scheduler integration.
- Long-running async pool.
- ZK validation.
- Block verifier.

Validation:

- Scheduled ZK callback arrives after Phase 1.
- Scheduler TTL too short rejects Phase 1 replay.

### `sequencing_rights_simple`

Work trace: transaction flow exercises Ritual sequencing-rights policy; builder may reorder within allowed policy while preserving tip-maximizing behavior and scheduled/async obligations; verifier rejects invalid sequencing/censorship outcomes.

Retain:

- Sequencing-rights transaction or contract semantics.
- Builder ordering with regular, scheduled, fulfilled async, and delivery tx classes.
- Scheduled censorship checks.
- Verifier fail-closed behavior for invalid ordering.

Merge surfaces:

- Payload collector and unified builder.
- `ritual-sequencing-rights`.
- Block verifier.
- Txpool ordering/demotion.

Validation:

- Simple sequencing-rights traffic passes.
- Invalid ordering fixture rejected by verifier.

## Agent-Specific Traces From The User Guide

These are important even if they are not explicit gold standard workload names. The gold standard enables an agent orchestrator sidecar, and the user guide treats agents as first-class dApp primitives.

### Sovereign Agent `0x080C`

Work trace:

1. User/app selects an HTTP-call-capable executor; sovereign agents use capability `HTTP_CALL` (`0`) in the current guide.
2. Request encodes a 23-field sovereign payload: executor, TTL, user public key, polling/deadline fields, delivery config, `cliType`, prompt, encrypted secrets, conversation/output refs, skills refs, system prompt, model, tools, max turns/tokens, and RPC URLs.
3. Phase 1 submits a long-running async job and returns task/job id.
4. Executor starts an ephemeral agent harness in TEE.
5. Harness uses `LLM_PROVIDER` from encrypted secrets; guide default is ZeroClaw (`cliType=6`) plus Ritual GLM (`LLM_PROVIDER=ritual`, model `zai-org/GLM-4.7-FP8`).
6. Executor writes conversation/artifacts if refs are provided.
7. Phase 2 delivers result through `AsyncDelivery` callback.

Retain:

- Supported `cliType` semantics: build against `0` Claude Code, `5` Crush, `6` ZeroClaw; rejected/disabled legacy values remain rejected/disabled if shipped.
- `LLM_PROVIDER` required in encrypted secrets, with `ritual` provider available only for Sovereign Agent.
- Sovereign `skills[]` and `tools[]` are distinct: skills are storage refs; tools are harness allowlist strings.
- Factory-backed deployments require `deliveryTarget` to be the predicted child harness.
- Rolling scheduled windows invoke `0x080C` on every scheduled callback; threshold only schedules successor window.

Merge surfaces:

- Long-running agent validation.
- Agent type validation.
- Secret handling and model/provider validation.
- Scheduler if using factory rolling windows.
- Delivery settlement and callback.

Validation:

- Direct sovereign job returns callback.
- Factory harness predicted delivery target accepted; wrong target rejected.
- `cliType=6`, `LLM_PROVIDER=ritual` happy path.
- Missing `LLM_PROVIDER` rejected by executor/result path.

### Persistent Agent `0x0820`

Work trace:

1. User/app selects an HTTP-call-capable executor.
2. Request encodes a 26-field persistent payload: base executor fields, max spawn block, delivery config, provider/model/API-key ref, DA config, soul/agents/user/memory/identity/tools/runtime config refs, restore CID, RPC URLs, and agent runtime.
3. Phase 1 creates/spawns a long-running service and returns a pending id.
4. Phase 2 returns instance/container/checkpoint data or error.
5. Agent persists state through encrypted DA-backed workspace/checkpoints.
6. Agent registers and posts heartbeats using funded DKMS-derived identity/payment address.
7. Heartbeat tracker marks monitored, failed, reviving, monitored again, or removed.
8. Revival starts from latest encrypted checkpoint/manifest when possible.

Retain:

- Persistent agents are service primitives, not one-shot jobs.
- DA credentials are mandatory for usable persistent agents.
- DKMS-derived address must be funded for heartbeat registration and on-chain activity.
- `rpcUrls` must be reachable from inside the TEE container.
- Persistent Agent has no `skills_ref`; behavior is shaped by workspace docs such as `SOUL.md`, `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, and runtime config.
- Persistent `tools_ref`, Sovereign `skills[]`, and Sovereign `tools[]` must not be conflated.
- Agent runtime enum keeps current behavior: ZeroClaw `0`, Hermes `2`, legacy `1` reserved.
- Persistent Agent does not support the `ritual` provider in the same way Sovereign Agent does.

Merge surfaces:

- Persistent-agent payload validation.
- DA and secret payload compatibility.
- Heartbeat tracker and scheduled revival.
- Async delivery and result encoding.
- Fee and registry checks.

Validation:

- Spawn returns Phase 2 instance data.
- Heartbeat registration and alive status.
- Missed heartbeat leads to failed/revival-eligible state.
- Underfunded DKMS/payment address path is caught.
- Restore-from-checkpoint path if available.

### Factory-Backed Agent Deployment

Work trace:

1. App verifies factory addresses and wiring to Scheduler, RitualWallet, TEE registry, and AsyncDelivery.
2. App predicts child harness/launcher address from owner and user salt.
3. Payload uses predicted child as delivery target.
4. Factory deploys child and funds/arms schedule or launch configuration.
5. Child owns repeated wakeup, scheduler funding, wallet lock duration, and rolling window state.

Retain:

- Deterministic child address derivation.
- Delivery target must be predicted child, not factory.
- Scheduler funding and lock duration are deposited into child/payer wallet.
- Rolling windows obey Scheduler `MAX_LIFESPAN` and safe frequency defaults.

Merge surfaces:

- Scheduler.
- RitualWallet/payer semantics.
- Agent long-running validation.
- Deployment scripts and generated examples.

Validation:

- Predicted child receives callback.
- Invalid delivery target reverts.
- Rolling window schedules successor before current window expires.

### Agent Orchestrator Sidecar

Work trace:

1. Gold standard deploys one Phala-labeled LLM executor and enables an orchestrator sidecar.
2. LLM/agent requests route to the executor/orchestrator stack.
3. In mock proxy mode, per-deployment mock proxy returns canned responses.
4. In shared proxy mode, chain registers with shared proxy and routes real GLM inference through mTLS.
5. Orchestrator/executor logs are primary operational evidence for agent traffic.

Retain:

- Deployment config still produces the sidecar where agent workloads expect it.
- Shared proxy registration/funding/whitelisting works when enabled.
- Mock proxy mode remains a hermetic local/dev/CI path.
- Agent traffic can be correlated across chain events, executor logs, and orchestrator logs.

Merge surfaces:

- Mostly `chain-deployment-infra`, `executor-go`, proxy services, and `ritual-node-internal`.
- Reth-facing surfaces are registry, async result RPC, receipts, and block verification.

Validation:

- Gold standard deployment has executor and orchestrator containers healthy.
- Agent or LLM call logs show end-to-end request and settlement.

## User Guide Functionality Not In Gold Standard Traffic

### Multimodal Image/Audio/Video `0x0818`/`0x0819`/`0x081A`

Work trace: long-running async precompile accepts modal inputs, output config, and DA output storage ref; executor generates media; Phase 2 callback returns metadata, URI/content hash, encrypted flag, dimensions/duration/size, and error message.

Retain:

- Modal input/output ABI compatibility.
- DA output storage refs and encrypted output behavior.
- Long-running callback semantics.
- Capability routing for image/audio/video executors.

Validation:

- One minimal image generation or mocked multimodal callback fixture.
- Bad storage credentials or output config path.

### Passkey / P-256

Work trace: SECP256R1 precompile `0x0100` verifies P-256/WebAuthn signatures; TxPasskey transaction type `0x77` carries passkey signature/synthetic sender semantics through transaction encoding, hashing, recovery, pool validation, storage, RPC, and receipts.

Retain:

- `0x0100` ABI and SHA-256 hashing behavior.
- TxPasskey `0x77` wire/storage/RPC identity.
- Synthetic sender handling and passkey signature representation.
- Compatibility with persisted blocks/transactions if already shipped.

Merge surfaces:

- Alloy transaction envelope.
- Reth primitives/codecs/RPC.
- Txpool validation.
- EVM sender context.

Validation:

- Passkey tx round-trip fixture.
- WebAuthn/P-256 valid and invalid signature tests.

### FHE `0x0807`

Work trace: long-running async FHE/CKKS inference path follows the same two-phase lifecycle as other heavy precompiles, with FHE-specific payload validation and result encoding.

Retain:

- ABI compatibility.
- Long-running delivery semantics.
- Capability routing and validation.

Validation:

- If shipped and available, one fixture or mocked result path.
- At minimum, payload validation compile/test coverage so FHE is not silently dropped.

## Deployment And Platform Traces

### Mock Proxy Mode

Work trace: gold standard sets `USE_MOCK_PROXY=true`; input generation deploys a per-deployment mock vLLM proxy; LLM traffic uses `mock-model`; no shared GPU dependency.

Retain:

- Local/dev/CI deployments do not require external proxy availability.
- LLM workloads still exercise async/Reth paths even with canned model output.

Validation:

- `check_mock_proxy_status.sh` passes.
- `llm_call` and `llm_call_streaming` traffic settle against mock model.

### Shared GLM Proxy Mode

Work trace: `USE_MOCK_PROXY=false`; preflight checks proxy health, model, attestation, registration API, and backend inference; generated deployment passes proxy ops/mTLS URLs; deployment funds/whitelists proxy TEE and registers chain with shared proxy.

Retain:

- Registration API compatibility.
- Proxy TEE address funding/whitelisting.
- Real GLM model selection.
- mTLS URL and ops URL distinction.

Validation:

- Preflight health/model/attestation/registration/inference checks pass.
- Chain appears in `/registrations`.
- LLM call uses real GLM path.

### dKMS Mode

Work trace: gold standard passes `--dkms-mode enabled`; deployments run dKMS service; X402 and persistent-agent flows derive or use keys/payment addresses through dKMS rather than legacy secrets only.

Retain:

- DKMS precompile/service ABI.
- Key derivation indexes/formats.
- Derived address funding requirements.
- Backward behavior when `USE_DKMS=false` if still supported.

Validation:

- DKMS key derivation request.
- X402 dKMS traffic.
- Persistent-agent DKMS funding/heartbeat path.

### GCS DA

Work trace: gold standard provides `--gcs-key-file` and `--gcs-bucket`; LLM history, multimodal outputs, and persistent-agent state/checkpoints can use GCS storage refs and credentials.

Retain:

- StorageRef platform/path/keyRef conventions.
- Credential encryption and substitution.
- DA writes for persistent state and output artifacts.

Validation:

- GCS credential preflight.
- LLM conversation history or persistent checkpoint write/read.

### Summit And Chain-Driver Consensus

Work trace: Summit is default; chain-driver alternate resolves/pulls/builds an image tied to `ritual-node-internal` commit and uses chain-driver-specific block time. Both must import builder-produced blocks under Ritual verification.

Retain:

- Reth block production and verification are consensus-client agnostic at the execution-layer boundary.
- Chain-driver image tag/commit consistency if alternate path is used.
- Summit timing and large message settings from deployment remain viable.

Validation:

- Summit localnet gold standard.
- Chain-driver image preflight and smoke if this alternate remains supported for merge acceptance.

### Reth Env Gates

Work trace: gold standard passes `SKIP_VALIDITY_CONSTRAINTS` and `RITUAL_FORCE_CONTRACT_SCAN` through `--reth-env-vars`.

Retain:

- Environment-gated behavior only where intentionally shipped.
- Defaults should not silently weaken consensus validity.
- Contract scan behavior remains explicit and observable.

Validation:

- Run with default gold standard envs.
- Run targeted verifier test with validity constraints enabled before final merge acceptance.

## Generalized Merge Retention Model

The flows above reduce to eight preservation classes.

### 1. Wire, Storage, And Receipt Compatibility

Must preserve:

- `TxScheduled` `0x10`.
- `TxAsyncCommitment` `0x11`.
- `TxAsyncSettlement` `0x12`.
- TxPasskey `0x77`.
- SPC call fields in receipts.
- RLP/2718/compact/static-file/storage codecs for custom transaction families.
- Callback/result ABI encodings already exposed to dApps.

Primary repos:

- `ritual-alloy-internal`
- `ritual-reth-internal`
- `ritual-reth-nodebuilder-internal`

Gate:

- Round-trip fixtures and old-block/data decode where available.

### 2. Admission And Validation Compatibility

Must preserve:

- RPC async simulation as helpful feedback, not authority.
- Builder/verifier parent-state validation as the consensus source of truth.
- Payload limits, TTLs, deadline extraction, model/TEE/wallet/registry checks.
- Sender lock behavior and scheduled exemptions.
- Secret/delegation validation.

Primary repos:

- `ritual-reth-internal`
- `ritual-revm-internal`
- `ritual-alloy-evm-internal`
- `ritual-reth-nodebuilder-internal`

Gate:

- Negative tests for each rejected payload class.

### 3. Builder Obligation Compatibility

Must preserve:

- Scheduled obligation augmentation.
- Async commitment insertion.
- Fulfilled replay and settlement same-block ordering for short async.
- Long-running Phase 1 and delivery-ready settlement handling.
- Mixed regular/scheduled/async/delivery ordering.
- Sequencing-rights policy.

Primary repos:

- `ritual-reth-internal`
- `ritual-reth-nodebuilder-internal`

Gate:

- Builder scenario tests for each transaction class and mixed blocks.

### 4. Verifier Fail-Closed Compatibility

Must preserve:

- Builder-produced blocks replay under verifier rules.
- Invalid async commitments, settlements, deliveries, scheduler constraints, nonce locks, SPC signatures, fees, and sequencing-rights outcomes are rejected.
- Env gates do not accidentally disable required shipped validation.

Primary repos:

- `ritual-reth-internal`
- `ritual-revm-internal`
- `ritual-alloy-evm-internal`

Gate:

- Invalid block fixtures per verifier phase.

### 5. Executor And Operator Surface Compatibility

Must preserve:

- Ritual RPC namespace for async result submission, batch submission, delivery result submission, pending jobs, traces, scheduled incidents, and heartbeat state.
- Executor capability matching through `TEEServiceRegistry`.
- Proxy registration and LLM/streaming operational routes.
- Orchestrator and executor log correlation.

Primary repos:

- `ritual-reth-internal`
- `ritual-reth-nodebuilder-internal`
- `ritual-node-internal`
- deployment/executor/proxy repos outside this merge set as integration dependencies.

Gate:

- JSON-RPC smoke tests plus gold standard traffic logs.

### 6. Product Economics Compatibility

Must preserve:

- RitualWallet deposit/lock requirements.
- Async inclusion/settlement/delivery fees.
- LLM/model pricing and worst-case escrow/refund behavior.
- X402 paid API credential privacy and budget patterns.
- Persistent-agent heartbeat minimum funding and removal behavior.

Primary repos:

- `ritual-reth-internal`
- `ritual-reth-nodebuilder-internal`
- system contract deployment/config repos.

Gate:

- Fee formula unit tests and one end-to-end paid/async settlement case.

### 7. Agent Lifecycle Compatibility

Must preserve:

- Sovereign as ephemeral task primitive.
- Persistent as long-lived service primitive.
- Factory deterministic child address and delivery-target rules.
- Persistent DA/checkpoint/heartbeat/revival lifecycle.
- Agent harness/provider/runtime enum behavior.

Primary repos:

- `ritual-reth-internal`
- `ritual-reth-nodebuilder-internal`
- `ritual-node-internal`
- executor/orchestrator repos.

Gate:

- At least one sovereign direct or factory callback.
- At least one persistent spawn/heartbeat/revival-oriented smoke, even if full revival is deferred to localnet.

### 8. Deployment Reproducibility Compatibility

Must preserve:

- Gold standard input generation.
- Mock and shared proxy modes.
- dKMS mode.
- GCS DA config.
- Summit default and chain-driver alternate if still required.
- Streaming service flag.
- ZK executor deployment.

Primary repos:

- `chain-deployment-infra`
- `ritual-node-internal`
- `ritual-reth-nodebuilder-internal`

Gate:

- Generate config with `gold_standard.sh`.
- Run deployment.
- Run all gold standard traffic.
- Capture logs for executor, orchestrator, traffic generator, and Reth.

## Dependency-Ordered Feature Verification Plan

Use this as the working order once the pre-Reth dependency repos are being merged. It separates "the code can be ported" from "traffic is meaningful proof." Early steps should mostly use compile checks and focused fixtures; later steps should graduate to `ritual-reth-nodebuilder-internal`, `ritual-node-internal`, and gold-standard localnet traffic.

Local-network testing should follow `.cursor/skills/local-network/SKILL.md`: start from `ritual-node-internal`, inspect the `Makefile` before relying on command names, rebuild the narrowest trustworthy image set, restart with `make restart-network`, then verify status/registries before traffic. Treat localnet as integration/E2E evidence, not a substitute for unit and fixture tests that isolate consensus behavior.

### Feature Dependency Tree

```text
0. Dependency repo floor
   Alloy transaction/RPC primitives
   revm precompiles, context, and gas behavior
   Alloy EVM bridge over Alloy + revm
   revm-inspectors compatibility
   readiness: no unresolved merge state, coherent lockfiles, scoped checks recorded, intended sibling path dependencies confirmed
   |
1. Reth 2.2 integration skeleton
   upstream node builder shape, EVM config propagation, RPC/payload/verifier extension points
   |
2. Wire, storage, and receipt identity
   TxScheduled, TxAsyncCommitment, TxAsyncSettlement, TxPasskey, SPC receipt fields
   |
3. Basic execution
   plain EVM traffic and synchronous precompiles
   |
4. Async admission foundation
   parent-state async detection, RPC UX validation, async EVM context, SPC capture
   |
5. Async pool lifecycle
   commitments, sender locks, expiry, canonical cleanup, result metadata
   |
6. Short async settlement
   HTTP/LLM short results, fulfilled replay, same-block settlement, fee settlement
   |
7. Secrets, private output, and dKMS
   encrypted secrets, delegation, private output, dKMS-derived addresses
   |
8. Long-running delivery
   Phase 1, delivery result submission, callback execution, expiry
   |
9. Scheduling and heartbeat base
   TxScheduled insertion, hydration, predicates, C1-C11, revival state
   |
10. Scheduled async combinations
    scheduled short async, scheduled long-running, scheduled ZK, scheduled X402
    |
11. Mixed payload policy and verifier hardening
    sequencing rights, censorship checks, caps/demotion, invalid-block fixtures
    |
12. Operator, observability, and deployment integration
    ritual_* RPC, traces, incidents, metrics, agents, nodebuilder image, localnet traffic
```

Scheduling base does not have to wait for every async feature before code porting starts. The dependency is behavioral: `scheduled_onnx_inference` can verify scheduling once basic execution works, but `x402_dkms_scheduled` and `scheduled_zk_two_phase` are not useful gates until the corresponding secret, dKMS, and long-running async paths already pass.

### Testing Cadence And Local-Network Handoff

Use `merge-principles.md` for the general cadence: cheap checks per batch, broader package/workspace checks per subsystem, cross-repo builds after dependency repos land, and localnet/full traffic only at checkpoints. Use `.cursor/skills/local-network/SKILL.md` when a gate needs a live Ritual network.

The practical split should be:

```text
Tree levels 0-2: unit / fixture / compile gates
                 no localnet required

Tree level 3: first local-network smoke is allowed after basic execution fixtures pass
              token_transfer, swap, and sync precompile smoke

Tree levels 4-5: mostly unit / simulation / FSM gates
                 no "done" localnet claim yet

Tree levels 6-11: feature integration gates
                  localnet is required for traffic involving RPC, executors, sidecars, registry, fees, scheduling, or mixed payload behavior

After tree level 12: done / acceptance gates
                     local-network skill workflow plus gold-standard traffic and evidence capture
```

Local-network workflow should start in `ritual-node-internal` and inspect the `Makefile` before assuming targets. If branch alignment is needed, decide whether repos should move to `dev` or stay on current feature branches before `make setup-repos`. If smart contracts changed, refresh genesis exports from `ritual-sc-internal` before restarting the network.

For Reth-only or nodebuilder-only changes, the first localnet checkpoint should usually rebuild the execution-layer image with the narrowest verified Make target, commonly `make build-reth` from `ritual-node-internal`. That target delegates to `ritual-reth-nodebuilder-internal build-slim`, which compiles against `../ritual-reth-internal`. If dependency repos, services, contracts, or image state are uncertain, prefer `make build-all` before trusting localnet results.

For live network checkpoints, prefer a hermetic mock-inference restart first:

```bash
make restart-network vllm_mode=local_mock
make status
make show-network
make tee-registry
```

Then run the smallest relevant traffic or `make test-e2e TEST=<name>` before broad traffic. Use `make restart-network` again after rebuilding executor or sidecar images; do not treat a container-only restart as enough when funding, registration, whitelist, or genesis setup could matter.

### Local-Network Entry Points By Tree Level

- Tree level 0, dependency repo floor: use repo-local compile, unit tests, and scoped merge checks. Do not spend localnet time until dependency resolution is coherent.
- Tree level 1, `Reth 2.2 integration skeleton`: use cross-repo compile/check and nodebuilder image-build readiness. Image build may be useful, but it is not traffic proof.
- Tree level 2, wire/storage/receipt identity: use codec round-trip fixtures and old-data decode where available. Localnet is not required unless an RPC shape can only be checked against a live node.
- Tree level 3, basic execution: run unit fixtures and verifier replay first, then allow the first localnet smoke for `token_transfer`, `swap`, and sync precompile behavior.
- Tree level 4, async admission foundation: use simulation and negative validation tests. Optional RPC smoke can prove endpoint wiring, but it is not enough to claim async works.
- Tree level 5, async pool lifecycle: use FSM/unit tests and canonical/reorg fixtures. Localnet is only for debugging pool/RPC metadata unless this level blocks later traffic.
- Tree level 6, short async settlement: localnet becomes required for `http_call`, `llm_call`, executor registration, receipt `spcCalls`, and fee evidence.
- Tree level 7, secrets/private output/dKMS: localnet is required for X402, dKMS, private output, delegation, wallet funding, and registry behavior.
- Tree level 8, long-running delivery: localnet is required for Phase 1/Phase 2 callbacks, delivery RPC, executor polling, and ZK capability routing.
- Tree level 9, scheduling/heartbeat base: localnet is required for due scheduled traffic, hydration, heartbeat tracker state, and revival visibility.
- Tree level 10, scheduled async combinations: localnet is required, and these levels are not meaningful until their underlying async/dKMS/ZK path already passes.
- Tree level 11, mixed payload policy/verifier hardening: localnet is required for mixed traffic, while invalid-block rejection can remain fixture-based.
- Tree level 12 and final acceptance: localnet evidence becomes the acceptance artifact. Use the local-network skill workflow, gold-standard traffic, and captured logs/state evidence.

### Step Gates

1. Dependency repo floor
   Objective: make the non-Reth repos safe for agents to finish before the Reth port depends on them.
   Depends on: none inside this plan.
   Verification: each dependency repo builds or reaches its scoped merge check; no unresolved merge paths or conflict markers remain; repo-local `MERGE_NOTES.md` records risky resolutions; Reth/nodebuilder dependency resolution uses the intended local Alloy, revm, Alloy EVM, and inspector crates without accidentally pulling stale crates.io versions of forked crates; `alloy-evm` composes with the merged Alloy and revm APIs. For `alloy-evm`, explicitly verify Ritual `TxEnv` metadata conversion, async-context error propagation, explicit-gas system calls, and custom reward plumbing. If upstream deletes an OP bridge crate, prove the target Reth/nodebuilder stack has no live `alloy-op-evm` dependency before accepting the deletion.

2. Reth 2.2 integration skeleton
   Objective: port onto upstream Reth `v2.2.0` shape without proving Ritual traffic yet.
   Depends on: dependency repo floor.
   Verification: `ritual-reth-internal` compiles far enough to expose the current upstream node builder, payload, RPC, and verifier extension points; `ritual-reth-nodebuilder-internal` compiles against the new trait shapes; the same `EthEvmConfig<RitualEvmFactory>` reaches payload building, RPC simulation, and block validation rather than being recreated through parallel configs; the execution contexts on those paths are `AsyncContextTr`-capable when Ritual async precompiles can execute; OP execution is either proven to preserve async/SPC context or explicitly marked out of scope for async flows.

3. Wire, storage, and receipt identity
   Objective: preserve shipped data identity before behavior depends on it.
   Depends on: Reth 2.2 integration skeleton and Alloy transaction primitives.
   Verification: round-trip fixtures for `TxScheduled(0x10)`, `TxAsyncCommitment(0x11)`, `TxAsyncSettlement(0x12)`, `TxPasskey(0x77)`, and SPC receipt fields; transaction hash/root equality for blocks containing each custom family; old DB/static-file decode if fixtures are available; upstream `v107` EIP-7702 authorization-list support remains intact while Ritual `TxEnv` metadata (`commitment_tx`, `settlement_tx`, `spc_calls`, `tx_hash`) survives Reth/Alloy EVM conversion.

4. Basic execution
   Objective: prove regular Ethereum behavior and synchronous native precompiles still replay deterministically.
   Depends on: Reth 2.2 integration skeleton, revm precompile registration, Alloy EVM integration.
   Verification: `token_transfer` localnet smoke; `swap` in a block that also has room for system transactions; ONNX, JQ, Ed25519, SECP256R1/passkey-precompile fixtures; builder-produced blocks import under verifier replay with matching outputs.

5. Async admission foundation
   Objective: establish async classification and validation before any settlement traffic is trusted.
   Depends on: wire identity and basic execution.
   Verification: one valid detection fixture proving parent-state builder/verifier classification and SPC capture; negative tests for TTL, phase-two offset, malformed payload, unsupported agent type, bad ECIES/user key, missing model/executor/registry data, and oversized inputs; RPC validation remains an early-feedback path and does not become consensus authority.

6. Async pool lifecycle
   Objective: preserve the async/scheduled pool state machine before payload building consumes it.
   Depends on: async admission foundation.
   Verification: async pool FSM tests for commitment insertion, sender lock acquisition/release, expiry, pending/queued/basefee cleanup, stale duplicate pruning, canonical-state cleanup, reorg behavior, and pool metadata RPC.

7. Short async settlement
   Objective: prove the smallest complete async loop: detect, commit, execute off-chain, replay fulfilled tx, settle in the same block, and verify.
   Depends on: async pool lifecycle, SPC capture, fee/registry/wallet reads.
   Verification: `http_call` and `llm_call` happy paths with decoded `spcCalls`; invalid wallet/model/executor cases reject fail-closed; fee settlement balances match the formula tests; verifier rejects malformed commitments, mismatched SPC context, and invalid settlement blocks.

8. Secrets, private output, and dKMS
   Objective: layer secret-bearing traffic onto the proven short-async path.
   Depends on: short async settlement and registry/wallet checks.
   Verification: `x402_dkms_http_call`, `private_io`, and `delegate_secret` traffic; placeholder substitution succeeds; wrong secret signature or revoked delegation is denied; private output decrypts only with the user key; dKMS-derived address is funded and used by at least one dependent flow.

9. Long-running delivery
   Objective: prove Phase 1/Phase 2 lifecycle and callback semantics.
   Depends on: async admission, async pool lifecycle, result-submission RPC, delivery settlement codecs.
   Verification: `long_running_echo` callback happy path; wrong selector, low delivery gas, callback revert, and expiry cleanup cases; `zk_two_phase` happy path once ZK executor capability routing is available; missing executor or expired deadline fails in the expected phase.

10. Scheduling and heartbeat base
   Objective: prove scheduled execution independently before combining it with async-heavy flows.
   Depends on: wire identity, basic execution, txpool system-tx exemptions, verifier hooks.
   Verification: `scheduled_onnx_inference` due call executes; predicate-false and expired calls are skipped or rejected as specified; Scheduler storage hydration works on startup/canonical updates; heartbeat tracker hydration and `ritual_getHeartbeatTrackerState` expose the expected state.

11. Scheduled async combinations
   Objective: prove scheduled execution composes with short async, long-running, secrets, dKMS, and ZK.
   Depends on: scheduling base plus the corresponding async path under test.
   Verification: scheduled short async settles within Scheduler TTL; tight Scheduler TTL rejects Phase 1 replay; `x402_dkms_scheduled` fires and settles; `scheduled_zk_two_phase` produces Phase 2 callback after Phase 1 succeeds; scheduled async sender-lock exemption and per-block duplicate controls both hold.

12. Mixed payload policy and verifier hardening
   Objective: prove the builder/verifier agree once all transaction classes compete in the same block.
   Depends on: short async, long-running delivery, scheduling combinations, sequencing-rights port.
   Verification: mixed block containing regular, scheduled, async commitment, fulfilled async, delivery, and sequencing-rights traffic; `sequencing_rights_simple` passes; invalid ordering, censorship, nonce-lock, SPC, fee, and scheduled-obligation fixtures are rejected by verifier; cap/demotion traces explain skipped optional work.

13. Operator, observability, and deployment integration
   Objective: turn feature-level confidence into merge acceptance evidence.
   Depends on: all prior gates.
   Verification: `ritual_*` JSON-RPC smoke for submissions, pending jobs, heartbeat state, traces, and scheduled incidents; block-build and async simulation traces are bounded and populated; `ritual-reth-nodebuilder-internal` image builds; `ritual-node-internal` starts a localnet; `gold_standard.sh` config generation and all gold-standard traffic pass; mock proxy mode works, and shared proxy mode passes if it remains a required merge gate; at least one sovereign or persistent-agent smoke runs if the gold standard does not cover `0x080C` or `0x0820`.

### Parallel Work While Dependency Repos Are In Flight

Do not block all Reth-side work on the dependency agents, but keep the work split by churn risk.

Start now:

- Port the clean upstream Reth `v2.2.0` structure and the `Reth 2.2 integration skeleton`.
- Identify the current node-builder, payload, RPC, and verifier extension points.
- Extract or write fixture expectations for custom transaction families, receipts, sync precompiles, verifier failures, scheduler predicates, and txpool FSM behavior.
- Prepare `MERGE_NOTES.md` and invariant checklists for each feature gate.
- Build against dependency agents' branches when they have compile-stable checkpoints, treating failures as integration feedback rather than final feature failures.

Wait for dependency repos to stabilize before finalizing:

- Code that depends directly on final Alloy transaction envelope shapes, revm `TxEnv` / context APIs, Alloy EVM conversion APIs, OP execution behavior, or inspector API compatibility.
- End-to-end async, scheduled async, and agent traffic gates.
- Any localnet "done" claim that would be invalidated by a later dependency repo API or semantic change.

Practical rule: Reth agents can work on skeleton, mapping, fixtures, and compile integration now. Feature agents should only claim a traffic gate complete after the relevant dependency branches have landed or been pinned to an agreed integration branch, then rebuilt into the localnet image.

### Recommended Traffic Order

1. `token_transfer`, then `swap`.
2. Sync precompiles: `onnx_inference`, `jq_query`, `ed25519_verify`, plus passkey/P-256 fixtures even though passkey is not listed as gold-standard traffic.
3. Short async: `http_call`, `llm_call`, then `llm_call_streaming` with final on-chain receipt confirmation.
4. Secret and private-output paths: `x402_dkms_http_call`, `private_io`, `delegate_secret`.
5. Long-running paths: `long_running_echo`, then `zk_two_phase`.
6. Scheduling without async first: `scheduled_onnx_inference`.
7. Scheduled async after the relevant base paths pass: `x402_dkms_scheduled`, `scheduled_zk_two_phase`.
8. Mixed policy: `sequencing_rights_simple` and invalid-ordering verifier fixtures.
9. Agent-specific traffic: direct sovereign job, persistent spawn/heartbeat smoke, and factory predicted-delivery-target flow if agents are a blocking merge requirement.
10. Full deployment evidence: gold-standard localnet, executor/orchestrator logs, Reth payload/verifier logs, streaming logs, Scheduler state, AsyncJobTracker state, and HeartbeatTracker state.

## Suggested Merge Gates

Use these as acceptance gates for the Reth upstream port, not as mandatory per-commit tests.

### Batch Gates

- Transaction formats: custom tx round-trip tests for scheduled, async commitment, async settlement, passkey, and SPC fields.
- Precompile registration: sync precompile fixtures for ONNX, JQ, Ed25519, SECP256R1.
- Short async: HTTP and LLM happy paths plus invalid TTL/wallet/sender-lock/model cases.
- Long async: Long HTTP happy callback plus callback failure and timeout.
- Scheduler: due, predicate-false, expired, scheduled short async, scheduled long async.
- Verifier: invalid block fixtures for async, scheduled, sequencing rights, nonce lock, and SPC.
- RPC: `ritual_*` namespace smoke tests and receipt `spcCalls`.

### Integration Gates

- Build `ritual-reth-nodebuilder-internal` against merged dependency repos.
- Build execution-layer image.
- Use `ritual-node-internal` or deployment infra to start a localnet.
- Generate gold standard config.
- Run all gold standard traffic.
- Repeat LLM path in mock proxy mode and, if available, shared proxy mode.
- Run at least one agent-specific smoke outside the current gold standard traffic if agents are not covered there.

### Final Localnet Evidence To Capture

- Reth logs around payload build, async detection, settlement, and verifier import.
- Traffic generator success/failure per workload.
- Executor logs for HTTP, LLM, X402, ZK, long-running, and agent calls.
- Orchestrator logs for agent/LLM flows.
- Streaming service logs for SSE traffic.
- AsyncJobTracker state before/after long-running jobs.
- Scheduler state for scheduled workloads.
- Heartbeat tracker state for persistent-agent smoke if run.

## Open Questions

- Does the gold standard traffic currently execute either `0x080C` or `0x0820`, or does it only deploy the agent orchestrator sidecar?
- Should the upstream merge acceptance suite add explicit sovereign and persistent agent traffic, or is a separate post-merge agent localnet gate acceptable?
- Which FHE/multimodal flows are considered shipped enough to require blocking merge tests?
- Should `SKIP_VALIDITY_CONSTRAINTS=true` remain in the gold standard, or should final merge validation include a second run with constraints enabled?
- Are chain-driver deployments still required for the upstream merge acceptance gate, or is Summit-only enough until node/deployment repos change?
