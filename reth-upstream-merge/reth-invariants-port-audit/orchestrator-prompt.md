# Reth Current Invariants Port Audit Orchestrator Prompt

Use this prompt for the parent/orchestrating agent that verifies whether every
current Ritual Reth invariant is preserved in the Reth `v2.2.0` port workspace or
one of the dependency repos on the `spencer/2605-reth-upstream-merge` line.

This task is related to, but distinct from, the downstream-diff coverage map. The
coverage map proves that old downstream code facts were ported. This invariant
audit proves that every current invariant from the invariant atlas has an
evidence-backed implementation mapping or is an evidence-backed confirmed gap.

## Objective

Build a complete, evidence-backed invariant coverage map for all current refined
invariants.

The outer progress unit is the invariant, not a file. The queue is the complete
set of `refined_invariants` whose `status` is `current` in the Atlas bundle:

`https://invariants-atlas-59313947041.us-central1.run.app/data/bundle.json`

At the time this prompt was drafted, the bundle reported:

- generated date: `2026-05-10`
- `refined_invariants`: `1993`
- `current`: `1954`

Do not rely on those counts blindly. Fetch the bundle at run time, record its
`generated` date and current count, and build the queue from the fetched data.

Success means:

- every current refined invariant appears exactly once in the queue
- every current refined invariant has exactly one per-invariant JSON artifact
- every per-invariant artifact is terminal and complete when written
- every invariant is classified as either `mapped_in_port`,
`mapped_in_dependency`, or `confirmed_gap`
- every mapped invariant cites concrete destination code evidence
- every confirmed gap cites concrete negative search evidence and the missing
behavior
- validation proves there are no skipped, duplicated, unresolved, blocked, or
needs-review invariant artifacts

## Non-Negotiable Completion Rule

There are no temporary artifact states.

Do not write a per-invariant artifact until the invariant is actually complete.
Do not write artifacts with `blocked`, `needs_review`, `pending`, `partial`,
`unknown`, or similar status values. If an investigator cannot finish an
invariant, the parent must continue investigation, assign another investigator,
or do the work itself before writing the artifact.

The completed artifact set has only these mapping statuses:

- `mapped_in_port`
- `mapped_in_dependency`
- `confirmed_gap`

The final audit must not contain a `not_applicable_to_port` category. Every
current invariant must be mapped somewhere in the audited repo set or confirmed
as a gap.

## Resource Strategy

Use the Atlas bundle as the canonical queue source.

The Atlas UI at:

`https://invariants-atlas-59313947041.us-central1.run.app/`

is useful for human inspection, but do not scrape it for iteration. The UI is a
client-rendered view over the data bundle.

Use the ritual-invariants MCP as the enrichment and relevance layer. The server
is configured in Cursor as:

`user-ritual-invariants`

Useful MCP tools include:

- `get_invariant`: fetches a full invariant record by id
- `invariants_for_changed_files`: maps known file paths to current invariants
- `invariants_for_symbol`: maps code symbols to current invariants
- `relevance_signals`: maps capability or concept queries to pre-clustered
invariant relevance signals
- `search_invariants`: BM25 search over invariant title, statement, and
rationale
- `browse_themes`: table-of-contents view by subsystem
- `list_clusters`: cluster inventory by subsystem

Do not use MCP search as the primary queue. Search tools have ranking and limit
semantics; they are for enrichment, not complete enumeration.

## Audited Repos

Search for invariant implementations in this repo set:

- `/home/ritual/repos/ritual-reth-internal-v2.2.0-port`
- `/home/ritual/repos/ritual-reth-nodebuilder-internal`
- `/home/ritual/repos/ritual-alloy-internal`
- `/home/ritual/repos/ritual-alloy-evm-internal`
- `/home/ritual/repos/ritual-revm-internal`
- `/home/ritual/repos/ritual-revm-inspectors-internal`
- `/home/ritual/repos/ritual-node-internal`

The intended audit branch differs by repo. Before starting a production audit,
record each repo's current branch and commit.

