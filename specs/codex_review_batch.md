# Task: batch approval and wiki publishing in tools/review.py (ADR-021)

Read first: `docs/DECISIONS.md` ADR-021, `tools/review.py`, `tools/public_gate.py`, `tools/yamlrec.py`, `tools/test_public_gate.py`.

Context: a reviewer prepares a worksheet; the user reads it and approves many records at once. Approvals must stay human-only and bound to content hashes exactly as `review.approve_record` / `review.approve_wiki` already do.

You may edit: `tools/review.py`, `tools/test_public_gate.py` (or a new `tools/test_review.py`), and the "콘텐츠 작업 흐름" section of `README.md`. Nothing else. No network, no installs.

## Worksheet format (`review/<name>.yaml`)
```yaml
release: first-release
items:
  - id: clm:intro-sdpa          # graph record id, or wiki:<slug>
    kind: claim                  # claim | entity | wiki | item
    recommendation: approve      # what the pre-reviewer suggests: approve | fix | exclude
    decision: approve            # what the user decides (defaults to recommendation); only "approve" is approved
    publish: true                # wiki only: also set status: published
    notes: "..."
```

## Commands
1. `review.py approve-batch <worksheet> --by human:<name> [--yes]`
   - Refuse inside agent sessions exactly like `approve` (same check, exit 2).
   - List every item with `decision: approve` (id, kind) and the ones skipped (decision fix/exclude), then ask `승인할까요? [y/N]` on stdin unless `--yes`.
   - Approve each item with the existing functions (`approve_record` for graph ids, `approve_wiki` for `wiki:` ids). For wiki items with `publish: true`, after approving set `status: published` and `published_at: <today>` in the frontmatter (line edit; `wiki_hash` already ignores status/published_at, so the approval stays fresh). Unknown ids or failures are reported and the command exits 1 after processing the rest.
   - Print a summary: approved N, published M, skipped K, failed F.
2. `review.py publish wiki:<slug> --by human:<name>`: same status change for one document; refuse unless its approval is fresh (`wiki_approval == "approved"`); refuse in agent sessions.
3. Put the logic in a function `approve_batch(paths, wiki_dir, worksheet_path, by, today) -> dict` that the CLI calls, so tests can call it directly (tests run inside an agent session where the CLI refuses).

## Tests (tmp_path, reuse the helpers in tools/test_public_gate.py)
- A worksheet with two entities, one claim between them and a wiki doc citing the claim (`decision: approve`, wiki `publish: true`) plus one `decision: exclude` entity → after `approve_batch` the gate (`public_gate.gate`) lists exactly the approved records and the wiki; the excluded entity has no review; the wiki has `status: published` and a fresh approval.
- `publish` refuses a wiki whose approval is stale (edit the body after approving).
- The CLI `approve-batch` exits 2 when `CLAUDECODE=1` is in the environment.

## Done when
`.venv/bin/python -m pytest tools -q` and `.venv/bin/ruff check tools` pass. Record the real outputs in CODEX_PROGRESS.md.
