# Validity Constraint Audit - Second Pass

## Scope

This note continues `audit-loop-missed-findings.md` with a second read-only pass over:

- `ritual-reth-internal/crates/ethereum/payload/src/lib.rs`
- `ritual-reth-internal/crates/ritual-block-verification/src/verifier.rs`
- `ritual-reth-internal/crates/ritual-block-verification/src/nonce_lock.rs`
- shared async/scheduled/sequencing validity crates
- `ritual-sc-internal` contracts: `AsyncJobTracker`, `AsyncDelivery`, `Scheduler`, `AgentHeartbeat`, and `TEEServiceRegistry`

I pruned against the microsite matrix, GitHub issues `340`, `352`, `353`, the first-pass notes, `audit-loop-missed-findings.md`, and Asana task `1212349522094290`.

## New Candidate Findings

### 1. Async commitment calldata is not bound to the typed commitment fields

**Confidence:** high

**Category:** validity gap / contract side-effect binding gap

**Observed shape:**

- The builder creates a `TxAsyncCommitment` with typed fields such as `origin_tx`, `origin_tx_rlp`, `precompile_address`, `precompile_input`, `ttl`, `executor_address`, and `commitment_validator`.
- The same transaction also carries executable calldata for `AsyncJobTracker.addJob(...)`.
- `verify_async_commitments()` validates the typed commitment fields by re-simulating the origin transaction and checking the detected async precompile/input.
- I did not find a verifier check that decodes the commitment transaction `input` and proves that the `addJob(...)` arguments exactly match the typed commitment fields plus the parent header context.
- `AsyncJobTracker.addJob()` only sees calldata. It can enforce size, TTL, and active-job uniqueness, but it cannot know whether calldata matched the typed transaction fields that the verifier validated.

**Why this matters:**

A malicious proposer may be able to include a `TxAsyncCommitment` whose typed fields pass verifier re-simulation, while its executable `addJob(...)` calldata stores a different job in `AsyncJobTracker`: different executor, input hash, sender, `commitVal`, original RLP, or previous-block signing context. That creates a split between "what the verifier validated" and "what the block actually committed to contract state."

This is distinct from issue `353`. Issue `353` is about missing commitment coverage for in-block async calls. This finding is about a present commitment whose side effects are not canonically bound to the validated commitment fields.

**Likely source of truth:** parent block header, canonical origin transaction hash/RLP, async precompile detector result, and `AsyncJobTracker.addJob` ABI.

**Likely placement:** Reth verifier. Some size/TTL checks are already contract-enforced, but the equality between typed transaction fields and calldata must be verified before block acceptance unless the transaction type is redesigned to remove the duplicated representation.

**Concrete reproduction test:**

1. Build a valid async origin transaction and a matching `TxAsyncCommitment`.
2. Mutate only the commitment transaction calldata, e.g. `addJob.exec`, `addJob.input`, `addJob.sender`, `addJob.commitVal`, or `addJob.prevHash`, while leaving the typed `TxAsyncCommitment` fields unchanged.
3. Include the mutated commitment in a block.
4. Expected secure behavior: verifier rejects before execution or block import.
5. Suspected current behavior: verifier validates the typed fields, while execution stores the mutated calldata into `AsyncJobTracker`.

**Questions blocking final classification:**

- Is there any lower-layer transaction decoder that overwrites `input` from typed fields before execution? I did not see that in the reviewed paths.
- Is `TxAsyncCommitment.input` intended to be authoritative or merely cached derived data? The code currently treats it as executable calldata.

### 2. Settlement calldata is only partially bound to `AsyncJobTracker` state

**Confidence:** high

**Category:** validity gap / economic consistency gap

**Observed shape:**

- `verify_settlement_payments()` reads the job from `AsyncJobTracker`, verifies job existence, expiry, `keccak256(precompileInput) == job.input_hash`, expected executor payment address, expected fee amounts, and phase-specific validator fee semantics.
- I did not find checks binding `settlement_tx.user_address` / settlement calldata `user` to `job.sender`.
- For Phase 1, `AsyncDelivery.settle()` pays from the `user` address supplied in settlement calldata.
- For Phase 2, `AsyncDelivery.deliver()` pays executor/callback costs from the `user` address supplied in settlement calldata, then executes the supplied `target`, `selector`, callback gas, and callback value.
- The verifier extracts `precompileInput` for pricing and hash checks, but I did not find a verifier check that the Phase 2 delivery calldata's `target`, `selector`, `callbackGasLimit`, `callbackValue`, `maxFeePerGas`, or `maxPriorityFeePerGas` equals the delivery config encoded in the original precompile input.

