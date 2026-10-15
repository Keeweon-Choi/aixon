#!/usr/bin/env python3
"""Audit a built static site (the output of `astro build` + `pagefind`).

Rules (docs/CONTENT_VALIDATION_PLAN.md layer L-B):

    V-DIST-LINK  every internal href/src resolves to a file once the deployment base is stripped
    V-SEO        every page has lang="ko", a title, a meta description and exactly one h1;
                 sitemap-index.xml and robots.txt exist and agree with the mode
    V-MATH       no `katex-error`; every `.katex` contains MathML
    V-NO-CDN     no external <script src> / stylesheet (HTML and CSS)
    V-SEC        no inline event handlers (on*=) and no javascript: URLs
    V-PUBLIC     (--mode public) exactly the tools/public_gate.py allow-list is published, and no prose of
                 any other record appears anywhere (taint test)

Usage:
    check_dist.py DIST --base /aixon/ --mode preview|public [--site URL]
                  [--graph a.yaml,b.yaml] [--wiki-dir DIR] [--json]

Exit code: 0 clean, 1 findings, 2 bad setup (missing dist, graph, ...).
"""

from __future__ import annotations

import argparse
import html
import json
import os
import posixpath
import re
import sys
import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


import public_gate
from seedtool import load_graph

DEFAULT_GRAPH = "data/seed/seed_graph.yaml,data/graph/atlas.yaml"
DEFAULT_WIKI_DIR = "src/content/wiki"
DRAFT_BANNER = "검토 전 초안"
SKIPPED_DIRECTORIES = ("pagefind", "_astro")
REQUIRED_FILES = ("index.html", "404.html", "graph.json", "node-index.json", "sitemap-index.xml", "robots.txt")
PAGEFIND_FILES = ("pagefind/pagefind.js", "pagefind/pagefind-ui.js", "pagefind/pagefind-ui.css")
MAX_LISTED_FINDINGS = 20

VOID_ELEMENTS = frozenset(
    ("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr")
)
REFERENCE_ATTRIBUTES = {
    "a": ("href",),
    "area": ("href",),
    "link": ("href",),
    "script": ("src",),
    "img": ("src",),
    "source": ("src",),
    "iframe": ("src",),
    "audio": ("src",),
    "video": ("src", "poster"),
    "form": ("action",),
    "astro-island": ("component-url", "renderer-url", "before-hydration-url"),
}
EXTERNAL_RESOURCE_RELS = frozenset(
    ("stylesheet", "preload", "modulepreload", "prefetch", "preconnect", "dns-prefetch")
)
IGNORED_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "blob:", "about:")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
CSS_EXTERNAL_RE = re.compile(r"""(?:url\(\s*['"]?|@import\s+['"]?)(?:https?:)?//[^\s'")]+""", re.I)


@dataclass
class Finding:
    """One problem found in the dist (error) or advisory (warning)."""

    level: str
    code: str
    file: str
    message: str

    def as_dict(self) -> dict[str, str]:
        """Return the JSON-report form."""
        return {"level": self.level, "code": self.code, "file": self.file, "message": self.message}


@dataclass
class Report:
    """Collects findings."""

    findings: list[Finding] = field(default_factory=list)

    def error(self, code: str, file: str, message: str) -> None:
        """Record an error."""
        self.findings.append(Finding("error", code, file, message))

    def warning(self, code: str, file: str, message: str) -> None:
        """Record a warning."""
        self.findings.append(Finding("warning", code, file, message))

    @property
    def errors(self) -> list[Finding]:
        """Return the errors only."""
        return [item for item in self.findings if item.level == "error"]

    @property
    def warnings(self) -> list[Finding]:
        """Return the warnings only."""
        return [item for item in self.findings if item.level == "warning"]


@dataclass
class PageInfo:
    """Facts extracted from one HTML page."""

    lang: str | None = None
    title: str = ""
    description: str | None = None
    h1_count: int = 0
    images_without_alt: int = 0
    katex_count: int = 0
    katex_without_mathml: int = 0
    references: list[tuple[str, str, str, str]] = field(default_factory=list)  # tag, attr, value, rel


