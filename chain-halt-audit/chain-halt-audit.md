# Ritual Chain Halt Audit Plan

**Goal:** Systematically identify and test vectors that could cause the Ritual blockchain to halt, crash, or degrade to the point of unusability.

**Repos in scope:**
- `ritual-reth-internal` — Execution client (Reth fork)
- `ritual-summit-internal` — Consensus client (Simplex protocol)
- `ritual-sc-internal` — System smart contracts

---

## 1. Panic & Crash Path Analysis

### 1A. ritual-reth: Panic/Unwrap Audit

**Status:** 0 `panic!` in production code. 119 `unwrap()` calls across 15 Ritual-specific crates.

**High-priority crates to investigate** (by unwrap density in production code):

| Crate | unwrap() count | Key risk area |
|-------|---------------|---------------|
| `ritual-async-fees` | 26 | Registry lookups, fee calculations |
| `ritual-spc-verification` | 21 | `RwLock` read/write, proof verification |
| `ritual-async-registry` | 20 | AsyncJobTracker state reads |
| `ritual-precompile-codecs` | 19 | ABI decoding of precompile inputs |
| `ritual-scheduled-verification` | 15 | Scheduler contract state reads |
| `ritual-spc-signature` | 11 | Signature verification |
| `ritual-sequencing-rights` | 10 | Transaction ordering |

**Investigation tasks:**

- [ ] **Task 1A-1:** For each `unwrap()` in production code in `ritual-spc-verification/src/verifier.rs`, trace the call path — can a malicious transaction supply input that causes the `RwLock` to be poisoned or the unwrap to fail?
- [ ] **Task 1A-2:** In `ritual-precompile-codecs`, audit every `unwrap()` on ABI decode paths. Can a transaction with malformed precompile calldata (HTTP call 0x0801, LLM call 0x0802, agent call, etc.) cause a panic?
- [ ] **Task 1A-3:** In `ritual-async-fees/src/registry.rs`, trace the unwrap paths for fee lookups. What happens if a fee registry entry is missing or corrupted in storage?
- [ ] **Task 1A-4:** In `ritual-async-registry`, what happens if the `AsyncJobTracker` contract storage is in an unexpected state (e.g., slot values are zero, or indices are out of bounds)?
- [ ] **Task 1A-5:** In `ritual-scheduled-verification`, what happens if the `Scheduler` contract storage returns unexpected values for validity constraints C1-C10?

### 1B. ritual-summit: Panic/Unwrap Audit

**Status:** 66 `panic!` and 321 `unwrap()` and 301 `expect()` in production code. **This is the higher-risk target.**

**High-priority files to investigate:**

| File | panic! | unwrap() | expect() | Risk area |
|------|--------|----------|----------|-----------|
| `node/src/args.rs` | 20 | — | — | CLI arg parsing, checkpoint lookup |
| `types/src/consensus_state.rs` | 29 | — | — | Enum variant mismatches in consensus |
| `syncer/src/actor.rs` | 9 | — | — | Block retrieval, chain gap handling |
| `finalizer/src/actor.rs` | 8 | — | — | Message handling variant mismatches |
| `types/src/engine_client.rs` | — | 103 | 48 | Engine API reconnection, block lookups |
| `node/src/engine.rs` | — | 97 | 151 | Engine client interactions |

**Investigation tasks:**

- [ ] **Task 1B-1:** Audit `syncer/src/actor.rs` — the panics on "failed to get block" and "gapped block missing" are reachable in production. Can a malicious validator craft a block proposal that triggers chain gaps? Can network partitions cause this?
- [ ] **Task 1B-2:** Audit `finalizer/src/actor.rs` — the 8 panics on "wrong response variant" suggest the finalizer assumes specific message types. Can a malicious peer send unexpected message variants?
- [ ] **Task 1B-3:** Audit `types/src/consensus_state.rs` — the 29 panics on enum variant mismatches (e.g., "Expected MinimumStake variant"). Can corrupted or adversarial consensus state updates trigger these?
- [ ] **Task 1B-4:** Audit `types/src/engine_client.rs` and `node/src/engine.rs` — the engine client has 250+ unwrap/expect calls. If the execution client (reth) returns unexpected responses, drops connection, or responds slowly, which of these paths panic?
- [ ] **Task 1B-5:** Audit `node/src/args.rs` — can node restart with corrupted checkpoint data trigger the 20 panic paths?

