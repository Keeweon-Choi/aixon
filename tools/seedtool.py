"""Small, deterministic reference implementation for the AIXON seed graph.

`load_graph` returns the YAML under ``raw`` plus indexed ``entities``, ``types``,
``claims`` and ``sources`` mappings.  It deliberately has no runtime dependency
other than PyYAML (and optionally pypdf for quote checks).
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import html.parser
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

SECTIONS = {
    "fields": ("ResearchField", "field"), "problems": ("ResearchProblem", "problem"),
    "concepts": ("Concept", "concept"), "methods": ("Method", "method"),
    "models": ("Model", "model"), "papers": ("Paper", "paper"),
    "datasets": ("Dataset", "dataset"), "metrics": ("Metric", "metric"),
    "benchmarks": ("Benchmark", "benchmark"), "objectives": ("LearningObjective", "lo"),
    "resources": ("LearningResource", "res"), "assessment_items": ("AssessmentItem", "ai"),
    "labs": ("LabExperiment", "lab"), "sources": ("Source", "src"), "claims": ("Claim", "clm"),
}
KU = {"Concept", "Method", "Model"}
WIKI_TYPES = KU | {"ResearchField", "ResearchProblem", "Dataset", "Metric", "Benchmark"}
DIMS = ("recognize", "explain", "derive", "implement", "analyze")
RANK = {"recognize": 0, "explain": 1, "derive": 2, "implement": 2, "analyze": 2}
WEIGHT = {"mcq": 1, "numeric": 2, "short_text": 2, "lab_prediction": 1, "self_explanation": 1}
DEFAULT_MINUTES = {"recognize": 5, "explain": 20, "derive": 30, "implement": 30, "analyze": 25}
EVIDENCE_TYPES = {"bibliographic_metadata", "author_statement", "experimental_result", "analytical_result", "definitional_dependency", "third_party_statement", "curator_rationale"}
DOMAINS = {
    "CITES": ({"Paper"}, {"Paper"}), "INTRODUCES": ({"Paper"}, {"Method", "Model", "Dataset", "Benchmark", "Metric"}),
    "EXTENDS": ({"Method", "Model"}, {"Method", "Model"}), "ADAPTS": ({"Method", "Model"}, {"Method", "Model"}),
    "IMPROVES_ON": ({"Method", "Model"}, {"Method", "Model"}), "COMPARED_WITH": ({"Method", "Model"}, {"Method", "Model"}),
    "ADDRESSES": ({"Paper", "Method", "Model"}, {"ResearchProblem"}), "MITIGATES": ({"Method", "Model"}, {"ResearchProblem"}),
    "EVALUATED_ON": ({"Method", "Model"}, {"Benchmark"}), "TRAINED_ON": ({"Model"}, {"Dataset"}),
    "PREREQUISITE_OF": (KU, KU), "RECOMMENDED_BEFORE": (KU, KU), "PART_OF": (KU, KU), "IS_A": (KU, KU),
}
ID_RE = re.compile(r"^[a-z]+:[a-z0-9]+(?:-[a-z0-9]+)*$")
SRC_RE = re.compile(r"^src:[a-z0-9.:_-]+$")


@dataclass(frozen=True)
class Issue:
    code: str
    ref: str
    message: str


def _plain(value: Any) -> Any:
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_plain(v) for v in value]
    return value


def _canonical(value: Any) -> Any:
    value = _plain(value)
    if isinstance(value, dict):
        return {k: _canonical(value[k]) for k in sorted(value)}
    if isinstance(value, list):
        vals = [_canonical(v) for v in value]
        if all(isinstance(v, dict) and "id" in v for v in vals):
            return sorted(vals, key=lambda v: str(v["id"]))
        return vals
    return value


def _dump(value: Any) -> str:
    return json.dumps(_canonical(value), ensure_ascii=False, sort_keys=True, indent=2)


def _graph_paths(path_or_paths: str | Path | Iterable[str | Path]) -> list[Path]:
    """Resolve graph inputs to a stable list of YAML files."""
    if isinstance(path_or_paths, (str, Path)):
        candidates = [Path(path_or_paths)]
    else:
        candidates = [Path(path) for path in path_or_paths]
    paths: list[Path] = []
    for candidate in candidates:
        if candidate.is_dir():
            paths.extend(candidate.glob("*.yaml"))
        else:
            paths.append(candidate)
    return sorted(paths, key=lambda path: str(path.resolve()))


def load_graph(path_or_paths: str | Path | Iterable[str | Path]) -> dict:
    """Read one or more YAML graphs and build stable lookup maps.

    Directory inputs include their ``*.yaml`` children.  Inputs are sorted so
    merging and the resulting graph version do not depend on caller order.
    """
    paths = _graph_paths(path_or_paths)
    raw: dict[str, Any] = {section: [] for section in SECTIONS}
    graph_header: dict[str, Any] = {}
    assumed_background: set[str] = set()
    schema_version = None
    for path in paths:
        with open(path, encoding="utf-8") as f:
            document = _plain(yaml.safe_load(f) or {})
        if schema_version is None and "schema_version" in document:
            schema_version = document["schema_version"]
        header = document.get("graph") or {}
        for key, value in header.items():
            if key == "assumed_background":
                assumed_background.update(str(item) for item in value or [])
            else:
                graph_header.setdefault(key, value)
        for section in SECTIONS:
            raw[section].extend(document.get(section, []) or [])
    if schema_version is not None:
        raw["schema_version"] = schema_version
    if assumed_background:
        graph_header["assumed_background"] = sorted(assumed_background)
    if graph_header:
        raw["graph"] = graph_header
    entities, types, records = {}, {}, []
    for section, (typ, _prefix) in SECTIONS.items():
        for rec in raw.get(section, []) or []:
            if not isinstance(rec, dict):
                continue
            rec = _plain(rec)
            records.append((section, typ, rec))
            ident = rec.get("id")
            if ident is not None and ident not in entities:
                entities[ident], types[ident] = rec, typ
    return {"raw": raw, "entities": entities, "types": types, "records": records,
            "claims": {i: r for i, r in entities.items() if types.get(i) == "Claim"},
            "sources": {i: r for i, r in entities.items() if types.get(i) == "Source"}}


def graph_version(graph: dict) -> str:
    return hashlib.sha256(_dump(graph["raw"]).encode()).hexdigest()[:12]


def claim_content_hash(claim: dict) -> str:
    body = {k: claim.get(k, {} if k == "qualifiers" else None) for k in ("predicate", "subject", "object", "qualifiers", "status")}
    return hashlib.sha256(_dump(body).encode()).hexdigest()[:12]


HUMAN_RE = re.compile(r"^human:[a-z0-9][a-z0-9_-]*$")
SURFACE_RE = re.compile(r"[^0-9a-z\uac00-\ud7a3]+")


def review_hash(record: dict) -> str:
    """Content hash an approval is bound to: the record without its ``review`` (ADR-021)."""
    body = {k: v for k, v in record.items() if k != "review"}
    return hashlib.sha256(_dump(body).encode()).hexdigest()[:12]


def approval_state(record: dict) -> str | None:
    """None (no approval), "approved", "stale" (record changed after approval) or "invalid"."""
    review = record.get("review")
    if not isinstance(review, dict) or review.get("decision") != "approve":
        return None
    if not HUMAN_RE.match(str(review.get("by", ""))) or not review.get("at"):
        return "invalid"
    if review.get("reviewed_hash") != review_hash(record):
        return "stale"
    return "approved"


def _tokens(text: str) -> list[str]:
    return SURFACE_RE.sub(" ", unicodedata.normalize("NFKC", str(text)).lower()).split()


def surface_forms(entity: dict) -> list[list[str]]:
    """Token lists of name, aliases and key_terms used to check that a quote is about the entity (G023)."""
    forms = [entity.get("name"), entity.get("title"), *(entity.get("aliases") or []), *(entity.get("key_terms") or [])]
    return [t for t in (_tokens(x) for x in forms if x) if len("".join(t)) >= 2]


def mentions(text: str, forms: list[list[str]]) -> bool:
    """True if some form occurs as consecutive word prefixes ("patch embedding" matches "patch embeddings",
    "vit" does not match "Dosovitskiy", "어텐션" matches "어텐션을")."""
    words = _tokens(text)
    return any(all(words[i + j].startswith(f[j]) for j in range(len(f)))
               for f in forms for i in range(len(words) - len(f) + 1))


def _issue(out, code, ref, msg):
    out.append(Issue(code, str(ref), msg))


def _claim_key(c: dict):
    q = c.get("qualifiers") or {}
    return tuple(c.get(k) if k not in ("group", "for_dimension", "benchmark", "metric", "subject_variant", "object_variant") else q.get(k)
                 for k in ("predicate", "subject", "object", "group", "for_dimension", "benchmark", "metric", "subject_variant", "object_variant"))


def _implies(higher: str, lower: str) -> bool:
    return higher == lower or (higher == "explain" and lower == "recognize") or (higher in {"derive", "implement", "analyze"} and lower in {"recognize", "explain"})


def _reference_checks(g: dict, out: list[Issue]):
    e, t = g["entities"], g["types"]
    def ref(owner, target, allowed=None, label="reference"):
        if not target or target not in e or (allowed and t.get(target) not in allowed):
            _issue(out, "G003", owner, f"dangling {label}: {target}")
    for ident, rec in sorted(e.items()):
        typ = t[ident]
        for f in ("fields", "parents"):
            for x in rec.get(f, []) or []: ref(ident, x, {"ResearchField"}, f)
        for rel in rec.get("related", []) or []:
            ref(ident, rel.get("id"), None, "related")
            if not rel.get("note"):
                _issue(out, "G003", ident, "related note required")
        if typ == "Claim":
            ref(ident, rec.get("subject"), None, "subject"); ref(ident, rec.get("object"), None, "object")
            for idx, ev in enumerate(rec.get("evidence", []) or []):
                if ev.get("type") != "curator_rationale": ref(ident, ev.get("source"), {"Source"}, f"evidence[{idx}].source")
            for key, allowed in (("from_field", {"ResearchField"}), ("to_field", {"ResearchField"}), ("benchmark", {"Benchmark"}), ("metric", {"Metric"})):
                if key in (rec.get("qualifiers") or {}): ref(ident, rec["qualifiers"][key], allowed, key)
            if rec.get("supersedes"): ref(ident, rec["supersedes"], {"Claim"}, "supersedes")
        elif typ == "LearningResource":
            for x in rec.get("explains", []) or []: ref(ident, x.get("unit"), KU, "explains.unit")
        elif typ == "AssessmentItem":
            ref(ident, (rec.get("assesses") or {}).get("unit"), KU, "assesses.unit")
            if rec.get("lab"): ref(ident, rec["lab"], {"LabExperiment"}, "lab")
        elif typ == "LabExperiment":
            for x in rec.get("demonstrates", []) or []: ref(ident, x.get("unit"), KU, "demonstrates.unit")
            for x in rec.get("items", []) or []: ref(ident, x, {"AssessmentItem"}, "items")
        elif typ == "LearningObjective":
            for x in rec.get("targets", []) or []: ref(ident, x.get("unit"), KU, "targets.unit")
            if rec.get("context"): ref(ident, rec["context"], None, "context")
        elif typ == "Benchmark":
            ref(ident, rec.get("dataset"), {"Dataset"}, "dataset")
            for x in rec.get("metrics", []) or []: ref(ident, x, {"Metric"}, "metrics")
        elif typ == "Dataset" and rec.get("introduced_by"):
            ref(ident, rec["introduced_by"], {"Paper"}, "introduced_by")
        elif typ == "Source" and rec.get("paper"):
            ref(ident, rec["paper"], {"Paper"}, "paper")


def _cycle(edges: dict) -> list[str] | None:
    state, stack = {}, []
    def visit(n):
        state[n] = 1; stack.append(n)
        for x in sorted(edges.get(n, ())):
            if state.get(x) == 1: return stack[stack.index(x):] + [x]
            if state.get(x, 0) == 0:
                got = visit(x)
                if got: return got
        stack.pop(); state[n] = 2
    for n in sorted(edges):
        if state.get(n, 0) == 0:
            got = visit(n)
            if got: return got
    return None


def _valid_evidence(c: dict, g: dict) -> bool:
    supports = [x for x in c.get("evidence", []) or [] if x.get("stance") == "supports"]
    p = c.get("predicate"); q = c.get("qualifiers") or {}
    types = {x.get("type") for x in supports}
    if p == "CITES": return "bibliographic_metadata" in types
    if p == "INTRODUCES":
        return any(x.get("type") == "author_statement" and g["sources"].get(x.get("source"), {}).get("paper") == c.get("subject") for x in supports)
    if p in {"EXTENDS", "ADAPTS"}:
        evidence = [x for x in supports if x.get("type") == "author_statement"]
        intro = [x for x in g["claims"].values() if x.get("status") == "verified" and x.get("predicate") == "INTRODUCES" and x.get("object") == c.get("subject")]
        return bool(evidence) and (not intro or any(g["sources"].get(x.get("source"), {}).get("paper") in {z.get("subject") for z in intro} for x in evidence))
    if p == "ADDRESSES": return "author_statement" in types
    if p == "MITIGATES": return bool(types & {"experimental_result", "analytical_result"})
    if p == "IMPROVES_ON": return any(x.get("type") == "experimental_result" and ((x.get("locator") or {}).get("table") or (x.get("locator") or {}).get("figure")) for x in supports)
    if p == "COMPARED_WITH": return "experimental_result" in types and bool(q.get("benchmark"))
    if p in {"EVALUATED_ON", "TRAINED_ON"}:
        return bool(types & {"author_statement", "experimental_result"}) and (p != "TRAINED_ON" or q.get("stage") in {"pretraining", "training", "finetuning"})
    if p in {"PART_OF", "IS_A"}: return bool(types & {"author_statement", "definitional_dependency", "third_party_statement"})
    if p in {"PREREQUISITE_OF", "RECOMMENDED_BEFORE"}:
        return "definitional_dependency" in types or ("curator_rationale" in types and approval_state(c) == "approved")
    return False


def validate(graph: dict) -> list[Issue]:
    """Return deterministic G/W issues; no exception is raised for malformed graphs."""
    out: list[Issue] = []; e, t = graph["entities"], graph["types"]
    seen = {}
    for section, typ, rec in graph["records"]:
        ident = rec.get("id", "<missing>")
        if ident in seen: _issue(out, "G001", ident, "duplicate id")
        seen[ident] = section
        prefix = SECTIONS[section][1]
        good = bool(SRC_RE.match(str(ident))) if prefix == "src" else bool(ID_RE.match(str(ident)))
        if not good or not str(ident).startswith(prefix + ":"):
            _issue(out, "G002", ident, "id format or prefix mismatch")
    _reference_checks(graph, out)
    for cid, c in sorted(graph["claims"].items()):
        p, s, o = c.get("predicate"), c.get("subject"), c.get("object")
        if p not in DOMAINS or t.get(s) not in DOMAINS.get(p, (set(), set()))[0] or t.get(o) not in DOMAINS.get(p, (set(), set()))[1]:
            _issue(out, "G004", cid, "predicate domain/range")
    ids = {}
    for pid, p in sorted((i, r) for i, r in e.items() if t[i] == "Paper"):
        for k in ("doi", "arxiv", "arxiv_doi", "s2", "dblp", "openreview"):
            if (v := (p.get("identifiers") or {}).get(k)):
                ids.setdefault((k, str(v).lower()), []).append(pid)
        for v in (p.get("identifiers") or {}).get("openalex", []) or []: ids.setdefault(("openalex", str(v).lower()), []).append(pid)
    for key, vals in sorted(ids.items()):
        if len(set(vals)) > 1: _issue(out, "G005", ",".join(sorted(set(vals))), f"duplicate external id {key[0]}")
    active = [c for c in graph["claims"].values() if c.get("status") in {"proposed", "verified", "disputed"}]
    grouped = {}
    for c in active: grouped.setdefault(_claim_key(c), []).append(c)
    for cs in grouped.values():
        if len(cs) > 1: _issue(out, "G006", min(str(x.get("id")) for x in cs), "duplicate active claim key")
    for cid, c in sorted(graph["claims"].items()):
        evs = c.get("evidence", []) or []
        if c.get("status") == "verified":
            if not all((c.get("verification") or {}).get(k) for k in ("method", "by", "at")) or not _valid_evidence(c, graph): _issue(out, "G007", cid, "verified evidence policy")
            if any(x.get("stance") == "contradicts" for x in evs): _issue(out, "G007", cid, "verified claim should be disputed")
        if c.get("status") == "disputed" and not ({"supports", "contradicts"} <= {x.get("stance") for x in evs}): _issue(out, "G007", cid, "disputed needs support and contradiction")
        if c.get("status") == "rejected" and not c.get("rejected_reason"): _issue(out, "G007", cid, "rejected_reason required")
        for x in evs:
            et = x.get("type")
            if et not in EVIDENCE_TYPES or x.get("stance") not in {"supports", "contradicts", "qualifies"}: _issue(out, "G017", cid, "invalid evidence type or stance")
            if et == "curator_rationale":
                if not x.get("rationale"): _issue(out, "G017", cid, "curator rationale required")
            elif not x.get("source") or not isinstance(x.get("quote"), str) or not x["quote"].strip() or len(x["quote"]) > 300: _issue(out, "G017", cid, "source and short quote required")
    edges = {}
    for u, r in sorted(e.items()):
        if t[u] in KU:
            for d in r.get("dimensions", []) or []:
                if d == "explain": edges.setdefault(f"{u}@{d}", set()).add(f"{u}@recognize")
                elif d in {"derive", "implement", "analyze"}: edges.setdefault(f"{u}@{d}", set()).add(f"{u}@explain")
    for c in graph["claims"].values():
        if c.get("status") == "verified" and c.get("predicate") == "PREREQUISITE_OF":
            q = c.get("qualifiers") or {}; edges.setdefault(f"{c.get('object')}@{q.get('for_dimension', 'explain')}", set()).add(f"{c.get('subject')}@{q.get('required_dimension', 'explain')}")
    if cyc := _cycle(edges): _issue(out, "G008", " -> ".join(cyc), "prerequisite cycle")
    orgroups = {}
    for c in active:
        if c.get("predicate") == "PREREQUISITE_OF" and (q := c.get("qualifiers") or {}).get("group"):
            orgroups.setdefault((c.get("object"), q.get("for_dimension", "explain"), q["group"]), []).append(c)
    for key, cs in sorted(orgroups.items()):
        if len(cs) < 2: _issue(out, "G009", str(key), "OR group requires two members")
    used = []
    for rec in e.values():
        typ = t.get(rec.get("id"))
        if typ in KU and not {"recognize", "explain"} <= set(rec.get("dimensions") or []): _issue(out, "G010", rec.get("id"), "KU requires recognize and explain")
        if typ == "LearningObjective": used += [(x.get("unit"), x.get("dimension")) for x in rec.get("targets", []) or []]
        if typ == "AssessmentItem": used.append(((rec.get("assesses") or {}).get("unit"), (rec.get("assesses") or {}).get("dimension")))
        if typ == "LearningResource": used += [(x.get("unit"), d) for x in rec.get("explains", []) or [] for d in x.get("dimensions", []) or []]
        if typ == "LabExperiment": used += [(x.get("unit"), d) for x in rec.get("demonstrates", []) or [] for d in x.get("dimensions", []) or []]
    for c in graph["claims"].values():
        if c.get("predicate") in {"PREREQUISITE_OF", "RECOMMENDED_BEFORE"}:
            q = c.get("qualifiers") or {}; used += [(c.get("subject"), q.get("required_dimension", "explain")), (c.get("object"), q.get("for_dimension", "explain"))]
    for u, d in used:
        if d not in (e.get(u, {}).get("dimensions") or []): _issue(out, "G010", f"{u}@{d}", "undeclared dimension")
    for predicate in ("PART_OF", "IS_A"):
        x = {}
        for c in graph["claims"].values():
            if c.get("status") == "verified" and c.get("predicate") == predicate:
                x.setdefault(c["subject"], set()).add(c["object"])
        if cyc := _cycle(x): _issue(out, "G011", " -> ".join(cyc), f"{predicate} cycle")
    parents = {i: set(r.get("parents", []) or []) for i, r in e.items() if t[i] == "ResearchField"}
    if cyc := _cycle(parents): _issue(out, "G011", " -> ".join(cyc), "field parent cycle")
    comparisons = {(c.get("subject"), c.get("object"), (c.get("qualifiers") or {}).get("benchmark")): c for c in active if c.get("predicate") == "COMPARED_WITH"}
    for a, b, bm in sorted(comparisons):
        if (b, a, bm) in comparisons and a < b: _issue(out, "G012", f"{a},{b}", "bidirectional COMPARED_WITH")
    for c in active:
        q = c.get("qualifiers") or {}
        if c.get("predicate") == "ADAPTS" and (not q.get("from_field") or not q.get("to_field") or q["from_field"] == q["to_field"]): _issue(out, "G013", c.get("id"), "ADAPTS needs distinct fields")
    intro = {}
    for c in graph["claims"].values():
        if c.get("status") == "verified" and c.get("predicate") == "INTRODUCES":
            d = e.get(c.get("subject"), {}).get("earliest_public_date")
            if d: intro[c.get("object")] = min(str(d), intro.get(c.get("object"), str(d)))
    for c in active:
        if c.get("predicate") in {"EXTENDS", "ADAPTS", "IMPROVES_ON"} and c.get("subject") in intro and c.get("object") in intro and intro[c["subject"]] < intro[c["object"]] and not (c.get("qualifiers") or {}).get("concurrent"):
            _issue(out, "G014", c.get("id"), "subject predates object")
        if c.get("predicate") == "IMPROVES_ON":
            q = c.get("qualifiers") or {}; metric, bench = e.get(q.get("metric")), e.get(q.get("benchmark"))
            good = bench and metric and q.get("metric") in (bench.get("metrics") or []) and isinstance(q.get("subject_value"), (int, float)) and isinstance(q.get("object_value"), (int, float))
            if good: good = q["subject_value"] > q["object_value"] if metric.get("direction") == "higher_is_better" else q["subject_value"] < q["object_value"]
            if not good: _issue(out, "G015", c.get("id"), "invalid improvement values")
    rejected = {_claim_key(c) for c in graph["claims"].values() if c.get("status") == "rejected"}
    for c in active:
        if _claim_key(c) in rejected: _issue(out, "G016", c.get("id"), "repeats rejected claim")
    for iid, item in sorted((i, r) for i, r in e.items() if t[i] == "AssessmentItem"):
        a, kind = item.get("assesses"), item.get("kind")
        bad = not a or not item.get("prompt") or not item.get("rationale") or kind not in WEIGHT
        ans = item.get("answer")
        if kind == "mcq": bad |= not isinstance(item.get("choices"), list) or len(item["choices"]) < 2 or not isinstance(ans, int) or not 0 <= ans < len(item["choices"])
        elif kind == "numeric": bad |= not isinstance(ans, (int, float)) or not isinstance(item.get("tolerance"), (int, float)) or item.get("tolerance", -1) < 0
        elif kind == "short_text": bad |= not isinstance(ans, list) or not ans or not all(isinstance(x, str) and x for x in ans)
        elif kind == "lab_prediction":
            lab = e.get(item.get("lab")); bad |= not lab or iid not in (lab.get("items") or [])
            choice = isinstance(item.get("choices"), list) and len(item["choices"]) >= 2 and isinstance(ans, int) and 0 <= ans < len(item["choices"])
            number = isinstance(ans, (int, float)) and isinstance(item.get("tolerance"), (int, float)) and item.get("tolerance", -1) >= 0
            bad |= not (choice or number)
        elif kind == "self_explanation": bad |= not isinstance(item.get("rubric"), list) or not item["rubric"]
        if bad: _issue(out, "G018", iid, "invalid assessment item")
    # G020 required fields (docs/03 §2.2) and G021 identifier value types.
    required = {"ResearchField": ["name"], "ResearchProblem": ["name", "summary", "question"], "Concept": ["name", "summary", "dimensions"],
                "Method": ["name", "summary", "dimensions"], "Model": ["name", "summary", "dimensions"], "Paper": ["title", "authors", "earliest_public_date", "identifiers"],
                "Dataset": ["name", "summary"], "Metric": ["name", "summary", "direction"], "Benchmark": ["name", "dataset", "metrics", "split"],
                "LearningObjective": ["name", "targets"], "LearningResource": ["name", "format", "verified_at", "explains"], "LabExperiment": ["name", "component", "version", "parameters", "demonstrates", "items"],
                "Source": ["kind", "url", "retrieved_at"], "Claim": ["predicate", "subject", "object", "status", "confidence"]}
    for ident, rec in sorted(e.items()):
        for field in required.get(t[ident], []):
            if rec.get(field) in (None, "", [], {}): _issue(out, "G020", ident, f"required field missing: {field}")
        if t[ident] == "LearningResource" and not (rec.get("url") or rec.get("lab")): _issue(out, "G020", ident, "required field missing: url or lab")
        if t[ident] == "Source" and rec.get("kind") == "paper_version" and not rec.get("paper"): _issue(out, "G020", ident, "required field missing: paper")
        if t[ident] == "Paper":
            for key, val in sorted((rec.get("identifiers") or {}).items()):
                vals = val if key == "openalex" else [val]
                if key == "openalex" and not isinstance(val, list): vals = [val]
                for v in vals:
                    if not isinstance(v, str) or not v.strip(): _issue(out, "G021", ident, f"identifier {key} must be a non-empty string, got {type(v).__name__}")
    # G022 approvals must be human-signed and bound to the current content (ADR-021).
    for ident, rec in sorted(e.items()):
        state = approval_state(rec)
        if state == "invalid": _issue(out, "G022", ident, "review must be by human:<id> with a date")
        if state == "stale": _issue(out, "G022", ident, "stale review: record changed after approval (re-approve with tools/review.py)")
    # G023 definitional_dependency evidence must mention the subject concept in at least one quote (ADR-022).
    for cid, c in sorted(graph["claims"].items()):
        if c.get("status") not in {"verified", "disputed"}:
            continue
        forms = surface_forms(e.get(c.get("subject"), {}))
        quotes = [x.get("quote", "") for x in c.get("evidence", []) or []
                  if x.get("type") == "definitional_dependency" and x.get("stance") == "supports"]
        if forms and quotes and not any(mentions(q, forms) for q in quotes):
            _issue(out, "G023", cid, "definitional_dependency quotes do not mention the subject (name/aliases/key_terms)")
    # G024 slugs are unique across entities (wiki file names and URLs, ADR-023).
    slugs: dict[str, list[str]] = {}
    for ident in e:
        if t[ident] in WIKI_TYPES: slugs.setdefault(ident.split(":", 1)[1], []).append(ident)
    for slug, ids in sorted(slugs.items()):
        if len(ids) > 1: _issue(out, "G024", ",".join(sorted(ids)), f"slug {slug} used by several entities")
    # G025 links are https only (no javascript:, data:, http:).
    for ident, rec in sorted(e.items()):
        for key in ("url", "fulltext_url"):
            if rec.get(key) and not str(rec[key]).startswith("https://"): _issue(out, "G025", ident, f"{key} must be https://")
    # W107 domain entities belong to a field; W108 names collide; W109 copy-paste summaries; W110 slug-like names.
    names: dict[str, set[str]] = {}
    summaries: dict[str, list[str]] = {}
    for ident, rec in sorted(e.items()):
        if t[ident] in {"Concept", "Method", "Model", "Paper", "ResearchProblem"} and not rec.get("fields"):
            _issue(out, "W107", ident, "not in any field")
        if t[ident] in WIKI_TYPES:
            for form in [entity_name for entity_name in (rec.get("name"), *(rec.get("aliases") or [])) if entity_name]:
                names.setdefault(" ".join(_tokens(form)), set()).add(ident)
            if rec.get("summary"): summaries.setdefault(str(rec["summary"]), []).append(ident)
            name = str(rec.get("name", ""))
            if re.fullmatch(r"[a-z0-9 -]+", name) and not rec.get("aliases"):
                _issue(out, "W110", ident, f"slug-like name without aliases: {name}")
    for form, ids in sorted(names.items()):
        if len(ids) > 1: _issue(out, "W108", ",".join(sorted(ids)), f"same name or alias: {form}")
    for text, ids in sorted(summaries.items()):
        if len(ids) > 1: _issue(out, "W109", ",".join(ids), "identical summary")
    # W111 a prerequisite that only re-uses its PART_OF evidence shows composition, not necessity.
    part_quotes = {(c.get("subject"), c.get("object")): {x.get("quote") for x in c.get("evidence", []) or []}
                   for c in graph["claims"].values() if c.get("predicate") == "PART_OF"}
    for cid, c in sorted(graph["claims"].items()):
        if c.get("predicate") == "PREREQUISITE_OF" and c.get("status") == "verified":
            quotes = {x.get("quote") for x in c.get("evidence", []) or [] if x.get("stance") == "supports"}
            if quotes and quotes <= part_quotes.get((c.get("subject"), c.get("object")), set()):
                _issue(out, "W111", cid, "evidence identical to the PART_OF claim")
    # W101/W102 closure is calculated by the same deterministic prerequisite walker used by plan.
    for oid, objective in sorted((i, r) for i, r in e.items() if t[i] == "LearningObjective"):
        nodes = _closure(graph, [(x.get("unit"), x.get("dimension")) for x in objective.get("targets", []) or []], all_or=True)
        maximal = {(u, d) for u, d in nodes if not any(u == x and d != y and _implies(y, d) for x, y in nodes)}
        for u, d in sorted(maximal):
            items = _items(graph, u, d)
            if len(items) < 2: _issue(out, "W101", f"{oid}:{u}@{d}", "fewer than two assessment items")
            if not _resources(graph, u, [d]) and not _labs(graph, u, [d]): _issue(out, "W102", f"{oid}:{u}@{d}", "no resource or lab")
    proposed = sum(c.get("status") == "proposed" for c in graph["claims"].values())
    _issue(out, "W103", "claims", f"{proposed} proposed claims")
    # W104 intentionally conservatively treats any explicit reference as a use.
    referenced = set()
    def collect(x):
        if isinstance(x, str) and x in e: referenced.add(x)
        elif isinstance(x, dict):
            for v in x.values(): collect(v)
        elif isinstance(x, list):
            for v in x: collect(v)
    for rec in e.values(): collect({k: v for k, v in rec.items() if k != "id"})
    watch = {"ResearchField", "ResearchProblem", "Concept", "Method", "Model", "Paper", "Dataset", "Metric", "Benchmark"}
    for i in sorted(e):
        if t[i] in watch and i not in referenced: _issue(out, "W104", i, "unreferenced entity")
    for i in sorted(referenced):
        if e.get(i, {}).get("status") == "merged": _issue(out, "W105", i, "reference to merged entity")
    return sorted(out, key=lambda x: (x.code, x.ref, x.message))


def _items(g: dict, u: str, d: str) -> list[tuple[str, dict]]:
    return sorted(((i, r) for i, r in g["entities"].items() if g["types"].get(i) == "AssessmentItem" and (r.get("assesses") or {}).get("unit") == u and (r.get("assesses") or {}).get("dimension") == d), key=lambda x: x[0])


def _resources(g: dict, u: str, dims: list[str]) -> list[tuple[str, dict, set[str]]]:
    ans = []
    for i, r in g["entities"].items():
        if g["types"].get(i) != "LearningResource": continue
        for x in r.get("explains", []) or []:
            hit = set(x.get("dimensions", []) or []) & set(dims)
            if x.get("unit") == u and hit: ans.append((i, r, hit)); break
    return sorted(ans, key=lambda x: (-len(x[2]), x[1].get("estimated_minutes", 999), x[0]))


def _labs(g: dict, u: str, dims: list[str]) -> list[tuple[str, dict]]:
    ans = []
    for i, r in g["entities"].items():
        if g["types"].get(i) == "LabExperiment" and any(x.get("unit") == u and set(x.get("dimensions", []) or []) & set(dims) for x in r.get("demonstrates", []) or []): ans.append((i, r))
    return sorted(ans)


def _requirement_groups(g: dict, node: tuple[str, str], soft=False):
    """Return (kind, key, [(node, claim)]) in the exact planner order."""
    u, d = node; ans = []
    if not soft and d == "explain": ans.append(("and", "dimension_implication", [((u, "recognize"), None)]))
    elif not soft and d in {"derive", "implement", "analyze"}: ans.append(("and", "dimension_implication", [((u, "explain"), None)]))
    pred = "RECOMMENDED_BEFORE" if soft else "PREREQUISITE_OF"
    matches = []
    for cid, c in sorted(g["claims"].items()):
        if c.get("status") != "verified" or c.get("predicate") != pred or c.get("object") != u: continue
        q = c.get("qualifiers") or {}; fd = q.get("for_dimension", "explain")
        if d == fd: matches.append((cid, c, q))
    ands = [(cid, c, q) for cid, c, q in matches if not q.get("group")]
    for cid, c, q in sorted(ands, key=lambda z: (z[1].get("subject", ""), RANK.get(z[2].get("required_dimension", "explain"), 9), z[0])):
        ans.append(("and", cid, [((c.get("subject"), q.get("required_dimension", "explain")), cid)]))
    groups = {}
    for cid, c, q in matches:
        if q.get("group"):
            key = f"{u}@{q.get('for_dimension', 'explain')}#{q['group']}"
            groups.setdefault(key, []).append(((c.get("subject"), q.get("required_dimension", "explain")), cid))
    for key in sorted(groups): ans.append(("or", key, sorted(groups[key], key=lambda z: (z[0][0], RANK.get(z[0][1], 9), z[1]))))
    return ans


def _closure(g: dict, targets, all_or=False) -> set[tuple[str, str]]:
    seen = set()
    def visit(n):
        if n in seen: return
        seen.add(n)
        for kind, _key, vals in _requirement_groups(g, n):
            for child, _cid in vals if (all_or or kind == "and") else vals[:1]: visit(child)
    for n in targets:
        if n[0] in g["entities"]: visit(n)
    return seen


def compute_mastery(graph: dict, learner: dict) -> dict:
    """Implement mastery-v1.  Keys are `(unit, dimension)` tuples."""
    attempts = learner.get("attempts", []) or []
    grouped: dict[tuple[str, str], list[tuple[int, dict]]] = {}
    for index, a in enumerate(attempts):
        item = graph["entities"].get(a.get("item"), {})
        target = item.get("assesses") or {}
        if target.get("unit") and target.get("dimension"): grouped.setdefault((target["unit"], target["dimension"]), []).append((index, a))
    reports = {}
    for index, x in enumerate(learner.get("self_reports", []) or []):
        key = x.get("unit")
        if key and (key not in reports or (str(x.get("at", "")), index) >= reports[key][0]): reports[key] = ((str(x.get("at", "")), index), x)
    nodes = {(i, d) for i, r in graph["entities"].items() if graph["types"].get(i) in KU for d in r.get("dimensions", []) or []} | set(grouped)
    result = {}
    for u, d in sorted(nodes):
        rows = sorted(grouped.get((u, d), []), key=lambda x: (str(x[1].get("at", "")), x[0]))
        latest_by_item = {}
        ever = False
        for _idx, a in rows:
            latest_by_item[a.get("item")] = a
            positives = [x for x in latest_by_item.values() if x.get("correct") and not x.get("hinted")]
            score = sum(WEIGHT.get(graph["entities"].get(x.get("item"), {}).get("kind"), 0) for x in positives)
            last = a
            if score >= 3 and len(positives) >= 2 and last.get("correct") and not last.get("hinted"): ever = True
        positives = [x for x in latest_by_item.values() if x.get("correct") and not x.get("hinted")]
        score = sum(WEIGHT.get(graph["entities"].get(x.get("item"), {}).get("kind"), 0) for x in positives)
        last = rows[-1][1] if rows else None
        mastered = bool(last and score >= 3 and len(positives) >= 2 and last.get("correct") and not last.get("hinted"))
        report = reports.get(u, (None, {}))[1]; familiarity = report.get("familiarity", 0)
        claimed = (familiarity >= 4 or (familiarity >= 3 and d in {"recognize", "explain"})) and not any(k[0] == u for k in grouped)  # evidence on any dimension of the unit supersedes self-report (mastery-v1.1)
        state = "mastered" if mastered else "needs_review" if ever else "practicing" if rows else "claimed" if claimed else "unknown"
        confidence = "high" if mastered and score >= 4 and any(WEIGHT.get(graph["entities"].get(x.get("item"), {}).get("kind"), 0) == 2 for x in positives) else "medium" if mastered else "low" if state in {"practicing", "needs_review"} else None
        result[(u, d)] = {"state": state, "evidence_score": score, "positive_items": sorted(x.get("item") for x in positives), "confidence": confidence, "last_attempt_at": last.get("at") if last else None, "ever_mastered": ever, "self_report": familiarity if report else None}
    return result


def _latest_overrides(learner):
    out = {}
    for index, x in enumerate(learner.get("overrides", []) or []):
        key = (x.get("unit"), x.get("dimension")); rank = (str(x.get("at", "")), index)
        if key not in out or rank >= out[key][0]: out[key] = (rank, x.get("action"))
    return {k: v[1] for k, v in out.items()}


def plan(graph: dict, learner: dict, targets: list[dict], options: dict | None = None) -> dict:
    """Create a deterministic planner-v1 plan for explicit target mappings."""
    options = copy.deepcopy(options or {})
    opts = {"include_recommended": False, "diagnostics_first": True, **options}
    for target in targets:
        u, d = target.get("unit"), target.get("dimension")
        if graph["types"].get(u) not in KU or d not in (graph["entities"].get(u, {}).get("dimensions") or []): raise ValueError(f"E_TARGET: {u}@{d}")
    mastery, overrides = compute_mastery(graph, learner), _latest_overrides(learner)
    states, skipped, first_parent, choices, used = {}, {}, {}, [], set()
    choice_cache, cost_memo, costing = {}, {}, set()
    def evidence(state):
        return {"evidence_score": state.get("evidence_score", 0), "items": sorted(state.get("positive_items", [])),
                "last_attempt_at": state.get("last_attempt_at")}
    def classify(n):
        if overrides.get(n) == "skip": return "SKIP_OVERRIDE", {"reason": "override"}
        own = mastery.get(n, {"state": "unknown"})
        if own["state"] == "mastered": return "SKIP_MASTERED", {"reason": "mastered", "evidence": evidence(own)}
        u, d = n
        higher = sorted((x for x, m in mastery.items() if x[0] == u and x[1] != d and m["state"] == "mastered" and _implies(x[1], d)), key=lambda x: (RANK[x[1]], x[1]))
        if higher:
            implied = higher[0]
            return "SKIP_MASTERED", {"reason": "implied_by_higher_dimension", "implied_by": f"{implied[0]}@{implied[1]}", "evidence": evidence(mastery[implied])}
        return {"claimed": ("DIAGNOSE", {"reason": "claimed"}), "needs_review": ("REVIEW", {"reason": "needs_review"})}.get(own["state"], ("LEARN", {"reason": "learn"}))
    def minutes(n, cls=None):
        if cls == "DIAGNOSE" or cls == "REVIEW": return 5
        return graph["entities"][n[0]].get("estimated_minutes", {}).get(n[1], DEFAULT_MINUTES[n[1]])
    def cost(n):
        # ponytail: alternative closure costs double-count shared nodes across alternatives; enumerate group combinations when groups <= 10.
        if n in cost_memo: return cost_memo[n]
        if n in costing: return 0
        costing.add(n); added = set()
        def add(node):
            if node in added: return
            cls, _why = classify(node)
            if cls.startswith("SKIP"): return
            added.add(node)
            if cls != "LEARN": return
            for kind, key, vals in _requirement_groups(graph, node):
                child, _cid = vals[0] if kind == "and" else choose(key, vals)
                add(child)
        add(n)
        total = sum(minutes(node, classify(node)[0]) for node in added)
        costing.remove(n)
        cost_memo[n] = total
        return total
    def choose(key, vals):
        if key in choice_cache: return choice_cache[key]
        pref = (opts.get("prefer") or {}).get(key)
        if pref and any(x[0][0] == pref for x in vals): chosen = next(x for x in vals if x[0][0] == pref)
        else:
            satisfied = [x for x in vals if classify(x[0])[0].startswith("SKIP")]
            if satisfied: chosen = satisfied[0]
            else:
                ranked = sorted(vals, key=lambda x: (cost(x[0]), 0 if (graph["claims"][x[1]].get("qualifiers") or {}).get("preferred") else 1, x[0][0]))
                chosen = ranked[0]
        choice_cache[key] = chosen
        return chosen
    def record_choice(key, vals):
        chosen = choose(key, vals)
        choices.append({"group": key, "chosen": chosen[0][0], "alternatives": [{"unit": x[0][0], "dimension": x[0][1], "claim": x[1], "cost": cost(x[0])} for x in vals]})
        return chosen
    def visit(n, parent=None, optional=False):
        if n in states or n in skipped: return
        cls, why = classify(n)
        if cls.startswith("SKIP"):
            skipped[n] = why; return
        states[n] = {"classification": cls, "why": why, "optional": optional}; first_parent[n] = parent
        if cls == "LEARN":
            for kind, key, vals in _requirement_groups(graph, n):
                child, cid = vals[0] if kind == "and" else record_choice(key, vals)
                if cid: used.add(cid)
                visit(child, (n, cid or "dimension_implication"))
            if opts["include_recommended"]:
                for _kind, _key, vals in _requirement_groups(graph, n, soft=True):
                    for child, cid in vals[:1]:
                        used.add(cid); visit(child, (n, cid), True)
    for x in targets: visit((x["unit"], x["dimension"]))
    # Failure rule adds direct mastered requirements back as review nodes.
    failed = set()
    for n, data in list(states.items()):
        if data["classification"] != "LEARN": continue
        bad = [a for a in learner.get("attempts", []) or [] if not a.get("correct") and (graph["entities"].get(a.get("item"), {}).get("assesses") or {}).get("unit") == n[0] and (graph["entities"].get(a.get("item"), {}).get("assesses") or {}).get("dimension") == n[1]]
        if len(bad) >= 2:
            for kind, key, vals in _requirement_groups(graph, n):
                candidates = vals[:1] if kind == "and" else [choice_cache[key]]
                for child, cid in candidates:
                    if child in skipped and skipped[child]["reason"] in {"mastered", "implied_by_higher_dimension"}:
                        skipped.pop(child); states[child] = {"classification": "REVIEW", "why": {"reason": "recheck_after_failures"}, "optional": False}; first_parent[child] = (n, cid or "dimension_implication"); failed.add(child)
    order, marked = [], set()
    def dfs(n):
        if n in marked or n not in states: return
        marked.add(n)
        groups = _requirement_groups(graph, n)
        # Order pass: other units' prerequisites first, the same unit's lower dimension last, so a unit's
        # dimensions end up adjacent and merge into one step without breaking topological order (04 §4.3).
        groups = [x for x in groups if x[1] != "dimension_implication"] + [x for x in groups if x[1] == "dimension_implication"]
        for kind, _key, vals in groups:
            candidates = vals[:1] if kind == "and" else vals
            for child, cid in candidates:
                if child in states and (kind == "and" or cid in used): dfs(child)
        for _kind, _key, vals in _requirement_groups(graph, n, soft=True):
            for child, _cid in vals:
                if child in states: dfs(child)
        order.append(n)
    for x in targets: dfs((x["unit"], x["dimension"]))
    # Any defensive additions whose parent was skipped still need a stable position.
    order += [n for n in sorted(states, key=lambda x: (x[0], RANK[x[1]])) if n not in order]
    if opts.get("diagnostics_first", True): order = [n for n in order if states[n]["classification"] in {"DIAGNOSE", "REVIEW"}] + [n for n in order if states[n]["classification"] not in {"DIAGNOSE", "REVIEW"}]
    # Merge only CONSECUTIVE LEARN nodes of the same unit (04 §4.3 step 5). Moving an earlier dimension later
    # (e.g. to the unit's last occurrence) can place it after a node that requires it (regression P16).
    merged = []
    for n in order:
        cls = states[n]["classification"]
        if cls == "LEARN" and merged and merged[-1]["action"] == "learn" and merged[-1]["unit"] == n[0]:
            merged[-1]["dimension"] = n[1]; merged[-1]["covers"].append(n[1]); merged[-1]["why"] = _why_chain(n, first_parent)
            continue
        merged.append({"action": cls.lower(), "unit": n[0], "dimension": n[1], "covers": [n[1]], "why": _why_chain(n, first_parent), "optional": states[n]["optional"]})
    steps = []
    for idx, step in enumerate(merged, 1):
        u, covers = step["unit"], step["covers"]
        if step["action"] in {"diagnose", "review"}:
            candidates = sorted(_items(graph, u, step["dimension"]), key=lambda x: (-WEIGHT.get(x[1].get("kind"), 0), x[0])); selected=[]; score=0
            for iid, item in candidates:
                selected.append(iid); score += WEIGHT.get(item.get("kind"), 0)
                if len(selected) >= 2 and score >= 3: break
        else: selected = [iid for d in covers for iid, _item in _items(graph, u, d)]
        resources = [x[0] for x in _resources(graph, u, covers)[:2]]; labs = _labs(graph, u, covers)
        final = {"id": f"s{idx}", **step, "items": selected, "resources": resources, "lab": labs[0][0] if labs else None,
                 "estimated_minutes": 5 if step["action"] in {"diagnose", "review"} else sum(minutes((u, d)) for d in covers)}
        if not final["optional"]: final.pop("optional")
        steps.append(final)
    warnings = []
    present_units = {n[0] for n in states}
    for cid, c in sorted(graph["claims"].items()):
        if c.get("predicate") in {"PREREQUISITE_OF", "RECOMMENDED_BEFORE"} and c.get("status") in {"proposed", "disputed"} and c.get("object") in present_units: warnings.append({"code": "excluded_claim", "claim": cid, "status": c["status"]})
    for s in steps:
        if len(_items(graph, s["unit"], s["dimension"])) < 2: warnings.append({"code": "unassessable", "ref": f"{s['unit']}@{s['dimension']}"})
    for s in steps:
        if s["action"] == "learn" and not s["resources"] and not s["lab"]: warnings.append({"code": "no_resource", "ref": f"{s['unit']}@{s['dimension']}"})
    for n, data in sorted(skipped.items()):
        if data["reason"] == "override": warnings.append({"code": "overridden", "ref": f"{n[0]}@{n[1]}"})
    if background := (graph["raw"].get("graph") or {}).get("assumed_background"):
        warnings.append({"code": "assumed_background", "ref": "graph", "items": background})
    warnings.sort(key=lambda x: (x["code"], x.get("ref", x.get("claim", ""))))
    skipped_out = [{"unit": n[0], "dimension": n[1], **v} for n, v in sorted(skipped.items(), key=lambda x: (x[0][0], RANK.get(x[0][1], 9)))]
    node_states = {f"{u}@{d}": x["classification"] for (u, d), x in sorted(states.items())}
    inputs = {"algorithm_version": "planner-v1", "graph_version": graph_version(graph), "targets": targets, "options": options, "node_states": node_states}
    output = {"algorithm_version": "planner-v1", "graph_version": graph_version(graph), "targets": targets,
              "inputs_hash": hashlib.sha256(_dump(inputs).encode()).hexdigest()[:16], "steps": steps, "skipped": skipped_out,
              "choices": choices, "warnings": warnings, "used_claims": [[cid, claim_content_hash(graph["claims"][cid])] for cid in sorted(used)],
              "total_estimated_minutes": sum(x["estimated_minutes"] for x in steps)}
    budget = opts.get("time_budget_minutes", opts.get("time_budget"))
    if budget:
        session = 1; running = 0
        for s in steps:
            if running and running + s["estimated_minutes"] > budget: session += 1; running = 0
            s["session"] = session; running += s["estimated_minutes"]
    return output


def _why_chain(n, parents):
    chain = []
    while parents.get(n):
        parent, via = parents[n]; chain.append({"from": f"{n[0]}@{n[1]}", "to": f"{parent[0]}@{parent[1]}", "via": via}); n = parent
    return chain


class _TextHTML(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.parts = []; self.hidden = 0
    def handle_starttag(self, tag, attrs):
        if tag.lower() in {"script", "style", "annotation", "annotation-xml"}: self.hidden += 1
        self.parts.append(" ")
    def handle_endtag(self, tag):
        if tag.lower() in {"script", "style", "annotation", "annotation-xml"} and self.hidden: self.hidden -= 1
        self.parts.append(" ")
    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)


def _normal(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = text.translate(str.maketrans({"‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "―": "-", "−": "-", "‘": "'", "’": "'", "‚": "'", "‛": "'", "“": '"', "”": '"', "„": '"', "‟": '"'}))
    return re.sub(r"\s+", "", text).lower()


def _read_text(data: bytes, url: str, content_type: str):
    suffix = Path(urllib.request.url2pathname(urllib.parse.urlparse(url).path)).suffix.lower()
    if "pdf" in content_type.lower() or suffix == ".pdf":
        try:
            import pypdf  # optional by contract
        except ImportError:
            return None, "no_pdf_support"
        import io
        return " ".join(p.extract_text() or "" for p in pypdf.PdfReader(io.BytesIO(data)).pages), None
    parser = _TextHTML(); parser.feed(data.decode("utf-8", "replace")); return "".join(parser.parts), None


def check_quotes(graph: dict, cache_dir: str | Path | None = None, offline=False, read_digests: dict[str, str] | None = None) -> list[dict]:
    cache = Path(cache_dir or "data/cache/fulltext"); rows = []
    for cid, claim in sorted(graph["claims"].items()):
        for index, ev in enumerate(claim.get("evidence", []) or []):
            quote, sid = ev.get("quote"), ev.get("source")
            if not quote: continue
            source = graph["sources"].get(sid, {}); url = source.get("fulltext_url")
            base = {"claim": cid, "evidence_index": index, "source": sid}
            if not url:
                rows.append({**base, "status": "no_fulltext_url", "detail": "source has no fulltext_url"}); continue
            suffix = Path(urllib.parse.urlparse(url).path).suffix or ".bin"; stem = hashlib.sha256(url.encode()).hexdigest()[:16] + suffix
            path, meta = cache / stem, cache / (stem + ".meta.json")
            try:
                if path.exists(): data = path.read_bytes(); content_type = json.loads(meta.read_text(encoding="utf-8")).get("content_type", "") if meta.exists() else ""
                elif offline: rows.append({**base, "status": "no_text", "detail": "cache miss"}); continue
                else:
                    req = urllib.request.Request(url, headers={"User-Agent": "aixon-seedtool/0.1"})
                    with urllib.request.urlopen(req, timeout=30) as response: data, content_type = response.read(), response.headers.get_content_type()
                    cache.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
                    meta.write_text(json.dumps({"url": url, "fetched_at": dt.datetime.now(dt.UTC).isoformat(), "sha256": hashlib.sha256(data).hexdigest(), "content_type": content_type}, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
            except Exception as exc:  # noqa: BLE001 - reported per evidence row as fetch_error
                rows.append({**base, "status": "fetch_error", "detail": str(exc)}); continue
            digest = hashlib.sha256(data).hexdigest()
            if read_digests is not None:
                read_digests[sid] = digest
            if source.get("content_sha256") and source["content_sha256"] != digest:
                rows.append({**base, "status": "source_changed", "detail": f"expected {source['content_sha256']}, got {digest}"})
            text, error = _read_text(data, url, content_type)
            if error: rows.append({**base, "status": error, "detail": error}); continue
            joined = re.sub(r"-\s*\n\s*", "", text); kept = re.sub(r"\s*\n\s*", "", text)
            found = _normal(quote) in _normal(joined) or _normal(quote) in _normal(kept)
            rows.append({**base, "status": "found" if found else "not_found", "detail": "matched" if found else "quote not found"})
    return rows


def _read_learner(path):
    with open(path, encoding="utf-8") as f: return _plain(yaml.safe_load(f) or {})


def main(argv=None):
    parser = argparse.ArgumentParser(prog="seedtool.py"); sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("validate"); p.add_argument("graph", nargs="+"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("quotes"); p.add_argument("graph", nargs="+"); p.add_argument("--cache"); p.add_argument("--offline", action="store_true"); p.add_argument("--pin", action="store_true")
    p = sub.add_parser("mastery"); p.add_argument("graph", nargs="+"); p.add_argument("--learner", required=True)
    p = sub.add_parser("plan"); p.add_argument("graph", nargs="+"); p.add_argument("--objective", required=True); p.add_argument("--learner", required=True); p.add_argument("--include-recommended", action="store_true"); p.add_argument("--no-diagnostics-first", action="store_true"); p.add_argument("--prefer", action="append", default=[]); p.add_argument("--time-budget", type=int)
    args = parser.parse_args(argv); graph = load_graph(args.graph)
    if args.command == "validate":
        issues = validate(graph); payload = [x.__dict__ for x in issues]
        print(_dump(payload) if args.json else "\n".join(f"{x.code} {x.ref}: {x.message}" for x in issues))
        return 1 if any(x.code.startswith("G") for x in issues) else 0
    if args.command == "quotes":
        read_digests: dict[str, str] = {}
        rows = check_quotes(graph, args.cache, args.offline, read_digests)
        if args.pin:
            # Pin only sources whose every quote was found: a changed source must be reviewed, not re-pinned.
            unverified = {row["source"] for row in rows if row["status"] != "found"}
            if unverified:
                print(f"not pinned (quotes not all found): {', '.join(sorted(unverified))}", file=sys.stderr)
            read_digests = {source: digest for source, digest in read_digests.items() if source not in unverified}
            try:
                from tools.yamlrec import edit_file, set_field
            except ModuleNotFoundError:
                from yamlrec import edit_file, set_field

            pending = set(read_digests)
            for path in _graph_paths(args.graph):
                document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                ids = {source.get("id") for source in document.get("sources", []) or [] if isinstance(source, dict)}
                updates = {source: digest for source, digest in read_digests.items() if source in ids}
                if updates:
                    def pin(lines, updates=updates):
                        for source, digest in updates.items():
                            lines = set_field(lines, source, "content_sha256", digest)
                        return lines
                    edit_file(str(path), pin)
                    pending.difference_update(updates)
            if pending:
                raise ValueError(f"sources not found in graph files: {', '.join(sorted(pending))}")
        print(_dump(rows)); return 1 if any(x["status"] != "found" for x in rows) else 0
    learner = _read_learner(args.learner)
    if args.command == "mastery":
        payload = {f"{u}@{d}": x for (u, d), x in compute_mastery(graph, learner).items()}; print(_dump(payload)); return 0
    obj = graph["entities"].get(args.objective)
    if graph["types"].get(args.objective) != "LearningObjective": raise ValueError(f"E_TARGET: {args.objective}")
    prefer = dict(x.split("=", 1) for x in args.prefer)
    result = plan(graph, learner, obj.get("targets", []), {"include_recommended": args.include_recommended, "diagnostics_first": not args.no_diagnostics_first, "prefer": prefer, "time_budget_minutes": args.time_budget})
    result["objective"] = args.objective; print(_dump(result)); return 0


if __name__ == "__main__":
    sys.exit(main())
