"""Public gate and review tool (ADR-021): fail closed, human-only, content-bound approvals."""
import shutil
from pathlib import Path

import pytest
import yaml

import public_gate as pg
import review
import seedtool as st

HERE = Path(__file__).resolve().parent
WIKI = """---
id: wiki:softmax
entity: concept:softmax
title: Softmax
status: {status}
claims: [clm:algebra-prereq-softmax]
sources: [src:mini:notes]
review: null
published_at: null
---

Softmax body.
"""


def setup(tmp_path, status="published"):
    graph = tmp_path / "g.yaml"
    shutil.copy(HERE / "fixtures/mini_graph.yaml", graph)
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    (wiki_dir / "softmax.mdx").write_text(WIKI.format(status=status), encoding="utf-8")
    return [str(graph)], str(wiki_dir)


def approve(paths, ident):
    review.approve_record(paths, ident, "human:tester", "ok", ["support"], "2026-10-15")


def test_nothing_is_public_without_human_approval(tmp_path):
    paths, wiki = setup(tmp_path)
    out = pg.gate(paths, wiki)
    assert out["entities"] == [] and out["claims"] == [] and out["wiki"] == []
    assert out["errors"] and "review missing" in out["errors"][0]["reasons"]


def test_claim_needs_public_endpoints_then_wiki_follows(tmp_path):
    paths, wiki = setup(tmp_path)
    approve(paths, "clm:algebra-prereq-softmax")
    out = pg.gate(paths, wiki)
    assert out["claims"] == [] and any(x["reason"] == "subject or object is not public" for x in out["excluded"])
    for ident in ("concept:algebra", "concept:softmax"):
        approve(paths, ident)
    assert pg.gate(paths, wiki)["claims"] == ["clm:algebra-prereq-softmax"]
    review.approve_wiki(Path(wiki) / "softmax.mdx", "human:tester", "ok", "2026-10-15")
    out = pg.gate(paths, wiki)
    assert out["wiki"] == ["wiki:softmax"] and out["errors"] == []
    assert "src:mini:notes" in out["sources"]


def test_edit_after_approval_makes_it_stale(tmp_path):
    paths, wiki = setup(tmp_path, status="draft")
    approve(paths, "concept:softmax")
    text = Path(paths[0]).read_text(encoding="utf-8").replace("Softmax", "Softmax (edited)", 1)
    Path(paths[0]).write_text(text, encoding="utf-8")
    out = pg.gate(paths, wiki)
    assert "concept:softmax" not in out["entities"]
    assert {"id": "concept:softmax", "reason": "review stale"} in out["excluded"]
    assert "G022" in {x.code for x in st.validate(st.load_graph(paths))}


def test_agent_signature_and_proposed_status_never_publish(tmp_path):
    paths, wiki = setup(tmp_path, status="draft")
    for ident in ("concept:algebra", "concept:softmax"):
        approve(paths, ident)
    raw = yaml.safe_load(Path(paths[0]).read_text(encoding="utf-8"))
    claim = raw["claims"][0]
    claim["status"] = "proposed"
    claim["review"] = {"by": "agent:codex", "at": "2026-10-15", "decision": "approve", "reviewed_hash": "x"}
    Path(paths[0]).write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
    assert pg.gate(paths, wiki)["claims"] == []
    approve(paths, claim["id"])  # a human approval of a proposed claim is still not public
    out = pg.gate(paths, wiki)
    assert out["claims"] == [] and any("never public" in x["reason"] for x in out["excluded"])


def test_wiki_body_edit_is_stale_and_missing_graph_fails_closed(tmp_path):
    paths, wiki = setup(tmp_path)
    page = Path(wiki) / "softmax.mdx"
    review.approve_wiki(page, "human:tester", "ok", "2026-10-15")
    page.write_text(page.read_text(encoding="utf-8") + "\nAdded later.\n", encoding="utf-8")
    meta, body = pg.read_wiki(page)
    assert pg.wiki_approval(meta, body) == "stale"
    with pytest.raises(FileNotFoundError):
        pg.gate(paths + [str(tmp_path / "missing.yaml")], wiki)


def test_review_cli_refuses_inside_agent_sessions():
    assert review.agent_session({"CLAUDECODE": "1"})
    assert review.agent_session({"CODEX_SANDBOX": "seatbelt"})
    assert not review.agent_session({"HOME": "/home/x"})
