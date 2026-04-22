# Analysis of Pipelining Suggestions (Summit / Commonware / Simplex)

This note cross-checks the blog post against the current public upstream repos and, separately, the current Ritual forks.

## Public Upstream Commits

- `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`
- `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`

## Ritual Current State Commits

- `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`
- `ritual-summit-internal @ 2b9d783e70a109d69fe7013eaf03758ad6461191`

## Classification Legend

- ✅ Present in public upstream
- 🟡 The blog is proposing a real difference from public Summit behavior
- 🔴 Design change, not present in public upstream

---

## Glossary

- `View`: one consensus round / slot with an expected leader. A view is the container in which the protocol tries to make progress.
- `Proposal`: the leader's candidate block for a given view.
- `Notarization`: the certificate showing enough validators supported the proposal in that view.
- `Finalization`: the stronger certificate showing the proposal is finalized.
- `Nullification`: the certificate showing the view was skipped / timed out without a finalized proposal, allowing safe progress to the next view.

---

## Present In Public Upstream

### 1) Safe Parent = Only Requirement for Block Building

## Suggestion
Block building only requires identifying a fork where no conflicting finalized block can exist.

## Current State
✅ Public upstream: this is explicit in public Commonware, where the state machine walks backward until it finds a certified parent, skipping nullified views. Ritual current state: already present.

## Where To Look
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:553-599`
- Ritual current state: `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`: `consensus/src/simplex/actors/voter/state.rs:553-599`

## Takeaway
- This is not just "intended by design"; it is implemented directly in the parent-selection logic.

---

### 2) Pipelining / Overlapping Consensus Instances

## Suggestion
Start consensus on block `v+1` before finishing block `v`.

## Current State
✅ Public upstream: this exists at the consensus-engine level. In practice, pipelining here means the state machine does not wait for full completion of block `v` before preparing the machinery for `v+1`: it can derive the next leader, carry forward the certificate context needed for the next view, and keep certification work for one view in flight while continuing proposal / verification work for another. So yes, "they've decided the next leader" is part of it, but pipelining here is broader than just leader selection. Ritual current state: already present.

## Where To Look
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/actor.rs:843-860`
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:300-316`
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:605-628`
- Ritual current state: `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`: `consensus/src/simplex/actors/voter/actor.rs:913-923`

## Takeaway
- Pipelining is present in the consensus state machine, meaning consensus can overlap cross-view bookkeeping and certificate-driven progress before the execution layer starts building the next block.
- This should not be confused with Summit pre-building the next block early.

---

## Real Differences From Public Summit Behavior

### 3) Start Block Building Earlier
This is the general rule, with specific examples in 5) and 6)

## Suggestion
Do not wait until entering view `v` to start building block `v`.  
Instead, begin as soon as a safe parent is known (e.g. notarization or nullification).

## Current State
🟡 Public upstream: the blog is accurately identifying a real difference from upstream behavior. Public Commonware can determine a safe parent for the current view, but public Summit's block-building path is still driven by `propose` for the current view rather than by an earlier "safe parent is now known" trigger. Ritual current state: not yet implemented as an earlier safe-parent-triggered block-building path. If Ritual wanted to diverge here, this would likely be a `Commonware + Summit` edit: Commonware currently ties proposal construction to the current-view `propose` path, and Summit currently only starts EL work from that path.

## Where To Look
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:482-511`
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/round.rs:104-109`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/ingress.rs:59-75`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/actor.rs:320-474`
- Ritual current state: `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`: `consensus/src/simplex/actors/voter/state.rs:375-409`
- Ritual current state: `ritual-summit-internal @ 2b9d783e70a109d69fe7013eaf03758ad6461191`: `application/src/actor.rs:804-845`

## Takeaway
- Evaluate the latency benefit of earlier EL work against the engineering cost of adding a new pre-build trigger, plus the need to handle cancellation, parent invalidation, and coordination across the consensus / execution boundary.

---

### 4) Exploit Leader Predictability
This is precondition for the concrete suggestions in 5) and 6)

## Suggestion
Future proposers should start building blocks early because leader schedule is known.

