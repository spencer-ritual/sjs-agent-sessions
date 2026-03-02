# ritual-reth Fork Diff Analysis

## Overview

**Fork base:** reth v1.3.12 (upstream)
**Merge-base commit:** `6f8e7258f` — `chore: release 1.3.12 (#15797)`
**Upstream branch:** `origin/upstream/v1.3.12`
**Working branch:** `dev`
**Total commits since fork:** 920
**Total files changed:** 573
**Lines changed:** +63,534 / -4,705

---

## Summary Table of Feature Areas

| # | Feature Area | New Crates | Files Changed | Est. Commits | Lines Added |
|---|---|---|---|---|---|
| 1 | **Custom Transaction Types** | — | ~15 | ~50 | ~2,500 |
| 2 | **Async Transaction Execution** | `ritual-async`, `ritual-async-inspector`, `ritual-async-registry`, `ritual-async-commitment-validator` | ~30 | ~250 | ~8,000 |
| 3 | **Async Fee Calculation** | `ritual-async-fees` | ~12 | ~60 | ~5,600 |
| 4 | **Precompile Codecs** | `ritual-precompile-codecs` | ~10 | ~40 | ~4,500 |
| 5 | **SPC Verification** | `ritual-spc-verification`, `ritual-spc-signature` | ~8 | ~40 | ~2,200 |
| 6 | **Block Verification / Validity Constraints** | `ritual-block-verification` | ~8 | ~80 | ~6,000 |
| 7 | **Scheduled Transactions** | `scheduling`, `ritual-scheduled-block-building`, `ritual-scheduled-verification` | ~15 | ~100 | ~6,500 |
| 8 | **Sequencing Rights** | `ritual-sequencing-rights` | ~6 | ~15 | ~2,500 |
| 9 | **Heartbeat Tracker** | `ritual-heartbeat-tracker` | ~4 | ~15 | ~500 |
| 10 | **TEE Registry Reader** | `ritual-tee-registry-reader` | ~6 | ~15 | ~720 |
| 11 | **Payload Builder Modifications** | — | ~8 | ~80 | ~5,200 |
| 12 | **Transaction Pool Extensions** | — | ~31 | ~80 | ~5,300 |
| 13 | **RPC Extensions** | — | ~20 | ~40 | ~2,200 |
| 14 | **Metrics & Instrumentation** | `ritual-metrics` | ~5 | ~30 | ~1,000 |
| 15 | **Chainspec & Consensus Modifications** | — | ~8 | ~20 | ~450 |
| 16 | **Storage Codec Extensions** | — | ~12 | ~20 | ~1,250 |
| 17 | **Engine Tree / Cached State** | — | ~10 | ~15 | ~400 |
| 18 | **Networking / P2P Changes** | — | ~60 | ~10 | ~300 |
| 19 | **Blocking PubSub** | `ritual-blocking-pubsub` | ~2 | ~5 | ~50 |
| 20 | **CI / Tooling / Docs** | — | ~15 | ~25 | ~1,800 |

---

## Detailed Feature Area Breakdown

---

### 1. Custom Transaction Types

**Summary:** The fork introduces 6+ new Ethereum transaction types beyond the standard EIP types: `TxAsyncCommitment`, `TxAsyncSettlement`, `TxScheduled`, `TxSpcCall`, `TxPasskey`, and more. These are core to the Ritual chain's async execution model and are deeply integrated into the transaction envelope, RLP encoding, hashing, signing, and receipt handling.

**Key files changed:**
- `crates/ethereum/primitives/src/transaction.rs` (+1,246 lines) — The largest single-file change. Adds new `EthTxEnvelope` variants for all custom types, implements `From`/`Into` conversions, RLP encode/decode, hash computation, gas limit handling, `as_async()`, `as_scheduled()` helpers, and `FromRecoveredTx` for all 9 transaction types.
- `crates/ethereum/primitives/src/receipt.rs` (+18) — Adds `spc_calls` and `delivery_spc_calls` fields to receipts for tracking system precompile call outputs.
- `crates/storage/codecs/src/alloy/transaction/` — New codec files for each custom transaction type:
  - `async_commitment.rs` (+82)
  - `async_settlement.rs` (+101)
  - `scheduled.rs` (+96)
  - `spc_call.rs` (+349)
  - `passkey.rs` (+80)
  - `txtype.rs` (+35) — Extended `TxType` enum
  - `ethereum.rs` (+179) — Updated `EthTxEnvelope` codec
