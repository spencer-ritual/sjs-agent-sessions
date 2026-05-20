# Functionality-Flow Review Queue Additions

### File 0316: crates/ritual-precompile-addresses/src/lib.rs

- Source: `crates/ritual-precompile-addresses/src/lib.rs:48-69`
- Claim: The canonical precompile-address catalog keeps all dApp-facing SPC-verified and two-phase addresses in one source of truth, covering HTTP, LLM, long HTTP, ZK, FHE, multimodal, DKMS, sovereign-agent, and persistent-agent flows.
- Flow labels: `Source Inventory`, `Short-Running Async SPC Trace`, `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Source Inventory, Short-Running Async SPC Trace, Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0321: crates/ritual-precompile-codecs/src/http_call.rs

- Source: `crates/ritual-precompile-codecs/src/http_call.rs:48-69`
- Claim: HTTP async payload decoding preserves the ExecutorRequest base fields, encrypted secret arrays, user public key, URL, method, headers, and optional body expected by HTTP and X402 HTTP traffic.
- Flow labels: `http_call`, `x402_dkms_http_call`, `Secret, Private Output, And dKMS Trace`
- Negative test: Replay the smallest http_call, x402_dkms_http_call, Secret, Private Output, And dKMS Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0323: crates/ritual-precompile-codecs/src/llm_call.rs

- Source: `crates/ritual-precompile-codecs/src/llm_call.rs:16-37`
- Claim: LLM async payload decoding preserves the 30-field request shape while extracting executor, encrypted secrets, TTL, user public key, messages JSON, and model for shared RPC and builder validation.
- Flow labels: `llm_call`, `llm_call_streaming`, `Short-Running Async SPC Trace`
- Negative test: Replay the smallest llm_call, llm_call_streaming, Short-Running Async SPC Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:12-33`
- Claim: Long-running delivery config decoding preserves callback target, selector, gas, fee caps, and value as the common Phase 2 callback contract between the executor, payload builder, and AsyncDelivery.deliver.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:50-71`
- Claim: Long-running HTTP decoding extracts delivery configuration and the URL, poll URL, and result URL needed to validate and poll two-phase HTTP jobs without changing the shipped ABI layout.
- Flow labels: `long_running_echo`, `x402_dkms_long_running_http`
- Negative test: Replay the smallest long_running_echo, x402_dkms_long_running_http scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:202-223`
- Claim: ZK two-phase delivery decoding reads the max proof block and delivery callback fields from the ZK ABI so Phase 2 proof delivery uses the same callback contract as long-running HTTP.
- Flow labels: `zk_two_phase`, `scheduled_zk_two_phase`
- Negative test: Replay the smallest zk_two_phase, scheduled_zk_two_phase scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:348-369`
- Claim: Sovereign-agent delivery decoding uses the agent-specific ABI layout to extract max poll block and callback fields without depending on the long-HTTP field offsets.
- Flow labels: `Sovereign Agent Precompile Trace`
- Negative test: Replay the smallest Sovereign Agent Precompile Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:507-528`
- Claim: Persistent-agent delivery decoding uses the 0x0820 ABI layout to extract max spawn block and callback fields used when spawning a long-running agent instance.
- Flow labels: `Persistent Agent Lifecycle Trace`
- Negative test: Replay the smallest Persistent Agent Lifecycle Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:661-682`
- Claim: FHE delivery decoding reads the 19-field FHE request layout and max inference block so encrypted Phase 2 output delivery can be priced and settled deterministically.
- Flow labels: `FHE / Private Compute Trace`
- Negative test: Replay the smallest FHE / Private Compute Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0324: crates/ritual-precompile-codecs/src/long_running.rs

- Source: `crates/ritual-precompile-codecs/src/long_running.rs:852-873`
- Claim: FHE Phase 2 result decoding extracts the encrypted output size from the delivery result, making output-size fee calculation depend on the delivered result struct rather than external metadata.
- Flow labels: `FHE / Private Compute Trace`, `Product Economics Compatibility`
- Negative test: Replay the smallest FHE / Private Compute Trace, Product Economics Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Source: `crates/ritual-precompile-codecs/src/persistent_agent.rs:118-139`
- Claim: Persistent-agent request decoding preserves the base executor fields, max spawn block, delivery config, model/provider/runtime settings, storage refs, and RPC URLs required to spawn OpenClaw or Hermes agents.
- Flow labels: `Persistent Agent Lifecycle Trace`, `Factory-Backed Agent Deployment`
- Negative test: Replay the smallest Persistent Agent Lifecycle Trace, Factory-Backed Agent Deployment scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0325: crates/ritual-precompile-codecs/src/persistent_agent.rs

- Source: `crates/ritual-precompile-codecs/src/persistent_agent.rs:629-650`
- Claim: Persistent-agent responses round-trip instance id, endpoint, checkpoint CID, and error message so Phase 2 delivery can distinguish successful spawns from spawn failures.
- Flow labels: `Persistent Agent Lifecycle Trace`
- Negative test: Replay the smallest Persistent Agent Lifecycle Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0326: crates/ritual-precompile-codecs/src/sovereign_agent.rs

- Source: `crates/ritual-precompile-codecs/src/sovereign_agent.rs:51-72`
- Claim: Sovereign-agent request decoding preserves TTL, poll and deadline fields, delivery config, agent type, prompt, model, tools, max turns, max tokens, and RPC URLs used by multi-step agent flows.
- Flow labels: `Sovereign Agent Precompile Trace`, `Agent Orchestrator Surface`
- Negative test: Replay the smallest Sovereign Agent Precompile Trace, Agent Orchestrator Surface scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0297: crates/ritual-async/src/validation.rs

- Source: `crates/ritual-async/src/validation.rs:49-70`
- Claim: Shared async payload validation rejects zero executors, zero or over-limit TTLs, malformed ECIES secret blobs, and compressed or wrong-size user public keys before RPC, builder, or verifier depend on the payload.
- Flow labels: `Admission And Validation Compatibility`, `Secret, Private Output, And dKMS Trace`
- Negative test: Replay the smallest Admission And Validation Compatibility, Secret, Private Output, And dKMS Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0297: crates/ritual-async/src/validation.rs

- Source: `crates/ritual-async/src/validation.rs:208-229`
- Claim: Async precompile data extraction routes HTTP, LLM, sovereign-agent, persistent-agent, DKMS, and generic ExecutorRequest payloads through their dedicated decoders before validating executor and TTL.
- Flow labels: `Short-Running Async SPC Trace`, `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0297: crates/ritual-async/src/validation.rs

