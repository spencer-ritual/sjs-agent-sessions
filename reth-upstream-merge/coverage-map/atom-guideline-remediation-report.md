# Atom Guideline Remediation Report

## Summary

- Reclassified unsupported filename/path-only mappings away from `moved_to_dependency` or `structural_equivalent`.
- Reclassified unapproved `intentionally_absent` atoms to `blocked` pending explicit approval or obsolete-behavior citation.
- Marked broad derived atoms with `needs_atomization` so they are not treated as indivisible code facts until split or merged.
- Regenerated `index.jsonl`, `review-queue.md`, and `validation-summary.json` from canonical file artifacts.

## Counts After Remediation

- Atoms total: 717
- Mapping statuses: `{'structural_equivalent': 219, 'missing': 347, 'intentionally_absent': 10, 'exact': 93, 'blocked': 34, 'noise': 4, 'covered_by_upstream': 4, 'moved_to_dependency': 6}`
- File classifications: `{'noise': 284, 'mapped': 168, 'missing': 114, 'blocked': 13}`
- Human review queue entries: 592
- Broad derived atoms marked for atomization: 130

## Explicit Atom Changes

- No explicit atom changes were required.

## Validation

- Validation errors: none
