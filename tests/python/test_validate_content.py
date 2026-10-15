"""tools/validate_content.py: the good fixtures pass, every bad fixture fails with exactly its rule."""

from __future__ import annotations

import json
import re
import shutil

import pytest
from conftest import BAD_WIKI, FIXTURE_GRAPH, FIXTURE_WIKI

# bad fixture (file stem) -> the only rule code it may trigger
EXPECTED_RULE = {
    "v-schema-missing-field": "V-SCHEMA-1",
    "v-schema-sections-mismatch": "V-SCHEMA-3",
    "v-link-unknown": "V-LINK-1",
    "v-cite-unknown": "V-CITE-1",
    "v-cite-not-in-frontmatter": "V-CITE-3",
    "v-cite2-math-without-cite": "V-CITE-2",
    "v-status-published-without-review": "V-STATUS-1",
    "v-status-ai-reviewed-by-agent": "V-STATUS-2",
    "v-status-cites-rejected": "V-STATUS-3",
    "v-code-failing-assert": "V-CODE-1",
    "v-fig-not-listed": "V-FIG-1",
    "v-labref-not-listed": "V-LABREF-1",
}


@pytest.fixture
def validate(run_tool):
    """Return validate(wiki_dir, graph=FIXTURE_GRAPH) -> (exit code, parsed --json report)."""

    def run(wiki_dir, graph=FIXTURE_GRAPH):
        result = run_tool("validate_content.py", "--wiki-dir", wiki_dir, "--graph", graph, "--json")
        report = json.loads(result.stdout) if result.stdout.strip().startswith("{") else None
        return result.returncode, report

    return run


def write_doc(directory, name, text):
    """Write an MDX file into directory and return its path."""
    path = directory / name
    path.write_text(text, encoding="utf8")
    return path


def transformer_text():
    """Return the text of the small published fixture document."""
    return (FIXTURE_WIKI / "transformer.mdx").read_text(encoding="utf8")


def codes(report, level="errors"):
    """Return the set of rule codes of a report section."""
    return {item["code"] for item in report[level]}


def test_good_fixtures_have_no_findings(validate):
    exit_code, report = validate(FIXTURE_WIKI)
    assert exit_code == 0, report
    assert report["documents"] == 2
    assert report["errors"] == []
    assert report["warnings"] == []


def test_every_bad_fixture_has_an_expected_rule():
    assert {path.stem for path in BAD_WIKI.glob("*.mdx")} == set(EXPECTED_RULE)


@pytest.mark.parametrize("stem", sorted(EXPECTED_RULE))
def test_bad_fixture_fails_with_only_its_rule(stem, tmp_path, validate):
    shutil.copy(BAD_WIKI / f"{stem}.mdx", tmp_path / "scaled-dot-product-attention.mdx")
    exit_code, report = validate(tmp_path)
    assert exit_code == 1, report
    expected = {EXPECTED_RULE[stem]}
    if stem == "v-status-published-without-review":
        expected.add("V-STATUS")
    assert codes(report) == expected, report["errors"]
    first = report["errors"][0]
    assert first["file"] == "scaled-dot-product-attention.mdx"
    assert first["line"] >= 1
    assert first["message"]


def test_human_output_names_rule_file_and_line(tmp_path, run_tool):
    shutil.copy(BAD_WIKI / "v-link-unknown.mdx", tmp_path / "scaled-dot-product-attention.mdx")
    result = run_tool("validate_content.py", "--wiki-dir", tmp_path, "--graph", FIXTURE_GRAPH)
    assert result.returncode == 1
    assert "ERROR V-LINK-1 scaled-dot-product-attention.mdx:" in result.stdout
    assert "1 error(s)" in result.stdout


def test_file_name_must_match_id_and_entity_slug(tmp_path, validate):
    write_doc(tmp_path, "wrong-name.mdx", transformer_text())
    exit_code, report = validate(tmp_path)
    assert exit_code == 1
    assert codes(report) == {"V-SCHEMA-2"}


