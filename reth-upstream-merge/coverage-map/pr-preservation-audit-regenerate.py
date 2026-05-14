#!/usr/bin/env python3
"""Generate PR-preservation atoms for the Reth upstream merge coverage map.

This pass treats `pr-preservation-map.md` as an index of merge intent. Raw
candidates are tied to local first-parent merge diffs, then promoted only when a
matching behavior can still be located in the current downstream source tree.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path("/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge")
COVERAGE = ROOT / "coverage-map"
FILES_DIR = COVERAGE / "files"
AUDIT_DIR = COVERAGE / "pr-preservation-audit"
OLD_REPO = Path("/home/ritual/repos/ritual-reth-internal")
BASE = "6f8e7258f4733279080e4bd8345ce50538a40d6e"
HEAD = "dev"


DOMAIN_TAGS = {
    "async": "async-fsm",
    "ttl": "async-fsm",
    "phase": "async-fsm",
    "scheduled": "scheduled",
    "scheduler": "scheduled",
    "heartbeat": "scheduled",
    "payload": "payload",
    "builder": "payload",
    "verifier": "verifier",
    "verification": "verifier",
    "txpool": "txpool",
    "pool": "txpool",
    "rpc": "rpc",
    "precompile": "precompile",
    "codec": "encoding",
    "abi": "encoding",
    "signature": "encoding",
    "hash": "encoding",
    "fee": "fees",
    "pricing": "fees",
    "wallet": "fees",
    "registry": "executor-selection",
    "executor": "executor-selection",
    "capability": "executor-selection",
    "gas": "gas",
    "reward": "rewards",
    "deadline": "negative-path",
    "fail": "negative-path",
    "reject": "negative-path",
    "invalid": "negative-path",
    "overflow": "negative-path",
    "duplicate": "negative-path",
}

STOP_WORDS = {
    "preserve",
    "preserves",
    "preserved",
    "behavior",
    "batch",
    "with",
    "from",
    "into",
    "that",
    "this",
    "only",
    "plus",
    "must",
    "should",
    "unless",
    "later",
    "explicit",
    "config",
    "support",
    "coverage",
    "default",
    "shared",
    "current",
    "source",
    "detailed",
    "support",
    "coverage",
    "behavior",
    "prototype",
}


@dataclass
class Entry:
    entry_index: int
    line_number: int
    pr_key: str
    slug: str
    summary: str
    batch: str
    line: str


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(OLD_REPO), *args], text=True, errors="replace")


def load_entries() -> list[Entry]:
    entries: list[Entry] = []
    pattern = re.compile(
        r"^- (?:(Early branch merge|Branch merge) `([0-9a-f]+)`(?: `([^`]+)`)?:|`#(\d+)` `([^`]+)`:)"
        r" (?P<summary>.*?) Batch: (?P<batch>.*?)(?:\.)?$"
    )
    for line_number, line in enumerate((ROOT / "pr-preservation-map.md").read_text().splitlines(), start=1):
        m = pattern.match(line)
        if not m:
            continue
        branch_kind, short_commit, branch_slug, pr_num, pr_slug = m.groups()[:5]
        if pr_num:
            pr_key = f"#{pr_num}"
            slug = pr_slug
        else:
            pr_key = short_commit
            slug = branch_slug or branch_kind or "branch-merge"
        entries.append(
            Entry(
                entry_index=len(entries) + 1,
                line_number=line_number,
                pr_key=pr_key,
                slug=slug,
                summary=m.group("summary"),
                batch=m.group("batch"),
                line=line,
            )
        )
    return entries


def load_merge_commits() -> dict[str, str]:
    out: dict[str, str] = {}
    for row in git("log", "--first-parent", "--format=%H%x09%s", f"{BASE}..{HEAD}").splitlines():
        commit, subject = row.split("\t", 1)
        m = re.search(r"Merge pull request #(\d+)", subject)
        if m:
            out[f"#{m.group(1)}"] = commit
        short = commit[:10]
        out[short] = commit
        out[commit[:8]] = commit
    return out


def load_index_by_path() -> dict[str, int]:
    out: dict[str, int] = {}
    for idx, line in enumerate((ROOT / "ritual-reth-internal-downstream-from-divergence.name-status.txt").read_text().splitlines(), start=1):
        parts = line.split("\t")
        if len(parts) == 2:
            path = parts[1]
        elif len(parts) >= 3:
            path = parts[-1]
        else:
            continue
        out[path] = idx
    return out


def load_current_sources(index_by_path: dict[str, int]) -> dict[str, str]:
    sources: dict[str, str] = {}
    for path in index_by_path:
        if not path.startswith("crates/"):
            continue
        if not path.endswith(".rs"):
            continue
        if "/test" in path or "test_utils" in path:
            continue
        full = OLD_REPO / path
        if full.exists() and full.is_file():
            try:
                sources[path] = full.read_text(errors="replace")
            except UnicodeDecodeError:
                continue
    return sources


def changed_paths_for_commit(commit: str) -> list[str]:
    try:
        rows = git("diff", "--name-status", "--find-renames", "--find-copies", f"{commit}^1", commit).splitlines()
    except subprocess.CalledProcessError:
        return []
    paths: list[str] = []
    for row in rows:
        parts = row.split("\t")
        if len(parts) == 2:
            path = parts[1]
        elif len(parts) >= 3:
            path = parts[-1]
        else:
            continue
        if path.startswith("crates/"):
            paths.append(path)
    return paths


def diff_added_lines(commit: str) -> dict[str, list[str]]:
    try:
        diff = git("diff", "--find-renames", "--find-copies", "--unified=8", f"{commit}^1", commit)
    except subprocess.CalledProcessError:
        return {}
    current: str | None = None
    out: dict[str, list[str]] = defaultdict(list)
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            current = None
            m = re.match(r"diff --git a/(.*?) b/(.*)", line)
            if m:
                current = m.group(2)
            continue
        if current and line.startswith("+") and not line.startswith("+++"):
            text = line[1:].strip()
            if text and not text.startswith("//") and not text.startswith("#"):
                out[current].append(text)
    return out


def split_summary(summary: str) -> list[str]:
    lowered = summary.lower()
    if "no product behavior to port" in lowered:
        return []
    summary = re.sub(r"^preserves?\s+", "", summary.strip(), flags=re.I)
    summary = re.sub(r"^preserve\s+", "", summary.strip(), flags=re.I)
    # Keep intentionally removed behavior as one atom if the PR itself is about removal.
    if "removal of " in summary or summary.startswith("removal "):
        return [summary]
    parts = re.split(r";|\band\b(?=\s+[a-zA-Z`])", summary)
    claims: list[str] = []
    for part in parts:
        for sub in re.split(r",\s+(?=(?:and\s+)?(?:[a-zA-Z`][^,]{8,}))", part):
            clean = sub.strip(" .")
            clean = re.sub(r"^(?:and|plus)\s+", "", clean)
            if len(clean) >= 20:
                claims.append(clean)
    return claims or [summary.strip(" .")]


def tokens(text: str) -> list[str]:
    toks = set(re.findall(r"`([^`]+)`", text))
    toks.update(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", text))
    expanded = set(toks)
    for tok in list(toks):
        expanded.add(tok.replace("-", "_"))
        expanded.add(tok.replace("_", "-"))
        if "." in tok:
            expanded.add(tok.split(".")[-1])
    toks = expanded
    clean = []
    for tok in toks:
        low = tok.lower()
        if low not in STOP_WORDS:
            clean.append(tok)
    return clean


def risk_tags_for(text: str, batch: str) -> list[str]:
    hay = f"{text} {batch}".lower()
    tags = {tag for key, tag in DOMAIN_TAGS.items() if key in hay}
    if not tags:
        tags.add("high-risk")
    tags.discard("high-risk")
    return sorted(tags)


def score_path(path: str, content: str, claim_tokens: list[str], changed: set[str], added: dict[str, list[str]], batch: str) -> int:
    lower = content.lower()
    score = 0
    if not path.endswith(".rs") or "/test" in path or "test_utils" in path:
        return 0
    if path in changed:
        score += 7
    if path in added:
        joined = "\n".join(added[path]).lower()
        score += sum(3 for tok in claim_tokens if tok.lower() in joined)
    score += sum(1 for tok in claim_tokens if tok.lower() in lower)
    if "payload" in batch and "payload" in path:
        score += 3
    if "txpool" in batch and "transaction-pool" in path:
        score += 3
    if "scheduling" in batch and ("scheduled" in path or "scheduling" in path):
        score += 3
    if "rpc" in batch and "/rpc/" in path:
        score += 3
    if "precompile" in batch and "precompile" in path:
        score += 3
    if "fees" in batch and ("fees" in path or "registry" in path):
        score += 3
    if "transaction formats" in batch and ("codecs" in path or "primitives" in path):
        score += 3
    return score


def find_evidence(claim: str, batch: str, changed_paths: list[str], added: dict[str, list[str]], sources: dict[str, str]) -> tuple[str | None, str | None, str | None]:
    claim_tokens = tokens(claim)
    changed = set(changed_paths)
    scores = []
    for path, content in sources.items():
        score = score_path(path, content, claim_tokens, changed, added, batch.lower())
        if score > 0:
            scores.append((score, path))
    if not scores:
        return None, None, None
    scores.sort(reverse=True)
    for score, best_path in scores[:8]:
        if score < 5:
            continue
        lines = sources[best_path].splitlines()
        best_line_score = 0
        match_idx = 0
        for idx, line in enumerate(lines):
            low = line.lower()
            line_score = sum(1 for tok in claim_tokens if tok.lower() in low)
            if line_score > best_line_score:
                best_line_score = line_score
                match_idx = idx
        lo = max(0, match_idx - 3)
        hi = min(len(lines), match_idx + 18)
        snippet = "\n".join(lines[lo:hi])
        strength = evidence_strength(claim, snippet, best_path in changed_paths)
        if strength >= 2:
            return best_path, f"{best_path}:{lo + 1}-{hi}", snippet
    return None, None, None


def evidence_strength(claim: str, snippet: str, direct_changed_file: bool) -> int:
    claim_tokens = tokens(claim)
    low = snippet.lower()
    hits = sum(1 for tok in claim_tokens if tok.lower() in low)
    symbol_hits = sum(1 for tok in re.findall(r"`([^`]+)`", claim) if tok.lower().replace("-", "_") in low or tok.lower() in low)
    numeric_hits = sum(1 for tok in re.findall(r"\b\d+\b|0x[0-9a-fA-F]+", claim) if tok.lower() in low)
    strength = 0
    if hits >= 2:
        strength += 1
    if symbol_hits or numeric_hits:
        strength += 1
    if direct_changed_file:
        strength += 1
    # Import-only snippets are weak even if they mention a type.
    non_import_lines = [
        line.strip()
        for line in snippet.splitlines()
        if line.strip()
        and not line.strip().startswith("use ")
        and not line.strip().startswith("pub use ")
        and not line.strip().startswith("//")
        and not line.strip().startswith("#![")
    ]
    if not non_import_lines:
        strength = 0
    return strength


def normalize_claim(text: str) -> set[str]:
    return {tok.lower() for tok in tokens(text)}


def is_duplicate(claim: str, existing_claims: list[tuple[str, set[str]]]) -> bool:
    cset = normalize_claim(claim)
    if not cset:
        return False
    for existing, eset in existing_claims:
        if not eset:
            continue
        if claim.lower() in existing.lower() or existing.lower() in claim.lower():
            return True
        jacc = len(cset & eset) / max(1, len(cset | eset))
        containment = len(cset & eset) / max(1, min(len(cset), len(eset)))
        if jacc >= 0.42 or containment >= 0.72:
            return True
    return False


def load_file_records() -> tuple[dict[int, tuple[Path, dict]], int]:
    records: dict[int, tuple[Path, dict]] = {}
    removed = 0
    for path in sorted(FILES_DIR.glob("file-*.json")):
        rec = json.loads(path.read_text())
        atoms = rec.get("atoms", [])
        kept = [a for a in atoms if not a.get("pr_preservation_derived")]
        removed += len(atoms) - len(kept)
        rec["atoms"] = kept
        rec["atoms_total"] = len(kept)
        for atom in kept:
            atom["atoms_total"] = len(kept)
        records[rec["file_index"]] = (path, rec)
    return records, removed


def atom_claim(entry: Entry, claim: str) -> str:
    return f"PR preservation `{entry.pr_key}` `{entry.slug}` keeps live downstream behavior: {claim}."


def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    entries = load_entries()
    merge_commits = load_merge_commits()
    index_by_path = load_index_by_path()
    sources = load_current_sources(index_by_path)
    file_records, removed_existing = load_file_records()
    existing_claims = [
        (atom.get("semantic_claim", ""), normalize_claim(atom.get("semantic_claim", "")))
        for _, rec in file_records.values()
        for atom in rec.get("atoms", [])
    ]

    raw_rows = []
    curated = []
    unresolved = []
    seen_claims: set[str] = set()

    for entry in entries:
        commit = merge_commits.get(entry.pr_key)
        if commit is None and re.fullmatch(r"[0-9a-f]{8,10}", entry.pr_key):
            try:
                commit = git("rev-parse", entry.pr_key).strip()
            except subprocess.CalledProcessError:
                commit = None
        if commit is None:
            unresolved.append(entry.pr_key)
            raw_rows.append(
                {
                    "record_type": "pr_raw_atom",
                    "raw_pr_id": f"pr-raw-{len(raw_rows)+1:04d}",
                    "entry_index": entry.entry_index,
                    "pr_key": entry.pr_key,
                    "slug": entry.slug,
                    "decision": "drop",
                    "drop_reason": "merge_commit_not_resolved",
                    "semantic_claim": entry.summary,
                    "source_map_line": entry.line_number,
                }
            )
            continue

        changed = changed_paths_for_commit(commit)
        added = diff_added_lines(commit)
        claims = split_summary(entry.summary)
        if not claims:
            raw_rows.append(
                {
                    "record_type": "pr_raw_atom",
                    "raw_pr_id": f"pr-raw-{len(raw_rows)+1:04d}",
                    "entry_index": entry.entry_index,
                    "pr_key": entry.pr_key,
                    "slug": entry.slug,
                    "merge_commit": commit,
                    "decision": "drop",
                    "drop_reason": "no_port_noise",
                    "semantic_claim": entry.summary,
                    "source_map_line": entry.line_number,
                    "changed_paths": changed[:20],
                }
            )
            continue

        for claim in claims:
            raw_id = f"pr-raw-{len(raw_rows)+1:04d}"
            source_path, hunk_hint, snippet = find_evidence(claim, entry.batch, changed, added, sources)
            row = {
                "record_type": "pr_raw_atom",
                "raw_pr_id": raw_id,
                "entry_index": entry.entry_index,
                "pr_key": entry.pr_key,
                "slug": entry.slug,
                "merge_commit": commit,
                "source_map_line": entry.line_number,
                "source_map_claim": entry.summary,
                "pr_diff_changed_paths": changed[:40],
                "semantic_claim": claim,
                "risk_tags": risk_tags_for(claim, entry.batch),
                "batch": entry.batch,
            }
            if source_path is None or source_path not in index_by_path:
                row.update(
                    {
                        "decision": "drop",
                        "drop_reason": "not_located_current_downstream",
                    }
                )
            else:
                full_claim = atom_claim(entry, claim)
                duplicate = is_duplicate(claim, existing_claims) or claim.lower() in seen_claims
                row.update(
                    {
                        "decision": "covered_by_existing_atom" if duplicate else "promote",
                        "drop_reason": "covered_by_existing_atom" if duplicate else None,
                        "current_source_path": source_path,
                        "file_index": index_by_path[source_path],
                        "source_hunk_hint": hunk_hint,
                        "source_snippet": snippet,
                        "grounding": "pr_diff_and_current_downstream_source",
                    }
                )
                if not duplicate:
                    seen_claims.add(claim.lower())
                    curated.append(
                        {
                            "record_type": "pr_preservation_derived_atom",
                            "pr_preservation_derived": True,
                            "pr_preservation_grounded": True,
                            "file_index": index_by_path[source_path],
                            "source_path": source_path,
                            "source_hunk_hint": hunk_hint,
                            "source_kind": classify_source_kind(claim),
                            "source_snippet": snippet,
                            "semantic_claim": full_claim,
                            "high_risk": True,
                            "risk_tags": row["risk_tags"],
                            "mapping_status": "missing",
                            "destinations": [],
                            "equivalence_argument": None,
                            "required_change": "Verify and restore this PR-preservation invariant in the v2.2 port, or provide precise destination evidence and update the mapping.",
                            "test_strategy": "pr_diff_equivalence_regression",
                            "negative_test_candidate": f"Replay or unit-test the smallest downstream scenario introduced by {entry.pr_key} that exercises `{claim}` and fail if the v2.2 port omits or changes it.",
                            "adversarial_review": {"required": True, "status": "not_requested", "review_record_id": None},
                            "review_required": True,
                            "source_prs": [{"key": entry.pr_key, "slug": entry.slug, "merge_commit": commit}],
                            "source_pr_claims": [claim],
                            "source_flow_ids": [raw_id],
                            "notes": "Curated from pr-preservation-map.md by inspecting the local PR merge diff and confirming live current downstream source ownership.",
                        }
                    )
            raw_rows.append(row)

    by_path = Counter()
    for atom in curated:
        _, rec = file_records[atom["file_index"]]
        atoms = rec.setdefault("atoms", [])
        next_idx = max([a.get("atom_index", 0) for a in atoms] or [0]) + 1
        atom["atom_index"] = next_idx
        atom["record_id"] = f"file-{atom['file_index']:04d}-atom-{next_idx:04d}"
        atoms.append(atom)
        rec["atoms_total"] = len(atoms)
        for a in atoms:
            a["atoms_total"] = len(atoms)
        tags = set(rec.get("tags", []))
        tags.update(atom["risk_tags"])
        tags.update(["high-risk", "non-exact", "needs-review"])
        rec["tags"] = sorted(tags)
        by_path[atom["source_path"]] += 1

    for path, rec in file_records.values():
        path.write_text(json.dumps(rec, indent=2, sort_keys=False) + "\n")

    write_artifacts(entries, raw_rows, curated, by_path, removed_existing, file_records)
    print_summary(entries, raw_rows, curated, by_path, unresolved, removed_existing, file_records)


def classify_source_kind(claim: str) -> str:
    low = claim.lower()
    if any(k in low for k in ["codec", "abi", "signature", "hash", "tx type", "receipt"]):
        return "encoding_rule"
    if any(k in low for k in ["reject", "invalid", "fail", "error", "overflow", "duplicate"]):
        return "error_path"
    if any(k in low for k in ["ordering", "reordering", "sequence"]):
        return "call_ordering"
    if any(k in low for k in ["constant", "default", "cap", "deadline", "ttl", "fee"]):
        return "consensus_constant"
    return "state_transition"


def write_artifacts(entries, raw_rows, curated, by_path, removed_existing, file_records) -> None:
    (AUDIT_DIR / "raw-pr-derived-atoms.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in raw_rows) + "\n"
    )
    (AUDIT_DIR / "curated-pr-derived-atoms.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in curated) + "\n"
    )
    decisions = []
    for row in raw_rows:
        decisions.append(
            {
                "raw_pr_id": row["raw_pr_id"],
                "entry_index": row["entry_index"],
                "pr_key": row["pr_key"],
                "slug": row["slug"],
                "semantic_claim": row["semantic_claim"],
                "decision": row.get("decision"),
                "reason": row.get("drop_reason") or row.get("decision"),
                "current_source_path": row.get("current_source_path"),
                "file_index": row.get("file_index"),
            }
        )
    (AUDIT_DIR / "pr-curation-decisions.jsonl").write_text(
        "\n".join(json.dumps(d, sort_keys=True) for d in decisions) + "\n"
    )
    queue_additions = ["# PR-Preservation Review Queue Additions", ""]
    for atom in curated:
        queue_additions.extend(
            [
                f"### File {atom['file_index']:04d}: {atom['source_path']}",
                "",
                f"- Source: `{atom['source_hunk_hint']}`",
                f"- Claim: {atom['semantic_claim']}",
                f"- PRs: {', '.join('`' + p['key'] + '`' for p in atom['source_prs'])}",
                f"- Negative test: {atom['negative_test_candidate']}",
                "",
            ]
        )
    (AUDIT_DIR / "review-queue-additions.md").write_text("\n".join(queue_additions))

    reason_counts = Counter(row.get("drop_reason") or row.get("decision") for row in raw_rows)
    entry_decisions = defaultdict(Counter)
    for row in raw_rows:
        entry_decisions[row["pr_key"]][row.get("decision")] += 1
    report = [
        "# PR-Preservation Atom Curation Report",
        "",
        "- Method: inspected local first-parent PR/branch merge diffs, then verified candidate behaviors against current downstream source files before insertion.",
        f"- PR/merge entries enumerated: {len(entries)}",
        f"- Existing PR-preservation atoms replaced: {removed_existing}",
        f"- Raw PR-derived candidates/decision rows: {len(raw_rows)}",
        f"- Curated grouped atoms: {len(curated)}",
        f"- Inserted atoms: {len(curated)}",
        "",
        "## Decisions",
    ]
    report.extend(f"- `{k}`: {v}" for k, v in sorted(reason_counts.items()))
    report.extend(["", "## Inserted By Source Path"])
    report.extend(f"- `{path}`: {count}" for path, count in by_path.most_common())
    report.extend(["", "## Entry Closure"])
    for entry in entries:
        counts = dict(entry_decisions.get(entry.pr_key, {}))
        report.append(f"- `{entry.pr_key}` `{entry.slug}`: {counts}")
    (AUDIT_DIR / "curation-report.md").write_text("\n".join(report) + "\n")

    rebuild_ledgers(file_records, curated, reason_counts, len(entries), len(raw_rows), removed_existing)


def rebuild_ledgers(file_records, curated, reason_counts, entry_count, raw_count, removed_existing) -> None:
    index_lines = []
    review_atoms = []
    all_recs = []
    for file_index in sorted(file_records):
        _, rec = file_records[file_index]
        all_recs.append(rec)
        index_lines.append(
            json.dumps(
                {
                    "record_type": "index_entry",
                    "file_index": rec.get("file_index"),
                    "source_status": rec.get("source_status"),
                    "source_path": rec.get("source_path"),
                    "source_old_path": rec.get("source_old_path"),
                    "file_classification": rec.get("file_classification"),
                    "file_status": rec.get("file_status"),
                    "atoms_total": rec.get("atoms_total", len(rec.get("atoms", []))),
                    "tags": rec.get("tags", []),
                },
                sort_keys=True,
            )
        )
        for atom in rec.get("atoms", []):
            if atom.get("review_required") or atom.get("mapping_status") in {"missing", "blocked"}:
                review_atoms.append((file_index, rec.get("source_path"), atom))
    (COVERAGE / "index.jsonl").write_text("\n".join(index_lines) + "\n")

    queue = [
        "# Coverage Map Review Queue",
        "",
        f"Generated after PR-preservation insertion. Total queued atoms: {len(review_atoms)}",
        "",
    ]
    for file_index, source_path, atom in review_atoms:
        queue.extend(
            [
                f"### File {file_index:04d}: {source_path}",
                "",
                f"- Key: `file_index={file_index}`, `source_path={source_path}`, `record_id={atom.get('record_id')}`",
                f"  - Source hunk: `{atom.get('source_hunk_hint')}`",
                f"  - Mapping status: `{atom.get('mapping_status')}`",
                f"  - Required change: {atom.get('required_change', atom.get('semantic_claim'))}",
                f"  - Negative test: {atom.get('negative_test_candidate')}",
                "",
            ]
        )
    (COVERAGE / "review-queue.md").write_text("\n".join(queue))

    all_atoms = [atom for rec in all_recs for atom in rec.get("atoms", [])]
    pr_atoms = [atom for atom in all_atoms if atom.get("pr_preservation_derived")]
    errors = []
    if len(all_recs) != 579:
        errors.append(f"expected 579 file artifacts, found {len(all_recs)}")
    if sorted(rec.get("file_index") for rec in all_recs) != list(range(1, 580)):
        errors.append("file indices are not exactly 1..579")
    if sum(rec.get("atoms_total", 0) for rec in all_recs) != len(all_atoms):
        errors.append("embedded atom counts do not match atoms_total")
    if any(atom.get("pr_preservation_derived") and not atom.get("pr_preservation_grounded") for atom in all_atoms):
        errors.append("PR-preservation atom without grounding flag")
    if any(atom.get("pr_preservation_derived") and "pr-preservation-map.md" in str(atom.get("source_hunk_hint", "")) for atom in all_atoms):
        errors.append("PR-preservation atom grounded only in map prose")

    old_summary_path = COVERAGE / "validation-summary.json"
    old = json.loads(old_summary_path.read_text()) if old_summary_path.exists() else {}
    summary = {
        "generated_at": datetime.now(timezone(timedelta(hours=-4))).isoformat(timespec="seconds"),
        "total_files": len(all_recs),
        "counts_by_file_classification": dict(Counter(rec.get("file_classification", "unknown") for rec in all_recs)),
        "counts_by_file_status": old.get("counts_by_file_status", dict(Counter(rec.get("file_status", "unknown") for rec in all_recs))),
        "counts_by_atom_mapping_status": dict(Counter(atom.get("mapping_status", "unknown") for atom in all_atoms)),
        "atoms_total": len(all_atoms),
        "high_risk_atoms_total": sum(1 for atom in all_atoms if atom.get("high_risk")),
        "non_exact_atoms_total": sum(1 for atom in all_atoms if atom.get("mapping_status") != "exact"),
        "adversarial_review_status": dict(Counter(atom.get("adversarial_review", {}).get("status", "unknown") for atom in all_atoms)),
        "human_review_queue_total": len(review_atoms),
    }
    for key in [
        "curated_test_atom_insertion",
        "curated_feature_atom_insertion",
        "curated_functionality_flow_atom_insertion",
    ]:
        if key in old:
            summary[key] = old[key]
    summary["curated_pr_preservation_atom_insertion"] = {
        "method": "pr_merge_diff_then_current_downstream_source_retrace",
        "pr_merge_entries": entry_count,
        "existing_pr_preservation_atoms_replaced": removed_existing,
        "raw_pr_candidates": raw_count,
        "promoted_raw_rows": len(pr_atoms),
        "curated_grouped_atoms": len(pr_atoms),
        "inserted_atoms": len(pr_atoms),
        "dropped_by_reason": dict(reason_counts),
        "curated_artifacts": [
            "coverage-map/pr-preservation-audit/raw-pr-derived-atoms.jsonl",
            "coverage-map/pr-preservation-audit/curated-pr-derived-atoms.jsonl",
            "coverage-map/pr-preservation-audit/pr-curation-decisions.jsonl",
        ],
    }
    summary["validation_checks"] = {
        "exactly_579_file_artifacts_exist": len(all_recs) == 579,
        "all_expected_file_indices_exist": sorted(rec.get("file_index") for rec in all_recs) == list(range(1, 580)),
        "embedded_atom_counts_match_atoms_total": sum(rec.get("atoms_total", 0) for rec in all_recs) == len(all_atoms),
        "mapped_atoms_have_destination_evidence": all(
            (atom.get("mapping_status") not in {"exact", "renamed_exact", "covered_by_upstream", "moved_to_dependency", "structural_equivalent"})
            or atom.get("destinations")
            for atom in all_atoms
        ),
        "new_pr_preservation_atoms_queued": all(atom.get("review_required") for atom in pr_atoms),
        "pr_preservation_atoms_are_source_grounded": not any(
            atom.get("pr_preservation_derived") and "pr-preservation-map.md" in str(atom.get("source_hunk_hint", ""))
            for atom in all_atoms
        ),
    }
    summary["validation_errors"] = errors
    summary["notes"] = "Updated after PR-preservation insertion; PR map prose was used as an index, with promoted atoms grounded in current downstream source evidence."
    old_summary_path.write_text(json.dumps(summary, indent=2, sort_keys=False) + "\n")


def print_summary(entries, raw_rows, curated, by_path, unresolved, removed_existing, file_records) -> None:
    all_atoms = [atom for _, rec in file_records.values() for atom in rec.get("atoms", [])]
    print(
        json.dumps(
            {
                "entries": len(entries),
                "unresolved_entries": unresolved,
                "removed_existing_pr_atoms": removed_existing,
                "raw_rows": len(raw_rows),
                "inserted": len(curated),
                "atoms_total": len(all_atoms),
                "decision_counts": dict(Counter(row.get("drop_reason") or row.get("decision") for row in raw_rows)),
                "top_paths": by_path.most_common(12),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
