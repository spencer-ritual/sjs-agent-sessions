# Refactors to Reduce Builder / Verifier Divergence Risk

After the main fix in `TX_ORIGIN_PRECOMPILE_VULNERABILITY_IMPLEMENTATION_PLAN_V2.md`, three call
sites have to agree on "the sender of a commitment": detector commitment write,
`verify_async_commitments_pre_execution`, and `verify_nonce_locks`. The current code has already
demonstrated that two such sites can drift (see `nonce_lock.rs:43-52` using `original_tx.sender()`
while `verify_async_commitments_pre_execution` uses `extract_commitment_sender`). The refactors
below exist to shrink the divergence surface so a future change cannot quietly re-introduce a
different rule.

Backing audit: `CLAIM_MAPPING_POST_REFACTOR.md`.

## Decisions Locked

The following decisions have been made and are reflected throughout this document and the
implementation plan:

- **All five refactors (A–E) will be done.** Cost is accepted in exchange for closing the
  divergence surfaces enumerated below.
- **All five refactors are non-breaking** (behavior-preserving for A and D, additive for B and
  E, doc-only for C). They land **before** the semantic chunks of the main plan, bundled into
  one refactor-only group at chunk 0 of the implementation plan, in the order D → E → A → B → C
  (justification below).
- **JobSender newtype placement.** The type itself plus its storage-side constructor lives in
  `reth-ritual-async-registry` (the lower-graph crate; see its `Cargo.toml:16-20` comment
  marking it a pure leaf). The calldata-decoding constructor stays in `reth-ritual-async-fees`
  as a free function `commitment_job_sender(commitment_tx) -> Result<JobSender>`, because the
  decoder needs `alloy-sol-types` / `ethabi` deps that the leaf intentionally avoids.
- **`extract_commitment_sender` is retired entirely** (deleted, not deprecated) once
  `commitment_job_sender` is wired into both verifier passes. The current dual-rule drift
  between `extract_commitment_sender` and `nonce_lock.rs::original_tx.sender()` is the
  divergence we are closing; leaving the old helper around is exactly the failure mode we want
  to prevent.
- **Inspector allowlist semantics.** We adopt "SPC-verified == all async precompiles" as an
  explicit invariant. The inspector consumes
  `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES.contains(...)` directly. If a future async
  precompile is added that should *not* be SPC-block-verified, that is a deliberate change
  requiring updates to both the allowlist name and the inspector — i.e. it has to be visible.
- **`RITUAL_ALL_PRECOMPILE_ADDRESSES` placement.** Lives in
  `ritual-alloy-internal/crates/ritual-precompile-addresses` (canonical home for addresses).
  Sync precompile address constants either move there or get `use`-imported by the alloy crate
  to keep one source of truth; the implementation files themselves stay in
  `ritual-reth-nodebuilder-internal/crates/precompiles/`.
- **Refactor D lands first within the refactor bundle.** It is purely mechanical and
  behavior-preserving, and once the inspector switches from the hardcoded 11-way `||` chain to
  `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES.contains(...)`, every downstream refactor reads
  a cleaner choke point.
- **Migration window: hard cutover, no backwards compatibility.** Confirmed in the main status
  doc's Design Plan. There is no support for a coexistence period where old (metadata-sender)
  and new (`msg.sender`) commitments live on the same chain. This is a breaking change
  intentionally.

Open ambiguities still on the table (not blockers for refactor work, but blockers for chunk 6
and merge gating): RPC rename style (breaking vs additive aliases), `PrecompileConsumer`
client-facing migration scope, summit/consensus-layer coordination pass, fork-test/replay
infrastructure, and E2E regression bar. See `TX_ORIGIN_PRECOMPILE_VULNERABILITY_V2.md` for the
running list.

## Divergence Surfaces We Are Trying To Close

1. Sender-extraction rule drift across the two verifier passes (already present today) and any
   future builder pruning pass.
2. Field-vs-derivation drift: every consumer currently re-derives sender from
   `OriginalTransaction`, so each new commitment variant has to be handled in every site.
3. Type confusion: `AsyncCallResult.job_sender: Address` and `tx.signer() -> Address` are the
   same type, so a mis-targeted "fix" can swap them with no compile-time signal.
