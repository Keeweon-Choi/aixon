#!/usr/bin/env python3
"""Human review of graph records and wiki documents (ADR-021).

  review.py list [--kind entity|claim|wiki] [--state pending|approved|stale|invalid]
  review.py show <id>
  review.py approve <id> --by human:<name> [--note TEXT] [--checked support,numbers,direction,conditions]

`approve` writes a `review` block bound to the record's current content hash; any later edit makes the
approval stale (seedtool G022) and the record drops out of the public build until re-approved.
It refuses to run inside an AI agent session (CLAUDECODE, AI_AGENT, CODEX_* variables). That is a guard
against accidents, not a security boundary: the real controls are reviewing the git diff and the
deployment environment's required reviewers.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import public_gate as pg  # noqa: E402
import seedtool as st  # noqa: E402
import yamlrec  # noqa: E402

AGENT_VARS = ("CLAUDECODE", "AI_AGENT")


def agent_session(env=os.environ) -> bool:
    return any(env.get(v) for v in AGENT_VARS) or any(k.startswith("CODEX_") for k in env)


def wiki_files(wiki_dir: str) -> dict[str, Path]:
    out = {}
    for path in sorted(Path(wiki_dir).glob("*.mdx")):
        meta, _ = pg.read_wiki(path)
        if meta.get("id"):
            out[meta["id"]] = path
    return out


def state_of(ident: str, graph: dict, wikis: dict[str, Path]) -> str:
    if ident in wikis:
        meta, body = pg.read_wiki(wikis[ident])
        return pg.wiki_approval(meta, body) or "pending"
    return st.approval_state(graph["entities"][ident]) or "pending"


def kind_of(ident: str, graph: dict) -> str:
    if ident.startswith("wiki:"):
        return "wiki"
    return "claim" if graph["types"].get(ident) == "Claim" else "entity"


def approve_record(paths: list[str], ident: str, by: str, note: str, checked: list[str], today: str) -> None:
    graph = st.load_graph(paths)
    record = graph["entities"][ident]
    review = {"by": by, "at": today, "decision": "approve", "reviewed_hash": st.review_hash(record), "note": note}
    if checked:
        review["checked"] = checked
    for path in paths:
        text = Path(path).read_text(encoding="utf-8").split("\n")
        try:
            yamlrec.record_span(text, ident)
        except KeyError:
            continue
        yamlrec.edit_file(path, lambda lines: yamlrec.set_field(lines, ident, "review", review))
        state = st.approval_state(st.load_graph(paths)["entities"][ident])
        assert state == "approved", f"self-check failed: {state}"
        return
    raise KeyError(ident)


def approve_wiki(path: Path, by: str, note: str, today: str) -> None:
    meta, body = pg.read_wiki(path)
    review = {"by": by, "at": today, "decision": "approve", "reviewed_hash": pg.wiki_hash(meta, body), "note": note}
    text = path.read_text(encoding="utf-8")
    head, rest = text.split("\n---\n", 1)
    lines = head.split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("review:"))
    stop = start + 1
    while stop < len(lines) and lines[stop].startswith((" ", "-")):
        stop += 1
    block = yaml.safe_dump({"review": review}, allow_unicode=True, sort_keys=False, width=1000).rstrip("\n").split("\n")
    path.write_text("\n".join(lines[:start] + block + lines[stop:]) + "\n---\n" + rest, encoding="utf-8")
    meta, body = pg.read_wiki(path)
    assert pg.wiki_approval(meta, body) == "approved", "self-check failed"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Human review of AIXON records (ADR-021).")
    ap.add_argument("--graph", help="comma-separated graph files")
    ap.add_argument("--wiki-dir", default=os.environ.get("AIXON_WIKI_DIR", "src/content/wiki"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("--kind", choices=["entity", "claim", "wiki"])
    p.add_argument("--state", choices=["pending", "approved", "stale", "invalid"])
    p = sub.add_parser("show")
    p.add_argument("id")
    p = sub.add_parser("approve")
    p.add_argument("id")
    p.add_argument("--by", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--checked", default="")
    args = ap.parse_args(argv)

    paths = pg.graph_paths(args.graph)
    graph = st.load_graph(paths)
    wikis = wiki_files(args.wiki_dir)

    if args.cmd == "list":
        ids = [i for i, typ in graph["types"].items() if typ == "Claim" or typ in pg.ENTITY_TYPES] + list(wikis)
        for ident in sorted(ids):
            kind, state = kind_of(ident, graph), state_of(ident, graph, wikis)
            if (args.kind in (None, kind)) and (args.state in (None, state)):
                print(f"{state:9} {kind:7} {ident}")
        return 0
    if args.cmd == "show":
        if args.id in wikis:
            print(wikis[args.id].read_text(encoding="utf-8"))
        else:
            print(yaml.safe_dump(graph["entities"][args.id], allow_unicode=True, sort_keys=False))
        print(f"# state: {state_of(args.id, graph, wikis)}")
        return 0

    if agent_session():
        print("refused: approvals must be made by a person, not inside an AI agent session (ADR-021)", file=sys.stderr)
        return 2
    if not st.HUMAN_RE.match(args.by):
        print("--by must look like human:<name> (lowercase letters, digits, - or _)", file=sys.stderr)
        return 2
    today = dt.date.today().isoformat()
    if args.id in wikis:
        approve_wiki(wikis[args.id], args.by, args.note, today)
    else:
        approve_record(paths, args.id, args.by, args.note, [c for c in args.checked.split(",") if c], today)
    print(f"approved {args.id} by {args.by}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