**Why this matters:**

If the settlement transaction's payment/callback fields can differ from the original job's canonical input and sender, a proposer can potentially settle a valid job while billing the wrong wallet, routing callback value to the wrong target, or changing the callback envelope. The contract cannot fully enforce this because it receives only settlement calldata and an input hash; it does not decode every protocol-level relationship back to the original precompile request.

This overlaps with issue `352` / microsite "Coinbase / Fee-Recipient Binding", but appears broader than fee-recipient binding. It includes `user` and Phase 2 delivery config binding.

**Likely source of truth:** `AsyncJobTracker` job fields plus the precompile-family delivery config decoded from the hashed `precompileInput`.

**Likely placement:** Reth verifier, with selective contract reinforcement where cheap:

- Contract can enforce input hash and job existence, which it already does.
- Reth should enforce `settlement.user == job.sender`.
- Reth should decode delivery config from `precompileInput` and compare Phase 2 `deliver(...)` calldata fields.

**Concrete reproduction tests:**

1. Phase 1: create a valid committed job for user `U`; include settlement with identical `origin_tx`, input hash, fees, and executor address, but set `user = V`.
2. Phase 2: create a phase-1-settled long-running job with delivery config `(target=T, selector=S, gas=G, value=W)`; include delivery settlement with `target=T2` or `value=W2` while keeping `precompileInput` unchanged.
3. Expected secure behavior: verifier rejects.
4. Suspected current behavior: verifier may accept as long as input hash, fees, expiry, and executor payment address match.

**Questions blocking final classification:**

- Does `RitualWallet` internally bind `jobId` to the same user at debit time? If yes, that may reduce the payment-address part, but the verifier should still reject mismatched settlement calldata for consensus clarity.
- Are any Phase 2 precompile families intentionally allowed to override callback target/value at delivery time? I did not see evidence that they are.

### 3. Coinbase / fee-recipient binding appears unverified

**Confidence:** medium-high

**Category:** economic validity gap

**Observed shape:**

- The builder passes `attributes.suggested_fee_recipient()` as the commitment validator and inclusion validator for Phase 1.
- The verifier checks Phase 1 `settlement_tx.commitment_validator == job.commitment_validator`.
- I did not find a verifier check that the original commitment's `commitment_validator` equals the block beneficiary / coinbase.
- I also did not find any verifier check for Phase 1 `settlement_tx.inclusion_validator` beyond fee amount correctness.

**Why this matters:**

A malicious proposer can potentially route validator-side async fees to an arbitrary address while still producing a block that satisfies the current purity checks. This confirms the microsite / issue `352` "needs audit" item as likely live, not just hypothetical.

**Likely placement:** Reth verifier; contracts do not know the block beneficiary.

**Concrete reproduction test:**

1. Include a valid async commitment with `commitment_validator = attacker` while the block beneficiary is `B`.
2. Include a Phase 1 settlement with `commitment_validator = attacker` and `inclusion_validator = attacker`.
3. Expected secure behavior: verifier rejects because both validator fee recipients are not `block.header().beneficiary()`.
4. Suspected current behavior: verifier accepts if fee amounts and job state match.

**Duplicate status:** already suspected by issue `352` and the microsite, but this pass found no verifier binding, so it should be promoted from "needs audit" to a concrete candidate.

### 4. Sequencing-rights full-call-graph mode is an env-driven consensus parameter

**Confidence:** medium-high

**Category:** consistency gap / local config can change validity

**Observed shape:**

- `RITUAL_SEQUENCING_RIGHTS_FULL_CALL_GRAPH_ENABLED` controls whether sequencing-rights classification uses only top-level calls or performs full EVM call-graph inspection.
- The builder and verifier both call `sequencing_rights_full_call_graph_enabled()`.
- If validators run with different values, they can classify the same transaction differently and disagree on whether the block order violates sequencing rights.

**Why this matters:**

