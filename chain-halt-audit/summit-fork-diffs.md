# ritual-summit Fork Diff Analysis

## Fork Point Determination

**Upstream project:** [SeismicSystems/summit](https://github.com/SeismicSystems/summit) — a consensus client built on the [commonware](https://github.com/commonwarexyz/monorepo) framework.

**Fork point commit:**
```
43b860a feat: add historical engine client that supports eth transactions (#50)
Author: Matthias Wright
```

**Method:** The repository has a remote branch `remotes/upstream-summit/main` tracking the upstream SeismicSystems/summit repo (204 commits). The fork point was determined via `git merge-base remotes/upstream-summit/main dev`, which returned `43b860a`. This is the last common commit between Ritual's `dev` branch and the upstream `main`.

**Since fork:** 148 commits on `dev`, touching 154 files with **+36,827 / -5,911 lines changed**.

**Contributors (commits):** arshan-ritual (75), arshan (28), akilesh-ritual (18), Spencer (18), Arshan (5), Ding (2), claude[bot] (1), Kartik (1).

---

## Summary Table

| # | Feature Area | Commits | Files Changed | Lines (+/-) |
|---|---|---|---|---|
| 1 | [Ritual Extension Crates](#1-ritual-extension-crates) | 14 | 15 | +1,880 / 0 |
| 2 | [Stake-Weighted Consensus & Quorum](#2-stake-weighted-consensus--quorum) | 8 | ~12 | ~+1,200 |
| 3 | [Epoch Transitions & Dynamic Validators](#3-epoch-transitions--dynamic-validators) | 7 | ~10 | ~+1,500 |
| 4 | [Syncer Overhaul & P99 Latency](#4-syncer-overhaul--p99-latency) | 16 | 17 | +5,221 / -789 |
| 5 | [Finalizer & Orchestrator (New Crates)](#5-finalizer--orchestrator-new-crates) | 14 | 13 | +3,690 / 0 |
| 6 | [Disaster Recovery & Resilience](#6-disaster-recovery--resilience) | 10 | ~8 | ~+1,100 |
| 7 | [Consensus Metrics & Logging](#7-consensus-metrics--logging) | 14 | ~12 | ~+800 |
| 8 | [RPC Enhancements](#8-rpc-enhancements) | 8 | 11 | +1,498 / -54 |
| 9 | [Types System Expansion](#9-types-system-expansion) | 16 | 22 | +5,862 / -356 |
| 10 | [Application Actor Refactor](#10-application-actor-refactor) | ~20 | 9 | +850 / -2,722 |
| 11 | [Node Engine & Configuration](#11-node-engine--configuration) | 28 | 26 | +7,767 / -1,160 |
| 12 | [Build, Docker & CI Infrastructure](#12-build-docker--ci-infrastructure) | 10 | ~12 | +3,550 / -1,340 |
| 13 | [PR Review Infrastructure](#13-pr-review-infrastructure) | 6 | 8 | ~+700 |
| 14 | [Documentation & Analysis Artifacts](#14-documentation--analysis-artifacts) | 7 | ~20 | ~+5,400 |
| 15 | [Upstream Merge (commonware 0.0.65)](#15-upstream-merge-commonware-0065) | 8 | ~30 | (cross-cutting) |

> Note: Many commits are cross-cutting and touch multiple feature areas. Line counts in sub-areas may overlap with the total.

---

## Detailed Feature Areas

### 1. Ritual Extension Crates

New Rust crates under `crates/` that encapsulate Ritual-specific logic, cleanly separated from the upstream Summit code.

**Commits:**
| Hash | Message |
|------|---------|
| `d0dc29d` | feat(ritual): add Ritual extension crates |
| `84bb800` | refactor: re-export ritual-metrics from commonware |
| `22abee5` | feat: add block_time to consensus metrics |
| `3612bd6` | fix(consensus): capture engine validation details |
| `edb7cb6` | Use deterministic seed for stake-weighted leader selection |
| `03f2dec` | feat: add stake-weighted quorum support with local commonware patch |
| `f23b453` | feat: integrate Ritual features - coinbase derivation, execution validation, inactivity timeout |
| `04a035f` | refactor(metrics): unify consensus lifecycle metrics with ts_start in end events |
| `19aac3b` | chore: metrics and actor updates |
| `9bfc436` | fix(metrics): use only existing BigQuery columns |
| `da90db0` | feat(metrics): add verification failure and engine RTT logging |
| `11cc86a` | fix: add instrumentation |
| `adaa3a3` | feat: implement EL snapshot bootstrap for monolithic recovery |

**Files:**
- `crates/ritual-config/` — Centralized configuration (207 lines), env-var-driven settings for block build delay, inactivity timeout, recovery, etc.
- `crates/ritual-consensus/` — Execution gate (125 lines), recovery logic (199 lines), stake-weighted quorum policy (245 lines)
- `crates/ritual-engine-client/` — Abstracted engine client (342 lines) for EL communication
- `crates/ritual-metrics/` — Metrics re-exports (7 lines)
- `crates/ritual-rpc/` — JSON-RPC server extensions (191 lines)
- `crates/ritual-validator-db/` — Validator set persistence with RocksDB-backed EL snapshots (403 lines)

**Summary:** These crates form the architectural spine of the Ritual fork. They separate Ritual-specific concerns (staking, recovery, metrics, engine client) from upstream code, making future upstream merges cleaner.

---

### 2. Stake-Weighted Consensus & Quorum

Replaces the upstream equal-weight voting with stake-proportional quorum and leader selection.

**Commits:**
| Hash | Message |
|------|---------|
| `8ba4d0d` | feat: stake weight implementation |
| `41b23d3` | feat: add stake-weighted quorum support |
| `03f2dec` | feat: add stake-weighted quorum support with local commonware patch |
| `edb7cb6` | Use deterministic seed for stake-weighted leader selection |
| `c29c01d` | Merge pull request #30 from ritual-net/feature/stake-weighted-quorum |
| `6577baf` | fix: use balance as single source of truth for validator stake |
| `34366a4` | Merge pull request #46 from ritual-net/arshan/min-stake-stuff |
| `6fb09f6` | feat: use unbounded certificate codec to support dynamic validator sets |

**Files:**
- `crates/ritual-consensus/src/stake_weighted.rs` — `StakeQuorumPolicy` implementing stake-proportional voting thresholds
- `types/src/scheme.rs` — `ThresholdSchemeProvider` and `MultisigScheme` types
- `types/src/account.rs` — Validator account with balance/stake tracking
- `node/src/args.rs` — CLI args for stake parameters
- `application/src/actor.rs` — Integration of stake-weighted leader selection

**Summary:** Core change: consensus weight is proportional to validator stake rather than 1-validator-1-vote. Leader selection uses a deterministic seed derived from stake. The `StakeQuorumPolicy` ensures quorum thresholds respect economic weight. Minimum stake enforcement was added as a follow-up.

---

### 3. Epoch Transitions & Dynamic Validators

Supports dynamic validator set changes across epochs, with snapshotting and recovery.

**Commits:**
| Hash | Message |
|------|---------|
| `d28668e` | Merge pull request #36 from ritual-net/arshan/epoch-transition-issues |
| `9f1aa3b` | fix: stabilize EL bootstrap and epoch handling |
| `5c65516` | fix: embed finalized header in EL snapshots |
| `2921a10` | fix: recover validator set and epoch from EL snapshots |
| `bccc024` | docs: clarify backfill race condition is intentional design |
| `890c4be` | feat: add validator set RPC endpoints and configurable BLOCKS_PER_EPOCH |
| `adaa3a3` | feat: implement EL snapshot bootstrap for monolithic recovery |

**Files:**
- `types/src/snapshot.rs` (708 lines, new) — Full EL snapshot serialization for consensus state
- `types/src/consensus_state.rs` (+774 lines) — Epoch-aware consensus state management
- `types/src/bootstrap.rs` (264 lines, new) — Bootstrap from checkpoint or genesis
- `crates/ritual-validator-db/src/lib.rs` — Persistent validator set across epochs
- `node/src/engine.rs` — Epoch-aware engine initialization
- `node/src/bin/stake_and_checkpoint.rs` (717 lines, new) — Staking and checkpoint creation binary

**Summary:** Enables validators to join/leave across epoch boundaries. EL snapshots embed the full validator set and finalized header, allowing nodes to bootstrap from a checkpoint without replaying history. `BLOCKS_PER_EPOCH` is configurable.

---

### 4. Syncer Overhaul & P99 Latency

Major refactor of the syncer component with focus on P99 block latency improvements.

**Commits:**
| Hash | Message |
|------|---------|
| `4c72a03` | Merge pull request #45 from ritual-net/spencer/p99 |
| `f837665` | syncer: address summit PR feedback (try_complete, pending_notarized prune, cfg gates) |
| `faa8668` | syncer: address summit PR feedback |
| `6247517` | syncer: refine pending_notarized handling and add Proposed/Block Deliver tests |
| `bc394f0` | syncer: complete pending notarized locally when block arrives via gossip |
| `9c5e2e4` | fix(syncer): repair test harness for test-mocks |
| `b9d4e6d` | problem thesis |
| `50d82dc` | feat(consensus): adopt upstream syncer/finalizer/orchestrator architecture |
| `b8d64a8` | feat: add graceful shutdown handling from upstream PR #57 |
| `ed4d332` | address manus feedback |
| `2721630` | block recieved log |
| `3ddbb25` | fix casting issue |
| `8a02e49` | made log live in commonware |
| `e3131bc` | add logging for cl_block_received |
| `14172a6` | feat: implement finalization vote and block execution logging |
| `9f1aa3b` | fix: stabilize EL bootstrap and epoch handling |

**Files (17 changed, +5,221 / -789):**
- `syncer/src/actor.rs` — Major refactor of syncer state machine
- `syncer/src/cache.rs` (390 lines, new) — Block caching layer
- `syncer/src/config.rs` (68 lines, new) — Syncer configuration
- `syncer/src/ingress/handler.rs` (525 lines, new) — Message handler refactor
- `syncer/src/ingress/mailbox.rs` (569 lines, new) — Mailbox-based ingress
- `syncer/src/lib.rs` (+2,047 lines) — Core syncer logic expansion
- `syncer/src/mocks/` (4 new files) — Test mock infrastructure
- `syncer/src/resolver/` (2 new files) — P2P block resolution

**Summary:** The syncer was overhauled to fix P99 latency issues. Key fix: when a block arrives via gossip before notarization completes, the syncer now completes notarization locally instead of re-fetching. Added a caching layer, mailbox-based ingress, and comprehensive test mocks. Documentation in `docs/sjs-p99/` details the root cause analysis.

---

### 5. Finalizer & Orchestrator (New Crates)

Extracted from the monolithic application into standalone crates, following upstream architecture.

**Commits:**
| Hash | Message |
|------|---------|
| `50d82dc` | feat(consensus): adopt upstream syncer/finalizer/orchestrator architecture |
| `14172a6` | feat: implement finalization vote and block execution logging |
| `6250901` | feat: add cl_finalize event logging to finalization |
| `ed4d332` | address manus feedback |
| `5c65516` | fix: embed finalized header in EL snapshots |
| `2921a10` | fix: recover validator set and epoch from EL snapshots |
| `9f1aa3b` | fix: stabilize EL bootstrap and epoch handling |
| `890c4be` | feat: add validator set RPC endpoints and configurable BLOCKS_PER_EPOCH |
| `415148a` | feat: add trusted checkpoint sync and archive mode file output |
| `3612bd6` | fix(consensus): capture engine validation details |
| `03f2dec` | feat: add stake-weighted quorum support with local commonware patch |
| `41b23d3` | feat: add stake-weighted quorum support |
| `f23b453` | feat: integrate Ritual features - coinbase derivation, execution validation, inactivity timeout |

**Files (13 changed, +3,690):**
- `finalizer/src/actor.rs` (1,749 lines) — Finalization state machine
- `finalizer/src/db.rs` (499+ lines) — Finalization database (migrated from `application/src/db.rs`)
- `finalizer/src/config.rs` — Finalizer configuration
- `finalizer/src/ingress.rs` (319 lines) — Finalizer message ingress
- `orchestrator/src/actor.rs` (354 lines) — Orchestrates syncer + finalizer lifecycle
- `orchestrator/src/ingress.rs` — Orchestrator message ingress

**Summary:** The upstream Summit project split its consensus pipeline into syncer (block proposal/notarization), finalizer (finalization certificates), and orchestrator (lifecycle management). This fork adopted that architecture and added Ritual-specific extensions: EL snapshot embedding, finalization logging, and trusted checkpoint support.

---

### 6. Disaster Recovery & Resilience

Multiple recovery mechanisms for handling chain halts, Reth divergence, and node restarts.

**Commits:**
| Hash | Message |
|------|---------|
| `85d0f21` | Add trusted block restart disaster recovery mechanism |
| `f335112` | feat(summit): add automatic recovery from Reth/Summit divergence |
| `97c9bb6` | feat(summit): implement automatic IPC reconnection on Reth restart |
| `1b3b9bf` | feat(summit): initialize forkchoice from Reth's head on startup |
| `20ac48e` | feat: make network inactivity timeout configurable via env var |
| `6df4142` | feat: add external trigger for manual recovery |
| `5de74ef` | feat: add RPC endpoint for external recovery trigger |
| `958c648` | fix: complete RPC recovery trigger implementation |
| `415148a` | feat: add trusted checkpoint sync and archive mode file output |
| `adaa3a3` | feat: implement EL snapshot bootstrap for monolithic recovery |

**Files:**
- `crates/ritual-consensus/src/recovery.rs` (199 lines) — Automated recovery state machine
- `crates/ritual-config/src/lib.rs` — `SUMMIT_INACTIVITY_TIMEOUT_MS`, `SUMMIT_TRUSTED_BLOCK_*` env vars
- `application/src/actor.rs` — Recovery trigger integration, IPC reconnection
- `node/src/ritual.rs` (199 lines, new) — Ritual-specific node bootstrap logic
- `node/src/bin/sync_from_genesis.rs` (687 lines, new) — Genesis sync binary for full recovery

**Summary:** Comprehensive disaster recovery: (1) Automatic Reth/Summit divergence detection and recovery, (2) IPC auto-reconnection on Reth restart, (3) Forkchoice initialization from Reth head, (4) Configurable inactivity timeout, (5) RPC-triggered manual recovery, (6) Trusted block restart mechanism, (7) EL snapshot bootstrap. These address real-world operational failure modes on the Ritual chain.

---

### 7. Consensus Metrics & Logging

Structured JSON logging and Prometheus metrics for consensus lifecycle events, designed for BigQuery ingestion.

**Commits:**
| Hash | Message |
|------|---------|
| `35b61ac` | feat: add JSON logging support for consensus lifecycle metrics |
| `d03ce26` | feat: add consensus lifecycle metrics parity with dev branch |
| `6dd341e` | feat: add JSON logging support for consensus lifecycle metrics |
| `2530b92` | feat: add consensus lifecycle metrics parity with dev branch |
| `2f3f075` | feat(metrics): add vote visibility logging for consensus analysis |
| `04a035f` | refactor(metrics): unify consensus lifecycle metrics with ts_start in end events |
| `19aac3b` | chore: metrics and actor updates |
| `9bfc436` | fix(metrics): use only existing BigQuery columns |
| `da90db0` | feat(metrics): add verification failure and engine RTT logging |
| `22abee5` | feat: add block_time to consensus metrics |
| `14172a6` | feat: implement finalization vote and block execution logging |
| `6250901` | feat: add cl_finalize event logging to finalization |
| `2721630` | block received log |
| `e3131bc` | add logging for cl_block_received |

**Files:**
- `crates/ritual-metrics/` — Metrics re-exports
- `application/src/actor.rs` — Lifecycle event emissions (propose, vote, notarize, finalize)
- `node/src/prom/server.rs` — Prometheus endpoint enhancements
- `syncer/src/actor.rs` — Block receipt and notarization timing

**Summary:** Every major consensus lifecycle event (propose, vote, notarize, finalize, engine RTT) is now emitted as structured JSON with timestamps. Fields are aligned to BigQuery schema for operational analytics. Includes `ts_start`/`ts_end` pairs, block_time metrics, and verification failure tracking.

---

### 8. RPC Enhancements

Extended RPC surface for validators, executors, and operational tooling.

**Commits:**
| Hash | Message |
|------|---------|
| `607f82c` | feat: add Summit RPC /get_peer_list endpoint with RwLock caching |
| `3b3c23e` | feat(rpc): add get_peer_list and trigger_recovery JSON-RPC endpoints |
| `6d619da` | feat(rpc): add REST endpoints alongside JSON-RPC for executor compatibility |
| `3694e98` | refactor(rpc): adopt upstream JSON-RPC architecture |
| `890c4be` | feat: add validator set RPC endpoints and configurable BLOCKS_PER_EPOCH |
| `5de74ef` | feat: add RPC endpoint for external recovery trigger |
| `958c648` | fix: complete RPC recovery trigger implementation |

**Files (11 changed, +1,498 / -54):**
- `rpc/src/api.rs` (74 lines, new) — API trait definitions
- `rpc/src/builder.rs` (114 lines, new) — RPC server builder
- `rpc/src/server.rs` (401 lines, new) — JSON-RPC server implementation
- `rpc/src/routes.rs` (+189 lines) — REST route handlers
- `rpc/src/types.rs` (69 lines, new) — RPC request/response types
- `rpc/tests/integration_test.rs` (246 lines, new) — Integration tests
- `crates/ritual-rpc/src/lib.rs` (191 lines) — Ritual-specific RPC extensions

**Summary:** Dual REST + JSON-RPC interface. New endpoints include: `get_peer_list` (cached with RwLock), `trigger_recovery`, validator set queries, and `GetLatestCheckpoint`. REST endpoints maintained for backward compatibility with executor infrastructure.

---

### 9. Types System Expansion

Massive expansion of the types crate to support Ritual's extended consensus model.

**Commits (16):**
| Hash | Message |
|------|---------|
| `b69e3c3` | feat(types): adopt upstream types with ThresholdSchemeProvider |
| `3d3bb5f` | WIP: commonware 0.0.65 migration - core types and supervisor |
| `6fb09f6` | feat: use unbounded certificate codec to support dynamic validator sets |
| `03f2dec` | feat: add stake-weighted quorum support with local commonware patch |
| `41b23d3` | feat: add stake-weighted quorum support |
| `5c65516` | fix: embed finalized header in EL snapshots |
| `2921a10` | fix: recover validator set and epoch from EL snapshots |
| `890c4be` | feat: add validator set RPC endpoints and configurable BLOCKS_PER_EPOCH |
| `6577baf` | fix: use balance as single source of truth for validator stake |
| `0d05a3f` | fix: address PR review comments - panic consistency, error context, tests |
| `6ccbdca` | fix: return PayloadStatus::Invalid instead of panicking on EL errors |
| `adaa3a3` | feat: implement EL snapshot bootstrap for monolithic recovery |
| `f23b453` | feat: integrate Ritual features - coinbase derivation, execution validation, inactivity timeout |
| `6ce4303` | feat: add --allow-private-ips flag and update to MultisigScheme |
| `8ba4d0d` | feat: stake weight implementation |

**New files (22 changed, +5,862 / -356):**
- `types/src/snapshot.rs` (708 lines) — EL state snapshots
- `types/src/engine_client.rs` (827 lines) — Engine client trait and types
- `types/src/scheme.rs` (431 lines) — Cryptographic scheme definitions (ThresholdSchemeProvider, MultisigScheme)
- `types/src/reth.rs` (650 lines) — Reth integration types
- `types/src/protocol_params.rs` (279 lines) — On-chain protocol parameter types
- `types/src/bootstrap.rs` (264 lines) — Bootstrap mode definitions
- `types/src/consensus_state_query.rs` (201 lines) — State query interface
- `types/src/key_paths.rs` (86 lines) — Key derivation path definitions
- `types/src/network_oracle.rs` (58 lines) — Network state oracle
- `types/src/rpc.rs` (16 lines) — RPC type definitions

**Summary:** The types crate grew from a thin wrapper to a comprehensive type system covering snapshots, engine client abstractions, cryptographic schemes, Reth integration, protocol parameters, bootstrap modes, and network oracles. This reflects the fork's evolution from a simple consensus client to a full chain infrastructure component.

---

### 10. Application Actor Refactor

Refactored the monolithic application actor, extracting finalizer/registry and adding Ritual features.

**Commits (~20 touching application/):**
| Hash | Message |
|------|---------|
| `cac3f97` | refactor(application): adopt upstream simplified actor model |
| `05d7c67` | WIP: summit-application compiles with commonware 0.0.65 |
| `f23b453` | feat: integrate Ritual features - coinbase derivation, execution validation, inactivity timeout |
| `a1fe2e9` | feat(consensus): set default block build delay to 0 for eager payload fetching |
| `fc9729f` | feat: restore SUMMIT_BLOCK_BUILD_DELAY_MS environment variable |
| `acdcd53` | feat: add execution validation before voting in consensus |
| `97c9bb6` | feat(summit): implement automatic IPC reconnection on Reth restart |
| `1b3b9bf` | feat(summit): initialize forkchoice from Reth's head on startup |
| `f335112` | feat(summit): add automatic recovery from Reth/Summit divergence |
| `85d0f21` | Add trusted block restart disaster recovery mechanism |
| `22abee5` | feat: add block_time to consensus metrics |

**Files (9 changed, +850 / -2,722):**
- `application/src/actor.rs` (+918 lines) — Expanded with recovery, metrics, execution validation
- `application/src/config.rs` (+86 lines) — Ritual configuration integration
- `application/src/engine_client.rs` (-448 lines, deleted) — Moved to `crates/ritual-engine-client/`
- `application/src/finalizer.rs` (-695 lines, deleted) — Moved to `finalizer/`
- `application/src/registry.rs` (-715 lines, deleted) — Extracted to separate crates
- `application/src/ingress.rs` — Updated message types

**Summary:** The application actor was significantly refactored: the finalizer and registry were extracted to standalone crates, the engine client was abstracted, and Ritual-specific features (execution validation before voting, coinbase derivation, eager payload fetching, IPC reconnection, recovery) were integrated. Net code reduction despite adding features.

---

### 11. Node Engine & Configuration

Extensive changes to the node binary: new sub-binaries, expanded CLI, engine integration.

**Commits (28 touching node/):**

Key commits:
| Hash | Message |
|------|---------|
| `d784525` | feat(node): adopt upstream engine architecture with ritual extensions |
| `890c4be` | feat: add validator set RPC endpoints and configurable BLOCKS_PER_EPOCH |
| `adaa3a3` | feat: implement EL snapshot bootstrap for monolithic recovery |
| `415148a` | feat: add trusted checkpoint sync and archive mode file output |
| `6ce4303` | feat: add --allow-private-ips flag and update to MultisigScheme |
| `9bb65a8` | feat: Derive validator coinbase from Ed25519 public key |
| `2f3f075` | feat(metrics): add vote visibility logging for consensus analysis |

**Files (26 changed, +7,767 / -1,160):**

New binaries:
- `node/src/bin/genesis.rs` (82 lines) — Genesis file creation
- `node/src/bin/protocol_params.rs` (399 lines) — On-chain protocol parameter management
- `node/src/bin/stake_and_checkpoint.rs` (717 lines) — Validator staking and checkpoint creation
- `node/src/bin/stake_and_join_with_outdated_ckpt.rs` (834 lines) — Join with outdated checkpoint
- `node/src/bin/sync_from_genesis.rs` (687 lines) — Full genesis sync
- `node/src/bin/withdraw_and_exit.rs` (411 lines) — Validator exit and withdrawal

Modified:
- `node/src/args.rs` (+1,158 lines) — Massively expanded CLI with Ritual-specific flags
- `node/src/engine.rs` (+515 lines) — Engine client lifecycle management
- `node/src/config.rs` (+111 lines) — Node configuration
- `node/src/ritual.rs` (199 lines, new) — Ritual bootstrap logic
- `node/src/keys.rs` (+170 lines) — Key management and derivation
- `node/src/test_harness/` — Expanded test infrastructure
- `node/src/tests/` — Checkpointing, execution request, and syncer tests

**Summary:** The node was transformed from a simple testnet binary into a production-grade validator node with: 6 new operational sub-binaries for the full validator lifecycle (genesis, stake, checkpoint, sync, withdraw), massively expanded CLI arguments, Ritual-specific bootstrap logic, and comprehensive test coverage.

---

### 12. Build, Docker & CI Infrastructure

Production deployment and build tooling.

**Commits:**
| Hash | Message |
|------|---------|
| `c485dab` | feat: include commonware commit hash in Docker image tag |
| `b8d64a8` | feat: add graceful shutdown handling from upstream PR #57 |
| `71b8d35` | build: pin Rust toolchain to nightly for commonware compatibility |
| `b0002f0` | fix: argparsing + makefile |
| `bec65c6` | fix: setup script |

**Files (6 changed, +3,312 / -1,340):**
- `Dockerfile` (55 lines, new) — Multi-stage Docker build
- `Dockerfile.slim` (31 lines, new) — Slim production image
- `Makefile` (149 lines, new) — Build targets (build, test, docker-build, docker-push)
- `rust-toolchain.toml` (3 lines, new) — Pinned nightly toolchain
- `Cargo.toml` (+142 lines) — Workspace reorganization with Ritual crates
- `Cargo.lock` (+4,272 / -varies) — Dependency updates

**Summary:** Added production Docker builds (full and slim), a Makefile for common operations, pinned Rust nightly toolchain, and reorganized the Cargo workspace to include all Ritual crates.

---

### 13. PR Review Infrastructure

AI-assisted PR review system using Claude, Devin, and Manus.

**Commits:**
| Hash | Message |
|------|---------|
| `8516771` | feat: add Manus, Claude, and Devin PR review infrastructure |
| `bef9393` | fix: address Devin feedback - add validation, retry logic, and README |
| `afdb41d` | docs: add README and clarify config.yml usage |
| `0a161bf` | fix: add curl timeouts and EOF newlines |
| `34c9966` | Merge pull request #12 from ritual-net/feat/add-pr-review-infrastructure-clean |
| `f9b90aa` | chore: add code hygiene detection to PR review prompts (#18) |

**Files:**
- `.github/workflows/claude-pr-review.yml` (92 lines) — Claude review workflow
- `.github/workflows/devin-pr-review.yml` (136 lines) — Devin review workflow
- `.github/workflows/manus-pr-review.yml` (148 lines) — Manus review workflow
- `.ritual-pr/config.yml` (35 lines) — Review configuration
- `.ritual-pr/prompts/shared/engineering.md` (56 lines) — Shared engineering review prompts
- `.ritual-pr/prompts/shared/fsm-verification.md` (31 lines) — FSM verification prompts
- `.ritual-pr/README.md` (202 lines) — PR review infrastructure documentation

**Summary:** Automated PR review using three AI systems (Claude, Devin, Manus) with shared prompt templates covering engineering best practices and finite state machine verification. Includes code hygiene detection.

---

### 14. Documentation & Analysis Artifacts

Engineering documentation, merge strategy docs, and performance analysis.

**Commits:**
| Hash | Message |
|------|---------|
| `899b14c` | docs: add Ritual integration documentation |
| `1c15e78` | docs: Add top-level documentation README |
| `342d546` | docs: Add upstream merge documentation for future reference |
| `36b7e6a` | more docs |
| `b9d4e6d` | problem thesis |
| `97c9bb6` | feat(summit): implement automatic IPC reconnection on Reth restart (also added analysis docs) |

**Files:**
- `docs/README.md` (77 lines) — Top-level documentation index
- `docs/RITUAL_INTEGRATION.md` (133 lines) — Ritual integration guide
- `docs/CHANGELOG_RITUAL.md` (109 lines) — Ritual-specific changelog
- `docs/merge-upstream-2025-10-14/` — 5 files documenting the upstream merge strategy, resolution log, feature verification checklist
- `docs/sjs-p99/` — 4 files documenting P99 latency investigation, bug analysis, fix plan
- `COMPLETE_ANALYSIS_SUMMARY.md` (631 lines) — Comprehensive analysis
- `CORRECTED_COST_ANALYSIS.md` (555 lines) — Cost analysis
- `EXECUTION_VALIDATION_IMPLEMENTATION.md` (469 lines) — Execution validation design doc
- `STOCHASTIC_OPTIMIZATION_ANALYSIS.md` (761 lines) — Optimization analysis
- `optimization_calculator.py` (412 lines) — Optimization calculator script
- `stochastic_optimization_solver.py` (713 lines) — Stochastic optimization solver

**Summary:** Extensive engineering documentation including merge strategy playbooks, P99 latency root cause analysis, execution validation design docs, and cost/optimization analyses. The merge-upstream docs are particularly valuable for future upstream sync operations.

---

### 15. Upstream Merge (commonware 0.0.65)

Major upstream merge bringing the SeismicSystems/summit codebase forward to commonware 0.0.65.

**Commits:**
| Hash | Message |
|------|---------|
| `47610aa` | Merge pull request #26 from ritual-net/feat/upstream-merge-jan-2026 |
| `0530d10` | Merge branch 'dev' into feat/upstream-merge-jan-2026 |
| `4241c5c` | build: update workspace for commonware 0.0.65 and new crates |
| `6443d9b` | chore: update example_genesis.toml for upstream format |
| `50d82dc` | feat(consensus): adopt upstream syncer/finalizer/orchestrator architecture |
| `3694e98` | refactor(rpc): adopt upstream JSON-RPC architecture |
| `cac3f97` | refactor(application): adopt upstream simplified actor model |
| `b69e3c3` | feat(types): adopt upstream types with ThresholdSchemeProvider |
| `3d3bb5f` | WIP: commonware 0.0.65 migration - core types and supervisor |
| `05d7c67` | WIP: summit-application compiles with commonware 0.0.65 |
| `bf2b917` | Merge upstream/main: Add checkpoint and consensus state types |

**Summary:** This cross-cutting effort upgraded the commonware dependency from ~0.0.56 to 0.0.65, adopted the upstream's new architecture (syncer/finalizer/orchestrator split, JSON-RPC, simplified actor model), and migrated the type system to use `ThresholdSchemeProvider`. The merge was carefully documented in `docs/merge-upstream-2025-10-14/` with resolution logs and feature verification checklists.

---

## Key Architectural Differences from Upstream

| Aspect | Upstream (SeismicSystems/summit) | Ritual Fork |
|--------|----------------------------------|-------------|
| **Voting** | Equal-weight | Stake-weighted quorum |
| **Validators** | Static set | Dynamic set with epoch transitions |
| **Recovery** | None | Multi-modal (auto-divergence, IPC reconnect, trusted restart, RPC trigger) |
| **Engine Client** | Inline | Abstracted crate with trait-based design |
| **Metrics** | Basic Prometheus | Structured JSON for BigQuery + Prometheus |
| **RPC** | JSON-RPC only | Dual REST + JSON-RPC |
| **Coinbase** | Manual config | Derived from Ed25519 public key |
| **Execution Validation** | None | Pre-vote execution validation gate |
| **Crate Organization** | Monolithic + syncer/finalizer/orchestrator | + 6 ritual-* extension crates |
| **Operational Tooling** | Testnet binary only | 6 production sub-binaries |