class PageParser(HTMLParser):
    """Extract SEO, math and reference facts from one HTML document."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.info = PageInfo()
        self._in_title = False
        self._open_elements: list[list] = []  # [tag, is_katex, has_mathml]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Handle an opening tag."""
        self._visit(tag, dict(attrs), push=tag not in VOID_ELEMENTS)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Handle a self-closing tag such as <path />."""
        self._visit(tag, dict(attrs), push=False)

    def handle_endtag(self, tag: str) -> None:
        """Close the nearest open element with this name."""
        if tag == "title":
            self._in_title = False
        for index in range(len(self._open_elements) - 1, -1, -1):
            if self._open_elements[index][0] == tag:
                self._close_until(index)
                return

    def handle_data(self, data: str) -> None:
        """Collect the title text."""
        if self._in_title:
            self.info.title += data

    def close(self) -> None:
        """Finish parsing and account for katex elements that were never closed."""
        super().close()
        self._close_until(0)

    def _close_until(self, index: int) -> None:
        """Pop open elements down to index, scoring the katex ones."""
        while len(self._open_elements) > index:
            _tag, is_katex, has_mathml = self._open_elements.pop()
            if is_katex and not has_mathml:
                self.info.katex_without_mathml += 1

    def _visit(self, tag: str, attributes: dict[str, str | None], push: bool) -> None:
        """Record what a start tag tells us."""
        info = self.info
        if tag == "html":
            info.lang = attributes.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            info.h1_count += 1
        elif tag == "img" and attributes.get("alt") is None:
            info.images_without_alt += 1
        elif tag == "meta" and (attributes.get("name") or "").lower() == "description":
            info.description = attributes.get("content") or ""
        elif tag == "math":
            for element in self._open_elements:
                element[2] = True
        for attribute in REFERENCE_ATTRIBUTES.get(tag, ()):
            value = attributes.get(attribute)
            if value is not None:
                info.references.append((tag, attribute, value, attributes.get("rel") or ""))
        classes = (attributes.get("class") or "").split()
        is_katex = "katex" in classes
        if is_katex:
            info.katex_count += 1
        if push:
            self._open_elements.append([tag, is_katex, False])
        elif is_katex:
            info.katex_without_mathml += 1


def parse_page(text: str) -> PageInfo:
    """Parse one HTML document."""
    parser = PageParser()
    parser.feed(text)
    parser.close()
    return parser.info


def page_url_path(dist: Path, page: Path, base: str) -> str:
    """Return the URL path (with base) a page file is served at."""
    relative = page.relative_to(dist).as_posix()
    if relative == "index.html":
        return base
    if relative.endswith("/index.html"):
        return base + relative[: -len("index.html")]
    return base + relative


def resolve_internal_path(raw: str, page_path: str, site: str | None) -> str | None:
    """Return the absolute URL path of an internal reference, or None for external/ignored ones."""
    value = raw.strip()
    if not value or value.startswith("#") or value.lower().startswith(IGNORED_SCHEMES):
        return None
    if value.startswith("//"):
        return None
    if SCHEME_RE.match(value):
        if site and value.startswith(site):
            value = value[len(site.rstrip("/")) :] or "/"
        else:
            return None
    value = value.split("#", 1)[0].split("?", 1)[0]
    if not value:
        return None
    if value.startswith("/"):
        return unquote(value)
    directory = page_path if page_path.endswith("/") else posixpath.dirname(page_path) + "/"
    joined = posixpath.normpath(posixpath.join(directory, unquote(value)))
    return joined + "/" if value.endswith("/") and not joined.endswith("/") else joined


def find_target(dist: Path, url_path: str, base: str) -> str | None:
    """Return None when url_path resolves to a file under dist, else the reason it does not."""
    if url_path.rstrip("/") + "/" == base:
        relative = ""
    elif url_path.startswith(base):
        relative = url_path[len(base) :]
    else:
        return f"is outside the deployment base {base}"
    if relative == "" or relative.endswith("/"):
        target = dist / relative / "index.html"
        return None if target.is_file() else "no such page"
    target = dist / relative
    if target.is_file():
        return None
    if target.is_dir():
        return "is a directory; the link lacks the trailing slash"
    return "no such file"


def check_page(dist: Path, page: Path, text: str, args: argparse.Namespace, report: Report) -> None:
    """V-SEO, V-MATH, V-NO-CDN and V-DIST-LINK for one HTML page."""
    name = page.relative_to(dist).as_posix()
    info = parse_page(text)
    if info.lang != "ko":
        report.error("V-SEO", name, f'<html lang> must be "ko", got {info.lang!r}')
    if not info.title.strip():
        report.error("V-SEO", name, "missing or empty <title>")
    if not (info.description or "").strip():
        report.error("V-SEO", name, 'missing or empty <meta name="description">')
    if info.h1_count != 1:
        report.error("V-SEO", name, f"expected exactly one <h1>, found {info.h1_count}")
    if info.images_without_alt:
        report.error("V-SEO", name, f"{info.images_without_alt} <img> without an alt attribute")
    if "katex-error" in text:
        report.error("V-MATH", name, "contains katex-error")
    if re.search(r"<[a-z][^>]*\son[a-z]+\s*=", text, re.I):
        report.error("V-SEC", name, "inline event handler attribute (on*=)")
    if re.search(r"(?:href|src|action|formaction)\s*=\s*[\"']?\s*javascript:", text, re.I):
        report.error("V-SEC", name, "javascript: URL")
    for tag, value in re.findall(r"<(img|iframe|source)\b[^>]*\s(?:src|srcset)\s*=\s*[\"']([^\"']+)", text, re.I):
        if re.search(r"(?:^|[\s,])(?:https?:)?//", value) and not (args.site and value.startswith(args.site)):
            report.error("V-NO-CDN", name, f"external {tag.lower()} resource: {value[:80]}")
    if info.katex_without_mathml:
        report.error("V-MATH", name, f"{info.katex_without_mathml} .katex element(s) without MathML")
    own_path = page_url_path(dist, page, args.base)
    for tag, attribute, value, rel in info.references:
        check_external_resource(name, tag, value, rel, args.site, report)
        url_path = resolve_internal_path(value, own_path, args.site)
        if url_path is None:
            continue
        problem = find_target(dist, url_path, args.base)
        if problem is None:
            continue
        message = f'{tag} {attribute}="{value}" {problem}'
        # 404.html is served for every unknown URL, so its canonical link cannot point at a real page.
        if name == "404.html" and "canonical" in rel.split():
            report.warning("V-DIST-LINK", name, message)
        else:
            report.error("V-DIST-LINK", name, message)


def check_external_resource(name: str, tag: str, value: str, rel: str, site: str | None, report: Report) -> None:
    """V-NO-CDN: scripts and stylesheets must be local."""
    external = value.startswith(("http://", "https://", "//")) and not (site and value.startswith(site))
    if not external:
        return
    rels = set(rel.lower().split())
    if tag == "script" or (tag == "link" and rels & EXTERNAL_RESOURCE_RELS):
        report.error("V-NO-CDN", name, f"external {tag} resource: {value}")


def check_css_files(dist: Path, report: Report) -> None:
    """V-NO-CDN: bundled CSS must not pull fonts or styles from a CDN."""
    for css in sorted(dist.rglob("*.css")):
        name = css.relative_to(dist).as_posix()
        if name.startswith("pagefind/"):
            continue
        match = CSS_EXTERNAL_RE.search(css.read_text(encoding="utf8", errors="replace"))
        if match:
            report.error("V-NO-CDN", name, f"CSS loads an external resource: {match.group(0)}")


def check_required_files(dist: Path, report: Report) -> None:
    """V-SEO / V-DIST-LINK: files every deployment needs."""
    for name in REQUIRED_FILES:
        if not (dist / name).is_file():
            report.error("V-DIST-LINK", name, "required file is missing")
    if (dist / "search" / "index.html").is_file():
        for name in PAGEFIND_FILES:
            if not (dist / name).is_file():
                report.error("V-DIST-LINK", name, "the search page needs the pagefind index (run pagefind)")
    for name in ("graph.json", "node-index.json"):
        path = dist / name
        if path.is_file():
            try:
                json.loads(path.read_text(encoding="utf8"))
            except json.JSONDecodeError as error:
                report.error("V-DIST-LINK", name, f"is not valid JSON: {error}")


def check_sitemap(dist: Path, args: argparse.Namespace, report: Report) -> None:
    """V-SEO: sitemap-index.xml lists sitemaps whose URLs start with site + base and exist."""
    index = dist / "sitemap-index.xml"
    if not index.is_file():
        return
    prefix = (args.site.rstrip("/") + args.base) if args.site else None
    sitemap_urls = sitemap_locations(index, report)
    page_urls: list[str] = []
    for location in sitemap_urls:
        sitemap_file = dist / location.rsplit("/", 1)[-1]
        if not sitemap_file.is_file():
            report.error("V-SEO", "sitemap-index.xml", f"lists a sitemap that does not exist: {location}")
            continue
        page_urls.extend(sitemap_locations(sitemap_file, report))
    if not page_urls:
        report.error("V-SEO", "sitemap-index.xml", "the sitemap lists no page")
    origins = {origin_of(location) for location in sitemap_urls + page_urls}
    for location in sitemap_urls + page_urls:
        if prefix and not location.startswith(prefix):
            report.error("V-SEO", "sitemap-index.xml", f"URL does not start with {prefix}: {location}")
    if len(origins) > 1:
        report.error("V-SEO", "sitemap-index.xml", f"URLs mix several origins: {sorted(origins)}")
    for location in page_urls:
        problem = find_target(dist, location[len(origin_of(location)) :], args.base)
        if problem is not None:
            report.error("V-SEO", "sitemap-index.xml", f"{location} {problem}")


def origin_of(url: str) -> str:
    """Return scheme://host of an absolute URL ('' for anything else)."""
    match = re.match(r"^[a-z]+://[^/]+", url)
    return match.group(0) if match else ""


