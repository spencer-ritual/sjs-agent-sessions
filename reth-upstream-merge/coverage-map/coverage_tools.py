#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path

TOTAL_FILES = 579
BASE = Path("/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge")
COVERAGE = BASE / "coverage-map"
FILES_DIR = COVERAGE / "files"
REVIEWS_DIR = COVERAGE / "reviews"
QUEUE_PATH = BASE / "ritual-reth-internal-downstream-from-divergence.name-status.txt"

NON_EXACT_WITH_EQUIV = {
    "covered_by_upstream",
    "moved_to_dependency",
    "structural_equivalent",
}
ACTIONABLE = {"missing", "blocked", "intentionally_absent"}
MAPPED_WITH_EVIDENCE = {
    "exact",
    "renamed_exact",
    "covered_by_upstream",
    "moved_to_dependency",
    "structural_equivalent",
}


def load_queue():
    queue = {}
    for idx, line in enumerate(QUEUE_PATH.read_text().splitlines(), 1):
        parts = line.split("\t")
        status = parts[0]
        if status.startswith(("R", "C")):
            old_path, path = parts[1], parts[2]
        else:
            old_path, path = None, parts[1]
        queue[idx] = {
            "source_status": status,
            "source_path": path,
            "source_old_path": old_path,
        }
    return queue


def queue_entry_from_artifact(data):
    return {
        "source_status": data["source_status"],
        "source_path": data["source_path"],
        "source_old_path": data.get("source_old_path"),
    }


def list_existing_indices():
    indices = []
    for path in sorted(FILES_DIR.glob("file-*.json")):
        try:
            indices.append(int(path.stem.split("-")[1]))
        except Exception:
            pass
    return indices


def load_artifact(index):
    path = FILES_DIR / f"file-{index:04d}.json"
    return path, json.loads(path.read_text())


def load_review_queue_text():
    path = COVERAGE / "review-queue.md"
    return path.read_text() if path.exists() else ""


def load_review_map():
    reviews = {}
    if not REVIEWS_DIR.exists():
        return reviews
    for path in sorted(REVIEWS_DIR.glob("review-*.json")):
        data = json.loads(path.read_text())
        reviews[data["atom_record_id"]] = data
    return reviews


def rebuild_index(artifacts):
    lines = []
    for data in artifacts:
        line = {
            "file_index": data["file_index"],
            "artifact": f"coverage-map/files/file-{data['file_index']:04d}.json",
            "source_status": data["source_status"],
            "source_path": data["source_path"],
            "file_classification": data["file_classification"],
            "atoms_total": data["atoms_total"],
            "high_risk_atoms_total": data["high_risk_atoms_total"],
            "non_exact_atoms_total": data["non_exact_atoms_total"],
            "status": data["status"],
            "review_required": data["review_required"],
            "summary": data["summary"],
        }
        lines.append(json.dumps(line, separators=(",", ":")))
    (COVERAGE / "index.jsonl").write_text("\n".join(lines) + ("\n" if lines else ""))


def rebuild_review_queue(artifacts):
    lines = ["# Coverage Review Queue", ""]
    any_entries = False
    for data in sorted(artifacts, key=lambda item: item["file_index"]):
        file_lines = []
        for atom in data.get("atoms", []):
            status = atom.get("mapping_status")
            actionable = status in ACTIONABLE or status == "intentionally_absent"
            if not actionable and not atom.get("review_required"):
                continue
            any_entries = True
            file_lines.extend(
                [
                    f"- Key: `file_index={data['file_index']}`, `source_path={data['source_path']}`, `record_id={atom['record_id']}`",
                    f"  - Source hunk: `{atom['source_hunk_hint']}`",
                    "  - "
                    + (
                        f"Required change: {atom['required_change']}"
                        if atom.get("required_change")
                        else f"Human question: {atom.get('human_question', atom.get('notes', 'Review required.'))}"
                    ),
                    "  - Likely destination: "
                    + (
                        f"`{atom['destinations'][0]['repo']}/{atom['destinations'][0]['path']}`"
                        if atom.get("destinations")
                        else "`unknown`"
                    ),
                    "",
                ]
            )
        if file_lines:
            lines.append(f"## File {data['file_index']:04d}: {data['source_path']}")
            lines.append("")
            lines.extend(file_lines)
    if not any_entries:
        lines.extend(
            [
                "No actionable review entries are currently required.",
                "",
                "Rationale: no atom is currently classified as `missing`, `blocked`, or `intentionally_absent`, and no mapped atom is flagged `review_required` without a separate review file.",
            ]
        )
    (COVERAGE / "review-queue.md").write_text("\n".join(lines).rstrip() + "\n")