These repos are intentionally audited on `spencer/2605-rum-iot`; do not normalize
them to `spencer/2605-reth-upstream-merge`:

- `/home/ritual/repos/ritual-reth-internal-v2.2.0-port`
- `/home/ritual/repos/ritual-reth-nodebuilder-internal`

The remaining dependency repos are intended to be audited on
`spencer/2605-reth-upstream-merge`:

- `/home/ritual/repos/ritual-alloy-internal`
- `/home/ritual/repos/ritual-alloy-evm-internal`
- `/home/ritual/repos/ritual-revm-internal`
- `/home/ritual/repos/ritual-revm-inspectors-internal`
- `/home/ritual/repos/ritual-node-internal`

The working convention is that `spencer/2605-rum-iot` may be ahead by a few
working commits for the port and nodebuilder repos while the broader
`spencer/2605-reth-upstream-merge` line continues receiving new work in the
dependency repos. Do not silently audit against an unexpected branch. Record the
branch and commit in the run metadata.

Execution locality rule: audit only the local checkouts listed above. Do not SSH
to remote hosts, do not access `spencer-tdxbox-3`, do not fetch from the
network, and do not request elevated or dangerous permissions. If a dependency
repo or expected source path is missing locally, record that as local negative
search evidence and let the parent decide how to resolve it.

## Prior Context

Before broad exploration, read the repo memory for the port workspace when
available:

`/home/ritual/repos/agent-memory/codebases/ritual-reth-internal-v2.2.0-port/index.md`

The memory contains many prior coverage-map sessions and known areas around
async, scheduled transactions, precompile registries, txpool, RPC, payload
building, block verification, heartbeat revival, and dependency repo moves.
Treat it as hints, not source of truth. The invariant audit must still produce
fresh per-invariant evidence.

The earlier downstream-diff coverage orchestrator prompt is useful as a workflow
model:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-orchestrator-prompt.md`

Reuse the accounting discipline from that prompt:

- stable numbered units
- one JSON artifact per completed unit
- exact or near-exact code search before semantic arguments
- concise destination evidence
- separate validation summary
- no prose-only actionable findings

Do not reuse the coverage map's source-file queue or atom schema directly. This
audit is invariant-indexed.

## Required Output Directory

Create and maintain all audit artifacts under:

`/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/reth-invariants-port-audit/`

Use this layout:

```text
reth-invariants-port-audit/
  orchestrator-prompt.md
  atlas-bundle.generated-YYYY-MM-DD.json
  run-metadata.json
  queue.current-invariants.jsonl
  invariants/
    invariant-0001.json
    invariant-0002.json
    ...
  index.jsonl
  confirmed-gaps.md
  progress.md
  validation-summary.json
```

The `invariants/` directory is the main completion surface. A complete run must
have exactly one zero-padded JSON file for every current refined invariant in the
queue.

Do not include invariant titles in filenames. Use stable queue indices in
filenames and store invariant IDs and titles inside the JSON.

`index.jsonl` is a convenience index with one line per invariant. It does not
replace the per-invariant artifacts.

`confirmed-gaps.md` is a human-readable view of all confirmed gaps. It does not
replace the full JSON record.

If correcting a bad artifact, overwrite that `invariant-####.json` and record the
correction in `progress.md`.

## Queue Construction

Fetch the Atlas bundle and write it to:

`atlas-bundle.generated-YYYY-MM-DD.json`

Build `queue.current-invariants.jsonl` by selecting:

```text
bundle.refined_invariants where status == "current"
```

Assign stable `invariant_index` values from `1` to `N` using the bundle order,
unless a deterministic sort is explicitly chosen before any work begins. If a
sort is chosen, record it in `run-metadata.json` and never change it mid-run.

Each queue line should include:

```json
{
  "invariant_index": 1,
  "total_invariants": 1954,
  "invariant_id": "cur-...",
  "title": "...",
  "subsystem": "...",
  "section": "...",
  "status": "current",
  "confidence": "high|medium|low|null",
  "evidence_files": [],
  "cluster_key": null
}
```