def sitemap_locations(path: Path, report: Report) -> list[str]:
    """Return the <loc> values of a sitemap or sitemap index file."""
    try:
        root = ElementTree.fromstring(path.read_text(encoding="utf8"))
    except ElementTree.ParseError as error:
        report.error("V-SEO", path.name, f"is not valid XML: {error}")
        return []
    return [(element.text or "").strip() for element in root.iter() if element.tag.endswith("}loc") or element.tag == "loc"]


def check_robots(dist: Path, args: argparse.Namespace, report: Report) -> None:
    """V-SEO: preview blocks crawlers; public allows them and lists the sitemap."""
    robots = dist / "robots.txt"
    if not robots.is_file():
        return
    lines = [line.strip() for line in robots.read_text(encoding="utf8").splitlines()]
    blocks_everything = "Disallow: /" in lines
    sitemap_lines = [line for line in lines if line.lower().startswith("sitemap:")]
    if args.mode == "preview" and not blocks_everything:
        report.error("V-SEO", "robots.txt", "a preview build must contain `Disallow: /`")
    if args.mode == "public":
        if blocks_everything:
            report.error("V-SEO", "robots.txt", "a public build must not contain `Disallow: /`")
        if not any(line.split(":", 1)[1].strip().endswith("sitemap-index.xml") for line in sitemap_lines):
            report.error("V-SEO", "robots.txt", "a public build must list sitemap-index.xml")
        prefix = (args.site.rstrip("/") + args.base) if args.site else None
        for line in sitemap_lines:
            if prefix and not line.split(":", 1)[1].strip().startswith(prefix):
                report.error("V-SEO", "robots.txt", f"Sitemap URL does not start with {prefix}: {line}")


