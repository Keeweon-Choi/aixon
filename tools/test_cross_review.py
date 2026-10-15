"""Offline regression tests for ADR-026 panel checks and gate behavior."""
import hashlib
import json
import shutil
from pathlib import Path

import pytest
import yaml

import cross_review as cr
import public_gate as pg
import review
import seedtool as st

SOURCE = {"url": "https://example.org/paper", "tier": "A", "passage": "A checked passage."}
ENTITY = "concept:algebra"
WIKI = "wiki:algebra"


def dump(path, value):
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False), encoding="utf-8")


def setup_release(tmp_path, with_wiki=False):
    graph = tmp_path / "g.yaml"
    shutil.copy(Path(__file__).parent / "fixtures" / "mini_graph.yaml", graph)
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    ids = [ENTITY]
    if with_wiki:
        page = wiki_dir / "algebra.mdx"
        page.write_text("---\nid: wiki:algebra\nentity: concept:algebra\ntitle: Algebra\nstatus: draft\nclaims: []\nsources: []\nreview: null\npublished_at: null\n---\n\nFirst paragraph.\n\nSecond paragraph.\n", encoding="utf-8")
        ids.append(WIKI)
    directory = cr.release_dir("test", tmp_path)
    directory.mkdir(parents=True)
    dump(tmp_path / "review" / "test.yaml", {"release": "test", "items": [{"id": ident, "kind": "wiki" if ident == WIKI else "entity", "publish": ident == WIKI} for ident in ids]})
    paths = [str(graph)]
    _, available = cr.records(paths, wiki_dir)
    for stem, start in (("source", "source-first"), ("claim", "claim-first")):
        dump(directory / f"{stem}.yaml", {"release": "test", "reviewer": f"agent:{stem}", "start": start,
             "items": [make_item(ident, available) for ident in ids]})
    write_confirm(directory)
    return paths, str(wiki_dir), directory


def make_item(ident, available):
    kind, record, digest = available[ident]
    return {"id": ident, "reviewed_hash": digest, "decision": "approve", "unchecked": [],
            "checks": [{"field": field, "verdict": "supported", "sources": [SOURCE.copy()]}
                       for field in cr.required_fields(kind, record)]}


def write_confirm(directory, sources=None):
    rows = sources or {f"{SOURCE['url']}\n{SOURCE['passage']}": {"status": "found"}}
    (directory / "confirm.json").write_text(json.dumps({"schema": 1, "sources": rows}), encoding="utf-8")


def mutate_report(directory, stem, fn):
    path = directory / f"{stem}.yaml"
    data = yaml.safe_load(path.read_text())
    fn(data)
    dump(path, data)


def test_check_passes_and_wiki_paragraph_is_required(tmp_path):
    paths, wiki, directory = setup_release(tmp_path, True)
    assert cr.check_release("test", paths, wiki, tmp_path) == {ENTITY: [], WIKI: []}
    mutate_report(directory, "claim", lambda d: d["items"][1]["checks"].pop())
    assert "missing required field para:2" in " ".join(cr.check_release("test", paths, wiki, tmp_path)[WIKI])


@pytest.mark.parametrize(("change", "reason"), [
    (lambda d: d["items"].clear(), "two distinct reviewers"),
    (lambda d: d.update(start="source-first"), "claim-first"),
    (lambda d: d["items"][0].update(reviewed_hash="stale"), "stale reviewed_hash"),
    (lambda d: d["items"][0]["checks"][0].update(verdict="wrong"), "failing verdict wrong"),
    (lambda d: d.update(reviewer="agent:other"), "reviewer does not match file stem"),
    (lambda d: d["items"][0].update(unchecked=["name"]), "unchecked is non-empty"),
])
def test_check_rejects_bad_reports(tmp_path, change, reason):
    paths, wiki, directory = setup_release(tmp_path)
    mutate_report(directory, "claim", change)
    assert reason in " ".join(cr.check_release("test", paths, wiki, tmp_path)[ENTITY])