---

## 2. Recent Commit History — Feature-Focused Audit

Recent commits (Feb 10-24, 2026) reveal actively-changed features that are most likely to contain bugs.

### 2A. ritual-reth Recent Changes

| Feature Area | Commits | Risk Level | Rationale |
|-------------|---------|------------|-----------|
| SPC Verification & Phase 2 Delivery | 8 | **HIGH** | Core verification logic, actively hardened — may still have edge cases |
| Async Job Management & Validation | 6 | **HIGH** | Recent fixes for "silent fallback" bugs suggest fragile error handling |
| Fee Calculation (ZK two-phase, FHE) | 3 | **MEDIUM** | Missing fee paths recently added — are there more missing? |
| TTL Increase (60 → 500 blocks) | 1 | **MEDIUM** | 8x increase in max TTL — does this create new resource exhaustion vectors? |
| TEEServiceRegistry Upgrade | 1 | **MEDIUM** | Storage slot changes — could old/new slot mismatch cause reads to fail? |

**Investigation tasks:**

- [ ] **Task 2A-1:** Audit the SPC verification changes. Focus on `ritual-spc-verification/src/verifier.rs` — the recent "harden" commits suggest there were verification bypasses. Are there remaining edge cases where an invalid SPC proof is accepted or a valid one is rejected (causing a halt on verification mismatch)?
- [ ] **Task 2A-2:** Audit the async job lifecycle. The commit "replace silent fallback with explicit failure" changed error handling. Trace the call paths — does an explicit failure now cause a panic or block rejection where it previously would have silently continued?
- [ ] **Task 2A-3:** Audit the TTL increase. With `DEFAULT_MAX_TTL_BLOCKS = 500`, can an attacker submit async jobs that persist for 500 blocks, accumulating until they exhaust memory or storage?
- [ ] **Task 2A-4:** Audit the TEEServiceRegistry storage slot migration. If a node has stale state from before the `OwnableUpgradeable` migration, do the new slot constants cause incorrect reads?

### 2B. ritual-summit Recent Changes

| Feature Area | Commits | Risk Level | Rationale |
|-------------|---------|------------|-----------|
| Syncer/Marshal improvements | 6 | **HIGH** | Block delivery ordering — bugs here can halt consensus |
| Error handling & panic reduction | 3 | **HIGH** | Recent changes to return Invalid instead of panicking — are all paths covered? |
| Helios integration | 3 | **MEDIUM** | Validator set extraction — bugs could cause consensus mismatches |
| Validator stake management | 2 | **HIGH** | Using balance as single source of truth — what if balance is manipulated? |

**Investigation tasks:**

- [ ] **Task 2B-1:** Audit the syncer/marshal changes for pending notarized block handling. Can blocks arrive out of order in a way that causes the syncer to deadlock or panic?
- [ ] **Task 2B-2:** Audit the "Return PayloadStatus::Invalid instead of panicking" change. Map all remaining paths where the EL returns an error — are there any that still panic?
- [ ] **Task 2B-3:** Audit the validator stake changes. If "balance as single source of truth" is used, can an attacker manipulate their balance (e.g., via a reorg or a specific transaction pattern) to gain or lose validator status mid-epoch?
- [ ] **Task 2B-4:** Audit the Helios integration functions `get_active_validators_with_stakes` and `build_participant_bimap`. If these return inconsistent data (e.g., duplicate keys, zero stakes), does the consensus layer handle it gracefully?

---

## 3. VM Crash Vectors

General categories of how the execution VM (reth) can crash or halt.

### 3A. Memory Exhaustion

- [ ] **Task 3A-1:** Can a single transaction cause unbounded memory allocation in the EVM? Investigate:
  - Precompile calls with very large input data (especially ritual precompiles: HTTP 0x0801, LLM 0x0802, ONNX, etc.)
  - Memory expansion in EVM with `MSTORE` at very high offsets
  - Large return data from precompile calls
