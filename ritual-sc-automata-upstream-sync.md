# Ritual SC Automata Upstream Sync

## Objective

Bring the private Automata submodules in `ritual-sc-internal` forward to the latest upstream-based stack, make the dependent `flashtestations` code compatible with the new DCAP output/type changes, and get the top-level local workflow working again.

The immediate operational goal is:

- `dev` should continue to point at the old working submodule stack
- `spencer/2604-automata-upstream` should point at the new submodule stack
- switching branches should restore the corresponding submodule commits via the checkout hook
- `make dump-state-anvil` should run successfully on the new stack

## Repos Involved

- `ritual-sc-internal`
- `ritual-sc-internal/lib/flashtestations`
- `ritual-sc-internal/lib/flashtestations/lib/automata-dcap-attestation`
- `ritual-sc-internal/lib/flashtestations/lib/automata-dcap-attestation/evm/lib/automata-on-chain-pccs`

## Branches

- top-level `ritual-sc-internal`: `spencer/2604-automata-upstream`
- `flashtestations`: `spencer/2604-upstream-merge`
- `automata-dcap-attestation`: `spencer/2604-upstream-merge`
- nested PCCS branch was previously aligned to the merged private fork state and is currently pinned by gitlink

## Important Commits

### New stack currently pinned by `spencer/2604-automata-upstream`

- `ritual-sc-internal`: `2f4d96a`
- `flashtestations`: `e815122`
- `automata-dcap-attestation`: `7aafa11`
- `automata-on-chain-pccs`: `f0f7100`

### Purpose of those commits

- `7aafa11` in DCAP restores a compatibility `V4Structs.sol` file so downstream Ritual code still compiles against the old import path.
- `e815122` in `flashtestations` updates `QuoteParser` so it accepts both:
  - legacy DCAP verifier output layout
  - newer quoteBodyType-based DCAP output layout
- `2f4d96a` in `ritual-sc-internal` updates the `lib/flashtestations` gitlink to point at the new `flashtestations` commit.

## What Changed

### In `automata-dcap-attestation`

Added:

- `evm/contracts/types/V4Structs.sol`

Reason:

- upstream removed the old path used by Ritual-side imports
- downstream code still expected `automata-dcap-attestation/contracts/types/V4Structs.sol`
- this was a compile-time compatibility shim

### In `flashtestations`

Updated:

- `src/utils/QuoteParser.sol`

Reason:

- old parser assumed the serialized verifier output layout was:
  - `quoteVersion (2) + tee (4) + tcbStatus (1) + fmspc (6) + quoteBody`
- new upstream DCAP output layout is:
  - `quoteVersion (2) + quoteBodyType (2) + tcbStatus (1) + fmspc (6) + quoteBody`
- the parser now detects which layout it is reading and extracts the TD10 report body correctly in both cases

### In `ritual-sc-internal`

Updated:

- `lib/flashtestations` gitlink

Reason:

- branch checkout should move between old and new submodule states automatically

## What Was Verified

### Verified as working

- top-level `forge build` in `ritual-sc-internal` succeeds on the new stack
- branch checkout hook correctly syncs submodules on checkout
- current pinned submodule state on `spencer/2604-automata-upstream` is:
  - `lib/flashtestations` -> `e815122`
  - `lib/flashtestations/lib/automata-dcap-attestation` -> `7aafa11`
  - nested PCCS -> `f0f7100`

### Verified by user observation

- `dev` branch behavior is working with the old submodule setup

## Current Blocker

The remaining issue is **not** the quote parsing change in `flashtestations`.

The current blocker is in:

- `scripts/genesis-deployment/deploy.sh`

The failure is:

- `Failed to extract RITUAL_WALLET_IMPL_ADDR from deployment output`

This happens during `make dump-state-anvil`.

## Why This Looks Unrelated To Quote Parsing

The failure occurs after deployment orchestration in the shell wrapper, not in the TEE quote registration flow.

The `QuoteParser` change is only relevant when `FlashtestationRegistry` calls:

- `attestationContract.verifyAndAttestOnChain(rawQuote)`
- then `QuoteParser.parseV4VerifierOutput(output)`

That is the quote-registration path, not the genesis deployment output parsing path.

## Current Hypothesis

`deploy.sh` is brittle because it scrapes `forge script` stdout for addresses like:

- `RitualWallet implementation deployed:`
- `Scheduler implementation deployed:`
- etc.

If the `forge script` output format changes, or if `console.log` lines are not emitted in the expected way, the wrapper fails even if deployment itself succeeded.

This is consistent with the observed error:

- deploy script reports success
- wrapper then fails while extracting addresses from text output

## Best Next Fix

Replace stdout scraping with a machine-readable handoff.

Preferred direction:

1. update `scripts/genesis-deployment/Deploy.s.sol` to write a fresh address manifest for the current run
2. update `scripts/genesis-deployment/deploy.sh` to read that manifest instead of parsing console text
3. rerun `make dump-state-anvil`

This is more robust than:

- scraping `forge script` logs
- reading stale `states/*.json`
- depending on terminal output formatting

## Current Working Tree Notes

On `spencer/2604-automata-upstream`, the repo may contain many modified `states/*.json` files from previous `dump-state-anvil` attempts. These are run artifacts and should not be casually reverted without checking whether the user wants to keep or discard them.

## Commands / Facts Worth Remembering

Current top-level branch:

- `spencer/2604-automata-upstream`

Current pinned submodules:

- `lib/flashtestations` -> `e815122`
- `lib/flashtestations/lib/automata-dcap-attestation` -> `7aafa11`
- `lib/flashtestations/lib/automata-dcap-attestation/evm/lib/automata-on-chain-pccs` -> `f0f7100`

Known failing command:

- `make dump-state-anvil`

Observed failure text:

- `Failed to extract RITUAL_WALLET_IMPL_ADDR from deployment output`

## Summary

The upstream Automata integration work has already been landed into the submodules and wired into `ritual-sc-internal`.

The remaining task is to harden the genesis deployment wrapper so the new branch can complete `make dump-state-anvil` without relying on fragile stdout parsing.