- Source: `crates/ritual-async/src/validation.rs:316-337`
- Claim: Two-phase deadline extraction uses precompile-specific ABI offsets for sovereign-agent, persistent-agent, long-running HTTP, ZK, FHE, and multimodal requests, and returns no deadline for non-two-phase precompiles.
- Flow labels: `Long-Running Two-Phase Trace`, `Scheduled Execution Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace, Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0297: crates/ritual-async/src/validation.rs

- Source: `crates/ritual-async/src/validation.rs:417-438`
- Claim: Two-phase deadline validation requires the Phase 2 deadline offset to be strictly greater than TTL so Phase 2 delivery cannot expire before Phase 1 settlement.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0297: crates/ritual-async/src/validation.rs

- Source: `crates/ritual-async/src/validation.rs:441-462`
- Claim: Async payload validation enforces max input size and routes precompile-specific URL, model, prompt, multimodal, FHE, DKMS, and agent checks from one shared validation surface.
- Flow labels: `Admission And Validation Compatibility`
- Negative test: Replay the smallest Admission And Validation Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Source: `crates/rpc/rpc/src/async_tx_validator.rs:5-26`
- Claim: RPC async validation is explicitly a user-feedback layer that delegates consensus-relevant payload checks to shared validation so invalid async traffic receives descriptive errors without becoming the authority over builder or verifier behavior.
- Flow labels: `Short-Running Async SPC Trace`, `Admission And Validation Compatibility`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Admission And Validation Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Source: `crates/rpc/rpc/src/async_tx_validator.rs:165-186`
- Claim: RPC executor registration checks map each async precompile to its required TEE capability, allowing sovereign and persistent agents to use HTTP or LLM executors while enforcing media, ZK, FHE, and HTTP capabilities.
- Flow labels: `Executor And Operator Surface Compatibility`
- Negative test: Replay the smallest Executor And Operator Surface Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Source: `crates/rpc/rpc/src/async_tx_validator.rs:283-304`
- Claim: RPC wallet validation calls the same commitment wallet verifier as the builder and translates insufficient balance, lock duration, and model failures into user-facing async validation errors.
- Flow labels: `Admission And Validation Compatibility`, `Product Economics Compatibility`
- Negative test: Replay the smallest Admission And Validation Compatibility, Product Economics Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0396: crates/rpc/rpc/src/async_tx_validator.rs

- Source: `crates/rpc/rpc/src/async_tx_validator.rs:361-382`
- Claim: RPC two-phase deadline validation delegates deadline extraction and offset-vs-TTL checks to the shared async validation module instead of maintaining a separate deadline rule.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0280: crates/ritual-async-fees/src/lib.rs

- Source: `crates/ritual-async-fees/src/lib.rs:115-136`
- Claim: Sovereign-agent Phase 2 pricing charges actual work through iterations and tool calls, with zero commitment and inclusion fees because Phase 1 already paid them.
- Flow labels: `Sovereign Agent Precompile Trace`, `Product Economics Compatibility`
- Negative test: Replay the smallest Sovereign Agent Precompile Trace, Product Economics Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0280: crates/ritual-async-fees/src/lib.rs

- Source: `crates/ritual-async-fees/src/lib.rs:241-262`
- Claim: Image Phase 2 pricing uses model-specific per-pixel and minimum fees plus UX step multipliers, and returns executor fee only after Phase 1.
- Flow labels: `Multimodal Precompile Trace`, `Product Economics Compatibility`
- Negative test: Replay the smallest Multimodal Precompile Trace, Product Economics Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0280: crates/ritual-async-fees/src/lib.rs

- Source: `crates/ritual-async-fees/src/lib.rs:311-332`
- Claim: Video escrow pricing reserves worst-case max resolution and duration with model-specific pixel-second fees and step and FPS multipliers before long-running video work is admitted.
- Flow labels: `Multimodal Precompile Trace`, `Product Economics Compatibility`
- Negative test: Replay the smallest Multimodal Precompile Trace, Product Economics Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Source: `crates/ritual-scheduled-verification/src/lib.rs:1-21`
- Claim: Scheduled transaction verification defines C1-C11 constraints, including existence, state, timing, system sender, target, funds, uniqueness, and predicate behavior as consensus checks.
- Flow labels: `Scheduled Execution Trace`
- Negative test: Replay the smallest Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Source: `crates/ritual-scheduled-verification/src/lib.rs:36-57`
- Claim: Scheduled transactions bypass normal signature verification only through the fixed dummy signature r=0, s=0, v=false expected by verifier logic.
- Flow labels: `Scheduled Execution Trace`
- Negative test: Replay the smallest Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Source: `crates/ritual-scheduled-verification/src/lib.rs:403-424`
- Claim: Scheduler state hydration preserves target, caller, start block, num calls, frequency, gas, TTL, max fees, value, call data, and call id read from Scheduler contract storage.
- Flow labels: `Scheduled Execution Trace`
- Negative test: Replay the smallest Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Source: `crates/ritual-scheduled-verification/src/lib.rs:431-452`
- Claim: Scheduled execution timing computes expected block, per-execution TTL deadline, and overall expiry from start block, frequency, num calls, and TTL using saturating arithmetic.
- Flow labels: `Scheduled Execution Trace`
- Negative test: Replay the smallest Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0332: crates/ritual-scheduled-verification/src/lib.rs

- Source: `crates/ritual-scheduled-verification/src/lib.rs:821-842`
- Claim: Scheduled filtering separates permanent removal reasons from temporary retry reasons, keeping too-early, insufficient-funds, and predicate failures retryable while dropping invalid state, target, signature, and executed calls.
- Flow labels: `Scheduled Execution Trace`
- Negative test: Replay the smallest Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0344: crates/ritual-spc-signature/src/lib.rs

- Source: `crates/ritual-spc-signature/src/lib.rs:15-36`
- Claim: SPC verification membership delegates to the canonical address allowlist so RPC, builder, and verifier cannot drift on which async precompiles require SPC proof checking.
- Flow labels: `Short-Running Async SPC Trace`, `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0344: crates/ritual-spc-signature/src/lib.rs