- [ ] **Task 3A-2:** Can the transaction pool grow unbounded? Investigate:
  - Are there limits on pending async transactions?
  - What happens when `MAX_PENDING_JOBS = 10,000` jobs all have pending settlement transactions?
  - Does the async transaction pool have separate memory limits?
- [ ] **Task 3A-3:** Can block building exhaust memory? Investigate:
  - If a block contains many async settlement transactions, does the block builder hold all intermediate states in memory?
  - What's the memory profile of SPC verification (parallel proof verification with caching)?

### 3B. CPU Exhaustion / Infinite Loops

- [ ] **Task 3B-1:** Can SPC proof verification be made arbitrarily expensive? Investigate:
  - Is there a timeout on TDX/ECDSA attestation verification?
  - Can a crafted proof cause the verifier to loop or take excessive time?
- [ ] **Task 3B-2:** Can the sequencing rights system (`ritual-sequencing-rights`) cause infinite reordering loops?
- [ ] **Task 3B-3:** Can the scheduled transaction verification (C1-C10 constraints) be made to take unbounded time by crafting specific scheduler state?

### 3C. Disk Exhaustion

- [ ] **Task 3C-1:** Investigate state growth rate under adversarial conditions:
  - What's the maximum state growth per block?
  - Can the `AsyncJobTracker` create 10,000 jobs × large calldata, then repeat every 500 blocks (new TTL)?
- [ ] **Task 3C-2:** Investigate log/event spam:
  - Can transactions generate excessive logs that bloat the node's database?
  - Are there limits on event emission per transaction?

### 3D. Network-Level Crashes

- [ ] **Task 3D-1:** What happens to the summit consensus client if the execution client (reth) becomes unresponsive?
  - Does the engine client have timeouts?
  - Do the 250+ unwrap/expect calls in engine_client.rs / engine.rs panic if the connection drops mid-call?
- [ ] **Task 3D-2:** Can a malicious validator send oversized or malformed consensus messages that crash other validators?
- [ ] **Task 3D-3:** What happens during a network partition where validators see different execution states?

### 3E. Consensus-Execution Mismatch

- [ ] **Task 3E-1:** Can a determinism violation cause a chain split?
  - The `ritual-block-verification` crate has determinism checks. What happens if two nodes produce different EVM results for the same block?
  - Are the ritual precompiles (HTTP, LLM, ONNX) fully deterministic? If not, how is non-determinism handled?
- [ ] **Task 3E-2:** Can the async commitment validator produce different results during block building vs. block verification, causing nodes to disagree?

---

## 4. Smart Contract Attack Vectors

### 4A. Unbounded Storage Growth ("Memory Leaks")

| Contract | Data Structure | Cap | Risk |
|----------|---------------|-----|------|
| `ModelPricingRegistry` | `modelNames[]` | **None** | **CRITICAL** |
| `ModelPricingRegistry` | `modelWorkloads[model][]` | **None** | **CRITICAL** |
| `ModelPricingRegistry` | `workloadModels[workload][]` | **None** | **CRITICAL** |
| `TEECapabilityPolicy` | `capabilityToWorkloads[cap].workloadIds[]` | **None** | **HIGH** |
| `AsyncJobTracker` | `executorJobs[executor][]` | 10,000 total | MEDIUM |
| `AsyncJobTracker` | `senderJobs[sender][]` | 10,000 total | MEDIUM |
| `AsyncJobTracker` | `expiryBuckets[block][]` | 10,000 total | MEDIUM |
| `Scheduler` | `slots[]` | Cleanup threshold 1000 | MEDIUM |
| `TEEServiceRegistry` | `serviceAddresses[]` | 10,000 | LOW |

**Investigation tasks:**