## Orchestrator Role

The parent agent owns accounting, artifact writes, and validation.

For each current invariant:

1. Load the queue entry and, when useful, fetch the full record through
  `get_invariant`.
2. Extract the invariant's statement, rationale, evidence files, source commits,
  suggested falsification tests, cluster key, and open questions.
3. Search the audited repo set for exact or near-exact implementation evidence.
4. If exact evidence is not found, search for renamed, moved, or structurally
  equivalent behavior in dependency repos.
5. If no mapping is found, perform a negative search pass across likely files,
  symbols, concepts, and evidence-file analogs before classifying a confirmed
   gap.
6. Write exactly one complete per-invariant JSON artifact.
7. Append one complete line to `index.jsonl`.
8. Append confirmed gaps to `confirmed-gaps.md`.
9. Update `progress.md` with completed counts and any correction history.

Investigators or subagents may help with searches, but the parent must not write
an artifact until the record is complete. Child output is evidence to inspect,
not a completed artifact by itself.

## Evidence Standard

Mapped invariants must cite concrete code.

Good evidence includes:

- destination repo path
- relevant symbol or function name
- concise destination snippet
- explanation of why the snippet enforces the invariant
- any linked verifier/builder/pool/RPC parity path needed for the invariant

For `mapped_in_dependency`, name the dependency repo and explain why that repo is
the correct owner of the invariant behavior in the v2.2.0 architecture.

For structural equivalence, prove behavior, not source shape. The equivalence
argument must address relevant guards, state transitions, side effects,
serialization or hash identity, rejection paths, and builder/verifier parity.

Confirmed gaps must also cite evidence.

Good gap evidence includes:

- checked repos
- checked paths
- checked symbols or search queries
- likely implementation locations examined
- related code that is present but insufficient
- the exact missing behavior
- the smallest test or scenario that would expose the gap, when one can be
formulated

Do not classify a gap merely because the first search failed.

## Mapping Status Semantics

Use exactly one of these statuses in completed artifacts:

- `mapped_in_port`: the invariant is implemented in
`/home/ritual/repos/ritual-reth-internal-v2.2.0-port`
- `mapped_in_dependency`: the invariant is implemented in one of the audited
dependency repos
- `confirmed_gap`: the invariant is not implemented in the audited repo set, and
negative search evidence supports the finding

Do not use:

- `not_applicable_to_port`
- `blocked`
- `needs_review`
- `partial`
- `unknown`
- `deferred`
- `pending`

If the agent cannot prove a mapping or a gap, the invariant is not done. Continue
investigating before writing the artifact.

## Search Guidance

Start with precise evidence from the invariant record:

- `evidence_files`
- `statement`
- `title`
- `rationale`
- `suggested_falsification_tests`
- `source_commits`
- `cluster_key`

Use exact-code-first search:

1. Search destination repos for evidence-file path fragments and filename
  analogs.
2. Search for symbols, constants, enum variants, method names, RPC names,
  precompile addresses, selectors, error names, and event names.
3. Search for statement-specific behavior words only after symbol/path searches.
4. Use MCP `invariants_for_symbol` or `relevance_signals` to find neighboring
  concepts when the invariant is broad.
5. Read the smallest relevant code ranges needed to prove or disprove the claim.

Avoid broad semantic claims without code evidence.

## Risk Guidance

Be especially strict for invariants involving:

- async FSM state, settlement, fulfillment, delivery, replay, expiry, cleanup, or
canonical commitments
- scheduled transaction identity, predicates, missed obligations, block math, or
verifier parity
- precompile dispatch, registry metadata, allowlists, capabilities, pricing, gas,
and wallet behavior
- payload building, block verification, engine validation, execution, txpool, and
RPC result submission
- transaction encoding, hashing, signing, sender recovery, or storage identity
- heartbeat tracking, hydration, revival, owner reads, and deduplication
- negative paths: malformed inputs, duplicate handling, stale state, expiry,
wrong executor, verifier-builder disagreement, and fail-closed behavior