- Source: `crates/ritual-spc-signature/src/lib.rs:199-220`
- Claim: SPC signature payload construction uses sorted compact JSON with hex strings without 0x prefixes for block number, tx hash, precompile address, input, output, previous block context, and error.
- Flow labels: `Short-Running Async SPC Trace`, `Executor And Operator Surface Compatibility`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Executor And Operator Surface Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0344: crates/ritual-spc-signature/src/lib.rs

- Source: `crates/ritual-spc-signature/src/lib.rs:181-202`
- Claim: SPC signature verification accepts recovery ids 0/1 and Ethereum-style 27/28 only, rejecting malformed recovery IDs instead of normalizing arbitrary values.
- Flow labels: `Short-Running Async SPC Trace`
- Negative test: Replay the smallest Short-Running Async SPC Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0461: crates/storage/codecs/src/alloy/transaction/async_settlement.rs

- Source: `crates/storage/codecs/src/alloy/transaction/async_settlement.rs:37-58`
- Claim: Async settlement compact storage preserves both delivery SPC calls and settlement SPC calls while converting empty vectors back to None to keep RLP identity stable.
- Flow labels: `Long-Running Two-Phase Trace`, `Receipt And Client Surface Compatibility`
- Negative test: Replay the smallest Long-Running Two-Phase Trace, Receipt And Client Surface Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0469: crates/storage/codecs/src/alloy/transaction/txtype.rs