def test_source_tiers_and_confirm_status(tmp_path):
    paths, wiki, directory = setup_release(tmp_path)
    change = lambda d: [check.update(sources=[{"url": "https://wikipedia.org/a", "tier": "A", "passage": "X"}]) for check in d["items"][0]["checks"]]
    for stem in ("source", "claim"):
        mutate_report(directory, stem, change)
    key = "https://wikipedia.org/a\nX"
    write_confirm(directory, {key: {"status": "not-found"}})
    assert "no found source" in " ".join(cr.check_release("test", paths, wiki, tmp_path)[ENTITY])
    write_confirm(directory, {key: {"status": "found"}})
    assert "two C hosts" in " ".join(cr.check_release("test", paths, wiki, tmp_path)[ENTITY])
    extra = {"url": "https://reddit.com/a", "tier": "C", "passage": "Y"}
    for stem in ("source", "claim"):
        mutate_report(directory, stem, lambda d: [check["sources"].append(extra) for check in d["items"][0]["checks"]])
    write_confirm(directory, {key: {"status": "found"}, "https://reddit.com/a\nY": {"status": "found"}})
    assert cr.check_release("test", paths, wiki, tmp_path)[ENTITY] == []


def test_two_c_sources_on_same_host_fail(tmp_path):
    paths, wiki, directory = setup_release(tmp_path)
    sources = [{"url": f"https://wikipedia.org/{i}", "tier": "A", "passage": str(i)} for i in (1, 2)]
    for stem in ("source", "claim"):
        mutate_report(directory, stem, lambda d: [check.update(sources=sources) for check in d["items"][0]["checks"]])
    write_confirm(directory, {f"{s['url']}\n{s['passage']}": {"status": "found"} for s in sources})
    assert "two C hosts" in " ".join(cr.check_release("test", paths, wiki, tmp_path)[ENTITY])


def test_packet_blinds_pre_review_fields(tmp_path):
    paths, wiki, directory = setup_release(tmp_path, True)
    sheet = tmp_path / "review" / "test.yaml"
    data = yaml.safe_load(sheet.read_text())
    data["items"][0].update(recommendation="fix", decision="reject", notes="secret", checked=["secret"], fix="secret")
    dump(sheet, data)
    cr.packet("test", paths, wiki, tmp_path)
    packet = (directory / "packet.yaml").read_text()
    assert "secret" not in packet and "recommendation:" not in packet and "decision:" not in packet
    assert "para:2" in packet


def test_metadata_and_evidence_need_primary_source():
    confirmed = {"https://example.org/b\nB": {"status": "found"}}
    check = {"field": "metadata", "verdict": "supported", "sources": [{"url": "https://example.org/b", "tier": "B", "passage": "B"}]}
    for field in ("metadata", "evidence[0]"):
        check["field"] = field
        assert "tier-A" in " ".join(cr.report_item_problems({"decision": "approve", "reviewed_hash": "x", "checks": [check]}, [field], "x", "claim", confirmed))


def test_confirm_statuses_and_arxiv_cache(tmp_path, monkeypatch):
    paths, wiki, directory = setup_release(tmp_path)
    report = yaml.safe_load((directory / "source.yaml").read_text())
    report["items"][0]["checks"][0]["sources"] = [
        {"url": "https://example.org/found", "tier": "A", "passage": "there"},
        {"url": "https://example.org/missing", "tier": "A", "passage": "absent"},
        {"url": "https://example.org/error", "tier": "A", "passage": "any"},
    ]
    dump(directory / "source.yaml", report)

    def fake_fetch(url, root, graph_paths):
        if url.endswith("error"):
            raise OSError("offline")
        return "there is a passage"

    real_fetch = cr.fetch_text
    monkeypatch.setattr(cr, "fetch_text", fake_fetch)
    result = cr.confirm("test", paths, tmp_path, True)["sources"]
    assert {v["status"] for v in result.values()} == {"found", "not-found", "fetch-failed"}

    full = "https://arxiv.org/html/1706.03762v7"
    raw = yaml.safe_load(Path(paths[0]).read_text())
    raw["sources"][0]["fulltext_url"] = full
    dump(Path(paths[0]), raw)
    cache = tmp_path / "data" / "cache" / "fulltext"
    cache.mkdir(parents=True)
    stem = hashlib.sha256(full.encode()).hexdigest()[:16] + (Path(full).suffix or ".bin")
    (cache / stem).write_text("A cached arxiv passage.")
    assert "cached arxiv" in real_fetch("https://arxiv.org/html/1706.03762v7", tmp_path, paths)

    def offline(*args, **kwargs):
        raise OSError("network disabled in test")

    # abs pages and other versions are not the cached full text: they go to the network
    monkeypatch.setattr(cr.urllib.request, "urlopen", offline)
    for url in ("https://arxiv.org/abs/1706.03762v7", "https://arxiv.org/html/1706.03762v1"):
        with pytest.raises(OSError):
            real_fetch(url, tmp_path, paths)