4. Precompile-address registry drift: the async precompile address list is duplicated across
   three places (canonical alloy crate, `async-fees/src/constants.rs`,
   `async-inspector/src/inspector.rs`). Adding a 12th precompile requires three edits; a missed
   inspector edit silently means the new precompile is never detected.
5. No unified Ritual precompile inventory: sync precompile addresses live as scattered per-file
   constants in `ritual-reth-nodebuilder-internal/crates/precompiles/`, with no aggregate that
   would let observability tooling or a new engineer enumerate the full set in one place.

## Refactor A: `Job.sender` becomes the only canonical surface, decoded once

The cleanest invariant available is that `Job.sender` on-chain is the truth. Every commitment tx
is an `addJob` call whose calldata already contains that field. After step 1 of the main plan,
that field holds the precompile caller. Therefore no consumer needs to "re-derive" sender from
`OriginalTransaction` ever again; they decode the `addJob` calldata.

Concrete change:

- Add `reth_ritual_async_fees::commitment_job_sender(commitment_tx) -> Result<JobSender>` that
  decodes `Job.sender` directly from the `addJob` call data on the commitment transaction.
  Returns the newtype introduced by Refactor B; lives in `async-fees` because decoding needs
  `alloy-sol-types` / `ethabi` deps the leaf `async-registry` intentionally avoids.
- Replace every call to `extract_commitment_sender` with `commitment_job_sender`. Currently:
  - `crates/ritual/block-verification/src/lib.rs:1073-1087`
    (`verify_async_commitments_pre_execution`)
  - `crates/ritual/async-fees/src/lib.rs:49` (re-export)
- Replace `original_tx.sender()` inside `crates/ritual/block-verification/src/nonce_lock.rs:43-52`
  with `commitment_job_sender`. Remove the special-case skip for scheduled commitments at
  `:38-40`: scheduled commitments now have a meaningful `Job.sender` too, and the unified rule
  applies uniformly.
- **Delete `extract_commitment_sender` entirely** (locked decision; see Decisions Locked
  section). Before deletion, run a workspace-wide `rg extract_commitment_sender` to confirm
  there are no consumers outside the verifier paths above; if any are found, route them
  through `commitment_job_sender` in the same PR. Do not leave the function `#[deprecated]` —
  the dual-rule drift it enables is the bug we are closing.

Why this is safe to land first:

The helper decodes the same `Job.sender` field that the detector currently writes from the
metadata cascade. Pre-step-1, `Job.sender` happens to equal whatever
`extract_commitment_sender` would have produced. Switching verifier consumers to read it
directly is behavior-preserving. After step 1 changes what the detector writes, every consumer
that goes through the helper picks up the new semantics automatically.

Cost: low. Verifier passes get simpler. Two distinct sender rules collapse into one.

Risk: low. The change is behavior-preserving until step 1 lands, at which point all consumers
move together.

## Refactor B: Newtype `JobSender(Address)` for compile-time enforcement

Make the type system carry the invariant that "job ownership" and "transaction-level signer"
are different concepts.

Concrete change:

- Define the newtype in `reth-ritual-async-registry` (lower in the dep graph than
  `async-fees`; the crate's `Cargo.toml:16-20` explicitly preserves it as a pure leaf with no
  `reth-ritual-*` / `alloy-ritual-*` deps). This is the placement that does not break the
  leaf property:

  ```rust
  // in async-registry/src/lib.rs (or a new src/job_sender.rs)
  #[derive(Clone, Copy, Debug, Eq, PartialEq, Hash, Ord, PartialOrd)]
  pub struct JobSender(Address);

  impl JobSender {
      /// Wrap an address read from on-chain `Job.sender` storage.
      pub fn from_storage(addr: Address) -> Self { Self(addr) }
      /// Wrap the inspector-captured `caller_address` at detection time.
      /// (Used by detector when constructing `AsyncCallResult.job_sender`.)
      pub fn from_caller(addr: Address) -> Self { Self(addr) }
      pub fn as_address(&self) -> Address { self.0 }
  }
  ```

- The decoding constructor — which needs ABI-decoding deps — lives in `async-fees` as a free
  function alongside Refactor A's helper:

  ```rust
  // in async-fees/src/wallet.rs (replaces extract_commitment_sender)
  pub fn commitment_job_sender(
      commitment_tx: &RitualTransactionSigned,
  ) -> Result<JobSender, CommitmentDecodeError> {
      // decode addJob(...) calldata, extract Job.sender field,
      // return JobSender::from_storage(decoded_addr).
  }
  ```