This is not the same as issue `352` Gap 3, which concerns builder deadline-skip asymmetry. This is a separate local configuration split: even with no deadline skip, nodes can disagree on the classification predicate itself.

**Likely source of truth:** chain/fork config, not process env.

**Concrete reproduction test:**

1. Build a block containing a transaction whose top-level target has no sequencing rights but whose internal call graph reaches a sequencing-rights contract.
2. Order it such that the block is valid under top-level classification but invalid under full-call-graph classification.
3. Run verifier once with `RITUAL_SEQUENCING_RIGHTS_FULL_CALL_GRAPH_ENABLED=0` and once with `=1`.
4. Expected secure behavior: both nodes agree.
5. Suspected current behavior: acceptance differs.

**Coverage comparison:** not covered by Asana `1212349522094290`, which only names model/executor registry address migration. It should be added to the broader env/config migration inventory.

### 5. Verifier fail-open constructors need production-use confirmation

**Confidence:** medium

**Category:** emergency bypass / missing counterpart if used in production

**Observed shape:**

- `verify_async_commitments()` returns `Ok(())` when `state_provider` or `evm_env_factory` is absent.
- `verify_scheduled_censorship()` returns `Ok(())` when `state_provider` is absent.
- `BlockVerifier::new(pool)` constructs a verifier with no state provider and no EVM config.
- Other phases, such as nonce locks and sequencing rights, hard-fail when required state/EVM config is missing.

**Why this matters:**

If `BlockVerifier::new(pool)` is reachable on a production/import path, key validity checks silently do not run. If it is only test or legacy construction, this is a non-issue but should be made explicit.

**Concrete reproduction test:**

1. Instantiate `BlockVerifier::new(pool)`.
2. Verify a block containing an invalid async commitment that would fail re-simulation under `new_with_evm_classification`.
3. Verify a block omitting a scheduled obligation with remaining gas capacity.
4. Expected secure behavior: production verifier construction should reject or be impossible without required state/EVM dependencies.

**Questions blocking final classification:**

- Which verifier constructor is used by the engine tree / block import path in current `dev`?
- Are no-state verifier modes intentionally limited to tests or RPC-only diagnostics?

## Suspected Duplicates / Already Covered Work

- **Async commitment coverage for in-block async calls:** covered by issue `353` and microsite "Async Commitment Coverage." The new commitment-calldata binding finding is adjacent but not the same.
- **Heartbeat `checkAndRevive` inclusion and `reviveAgent` inclusion:** covered by issue `352` and microsite. The first-pass note already separated `reviveAgent` payload purity.
- **Delivery timeout/refund inclusion:** covered by issue `352` and microsite.
- **Sequencing-rights deadline skip:** covered by issue `352` and microsite. The env-driven full-call-graph mode is separate.
- **Runtime address migration:** Asana `1212349522094290` covers `MODEL_REGISTRY_CONTRACT_ADDRESS` and executor/TEE registry address migration to chain config. It does not appear to cover scheduler/wallet/system/heartbeat addresses, `ASYNC_MAX_TTL_BLOCKS`, sequencing-rights mode, or emergency bypass flags.
- **Async payload validation RPC-only, input-size drift, two-phase fail-open, same-block nonce lock, revive payload purity, reverted-origin semantics:** covered in `audit-loop-missed-findings.md`.

## Builder Phase Obligation Map

