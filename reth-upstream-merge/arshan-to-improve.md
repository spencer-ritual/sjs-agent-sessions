# Arshan To Improve

This file captures targeted improvements for Arshan's upstream-merge approach.

## Separate Sequencing Rights From Payload Control Flow

- **Suggestion:** extract sequencing-rights ordering into a dedicated module or nodebuilder payload component instead of leaving it embedded directly in the main payload-builder flow.
- **Why:** sequencing rights are a distinct Ritual block-construction policy. Keeping the classification and reordering logic separated makes it easier to review, test, and eventually move behind a clean `PayloadBuilderBuilder` / Ritual payload component boundary.
- **Current concern:** Arshan's latest shape is strong because scheduled and async payload behavior now lives in nodebuilder, but sequencing-rights logic should follow the same separation principle. If it stays mixed into the broader payload loop, future Reth payload updates become harder to merge and behavioral review becomes more expensive.
- **Better end state:** a small sequencing-rights helper/component that receives prepared payload candidates, classifies them, applies the ordering rule, and returns the reordered candidate list without owning unrelated scheduled, async, gas, or size-limit logic.
- **Review probes:** compare Arshan against old `dev` for top-level sequencing-rights classification, optional full-call-graph classification, mixed scheduled/async/regular candidate ordering, and verifier replay of the final ordering.