- [ ] **Task 4A-1:** `ModelPricingRegistry` — Determine who can call `addModel()` and `addWorkloadModel()`. If these are governance-gated, the risk is lower. If any executor can add models, quantify how many models/workloads an attacker can add and what the gas cost of `getAllModels()` and `getAllModelWorkloads()` becomes.
- [ ] **Task 4A-2:** `TEECapabilityPolicy` — Same analysis. Who can bind workloads to capabilities? Can an attacker create thousands of workload-capability bindings?
- [ ] **Task 4A-3:** `AsyncJobTracker` — With the 10,000 cap, can an attacker fill all 10,000 slots with cheap jobs to prevent legitimate users from submitting jobs? What's the minimum cost to fill the tracker?
- [ ] **Task 4A-4:** `Scheduler` — With `MAX_CLEANUP_PER_EXECUTE = 25` and `CLEANUP_THRESHOLD = 1000`, can the slots array grow faster than cleanup can prune it? Is there a steady-state where slots accumulate indefinitely?

### 4B. Contract Lock-Up / DoS

- [ ] **Task 4B-1:** `AsyncDelivery.deliver()` — The delivery function makes an external call to the user's target contract. Can a malicious target contract:
  - Consume all forwarded gas, causing the delivery to fail?
  - Reenter and corrupt state?
  - Return data so large it causes an out-of-gas on the caller side?
- [ ] **Task 4B-2:** `RitualWallet` — Can a user lock funds with `_lockUntil` set to `type(uint256).max`, permanently locking their funds? Does this affect any system invariants?
- [ ] **Task 4B-3:** `Scheduler._wipeBytes()` — This iterates over calldata length in 32-byte words. Can a scheduled call with maximum calldata size (~10KB) cause gas exhaustion during cleanup?
- [ ] **Task 4B-4:** `Staking` — Can a validator stake/unstake rapidly to disrupt the validator set? Are there cooldown periods?

### 4C. State Corruption

- [ ] **Task 4C-1:** `TEEServiceRegistry` — After the `OwnableUpgradeable` migration, are old storage slots properly cleared? Can residual data in old slots be misinterpreted?
- [ ] **Task 4C-2:** `AsyncJobTracker` — The expiry bucket system uses block numbers as keys. What happens at the boundary when `expiryBlock` overflows or when a chain reorg changes which block a job expires in?
- [ ] **Task 4C-3:** Are there any proxy/upgrade patterns in the system contracts? If so, is there a storage collision risk between implementation versions?

---

## 5. Cross-Component Interaction Vectors

These span multiple components and are often the most dangerous.

- [ ] **Task 5-1:** **Async Transaction Lifecycle:** Trace the full lifecycle of an async transaction from submission to settlement. Identify every handoff point between reth, summit, and the system contracts. Where can a failure at one stage cause inconsistency at another?
- [ ] **Task 5-2:** **Block Building vs. Verification Divergence:** If the block builder (reth) includes a transaction that the verifier (also reth, but different code path) rejects, what happens? Does the chain halt? Does the block get orphaned?
- [ ] **Task 5-3:** **Consensus-Execution Reconnection:** If the summit consensus client loses connection to reth and reconnects, does it correctly resync? The `expect("Failed to update fork choice after reconnect")` in `engine_client.rs` suggests this path can panic.
- [ ] **Task 5-4:** **Validator Set Transition:** When the validator set changes (stake/unstake), is there a window where summit and reth disagree on who the active validators are? Can this cause blocks to be rejected?

---

## 6. Documentation vs. Implementation Audit

Documentation often describes the intended behavior, constraints, and invariants that should hold. Mismatches between documentation and actual code can reveal:
- Unimplemented safety checks
- Violated invariants
- Outdated assumptions after refactoring
- Missing validation logic

**Investigation tasks:**

- [ ] **Task 6-1:** Locate and catalog all documentation files (README.md, docs/, DESIGN.md, ADRs, etc.) in `ritual-reth-internal`, `ritual-summit-internal`, and `ritual-sc-internal`.
- [ ] **Task 6-2:** Cross-reference async transaction documentation against implementation:
  - Do documented lifecycle phases (submission → validation → settlement) match the actual code paths in `ritual-async-registry` and `ritual-async-fees`?
  - Are documented constraints (TTL limits, max pending jobs, expiry logic) correctly enforced in code?
  - Are documented error conditions handled as specified?
