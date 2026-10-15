"""tools/check_dist.py on tiny hand-made dist trees: one clean tree per mode, one broken tree per rule."""

from __future__ import annotations

import json

import pytest
from conftest import FIXTURE_GRAPH, FIXTURE_WIKI

SITE = "http://127.0.0.1:4329"
BASE = "/aixon/"
TRANSFORMER_SUMMARY = "(fixture) 어텐션만으로 시퀀스를 변환하는 모델 계열이다."  # human-approved in the fixture
VIT_SUMMARY = "(fixture) 이미지를 패치 토큰열로 바꿔 Transformer에 넣는 모델 계열이다."  # AI summary, unapproved
KATEX_OK = (
    '<span class="katex"><span class="katex-mathml"><math><mi>x</mi></math></span>'
    '<span class="katex-html" aria-hidden="true">x</span></span>'
)


def page(title="제목", body="", lang="ko", description="설명", head=""):
    """Return a minimal valid HTML page."""
    meta = f'<meta name="description" content="{description}">' if description is not None else ""
    return (
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{title}</title>'
        f"{meta}{head}</head><body><h1>{title}</h1>{body}</body></html>"
    )


def sitemap_xml(*locations):
    """Return a sitemap or sitemap-index document listing the given locations."""
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    items = "".join(f"<url><loc>{loc}</loc></url>" for loc in locations)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="{namespace}">{items}</urlset>'


def sitemap_index_xml(location):
    """Return a sitemap index with one sitemap."""
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    return (
        f'<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="{namespace}">'
        f"<sitemap><loc>{location}</loc></sitemap></sitemapindex>"
    )


def write(root, relative, text):
    """Write a text file below root, creating folders."""
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf8")
    return path


def make_dist(root, mode="preview", extra_pages=()):
    """Write a small valid site (base /aixon/) and return its root."""
    home_body = (
        '<a href="/aixon/e/model/vit/">ViT</a> <a href="/aixon/atlas/#node-model~vit">atlas</a> '
        '<a href="e/model/vit/">relative</a> <a href="https://example.org/">external</a> '
        '<a href="mailto:a@b.c">mail</a> <script type="module" src="/aixon/_astro/app.js"></script> '
        '<astro-island component-url="/aixon/_astro/island.js" renderer-url="/aixon/_astro/island.js"></astro-island> '
        f'<img src="/aixon/_astro/logo.svg" alt="logo"> {KATEX_OK}'
    )
    head = (
        '<link rel="stylesheet" href="/aixon/_astro/app.css">'
        f'<link rel="canonical" href="{SITE}/aixon/">'
    )
    write(root, "index.html", page("홈", home_body, head=head))
    write(root, "404.html", page("없음", '<a href="/aixon/">home</a>'))
    write(root, "e/model/vit/index.html", page("ViT", '<a href="../../../atlas/">atlas</a>'))
    write(root, "atlas/index.html", page("아틀라스"))
    for name in ("app.js", "island.js"):
        write(root, f"_astro/{name}", "export {};")
    write(root, "_astro/app.css", "body{margin:0}")
    write(root, "_astro/logo.svg", "<svg xmlns='http://www.w3.org/2000/svg'/>")
    write(root, "graph.json", json.dumps({"build": mode, "nodes": [], "edges": []}))
    write(root, "node-index.json", "[]")
    write(root, "sitemap-index.xml", sitemap_index_xml(f"{SITE}/aixon/sitemap-0.xml"))
    urls = [f"{SITE}/aixon/", f"{SITE}/aixon/atlas/", f"{SITE}/aixon/e/model/vit/"]
    write(root, "sitemap-0.xml", sitemap_xml(*urls))
    if mode == "preview":
        write(root, "robots.txt", "User-agent: *\nDisallow: /\n")
    else:
        write(root, "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/aixon/sitemap-index.xml\n")
    for relative, text in extra_pages:
        write(root, relative, text)
    return root