def test_only_one_wiki_per_entity(tmp_path, validate):
    write_doc(tmp_path, "transformer.mdx", transformer_text())
    write_doc(tmp_path, "transformer-copy.mdx", transformer_text())
    _exit_code, report = validate(tmp_path)
    messages = [item["message"] for item in report["errors"] if item["code"] == "V-SCHEMA-2"]
    assert any("already has a wiki" in message for message in messages), messages


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("sources: [src:fixture:attention-2017-v1]", "sources: [src:does-not-exist]"),
        ("claims: [clm:intro-transformer]", "claims: [clm:does-not-exist]"),
        ("labs: []", "labs: lab:softmax-temperature"),
        ("entity: model:transformer", "entity: model:does-not-exist"),
        ("status: published", "status: finished"),
        ("levels: [intuition]", "levels: [deep, intuition]"),
        ("ai_generated: true", "ai_generated: false"),
    ],
)
def test_frontmatter_values_are_checked(old, new, tmp_path, validate):
    text = transformer_text()
    assert old in text
    write_doc(tmp_path, "transformer.mdx", text.replace(old, new))
    exit_code, report = validate(tmp_path)
    assert exit_code == 1
    assert "V-SCHEMA-1" in codes(report), report["errors"]


def test_unknown_lab_in_frontmatter_is_a_lab_reference_error(tmp_path, validate):
    text = transformer_text().replace("status: published", "status: draft").replace("labs: []", "labs: [lab:does-not-exist]")
    write_doc(tmp_path, "transformer.mdx", text)
    exit_code, report = validate(tmp_path)
    assert exit_code == 1
    assert codes(report) == {"V-LABREF-1"}


def test_proposed_and_disputed_citations_are_warnings_not_errors(tmp_path, validate):
    proposed = "clm:prereq-multi-head-attention-vit"
    disputed = "clm:transformer-mitigates-sequential"
    text = transformer_text().replace("status: published", "status: draft")
    text = text.replace(
        "claims: [clm:intro-transformer]",
        f"claims: [clm:intro-transformer, {proposed}, {disputed}]",
    )
    text = text.replace(
        '<Cite claim="clm:intro-transformer" loc="§1 (fixture)" />',
        f'<Cite claim="clm:intro-transformer" /><Cite claim="{proposed}" /><Cite claim="{disputed}" />',
    )
    write_doc(tmp_path, "transformer.mdx", text)
    exit_code, report = validate(tmp_path)
    assert exit_code == 0, report["errors"]
    assert codes(report, "warnings") == {"V-STATUS-3"}
    assert len(report["warnings"]) == 2


def test_outline_documents_need_no_citations(tmp_path, validate):
    text = (BAD_WIKI / "v-cite2-math-without-cite.mdx").read_text(encoding="utf8")
    write_doc(tmp_path, "scaled-dot-product-attention.mdx", text.replace("status: draft", "status: outline"))
    exit_code, report = validate(tmp_path)
    assert exit_code == 0, report["errors"]


def test_components_inside_code_blocks_are_ignored(tmp_path, validate):
    text = transformer_text().replace("status: published", "status: draft").replace(
        "</Section>",
        '\n```mdx\n<ConceptLink id="concept:nope">x</ConceptLink>\n<Cite claim="clm:nope" />\n```\n\n</Section>',
    )
    write_doc(tmp_path, "transformer.mdx", text)
    exit_code, report = validate(tmp_path)
    assert exit_code == 0, report["errors"]


def test_published_document_outside_public_gate_is_a_status_error(tmp_path, validate):
    text = re.sub(r"review:\n(?:  .*\n)+", "review: null\n", transformer_text())
    write_doc(tmp_path, "transformer.mdx", text)
    exit_code, report = validate(tmp_path)
    assert exit_code == 1
    assert "V-STATUS" in codes(report)


@pytest.mark.parametrize(
    "snippet",
    [
        'import Widget from "./widget"',
        '<div>not an allowed MDX element</div>',
        '<Callout onclick="bad()">unsafe</Callout>',
        '<Callout href="javascript:bad()">unsafe</Callout>',
        "[x](javascript:alert(1))",
        '<Callout kind={"javascript:alert(1)"}>x</Callout>',
        r'\$5 <img src="x" onerror="alert(1)" /> \$10',
    ],
)
def test_mdx_security_rules_reject_unsafe_content(tmp_path, validate, snippet):
    text = transformer_text().replace("status: published", "status: draft")
    write_doc(tmp_path, "transformer.mdx", text.replace("</Section>", f"\n{snippet}\n</Section>"))
    exit_code, report = validate(tmp_path)
    assert exit_code == 1
    assert codes(report) == {"V-SEC"}


