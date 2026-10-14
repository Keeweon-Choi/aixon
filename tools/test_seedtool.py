"""Focused T/M/P and quote scenarios for seedtool."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from tools.seedtool import (
    check_quotes,
    compute_mastery,
    graph_version,
    load_graph,
    plan,
    validate,
)

HERE = Path(__file__).parent


def load(tmp_path, raw, name="graph"):
    path = tmp_path / f"{name}.yaml"
    path.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    return load_graph(path)


def mini(tmp_path, mutate=None, name="mini"):
    raw = yaml.safe_load((HERE / "fixtures/mini_graph.yaml").read_text())
    if mutate: mutate(raw)
    return load(tmp_path, raw, name), raw


def cs(g): return {x.code for x in validate(g)}
def gs(g): return {x.code for x in validate(g) if x.code.startswith("G")}  # exact G set: catches false positives (02 §9 "해당 코드만")


def claim(ident, predicate, subject, obj, status="verified", **q):
    evidence = [{"source": "src:test:notes", "type": "definitional_dependency", "stance": "supports", "quote": f"Definition evidence for {subject.split(':')[-1]}."}]
    if status == "disputed": evidence.append({"source": "src:test:notes", "type": "definitional_dependency", "stance": "contradicts", "quote": "Contrary evidence."})
    out = {"id": ident, "predicate": predicate, "subject": subject, "object": obj, "qualifiers": q, "status": status, "confidence": "high", "evidence": evidence}
    if status == "verified": out["verification"] = {"method": "review", "by": "t", "at": "2026-01-01"}
    if status == "rejected": out["rejected_reason"] = "rejected"
    return out


def pg(tmp_path, units, rels=(), items=None, minutes=None, name="plan"):
    """rels are (subject, object, for_dimension, required_dimension, group, status, predicate)."""
    items, minutes = items or {}, minutes or {}
    raw = {"schema_version": 1, "graph": {"id": "test"}, "concepts": [], "resources": [], "assessment_items": [], "claims": [],
           "sources": [{"id": "src:test:notes", "name": "n", "kind": "web_page", "url": "https://example.invalid", "retrieved_at": "2026-01-01"}]}
    for u, dims in units.items():
        rec = {"id": f"concept:{u}", "name": u, "summary": u, "dimensions": dims}
        em = {d: v for (unit, d), v in minutes.items() if unit == u}
        if em: rec["estimated_minutes"] = em
        raw["concepts"].append(rec)
        raw["resources"].append({"id": f"res:{u}", "name": u, "url": "https://example.invalid", "format": "text", "verified_at": "2026-01-01", "explains": [{"unit": f"concept:{u}", "dimensions": dims}]})
        for d in dims:
            for n in range(1, items.get((u, d), 2) + 1):
                raw["assessment_items"].append({"id": iid(u, d, n), "name": f"{u}{d}{n}", "assesses": {"unit": f"concept:{u}", "dimension": d}, "kind": "numeric", "prompt": "1+1", "answer": 2, "tolerance": 0, "rationale": "r"})
    for n, (s, o, fd, rd, group, status, pred) in enumerate(rels, 1):
        q = {"for_dimension": fd, "required_dimension": rd}
        if group: q["group"] = group
        raw["claims"].append(claim(f"clm:relation-{n}", pred, f"concept:{s}", f"concept:{o}", status, **q))
    return load(tmp_path, raw, name), raw


def iid(u, d, n): return f"ai:{u}-{d}-{n:02d}"
def att(item, correct=True, hinted=False, at="2026-01-01"): return {"item": item, "correct": correct, "hinted": hinted, "at": at}
def mastered(u, d="explain"): return [att(iid(u, d, 1)), att(iid(u, d, 2), at="2026-01-02")]


# 02_DOMAIN_ONTOLOGY.md §9.1
# exact set: dangling object -> also no type (G004) and no declared dimension (G010)
def test_t1(tmp_path):
    _, r = mini(tmp_path); r["claims"].append(claim("clm:t1", "PREREQUISITE_OF", "concept:algebra", "method:nope", for_dimension="explain", required_dimension="explain")); assert gs(load(tmp_path, r, "t1")) == {"G003", "G004", "G010"}


# exact set: a verified INTRODUCES from a concept also fails the INTRODUCES evidence policy (G007)
def test_t2(tmp_path):
    _, r = mini(tmp_path); r["claims"].append(claim("clm:t2", "INTRODUCES", "concept:softmax", "method:attention")); assert gs(load(tmp_path, r, "t2")) == {"G004", "G007"}


def test_t3(tmp_path):
    _, r = mini(tmp_path); r["papers"] = [{"id": f"paper:{x}", "title": x, "authors": [x], "earliest_public_date": "2020-01-01", "identifiers": {"arxiv": "same"}} for x in "ab"]; assert gs(load(tmp_path, r, "t3")) == {"G005"}


def test_t4(tmp_path):
    _, r = mini(tmp_path); r["methods"].append({"id": "method:other", "name": "o", "summary": "o", "dimensions": ["recognize", "explain"]}); x = claim("clm:t4", "EXTENDS", "method:attention", "method:other"); x["evidence"] = []; r["claims"].append(x); assert gs(load(tmp_path, r, "t4")) == {"G007"}


def test_t5(tmp_path):
    _, r = mini(tmp_path); r["claims"].append(claim("clm:t5", "PREREQUISITE_OF", "concept:softmax", "concept:algebra", for_dimension="explain", required_dimension="explain")); assert gs(load(tmp_path, r, "t5")) == {"G008"}


def test_t6(tmp_path):
    g, _ = pg(tmp_path, {"a": ["recognize", "explain", "derive"], "b": ["recognize", "explain"]}, [("b", "a", "derive", "explain", None, "verified", "PREREQUISITE_OF"), ("a", "b", "explain", "derive", None, "verified", "PREREQUISITE_OF")], name="t6"); assert gs(g) == {"G008"}


def test_t7(tmp_path):
    g, _ = pg(tmp_path, {"a": ["recognize", "explain", "analyze"], "b": ["recognize", "explain"]}, [("b", "a", "analyze", "explain", None, "verified", "PREREQUISITE_OF"), ("a", "b", "explain", "recognize", None, "verified", "PREREQUISITE_OF")], name="t7"); assert not [x for x in validate(g) if x.code.startswith("G")]


def test_t8(tmp_path):
    _, r = mini(tmp_path); r["claims"].append(claim("clm:t8", "PREREQUISITE_OF", "concept:algebra", "method:attention", for_dimension="explain", required_dimension="explain", group="only")); assert gs(load(tmp_path, r, "t8")) == {"G009"}


def test_t9(tmp_path):
    _, r = mini(tmp_path); r["methods"].append({"id": "method:class-token", "name": "ct", "summary": "ct", "dimensions": ["recognize", "explain"]}); r["assessment_items"].append({"id": "ai:ct", "name": "ct", "assesses": {"unit": "method:class-token", "dimension": "derive"}, "kind": "numeric", "prompt": "x", "answer": 1, "tolerance": 0, "rationale": "x"}); assert gs(load(tmp_path, r, "t9")) == {"G010"}


# exact set: benchmark:no is dangling on purpose (G003); COMPARED_WITH needs experimental evidence (G007)
def test_t10(tmp_path):
    _, r = mini(tmp_path); r["methods"].append({"id": "method:other", "name": "o", "summary": "o", "dimensions": ["recognize", "explain"]}); r["claims"] += [claim("clm:ab", "COMPARED_WITH", "method:attention", "method:other", benchmark="benchmark:no"), claim("clm:ba", "COMPARED_WITH", "method:other", "method:attention", benchmark="benchmark:no")]; assert gs(load(tmp_path, r, "t10")) == {"G003", "G007", "G012"}


# exact set: field:x is dangling on purpose (G003); ADAPTS needs an author statement (G007)
def test_t11(tmp_path):
    _, r = mini(tmp_path); r["methods"].append({"id": "method:other", "name": "o", "summary": "o", "dimensions": ["recognize", "explain"]}); r["claims"].append(claim("clm:t11", "ADAPTS", "method:attention", "method:other", from_field="field:x", to_field="field:x")); assert gs(load(tmp_path, r, "t11")) == {"G003", "G007", "G013"}


# exact set: minimal papers have no identifiers (G020); EXTENDS needs an author statement (G007)
def test_t12(tmp_path):
    _, r = mini(tmp_path); r["methods"].append({"id": "method:other", "name": "o", "summary": "o", "dimensions": ["recognize", "explain"]}); r["papers"] = [{"id": "paper:old", "title": "o", "authors": ["o"], "earliest_public_date": "2017-01-01"}, {"id": "paper:new", "title": "n", "authors": ["n"], "earliest_public_date": "2020-01-01"}]; r["claims"] += [claim("clm:io", "INTRODUCES", "paper:old", "method:attention"), claim("clm:in", "INTRODUCES", "paper:new", "method:other"), claim("clm:t12", "EXTENDS", "method:attention", "method:other")]; assert gs(load(tmp_path, r, "t12")) == {"G007", "G014", "G020"}


def test_t13(tmp_path):
    _, r = mini(tmp_path); r["methods"].append({"id": "method:other", "name": "o", "summary": "o", "dimensions": ["recognize", "explain"]}); r["datasets"] = [{"id": "dataset:dx", "name": "dx", "summary": "x"}]; r["metrics"] = [{"id": "metric:mx", "name": "mx", "summary": "x", "direction": "lower_is_better"}]; r["benchmarks"] = [{"id": "benchmark:bx", "name": "bx", "summary": "x", "dataset": "dataset:dx", "metrics": ["metric:mx"], "split": "test"}]; x = claim("clm:t13", "IMPROVES_ON", "method:attention", "method:other", benchmark="benchmark:bx", metric="metric:mx", subject_value=4, object_value=2); x["evidence"] = [{"source": "src:mini:notes", "type": "experimental_result", "stance": "supports", "quote": "Table.", "locator": {"table": "1"}}]; r["claims"].append(x); assert gs(load(tmp_path, r, "t13")) == {"G015"}


# exact set: the re-proposed copy also duplicates the original active claim key (G006)
def test_t14(tmp_path):
    _, r = mini(tmp_path); rejected, active = copy.deepcopy(r["claims"][0]), copy.deepcopy(r["claims"][0]); rejected.update({"id": "clm:rejected", "status": "rejected", "rejected_reason": "no"}); active.update({"id": "clm:active", "status": "proposed"}); r["claims"] += [rejected, active]; assert gs(load(tmp_path, r, "t14")) == {"G006", "G016"}


def test_t15(tmp_path):
    _, r = mini(tmp_path); r["assessment_items"][0].pop("tolerance"); assert gs(load(tmp_path, r, "t15")) == {"G018"}


def test_t16(tmp_path):
    """CITES is bibliography, not influence: a citation between the papers that introduce two units must not
    make one a prerequisite of the other or create a research relation (02 O2, V-CITES-NOT-INFLUENCE)."""
    g, raw = pg(tmp_path, {"a": ["recognize", "explain"], "b": ["recognize", "explain"]}, name="t16")
    raw["papers"] = [{"id": f"paper:p{x}", "title": x, "authors": [x], "earliest_public_date": "2020-01-01", "identifiers": {"arxiv": f"2001.0000{i}"}} for i, x in enumerate("ab")]
    cites = claim("clm:cites", "CITES", "paper:pa", "paper:pb")
    cites["evidence"] = [{"source": "src:test:notes", "type": "bibliographic_metadata", "stance": "supports", "quote": "Reference list."}]
    raw["claims"].append(cites)
    for x in "ab":  # each paper introduces one unit, so "a's paper cites b's paper" is the tempting (wrong) inference
        raw["claims"].append(claim(f"clm:intro-{x}", "INTRODUCES", f"paper:p{x}", f"concept:{x}"))
    g = load(tmp_path, raw, "t16b")
    out = plan(g, {}, [{"unit": "concept:a", "dimension": "explain"}])
    assert [s["unit"] for s in out["steps"]] == ["concept:a"]
    assert {c["predicate"] for c in g["claims"].values()} == {"CITES", "INTRODUCES"}


def test_t17(tmp_path):
    g, _ = pg(tmp_path, {"a": ["recognize", "explain"], "b": ["recognize", "explain"]}, [("b", "a", "explain", "explain", None, "disputed", "PREREQUISITE_OF")], name="t17"); out = plan(g, {}, [{"unit": "concept:a", "dimension": "explain"}]); assert [x["unit"] for x in out["steps"]] == ["concept:a"] and any(x["code"] == "excluded_claim" for x in out["warnings"])


# 04_LEARNING_ENGINE.md §8.1
def test_m1(tmp_path):
    g, _ = mini(tmp_path); s = compute_mastery(g, {"attempts": [att("ai:softmax-01")]})[("concept:softmax", "explain")]; assert (s["state"], s["evidence_score"]) == ("practicing", 1)


def test_m2(tmp_path):
    g, _ = mini(tmp_path); s = compute_mastery(g, {"attempts": [att("ai:softmax-01"), att("ai:softmax-02", at="2026-01-02")]})[("concept:softmax", "explain")]; assert (s["state"], s["evidence_score"], s["confidence"]) == ("mastered", 3, "medium")


def test_m3(tmp_path):
    g, _ = mini(tmp_path); s = compute_mastery(g, {"attempts": [att("ai:algebra-01"), att("ai:algebra-02", at="2026-01-02")]})[("concept:algebra", "explain")]; assert (s["state"], s["evidence_score"], s["confidence"]) == ("mastered", 4, "high")


def test_m4(tmp_path):
    g, _ = mini(tmp_path); s = compute_mastery(g, {"attempts": [att("ai:algebra-01", hinted=True), att("ai:algebra-02", hinted=True, at="2026-01-02")]})[("concept:algebra", "explain")]; assert (s["state"], s["evidence_score"]) == ("practicing", 0)


def test_m5(tmp_path):
    g, _ = mini(tmp_path); a = [att("ai:algebra-01"), att("ai:algebra-02", at="2")]; assert compute_mastery(g, {"attempts": a})[("concept:algebra", "explain")]["state"] == "mastered"; a.append(att("ai:algebra-01", False, at="3")); assert compute_mastery(g, {"attempts": a})[("concept:algebra", "explain")]["state"] == "needs_review"; a.append(att("ai:algebra-01", at="4")); assert compute_mastery(g, {"attempts": a})[("concept:algebra", "explain")]["state"] == "mastered"


def test_m6(tmp_path):
    g, _ = mini(tmp_path); assert compute_mastery(g, {"self_reports": [{"unit": "concept:softmax", "familiarity": 3, "at": "1"}]})[("concept:softmax", "explain")]["state"] == "claimed"


def test_m7(tmp_path):
    g, _ = mini(tmp_path); a = [att("ai:algebra-01", at=str(n)) for n in range(1, 4)] + [att("ai:algebra-02", at="4"), att("ai:softmax-01", at="5"), att("ai:softmax-02", at="6")]; final = compute_mastery(g, {"attempts": a}); [assert_same_prefix(g, a[:n]) for n in range(1, 7)]; assert final == compute_mastery(g, {"attempts": list(a)})


def assert_same_prefix(g, attempts): assert compute_mastery(g, {"attempts": attempts}) == compute_mastery(g, {"attempts": list(attempts)})


def test_m8(tmp_path):
    g, _ = mini(tmp_path); assert compute_mastery(g, {"self_reports": [{"unit": "concept:softmax", "familiarity": 2, "at": "1"}], "lab_events": [{"lab": "x"}]})[("concept:softmax", "explain")]["state"] == "unknown"


def test_m9(tmp_path):
    g, _ = mini(tmp_path); learner = {"attempts": [att("ai:softmax-01"), att("ai:softmax-02", at="2026-01-02")]}; assert compute_mastery(g, learner)[("concept:softmax", "recognize")]["state"] == "unknown"; skip = plan(g, learner, [{"unit": "concept:softmax", "dimension": "recognize"}])["skipped"][0]; assert skip == {"unit": "concept:softmax", "dimension": "recognize", "reason": "implied_by_higher_dimension", "implied_by": "concept:softmax@explain", "evidence": {"evidence_score": 3, "items": ["ai:softmax-01", "ai:softmax-02"], "last_attempt_at": "2026-01-02"}}


# 04_LEARNING_ENGINE.md §8.2
def test_p1(tmp_path):
    g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abc"}, [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("c", "b", "explain", "explain", None, "verified", "PREREQUISITE_OF")], name="p1"); assert [x["unit"] for x in plan(g, {}, [{"unit": "concept:a", "dimension": "explain"}])["steps"]] == ["concept:c", "concept:b", "concept:a"]


def test_p2(tmp_path):
    g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abc"}, [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("c", "b", "explain", "explain", None, "verified", "PREREQUISITE_OF")], name="p2"); out = plan(g, {"attempts": mastered("b")}, [{"unit": "concept:a", "dimension": "explain"}]); assert [x["unit"] for x in out["steps"]] == ["concept:a"] and out["skipped"][0]["evidence"]["items"] == [iid("b", "explain", 1), iid("b", "explain", 2)]


def test_p3(tmp_path):
    r = [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("c", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("d", "b", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("d", "c", "explain", "explain", None, "verified", "PREREQUISITE_OF")]; g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abcd"}, r, name="p3"); assert [x["unit"] for x in plan(g, {}, [{"unit": "concept:a", "dimension": "explain"}])["steps"]] == ["concept:d", "concept:b", "concept:c", "concept:a"]


def test_p4(tmp_path):
    r = [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("c", "b", "explain", "explain", None, "verified", "PREREQUISITE_OF")]; g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abc"}, r, name="p4"); out = plan(g, {"self_reports": [{"unit": "concept:b", "familiarity": 3, "at": "1"}]}, [{"unit": "concept:a", "dimension": "explain"}]); assert [(x["action"], x["unit"]) for x in out["steps"]] == [("diagnose", "concept:b"), ("learn", "concept:a")]


def test_p5(tmp_path):
    r = [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("c", "b", "explain", "explain", None, "verified", "PREREQUISITE_OF")]; g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abc"}, r, name="p5"); out = plan(g, {"attempts": [att(iid("b", "explain", 1), False), att(iid("b", "explain", 2), at="2")]}, [{"unit": "concept:a", "dimension": "explain"}]); assert [(x["action"], x["unit"]) for x in out["steps"]] == [("learn", "concept:c"), ("learn", "concept:b"), ("learn", "concept:a")]


def test_p6(tmp_path):
    r = [("b", "a", "recognize", "recognize", "route", "verified", "PREREQUISITE_OF"), ("c", "a", "recognize", "recognize", "route", "verified", "PREREQUISITE_OF")]; g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abc"}, r, minutes={("b", "recognize"): 20, ("c", "recognize"): 50}, name="p6"); target = [{"unit": "concept:a", "dimension": "recognize"}]; base = plan(g, {}, target); assert base["choices"] == [{"group": "concept:a@recognize#route", "chosen": "concept:b", "alternatives": [{"unit": "concept:b", "dimension": "recognize", "claim": "clm:relation-1", "cost": 20}, {"unit": "concept:c", "dimension": "recognize", "claim": "clm:relation-2", "cost": 50}]}]; assert plan(g, {"attempts": mastered("b", "recognize")}, target)["choices"][0]["alternatives"][0]["cost"] == 0; assert plan(g, {}, target, {"prefer": {"concept:a@recognize#route": "concept:c"}})["choices"][0]["chosen"] == "concept:c"


def test_p7(tmp_path):
    u = {x: ["recognize", "explain"] for x in ("softmax", "temperature", "variance")}; u["sdpa"] = ["recognize", "explain", "derive"]; r = [("softmax", "sdpa", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("temperature", "sdpa", "derive", "explain", None, "verified", "PREREQUISITE_OF"), ("variance", "sdpa", "derive", "explain", None, "verified", "PREREQUISITE_OF")]; g, _ = pg(tmp_path, u, r, name="p7"); e = plan(g, {}, [{"unit": "concept:sdpa", "dimension": "explain"}]); d = plan(g, {}, [{"unit": "concept:sdpa", "dimension": "derive"}]); assert {x["unit"] for x in e["steps"]} == {"concept:softmax", "concept:sdpa"} and {x["unit"] for x in d["steps"]} >= {"concept:softmax", "concept:temperature", "concept:variance", "concept:sdpa"}


def test_p8(tmp_path):
    r = [("x", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("y", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("x", "y", "explain", "explain", None, "verified", "RECOMMENDED_BEFORE")]; g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "axy"}, r, name="p8"); units = [x["unit"] for x in plan(g, {}, [{"unit": "concept:a", "dimension": "explain"}], {"include_recommended": True})["steps"]]; assert units.index("concept:x") < units.index("concept:y"); cyc, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "xy"}, [("y", "x", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("x", "y", "explain", "explain", None, "verified", "RECOMMENDED_BEFORE")], name="p8cyc"); assert [x["unit"] for x in plan(cyc, {}, [{"unit": "concept:x", "dimension": "explain"}], {"include_recommended": True})["steps"]] == ["concept:y", "concept:x"]


def test_p9(tmp_path):
    r = [("b", "a", "explain", "explain", None, "proposed", "PREREQUISITE_OF"), ("c", "a", "explain", "explain", None, "disputed", "PREREQUISITE_OF")]; g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abc"}, r, name="p9"); out = plan(g, {}, [{"unit": "concept:a", "dimension": "explain"}]); assert [x["unit"] for x in out["steps"]] == ["concept:a"] and {(x["claim"], x["status"]) for x in out["warnings"] if x["code"] == "excluded_claim"} == {("clm:relation-1", "proposed"), ("clm:relation-2", "disputed")}


def test_p10(tmp_path):
    g, raw = pg(tmp_path, {x: ["recognize", "explain"] for x in "abc"}, [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("c", "b", "explain", "explain", None, "verified", "PREREQUISITE_OF")], name="p10"); shuffled = copy.deepcopy(raw); [shuffled[k].reverse() for k in ("concepts", "resources", "assessment_items", "claims")]; g2 = load(tmp_path, shuffled, "p10s"); target = [{"unit": "concept:a", "dimension": "explain"}]; assert graph_version(g) == graph_version(g2) and json.dumps(plan(g, {}, target), sort_keys=True) == json.dumps(plan(g2, {}, target), sort_keys=True)


def test_p11(tmp_path):
    g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "ab"}, [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF")], name="p11"); out = plan(g, {"overrides": [{"unit": "concept:b", "dimension": "explain", "action": "skip", "at": "1"}]}, [{"unit": "concept:a", "dimension": "explain"}]); assert out["skipped"] == [{"unit": "concept:b", "dimension": "explain", "reason": "override"}] and any(x["code"] == "overridden" for x in out["warnings"])


def test_p12(tmp_path):
    g, _ = pg(tmp_path, {"a": ["recognize", "explain"]}, name="p12");
    with pytest.raises(ValueError, match="E_TARGET"): plan(g, {}, [{"unit": "concept:nope", "dimension": "explain"}])
    with pytest.raises(ValueError, match="E_TARGET"): plan(g, {}, [{"unit": "concept:a", "dimension": "derive"}])


def test_p13(tmp_path):
    g, _ = pg(tmp_path, {"merge": ["recognize", "explain"], "bare": ["recognize", "explain"]}, items={("merge", "recognize"): 0, ("merge", "explain"): 2, ("bare", "recognize"): 0, ("bare", "explain"): 0}, name="p13"); refs = {x["ref"] for x in plan(g, {}, [{"unit": "concept:merge", "dimension": "explain"}, {"unit": "concept:bare", "dimension": "explain"}])["warnings"] if x["code"] == "unassessable"}; assert "concept:merge@explain" not in refs and "concept:bare@explain" in refs


def test_p14(tmp_path):
    r = [("b", "a", "explain", "explain", None, "verified", "PREREQUISITE_OF"), ("c", "a", "explain", "explain", "route", "verified", "PREREQUISITE_OF"), ("d", "a", "explain", "explain", "route", "verified", "PREREQUISITE_OF")]; g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abcd"}, r, minutes={("c", "explain"): 10, ("d", "explain"): 50}, name="p14"); learner = {"attempts": mastered("b") + mastered("c") + [att(iid("a", "explain", 1), False, at="3"), att(iid("a", "explain", 1), False, at="4")]}; out = plan(g, learner, [{"unit": "concept:a", "dimension": "explain"}]); reviews = [x for x in out["steps"] if x["action"] == "review"]; assert {x["unit"] for x in reviews} == {"concept:b", "concept:c"} and all(x["why"][0]["via"] in {"clm:relation-1", "clm:relation-2"} for x in reviews)


def test_requirement_groups_match_exact_dimension_once(tmp_path):
    r = [("b", "a", "explain", "explain", "route", "verified", "PREREQUISITE_OF"), ("c", "a", "explain", "explain", "route", "verified", "PREREQUISITE_OF")]
    g, _ = pg(tmp_path, {"a": ["recognize", "explain", "derive"], "b": ["recognize", "explain"], "c": ["recognize", "explain"]}, r, name="exact")
    out = plan(g, {}, [{"unit": "concept:a", "dimension": "derive"}])
    assert [x["group"] for x in out["choices"]] == ["concept:a@explain#route"]


def test_or_cost_counts_shared_descendant_once(tmp_path):
    r = [("b", "a", "recognize", "recognize", "route", "verified", "PREREQUISITE_OF"), ("c", "a", "recognize", "recognize", "route", "verified", "PREREQUISITE_OF"), ("d", "b", "recognize", "recognize", None, "verified", "PREREQUISITE_OF"), ("e", "b", "recognize", "recognize", None, "verified", "PREREQUISITE_OF"), ("f", "d", "recognize", "recognize", None, "verified", "PREREQUISITE_OF"), ("f", "e", "recognize", "recognize", None, "verified", "PREREQUISITE_OF")]
    g, _ = pg(tmp_path, {x: ["recognize", "explain"] for x in "abcdef"}, r, minutes={("b", "recognize"): 10, ("c", "recognize"): 50, ("d", "recognize"): 3, ("e", "recognize"): 4, ("f", "recognize"): 7}, name="cost-set")
    assert plan(g, {}, [{"unit": "concept:a", "dimension": "recognize"}])["choices"][0]["alternatives"][0]["cost"] == 24


def test_assumed_background_warning_includes_items(tmp_path):
    _g, raw = pg(tmp_path, {"a": ["recognize", "explain"]}, name="background")
    raw["graph"]["assumed_background"] = ["algebra", "logs"]
    warning = next(x for x in plan(load(tmp_path, raw, "background-items"), {}, [{"unit": "concept:a", "dimension": "explain"}])["warnings"] if x["code"] == "assumed_background")
    assert warning == {"code": "assumed_background", "ref": "graph", "items": ["algebra", "logs"]}


def test_load_graph_merges_two_files_and_headers(tmp_path):
    first = {"schema_version": 1, "graph": {"id": "first", "name": "First", "assumed_background": ["algebra"]},
             "fields": [{"id": "field:one", "name": "One", "summary": "첫 번째 분야이다."}]}
    second = {"schema_version": 1, "graph": {"id": "second", "name": "Second", "assumed_background": ["calculus", "algebra"]},
              "concepts": [{"id": "concept:two", "name": "Two", "summary": "두 번째 개념이다.", "dimensions": ["recognize", "explain"], "fields": ["field:one"]}]}
    a, b = tmp_path / "a.yaml", tmp_path / "b.yaml"
    a.write_text(yaml.safe_dump(first, sort_keys=False), encoding="utf-8")
    b.write_text(yaml.safe_dump(second, sort_keys=False), encoding="utf-8")
    graph = load_graph([b, a])
    assert not [issue for issue in validate(graph) if issue.code.startswith("G")]
    assert graph["raw"]["graph"] == {"id": "first", "name": "First", "assumed_background": ["algebra", "calculus"]}


def test_load_graph_duplicate_id_across_files_is_g001(tmp_path):
    for name in ("a", "b"):
        (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump({"schema_version": 1, "concepts": [{"id": "concept:duplicate", "name": "Duplicate", "summary": "중복 개념이다.", "dimensions": ["recognize", "explain"]}]}), encoding="utf-8")
    assert "G001" in cs(load_graph([tmp_path / "a.yaml", tmp_path / "b.yaml"]))


def test_load_graph_file_order_does_not_change_graph_version(tmp_path):
    for name, ident in (("a", "concept:alpha"), ("b", "concept:beta")):
        (tmp_path / f"{name}.yaml").write_text(yaml.safe_dump({"schema_version": 1, "graph": {"id": "merged"}, "concepts": [{"id": ident, "name": ident, "summary": "개념이다.", "dimensions": ["recognize", "explain"]}]}), encoding="utf-8")
    a, b = tmp_path / "a.yaml", tmp_path / "b.yaml"
    assert graph_version(load_graph([a, b])) == graph_version(load_graph([b, a]))


def qgraph(tmp_path, text, quote, digest=None, name="q"):
    html = tmp_path / f"{name}.html"; html.write_text(text)
    _, raw = mini(tmp_path, name=f"{name}0"); raw["claims"] = [raw["claims"][0]]; raw["sources"][0]["fulltext_url"] = html.as_uri(); raw["claims"][0]["evidence"][0]["quote"] = quote
    if digest: raw["sources"][0]["content_sha256"] = digest
    return load(tmp_path, raw, f"{name}1")


def test_quote_found(tmp_path): assert check_quotes(qgraph(tmp_path, "<p>Exact source text.</p>", "Exact source text."), tmp_path / "cache")[0]["status"] == "found"
def test_quote_not_found(tmp_path): assert check_quotes(qgraph(tmp_path, "<p>Source text.</p>", "Absent text."), tmp_path / "cache")[0]["status"] == "not_found"
def test_quote_ligature_curly_soft_hyphen(tmp_path): assert check_quotes(qgraph(tmp_path, "<p>The ﬁeld’s co\u00adoperate.</p>", "The field's cooperate."), tmp_path / "cache")[0]["status"] == "found"
def test_quote_hyphenated_line_breaks(tmp_path):
    assert check_quotes(qgraph(tmp_path, "<p>hyphen-\nated</p>", "hyphenated", name="joined"), tmp_path / "cache")[0]["status"] == "found"
    assert check_quotes(qgraph(tmp_path, "<p>data-\nefficient</p>", "data-efficient", name="kept"), tmp_path / "cache")[0]["status"] == "found"
def test_quote_citation_marker_inside_inline_tags(tmp_path): assert check_quotes(qgraph(tmp_path, '<p>We employ a residual connection <cite>[<a href="#b11">11</a>]</cite> around each; co<span>operate</span>.</p>', "We employ a residual connection [11] around each; cooperate."), tmp_path / "cache")[0]["status"] == "found"
def test_quote_offline_cache_miss(tmp_path): assert check_quotes(qgraph(tmp_path, "<p>Unused.</p>", "Unused."), tmp_path / "empty", offline=True)[0]["status"] == "no_text"
def test_quote_source_changed_and_quote_result(tmp_path): assert [x["status"] for x in check_quotes(qgraph(tmp_path, "<p>Still here.</p>", "Still here.", "0" * 64), tmp_path / "cache")] == ["source_changed", "found"]


def test_t18_p15_seed_if_present():
    root = HERE.parent; seed, learner, expected = root / "data/seed/seed_graph.yaml", root / "data/seed/learner_e2e.yaml", root / "data/seed/expected_plan_e2e.json"
    if not seed.exists(): pytest.skip("seed graph not present")
    g = load_graph([seed, root / "data/graph/atlas.yaml"]); assert not [x for x in validate(g) if x.code.startswith("G")]
    if not (learner.exists() and expected.exists()): pytest.skip("e2e fixtures not present")
    # graph_version/inputs_hash are content hashes of the graph file: any edit (e.g. a summary) changes them
    # without changing the plan, so the golden comparison covers everything else.
    volatile = {"graph_version", "inputs_hash", "objective"}  # objective: added by the CLI, not by plan()
    actual = plan(g, yaml.safe_load(learner.read_text()), g["entities"]["lo:vit-attention-math"]["targets"])
    golden = json.loads(expected.read_text())
    assert {k: v for k, v in actual.items() if k not in volatile} == {k: v for k, v in golden.items() if k not in volatile}


def _assert_topological(graph, out):
    """Every step's hard requirements that are in the plan must appear in an earlier step (or the same merged step)."""
    from tools.seedtool import _requirement_groups
    pos = {}
    for idx, step in enumerate(out["steps"]):
        for d in step["covers"]:
            pos[(step["unit"], d)] = idx
    for idx, step in enumerate(out["steps"]):
        for d in step["covers"]:
            for kind, _key, vals in _requirement_groups(graph, (step["unit"], d)):
                for child, _cid in vals:
                    if child in pos:
                        assert pos[child] <= idx, f"{step['unit']}@{d} (step {idx}) before its prerequisite {child} (step {pos[child]})"


