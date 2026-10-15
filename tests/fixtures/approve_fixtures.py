"""
# TEST FIXTURE — not real research data
Write the TEST FIXTURE approvals with real content hashes (ADR-021). Test data only.

Run after any edit of an approved fixture record:  .venv/bin/python tests/fixtures/approve_fixtures.py
It calls the same functions as `tools/review.py approve`; the CLI itself refuses inside agent sessions,
which is meant for real content, not for these made-up fixtures.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import review  # noqa: E402

GRAPH = [str(ROOT / "tests/fixtures/graph/site_graph.yaml")]
WIKI = ROOT / "tests/fixtures/wiki/transformer.mdx"
APPROVED = ["paper:fixture-attention-2017", "model:transformer", "clm:intro-transformer"]
BY, AT = "human:fixture-editor", "2026-10-15"

for ident in APPROVED:
    review.approve_record(GRAPH, ident, BY, "fixture", ["support"], AT)
review.approve_wiki(WIKI, BY, "fixture", AT)
print(f"approved {len(APPROVED)} records and {WIKI.name}")