def check_public(dist: Path, pages: dict[Path, str], args: argparse.Namespace, report: Report) -> None:
    """V-PUBLIC: exactly the allow-list of tools/public_gate.py is published and nothing else leaks (ADR-021)."""
    paths = [item.strip() for item in args.graph.split(",") if item.strip()]
    expected = public_gate.gate(paths, args.wiki_dir)
    if args.gate:
        used = json.loads(Path(args.gate).read_text(encoding="utf8"))
        for key in ("entities", "claims", "wiki", "sources"):
            if sorted(used.get(key, [])) != expected[key]:
                report.error("V-PUBLIC", args.gate, f"{key} differ from a fresh public_gate run (stale gate file?)")
    for page, text in pages.items():
        if DRAFT_BANNER in text:
            report.error("V-PUBLIC", page.relative_to(dist).as_posix(), f"public page contains '{DRAFT_BANNER}'")
    check_public_pages(dist, expected, report)
    check_public_json(dist, expected, report)
    check_taint(dist, pages, paths, args.wiki_dir, expected, report)


def emitted_ids(dist: Path) -> dict[str, str]:
    """{record id: page folder} for every entity, field, claim and wiki page in the dist."""
    out = {}
    for folder in sorted(path for path in (dist / "claims").glob("*") if path.is_dir()):
        out[f"clm:{folder.name}"] = f"claims/{folder.name}/"
    for folder in sorted(path for path in (dist / "fields").glob("*") if path.is_dir()):
        out[f"field:{folder.name}"] = f"fields/{folder.name}/"
    for folder in sorted(path for path in (dist / "e").glob("*/*") if path.is_dir()):
        out[f"{folder.parent.name}:{folder.name}"] = f"e/{folder.parent.name}/{folder.name}/"
    for folder in sorted(path for path in (dist / "wiki").glob("*") if path.is_dir()):
        out[f"wiki:{folder.name}"] = f"wiki/{folder.name}/"
    return out


