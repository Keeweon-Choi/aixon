# Task F13: make quote and identifier checks reproducible (design audit F-13)

Problem (audit F-13): no Source has `content_sha256`, so a changed arXiv HTML/PDF is never noticed (W106 can never fire); `tools/verify_identifiers.py --write-checked` is a no-op since it switched to a YAML parser; `paper:deng2009-imagenet` and `paper:krizhevsky2012-alexnet` carry `metadata_checked.arxiv` although they have no arXiv id (the tool skips them).

You may edit: `tools/seedtool.py` (only the `quotes` command and `check_quotes`), `tools/verify_identifiers.py`, `tools/test_seedtool.py`, `tools/test_verify_identifiers.py`, `data/seed/seed_graph.yaml` and `data/graph/atlas.yaml` **only through the tools below** (no hand edits), `data/seed/validate_snapshot.json` (only if the warning counts legitimately change). Use `tools/yamlrec.py` (`set_field`, `delete_field`, `edit_file`) for every YAML write so the rest of the file stays byte-identical. No network: `data/cache/fulltext` holds the cached sources (if it is missing in your worktree, stop and say so).

## 1. `seedtool.py quotes --pin`
- New flag `--pin`: after checking, write `content_sha256` (sha256 of the fetched/cached bytes, the same digest `check_quotes` already computes) into each Source record that was read, in whichever graph file defines it. Without `--pin` nothing is written.
- A Source whose stored `content_sha256` differs from the current bytes yields `source_changed` (existing behaviour) and makes the command exit 1.
- `no_fulltext_url` already counts as a failure (exit 1) — keep it.
- Tests (`tools/test_seedtool.py`, tmp_path graphs + a fake cache like the existing quote tests): `--pin` writes the digest and a second run is clean; changing the cached bytes afterwards gives `source_changed` and exit 1; other lines of the YAML file are unchanged byte-for-byte.
- Then run on the real data: `.venv/bin/python tools/seedtool.py quotes --offline --cache data/cache/fulltext --pin data/seed/seed_graph.yaml data/graph/atlas.yaml` → all `found`, and all 15 seed Sources now carry `content_sha256`.

## 2. `verify_identifiers.py --write-checked`
- Make it actually write: for every paper whose arXiv title matched, set `metadata_checked.arxiv` to the run date (keep other keys of `metadata_checked`), via yamlrec. Never stamp a paper that has no arXiv id; remove an existing `metadata_checked.arxiv` from such papers (`paper:deng2009-imagenet`, `paper:krizhevsky2012-alexnet`) — if `metadata_checked` becomes empty, delete the key.
- Tests (`tools/test_verify_identifiers.py`, offline with `tools/fixtures/arxiv_sample.xml` or a monkeypatched fetch): stamps are written for matches only, non-arXiv papers lose a stale stamp, a non-matching title is not stamped, other YAML lines unchanged.
- On the real data, without network you cannot run the matcher; only apply the removal of the two wrong stamps (write a tiny function or flag such as `--drop-stale-stamps` that needs no network, and run it).

## Done when (record real outputs in CODEX_PROGRESS.md)
`.venv/bin/python -m pytest tools -q` passes; `.venv/bin/ruff check tools` passes; `.venv/bin/python tools/seedtool.py validate data/seed/seed_graph.yaml data/graph/atlas.yaml` has 0 G errors; the offline quotes run above prints 132 `found` and exit 0; `git diff --stat data/` shows only the added `content_sha256` lines and the two removed stamps.