- Switch the following bare `Address` fields to `JobSender`:
  - `AsyncCallResult.job_sender` (the new field introduced in chunk 1 of the main plan).
  - `SettlementData.sender` in `crates/ritual/async-registry/src/lib.rs:126-155`.
- Switch dedup maps to `HashMap<JobSender, _>` in:
  - `crates/ritual/block-verification/src/lib.rs` (`verify_async_commitments_pre_execution`).
  - `crates/ritual/block-verification/src/nonce_lock.rs` (`verify_nonce_locks`).
  - Any nodebuilder builder-side pruning added under chunk 3 of the main plan, if needed.
- Leave plain `Address` (no wrapper) for transaction-level senders: `tx.signer()`,
  `scheduled_caller(...)`, `async_settlement_user_address(...)`,
  `RpcSimulationResult.tx_orig_sender`. The compiler will refuse to mix the two without an
  explicit coercion.

Cost: moderate. Likely 30–50 small mechanical edits across the three crates, mostly
type-driven; cargo flags every confusion site.

Risk: low. Type-only labeling; behavior is unchanged.

Sequencing: land in the same PR that introduces step 1's `job_sender` field, so the new type
arrives with its first real consumer.

## Refactor C: Doc-comment / rename transaction-level helpers

The transaction-level sender helpers look like they could be sources of async ownership at a
glance. Post-fix they are not, and that boundary should be visible.

Concrete change:

- Add `///` doc comments to the following functions stating clearly: "Returns the
  transaction-level caller for logging, RPC, and heartbeat handling. NOT the async job owner.
  For job ownership use `JobSender::from_commitment(...)` (or
  `AsyncCallResult::job_sender`)."
  - `crates/ritual/async/src/detector.rs::scheduled_caller`
  - `crates/ritual/async/src/detector.rs::async_settlement_user_address`
  - `crates/ritual/async/src/detector.rs::RpcSimulationResult::sender` field (if it stays named
    `sender`; if renamed via main-plan chunk 6 the new name is self-documenting)
- Optional: rename `scheduled_caller` to `scheduled_tx_caller` for symmetry with the renamed
  RPC field naming. Decide at the same time as chunk 6 of the main plan to keep one rename
  cycle.

Cost: trivial. Risk: zero. High readability payoff for the next reviewer landing in this code
cold.

## Refactor D: Collapse duplicated precompile-address registries

The set of async precompile addresses is currently defined in three places, with the inspector
copy hand-rolled as an 11-way `||` chain. A 12th precompile added in the future has to be added
in all three places or things silently break — the inspector failure mode is the worst, because
a missed update means the new precompile is never detected at all (no commitment, no
settlement, just executes and vanishes).

Concrete change:

- Wire `ritual-reth-internal` to depend on the canonical home,
  `ritual-alloy-internal/crates/ritual-precompile-addresses` (where the comment in
  `crates/ritual/async-fees/src/constants.rs:5` already says this is the intended path,
  pending the locked Alloy-stack precompile-address crate).
- Delete the local duplicate at `crates/ritual/async-fees/src/constants.rs:103-169` (the 11
  address constants, `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES`,
  `ALL_TWO_PHASE_PRECOMPILE_ADDRESSES`, and `is_two_phase_precompile`). If downstream callers
  expect the `async-fees` import path, re-export from `async-fees/src/lib.rs` instead of
  redefining.
- Delete the local duplicate at `crates/ritual/async-inspector/src/inspector.rs:12-44`.
  Replace the 11-way `||` chain at `:162-173` with
  `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES.contains(&inputs.target_address)`. This codifies
  the locked invariant **SPC-verified == all async precompiles**: if a future async precompile
  is added that should not be SPC-block-verified, the renaming and inspector divergence become
  a deliberate, visible decision rather than an accidental drift.

The canonical crate already has the two unit tests that should backstop this work:
`precompile_addresses_are_nonzero_and_pairwise_distinct` and
`two_phase_precompiles_are_subset_of_spc_verified_allowlist`
(`ritual-alloy-internal/crates/ritual-precompile-addresses/src/lib.rs:91-115`). After Refactor
D, every consumer in `ritual-reth-internal` and `ritual-reth-nodebuilder-internal` reads from
one allowlist, so adding a precompile is a single edit instead of a cross-repo audit.