## Current State
🟡 Public upstream: the blog is accurately pointing to a real unused capability. Public Summit wires in public Commonware `RoundRobin`, so leader predictability is present upstream, but it is not being used to trigger speculative or early block building. Ritual current state: already has predictable leaders at a high level, but not yet using that to trigger early block building. This is best understood as an operational enabler for the earlier-building ideas, not as the safety condition by itself.

## Where To Look
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/elector.rs:46-77`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `orchestrator/src/actor.rs:294-301`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/ingress.rs:59-75`
- Ritual current state: `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`: `consensus/src/simplex/elector.rs:46-77`
- Ritual current state: `ritual-summit-internal @ 2b9d783e70a109d69fe7013eaf03758ad6461191`: `crates/ritual-consensus/src/stake_weighted.rs:159-171`

## Takeaway
- Evaluate the latency win from proposer-specific pre-building against the downside of wasted work, mempool churn, and any operational or security concerns that come from making future proposers more behaviorally predictable.

---

### 5) Use Notarization as Trigger for Block Building

## Suggestion
Start building immediately after seeing a notarized block in the previous view.

## Current State
🟡 Public upstream: the blog is proposing a concrete trigger under the broader "start earlier once the parent is safe" rule. Public Commonware records notarization and later advances view after certification succeeds, while public Summit starts block building when it receives `Message::Propose`, not when notarization is first observed. Ritual current state: not yet implemented as an earlier notarization-triggered block-building path. If Ritual wanted to diverge here, this would likely be a `Commonware + Summit` edit: Commonware would need to surface an earlier notarization-derived hook, and Summit would need to consume it to start building sooner.

## Where To Look
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:300-316`
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:605-628`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/ingress.rs:59-75`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/actor.rs:124-136`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/actor.rs:320-474`
- Ritual current state: `ritual-summit-internal @ 2b9d783e70a109d69fe7013eaf03758ad6461191`: `application/src/ingress.rs:62-77`
- Ritual current state: `ritual-summit-internal @ 2b9d783e70a109d69fe7013eaf03758ad6461191`: `application/src/actor.rs:804-845`

## Takeaway
- Evaluate the latency benefit of using notarization as the earlier build trigger against the added complexity around cancellation, parent changes, wasted EL work, and race handling.

---

### 6) Use Nullification Certificates as Trigger

## Suggestion
If no block was proposed (nullification), that is also sufficient to safely start building.

## Current State
🟡 Public upstream: the blog is directionally accurate. Nullification is implemented and advances the view immediately in public Commonware, but public Summit still does not use nullification receipt itself as a dedicated trigger for earlier block building. Ritual current state: not yet implemented as a nullification-triggered early block-building path. If Ritual wanted to diverge here, this would likely be a `Commonware + Summit` edit: Commonware would need to surface nullification as an earlier build signal, and Summit would need to act on that signal.

## Where To Look
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:318-328`
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:553-599`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/ingress.rs:59-75`
- Public upstream: `SeismicSystems/summit @ 82719ced40f21768f765d1ff62c25ceb1e9c0a39`: `application/src/actor.rs:320-474`
- Ritual current state: `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`: `consensus/src/simplex/actors/voter/state.rs:250-255`
- Ritual current state: `ritual-summit-internal @ 2b9d783e70a109d69fe7013eaf03758ad6461191`: `application/src/actor.rs:804-845`

## Takeaway
- Evaluate the latency improvement available in nullified or stalled views against the extra implementation complexity and the risk of doing speculative execution-layer work that may later need to be discarded.

---

## Design Changes

### 7) Aggressive Mode: Economic Security Instead of Strict Safety

## Suggestion
Allow earlier block building based on weaker signals (e.g. partial messages),  
and rely on slashing / accountability if forks occur.

## Current State
🔴 Public upstream: this would be a real protocol/design change, and I did not find this behavior in public Commonware / Summit. Ritual current state: not yet present.

