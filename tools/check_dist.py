#!/usr/bin/env python3
"""Audit a built static site (the output of `astro build` + `pagefind`).

Rules (docs/CONTENT_VALIDATION_PLAN.md layer L-B):

    V-DIST-LINK  every internal href/src resolves to a file once the deployment base is stripped
    V-SEO        every page has lang="ko", a title, a meta description and exactly one h1;
                 sitemap-index.xml and robots.txt exist and agree with the mode
    V-MATH       no `katex-error`; every `.katex` contains MathML
    V-NO-CDN     no external <script src> / stylesheet (HTML and CSS)
    V-PUBLIC     (--mode public) nothing that lacks a human approval is published

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

import yaml

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


def human_approved(record: dict, key: str = "review") -> bool:
    """Return True when record[key] is an approval by a human."""
    review = record.get(key) or {}
    return review.get("decision") == "approve" and str(review.get("by", "")).startswith("human:")


def unapproved_ai_summaries(graph: dict) -> dict[str, str]:
    """Return {summary text: entity id} for AI written summaries without a human approval."""
    approved_texts = set()
    forbidden: dict[str, str] = {}
    for ident, record in graph["entities"].items():
        if graph["types"][ident] in ("Claim", "Source"):
            continue
        summary = str(record.get("summary") or "").strip()
        if not summary:
            continue
        written_by_agent = str(record.get("summary_by", "")).startswith("agent:")
        if written_by_agent and not human_approved(record, "summary_review"):
            forbidden[summary] = ident
        else:
            approved_texts.add(summary)
    return {text: ident for text, ident in forbidden.items() if text not in approved_texts and len(text) >= 6}


def check_public(dist: Path, pages: dict[Path, str], args: argparse.Namespace, report: Report) -> None:
    """V-PUBLIC: nothing without a human approval may be published."""
    graph = load_graph([item.strip() for item in args.graph.split(",") if Path(item.strip()).exists()])
    for page, text in pages.items():
        if DRAFT_BANNER in text:
            report.error("V-PUBLIC", page.relative_to(dist).as_posix(), f"public page contains '{DRAFT_BANNER}'")
    check_public_claims(dist, graph, report)
    check_public_wiki(dist, Path(args.wiki_dir), report)
    check_public_summaries(dist, pages, graph, report)


def check_public_claims(dist: Path, graph: dict, report: Report) -> None:
    """V-PUBLIC: claim pages and graph.json edges all belong to human-approved claims."""
    claims = graph["claims"]
    claims_dir = dist / "claims"
    if claims_dir.is_dir():
        for folder in sorted(path for path in claims_dir.iterdir() if path.is_dir()):
            claim = claims.get(f"clm:{folder.name}")
            if claim is None or not human_approved(claim):
                report.error("V-PUBLIC", f"claims/{folder.name}/", "claim page without a human approval in the graph")
    graph_json = dist / "graph.json"
    if not graph_json.is_file():
        return
    data = json.loads(graph_json.read_text(encoding="utf8"))
    for edge in data.get("edges", []):
        if edge.get("kind") != "claim":
            continue
        claim = claims.get(edge.get("id", ""))
        if claim is None or not human_approved(claim):
            report.error("V-PUBLIC", "graph.json", f"edge {edge.get('id')} is not a human-approved claim")
    if data.get("build") not in (None, "public"):
        report.error("V-PUBLIC", "graph.json", f"build is {data.get('build')!r}, expected 'public'")


def check_public_wiki(dist: Path, wiki_dir: Path, report: Report) -> None:
    """V-PUBLIC: every emitted wiki page is a published, human-reviewed document."""
    wiki_pages = dist / "wiki"
    if not wiki_pages.is_dir():
        return
    for folder in sorted(path for path in wiki_pages.iterdir() if path.is_dir()):
        source = wiki_dir / f"{folder.name}.mdx"
        meta = read_frontmatter(source)
        approved = meta.get("status") == "published" and human_approved(meta)
        if not approved:
            report.error("V-PUBLIC", f"wiki/{folder.name}/", f"wiki page without a published, human-reviewed {source}")


def read_frontmatter(path: Path) -> dict:
    """Return the YAML frontmatter of an MDX file ({} when missing or unreadable)."""
    if not path.is_file():
        return {}
    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---", path.read_text(encoding="utf8"), re.S)
    if match is None:
        return {}
    try:
        loaded = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def check_public_summaries(dist: Path, pages: dict[Path, str], graph: dict, report: Report) -> None:
    """V-PUBLIC: AI summaries without a human approval never reach pages, graph.json or node-index.json."""
    forbidden = unapproved_ai_summaries(graph)
    haystacks = {page.relative_to(dist).as_posix(): html.unescape(text) for page, text in pages.items()}
    for name in ("graph.json", "node-index.json"):
        path = dist / name
        if path.is_file():
            haystacks[name] = path.read_text(encoding="utf8")
    leaks = []
    for name, text in sorted(haystacks.items()):
        for summary, ident in forbidden.items():
            if summary in text:
                leaks.append((name, f"shows the unapproved AI summary of {ident}"))
                break
    for name, message in leaks[:MAX_LISTED_FINDINGS]:
        report.error("V-PUBLIC", name, message)
    if len(leaks) > MAX_LISTED_FINDINGS:
        report.error("V-PUBLIC", "(many)", f"{len(leaks) - MAX_LISTED_FINDINGS} more files show unapproved AI summaries")


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
        args.site = args.site.rstrip("/")
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