For these invariants, a mapping must prove both the happy path and the relevant
failure or rejection path.

## Per-Invariant Artifact Schema

Each completed invariant writes one JSON object to:

`invariants/invariant-####.json`

```json
{
  "record_type": "invariant_mapping",
  "invariant_index": 1,
  "total_invariants": 1954,
  "invariant_id": "cur-...",
  "title": "...",
  "subsystem": "...",
  "section": "...",
  "status": "current",
  "confidence": "high",
  "cluster_key": "...",
  "statement": "...",
  "rationale": "...",
  "evidence_files": [],
  "source_commits": [],
  "suggested_falsification_tests": [],
  "mapping_status": "mapped_in_port|mapped_in_dependency|confirmed_gap",
  "mapped_repos": [],
  "destinations": [
    {
      "repo": "/home/ritual/repos/ritual-reth-internal-v2.2.0-port",
      "branch": "spencer/2605-reth-upstream-merge",
      "commit": "...",
      "path": "crates/...",
      "symbols": ["..."],
      "snippet": "small destination snippet",
      "evidence": "why this code enforces the invariant"
    }
  ],
  "equivalence_argument": "required for non-trivial or moved mappings",
  "negative_search_evidence": {
    "checked_repos": [],
    "checked_paths": [],
    "checked_symbols": [],
    "checked_queries": [],
    "related_but_insufficient_code": [],
    "missing_behavior": null
  },
  "test_or_falsification_candidate": "...",
  "summary": "one concise sentence",
  "notes": "short rationale"
}
```

For `mapped_in_port` and `mapped_in_dependency`:

- `destinations` must be non-empty
- each destination must cite path-level evidence
- `negative_search_evidence.missing_behavior` should be `null`

For `confirmed_gap`:

- `destinations` should be empty unless citing related-but-insufficient code
- `negative_search_evidence` must be populated
- `negative_search_evidence.missing_behavior` must describe the exact gap
- the gap must also appear in `confirmed-gaps.md`

## Index Schema

Append one JSON object per completed invariant to `index.jsonl`:

```json
{
  "invariant_index": 1,
  "invariant_id": "cur-...",
  "title": "...",
  "subsystem": "...",
  "mapping_status": "mapped_in_port",
  "mapped_repos": ["/home/ritual/repos/ritual-reth-internal-v2.2.0-port"],
  "artifact": "invariants/invariant-0001.json",
  "summary": "one concise sentence"
}
```

The index must be derivable from the per-invariant artifacts. If the index and
artifact disagree, the artifact is authoritative and the index must be corrected.

## Confirmed Gaps Format

For every `confirmed_gap`, append a concise entry to `confirmed-gaps.md`:

```text
## invariant-0001 cur-...

- Title: ...
- Subsystem: ...
- Missing behavior: ...
- Checked repos: ...
- Likely owner: ...
- Falsification candidate: ...
- Artifact: invariants/invariant-0001.json
```

Do not report confirmed gaps only in prose. Every gap must be keyed back to its
artifact.

## Child Investigator Prompt Template

Use this template when delegating one invariant. Child investigators should be
read-only.

