# Ritual SC PR Notes: StakeHub Contract Port

Reviewed PR:

- `ritual-sc-internal#203`: Add BSC-derived Ritual staking contracts

Related PR context:

- `ritual-node-internal#358`: wires StakeHub validator workflows and generated resources
- `ritual-common-internal#126`: updates staking contract addresses
- `ritual-reth-internal#409`: removes legacy deposit address wiring
- `ritual-alloy-evm-internal#64`: routes block rewards through StakeHub
- `ritual-summit-internal#65`: reads validator committees from Ritual StakeHub

## Ritual SC-Specific Review Notes

| Priority | Issue | Notes |
| --- | --- | --- |
| High | Increase the default unbond period; `1000` blocks is too short for production staking. | Ritual changes unbonding from BSC's time-based `7 days` prior to a block-based `unbondPeriod`, then initializes it to `1000` blocks. At the assumed 300ms block time, `1000` blocks is about 5 minutes. The BSC contract/comment gives a prior that undelegated funds should be claimable a few days later, which protects against fast exit around validator misbehavior and operational incidents. Pick a production-scale block count and document the intended duration/tradeoff. |
| Medium | Preserve explicit validator fields if slashing, jailing, or vote-address support is expected soon. | `RitualStakeHub.Validator` removes BSC's `voteAddress`, `jailed`, `jailUntil`, and `agent` fields and replaces the remaining capacity with `uint256[20] __reservedSlots`. That is fine if those features are intentionally out of scope long-term, but it is not the same storage shape as BSC and makes later reintroduction a storage-layout design/migration task. If we intend to support slashing, jailing, fast-finality vote addresses, or validator agents soon, it is safer to keep explicit unused fields or document a precise reserved-slot plan now. |
| Medium | Move active-validator sorting out of `RitualStakeHub` and into Summit if sorting is required. | Ritual's `_activeValidators()` filters validators by `minSelfDelegation`, then sorts them by voting power and consensus address before returning the active set. If that ordering is only needed so Summit can build a deterministic committee, the sorting policy belongs on the Summit side rather than inside the staking contract. Keeping the contract closer to BSC's raw election-info surface reduces protocol coupling and makes the contract expose stake/accounting state while Summit owns committee-construction policy. |
| Nit | Avoid formatting-only churn and moved-function churn in the BSC-derived port where possible. | The source diff would be easier to review if single-line upstream checks such as `if (_validatorSet.contains(operatorAddress)) revert ValidatorExisted();` were not reformatted into multi-line blocks unless the condition or behavior changes. The same applies to moving functions such as `editCommissionRate`, `editConsensusAddress`, and `editDescription`: they existed upstream, but the new location makes the diff look like a deletion plus a completely new implementation. Keeping formatting and function order stable around retained logic makes the semantic differences from BSC easier to audit. |
| Nit | Prefer BSC parity over tiny cleanup improvements unless the change is intentional. | Ritual changes `uint256 delegation = msg.value - LOCK_AMOUNT` into a guarded ternary that maps underfunded creation to `delegation = 0` and then reverts with `SelfDelegationNotEnough`. That is slightly nicer than BSC's Solidity checked-arithmetic panic when `msg.value < LOCK_AMOUNT`, but it is still a behavioral diff. Ritual also extracts the inline commission validation into `_checkCommission(...)` and changes `_checkMoniker(...)` semantics, which may be cleaner locally but adds more source drift. For this kind of port, prefer fewer diffs unless the improved revert behavior, helper extraction, or moniker policy change is intentionally worth carrying and documenting. |

## Evidence

Binance `StakeHub.Validator` includes:

```solidity
struct Validator {
    address consensusAddress;
    address operatorAddress;
    address creditContract;
    uint256 createdTime;
    bytes voteAddress;
    Description description;
    Commission commission;
    bool jailed;
    uint256 jailUntil;
    uint256 updateTime;
    address agent;
    uint256[19] __reservedSlots;
}
```

Ritual `RitualStakeHub.Validator` keeps only:

```solidity
struct Validator {
    address consensusAddress;
    address operatorAddress;
    address creditContract;
    uint256 createdTime;
    Description description;
    Commission commission;
    uint256 updateTime;
    uint256[20] __reservedSlots;
}
```

Because `RitualStakeHub` is UUPS/`ERC1967Proxy` deployed, struct storage layout matters for future upgrades. Re-adding removed fields in their original BSC positions would shift existing fields; adding them at the end is possible, but no longer source- or storage-shape compatible with the BSC layout.

Example formatting-only diff noise:

```diff
-        if (_validatorSet.contains(operatorAddress)) revert ValidatorExisted();
+        if (_validatorSet.contains(operatorAddress)) {
+            revert ValidatorExisted();
+        }
```

Example tiny semantic cleanup:

```diff
-        uint256 delegation = msg.value - LOCK_AMOUNT; // create validator need to lock 1 BNB
+        uint256 delegation = msg.value > LOCK_AMOUNT ? msg.value - LOCK_AMOUNT : 0;
```

The same parity concern applies to extracting BSC's inline commission check into `_checkCommission(...)`: it is a reasonable local cleanup, but it adds another nonessential diff in a contract where source-level comparison is part of the review strategy. It also applies to `_checkMoniker(...)`: BSC required length 3-9 with an uppercase first character and alphanumeric remaining characters, while Ritual allows length 1-20 and permits `-` / `_`. That may be fine, but it should be documented as an intentional naming-policy change rather than incidental port drift.

## Active Validator Sorting

Ritual adds `_activeValidators()` as a contract-side election helper. It filters out validators whose self-delegation is below `minSelfDelegation`, computes voting power from `totalPooledRITUAL()`, sorts candidates through `_shouldSwap(...)`, and then truncates to `maxElectedValidators`.

BSC's comparable election-info surface returns the validator set order and voting powers, with jailed validators zeroed. If Ritual needs deterministic stake-ranked ordering for Summit committee construction, that policy should likely live in Summit, where the committee is consumed and where ordering can be tested against Summit's epoch-transition behavior. Putting it in `RitualStakeHub` makes the staking contract responsible for a consensus-client ordering rule rather than exposing stake/accounting data.

## Unbond Period

BNB initializes `unbondPeriod = 7 days`, and its undelegate docs say funds are only claimable a few days later. Ritual changes this to a block-based period:

```solidity
uint256 unlockBlock = block.number + IRitualStakeHub(STAKE_HUB_ADDR).unbondPeriod();
```

The PR initializes `unbondPeriod: 1000`. With the assumed 300ms block time, that is:

```text
1000 * 0.3s = 300s = 5 minutes
```

That is a material protocol change from the BSC prior. It may be useful for local testing, but the production default should be set deliberately and documented.

## Code Pointers

- Ritual contract: `src/staking/RitualStakeHub.sol`
- BSC comparison diff: `sjs-agent-sessions/stakehub/ritual-vs-bsc-stakehub.diff`
