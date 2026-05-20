# Agent Prompt: tx-origin Refactor Bundle (Chunk 0)

Copy the section between the `---` markers below into a fresh agent session. The agent should
not need any other context.

---

## Task

Implement chunk 0 of `TX_ORIGIN_PRECOMPILE_VULNERABILITY_IMPLEMENTATION_PLAN_V2.md` — the
non-breaking refactor bundle that lands before any semantic work on the tx-origin precompile
vulnerability fix. Do **not** touch chunks 1–8 (the semantic work). Stop after chunk 0 is
merged and report status.

## Required reading (in this order)

Read all four docs end-to-end before starting. They are the source of truth; this prompt is
only the operational wrapper.

1. `/home/ritual/repos/sjs-agent-sessions/pre-tx-origin/CLAIM_MAPPING_POST_REFACTOR.md` —
   audit of the current code state. Tells you where every file and symbol lives today.
2. `/home/ritual/repos/sjs-agent-sessions/pre-tx-origin/TX_ORIGIN_PRECOMPILE_VULNERABILITY_V2.md` —
   status doc. Read the "Ambiguities → Resolved" section in particular; those are locked
   decisions you are bound by.
3. `/home/ritual/repos/sjs-agent-sessions/pre-tx-origin/REFACTORING_FOR_SYMMETRY.md` —
   the refactor rationale, the Decisions Locked block at the top, and each Refactor A–E
   section.
4. `/home/ritual/repos/sjs-agent-sessions/pre-tx-origin/TX_ORIGIN_PRECOMPILE_VULNERABILITY_IMPLEMENTATION_PLAN_V2.md` —
   the implementation plan. Chunk 0 is your full scope.

If anything in this prompt disagrees with those docs, the docs win.

## Scope

Chunk 0 has five sub-steps. Land in this order:

- 0.D — Consolidate precompile address registries
- 0.E — Unified precompile inventory
- 0.A + 0.B — Together (tightly coupled, see below)
- 0.C — Doc-comments / rename

### Important: 0.A and 0.B are intertwined

Refactor A introduces `commitment_job_sender(commitment_tx) -> Result<JobSender, _>` in
`reth-ritual-async-fees`. The return type `JobSender` is defined by Refactor B in
`reth-ritual-async-registry`. You cannot land 0.A without 0.B's type, and 0.B is hollow
without 0.A's decoder consumer. Treat 0.A + 0.B as a single PR. Within that PR, land 0.B's
type definition first (a few commits in), then 0.A's `commitment_job_sender`, then the
verifier-site switch-over and the `extract_commitment_sender` deletion as separate commits.

## Repo state

Work happens across three repos, all in `/home/ritual/repos/`:

- `ritual-reth-internal/` — branch `spencer/precomp-msg-sender-rerefresh`. Most of chunk 0
  lives here.
- `ritual-reth-nodebuilder-internal/` — branch `spencer/precomp-msg-sender-rerefresh`.
  Affected by 0.D's removal of duplicate address constants if any get re-exported through
  here, and by 0.E's potential restructuring of where sync precompile address constants
  live.
- `ritual-alloy-internal/` — branch `spencer/precomp-msg-sender-rerefresh`. The canonical
  home for both 0.D's address allowlist and 0.E's new inventory.

Confirm all three repos are on `spencer/precomp-msg-sender-rerefresh` before starting. If any
is not, stop and ask the operator — do not silently switch branches or pull foreign work.

Do not modify any other repo without an explicit decision in your status note explaining why.

## Per-sub-step constraints

### 0.D — Registry consolidation

- Wire `ritual-reth-internal` to depend on
  `ritual-alloy-internal/crates/ritual-precompile-addresses`. Add the dependency in the
  affected `Cargo.toml`s using a workspace path or registry version, matching the convention
  in the workspace `Cargo.toml`.
- Delete the local duplicate at `crates/ritual/async-fees/src/constants.rs:103-169` (the
  precompile address constants block — keep the fee-calculation constants below it).
- Delete the local duplicate at `crates/ritual/async-inspector/src/inspector.rs:12-44`.
- Rewrite the 11-way `||` chain at `crates/ritual/async-inspector/src/inspector.rs:162-173`
  as `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES.contains(&inputs.target_address)`.