| Builder phase | Builder action | Semantic obligation | Source of truth | Verifier counterpart | Can omission / mutation / reordering / local config change validity? |
| --- | --- | --- | --- | --- | --- |
| Initialization | Builds EVM for next block, applies pre-execution changes, reads `MODEL_REGISTRY_CONTRACT_ADDRESS`, tx caps, block size limits, build policy. | Block env and pricing inputs must match verifier/import. | Parent header, payload attributes, chain spec, model registry address. | Standard execution/import plus settlement fee verifier. | Yes for model registry env; local caps are mostly builder policy unless they suppress required inclusion. |
| Heartbeat Phase 0b | Optionally injects `checkAndRevive()` when tracker sees expired agents. | If heartbeat liveness is consensus-required, block should include the check under deterministic conditions. | `AgentHeartbeat` parent state; tracker is builder-local cache. | Purity-only CH checks when present. | Omission changes liveness; covered by issue `352`. Local skip knobs matter if inclusion becomes mandatory. |
| Scheduled obligation augmentation | Computes due Scheduler obligations from pool or contract scan and filters C11 predicates. | Due scheduled calls should be included if capacity exists. | `Scheduler` state, wallet state, C11 predicate result at parent state. | `verify_scheduled_censorship()` inclusion check. | Yes; verifier checks omission except active async job and gas-cap cases. Env cap consistency remains important. |
| Async Phase 1 detection | Simulates scheduled and regular candidates with async inspector under sim caps/deadline. | Any included async-precompile call must have a commitment; committed payload must match detection. | Parent-state EVM simulation and async precompile codecs. | Present commitments validated; missing coverage covered by issue `353`. | Yes; local sim caps are safe only if unclassified txs are not included. |
| Async commitment execution | Executes `TxAsyncCommitment` system txs to call `AsyncJobTracker.addJob`. | `addJob` side effect must match the validated typed commitment. | Typed commitment fields, parent header, canonical origin tx encoding, `AsyncJobTracker` ABI. | Partial: structure + re-simulation only. | Yes; new finding 1. |
| Scheduled collection/filter | Pulls scheduled txs from pool, checks C1-C10 and C11, adds non-async scheduled txs to unified collection. | Included scheduled txs must be valid and predicate-true. | `Scheduler`, wallet, C11 predicate. | `verify_scheduled_transactions()`. | Mutation/reordering can violate C constraints or C11. |
| Augmented scheduled execution | Executes contract-derived scheduled txs missing from pool. | Contract-state obligations should be executable even when local pool is stale. | `Scheduler` contract state. | Censorship verifier treats scheduled tx or commitment-wrapped scheduled origin as fulfilled. | Omission covered if gas remains; execution failures remain contract/state-root visible. |
| Fulfilled async Phase B | Converts fulfilled async pool metadata to original tx + settlement pair; reads job from contract; injects SPC; verifies SPC at build time. | Settlement pair must be atomic; SPC must bind executor output to job. | `AsyncJobTracker`, TEE registry, model registry, SPC signature payload. | Settlement payment verifier + SPC verifier. | Yes if settlement calldata or SPC differs; new finding 2 for settlement field binding. |
| Phase 2 delivery collection | Reads delivery-ready jobs from pool, re-reads job from contract, creates `AsyncDelivery.deliver` tx. | Delivery settlement must match job state and original delivery config. | `AsyncJobTracker`, precompile input hash, delivery config encoded in input. | Settlement verifier checks input hash/fees/expiry/payment address, not all delivery config fields observed in this pass. | Yes; new finding 2. |
| Nested async from delivery | Simulates delivery callback; if nested async detected, emits nested commitment and defers delivery. | Callback-triggered async work must be committed or delivery semantics change. | Parent-state EVM simulation of delivery settlement. | Missing coverage covered by issue `353`. | Yes; already covered. |
| Regular tx collection | Includes only txs classified as not async and not nonce-locked. | Regular txs must not bypass async commitment or nonce locks. | Async detector, `AsyncJobTracker` sender jobs. | Nonce lock verifier; missing async coverage issue `353`. | Yes if unclassified async txs enter block; covered. |
| Sort + sequencing rights | Tip-sort, then optionally reorder by sequencing-rights priority. | SR buckets must be monotonic by contract-defined priority. | Sequencing-rights contract state at parent state. | `verify_sequencing_rights()`. | Yes; deadline skip covered by issue `352`; env full-call-graph mode is new finding 4. |
| Unified execution | Executes single txs, fulfilled async pairs atomically, and delivery settlements. | Header gas/state root must reflect the same custom accounting and atomicity semantics. | Block executor, async gas rules, settlement contracts. | Standard execution plus settlement verifier. | Possible; async gas accounting already "needs audit" in microsite. |
| Finalization / diagnostics | Seals block, creates payload, logs post-build SR diagnostics. | Diagnostics should not affect validity. | Local observability only. | None required. | No, unless diagnostic-only paths are mistaken for enforcement. |

## Verifier Phase Classification