Cost: low. Pure mechanical, no behavior change.

Risk: low. Behavior is preserved by construction; the local copies are already address-equal
to the canonical crate.

Sequencing: orthogonal to Refactors A/B/C. Land it whenever convenient — alongside Refactor A
is natural because both consolidate consensus-critical registries.

## Refactor E: Unified precompile inventory across sync and async families

There is currently no Rust file that lists every Ritual-specific precompile address. Async
addresses are in `ritual-alloy-internal/crates/ritual-precompile-addresses`; sync addresses are
scattered as per-precompile constants across `ritual-reth-nodebuilder-internal/crates/precompiles/src/`
with only individual re-exports in that crate's `lib.rs:17-21`. The address space is also
interleaved (sync at `0x009`, `0x100`, `0x101`, `0x800`, `0x803`, `0x804`, `0x830`; async at
`0x801`, `0x802`, `0x805–0x807`, `0x80C`, `0x818–0x81B`, `0x820`), so reading a hex address in
a log does not tell you which family it belongs to.

This is hygiene rather than consensus-critical — each sync precompile gas-meters itself, and
the consensus-critical async predicate (`is_spc_block_verified_precompile`) is unaffected by a
missing inventory. But it is a low-cost win for observability, admin tooling, debug logs, and
the "did I remember to wire this up everywhere?" question.

Concrete change:

- In `ritual-alloy-internal/crates/ritual-precompile-addresses/src/lib.rs`, add:

  ```rust
  pub enum PrecompileFamily {
      AsyncSinglePhase,    // HTTP, LLM, DKMS
      AsyncTwoPhase,       // long-running HTTP, ZK, FHE, Sovereign Agent,
                           // Image, Audio, Video, Persistent Agent
      Sync,                // ONNX, JQ, SigVer (ed25519, secp256r1), Nitro,
                           // TX_HASH
      TestOnly,            // TEST_NONDETERMINISTIC (env-gated)
  }

  pub const RITUAL_ALL_PRECOMPILE_ADDRESSES:
      &[(Address, &'static str, PrecompileFamily)] = &[
          // async single-phase
          (HTTP_CALL_PRECOMPILE,           "HTTP_CALL",           PrecompileFamily::AsyncSinglePhase),
          (LLM_CALL_PRECOMPILE,            "LLM_CALL",            PrecompileFamily::AsyncSinglePhase),
          (DKMS_KEY_PRECOMPILE,            "DKMS_KEY",            PrecompileFamily::AsyncSinglePhase),
          // async two-phase
          (LONG_RUNNING_HTTP_PRECOMPILE,   "LONG_RUNNING_HTTP",   PrecompileFamily::AsyncTwoPhase),
          (ZK_TWO_PHASE_PRECOMPILE,        "ZK_TWO_PHASE",        PrecompileFamily::AsyncTwoPhase),
          (FHE_PRECOMPILE,                 "FHE",                 PrecompileFamily::AsyncTwoPhase),
          (SOVEREIGN_AGENT_PRECOMPILE,     "SOVEREIGN_AGENT",     PrecompileFamily::AsyncTwoPhase),
          (IMAGE_CALL_PRECOMPILE,          "IMAGE_CALL",          PrecompileFamily::AsyncTwoPhase),
          (AUDIO_CALL_PRECOMPILE,          "AUDIO_CALL",          PrecompileFamily::AsyncTwoPhase),
          (VIDEO_CALL_PRECOMPILE,          "VIDEO_CALL",          PrecompileFamily::AsyncTwoPhase),
          (PERSISTENT_AGENT_PRECOMPILE,    "PERSISTENT_AGENT",    PrecompileFamily::AsyncTwoPhase),
          // sync (re-exported from nodebuilder addresses, or moved here)
          (SIGVER_ED25519_ADDRESS,         "SIGVER_ED25519",      PrecompileFamily::Sync),
          (SIGVER_SECP256R1_ADDRESS,       "SIGVER_SECP256R1",    PrecompileFamily::Sync),
          (NITRO_VERIFICATION_ADDRESS,     "NITRO_VERIFICATION",  PrecompileFamily::Sync),
          (ONNX_ADDRESS,                   "ONNX",                PrecompileFamily::Sync),
          (JQ_ADDRESS,                     "JQ",                  PrecompileFamily::Sync),
          (TX_HASH_ADDRESS,                "TX_HASH",             PrecompileFamily::Sync),
          // test-only
          (TEST_NONDETERMINISTIC_ADDRESS,  "TEST_NONDETERMINISTIC", PrecompileFamily::TestOnly),
      ];
  ```

