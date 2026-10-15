# Task H1: align the verification harness with the public gate v2 (ADR-021)

Read first: `docs/DECISIONS.md` ADR-021..023, `specs/site_common.md`, `tools/public_gate.py`, `tools/review.py`, `tools/check_dist.py` (its `check_public`, `check_taint`, `V-SEC` checks were just rewritten by the orchestrator — keep their behaviour), `tests/fixtures/approve_fixtures.py`, `tests/fixtures/graph/site_graph.yaml` (header comment explains the public set).

You may edit: `tests/python/**`, `tools/validate_content.py`, `tools/scan_secrets.py`, `tools/verify.py`, `.github/workflows/**`, `README.md`, `tests/fixtures/approve_fixtures.py` (only to add the fixture marker comment). Do not edit `src/**`, `data/**`, `docs/**`, `specs/**`, `tools/seedtool.py`, `tools/public_gate.py`, `tools/review.py`, `tools/yamlrec.py`, `tools/check_dist.py`, `tests/fixtures/graph/**`, `tests/fixtures/wiki/**`, `tests/e2e/**`, `Makefile`. No network, do not run `npm install`/`pip install`.

## 1. Python tests that still assume the old approval model (11 failing now)
`.venv/bin/python -m pytest tools tests/python -q` currently fails in `tests/python/test_check_dist.py` (public-mode cases) and `tests/python/test_fixtures.py` (marker, review cases). Rewrite them for ADR-021:
- check_dist public mode now recomputes the allow-list with `public_gate.gate(graph_paths, wiki_dir)` and compares the dist against it; approvals must carry a correct `reviewed_hash`. Build tiny graphs/wiki in `tmp_path` and create approvals with `review.approve_record(...)` / `review.approve_wiki(...)` (never type a hash). Cases that must fail: a claim page whose claim is not in the gate (no approval / agent-signed approval / approval made stale by editing the record afterwards), a `graph.json` node or claim edge not in the gate, `node-index.json` entry not in the gate, an entity/field/wiki page not in the gate, the text of a non-public record's summary or quote appearing on a page (taint), a `--gate` file whose lists differ from a fresh gate run, an `on*=` attribute and a `javascript:` URL (V-SEC), an external `<img src>` (V-NO-CDN). One clean public tree with one approved claim + its two approved endpoint entities passes.
- test_fixtures: the agent-signed approval trap was removed from the site fixture on purpose (the gate test in `tools/test_public_gate.py` covers it); assert instead that the fixture's public set equals exactly `{paper:fixture-attention-2017, model:transformer, clm:intro-transformer, wiki:transformer}` via `public_gate.gate`, that every other claim has `review: null`, and that `tools/seedtool.py validate` on the fixture has 0 G errors. Add the `# TEST FIXTURE — not real research data` marker line to `tests/fixtures/approve_fixtures.py` (top of the docstring is fine) so the marker test passes.

## 2. validate_content.py
Add, each with a failing fixture under `tests/fixtures/wiki_bad/` **created by your Python tests in tmp_path** (do not add files to the committed fixture dirs except as described):
- (a) published wiki docs must pass the gate: call `public_gate.gate(graph_paths, wiki_dir)` and report each entry of `errors` as a `V-STATUS` error.
- (b) MDX must contain no `import`/`export` statements (labs use `<Lab id>`), no raw HTML elements outside an allow-list (the wiki components `Section Level ConceptLink Cite Callout Figure Lab`, inline SVG elements `svg g defs marker path line rect circle ellipse polyline polygon text tspan title desc`, and `br sup sub em strong code`), no `on*=` attributes, no `javascript:` (code blocks and math excluded from the scan) → `V-SEC` errors.
- (c) V-CITE-2 counts only `<Cite>` outside `<Level of="deep">`: a math/mechanism/history section whose only Cites sit inside a deep Level is an error.
The real document `src/content/wiki/scaled-dot-product-attention.mdx` must still pass (`make validate`).

## 3. scan_secrets.py
Add a test that the URL slug `same-risk-of-hallucination-as-other-ai-tools` and `sk-learn-style-names` are not reported, while a runtime-generated fake `sk-ant-` key and `AKIA` key are.

## 4. verify.py
Steps in order: lint, typecheck, test, validate, validate-fixtures, build, check-dist, build-public, check-dist-public, e2e, e2e-seed, secrets (each `make <step>`). Keep: continue after failures, non-zero exit if any failed, `summary.json` with versions, git commit + dirty flag, per-step logs; never record environment variables.

## 5. CI workflows (do not push or enable anything)
- `pages.yml`: job `build` (checkout, setup-node 22 with npm cache, setup-python 3.12, `npm ci`, `pip install -r requirements-dev.txt`, `make validate test`, `make build-public check-dist-public` with `PUBLIC_BASE=/${{ github.event.repository.name }}/` and `PUBLIC_SITE=https://${{ github.repository_owner }}.github.io`, upload-pages-artifact from `dist-public`); job `deploy` with `needs: build`, `environment: {name: github-pages, url: ...}`, `permissions: {pages: write, id-token: write}` only on this job (workflow-level `permissions: contents: read`), `actions/deploy-pages`.
- `verify-online.yml`: `schedule` weekly + `workflow_dispatch`, runs `make verify-online` (network checks of quotes and identifiers) and uploads `artifacts/verification/online/*.json`.
- `ci.yml`: keep `make verify`; upload `artifacts/verification/runs` and `playwright-report` with `if: always()`.
- README: one short section "공개 배포 전 체크" (repository Settings → Environments → github-pages → required reviewers; approvals via `tools/review.py`).

## Done when (record real outputs in CODEX_PROGRESS.md)
`.venv/bin/python -m pytest tools tests/python -q` all pass; `.venv/bin/ruff check tools tests` passes; `make validate` and `make validate-fixtures` pass; `npx prettier --check .` passes. Short checks only (each < 30 s); do not run builds or Playwright.