def check_public_pages(dist: Path, expected: dict, report: Report) -> None:
    """V-PUBLIC: every record page belongs to the allow-list (redirect stubs of merged ids excepted)."""
    allowed = set(expected["entities"]) | set(expected["claims"]) | set(expected["wiki"])
    for ident, folder in emitted_ids(dist).items():
        if ident in allowed:
            continue
        text = (dist / folder / "index.html").read_text(encoding="utf8", errors="replace")
        if 'http-equiv="refresh"' not in text:
            report.error("V-PUBLIC", folder, f"{ident} is published but not in the public gate")


def check_public_json(dist: Path, expected: dict, report: Report) -> None:
    """V-PUBLIC: graph.json and node-index.json list only allow-listed nodes and claims."""
    entities, claims = set(expected["entities"]), set(expected["claims"])
    graph_json = dist / "graph.json"
    if graph_json.is_file():
        data = json.loads(graph_json.read_text(encoding="utf8"))
        if data.get("build") not in (None, "public"):
            report.error("V-PUBLIC", "graph.json", f"build is {data.get('build')!r}, expected 'public'")
        for node in data.get("nodes", []):
            if node.get("id") not in entities:
                report.error("V-PUBLIC", "graph.json", f"node {node.get('id')} is not in the public gate")
        for edge in data.get("edges", []):
            if edge.get("kind") == "claim" and edge.get("id") not in claims:
                report.error("V-PUBLIC", "graph.json", f"edge {edge.get('id')} is not in the public gate")
            if edge.get("source") not in entities or edge.get("target") not in entities:
                report.error("V-PUBLIC", "graph.json", f"edge {edge.get('id')} touches a non-public node")
    index = dist / "node-index.json"
    if index.is_file():
        for node in json.loads(index.read_text(encoding="utf8")):
            if node.get("id") not in entities:
                report.error("V-PUBLIC", "node-index.json", f"{node.get('id')} is not in the public gate")


PROSE_KEYS = ("summary", "question", "note", "rationale", "prompt", "description", "classification_note")
MIN_TAINT_LENGTH = 25


def prose_of(record: dict) -> set[str]:
    """Prose strings of a record (and its evidence) that only a human approval may publish."""
    out = {str(record.get(key)).strip() for key in PROSE_KEYS if isinstance(record.get(key), str)}
    for evidence in record.get("evidence") or []:
        out |= {str(evidence.get(key)).strip() for key in ("quote", "rationale") if isinstance(evidence.get(key), str)}
    return {text for text in out if len(text) >= MIN_TAINT_LENGTH}


def wiki_plain(body: str) -> str:
    """MDX body with tags, math and code removed."""
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    body = re.sub(r"\$\$.*?\$\$|\$[^$\n]*\$", " ", body, flags=re.S)
    return re.sub(r"<[^>]+>|\*\*|`", " ", body)


def wiki_sentences(body: str) -> set[str]:
    """Plain sentences of an MDX body (tags, math and code removed) for the taint test."""
    parts = re.split(r"(?<=[.!?다요])\s+|\n+", wiki_plain(body))
    return {re.sub(r"\s+", " ", part).strip() for part in parts if len(part.strip()) >= MIN_TAINT_LENGTH}