- Behavior must be **exactly** preserved. If `cargo test` produces any diff in passing tests,
  stop and investigate.

### 0.E — Unified inventory

- Add `PrecompileFamily` enum and `RITUAL_ALL_PRECOMPILE_ADDRESSES: &[(Address, &'static str,
  PrecompileFamily)]` to `ritual-alloy-internal/crates/ritual-precompile-addresses/src/lib.rs`.
- Use the complete inventory in `REFACTORING_FOR_SYMMETRY.md` section "Complete current
  inventory" — 11 async + 7 sync = 18 entries.
- Sync precompile addresses currently live in
  `ritual-reth-nodebuilder-internal/crates/precompiles/src/{onnx,jq,sigver,test_nondeterministic,tx_hash}.rs`.
  Either move those constants into `ritual-precompile-addresses` and have the implementations
  `use` them, or have `ritual-precompile-addresses` `use` them from the nodebuilder crate —
  whichever does **not** create a dependency cycle. Verify with `cargo check` from the
  workspace root before committing.
- Add the three exhaustiveness unit tests described in `REFACTORING_FOR_SYMMETRY.md` Refactor
  E (pairwise distinct, async subset equality, two-phase subset equality). The
  "every implementation file's `_ADDRESS` constant appears in the list" test mechanism is
  one of the open ambiguities — use a hand-maintained companion test for now and add a TODO
  comment pointing to that open question.

### 0.A + 0.B — Helper + newtype, together

Order of commits within the PR:

1. Define `JobSender(Address)` in `crates/ritual/async-registry/src/lib.rs` (or new
   `src/job_sender.rs`). Provide `from_storage`, `from_caller`, `as_address`. Do **not**
   add `Cargo.toml` deps to `async-registry`; the leaf-property comment at
   `Cargo.toml:16-20` is load-bearing.
2. Convert `SettlementData.sender: Address` → `SettlementData.sender: JobSender` at
   `async-registry/src/lib.rs:126-155`. Update `read_jobs_for_settlement(...)` in
   `ritual-reth-nodebuilder-internal/crates/node/src/payload.rs:3408-3478` to wrap the
   storage-read address via `JobSender::from_storage(...)`.
3. Add `reth_ritual_async_fees::commitment_job_sender(commitment_tx) -> Result<JobSender,
   CommitmentDecodeError>` in `crates/ritual/async-fees/src/wallet.rs` (or a new module).
   This decodes `Job.sender` from the `addJob` call's calldata using `alloy-sol-types`. If
   `CommitmentDecodeError` does not already exist, add it as a `thiserror` type in
   `async-fees`.
4. Replace `extract_commitment_sender(...)` callers with `commitment_job_sender`:
   - `crates/ritual/block-verification/src/lib.rs:1073-1087`
     (`verify_async_commitments_pre_execution`).
   - `crates/ritual/block-verification/src/nonce_lock.rs:43-52` (`verify_nonce_locks`).
     Also remove the special-case skip for scheduled commitments at `:38-40`.
5. Switch dedup maps to `HashMap<JobSender, _>` in both verifier passes.
6. **Delete** `extract_commitment_sender` (`crates/ritual/async-fees/src/wallet.rs:508-528`)
   and its `lib.rs` re-export (`crates/ritual/async-fees/src/lib.rs:49`). Before deletion,
   run `rg extract_commitment_sender` workspace-wide and confirm no consumer remains. If any
   are found outside the two verifier paths above, route them through `commitment_job_sender`
   in this PR. Do **not** leave the old symbol as `#[deprecated]`.

Constraints:

- After this PR, the workspace must build with no behavior change vs the pre-PR tip. The
  on-chain commitment sender semantics are still the old metadata-derived rule because
  detector Step 10 is unchanged; that is correct and expected at the end of chunk 0.
- Do not touch `crates/ritual/async/src/detector.rs` Step 10 (`:1458-1471`), the
  `AsyncCallResult` struct (`:663-678`), or `AsyncCallResult::new` (`:687-708`) in this PR.
  Those edits belong to chunk 1.

### 0.C — Doc-comments / rename

