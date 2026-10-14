from pathlib import Path

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
