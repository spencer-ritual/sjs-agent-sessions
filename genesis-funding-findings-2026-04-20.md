# Genesis Funding Findings

## Scope

This note captures current findings about genesis-funded assets and replayed liquidity on the live Ritual chain.

## Confirmed: live chain is using `WETH.release.json`

### Why

The live RPC at `https://rpc.ritualfoundation.org` matches the `release` funding set rather than `dev`.

Strongest signal:

- a `release`-only prefunded agent address exists live:
  - `0xE305d3C3A62c14605221bbd669957446851C95B0`
- that address is present in `prefunded_agents.release.json`
- that address is not present in `prefunded_agents.dev.json`
- live balances for that address are:
  - about `20,000,000 ETH`
  - about `10,000,000 WETH`

That is strong evidence that the live chain was generated from the `release` genesis variant, not the `dev` one.

### How `release` vs `dev` gets chosen

`ritual-node-internal` does not merge both WETH files. It chooses one environment-specific file:

- `WETH.dev.json`
- `WETH.release.json`
- fallback `WETH.json` only if no matching env-specific file is selected

The selection logic lives in `ritual-node-internal/configgen/el_genesis.py`.

Important behavior:

- `WETH` is treated as an environment-specific resource
- if the environment is `dev`, configgen uses `WETH.dev.json`
- if the environment is `release`, configgen uses `WETH.release.json`
- the chosen WETH file is loaded last so it overrides any WETH state inside `uniswap_replayed.json`

Operational defaults we found:

- local `ritual-node-internal` startup defaults to `dev`
- `chain-deployment-infra` defaults to `release`-tagged Reth images

So for the live chain, current evidence points to the `release` path.

## WETH release holder set

Current finding for `WETH.release.json`:

- the holder set matches:
  - all addresses in `prefunded_agents.release.json`
  - plus the Uniswap pool `0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640`
- no extra WETH holders were found beyond that set

This means `WETH.release.json` is not "only prefunded keys" from `prefunded-pk.txt`.

It aligns with:

- `prefunded_agents.release.json`
- one replayed Uniswap pool

## Uniswap findings so far

### Confirmed live pool identity

The live chain has a pool at:

- `0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640`

Live calls show:

- `token0()` = `USDC` at `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- `token1()` = `WETH` at `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`
- `liquidity()` is nonzero

So the replayed USDC/WETH pool is present live and active.

### Current live pool balances

At the time of checking, the pool held approximately:

- `51,984.280215301395863585 WETH`
- `38,498,579.91491 USDC`

### LP ownership / withdrawal path

We checked the canonical Uniswap V3 management addresses on the live chain:

- `NonfungiblePositionManager` at `0xC36442b4a4522E871399CD717aBDD847Ab11FE88`
- `Factory` at `0x1F98431c8aD98523631AE4a59f267346ea31F984`

Both returned `0x` code on the live chain.

Additional live-chain evidence:

- `SwapRouter.factory()` returns `0x1F98431c8aD98523631AE4a59f267346ea31F984`
- `UniswapV3Pool.factory()` also returns `0x1F98431c8aD98523631AE4a59f267346ea31F984`
- there is no obvious `positionManager()`-style view on the pool or router that points at `0xC364...FE88`
- scanning all Ritual blocks found **no** `Mint` events for this pool
- recent pool logs are `Swap` events, not `Mint`, `Burn`, or `Collect`

Additional genesis-state evidence:

- the replay file's pool entry only seeds 4 storage slots
- one hashed slot matches `tickBitmap[77]`
- a candidate `positions` mapping slot probe returns zero
- so the replay snapshot appears to seed a minimal swap-capable pool shell, not an obvious on-chain LP ownership record

Current conclusion:

- the usual canonical Uniswap V3 NFT-position ownership path does not appear to exist on Ritual for this pool
- the live pool appears to have been seeded directly from genesis state, not minted on Ritual through the standard V3 flow
- that makes normal LP withdrawal via the canonical position manager very unlikely

This is still **not a formal proof that no custom withdrawal path exists anywhere**, but it is now stronger than the earlier hypothesis. We did not find any standard on-chain path that could point to a live LP NFT manager or owner.

## Pre-funded account documentation sources

The documented sources for prefunded accounts are:

- `ritual-node-internal/resources/el/README.md`
  - explains `prefunded_agents.dev.json`
  - explains `prefunded_agents.release.json`
  - explains the matching agent key files

The loader path is:

- `ritual-node-internal/configgen/el_genesis.py`

That file:

- derives funded ETH accounts from `prefunded-pk.txt`
- loads environment-specific JSON resources such as:
  - `prefunded_agents.release.json`
  - `WETH.release.json`
  - `RitualWallet.release.json`

## `uniswap_replayed.json` funded addresses audit

`uniswap_replayed.json` contains 18 top-level accounts. The funded entries are not just the Uniswap pool.

### Important correction

The huge ETH balance on `0xe08d9c...b902` is **not** evidence that we copied that wallet's real Ethereum balance into genesis.

The replay script at `traffic-gen-internal/scripts/replay_tx.sh` explicitly does:

- `anvil_impersonateAccount "${FROM}"`
- `anvil_setBalance "${FROM}" ...`

before replaying the chosen Ethereum transaction and dumping state.

So the replay process itself artificially prefunds the transaction sender inside Anvil, and that prefunded balance then ends up in the dumped genesis state.

### What the replayed transaction actually was

The default replay tx is:

- `0x16043b99b8ee8808c6067b15013ab4b723d617207458eea2f38f39ec1d126d95`

Live Ethereum tx data shows:

- `from = 0xe08d9cc9b651cb95de82562a3642afe7c7cdb902`
- `to = 0xdef1c0ded9bec7f1a1670819833240f027b25eff`

That means the replay is a real user EOA calling the labeled `0x: Exchange Proxy`, not a minimal "just Uniswap pool" state import.

The route also touches:

- `0xE592...1564` (`Uniswap V3: Router`)
- `0x88e6...5640` (the replayed Uniswap V3 pool)
- `0xC02a...6Cc2` (`WETH`)
- `0xA0b8...6eB48` (`USDC`)
- `0x5C5b...8326` (`Elixir Protocol: sdeUSD Token`)
- several 0x helper contracts such as `0x22f9...8c18` (`0x: Exchange Proxy Flash Wallet`)

So the imported state is a bundle of accounts touched by a specific 0x-routed Ethereum trade, not a narrowly curated Uniswap-only snapshot.

### Funded entries worth calling out

- `0xe08d9c...b902`
  - Etherscan shows an unlabeled address page / authority-style EOA page
  - this is the **sender** of the replayed Ethereum tx
  - it has no code in `uniswap_replayed.json`
  - the enormous ETH balance in the replay file comes from the replay script's `anvil_setBalance`
  - this is the most concerning imported address, because if that same private key holder exists, they could control that Ritual-chain balance

- `0xdef1c0...5eff`
  - labeled on Etherscan as `0x: Exchange Proxy`
  - contract
  - only a small ETH balance (`~0.0326 ETH`) in the replay file
  - this looks like expected infrastructure from the 0x-routed swap path

- `0xC02a...6Cc2`
  - `WETH` contract
  - contract
  - native ETH backing balance of about `2,933,842.9471 ETH` in the replay file
  - expected as part of WETH state, though Ritual later overrides WETH storage with the environment-specific `WETH.release.json` / `WETH.dev.json`

- `0x000000...0000`
  - zero address
  - about `14,056.3991 ETH`
  - notable as imported balance, but not a normal spendable user account

### Current conclusion

The replay import is **not** simply "fund some random Ethereum accounts that happened to exist."

It is more specific:

- replay one chosen Ethereum trade on an Anvil fork
- artificially top up the sender so the replay succeeds
- dump every touched account into genesis

That still means `uniswap_replayed.json` can introduce funded accounts beyond the intended Uniswap pool, including a real external EOA sender address. The biggest concrete issue is the replay sender `0xe08d...b902`, whose huge balance appears to be created by the replay script itself.

## Why the new script is safer

We added a replacement extractor at:

- `traffic-gen-internal/scripts/replay_safe_uniswap_state.py`

Why it is safer than `traffic-gen-internal/scripts/replay_tx.sh`:

### 1. Real user ownership risk

Old problem: a real user account is funded because the old script takes touched state from the EOA of a real Ethereum transaction.

Now: the new script creates a fresh ephemeral sender only on the local fork and zeros its balance in the final state file.

### 2. Replay-script-funded EOA risk

Old problem: the old script uses `anvil_setBalance` on the replay sender, so an artificially funded EOA can leak into genesis.

Now: the new script funds only a fork-local ephemeral sender and removes that sender from the exported state.

### 3. Overbroad imported state risk

Old problem: the old script replays a 0x-routed trade, so it imports extra touched contracts and accounts that are not part of the minimal swap path.

Now: the new script performs a direct `Uniswap V3 SwapRouter.exactInputSingle` swap for `WETH -> USDC`, so the exported state stays much narrower.

### 4. Minimal-state auditability

Old problem: the old dump kept every touched account, which made the final allocation larger and harder to audit.

Now: the sanitizer keeps only swap-supporting contracts plus one sink account, reducing the tested output to 6 kept accounts.

### 5. Swap recipient ownership risk

Old problem: if swap output lands at a normal address, someone may have a claim on those assets, and the literal zero address is not a reliable ERC20 recipient.

Now: the new script sends swap output to a contract-created sink address with empty runtime code and no normal user key path.

### 6. Fork-local dev account leakage

Old problem: Anvil default dev accounts can leak into the dump and accidentally become part of Ritual genesis.

Now: the new script explicitly drops local Anvil dev accounts from the exported state.

### Bottom line

- no real user sender account is imported
- no replay-script-funded EOA survives into the output

## Remaining open questions

- confirm whether the live chain came specifically from a `chain-deployment-infra` release deployment
- trace whether the replayed Uniswap liquidity has any nonstandard ownership/control path on this chain
- determine whether the replay sender `0xe08d...b902` is acceptable to leave funded on Ritual or should be removed/replaced during genesis generation

## Repro commands

These are the commands used to reproduce the findings so far.

### Basic live chain identification

```bash
cast chain-id --rpc-url https://rpc.ritualfoundation.org
cast block-number --rpc-url https://rpc.ritualfoundation.org
```

Recent output:

- chain ID: `1979`
- block: `8364734`

### Confirm `release` via a release-only prefunded agent

Release-only agent checked:

- `0xE305d3C3A62c14605221bbd669957446851C95B0`

```bash
cast balance 0xE305d3C3A62c14605221bbd669957446851C95B0 --rpc-url https://rpc.ritualfoundation.org
cast call 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 "balanceOf(address)(uint256)" 0xE305d3C3A62c14605221bbd669957446851C95B0 --rpc-url https://rpc.ritualfoundation.org
```

Recent output:

- ETH: `19999999994152514757153919`
- WETH: `10000000000000000905969664`

### Confirm release WETH holder set against prefunded agents

```bash
python3 - <<'PY'
import json, subprocess
from pathlib import Path
root = Path('/home/ritual/repos/ritual-node-internal/resources/el')
with open(root/'WETH.release.json') as f: weth = json.load(f)
with open(root/'prefunded_agents.release.json') as f: pref = json.load(f)
state = next(iter(weth.values()))
pool='0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640'
matched=[]
for a in list(pref.keys()) + [pool]:
    idx = subprocess.check_output(['cast','index','address',a,'3'], text=True).strip()
    v = state['storage'].get(idx)
    if v and int(v,16)>0:
        matched.append(a)
