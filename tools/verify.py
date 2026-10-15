#!/usr/bin/env python3
"""Run every verification step and keep auditable evidence of the run.

Steps (each is a `make` target, run in this order, a failure does not stop the later steps):
    lint, typecheck, test, validate, validate-fixtures, build, check-dist, build-public, check-dist-public,
    e2e, e2e-seed, secrets

Evidence is written to artifacts/verification/runs/<UTC yyyymmddTHHMMSSZ>/:
    summary.json            run id, times, git commit + dirty flag, tool versions, OS, per-step result
    logs/NN-<step>.log      combined stdout/stderr of each step
    graph-validation.json   `seedtool validate --json` of the seed + atlas graphs and the fixture graph
    test-results/           Playwright JSON reports and per-test failure output
    screenshots/            failure screenshots
    playwright-traces/      failure traces (open with `npx playwright show-trace`)

Environment variables and tokens are never written to the evidence folder.

Usage:
    verify.py [--steps lint,test,...] [--runs-dir DIR]

Exit code: 0 when every step passed, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STEPS = (
    "lint",
    "typecheck",
    "test",
    "validate",
    "validate-fixtures",
    "build",
    "check-dist",
    "build-public",
    "check-dist-public",
    "e2e",
    "e2e-seed",
    "secrets",
)
DEFAULT_RUNS_DIR = "artifacts/verification/runs"
STEP_TIMEOUT_SECONDS = 1800
LOG_TAIL_LINES = 12
CAPTURE_TIMEOUT_SECONDS = 5
GRAPH_SETS = (
    ("seed+atlas", ["data/seed/seed_graph.yaml", "data/graph/atlas.yaml"]),
    ("fixture", ["tests/fixtures/graph/site_graph.yaml"]),
)
PLAYWRIGHT_TARGETS = ("fixture", "seed")


def utc_now() -> datetime:
    """Return the current time in UTC."""
    return datetime.now(timezone.utc)


def iso(moment: datetime) -> str:
    """Format a time as an ISO 8601 UTC string."""
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def capture(command: list[str]) -> str | None:
    """Run a command and return its stripped stdout, or None when it cannot run."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=CAPTURE_TIMEOUT_SECONDS)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def git_info() -> dict[str, Any]:
    """Return the commit, branch and whether the working tree has uncommitted changes."""
    commit = capture(["git", "rev-parse", "HEAD"])
    branch = capture(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    status = capture(["git", "status", "--porcelain"])
    return {"commit": commit, "branch": branch, "dirty": bool(status) if status is not None else None}


def tool_versions() -> dict[str, str | None]:
    """Return the versions of the tools the steps rely on."""
    playwright = capture(["npx", "--no-install", "playwright", "--version"]) if Path("node_modules").is_dir() else None
    make = capture(["make", "--version"])
    return {
        "node": capture(["node", "--version"]),
        "python": platform.python_version(),
        "playwright": playwright.replace("Version ", "") if playwright else None,
        "make": make.splitlines()[0] if make else None,
    }


def os_info() -> dict[str, str]:
    """Return operating system facts (no environment variables)."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "platform": platform.platform(),
    }


def run_step(index: int, name: str, run_dir: Path) -> dict[str, Any]:
    """Run `make <name>`, log its output and return the step record."""
    command = ["make", name]
    log_path = run_dir / "logs" / f"{index:02d}-{name}.log"
    started = time.monotonic()
    with log_path.open("w", encoding="utf8") as log:
        log.write(f"$ {' '.join(command)}\n\n")
        log.flush()
        try:
            completed = subprocess.run(
                command, stdout=log, stderr=subprocess.STDOUT, timeout=STEP_TIMEOUT_SECONDS
            )
            exit_code = completed.returncode
        except subprocess.TimeoutExpired:
            log.write(f"\nTIMEOUT after {STEP_TIMEOUT_SECONDS} s\n")
            exit_code = 124
        except OSError as error:
            log.write(f"\ncannot run the command: {error}\n")
            exit_code = 127
    return {
        "name": name,
        "command": " ".join(command),
        "exit_code": exit_code,
        "status": "PASS" if exit_code == 0 else "FAIL",
        "duration_s": round(time.monotonic() - started, 2),
        "log": log_path.relative_to(run_dir).as_posix(),
    }


def tail(path: Path, lines: int = LOG_TAIL_LINES) -> str:
    """Return the last lines of a text file."""
    return "\n".join(path.read_text(encoding="utf8", errors="replace").splitlines()[-lines:])


def write_graph_validation(run_dir: Path) -> dict[str, Any]:
    """Run `seedtool validate --json` on each graph set and save graph-validation.json."""
    seedtool = Path(__file__).resolve().parent / "seedtool.py"
    results = []
    for label, paths in GRAPH_SETS:
        existing = [item for item in paths if Path(item).is_file()]
        if not existing:
            results.append({"graph": label, "paths": paths, "skipped": "no graph file found"})
            continue
        completed = subprocess.run(
            [sys.executable, str(seedtool), "validate", "--json", *existing],
            capture_output=True,
            text=True,
        )
        try:
            issues = json.loads(completed.stdout) if completed.stdout.strip() else []
        except json.JSONDecodeError:
            issues = [{"code": "TOOL", "ref": "seedtool", "message": completed.stdout[:300]}]
        counts: dict[str, int] = {}
        for issue in issues:
            counts[issue["code"]] = counts.get(issue["code"], 0) + 1
        results.append(
            {
                "graph": label,
                "paths": existing,
                "exit_code": completed.returncode,
                "g_errors": sum(1 for issue in issues if str(issue["code"]).startswith("G")),
                "counts_by_code": counts,
                "issues": issues,
            }
        )
    document = {"tool": "tools/seedtool.py validate --json", "results": results}
    (run_dir / "graph-validation.json").write_text(
        json.dumps(document, ensure_ascii=False, indent=2), encoding="utf8"
    )
    return document


def collect_playwright_evidence(run_dir: Path) -> dict[str, list[str]]:
    """Copy Playwright JSON reports and failure screenshots / traces into the run folder."""
    copied: dict[str, list[str]] = {"reports": [], "screenshots": [], "traces": []}
    for target in PLAYWRIGHT_TARGETS:
        report = Path("playwright-report") / f"{target}.json"
        if report.is_file():
            destination = run_dir / "test-results" / f"playwright-{target}.json"
            shutil.copy2(report, destination)
            copied["reports"].append(destination.relative_to(run_dir).as_posix())
        results = Path("test-results") / target
        if not results.is_dir():
            continue
        for path in sorted(item for item in results.rglob("*") if item.is_file()):
            relative = path.relative_to(results)
            flat = "__".join(relative.parts)
            if path.suffix == ".png":
                destination = run_dir / "screenshots" / target / flat
                key = "screenshots"
            elif path.name == "trace.zip":
                destination = run_dir / "playwright-traces" / target / f"{relative.parts[0]}.zip"
                key = "traces"
            else:
                destination = run_dir / "test-results" / target / flat
                key = None
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            if key:
                copied[key].append(destination.relative_to(run_dir).as_posix())
    return copied


def build_parser() -> argparse.ArgumentParser:
    """Return the command line parser."""
    parser = argparse.ArgumentParser(description="Run all verification steps and keep the evidence.")
    parser.add_argument("--steps", help="comma-separated subset of: " + ", ".join(STEPS))
    parser.add_argument("--runs-dir", default=DEFAULT_RUNS_DIR, help="where run folders are created")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the steps, write the evidence and return the exit code."""
    args = build_parser().parse_args(argv)
    chosen = [item.strip() for item in args.steps.split(",") if item.strip()] if args.steps else list(STEPS)
    unknown = [item for item in chosen if item not in STEPS]
    if unknown:
        print(f"error: unknown step(s): {', '.join(unknown)}", file=sys.stderr)
        return 2
    steps = [item for item in STEPS if item in chosen]
    started = utc_now()
    run_id = started.strftime("%Y%m%dT%H%M%SZ")
    run_dir = Path(args.runs_dir) / run_id
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    print(f"verify: run {run_id} -> {run_dir}")
    write_graph_validation(run_dir)
    records = []
    for index, name in enumerate(steps, start=1):
        print(f"[{index}/{len(steps)}] make {name} ...", flush=True)
        record = run_step(index, name, run_dir)
        records.append(record)
        print(f"[{index}/{len(steps)}] make {name}: {record['status']} ({record['duration_s']} s)", flush=True)
        if record["status"] == "FAIL":
            print(tail(run_dir / record["log"]))
    evidence = collect_playwright_evidence(run_dir)
    finished = utc_now()
    passed = all(record["status"] == "PASS" for record in records)
    summary = {
        "run_id": run_id,
        "started_at": iso(started),
        "finished_at": iso(finished),
        "duration_s": round((finished - started).total_seconds(), 2),
        "status": "PASS" if passed else "FAIL",
        "git": git_info(),
        "versions": tool_versions(),
        "os": os_info(),
        "steps": records,
        "evidence": {"graph_validation": "graph-validation.json", **evidence},
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf8")
    print()
    for record in records:
        print(f"  {record['status']:4}  {record['name']:<18} {record['duration_s']:>8} s  {record['log']}")
    print(f"\nverify: {summary['status']} - evidence in {run_dir}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
