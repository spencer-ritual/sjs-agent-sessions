# Reth Upstream Merge Coverage Orchestrator Prompt

Use this prompt for the parent/orchestrating agent that verifies whether every
downstream Ritual change from the old `ritual-reth-internal` fork has been
ported into the Reth `v2.2.0` merge workspace or an intentional dependency repo.

## Objective

Build an injective, evidence-backed coverage map from the old downstream diff to
the new port. The outer progress unit is the 579 changed files, because that
gives the parent agent a concrete completion counter. The actual verification
unit is smaller: every non-noise file must be decomposed into diff atoms, and
every atom must be accounted for.

An atom is one indivisible downstream code fact, such as:

- a new branch condition
- a changed constant
- an added match arm
- a removed early return
- a new field or enum variant
- a serialization, hash, signing, or transaction identity rule
- a state transition
- a side effect after settlement
- an error path
- a call ordering constraint
- a test fixture or traffic expectation

Success means:

- the output directory contains exactly 579 per-file JSON records:
`coverage-map/files/file-0001.json` through
`coverage-map/files/file-0579.json`
- every non-noise file has an `atoms_total` count
- every atom is embedded in exactly one per-file JSON record
- every exact or equivalent mapping cites destination code evidence
- every non-exact high-risk atom receives adversarial review or is put in the
human-review queue

### Behavior bar for merge completeness (how to interpret atoms)

The file-level coverage map counts atoms and destinations; **merge “done”** for
behavior is stricter and **FSM-shaped**:

- **Not sufficient:** proving that selected traffic workloads (e.g. scheduled
gold paths) are **green**. That validates **happy paths** only and can miss
**negative cases**, **guard failures**, and **ordering** bugs.

- **Not required:** **byte-for-byte** parity with downstream source. The port
may **refactor** integration (e.g. node builder, payload builder, canonical vs
pool hooks). Mapping should still record **where** behavior lives.

- **Required:** **behavioral equivalence** — the **same effective finite state
machine** for Ritual-owned stateful logic: **states, transitions, guards, and
outputs** (including **failure modes** and **rejection paths**) over the **full
surface** implied by downstream, not only exercised workloads.

When classifying atoms, prioritize:

1. **Is downstream behavior missing in the port?** (`missing` / blocked /
   unmapped negative paths)
2. **If not missing, why is the mapping non-exact?** (`structural_equivalent`,
   `moved_to_dependency`, `intentionally_absent`, `covered_by_upstream`, etc.)
3. **Is that gap or refactor acceptable for consensus / safety?** Document in
   `review-queue.md` when uncertain.

Labels like `structural_equivalent` or `intentionally_absent` **explain** a
non-exact mapping; they **do not** downgrade a true **behavioral** omission.

### Cross-repo executor capability contract (async precompiles)

Reth-only evidence (decode gates, two-phase registration, SPC allowlists) is **not**
sufficient when settlement compares the TEE registry executor’s `Capability` to
`expected_capability_tag` for the job precompile. For **parity with the legacy stack**,
always trace the full chain when classifying or closing atoms:

`precompile address` → `expected_capability_tag` / registry u8 → traffic-gen
`ExecutorSelector` capability → node `configgen` / executor `CAPABILITIES=` → payload
builder + block verifier expectations.

A **name-plausible** mapping (e.g. Sovereign Agent → `AutonomousAgent`) can still
**break localnet** if downstream continues to pin **HTTP_CALL** executors. Prefer
**executable** atoms: destination tests or cross-repo citations, not “reasonable
abstraction” arguments. Multimodal (`IMAGE_CALL`, `AUDIO_CALL`, `VIDEO_CALL`) and
`FHE` should use the same checklist against `image_call.py`, `audio_call.py`,
`video_call.py`, `fhe_inference.py`, and `docker.py` capability wiring.

### Feature completion hard gate (merge-auditable)

A **feature** (section in `feature-map.md`, or a named cross-cutting concern such as
“async precompile registry contracts”) is **not complete** while **any** of the following
remain anywhere in that feature’s atom footprint:

- `mapping_status` is `blocked`
- `needs_atomization` is true
- `review_required` is true **without** a recorded adversarial review **or** an explicit
  decision note in the atom
- `semantic_claim` is broad/feature-derived **without** a machine-checkable proof path
  (tests, or a script such as `coverage-map/verify_async_precompile_cross_repo.py`)

Orchestrators must not treat “some atoms are green” as featuredone. **`coverage_tools.py validate`**
must pass, and for async precompile work **verify_async_precompile_cross_repo.py** must exit 0.

## Scope Boundary

This is a mapping and audit pass only. The orchestrator and child agents must not
modify implementation code in any repo. If an atom is missing, incomplete, or
blocked, record it precisely in the coverage output and review queue. Do not fix
it during this pass.

## Crates-Only Scope Rule

For the remainder of this coverage pass, only source paths under `crates/` are in
scope for atom decomposition and missing-behavior review. Treat every queue entry
whose `source_path` does not start with `crates/` as `noise`, with
`atoms_total: 0`, unless the user explicitly requests a targeted exception.

This includes root files, lockfiles, workflow/config files, docs, examples,
scripts, testing utilities, and `bin/` tools. Earlier non-`crates/` entries were
reviewed or ported separately; future coverage work should not spend context on
them.

## Source Artifacts

Use these files as the source of truth:

- Main diff:
`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/ritual-reth-internal-downstream-from-divergence.diff`
- Metadata:
`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/ritual-reth-internal-downstream-from-divergence.meta.txt`
- Work queue:
`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/ritual-reth-internal-downstream-from-divergence.name-status.txt`
- Stat summary:
`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/ritual-reth-internal-downstream-from-divergence.stat.txt`

The diff was generated from:

```sh
git -C /home/ritual/repos/ritual-reth-internal diff --find-renames --find-copies --binary 6f8e7258f4733279080e4bd8345ce50538a40d6e f2f96b9b545ae4bdf80dd3753010aa8e01ac0402
```

## Destination Search Scope

Search these repos when mapping atoms:

- `/home/ritual/repos/ritual-reth-internal-v2.2.0-port`
- `/home/ritual/repos/ritual-reth-nodebuilder-internal`
- `/home/ritual/repos/ritual-alloy-internal`
- `/home/ritual/repos/ritual-alloy-evm-internal`
- `/home/ritual/repos/ritual-revm-internal`
- `/home/ritual/repos/ritual-revm-inspectors-internal`
- `/home/ritual/repos/ritual-node-internal`, only for orchestration or verification behavior

## Orchestrator Role

You are the parent agent. Your job is orchestration, accounting, and validation.
Do not personally do deep per-file analysis except for smoke-testing the first
file, validating child output, or resolving ambiguity.

For each file in the 579-entry queue:

1. Assign a stable `file_index` from `1` to `579`.
2. Extract or generate the per-file patch for that entry.
3. Spawn a subagent to analyze exactly that one file.
4. Require the subagent to decompose the patch into atoms before mapping.
5. Require the subagent to return structured JSON only.
6. Validate the child result before writing the per-file JSON artifact.
7. Write exactly one file artifact at `coverage-map/files/file-####.json`.
8. Spawn adversarial review for high-risk or non-exact atoms.
9. Track progress in a progress file.

The parent agent owns all writes under `coverage-map/`. Child agents should be
read-only investigators unless explicitly directed otherwise.

## Required Output Directory

Create and maintain all coverage artifacts under:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map/`

Use this layout:

```text
coverage-map/
  files/
    file-0001.json
    file-0002.json
    ...
    file-0579.json
  reviews/
    review-file-0001-atom-0001.json
    ...
  index.jsonl
  progress.md
  review-queue.md
  validation-summary.json
```

The `files/` directory is the main completion surface. A complete run must have
exactly 579 files named with zero-padded indices from `file-0001.json` through
`file-0579.json`. Do not include source paths in filenames; source paths belong
inside the JSON.

`index.jsonl` is a convenience index with one line per file. It does not replace
the 579 per-file JSON artifacts.

`reviews/` stores one JSON file per adversarial review. Review files are optional
for exact low-risk atoms, but required for high-risk non-exact atoms unless the
atom is listed in `review-queue.md`.

If correcting a bad per-file artifact, overwrite that `file-####.json` and record
the correction in `progress.md`.