print('prefunded_agents_release_count', len(pref))
print('matched_prefunded_plus_pool', len(matched))
print('pool_in_weth_release', pool in matched)
print('total_storage_slots', len(state['storage']))
print('derived_balance_entries_estimate', len(state['storage']) - 4)
PY
```

Recent output:

- `prefunded_agents_release_count 8000`
- `matched_prefunded_plus_pool 8001`
- `pool_in_weth_release True`
- `total_storage_slots 8005`
- `derived_balance_entries_estimate 8001`

### Live Uniswap checks

```bash
cast call 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 "token0()(address)" --rpc-url https://rpc.ritualfoundation.org
cast call 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 "token1()(address)" --rpc-url https://rpc.ritualfoundation.org
cast call 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 "liquidity()(uint128)" --rpc-url https://rpc.ritualfoundation.org
cast call 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 "balanceOf(address)(uint256)" 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --rpc-url https://rpc.ritualfoundation.org
cast call 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 "balanceOf(address)(uint256)" 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --rpc-url https://rpc.ritualfoundation.org
cast code 0xC36442b4a4522E871399CD717aBDD847Ab11FE88 --rpc-url https://rpc.ritualfoundation.org
cast code 0x1F98431c8aD98523631AE4a59f267346ea31F984 --rpc-url https://rpc.ritualfoundation.org
```

Recent output:

- `token0`: `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`
- `token1`: `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`
- liquidity: `11958707625084316458`
- pool WETH balance: `51984498809745425659551`
- pool USDC balance: `38498125458109`
- `NonfungiblePositionManager` code: `0x`
- canonical factory code: `0x`