- [ ] **Task 6-3:** Cross-reference SPC verification documentation against implementation:
  - Does the verification flow in `ritual-spc-verification` match the documented security model?
  - Are all documented proof checks (TDX attestation, ECDSA signatures, merkle proofs) actually performed?
  - Are documented failure modes (invalid proof, expired attestation) handled correctly?
- [ ] **Task 6-4:** Cross-reference consensus protocol documentation in `ritual-summit-internal`:
  - Does the syncer/marshal/finalizer flow match the documented consensus phases?
  - Are documented safety guarantees (e.g., "no block finalized without 2/3+ stake") enforced in code?
  - Are documented validator set transition rules correctly implemented?
- [ ] **Task 6-5:** Cross-reference smart contract documentation in `ritual-sc-internal`:
  - Do contract NatSpec comments describe constraints that aren't enforced (e.g., "should not exceed X" without a require)?
  - Are documented access controls (onlyOwner, role-based) consistently applied?
  - Do README or design docs describe limits that aren't present in the code (e.g., documented caps on array growth)?
- [ ] **Task 6-6:** Cross-reference precompile documentation:
  - Are the ritual precompiles (HTTP 0x0801, LLM 0x0802, ONNX, etc.) documented?
  - Do documented input validation rules match the actual `ritual-precompile-codecs` implementation?
  - Are documented gas cost models correctly applied?

---

## 7. P2P Bypass of RPC-Layer Async Payload Validation

### Finding

The RPC-layer validator (`validate_image_call_payload` / `validate_async_payload`) runs `ExecutorRequest::decode_base_fields` on raw calldata before it enters the mempool. This catches malformed payloads, `executor == address(0)`, `ttl == 0`, and `ttl > max_ttl` — but **only for transactions submitted via RPC**.

Transactions received via P2P gossip take a completely different path:

```
P2P gossip → import_transactions() → pool.add_external_transactions() → EthTransactionValidator
```

`EthTransactionValidator` checks chain ID, gas limits, nonce, balance, and signature — it does **not** inspect calldata or check whether `to` targets a precompile address. The `validate_async_payload` function is never called. This means a peer can gossip a transaction with `executor = address(0)`, `ttl = 0`, or `ttl = MAX_UINT` and it enters every peer's mempool without validation.

### Validation gap by transaction source

| Path | Async payload validation | Catches bad executor/TTL? |
|------|--------------------------|---------------------------|
| **RPC submission** | `validate_async_payload` → `validate_image_call_payload` | Yes |
| **P2P gossip** | None — only `EthTransactionValidator` (chain ID, gas, sig) | **No** |
| **Block proposal (commitment)** | `validate_commitment_structure` (TTL bounds) | Partially — checks TTL but not executor=zero at commitment level |
| **Detector/builder** | Depends on detector logic | Must independently reject |

### How to become a peer

Ritual's reth fork uses standard devp2p peering (discv4, discv5, DNS discovery). To peer, an attacker needs:
1. The genesis config and fork schedule (to pass ForkId validation during the devp2p handshake)
2. Network reachability to port 30303 on a validator node

There is a `trusted_nodes_only` flag in reth's peer config that, when set to `true`, restricts connections to whitelisted peer IDs only. However, **this flag is not set by chain-deployment-infra** — the reth pod template does not pass `--trusted-only` to reth. Notably, `TRUSTED_PEERS_ARG` is exported in `node_deployment.sh` but never referenced in `reth-pod.yaml.template`, so `--trusted-peers` is likely dead code as well.

### Current mitigation: GCP firewall lockdown

When `SKIP_FIREWALL_LOCKDOWN=false`, `firewall_lockdown.sh` replaces permissive GCP firewall rules (`0.0.0.0/0`) with IP-whitelisted rules. Port 30303 (P2P/discovery) is only allowed from:
- Validator IPs (validator-internal rule)
- Snapshot VM IPs (snapshot-to-el rule)