## Future Agent Usage Path

When a later agent uses `coverage-map/` to fix or review port gaps, it should
consume the artifacts before reading source files:

1. Start with `coverage-map/index.jsonl` to identify file indices, source paths,
  classifications, atom counts, and review status.
2. Skip any record with `file_classification: "noise"`, `atoms_total: 0`, and
  `status: "complete"` without opening the original source file.
3. For actionable work, start with `coverage-map/review-queue.md`; every entry
  must key back to `file_index`, `source_path`, atom `record_id`, and hunk.
4. Open only the relevant `coverage-map/files/file-####.json` records for the
  listed atom IDs, then read destination/source code only as needed to implement
   or verify that atom.
5. Treat `validation-summary.json` as the high-level dashboard for remaining
  counts, but never as a substitute for the atom record when making code
   changes.
6. If a fixer agent resolves a missing or blocked atom, it should update the
  corresponding per-file artifact, remove or amend the keyed review-queue
   entry, and record the correction in `progress.md`.

The intended fast path is: `index.jsonl` -> `review-queue.md` -> specific
`file-####.json` atom -> source/destination code only for that atom.

## Tagging Rules

Each per-file JSON record must include `tags`, an array of short machine-readable
labels. Tags are for filtering and sanity checks; they do not replace structured
fields.

Use these tag families:

- Classification tags: `mapped`, `noise`, `missing`, `blocked`, `dropped`
- Risk tags: `high-risk`, `non-exact`, `needs-review`
- Domain tags: `async-fsm`, `scheduled`, `payload`, `verifier`, `execution`,
`txpool`, `rpc`, `precompile`, `encoding`, `fees`, `gas`, `rewards`,
`executor-selection`, `consensus-constant`, `negative-path`
- Location tags: `reth-port`, `nodebuilder`, `alloy`, `alloy-evm`, `revm`,
`revm-inspectors`, `node-orchestration`, `upstream-covered`

Every high-risk atom should also carry `risk_tags` scoped to the atom.

## Exact-Code-First Rule

For each atom, the child agent must first try to find exact or near-exact code in
the destination repos before writing a semantic-equivalence argument.

Preferred evidence order:

1. `exact`: same code, same logic, or trivial formatting/import adaptation exists.
2. `renamed_exact`: same code exists after path, module, type, function, or field
  rename.
3. `covered_by_upstream`: upstream Reth `v2.2.0` already implements the same
  downstream behavior, making the local patch unnecessary.
4. `moved_to_dependency`: the atom landed in Alloy, revm, nodebuilder, or another
  dependency/integration repo.
5. `structural_equivalent`: logic moved into a different architecture, with a
  precise equivalence argument.
6. `intentionally_absent`: human-approved non-port or obsolete behavior.
7. `missing`: no destination evidence found.
8. `blocked`: agent cannot decide with available context.
9. `noise`: generated, docs-only, lockfile-only, scratch, or non-behavioral.

Do not use `structural_equivalent` when exact or renamed-exact evidence exists.
Do not use `covered_by_upstream`, `moved_to_dependency`, or
`structural_equivalent` without code evidence.

## Markdown Skip Rule

For this coverage pass, treat every Markdown file (`*.md`) as `noise` regardless
of content. Do not atomize Markdown files, do not spawn deep mapping work for
them, and do not search destination repos for Markdown evidence. Write the
per-file artifact with `file_classification: "noise"`, `tags: ["noise"]`,
`atoms_total: 0`, `atoms: []`, `status: "complete"`, and a concise note that
Markdown is intentionally skipped for this audit.

## High-Risk Atom Rule

Mark an atom `high_risk: true` if it touches any of:

- async FSM state, transition, settlement, fulfillment, replay, cleanup, or
canonical commitment behavior
- scheduled transaction identity, predicates, missed obligations, block math, or
verifier parity
- payload building, block verification, execution, transaction pool, RPC result
submission, engine validation, or precompile dispatch
- transaction encoding, hashing, signing, wire/storage identity, runtime fields,
or custom transaction types
- fee accounting, executor selection, wallet behavior, gas limits, rewards, or
consensus-visible constants
- negative paths: rejection, error mapping, malformed input, duplicate handling,
expiry, stale state, wrong executor, or verifier-builder disagreement

Every high-risk atom whose mapping status is not `exact` or `renamed_exact` must
receive either:

- an adversarial review by a second subagent, or
- a `review_required: true` entry in `coverage-map/review-queue.md`.

## Test Candidate Rule

Every high-risk atom must include a `negative_test_candidate` when one can be
formulated. The test candidate is not required to be implemented during the
mapping pass, but it must describe the smallest stimulus that could falsify the
mapping.

Use one of these test strategy labels:

- `same_test_both_repos`
- `adapted_equivalence_test`
- `destination_only_regression`
- `integration_traffic`
- `not_testable`
- `not_needed`

## Actionable Finding Traceability Rule

Every missing, blocked, intentionally absent, or change-needed finding must be
keyed back to the exact source queue entry and atom. The key must include:

- `file_index`
- `source_path`
- atom `record_id`
- `source_hunk_hint`
- a concise `required_change` or `human_question`
- the destination repo/path that likely needs work, when known

For any such finding, the per-file artifact must keep the full atom record, and
`coverage-map/review-queue.md` must include a human-readable entry using the
same key. Do not report an actionable finding only in prose or only in an
aggregate summary.

## Per-File Artifact Schema

Each completed file writes one JSON object to
`coverage-map/files/file-####.json`:

```json
{
  "record_type": "file",
  "file_index": 1,
  "total_files": 579,
  "source_status": "A|M|D|R|C",
  "source_path": "path/from/name-status.txt",
  "source_old_path": null,
  "source_commit_range": {
    "base": "6f8e7258f4733279080e4bd8345ce50538a40d6e",
    "head": "f2f96b9b545ae4bdf80dd3753010aa8e01ac0402"
  },
  "file_classification": "mapped|noise|missing|blocked|dropped",
  "tags": ["mapped", "high-risk", "async-fsm"],
  "atoms_total": 3,
  "atoms": [],
  "high_risk_atoms_total": 1,
  "non_exact_atoms_total": 1,
  "adversarial_reviews": [],
  "summary": "one concise sentence",
  "review_required": false,
  "status": "complete",
  "notes": "short rationale"
}
```

`status` must be one of `complete`, `needs_review`, or `blocked`. Do not write a
`complete` file artifact unless all atoms for that file are accounted for.

## Atom Schema

Embed atom objects in the per-file artifact's `atoms` array:

```json
{
  "record_id": "file-0001-atom-0001",
  "file_index": 1,
  "atom_index": 1,
  "atoms_total": 3,
  "source_path": "path/from/name-status.txt",
  "source_hunk_hint": "@@ ... @@",
  "source_kind": "changed_branch_condition|changed_constant|added_match_arm|removed_early_return|new_field|encoding_rule|state_transition|side_effect|error_path|call_ordering|test_fixture|other",
  "source_snippet": "small source snippet, not the entire hunk",
  "semantic_claim": "specific behavior encoded by this atom",
  "high_risk": true,
  "risk_tags": ["async-fsm", "negative-path"],
  "mapping_status": "exact|renamed_exact|covered_by_upstream|moved_to_dependency|structural_equivalent|intentionally_absent|missing|blocked|noise",
  "destinations": [
    {
      "repo": "/home/ritual/repos/ritual-reth-internal-v2.2.0-port",
      "path": "crates/...",
      "symbols": ["..."],
      "snippet": "small destination snippet",
      "evidence": "why this destination implements the same atom"
    }
  ],
  "equivalence_argument": "required for structural_equivalent, covered_by_upstream, or moved_to_dependency",
  "test_strategy": "same_test_both_repos|adapted_equivalence_test|destination_only_regression|integration_traffic|not_testable|not_needed",
  "negative_test_candidate": "smallest stimulus that would falsify this mapping, or null",
  "adversarial_review": {
    "required": true,
    "status": "not_requested|pass|fail|blocked",
    "review_record_id": null
  },
  "review_required": false,
  "notes": "short rationale"
}
```

