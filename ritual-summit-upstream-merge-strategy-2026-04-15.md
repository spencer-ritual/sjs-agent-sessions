# Ritual Summit Upstream Merge Strategy

## Purpose

This document is a working playbook for doing an upstream merge from `SeismicSystems/summit` into `ritual-summit-internal` **right now**, with a focus on:

- preserving Ritual-specific behavior we still depend on
- identifying areas where Ritual and upstream have repeated or converged work that should be de-duplicated
- identifying newer upstream work we likely want to absorb

The goal is to treat `ritual-summit-internal/dev` as:

- **shared Summit base** plus
- **Ritual extension layer**

That framing matters because a large part of the current codebase was already re-aligned to upstream in the January 2026 architecture sync.

## Current Context

- Current Ritual branch of interest: `ritual-summit-internal/dev`
- Current upstream branch of interest: `SeismicSystems/summit/main`
- Latest common ancestor for the current comparison: `43b860a`
- Ritual has a large number of fork-only commits since then, but a meaningful chunk of the current tree is still upstream-derived architecture that we later modified
- Upstream has **no releases** and **no tags**, so there is no clean release-based merge target today

## High-Level Merge Strategy

1. Start from the assumption that `types/`, `node/`, `syncer/`, `finalizer/`, `orchestrator/`, `rpc/`, and much of `application/` are now **shared base** and should trend toward upstream where possible.
2. Treat Ritual-specific functionality as a narrow compatibility layer that must be re-applied carefully.
3. Resolve overlaps by preferring:
   - upstream implementation when it is now functionally equivalent and cleaner
   - Ritual implementation when it encodes chain-specific behavior or operational requirements
   - a merged implementation when both sides solved adjacent pieces of the same problem
4. Do the merge in phases, not as one giant conflict-resolution session.

## Phase Plan

### Phase 1: Import Upstream Base

Goal: land upstream structural changes with minimal Ritual behavior reintroduced during the same step.

Checklist:

- merge upstream `main` into a dedicated branch off `dev`
- accept upstream structure in shared base modules unless a Ritual-specific reason is known
- preserve compile-ability as a checkpoint, even if some Ritual features are temporarily stubbed
- record every conflict as one of:
  - `ritual-only`
  - `shared-overlap`
  - `take-upstream`

### Phase 2: Reapply Ritual Extension Layer

Goal: restore chain-specific behavior after the base merge is stable.

Checklist:

- rewire Ritual config loading
- rewire Ritual signing scheme selection
- restore Ritual engine client behavior
- restore Ritual recovery behavior
- restore Ritual RPC extensions
- restore Ritual metrics and logging behavior

### Phase 3: De-duplicate Converged Work

Goal: remove double-implementations where both repos now solve similar problems.

Checklist:

- collapse duplicate stake-handling logic
- collapse duplicate recovery triggers and RPC surface
- collapse duplicate checkpoint/snapshot abstractions where practical
- choose one source of truth for protocol-param behavior
- choose one source of truth for consensus-event metrics

### Phase 4: Validate Behavior

Checklist:

- build workspace
- run focused tests around checkpointing, syncer, execution requests, and RPC
- verify Ritual threshold-signing path
- verify multisig path still works if it remains supported
- verify recovery flows on EL disconnect / restart
- verify validator lifecycle flows

## Ritual-Specific Things We Must Preserve

These are the highest-risk Ritual features to lose during an upstream merge.

### 1. Threshold Signing / DKG Integration

Preserve:

- `types/src/scheme.rs` additions around `ThresholdSchemeProvider`
- `node/src/ritual.rs`
- `dkg-gen/`
- `crates/ritual-config`
- threshold key loading and polynomial/share handling
- runtime selection between Ritual threshold flow and upstream multisig flow

Why it matters:

- this is the clearest Ritual-only extension layer
- upstream README still describes DKG threshold signatures as future-looking rather than the current mainline integration path

Merge note:

- prefer keeping upstream scheme interfaces where possible, but preserve Ritual's provider and bootstrap path

### 2. Stake-Weighted Leader Election

Preserve:

- `crates/ritual-consensus/src/stake_weighted.rs`
- any wiring that causes leader election to use stake rather than equal weights
- deterministic-seed behavior added to avoid leader divergence

Why it matters:

- upstream now has stake-aware quorum logic, but Ritual still has distinct elector behavior

Merge note:

- likely keep upstream quorum plumbing where possible
- preserve Ritual elector semantics unless upstream has fully equivalent logic

### 3. Ritual Recovery and Bootstrap Behavior