def test_sample_approve_gate_and_tampering(tmp_path, monkeypatch):
    paths, wiki, directory = setup_release(tmp_path, True)
    first = cr.sampled_ids("test", paths, wiki, tmp_path)
    assert first == cr.sampled_ids("test", paths, wiki, tmp_path)
    assert cr.approve("test", paths, wiki, tmp_path, "2026-10-15")["errors"]
    _, available = cr.records(paths, wiki)
    dump(directory / "audit.yaml", {"release": "test", "reviewer": "agent:audit", "start": "audit", "items": [make_item(i, available) for i in first]})
    mutate_report(directory, "audit", lambda d: d["items"][0].update(decision="fix"))
    assert "fix or reject" in " ".join(cr.approve("test", paths, wiki, tmp_path, "2026-10-15")["errors"])
    mutate_report(directory, "audit", lambda d: d["items"][0].update(decision="approve"))
    monkeypatch.setenv("CLAUDECODE", "1")
    outcome = cr.approve("test", paths, wiki, tmp_path, "2026-10-15")
    assert (outcome["approved"], outcome["published"], outcome["failed"]) == (2, 1, 0)
    graph = st.load_graph(paths)
    assert st.approval_state(graph["entities"][ENTITY]) == "approved"
    assert pg.wiki_approval(*pg.read_wiki(Path(wiki) / "algebra.mdx")) == "approved"
    monkeypatch.chdir(tmp_path)
    assert ENTITY in pg.gate(paths, wiki)["entities"]
    assert WIKI in pg.gate(paths, wiki)["wiki"]
    raw = yaml.safe_load(Path(paths[0]).read_text())
    raw["concepts"][0]["review"]["reviewers"] = ["agent:source", "agent:other"]
    dump(Path(paths[0]), raw)
    assert ENTITY not in pg.gate(paths, wiki)["entities"]
    raw["concepts"][0]["review"]["reviewers"] = ["agent:claim", "agent:source"]
    dump(Path(paths[0]), raw)
    assert ENTITY in pg.gate(paths, wiki)["entities"]
    mutate_report(directory, "claim", lambda d: d["items"][0].update(decision="fix"))
    assert ENTITY not in pg.gate(paths, wiki)["entities"]
    mutate_report(directory, "claim", lambda d: d["items"][0].update(decision="approve"))
    (directory / "confirm.json").unlink()
    assert ENTITY not in pg.gate(paths, wiki)["entities"]


def test_sample_changes_with_report_bytes(tmp_path):
    paths, wiki, directory = setup_release(tmp_path)
    raw = yaml.safe_load(Path(paths[0]).read_text())
    ids = [row["id"] for row in raw["concepts"] + raw["methods"]]
    sheet = tmp_path / "review" / "test.yaml"
    dump(sheet, {"release": "test", "items": [{"id": ident, "kind": "entity"} for ident in ids]})
    _, available = cr.records(paths, wiki)
    for stem in ("source", "claim"):
        mutate_report(directory, stem, lambda d: d.update(items=[make_item(i, available) for i in ids]))
    original = cr.sampled_ids("test", paths, wiki, tmp_path)
    for attempt in range(20):
        mutate_report(directory, "claim", lambda d: d.update(note=f"revision {attempt}"))
        if cr.sampled_ids("test", paths, wiki, tmp_path) != original:
            break
    assert cr.sampled_ids("test", paths, wiki, tmp_path) != original


def test_human_skip_and_agent_signature_invalid(tmp_path):
    paths, wiki, directory = setup_release(tmp_path)
    review.approve_record(paths, ENTITY, "human:tester", "ok", [], "2026-10-15")
    _, available = cr.records(paths, wiki)
    dump(directory / "audit.yaml", {"release": "test", "reviewer": "agent:audit", "start": "audit", "items": [make_item(ENTITY, available)]})
    assert cr.approve("test", paths, wiki, tmp_path, "2026-10-15")["skipped"] == 1
    record = st.load_graph(paths)["entities"][ENTITY]
    record["review"] = {"by": "agent:x", "decision": "approve", "at": "2026-10-15", "reviewed_hash": st.review_hash(record)}
    assert st.approval_state(record) == "invalid"


