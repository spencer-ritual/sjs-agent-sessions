#!/usr/bin/env python3
"""Run selected gold1p traffic workloads and write structured results."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path(__file__).with_name("gold1p-batch-results.json")
DEFAULT_TRAFFIC_REPO = Path("/home/ritual/repos/traffic-gen-internal")


def parse_csv(value: str | None) -> set[str]:
    if not value:
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def parse_rows(value: str | None) -> set[int]:
    rows: set[int] = set()
    for item in parse_csv(value):
        rows.add(int(item))
    return rows


def load_workloads(path: Path) -> list[dict[str, Any]]:
    with path.open() as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array")
    return data


def select_workloads(
    workloads: list[dict[str, Any]],
    *,
    only: set[str],
    rows: set[int],
    skip: set[str],
) -> list[dict[str, Any]]:
    selected = []
    for workload in workloads:
        name = str(workload["name"])
        row = int(workload["row"])
        if only and name not in only:
            continue
        if rows and row not in rows:
            continue
        if name in skip:
            continue
        selected.append(workload)
    return selected


def rewrite_start_agent_index(
    command: str,
    *,
    base: int | None,
    step: int,
    selected_index: int,
) -> str:
    if base is None:
        return command
    replacement = f"--start-agent-index {base + selected_index * step}"
    if "--start-agent-index" not in command:
        return command
    return re.sub(r"--start-agent-index\s+\d+", replacement, command, count=1)


def run_command(
    command: str,
    *,
    cwd: Path,
    timeout: int,
) -> tuple[int, float, str]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        return completed.returncode, time.monotonic() - started, completed.stdout
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        return 124, time.monotonic() - started, output + "\n[TIMEOUT]\n"


def output_tail(output: str, max_chars: int) -> str:
    if len(output) <= max_chars:
        return output
    return output[-max_chars:]


def write_markdown(path: Path, results: list[dict[str, Any]], source_json: Path) -> None:
    passed = sum(1 for result in results if result["status"] == "PASS")
    failed = len(results) - passed
    lines = [
        "# Gold1p Traffic Rerun",
        "",
        f"Source workload JSON: `{source_json}`",
        "",
        "## Summary",
        "",
        f"- Result: `{passed}/{len(results)}` workloads passed; `{failed}` failed.",
        f"- Total runtime: `{sum(result['elapsed_seconds'] for result in results):.1f}s`.",
        "",
        "## Workloads",
        "",
        "| Row | Workload | Status | Runtime | Attempts | Command | Note |",
        "| --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for result in results:
        note = result.get("note", "").replace("|", "\\|")
        command = result["cmd"].replace("|", "\\|")
        lines.append(
            f"| {result['row']} | `{result['name']}` | `{result['status']}` | "
            f"`{result['elapsed_seconds']:.1f}s` | `{result['attempts']}` | "
            f"`{command}` | {note} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path)
    parser.add_argument("--traffic-repo", type=Path, default=DEFAULT_TRAFFIC_REPO)
    parser.add_argument("--only", help="Comma-separated workload names to run")
    parser.add_argument("--rows", help="Comma-separated workload row numbers to run")
    parser.add_argument("--skip", help="Comma-separated workload names to skip")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--retries", type=int, default=0)
    parser.add_argument("--tail-chars", type=int, default=12_000)
    parser.add_argument("--start-agent-index-base", type=int)
    parser.add_argument("--start-agent-index-step", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    workloads = load_workloads(args.input)
    selected = select_workloads(
        workloads,
        only=parse_csv(args.only),
        rows=parse_rows(args.rows),
        skip=parse_csv(args.skip),
    )
    if not selected:
        raise SystemExit("No workloads selected")

    results = []
    for selected_index, workload in enumerate(selected):
        command = rewrite_start_agent_index(
            workload["cmd"],
            base=args.start_agent_index_base,
            step=args.start_agent_index_step,
            selected_index=selected_index,
        )
        print(f"[gold1p] row={workload['row']} name={workload['name']} cmd={command}", flush=True)
        if args.dry_run:
            results.append(
                {
                    "row": workload["row"],
                    "name": workload["name"],
                    "cmd": command,
                    "status": "DRY_RUN",
                    "code": None,
                    "elapsed_seconds": 0.0,
                    "attempts": 0,
                    "note": "Not executed",
                    "output_tail": "",
                }
            )
            continue

        attempts = 0
        final_code = 1
        final_elapsed = 0.0
        final_output = ""
        for attempt in range(args.retries + 1):
            attempts = attempt + 1
            final_code, final_elapsed, final_output = run_command(
                command,
                cwd=args.traffic_repo,
                timeout=args.timeout,
            )
            if final_code == 0:
                break
            if attempt < args.retries:
                print(
                    f"[gold1p] retrying row={workload['row']} after code={final_code}",
                    flush=True,
                )

        status = "PASS" if final_code == 0 else "FAIL"
        note = workload.get("note", "")
        results.append(
            {
                "row": workload["row"],
                "name": workload["name"],
                "cmd": command,
                "status": status,
                "code": final_code,
                "elapsed_seconds": round(final_elapsed, 3),
                "attempts": attempts,
                "note": note,
                "output_tail": output_tail(final_output, args.tail_chars),
            }
        )
        print(
            f"[gold1p] {status} row={workload['row']} name={workload['name']} "
            f"elapsed={final_elapsed:.1f}s attempts={attempts}",
            flush=True,
        )

    args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    if args.markdown:
        write_markdown(args.markdown, results, args.input)

    failed = [result for result in results if result["status"] == "FAIL"]
    if failed:
        print(f"[gold1p] failed workloads: {[result['name'] for result in failed]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
