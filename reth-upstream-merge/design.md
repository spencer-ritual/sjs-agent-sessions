# Upstream Merge Dependency Repos

Date: 2026-05-05

## Context

`ritual-reth-internal` does not use `.gitmodules`, `vendor/`, or a `patches/` directory for the Alloy/revm-style dependencies checked here. The active coupling is through root `Cargo.toml` workspace dependencies that point at sibling repos with `../` paths.

`ritual-reth-nodebuilder-internal` is a real member of the merge working set, not just a downstream smoke-test repo. Its root `Cargo.toml` points at `ritual-reth-internal`, `ritual-revm-internal`, `ritual-revm-inspectors-internal`, `ritual-alloy-internal`, and `ritual-alloy-evm-internal`; its `Makefile` builds the execution-layer image as `ritualnetwork/ritual-reth-internal` with a tag composed from both the Reth and nodebuilder commits.

`ritual-node-internal` is not a Cargo sibling dependency of nodebuilder, but it is the orchestration and verification repo for local networks and image publication. Its `Makefile` runs `make -C ../ritual-reth-nodebuilder-internal build-slim`, and its repo-management scripts include the same Reth/nodebuilder/revm/Alloy repos.

The relevant local repos currently have only `origin` configured, pointing at Ritual forks:


| Local repo                         | Current branch | Current HEAD | Origin                                                           | Upstream source represented                      |
| ---------------------------------- | -------------- | ------------ | ---------------------------------------------------------------- | ------------------------------------------------ |
| `ritual-reth-internal`             | `dev`          | `851b51500`  | `git@github.com:ritual-net/ritual-reth-internal.git`             | `https://github.com/paradigmxyz/reth`            |
| `ritual-reth-nodebuilder-internal` | `dev`          | `44fa75a`    | `git@github.com:ritual-net/ritual-reth-nodebuilder-internal.git` | Ritual integration repo over Reth                |
| `ritual-alloy-internal`            | `dev`          | `d265f1f4`   | `git@github.com:ritual-net/ritual-alloy-internal.git`            | `https://github.com/alloy-rs/alloy`              |
| `ritual-alloy-evm-internal`        | `dev`          | `d531136`    | `git@github.com:ritual-net/ritual-alloy-evm-internal.git`        | `https://github.com/alloy-rs/evm`                |
| `ritual-revm-internal`             | `dev`          | `b274a85a`   | `git@github.com:ritual-net/ritual-revm-internal.git`             | `https://github.com/bluealloy/revm`              |
| `ritual-revm-inspectors-internal`  | `dev`          | `0b81109`    | `git@github.com:ritual-net/ritual-revm-inspectors-internal.git`  | `https://github.com/paradigmxyz/revm-inspectors` |
| `ritual-node-internal`             | `dev`          | `63974f5`    | `git@github.com:ritual-net/ritual-node-internal.git`             | Localnet orchestration / verification            |


## Target Upstream Commits

The upstream merge target is Reth `v2.2.0`. The release-compatible dependency versions are:

- `revm`: `38.0.0`
- `alloy-*`: `2.0.4`
- `alloy-evm`: `0.34.0`
- `revm-inspectors`: `0.39.0`

Resolved commit targets:


| Ritual repo                        | Upstream repo                 | Upstream tag/version   | Tag object                                 | Commit to merge                                                                              |
| ---------------------------------- | ----------------------------- | ---------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------- |
| `ritual-reth-internal`             | `paradigmxyz/reth`            | `v2.2.0`               | direct commit                              | `88505c7fcbfdebfd3b56d88c86b62e950043c6c4`                                                   |
| `ritual-alloy-internal`            | `alloy-rs/alloy`              | `v2.0.4`               | `1e57a4bd5cad7b68d0ca4cd4ce2e6f81cf718956` | `f3fe4cfff0553e9e234a53208bb69b7c222c66e5`                                                   |
| `ritual-alloy-evm-internal`        | `alloy-rs/evm`                | `v0.34.0`              | `5848da68c37cb52f2bf677593b2a2f0799c07924` | `6022e02ee1ab669f7c1ee59b58fc7a6b3f5f15d5`                                                   |
| `ritual-revm-internal`             | `bluealloy/revm`              | `v107` / `revm 38.0.0` | direct commit                              | `d62933180e442319a93991fe4070dbeb466ef222`                                                   |
| `ritual-revm-inspectors-internal`  | `paradigmxyz/revm-inspectors` | `v0.39.0`              | `1741db702e5a798530e2bbdac94692eebd104009` | `10173a3f957c948ced52c8e54a396a445d13cd16`                                                   |
| `ritual-reth-nodebuilder-internal` | none public upstream found    | N/A                    | N/A                                        | no upstream merge commit; update on top of current Ritual branch after dependency repos land |
| `ritual-node-internal`             | none public upstream needed   | N/A                    | N/A                                        | no upstream merge commit; use for verification unless localnet/image scripts need changes    |