| Verifier phase | Main checks | Classification | Builder counterpart | Missing / weak counterpart |
| --- | --- | --- | --- | --- |
| `verify_async_commitments` | Duplicate sender, active-job absence, TTL/precompile/executor, wallet, two-phase deadline, re-simulation equality. | Purity + global block check. | Async detection + commitment execution. | No coverage rule for omitted commitments (`353`); no binding of commitment calldata to typed fields (new finding 1). |
| `verify_settlement_payments` | Job exists, not expired, input hash, Phase 1 adjacency, fee amounts, executor payment address, commitment validator for Phase 1. | Purity + contract-state check. | Phase B / Phase C settlement creation. | Settlement `user`, inclusion validator, and Phase 2 callback config appear under-bound (new findings 2 and 3). |
| `verify_spc_calls` | SPC proof length, executor extraction, job exists, block number, input hash, executor key, signature. | Purity + contract-state check. | SPC injection and build-time verification. | Does not require SPC presence except when settlement/origin carries it; inclusion coverage is tied to settlement presence. |
| `verify_scheduled_transactions` | C1-C11 and CH2-CH9 for scheduled/heartbeat txs present in block. | Purity check; C11 is parent-state deterministic. | Scheduled filtering and heartbeat injection. | Heartbeat/revival inclusion covered by issue `352`; revive payload purity covered by first pass. |
| `verify_nonce_locks` / `nonce_lock.rs` | Parent-state sender locks, in-block duplicate commitments, fulfillment exemption. | Global block check. | Regular collection sender-lock filter. | Same-block commitment locking later regular tx from same sender covered by first pass. |
| `verify_sequencing_rights` | Classify txs and enforce monotonic priority per SR contract. | Global block order check. | Sequencing-rights reorder in unified builder. | Deadline skip covered by issue `352`; env full-call-graph mode new finding 4. |
| `verify_scheduled_censorship` | Recomputes due obligations and rejects omissions with enough gas. | Inclusion check. | Obligation augmentation and scheduled collection. | No analogous inclusion checks for heartbeat, revival, async coverage, delivery timeout; mostly covered by issue `352` / `353`. |

## Async Precompile Family Matrix

Legend: `Y` = explicit path exists, `Partial` = only common fields or fee-only check, `No` = not observed, `N/A` = not applicable or not consensus-visible.

| Family | Codec validation | RPC validation | Builder detector | Commitment verifier | Settlement verifier | Contract validation | Executor assumption / notable gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HTTP `0x0801` | ABI + URL/model-specific codec. | `validate_async_payload()` checks URL scheme, executor, TTL, secrets/key. | Extracts executor/TTL and 10KB size. | Re-simulation + typed input equality; no full payload validation call observed. | Phase 1 fee/input-hash checks. | Size/TTL/input hash via tracker. | Executor assumes URL semantics; RPC-only URL checks remain first-pass finding. |
| LLM `0x0802` | LLM codec with model/messages. | Checks non-empty model/messages. | Common executor/TTL + size. | Re-simulation + typed input equality only. | Phase 1 model registry pricing. | Size/TTL/input hash. | Model existence enforced during pricing, but payload semantic checks are not fully verifier-side. |
| Long HTTP `0x0805` | Long-running codec with URL/poll/result URLs and delivery config. | URL checks; deadline offset not fully shared with all paths. | Executor/TTL/size + deadline subset. | Two-phase deadline check but fail-open on extraction covered first pass. | Phase 2 fees and input hash; callback config binding appears weak. | Phase2 offset cap, size, TTL, input hash. | Delivery target/gas/value should be verifier-bound to input. |
| ZK `0x0806` | Base executor request + delivery config. | Base checks only. | Executor/TTL/size + deadline subset. | Two-phase deadline check. | ZK proof verification appears stubbed; fee/input checks. | Phase2 offset cap, fees u128, input hash. | Proof correctness remains known broader audit item. |
| FHE `0x0807` | Base + best-effort structure validation. | Base checks; FHE structure debug-only on failure. | Executor/TTL/size; no detector deadline check observed in first pass. | Two-phase deadline check with FHE-specific offset. | Output-size fee extraction. | Phase2 offset cap and u128 fee field checks. | StorageRef/content-hash/executor assumptions remain mostly off-chain. |
| Sovereign Agent `0x080C` | Custom codec. | Prompt/model/agent-type/deadline checks. | Executor/TTL/size + deadline. | Two-phase deadline check. | Work-based Phase 2 pricing. | Phase2 offset cap and input hash. | Capability/model/prompt semantics mostly RPC/executor; revival payload binding covered first pass. |
| Image `0x0818` | Base executor request. | Base checks only. | Executor/TTL/size; no detector deadline check observed in first pass. | Two-phase deadline check. | Dimensions/model/UX pricing from input/result. | Phase2 offset cap and input hash. | Delivery config binding and media output truth remain weak/known. |
| Audio `0x0819` | Base executor request. | Base checks only. | Executor/TTL/size; no detector deadline check observed in first pass. | Two-phase deadline check. | Duration/model pricing. | Phase2 offset cap and input hash. | Delivery config binding and output truth remain weak/known. |
| Video `0x081A` | Base executor request. | Base checks only. | Executor/TTL/size; no detector deadline check observed in first pass. | Two-phase deadline check. | Dimensions/duration/model/UX pricing. | Phase2 offset cap and input hash. | Delivery config binding and output truth remain weak/known. |
| DKMS `0x081B` | DKMS codec. | Executor/owner/TTL/secrets/key; no `key_format` check observed. | Common executor/TTL + size. | Re-simulation + typed input equality. | Phase 1 fee/input checks. | Size/TTL/input hash. | `key_format` validation is already in issue `340`; likely RPC/executor-side unless promoted. |
| Persistent Agent `0x0820` | Custom codec. | Model non-empty and base checks; deadline offset not validated here. | Executor/TTL/size + deadline. | Two-phase deadline check. | Payload-length Phase 2 pricing. | Phase2 offset cap and input hash. | Delivery config binding and model/capability assumptions mostly off-chain/RPC. |

