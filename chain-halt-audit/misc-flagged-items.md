# Misc Flagged Items

## `tx.origin` vs `msg.sender` inconsistency in `AsyncJobTracker.sol`

**File:** `ritual-sc-internal/src/async/AsyncJobTracker.sol` (lines 69–77)

```solidity
modifier onlyCommitmentSender() {
    require(msg.sender == ASYNC_COMMITMENT_SYSTEM_SENDER, "only commitment sender");
    _;
}

modifier onlySettlementSender() {
    require(tx.origin == ASYNC_SETTLEMENT_SYSTEM_SENDER, "only settlement sender");
    _;
}
```

`onlyCommitmentSender` checks `msg.sender` while `onlySettlementSender` checks `tx.origin`. This is inconsistent and the use of `tx.origin` is generally discouraged—it bypasses intermediate contract identity, which can open phishing/relay attack surfaces. If there is a reason settlement must trace back to the EOA origin rather than the direct caller, it should be explicitly documented and justified. Otherwise this should be brought in line with the `msg.sender` pattern used by the commitment modifier.

## Max TTL enforced off-chain only — not in the delivery/tracker contracts

The Rust validation layer (`validate_image_call_payload` and all other `validate_*_payload` functions in `ritual-reth-internal/crates/ritual-async/src/validation.rs`) enforces that TTL does not exceed `max_ttl_blocks()`. The current default is **500 blocks** (configurable via `ASYNC_MAX_TTL_BLOCKS` env var, defined in `ritual-reth-internal/crates/ritual-async-inspector/src/lib.rs`).

However, the Solidity contracts (`AsyncJobTracker.sol`, `AsyncDelivery.sol`) perform **no TTL bounds check**. `_storeJob` in `AsyncJobTracker.sol` stores the TTL and computes the expiry bucket as `block.number + ttl` with no upper-bound validation:

```solidity
// AsyncJobTracker.sol — _storeJob (line 249–260)
j.ttl = ttl;
j.created = createdAt;
// ...
uint256 exp = block.number + ttl;
expiryBuckets[exp].push(id);
```

The max TTL check is enforced at three off-chain layers — RPC validation, block builder, and block verifier (`validate_commitment_structure` in `ritual-async-commitment-validator`). The verifier is consensus-critical: other honest validators will reject a proposed block containing a commitment with `ttl > max_ttl_blocks()`. So a single malicious node cannot unilaterally sneak in an infinite TTL.

However, `max_ttl_blocks()` itself is **not a protocol constant** — it's read from the `ASYNC_MAX_TTL_BLOCKS` environment variable per-node, defaulting to 500. The code comments say "All validators on the network MUST use the same value", but nothing enforces this. Risks:

1. **Configuration drift → consensus failure.** If validators disagree on `ASYNC_MAX_TTL_BLOCKS`, they will disagree on block validity. A block with TTL 600 would be accepted by a node configured with max 1000 but rejected by one using the default 500 — causing chain splits or stalls.
2. **No on-chain backstop.** The Solidity contracts perform zero TTL bounds checking, so there is no defense-in-depth if the off-chain layer is misconfigured or a future refactor removes the check.
3. **A consensus-critical parameter lives in an env var.** Whether a block is valid or invalid hinges on a per-node configuration value with no on-chain anchor or governance mechanism.

## Redundant `agentAddress` field and odd existence check in `AgentHeartbeat.sol`

**File:** `ritual-sc-internal/src/heartbeat/AgentHeartbeat.sol`

The `AgentRecord` struct stores an `agentAddress` field that is always set to `msg.sender` — the same value used as the key in the `_agents` mapping. This makes the field redundant with the mapping key (it exists so the struct is self-contained when returned from view functions like `getAgentInfo()`).

The existence/registration check throughout the contract uses this field in an unintuitive way:

```solidity
// unregister (line 91–94)
function unregister() external {
    require(_agents[msg.sender].agentAddress == msg.sender, "not registered");
    _removeAgent(msg.sender);
}

// heartbeat (line 100–102)
function heartbeat(string calldata manifestCID, bytes calldata executorSignature) external {
    AgentRecord storage record = _agents[msg.sender];
    require(record.agentAddress == msg.sender, "not registered");
```