def test_panel_signature_and_content_freshness(tmp_path, monkeypatch):
    paths, wiki, directory = setup_release(tmp_path)
    _, available = cr.records(paths, wiki)
    dump(directory / "audit.yaml", {"release": "test", "reviewer": "agent:audit", "start": "audit", "items": [make_item(ENTITY, available)]})
    assert cr.approve("test", paths, wiki, tmp_path, "2026-10-15")["approved"] == 1
    monkeypatch.chdir(tmp_path)
    assert ENTITY in pg.gate(paths, wiki)["entities"]
    raw = yaml.safe_load(Path(paths[0]).read_text())
    raw["concepts"][0]["summary"] = "Changed after approval."
    dump(Path(paths[0]), raw)
    record = st.load_graph(paths)["entities"][ENTITY]
    assert st.approval_state(record) == "stale"
    assert {"id": ENTITY, "reason": "review stale"} in pg.gate(paths, wiki)["excluded"]


def test_panel_roster_is_per_record(tmp_path, monkeypatch):
    paths, wiki, directory = setup_release(tmp_path, True)
    _, available = cr.records(paths, wiki)
    dump(directory / "extra.yaml", {"release": "test", "reviewer": "agent:extra", "start": "source-first",
                                    "items": [make_item(ENTITY, available)]})
    sample = cr.sampled_ids("test", paths, wiki, tmp_path)
    dump(directory / "audit.yaml", {"release": "test", "reviewer": "agent:audit", "start": "audit",
                                    "items": [make_item(i, available) for i in sample]})
    assert cr.approve("test", paths, wiki, tmp_path, "2026-10-15")["approved"] == 2
    entity = st.load_graph(paths)["entities"][ENTITY]
    meta, _ = pg.read_wiki(Path(wiki) / "algebra.mdx")
    assert "agent:extra" in entity["review"]["reviewers"]
    assert "agent:extra" not in meta["review"]["reviewers"]
    monkeypatch.chdir(tmp_path)
    assert pg.gate(paths, wiki)["wiki"] == [WIKI]


@pytest.mark.parametrize("change", [
    lambda block: block.update(method="manual"),
    lambda block: block.update(reviewers=["agent:source", "agent:source"]),
    lambda block: block.update(audit="agent:source"),
    lambda block: block.update(report="review/cross/other"),
    lambda block: block.update(at=""),
])
def test_panel_signature_requires_all_fields(change):
    block = {"by": "panel:test", "method": "cross-review", "reviewers": ["agent:source", "agent:claim"],
             "audit": "agent:audit", "report": "review/cross/test", "at": "2026-10-15", "decision": "approve"}
    assert st.approval_kind(block) == "panel"
    change(block)
    assert st.approval_kind(block) is None


def test_verifier_regressions(tmp_path, monkeypatch):
    found = {"https://en.wikipedia.org/a\nP": "found", "https://de.wikipedia.org/b\nQ": {"status": "found"}}
    two_langs = {"field": "summary", "verdict": "supported", "sources": [
        {"url": "https://en.wikipedia.org/a", "tier": "C", "passage": "P"},
        {"url": "https://de.wikipedia.org/b", "tier": "C", "passage": "Q"}]}
    item = {"decision": "approve", "reviewed_hash": "h", "checks": [two_langs]}
    assert "two C hosts" in " ".join(cr.report_item_problems(item, ["summary"], "h", "entity", found))
    blank_note = {"decision": "approve", "reviewed_hash": "h", "checks": [{"field": "summary", "verdict": "computed", "note": None}]}
    assert "computed needs a note" in " ".join(cr.report_item_problems(blank_note, ["summary"], "h", "entity", {}))
    paths, wiki, directory = setup_release(tmp_path, True)
    mutate_report(directory, "source", lambda d: d["items"][0]["checks"][0].update(
        sources=[{"url": "https://example.org/x", "tier": "A", "passage": "  "}]))
    monkeypatch.setattr(cr, "fetch_text", lambda url, root, graph_paths: "page text")
    assert cr.confirm("test", paths, tmp_path, True)["sources"]["https://example.org/x\n  "]["status"] == "fetch-failed"
    review.approve_wiki(Path(wiki) / "algebra.mdx", "human:tester", "ok", "2026-10-14")
    write_confirm(directory)
    _, available = cr.records(paths, wiki)
    for stem in ("source", "claim"):
        mutate_report(directory, stem, lambda d: d.update(items=[make_item(i, available) for i in (ENTITY, WIKI)]))
    dump(directory / "audit.yaml", {"release": "test", "reviewer": "agent:audit", "start": "audit",
                                    "items": [make_item(i, available) for i in cr.sampled_ids("test", paths, wiki, tmp_path)]})
    assert cr.approve("test", paths, wiki, tmp_path, "2026-10-15")["skipped"] == 1
    assert pg.read_wiki(Path(wiki) / "algebra.mdx")[0]["review"]["by"] == "human:tester"