Field focus summary:

- **Executor:** typed commitment checks non-zero; settlement checks expected payment address. Commitment calldata must also be bound to typed executor (new finding 1).
- **TTL:** checked by shared extraction, commitment verifier, and contract. `ASYNC_MAX_TTL_BLOCKS` remains env-driven.
- **Input size:** RPC uses 1MB; detector/contract/fees use 10KB. Covered first pass.
- **Deadline:** duplicated per-family offsets; fail-open and family coverage covered first pass.
- **Delivery config:** builder decodes it to create Phase 2 delivery; verifier does not appear to compare all delivery calldata fields back to decoded input (new finding 2).
- **Fees:** verifier recomputes amounts, but recipient binding is weak (new finding 3).
- **Callback gas/value:** builder derives from input; contract executes settlement calldata; verifier should compare.
- **Model/capability:** model registry is enforced for fee calculation in some paths; capability matching is mostly TEE registry / executor policy, not uniformly verifier-side.
- **Output/result binding:** SPC binds signed output for allowlisted Phase 1; Phase 2 uses settlement result bytes for fee extraction but proof/content correctness varies by family.

## Runtime Config Classification

| Config / env var | Readers observed | Classification | Existing coverage |
| --- | --- | --- | --- |
| `MODEL_REGISTRY_CONTRACT_ADDRESS` | Builder, verifier, fees wallet. | Consensus-critical. | Asana `1212349522094290` covers. |
| `TEE_SERVICE_REGISTRY_CONTRACT_ADDRESS` | Verifier, registry reader, async registry, cached-state pinning, SPC config. | Consensus-critical. | Partially covered by Asana as executor registry. |
| `ASYNC_JOB_TRACKER_ADDRESS` | Async registry, cached-state pinning. | Consensus-critical. | Not explicitly covered by Asana notes retrieved. |
| `ASYNC_DELIVERY_ADDRESS` | Async wallet / cached-state pinning. | Consensus-critical. | Not explicitly covered by Asana notes retrieved. |
| `SCHEDULER_ADDRESS` | Scheduled verification. | Consensus-critical. | Not covered by Asana `1212349522094290`. |
| `RITUAL_WALLET_ADDRESS` | Scheduled verification, async fees wallet, cached-state pinning. | Consensus-critical. | Not covered by Asana `1212349522094290`. |
| `SYSTEM_ACCOUNT_ADDRESS` | Scheduled verification. | Consensus-critical. | Not covered by Asana `1212349522094290`. |
| `AGENT_HEARTBEAT_ADDRESS` | Scheduled verification, builder, cached-state pinning. | Consensus-critical if heartbeat rules are active. | Not covered by Asana `1212349522094290`. |
| `ASYNC_MAX_TTL_BLOCKS` | Async inspector, validation, commitment validator. | Consensus-critical. | First-pass env finding; not Asana-covered. |
| `RITUAL_SEQUENCING_RIGHTS_FULL_CALL_GRAPH_ENABLED` | Sequencing-rights builder/verifier classification. | Consensus-critical. | New finding 4; not Asana-covered. |
| `SKIP_VALIDITY_CONSTRAINTS` | Block verifier. | Emergency bypass. | Microsite "Production Validity Bypass Controls"; not Asana-covered. |
| `RETH_MAX_OBLIGATIONS_PER_BLOCK` | Builder and scheduled verification. | Consensus-affecting inclusion cap if used to prune obligations. | Issue `352` Gap 10 pattern; not Asana-covered. |
| `RETH_MAX_ASYNC_SIMS_PER_BLOCK`, `RETH_MAX_SCHEDULED_ASYNC_SIMS_PER_BLOCK`, `RETH_MAX_REGULAR_ASYNC_SIMS_PER_BLOCK`, `RETH_ASYNC_SIM_DEADLINE_MS` | Builder async detection. | Builder-local policy only if async coverage verifier exists; otherwise can affect missing-commitment behavior. | Issue `353` covers missing coverage. |
| `RETH_MAX_FULFILLED_ASYNC_PER_BLOCK`, `RETH_MAX_DELIVERY_PER_BLOCK` | Builder fulfilled/delivery collection. | Builder-local policy unless timeout/refund inclusion becomes consensus. | Issue `352` delivery timeout inclusion. |
| `RETH_MAX_TRANSACTIONS_PER_BLOCK`, `RETH_BUILD_DEADLINE_MS`, `RETH_PAYLOAD_SEAL_EPSILON_MS`, `RETH_POLICY_LOOP_CHECK_INTERVAL` | Builder policy. | Builder-local policy, but dangerous if used to skip required protocol work. | Gap-pattern covered by issue `352`. |
| `RETH_HEARTBEAT_SKIP_THRESHOLD_MICROS`, `RETH_REVIVAL_SKIP_PCT`, `RETH_REVIVAL_SKIP_MIN_COUNT`, `RETH_REVIVAL_SUBSET_ON_STALL`, `RETH_MAX_REVIVAL_SIMS_WHEN_STALLED` | Builder heartbeat/revival. | Builder-local policy today; consensus-critical if revival inclusion is formalized. | Issue `352`. |
| `RITUAL_FORCE_CONTRACT_SCAN`, `RITUAL_ZERO_POOL_SCHEDULED` | Builder scheduled augmentation. | Builder-local/testing policy; can affect liveness but verifier catches due scheduled omissions. | Not necessary if verifier remains authoritative. |
| `RITUAL_BLOCK_BUILD_TRACE_ENABLED`, `RITUAL_SCHEDULED_INCIDENT_TRACE_ENABLED`, trace capacities | Metrics. | Observability only. | Microsite observability PR. |
| `RETH_MAX_POOL_CALLDATA_BYTES`, `RETH_MAX_SENDER_CALLDATA_BYTES`, `RETH_MAX_TX_INPUT_BYTES`, `CHAIN_HALT_THRESHOLD_SECS` | Pool/maintenance. | RPC/mempool-only or operational policy. | Not consensus unless reused during import. |
| `RITUAL_SIDECAR_BASE_URL`, `SPC_VERIFICATION_*`, `TEE_SERVICE_REGISTRY_MAX_SIZE` | RPC/SPC sidecar config. | RPC/off-chain verification policy, unless used in block verifier path. | Needs separate SPC operational audit, not a Reth validity rule from this pass. |