## Adversarial Review Schema

When a second subagent reviews a high-risk or non-exact atom, write one file
under `coverage-map/reviews/`:

```json
{
  "record_type": "adversarial_review",
  "record_id": "review-file-0001-atom-0001",
  "atom_record_id": "file-0001-atom-0001",
  "review_result": "pass|fail|blocked",
  "falsification_attempt": "what the reviewer checked",
  "missed_risks": [],
  "notes": "short rationale"
}
```

## Child Agent Prompt Template

Use one subagent per source file. Fill in the placeholders before dispatch.

```text
You are analyzing one file from the Ritual Reth downstream divergence diff.

Parent accounting:
- file_index: {FILE_INDEX}
- total_files: 579
- source status: {SOURCE_STATUS}
- source path: {SOURCE_PATH}
- old path for rename/copy/delete if applicable: {SOURCE_OLD_PATH}

Source context:
- downstream source repo: /home/ritual/repos/ritual-reth-internal
- divergence base: 6f8e7258f4733279080e4bd8345ce50538a40d6e
- downstream head: f2f96b9b545ae4bdf80dd3753010aa8e01ac0402
- upstream target: Reth v2.2.0 at 88505c7fcbfdebfd3b56d88c86b62e950043c6c4
- port repo: /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- dependency repos to search when behavior moved:
  - /home/ritual/repos/ritual-reth-nodebuilder-internal
  - /home/ritual/repos/ritual-alloy-internal
  - /home/ritual/repos/ritual-alloy-evm-internal
  - /home/ritual/repos/ritual-revm-internal
  - /home/ritual/repos/ritual-revm-inspectors-internal
  - /home/ritual/repos/ritual-node-internal

Your task:
1. Analyze only this source file's downstream diff.
2. Decompose the patch into atomic code facts. Do not skip branches, constants, match arms, error paths, ordering constraints, serialization/hash rules, side effects, or tests.
3. Set `atoms_total` before mapping.
4. For each atom, first search for exact or near-exact code in destination repos.
5. If exact code is not present, determine whether the atom is renamed-exact, covered by upstream, moved to a dependency, structurally equivalent, intentionally absent, missing, blocked, or noise.
6. For structural equivalence, explain the same guard, transition, side effect, and verifier/builder parity where relevant.
7. Mark high-risk atoms precisely. High-risk includes async FSM, scheduled transactions, payload, verification, execution, txpool, RPC, precompile dispatch, encoding/hash/signing, fee/gas/reward logic, executor selection, consensus constants, and all negative paths.
8. For every high-risk atom, include a negative test candidate unless genuinely not testable.
9. Do not modify implementation code. This is a mapping-only audit.
10. Return JSON only, matching the schema below.

Important: do not summarize a whole file as covered. The parent needs atom-level accounting. If the file is noise, return `atoms_total: 0` and explain why.

Source file patch:

```diff
{SOURCE_FILE_PATCH}
```

Return JSON:

```json
{
  "file_index": {FILE_INDEX},
  "source_status": "{SOURCE_STATUS}",
  "source_path": "{SOURCE_PATH}",
  "source_old_path": {SOURCE_OLD_PATH_JSON},
  "file_classification": "mapped|noise|missing|blocked|dropped",
  "tags": [],
  "atoms_total": 0,
  "atoms": [],
  "high_risk_atoms_total": 0,
  "non_exact_atoms_total": 0,
  "adversarial_reviews": [],
  "summary": "one concise sentence",
  "review_required": false,
  "status": "complete|needs_review|blocked",
  "notes": "short rationale"
}
```

For each atom, use:

```json
{
  "atom_id": "file-{FILE_INDEX_PADDED}-atom-0001",
  "atom_index": 1,
  "atoms_total": 1,
  "source_hunk_hint": "@@ ... @@",
  "source_kind": "changed_branch_condition|changed_constant|added_match_arm|removed_early_return|new_field|encoding_rule|state_transition|side_effect|error_path|call_ordering|test_fixture|other",
  "source_snippet": "small source snippet",
  "semantic_claim": "specific behavior",
  "high_risk": false,
  "risk_tags": [],
  "mapping_status": "exact|renamed_exact|covered_by_upstream|moved_to_dependency|structural_equivalent|intentionally_absent|missing|blocked|noise",
  "destinations": [],
  "equivalence_argument": null,
  "test_strategy": "same_test_both_repos|adapted_equivalence_test|destination_only_regression|integration_traffic|not_testable|not_needed",
  "negative_test_candidate": null,
  "adversarial_review_required": false,
  "review_required": false,
  "notes": "short rationale"
}
```

```