```text
You are investigating one current Ritual Reth invariant for the v2.2.0 port
invariant audit.

Parent accounting:
- invariant_index: {INVARIANT_INDEX}
- total_invariants: {TOTAL_INVARIANTS}
- invariant_id: {INVARIANT_ID}
- title: {TITLE}
- subsystem: {SUBSYSTEM}

Invariant record:
```json
{INVARIANT_RECORD_JSON}
```

Audited repos:

- /home/ritual/repos/ritual-reth-internal-v2.2.0-port
- /home/ritual/repos/ritual-reth-nodebuilder-internal
- /home/ritual/repos/ritual-alloy-internal
- /home/ritual/repos/ritual-alloy-evm-internal
- /home/ritual/repos/ritual-revm-internal
- /home/ritual/repos/ritual-revm-inspectors-internal
- /home/ritual/repos/ritual-node-internal

Execution constraints:

- Use only the local filesystem under /home/ritual/repos.
- Do not SSH to any host, including spencer-tdxbox-3.
- Do not use network access or fetch remote branches.
- Do not request elevated, dangerous, or manual permissions.
- If required evidence is not available locally, report the local searches and
absence as negative evidence.

Your task:

1. Search for exact or near-exact implementation evidence first.
2. If exact evidence is absent, search for renamed, moved, or structurally
  equivalent behavior in all audited repos.
3. If no mapping is found, perform a negative search pass across likely paths,
  symbols, and concepts.
4. Return evidence only. Do not modify code. Do not write artifacts.
5. Do not return blocked, needs-review, partial, unknown, or not-applicable
  statuses. If you cannot finish, return the searches performed and the next
   concrete searches needed; the parent will continue before writing an artifact.

Return JSON:

```json
{
  "invariant_index": {INVARIANT_INDEX},
  "invariant_id": "{INVARIANT_ID}",
  "proposed_mapping_status": "mapped_in_port|mapped_in_dependency|confirmed_gap",
  "destinations": [],
  "equivalence_argument": null,
  "negative_search_evidence": {
    "checked_repos": [],
    "checked_paths": [],
    "checked_symbols": [],
    "checked_queries": [],
    "related_but_insufficient_code": [],
    "missing_behavior": null
  },
  "test_or_falsification_candidate": null,
  "summary": "one concise sentence",
  "notes": "short rationale"
}
```

```

The parent must validate child output before writing the final artifact.

## Validation Checklist

Before considering the run complete, verify:

- `queue.current-invariants.jsonl` contains exactly the fetched count of current
  refined invariants
- `invariants/` contains exactly one JSON file per queue entry
- files are named `invariant-0001.json` through `invariant-NNNN.json` with no
  gaps
- every artifact has matching `invariant_index`, `total_invariants`,
  `invariant_id`, title, subsystem, and `status: "current"` from the queue
- every artifact has exactly one `mapping_status`
- every `mapping_status` is one of `mapped_in_port`, `mapped_in_dependency`, or
  `confirmed_gap`
- there are no artifacts containing `blocked`, `needs_review`, `partial`,
  `unknown`, `deferred`, `pending`, or `not_applicable_to_port`
- every mapped artifact has at least one destination with repo, branch, commit,
  path, snippet, and evidence
- every dependency mapping names one of the audited dependency repos
- every non-trivial or moved mapping has an equivalence argument
- every confirmed gap has populated negative search evidence and appears in
  `confirmed-gaps.md`
- `index.jsonl` has exactly one line per artifact and agrees with the artifacts
- `validation-summary.json` reports counts by subsystem, mapping status, mapped
  repo, confidence, and confirmed gap likely owner

## Validation Summary Schema

Write `validation-summary.json`:

```json
{
  "record_type": "invariant_audit_validation_summary",
  "atlas_generated": "YYYY-MM-DD",
  "total_current_invariants": 1954,
  "artifacts_total": 1954,
  "missing_artifacts": [],
  "duplicate_invariant_ids": [],
  "invalid_status_artifacts": [],
  "counts_by_mapping_status": {
    "mapped_in_port": 0,
    "mapped_in_dependency": 0,
    "confirmed_gap": 0
  },
  "counts_by_subsystem": {},
  "counts_by_repo": {},
  "confirmed_gaps_total": 0,
  "repo_revisions": [
    {
      "repo": "/home/ritual/repos/ritual-reth-internal-v2.2.0-port",
      "branch": "spencer/2605-rum-iot",
      "commit": "..."
    }
  ],
  "status": "complete"
}
```

`status` may be `complete` only if the validation checklist passes.

## Scope Boundary

This pass is an audit and mapping pass only. Do not modify implementation code
while building the invariant map. If an invariant is a confirmed gap, record it
precisely in the artifact and `confirmed-gaps.md`; do not fix it during this
pass unless the user explicitly changes the scope.