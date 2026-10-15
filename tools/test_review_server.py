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


# --- cross-review integration (queue() called directly, no sockets) ---
import cross_review as cr  # noqa: E402
import test_cross_review as tcr  # noqa: E402


def cross_queue(tmp_path, with_wiki=False):
    paths, wiki, directory = tcr.setup_release(tmp_path, with_wiki)
    service = server.ReviewService(paths, wiki, str(tmp_path / "review"), "human:t", "tok")
    return service, paths, wiki, directory


def queue_rows(service):
    return {row["id"]: row for row in service.queue()["records"]}


def test_queue_shows_confirm_status_from_real_confirm_json(tmp_path):
    service, _paths, _wiki, directory = cross_queue(tmp_path)
    other = {"url": "https://example.org/other", "tier": "A", "passage": "Another passage."}
    tcr.mutate_report(directory, "source", lambda d: d["items"][0]["checks"][0]["sources"].append(other))
    tcr.write_confirm(directory, {f"{tcr.SOURCE['url']}\n{tcr.SOURCE['passage']}": {"status": "found"}, f"{other['url']}\n{other['passage']}": {"status": "not-found"}})
    by_reviewer = {entry["reviewer"]: entry for entry in queue_rows(service)[tcr.ENTITY]["cross_review"]}
    assert [s["confirm"] for s in by_reviewer["agent:source"]["checks"][0]["sources"]] == ["found", "not-found"]
    assert {s["confirm"] for check in by_reviewer["agent:claim"]["checks"] for s in check["sources"]} == {"found"}


def test_queue_includes_real_check_release_problems_for_fix_decision(tmp_path):
    service, paths, wiki, directory = cross_queue(tmp_path)
    tcr.mutate_report(directory, "claim", lambda d: d["items"][0].update(decision="fix"))
    expected = cr.check_release("test", paths, wiki, tmp_path)[tcr.ENTITY]
    row = queue_rows(service)[tcr.ENTITY]
    assert expected and row["cross_review_problems"] == {"test": expected}
    assert {entry["decision"] for entry in row["cross_review"]} == {"approve", "fix"}


def test_queue_survives_invalid_yaml_report(tmp_path):
    service, _paths, _wiki, directory = cross_queue(tmp_path)
    (directory / "broken.yaml").write_text("items: [unclosed\n", encoding="utf-8")
    row = queue_rows(service)[tcr.ENTITY]
    assert len(row["cross_review"]) == 2 and "cross_review_problems" not in row


def test_queue_survives_non_mapping_confirm_json(tmp_path):
    service, _paths, _wiki, directory = cross_queue(tmp_path)
    (directory / "confirm.json").write_text("[1, 2]", encoding="utf-8")
    row = queue_rows(service)[tcr.ENTITY]
    assert {s["confirm"] for entry in row["cross_review"] for check in entry["checks"] for s in check["sources"]} == {None}
    assert row["cross_review_problems"] == {"test": ["missing or invalid confirm.json"]}


def test_queue_runs_check_release_once_per_release(tmp_path, monkeypatch):
    service, _paths, _wiki, _directory = cross_queue(tmp_path, with_wiki=True)
    calls = []
    monkeypatch.setattr(cr, "check_release", lambda *args, **kwargs: calls.append(args) or {})
    rows = queue_rows(service)
    assert tcr.ENTITY in rows and tcr.WIKI in rows and len(calls) == 1
