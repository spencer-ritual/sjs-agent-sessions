# ritual-summit Panic Audit — High-Likelihood Chain-Halt Targets

> **Goal:** Identify all locations where `ritual-summit` can `panic!`, `unwrap()`, or `expect()` in production code, ranked by likelihood of being triggered and severity of impact (chain halt).
>
> **Codebase:** `ritual-summit-internal` @ `dev` branch, commit `4c72a03` (up to date with `origin/dev`)

---

## Recent Fixes Already on `dev`

Three recent commits (merged via PRs #45 and #48) partially address engine client panics:

| Commit | What it fixed | Audit finding |
|--------|--------------|---------------|
| `6ccbdca` | `check_payload()`: non-transport RPC errors now return `PayloadStatus::Invalid` instead of `panic!` | **C1 (partially)** — the `check_payload` non-transport path is fixed |
| `0d05a3f` | `start_building_block()`: non-transport errors now `return None` instead of `panic!`; `commit_hash()`: non-transport errors now `return` instead of `panic!`; added test for check_payload | **C1 (more)** — `start_building_block` and `commit_hash` non-transport paths fixed |
| `f837665` | Syncer: `try_complete_pending_notarized` optimization, pending_notarized pruning to fix unbounded memory growth | Not a panic fix, but prevents OOM (which could cascade) |

### What's still NOT fixed after these commits:

1. **`get_payload()` non-transport panic** (line 295) — still `panic!("Unable to get a response: {:?}", e)`. The only function not patched.
2. **All 4 post-reconnect `.expect()` calls** (lines 265, 291, 322, 354) — transport error → reconnect → retry-once → `.expect()`. If the retry also fails, node still crashes.
3. **All IPC connection `.unwrap()` calls** (lines 102, 122) — no retry at startup.
4. **Everything else in the audit** (syncer storage panics, finalizer panics, checkpoint panics, etc.) — untouched.

---

## Executive Summary

| Severity | Count | Description |
|----------|-------|-------------|
| **CRITICAL** | 18 | Can be triggered by external input, network conditions, or EL failures |
| **HIGH** | 22 | Can be triggered by state corruption, timing, or component failures |
| **MEDIUM** | 12 | Unlikely but possible under operational conditions |
| **LOW** | ~50 | Essentially unreachable (constants, test-only, debug-only) |

**The three dominant panic patterns:**

1. **Storage I/O failures → panic** — Every storage read/write error in the syncer and its cache layer is a hard crash. No graceful degradation.
2. **EL (reth) failures → panic** — The engine client retries once after a transport error, then `expect()`s the retry. Persistent EL issues crash the CL.
3. **Cross-component state assumptions → panic** — The finalizer, syncer, and orchestrator all `expect()` specific message variants and state invariants. Any desync between components cascades into a crash.

---

## Tier 1: CRITICAL — Likely Chain-Halt Targets

These are the highest-priority audit targets. Each can be triggered by conditions that occur in production (network issues, EL downtime, disk pressure, malformed external data).

---

### C1. Engine Client: `get_payload()` panic on non-transport error — STILL LIVE

**File:** `types/src/engine_client.rs:295`
**Function:** `RethEngineClient::get_payload()`

```rust
panic!("Unable to get a response: {:?}", e)
```

**Trigger:** Reth returns any non-transport error (payload not found, build timeout, internal error).

**Recent fix context:** Commits `6ccbdca` and `0d05a3f` fixed the sister functions `check_payload()` (returns `PayloadStatus::Invalid`), `start_building_block()` (returns `None`), and `commit_hash()` (returns early). But `get_payload()` was **never patched** — it's the only function in the engine client that still panics on non-transport errors.

**Impact:** Block proposer crashes. Called every time this node proposes a block.

**Exploitability:** Moderate. If reth is under load or the payload build times out, this fires.

---

### C2. Engine Client: Post-reconnect expects (4 instances) — STILL LIVE

**File:** `types/src/engine_client.rs`

| Line | Function | Message | Non-transport path |
|------|----------|---------|--------------------|
| 265 | `start_building_block()` | `"Failed to update fork choice after reconnect"` | FIXED (returns `None`) |
| 291 | `get_payload()` | `"Failed to get payload after reconnect"` | NOT FIXED (panics) |
| 322 | `check_payload()` | `"Failed to check payload after reconnect"` | FIXED (returns Invalid) |
| 354 | `commit_hash()` | `"Failed to get payload after reconnect"` | FIXED (returns early) |

**Trigger:** Transport error → reconnect succeeds → retry also fails. Pattern: detect IPC error → call `wait_until_reconnect_available()` → retry once → `.expect()`.

**What was fixed:** The non-transport (first-attempt) error paths for `start_building_block`, `check_payload`, and `commit_hash` now handle errors gracefully. But the **post-reconnect** `.expect()` on the retry attempt is still present on all 4 functions. If reconnect succeeds but the RPC call fails again, the node still crashes.

**Impact:** A reth crash-loop or IPC socket corruption crashes the CL node even after reconnect.

**Exploitability:** High. Reth restarts, OOM kills, or IPC file deletion are normal operational events.

---

### C3. Syncer: `find_block()` panic on storage read

**File:** `syncer/src/actor.rs:1191`
**Function:** `Actor::find_block()`

```rust
match self.finalized_blocks.get(ArchiveID::Key(&commitment)).await {
    Ok(block) => block,
    Err(e) => panic!("failed to get block: {e}"),
}
```

**Trigger:** Any storage read error on the finalized blocks archive.

**Impact:** This is the most-called panic point in the syncer. External messages (notarizations, finalizations, block requests, subscriptions) all route through `find_block()`. A single I/O error crashes the node.

**Exploitability:** Disk full, I/O timeout, or storage corruption triggers this in the hot loop.

---

### C4. Syncer: `store_finalization()` panic on storage write

**File:** `syncer/src/actor.rs:1135`
**Function:** `Actor::store_finalization()`

```rust
if let Err(e) = try_join!(
    async { self.finalized_blocks.put(block).await.map_err(Box::new)?; Ok::<_, BoxedError>(()) },
    async { /* finalizations write */ Ok::<_, BoxedError>(()) }
) {
    panic!("failed to finalize: {e}");
}
```

**Trigger:** Write failure (disk full, permissions, I/O error) during finalization.

**Impact:** Called on every finalized block. Network-delivered finalizations trigger this path. A full disk crashes every node that receives the finalization.

---

### C5. Syncer: `buffer subscriber closed` expect

**File:** `syncer/src/actor.rs:629`
**Function:** `Actor::run()` (Subscribe handler)

```rust
let aborter = waiters.push(async move {
    (commitment, rx.await.expect("buffer subscriber closed"))
});
```

**Trigger:** The broadcast buffer drops the oneshot sender before delivering the block. Buffer cleanup, shutdown sequences, or memory pressure could cause this.

**Impact:** Crashes the syncer's main loop. Any buffer lifecycle issue becomes a node crash.

---

### C6. Syncer Cache: `put` panic on insertion failure

**File:** `syncer/src/cache.rs:293`
**Function:** `Manager::put()`

```rust
panic!("failed to insert {name}: {e}")
```

**Trigger:** Archive insert fails (disk full, codec error).

**Impact:** Called on every `put_block`, `put_notarization`, `put_finalization` from the syncer hot loop. Every block processed goes through this.

---

### C7. Finalizer: Withdrawal state mismatch (2 instances)

**File:** `finalizer/src/actor.rs:1600-1601`
**Function:** `process_execution_requests()`

```rust
let pending_withdrawal = pending_withdrawal.expect("pending withdrawal must be in state");
assert_eq!(pending_withdrawal.inner, *withdrawal);
```

**Trigger:** A block proposer includes withdrawals that don't match the expected state queue (wrong count, wrong order, wrong amounts).

**Impact:** Every node processing the block crashes. If a proposer crafts a block with unexpected withdrawals, the entire network halts.

**Exploitability:** HIGH. This processes external block data. A TODO comment in the code acknowledges: *"these checks should never fail. we have to make sure that these withdrawals are verified when the block is verified"* — suggesting the verification may be incomplete.

---

### C8. Finalizer: `execute_block()` epoch assertion

**File:** `finalizer/src/actor.rs:1275`
**Function:** `execute_block()`

```rust
assert_eq!(block.epoch(), state.epoch);
```

**Trigger:** A block's epoch field doesn't match the consensus state's current epoch.

**Impact:** Hard assert in the hot path of every block execution (notarized and finalized). A single epoch mismatch from the consensus layer crashes the node.

---

### C9. Finalizer: Mailbox expect

**File:** `finalizer/src/actor.rs:234`
**Function:** `Finalizer::run()`

```rust
let mail = mailbox_message.expect("Finalizer mailbox closed");
```

**Trigger:** All senders drop the mailbox channel (orchestrator/syncer panic or get killed).

**Impact:** Any upstream component crash cascades into the finalizer crashing. OOM kills on the orchestrator propagate here.

---

### C10. Checkpoint: Corrupted checkpoint crashes node on restart (6 instances)

**File:** `node/src/args.rs`

| Line | Function | Trigger |
|------|----------|---------|
| 1093, 1108 | `read_checkpoint()` | Checkpoint file exists but has I/O error or is truncated |
| 1095, 1111 | `read_checkpoint()` | Checkpoint file has corrupted SSZ bytes (partial write, bitrot) |
| 1098, 1114 | `read_checkpoint()` | Checkpoint SSZ valid but semantically invalid (version mismatch) |

**Trigger:** Node restart with a corrupted checkpoint file. A crash mid-write, disk corruption, or version upgrade changing the checkpoint schema all trigger this.

**Impact:** Node cannot restart. No fallback, no retry, no recovery. The only escape is `--checkpoint-or-default` which silently falls back to genesis (potentially worse — starts from height 0).

---

### C11. Consensus State Query: Channel drop panics (9 instances)

**File:** `types/src/consensus_state_query.rs`

Lines 81, 95, 109, 123, 137, 151, 165, 181, 195 — all:

```rust
.expect("consensus state query response sender dropped")
```

**Trigger:** If the finalizer drops the response channel for any reason, all consensus state queries crash.

**Impact:** Systemic — affects checkpoint queries, height queries, balance queries, validator queries. Any finalizer hiccup cascades to all query callers.

---

## Tier 2: HIGH — State Corruption / Timing Targets

These require specific (but realistic) conditions to trigger.

---

### H1. Syncer: Finalized block height mismatch

**File:** `syncer/src/actor.rs:969-973`
**Function:** `Actor::try_dispatch_block()`

```rust
assert_eq!(block.height(), Height::new(next_height), "finalized block height mismatch");
```

**Trigger:** Block retrieved from archive at index `next_height` has a different `.height()`. Indicates archive corruption or index/height mapping bug. Crash-recovery scenarios where a write was partially committed could cause this.

---

### H2. Syncer: Storage read panics (3 instances)

**File:** `syncer/src/actor.rs`

| Line | Function | Target |
|------|----------|--------|
| 1065 | `get_finalized_block()` | `panic!("failed to get block: {e}")` |
| 1081 | `get_finalization_by_height()` | `panic!("failed to get finalization: {e}")` |
| 1168 | `get_latest()` | `.expect("finalization missing")` — index says entry exists but it's absent |

---

### H3. Syncer: Gapped block missing

**File:** `syncer/src/actor.rs:1214`
**Function:** `Actor::try_repair_gaps()`

```rust
panic!("gapped block missing that should exist: {}", gap_end.get());
```

**Trigger:** Gap detection says a block exists at `gap_end` but `get_finalized_block()` returns `None`. Archive state divergence after partial writes or pruning races.

---

### H4. Syncer Cache: Pruning and retrieval panics (8 instances)

**File:** `syncer/src/cache.rs`

| Line | Function | Message |
|------|----------|---------|
| 66 | prune | `"failed to prune archives: {e}"` |
| 135 | metadata | `"failed to write metadata"` |
| 220 | init | `"failed to initialize {name} archive"` |
| 308 | get notarization | `"failed to get notarization"` |
| 320 | get finalization | `"failed to get cached finalization: {e}"` |
| 335 | get verified block | `"failed to get verified block"` |
| 345 | get notarized block | `"failed to get notarized block"` |
| 370-374 | epoch removal | `.remove(epoch).unwrap()` + `.destroy().await.expect(...)` |

---

### H5. Finalizer: BLS key encoding panic

**File:** `finalizer/src/actor.rs:850-851`
**Function:** `Finalizer::handle_aux_data_mailbox()`

```rust
let consensus_bytes: [u8; 48] = acc.consensus_public_key
    .encode().as_ref()[..48].try_into()
    .expect("BLS public key must be 48 bytes");
```

**Trigger:** A validator's stored BLS public key encodes to fewer than 48 bytes (malformed deposit, dependency upgrade changing encoding).

**Impact:** Triggered during epoch boundary block proposals. A single corrupt validator account crashes every node building aux data for the last block of the epoch.

---

### H6. Finalizer: Validator account missing during activation

**File:** `finalizer/src/actor.rs:1034-1036`
**Function:** `Finalizer::update_validator_committee()`

```rust
let account = self.canonical_state.validator_accounts
    .get_mut(&key_bytes)
    .expect("only validators with accounts are added to the added_validators queue");
```

**Trigger:** A validator pubkey is in `added_validators` but has no entry in `validator_accounts`. State corruption or account removal before activation epoch.

**Impact:** Every epoch boundary where new validators activate. One inconsistent entry crashes all nodes.

---

### H7. Finalizer: Epoch genesis hash assertion

**File:** `finalizer/src/actor.rs:296`
**Function:** `Finalizer::run()`

```rust
assert_eq!(epoch, self.canonical_state.epoch);
```

**Trigger:** A `GetEpochGenesisHash` message for a non-current epoch. The code has a TODO: *"verify that this can never happen"*.

---

### H8. Consensus State: Validator key deserialization (5 instances)

**File:** `types/src/consensus_state.rs`

Lines 266, 282, 301, 330, 346 — all the same pattern:

```rust
let node_public_key = PublicKey::read(&mut key_bytes).expect("failed to parse public key");
```

**Trigger:** A `[u8; 32]` key in `validator_accounts` fails `PublicKey::read()` deserialization. Requires state corruption or a deserialization bug. Called on every epoch transition and committee query.

**Root cause:** Design mismatch — `BTreeMap<[u8; 32], ValidatorAccount>` requires re-parsing keys on every access.

---

### H9. Engine Config: DB corruption at startup

**File:** `node/src/args.rs:623`
**Function:** `run_node()`

```rust
.unwrap();  // EngineConfig::get_engine_config()
```

**Trigger:** Corrupted consensus DB at restart. This is where DB state and checkpoint state interact.

---

### H10. EL Bootstrap: Missing snapshot panic

**File:** `node/src/args.rs:448-459`
**Function:** `run_node()`

```rust
panic!("FATAL: No EL snapshot found at epoch boundary block {}! ...", block_num);
```

**Trigger:** EL bootstrap at an epoch boundary block that lacks a snapshot in `extra_data`. EL corruption, version mismatch, or running against an older EL.

---

### H11. Application Actor: Finalizer coordination panics

**File:** `application/src/actor.rs`

| Line | Message | Trigger |
|------|---------|---------|
| 263 | `"failed to get epoch genesis hash from finalizer"` | Finalizer drops |
| 450 | `result.unwrap()` | Block verification join failure |
| 474 | `"Finalizer dropped"` | Finalizer drops during aux data fetch |

---

### H12. Scheme Provider: Lock and initialization panics

**File:** `types/src/scheme.rs`

| Line | Issue |
|------|-------|
| 94, 100, 109, 119 | `.lock().unwrap()` on schemes HashMap — poisoned mutex |
| 137 | `"failed to decode BLS public key"` |
| 141 | `"failed to build BiMap"` |
| 294 | `"failed to create threshold scheme"` |
| 369 | `"failed to build participants set"` |

---

### H13. Engine: Startup key material panics

**File:** `node/src/engine.rs`

| Line | Message | Trigger |
|------|---------|---------|
| 148 | `"failed to extract scalar from private key"` | Malformed consensus key at startup |
| 178 | `"BLS public key must be 48 bytes"` | Any validator in initial state has malformed BLS key → every node panics |
| 269 | `"failed to initialize finalizations by height archive"` | Storage init failure |
| 304 | `"failed to initialize finalized blocks archive"` | Storage init failure |

---

### H14. Engine Client: IPC connection (no retry)

**File:** `types/src/engine_client.rs:102, 122`

```rust
let provider = ProviderBuilder::default().on_ipc(ipc).await.unwrap();
```

**Trigger:** Reth IPC socket doesn't exist or reth hasn't started yet. No retry loop at startup (unlike post-init reconnects which have `wait_until_reconnect_available()`).

---

## Tier 3: MEDIUM — Operational Edge Cases

| File | Line(s) | Issue |
|------|---------|-------|
| `args.rs` | 266, 269, 273-275 | Genesis file missing/malformed at startup |
| `args.rs` | 314, 465 | Malformed CLI args (`--restart-from-block`, `--bootstrap-from-el`) |
| `args.rs` | 554, 556 | Bootstrappers file missing/malformed |
| `args.rs` | 379 | EL unreachable during `--bootstrap-from-el latest` |
| `args.rs` | 547 | Prometheus port conflict |
| `consensus_state.rs` | 372 | `try_into().unwrap()` on PublicKey→[u8;32] |
| `rpc/server.rs` | 219, 225, 227, 229 | Signature/key size assumptions in RPC responses |
| `orchestrator/actor.rs` | 347-349 | Epoch channel registration failures |

---

## Remote Attack Surface Analysis

> **Constraint:** Attacker does NOT have SSH access to validator machines. They can only interact over the P2P network or as a validator in the committee. Killing reth or corrupting local files is trivially a chain halt and not interesting.
>
> **Testnet note:** For the upcoming testnet, Ritual runs all validators. The findings below that require a **malicious staked validator** (committee member) are **not a risk for testnet** — they only matter for mainnet or any deployment where third parties run validators. An external user submitting transactions to the RPC cannot trigger any of these paths.

### Network Exposure: Firewall + Crypto Validation

**Layer 0: GCP Firewall (when `SKIP_FIREWALL_LOCKDOWN=false`)**

The deployment infra (`firewall_lockdown.sh`) replaces permissive `0.0.0.0/0` rules with IP whitelists:

| Rule | Who gets access | Ports |
|------|----------------|-------|
| `validator-internal` | Only validator node IPs | TCP 27656 (P2P), 3030 (RPC), 8545/8546 (EL), K3s internals |
| `executor-to-el` | Only executor IPs | TCP 8545, 8546, 3030 |
| `traffic-to-el` | Only traffic-gen IPs | TCP 8545, 8546 |
| `operator-access` | Only deployer IP | TCP 22, 8545, 3030, etc. |

Summit listens on **port 27656** (P2P/commonware) and **port 3030** (RPC). When firewall lockdown is enabled, only other validators can reach port 27656. An external party cannot even open a TCP connection to summit's P2P layer.

**Current testnet config (`sjs-hel.sh`) uses `SKIP_FIREWALL_LOCKDOWN=true`** — firewall is open for testing. For production/mainnet, this should be `false`.

**Layer 1-3: Cryptographic validation (defense-in-depth even without firewall)**

Even if the firewall is open (or an attacker is on the same network), summit has three layers of signature verification:

1. **Batcher (first line):** All votes and certificates from peers pass through `verify()` (aggregate signature check) before forwarding. Invalid messages get the peer blocked.
2. **Resolver (second line):** Certificates fetched via request/response are re-verified before delivery.
3. **Syncer handler (third line):** Notarizations/finalizations delivered via the resolver are verified again with commitment matching.

**Result: An outsider who is not in the validator set cannot get messages past the batcher's signature checks.** Even with `SKIP_FIREWALL_LOCKDOWN=true`, the cryptographic verification rejects all messages from non-validators. All of the syncer panics (C3, C4, C5, H1-H4) require local storage failures, not crafted network input.

**Can someone flood summit's P2P port with junk?** They can open connections and send garbage bytes, but the batcher will reject and block the peer after the first invalid message. This is a bandwidth/resource concern (connection exhaustion) rather than a panic path — but with firewall lockdown enabled, they can't even reach the port.

### What a Malicious VALIDATOR Can Do

A malicious validator (committee member) can propose blocks. The block verification path is:

1. `application::handle_verify()` — checks metadata only (parent, height, timestamp)
2. `engine_client.check_payload()` — calls `engine_newPayloadV4` on reth. Validates EL execution.
3. **Validators vote. Block gets notarized/finalized.**
4. `finalizer::execute_block()` — runs `process_execution_requests()`

**Critical gap: Withdrawal verification happens POST-CONSENSUS, not PRE-CONSENSUS.**

The `verify()` step checks zero CL-level withdrawal data. The EL `check_payload` validates EL execution but not CL withdrawal semantics. This means:

#### Finding: CL/EL State Divergence via Invalid Withdrawals

> **Attacker model: Malicious staked validator only.** This requires being a committee member who is selected as block proposer. A regular user submitting transactions to the RPC endpoint **cannot** trigger this — withdrawals are a CL-level concept controlled entirely by the block proposer, not by EL transaction senders. **Not a risk for testnet** (Ritual runs all validators). **Mainnet risk** when third-party validators join.

A malicious proposer can include incorrect withdrawals in a block. The block passes `verify()` and `check_payload()`, honest validators vote for it, and it gets finalized. Then in `execute_block()`:

```
withdrawals_match = block.payload.payload_inner.withdrawals == expected_withdrawals;
```

This fails. The `else` branch fires (line 1238):
- EL state transitions are **NOT applied** (forkchoice head not updated)
- But CL state **still advances unconditionally** (line 1272): height, view, head digest all update

**Impact:** CL and EL diverge. The CL considers the block part of the chain, but the EL never applied it. Subsequent blocks referencing this EL parent also fail `parent_matches`, cascading the failure. **EL progress halts while the CL chain continues.**

The TODO in the code (line 1598) acknowledges this: *"these checks should never fail. we have to make sure that these withdrawals are verified when the block is verified. it is too late when the block is committed."*

**Note:** The `expect`/`assert_eq` panics at lines 1600-1601 are actually **guarded** by the `withdrawals_match` check — `process_execution_requests` only runs inside the `if withdrawals_match` branch. So the panics themselves are not reachable via crafted withdrawals, but the state divergence is.

#### Finding: Deposit Request Processing Panics

A related question: can a malicious proposer include deposit requests that trigger panics in `parse_execution_requests()`? The deposit requests come from the EL block's execution requests, which are validated by `check_payload`. If reth's `engine_newPayloadV4` returns `VALID`, the deposit requests should be consistent with the EL state. However, the `verify_deposit_request()` function (line 1650) does additional CL-level checks that could reject deposits — but rejection doesn't panic, it logs a warning.

### Panic Reachability Summary (Remote Attacker)

| Panic | Remotely Triggerable? | Requires |
|-------|----------------------|----------|
| C1-C2: Engine client panics | **No** | Local reth failure |
| C3-C6: Storage panics | **No** | Local disk failure |
| C5: Buffer subscriber | **No** | Node shutdown race |
| C7: Withdrawal expect/assert | **No** — guarded by `withdrawals_match` | N/A |
| C8: Epoch assert | **Possibly** by malicious validator | Epoch desync between components |
| C9: Mailbox drop | **No** | Internal component crash |
| C10: Checkpoint | **No** | Local file corruption |
| C11: Query channel drop | **No** | Internal finalizer failure |
| H1-H4: Syncer invariants | **No** | Local state corruption |
| H5: BLS key encoding | **Possibly** by malicious deposit | Malformed BLS key in deposit accepted by EL |
| H8: Consensus state keys | **No** | State corruption |

### The Real Remote Attack: CL/EL State Divergence

**Not a panic, but potentially worse.** A malicious validator (1 of N) can halt EL progress for the entire chain by proposing a block with invalid withdrawals. The block passes pre-consensus verification, gets finalized, then fails post-consensus withdrawal matching. The CL continues but the EL stops making progress.

**Severity:** CRITICAL for mainnet — a single malicious committee member can halt EL execution.

**Requires:** Being a staked validator in the committee. **Cannot** be triggered by an external user sending transactions. Not a risk for testnet where Ritual controls all validators.

---

## Panic Attack Surface Map (Corrected)

```
    REMOTE ATTACKER (non-validator)
    │
    │  All messages rejected by batcher signature verification.
    │  No panic paths reachable.
    │
    ╳ ← blocked here

    MALICIOUS VALIDATOR (committee member)
    │
    ├─► Propose block with bad withdrawals
    │     ├─ Passes verify() ✓ (no withdrawal checks)
    │     ├─ Passes check_payload() ✓ (EL-only)
    │     ├─ Gets notarized/finalized ✓
    │     └─► execute_block() → withdrawals_match=false
    │           ├─ EL state NOT updated (forkchoice head stale)
    │           ├─ CL state advances anyway
    │           └─► CL/EL DIVERGENCE — EL halted
    │                (not a panic, but chain halt)
    │
    ├─► Propose block with bad epoch?
    │     └─ assert_eq!(block.epoch(), state.epoch)
    │        Unclear if reachable — needs investigation
    │
    └─► Include malformed deposit via EL?
          └─ BLS key encoding expect at epoch boundary
             Unlikely — EL validates deposit format
```

---

## Targets for Inducing Panics (Revised)

Reframed for realistic operational scenarios (not "attacker has root access"):

| # | Target | Scenario | Attacker model | Testnet risk? | File:Line |
|---|--------|----------|----------------|---------------|-----------|
| 1 | **CL/EL state divergence** | Malicious validator proposes block with bad withdrawals → EL halts | Staked validator (committee member) | **No** — Ritual runs all validators | `finalizer/actor.rs:1177,1238` |
| 2 | **Disk exhaustion** | Sustained high block production fills disk → storage panics cascade | Staked validator (spam blocks) | **No** — Ritual runs all validators | `syncer/actor.rs`, `cache.rs` |
| 3 | **Checkpoint corruption on restart** | Node crashes mid-write, checkpoint corrupted → can't restart | Operational (no attacker needed) | **Yes** — can happen to anyone | `args.rs:1093-1114` |
| 4 | **Archive inconsistency after crash** | SIGKILL during `store_finalization()` → height mismatch / gap panic on restart | Operational (no attacker needed) | **Yes** — can happen to anyone | `syncer/actor.rs:969,1214` |
| 5 | **Epoch boundary BLS key panic** | Malformed BLS key enters validator set via deposit → crashes all nodes at epoch transition | Staked validator or deposit submitter (if EL doesn't validate key format) | **Unlikely** — needs investigation of deposit validation | `finalizer/actor.rs:850` |

**For testnet:** Only items 3 and 4 are relevant — both are operational reliability issues (crash recovery), not attacks. Everything else requires a malicious staked validator, which doesn't apply when Ritual controls the full committee.

---

## Structural Observations

### Pattern 1: Storage errors are always fatal
The entire storage layer (`finalized_blocks`, `finalizations_by_height`, cache archives) treats every `Err` as unrecoverable via `panic!`. There is no retry, no degraded mode, no circuit breaker. A transient disk hiccup crashes the node. Not remotely triggerable, but a reliability concern.

### Pattern 2: One-retry-then-crash for EL communication
The engine client has a reconnect mechanism (`wait_until_reconnect_available`) but only retries once. The retry itself uses `.expect()`, so a double-failure (reconnect succeeds but the call fails again) is still a crash. Only relevant if reth is unstable on the same machine.

### Pattern 3: Cross-component cascading failures
Component death propagates via channel closes:
- Finalizer dies → mailbox closes → syncer crashes on query expect
- Orchestrator dies → finalizer mailbox closes → finalizer crashes
- Any component panic poisons shared mutexes → all lock users crash

### Pattern 4: Checkpoint/restart has zero fault tolerance
The checkpoint loading path has 6 sequential `expect()` calls with no recovery. A single corrupt byte means the node cannot restart. There's no checksum validation, no backup checkpoint, and the fallback (`--checkpoint-or-default`) silently resets to genesis.

### Pattern 5: Consensus state key type mismatch
`validator_accounts` uses `BTreeMap<[u8; 32], ValidatorAccount>` but the API returns `PublicKey`. Every access requires `PublicKey::read().expect()` — a design-level issue causing 5 identical panic points on consensus-critical paths.

### Pattern 6: Pre-consensus verification gap (NEW — most important)
Withdrawal validation is entirely absent from the pre-consensus `verify()` path. The `handle_verify()` function checks only metadata (parent, height, timestamp) and the EL validates only execution semantics. CL-specific data (withdrawals, validator operations) is only checked post-consensus in `execute_block()`, by which point the block is already finalized. This is the only path where a remote actor (malicious validator) can cause chain-level damage without local access.
