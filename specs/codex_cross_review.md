# Task: AI cross-review panel approvals (ADR-026)

Content may be published without a human approval when two independent AI reviewers approved it against real web sources, a tool confirmed their quoted passages, and a third reviewer's sample audit passed. Build the tooling and make the public gate and the site understand panel approvals.

Read first: `docs/verification/CROSS_REVIEW.md` (normative: §1 fields and verdicts, §2 source tiers, §7 procedure, §10 file formats), `docs/DECISIONS.md` ADR-021/022/026, `tools/seedtool.py` (`approval_state`, `review_hash`, `HUMAN_RE`, G022, `_normal`, `_read_text`, `check_quotes` and its fetch code), `tools/public_gate.py` (`wiki_hash`, `wiki_approval`, `gate`), `tools/review.py` (`approve_record`, `set_wiki_frontmatter`, `publish_wiki`, `worksheet_items`), `tools/yamlrec.py`, `tools/test_public_gate.py`, `src/lib/badges.ts`, `review/first-release.yaml` (worksheet format; see also `specs/codex_review_batch.md`).

You may create/edit: `tools/cross_review.py` (new), `tools/test_cross_review.py` (new), `tools/seedtool.py` (approval logic and G022 only), `tools/public_gate.py`, `tools/review.py` (shared helpers, `publish_wiki`), `src/lib/badges.ts`, `tests/unit/*.test.ts`, any `src/pages/**`/`src/components/**` file that shows the review label (label change only), `src/pages/about.astro`, `tests/e2e/*.spec.ts` (only assertions on the changed label text), `README.md` (new section "AI 교차 검증"). Nothing in `data/`, `src/content/`, `docs/`, `review/`. Stdlib + PyYAML (+ pypdf where seedtool already uses it). No network in tests, no installs.

## 1. Panel signature (structural rule)
In `seedtool.approval_state` and `public_gate.wiki_approval`, keep the human rule and also accept a review with `decision: approve` when all of these hold, otherwise return `"invalid"`:
- `by` matches `^panel:[a-z0-9][a-z0-9_-]*$`; `method == "cross-review"`; `at` set;
- `reviewers`: list of at least 2 distinct strings matching `^agent:[a-z0-9][a-z0-9_.-]*$`;
- `audit`: same pattern, not one of `reviewers`;
- `report == "review/cross/<release>"` where `<release>` is the part after `panel:`.
Freshness (`reviewed_hash`) works as for humans (`"stale"`). `by: agent:...` or anything else stays `"invalid"`. Add `approval_kind(review) -> "human" | "panel" | None` in seedtool. G022 text: "review must be by human:<id> or a cross-review panel, with a date". This is structural only; the gate does the deep check (§3).

## 2. `tools/cross_review.py`
`python tools/cross_review.py <packet|confirm|check|sample|approve> <release> [--graph a,b] [--wiki-dir DIR] [--root DIR]`. Defaults as in `public_gate` (`graph_paths()`, `src/content/wiki`); `--root` (default `.`) is where `review/` lives. Release dir `review/cross/<release>/`, worksheet `review/<release>.yaml`. Reports are `*.yaml` in the release dir except `packet.yaml`.

**Required fields** (`required_fields(kind, record) -> list[str]`, used by packet and check):
- entity: `name`; `summary` if present; `aliases` if non-empty; `classification` if `fields`/`parents` non-empty; `questions` if non-empty; `metadata` for papers (`title`, `authors`, `earliest_public_date`, `venue`, `identifiers`) and any record with `authors`/`venue`/`identifiers`.
- claim: `relation` (predicate, subject, object, qualifiers); `evidence[i]` for each evidence entry.
- item (`assessment_items`, e.g. `ai:lab-sdpa-01`): `prompt`, `answer`, `choices` if non-empty, `rationale` if present.
- wiki: `para:1..N`. Paragraphs: body after frontmatter; drop fenced code blocks and lines starting with `import ` or `export `; split on blank lines; drop blocks that are a single markdown heading line; strip; number the rest from 1 (prose, lists, `$$` math, JSX all count).

**packet**: write `packet.yaml` and a readable `packet.md` in the release dir: for every worksheet item, `id`, `kind`, current hash (`review_hash` / `wiki_hash`), required fields, and the content: graph record without `review` (claims: plus subject/object names, predicate meaning if available in Python or parsed from `src/lib/predicates.ts`, each evidence quote with locator, source title, version, `url`/`fulltext_url`); wiki: frontmatter without `review`/`status`/`published_at` and the numbered paragraphs. Never include worksheet `recommendation`, `decision`, `notes`, `fix`, `checked` (reviewers must be blind to the pre-review).