def test_p16_no_merge_across_dependent_step(tmp_path):
    # xray@explain requires alpha@explain; alpha@derive additionally requires charlie@explain.
    # DFS order: alpha@R, alpha@E, xray@R, xray@E, charlie@R, charlie@E, alpha@D.
    # alpha's explain and derive steps are not consecutive, so they must stay separate (04 §4.3 step 5).
    g, _ = pg(tmp_path, {"alpha": ["recognize", "explain", "derive"], "xray": ["recognize", "explain"], "charlie": ["recognize", "explain"]},
              rels=[("alpha", "xray", "explain", "explain", None, "verified", "PREREQUISITE_OF"),
                    ("charlie", "alpha", "derive", "explain", None, "verified", "PREREQUISITE_OF")], name="p16")
    out = plan(g, {}, [{"unit": "concept:xray", "dimension": "explain"}, {"unit": "concept:alpha", "dimension": "derive"}])
    assert [s["unit"] for s in out["steps"]].count("concept:alpha") == 2, out["steps"]
    _assert_topological(g, out)


def test_seed_plan_is_topological_for_every_objective():
    root = HERE.parent
    seed = root / "data/seed/seed_graph.yaml"
    if not seed.exists(): pytest.skip("seed graph not present")
    graph = load_graph(seed)
    for oid, rec in graph["entities"].items():
        if graph["types"].get(oid) == "LearningObjective":
            _assert_topological(graph, plan(graph, {}, rec["targets"]))


