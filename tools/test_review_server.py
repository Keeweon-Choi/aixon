"""HTTP-level tests for the local ADR-025 review server."""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import pytest

import public_gate as pg
import review
import review_server as server


HERE = Path(__file__).resolve().parent
WIKI = """---
id: wiki:softmax
entity: concept:softmax
title: Softmax
status: draft
claims: [clm:algebra-prereq-softmax]
sources: [src:mini:notes]
review: null
published_at: null
---

Softmax body.
"""


def clean_env(agent=False):
    env = {key: value for key, value in os.environ.items() if key not in {"CLAUDECODE", "AI_AGENT"} and not key.startswith("CODEX_")}
    if agent:
        env["CLAUDECODE"] = "1"
    return env


def free_port():
    try:
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]
    except PermissionError:
        pytest.skip("sandbox does not permit localhost sockets")


def start(tmp_path, agent=False):
    tmp_path.mkdir(parents=True, exist_ok=True)
    graph = tmp_path / "g.yaml"
    if not graph.exists():
        shutil.copy(HERE / "fixtures/mini_graph.yaml", graph)
    wiki_dir = tmp_path / "wiki"; wiki_dir.mkdir()
    (wiki_dir / "softmax.mdx").write_text(WIKI, encoding="utf-8")
    review_dir = tmp_path / "review"; review_dir.mkdir()
    (review_dir / "pre.yaml").write_text("items:\n  - id: concept:softmax\n    recommendation: fix\n    notes: pre-review note\n    fix: revise summary\n", encoding="utf-8")
    port = free_port()
    process = subprocess.Popen(
        [sys.executable, str(HERE / "review_server.py"), "--graph", str(graph), "--wiki-dir", str(wiki_dir), "--review-dir", str(review_dir), "--port", str(port), "--by", "human:default"],
        cwd=tmp_path, env=clean_env(agent), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    line = process.stdout.readline().strip()
    if not line:
        stderr = process.stderr.read()
        process.wait(timeout=2)
        raise RuntimeError(stderr)
    return process, line, graph, wiki_dir, review_dir


def request(url, method="GET", data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def stop(process):
    process.terminate()
    process.wait(timeout=2)


def test_queue_requires_token_and_reports_fresh_then_stale_approval(tmp_path):
    graph = tmp_path / "g.yaml"
    shutil.copy(HERE / "fixtures/mini_graph.yaml", graph)
    review.approve_record([str(graph)], "concept:algebra", "human:tester", "ok", [], "2026-10-15")
    process, url, graph, _wiki, _review = start(tmp_path)
    try:
        status, _body = request(url.split("/?")[0] + "/api/queue")
        assert status == 403
        queue_url = url.replace("/?token=", "/api/queue?token=")
        status, body = request(queue_url)
        assert status == 200
        rows = {row["id"]: row for row in body["records"]}
        assert rows["concept:algebra"]["state"] == "approved"
        assert rows["concept:softmax"]["pre_review"]["notes"] == "pre-review note"
        graph.write_text(graph.read_text(encoding="utf-8").replace("Basic symbolic algebra.", "Edited algebra."), encoding="utf-8")
        status, body = request(queue_url)
        assert status == 200
        assert {row["id"]: row for row in body["records"]}["concept:algebra"]["state"] == "stale"
    finally:
        stop(process)


def test_decisions_refuse_agent_server_and_apply_clean_server(tmp_path):
    process, url, _graph, _wiki, _review = start(tmp_path, agent=True)
    try:
        status, body = request(url.replace("/?token=", "/api/decisions?token="), "POST", {"by": "human:tester", "decisions": []})
        assert status == 403 and "AI 에이전트" in body["error"]
    finally:
        stop(process)

    process, url, graph, wiki_dir, review_dir = start(tmp_path / "clean")
    try:
        status, body = request(url.replace("/?token=", "/api/decisions?token="), "POST", {"by": "human:tester", "decisions": [
            {"id": "concept:algebra", "decision": "approve", "note": "entity"},
            {"id": "clm:algebra-prereq-softmax", "decision": "approve", "note": "claim"},
            {"id": "method:attention", "decision": "exclude", "note": "not now"},
            {"id": "wiki:softmax", "decision": "approve", "note": "wiki", "publish": True},
        ]})
        assert status == 200 and not body["failed"]
        assert list((review_dir / "decisions").glob("*.yaml"))
        records = server.st.load_graph([str(graph)])["entities"]
        assert server.st.approval_state(records["concept:algebra"]) == "approved"
        assert records["method:attention"].get("review") is None
        meta, body_text = pg.read_wiki(wiki_dir / "softmax.mdx")
        assert meta["status"] == "published" and pg.wiki_approval(meta, body_text) == "approved"
    finally:
        stop(process)


def test_commit_push_scopes_paths_without_touching_remote():
    assert server.COMMIT_PATHS == ("review", "data", "src/content/wiki")


def test_commit_push_refuses_non_human_reviewer(monkeypatch):
    for key in [k for k in os.environ if k in {"CLAUDECODE", "AI_AGENT"} or k.startswith("CODEX_")]:
        monkeypatch.delenv(key)
    monkeypatch.setattr(server.subprocess, "run", lambda *a, **k: pytest.fail("git must not run"))
    for by in ("agent:x", "panel:rel1", 123):
        with pytest.raises(PermissionError):
            server.ReviewService.commit_push(by, 1)


def test_two_saves_in_one_second_keep_both_decision_files(tmp_path, monkeypatch):
    for key in [k for k in os.environ if k in {"CLAUDECODE", "AI_AGENT"} or k.startswith("CODEX_")]:
        monkeypatch.delenv(key)
    graph = tmp_path / "g.yaml"
    shutil.copy(HERE / "fixtures/mini_graph.yaml", graph)
    service = server.ReviewService([str(graph)], str(tmp_path / "wiki"), str(tmp_path / "review"), "human:t", "tok")
    for ident in ("method:attention", "concept:softmax"):
        service.write_decisions("human:t", [{"id": ident, "decision": "exclude"}])
    assert len(list((tmp_path / "review/decisions").glob("*.yaml"))) == 2
