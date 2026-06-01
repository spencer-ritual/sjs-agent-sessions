# Alloy EVM PR Notes: StakeHub Reward Routing

Reviewed PR:

- `ritual-alloy-evm-internal#64`: Route block rewards through Ritual StakeHub

Related PR context:

- `ritual-sc-internal#203`: adds `RitualStakeHub` / `RitualStakeCredit`
- `ritual-node-internal#358`: wires StakeHub validator workflows and generated resources
- `ritual-common-internal#126`: updates staking contract addresses
- `ritual-reth-internal#409`: removes legacy deposit address wiring
- `ritual-summit-internal#65`: reads validator committees from Ritual StakeHub

## Alloy EVM-Specific Review Notes

| Priority | Issue | Notes |
| --- | --- | --- |
| High | Fix priority-fee accounting before routing rewards through StakeHub. | PR #64 explicitly accumulates transaction priority fees and adds them to `total_staking_reward`, then funds `SYSTEM_ADDRESS` and calls `RitualStakeHub.distributeReward(...)`. Unless the normal revm priority-fee payment to `block.beneficiary()` is also disabled, redirected, or debited, this double-counts tips. The logic is only justified if StakeHub is meant to own tips too; in that case the PR needs to remove the original tip payment path or settle against it. |
| Medium | Review the `Some(0)` post-block balance increment path instead of treating it as an obvious preserve. | `crates/ritual-evm/src/eth/block.rs` still calls `post_block_balance_increments_with_reward(...)` and passes `Some(0)` to suppress direct block/ommer rewards, then manually credits `SYSTEM_ADDRESS` with `total_staking_reward`. That helper also handles withdrawals and ommer reward entries, so the PR should explicitly justify which parts of the old post-block increment path still belong after StakeHub owns reward distribution. |
| Low | Rename or reframe the value-bearing `transact_system_call_with_value` helper. | In upstream EVM/Reth code, “system call” has a specific meaning: protocol-triggered calls to system contracts such as EIP-4788/2935/7002/7251, generally with no `msg.value`. The StakeHub reward path is a chain-specific payable protocol reward call. The helper may be mechanically needed, but naming/framing it as just another system call makes the semantic boundary less clear. |

## Evidence

Before this PR, there were two separate reward paths:

- Transaction priority fees were handled during normal revm transaction execution and paid to `block.beneficiary()`.
- The configured/base block reward was handled later through `post_block_balance_increments_with_reward(...)`.

So `block.rs` did not need to calculate priority fees itself.

PR #64 changes the base reward path: instead of directly incrementing the beneficiary, it builds a `total_staking_reward = base_block_reward + priority_fees_accumulated`, funds `SYSTEM_ADDRESS`, then calls `RitualStakeHub.distributeReward(...)` with that value. That requires explicitly tracking priority fees because the post-block reward helper never tracked them before.

The concern is: unless the normal revm priority-fee payment to `beneficiary` is also disabled, redirected, or debited, this new logic double-counts tips. So the logic is only justified if StakeHub is meant to own tips too, but then the PR needs to remove the original tip payment path or settle against it.

## Post-Block Balance Increment Path

File: `crates/ritual-evm/src/eth/block.rs`

Relevant PR snippet:

```rust
let base_block_reward = base_block_reward.unwrap_or_default();
let total_staking_reward = base_block_reward.saturating_add(self.priority_fees_accumulated);

let mut balance_increments = post_block_balance_increments_with_reward(
    &self.spec,
    alloy_evm::Evm::block(&self.evm),
    self.ctx.ommers,
    self.ctx.withdrawals.as_deref(),
    Some(0),
);
if total_staking_reward > 0 {
    *balance_increments.entry(SYSTEM_ADDRESS).or_default() += total_staking_reward;
}
```

High level, `post_block_balance_increments_with_reward(...)` builds a map of end-of-block balance credits. It updates three categories:

- Ommer/uncle rewards, credited to each ommer beneficiary.
- The block reward, credited to `block_env.beneficiary()`.
- Withdrawals, credited to withdrawal recipients after Shanghai.

Passing `Some(0)` suppresses the reward part by forcing the custom block reward to zero instead of falling back to the chainspec/default reward. That means the block beneficiary and ommer reward entries are zeroed out, while the helper still runs the rest of the post-block increment machinery, especially withdrawals.

That may be correct, but it deserves explicit review. Once StakeHub owns reward distribution, it is not self-evident that the old helper should stay in place with only one category suppressed. The PR should justify whether ommer handling and withdrawal handling should still happen through this same block of code, or whether the reward-routing change should delete/split the old reward increment path and keep only the explicitly intended non-reward increments.

## Value-Bearing Protocol Call Framing

PR #64 adds `transact_system_call_with_value(...)` so the StakeHub reward call can carry `msg.value`. The existing upstream-style `transact_system_call(...)` helpers are zero-value protocol calls into system contracts, and several of them intentionally retain only the target contract state.

The StakeHub call is different: it funds `SYSTEM_ADDRESS`, sends value to `RitualStakeHub.distributeReward(...)`, and must preserve full state because value movement and reward distribution can touch multiple accounts/contracts. That is a real need, but the name `transact_system_call_with_value` makes it look like a small extension of upstream EIP system-call semantics. A clearer name or comment should mark it as a Ritual-specific payable reward-distribution protocol call.

## Code Pointers

- Reward routing: `crates/ritual-evm/src/eth/block.rs`
- Post-block reward increments: `crates/ritual-evm/src/block/state_changes.rs::post_block_balance_increments_with_reward`
- StakeHub reward helpers: `crates/ritual-evm/src/block/system_calls/block_reward.rs`
