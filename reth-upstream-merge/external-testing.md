# External Reth Behavior Testing

## Understanding

The goal is to design tests that can be run against a reth instance as an external system, independent of which source branch, local checkout, or image produced that instance. These tests should answer: "Does this reth behave like the downstream Ritual fork where it matters?"

This is different from checking whether the current port branch is internally consistent, and different from running focused Rust unit tests that already live in one implementation. Unit tests can still be useful as hints or as examples of intended behavior, but they are not the deliverable. The deliverable is an external conformance-style test suite that can be pointed at any candidate reth node or reth image.

## How To Use The Coverage Maps

There are two coverage maps:

- `coverage-map/` is a first pass.
- `coverage-map-fresh-restart-gpt55/` is a second pass.

Neither map is authoritative. Both maps are research aids. For a given source file, the right workflow is:

1. Read both map records for that file.
2. Union all unique atoms from both records.
3. Treat every atom claim, destination mapping, risk label, and test candidate as a hypothesis.
4. Verify each hypothesis against source behavior and destination behavior before relying on it.
5. Translate verified behavior into an external test only when the behavior can be observed or falsified from outside a reth instance.

If the maps disagree, that disagreement is useful signal, not something to smooth over. It usually means the atom needs independent verification before it becomes a test requirement.

## Test Design Bar

The tests should preserve behavior across reth instances, not source layouts. A passing test should not depend on:

- a local checkout path,
- a private Rust symbol,
- a particular module layout,
- a unit test name,
- or evidence that code exists in a specific branch.

The test should depend on externally observable behavior: RPC responses, accepted or rejected transactions, block validity, payload building results, chain state transitions, logs/receipts, settlement effects, and verifier/builder agreement.

Happy-path traffic is not enough. The useful tests should include guards, rejection paths, ordering constraints, duplicate handling, malformed inputs, stale or expired state, wrong executor/capability behavior, and builder/verifier disagreement cases.

## What "External" Likely Means

For each verified atom, classify whether it can be tested by:

- running one or more nodes and sending RPC calls,
- building and submitting transactions,
- asking the engine API to validate payloads,
- replaying blocks or payloads through a candidate node,
- comparing two candidate images on the same stimulus,
- or using a small harness that drives node state and inspects receipts/state roots.

Some atoms may not be directly testable from outside the process. For those, the document should say so explicitly and identify the closest observable proxy.

## Reference Testing Patterns

The intended shape is closer to the `ritual-node-internal` and `traffic-gen-internal` harnesses than to in-crate reth tests.

`ritual-node-internal` PR 350 (`spencer/rum-test-improvements`) is a useful reference pattern. It adds a shared E2E harness and a matrix test for short async precompile lifecycles. The important properties are:

- it drives an isolated node through public behavior,
- it registers mock executors and funds users through normal chain interactions,
- it sends real precompile consumer transactions,
- it observes commitment transactions, settlement transactions, receipts, decoded `spcCalls`, job creation, and job cleanup,
- and it makes the tested behavior table-driven by precompile/capability rather than tied to one source implementation.

That is the style of test this document should aim for: a reusable external stimulus plus observable pass/fail conditions.

Before creating a new conformance test for an atom, first search for an existing user journey that already exercises most of the behavior. Prefer strengthening that journey with stricter assertions over adding a near-duplicate test. Create a new test or file when the atom needs a distinct stimulus, harness mode, fixture, or failure boundary that would make an existing journey unclear or overbroad.

`traffic-gen-internal` provides the other useful pattern: `make run-*` commands that exercise deployed or local nodes through user-level traffic. Examples include async calls, scheduled calls, long-running HTTP phase 1/phase 2 flows, x402 flows, multimodal calls, sovereign agent calls, persistent agent spawning, and helper probes such as `scheduled-txs` and `commitment-tx`.

Those commands are valuable because they already package real user journeys. For conformance testing, they may need stricter assertions than normal traffic generation. A workload that merely "runs" is not enough; the test wrapper should assert the exact observable behavior implied by the atom.

## Harness Levels

Use two levels of external testing, in increasing cost:

1. Node E2E harness tests, like `make test-e2e TEST=test_async_short_matrix` in `ritual-node-internal`. These are best for deterministic CI coverage because they can run a controlled isolated node, mock executors, and inspect blocks/receipts/state.
2. Traffic-gen action tests, like `make run-scheduled-http`, `make run-long-running-echo`, or `make run-sovereign-agent-call`. These are best for production-like user journeys and cross-service wiring.
3. Potentially: State Fixture Replay Tests - replay a small genesis plus one or more prepared payloads/blocks through a candidate node, then assert Engine API status and externally visible post-state such as receipts, logs, balances, storage, and block validity.

The same atom can map to more than one level. The preferred first implementation should be the cheapest level that can falsify the behavior.

## What To Assert

External tests should assert outcomes, not implementation evidence. Every test should assert one or more of these observable categories:

1. Admission: whether the node accepts or rejects the stimulus correctly, such as transaction submission, Engine API payload status, or malformed input rejection.
2. Inclusion / Ordering: whether the expected objects appear in the chain in the expected place, such as system transactions, scheduled transactions, commitment-before-settlement ordering, transaction type, or sender.
3. State Transition: whether chain state changes correctly, such as balances, storage, async job creation/removal, reward payment, nonce locks, or settlement cleanup.
4. Output Surface: whether externally visible outputs match, such as receipts, logs, decoded `spcCalls`, returned RPC fields, final block validity, or verifier/builder agreement.

For negative cases, prefer a stimulus that differs from the valid case by one fact, such as wrong precompile capability, wrong event topic, expired TTL, duplicate result, malformed input, insufficient fee, wrong sender, overlarge `extra_data`, stale scheduled call, or active async job conflict.

## Commit Discipline

When implementing these tests and the user asks for commits, keep commits unitized by atom or tightly related invariant. A commit should represent one externally observable behavior now caught by E2E, not a broad batch of unrelated coverage.

Commit messages should say what invariant the E2E now catches, in the same direct style as:

- `test: cover async sender-lock admission`
- `test: assert malformed async tx side effects`
- `test: catch fulfilled-original replay metadata`

Before committing, verify the specific E2E target that covers the invariant and mention that command in the handoff.