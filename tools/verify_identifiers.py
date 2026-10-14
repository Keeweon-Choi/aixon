"""Verify arXiv identifiers in AIXON graph YAML files without third-party modules."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable


ARXIV_URL = "http://export.arxiv.org/api/query"
USER_AGENT = "aixon-verify/0.1"
ATOM = "{http://www.w3.org/2005/Atom}"


def normalize_title(title: str) -> str:
    """Normalize titles for a deliberately forgiving metadata comparison."""
    text = re.sub(r"\$.*?\$", "", unicodedata.normalize("NFKC", title), flags=re.DOTALL).lower()
    return "".join(char for char in text if not char.isspace() and not unicodedata.category(char).startswith("P"))


def _unquote(value: str) -> str:
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _paths(inputs: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for item in inputs:
        path = Path(item)
        paths.extend(path.glob("*.yaml") if path.is_dir() else [path])
    return sorted(paths, key=lambda path: str(path.resolve()))


def papers_in_file(path: Path) -> list[dict]:
    """Read the small Paper subset needed by this verifier, retaining line indexes."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    papers: list[dict] = []
    in_papers = False
    current: dict | None = None
    in_identifiers = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s*(?:#.*)?$", line):
            if current:
                papers.append(current); current = None
            in_papers = stripped == "papers:"
            in_identifiers = False
            continue
        if not in_papers:
            continue
        flow = re.match(r"^  - \{.*?id: (paper:[a-z0-9-]+), title: (.*?), authors: .*?identifiers: \{arxiv: ([^}]+)\}.*\}$", line)
        if flow:
            title = _unquote(flow.group(2))
            papers.append({"id": flow.group(1), "title": title, "arxiv": _unquote(flow.group(3)), "path": path, "lines": lines})
            continue
        match = re.match(r"^  - id:\s*(.+?)\s*$", line)
        if match:
            if current:
                papers.append(current)
            current = {"id": _unquote(match.group(1)), "path": path, "lines": lines}
            in_identifiers = False
            continue
        if not current:
            continue
        if re.match(r"^    identifiers:\s*", line):
            in_identifiers = True
            continue
        if re.match(r"^    metadata_checked:\s*", line):
            current["metadata_line"] = index
            in_identifiers = False
            continue
        key_match = re.match(r"^    (title|earliest_public_date):\s*(.+?)\s*$", line)
        if key_match:
            current[key_match.group(1)] = _unquote(key_match.group(2))
            in_identifiers = False
            continue
        arxiv_match = re.match(r"^      arxiv:\s*(.+?)\s*$", line) if in_identifiers else None
        if arxiv_match:
            current["arxiv"] = _unquote(arxiv_match.group(1))
    if current:
        papers.append(current)
    return [paper for paper in papers if paper.get("arxiv")]


def _arxiv_id(entry: ET.Element) -> str:
    value = entry.findtext(f"{ATOM}id", "")
    match = re.search(r"/(?:abs|pdf)/([^/]+?)(?:\.pdf)?$", value)
    return match.group(1).split("v", 1)[0] if match else ""


def parse_atom(raw: bytes) -> dict[str, dict[str, str]]:
    root = ET.fromstring(raw)
    entries: dict[str, dict[str, str]] = {}
    for entry in root.findall(f"{ATOM}entry"):
        arxiv = _arxiv_id(entry)
        if arxiv:
            entries[arxiv] = {"title": " ".join(entry.findtext(f"{ATOM}title", "").split()),
                              "published": entry.findtext(f"{ATOM}published", "")}
    return entries


def compare_papers(papers: Iterable[dict], entries: dict[str, dict[str, str]], errors: dict[str, str] | None = None) -> list[dict]:
    """Return one stable verification row per graph paper."""
    errors = errors or {}
    rows = []
    for paper in sorted(papers, key=lambda item: item["id"]):
        arxiv = paper["arxiv"].split("v", 1)[0]
        base = {"paper": paper["id"], "arxiv": arxiv, "yaml_title": paper.get("title", "")}
        if arxiv in errors:
            rows.append({**base, "status": "error", "arxiv_title": None, "arxiv_published": None, "date_flag": None, "error": errors[arxiv]})
            continue
        found = entries.get(arxiv)
        if not found:
            rows.append({**base, "status": "not_found", "arxiv_title": None, "arxiv_published": None, "date_flag": None})
            continue
        date_flag = "month_mismatch" if paper.get("earliest_public_date", "")[:7] != found["published"][:7] else None
        status = "match" if normalize_title(paper.get("title", "")) == normalize_title(found["title"]) else "title_mismatch"
        rows.append({**base, "status": status, "arxiv_title": found["title"], "arxiv_published": found["published"], "date_flag": date_flag})
    return rows


def _cache_path(cache: Path, identifiers: list[str]) -> Path:
    digest = hashlib.sha256(",".join(sorted(identifiers)).encode()).hexdigest()[:20]
    return cache / f"batch-{digest}.xml"


def fetch_entries(identifiers: list[str], cache: Path, offline: bool) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}
    errors: dict[str, str] = {}
    last_request = 0.0
    for start in range(0, len(identifiers), 50):
        batch = identifiers[start:start + 50]
        path = _cache_path(cache, batch)
        try:
            if path.exists():
                raw = path.read_bytes()
            elif offline:
                raise RuntimeError("cache miss in offline mode")
            else:
                delay = 3 - (time.monotonic() - last_request)
                if last_request and delay > 0:
                    time.sleep(delay)
                query = urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": 100})
                request = urllib.request.Request(f"{ARXIV_URL}?{query}", headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(request, timeout=30) as response:
                    raw = response.read()
                last_request = time.monotonic()
                cache.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            entries.update(parse_atom(raw))
        except Exception as exc:  # each requested id needs an observable result
            errors.update({identifier: str(exc) for identifier in batch})
    return entries, errors


def write_checked(papers: Iterable[dict], rows: Iterable[dict], today: str) -> None:
    """Set only inline metadata_checked mappings for arXiv title matches."""
    matched = {row["paper"] for row in rows if row["status"] == "match"}
    by_path: dict[Path, list[dict]] = {}
    for paper in papers:
        if paper["id"] in matched and "metadata_line" in paper:
            by_path.setdefault(paper["path"], []).append(paper)
    for path, updates in by_path.items():
        lines = updates[0]["lines"][:]
        for paper in sorted(updates, key=lambda item: item["metadata_line"], reverse=True):
            index = paper["metadata_line"]
            line = lines[index]
            match = re.match(r"^(\s*metadata_checked:\s*)\{(.*?)\}(\s*(?:#.*)?\n?)$", line)
            if not match:
                continue
            values = [value.strip() for value in match.group(2).split(",") if value.strip() and not value.strip().startswith("arxiv:")]
            values.append(f"arxiv: {today}")
            lines[index] = f"{match.group(1)}{{{', '.join(values)}}}{match.group(3)}"
        path.write_text("".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="verify_identifiers.py")
    parser.add_argument("graph", nargs="+")
    parser.add_argument("--cache", default="data/cache/arxiv")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-checked", action="store_true")
    args = parser.parse_args(argv)
    papers = [paper for path in _paths(args.graph) for paper in papers_in_file(path)]
    identifiers = sorted({paper["arxiv"].split("v", 1)[0] for paper in papers})
    entries, errors = fetch_entries(identifiers, Path(args.cache), args.offline)
    rows = compare_papers(papers, entries, errors)
    if args.write_checked:
        write_checked(papers, rows, dt.date.today().isoformat())
        cache = Path(args.cache); cache.mkdir(parents=True, exist_ok=True)
        (cache / "report.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(rows, ensure_ascii=False, indent=2) if args.json else "\n".join(f"{row['status']} {row['paper']} {row['arxiv']}" for row in rows))
    return 1 if any(row["status"] in {"title_mismatch", "not_found", "error"} for row in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