Because `agentAddress` can only ever be `msg.sender` (set at registration) or `address(0)` (default for uninitialized storage), checking `== msg.sender` is functionally equivalent to `!= address(0)`. No real caller can have `msg.sender == address(0)`, so both forms work. However, `!= address(0)` is the conventional Solidity idiom for an existence check and would be immediately obvious to readers. The `== msg.sender` form requires tracing through the registration logic to confirm it's equivalent.

Notably the contract already uses the conventional form in `register()`:

```solidity
// register (line 64)
require(_agents[msg.sender].agentAddress == address(0), "already registered");
```

This is an inconsistency — register checks `== address(0)` (conventional) while unregister and heartbeat check `== msg.sender` (unconventional). Not a bug, but a readability issue worth normalizing.

## Refunds in `AsyncDelivery.sol` should be non-blocking

**File:** `ritual-sc-internal/src/async/AsyncDelivery.sol`

In `deliver()`, after the callback executes, the contract refunds unused gas (and value on revert) to the user via `RITUAL_WALLET.refundGas{value: ...}(...)`. These refund calls are made inline and their failure would revert the entire delivery transaction:

```solidity
// Lines 185–187 (callback reverted path)
if (totalRefund > 0) {
    RITUAL_WALLET.refundGas{value: totalRefund}(user, totalRefund, uint256(jobId));
}

// Lines 190–192 (callback succeeded path)
if (gasRefund > 0) {
    RITUAL_WALLET.refundGas{value: gasRefund}(user, gasRefund, uint256(jobId));
}
```

If `refundGas` reverts for any reason — the wallet contract is paused, upgraded with a bug, the user's wallet rejects ETH, or the call runs out of gas — the entire `deliver()` transaction reverts. This means the callback result is lost, the job is not marked as delivered, and the executor's payment is rolled back, even though all of that work was already done successfully.

Refunds should be made non-blocking so that a refund failure does not take down the entire delivery. Options include:

1. **Wrap refund calls in a try/catch or low-level call** so a failure is logged (e.g. via a `RefundFailed` event) but does not revert delivery. Failed refunds can be retried or claimed later.
2. **Use a pull-based refund pattern** — record the refund amount owed and let the user withdraw it separately.

Either approach makes the delivery path more robust: the callback result gets recorded, the executor gets paid, and the job reaches its terminal state regardless of whether the refund transfer succeeds.

## Unbounded `Call.data` enables storage/gas griefing in `Scheduler.sol`

**File:** `ritual-sc-internal/src/scheduler/Scheduler.sol`

`Call.data` is stored in contract storage with no max length check. An attacker can schedule calls with large `data` (~30–40 KB per call, bounded only by block gas at schedule time). The problem is **asymmetric cost**:

- **Creation:** Attacker pays per `schedule()` tx; each fits in one block.
- **Cleanup:** When `slots.length > CLEANUP_THRESHOLD`, `execute()` triggers `_cleanupExpiredCalls`, which can free up to `MAX_CLEANUP_PER_EXECUTE` (25) expired slots in a single tx. Each `_freeSlot()` calls `_wipeBytes(slots[i].data)`, which does `ceil(len/32)` SSTORE operations.

If the attacker creates ~25 expired calls with ~30 KB `data` each, the cleanup path would perform 25 × ~960 ≈ 24,000 SSTOREs in one tx — roughly 70M gas for wipes alone, exceeding typical block limits. The `execute()` tx would revert with OOG, impacting liveness.

**Why gas doesn't mitigate:** The attacker's cost is spread over many blocks; the victim's cleanup cost is concentrated in one tx and hits the block gas limit.

**Remedy:** Add `require(data.length <= MAX_DATA_BYTES)` in `_schedule()`, e.g. `MAX_DATA_BYTES = 4096`, so that even when 25 slots are wiped in one cleanup batch, the total wipe cost stays within block gas.