**confirm** `[--refresh]`: for every source of every check in every report, check that `_normal(passage)` occurs in `_normal(text)` of the page. For arXiv URLs (abs/pdf/html, any version) first try the cached fulltext the way `check_quotes` maps sources to `data/cache/fulltext`; otherwise fetch (reuse seedtool's fetch/`_read_text`, descriptive User-Agent, 20 s timeout, 10 MB cap, redirects). Cache extracted text in `.aixon/web-cache/<sha256(url)>.txt` (already gitignored); `--refresh` ignores it. Write `confirm.json`: `{schema: 1, generated_at, sources: {"<url>\n<passage>": {status: found|not-found|fetch-failed, detail, fetched_at, text_sha256}}}`. Print counts; exit 0.

**check**: `check_release(release, paths, wiki_dir, root) -> {id: [problems]}`; print `PASS`/`FAIL id: reasons`; exit 1 if any covered record fails. Rules:
- every report: `reviewer == "agent:" + file stem`, `release` matches, `start` in {source-first, claim-first, audit}.
- per id: reviewer reports (start ≠ audit) from ≥2 distinct reviewers contain it, with both `source-first` and `claim-first` among them.
- in every report that contains the id (audit included): `decision: approve`; `reviewed_hash` == current hash; `unchecked` empty; each required field has ≥1 passing check (`supported`, `computed`, `analogy-sourced`; `no-claim` only for wiki `para:N`); no failing check (`unsupported`, `wrong`, `analogy-unsourced`); `computed` has a non-empty `note`; each `supported`/`analogy-sourced` check passes the source rule.
- source rule: count only sources whose confirm status is `found`. Effective tier is `C` when the host is a community site (wikipedia.org, stackoverflow.com, *.stackexchange.com, reddit.com, medium.com, quora.com, *.tistory.com, velog.io, blog.naver.com, *.blogspot.com, *.wordpress.com, dev.to, *.hashnode.dev), else the tier the reviewer wrote. Passes with one found A or B source, or found C sources from ≥2 distinct hosts. For `metadata` and `evidence[i]` at least one found source must be effective tier A.

**sample**: k = max(3, ceil(0.1·n)) of the n passing ids (all if n ≤ 3), ordered by sha256(release + "\n" + sha256 of the concatenated bytes of the non-audit report files sorted by name + "\n" + id). Print and write `sample.json`.

**approve** `[--yes] [--today YYYY-MM-DD]`: refuse (exit 1, say why) unless an audit report exists whose reviewer is not a panel reviewer, covers exactly the recomputed sample, and every audited record passes the per-report rules; any audited `fix`/`reject` refuses the whole release. Then for each passing record: skip it if it has a fresh human approval; otherwise write the panel review block of CROSS_REVIEW.md §10 (graph: extract the writer from `review.approve_record` into a helper and reuse it; wiki: `review.set_wiki_frontmatter`), and publish wiki items whose worksheet entry has `publish: true` (make `publish_wiki` accept a fresh panel approval). Allowed inside agent sessions. Without `--yes` ask `패널 승인을 기록할까요? [y/N]`. Summary: approved N, published M, skipped (human) K, failed F.

## 3. Gate
In `public_gate.gate`, a record (graph or wiki) whose approval is a fresh panel approval is public only if `cross_review` says: it passes `check_release` for its release, the release audit passes as in `approve`, and the review block's `reviewers`/`audit` equal the reports'. Otherwise exclude it (`reason: "panel: <first problem>"`, or a wiki error reason). A missing release dir or `confirm.json` excludes (fail closed, no exception). Memoize per release. The gate stays offline.

## 4. Site
- `badges.ts`: replace `humanReviewLabel` with `reviewLabel(record)`: human → `사람 검토: <by>, <at>`; panel → `AI 교차 검증 <n>명, <at>`; else `검토 대기`. Update every caller (ClaimBadges, index, wiki page, coverage if it counts reviews); the reviewed count must include panel approvals. Make sure `by`, `at`, `method`, `reviewers` reach the pages in public builds without exposing other review fields.
- `about.astro`: "세 가지 배지" and "AI 콘텐츠 정책" now say a record is public after a human approval or a passed AI cross-review; add a short section "AI 교차 검증" (two independent AI reviewers, every statement checked against real web sources whose quoted passages a tool re-fetches, analogies only from human-written sources, third-reviewer sample audit, limits: same model family; the tool only confirms that a passage exists) linking `https://github.com/Keeweon-Choi/aixon/blob/main/docs/verification/CROSS_REVIEW.md`. Plain practitioner Korean, a few sentences.

## 5. Tests
`tools/test_cross_review.py` (tmp_path; graph from `tools/fixtures/mini_graph.yaml` plus one wiki doc like `tools/test_public_gate.py`; build reports and `confirm.json` in tmp):
- check passes with a source-first and a claim-first report and found sources; fails, each with a specific reason, for: one reviewer; two source-first reports; stale hash; a missing required field (wiki `para:2`); a failing verdict; a supported check whose source is not-found; one C source; two C sources on the same host; `metadata`/`evidence[0]` without a found tier-A source; reviewer ≠ file stem; non-empty `unchecked`.
- confirm with a monkeypatched fetch: found, not-found, fetch-failed; an arXiv source resolved from a tmp fulltext cache without fetching.
- sample is deterministic and changes when a report file changes.
- approve: refuses without an audit and when the audit has `fix`; writes panel blocks that `approval_state` calls approved; skips a record with a fresh human approval; publishes a wiki with `publish: true`; works with `CLAUDECODE=1` in the environment.
- gate: panel-approved records are public; after approve, flipping a report decision to `fix`, deleting `confirm.json`, or changing `reviewers` in the review block excludes the record; editing the record makes it stale; `by: agent:x` is invalid.
- vitest: `reviewLabel` for human, panel, none.

## Done when (record real outputs in CODEX_PROGRESS.md; mark anything you could not run NOT RUN)
`.venv/bin/python -m pytest tools tests/python -q`, `.venv/bin/ruff check tools tests/python`, `npx vitest run`, `npx prettier --check .`, `npx tsc --noEmit -p .`.