def test_p15b_seed_replanning_sequence():
    """Hand-derived replanning sequence for lo:vit-attention-math (docs/04 §9 steps 5–9)."""
    root = HERE.parent
    seed, learner_path = root / "data/seed/seed_graph.yaml", root / "data/seed/learner_e2e.yaml"
    if not (seed.exists() and learner_path.exists()): pytest.skip("seed fixtures not present")
    graph = load_graph([seed, root / "data/graph/atlas.yaml"]); learner = yaml.safe_load(learner_path.read_text()); targets = graph["entities"]["lo:vit-attention-math"]["targets"]
    def skel(lr): return [(s["action"], s["unit"].split(":")[1], tuple(s["covers"])) for s in plan(graph, lr, targets)["steps"]]
    def att(item, ok, minute): return {"item": item, "correct": ok, "hinted": False, "at": f"2026-10-15T10:{minute:02d}:00Z"}
    E = ("recognize", "explain")
    assert skel(learner)[0] == ("diagnose", "softmax", ("explain",))
    # 6: the diagnostic reveals a gap (numeric item wrong) -> softmax is learned, no diagnose step remains
    learner["attempts"] += [att("ai:softmax-01", False, 1), att("ai:softmax-02", True, 2)]
    # softmax-temperature is no longer a prerequisite of sdpa@derive (proposed after audit F-03), so it is not planned.
    # sdpa@derive is visited first (implication-last, P16): its derive prerequisite variance-of-sum comes before
    # softmax, the prerequisite of the implied sdpa@explain.
    assert skel(learner) == [("learn", "variance-of-sum", E), ("learn", "softmax", E),
                             ("learn", "scaled-dot-product-attention", ("recognize", "explain", "derive")), ("learn", "multi-head-attention", E)]
    # 7–8: softmax and temperature (incl. the lab prediction items) are demonstrated -> they drop out
    learner["attempts"] += [att("ai:softmax-01", True, 3), att("ai:softmax-temperature-01", True, 4), att("ai:lab-softmax-temp-01", True, 5), att("ai:lab-softmax-temp-02", True, 6)]
    assert skel(learner) == [("learn", "variance-of-sum", E), ("learn", "scaled-dot-product-attention", ("recognize", "explain", "derive")), ("learn", "multi-head-attention", E)]
    # moving a lab slider or reading is not evidence: the plan is unchanged without attempts (no event types exist for it)
    # 9: the rest is demonstrated -> nothing left; sdpa@explain is implied by sdpa@derive mastery
    learner["attempts"] += [att("ai:variance-of-sum-01", True, 7), att("ai:variance-of-sum-02", True, 8), att("ai:sdpa-derive-02", True, 9), att("ai:sdpa-derive-01", True, 10),
                            att("ai:mha-01", True, 11), att("ai:mha-02", True, 12)]
    out = plan(graph, learner, targets)
    assert out["steps"] == []
    assert {(s["unit"].split(":")[1], s["dimension"], s["reason"]) for s in out["skipped"]} >= {("scaled-dot-product-attention", "derive", "mastered"), ("multi-head-attention", "explain", "mastered")}


