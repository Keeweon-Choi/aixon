"""Shared helpers for the harness tests: run the tools/ scripts exactly as `make` does."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
FIXTURES = ROOT / "tests" / "fixtures"
FIXTURE_GRAPH = FIXTURES / "graph" / "site_graph.yaml"
FIXTURE_WIKI = FIXTURES / "wiki"
BAD_WIKI = FIXTURES / "wiki_bad"


def run_script(script: str, *args: object, cwd: Path = ROOT, env: dict | None = None):
    """Run tools/<script> with the current interpreter and return the CompletedProcess."""
    command = [sys.executable, str(TOOLS / script), *[str(item) for item in args]]
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, env=env)


@pytest.fixture
def run_tool():
    """Return the function that runs a script of tools/."""
    return run_script
