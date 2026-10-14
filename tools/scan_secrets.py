#!/usr/bin/env python3
"""Scan the repository and its build outputs for committed secrets.

Scanned: every file git tracks or would add (untracked, not ignored), plus these folders when they
exist: dist, dist-public, dist-e2e, dist-seed, dist-public-e2e, artifacts, playwright-report,
test-results. Binary files are skipped.

Usage:
    scan_secrets.py [ROOT]

A hit prints `path:line: <pattern name>: <masked match>`; the secret itself is never printed.
Exit code: 0 clean, 1 hits, 2 ROOT is not a git repository.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

OUTPUT_FOLDERS = (
    "dist",
    "dist-public",
    "dist-e2e",
    "dist-seed",
    "dist-public-e2e",
    "artifacts",
    "playwright-report",
    "test-results",
)
MAX_FILE_BYTES = 20_000_000
BINARY_SNIFF_BYTES = 8192
PLACEHOLDER_WORDS = ("example", "placeholder", "your", "xxxx", "changeme", "dummy", "redacted")

# Order matters: the first matching pattern names the hit (Anthropic keys also look like OpenAI keys).
PATTERNS = (
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("github-fine-grained-token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("anthropic-api-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("openai-api-key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    (
        "private-key-header",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----"),
    ),
)
ASSIGNMENT_RE = re.compile(
    r"""\b[A-Za-z0-9_]*(?:API_KEY|SECRET_KEY|ACCESS_TOKEN)\s*[=:]\s*['"]?([A-Za-z0-9_\-+/=.]{20,})""",
    re.IGNORECASE,
)


@dataclass
class Hit:
    """One suspected secret."""

    path: str
    line: int
    pattern: str
    masked: str


def mask(secret: str) -> str:
    """Return a printable stand-in that does not reveal the secret."""
    return f"{secret[:4]}…({len(secret)} chars)"


def find_in_line(text: str) -> list[tuple[str, str]]:
    """Return (pattern name, matched text) for every secret-looking thing in one line."""
    found = []
    for name, pattern in PATTERNS:
        match = pattern.search(text)
        if match:
            found.append((name, match.group(0)))
    assignment = ASSIGNMENT_RE.search(text)
    if assignment and not any(word in assignment.group(1).lower() for word in PLACEHOLDER_WORDS):
        found.append(("api-key-assignment", assignment.group(1)))
    return found


def scan_file(path: Path, display: str) -> list[Hit]:
    """Scan one file. Binary and oversized files are skipped."""
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return []
        data = path.read_bytes()
    except OSError:
        return []
    if b"\0" in data[:BINARY_SNIFF_BYTES]:
        return []
    hits = []
    for number, line in enumerate(data.decode("utf8", errors="replace").splitlines(), start=1):
        for name, secret in find_in_line(line)[:1]:
            hits.append(Hit(display, number, name, mask(secret)))
    return hits


def candidate_files(root: Path) -> list[Path]:
    """Return tracked + untracked-not-ignored files, then the files of the build output folders."""
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        capture_output=True,
        check=True,
    ).stdout
    files = [root / name for name in listing.decode("utf8").split("\0") if name]
    for folder in OUTPUT_FOLDERS:
        directory = root / folder
        if directory.is_dir():
            files.extend(path for path in directory.rglob("*") if path.is_file())
    return sorted(set(files))


def main(argv: list[str] | None = None) -> int:
    """Scan ROOT (default: the current directory) and report hits."""
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]) if args else Path(".")
    try:
        files = candidate_files(root)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"error: {root} is not a git repository", file=sys.stderr)
        return 2
    hits = []
    for path in files:
        if path.is_symlink() and not path.exists():
            continue
        hits.extend(scan_file(path, path.relative_to(root).as_posix()))
    for hit in hits:
        print(f"{hit.path}:{hit.line}: {hit.pattern}: {hit.masked}")
    if hits:
        print(f"secrets: {len(hits)} suspected secret(s) in {len({hit.path for hit in hits})} file(s)")
        return 1
    print(f"secrets: OK ({len(files)} files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
