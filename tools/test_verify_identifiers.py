import datetime as dt
from pathlib import Path

from tools import verify_identifiers
from tools.verify_identifiers import compare_papers, normalize_title, parse_atom


def test_normalize_title_removes_math_punctuation_and_spacing():
    assert normalize_title("A $x^2$ — Test:  Model") == "atestmodel"


def test_compare_arxiv_fixture_match_mismatch_and_not_found():
    fixture = Path(__file__).parent / "fixtures" / "arxiv_sample.xml"
    entries = parse_atom(fixture.read_bytes())
    rows = compare_papers([
        {"id": "paper:match", "arxiv": "1706.03762", "title": "Attention Is All You Need", "earliest_public_date": "2017-06-01"},
        {"id": "paper:mismatch", "arxiv": "1512.03385", "title": "A Different Title", "earliest_public_date": "2015-11-01"},
        {"id": "paper:missing", "arxiv": "9999.99999", "title": "Missing", "earliest_public_date": "2020-01-01"},
    ], entries)
    assert [(row["paper"], row["status"], row["date_flag"]) for row in rows] == [
        ("paper:match", "match", None),
        ("paper:mismatch", "title_mismatch", "month_mismatch"),
        ("paper:missing", "not_found", None),
    ]


def test_write_checked_stamps_matches_and_drops_stale_non_arxiv_stamp(tmp_path, monkeypatch):
    graph = tmp_path / "papers.yaml"
    before = """papers:
  - id: paper:match
    title: Attention Is All You Need
    identifiers:
      arxiv: '1706.03762'
    metadata_checked:
      openalex: '2020-01-01'
    note: leave this line alone
  - id: paper:mismatch
    title: Incorrect title
    identifiers:
      arxiv: '1512.03385'
    metadata_checked:
      openalex: '2020-01-01'
  - id: paper:no-arxiv
    title: Not on arXiv
    metadata_checked:
      arxiv: '2020-01-01'
      openalex: '2020-01-01'
"""
    graph.write_text(before, encoding="utf-8")
    fixture = Path(__file__).parent / "fixtures" / "arxiv_sample.xml"
    monkeypatch.setattr(verify_identifiers, "fetch_entries", lambda identifiers, cache, offline: (parse_atom(fixture.read_bytes()), {}))

    assert verify_identifiers.main(["--offline", "--write-checked", str(graph)]) == 1
    today = dt.date.today().isoformat()
    expected = before.replace(
        "      openalex: '2020-01-01'\n    note",
        f"      openalex: '2020-01-01'\n      arxiv: '{today}'\n    note",
        1,
    ).replace("    metadata_checked:\n      arxiv: '2020-01-01'\n      openalex: '2020-01-01'\n", "    metadata_checked:\n      openalex: '2020-01-01'\n")
    assert graph.read_text(encoding="utf-8") == expected