- Source: `crates/storage/codecs/src/alloy/transaction/txtype.rs:37-58`
- Claim: Compact transaction type encoding preserves extended identifiers for scheduled, async commitment, async settlement, and passkey transactions instead of collapsing them into upstream Ethereum transaction types.
- Flow labels: `Scheduled Execution Trace`, `Short-Running Async SPC Trace`, `Passkey / P-256 Trace`
- Negative test: Replay the smallest Scheduled Execution Trace, Short-Running Async SPC Trace, Passkey / P-256 Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0466: crates/storage/codecs/src/alloy/transaction/passkey.rs

- Source: `crates/storage/codecs/src/alloy/transaction/passkey.rs:21-42`
- Claim: Passkey compact storage preserves chain id, nonce, gas, fees, kind, value, access list, settlement transaction, optional SPC calls, and trailing input for P-256 and WebAuthn transactions.
- Flow labels: `Passkey / P-256 Trace`
- Negative test: Replay the smallest Passkey / P-256 Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0528: crates/transaction-pool/src/pool/async_pool.rs

- Source: `crates/transaction-pool/src/pool/async_pool.rs:28-49`
- Claim: The async pool extracts resolved Phase 2 deadlines from precompile-specific ABI slots, including long HTTP, sovereign agent, FHE, persistent agent, and ZK layouts.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0528: crates/transaction-pool/src/pool/async_pool.rs