- Move the sync precompile address constants into the same crate (or re-export them from
  there), so the inventory references the same constants the implementations use. The sync
  implementations themselves can stay in
  `ritual-reth-nodebuilder-internal/crates/precompiles/src/` and just `use` the addresses.
- Add a unit test in `ritual-precompile-addresses` that asserts:
  - All addresses in `RITUAL_ALL_PRECOMPILE_ADDRESSES` are pairwise distinct.
  - The subset filtered by `PrecompileFamily::AsyncSinglePhase | AsyncTwoPhase` equals
    `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES` as a set.
  - The subset filtered by `PrecompileFamily::AsyncTwoPhase` equals
    `ALL_TWO_PHASE_PRECOMPILE_ADDRESSES`.
  - Every implementation file's `_ADDRESS` constant appears somewhere in the list (this last
    one needs a small build-time script or a hand-maintained companion test; the value is
    that "did anyone add a precompile and forget to register it" becomes a single failing
    test).

### Complete current inventory (so nothing is forgotten)

**Async precompiles, 11 total** (implementations in
`ritual-revm-internal/crates/precompile/src/*.rs`, gated by `async-context` feature):

| Address | Constant | File | Family |
|---|---|---|---|
| `0x801` | `HTTP_CALL_PRECOMPILE` | `http_call.rs` | single-phase |
| `0x802` | `LLM_CALL_PRECOMPILE` | `llm_call.rs` | single-phase |
| `0x805` | `LONG_RUNNING_HTTP_PRECOMPILE` | `long_running_http_call.rs` | two-phase |
| `0x806` | `ZK_TWO_PHASE_PRECOMPILE` | `zk_two_phase.rs` | two-phase |
| `0x807` | `FHE_PRECOMPILE` | `fhe_call.rs` | two-phase |
| `0x80C` | `SOVEREIGN_AGENT_PRECOMPILE` | `sovereign_agent.rs` | two-phase |
| `0x818` | `IMAGE_CALL_PRECOMPILE` | `image_call.rs` | two-phase |
| `0x819` | `AUDIO_CALL_PRECOMPILE` | `audio_call.rs` | two-phase |
| `0x81A` | `VIDEO_CALL_PRECOMPILE` | `video_call.rs` | two-phase |
| `0x81B` | `DKMS_KEY_PRECOMPILE` | `dkms_key.rs` | single-phase |
| `0x820` | `PERSISTENT_AGENT_PRECOMPILE` | `persistent_agent.rs` | two-phase |

**Sync precompiles, 7 total** (implementations in
`ritual-reth-nodebuilder-internal/crates/precompiles/src/*.rs`):

| Address | Constant | File | Notes |
|---|---|---|---|
| `0x009` | `SIGVER_ED25519_ADDRESS` | `sigver.rs` | ed25519 verification |
| `0x100` | `SIGVER_SECP256R1_ADDRESS` | `sigver.rs` | secp256r1 verification |
| `0x101` | `NITRO_VERIFICATION_ADDRESS` | `sigver.rs` | AWS Nitro attestation |
| `0x800` | `ONNX_ADDRESS` | `onnx.rs` | ONNX inference |
| `0x803` | `JQ_ADDRESS` | `jq.rs` | jq JSON query |
| `0x804` | `TEST_NONDETERMINISTIC_ADDRESS` | `test_nondeterministic.rs` | testing only, env-gated by `RITUAL_ENABLE_TEST_NONDETERMINISTIC_PRECOMPILE` |
| `0x830` | `TX_HASH_ADDRESS` | `tx_hash.rs` | returns current tx hash |