Evidence:

- Reth `v2.2.0` tag resolves directly to commit `88505c7fcbfdebfd3b56d88c86b62e950043c6c4`.
- `alloy-rs/alloy` tag `v2.0.4` is an annotated tag that peels to commit `f3fe4cfff0553e9e234a53208bb69b7c222c66e5`.
- `alloy-rs/evm` tag `v0.34.0` is an annotated tag that peels to commit `6022e02ee1ab669f7c1ee59b58fc7a6b3f5f15d5`.
- `bluealloy/revm` release `v107` is named `tag v107 revm v38.0.0` and resolves to commit `d62933180e442319a93991fe4070dbeb466ef222`.
- `paradigmxyz/revm-inspectors` tag `v0.39.0` is an annotated tag that peels to commit `10173a3f957c948ced52c8e54a396a445d13cd16`.
- `paradigmxyz/reth` `Cargo.toml` at `v2.2.0` declares `revm = "38.0.0"`, `revm-inspectors = "0.39.0"`, `alloy-evm = "0.34.0"`, and the local forked Alloy workspace crates at `2.0.4`.

## What “done” means (behavior bar)

This section is the merge **completeness bar** for Ritual behavior when comparing the old downstream fork to the `v2.2.0` port. It is **orthogonal** to dependency/repo layout above.

- **Not sufficient:** selected scheduled (or other) traffic workloads are **green**. That only exercises **happy paths** and does not prove **negative cases**, **edge transitions**, or **failure-mode parity**.

- **Not required:** **byte-for-byte** parity with downstream files. The port may **refactor** wiring (for example **node builder**, **payload builder**, pool versus canonical hooks) as long as observables match.

- **Required:** **behavioral equivalence** expressed as the **same effective FSM** wherever Ritual logic is stateful: **same states, transitions, guards, and outputs** (including **errors, rejections, and ordering constraints**) over the **full behavioral surface** that downstream exposed—not only workloads already run in traffic-gen.

Coverage mapping and review should treat **missing downstream behavior in the port** as the **highest-severity** gap. Finer atom labels (`structural_equivalent`, `intentionally_absent`, `moved_to_dependency`) answer **why** something is not `exact` or `missing`; they do **not** replace the core questions: **Is behavior missing? Why? Is that acceptable?**

## Design Plan

- Goal: define the repo working set for an upstream `ritual-reth-internal` merge before starting implementation-level merge steps.
- Main workstreams:
  - Treat `ritual-reth-internal` as the primary merge repo, with `paradigmxyz/reth` as the upstream source.
  - Treat `ritual-reth-nodebuilder-internal` as a required integration repo because it assembles the actual `ritual-node` binary/image using local Reth, revm, inspectors, Alloy, and Alloy EVM path dependencies.
  - Coordinate `ritual-revm-internal` because `ritual-reth-internal/Cargo.toml` points all core revm crates at `../ritual-revm-internal`, and `ritual-revm-internal/Cargo.toml` points `reth-evm` back at `../ritual-reth-internal/crates/evm`.
  - Coordinate `ritual-revm-inspectors-internal` because `ritual-reth-internal` points `revm-inspectors` at it, and it also depends on local Alloy and revm paths.
  - Coordinate `ritual-alloy-internal` because `ritual-reth-internal` points the major `alloy-*` workspace crates at it.
  - Coordinate `ritual-alloy-evm-internal` because `ritual-reth-internal` points `alloy-evm` at it, and that repo bridges Alloy plus revm APIs. Earlier local state also had `alloy-op-evm` in this repo, but the first `v0.34.0` checkpoint accepted upstream's deletion of `crates/op-evm`; downstream Reth/nodebuilder manifests should remove or remap any stale `alloy-op-evm` references rather than reintroducing that crate by default.
  - Use `ritual-node-internal` for final build, localnet, and publish-path verification; decide separately whether it needs merge changes or only test/config updates.
- Dependency tree and merge order:

```text
1. ritual-alloy-internal
   merge alloy-rs/alloy v2.0.4

2. ritual-revm-internal
   merge bluealloy/revm v107
   depends on: alloy

3a. ritual-alloy-evm-internal
    merge alloy-rs/evm v0.34.0
    depends on: alloy, revm

3b. ritual-revm-inspectors-internal
    merge revm-inspectors v0.39.0
    depends on: alloy, revm

4. ritual-reth-internal
   merge paradigmxyz/reth v2.2.0
   depends on: alloy, revm, alloy-evm, revm-inspectors

5. ritual-reth-nodebuilder-internal
   reconcile integration crate/image
   depends on: alloy, revm, alloy-evm, revm-inspectors, reth

6. ritual-node-internal
   localnet and publish-path verification
   depends on: nodebuilder image
```

- Dependency notes:
  - `ritual-reth-internal` pulls local revm, revm-inspectors, Alloy EVM, and Alloy crates through sibling `../` paths.
  - `ritual-reth-nodebuilder-internal` pulls local Reth, revm, revm-inspectors, Alloy, and Alloy EVM crates through sibling `../` paths and adds its own local `[patch.crates-io]` for `revm-handler`.
  - `ritual-node-internal` is not a Cargo dependency, but it builds/runs/publishes the nodebuilder execution-layer image and should verify the final integrated stack.
  - The target commit table above encodes the upstream repos and versions. Reth `v2.2.0`'s `Cargo.toml` encodes the version-only crate families that still need manifest/lockfile audit during the merge.
- Feature/traffic order: repo merge order is only the dependency floor. Once the dependency repos land, use `functionality-flow-traces.md` section `Dependency-Ordered Feature Verification Plan` for the Reth/nodebuilder feature port order and per-step gates.
- Dependency repo readiness gate before Reth/nodebuilder:
  - Treat a dependency repo as ready only after unmerged paths are gone, conflict markers are absent, manifest/lockfile resolution is coherent, scoped checks are recorded in repo-local `MERGE_NOTES.md`, and the merge is committed or otherwise clearly checkpointed for downstream consumers.
  - Before starting Reth/nodebuilder E2E, re-check that `ritual-reth-internal` and `ritual-reth-nodebuilder-internal` resolve Alloy, revm, Alloy EVM, and revm-inspectors from the intended sibling repos rather than stale crates.io versions.
  - `ritual-alloy-evm-internal` is the dependency bridge most likely to surface revm/Alloy drift; do not treat Reth/nodebuilder failures as primary Reth issues until this bridge repo has no unresolved merge state and has passed a scoped check.
- Risks and dependencies:
  - `ritual-reth-nodebuilder-internal` can surface API drift that does not appear when building `ritual-reth-internal` alone, especially around async-context features, custom precompiles, node components, and block verification.
  - `ritual-alloy-evm-internal` is likely to break early if either Alloy or revm APIs shift, because it bridges both.
  - `ritual-revm-inspectors-internal` should be updated after or alongside Alloy and revm rather than independently.
  - `op-revm` policy still needs a downstream audit. Initial local state was mixed: `ritual-reth-internal` and `ritual-reth-nodebuilder-internal` declared `op-revm = { version = "3.0.2" }`, while `ritual-alloy-evm-internal` pointed `op-revm` at `../ritual-revm-internal/crates/op-revm`. The `ritual-alloy-evm-internal` `v0.34.0` checkpoint accepted upstream Alloy EVM's removal of `crates/op-evm`; any remaining OP execution dependency should now be handled in Reth/revm/nodebuilder policy, not by keeping the old Alloy EVM OP wrapper.
  - `ritual-node-internal` should probably be included in the verification flow even if it does not receive merge commits, because localnet startup and publish scripts depend on the nodebuilder execution-layer image.
  - The commented-out `[patch.crates-io]` block in `ritual-reth-internal/Cargo.toml` is inactive but records prior pins for `alloy-rs/alloy`, `alloy-rs/op-alloy`, and `paradigmxyz/revm-inspectors`.

## Merge Probe Estimates

All upstream-backed merge probes were run in isolated temporary worktrees or clones, then aborted and cleaned up. These estimates measure textual merge conflicts and static integration surface; they do not include compile/test fallout after resolution.

### Implement-on-top vs Conflict Resolve Heuristics

Conflict volume is only a weak signal. The decision should mostly come from two axes: global upstream complexity and local Ritual complexity.