An arbitrary external attacker **cannot reach the P2P port at all** — the GCP firewall drops the packets before they ever hit reth. This makes the P2P bypass risk **low in the current testnet/devnet deployment** where Ritual controls the infrastructure.

### Risk on mainnet

On mainnet (or any deployment where Ritual does not control the network perimeter), this becomes a real concern:
- Port 30303 must be open for public peering — there is no GCP firewall to restrict it
- Anyone can become a peer by matching the ForkId
- `trusted_nodes_only` is not enabled at the reth level
- Once peered, an attacker can gossip transactions with invalid async payloads that bypass all RPC-layer checks and enter every node's mempool

The downstream risk depends on what happens when bad payloads reach the detector/builder:
- If any codepath does an `unwrap()` on a decode that assumes RPC validation already ran, it's a **crash vector** (ties into Task 1A-2)
- Even without crashes, mempool pollution with invalid async TXs wastes detector resources
- A commitment derived from a bad-TTL origin TX should be caught by `validate_commitment_structure`, but executor=zero may not be

### Recommended hardening (pre-mainnet)

- [ ] **Task 7-1:** Add async payload validation to the transaction pool validator (`EthTransactionValidator`) so it applies uniformly regardless of transaction source (RPC vs P2P)
- [ ] **Task 7-2:** Wire `TRUSTED_PEERS_ARG` into `reth-pod.yaml.template` (currently dead code) and evaluate enabling `--trusted-only` for production deployments
- [ ] **Task 7-3:** Audit the detector/builder code paths for `unwrap()` calls on decoded async payloads — these assume RPC validation already ran and would panic on malformed P2P-gossiped transactions
- [ ] **Task 7-4:** Verify that `validate_commitment_structure` catches all the same invalid states that `validate_async_payload` does (executor=zero, TTL=0, etc.) as a defense-in-depth layer

---

## Prioritized Investigation Order

### P0 — Highest Risk (Chain Halt)
1. **Task 1B-4** — Summit engine client panic paths (250+ unwrap/expect on EL communication)
2. **Task 1B-1** — Summit syncer panic on block gaps
3. **Task 3E-1** — Determinism violations causing chain split
4. **Task 5-2** — Build vs. verify divergence
5. **Task 5-3** — Consensus-execution reconnection panic

### P1 — High Risk (Chain Degradation)
6. **Task 7-1** — Add async payload validation to the pool validator (P2P bypass)
7. **Task 7-3** — Audit detector/builder unwrap paths that assume RPC validation
8. **Task 1A-2** — Reth precompile codec panic on malformed input
9. **Task 2A-2** — Async job lifecycle error handling changes
10. **Task 2B-1** — Syncer/marshal block ordering
11. **Task 3A-2** — Transaction pool memory exhaustion
12. **Task 4A-3** — AsyncJobTracker slot filling DoS

### P2 — Medium Risk (Performance / Economic)
13. **Task 7-2** — Wire trusted-peers into reth pod template (dead code)
14. **Task 7-4** — Verify commitment validation covers all RPC-checked states
15. **Task 4A-1** — ModelPricingRegistry unbounded growth
16. **Task 3A-1** — Single transaction memory exhaustion
17. **Task 2A-3** — TTL increase resource exhaustion
18. **Task 4A-4** — Scheduler cleanup race
19. **Task 3D-2** — Malicious consensus messages

### P3 — Lower Risk (Edge Cases)
20. **Task 4B-1** — AsyncDelivery.deliver() reentrancy
21. **Task 4C-1** — TEEServiceRegistry storage migration
22. **Task 1A-4** — AsyncJobTracker unexpected storage state
23. **Task 4B-4** — Validator stake/unstake churn
24. **Task 2A-4** — Storage slot migration stale state

---

## Appendix: Repository Locations

| Repo | Path | Type |
|------|------|------|
| ritual-reth | `/home/ritual/repos/ritual-reth-internal` | Rust (Reth fork) |
| ritual-summit | `/home/ritual/repos/ritual-summit-internal` | Rust (Consensus client) |
| ritual-sc | `/home/ritual/repos/ritual-sc-internal` | Solidity (Foundry) |