## Contract-Enforceable Reth Invariants

Only checks enforceable from calldata/state are listed.

| Contract | Reth-side invariant | Contract-enforceable? | Notes |
| --- | --- | --- | --- |
| `AsyncJobTracker` | `ttl` bounds, input/origin RLP max size, active job uniqueness, input hash match for settlement, phase1/phase2 state, phase2 offset max. | Yes, mostly already enforced. | Contract cannot bind typed `TxAsyncCommitment` fields to `addJob` calldata; Reth must. |
| `AsyncJobTracker` | `phase2_offset > ttl`. | Yes. | Contract currently checks offset max; adding `> ttl` is enforceable from stored job TTL and decoded input. |
| `AsyncJobTracker` | `addJob.sender` equals decoded origin transaction sender. | Not cheaply inside Solidity without full tx decoding/signature recovery. | Reth verifier should enforce by binding calldata to typed fields and decoded origin. |
| `AsyncDelivery` | `precompileInput` hash matches job. | Yes, already delegated to tracker. | Good contract-side anchor. |
| `AsyncDelivery` | Settlement `user == job.sender`. | Yes if `AsyncDelivery` reads job sender or tracker exposes it. | Currently appears Reth-side only; worth considering contract-side because it is state/calldata-enforceable. |
| `AsyncDelivery` | Phase 2 `target`, `selector`, gas/value match delivery config in `precompileInput`. | Partially. | Enforceable if contract decodes per-family delivery config. Might be expensive/duplicative; verifier is the likely minimum. |
| `AsyncDelivery` | `commitmentValidator` / `inclusionValidator` equals block coinbase. | No. | Contracts cannot read block beneficiary in EVM semantics; Reth must enforce. |
| `Scheduler` | C1-C10 execution validity, sender system account, index, due/expired state, funds, replay. | Yes, mostly already enforced. | C11 custom predicate remains Reth-side because `execute()` intentionally does not call arbitrary predicate during execution. |
| `Scheduler` | Anti-censorship inclusion of due scheduled txs. | No. | Requires global block context/capacity; Reth-only. |
| `AgentHeartbeat` | `checkAndRevive` caller, `reviveAgent` caller, failed-state requirement, non-empty manifest. | Yes, mostly enforced. | Contract can also decode/bind some revival payload fields if ABI stable. |
| `AgentHeartbeat` | `reviveAgent(agent, precompileInput)` input agent/model/manifest/DA config matches stored agent record. | Partially yes. | Contract currently extracts only executor; deeper binding is calldata/state-enforceable but may require decoding persistent-agent ABI. |
| `AgentHeartbeat` | Inclusion of `checkAndRevive` / `reviveAgent`. | No. | Requires global block inclusion/capacity; Reth-only. |
| `TEEServiceRegistry` | Executor/payment address exists, public key exists, capability assigned, service active/attestation valid. | Yes for direct lookups/registration. | Reth should use registry state as source of truth; capability matching per precompile may need explicit verifier policy. |
| `TEEServiceRegistry` | Selected revival executor is the canonical one. | Partially. | Registry can expose indexed capability sets; exact deterministic selection is easier to specify in Reth unless moved into contract API. |

