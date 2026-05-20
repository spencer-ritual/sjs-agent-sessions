#!/usr/bin/env python3
"""Apply the non-exact atom guideline audit remediation.

This is an artifact-only migration for the coverage map. It does not inspect or
modify implementation repositories.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from copy import deepcopy
from datetime import datetime
from pathlib import Path


COVERAGE_ROOT = Path(__file__).resolve().parent
FILES_DIR = COVERAGE_ROOT / "files"
INDEX_PATH = COVERAGE_ROOT / "index.jsonl"
REVIEW_QUEUE_PATH = COVERAGE_ROOT / "review-queue.md"
VALIDATION_SUMMARY_PATH = COVERAGE_ROOT / "validation-summary.json"
REPORT_PATH = COVERAGE_ROOT / "atom-guideline-remediation-report.md"

MAPPED_STATUSES = {
    "exact",
    "renamed_exact",
    "covered_by_upstream",
    "moved_to_dependency",
    "structural_equivalent",
}
NON_EXACT_STATUSES = {
    "covered_by_upstream",
    "moved_to_dependency",
    "structural_equivalent",
    "intentionally_absent",
    "missing",
    "blocked",
}
EQUIVALENCE_REQUIRED = {
    "covered_by_upstream",
    "moved_to_dependency",
    "structural_equivalent",
}

CRITICAL_MISSING = {
    "file-0081-atom-0006": "The public `reth-node-ethereum/async-context` feature no longer exists in the port. Treat as missing unless a human explicitly approves the public API removal.",
}

FILENAME_ONLY_MOVED_HIGH_RISK = {
    "file-0091-atom-0001",
    "file-0218-atom-0001",
    "file-0226-atom-0001",
    "file-0283-atom-0001",
    "file-0287-atom-0001",
    "file-0297-atom-0001",
    "file-0304-atom-0001",
    "file-0348-atom-0001",
    "file-0352-atom-0001",
    "file-0416-atom-0001",
    "file-0420-atom-0001",
    "file-0422-atom-0001",
    "file-0535-atom-0001",
}

FILENAME_ONLY_MOVED_NON_HIGH_RISK = {
    "file-0062-atom-0001",
    "file-0098-atom-0001",
    "file-0222-atom-0001",
    "file-0248-atom-0001",
    "file-0250-atom-0001",
    "file-0311-atom-0001",
    "file-0314-atom-0001",
    "file-0340-atom-0001",
    "file-0341-atom-0001",
    "file-0431-atom-0001",
}

INTENTIONALLY_ABSENT_RATIONALES = {
    "file-0047-atom-0001": {
        "basis": "destination_absence_of_diagnostic_callsite",
        "rationale": "The downstream `tracing` dependency only supported Ritual debug/error logging in consensus validation; the v2.2 port has no corresponding tracing call sites, so the manifest dependency is obsolete rather than a behavior gap.",
    },
    "file-0056-atom-0001": {
        "basis": "destination_absence_of_metrics_callsite",
        "rationale": "The downstream `ritual-metrics` dependency only supported engine-tree Ritual instrumentation that is absent from the v2.2 port; the manifest edge has no active destination consumer.",
    },
    "file-0077-atom-0002": {
        "basis": "destination_absence_of_diagnostic_callsite",
        "rationale": "The downstream `tracing` dependency only supported debug logging in `reth-evm-ethereum`; the ported block assembler has no corresponding logging call site.",
    },
    "file-0081-atom-0006": {
        "basis": "user_approved_api_surface_non_goal",
        "rationale": "The user explicitly approved dropping the public `reth-node-ethereum/async-context` Cargo feature as an API-surface detail, provided the Reth chain preserves the same async-context runtime behavior elsewhere.",
    },
    "file-0082-atom-0001": {
        "basis": "user_approved_api_surface_non_goal",
        "rationale": "The user explicitly approved dropping old `reth_node_ethereum::spc` module-surface compatibility as an API detail, provided SPC/runtime verification behavior is preserved through the active chain path.",
    },
    "file-0082-atom-0002": {
        "basis": "user_approved_api_surface_non_goal",
        "rationale": "The user explicitly approved dropping the old crate-root `SpcVerifierImpl` re-export as an API detail, provided SPC/runtime verification behavior is preserved through the active chain path.",
    },
    "file-0212-atom-0001": {
        "basis": "documented_scope_exclusion",
        "rationale": "The current v2.2/Summit port explicitly scopes old `crates/optimism/*` members out via `MERGE_NOTES.md`, so OP receipt-root behavior is outside the active merge target rather than missing Ethereum/Summit behavior.",
    },
    "file-0221-atom-0001": {
        "basis": "documented_scope_exclusion",
        "rationale": "The current v2.2/Summit port explicitly scopes old OP primitives out via `MERGE_NOTES.md`, so `OpReceipt` EIP-7702 handling is outside the active merge target rather than missing Ethereum/Summit behavior.",
    },
}

GENERIC_STRUCTURAL_TO_RECLASSIFY = {
    "file-0090-atom-0001": {
        "status": "missing",
        "claim": "Payload builder config should expose downstream build-deadline and max-block-size configuration behavior; same-path overlap alone does not prove this behavior in the v2.2 port.",
        "required_change": "Restore the build-deadline and max-block-size configuration behavior, or provide precise destination code evidence and an equivalence argument for the replacement.",
    },
    "file-0385-atom-0001": {
        "status": "blocked",
        "claim": "Fee-history behavior changed in the downstream diff, but the current same-path/overlapping-symbol evidence does not establish the exact fee-history behavior preserved by the v2.2 port.",
        "required_change": "Audit the fee-history diff into indivisible behavior atoms and either attach precise destination evidence or mark the concrete missing behavior.",
    },
}

HIGH_RISK_FIXES = {
    "file-0249-atom-0001": "Negative-path permanent precompile request eviction is high-risk because it affects txpool/payload rejection semantics.",
}

USER_APPROVED_STRUCTURAL_EQUIVALENTS = {
    "file-0087-atom-0011": {
        "rationale": "The user explicitly approved replacing the old opt-in payload `async-context` feature gate with always-on dependency wiring, provided runtime async-context behavior is preserved.",
    }
}

USER_REQUIRED_PAYLOAD_LOCAL_BEHAVIORS = {
    "file-0087-atom-0005": {
        "priority": "low",
        "decision": "Payload-local Ritual metrics are desired. They are the lowest priority of the payload-local behavior set, but should not be treated as an intentional drop.",
        "required_change": "Restore useful payload-local `ritual-metrics` instrumentation for Ritual payload paths, or provide destination evidence for equivalent operational metrics.",
    },
    "file-0087-atom-0006": {
        "priority": "high",
        "decision": "Sequencing-rights classification and reordering must preserve old chain behavior.",
        "required_change": "Restore or prove equivalent sequencing-rights-based transaction classification and reordering in the payload build path.",
    },
    "file-0087-atom-0007": {
        "priority": "high",
        "decision": "Heartbeat hydration/tracking is important runtime behavior for scheduled/async execution.",
        "required_change": "Restore or prove equivalent payload-local heartbeat tracking and hydration behavior used during scheduled or async execution.",
    },
    "file-0087-atom-0010": {
        "priority": "medium",
        "decision": "Rayon-backed preparation/performance behavior should be kept if it was part of the downstream performance work.",
        "required_change": "Restore or prove equivalent downstream Rayon-backed payload preparation behavior used for scheduled and async transaction handling.",
    },
}

GENERIC_CLAIM_PHRASE = "introduces behavior or wiring that must be accounted for"
FILENAME_ONLY_PHRASE = "uniquely named destination file"
BROAD_ATOMIZATION_NOTE = (
    "Guideline remediation: broad derived claim marked for atomization; it should not be "
    "treated as a precise code fact until split or merged."
)
STALE_INTENTIONAL_BLOCK_NOTE = (
    "Guideline remediation: blocked because the `intentionally_absent` status lacks an "
    "explicit human approval or obsolete-behavior citation."
)


def load_records() -> list[dict]:
    records = []
    for path in sorted(FILES_DIR.glob("file-*.json")):
        records.append(json.loads(path.read_text()))
    return records


def atom_id(atom: dict) -> str:
    return atom.get("record_id") or atom.get("atom_id")


def ensure_list(atom: dict, key: str) -> list:
    value = atom.get(key)
    if not isinstance(value, list):
        value = []
        atom[key] = value
    return value


def ensure_adversarial(atom: dict) -> dict:
    review = atom.get("adversarial_review")
    if not isinstance(review, dict):
        review = {
            "required": False,
            "status": "not_requested",
            "review_record_id": None,
        }
        atom["adversarial_review"] = review
    review.setdefault("required", False)
    review.setdefault("status", "not_requested")
    review.setdefault("review_record_id", None)
    return review


def append_note(atom: dict, note: str) -> None:
    existing = atom.get("notes")
    if existing:
        if note not in existing:
            atom["notes"] = f"{existing} {note}"
    else:
        atom["notes"] = note


def record_change(changes: list[str], change: str | None) -> None:
    if change:
        changes.append(change)


def set_blocked(atom: dict, reason: str, *, high_risk: bool | None = None) -> str | None:
    old = atom.get("mapping_status")
    atom["mapping_status"] = "blocked"
    atom["equivalence_argument"] = None
    atom["review_required"] = True
    atom["required_change"] = (
        "Re-audit this atom into specific behavior facts and provide code-backed "
        "equivalence, or reclassify each concrete behavior as missing."
    )
    atom["human_question"] = reason
    if high_risk is not None:
        atom["high_risk"] = high_risk
    if atom.get("high_risk"):
        review = ensure_adversarial(atom)
        review["required"] = True
        ensure_list(atom, "risk_tags")
    append_note(atom, f"Guideline remediation: blocked because {reason}")
    if old == "blocked":
        return None
    return f"{atom_id(atom)}: {old} -> blocked"


def set_missing(atom: dict, reason: str, required_change: str | None = None) -> str | None:
    old = atom.get("mapping_status")
    atom["mapping_status"] = "missing"
    atom["destinations"] = []
    atom["equivalence_argument"] = None
    atom["review_required"] = True
    atom["required_change"] = required_change or reason
    atom.pop("human_question", None)
    if atom.get("high_risk"):
        review = ensure_adversarial(atom)
        review["required"] = True
    append_note(atom, f"Guideline remediation: marked missing because {reason}")
    if old == "missing":
        return None
    return f"{atom_id(atom)}: {old} -> missing"


def set_intentionally_absent(atom: dict, basis: str, rationale: str) -> str | None:
    old = atom.get("mapping_status")
    atom["mapping_status"] = "intentionally_absent"
    atom["equivalence_argument"] = None
    atom["review_required"] = False
    atom["required_change"] = None
    atom["human_question"] = None
    if basis == "user_approved_api_surface_non_goal":
        atom["high_risk"] = False
        atom["risk_tags"] = []
    atom["intentional_absence_basis"] = basis
    atom["intentional_absence_rationale"] = rationale
    notes = atom.get("notes")
    if isinstance(notes, str) and STALE_INTENTIONAL_BLOCK_NOTE in notes:
        notes = notes.replace(STALE_INTENTIONAL_BLOCK_NOTE, "").strip()
        while "  " in notes:
            notes = notes.replace("  ", " ")
        atom["notes"] = notes or None
    review = ensure_adversarial(atom)
    if not atom.get("high_risk"):
        review["required"] = False
    append_note(atom, f"Guideline remediation: accepted as intentionally absent because {rationale}")
    if old == "intentionally_absent":
        return None
    return f"{atom_id(atom)}: {old} -> intentionally_absent"


def set_user_approved_structural_equivalent(atom: dict, rationale: str) -> str | None:
    old = atom.get("mapping_status")
    atom["mapping_status"] = "structural_equivalent"
    atom["equivalence_argument"] = (
        "The old crate-local feature gate is not preserved as an API surface, but the destination "
        "hard-enables the same async-context runtime capability through explicit dependency "
        f"features. {rationale}"
    )
    atom["review_required"] = False
    atom["human_question"] = None
    atom["required_change"] = None
    atom.pop("intentional_absence_basis", None)
    atom.pop("intentional_absence_rationale", None)
    review = ensure_adversarial(atom)
    if atom.get("high_risk"):
        review["required"] = True
    else:
        review["required"] = False
    append_note(atom, f"User scope decision: {rationale}")
    if old == "structural_equivalent":
        return None
    return f"{atom_id(atom)}: {old} -> structural_equivalent"


def apply_user_required_payload_behavior(atom: dict, decision: dict) -> None:
    atom["user_required_behavior"] = True
    atom["user_priority"] = decision["priority"]
    atom["user_scope_decision"] = decision["decision"]
    atom["review_required"] = True
    atom["required_change"] = decision["required_change"]
    if atom.get("mapping_status") == "intentionally_absent":
        atom["mapping_status"] = "missing"
        atom.pop("intentional_absence_basis", None)
        atom.pop("intentional_absence_rationale", None)
    append_note(atom, f"User scope decision: {decision['decision']}")


def backfill_intentional_absence_rationale(atom: dict) -> None:
    if atom.get("mapping_status") != "intentionally_absent":
        return
    if atom.get("intentional_absence_basis") and atom.get("intentional_absence_rationale"):
        return
    atom["intentional_absence_basis"] = "existing_scope_or_dormant_surface_rationale"
    atom["intentional_absence_rationale"] = (
        atom.get("notes")
        or "Existing coverage-map classification treats this atom as intentionally absent rather than a current active-chain behavior gap."
    )


def ensure_high_risk_non_exact_review_coverage(atom: dict) -> None:
    if not atom.get("high_risk"):
        return
    status = atom.get("mapping_status")
    if status in {"exact", "renamed_exact"}:
        return
    if (
        status == "intentionally_absent"
        and atom.get("intentional_absence_basis")
        and atom.get("intentional_absence_rationale")
    ):
        return
    if atom.get("review_required"):
        return
    review = ensure_adversarial(atom)
    review["required"] = True


def mark_high_risk(atom: dict, reason: str) -> str | None:
    old = atom.get("high_risk")
    atom["high_risk"] = True
    risks = ensure_list(atom, "risk_tags")
    if "negative-path" not in risks:
        risks.append("negative-path")
    atom["review_required"] = True
    review = ensure_adversarial(atom)
    review["required"] = True
    if not atom.get("negative_test_candidate"):
        atom["negative_test_candidate"] = (
            "Trigger the negative-path behavior and assert the destination rejects "
            "or evicts the input with the preserved hard-invalid semantics."
        )
    append_note(atom, f"Guideline remediation: marked high-risk because {reason}")
    if old is True:
        return None
    return f"{atom_id(atom)}: high_risk {old} -> true"


def is_generic_filename_only(atom: dict) -> bool:
    text = " ".join(
        str(atom.get(k) or "")
        for k in ("semantic_claim", "equivalence_argument", "notes", "human_question")
    ).lower()
    for dest in atom.get("destinations") or []:
        text += " " + str(dest.get("evidence") or "").lower()
    return GENERIC_CLAIM_PHRASE in text or FILENAME_ONLY_PHRASE in text


def is_derived(atom: dict) -> bool:
    return any(
        atom.get(flag)
        for flag in (
            "test_derived",
            "feature_derived",
            "functionality_flow_derived",
            "pr_preservation_derived",
        )
    )


def looks_broad(atom: dict) -> bool:
    text = " ".join(
        str(atom.get(k) or "")
        for k in ("semantic_claim", "required_change", "human_question")
    ).lower()
    broad_phrases = (
        "introduces behavior or wiring",
        "must be accounted for",
        "feature-preservation invariant",
        "pr-preservation invariant",
        "flow-derived invariant",
        "verify and restore this feature-preservation",
        "verify and restore this pr-preservation",
    )
    return any(phrase in text for phrase in broad_phrases)


def clear_atomization_marker_if_needed(atom: dict) -> None:
    if not atom.get("needs_atomization"):
        return
    atom.pop("needs_atomization", None)
    notes = atom.get("notes")
    if isinstance(notes, str) and BROAD_ATOMIZATION_NOTE in notes:
        notes = notes.replace(BROAD_ATOMIZATION_NOTE, "").strip()
        while "  " in notes:
            notes = notes.replace("  ", " ")
        atom["notes"] = notes or None


def update_file_rollups(record: dict) -> None:
    atoms = record.get("atoms") or []
    record["atoms_total"] = len(atoms)
    for idx, atom in enumerate(atoms, start=1):
        atom["atom_index"] = idx
        atom["atoms_total"] = len(atoms)

    high_risk = sum(1 for atom in atoms if atom.get("high_risk"))
    non_exact = sum(1 for atom in atoms if atom.get("mapping_status") in NON_EXACT_STATUSES)
    review_required = any(atom.get("review_required") for atom in atoms)
    statuses = [atom.get("mapping_status") for atom in atoms]

    if not atoms:
        classification = "noise"
    elif any(status == "missing" for status in statuses):
        classification = "missing"
    elif any(status == "blocked" for status in statuses):
        classification = "blocked"
    elif all(status == "noise" for status in statuses):
        classification = "noise"
    else:
        classification = "mapped"

    record["file_classification"] = classification
    record["high_risk_atoms_total"] = high_risk
    record["non_exact_atoms_total"] = non_exact
    record["review_required"] = review_required
    record["status"] = "needs_review" if review_required or classification in {"missing", "blocked"} else "complete"

    tags = set(record.get("tags") or [])
    tags.difference_update({"mapped", "missing", "blocked", "noise"})
    tags.add(classification)
    if high_risk:
        tags.add("high-risk")
    else:
        tags.discard("high-risk")
    if non_exact:
        tags.add("non-exact")
    else:
        tags.discard("non-exact")
    if record["status"] == "needs_review":
        tags.add("needs-review")
    else:
        tags.discard("needs-review")
    record["tags"] = sorted(tags)


def remediation_pass(records: list[dict]) -> list[str]:
    changes = []
    for record in records:
        for atom in record.get("atoms") or []:
            rid = atom_id(atom)
            if not rid:
                continue
            if rid in INTENTIONALLY_ABSENT_RATIONALES:
                rationale = INTENTIONALLY_ABSENT_RATIONALES[rid]
                record_change(
                    changes,
                    set_intentionally_absent(
                        atom,
                        rationale["basis"],
                        rationale["rationale"],
                    ),
                )
            elif rid in CRITICAL_MISSING:
                record_change(changes, set_missing(atom, CRITICAL_MISSING[rid]))
            elif rid in FILENAME_ONLY_MOVED_HIGH_RISK:
                record_change(
                    changes,
                    set_blocked(
                        atom,
                        "filename/path similarity is not evidence of preserved behavior, guards, transitions, side effects, or failure paths.",
                        high_risk=True,
                    ),
                )
            elif rid in FILENAME_ONLY_MOVED_NON_HIGH_RISK:
                record_change(
                    changes,
                    set_blocked(
                        atom,
                        "filename/path similarity is not evidence of preserved behavior.",
                    ),
                )
            elif rid in GENERIC_STRUCTURAL_TO_RECLASSIFY:
                fix = GENERIC_STRUCTURAL_TO_RECLASSIFY[rid]
                atom["semantic_claim"] = fix["claim"]
                if fix["status"] == "missing":
                    record_change(
                        changes, set_missing(atom, fix["required_change"], fix["required_change"])
                    )
                else:
                    record_change(
                        changes,
                        set_blocked(atom, fix["required_change"], high_risk=atom.get("high_risk")),
                    )
            elif rid in HIGH_RISK_FIXES:
                record_change(changes, mark_high_risk(atom, HIGH_RISK_FIXES[rid]))
            elif rid in USER_APPROVED_STRUCTURAL_EQUIVALENTS:
                record_change(
                    changes,
                    set_user_approved_structural_equivalent(
                        atom,
                        USER_APPROVED_STRUCTURAL_EQUIVALENTS[rid]["rationale"],
                    ),
                )
            elif rid in USER_REQUIRED_PAYLOAD_LOCAL_BEHAVIORS:
                apply_user_required_payload_behavior(atom, USER_REQUIRED_PAYLOAD_LOCAL_BEHAVIORS[rid])

            backfill_intentional_absence_rationale(atom)
            ensure_high_risk_non_exact_review_coverage(atom)

            if is_derived(atom):
                clear_atomization_marker_if_needed(atom)

            if is_derived(atom) and looks_broad(atom):
                atom["needs_atomization"] = True
                atom["review_required"] = True
                atom["required_change"] = (
                    atom.get("required_change")
                    or "Split this broad derived claim into indivisible branch, guard, transition, side-effect, or error-path atoms before using it as actionable coverage."
                )
                append_note(atom, BROAD_ATOMIZATION_NOTE)

        update_file_rollups(record)
    return changes


def write_records(records: list[dict]) -> None:
    for record in records:
        path = FILES_DIR / f"file-{record['file_index']:04d}.json"
        path.write_text(json.dumps(record, indent=2, sort_keys=False) + "\n")


def review_line_for_atom(record: dict, atom: dict) -> str:
    rid = atom_id(atom)
    hunk = atom.get("source_hunk_hint") or "unknown"
    likely = "unknown"
    for dest in atom.get("destinations") or []:
        repo = dest.get("repo")
        path = dest.get("path")
        if repo and path:
            likely = f"{repo}/{path}"
            break
    if atom.get("required_change"):
        action_label = "Required change"
        action = atom["required_change"]
    else:
        action_label = "Human question"
        action = atom.get("human_question") or (
            "Confirm whether this non-exact mapping is acceptable under the behavioral-equivalence guideline."
        )
    return (
        f"- Key: `file_index={record['file_index']}`, `source_path={record['source_path']}`, `record_id={rid}`\n"
        f"  - Source hunk: `{hunk}`\n"
        f"  - {action_label}: {action}\n"
        f"  - Likely destination: `{likely}`\n"
    )


def write_review_queue(records: list[dict]) -> int:
    lines = ["# Coverage Review Queue", ""]
    total = 0
    for record in records:
        entries = []
        for atom in record.get("atoms") or []:
            status = atom.get("mapping_status")
            if status in {"missing", "blocked"} or atom.get("review_required"):
                entries.append(review_line_for_atom(record, atom))
        if entries:
            lines.append(f"## File {record['file_index']:04d}: {record['source_path']}")
            lines.append("")
            for entry in entries:
                lines.append(entry.rstrip())
                lines.append("")
                total += 1
    REVIEW_QUEUE_PATH.write_text("\n".join(lines).rstrip() + "\n")
    return total


def write_index(records: list[dict]) -> None:
    with INDEX_PATH.open("w") as fh:
        for record in records:
            row = {
                "file_index": record["file_index"],
                "artifact": f"coverage-map/files/file-{record['file_index']:04d}.json",
                "source_status": record.get("source_status"),
                "source_path": record.get("source_path"),
                "file_classification": record.get("file_classification"),
                "atoms_total": record.get("atoms_total"),
                "high_risk_atoms_total": record.get("high_risk_atoms_total"),
                "non_exact_atoms_total": record.get("non_exact_atoms_total"),
                "status": record.get("status"),
                "review_required": record.get("review_required"),
                "summary": record.get("summary"),
            }
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")


def validate(records: list[dict], review_queue_total: int) -> tuple[dict, list[str]]:
    errors: list[str] = []
    expected = list(range(1, 580))
    actual = [record.get("file_index") for record in records]
    if actual != expected:
        errors.append("file_indices_are_not_exactly_1_to_579")
    if len(records) != 579:
        errors.append("coverage_map_does_not_have_579_file_artifacts")

    atom_status = Counter()
    file_classification = Counter()
    file_status = Counter()
    review_status = Counter()
    high_risk_total = 0
    non_exact_total = 0
    atoms_total = 0
    derived_total = 0
    broad_derived_total = 0

    for record in records:
        atoms = record.get("atoms") or []
        if record.get("atoms_total") != len(atoms):
            errors.append(f"{record['file_index']}: atoms_total mismatch")
        if record.get("file_classification") != "noise" and not atoms:
            errors.append(f"{record['file_index']}: non-noise file has no atoms")
        file_classification[record.get("file_classification")] += 1
        file_status[record.get("status")] += 1
        atoms_total += len(atoms)
        for atom in atoms:
            rid = atom_id(atom)
            status = atom.get("mapping_status")
            atom_status[status] += 1
            if atom.get("high_risk"):
                high_risk_total += 1
            if status in NON_EXACT_STATUSES:
                non_exact_total += 1
            if is_derived(atom):
                derived_total += 1
            if atom.get("needs_atomization"):
                broad_derived_total += 1
            review = ensure_adversarial(atom)
            review_status[review.get("status")] += 1
            if review.get("required"):
                review_status["required"] += 1
            if status in MAPPED_STATUSES and status not in {"exact", "renamed_exact"}:
                if not atom.get("destinations"):
                    errors.append(f"{rid}: mapped status lacks destination evidence")
                if status in EQUIVALENCE_REQUIRED and not atom.get("equivalence_argument"):
                    errors.append(f"{rid}: equivalence-required status lacks argument")
            if atom.get("high_risk") and status not in {"exact", "renamed_exact"}:
                if (
                    status == "intentionally_absent"
                    and atom.get("intentional_absence_basis")
                    and atom.get("intentional_absence_rationale")
                ):
                    pass
                elif not atom.get("review_required") and not review.get("required"):
                    errors.append(f"{rid}: high-risk non-exact atom lacks review coverage")
            if atom.get("high_risk"):
                strategy = atom.get("test_strategy")
                candidate = atom.get("negative_test_candidate")
                if not strategy:
                    errors.append(f"{rid}: high-risk atom lacks test_strategy")
                if strategy not in {"not_testable", "not_needed"} and not candidate:
                    errors.append(f"{rid}: high-risk atom lacks negative_test_candidate")
            if status == "intentionally_absent" and not atom.get("review_required"):
                if not atom.get("intentional_absence_basis") or not atom.get(
                    "intentional_absence_rationale"
                ):
                    errors.append(f"{rid}: accepted intentionally_absent atom lacks rationale")

    summary_counts = {
        "counts_by_file_classification": dict(file_classification),
        "counts_by_file_status": dict(file_status),
        "counts_by_atom_mapping_status": dict(atom_status),
        "atoms_total": atoms_total,
        "high_risk_atoms_total": high_risk_total,
        "non_exact_atoms_total": non_exact_total,
        "derived_atoms_total": derived_total,
        "broad_derived_atoms_marked_for_atomization": broad_derived_total,
        "adversarial_review_status": dict(review_status),
        "human_review_queue_total": review_queue_total,
    }
    return summary_counts, errors


def write_validation_summary(records: list[dict], counts: dict, errors: list[str]) -> None:
    existing = {}
    if VALIDATION_SUMMARY_PATH.exists():
        existing = json.loads(VALIDATION_SUMMARY_PATH.read_text())

    summary = deepcopy(existing)
    summary.update(
        {
            "record_type": "validation_summary",
            "scope": "full_run",
            "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "total_files_expected_for_full_run": 579,
            "files_processed": len(records),
            "file_indices_processed": [record["file_index"] for record in records],
            "counts_by_file_classification": counts["counts_by_file_classification"],
            "counts_by_file_status": counts["counts_by_file_status"],
            "counts_by_atom_mapping_status": counts["counts_by_atom_mapping_status"],
            "atoms_total": counts["atoms_total"],
            "high_risk_atoms_total": counts["high_risk_atoms_total"],
            "non_exact_atoms_total": counts["non_exact_atoms_total"],
            "derived_atoms_total": counts["derived_atoms_total"],
            "broad_derived_atoms_marked_for_atomization": counts[
                "broad_derived_atoms_marked_for_atomization"
            ],
            "adversarial_review_status": counts["adversarial_review_status"],
            "human_review_queue_total": counts["human_review_queue_total"],
            "validation_checks": {
                "exactly_579_file_artifacts_exist": len(records) == 579,
                "all_expected_file_indices_exist": [record["file_index"] for record in records]
                == list(range(1, 580)),
                "embedded_atom_counts_match_atoms_total": not any(
                    record.get("atoms_total") != len(record.get("atoms") or [])
                    for record in records
                ),
                "mapped_atoms_have_destination_evidence": not any(
                    atom.get("mapping_status") in EQUIVALENCE_REQUIRED
                    and not atom.get("destinations")
                    for record in records
                    for atom in record.get("atoms") or []
                ),
                "non_exact_semantic_mappings_have_equivalence_argument": not any(
                    atom.get("mapping_status") in EQUIVALENCE_REQUIRED
                    and not atom.get("equivalence_argument")
                    for record in records
                    for atom in record.get("atoms") or []
                ),
                "high_risk_review_or_queue_requirement_satisfied": not any(
                    atom.get("high_risk")
                    and atom.get("mapping_status") not in {"exact", "renamed_exact"}
                    and not (
                        atom.get("mapping_status") == "intentionally_absent"
                        and atom.get("intentional_absence_basis")
                        and atom.get("intentional_absence_rationale")
                    )
                    and not atom.get("review_required")
                    and not ensure_adversarial(atom).get("required")
                    for record in records
                    for atom in record.get("atoms") or []
                ),
                "accepted_intentionally_absent_atoms_have_rationale": not any(
                    atom.get("mapping_status") == "intentionally_absent"
                    and not atom.get("review_required")
                    and (
                        not atom.get("intentional_absence_basis")
                        or not atom.get("intentional_absence_rationale")
                    )
                    for record in records
                    for atom in record.get("atoms") or []
                ),
            },
            "validation_errors": errors,
            "notes": "Updated after atom-guideline remediation; weak filename-only equivalence was reclassified as blocked/missing and broad derived claims were marked for atomization.",
        }
    )
    VALIDATION_SUMMARY_PATH.write_text(json.dumps(summary, indent=2, sort_keys=False) + "\n")


def write_report(changes: list[str], counts: dict, errors: list[str]) -> None:
    lines = [
        "# Atom Guideline Remediation Report",
        "",
        "## Summary",
        "",
        "- Reclassified unsupported filename/path-only mappings away from `moved_to_dependency` or `structural_equivalent`.",
        "- Reclassified unapproved `intentionally_absent` atoms to `blocked` pending explicit approval or obsolete-behavior citation.",
        "- Marked broad derived atoms with `needs_atomization` so they are not treated as indivisible code facts until split or merged.",
        "- Regenerated `index.jsonl`, `review-queue.md`, and `validation-summary.json` from canonical file artifacts.",
        "",
        "## Counts After Remediation",
        "",
        f"- Atoms total: {counts['atoms_total']}",
        f"- Mapping statuses: `{counts['counts_by_atom_mapping_status']}`",
        f"- File classifications: `{counts['counts_by_file_classification']}`",
        f"- Human review queue entries: {counts['human_review_queue_total']}",
        f"- Broad derived atoms marked for atomization: {counts['broad_derived_atoms_marked_for_atomization']}",
        "",
        "## Explicit Atom Changes",
        "",
    ]
    for change in changes:
        lines.append(f"- {change}")
    if not changes:
        lines.append("- No explicit atom changes were required.")
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "- Validation errors: " + (", ".join(errors) if errors else "none"),
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    records = load_records()
    changes = remediation_pass(records)
    review_queue_total = write_review_queue(records) if not args.dry_run else 0
    counts, errors = validate(records, review_queue_total)

    if args.dry_run:
        print(json.dumps({"changes": changes, "counts": counts, "errors": errors}, indent=2))
        return

    write_records(records)
    write_index(records)
    write_validation_summary(records, counts, errors)
    write_report(changes, counts, errors)
    print(json.dumps({"changes": len(changes), "counts": counts, "errors": errors}, indent=2))


if __name__ == "__main__":
    main()