def validate():
    queue = load_queue()
    review_queue_text = ""
    review_map = load_review_map()
    errors = []
    artifacts = []
    counts_by_classification = Counter()
    counts_by_status = Counter()
    counts_by_atom_status = Counter()
    adversarial = Counter()
    file_indices_processed = []
    existing_files = sorted(FILES_DIR.glob("file-*.json"))
    if len(existing_files) != TOTAL_FILES:
        errors.append(
            f"expected {TOTAL_FILES} file artifacts, found {len(existing_files)}"
        )

    for idx in range(1, TOTAL_FILES + 1):
        path = FILES_DIR / f"file-{idx:04d}.json"
        if not path.exists():
            errors.append(f"missing artifact {path.name}")
            continue
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            errors.append(f"{path.name} does not parse: {exc}")
            continue
        artifacts.append(data)
        file_indices_processed.append(idx)

        if data.get("file_index") != idx:
            errors.append(f"{path.name} file_index mismatch")
        if data.get("total_files") != TOTAL_FILES:
            errors.append(f"{path.name} total_files mismatch")
        if idx not in queue:
            errors.append(f"{path.name} has no queue entry")
        elif queue_entry_from_artifact(data) != queue[idx]:
            errors.append(f"{path.name} queue metadata mismatch")

        atoms = data.get("atoms", [])
        atoms_total = data.get("atoms_total")
        if data.get("file_classification") != "noise" and atoms_total <= 0:
            errors.append(f"{path.name} non-noise artifact has atoms_total <= 0")
        if len(atoms) != atoms_total:
            errors.append(f"{path.name} embedded atom count != atoms_total")

        counts_by_classification[data["file_classification"]] += 1
        counts_by_status[data["status"]] += 1

        for atom in atoms:
            status = atom["mapping_status"]
            counts_by_atom_status[status] += 1
            if status in MAPPED_WITH_EVIDENCE and not atom.get("destinations"):
                errors.append(f"{atom['record_id']} missing destination evidence")
            if status in NON_EXACT_WITH_EQUIV and not atom.get("equivalence_argument"):
                errors.append(f"{atom['record_id']} missing equivalence argument")
            if atom.get("high_risk"):
                if not atom.get("test_strategy"):
                    errors.append(f"{atom['record_id']} missing test_strategy")
                if atom.get("test_strategy") != "not_testable" and atom.get("negative_test_candidate") in (None, ""):
                    errors.append(
                        f"{atom['record_id']} missing negative_test_candidate"
                    )
                if status not in {"exact", "renamed_exact"}:
                    in_queue = atom["record_id"] in review_queue_text
                    in_review = atom["record_id"] in review_map
                    if not (in_queue or in_review):
                        errors.append(
                            f"{atom['record_id']} high-risk non-exact atom lacks review file or queue entry"
                        )
            if status in ACTIONABLE and atom["record_id"] not in review_queue_text:
                errors.append(f"{atom['record_id']} actionable atom missing from review queue")

            review = atom.get("adversarial_review", {})
            if review:
                adversarial[review.get("status", "not_requested")] += 1
                if review.get("required"):
                    adversarial["required"] += 1

    artifacts = sorted(artifacts, key=lambda item: item["file_index"])
    rebuild_index(artifacts)
    rebuild_review_queue(artifacts)
    review_queue_text = load_review_queue_text()
    human_review_queue_total = review_queue_text.count("- Key:")

    # Re-check queue-dependent validation after regenerating review-queue.md.
    errors = [
        err
        for err in errors
        if "actionable atom missing from review queue" not in err
        and "high-risk non-exact atom lacks review file or queue entry" not in err
    ]
    for data in artifacts:
        for atom in data.get("atoms", []):
            status = atom["mapping_status"]
            if atom.get("high_risk") and status not in {"exact", "renamed_exact"}:
                in_queue = atom["record_id"] in review_queue_text
                in_review = atom["record_id"] in review_map
                if not (in_queue or in_review):
                    errors.append(
                        f"{atom['record_id']} high-risk non-exact atom lacks review file or queue entry"
                    )
            if status in ACTIONABLE or status == "intentionally_absent":
                if atom["record_id"] not in review_queue_text:
                    errors.append(f"{atom['record_id']} actionable atom missing from review queue")

    summary = {
        "record_type": "validation_summary",
        "scope": "full_run" if len(artifacts) == TOTAL_FILES and not errors else "session_partial",
        "total_files_expected_for_full_run": TOTAL_FILES,
        "files_processed": len(artifacts),
        "file_indices_processed": file_indices_processed,
        "artifacts": {
            "files": [
                f"coverage-map/files/file-{idx:04d}.json" for idx in file_indices_processed
            ],
            "index": "coverage-map/index.jsonl",
            "progress": "coverage-map/progress.md",
            "review_queue": "coverage-map/review-queue.md",
            "reviews": sorted(
                f"coverage-map/reviews/{path.name}"
                for path in REVIEWS_DIR.glob("review-*.json")
            )
            if REVIEWS_DIR.exists()
            else [],
        },
        "counts_by_file_classification": dict(counts_by_classification),
        "counts_by_file_status": dict(counts_by_status),
        "counts_by_atom_mapping_status": dict(counts_by_atom_status),
        "atoms_total": sum(data["atoms_total"] for data in artifacts),
        "high_risk_atoms_total": sum(data["high_risk_atoms_total"] for data in artifacts),
        "non_exact_atoms_total": sum(data["non_exact_atoms_total"] for data in artifacts),
        "adversarial_review_status": dict(adversarial),
        "human_review_queue_total": human_review_queue_total,
        "validation_checks": {
            "exactly_579_file_artifacts_exist": len(existing_files) == TOTAL_FILES,
            "all_expected_file_indices_exist": len(file_indices_processed) == TOTAL_FILES,
            "matching_file_index_total_files_status_and_path": not any(
                "queue metadata mismatch" in err or "file_index mismatch" in err or "total_files mismatch" in err
                for err in errors
            ),
            "non_noise_files_have_atoms_total_greater_than_zero": not any(
                "atoms_total <= 0" in err for err in errors
            ),
            "embedded_atom_counts_match_atoms_total": not any(
                "embedded atom count" in err for err in errors
            ),
            "mapped_atoms_have_destination_evidence": not any(
                "destination evidence" in err for err in errors
            ),
            "non_exact_semantic_mappings_have_equivalence_argument": not any(
                "equivalence argument" in err for err in errors
            ),
            "missing_blocked_intentionally_absent_atoms_queued": not any(
                "actionable atom missing from review queue" in err for err in errors
            ),
            "high_risk_review_or_queue_requirement_satisfied": not any(
                "high-risk non-exact atom lacks review file or queue entry" in err
                for err in errors
            ),
        },
        "validation_errors": errors,
        "notes": "Generated by coverage_tools.py validate.",
    }
    (COVERAGE / "validation-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def print_status():
    queue = load_queue()
    existing = set(list_existing_indices())
    remaining = [
        {
            "file_index": idx,
            "source_status": queue[idx]["source_status"],
            "source_path": queue[idx]["source_path"],
        }
        for idx in range(1, TOTAL_FILES + 1)
        if idx not in existing
    ]
    print(json.dumps({"processed": len(existing), "remaining": remaining}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("validate")
    sub.add_parser("rebuild-review-queue")
    args = parser.parse_args()

    if args.cmd == "status":
        print_status()
    elif args.cmd == "rebuild-review-queue":
        artifacts = []
        for idx in range(1, TOTAL_FILES + 1):
            path = FILES_DIR / f"file-{idx:04d}.json"
            if path.exists():
                artifacts.append(json.loads(path.read_text()))
        rebuild_review_queue(sorted(artifacts, key=lambda item: item["file_index"]))
    else:
        summary = validate()
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