- Prefer conflict resolution when the upstream shape is still close to the local fork, conflicts are small and localized, and Git has preserved enough surrounding context that resolving markers keeps useful history without forcing old architecture forward.
- Prefer implement-on-top when upstream has substantially reorganized the relevant subsystem, deleted or moved files that Ritual modified, or changed the primary extension points so much that resolving conflicts would mostly mean adapting old code to APIs that no longer exist.
- Treat complex Ritual logic as a reason to hesitate before reimplementation, not as a reason to let conflict markers drive the design. Reimplementation can miss subtle behavior encoding through accumulated bug fixes
- Mitigate reimplementation risk by first inventorying Ritual invariants from the old branch, mapping each invariant to a new upstream extension point, writing or preserving focused tests/fixtures, and reviewing the port against that checklist rather than against the old file layout.
- If both global upstream churn and local Ritual complexity are high, use a hybrid: start from clean upstream structure, but port only after extracting the old behavior into an explicit invariant list. Avoid broad agent-driven rewrites without tests or a line-by-line invariant map.


| Repo                               | Probe result     | Conflict / rework estimate                                       | Recommended strategy                                     |
| ---------------------------------- | ---------------- | ---------------------------------------------------------------- | -------------------------------------------------------- |
| `ritual-alloy-internal`            | conflicted       | `19 / 511` tracked files, about `3.7%`                           | direct conflict resolution with semantic care            |
| `ritual-revm-internal`             | conflicted       | `37 / 1201` tracked files, about `3.1%`                          | direct conflict resolution with focused semantic ports   |
| `ritual-alloy-evm-internal`        | conflicted       | `10 / 60` tracked files, about `16.7%`                           | reimplementation / port on clean upstream head           |
| `ritual-revm-inspectors-internal`  | conflicted       | `2 / 285` tracked files, about `0.7%`                            | direct conflict resolution                               |
| `ritual-reth-internal`             | conflicted       | `266 / 1841` tracked files, about `14.4%`                        | reimplementation / port on clean upstream head           |
| `ritual-reth-nodebuilder-internal` | integration-only | about `40%` likely impact surface by static dependency/API usage | incremental reimplementation after dependency repos land |


`ritual-alloy-internal`:

- Decision: direct conflict resolution, with semantic care in the consensus transaction layer.
- Evidence: the merge conflicts in `19 / 511` tracked files, about `3.7%` of the repo. The conflicts are concentrated in `crates/consensus`, with follow-on conflicts in network and RPC transaction/payload adapters.
- Analysis: the conflict footprint is small and localized enough that a direct merge is more efficient than rebuilding the fork from scratch. The risky part is not file volume; it is preserving Ritual's scheduled, async, passkey, `SpcCall`, envelope, signing, and RPC builder behavior while adapting to upstream's transaction model changes.
- Checkpoint update 2026-05-05: first `v2.0.4` merge checkpoint was committed as `4f808053` on `spencer/2605-reth-upstream-merge`. The direct-conflict strategy was still appropriate, but the important lesson is that "compiles/tests pass" is not enough for Alloy: semantic audit found wrapper and adapter paths that could silently drop Ritual metadata. The checkpoint fixed and tested `Signed<T>` / `Sealed<T>` Ritual metadata forwarding, separated signed wire/storage RLP from hash/signing preimages for runtime fields, preserved beacon `PayloadAttributes.extra_data`, removed stale txpool `commit_block`, and made `TransactionRequest` inference honor explicit `0x10` / `0x11` / `0x12` / `0x77` types.
- Validation recorded for the checkpoint: `cargo +nightly fmt`, `git diff --check`, `cargo +nightly test -p alloy-consensus --lib`, `cargo +nightly test -p alloy-rpc-types-beacon --lib`, targeted `alloy-rpc-types-eth` custom-type inference test, `cargo +nightly check -p alloy-rpc-types-txpool --lib`, and focused RPC/network crate checks. Warnings remain in upstream/noise areas, but the scoped tests cover the Ritual-specific fixes.

`ritual-revm-internal`:

- Decision: direct conflict resolution, with focused semantic ports in core execution paths.
- Evidence: the merge conflicts in `37 / 1201` tracked files, about `3.1%` of the local HEAD file set. The conflicts are mostly in `crates/handler`, `crates/op-revm`, `crates/context`, `crates/precompile`, workspace manifests, and metadata.
- Analysis: the conflict set is small enough that resolving the merge preserves useful fork history and avoids unnecessary wholesale rewriting. The reason it still needs careful review is that the conflicted files are execution abstractions, so system transactions, scheduled/async transactions, async precompile behavior, and upstream handler/context/op-revm API changes must be treated as semantic ports rather than marker cleanup.

`ritual-alloy-evm-internal`:

- Decision: reimplement / port onto clean upstream `alloy-evm v0.34.0`.
- Evidence: the merge conflicts in only `10 / 60` tracked files, but those files are core execution files: EVM interfaces, transaction conversion, `spc_calls`, async-context behavior, gas/accounting, custom rewards, and OP EVM support.
- Analysis: the small file count is misleading because the conflicts sit on consensus-sensitive execution semantics. Mechanical conflict resolution would risk preserving old assumptions around EVM envs, transaction handling, and gas behavior. It is safer to start from upstream's new execution shape and deliberately reapply Ritual's custom behavior.
- Checkpoint update 2026-05-05: first `v0.34.0` merge checkpoint passed `cargo check -p alloy-evm` after porting Ritual async/SPC transaction conversion, async-context error propagation, explicit-gas system calls, and custom reward plumbing. The checkpoint accepted upstream's deletion of `crates/op-evm` after confirming target Reth `v2.2.0` does not reference `alloy-op-evm` or `op-revm`. Important process lesson: do not leave consensus-sensitive TODOs that weaken behavior during a checkpoint; `transact_system_call_with_gas_limit` initially mapped to upstream `system_call_with_caller`, but that made scheduled predicate gas limits advisory, so it had to be ported before treating the checkpoint as clean.

`ritual-revm-inspectors-internal`:

- Decision: direct conflict resolution.
- Evidence: the merge conflicts in `2 / 285` tracked files, about `0.7%` of the repo. The only conflicts were dependency policy in `Cargo.toml` and a localized `src/edge_cov.rs` conflict around `EdgeCovInspector` implementation changes.
- Analysis: this is the clearest case for resolving conflicts in place because the conflict footprint is tiny and localized. The remaining risk is downstream compatibility: final effort mostly depends on whether the updated internal Alloy/revm repos remain API-compatible with upstream inspector expectations.

`ritual-reth-internal`:

- Decision: reimplement / port onto clean upstream Reth `v2.2.0`.
- Evidence: the merge conflicts in `266 / 1841` tracked files, spread across RPC, storage, networking, optimism, ethereum, transaction pool, trie, node, stages, and root workspace files. The probe also found many files modified locally but deleted or moved upstream.
- Analysis: this is not a normal "same file, both sides edited nearby lines" merge. Upstream has reorganized large parts of the repo, while Ritual has local changes attached to the old layout. Resolving markers in place would bias the merge toward keeping old structures. Porting onto clean `v2.2.0` is more efficient because each Ritual invariant can be mapped to the current upstream architecture instead of dragging forward obsolete file and module shapes.

`ritual-reth-nodebuilder-internal`:

- Decision: incremental reimplementation after the dependency repos land.
- Evidence: there is no public upstream merge target. The first commit in `ritual-reth-nodebuilder-internal` was by arshan-ritual [arshan@ritual.net](mailto:arshan@ritual.net), early PR history points at an `upstream/v1.3.12` base rather than a formal GitHub fork, and static analysis found about `40%` likely impact surface across nodebuilder/EVM/payload/precompile integration code.
- Analysis: because there is no real upstream branch to merge, conflict resolution is the wrong model. The useful upstream source of truth is Reth `v2.2.0` itself: inspect how it wires node builder, EVM, payload, and precompile components now, then port Ritual's nodebuilder-specific hooks onto that API. This should reduce time spent preserving adapters that only made sense around the older Reth `v1.3.12` shape.

`ritual-node-internal`:

- Decision: verification-only unless localnet, image-build, or publish-path scripts need changes.
- Evidence: it has no upstream target in this merge set and was not merge-probed. Its role in the dependency analysis is orchestration: it builds/runs/publishes the nodebuilder execution-layer image rather than acting as a Cargo dependency.
- Analysis: changing this repo before the dependency and nodebuilder work lands would add noise without proving the core merge. The efficient path is to use it at the end for localnet, image-build, and publish-path validation, then make script/config changes only if that verification exposes breakage.

## Implementation Artifacts

- Phase 2 has started in `impl-plan.md`; keep it updated as dependency checkpoints and Reth/nodebuilder gates land.

## Ambiguities To Resolve

- Should upstream remotes be added locally for the five upstream-backed repos, or should comparisons use temporary fetch refs only?
- Is the mixed `op-revm` setup intentional, or should `ritual-reth-internal` also use `../ritual-revm-internal/crates/op-revm` for this merge?
- Should Alloy core and OP Alloy remain crates.io-only during the Reth/nodebuilder stages, or do we need Ritual forks if upstream API movement touches Ritual patches? For `ritual-alloy-evm-internal` specifically, `alloy-op-evm` should be considered deleted unless downstream audit proves an active consumer.
- Should `ritual-node-internal` get its own merge branch and PR in this effort, or should it remain verification-only unless localnet scripts/configs need updates?

