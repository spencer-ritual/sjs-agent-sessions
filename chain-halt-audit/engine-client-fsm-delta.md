# Engine Client FSM — Full Model with PR Delta and Flagged Issues

> Models `RethEngineClient` block lifecycle as an FSM. Shows how PR #50 changes failure behavior and surfaces the issues flagged in review (commit_hash silent fail, check_payload Invalid-on-transport, and gaps).

---

## 1. Dual-Track State: CL vs EL

The engine client mediates between two state machines that can diverge:

```
┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│  CL (Consensus Layer)               │     │  EL (Execution Layer / Reth)         │
│  — finalizer, application           │     │  — forkchoice head, finalized head   │
│  — believes head = H                │◄───►│  — actual head may lag              │
└─────────────────────────────────────┘     └─────────────────────────────────────┘
```

**Ideal invariant:** CL head == EL head (after every successful `commit_hash`).

**Violation:** When `commit_hash` fails, CL has already advanced; EL has not. No signal propagates to caller.

---

## 2. Block Lifecycle FSM (Per Block)

### States

| State | Description | CL view | EL view |
|-------|-------------|---------|---------|
| **Idle** | No build in progress | head = H | head = H |
| **Building** | `start_building_block` succeeded, EL building | head = H | building block H+1 |
| **HavePayload** | `get_payload` succeeded | — | — |
| **Verified** | `check_payload` returned Valid (or Syncing, see §3) | block accepted | — |
| **Committed** | `commit_hash` succeeded | head = H+1 | head = H+1 |

### Transitions (Success Path)

```
    Idle ──start_building_block(Ok)──► Building
                                            │
                                            │ get_payload(Ok)
                                            ▼
                                       HavePayload
                                            │
                                            │ check_payload(Valid)
                                            ▼
                                       Verified
                                            │
                                            │ commit_hash(Ok)
                                            ▼
                                       Committed
```

---

## 3. Failure Transitions — PR Delta

### 3.1 start_building_block

| Condition | Before PR | After PR |
|-----------|-----------|----------|
| Non-transport Err | `return None` | `return None` |
| Transport Err → retry Ok | transition to Building | transition to Building |
| Transport Err → retry Err | **panic** | `return None` |

**New terminal:** `None` → caller skips proposal this round. Recoverable.

---

### 3.2 get_payload

| Condition | Before PR | After PR |
|-----------|-----------|----------|
| Ok | return payload | `return Some(payload)` |
| Non-transport Err | **panic** | `return None` |
| Transport Err → retry Ok | return payload | `return Some(payload)` |
| Transport Err → retry Err | **panic** | `return None` |

**New terminal:** `None` → caller skips proposal. Recoverable.  
**Side effect:** EL may have built a block that is never retrieved (wasted work; not a crash).

---

### 3.3 check_payload — Semantic Collapse (Issue)

PayloadStatus has distinct semantics:

| Status | Meaning | Finalizer behavior |
|--------|---------|--------------------|
| **Valid** | EL verified block | Apply block, advance forkchoice |
| **Syncing** | EL cannot verify yet (e.g. syncing) | Advance forkchoice only, trigger backfill |
| **Invalid** | EL verified block is bad | Reject block, do not advance |

**Current PR behavior:** Both non-transport errors and transport errors (including post-reconnect failure) return `Invalid`.

| Condition | Returns | Problem |
|-----------|---------|---------|
| Non-transport Err (payload bad, EL internal error) | Invalid | Correct — block is unverified/bad |
| Transport Err → retry Err (EL unreachable) | Invalid | **Wrong** — we didn't verify; we couldn't reach EL |

**Bug:** Transport failure is collapsed into `Invalid`. The node votes *against* a block it never verified. If enough validators have transient EL issues (rolling restart, network partition), valid blocks fail quorum → **liveness** impact.

**Correct semantics for transport failure:** Return `Syncing` (or a distinct "Unavailable") so consensus can abstain rather than vote no. Finalizer already treats `Syncing` differently (advance forkchoice, trigger backfill).

---

### 3.4 commit_hash — Silent Failure (Issue)

| Condition | Before PR | After PR |
|-----------|-----------|----------|
| Ok | return | return |
| Non-transport Err | log + return | log + return |
| Transport Err → retry Err | **panic** | log + return |

**Problem:** Trait returns `()`. Caller cannot observe failure.

**State divergence:**

