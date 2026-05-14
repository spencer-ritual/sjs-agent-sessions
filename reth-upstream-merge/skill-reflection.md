# Skill Reflection

## Queue Index Cross-Check Before Delegation

- Trigger: During the fresh-restart Reth coverage audit, a delegated prompt was initially launched with `file_index = 84` for `crates/ethereum/node/src/spc.rs`, but the authoritative queue showed `file-0084` was `crates/ethereum/node/src/payload.rs` and `spc.rs` was `file-0085`.
- Existing gap: The castle/orchestrator loop emphasized persisted JSON validation after child output, but did not make pre-delegation queue/index/source-path cross-check explicit enough for long batch audits.
- Candidate update: Before launching a file-scoped audit or persisting a child result, verify `file_index`, `source_status`, and `source_path` against the source queue using file tools; discard or relabel any child result whose parent accounting does not match the queue.
- Scope: Long-running coverage/audit orchestration with stable per-file artifact numbering, especially when many subagents run in parallel.
- Evidence: The mismatch was caught before any bad `files/file-0084.json` artifact was written; the corrected prompts split `file-0084` as `crates/ethereum/node/src/payload.rs` and `file-0085` as `crates/ethereum/node/src/spc.rs`.
- Promotion status: Not promoted yet

## File Tools As Coverage Authority

- Trigger: The same audit had prior evidence that shell validation once returned impossible empty success, while `Glob`/`ReadFile` consistently reflected the durable artifact set.
- Existing gap: The workflow allowed shell for convenience but did not explicitly require file-tool cross-checks after every batch when shell had already shown flakiness.
- Candidate update: In coverage-map tasks, if shell validation is known flaky, use `Glob` for artifact count and `ReadFile` for representative records plus `validation-summary.json` before reporting progress.
- Scope: Coverage accounting and artifact-generation tasks where progress is persisted files, not command output.
- Evidence: Durable progress was reported only after `Glob` confirmed file counts and `ReadFile` confirmed `validation-summary.json` and representative `file-####.json` contents.
- Promotion status: Not promoted yet

## Artifact Root Versus Per-File Subdirectory

- Trigger: During the fresh-restart coverage audit, the user asked where the generated records were and whether they should all be under `/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge/coverage-map-fresh-restart-gpt55`.
- Existing gap: Progress updates said records were persisted under the run directory but did not always spell out that per-file JSON artifacts live one level deeper in `coverage-map-fresh-restart-gpt55/files/`, while metadata lives at the run root.
- Candidate update: When reporting coverage-map progress or artifact locations, always state both the run root and the per-file record directory: root metadata at `<run>/`, per-file records at `<run>/files/file-####.json`.
- Scope: Long-running coverage/audit tasks with a root artifact directory plus nested completion surface.
- Evidence: `Glob` confirmed `validation-summary.json`, `index.jsonl`, `review-queue.md`, and `progress.md` at the run root, and 96 per-file records under `coverage-map-fresh-restart-gpt55/files/`.
- Promotion status: Not promoted yet
