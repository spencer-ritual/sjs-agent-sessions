# Why The Reth Merge Is Hard

Date: 2026-05-05

## Context

This note records why directly merging upstream Reth `v2.2.0` into `ritual-reth-internal` is hard, based on the live merge probe in `/home/ritual/repos/ritual-reth-merge-probe`.

The probe merged upstream commit `88505c7fcbfdebfd3b56d88c86b62e950043c6c4` into the Ritual branch `spencer/2605-reth-upstream-merge-probe`.

The important conclusion is not "do not merge." The better conclusion is: a merge can be useful because it keeps the old Ritual code physically present, but the resolution has to be a behavior port into upstream `v2.2.0` architecture rather than ordinary conflict-marker cleanup.

## Probe Shape

- The merge produced `266` unmerged paths.
- The unmerged index contained `188` normal content conflicts, `75` modify/delete conflicts, and `3` files added inside a directory that upstream renamed.
- Large conflict clusters appeared in `rpc`, `storage`, `net`, `optimism`, `ethereum`, `transaction-pool`, `trie`, `node`, and `stages`.
- The dependency repos appear to have relevant checkpoint work already: Alloy, revm, Alloy EVM, and revm-inspectors are on the same upstream-merge branch family with upstream merge commits plus Ritual follow-up fixes.

## Main Reasons The Merge Is Hard

### 1. Upstream moved architecture, not just nearby lines

Many conflicts are not simple edits to the same function. Upstream Reth changed core API shapes and ownership boundaries since Ritual diverged. The node builder path is the clearest example, and the difficulty is deeper than "call A before B."

Ritual's old builder path added `build_evm_with_pool` so EVM/block-verification construction could depend on an already-built transaction pool. That gave Ritual's verifier and execution wiring access to pool state, provider state, and EVM configuration at the same construction point.

Upstream `v2.2.0` reverses that dependency direction:

- The executor builder produces an EVM config by itself.
- The pool builder receives that EVM config.
- The payload service receives the same EVM config and the pool.
- Engine/tree validation, RPC, and payload building are wired through newer builder/add-on traits.

So the hard question is not "where did this code move?" It is "which current upstream component is now allowed to own behavior that used to be assembled at one custom Ritual hook?"

Preserving `build_evm_with_pool` mechanically would likely mean carrying forward an obsolete local extension point. Removing it means splitting the old behavior across current upstream hooks: some belongs in the EVM config, some in payload building, some in txpool policy, some in engine/tree validation, and some in RPC/add-on registration. That split is why the conflict is materially hard even though the surface description sounds like a small ordering change.

### 2. Some Ritual-heavy files were deleted or replaced upstream

The most important example is `crates/ethereum/primitives/src/transaction.rs`.

Ritual's old file contains custom transaction behavior for scheduled, async commitment, async settlement, passkey, SPC metadata, encoding, recovery, and Reth conversions. Upstream `v2.2.0` deleted that file and now aliases Ethereum transaction types through Alloy.

Because `ritual-alloy-internal` already has upstream `v2.0.4` merge work and Ritual transaction fixes, the right resolution is probably not to resurrect the old Reth file. The merge is hard because the old code is valuable evidence, but the destination is no longer the same file.

### 3. The biggest conflicts sit on consensus-sensitive behavior

The hard conflicts are in exactly the places where losing a detail is dangerous:

- transaction identity and storage codecs
- EVM config and precompile dispatch
- async context and SPC capture
- payload building and transaction ordering
- scheduled obligations and heartbeat revival
- txpool sender locks, expiry, and custom subpools
- block verification and engine validation
- RPC submission, validation, and result delivery

These are not cosmetic conflicts. A compile-only resolution could silently drop consensus, persistence, or product behavior.

### 4. The payload builder conflict is a full control-flow conflict

`crates/ethereum/payload/src/lib.rs` is especially difficult. Ritual's side contains a large multi-phase builder flow: scheduled hydration, heartbeat/revival, async detection, commitment insertion, fulfilled replay, delivery settlement, sequencing rights, caps/demotion, and trace instrumentation.

Upstream's side has the current `v2.2.0` default payload loop, new transaction execution result plumbing, sparse trie hooks, BAL/Amsterdam handling, and current `BuildOutcome` flow.

Resolving this file by keeping the old Ritual body would likely miss upstream's new payload semantics. Resolving it by taking upstream would drop core Ritual behavior. It needs a deliberate port.

### 5. There is a large amount of upstream-only churn around the real Ritual changes

The conflict set includes broad storage, trie, network, stages, optimism, examples, and provider changes. Many of these are likely upstream evolution rather than Ritual product behavior.

This creates noise and review burden. The hard part is separating:

- conflicts that preserve actual Ritual invariants
- conflicts that are upstream internals and should mostly take upstream
- conflicts that only exist because local changes were attached to old upstream file layout

Without that triage, an agent can spend a lot of time hand-merging upstream internals and still miss the important Ritual behavior.

### 6. The merge can preserve information, but it can also preserve obsolete structure

The strongest argument for doing a merge is real: the old Ritual code remains visible in the conflicted files, so there is less chance of losing behavior during a clean-room reimplementation.

The counter-risk is also real: if conflict resolution is treated as "make this old code compile," the result can carry forward APIs and module boundaries that upstream intentionally replaced.

The merge is therefore useful as an information-preserving port surface, not as a mechanical strategy.

## Practical Implication

The feasible strategy is a hybrid:

1. Keep upstream `v2.2.0` architecture by default.
2. Use the conflicted Ritual code as the invariant source.
3. Port Ritual behavior into current upstream extension points.
4. Prefer upstream for broad storage, net, trie, stages, optimism, and example churn unless a concrete Ritual invariant is present.
5. Resolve in batches around behavior surfaces, not file counts.

The first useful batch should focus on the Reth integration skeleton: node builder, EVM config propagation, payload builder entry points, engine/tree validation hooks, and RPC/add-on registration. The large feature ports should only proceed once that skeleton makes clear where Ritual behavior now belongs.