```
                    commit_hash(forkchoice_H+1)
                              │
              ┌───────────────┴───────────────┐
              │ Ok                            │ Err (any)
              ▼                               ▼
    CL head := H+1                    CL head := H+1  (already set by finalizer!)
    EL head := H+1  ✓                 EL head := H    ✗ DIVERGENCE
              │                               │
              │                               │ Next start_building_block
              │                               │ uses parent H+1
              │                               ▼
              │                       EL rejects: "unknown parent H+1"
              │                       → return None
              │                               │
              │                               │ Next finalized block also
              │                               │ references H+1
              │                               ▼
              │                       STUCK: can't build, can't verify
              │                       No recovery without restart
              └───────────────────────────────┘
```

**Unrecoverable state:** `CL_head > EL_head`, with no retry and no signal. Node is stuck until manual intervention.

**Missing:** `commit_hash` should return `Result<(), ()>` or `bool`, or at minimum emit `commit_hash_failures_total` so ops can alert.

---

## 4. Full FSM with Issue States Highlighted

```
                                    ┌─────────────────────────────────────────────┐
                                    │  IDLE                                       │
                                    └─────────────────────────────────────────────┘
                                                    │
                         start_building_block       │
                         ┌──────────────────────────┼──────────────────────────┐
                         │ Ok(pid)                  │ Err (any)                │
                         ▼                          ▼                          │
              ┌─────────────────────┐    ┌─────────────────────┐              │
              │  BUILDING           │    │  skip proposal       │              │
              └─────────────────────┘    │  (recoverable)       │              │
                         │              └─────────────────────┘              │
                         │                                                   │
         get_payload     │                                                   │
         ┌───────────────┼───────────────┐                                  │
         │ Some(payload)  │ None          │                                  │
         ▼               ▼               │                                  │
┌─────────────────┐  ┌─────────────────┐                                  │
│  HAVE_PAYLOAD   │  │  skip proposal   │                                   │
└─────────────────┘  │  (recoverable)   │                                   │
         │            └─────────────────┘                                   │
         │                                                                   │
         check_payload                                                       │
         ┌───────────────┬───────────────┬───────────────┐                   │
         │ Valid         │ Invalid       │ (transport)   │                   │
         ▼               ▼               ▼               │                   │
┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐         │
│  VERIFIED   │  │  vote NO    │  │  ⚠️ ISSUE: returns Invalid    │         │
│  (correct)  │  │  (correct   │  │  but meaning is "unreachable" │         │
└─────────────┘  │  if truly   │  │  → wrong consensus signal   │         │
         │        │  invalid)   │  │  → liveness risk              │         │
         │        └─────────────┘  └─────────────────────────────┘         │
         │                                                                   │
         commit_hash                                                         │
         ┌───────────────┬───────────────┐                                   │
         │ Ok            │ Err           │                                   │
         ▼               ▼               │                                   │
┌─────────────────┐  ┌─────────────────────────────────────────────┐     │
│  COMMITTED      │  │  🔴 CRITICAL: Silent failure                  │     │
│  CL_head=EL_head│  │  - Caller gets ()                             │     │
└─────────────────┘  │  - CL already advanced, EL did not           │     │
                      │  - Node stuck, no retry, no metric           │     │
                      │  - Unrecoverable without restart              │     │
                      └─────────────────────────────────────────────┘     │
                                                                           │
                                    ◄─────────────────────────────────────┘
                                              (next block)
```

---

## 5. Issues Summary (as FSM Properties)

| # | Issue | FSM State / Transition | Severity |
|---|-------|------------------------|----------|
| 1 | **commit_hash silent fail** | Transition to "Committed" can be believed by CL while EL never updated; no observable failure; leads to stuck state | Critical |
| 2 | **check_payload Invalid on transport** | Transport failure → Invalid; semantically wrong; causes vote-no on unverified block → liveness risk | High |
| 3 | **No commit_hash return value** | Caller cannot branch on failure; cannot retry or alert | Critical |
| 4 | **execute_blocks infinite loop** | Bench tool only; not production path | Low |
| 5 | **No Prometheus counters** | Failures in start_building_block, get_payload, check_payload, commit_hash are invisible to ops | Medium |
| 6 | **let _ = match antipattern** | Cosmetic; `Ok(res)` discarded in commit_hash | Low |

---

## 6. Recommended FSM Changes

| Change | Effect |
|--------|--------|
| `commit_hash(...) -> Result<(), CommitError>` | Caller can retry, alert, or halt |
| `check_payload` transport failure → `PayloadStatus::Syncing` | Honest "couldn't verify" signal; finalizer already handles Syncing |
| Emit `engine_client_commit_hash_failures_total` | Observability even if trait stays `()` |
| Emit `engine_client_check_payload_el_unreachable_total` | Distinguish EL errors from real Invalid |