- `crates/storage/codecs/src/alloy/passkey_signature.rs` (+148)

**Representative commits:**
- `d139cd221` feat: populate tx_hash in FromRecoveredTx for all 9 transaction types
- `2747ac87d` feat: add passkey transaction type support to reth
- `c2c244efa` feat: implement async settlement tx
- `8b4e9726a` fix: rename asyncexec to asynccommitment
- `8d05a1a80` feat: implement as_async() && uncover async tx when getting it in the mempool
- `cad8a2efa` feat: add P256 verification to TransactionSigned and preserve passkey signatures in payload builder
- `5e4af4cfe` feat(passkey): preserve runtime fields in TxEnv conversion (GAP-1 fix)

---

### 2. Async Transaction Execution (Core)

**Summary:** The centerpiece feature of the fork. Implements a two-phase async execution model where:
1. **Phase 1 (Commitment):** A user submits a transaction that calls a Ritual precompile (HTTP call, LLM call, ONNX, FHE, agent call, etc.). The EVM detects it, creates an `AsyncCommitment` transaction, and parks it in the async pool. An off-chain executor processes the job.
2. **Phase 2 (Settlement):** Once the executor returns a result, a `TxAsyncSettlement` transaction is created and included in a future block, containing the result and SPC calls.

This involves a custom `AsyncExecPool` subpool in the transaction pool, an async precompile inspector that hooks into the EVM, an async registry for tracking job state, and a commitment validator for block verification.

**New crates:**
- `crates/ritual-async/` — Core async detection (`detector.rs` ~1,296 lines), validation (`validation.rs` ~910 lines), wallet checks (`wallet.rs` ~116 lines)
- `crates/ritual-async-inspector/` — Shared EVM inspector for detecting precompile calls during execution (`inspector.rs` ~229 lines)
- `crates/ritual-async-registry/` — On-chain state reader for async job tracking (`lib.rs` ~2,223 lines, `slots.rs` ~155 lines)
- `crates/ritual-async-commitment-validator/` — Block-level async commitment validation (`lib.rs` ~589 lines)

**Key modified files:**
- `crates/evm/src/lib.rs` (+178) — Adds `ExecutionMode` (Build vs Verification), `AsyncCallMetadata`, `RitualAsyncContext` with thread-local storage, EVM context injection
- `crates/evm/src/spc.rs` (+151) — SPC (System Precompile Call) execution logic
- `crates/evm/src/pool_manager.rs` (+89) — Async pool management interface
- `crates/evm/src/async_context_tests.rs` (+99)
- `crates/evm/src/execute.rs` (+28) — Execution hooks for async context

**Representative commits:**
- `f454907d6` fix: prevent duplicate async commitments via contract state check
- `040df5782` fix: self-healing pool cleanup for duplicate async jobs
- `805eab0cd` fix: fail block building if cannot check for duplicate async jobs
- `b17fd7cae` Refactor EVM async context to use direct context access instead of EvmEnv fields
- `ecdcc58e1` Complete async context injection in RETH EVM factory with thread-local storage workaround
- `af35e16a0` feat: implement Task 9 async transaction processing in payload builder with ExecutionMode::Verification
- `2df8ff56f` feat: implement Task 7 async SpcCall extraction in payload builder
- `1ed3f777c` feat: extend TransactionPool trait with async result submission methods
- `a4b25926b` feat: add async transaction update methods and error types to AsyncExecPool
- `ee147f001` feat(block-verification): add intra-block duplicate commitment sender check

---

### 3. Async Fee Calculation

**Summary:** Comprehensive fee calculation system for all async precompile types. Includes per-model LLM pricing via an on-chain `ModelPricingRegistry`, multimodal pricing (text, image, audio, video), HTTP call pricing, FHE pricing, DKMS pricing, and gas bifurcation for system transactions. Features a per-block model cache for performance.

