# Upstream Merge Principles

Use this as the agent context for large fork/upstream merges.

## Goal

Merge upstream improvements while preserving Ritual product behavior. Prefer the current upstream architecture as the base when upstream has moved files, APIs, or ownership boundaries substantially.

## Merge Policy

1. Prefer upstream file layout and architecture.
2. Preserve fork product behavior.
3. Do not reintroduce upstream-deleted files without justification.
4. Move fork logic into the new upstream location rather than keeping legacy paths.
5. Keep each batch focused.
6. Use cheap checks per batch; run full tests only at checkpoints.
7. Document uncertain resolutions in `MERGE_NOTES.md`.

## Core Rule

Do not treat conflict-marker cleanup as the merge. Treat the merge as a behavior port.

For every batch, identify:

- Upstream shape to keep.
- Ritual behavior/invariants to preserve.
- New upstream extension point where each invariant belongs.
- Focused validation proving the port still works.

## Strategy

- Use direct conflict resolution only when conflicts are small, localized, and still in the same architectural shape.
- Use port-on-clean-upstream when upstream deleted, moved, or reorganized the files that Ritual modified.
- When both upstream churn and Ritual behavior are complex, start from clean upstream and port from an explicit invariant checklist.
- Preserve upstream performance and structure by default; do not drag old local scaffolding forward unless it still has a clear purpose.
- Preserve Ritual product behavior by semantics, not by old file layout.
- When upstream moved a subsystem, move Ritual behavior into the new upstream location unless there is a concrete reason to keep a legacy module.

## Agent Batch Loop

Each agent batch should be small enough to review but large enough to compile a meaningful slice.

1. Pick one subsystem or conflict cluster.
2. Read upstream version, fork version, and nearby tests.
3. Write a short invariant checklist before editing.
4. Apply the port or conflict resolution.
5. Run cheap scoped checks for that batch.
6. Commit or checkpoint only after the batch is coherent.
7. Record unresolved questions, uncertain resolutions, and skipped validations in `MERGE_NOTES.md`.

Avoid mixing unrelated subsystems in one batch.

## Implementation Learnings

- When upstream deletes a crate or subsystem, verify the target upstream dependency graph and downstream Ritual manifests before preserving it. If the target stack no longer references it, accepting the deletion is often the cleaner port; record the downstream audit in `MERGE_NOTES.md` instead of carrying a legacy wrapper forward.
- Treat explicit gas limits, sender/caller identity, transaction hash propagation, and SPC metadata as behavior, not plumbing. A compile-friendly TODO that makes those values advisory is not a clean checkpoint.
- Empty directories left behind by deleted workspace members can still break Cargo workspace discovery through glob members such as `crates/*`; remove the directory shell before trusting `cargo fmt` or `cargo check`.
- A dependency repo checkpoint should not stop at conflict resolution. At minimum, it should prove no unresolved merge paths remain, run `git diff --check`, run package formatting, and run the narrowest package check that exercises sibling dependency resolution.
- For transaction libraries, review trait/wrapper forwarding after conflict resolution. Concrete structs can preserve Ritual fields while downstream consumers still lose them through wrappers such as `Signed<T>`, sealed values, typed envelopes, generated macros, or RPC adapter structs.
- Keep wire/storage encoding and signing/hash preimages explicit when runtime metadata exists. Runtime `SPC` or async metadata may need to round-trip on the wire while remaining excluded from transaction hash/signature preimages; do not use one generic RLP helper for both paths unless tests prove that is intended.
- Treat optional adapter fields as data-loss risks. Beacon/engine payload attributes, txpool detail structs, and transaction request builders can silently drop or misclassify Ritual behavior without breaking compilation, so add round-trip or explicit-inference tests for these adapters at the dependency-repo checkpoint.

## Validation Cadence

Do not run full tests after every small edit.

- After each batch: run formatting, targeted compile/checks, and focused tests if they exist.
- After each subsystem: run broader package/workspace checks covering that subsystem and its dependents.
- After dependency repos land: run cross-repo integration builds.
- At the end: run full tests, image build, localnet, and publish-path verification as applicable.

If a check is too expensive, state why it was skipped and what later gate will cover it.

## Guardrails

- Never silently drop Ritual behavior. If behavior cannot be mapped, stop and ask.
- Never preserve old code solely because it resolves a conflict.
- Never reintroduce an upstream-deleted file solely to avoid moving Ritual logic into the new upstream structure.
- Prefer upstream APIs, module boundaries, and data flow over compatibility shims.
- Keep compatibility only for shipped interfaces, persisted data, wire formats, and consensus behavior.
- Be extra conservative around consensus, gas/accounting, transaction encoding, precompiles, async execution, RPC compatibility, and storage formats.
- Keep a running list of invariants, tests run, tests skipped, and follow-up risks.

## Review Standard

A finished batch should answer:

- What upstream structure did we keep?
- What Ritual behavior did we port?
- What evidence says the port is correct?
- What risks remain for a later integration gate?

## Questions For Self

- What should count as sufficient agent verification when important behavior is only covered by end-to-end tests?
- How can we extract a practical spec from existing fork behavior before porting it?
- Would an FSM-style spec help keep agents aligned for stateful behavior such as transaction flow, async execution, precompiles, RPC, and localnet lifecycle?
- What checklist or trace method reduces the chance that agents miss behavior hidden in old code paths?
- How should each batch distinguish "not tested yet" from "not expected to matter"?