def test_g020_required_fields_and_g021_identifier_types(tmp_path):
    def change(raw):
        raw.setdefault("papers", []).append({"id": "paper:float2016-id", "title": "t", "authors": ["a"], "earliest_public_date": "2016-11-01", "identifiers": {"arxiv": 1611.0353}})
        raw.setdefault("problems", []).append({"id": "problem:no-question", "name": "p", "summary": "s"})
    issues = validate(mini(tmp_path, change)[0])
    assert any(x.code == "G021" and x.ref == "paper:float2016-id" for x in issues)
    assert any(x.code == "G020" and x.ref == "problem:no-question" and "question" in x.message for x in issues)


def test_g022_approval_must_be_human_and_fresh(tmp_path):
    """ADR-021: an approval counts only if signed by human:* and bound to the current content hash (audit F-01, F-06)."""
    from seedtool import approval_state, review_hash
    _, r = mini(tmp_path)
    c = r["claims"][0]
    c["review"] = {"by": "agent:codex", "at": "2026-10-15", "decision": "approve", "reviewed_hash": review_hash(c)}
    assert approval_state(c) == "invalid"
    assert "G022" in gs(load(tmp_path, r, "g22a"))
    c["review"] = {"by": "human:keeweon", "at": "2026-10-15", "decision": "approve", "reviewed_hash": "000000000000"}
    assert approval_state(c) == "stale"
    c["review"]["reviewed_hash"] = review_hash(c)
    assert approval_state(c) == "approved"
    assert "G022" not in gs(load(tmp_path, r, "g22b"))
    c["evidence"][0]["quote"] = "Changed after approval."
    assert approval_state(c) == "stale"