## Concrete Test Backlog

1. Mutated async commitment `addJob` calldata vs typed fields: executor/input/sender/commit validator/prev header.
2. Async commitment `to != AsyncJobTracker` or calldata not `addJob`, while typed fields pass re-simulation.
3. Phase 1 settlement with `user != job.sender`.
4. Phase 1 settlement with `inclusion_validator != block.beneficiary`.
5. Async commitment with `commitment_validator != block.beneficiary`, followed by matching settlement.
6. Phase 2 delivery with `target`, `selector`, `callbackGasLimit`, or `callbackValue` changed from the delivery config encoded in `precompileInput`.
7. Sequencing-rights indirect-call block verified under `RITUAL_SEQUENCING_RIGHTS_FULL_CALL_GRAPH_ENABLED=0` vs `=1`.
8. `BlockVerifier::new(pool)` negative test: invalid async commitment and omitted scheduled obligation should not silently pass on any production construction path.
9. Contract-level test: `AsyncDelivery` rejects `user != job.sender` if that invariant is moved on-chain.

## Open Questions

- Which `BlockVerifier` constructor is used in every production/import path?
- Is `TxAsyncCommitment.input` intended to be canonical executable calldata, or can it be recomputed from typed fields before execution?
- Should validator fee recipients for async commitments and settlements always be `block.header().beneficiary()`, or is there a protocol reason to allow a different address?
- Does `RitualWallet` bind debits to the original job sender internally, or does it trust settlement calldata `user`?
- Are any delivery precompile families allowed to mutate callback target/gas/value at delivery time?
- Should `RITUAL_SEQUENCING_RIGHTS_FULL_CALL_GRAPH_ENABLED` be removed, fixed at compile time, or moved to fork config?
