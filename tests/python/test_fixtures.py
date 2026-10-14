"""The fixtures are the ground truth of the E2E suite: check they are what the tests assume."""

from __future__ import annotations

import json
import re

import yaml
from conftest import BAD_WIKI, FIXTURE_GRAPH, FIXTURE_WIKI, FIXTURES

MARKER = "# TEST FIXTURE — not real research data"
LAB_ITEMS = ["ai:lab-softmax-temp-01", "ai:lab-softmax-temp-02", "ai:lab-sdpa-01", "ai:lab-sdpa-02"]
INFLUENCE_PREDICATES = {"EXTENDS", "ADAPTS", "IMPROVES_ON"}


def load_graph():
    """Return the fixture graph as a dict."""
    return yaml.safe_load(FIXTURE_GRAPH.read_text(encoding="utf8"))


def frontmatter(path):
    """Return the parsed frontmatter of an MDX fixture."""
    text = path.read_text(encoding="utf8")
    return yaml.safe_load(re.match(r"\A---\n(.*?)\n---", text, re.S).group(1))


def test_every_fixture_file_carries_the_marker():
    files = [path for path in FIXTURES.rglob("*") if path.is_file()]
    assert files, "no fixture files found"
    for path in files:
        head = path.read_text(encoding="utf8").splitlines()[:2]
        assert MARKER in head, f"{path.relative_to(FIXTURES)} lacks the fixture marker"


def test_fixture_graph_has_no_graph_errors(run_tool):
    result = run_tool("seedtool.py", "validate", "--json", FIXTURE_GRAPH)
    issues = json.loads(result.stdout)
    assert result.returncode == 0, result.stdout
    assert [issue for issue in issues if issue["code"].startswith("G")] == []


def test_fixture_graph_structure():
    graph = load_graph()
    assert graph["graph"]["id"] == "fixture-site"
    fields = {field["id"]: field for field in graph["fields"]}
    top = [ident for ident, field in fields.items() if not field["parents"]]
    assert len(top) >= 2
    for ident in top:
        assert any(ident in field["parents"] for field in fields.values()), f"{ident} has no subfield"
    assert {"field:computer-vision", "field:natural-language-processing"} <= set(top)
    units = {item["id"] for section in ("concepts", "methods", "models") for item in graph[section]}
    assert {
        "method:scaled-dot-product-attention",
        "concept:softmax",
        "concept:softmax-temperature",
        "concept:variance-of-sum",
        "concept:dot-product",
        "method:multi-head-attention",
        "model:transformer",
        "model:vit",
    } <= units
    assert len(graph["papers"]) == 3
    assert {source["paper"] for source in graph["sources"]} == {paper["id"] for paper in graph["papers"]}
    assert all("(fixture)" in paper["title"] for paper in graph["papers"])


def test_fixture_claims_cover_every_status_and_review_case():
    claims = {claim["id"]: claim for claim in load_graph()["claims"]}
    predicates = {(claim["predicate"], claim["status"]) for claim in claims.values()}
    assert {("INTRODUCES", "verified"), ("ADAPTS", "verified"), ("PART_OF", "verified")} <= predicates
    assert ("PREREQUISITE_OF", "verified") in predicates
    adapts = claims["clm:vit-adapts-transformer"]
    assert (adapts["subject"], adapts["object"], adapts["status"]) == ("model:vit", "model:transformer", "verified")
    by_status = {}
    for claim in claims.values():
        by_status.setdefault(claim["status"], []).append(claim["id"])
    assert len(by_status["disputed"]) == 1
    assert len(by_status["proposed"]) == 1
    assert len(by_status["rejected"]) == 1
    stances = {item["stance"] for item in claims[by_status["disputed"][0]]["evidence"]}
    assert {"supports", "contradicts"} <= stances
    human_approved = [
        ident
        for ident, claim in claims.items()
        if (claim.get("review") or {}).get("by") == "human:fixture-editor"
    ]
    assert human_approved == ["clm:intro-transformer"]
    review = claims["clm:intro-transformer"]["review"]
    assert (review["decision"], review["note"]) == ("approve", "fixture")
    agent_approved = [
        ident
        for ident, claim in claims.items()
        if str((claim.get("review") or {}).get("by", "")).startswith("agent:")
    ]
    assert agent_approved == ["clm:intro-vit"], "the agent self-approval trap must exist exactly once"


def test_fixture_has_a_cites_only_paper_pair():
    graph = load_graph()
    claims = graph["claims"]
    introduced = {}
    for claim in claims:
        if claim["predicate"] == "INTRODUCES" and claim["status"] == "verified":
            introduced.setdefault(claim["subject"], set()).add(claim["object"])
    cites = [claim for claim in claims if claim["predicate"] == "CITES"]
    assert len(cites) == 1
    citing, cited = introduced[cites[0]["subject"]], introduced[cites[0]["object"]]
    active_influence = [
        claim
        for claim in claims
        if claim["predicate"] in INFLUENCE_PREDICATES
        and claim["status"] != "rejected"
        and (claim["subject"] in citing and claim["object"] in cited)
    ]
    assert active_influence == [], "a CITES-only pair must not have an influence claim"


def test_fixture_lab_matches_the_seed_contract():
    graph = load_graph()
    lab = next(item for item in graph["labs"] if item["id"] == "lab:softmax-temperature")
    assert lab["items"] == LAB_ITEMS
    items = {item["id"]: item for item in graph["assessment_items"]}
    assert list(items) == LAB_ITEMS
    assert all(item["kind"] == "lab_prediction" and item["lab"] == lab["id"] for item in items.values())


def test_sdpa_wiki_fixture_uses_every_component():
    path = FIXTURE_WIKI / "scaled-dot-product-attention.mdx"
    text = path.read_text(encoding="utf8")
    meta = frontmatter(path)
    assert (meta["status"], meta["ai_generated"]) == ("draft", True)
    for needle in (
        "<Section ",
        "<Level of=",
        '<ConceptLink id="concept:softmax"',
        "<Cite src=",
        "<Cite claim=",
        "<Callout ",
        "<Figure id=",
        "<svg ",
        '<Lab id="lab:softmax-temperature" />',
        "$$",
        "픽스처어텐션",
    ):
        assert needle in text, f"missing {needle!r}"
    assert re.search(r"[^$]\$[^$\n]+\$[^$]", text), "no inline math"
    assert len(re.findall(r"^```python verify$", text, re.M)) == 2
    assert re.search(r"^```python$", text, re.M), "no plain code block"


def test_transformer_wiki_fixture_is_published_with_human_review():
    meta = frontmatter(FIXTURE_WIKI / "transformer.mdx")
    assert meta["status"] == "published"
    assert meta["review"]["by"] == "human:fixture-editor"
    assert meta["review"]["decision"] == "approve"
    assert meta["published_at"] is not None


def test_bad_fixtures_are_named_after_their_rule():
    names = sorted(path.name for path in BAD_WIKI.glob("*.mdx"))
    assert names
    assert all(re.fullmatch(r"v-[a-z0-9]+(-[a-z0-9]+)+\.mdx", name) for name in names)
