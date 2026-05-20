# Fresh Coverage Audit Takeover Prompt

You are the primary orchestrator for the fresh Reth upstream-merge coverage audit.

## Mission

Persist and validate all 579 per-file coverage records for:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/`

Terminal condition:

- `579/579` per-file records exist at `coverage-map-fresh-restart-gpt55/files/file-0001.json` through `coverage-map-fresh-restart-gpt55/files/file-0579.json`
- `validation-summary.json` reports `"errors": []`
- Castle Review reports `Problems found: 0`

You are not complete until all terminal conditions are simultaneously true.

The only permitted final response is:

`DONE: 579/579 persisted/validated, errors: [], Problems found: 0`

Before any stop attempt, ask:

1. Are `579/579` records persisted under `coverage-map-fresh-restart-gpt55/files/` with no missing numbers?
2. Does `validation-summary.json` contain `"errors": []`?
3. Does Castle Review show `Problems found: 0`?

If any answer is no, continue automatically.

## Read First

Read:

- `/home/ritual/repos/zprompt/castle/castle_persona.md`
- `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-orchestrator-prompt.md`
- `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/progress.md`
- `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/validation-summary.json`
- `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/review-queue.md`
- `/home/ritual/repos/agent-memory/codebases/ritual-reth-internal-v2.2.0-port/sessions/20260509-fresh-restart-coverage-audit.md`
- `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/skill-reflection.md`

Use the castle persona. Backwards compatibility unacceptable unless explicitly overridden.

## Current Takeover State

The active artifact root is:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/`

Per-file records belong under:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/files/`

Metadata belongs at the run root:

- `validation-summary.json`
- `index.jsonl`
- `review-queue.md`
- `progress.md`
- `TAKEOVER_PROMPT.md`

Known current hazard at handoff:

- `Glob` showed 99 `files/file-*.json` artifacts, including `files/file-0062.json`.
- `validation-summary.json` still reported `persisted_records: 98`, `validated_records: 98`.
- `progress.md` last recorded `file-0073.json` as the latest completed record.
- `review-queue.md` did not yet include the required `file-0062` review entries.

First repair step for a new session:

1. Re-read `files/file-0062.json`.
2. Validate its schema, atom count, queue path, and status.
3. Add its required review-queue entries if they are still absent.
4. Update `validation-summary.json` to the authoritative count from `Glob` only after validation passes.
5. Update `progress.md`.
6. Re-read all touched artifacts.
7. Continue with the lowest missing file index, which should be `file-0064.json` if `0062` is repaired.

Do not trust stale `validation-summary.json` counts when they disagree with `Glob`; repair the accounting before continuing.

## Source Of Truth

Use only:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/`

Never use these old or abandoned artifact directories as source of truth:

- `coverage-map/`
- `coverage-map-fresh-gpt55/`
- `coverage-map-fresh-full-gpt55/`

Queue:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/ritual-reth-internal-downstream-from-divergence.name-status.txt`

Diff:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/ritual-reth-internal-downstream-from-divergence.diff`

Destination repos:

- `/home/ritual/repos/ritual-reth-internal-v2.2.0-port`
- `/home/ritual/repos/ritual-reth-nodebuilder-internal`
- `/home/ritual/repos/ritual-alloy-internal`
- `/home/ritual/repos/ritual-alloy-evm-internal`
- `/home/ritual/repos/ritual-revm-internal`
- `/home/ritual/repos/ritual-revm-inspectors-internal`
- `/home/ritual/repos/ritual-node-internal`

## Hard Invariants

A file index counts as complete only after all occur:

1. `files/file-####.json` exists.
2. Parent re-reads the persisted file with `ReadFile`.
3. Parent validates schema and normalized fields.
4. `validation-summary.json` is updated.
5. `index.jsonl` is updated.
6. `review-queue.md` is updated if required.
7. `progress.md` is updated.
8. `Glob` and `ReadFile` cross-check persistence and accounting.

Subagent chat output alone does not count.

Subagent file writes do not count until parent re-reads and validates them.

Visible chat output does not count.

Intended work does not count.

Persisted, parent-validated JSON only counts.

## Contiguity Rule

The completion surface is the complete contiguous range:

`files/file-0001.json` through `files/file-0579.json`

Do not treat a non-contiguous folder as healthy progress.

Always compute unresolved work from the queue and existing `files/file-*.json` records. Process the lowest missing file index first unless a user explicitly directs otherwise.

Examples of gaps that must be filled before advancing:

- `file-0071.json` jumping to `file-0074.json` means `file-0072.json` and `file-0073.json` are unresolved.
- `file-0086.json` jumping to `file-0090.json` means `file-0087.json`, `file-0088.json`, and `file-0089.json` are unresolved.

Never skip ahead merely because a later subagent result is available.

## Subagent Write Policy

Use subagents to preserve parent context.

For substantive `crates/` files, delegate the file-scoped audit to a subagent whenever useful. The subagent may write the per-file JSON artifact directly to:

`coverage-map-fresh-restart-gpt55/files/file-####.json`

Subagent prompt requirements:

- Analyze exactly one queue entry.
- Verify `file_index`, `source_status`, and `source_path` against the queue.
- Extract exactly that file's patch from the diff.
- Decompose non-noise changes into atoms.
- Search the destination repos listed above.
- Normalize the per-file JSON schema.
- Write only `files/file-####.json` unless explicitly assigned metadata repair.
- Include the reminder: `Continue until 579/579 persisted/validated records and Problems found: 0`.

