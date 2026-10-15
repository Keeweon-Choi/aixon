#!/usr/bin/env python3
"""Decide what a public build may show (ADR-021) and write the allow-list the Astro build reads.

Public = explicitly human-approved records whose content has not changed since approval:
  entity  -> its own `review` is approved (covers name, aliases, summary, fields, question, metadata)
  claim   -> approved, status verified|disputed, and both endpoints public
  wiki    -> status published, approved, its entity public, and every claim it cites public
  source  -> cited by a public claim or a public wiki document
A published wiki document that fails the gate is an error (exit 1), so the problem shows up at review
time instead of after a deploy (audit F-07).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seedtool as st  # noqa: E402

DEFAULT_GRAPH = "data/seed/seed_graph.yaml,data/graph/atlas.yaml"
PUBLIC_CLAIM_STATUS = {"verified", "disputed"}
ENTITY_TYPES = {typ for typ, _ in st.SECTIONS.values()} - {"Claim", "Source"}  # same set the site loader gates
FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_wiki(path: Path) -> tuple[dict, str]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        return {}, ""
    return st._plain(yaml.safe_load(match.group(1)) or {}), match.group(2)


def wiki_hash(meta: dict, body: str) -> str:
    """Hash a wiki approval is bound to: frontmatter without review/status/published_at, plus the body."""
    core = {k: v for k, v in meta.items() if k not in ("review", "status", "published_at")}
    return hashlib.sha256((st._dump(core) + "\n" + body).encode()).hexdigest()[:12]


def wiki_approval(meta: dict, body: str) -> str | None:
    review = meta.get("review")
    if not isinstance(review, dict) or review.get("decision") != "approve":
        return None
    if st.approval_kind(review) is None:
        return "invalid"
    return "approved" if review.get("reviewed_hash") == wiki_hash(meta, body) else "stale"


def graph_paths(spec: str | None) -> list[str]:
    return [p.strip() for p in (spec or os.environ.get("AIXON_GRAPH") or DEFAULT_GRAPH).split(",") if p.strip()]


def gate(paths: list[str], wiki_dir: str) -> dict:
    missing = [p for p in paths if not Path(p).exists()]
    if missing:
        raise FileNotFoundError(f"graph files missing: {missing}")  # fail closed (audit F-01)
    g = st.load_graph(paths)
    e, t = g["entities"], g["types"]
    excluded: list[dict] = []

    panel_cache: dict[str, tuple[dict, list[str], set[str], str | None]] = {}

    def panel_problem(ident: str, record: dict) -> str | None:
        signature = record.get("review") or {}
        if st.approval_kind(signature) != "panel":
            return None
        release = signature["by"].split(":", 1)[1]
        if release not in panel_cache:
            # Import here to avoid a module cycle: cross_review uses wiki_hash and read_wiki.
            import cross_review as cr

            root = Path(paths[0]).resolve().parent if Path(paths[0]).is_absolute() else Path.cwd()
            if not (root / "review" / "cross" / release).exists():
                root = Path.cwd()
            try:
                checks = cr.check_release(release, paths, wiki_dir, root)
                audit_errors, _, auditor = cr.audit_problems(release, paths, wiki_dir, root)
                panel_reports = cr.reports(cr.release_dir(release, root))
                reviewers = {r.get("reviewer") for r in panel_reports.values()
                             if r.get("start") in ("source-first", "claim-first")}
                panel_cache[release] = (checks, audit_errors, reviewers, auditor)
            except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
                panel_cache[release] = ({}, [f"release verification failed: {exc}"], set(), None)
        checks, audit_errors, reviewers, auditor = panel_cache[release]
        if checks.get(ident):
            return checks[ident][0]
        if ident not in checks:
            return "record is absent from release worksheet"
        if audit_errors:
            return audit_errors[0]
        if set(signature.get("reviewers", [])) != reviewers or signature.get("audit") != auditor:
            return "reviewers or audit do not match reports"
        return None

    entities = set()
    for ident, rec in sorted(e.items()):
        if t[ident] not in ENTITY_TYPES or rec.get("status") in {"merged", "deprecated"}:
            continue
        state = st.approval_state(rec)
        problem = panel_problem(ident, rec) if state == "approved" else None
        if state == "approved" and problem is None:
            entities.add(ident)
        elif problem:
            excluded.append({"id": ident, "reason": f"panel: {problem}"})
        elif state:
            excluded.append({"id": ident, "reason": f"review {state}"})

    claims = set()
    for cid, c in sorted(g["claims"].items()):
        state = st.approval_state(c)
        if state is None:
            continue
        problem = panel_problem(cid, c) if state == "approved" else None
        if problem:
            excluded.append({"id": cid, "reason": f"panel: {problem}"})
        elif state != "approved":
            excluded.append({"id": cid, "reason": f"review {state}"})
        elif c.get("status") not in PUBLIC_CLAIM_STATUS:
            excluded.append({"id": cid, "reason": f"status {c.get('status')} is never public"})
        elif not {c.get("subject"), c.get("object")} <= entities:
            excluded.append({"id": cid, "reason": "subject or object is not public"})
        else:
            claims.add(cid)

    wiki, errors, wiki_files = set(), [], sorted(Path(wiki_dir).glob("*.mdx")) if Path(wiki_dir).is_dir() else []
    sources = {ev.get("source") for cid in claims for ev in g["claims"][cid].get("evidence") or [] if ev.get("source")}
    for path in wiki_files:
        meta, body = read_wiki(path)
        if meta.get("status") != "published":
            continue
        reasons = []
        state = wiki_approval(meta, body)
        problem = panel_problem(meta["id"], meta) if state == "approved" else None
        if problem:
            reasons.append(f"panel: {problem}")
        elif state != "approved":
            reasons.append(f"review {state or 'missing'}")
        if meta.get("entity") not in entities:
            reasons.append(f"entity {meta.get('entity')} is not public")
        reasons += [f"cites non-public claim {cid}" for cid in meta.get("claims") or [] if cid not in claims]
        if reasons:
            errors.append({"id": meta.get("id"), "file": str(path), "reasons": reasons})
        else:
            wiki.add(meta["id"])
            sources |= set(meta.get("sources") or [])

    inputs = {p: file_sha256(p) for p in paths}
    inputs.update({str(p): file_sha256(p) for p in wiki_files})
    return {
        "schema": 1,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "graph_files": paths,
        "wiki_dir": wiki_dir,
        "inputs": inputs,
        "entities": sorted(entities),
        "claims": sorted(claims),
        "wiki": sorted(wiki),
        "sources": sorted(s for s in sources if s in g["sources"]),
        "excluded": excluded,
        "errors": errors,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--graph", help=f"comma-separated graph files (default: $AIXON_GRAPH or {DEFAULT_GRAPH})")
    ap.add_argument("--wiki-dir", default=os.environ.get("AIXON_WIKI_DIR", "src/content/wiki"))
    ap.add_argument("--out", default=".aixon/public-gate.json")
    args = ap.parse_args(argv)
    result = gate(graph_paths(args.graph), args.wiki_dir)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"public gate: {len(result['entities'])} entities, {len(result['claims'])} claims, {len(result['wiki'])} wiki, "
          f"{len(result['excluded'])} excluded, {len(result['errors'])} errors -> {args.out}")
    for err in result["errors"]:
        print(f"ERROR {err['id']}: {'; '.join(err['reasons'])}", file=sys.stderr)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