Preserve:

- automatic IPC reconnection
- initialize forkchoice from Reth head on startup
- network inactivity timeout handling
- manual recovery trigger flow
- trusted block / trusted checkpoint restart logic
- EL snapshot bootstrap and validator/epoch recovery behavior

Relevant areas:

- `crates/ritual-consensus/src/recovery.rs`
- `crates/ritual-engine-client/`
- `node/src/ritual.rs`
- `types/src/snapshot.rs`
- `types/src/bootstrap.rs`

Why it matters:

- these changes reflect actual operational needs on Ritual, not just feature experimentation

### 4. Ritual RPC Extensions

Preserve:

- peer discovery endpoints
- manual recovery trigger endpoints
- backward-compatible REST surface where still needed by Ritual infra

Relevant areas:

- `crates/ritual-rpc/`
- `rpc/src/api.rs`
- `rpc/src/server.rs`

### 5. Ritual Validator / Snapshot Persistence

Preserve:

- Ritual-specific validator DB behavior
- snapshot persistence used for bootstrap and validator-set recovery
- any archive or trusted-sync outputs required by operations

Relevant areas:

- `crates/ritual-validator-db/`
- `types/src/snapshot.rs`
- `node/src/bin/stake_and_checkpoint.rs`
- `node/src/bin/sync_from_genesis.rs`

### 6. Ritual Metrics and Ops Tooling

Preserve:

- structured consensus lifecycle logging
- verification failure logging
- engine RTT logging
- BigQuery-oriented field compatibility where still used
- Docker / Makefile workflows if still part of deployment

Relevant areas:

- `crates/ritual-metrics/`
- `application/src/actor.rs`
- `syncer/src/*`
- `finalizer/src/*`
- `Dockerfile`
- `Dockerfile.slim`
- `Makefile`

## Overlap Areas We Should Intentionally De-Duplicate

These are the places where both teams appear to have repeated or converged work.

### 1. Stake Handling

Overlap:

- Ritual stake-weighted leader election and quorum work
- upstream stake-aware quorum / validator-balance driven behavior
- repeated fixes around validator stake source of truth

Strategy:

- keep one authoritative source for validator balances
- keep one authoritative quorum policy path
- explicitly decide whether leader election remains Ritual-only or becomes upstream-compatible

### 2. Protocol Parameter Surface

Overlap:

- `blocks_per_epoch`
- min/max stake
- epoch length behavior
- deposit and withdrawal limits
- treasury and timestamp-related params

Strategy:

- prefer upstream types and param plumbing where available
- re-apply Ritual-only params only if they drive chain-specific behavior
- avoid parallel config knobs for the same concept in env vars, CLI args, and protocol params

### 3. Checkpoint / Consensus State / Snapshot Infrastructure

Overlap:

- upstream checkpointing and consensus state model
- Ritual trusted checkpoint sync and EL snapshot bootstrap work
- Ritual finalized-header embedding and validator-set recovery

Strategy:

- prefer upstream checkpoint and consensus-state data model as the base
- layer Ritual bootstrap/recovery semantics on top
- avoid maintaining two snapshot concepts unless they serve clearly different operational purposes

### 4. Recovery Triggers

Overlap:

- upstream checkpoint/restart fixes
- Ritual inactivity recovery
- Ritual manual recovery trigger endpoints
- Ritual divergence and bootstrap logic

Strategy:

- unify around one recovery state machine
- keep Ritual operational triggers if upstream does not replace them
- remove duplicate trigger APIs if both REST and JSON-RPC versions now do the same thing

### 5. Metrics / Logging

Overlap:

- upstream critical logs and metrics endpoint work
- Ritual JSON consensus lifecycle events
- Ritual BigQuery-oriented schema compatibility
- repeated logging additions in syncer/finalizer/application

Strategy:

- keep one event schema
- keep one place for critical logs
- decide whether upstream telemetry hooks can replace parts of Ritual's custom instrumentation

### 6. RPC Surface

Overlap:

- upstream JSON-RPC expansion
- Ritual REST + JSON-RPC support
- `get_peer_list`
- recovery endpoints
- validator-set and checkpoint-related endpoints

Strategy:

- define the supported public API surface first
- remove duplicate endpoints that expose the same data in two incompatible formats unless infra still depends on both

## New Upstream Work We Probably Want To Integrate

These are the upstream changes since late January that look relevant to Ritual.

### Protocol / Consensus Features

