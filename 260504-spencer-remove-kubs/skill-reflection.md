# Skill Reflection: Docker Migration Live Acceptance

## Trigger

A K3s-to-Docker migration looked statically ready, but the first live Docker simulation exposed runtime-only failures: a missing Summit entrypoint bind mount, a stale forge upload that needed targeted child-process termination, a recoverability variable alias bug, and an SSH session that hung after a traffic-gen container was already running.

## Existing Gap

The workflow already encouraged static scans and generated-artifact checks, but it did not explicitly require runtime validation of generated Compose mount paths, child process recovery semantics, or bounded SSH behavior for remote Docker orchestration.

## Candidate Update

Target skill: New skill, likely `/home/ritual/.claude/skills/ritual-deploy-orchestration/SKILL.md`.

For large orchestration migrations, add a live acceptance checklist after static verification:

- Validate generated Compose files against the actual container command paths and required host artifacts.
- When a chain was previously stalled, verify long-running transaction uploaders by checking both on-chain state and child process liveness; terminate only stale child processes when wrapper retries exist.
- In SSH fan-out deployers, bound remote execution and verify remote desired state before classifying timeout as failure.
- Re-run from the smallest safe runner step after manual recovery rather than redoing already-successful cloud provisioning.

## Scope

Applies to future deployment-orchestration migrations, especially Kubernetes-to-Docker or SSH fan-out conversions. It is not a general rule for all coding tasks.

## Evidence

- `ritual-cl` containers failed with `cannot open /etc/ritual/chain-node/node-N/cl-entry.sh` until the generated file was bind-mounted.
- After CL recovery, `eth_blockNumber` advanced and the PCCS wrapper succeeded after the stale forge child was terminated and retried.
- `7_7_recoverability_deploy.sh` failed under `set -u` because it referenced `PROJECT_ID` instead of `GCP_PROJECT_ID`.
- A traffic-gen SSH command stayed open after the remote container was already running; adding a timeout and remote container/log-policy verification let the rerun complete.

Promotion status: Not promoted yet

## Trigger

During the K3s-to-Docker capability restoration, the user corrected the workflow: deleted recoverability, observability, and RPC proxy files needed to be restored with git commands first, then edited in place. This mattered because those files encoded behavior that a clean-room rewrite was likely to miss.

## Existing Gap

The implementation workflow covered preserving user changes and avoiding destructive git operations, but it did not explicitly say that when a user asks to restore deleted capability code, the first step should be a source-controlled restore from the known base branch before making adaptation edits.

## Candidate Update

Target skill: `/home/ritual/repos/.cursor/skills/castle-implementation/SKILL.md`.

For capability restoration work, add a small guard:

- Identify the source branch or commit that still contains the deleted files.
- Use `git restore --source=<branch-or-commit> -- <paths>` before editing.
- Treat untracked restored files as expected when current `HEAD` deleted them.
- Then adapt the restored implementation, preserving encoded logic unless a specific invariant requires replacement.

## Scope

Applies to migration and rollback tasks where deleted files contained domain behavior. It should not override normal implementation work for genuinely new features.

## Evidence

- The restored RPC proxy template contained method-specific rate limits that needed to be preserved.
- The restored recovery FSM contained cooldown, young-node, progress, pause, and bootstrap-from-EL invariants that would have been easy to omit in a rewrite.
- `git status --short` showed the restored deleted files as untracked because current `HEAD` no longer tracked them, even though they were restored via `git restore --source=origin/arshan/delta-fixes-and-validator-setup`.

Promotion status: Not promoted yet

## Trigger

While reviewing these reflection proposals, the user pointed out that `Candidate Update` sections should identify the skill file to change, or say that the proposal should become a new skill altogether.

## Existing Gap

The reflection format asked for a candidate update, but did not require the proposal to name its promotion target. That makes later promotion ambiguous because a reviewer has to infer whether the proposal belongs in an existing skill, a repo-local rule, or a new skill.

## Candidate Update

Target skill: `/home/ritual/repos/.cursor/skills/skill-reflection/SKILL.md`.

Require `Candidate Update` entries to include either `Target skill: <path>` or `Target skill: New skill`, with an optional suggested path when a new skill name is already clear.

## Scope

Applies to skill-reflection diary entries that propose durable guidance. It should not force a target path for pure incident notes that are not candidates for promotion.

## Evidence

- The existing entries in this file proposed workflow changes without identifying whether they should update an existing skill or become a new skill.
- The user explicitly asked that candidate updates specify the target skill path or name a new skill.

Promotion status: Not promoted yet