Standard upstream EVM precompiles (ecrecover at `0x01`, sha256 at `0x02`, modexp, bn254, bls12-381,
kzg point evaluation, etc.) come from upstream revm in
`ritual-revm-internal/crates/precompile/src/`. They are out of Ritual-specific scope; the
inventory should not duplicate them, but its doc-comment should call out that "standard EVM
precompiles at addresses `0x01–0x0A` and `0x0F–0x14` come from upstream revm and are not listed
here."

Cost: low. One new enum, one new array, two or three unit tests, and a small audit pass to
make sure no sync precompile is missed. The sync address constants either move to
`ritual-precompile-addresses` or stay where they are with `use` statements.

Risk: low. Pure additive change; existing consumers of `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES`
and `ALL_TWO_PHASE_PRECOMPILE_ADDRESSES` are unaffected.

Sequencing: independent of A/B/C/D. Cheapest to land alongside Refactor D since both touch
`ritual-precompile-addresses`.

## Slot-In Into the Main Plan

Locked: all five refactors are non-breaking and land **first** in `TX_ORIGIN_PRECOMPILE_VULNERABILITY_IMPLEMENTATION_PLAN_V2.md`,
bundled into a single chunk 0, in the order D → E → A → B → C. Semantic chunks 1–8 follow
unchanged in intent (but adjusted for what the refactors did).

Order rationale:

1. **D first** (registry consolidation). Pure mechanical, behavior-preserving. Once the
   inspector reads its allowlist from a single canonical constant, every subsequent refactor
   touches a cleaner choke point.
2. **E second** (unified inventory). Additive on top of D and easy to land once D's canonical
   home is in place. Independent of A/B/C.
3. **A third** (commitment_job_sender helper; delete `extract_commitment_sender`).
   Behavior-preserving until chunk 1 lands. Routes both verifier passes through one rule.
4. **B fourth** (JobSender newtype in `async-registry` + decoder in `async-fees`). Lands the
   compile-time guard the rest of the plan relies on.
5. **C fifth** (doc-comments / optional rename). Trivial; lands at the end of the bundle to
   sweep up nomenclature in the same code-review pass.

Effects on semantic chunks (unchanged in intent, adjusted for refactor outcomes):

- **Chunk 1** uses `JobSender` for the new field. `create_commitment_tx` writes
  `job_sender.as_address()` into the `addJob` call's `Job.sender`.
- **Chunk 4** shrinks meaningfully. Both verifier passes already call `commitment_job_sender`
  after Refactor A; chunk 4 becomes "confirm both passes consume the new sender semantics and
  tighten any remaining tests." The chunk no longer has to choose between two ways to source
  the sender — that choice was made in Refactor A.
- **Chunk 6** picks up the rename portion of Refactor C if we choose the optional
  `scheduled_caller` → `scheduled_tx_caller` rename. Decide that bundling at chunk 6 time.
- **Chunk 7** adds one property test: for any commitment the verifier accepts, builder
  pruning's `commitment_job_sender(commitment_tx)` equals the verifier's. Trivial once
  Refactor B's newtype exists; high value as a regression fence.

## Net Effect on Plan Risk

Before refactor:

- Three call sites for "the sender of a commitment," two pre-existing sender rules, ambient
  drift risk on every future commitment-variant change. Builder/verifier symmetry held by code
  review.
- Three duplicate copies of the async precompile address list. Adding a 12th precompile
  requires three edits; missing the inspector silently means the new precompile is never
  detected at all.
- No single inventory of Ritual-specific precompile addresses. Adding a new sync precompile is
  effectively undiscoverable from any one entry point.

After refactor:

- One sender helper. One newtype. The compiler enforces ownership-vs-signer distinction. A
  future commitment variant has exactly one place that needs an update
  (`commitment_job_sender`'s decoder), and every consumer follows automatically. Symmetry held
  by the type system.
- One canonical precompile address registry. Adding a 12th precompile is a single edit; the
  inspector picks it up by allowlist membership, and the existing unit tests fail loudly on
  any mismatch.
- One unified inventory covering both async and sync precompile families, with family
  classification and exhaustiveness tests. Observability and admin tooling can iterate over a
  single source.

The cost is one consolidated refactor chunk (A, B, C) and one or two adjacent
registry-cleanup chunks (D, E), all mostly mechanical work landable safely ahead of the
semantic fix. The trade-off is favorable on the time horizon a consensus-critical invariant
typically needs to survive.
