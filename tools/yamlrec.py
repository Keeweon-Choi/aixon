"""Line-level edits of one record in a YAML graph file.

Records are list items (``- id: x`` or ``- other: …`` followed by ``  id: x``) at any indentation; their keys
sit two spaces deeper than the dash. Only the edited key's lines change, so the rest of the file stays
byte-identical (a full ``yaml.safe_dump`` round trip would re-quote thousands of lines).
"""
from __future__ import annotations

import re

import yaml


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _dump(key: str, value, indent: int) -> list[str]:
    text = yaml.safe_dump({key: value}, allow_unicode=True, sort_keys=False, width=1000)
    return [" " * indent + line for line in text.rstrip("\n").split("\n")]


def record_span(lines: list[str], ident: str) -> tuple[int, int, int]:
    """[start, end) line range of the record with this id, and the indentation of its keys."""
    pattern = re.compile(rf"^(\s*)(- )?id: ['\"]?{re.escape(ident)}['\"]?\s*$")
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if not m:
            continue
        key_indent = len(m.group(1)) + (2 if m.group(2) else 0)
        start = i
        while not lines[start].lstrip(" ").startswith("- ") or _indent(lines[start]) != key_indent - 2:
            start -= 1
        end = start + 1
        while end < len(lines) and (not lines[end].strip() or _indent(lines[end]) >= key_indent):
            end += 1
        return start, end, key_indent
    raise KeyError(f"record not found: {ident}")


def _key_line(lines: list[str], start: int, end: int, key_indent: int, key: str) -> int | None:
    dash = " " * (key_indent - 2) + "- "
    for k in range(start, end):
        if lines[k].startswith(" " * key_indent + key + ":") or lines[k].startswith(dash + key + ":"):
            return k
    return None


def _continuation_end(lines: list[str], k: int, end: int, key_indent: int) -> int:
    stop = k + 1
    while stop < end and lines[stop].strip() and (
            _indent(lines[stop]) > key_indent or lines[stop].startswith(" " * key_indent + "- ")):
        stop += 1
    return stop


def set_field(lines: list[str], ident: str, key: str, value) -> list[str]:
    """Return new lines with ``key`` of record ``ident`` set to ``value`` (replaced or appended)."""
    start, end, key_indent = record_span(lines, ident)
    new = _dump(key, value, key_indent)
    k = _key_line(lines, start, end, key_indent, key)
    if k is not None:
        if k == start:
            raise ValueError(f"{ident}: cannot edit {key} on the list-item line")
        return lines[:k] + new + lines[_continuation_end(lines, k, end, key_indent):]
    last = end
    while last > start and not lines[last - 1].strip():
        last -= 1
    return lines[:last] + new + lines[last:]


def delete_field(lines: list[str], ident: str, key: str) -> list[str]:
    """Return new lines without ``key`` (and its continuation lines) in record ``ident``."""
    start, end, key_indent = record_span(lines, ident)
    k = _key_line(lines, start, end, key_indent, key)
    if k is None or k == start:
        return lines
    return lines[:k] + lines[_continuation_end(lines, k, end, key_indent):]


def delete_record(lines: list[str], ident: str) -> list[str]:
    """Return new lines without the record ``ident``."""
    start, end, _ = record_span(lines, ident)
    return lines[:start] + lines[end:]


def append_record(lines: list[str], section: str, record: dict) -> list[str]:
    """Append a record at the end of a top-level section written in PyYAML style (items at column 0)."""
    head = lines.index(f"{section}:")
    end = head + 1
    while end < len(lines) and (lines[end].startswith(("- ", "  ")) or not lines[end].strip()):
        end += 1
    while end > head + 1 and not lines[end - 1].strip():
        end -= 1
    text = yaml.safe_dump([record], allow_unicode=True, sort_keys=False, width=1000)
    return lines[:end] + text.rstrip("\n").split("\n") + lines[end:]


def edit_file(path: str, fn) -> None:
    """Apply ``fn(lines) -> lines`` to a file and refuse if the YAML no longer parses."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    new = "\n".join(fn(text.split("\n")))
    yaml.safe_load(new)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)


if __name__ == "__main__":
    sample = ["claims:", "- id: clm:a", "  status: verified", "  review: null", "- id: clm:b", "  aliases:", "  - x", "  review:", "    by: human:k", "sources:", "- id: src:s"]
    out = set_field(sample, "clm:a", "review", {"by": "human:k", "decision": "approve"})
    assert out[3:6] == ["  review:", "    by: human:k", "    decision: approve"], out
    out = set_field(sample, "clm:b", "review", None)
    assert out[7] == "  review: null" and out[8] == "sources:", out
    out = set_field(sample, "clm:b", "aliases", ["y", "z"])
    assert out[5:8] == ["  aliases:", "  - y", "  - z"], out
    out = set_field(sample, "src:s", "url", "https://e.org")
    assert out[-1] == "  url: https://e.org", out
    out = delete_field(sample, "clm:b", "review")
    assert out[7] == "sources:" and "  aliases:" in out, out
    out = delete_record(sample, "clm:a")
    assert out[1] == "- id: clm:b", out
    out = append_record(sample, "claims", {"id": "clm:c", "status": "proposed"})
    assert out[9:11] == ["- id: clm:c", "  status: proposed"] and out[11] == "sources:", out
    nested = ["claims:", "  - id: clm:n", "    status: verified", "    qualifiers: {a: 1}", "  - id: clm:m", "    status: proposed"]
    out = set_field(nested, "clm:n", "review", {"by": "human:k"})
    assert out[4:6] == ["    review:", "      by: human:k"] and out[6] == "  - id: clm:m", out
    atlas = ["fields:", "- summary_by: agent:x", "  id: field:f", "  name: F", "- summary_by: agent:x", "  id: field:g"]
    out = set_field(atlas, "field:f", "fields", ["field:g"])
    assert out[4:6] == ["  fields:", "  - field:g"] and out[6] == "- summary_by: agent:x", out
    try:
        record_span(sample, "clm:zzz")
        raise AssertionError("missing record must raise")
    except KeyError:
        pass
    print("yamlrec self-check OK")