- Add doc-comments to `scheduled_caller`, `async_settlement_user_address`
  (`crates/ritual/async/src/detector.rs`) and to `RpcSimulationResult.sender`
  (`detector.rs:204`) stating: "Transaction-level caller, for logging / RPC / heartbeat
  handling. NOT the async job owner. For ownership use `JobSender` (or
  `AsyncCallResult::job_sender`)."
- Do **not** rename `scheduled_caller` to `scheduled_tx_caller`. That decision is parked on
  the chunk-6 RPC rename and is an open ambiguity. Leave a TODO comment in the doc-string
  pointing to the chunk-6 decision.

## PR structure

Open four PRs against `spencer/precomp-msg-sender-rerefresh`, in order. Wait for each to
merge before opening the next. Title each one with the sub-step letter for traceability:

1. `[refactor 0.D] Consolidate precompile address registries`
2. `[refactor 0.E] Add RITUAL_ALL_PRECOMPILE_ADDRESSES inventory`
3. `[refactor 0.A+0.B] Introduce JobSender newtype and commitment_job_sender; delete extract_commitment_sender`
4. `[refactor 0.C] Doc-comments on transaction-level sender helpers`

Each PR body should:
- Link to the relevant section of `REFACTORING_FOR_SYMMETRY.md` and
  `TX_ORIGIN_PRECOMPILE_VULNERABILITY_IMPLEMENTATION_PLAN_V2.md` for the reviewer.
- Note explicitly which Decisions Locked items it implements.
- Include the verification command output (or a brief summary if it's long).
- Confirm "behavior unchanged" with a one-line argument for each sub-step.

## Verification per sub-step

Run from the relevant crate's directory unless noted otherwise:

- 0.D: `cargo test -p ritual-precompile-addresses`, `cargo build -p reth-ritual-async-inspector`,
  `cargo build -p reth-ritual-async-fees`. Then `cargo build` from the `ritual-reth-internal`
  workspace root to confirm nothing else broke.
- 0.E: `cargo test -p ritual-precompile-addresses` (covers the new exhaustiveness tests).
  Then full workspace `cargo build` in any repo whose precompile constants moved.
- 0.A+0.B: `cargo build` workspace-wide, then
  `cargo test -p reth-ritual-async-registry`,
  `cargo test -p reth-ritual-async-fees`,
  `cargo test -p reth-ritual-block-verification`,
  `cargo test -p reth-ritual-async`. After all pass, search for any remaining
  `extract_commitment_sender` references workspace-wide and confirm the count is zero.
- 0.C: no mechanical verification; documentation hygiene only.

## When to stop and ask

Stop and ask the operator if any of these happen:

- Any of the three repos is not on `spencer/precomp-msg-sender-rerefresh` when you start.
- `cargo test` shows a regression on the pre-refactor tip (file an issue note before
  blaming your change).
- `extract_commitment_sender` has consumers outside the two verifier paths and you cannot
  determine whether they are safe to route through `commitment_job_sender`.
- Sync precompile address moves create a Cargo dependency cycle no matter which direction
  you point the dep.
- The `ritual-precompile-addresses` crate is not actually wired into the `ritual-reth-internal`
  workspace and adding it as a path dep does not work (e.g. the workspace Cargo.toml needs a
  members entry).
- Any locked decision in `REFACTORING_FOR_SYMMETRY.md` would be violated to make a sub-step
  work.

In all of those cases, do not improvise. Write a short note in the agent-sessions directory
explaining the conflict and stop.

## Output expectations

When you stop (either because all four PRs merged, or because you hit an escalation case),
write a status note to
`/home/ritual/repos/sjs-agent-sessions/pre-tx-origin/CHUNK_0_STATUS.md` with:

- Which sub-steps completed, with PR links.
- Which sub-steps are blocked, with the blocker described.
- Any new ambiguities you surfaced that are not already in
  `TX_ORIGIN_PRECOMPILE_VULNERABILITY_V2.md` "Ambiguities → Open."
- Any deviations from the plan, with justification. Deviations are not forbidden but they
  must be visible.

That status note becomes the handoff to whoever picks up the semantic chunks (1–8) next.