- dynamic epoch length and epoch-length bounds
- `blocks_per_epoch` in genesis
- treasury address protocol parameter
- allowed-future-timestamp protocol parameter
- max deposits per epoch
- max withdrawals per epoch

Why these matter:

- they overlap directly with Ritual's evolving validator / epoch / staking model

### Checkpointing / Finalization Hardening

- checkpoint verification
- require finalization certificate for the last block of an epoch
- fixes around pending checkpoint cleanup
- fixes for cold start from checkpoint deadlock
- epoch-keyed finalized header and consensus-state storage

Why these matter:

- they strengthen exactly the parts of the system Ritual has also been pushing on

### Execution / Engine Safety

- grouped execution requests
- payload attribute work
- fix for building on top of a bad ETH block
- more informative engine client errors
- orphan-block execution fix after finalized execution

Why these matter:

- they reduce fragility around EL/CL interaction, which is a known Ritual pain area

### Observability / Runtime

- critical event file logger
- merged metrics endpoints
- default thread count = number of cores
- additional logs for operational diagnosis

Why these matter:

- these likely complement, rather than replace, Ritual metrics work

### Networking / Infra

- external IP resolution
- CI updates
- newer commonware upgrades

## Merge Checklist

### Preserve Checklist

- [ ] `ThresholdSchemeProvider` still exists and is wired into runtime selection
- [ ] `node/src/ritual.rs` still owns Ritual bootstrap wiring
- [ ] DKG polynomial/share loading still works
- [ ] stake-weighted leader election is preserved
- [ ] stake-weighted quorum behavior is preserved or consciously replaced with an equivalent upstream path
- [ ] coinbase derivation behavior is preserved if still required
- [ ] execution validation before voting is preserved
- [ ] IPC reconnection still works
- [ ] forkchoice initialization from Reth head still works
- [ ] inactivity timeout recovery still works
- [ ] manual recovery trigger still works
- [ ] trusted restart / trusted checkpoint flow still works
- [ ] EL snapshot bootstrap still works
- [ ] validator-set recovery from snapshots still works
- [ ] Ritual metrics schema still emits the fields ops depends on
- [ ] Docker / Makefile workflows still build and run

### De-Duplicate Checklist

- [ ] one stake source of truth
- [ ] one quorum policy path
- [ ] one leader election path
- [ ] one checkpoint / consensus-state canonical model
- [ ] one recovery state machine
- [ ] one public RPC contract per capability
- [ ] one metrics event schema
- [ ] one place for critical logging configuration
- [ ] one source of truth for protocol parameters

### Upstream Integration Checklist

- [ ] dynamic epoch length
- [ ] epoch bounds validation
- [ ] checkpoint verification
- [ ] finalization-certificate requirement for last block of epoch
- [ ] grouped execution requests
- [ ] bad-ETH-block protection
- [ ] upstream engine-client error handling improvements
- [ ] max deposits / max withdrawals per epoch params
- [ ] treasury / timestamp protocol params
- [ ] critical event logger / metrics endpoint updates
- [ ] external IP resolution if still useful for deployment

## Recommended Conflict Resolution Rules

- If upstream added a cleaner base abstraction and Ritual only lightly patched it, take upstream and reapply the Ritual patch.
- If Ritual code reflects chain-specific behavior or operational requirements, preserve Ritual behavior even if upstream has something adjacent.
- If both sides implemented the same concept in parallel, do not keep both just because both are useful; choose a canonical path.
- If a feature affects signing, leader election, recovery, checkpointing, or EL/CL safety, require explicit sign-off before simplifying it away.

## Suggested Validation Matrix After Merge

- build `cargo test --workspace`
- run checkpointing tests
- run syncer tests
- run execution-request tests
- run RPC integration tests
- run a local validator lifecycle flow:
  - genesis
  - stake
  - checkpoint
  - restart
  - recovery trigger
- test a threshold-signing configuration
- test a multisig configuration if still supported
- test EL disconnect / reconnect behavior
- test bootstrap from snapshot / checkpoint

## Bottom Line

The right merge strategy is **not** "merge upstream and then manually re-fix random Ritual breakage." It should be:

1. treat upstream Summit as the evolving base client
2. preserve a narrow set of Ritual-critical extensions intentionally
3. aggressively de-duplicate places where both teams have been solving the same problem
4. explicitly import upstream hardening work around checkpointing, protocol params, execution safety, and observability

If we do this well, the long-term shape of the codebase should be:

- upstream owns most shared consensus client architecture
- Ritual owns threshold-signing, chain-specific recovery/bootstrap behavior, and any genuinely Ritual-only validator / ops integrations
