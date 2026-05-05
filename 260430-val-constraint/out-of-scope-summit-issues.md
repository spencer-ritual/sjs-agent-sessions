# 260430 Out-of-Scope Summit Issues

## Scope

These items came up during the validity-constraint review, but they do not fit the narrower definition used by `260430-val-audit-new-issues.md`: verifier-enforced block validity, builder/verifier symmetry, deterministic inclusion or purity rules, or consensus-visible Reth state-transition behavior.

They are still useful follow-up leads, but belong in a Summit / chain-halt / contract-liveness backlog rather than the Reth validity-constraints issue list.

## Out-Of-Scope Issues

### 1. Summit engine-client transport errors can collapse into semantic invalidity

**Sources:** `pt1-sad-springboard.md`

**Status:** current-code liveness/consensus-state lead.

`RethEngineClient::check_payload()` can map persistent transport failure after reconnect into `PayloadStatusEnum::Invalid`, while Summit voting treats non-valid status as a no vote. Execution-invalid payloads and local EL connectivity failures should not automatically have the same consensus meaning.

**Why out of scope:** This is not a Reth block-validity rule. It is CL/EL state-machine behavior that can affect liveness and voting under EL flaps.

### 2. Summit `commit_hash` failure policy remains under-specified

**Sources:** `pt1-sad-springboard.md`

**Status:** improved but still open policy gap.

`commit_hash()` now returns `Result`, but current finalizer paths may log errors and continue. If Summit advances CL state while EL forkchoice update failed, CL/EL agreement depends on later recovery behavior that is not clearly specified.

**Why out of scope:** This is a Summit recovery-policy question, not a concrete Reth verifier validity constraint.

### 3. Summit syncer, finalizer, cache, and startup panic paths remain liveness risks

**Sources:** `pt1-sad-springboard.md`

**Status:** availability class; not direct malicious-block validity.

The chain-halt pass still found panic paths in syncer storage reads, finalization writes, gapped blocks, subscriber closure, cache operations, checkpoint parsing, missing EL snapshots, and IPC startup. Some may be acceptable startup/operator failures, but hot runtime panics can halt nodes under storage corruption or local service failure.

**Why out of scope:** This is node availability hardening rather than verifier-enforced block validity.

### 4. Summit finalizer CL/EL advancement needs a focused agreement audit

**Sources:** `pt1-sad-springboard.md`

**Status:** validity-adjacent liveness/consistency concern.

Prior chain-halt notes report finalizer paths where EL forkchoice update may be skipped on withdrawal or parent mismatch, while Summit state/head advancement needs close review. The CL must not finalize or advance state in a way that leaves EL on a different canonical head without an explicit recovery path.

**Why out of scope:** This is the closest item to consensus safety, but it is still a Summit state-machine audit rather than a Reth validity-constraint finding.

### 5. Blocking refunds and scheduler cleanup remain contract-layer liveness leads

**Sources:** `pt1-sad-springboard.md`

**Status:** contract-layer liveness lead; not direct Reth validity.

`AsyncDelivery.deliver()` calls `RITUAL_WALLET.refundGas()` before `markDelivered()` without an obvious non-blocking fallback. `Scheduler` stores scheduled call data without an obvious `data.length` cap, while cleanup uses bounded batch cleanup and byte wiping.

**Why out of scope:** These are protocol-progress and contract-liveness risks, not block-import validity constraints.