@pytest.fixture
def audit(run_tool):
    """Return audit(dist, mode="preview", *extra args) -> (exit code, JSON report)."""

    def run(dist, mode="preview", *extra):
        args = [dist, "--base", BASE, "--site", SITE, "--mode", mode, "--json"]
        if mode == "public":
            args += ["--graph", FIXTURE_GRAPH, "--wiki-dir", FIXTURE_WIKI]
        result = run_tool("check_dist.py", *args, *extra)
        report = json.loads(result.stdout) if result.stdout.strip().startswith("{") else None
        return result.returncode, report

    return run


def has_error(report, code, needle):
    """Return True when an error of this code mentions needle."""
    return any(item["code"] == code and needle in item["message"] for item in report["errors"])


def test_clean_preview_tree_passes(tmp_path, audit):
    exit_code, report = audit(make_dist(tmp_path))
    assert exit_code == 0, report["errors"]
    assert report["errors"] == []
    assert report["pages"] == 4


def test_links_are_resolved_after_stripping_the_base(tmp_path, audit):
    """/aixon/x must be looked up as DIST/x, never as DIST/aixon/x."""
    dist = make_dist(tmp_path)
    assert not (dist / "aixon").exists()
    exit_code, report = audit(dist)
    assert exit_code == 0, report["errors"]


def mutate_append_to_home(snippet):
    """Return a mutation that adds an HTML snippet to the home page body."""

    def mutation(dist):
        home = dist / "index.html"
        home.write_text(home.read_text(encoding="utf8").replace("</body>", f"{snippet}</body>"), encoding="utf8")

    return mutation


def mutate_replace(relative, old, new):
    """Return a mutation that rewrites text inside one file."""

    def mutation(dist):
        path = dist / relative
        path.write_text(path.read_text(encoding="utf8").replace(old, new), encoding="utf8")

    return mutation


def mutate_write(relative, text):
    """Return a mutation that overwrites one file."""

    def mutation(dist):
        write(dist, relative, text)

    return mutation


def mutate_delete(relative):
    """Return a mutation that deletes one file."""

    def mutation(dist):
        (dist / relative).unlink()

    return mutation


PREVIEW_FAILURES = {
    "missing-internal-target-with-base": (
        mutate_append_to_home('<a href="/aixon/nowhere/">x</a>'), "V-DIST-LINK", "no such page"),
    "link-ignores-the-base": (
        mutate_append_to_home('<a href="/atlas/">x</a>'), "V-DIST-LINK", "outside the deployment base"),
    "missing-script": (
        mutate_append_to_home('<script src="/aixon/_astro/gone.js"></script>'), "V-DIST-LINK", "no such file"),
    "missing-island-bundle": (
        mutate_append_to_home('<astro-island component-url="/aixon/_astro/gone.js"></astro-island>'),
        "V-DIST-LINK", "no such file"),
    "directory-link-without-slash": (
        mutate_append_to_home('<a href="/aixon/atlas">x</a>'), "V-DIST-LINK", "trailing slash"),
    "broken-relative-link": (
        mutate_replace("e/model/vit/index.html", "../../../atlas/", "../../nowhere/"), "V-DIST-LINK", "no such page"),
    "canonical-points-nowhere": (
        mutate_replace("index.html", f'href="{SITE}/aixon/"', f'href="{SITE}/aixon/gone/"'),
        "V-DIST-LINK", "no such page"),
    "missing-required-file": (mutate_delete("graph.json"), "V-DIST-LINK", "required file is missing"),
    "invalid-graph-json": (mutate_write("graph.json", "{not json"), "V-DIST-LINK", "not valid JSON"),
    "two-h1": (mutate_append_to_home("<h1>again</h1>"), "V-SEO", "exactly one <h1>"),
    "no-h1": (mutate_replace("atlas/index.html", "<h1>", "<h2>"), "V-SEO", "exactly one <h1>"),
    "wrong-lang": (mutate_replace("atlas/index.html", 'lang="ko"', 'lang="en"'), "V-SEO", "lang"),
    "empty-title": (mutate_replace("atlas/index.html", "<title>아틀라스</title>", "<title> </title>"), "V-SEO", "title"),
    "no-description": (
        mutate_replace("atlas/index.html", '<meta name="description" content="설명">', ""), "V-SEO", "description"),
    "image-without-alt": (mutate_append_to_home('<img src="/aixon/_astro/logo.svg">'), "V-SEO", "alt"),
    "katex-error": (mutate_append_to_home('<span class="katex-error">\\bad</span>'), "V-MATH", "katex-error"),
    "katex-without-mathml": (
        mutate_append_to_home('<span class="katex"><span class="katex-html">x</span></span>'),
        "V-MATH", "without MathML"),
    "external-script": (
        mutate_append_to_home('<script src="https://cdn.example.org/lib.js"></script>'), "V-NO-CDN", "external script"),
    "external-stylesheet": (
        mutate_append_to_home('<link rel="stylesheet" href="https://fonts.example.org/x.css">'),
        "V-NO-CDN", "external link"),
    "css-imports-a-cdn": (
        mutate_write("_astro/app.css", '@import url("https://cdn.example.org/x.css");'), "V-NO-CDN", "CSS loads"),
    "preview-robots-allows-indexing": (
        mutate_write("robots.txt", "User-agent: *\nAllow: /\n"), "V-SEO", "Disallow: /"),
    "sitemap-url-outside-site-and-base": (
        mutate_replace("sitemap-0.xml", f"{SITE}/aixon/atlas/", f"{SITE}/atlas/"), "V-SEO", "does not start with"),
    "sitemap-lists-a-missing-page": (
        mutate_replace("sitemap-0.xml", f"{SITE}/aixon/atlas/", f"{SITE}/aixon/ghost/"), "V-SEO", "no such page"),
    "sitemap-index-lists-a-missing-sitemap": (
        mutate_replace("sitemap-index.xml", "sitemap-0.xml", "sitemap-9.xml"), "V-SEO", "does not exist"),
    "search-page-without-pagefind": (
        mutate_write("search/index.html", page("검색")), "V-DIST-LINK", "pagefind"),
}