## Where To Look
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:300-328`
- Public upstream: `commonwarexyz/monorepo @ 3c4e02ceede03126f524216605a1195e1cee7d0e`: `consensus/src/simplex/actors/voter/state.rs:605-628`
- Ritual current state: `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`: `consensus/src/simplex/actors/voter/state.rs:232-255`
- Ritual current state: `ritual-commonware-internal @ 6957b2279aff6233a6254bf66478025613b52cf8`: `consensus/src/simplex/actors/voter/state.rs:483-502`

## Takeaway
- Current state transitions are certificate-driven.
- Moving to weaker preconditions plus economic accountability would require deliberate protocol work, not just a local implementation tweak.

---

## Main Feedback To The Blog Author

### What A Convincing Proof Sketch Should Contain

If I were giving feedback on the blog, this is the single most useful request I would make.

#### Ask for a proof sketch with these parts:

##### Definitions
Define exactly:
- notarization,
- finalization,
- nullification,
- safe parent,
- speculative block-building,
- cancellation.

##### Claim
State the claim precisely, for example:

> "If an honest proposer starts speculative block-building after observing condition X, then either:
> 1. the resulting parent remains valid for the next proposal, or
> 2. the work is discarded without affecting safety."

##### Adversarial Cases
Work through:
- forged / malformed certificate,
- delayed delivery of the real block body,
- equivocation by the leader,
- nullification racing with notarization,
- honest nodes with different local views,
- block body withheld after cert propagation,
- proposer crash / restart,
- stale mempool assumptions.

##### Bound The Bad Outcomes
For each bad case, say whether it can cause:
- only wasted work,
- liveness degradation,
- safety violation,
- or slashable evidence.

##### Show What Remains Unchanged
A convincing proposal should say which original Simplex / Commonware safety arguments remain untouched. That is often the biggest reassurance.

---

### Public Discussion / Source-Backed Points That Are Useful In This Review

These are not direct answers to your fork's design, but they do help frame the review.

#### Evidence That Overlapping Progress Is Already Part Of The Simplex Family
Commonware publicly describes moving to the next height as soon as the previous height is notarized, which is already a form of overlapping progress. That means the debate is **not** whether pipelining exists at all; it is about how far earlier execution-layer work should start, and on what trigger.

#### Evidence That "In-Flight Ambiguity" Is Real, Not Imaginary
The Commonware docs explicitly discuss the case where nullification may arrive before certification completes, while still recommending continued certification attempts because future honest progress may build on either outcome. That strongly supports your intuition that there are real edge cases here, and that the blog should explain them more rigorously.

#### Evidence That Pipelining In Consensus Usually Works By Reusing Phases / Overlapping Instances
The DSN paper on pipelining states that pipelining improves performance by giving one phase additional meaning and replacing consecutive phases for one block with a phase that simultaneously advances multiple blocks. That is useful context: pipelining is a known optimization pattern, but it does **not** automatically prove that any specific earlier trigger is safe.

## De-risking Questions

- Is the proposal only about **block construction**, or also about **block execution**? This is important. "Construct a candidate block template" is much weaker than "execute and commit to it." If the proposal only means prefetching, ordering transactions, and preparing a candidate template, that is much easier to accept than doing expensive execution off a parent that is not yet fully settled.

- Suggested risk taxonomy for evaluating these ideas:
- `Safety risk`: can this produce a conflicting valid proposal or cause state divergence?
- `Liveness risk`: can an adversary force repeated cancellations or delay honest proposals?
- `Resource risk`: can an adversary induce expensive wasted EL work?
- `Operational risk`: does predictable early work make future proposers easier to target?
- It may help to explicitly classify each failure mode and adversarial case under one or more of those buckets, rather than treating "risk" as a single undifferentiated concern.

- Can the proposal FSM / lifecycle be enumerated more clearly?
  - Commonware’s docs point out that even after observing a nullification, nodes should still continue certifying an earlier notarization because the next proposer may build on either outcome. That implies the system can have multiple plausible futures live at once, rather than nullification uniquely determining the parent. How does your proposal handle that ambiguity when starting early block building—i.e., how do you ensure this remains purely speculative and doesn’t prematurely commit to the wrong branch?
  - What if a node sees competing stories during propagation?
  - What if certification is still in flight when nullification arrives?
  - Does building on nullification vs notarization have different properties?
- What are the different types of bad notarizations, and do they have different outcomes (e.g. malformed message vs untrue message)?

- What is the failure mode if the early trigger was wrong? How much work is wasted if reth needs to roll back? Can we derive how often this would need to happen to be a net negative?
- What is the measured payoff? The note and blog argue that the current delay can exceed one second in nullified views. That is a plausible motivation, but I would still want:
  - distribution of savings, not just best case,
  - % of views where the earlier trigger actually helps,
  - % of speculative work discarded.
- What are the powers of an adversary if this is implemented? How much damage can they cause? How are they detected and then mitigated?
- Does leader predictability create operational or security downsides? I think this had DoS tradeoffs for Solana.

---

## Start of Derisking

### Reth Already Supports Speculative Block Building

At the execution-layer API level, Reth already supports a **build now, commit later** workflow. In Summit today, proposal construction calls `engine_forkchoiceUpdatedV3(..., payloadAttributes)` to start building a candidate payload, then later calls `engine_getPayloadV4(payload_id)` to retrieve it. That is already speculative in the narrow sense that the payload can be built before it is committed as the canonical head.

Example from `ritual-summit-internal/types/src/engine_client.rs`:

```rust
async fn start_building_block(
    &mut self,
    fork_choice_state: ForkchoiceState,
    timestamp: u64,
    withdrawals: Vec<Withdrawal>,
    extra_data: Option<alloy_primitives::Bytes>,
) -> Option<PayloadId> {
    let payload_attributes = PayloadAttributes { ... };
    let res = self
        .provider
        .fork_choice_updated_v3(fork_choice_state, Some(payload_attributes))
        .await
        .ok()?;
    res.payload_id
}
```

The matching commit step is separate:

```rust
async fn commit_hash(&mut self, fork_choice_state: ForkchoiceState) -> Result<(), String> {
    self.provider
        .fork_choice_updated_v3(fork_choice_state, None)
        .await?;
    Ok(())
}
```

That separation matters. It means the baseline question is not "can Reth build speculatively at all?" but rather "how much earlier can we safely trigger that build, and on what signal?"

### What This Does And Does Not Prove

This does **not** automatically prove the blog's stronger claim. There is a difference between:

- asking EL to build a candidate on top of the currently selected parent in the ordinary proposal path, and
- asking EL to start earlier based on a still-ambiguous future parent (for example, when notarization and nullification are both still plausible local futures).

So "Reth already supports speculative building" should be read as: the execution client already has a candidate-build mechanism, not that it already endorses arbitrary early building on any plausible branch.

### Can The Build Be Interrupted?

At the Summit layer, I did **not** find a dedicated "cancel this EL build" RPC or wrapper. The application actor can stop **waiting** for a proposal result if consensus moves on or drops the oneshot receiver, but that is not the same thing as explicitly canceling the EL build job.

In other words:

- Summit can abandon the request from the consensus side.
- I did not find source-backed evidence here that Summit tells Reth to actively kill an in-flight build.
- So the safe assumption is that a wrong early trigger may still consume some EL CPU / memory even if consensus no longer wants the result.

There is one useful spec detail: the Engine API allows the execution client to stop the corresponding build process **after** serving `engine_getPayload`. That suggests cleanup of completed builds is expected, but it is not the same as a proactive cancellation mechanism for no-longer-needed speculative work.

### How Easy Is It To Discard An Unused Build?

At the consensus / application boundary, discarding an unused build appears relatively easy:

- if the built payload is never broadcast or never finalized, it does not become canonical,
- final commitment is a later `forkchoiceUpdated(..., None)` step,
- so the common failure mode looks more like **wasted speculative work** than "deep rollback of finalized state."

That said, "easy to discard logically" is not the same as "free operationally." The wasted cost can still include:

- EL block-building CPU time,
- temporary payload storage / cache state in Reth,
- Summit-side bookkeeping for in-flight proposals,
- and, if the block was executed in the notarized-fork path, temporary fork-state storage in the finalizer.

### Important Caveat About Alternate Parents

One concrete thing to test before relying on any earlier-trigger design: building on a non-tip historical ancestor is not obviously free-form. There are public Reth / Engine-API discussions indicating that `forkchoiceUpdated(..., payloadAttributes)` may return `VALID` but `payloadId: null` when targeting a valid ancestor of the current canonical head. So if the design depends on "just start building on some older alternative parent," that behavior should be verified against the exact Reth version in use.