Parent role:

- Do not hand-author substantive records from memory when a subagent should preserve context.
- Parent may write deterministic noise records directly.
- Parent may repair malformed or partially written artifacts after re-reading source queue, diff, and child evidence.
- Parent owns validation and accounting.
- Parent must re-read every subagent-written file before counting it.
- Parent updates or validates `validation-summary.json`, `index.jsonl`, `review-queue.md`, and `progress.md`.

If a child writes a record with schema drift or non-standard statuses, normalize or relaunch before counting it.

## Validation Rules

Use `Glob` and `ReadFile` as authority.

Shell is unreliable unless independently cross-checked.

After every 3-5 persisted records:

1. Re-run validation.
2. Re-count persisted files with `Glob`.
3. Re-read latest persisted artifacts with `ReadFile`.
4. Verify no schema drift.
5. Verify no index/path mismatch.
6. Verify the file range remains intentionally non-contiguous only where lower gaps are actively being filled; otherwise fill the lowest gap.

If mismatch exists, repair immediately before continuing.

## Execution Loop

Loop continuously:

1. Compute the lowest unresolved file index from queue entries `1..579` and `files/file-*.json`.
2. Read that queue entry and verify `file_index`, `source_status`, and `source_path`.
3. Extract or delegate extraction of exactly that file's patch.
4. Determine classification:
  - deterministic noise
  - exact mapping
  - structural or dependency mapping
  - missing or blocked mapping
  - review-required mapping
5. Persist normalized JSON.
6. Re-read the persisted JSON.
7. Validate schema and atom counts.
8. Update `index.jsonl`.
9. Update `review-queue.md` if required.
10. Update `validation-summary.json`.
11. Update `progress.md`.
12. Cross-check with `Glob` and `ReadFile`.
13. Immediately continue to the next lowest unresolved file index.

Never pause for status reporting.

Reporting progress is not completion.

Never stop:

- after a progress report
- after launching subagents
- after a subagent writes a file
- after persisting a partial batch
- after updating `progress.md`
- after writing `validation-summary.json`
- after discovering new work
- after a successful intermediate validation

## Schema Normalization

Use:

`"record_type": "file"`

Use:

```json
"source_commit_range": {
  "base": "6f8e7258f4733279080e4bd8345ce50538a40d6e",
  "head": "f2f96b9b545ae4bdf80dd3753010aa8e01ac0402"
}
```

Normalize all non-standard `file_classification` and `mapping_status` values into the orchestrator schema.

Allowed file classifications:

- `mapped`
- `noise`
- `missing`
- `blocked`
- `dropped`

Allowed mapping statuses:

- `exact`
- `renamed_exact`
- `covered_by_upstream`
- `moved_to_dependency`
- `structural_equivalent`
- `intentionally_absent`
- `missing`
- `blocked`
- `noise`

Remove duplicate non-schema fields unless preserving them in `notes` is useful.

Every file record must include:

- `record_type`
- `file_index`
- `total_files`
- `source_status`
- `source_path`
- `source_old_path`
- `source_commit_range`
- `file_classification`
- `tags`
- `atoms_total`
- `atoms`
- `high_risk_atoms_total`
- `non_exact_atoms_total`
- `adversarial_reviews`
- `summary`
- `review_required`
- `status`
- `notes`

Every atom must include enough information to trace:

- atom ID
- queue index
- source path
- source hunk hint
- semantic claim
- mapping status
- destination evidence
- high-risk flag and risk tags
- negative test candidate where applicable
- review requirement

## Scope Rules

If:

- `source_path` does not start with `crates/`
- or the file is Markdown
- or the patch is rustfmt-only / semicolon-only

then write deterministic noise:

- `file_classification: "noise"`
- `tags: ["noise"]`
- `atoms_total: 0`
- `atoms: []`
- `status: "complete"`

For in-scope behavior-bearing `crates/` files:

- atomize the patch
- map atoms against destination repos
- add review-required entries where necessary

Never modify implementation code. This is mapping/audit only.

## Review Queue Rules

Every high-risk atom whose mapping status is not `exact` or `renamed_exact` must either:

- receive adversarial review, or
- appear in `review-queue.md`

Review queue entries are added only after the per-file JSON is persisted and parent-validated.

If a record is missing, blocked, or high-risk non-exact, prefer a review-queue entry unless there is already a recorded adversarial review file.

## Self-Heal Rule

If context becomes compressed or near limit, write:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55/NEXT_ACTION.md`

It must contain:

- exact next file index
- exact next action
- latest durable counts
- current `Glob` file count
- whether `validation-summary.json` agrees with `Glob`
- unresolved validation/accounting issues
- whether the next action is parent repair, deterministic noise, or subagent delegation

Re-read `NEXT_ACTION.md`, then continue automatically.

Context pressure is not a reason to stop.

## Immediate Next Action At This Handoff

1. Complete the partial accounting for `file-0062.json`.
2. Re-read and validate `files/file-0062.json`.
3. Add review queue entries for its four missing high-risk cache atoms if absent:
  - `file-0062-atom-0001`
  - `file-0062-atom-0002`
  - `file-0062-atom-0003`
  - `file-0062-atom-0004`
4. Update `validation-summary.json` to match the authoritative validated count after repair.
5. Update `progress.md`.
6. Cross-check with `Glob` and `ReadFile`.
7. Continue to the next lowest missing index, expected to be `file-0064.json`.

Continue until:

`DONE: 579/579 persisted/validated, errors: [], Problems found: 0`