**New crate:** `crates/ritual-async-fees/`
- `lib.rs` (~1,738 lines) — Main fee calculation engine, dispatches by precompile address
- `llm.rs` (~817 lines) — LLM-specific pricing with token estimation, model lookups
- `registry.rs` (~1,120 lines) — On-chain ModelPricingRegistry reader, model cache
- `constants.rs` (~455 lines) — Fee constants, model definitions, pricing parameters
- `delivery.rs` (~252 lines) — Phase 2 delivery fee calculation
- `gas.rs` (~198 lines) — Gas calculation utilities for system transactions
- `wallet.rs` (~486 lines) — Wallet balance/escrow verification
- `scheduled.rs` (~373 lines) — Scheduled transaction fee handling
- `validators.rs` (~106 lines) — Fee validation logic
- `http.rs` (~44 lines)

**Representative commits:**
- `7a12cae98` feat(ritual-async-fees): create unified fee calculation crate
- `ac7ac299a` feat: integrate on-chain ModelPricingRegistry for dynamic LLM pricing
- `08de7bf9e` perf(async-fees): Add per-block model caching for LLM pricing
- `cf054db8d` fix: convert audio duration from ms to seconds in fee calculation
- `d7acc3260` fix: explicit DKMS pricing calibrated to HTTP-equivalent
- `8aa848f34` fix: remove fallback pricing patterns, add model-specific multimodal pricing
- `0192e13de` HTTP & LLM Pricing (#95)
- `dd457a6dd` feat: gas bifurcation for system transactions (#200)

---

### 4. Precompile Codecs

**Summary:** ABI encoding/decoding for all Ritual precompile call types. Each precompile has a unique address (0x0800-0x0820) and specific request/response formats. The codecs handle parsing precompile inputs from transactions for fee calculation, job tracking, and verification.

**New crate:** `crates/ritual-precompile-codecs/`
- `http_call.rs` (~548 lines) — HTTP call precompile (0x0800) codec
- `llm_call.rs` (~284 lines) — LLM call precompile codec
- `long_running.rs` (~1,135 lines) — Long-running HTTP call codec with Phase 2 support
- `agent_call.rs` (~364 lines) — Agent call (0x0808) codec
- `autonomous_agent.rs` (~1,000 lines) — Autonomous agent (0x0820) codec
- `cli_agent.rs` (~526 lines) — CLI agent (0x080C) codec
- `executor.rs` (~260 lines) — Executor request codec
- `dkms_key.rs` (~272 lines) — DKMS key management precompile codec
- `error.rs` (~22 lines)

**Supported precompile addresses:**
- `0x0800` — HTTP Call
- `0x0804` — ZK Precompile
- `0x0806` — ZK Two-Phase
- `0x0807` — FHE (CKKS)
- `0x0808` — Agent Call
- `0x080C` — CLI Agent
- `0x0810` — Long-Running HTTP Call
- `0x0818` — Image Call
- `0x0820` — Autonomous Agent
- `0x0830` — DKMS Key

**Representative commits:**
- `a5be13961` feat: agent-call (0x0808) + async verification fix (#179)
- `03acca5a9` feat(precompile): add Autonomous Agent (0x0820) two-phase precompile support
- `100404200` feat(cli-agent): add CLI Agent precompile (0x080C) support
- `8f8145958` Update Cargo.lock with revm-context dependency for async context integration
- `093c42cd9` Align HTTP codec with 1-based method enum (#135)
- `1dd16089d` feat(image-call): add 0x0818 support across reth crates
- `7a74a52e0` feat: ZK Two-Phase Delivery - Reth Integration (#181)

---

### 5. SPC Verification

**Summary:** System Precompile Call (SPC) verification ensures that async transactions include valid attestations from registered TEE executors. This involves verifying ECDSA signatures, checking executor registration on-chain, validating TEE attestation data, and matching precompile call parameters. Used both at block build time and during block verification.

**New crates:**
- `crates/ritual-spc-verification/` — Full SPC verification service
  - `verifier.rs` (~913 lines) — Core verification logic
  - `types.rs` (~380 lines) — Type definitions
  - `client.rs` (~180 lines) — Client interface
  - `error.rs` (~64 lines)
  - `README.md` (~177 lines)
- `crates/ritual-spc-signature/` — Shared ECDSA signature verification
  - `lib.rs` (~694 lines) — Signature recovery, verification utilities
- `crates/ethereum/node/src/spc.rs` (+175) — SPC verification service integration into node

**Representative commits:**
- `19bd287f1` feat: implement contract-based SPC verification for async original transactions
- `7a8f86307` feat(block-verification): implement contract-based SPC verification
- `26f42c211` feat: create ritual-spc-signature crate for shared signature verification
- `5e1d2ab08` test: add coverage for build-time SPC verification
- `9186e9c17` fix: batch SPC verification reads and document error param convention
- `8ba7c3628` fix: harden Phase 2 delivery SPC verification and async pool context

---

### 6. Block Verification / Validity Constraints

**Summary:** Comprehensive block verification that enforces Ritual-specific consensus rules. Validators verify blocks against constraints including: nonce-lock verification, async commitment/settlement validation, scheduled transaction inclusion rules, fee correctness, predicate evaluation, heartbeat constraints (CH2-CH9), and censorship detection. This is the consensus-critical layer ensuring all validators agree on block validity.

**New crate:** `crates/ritual-block-verification/`
- `verifier.rs` (~5,262 lines) — The main block verifier, implementing all validity constraints
- `nonce_lock.rs` (~422 lines) — Nonce-lock validity constraint verification
- `constants.rs` (~58 lines) — Verification constants
- `error.rs` (~167 lines) — Verification error types

**Key modified files:**
- `crates/engine/tree/src/tree/mod.rs` (+214) — Integration of block verification into the engine tree
- `crates/consensus/common/src/validation.rs` (+78) — Additional consensus validation rules
- `crates/ethereum/consensus/src/lib.rs` (+53) — Ritual consensus extensions

**Representative commits:**
- `5187fbee8` feat(censorship): add scheduled transaction censorship detection to block verification
- `4bbafcde2` feat: implement C11 predicate verification in block builder and verifier
- `396438683` feat(verifier): enforce CH2-CH9 heartbeat validity constraints
- `524c5ba18` feat: implement nonce-lock validity constraint verification
- `482d30c98` feat(block-verification): Add nonce-lock validity constraint
- `ee147f001` feat(block-verification): add intra-block duplicate commitment sender check
- `5722ce397` feat: implement all 5 settlement verification constraints
- `adec5e166` feat: implement contract-based async settlement verification
- `91dcf6d0a` fix(builder): verify Phase 1 settled on-chain before Phase 2 delivery
- `8047c442a2` Fix: Use Verification mode for ALL transactions during block verification

---

### 7. Scheduled Transactions

**Summary:** Implements a scheduled transaction system where transactions can be registered on-chain (via a Scheduler contract) to execute at specific block intervals or frequencies. Includes a scheduling service, consensus verification of scheduled inclusion, temporal divergence eviction, and block building integration.

**New crates:**
- `crates/scheduling/` — Core scheduling engine
  - `contract.rs` (~1,029 lines) — On-chain Scheduler contract interaction
  - `types.rs` (~519 lines) — Scheduling type definitions
  - `canonical.rs` (~279 lines) — Canonical state tracking
  - `singleton.rs` (~234 lines) — Singleton scheduler instance
  - `transaction.rs` (~151 lines) — Scheduled transaction handling
  - `service.rs` (~58 lines) — Scheduling service
  - `events.rs` (~24 lines)
- `crates/ritual-scheduled-block-building/` — Block building for scheduled TXs
  - `lib.rs` (~599 lines) — Scheduled TX collection and inclusion logic
- `crates/ritual-scheduled-verification/` — Consensus verification
  - `lib.rs` (~2,985 lines) — Scheduled TX verification (C1-C10 constraints)
  - `predicate.rs` (~235 lines) — Predicate evaluation (C11)
  - `slots.rs` (~228 lines) — Storage slot reading for on-chain state
  - `error.rs` (~158 lines)

**Key modified files:**
- `crates/transaction-pool/src/pool/scheduled.rs` (+154) — Scheduled subpool
- `crates/transaction-pool/src/pool/txpool.rs` (+411) — Pool integration

**Representative commits:**
- `dd5202f34` feat(scheduled-verification): implement consensus-critical scheduled TX validation (C1-C10)
- `59666581b` feat: implement scheduled tx verification
- `9e0865644` feat: implement contract-state augmentation for scheduled TX block building
- `695f6fd44` feat(payload): Implement temporal divergence eviction for scheduled transactions
- `442733e08` feat(scheduling): Add evict_call API for temporal divergence handling
- `ab5b9d248` feat(scheduling): implement production ABI decoding with real event topic hashes
- `c9aff6635` feat: implement lock-free FrequencyIndex for optimized scheduling
- `d554bed92` fix: correct execution index validation timing in scheduled transaction consensus
- `5187fbee8` feat(censorship): add scheduled transaction censorship detection to block verification

---

### 8. Sequencing Rights

**Summary:** Implements a stake-weighted sequencing rights system. Validators are classified into priority tiers based on their stake, and block building rights are assigned via a deterministic bucket-based algorithm. This ensures fair block production proportional to stake.

**New crate:** `crates/ritual-sequencing-rights/`
- `classifier.rs` (~714 lines) — Validator tier classification based on stake
- `bucket.rs` (~604 lines) — Bucket-based sequencing right allocation
- `priority.rs` (~287 lines) — Priority tier definitions
- `reader.rs` (~358 lines) — On-chain stake/validator state reader
- `types.rs` (~293 lines) — Type definitions
- `lib.rs` (~241 lines) — Public API
- `error.rs` (~39 lines)

**Representative commits:**
- Various commits related to sequencing rights and validator stake (merged via feature branches)

---

### 9. Heartbeat Tracker

**Summary:** Event-driven heartbeat monitoring for system health. Tracks validator heartbeat transactions, monitors revival events, and enforces cooldown periods. Integrated into block verification (CH2-CH9 constraints).

**New crate:** `crates/ritual-heartbeat-tracker/`
- `lib.rs` (~424 lines) — Heartbeat tracker with event processing, cooldown management, mutex recovery
- `events.rs` (~38 lines) — Event type definitions

**Representative commits:**
- `64b678137` feat(heartbeat): add event-driven heartbeat tracker and system tx pipeline
- `396438683` feat(verifier): enforce CH2-CH9 heartbeat validity constraints
- `e9bda6e52` fix(heartbeat): cleanup dead const, compute selectors from ABI, warn on unknown state, add tracker unit tests
- `dff99f96e` fix(heartbeat): recover from mutex poisoning instead of crashing
- `bb8efe731` refactor(heartbeat): extract shared is_heartbeat_tx() helper

---

### 10. TEE Registry Reader

**Summary:** Reads executor registration and capability data from the on-chain `TEEServiceRegistry` contract. Used by SPC verification, fee calculation, and RPC validation to check if an executor is registered and what capabilities (HTTP, LLM, FHE, etc.) it supports.

**New crate:** `crates/ritual-tee-registry-reader/`
- `reader.rs` (~473 lines) — On-chain state reader for TEE registry
- `types.rs` (~109 lines) — Executor capability types
- `storage_layout.rs` (~61 lines) — Storage slot layout
- `constants.rs` (~27 lines)
- `error.rs` (~22 lines)

**Representative commits:**
- `c007d9554` feat(registry): migrate to unified TEEServiceRegistry contract (#170)
- `c0c781360` feat(fhe): add FHE capability to TEE registry reader
- `e4609dc21` feat(rpc): Add executor registration and capability validation at RPC level

---

### 11. Payload Builder Modifications

**Summary:** Extensive modifications to the Ethereum payload builder to support Ritual's async execution, scheduled transactions, SPC injection, gas bifurcation, predicate enforcement, block size limits, and unified execution modes. New modules handle bundle construction, transaction collection from multiple sources, and unified build/verify execution paths.

**Key files:**
- `crates/ethereum/payload/src/lib.rs` (+3,704 lines) — Massively extended payload builder with async TX processing, scheduled TX inclusion, SPC injection, fee validation, gas accounting
- `crates/ethereum/payload/src/unified_builder.rs` (+335) — Unified builder abstraction
- `crates/ethereum/payload/src/unified_execution.rs` (+511) — Unified execution pipeline
- `crates/ethereum/payload/src/execution.rs` (+305) — Execution context
- `crates/ethereum/payload/src/bundle.rs` (+194) — Bundle handling
- `crates/ethereum/payload/src/collector.rs` (+124) — Transaction collection
- `crates/ethereum/payload/src/config.rs` (+14) — Config extensions
- `crates/ethereum/evm/src/build.rs` (+19) — Build-time hooks
- `crates/ethereum/evm/src/execute.rs` (+134) — Execution hooks

**Representative commits:**
- `f88acb62e` fix: execute non-async augmented TXs after unified collection
- `72d3c12a3` refactor: unify pool + augmented scheduled TX sources in async detection
- `9e0865644` feat: implement contract-state augmentation for scheduled TX block building
- `d69b24a72` feat: implement byte-based block size limit with log estimation
- `be5f72095` fix: use u64::MAX gas limit for system transactions and update block gas accounting
- `f5cb32591` feat(payload): Handle OnnxModelNotCached in payload builder (#180)
- `a65d397fe` feat(predicate): enforce gas limit at EVM level, remove post-execution checks
- `c706d7308` fix: include extra_data in payload ID hash
- `91dcf6d0a` fix(builder): verify Phase 1 settled on-chain before Phase 2 delivery

---

### 12. Transaction Pool Extensions

**Summary:** The transaction pool is heavily extended with:
- **AsyncExecPool** — A new subpool (`async_pool.rs`, ~1,477 lines) for tracking in-flight async transactions through their lifecycle (pending → committed → fulfilled → settled)
- **ScheduledPool** — A subpool for scheduled transactions (`scheduled.rs`, ~154 lines)
- **Blocking handlers** — Synchronous state update handlers (`blocking_handlers.rs`, ~231 lines)
- **Extended traits** — `TransactionPool` trait extended with async result submission, scheduled TX management, and dual-path timeout eviction
- **Validation extensions** — Legacy transaction rejection, async/scheduled TX validation

**Key files:**
- `crates/transaction-pool/src/pool/async_pool.rs` (+1,477) — Full async pool implementation
- `crates/transaction-pool/src/pool/async_pool_removal_tests.rs` (+453) — Tests
- `crates/transaction-pool/src/pool/mod.rs` (+931) — Pool integration
- `crates/transaction-pool/src/pool/txpool.rs` (+411) — Inner pool changes
- `crates/transaction-pool/src/traits.rs` (+292) — Extended trait definitions
- `crates/transaction-pool/src/lib.rs` (+211) — Public API
- `crates/transaction-pool/src/validate/eth.rs` (+148) — Validation rules
- `crates/transaction-pool/src/maintain.rs` (+146) — Maintenance/eviction
- `crates/transaction-pool/src/blocking_handlers.rs` (+231) — Blocking state handlers
- `crates/transaction-pool/src/pool/scheduled.rs` (+154) — Scheduled pool

**Representative commits:**
- `b27be5b92` fix: skip by_id map for scheduled transactions in async pool (#177)
- `529d6a70d` feat(txpool): Add dual-path timeout eviction for async and scheduled transactions
- `86b01148a` Reject legacy transactions in transaction pool validation (#123)
- `762590eac` perf: parallelize pool insertion and state validation in send_raw_transaction
- `09942d53e` feat: Long-Running HTTP Calls Phase 2 - Async Pool Cleanup (#156)
- `801d3b97d` feat: filter async transactions to only include fulfilled ones during block building

---

### 13. RPC Extensions

**Summary:** New Ritual-specific RPC namespace (`ritual_*`) and extensions to existing namespaces for async transaction management, executor validation, and scheduled transaction queries.

**Key files:**
- `crates/rpc/rpc/src/ritual.rs` (+921) — Full Ritual RPC implementation: async result submission, job queries, executor status
- `crates/rpc/rpc-api/src/ritual.rs` (+227) — Ritual RPC trait definition
- `crates/rpc/rpc/src/async_tx_validator.rs` (+606) — RPC-level async transaction validation
- `crates/rpc/rpc-eth-types/src/receipt.rs` (+134) — Extended receipt types with SPC data
- `crates/rpc/rpc/src/eth/helpers/transaction.rs` (+281) — Custom `send_raw_transaction` with async detection
- `crates/rpc/rpc/src/txpool.rs` (+245) — Extended txpool RPC with async/scheduled info
- `crates/rpc/rpc-api/src/txpool.rs` (+17) — Extended txpool trait

**Representative commits:**
- `a24b0ca99` Implement RPC handler for async transaction result submission
- `1ed3f777c` feat: extend TransactionPool trait with async result submission methods
- `8f0b2bcdb` feat(rpc): Add RPC-level async transaction validation
- `e4609dc21` feat(rpc): Add executor registration and capability validation at RPC level
- `d710dd149` feat(rpc): Add LLMCallRequest codec and validation for model/messages fields
- `d1d49982e` fix(rpc): retry async pool lookup to handle finalization race
- `d7a5578ae` Phase 6: Register Ritual RPC endpoint in EthereumAddOns

---

### 14. Metrics & Instrumentation

**Summary:** Custom metrics crate and extensive instrumentation throughout the codebase for monitoring block building, transaction processing, async execution, and scheduling performance.

**New crate:** `crates/ritual-metrics/`
- `block.rs` (~217 lines) — Block lifecycle metrics (build time, verify time, block_time)
- `tx.rs` (~601 lines) — Transaction-level metrics (gas, execution time, from/to, type)
- `scheduling.rs` (~121 lines) — Scheduling metrics
- `lib.rs` (~20 lines)

**Key modified files:**
- `crates/tracing/src/ritual_router.rs` (+147) — Custom tracing router for Ritual-specific log routing
- `crates/tracing/src/lib.rs` (+31) — Tracing extensions
- `crates/net/network/src/metrics.rs` (+36) — Network metrics extensions

**Representative commits:**
- `d1ed036d8` feat: add block_time to block lifecycle metrics (#257)
- `dbb900779` feat: additional instrumentation
- `e7908e963` feat: instrumentation (#6)
- Various instrumentation commits throughout the history

---

### 15. Chainspec & Consensus Modifications

**Summary:** Extensions to the chain specification for Ritual-specific parameters including system contract addresses, precompile configurations, block rewards, fee configurations, and validator settings.

**Key files:**
- `crates/chainspec/src/spec.rs` (+265) — Ritual chain parameters, system contract addresses, genesis configuration
- `crates/chainspec/src/api.rs` (+8) — API extensions
- `crates/chainspec/src/constants.rs` (+8) — New constants
- `crates/consensus/common/src/validation.rs` (+78) — Validation rule extensions
- `crates/ethereum/consensus/src/lib.rs` (+53) — Consensus rule extensions
- `crates/ethereum/consensus/src/validation.rs` (+12)

**Representative commits:**
- `f5e0ede38` fix: correct ModelRegistry address to match genesis
- `3d4a97387` fix: update contract addresses after secure deployer migration (#136)
- `13f17a856` fix: update TEEServiceRegistry storage slot constants for OwnableUpgradeable migration

---

### 16. Storage Codec Extensions

**Summary:** Extensions to reth's compact storage codecs to support serialization/deserialization of all custom transaction types and new data structures (passkey signatures, SPC calls, etc.).

**Key files (all under `crates/storage/codecs/src/alloy/transaction/`):**
- `async_commitment.rs` (+82) — AsyncCommitment codec
- `async_settlement.rs` (+101) — AsyncSettlement codec
- `scheduled.rs` (+96) — Scheduled TX codec
- `spc_call.rs` (+349) — SPC call codec
- `passkey.rs` (+80) — Passkey TX codec
- `txtype.rs` (+35) — Extended TxType enum
- `ethereum.rs` (+179) — Updated EthTxEnvelope codec
- `legacy.rs` (+24) — Legacy TX updates
- `eip1559.rs` (+45) — EIP-1559 extensions
- `crates/storage/codecs/src/alloy/passkey_signature.rs` (+148)

---

### 17. Engine Tree / Cached State

**Summary:** Modifications to the engine tree for Ritual block verification integration and extended cached state management for async/scheduled execution.

**Key files:**
- `crates/engine/tree/src/tree/mod.rs` (+214) — Block verification hooks, async pool state updates on canonical chain advances
- `crates/engine/tree/src/tree/cached_state.rs` (+243) — Extended cached state for async execution context
- `crates/chain-state/src/in_memory.rs` (+26) — In-memory state extensions
- `crates/chain-state/src/notifications.rs` (+19) — Notification system extensions

---

### 18. Networking / P2P Changes

**Summary:** Minor modifications to the networking layer, mostly for improved error handling, metrics, and compatibility with custom transaction types. The bulk of the changes in `crates/net/` are relatively small per-file modifications.

**Notable changes:**
- `crates/net/network/src/error.rs` (+124) — Enhanced error types
- `crates/net/network/src/transactions/mod.rs` (+103) — Transaction propagation updates
- `crates/net/network/src/peers.rs` (+72) — Peer management updates
- `crates/net/network/src/metrics.rs` (+36) — Network metrics

---

### 19. Blocking PubSub

**Summary:** A blocking publish-subscribe mechanism for synchronous event notification across components.

**New crate:** `crates/ritual-blocking-pubsub/`
- `lib.rs` (~38 lines) — Simple blocking pub/sub implementation

**Representative commits:**
- `64773e5b4` feat: blocking pubsub type shii

---

### 20. CI / Tooling / Documentation

**Summary:** AI-assisted PR review infrastructure, code hygiene detection, and design documentation.

**Key files:**
- `.github/workflows/claude-pr-review.yml` (+60) — Claude AI PR review
- `.github/workflows/devin-pr-review.yml` (+103) — Devin AI PR review
- `.github/workflows/manus-pr-review.yml` (+116) — Manus AI PR review
- `.ritual-pr/` — PR review configuration and prompts
  - `config.yml` (+29)
  - `prompts/shared/consensus-code-audit.md` (+184)
  - `prompts/shared/engineering.md` (+99)
  - `prompts/shared/fsm-verification.md` (+38)
- `docs/design/model-pricing-registry.md` (+112) — Design doc for model pricing
- `scripts/multi_tx_analysis.py` (+166) — Transaction analysis script

---

## Architecture Diagram (Textual)

```
User TX → [RPC: send_raw_transaction]
              ↓
         [Async TX Validator] ← ritual-precompile-codecs
              ↓                  ritual-tee-registry-reader
         [Transaction Pool]
           ├── PendingPool (standard EIP txs)
           ├── AsyncExecPool (async commitments/settlements)
           └── ScheduledPool (scheduled txs)
              ↓
         [Payload Builder]
           ├── Standard TXs
           ├── Scheduled TX Augmentation ← ritual-scheduled-block-building
           ├── Async Commitment Detection ← ritual-async, ritual-async-inspector
           ├── Async Settlement Injection
           ├── SPC Call Injection ← ritual-spc-verification
           ├── Fee Validation ← ritual-async-fees
           ├── Predicate Evaluation
           └── Gas Bifurcation (user vs system)
              ↓
         [Block Verification] ← ritual-block-verification
           ├── Nonce-lock constraints
           ├── Async commitment validation ← ritual-async-commitment-validator
           ├── Settlement verification ← ritual-async-registry
           ├── Scheduled TX validation (C1-C10) ← ritual-scheduled-verification
           ├── Heartbeat constraints (CH2-CH9) ← ritual-heartbeat-tracker
           ├── Fee correctness
           ├── Predicate verification (C11)
           └── Censorship detection
              ↓
         [Engine Tree] → Canonical chain advance → AsyncPool state updates
```

---

## Key Observations

1. **Scale of changes:** 63,500+ lines added across 573 files — this is a substantial fork, not a light patch.

2. **Consensus-critical surface area:** The block verification crate alone is 5,262 lines. Combined with scheduled verification (2,985 lines) and async commitment validation (589 lines), there is approximately 8,800+ lines of consensus-critical code that all validators must agree on.

3. **Two-phase async execution is the centerpiece:** The entire fork revolves around enabling async precompile calls (HTTP, LLM, ONNX, FHE, ZK, agents) with a commit-then-settle execution model. This touches nearly every layer of the stack.

4. **On-chain state dependency:** Many verification steps read from on-chain contracts (TEEServiceRegistry, ModelPricingRegistry, Scheduler, AsyncJobTracker). This creates tight coupling between contract state and consensus rules.

5. **Rapid iteration evidence:** Many commits show WIP patterns ("fix: the fuck", "ff", "wip", "shiii") indicating rapid development with later cleanup, which is expected for an internal fork.

6. **16 new crates:** The fork adds 16 entirely new crates to the workspace, all under the `ritual-*` or `scheduling` namespace.