@pytest.mark.parametrize("name", sorted(PREVIEW_FAILURES))
def test_preview_failure(name, tmp_path, audit):
    mutation, code, needle = PREVIEW_FAILURES[name]
    dist = make_dist(tmp_path)
    mutation(dist)
    exit_code, report = audit(dist)
    assert exit_code == 1, f"{name} was not detected"
    assert has_error(report, code, needle), report["errors"]


def test_canonical_of_the_404_page_is_only_a_warning(tmp_path, audit):
    dist = make_dist(tmp_path)
    write(dist, "404.html", page("없음", head=f'<link rel="canonical" href="{SITE}/aixon/404/">'))
    exit_code, report = audit(dist)
    assert exit_code == 0, report["errors"]
    assert any(item["file"] == "404.html" for item in report["warnings"])


def test_every_page_is_checked(tmp_path, audit):
    dist = make_dist(tmp_path, extra_pages=[("deep/er/index.html", page("깊은", "<h1>둘</h1>"))])
    exit_code, report = audit(dist)
    assert exit_code == 1
    assert {item["file"] for item in report["errors"]} == {"deep/er/index.html"}


def test_json_report_shape(tmp_path, audit):
    _exit_code, report = audit(make_dist(tmp_path))
    assert {"dist", "mode", "base", "site", "pages", "errors", "warnings"} <= set(report)
    assert report["mode"] == "preview"
    assert report["base"] == BASE


def test_missing_dist_is_a_setup_error(tmp_path, run_tool):
    result = run_tool("check_dist.py", tmp_path / "nope", "--base", BASE)
    assert result.returncode == 2
    assert "dist directory not found" in result.stderr


def public_extra_pages():
    """Return the pages a clean public build contains in addition to the base tree."""
    return [
        ("claims/intro-transformer/index.html", page("근거: 승인된 Claim")),
        ("wiki/transformer/index.html", page("Transformer", "사람 검토 완료")),
        ("e/model/transformer/index.html", page("Transformer", f"<p>{TRANSFORMER_SUMMARY}</p>")),
    ]