def check_taint(dist: Path, pages: dict[Path, str], paths: list[str], wiki_dir: str, expected: dict, report: Report) -> None:
    """V-PUBLIC taint test: no prose of a record outside the gate appears anywhere in the public output."""
    graph = load_graph(paths)
    public = set(expected["entities"]) | set(expected["claims"]) | set(expected["sources"])
    hidden, shown = set(), set()
    for ident, record in graph["entities"].items():
        (shown if ident in public else hidden).update(prose_of(record))
    public_wiki = []
    for path in sorted(Path(wiki_dir).glob("*.mdx")):
        meta, body = public_gate.read_wiki(path)
        (shown if meta.get("id") in expected["wiki"] else hidden).update(wiki_sentences(body))
        if meta.get("id") in expected["wiki"]:
            public_wiki.append(re.sub(r"\s+", " ", wiki_plain(body)))
    # A public wiki may quote a paper sentence that is also a hidden claim's evidence: text that is
    # already part of public prose is not a leak.
    public_text = "\n".join([*public_wiki, *shown])
    forbidden = {text for text in hidden - shown if re.sub(r"\s+", " ", text) not in public_text}
    haystacks = {page.relative_to(dist).as_posix(): html.unescape(text) for page, text in pages.items()}
    for name in ("graph.json", "node-index.json"):
        if (dist / name).is_file():
            haystacks[name] = (dist / name).read_text(encoding="utf8")
    leaks = [(name, text) for name, hay in sorted(haystacks.items()) for text in forbidden if text in hay]
    for name, text in leaks[:MAX_LISTED_FINDINGS]:
        report.error("V-PUBLIC", name, f"shows text of a non-public record: {text[:60]}…")
    if len(leaks) > MAX_LISTED_FINDINGS:
        report.error("V-PUBLIC", "(many)", f"{len(leaks) - MAX_LISTED_FINDINGS} more leaks")


def collect_pages(dist: Path) -> dict[Path, str]:
    """Read every HTML page of the dist (the pagefind and _astro folders hold no pages)."""
    pages = {}
    for page in sorted(dist.rglob("*.html")):
        top = page.relative_to(dist).parts[0]
        if top in SKIPPED_DIRECTORIES:
            continue
        pages[page] = page.read_text(encoding="utf8", errors="replace")
    return pages


def build_parser() -> argparse.ArgumentParser:
    """Return the command line parser."""
    parser = argparse.ArgumentParser(description="Audit a built AIXON site (V-DIST-LINK, V-SEO, V-MATH, V-NO-CDN, V-PUBLIC).")
    parser.add_argument("dist", help="build output directory, e.g. dist")
    parser.add_argument("--base", default=os.getenv("AIXON_BASE", "/"), help="deployment base path, e.g. /aixon/")
    parser.add_argument("--mode", choices=("preview", "public"), default="preview")
    parser.add_argument("--site", default=os.getenv("AIXON_SITE"), help="site origin, e.g. https://user.github.io")
    parser.add_argument("--graph", default=os.getenv("AIXON_GRAPH", DEFAULT_GRAPH), help="graph YAML files (public mode)")
    parser.add_argument("--wiki-dir", default=os.getenv("AIXON_WIKI_DIR", DEFAULT_WIKI_DIR), help="wiki MDX folder (public mode)")
    parser.add_argument("--gate", help="public-gate.json the build used (public mode): must match a fresh gate run")
    parser.add_argument("--json", action="store_true", help="print a JSON report instead of text")
    return parser


def normalize_base(base: str) -> str:
    """Return base with exactly one leading and one trailing slash."""
    return "/" + base.strip("/") + "/" if base.strip("/") else "/"


def main(argv: list[str] | None = None) -> int:
    """Audit the dist and print the report."""
    args = build_parser().parse_args(argv)
    args.base = normalize_base(args.base)
    if args.site:
        args.site = args.site.rstrip("/").lower()  # scheme and host are case-insensitive; Astro writes them lowercase
    dist = Path(args.dist)
    if not dist.is_dir():
        print(f"error: dist directory not found: {dist}", file=sys.stderr)
        return 2
    if args.mode == "public" and not any(Path(item.strip()).exists() for item in args.graph.split(",")):
        print(f"error: public mode needs an existing --graph, got {args.graph!r}", file=sys.stderr)
        return 2
    report = Report()
    pages = collect_pages(dist)
    check_required_files(dist, report)
    for page, text in pages.items():
        check_page(dist, page, text, args, report)
    check_css_files(dist, report)
    check_sitemap(dist, args, report)
    check_robots(dist, args, report)
    if args.mode == "public":
        check_public(dist, pages, args, report)
    summary = {
        "dist": str(dist),
        "mode": args.mode,
        "base": args.base,
        "site": args.site,
        "pages": len(pages),
        "errors": [item.as_dict() for item in report.errors],
        "warnings": [item.as_dict() for item in report.warnings],
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        for item in report.findings:
            print(f"{item.level.upper()} {item.code} {item.file}: {item.message}")
        status = "OK" if not report.errors else f"{len(report.errors)} error(s)"
        print(f"check-dist {args.mode} {dist}: {len(pages)} page(s), {status}")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
