#!/usr/bin/env python3
"""Prepare and verify independent AI cross-review panels (ADR-026)."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

import public_gate as pg
import review
import seedtool as st

COMMUNITY = ("wikipedia.org", "stackoverflow.com", "reddit.com", "medium.com", "quora.com",
             "velog.io", "blog.naver.com", "dev.to")


def release_dir(release, root):
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", release):
        raise ValueError("invalid release slug")
    return Path(root) / "review" / "cross" / release


def reports(directory):
    out = {}
    for path in sorted(directory.glob("*.yaml")):
        if path.name != "packet.yaml":
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            if not isinstance(data, dict) or not isinstance(data.get("items", []), list):
                raise ValueError(f"invalid report: {path.name}")
            out[path.stem] = data
    return out


def paragraphs(body):
    body = re.sub(r"^\s*```[^\n]*\n.*?^\s*```[^\n]*$", "", body, flags=re.M | re.S)
    lines = [line for line in body.splitlines() if not line.lstrip().startswith(("import ", "export "))]
    return [block.strip() for block in re.split(r"\n\s*\n", "\n".join(lines))
            if block.strip() and not re.fullmatch(r"#{1,6}\s+[^\n]+", block.strip())]


def required_fields(kind, record):
    if kind == "wiki":
        return [f"para:{i}" for i in range(1, len(paragraphs(record["body"])) + 1)]
    if kind == "claim":
        return ["relation"] + [f"evidence[{i}]" for i in range(len(record.get("evidence") or []))]
    if kind == "item":
        return ["prompt", "answer"] + (["choices"] if record.get("choices") else []) + (["rationale"] if "rationale" in record else [])
    fields = ["name"]
    if "summary" in record:
        fields.append("summary")
    if record.get("aliases"):
        fields.append("aliases")
    if record.get("fields") or record.get("parents"):
        fields.append("classification")
    if record.get("questions"):
        fields.append("questions")
    if str(record.get("id", "")).startswith("paper:") or any(k in record for k in ("authors", "venue", "identifiers")):
        fields.append("metadata")
    return fields


def records(paths, wiki_dir):
    graph = st.load_graph(paths)
    out = {}
    for ident, rec in graph["entities"].items():
        kind = "claim" if graph["types"].get(ident) == "Claim" else "item" if graph["types"].get(ident) == "AssessmentItem" else "entity"
        out[ident] = (kind, rec, st.review_hash(rec))
    for path in Path(wiki_dir).glob("*.mdx"):
        meta, body = pg.read_wiki(path)
        if meta.get("id"):
            out[meta["id"]] = ("wiki", {**meta, "body": body, "_path": path}, pg.wiki_hash(meta, body))
    return graph, out


def worksheet(release, root):
    return review.worksheet_items(Path(root) / "review" / f"{release}.yaml")


def packet(release, paths, wiki_dir, root):
    graph, available = records(paths, wiki_dir)
    predicate_text = (Path(__file__).resolve().parent.parent / "src" / "lib" / "predicates.ts").read_text(encoding="utf-8")
    descriptions = dict(re.findall(r"^\s*([A-Z_]+): '([^']+)',", predicate_text.split("export const predicateLabels")[0], re.M))
    entries = []
    for item in worksheet(release, root):
        ident = item["id"]
        kind, rec, digest = available[ident]
        if kind == "wiki":
            content = {"frontmatter": {k: v for k, v in rec.items() if k not in ("review", "status", "published_at", "body", "_path")},
                       "paragraphs": {f"para:{i}": p for i, p in enumerate(paragraphs(rec["body"]), 1)}}
        else:
            content = {k: v for k, v in rec.items() if k != "review"}
            if kind == "claim":
                content["subject_name"] = graph["entities"].get(rec.get("subject"), {}).get("name")
                content["object_name"] = graph["entities"].get(rec.get("object"), {}).get("name")
                content["predicate_meaning"] = descriptions.get(rec.get("predicate"), "")
                content["evidence"] = [{**ev, "source_detail": graph["sources"].get(ev.get("source"), {})}
                                       for ev in rec.get("evidence") or []]
        entries.append({"id": ident, "kind": kind, "reviewed_hash": digest,
                        "required_fields": required_fields(kind, rec), "content": content})
    directory = release_dir(release, root)
    directory.mkdir(parents=True, exist_ok=True)
    data = {"release": release, "items": entries}
    directory.joinpath("packet.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    directory.joinpath("packet.md").write_text("# Cross-review packet: " + release + "\n\n" + "\n\n".join(
        f"## {x['id']} ({x['kind']})\n\nHash: `{x['reviewed_hash']}`\n\nFields: {', '.join(x['required_fields'])}\n\n```yaml\n"
        + yaml.safe_dump(x["content"], allow_unicode=True, sort_keys=False) + "```" for x in entries) + "\n", encoding="utf-8")
    return entries


def _arxiv_id(url):
    match = re.search(r"arxiv\.org/(?:abs|pdf|html)/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?", url)
    return match.group(1) if match else None


def fetch_text(url, root, paths):
    """Return extracted text, using a seeded arXiv fulltext before a bounded web request."""
    arxiv = _arxiv_id(url)
    if arxiv:
        graph = st.load_graph(paths)
        for source in graph["sources"].values():
            full = source.get("fulltext_url", "")
            if _arxiv_id(full) != arxiv:
                continue
            suffix = Path(urllib.parse.urlparse(full).path).suffix or ".bin"
            stem = hashlib.sha256(full.encode()).hexdigest()[:16] + suffix
            cached = Path(root) / "data" / "cache" / "fulltext" / stem
            if cached.exists():
                meta = cached.with_name(cached.name + ".meta.json")
                ctype = json.loads(meta.read_text()).get("content_type", "") if meta.exists() else ""
                content, error = st._read_text(cached.read_bytes(), full, ctype)
                if error:
                    raise ValueError(error)
                return content
    req = urllib.request.Request(url, headers={"User-Agent": "AIXON cross-review quote verifier/1.0 (+https://github.com/Keeweon-Choi/aixon)"})
    with urllib.request.urlopen(req, timeout=20) as response:
        data = response.read(10 * 1024 * 1024 + 1)
        if len(data) > 10 * 1024 * 1024:
            raise ValueError("response exceeds 10 MB")
        content, error = st._read_text(data, response.geturl(), response.headers.get_content_type())
    if error:
        raise ValueError(error)
    return content


def confirm(release, paths, root, refresh=False):
    directory = release_dir(release, root)
    keys = {(src.get("url"), src.get("passage")) for report in reports(directory).values()
            for item in report.get("items") or [] for check in item.get("checks") or []
            for src in check.get("sources") or [] if isinstance(src, dict)}
    cache = Path(root) / ".aixon" / "web-cache"
    cache.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    output = {"schema": 1, "generated_at": now, "sources": {}}
    for url, passage in sorted(keys, key=str):
        key = f"{url}\n{passage}"
        try:
            if not isinstance(url, str) or not url.startswith(("https://", "http://")) or not isinstance(passage, str) or not passage:
                raise ValueError("URL and passage are required")
            saved = cache / (hashlib.sha256(url.encode()).hexdigest() + ".txt")
            if saved.exists() and not refresh:
                page = saved.read_text(encoding="utf-8")
            else:
                page = fetch_text(url, root, paths)
                saved.write_text(page, encoding="utf-8")
            status = "found" if st._normal(passage) in st._normal(page) else "not-found"
            detail = "matched" if status == "found" else "passage not found"
            digest = hashlib.sha256(page.encode()).hexdigest()
        except Exception as exc:  # noqa: BLE001 - each source failure is recorded
            status, detail, digest = "fetch-failed", str(exc), None
        output["sources"][key] = {"status": status, "detail": detail, "fetched_at": now, "text_sha256": digest}
    directory.joinpath("confirm.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def effective_tier(source):
    host = (urllib.parse.urlparse(str(source.get("url", ""))).hostname or "").lower()
    if any(host == domain or host.endswith("." + domain) for domain in COMMUNITY) or host.endswith((".stackexchange.com", ".tistory.com", ".blogspot.com", ".wordpress.com", ".hashnode.dev")):
        return "C", host
    return source.get("tier"), host


def report_item_problems(item, fields, digest, kind, confirmed):
    problems = []
    if item.get("decision") != "approve":
        problems.append(f"decision {item.get('decision')} is not approve")
    if item.get("reviewed_hash") != digest:
        problems.append("stale reviewed_hash")
    if item.get("unchecked"):
        problems.append("unchecked is non-empty")
    checks = item.get("checks") or []
    if not isinstance(checks, list):
        return problems + ["checks must be a list"]
    passed = set()
    for check in checks:
        if not isinstance(check, dict):
            problems.append("check must be a mapping")
            continue
        field, verdict = check.get("field"), check.get("verdict")
        if verdict in ("unsupported", "wrong", "analogy-unsourced"):
            problems.append(f"{field}: failing verdict {verdict}")
            continue
        if verdict == "computed" and not str(check.get("note", "")).strip():
            problems.append(f"{field}: computed needs a note")
            continue
        if verdict == "no-claim" and not (kind == "wiki" and field in fields):
            problems.append(f"{field}: no-claim is only for wiki paragraphs")
            continue
        if verdict in ("supported", "analogy-sourced"):
            found = []
            for source in check.get("sources") or []:
                if not isinstance(source, dict):
                    continue
                key = f"{source.get('url')}\n{source.get('passage')}"
                if confirmed.get(key, {}).get("status") == "found":
                    found.append(effective_tier(source))
            if not found:
                problems.append(f"{field}: no found source")
                continue
            if field == "metadata" or re.fullmatch(r"evidence\[\d+\]", str(field)):
                if not any(tier == "A" for tier, _ in found):
                    problems.append(f"{field}: needs a found tier-A source")
                    continue
            elif not (any(tier in ("A", "B") for tier, _ in found) or len({host for tier, host in found if tier == "C"}) >= 2):
                problems.append(f"{field}: needs A/B or two C hosts")
                continue
        elif verdict not in ("computed", "no-claim"):
            problems.append(f"{field}: invalid verdict {verdict}")
            continue
        passed.add(field)
    for field in fields:
        if field not in passed:
            problems.append(f"missing required field {field}")
    return problems


def _check_release(release, paths, wiki_dir, root, include_audit=True):
    directory = release_dir(release, root)
    _, available = records(paths, wiki_dir)
    try:
        items = worksheet(release, root)
    except (FileNotFoundError, ValueError, yaml.YAMLError):
        items = []
    ids = [item["id"] for item in items if isinstance(item.get("id"), str)]
    if not ids:
        return {"<release>": ["missing or empty worksheet"]}
    try:
        confirmed = json.loads(directory.joinpath("confirm.json").read_text(encoding="utf-8"))["sources"]
        if not isinstance(confirmed, dict):
            raise ValueError("sources is not a mapping")
    except (OSError, ValueError, KeyError):
        return {ident: ["missing or invalid confirm.json"] for ident in ids}
    all_reports = reports(directory)
    result = {}
    for ident in ids:
        problems = []
        if ident not in available:
            result[ident] = ["record is missing"]
            continue
        kind, record, digest = available[ident]
        fields = required_fields(kind, record)
        found = []
        for stem, report in all_reports.items():
            if not include_audit and report.get("start") == "audit":
                continue
            containing = [entry for entry in report.get("items") or [] if isinstance(entry, dict) and entry.get("id") == ident]
            if not containing:
                continue
            start = report.get("start")
            if report.get("reviewer") != f"agent:{stem}":
                problems.append(f"{stem}: reviewer does not match file stem")
            if report.get("release") != release:
                problems.append(f"{stem}: release mismatch")
            if start not in ("source-first", "claim-first", "audit"):
                problems.append(f"{stem}: invalid start")
            if start != "audit":
                found.append((report.get("reviewer"), start))
            if include_audit or start != "audit":
                for entry in containing:
                    problems.extend(f"{stem}: {reason}" for reason in report_item_problems(entry, fields, digest, kind, confirmed))
        if len({name for name, _ in found}) < 2:
            problems.append("needs two distinct reviewers")
        if not {"source-first", "claim-first"} <= {start for _, start in found}:
            problems.append("needs source-first and claim-first reports")
        result[ident] = problems
    return result


def check_release(release, paths, wiki_dir, root):
    return _check_release(release, paths, wiki_dir, root)


def sampled_ids(release, paths, wiki_dir, root):
    directory = release_dir(release, root)
    passing = [ident for ident, problems in _check_release(release, paths, wiki_dir, root, False).items() if not problems]
    blob = b"".join(path.read_bytes() for path in sorted(directory.glob("*.yaml"))
                    if path.name != "packet.yaml" and (yaml.safe_load(path.read_text()) or {}).get("start") != "audit")
    report_hash = hashlib.sha256(blob).hexdigest()
    ordered = sorted(passing, key=lambda ident: hashlib.sha256(f"{release}\n{report_hash}\n{ident}".encode()).hexdigest())
    return ordered[:max(3, math.ceil(len(passing) * .1))]


def audit_problems(release, paths, wiki_dir, root):
    directory = release_dir(release, root)
    all_reports = reports(directory)
    reviewers = {report.get("reviewer") for report in all_reports.values() if report.get("start") != "audit"}
    audits = [(stem, report) for stem, report in all_reports.items() if report.get("start") == "audit"]
    sample = sampled_ids(release, paths, wiki_dir, root)
    if len(audits) != 1:
        return ["exactly one audit report is required"], [], None
    stem, audit = audits[0]
    problems = []
    if audit.get("reviewer") != f"agent:{stem}" or audit.get("reviewer") in reviewers:
        problems.append("audit reviewer must match file stem and be independent")
    if audit.get("release") != release:
        problems.append("audit release mismatch")
    covered = [item.get("id") for item in audit.get("items") or []]
    if len(covered) != len(sample) or set(covered) != set(sample):
        problems.append("audit must cover exactly the recomputed sample")
    if any(item.get("decision") in ("fix", "reject") for item in audit.get("items") or []):
        problems.append("audit contains fix or reject")
    checks = check_release(release, paths, wiki_dir, root)
    for ident in sample:
        problems.extend(f"{ident}: {p}" for p in checks.get(ident, []))
    return problems, sample, audit.get("reviewer")


def approve(release, paths, wiki_dir, root, today):
    audit_errors, _, auditor = audit_problems(release, paths, wiki_dir, root)
    checked = check_release(release, paths, wiki_dir, root)
    if audit_errors:
        return {"approved": 0, "published": 0, "skipped": 0, "failed": sum(bool(v) for v in checked.values()), "errors": audit_errors}
    panel_reports = reports(release_dir(release, root))
    reviewers = sorted({r["reviewer"] for r in panel_reports.values() if r.get("start") in ("source-first", "claim-first")})
    _, available = records(paths, wiki_dir)
    wikis = review.wiki_files(wiki_dir)
    result = {"approved": 0, "published": 0, "skipped": 0, "failed": 0, "errors": []}
    for item in worksheet(release, root):
        ident = item["id"]
        if checked.get(ident):
            result["failed"] += 1
            result["errors"].append(f"{ident}: {checked[ident][0]}")
            continue
        kind, rec, digest = available[ident]
        old = rec.get("review")
        if st.approval_kind(old) == "human" and (pg.wiki_approval(rec, rec["body"]) if kind == "wiki" else st.approval_state(rec)) == "approved":
            result["skipped"] += 1
            continue
        block = {"by": f"panel:{release}", "method": "cross-review", "reviewers": reviewers,
                 "audit": auditor, "at": today, "decision": "approve", "reviewed_hash": digest,
                 "report": f"review/cross/{release}", "note": ""}
        try:
            if kind == "wiki":
                review.set_wiki_frontmatter(wikis[ident], {"review": block})
                if item.get("publish") is True:
                    review.publish_wiki(wikis[ident], today)
                    result["published"] += 1
            else:
                review.write_record_review(paths, ident, block)
            result["approved"] += 1
        except (OSError, ValueError, KeyError, AssertionError) as exc:
            result["failed"] += 1
            result["errors"].append(f"{ident}: {exc}")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("packet", "confirm", "check", "sample", "approve"))
    parser.add_argument("release")
    parser.add_argument("--graph")
    parser.add_argument("--wiki-dir", default="src/content/wiki")
    parser.add_argument("--root", default=".")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--today", default=dt.date.today().isoformat())
    args = parser.parse_args(argv)
    paths = pg.graph_paths(args.graph)
    try:
        if args.command == "packet":
            print(f"packet: {len(packet(args.release, paths, args.wiki_dir, args.root))} items")
        elif args.command == "confirm":
            data = confirm(args.release, paths, args.root, args.refresh)
            counts = {state: sum(x["status"] == state for x in data["sources"].values()) for state in ("found", "not-found", "fetch-failed")}
            print("confirm: " + ", ".join(f"{v} {k}" for k, v in counts.items()))
        elif args.command == "check":
            results = check_release(args.release, paths, args.wiki_dir, args.root)
            for ident, problems in results.items():
                print(f"{'FAIL' if problems else 'PASS'} {ident}" + (f": {'; '.join(problems)}" if problems else ""))
            return 1 if any(results.values()) else 0
        elif args.command == "sample":
            sample = sampled_ids(args.release, paths, args.wiki_dir, args.root)
            release_dir(args.release, args.root).joinpath("sample.json").write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n")
            print("sample: " + ", ".join(sample))
        else:
            if not args.yes and input("패널 승인을 기록할까요? [y/N] ").strip().lower() != "y":
                return 0
            result = approve(args.release, paths, args.wiki_dir, args.root, args.today)
            for error in result["errors"]:
                print("FAIL " + error)
            print(f"approved {result['approved']}, published {result['published']}, skipped (human) {result['skipped']}, failed {result['failed']}")
            return 1 if result["errors"] or result["failed"] else 0
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"FAIL {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
