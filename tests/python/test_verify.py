"""tools/verify.py against a throwaway project whose Makefile has a passing and a failing target."""

from __future__ import annotations

import json
import os

import pytest
from conftest import ROOT

MAKEFILE = """\
lint:
\t@echo lint is fine
typecheck:
\t@echo typecheck is fine
test:
\t@echo tests are failing
\t@exit 3
"""


@pytest.fixture
def project(tmp_path):
    """Return a folder with a Makefile (no git, no node_modules)."""
    (tmp_path / "Makefile").write_text(MAKEFILE, encoding="utf8")
    return tmp_path


def latest_run(project):
    """Return the only run folder below artifacts/verification/runs."""
    runs = list((project / "artifacts" / "verification" / "runs").iterdir())
    assert len(runs) == 1
    return runs[0]


def test_a_failing_step_does_not_stop_the_others_and_fails_the_run(project, run_tool):
    result = run_tool("verify.py", "--steps", "lint,test,typecheck", cwd=project)
    assert result.returncode == 1, result.stdout
    run = latest_run(project)
    summary = json.loads((run / "summary.json").read_text(encoding="utf8"))
    steps = {step["name"]: step for step in summary["steps"]}
    assert [step["name"] for step in summary["steps"]] == ["lint", "typecheck", "test"], "canonical order"
    assert steps["lint"]["status"] == "PASS" and steps["lint"]["exit_code"] == 0
    assert steps["test"]["status"] == "FAIL" and steps["test"]["exit_code"] != 0
    assert steps["typecheck"]["status"] == "PASS", "the step after the failing one must still run"
    assert summary["status"] == "FAIL"
    assert str(run.relative_to(project)) in result.stdout


def test_summary_records_the_run_environment_and_logs(project, run_tool):
    run_tool("verify.py", "--steps", "lint", cwd=project)
    run = latest_run(project)
    summary = json.loads((run / "summary.json").read_text(encoding="utf8"))
    assert summary["run_id"] == run.name and len(run.name) == len("20261015T040000Z")
    for key in ("started_at", "finished_at", "duration_s", "git", "versions", "os", "steps", "evidence"):
        assert key in summary
    assert {"commit", "dirty"} <= set(summary["git"])
    assert {"node", "python", "playwright"} <= set(summary["versions"])
    assert summary["os"]["system"]
    step = summary["steps"][0]
    assert {"name", "command", "exit_code", "status", "duration_s", "log"} <= set(step)
    assert step["command"] == "make lint"
    assert "lint is fine" in (run / step["log"]).read_text(encoding="utf8")
    assert (run / "graph-validation.json").is_file()


def test_a_passing_run_exits_zero(project, run_tool):
    result = run_tool("verify.py", "--steps", "lint,typecheck", cwd=project)
    assert result.returncode == 0, result.stdout
    summary = json.loads((latest_run(project) / "summary.json").read_text(encoding="utf8"))
    assert summary["status"] == "PASS"


def test_environment_variables_never_reach_the_evidence(project, run_tool):
    environment = {**os.environ, "AIXON_TEST_SECRET": "do-not-leak-0123456789"}
    run_tool("verify.py", "--steps", "lint", cwd=project, env=environment)
    run = latest_run(project)
    for path in run.rglob("*"):
        if path.is_file():
            assert "do-not-leak-0123456789" not in path.read_text(encoding="utf8", errors="replace")


def test_graph_validation_of_the_real_graphs_has_no_g_errors(run_tool, tmp_path):
    """Run from the repository root so the seed, atlas and fixture graphs are found."""
    result = run_tool("verify.py", "--steps", "secrets", "--runs-dir", tmp_path / "runs", cwd=ROOT)
    run = next((tmp_path / "runs").iterdir())
    document = json.loads((run / "graph-validation.json").read_text(encoding="utf8"))
    by_label = {item["graph"]: item for item in document["results"]}
    assert by_label["seed+atlas"]["g_errors"] == 0
    assert by_label["fixture"]["g_errors"] == 0
    assert result.returncode == 0, result.stdout


def test_unknown_step_is_rejected(project, run_tool):
    result = run_tool("verify.py", "--steps", "lint,bogus", cwd=project)
    assert result.returncode == 2
    assert "unknown step" in result.stderr
