# Shared rules for the AIXON v0.1 site tasks (A: graph views, B: pages + lab + public gate, C: harness)

Background: `specs/codex_site_mvp.md` is the full original spec. A first pass produced a thin skeleton (now merged on `main`). Tasks A/B/C finish it. Read `specs/codex_site_mvp.md` for anything not restated here.

## Non-negotiable
1. **Do not edit**: `data/seed/**`, `data/graph/**`, `docs/**`, `specs/**`, `src/content/wiki/**` (the representative wiki doc is orchestrator-owned), `tools/seedtool.py`, `tools/test_seedtool.py`, `tools/gen_lab_fixtures.py`, `tools/verify_identifiers.py`. Test data goes only under `tests/fixtures/`.
2. **Never invent research facts.** Every fact shown on a page comes from the graph YAML or the MDX. Fixture files under `tests/fixtures/` may contain made-up text but must start with the comment `# TEST FIXTURE — not real research data` and use `graph.id: fixture-…`; never reference fixtures from the real build.
3. **AI content is never auto-published**: in `AIXON_BUILD=public` nothing without a human approval (`review.decision: approve` by `human:…`) is emitted — no page, no graph.json entry, no search index entry, no sitemap URL (see task B for the exact rules).
4. Static only. No new npm/pip dependencies (no network). KaTeX works through `remark-math` + `rehype-katex` (Astro 7 needs the already-installed `@astrojs/markdown-remark`); do not remove them or hand-write MathML.
5. **Code style**: readable code, one statement per line, `npx prettier --write <files you touched>` before committing; `npx prettier --check .` must pass. Avoid `any`: extend the types in `src/lib/graph/types.ts`. Korean UI text. Escape untrusted strings — never build HTML with `innerHTML` from data; use DOM APIs / JSX.
6. Commit after each step with a clear message; keep `CODEX_PROGRESS.md` honest — a check you did not run is "NOT RUN", never "passed".

## File ownership (to avoid merge conflicts)
| Task | Owns |
|---|---|
| A | `src/islands/GraphView.tsx`, new `src/islands/graph/**`, new `src/lib/graph/view.ts`, `src/pages/atlas.astro`, `src/pages/trace.astro`, `src/pages/graph.json.ts`, new `src/styles/graph.css`, `tests/unit/view.test.ts` |
| B | every other file under `src/` (pages, layouts, components, `src/lib/graph/index.ts`, `types.ts`, `predicates.ts`, `url.ts`, `src/lib/lab/**`, `SoftmaxTemperatureLab.tsx`, `src/styles/global.css`, `src/pages/node-index.json.ts`), `tests/unit/graph.test.ts`, `tests/unit/lab.test.ts` |
| C | `tests/fixtures/**`, `tests/e2e/**`, `tests/python/**`, `playwright.config.ts`, `tools/validate_content.py`, `tools/check_dist.py`, `tools/scan_secrets.py`, `tools/verify.py`, `Makefile`, `.github/**`, `README.md`, `vitest.config.ts` |

If you need a change in a file you do not own, describe it under "## Requests for other tasks" in `CODEX_PROGRESS.md` instead of editing it.

## Selector contract (A and B implement it; C's E2E tests rely on it)
| Where | Selector | Meaning |
|---|---|---|
| header | `#quick-search` (input), `#quick-results a[data-node-id]` | quick search; ArrowDown/ArrowUp/Enter navigate results |
| graph views (A) | `[data-testid=graph-view][data-mode=atlas|local|trace]` | root of each view |
| | `[data-node-id="<id>"]` | a node (graph or list row), `aria-label="<타입> <이름> <상태>"` |
| | `[data-testid=node-panel]` with `h2` = node name, links `[data-testid=panel-entity-link]`, `[data-testid=panel-wiki-link]` (only if a wiki exists) | selected-node panel |
| | `[data-testid=list-toggle]` | switches graph ⇄ list (`목록 보기`/`그래프 보기`) |
| | `[data-testid=graph-list]` table; rows `tr[data-node-id]`; edge rows `tr[data-claim-id]` with an `a` to the claim page | list view |
| | `[data-testid=type-filter-<Type>]` checkboxes, `[data-testid=verified-only]` | atlas filters |
| | field nodes have `aria-expanded`; activating one reveals its subfields and members | progressive expansion |
| | `[data-claim-id="<clm id>"]` on every rendered edge label/button | edge → claim page |
| | `[data-year]` on trace nodes | introduction year |
| entity page (B) | `h1` = entity name, `[data-testid=wiki-link]`, `[data-testid=atlas-link]` (→ `atlas/#node-<id with : → ~>`), `[data-testid=prerequisites] li[data-node-id]`, `[data-testid=entity-claims] a[data-claim-id]` | |
| wiki page (B) | `[data-testid=status-banner]`, `input[name=wiki-level][value=intuition|fundamentals|deep]`, `section.wiki-section[data-level]`, `a[data-concept-id]`, `[data-testid=related]`, `[data-testid=references]` | |
| claim page (B) | `h1` = natural-language claim sentence, `[data-testid=claim-status]`, `[data-testid=evidence] [data-stance]` items each with `blockquote`, `[data-testid=locator]`, `a[data-testid=source-link]` (href contains `#:~:text=`) | Evidence Inspector |
| lab (B) | `input[aria-label="logit 0"]`…`logit 4`, `[data-testid=temperature]` (number input; the slider mirrors it), `[data-testid=prob-0…4]`, `max-prob`, `entropy`; `[data-testid=dk]` select, `[data-testid=scaling]` checkbox, `[data-testid=seed]`, `[data-testid=compute]`, `var-qk`, `mean-max-weight`, `jac`; quiz `[data-testid=quiz-<item slug>]`, `[data-testid=quiz-submit-<item slug>]`, `[data-testid=quiz-result-<item slug>]` (text contains `정답` or `오답`) | numbers are rendered with 4 decimals |
| coverage (B) | `[data-testid=coverage-table]` | |
| search (B) | `#search` (Pagefind UI) | |

`<item slug>` = the part after `ai:` in the assessment item id (e.g. `ai:lab-sdpa-01` → `lab-sdpa-01`).

## Environment facts
- Node 22, `node_modules` present (do not run `npm install`). Python: `.venv/bin/python` (pyyaml, pypdf, pytest, ruff, numpy).
- Astro needs a writable config dir: prefix astro commands with `XDG_CONFIG_HOME=/tmp/aixon-astro-config ASTRO_TELEMETRY_DISABLED=1`.
- Full build of the real data (`AIXON_BUILD=preview npx astro build`) takes ~10 s and emits ~640 pages.