- Source: `crates/transaction-pool/src/pool/async_pool.rs:288-309`
- Claim: The async pool state machine distinguishes AwaitingExecution, Fulfilled, AwaitingDelivery, and DeliveryReady so short async settlement and long-running Phase 2 delivery do not share an ambiguous state.
- Flow labels: `Short-Running Async SPC Trace`, `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0528: crates/transaction-pool/src/pool/async_pool.rs

- Source: `crates/transaction-pool/src/pool/async_pool.rs:335-356`
- Claim: Async pool metadata keeps the original tx, commitment tx, precompile address/input, state, execution result/proof, commit block, delivery result/proof, and ZK proof needed to bridge Phase 1 and Phase 2.
- Flow labels: `Long-Running Two-Phase Trace`, `Executor And Operator Surface Compatibility`
- Negative test: Replay the smallest Long-Running Two-Phase Trace, Executor And Operator Surface Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:430-451`
- Claim: Payload building classifies heartbeat, obligations, async simulations, commitments, fulfilled async, delivery, sequencing rights, regular transactions, and diagnostics under one deadline and demotion policy.
- Flow labels: `Builder Obligation Compatibility`, `Scheduled Execution Trace`
- Negative test: Replay the smallest Builder Obligation Compatibility, Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:1297-1318`
- Claim: Heartbeat revival runs as a payload-builder phase that hydrates tracker state from contract storage on cold start and only injects checkAndRevive work when expired agents exist.
- Flow labels: `Persistent Agent Heartbeat And Revival Trace`
- Negative test: Replay the smallest Persistent Agent Heartbeat And Revival Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:1440-1461`
- Claim: Payload building hydrates scheduled state from the synchronous scheduler or forced contract scan before computing obligations against parent state and the global build deadline.
- Flow labels: `Scheduled Execution Trace`
- Negative test: Replay the smallest Scheduled Execution Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:1742-1763`
- Claim: Payload building collects async candidates at the start of block building and records collection stats, deadline fallback, scheduled candidate count, simulated count, accepted count, and skipped-due-to-deadline count.
- Flow labels: `Short-Running Async SPC Trace`, `Builder Obligation Compatibility`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Builder Obligation Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2278-2299`
- Claim: Fulfilled async collection is skipped when the global deadline has passed and capped by RETH_MAX_FULFILLED_ASYNC_PER_BLOCK, allowing settlements to roll to later blocks instead of overrunning payload construction.
- Flow labels: `Short-Running Async SPC Trace`, `Builder Obligation Compatibility`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Builder Obligation Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2337-2358`
- Claim: Fulfilled async processing batch-reads SPC verification data before per-transaction processing and falls back to per-tx verification only if the batch read fails.
- Flow labels: `Short-Running Async SPC Trace`, `Executor And Operator Surface Compatibility`
- Negative test: Replay the smallest Short-Running Async SPC Trace, Executor And Operator Surface Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2882-2903`
- Claim: Phase 2 delivery collection reads each delivery-ready job from AsyncJobTracker, defers jobs whose Phase 1 is not settled, and skips missing on-chain jobs instead of trusting pool state alone.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2967-2988`
- Claim: Phase 2 delivery settlement checks pool metadata against contract state for precompile input hash, commit block, and precompile address before constructing a delivery transaction.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2992-3013`
- Claim: Phase 2 delivery expiry uses the contract expiry block, computed as max commit block plus TTL or Phase 2 deadline, so proposer-side inclusion cannot diverge from verifier-side contract checks.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:1-19`
- Claim: Phase 2 delivery settlement construction verifies a delivery result exists, packs ZK result and proof together for ZK jobs, extracts the TEE address from the Phase 1 commitment, and creates the system settlement from contract job data.
- Flow labels: `Long-Running Two-Phase Trace`, `zk_two_phase`
- Negative test: Replay the smallest Long-Running Two-Phase Trace, zk_two_phase scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:5340-5361`
- Claim: Phase 2 delivery pricing branches by precompile: sovereign agents charge work-based fees, media and FHE charge result-derived fees or DA-error fees, persistent agents charge spawn fees, and HTTP/ZK use block-based pricing.
- Flow labels: `Long-Running Two-Phase Trace`, `Product Economics Compatibility`, `Multimodal Precompile Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace, Product Economics Compatibility, Multimodal Precompile Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:5238-5259`
- Claim: Phase 2 delivery settlement encodes an AsyncDelivery.deliver call and pays only the executor fee, with validator fees set to zero because Phase 1 already paid validators.
- Flow labels: `Long-Running Two-Phase Trace`
- Negative test: Replay the smallest Long-Running Two-Phase Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:2730-2751`
- Claim: Payload building injects SPC call data into passkey transactions when replaying fulfilled async outputs so passkey/P-256 transactions can carry the same settlement context as normal async transactions.
- Flow labels: `Passkey / P-256 Trace`, `Short-Running Async SPC Trace`
- Negative test: Replay the smallest Passkey / P-256 Trace, Short-Running Async SPC Trace scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.

### File 0092: crates/ethereum/payload/src/lib.rs

- Source: `crates/ethereum/payload/src/lib.rs:3299-3320`
- Claim: Payload sorting applies tip-maximizing ordering together with sequencing-rights policy and can demote sequencing-rights work when the build deadline is exceeded.
- Flow labels: `sequencing_rights_simple`, `Builder Obligation Compatibility`
- Negative test: Replay the smallest sequencing_rights_simple, Builder Obligation Compatibility scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.