def test_mdx_security_ignores_code_and_math(tmp_path, validate):
    text = transformer_text().replace("status: published", "status: draft")
    text = text.replace("</Section>", '\n`<div onclick="bad()">code</div>`\n\n$<div>math</div>$\n</Section>')
    write_doc(tmp_path, "transformer.mdx", text)
    exit_code, report = validate(tmp_path)
    assert exit_code == 0, report["errors"]


def test_deep_level_citations_do_not_satisfy_section_coverage(tmp_path, validate):
    text = transformer_text().replace("status: published", "status: draft")
    text = text.replace("sections: [overview]", "sections: [math]")
    text = text.replace('id="overview"', 'id="math"').replace(
        '<Cite claim="clm:intro-transformer" loc="§1 (fixture)" />',
        '<Level of="deep"><Cite claim="clm:intro-transformer" loc="§1 (fixture)" /></Level>',
    )
    write_doc(tmp_path, "transformer.mdx", text)
    exit_code, report = validate(tmp_path)
    assert exit_code == 1
    assert codes(report) == {"V-CITE-2"}


def test_verify_blocks_may_only_import_numpy_and_the_standard_library(tmp_path, validate):
    text = (BAD_WIKI / "v-code-failing-assert.mdx").read_text(encoding="utf8")
    text = text.replace("import numpy as np", "import numpy as np\nimport scipy").replace(
        'assert np.allclose(np.exp(0.0), 2.0), "exp(0) is 1, not 2"', "assert np.exp(0.0) == 1.0"
    )
    write_doc(tmp_path, "scaled-dot-product-attention.mdx", text)
    exit_code, report = validate(tmp_path)
    assert exit_code == 1
    assert codes(report) == {"V-CODE-1"}
    assert "scipy" in report["errors"][0]["message"]


def test_verify_block_failure_message_shows_the_assertion(tmp_path, validate):
    shutil.copy(BAD_WIKI / "v-code-failing-assert.mdx", tmp_path / "scaled-dot-product-attention.mdx")
    _exit_code, report = validate(tmp_path)
    assert "AssertionError" in report["errors"][0]["message"]


def test_missing_wiki_directory_is_a_setup_error(run_tool, tmp_path):
    result = run_tool("validate_content.py", "--wiki-dir", tmp_path / "nope", "--graph", FIXTURE_GRAPH)
    assert result.returncode == 2
    assert "wiki directory not found" in result.stderr


def test_missing_graph_is_a_setup_error(run_tool):
    result = run_tool("validate_content.py", "--wiki-dir", FIXTURE_WIKI, "--graph", "no/such/graph.yaml")
    assert result.returncode == 2
    assert "no graph file found" in result.stderr


def test_real_wiki_validates_against_the_seed_graph(run_tool):
    """The default arguments are what `make validate` runs on the committed wiki documents."""
    result = run_tool("validate_content.py", "--json")
    report = json.loads(result.stdout)
    assert result.returncode == 0, report["errors"]
    assert report["documents"] >= 1


def test_panel_approval_satisfies_status_rules(tmp_path, validate):
    """ADR-026: a cross-review panel signature is not 'reviewed by an agent' (the gate checks the reports)."""
    panel = (
        "review:\n  by: panel:test\n  method: cross-review\n  reviewers: [agent:a, agent:b]\n  audit: agent:c\n"
        "  report: review/cross/test\n"
    )
    text = re.sub(r"review:\n  by: [^\n]+\n", panel, transformer_text(), count=1)
    write_doc(tmp_path, "transformer.mdx", text)
    _, report = validate(tmp_path)
    assert not codes(report) & {"V-STATUS-1", "V-STATUS-2"}, report["errors"]
    write_doc(tmp_path, "transformer.mdx", text.replace("by: panel:test", "by: agent:x"))
    _, report = validate(tmp_path)
    assert "V-STATUS-2" in codes(report)