def make_public_dist(root, extra=()):
    """Write a clean public build: approved claim, published wiki, approved summary."""
    dist = make_dist(root, "public", [*public_extra_pages(), *extra])
    graph = {
        "build": "public",
        "nodes": [{"id": "model:transformer", "summary": TRANSFORMER_SUMMARY}],
        "edges": [{"id": "clm:intro-transformer", "kind": "claim", "predicate": "INTRODUCES"}],
    }
    write(dist, "graph.json", json.dumps(graph, ensure_ascii=False))
    return dist


def test_clean_public_tree_passes(tmp_path, audit):
    exit_code, report = audit(make_public_dist(tmp_path), "public")
    assert exit_code == 0, report["errors"]


PUBLIC_FAILURES = {
    "draft-banner": (
        mutate_append_to_home("<p>검토 전 초안 · AI 작성</p>"), "V-PUBLIC", "검토 전 초안"),
    "claim-page-without-approval": (
        mutate_write("claims/vit-adapts-transformer/index.html", page("근거")), "V-PUBLIC", "without a human approval"),
    "claim-page-approved-only-by-an-agent": (
        mutate_write("claims/intro-vit/index.html", page("근거")), "V-PUBLIC", "without a human approval"),
    "claim-page-for-an-unknown-claim": (
        mutate_write("claims/ghost/index.html", page("근거")), "V-PUBLIC", "without a human approval"),
    "graph-json-with-an-unapproved-claim-edge": (
        mutate_write(
            "graph.json",
            json.dumps({"build": "public", "nodes": [], "edges": [{"id": "clm:vit-adapts-transformer", "kind": "claim"}]}),
        ),
        "V-PUBLIC", "not a human-approved claim"),
    "graph-json-built-in-preview-mode": (
        mutate_write("graph.json", json.dumps({"build": "preview", "nodes": [], "edges": []})), "V-PUBLIC", "build is"),
    "wiki-page-of-a-draft-document": (
        mutate_write("wiki/scaled-dot-product-attention/index.html", page("초안")), "V-PUBLIC", "published, human-reviewed"),
    "wiki-page-without-a-document": (
        mutate_write("wiki/ghost/index.html", page("유령")), "V-PUBLIC", "published, human-reviewed"),
    "unapproved-ai-summary-on-a-page": (
        mutate_write("e/model/vit/index.html", page("ViT", f"<p>{VIT_SUMMARY}</p>")), "V-PUBLIC", "unapproved AI summary"),
    "unapproved-ai-summary-in-graph-json": (
        mutate_write(
            "graph.json",
            json.dumps({"build": "public", "nodes": [{"id": "model:vit", "summary": VIT_SUMMARY}], "edges": []}, ensure_ascii=False),
        ),
        "V-PUBLIC", "unapproved AI summary"),
    "public-robots-disallows-everything": (
        mutate_write("robots.txt", "User-agent: *\nDisallow: /\n"), "V-SEO", "must not contain"),
    "public-robots-without-sitemap": (
        mutate_write("robots.txt", "User-agent: *\nAllow: /\n"), "V-SEO", "sitemap-index.xml"),
}


@pytest.mark.parametrize("name", sorted(PUBLIC_FAILURES))
def test_public_failure(name, tmp_path, audit):
    mutation, code, needle = PUBLIC_FAILURES[name]
    dist = make_public_dist(tmp_path)
    mutation(dist)
    exit_code, report = audit(dist, "public")
    assert exit_code == 1, f"{name} was not detected"
    assert has_error(report, code, needle), report["errors"]


def test_public_mode_without_a_graph_is_a_setup_error(tmp_path, run_tool):
    dist = make_public_dist(tmp_path)
    result = run_tool("check_dist.py", dist, "--base", BASE, "--mode", "public", "--graph", "no/such.yaml")
    assert result.returncode == 2
    assert "needs an existing --graph" in result.stderr


def test_preview_mode_does_not_apply_public_rules(tmp_path, audit):
    """A preview build legitimately contains drafts and unapproved claims."""
    dist = make_dist(
        tmp_path,
        extra_pages=[
            ("claims/vit-adapts-transformer/index.html", page("근거", "검토 전 초안")),
            ("wiki/scaled-dot-product-attention/index.html", page("초안")),
        ],
    )
    exit_code, report = audit(dist)
    assert exit_code == 0, report["errors"]
