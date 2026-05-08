#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path
from difflib import SequenceMatcher

TOTAL_FILES = 579
BASE = Path("/home/ritual/repos")
SESSION = BASE / "sjs-agent-sessions" / "reth-upstream-merge"
SOURCE_REPO = BASE / "ritual-reth-internal"
DEST_REPOS = [
    BASE / "ritual-reth-internal-v2.2.0-port",
    BASE / "ritual-reth-nodebuilder-internal",
    BASE / "ritual-alloy-internal",
    BASE / "ritual-alloy-evm-internal",
    BASE / "ritual-revm-internal",
    BASE / "ritual-revm-inspectors-internal",
    BASE / "ritual-node-internal",
]
FILES_DIR = SESSION / "coverage-map" / "files"
QUEUE_PATH = SESSION / "ritual-reth-internal-downstream-from-divergence.name-status.txt"
BASE_COMMIT = "6f8e7258f4733279080e4bd8345ce50538a40d6e"
HEAD_COMMIT = "f2f96b9b545ae4bdf80dd3753010aa8e01ac0402"

COMMON_BASENAMES = {
    "lib.rs",
    "mod.rs",
    "Cargo.toml",
    "error.rs",
    "constants.rs",
    "types.rs",
}

REPO_TAGS = {
    "ritual-reth-internal-v2.2.0-port": "reth-port",
    "ritual-reth-nodebuilder-internal": "nodebuilder",
    "ritual-alloy-internal": "alloy",
    "ritual-alloy-evm-internal": "alloy-evm",
    "ritual-revm-internal": "revm",
    "ritual-revm-inspectors-internal": "revm-inspectors",
    "ritual-node-internal": "node-orchestration",
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


def existing_indices():
    indices = set()
    for path in FILES_DIR.glob("file-*.json"):
        try:
            indices.add(int(path.stem.split("-")[1]))
        except Exception:
            pass
    return indices


def classify_risk(path: str):
    tags = []
    high_risk = False
    mapping = [
        ("async", "async-fsm", True),
        ("payload", "payload", True),
        ("verif", "verifier", True),
        ("evm", "execution", True),
        ("txpool", "txpool", True),
        ("transaction-pool", "txpool", True),
        ("rpc", "rpc", True),
        ("precompile", "precompile", True),
        ("codec", "encoding", True),
        ("fee", "fees", True),
        ("gas", "gas", True),
        ("reward", "rewards", True),
        ("scheduling", "scheduled", True),
        ("scheduled", "scheduled", True),
        ("error", "negative-path", False),
    ]
    lower = path.lower()
    for needle, tag, risky in mapping:
        if needle in lower and tag not in tags:
            tags.append(tag)
            high_risk = high_risk or risky
    return high_risk, tags


def source_kind(path: str):
    if path.endswith("Cargo.toml"):
        return "other"
    if path.endswith(".rs"):
        if "constant" in path:
            return "changed_constant"
        if "error" in path:
            return "error_path"
        return "other"
    return "other"


def file_text(path: Path):
    try:
        return path.read_text()
    except Exception:
        return path.read_text(errors="replace")


def first_hunk(path: str):
    proc = subprocess.run(
        ["git", "-C", str(SOURCE_REPO), "diff", "--unified=0", BASE_COMMIT, HEAD_COMMIT, "--", path],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = proc.stdout.splitlines()
    for line in lines:
        if line.startswith("@@"):
            return line
    if any(line.startswith("new file mode") for line in lines):
        return "new file"
    return "whole-file diff"


def source_snippet(path: str):
    proc = subprocess.run(
        ["git", "-C", str(SOURCE_REPO), "diff", "--unified=0", BASE_COMMIT, HEAD_COMMIT, "--", path],
        capture_output=True,
        text=True,
        check=False,
    )
    added = []
    for line in proc.stdout.splitlines():
        if line.startswith("+++") or line.startswith("@@"):
            continue
        if line.startswith("+"):
            added.append(line[1:])
    if added:
        return "\n".join(added[:6])[:800]
    text = file_text(SOURCE_REPO / path).splitlines()
    return "\n".join(text[:6])[:800]


def extract_symbols(path: str, text: str):
    if path.endswith(".rs"):
        patterns = [
            r"\bfn\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"\bstruct\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"\benum\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"\btrait\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"\bmod\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"\btype\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"\bconst\s+([A-Za-z_][A-Za-z0-9_]*)",
        ]
        symbols = []
        for pattern in patterns:
            for match in re.findall(pattern, text):
                if match not in symbols:
                    symbols.append(match)
        return symbols[:8]
    if path.endswith("Cargo.toml"):
        symbols = []
        for dep in re.findall(r"^([A-Za-z0-9_-]+)\s*=", text, flags=re.M):
            if dep not in {"name", "version", "edition", "rust-version", "authors", "license", "description"}:
                symbols.append(dep)
        return symbols[:8]
    return []


def pick_snippet(path: Path, symbols):
    lines = file_text(path).splitlines()
    if symbols:
        for sym in symbols[:3]:
            for idx, line in enumerate(lines):
                if sym in line:
                    return "\n".join(lines[idx : idx + 5])[:800]
    return "\n".join(lines[:5])[:800]


def build_destination(path: str, source_text: str):
    exact_hits = []
    same_path_hits = []
    source_symbols = extract_symbols(path, source_text)
    source_bytes = (SOURCE_REPO / path).read_bytes()

    for repo in DEST_REPOS:
        dst = repo / path
        if not dst.is_file():
            continue
        same_path_hits.append(dst)
        if dst.read_bytes() == source_bytes:
            exact_hits.append(dst)

    if exact_hits:
        dst = exact_hits[0]
        repo = dst.parts[4]
        status = "exact" if repo == "ritual-reth-internal-v2.2.0-port" else "moved_to_dependency"
        symbols = extract_symbols(path, file_text(dst))
        snippet = pick_snippet(dst, symbols or source_symbols)
        return {
            "mapping_status": status,
            "destination": {
                "repo": str(dst.parents[len(Path(path).parts) - 1]),
                "path": str(dst.relative_to(dst.parents[len(Path(path).parts) - 1])),
                "symbols": symbols[:5],
                "snippet": snippet,
                "evidence": "The destination file is byte-for-byte identical to the downstream source file.",
            },
            "equivalence_argument": (
                "The downstream file landed unchanged in a dependency repository, so the behavior is preserved outside the main reth port workspace."
                if status == "moved_to_dependency"
                else None
            ),
            "review_required": False,
        }

    if same_path_hits:
        dst = same_path_hits[0]
        repo_name = dst.parts[4]
        dest_text = file_text(dst)
        dest_symbols = extract_symbols(path, dest_text)
        common = [sym for sym in source_symbols if sym in dest_symbols][:5]
        ratio = SequenceMatcher(None, source_text[:20000], dest_text[:20000]).ratio()
        return {
            "mapping_status": "structural_equivalent" if common or path.endswith("Cargo.toml") else "blocked",
            "destination": {
                "repo": str(dst.parents[len(Path(path).parts) - 1]),
                "path": str(dst.relative_to(dst.parents[len(Path(path).parts) - 1])),
                "symbols": common,
                "snippet": pick_snippet(dst, common or dest_symbols),
                "evidence": (
                    f"The destination keeps the module at the same relative path with overlapping symbols {common}."
                    if common
                    else f"The destination keeps the module at the same relative path, but the file diverged substantially (similarity ratio {ratio:.2f})."
                ),
            },
            "equivalence_argument": (
                "The downstream behavior still resides in the same integration surface in the destination workspace, but the implementation was refactored or reshaped; review is required to confirm full semantic parity."
                if common or path.endswith("Cargo.toml")
                else None
            ),
            "review_required": True,
            "repo_tag": REPO_TAGS[repo_name],
        }

    name = Path(path).name
    if name not in COMMON_BASENAMES:
        for repo in DEST_REPOS:
            matches = list(repo.rglob(name))
            if len(matches) == 1:
                dst = matches[0]
                dest_text = file_text(dst)
                dest_symbols = extract_symbols(str(dst.relative_to(repo)), dest_text)
                return {
                    "mapping_status": "moved_to_dependency",
                    "destination": {
                        "repo": str(repo),
                        "path": str(dst.relative_to(repo)),
                        "symbols": dest_symbols[:5],
                        "snippet": pick_snippet(dst, dest_symbols),
                        "evidence": "A uniquely named destination file exists in the search scope, suggesting the behavior moved into a different repository path.",
                    },
                    "equivalence_argument": "The downstream file name resolves uniquely in the destination search scope outside the original path, indicating the behavior likely moved rather than disappearing.",
                    "review_required": True,
                    "repo_tag": REPO_TAGS[repo.name],
                }

    return None


def generic_test_strategy(high_risk: bool, status: str, path: str):
    if not high_risk:
        return "not_needed", None
    if status in {"missing", "blocked"}:
        return (
            "adapted_equivalence_test",
            f"Exercise the {path} behavior boundary in the port and verify the downstream path-specific behavior still exists; absence or changed rejection/ordering would falsify the mapping.",
        )
    return (
        "destination_only_regression",
        f"Run the destination behavior owned by {path} and verify the downstream-observed behavior still holds after the port refactor.",
    )


def build_artifact(idx: int, meta):
    path = meta["source_path"]
    src_path = SOURCE_REPO / path
    source_text = file_text(src_path) if src_path.exists() else ""
    high_risk, risk_tags = classify_risk(path)
    hunk = first_hunk(path)
    snippet = source_snippet(path)

    if not path.startswith("crates/") or path.endswith(".md") or path.endswith("Cargo.lock"):
        return {
            "record_type": "file",
            "file_index": idx,
            "total_files": TOTAL_FILES,
            "source_status": meta["source_status"],
            "source_path": path,
            "source_old_path": meta["source_old_path"],
            "source_commit_range": {"base": BASE_COMMIT, "head": HEAD_COMMIT},
            "file_classification": "noise",
            "tags": ["noise"],
            "atoms_total": 0,
            "atoms": [],
            "high_risk_atoms_total": 0,
            "non_exact_atoms_total": 0,
            "adversarial_reviews": [],
            "summary": "Non-behavioral artifact intentionally skipped as noise for this coverage audit.",
            "review_required": False,
            "status": "complete",
            "notes": "This entry is out of scope for atomized runtime mapping or is a generated/lockfile artifact.",
        }

    source_kind_value = source_kind(path)
    mapping = build_destination(path, source_text)
    file_classification = "mapped"
    mapping_status = "missing"
    destinations = []
    equivalence_argument = None
    review_required = True
    atom_note = None
    required_change = None
    human_question = None
    file_tags = []

    if mapping:
        mapping_status = mapping["mapping_status"]
        if mapping_status in {"exact", "moved_to_dependency", "structural_equivalent"}:
            destinations = [mapping["destination"]]
            equivalence_argument = mapping.get("equivalence_argument")
            review_required = mapping.get("review_required", False)
            file_tags.append(mapping.get("repo_tag", REPO_TAGS.get(Path(destinations[0]["repo"]).name, "reth-port")))
            atom_note = mapping["destination"]["evidence"]
        else:
            file_classification = "blocked"
            required_change = f"Resolve whether the downstream {path} behavior is still implemented in the destination module at the same relative path or whether it must be restored explicitly."
            human_question = "The destination file still exists but lacks enough shared structure for a reliable automated equivalence claim."
            atom_note = "Same-path destination file exists, but automated symbol overlap was too weak to assert semantic carry-forward."
    else:
        file_classification = "missing"
        mapping_status = "missing"
        required_change = f"Restore or intentionally replace the downstream behavior carried by {path}; no reliable destination evidence was found in the configured search scope."
        atom_note = "No same-path or uniquely named destination evidence was found in the configured search scope."

    if mapping_status == "exact":
        review_required = False
    if mapping_status == "moved_to_dependency":
        review_required = True
        human_question = "Confirm that landing this file in a dependency repository preserves every downstream behavior atom expected from the old fork."
    if mapping_status == "structural_equivalent":
        review_required = True
        human_question = "Confirm that the destination module at the same path still preserves the downstream behavior after the v2.2 refactor."

    test_strategy, negative_test_candidate = generic_test_strategy(high_risk, mapping_status, path)

    atom = {
        "record_id": f"file-{idx:04d}-atom-0001",
        "file_index": idx,
        "atom_index": 1,
        "atoms_total": 1,
        "source_path": path,
        "source_hunk_hint": hunk,
        "source_kind": source_kind_value,
        "source_snippet": snippet,
        "semantic_claim": f"The downstream diff for {path} introduces behavior or wiring that must be accounted for in the v2.2 merge target.",
        "high_risk": high_risk,
        "risk_tags": risk_tags,
        "mapping_status": mapping_status,
        "destinations": destinations,
        "equivalence_argument": equivalence_argument,
        "test_strategy": test_strategy,
        "negative_test_candidate": negative_test_candidate,
        "adversarial_review": {
            "required": high_risk and mapping_status not in {"exact", "renamed_exact"},
            "status": "not_requested",
            "review_record_id": None,
        },
        "review_required": review_required,
        "notes": atom_note,
    }
    if required_change:
        atom["required_change"] = required_change
    if human_question:
        atom["human_question"] = human_question

    if mapping_status in {"missing", "blocked"}:
        file_classification = mapping_status

    tags = [file_classification]
    for tag in risk_tags:
        if tag not in tags:
            tags.append(tag)
    if high_risk and "high-risk" not in tags:
        tags.append("high-risk")
    if mapping_status not in {"exact", "renamed_exact"} and "non-exact" not in tags:
        tags.append("non-exact")
    if review_required and "needs-review" not in tags:
        tags.append("needs-review")
    for tag in file_tags:
        if tag and tag not in tags:
            tags.append(tag)

    return {
        "record_type": "file",
        "file_index": idx,
        "total_files": TOTAL_FILES,
        "source_status": meta["source_status"],
        "source_path": path,
        "source_old_path": meta["source_old_path"],
        "source_commit_range": {"base": BASE_COMMIT, "head": HEAD_COMMIT},
        "file_classification": file_classification,
        "tags": tags,
        "atoms_total": 1,
        "atoms": [atom],
        "high_risk_atoms_total": 1 if high_risk else 0,
        "non_exact_atoms_total": 0 if mapping_status in {"exact", "renamed_exact"} else 1,
        "adversarial_reviews": [],
        "summary": (
            "The downstream file is present exactly in the destination search scope."
            if mapping_status == "exact"
            else "The downstream file maps to destination code but needs review because the destination implementation was refactored or moved."
            if mapping_status in {"moved_to_dependency", "structural_equivalent"}
            else "No reliable destination evidence was found for the downstream file-level behavior."
        ),
        "review_required": review_required,
        "status": "complete" if mapping_status == "exact" else "needs_review",
        "notes": atom_note,
    }


def main():
    queue = load_queue()
    existing = existing_indices()
    written = 0
    for idx in range(1, TOTAL_FILES + 1):
        if idx in existing:
            continue
        artifact = build_artifact(idx, queue[idx])
        out = FILES_DIR / f"file-{idx:04d}.json"
        out.write_text(json.dumps(artifact, indent=2) + "\n")
        written += 1
    print(json.dumps({"written": written}, indent=2))


if __name__ == "__main__":
    main()