def test_g023_definitional_quote_must_mention_subject(tmp_path):
    """ADR-022: definitional_dependency evidence of a verified claim must name the subject (word-prefix match)."""
    from seedtool import mentions, surface_forms
    assert not mentions("proposed by Dosovitskiy et al.", surface_forms({"name": "Vision Transformer", "aliases": ["ViT"]}))
    assert mentions("as the patch embeddings.", surface_forms({"name": "패치 임베딩", "aliases": ["patch embedding"]}))
    _, r = mini(tmp_path)
    c = claim("clm:g23", "PREREQUISITE_OF", "concept:softmax", "method:attention", for_dimension="explain", required_dimension="explain")
    c["evidence"][0]["quote"] = "The model computes weights."
    r["claims"].append(c)
    assert "G023" in gs(load(tmp_path, r, "g23a"))
    c["status"] = "proposed"
    assert "G023" not in gs(load(tmp_path, r, "g23b"))


def test_g024_g025_and_quality_warnings(tmp_path):
    _, r = mini(tmp_path)
    r.setdefault("datasets", []).append({"id": "dataset:softmax", "name": "softmax data", "summary": "Shared summary."})
    r["datasets"].append({"id": "dataset:other", "name": "vit data hunger", "summary": "Shared summary."})
    r["sources"][0]["url"] = "javascript:alert(1)"
    codes = cs(load(tmp_path, r, "g24"))
    assert {"G024", "G025", "W109", "W110"} <= codes


def test_t18_warning_snapshot():
    """T18: the warning profile of the real graph is pinned; a change must be deliberate (update the snapshot)."""
    root = HERE.parent
    g = load_graph([root / "data/seed/seed_graph.yaml", root / "data/graph/atlas.yaml"])
    counts = {}
    for x in validate(g):
        counts[x.code] = counts.get(x.code, 0) + 1
    snapshot = json.loads((root / "data/seed/validate_snapshot.json").read_text())
    assert counts == snapshot, f"warning profile changed: {counts} != {snapshot} (update data/seed/validate_snapshot.json if intended)"
