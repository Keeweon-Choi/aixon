#!/usr/bin/env python3
"""Validate Wiki MDX documents against docs/CONTENT_SCHEMA.md.

Implements the content rules of docs/CONTENT_VALIDATION_PLAN.md (layer L-C):

    V-SCHEMA-1  frontmatter follows CONTENT_SCHEMA section 2 (fields, enums, graph references)
    V-SCHEMA-2  file name slug == id slug == entity slug, one wiki per entity
    V-SCHEMA-3  frontmatter `sections` == the `<Section id>` set of the body, level values valid
    V-LINK-1    every <ConceptLink id> is an entity of the graph
    V-CITE-1    every <Cite src|claim> target exists in the graph
    V-CITE-2    math / mechanism / history sections contain a <Cite> (status above outline)
    V-CITE-3    every cited Source / Claim is listed in the frontmatter `sources` / `claims`
    V-STATUS-1  reviewed / published need a human approval, published needs published_at
    V-STATUS-2  an AI generated document is never reviewed by an agent
    V-STATUS-3  citing a rejected / deprecated claim is an error, proposed / disputed a warning
    V-CODE-1    every ```python verify block runs and passes (20 s limit, numpy only)
    V-FIG-1     every <Figure id> is listed in `figures` with origin self-made and an alt text
    V-LABREF-1  `labs` ids exist in the graph and every <Lab id> is listed in `labs`

Usage:
    validate_content.py [--wiki-dir DIR] [--graph a.yaml,b.yaml] [--json]

Defaults come from AIXON_WIKI_DIR / AIXON_GRAPH, then src/content/wiki and
data/seed/seed_graph.yaml,data/graph/atlas.yaml. Exit code: 0 ok, 1 rule errors, 2 bad setup.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from seedtool import load_graph

DEFAULT_GRAPH = "data/seed/seed_graph.yaml,data/graph/atlas.yaml"
DEFAULT_WIKI_DIR = "src/content/wiki"
VERIFY_TIMEOUT_SECONDS = 20

STATUSES = ("outline", "draft", "reviewed", "published")
LEVELS = ("intuition", "fundamentals", "deep")
SECTION_IDS = (
    "overview",
    "why",
    "mechanism",
    "math",
    "example",
    "code",
    "visual",
    "limitations",
    "history",
    "related",
    "references",
)
CITE_REQUIRED_SECTIONS = ("math", "mechanism", "history")
AUTHOR_ROLES = ("draft", "edit", "review")
REQUIRED_FIELDS = (
    "id",
    "entity",
    "title",
    "subtitle",
    "status",
    "levels",
    "sections",
    "authors",
    "ai_generated",
    "review",
    "published_at",
    "sources",
    "claims",
    "labs",
    "figures",
    "updated_at",
)

WIKI_ID_RE = re.compile(r"^wiki:[a-z0-9]+(?:-[a-z0-9]+)*$")
ENTITY_ID_RE = re.compile(r"^[a-z]+:[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)(.*)\Z", re.S)
FENCE_RE = re.compile(r"^(?P<fence>`{3,}|~{3,})[^\n]*\n.*?^(?P=fence)[ \t]*$", re.S | re.M)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
VERIFY_BLOCK_RE = re.compile(r"^```python[ \t]+verify[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
ATTRIBUTE_RE = re.compile(r"([A-Za-z_][\w:.-]*)\s*=\s*(?:\"([^\"]*)\"|'([^']*)')")
SECTION_BLOCK_RE = re.compile(r"<Section\b((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>(.*?)</Section>", re.S)

# Graph entity types that are not "concepts": they cannot be the target of a ConceptLink or an entity.
NON_ENTITY_TYPES = ("Claim", "Source")


@dataclass
class Issue:
    """One rule violation (error) or advisory (warning)."""

    level: str
    code: str
    file: str
    line: int
    message: str

    def as_dict(self) -> dict[str, Any]:
        """Return the JSON-report form of this issue."""
        return {
            "level": self.level,
            "code": self.code,
            "file": self.file,
            "line": self.line,
            "message": self.message,
        }


@dataclass
class Tag:
    """A component tag found in an MDX body, e.g. <Cite claim="clm:x" />."""

    name: str
    attributes: dict[str, str]
    line: int


@dataclass
class Document:
    """A parsed MDX file: frontmatter mapping, body text and where the body starts."""

    path: Path
    meta: dict[str, Any]
    body: str
    body_start_line: int
    source_lines: list[str] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)

    @property
    def name(self) -> str:
        """Return the file name used in reports."""
        return self.path.name

    def report(self, code: str, message: str, line: int = 1, warning: bool = False) -> None:
        """Record an issue for this document."""
        level = "warning" if warning else "error"
        self.issues.append(Issue(level, code, self.name, line, message))

    def line_of_key(self, key: str) -> int:
        """Return the 1-based line of a top-level frontmatter key (1 when not found)."""
        for number, text in enumerate(self.source_lines, start=1):
            if text.startswith(f"{key}:"):
                return number
        return 1


class GraphIndex:
    """Lookup of the ids a document may reference."""

    def __init__(self, graph: dict[str, Any]) -> None:
        self.entities: dict[str, Any] = graph["entities"]
        self.types: dict[str, str] = graph["types"]
        self.claims: dict[str, Any] = graph["claims"]
        self.sources: dict[str, Any] = graph["sources"]

    def is_entity(self, ident: str) -> bool:
        """Return True for ids of concepts, methods, models, fields, problems and papers."""
        return ident in self.entities and self.types.get(ident) not in NON_ENTITY_TYPES

    def is_lab(self, ident: str) -> bool:
        """Return True when ident is a LabExperiment."""
        return self.types.get(ident) == "LabExperiment"


def parse_document(path: Path) -> Document:
    """Split an MDX file into frontmatter and body, recording YAML problems as issues."""
    text = path.read_text(encoding="utf8")
    lines = text.splitlines()
    match = FRONTMATTER_RE.match(text)
    if match is None:
        document = Document(path, {}, text, 1, lines)
        document.report("V-SCHEMA-1", "the file has no YAML frontmatter block")
        return document
    meta_text, body = match.group(1), match.group(2)
    body_start_line = text[: match.start(2)].count("\n") + 1
    document = Document(path, {}, body, body_start_line, lines)
    try:
        loaded = yaml.safe_load(meta_text)
    except yaml.YAMLError as error:
        document.report("V-SCHEMA-1", f"frontmatter is not valid YAML: {error}")
        return document
    if not isinstance(loaded, dict):
        document.report("V-SCHEMA-1", "frontmatter must be a YAML mapping")
        return document
    document.meta = loaded
    return document


def blank_out(match: re.Match[str]) -> str:
    """Replace a matched text by spaces, keeping newlines so offsets and line numbers survive."""
    return re.sub(r"[^\n]", " ", match.group(0))


def mask_code(body: str) -> str:
    """Blank fenced code blocks and inline code so component tags inside code are ignored."""
    without_fences = FENCE_RE.sub(blank_out, body)
    return INLINE_CODE_RE.sub(blank_out, without_fences)


def parse_attributes(text: str) -> dict[str, str]:
    """Parse string-literal JSX attributes (name="value" or name='value')."""
    attributes: dict[str, str] = {}
    for name, double_quoted, single_quoted in ATTRIBUTE_RE.findall(text):
        attributes[name] = double_quoted or single_quoted
    return attributes


def find_tags(document: Document, masked: str, name: str) -> list[Tag]:
    """Return every <Name ...> tag of the body (code excluded) with its attributes and line."""
    pattern = re.compile(rf"<{name}\b((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>")
    tags = []
    for match in pattern.finditer(masked):
        line = document.body_start_line + masked.count("\n", 0, match.start())
        tags.append(Tag(name, parse_attributes(match.group(1)), line))
    return tags


def is_date_like(value: Any) -> bool:
    """Return True for YAML dates and YYYY-MM-DD strings."""
    if isinstance(value, (date, datetime)):
        return True
    return isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is not None


def check_frontmatter_fields(document: Document, graph: GraphIndex) -> bool:
    """V-SCHEMA-1: required fields, types, enums and graph references. Return True when sound."""
    meta = document.meta
    problems_before = len(document.issues)
    for name in REQUIRED_FIELDS:
        if name not in meta:
            document.report("V-SCHEMA-1", f"missing frontmatter field: {name}")
    if len(document.issues) > problems_before:
        return False

    def bad(key: str, message: str) -> None:
        document.report("V-SCHEMA-1", f"{key}: {message}", document.line_of_key(key))

    if not (isinstance(meta["id"], str) and WIKI_ID_RE.match(meta["id"])):
        bad("id", "must match ^wiki:[a-z0-9]+(-[a-z0-9]+)*$")
    if not (isinstance(meta["entity"], str) and ENTITY_ID_RE.match(meta["entity"])):
        bad("entity", "must be an entity id such as method:scaled-dot-product-attention")
    elif not graph.is_entity(meta["entity"]):
        bad("entity", f"unknown entity {meta['entity']}")
    for key in ("title", "subtitle"):
        if not (isinstance(meta[key], str) and meta[key].strip()):
            bad(key, "must be a non-empty string")
    if meta["status"] not in STATUSES:
        bad("status", f"must be one of {', '.join(STATUSES)}")
    check_levels(meta["levels"], bad)
    check_section_list(meta["sections"], bad)
    check_authors(meta["authors"], meta["ai_generated"], bad)
    check_review_shape(meta["review"], bad)
    if meta["published_at"] is not None and not is_date_like(meta["published_at"]):
        bad("published_at", "must be null or a YYYY-MM-DD date")
    if not is_date_like(meta["updated_at"]):
        bad("updated_at", "must be a YYYY-MM-DD date")
    check_reference_list("sources", meta["sources"], graph.sources, bad)
    check_reference_list("claims", meta["claims"], graph.claims, bad)
    check_reference_list("labs", meta["labs"], None, bad)  # existence is V-LABREF-1
    check_figure_shape(meta["figures"], bad)
    return len(document.issues) == problems_before


def check_levels(levels: Any, bad) -> None:
    """V-SCHEMA-1: levels is a non-empty ordered subset of intuition, fundamentals, deep."""
    if not isinstance(levels, list) or not levels:
        bad("levels", "must be a non-empty list")
    elif any(level not in LEVELS for level in levels):
        bad("levels", f"values must be among {', '.join(LEVELS)}")
    elif levels != sorted(set(levels), key=LEVELS.index):
        bad("levels", "must be unique and ordered intuition, fundamentals, deep")


def check_section_list(sections: Any, bad) -> None:
    """V-SCHEMA-1: sections is a non-empty list of known section ids without duplicates."""
    if not isinstance(sections, list) or not sections:
        bad("sections", "must be a non-empty list")
    elif any(item not in SECTION_IDS for item in sections):
        bad("sections", f"ids must be among {', '.join(SECTION_IDS)}")
    elif len(set(sections)) != len(sections):
        bad("sections", "must not repeat an id")


def check_authors(authors: Any, ai_generated: Any, bad) -> None:
    """V-SCHEMA-1: authors have agent:/human: ids and roles; agent authors imply ai_generated."""
    if not isinstance(ai_generated, bool):
        bad("ai_generated", "must be true or false")
    if not isinstance(authors, list) or not authors:
        bad("authors", "must be a non-empty list")
        return
    has_agent = False
    for author in authors:
        ident = author.get("id") if isinstance(author, dict) else None
        role = author.get("role") if isinstance(author, dict) else None
        if not (isinstance(ident, str) and re.match(r"^(agent|human):\S+$", ident)):
            bad("authors", "each author needs an id like agent:<model> or human:<handle>")
        elif ident.startswith("agent:"):
            has_agent = True
        if role not in AUTHOR_ROLES:
            bad("authors", f"each author role must be one of {', '.join(AUTHOR_ROLES)}")
    if has_agent and ai_generated is not True:
        bad("ai_generated", "must be true when an agent is listed as an author")


def check_review_shape(review: Any, bad) -> None:
    """V-SCHEMA-1: review is null or {by, at, decision: approve, note}."""
    if review is None:
        return
    if not isinstance(review, dict):
        bad("review", "must be null or a mapping with by, at, decision, note")
        return
    for key in ("by", "at", "decision", "note"):
        if key not in review:
            bad("review", f"missing key {key}")
    if "at" in review and not is_date_like(review["at"]):
        bad("review", "at must be a YYYY-MM-DD date")
    if "decision" in review and review["decision"] != "approve":
        bad("review", "decision must be approve")


def check_reference_list(key: str, values: Any, known: dict[str, Any] | None, bad) -> None:
    """V-SCHEMA-1: a list of ids; when `known` is given, every id must exist in the graph."""
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        bad(key, "must be a list of ids")
        return
    for ident in values:
        if known is not None and ident not in known:
            bad(key, f"unknown id {ident}")


def check_figure_shape(figures: Any, bad) -> None:
    """V-SCHEMA-1: figures is a list of mappings with an id (origin and alt are V-FIG-1)."""
    if not isinstance(figures, list):
        bad("figures", "must be a list")
        return
    for figure in figures:
        if not (isinstance(figure, dict) and isinstance(figure.get("id"), str)):
            bad("figures", "each figure needs an id")


def check_names(document: Document) -> None:
    """V-SCHEMA-2: file name slug, id slug and entity slug are the same."""
    meta = document.meta
    file_slug = document.path.stem
    id_slug = str(meta["id"]).split(":", 1)[-1]
    entity_slug = str(meta["entity"]).split(":", 1)[-1]
    if not (file_slug == id_slug == entity_slug):
        document.report(
            "V-SCHEMA-2",
            f"slugs differ: file '{file_slug}', id '{id_slug}', entity '{entity_slug}'",
        )


def check_unique_entities(documents: list[Document]) -> None:
    """V-SCHEMA-2: at most one wiki document per entity."""
    first_owner: dict[str, str] = {}
    for document in documents:
        entity = document.meta.get("entity")
        if not isinstance(entity, str):
            continue
        if entity in first_owner:
            message = f"entity {entity} already has a wiki: {first_owner[entity]}"
            document.report("V-SCHEMA-2", message)
        else:
            first_owner[entity] = document.name


def check_sections(document: Document, masked: str, frontmatter_ok: bool) -> None:
    """V-SCHEMA-3: section ids and levels, and agreement with the frontmatter `sections`."""
    found: list[str] = []
    for match in SECTION_BLOCK_RE.finditer(masked):
        line = document.body_start_line + masked.count("\n", 0, match.start())
        attributes = parse_attributes(match.group(1))
        ident, level, title = attributes.get("id"), attributes.get("level"), attributes.get("title")
        if ident not in SECTION_IDS:
            document.report("V-SCHEMA-3", f"<Section> has an invalid id: {ident!r}", line)
            continue
        if level not in LEVELS:
            document.report("V-SCHEMA-3", f"<Section id={ident}> has an invalid level: {level!r}", line)
        if not title:
            document.report("V-SCHEMA-3", f"<Section id={ident}> needs a title", line)
        if ident in found:
            document.report("V-SCHEMA-3", f"<Section id={ident}> appears twice", line)
        found.append(ident)
    for tag in find_tags(document, masked, "Level"):
        if tag.attributes.get("of") not in LEVELS:
            message = f"<Level> has an invalid 'of': {tag.attributes.get('of')!r}"
            document.report("V-SCHEMA-3", message, tag.line)
    if frontmatter_ok:
        listed = set(document.meta["sections"])
        missing_in_body = sorted(listed - set(found))
        missing_in_meta = sorted(set(found) - listed)
        if missing_in_body or missing_in_meta:
            message = (
                "frontmatter sections do not match the body <Section> ids "
                f"(only in frontmatter: {missing_in_body}, only in body: {missing_in_meta})"
            )
            document.report("V-SCHEMA-3", message, document.line_of_key("sections"))


def check_concept_links(document: Document, graph: GraphIndex, masked: str) -> None:
    """V-LINK-1: every ConceptLink points to an entity of the graph."""
    for tag in find_tags(document, masked, "ConceptLink"):
        ident = tag.attributes.get("id", "")
        if not graph.is_entity(ident):
            document.report("V-LINK-1", f"<ConceptLink> targets an unknown entity: {ident!r}", tag.line)


def check_cites(document: Document, graph: GraphIndex, masked: str, frontmatter_ok: bool) -> None:
    """V-CITE-1, V-CITE-3 and V-STATUS-3 for every <Cite>."""
    for tag in find_tags(document, masked, "Cite"):
        source, claim = tag.attributes.get("src"), tag.attributes.get("claim")
        if (source is None) == (claim is None):
            document.report("V-CITE-1", "<Cite> needs exactly one of src= or claim=", tag.line)
            continue
        ident = source if source is not None else claim
        known = graph.sources if source is not None else graph.claims
        if ident not in known:
            kind = "Source" if source is not None else "Claim"
            document.report("V-CITE-1", f"<Cite> targets an unknown {kind}: {ident}", tag.line)
            continue
        if frontmatter_ok:
            listed = document.meta["sources" if source is not None else "claims"]
            if ident not in listed:
                key = "sources" if source is not None else "claims"
                document.report("V-CITE-3", f"{ident} is cited but not listed in frontmatter {key}", tag.line)
        if claim is not None:
            check_claim_status(document, graph, claim, tag.line)


def check_claim_status(document: Document, graph: GraphIndex, claim: str, line: int) -> None:
    """V-STATUS-3: rejected / deprecated claims are errors, proposed / disputed are warnings."""
    status = graph.claims[claim].get("status")
    if status in ("rejected", "deprecated"):
        document.report("V-STATUS-3", f"cites {status} claim {claim}", line)
    elif status in ("proposed", "disputed"):
        document.report("V-STATUS-3", f"cites {status} claim {claim}", line, warning=True)


def check_cite_coverage(document: Document, masked: str) -> None:
    """V-CITE-2: math, mechanism and history sections of a non-outline document cite something."""
    if document.meta.get("status") == "outline":
        return
    for match in SECTION_BLOCK_RE.finditer(masked):
        attributes = parse_attributes(match.group(1))
        ident = attributes.get("id")
        if ident in CITE_REQUIRED_SECTIONS and "<Cite" not in match.group(2):
            line = document.body_start_line + masked.count("\n", 0, match.start())
            document.report("V-CITE-2", f"section '{ident}' needs at least one <Cite>", line)


def check_status(document: Document) -> None:
    """V-STATUS-1 and V-STATUS-2: what reviewed and published documents must have."""
    meta = document.meta
    status, review = meta["status"], meta["review"]
    if status not in ("reviewed", "published"):
        return
    line = document.line_of_key("status")
    if review is None:
        document.report("V-STATUS-1", f"status {status} needs a human review (review is null)", line)
    else:
        reviewer = str(review.get("by", ""))
        if not reviewer.startswith("human:"):
            if meta["ai_generated"]:
                message = f"AI generated document reviewed by non-human '{reviewer}'"
                document.report("V-STATUS-2", message, document.line_of_key("review"))
            else:
                message = f"status {status} needs a review by a human:<handle>, got '{reviewer}'"
                document.report("V-STATUS-1", message, document.line_of_key("review"))
    if status == "published" and not meta["published_at"]:
        document.report("V-STATUS-1", "status published needs published_at", line)


def check_figures(document: Document, masked: str, frontmatter_ok: bool) -> None:
    """V-FIG-1: used figures are listed as self-made with an alt text."""
    if not frontmatter_ok:
        return
    listed = {item["id"]: item for item in document.meta["figures"]}
    for ident, item in listed.items():
        if item.get("origin") != "self-made":
            document.report("V-FIG-1", f"figure {ident} must have origin: self-made")
        if not str(item.get("alt", "")).strip():
            document.report("V-FIG-1", f"figure {ident} needs a non-empty alt text")
    for tag in find_tags(document, masked, "Figure"):
        ident = tag.attributes.get("id", "")
        if ident not in listed:
            document.report("V-FIG-1", f"<Figure id={ident}> is not listed in frontmatter figures", tag.line)


def check_labs(document: Document, graph: GraphIndex, masked: str, frontmatter_ok: bool) -> None:
    """V-LABREF-1: `labs` ids exist, and every <Lab id> exists and is listed in `labs`."""
    listed = document.meta["labs"] if frontmatter_ok else []
    for ident in listed:
        if not graph.is_lab(ident):
            document.report("V-LABREF-1", f"frontmatter labs lists an unknown lab: {ident}")
    for tag in find_tags(document, masked, "Lab"):
        ident = tag.attributes.get("id", "")
        if not graph.is_lab(ident):
            document.report("V-LABREF-1", f"<Lab> targets an unknown lab: {ident!r}", tag.line)
        elif frontmatter_ok and ident not in listed:
            document.report("V-LABREF-1", f"<Lab id={ident}> is not listed in frontmatter labs", tag.line)


def disallowed_imports(code: str) -> list[str]:
    """Return imported top-level modules that are neither numpy nor the standard library."""
    names: set[str] = set()
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    allowed = set(sys.stdlib_module_names) | {"numpy"}
    return sorted(names - allowed)


def run_verify_block(code: str) -> str | None:
    """Run one verify block in an empty temp dir. Return an error text, or None on success."""
    try:
        forbidden = disallowed_imports(code)
    except SyntaxError as error:
        return f"syntax error: {error}"
    if forbidden:
        return f"imports {', '.join(forbidden)}; only numpy and the standard library are allowed"
    environment = {"PATH": os.environ.get("PATH", "")}
    with tempfile.TemporaryDirectory() as directory:
        script = Path(directory) / "verify_block.py"
        script.write_text(code, encoding="utf8")
        try:
            result = subprocess.run(
                [sys.executable, "-I", "-B", str(script)],
                cwd=directory,
                env=environment,
                capture_output=True,
                text=True,
                timeout=VERIFY_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return f"timed out after {VERIFY_TIMEOUT_SECONDS} s"
    if result.returncode == 0:
        return None
    output = (result.stderr or result.stdout).strip().splitlines()
    return " | ".join(output[-3:])[-300:] or f"exit code {result.returncode}"


def check_verify_blocks(document: Document) -> None:
    """V-CODE-1: every ```python verify block runs and passes."""
    for match in VERIFY_BLOCK_RE.finditer(document.body):
        line = document.body_start_line + document.body.count("\n", 0, match.start())
        error = run_verify_block(match.group(1))
        if error is not None:
            document.report("V-CODE-1", f"verify block failed: {error}", line)


def validate_document(document: Document, graph: GraphIndex) -> None:
    """Run every rule on one parsed document."""
    masked = mask_code(document.body)
    frontmatter_ok = False
    if document.meta:
        frontmatter_ok = check_frontmatter_fields(document, graph)
    if frontmatter_ok:
        check_names(document)
        check_status(document)
        check_cite_coverage(document, masked)
    check_sections(document, masked, frontmatter_ok)
    check_concept_links(document, graph, masked)
    check_cites(document, graph, masked, frontmatter_ok)
    check_figures(document, masked, frontmatter_ok)
    check_labs(document, graph, masked, frontmatter_ok)
    check_verify_blocks(document)


def load_graph_index(spec: str) -> tuple[GraphIndex, list[str]]:
    """Load the comma-separated graph files. Raise ValueError when none exists or ids repeat."""
    paths = [item.strip() for item in spec.split(",") if item.strip()]
    existing = []
    for item in paths:
        if Path(item).exists():
            existing.append(item)
        else:
            print(f"warning: graph file skipped (not found): {item}", file=sys.stderr)
    if not existing:
        raise ValueError(f"no graph file found in --graph {spec!r}")
    graph = load_graph(existing)
    seen: set[str] = set()
    for _section, _type, record in graph["records"]:
        ident = record.get("id")
        if ident in seen:
            raise ValueError(f"duplicate graph id: {ident}")
        seen.add(ident)
    return GraphIndex(graph), existing


def build_parser() -> argparse.ArgumentParser:
    """Return the command line parser."""
    parser = argparse.ArgumentParser(description="Validate Wiki MDX documents (V-* content rules).")
    parser.add_argument("--wiki-dir", default=os.getenv("AIXON_WIKI_DIR", DEFAULT_WIKI_DIR))
    parser.add_argument("--graph", default=os.getenv("AIXON_GRAPH", DEFAULT_GRAPH))
    parser.add_argument("--json", action="store_true", help="print a JSON report instead of text")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Validate every *.mdx file of the wiki directory and print a report."""
    args = build_parser().parse_args(argv)
    wiki_dir = Path(args.wiki_dir)
    if not wiki_dir.is_dir():
        print(f"error: wiki directory not found: {wiki_dir}", file=sys.stderr)
        return 2
    try:
        graph, graph_files = load_graph_index(args.graph)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    documents = [parse_document(path) for path in sorted(wiki_dir.glob("*.mdx"))]
    for document in documents:
        validate_document(document, graph)
    check_unique_entities(documents)
    issues = [issue for document in documents for issue in document.issues]
    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]
    if args.json:
        report = {
            "graph": graph_files,
            "wiki_dir": str(wiki_dir),
            "documents": len(documents),
            "errors": [issue.as_dict() for issue in errors],
            "warnings": [issue.as_dict() for issue in warnings],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for issue in issues:
            print(f"{issue.level.upper()} {issue.code} {issue.file}:{issue.line}: {issue.message}")
        summary = f"{len(errors)} error(s), {len(warnings)} warning(s) in {len(documents)} document(s)"
        print(summary)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
