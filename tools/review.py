#!/usr/bin/env python3
"""Human review of graph records and wiki documents (ADR-021).

  review.py list [--kind entity|claim|wiki] [--state pending|approved|stale|invalid]
  review.py show <id>
  review.py approve <id> --by human:<name> [--note TEXT] [--checked support,numbers,direction,conditions]
  review.py approve-batch <worksheet> --by human:<name> [--yes]
  review.py publish wiki:<slug> --by human:<name>

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
    set_wiki_frontmatter(path, {"review": review})
    meta, body = pg.read_wiki(path)
    assert pg.wiki_approval(meta, body) == "approved", "self-check failed"


def set_wiki_frontmatter(path: Path, fields: dict) -> None:
    """Set simple frontmatter fields without reformatting the document body."""
    text = path.read_text(encoding="utf-8")
    head, rest = text.split("\n---\n", 1)
    lines = head.split("\n")
    for key, value in fields.items():
        replacement = yaml.safe_dump(
            {key: value}, allow_unicode=True, sort_keys=False, width=1000
        ).rstrip("\n").split("\n")
        start = next((i for i, line in enumerate(lines) if line.startswith(f"{key}:")), None)
        if start is None:
            lines.extend(replacement)
        else:
            stop = start + 1
            while stop < len(lines) and lines[stop].startswith((" ", "-")):
                stop += 1
            lines[start:stop] = replacement
    path.write_text("\n".join(lines) + "\n---\n" + rest, encoding="utf-8")


def publish_wiki(path: Path, today: str) -> None:
    """Publish an already-fresh human-approved wiki document."""
    meta, body = pg.read_wiki(path)
    state = pg.wiki_approval(meta, body)
    if state != "approved":
        raise ValueError(f"wiki approval must be fresh before publishing (review {state or 'missing'})")
    set_wiki_frontmatter(path, {"status": "published", "published_at": today})
    meta, body = pg.read_wiki(path)
    assert meta.get("status") == "published" and meta.get("published_at") == today
    assert pg.wiki_approval(meta, body) == "approved", "publication made approval stale"


def worksheet_items(worksheet_path: str | Path) -> list[dict]:
    worksheet = yaml.safe_load(Path(worksheet_path).read_text(encoding="utf-8")) or {}
    items = worksheet.get("items", [])
    if not isinstance(items, list):
        raise ValueError("worksheet items must be a list")
    if not all(isinstance(item, dict) for item in items):
        raise ValueError("worksheet items must contain mappings")
    return items


def approve_batch(paths, wiki_dir, worksheet_path, by, today, items=None) -> dict:
    """Approve worksheet items, returning processed IDs grouped by outcome.

    This deliberately has no agent-session or confirmation check so tests and the CLI can
    use it after the human-only boundary and confirmation have been handled.
    """
    wikis = wiki_files(wiki_dir)
    result = {"approved": [], "published": [], "skipped": [], "failed": []}
    # items: what the CLI already showed the person, so the confirmed list is the one applied
    for item in worksheet_items(worksheet_path) if items is None else items:
        ident = item.get("id")
        kind = item.get("kind", "")
        decision = item.get("decision", item.get("recommendation"))
        entry = {"id": ident, "kind": kind, "decision": decision}
        if decision != "approve":
            result["skipped"].append(entry)
            continue
        try:
            if not isinstance(ident, str) or not ident:
                raise ValueError("item id is required")
            if ident.startswith("wiki:"):
                path = wikis.get(ident)
                if path is None:
                    raise KeyError(ident)
                approve_wiki(path, by, str(item.get("notes", "")), today)
                if item.get("publish") is True:
                    publish_wiki(path, today)
                    result["published"].append(entry)
            else:
                approve_record(paths, ident, by, str(item.get("notes", "")), [], today)
            result["approved"].append(entry)
        except (KeyError, ValueError, OSError, AssertionError) as exc:
            result["failed"].append({**entry, "error": str(exc)})
    return result


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
    p = sub.add_parser("approve-batch")
    p.add_argument("worksheet")
    p.add_argument("--by", required=True)
    p.add_argument("--yes", action="store_true")
    p = sub.add_parser("publish")
    p.add_argument("id")
    p.add_argument("--by", required=True)
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
    if args.cmd == "approve-batch":
        try:
            items = worksheet_items(args.worksheet)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            print(f"worksheet error: {exc}", file=sys.stderr)
            return 2
        approved = [item for item in items if item.get("decision", item.get("recommendation")) == "approve"]
        skipped = [item for item in items if item.get("decision", item.get("recommendation")) != "approve"]
        for item in approved:
            print(f"approve {item.get('id')} ({item.get('kind', '')})")
        for item in skipped:
            print(f"skip {item.get('id')} ({item.get('kind', '')}: {item.get('decision', item.get('recommendation'))})")
        if approved and not args.yes:
            answer = input("승인할까요? [y/N] ").strip().lower()
            if answer != "y":
                print(f"approved 0, published 0, skipped {len(skipped)}, failed 0")
                return 0
        result = approve_batch(paths, args.wiki_dir, args.worksheet, args.by, today, items)
        for failed in result["failed"]:
            print(f"failed {failed['id']}: {failed['error']}", file=sys.stderr)
        print(
            f"approved {len(result['approved'])}, published {len(result['published'])}, "
            f"skipped {len(result['skipped'])}, failed {len(result['failed'])}"
        )
        return 1 if result["failed"] else 0
    if args.cmd == "publish":
        if not args.id.startswith("wiki:"):
            print("publish accepts only wiki:<slug>", file=sys.stderr)
            return 2
        path = wikis.get(args.id)
        if path is None:
            print(f"unknown wiki: {args.id}", file=sys.stderr)
            return 1
        try:
            publish_wiki(path, today)
        except ValueError as exc:
            print(f"refused: {exc}", file=sys.stderr)
            return 1
        print(f"published {args.id} by {args.by}")
        return 0
    if args.id in wikis:
        approve_wiki(wikis[args.id], args.by, args.note, today)
    else:
        approve_record(paths, args.id, args.by, args.note, [c for c in args.checked.split(",") if c], today)
    print(f"approved {args.id} by {args.by}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