## Adversarial Reviewer Prompt Template

Use this only for one atom at a time.

```text
You are the adversarial reviewer for one mapped diff atom. Your job is to try to falsify the mapping, not to rubber-stamp it.

Review this atom:

```json
{ATOM_RECORD_JSON}
```

Source patch context:

```diff
{SOURCE_FILE_PATCH_OR_HUNK}
```

Check:

1. Does the destination evidence implement the same source atom, not merely related logic?
2. Are the same guards, state transitions, side effects, and error/rejection paths preserved?
3. If this is structural equivalence, did the original code split across multiple destination locations?
4. Is builder/verifier parity preserved when consensus-sensitive?
5. Is the negative test candidate capable of falsifying the claim?

Return JSON:

```json
{
  "atom_record_id": "{ATOM_RECORD_ID}",
  "review_result": "pass|fail|blocked",
  "falsification_attempt": "what you checked",
  "missed_risks": [],
  "notes": "short rationale"
}
```

```

## Validation Checklist

Before considering the run complete, verify:

- `coverage-map/files/` has exactly 579 JSON files.
- Every file from `file-0001.json` through `file-0579.json` exists exactly once.
- Every per-file artifact has matching `file_index`, `total_files: 579`, source
status, and source path from the queue.
- For every non-noise file, `atoms_total` is greater than zero.
- For every non-noise file, embedded atom count exactly matches `atoms_total`.
- Every atom has exactly one `mapping_status`.
- Every atom with `mapping_status` of `exact`, `renamed_exact`,
`covered_by_upstream`, `moved_to_dependency`, or `structural_equivalent` has
destination evidence.
- Every atom with `mapping_status` of `structural_equivalent`,
`covered_by_upstream`, or `moved_to_dependency` has an equivalence argument.
- Every high-risk atom has a test strategy and a negative test candidate, unless
marked `not_testable` with rationale.
- Every high-risk atom whose mapping is not `exact` or `renamed_exact` has an
adversarial review file under `coverage-map/reviews/` or appears in
`coverage-map/review-queue.md`.
- Every `missing`, `blocked`, or `intentionally_absent` atom appears in
`coverage-map/review-queue.md`.
- Every actionable finding in `coverage-map/review-queue.md` is keyed by
`file_index`, `source_path`, atom `record_id`, source hunk, and the required
change or human question.
- The final summary reports counts by file classification, atom mapping status,
high-risk status, adversarial review status, and remaining human-review queue.

## Full-Pass Continuation Mode

The first-file trial is complete. For the production pass, continue from the
current `coverage-map/` state rather than restarting from scratch.

Before processing new files:

- read `coverage-map/index.jsonl`, `coverage-map/progress.md`,
`coverage-map/review-queue.md`, and `coverage-map/validation-summary.json`
- identify which `file-####.json` artifacts already exist
- do not rewrite existing complete artifacts unless correcting a validation error
- continue assigning artifacts by the stable queue `file_index`

Process every remaining queue entry until the full 579-file surface is complete.
Apply the crates-only scope rule: non-`crates/` paths are `noise` unless the user
explicitly requests a targeted exception. For in-scope `crates/` paths, decompose
non-noise patches into atoms and map each atom using exact-code-first search.

This is still a mapping-only audit. Do not modify implementation code while
building the coverage map.
```

