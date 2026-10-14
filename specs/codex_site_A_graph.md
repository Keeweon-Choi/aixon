# Task A: real graph views (Atlas, local neighbourhood, Trace) for the AIXON static site

Read first: `specs/site_common.md` (rules, file ownership, selector contract — binding), `docs/05_UX_AND_INTERACTIVE_LAB.md` §3.2, §3.3, §4.1, §4.3, §4.5, `docs/02_DOMAIN_ONTOLOGY.md` §6 (projections) and §8 (predicates), `docs/DECISIONS.md` ADR-020.

Current state: `src/islands/GraphView.tsx` renders a flat list of buttons; React Flow and dagre are installed but unused. Replace it.

## Data (`src/pages/graph.json.ts`)
Keep the current shape and add what the views need: per node `fields`, `parents` (fields only), `year`, `status`, `hasWiki` (true when `${AIXON_WIKI_DIR}/<slug>.mdx` exists **and** the build may show it — in `public` only `status: published`), `wikiUrl`; per claim edge `predicate`, `status`, `reviewed`, `url`, `qualifiers.for_dimension`. Taxonomy (`parent`) and membership edges stay as they are. In `public` builds only approved claims are present (the loader already filters) — do not re-add others.

## Pure helpers (`src/lib/graph/view.ts`, no React, fully unit-tested in `tests/unit/view.test.ts`)
- `nodeAnchor(id)` / `parseNodeAnchor(hash)` — `#node-<id with ':' → '~'>`, round-trip safe.
- `atlasVisible(data, expanded:Set<string>, filters)` → visible nodes + edges: top fields (no parents) always visible; an expanded field shows its child fields and its member nodes; filters: node types (checkbox per type), `verifiedOnly` (drops non-`verified` claim edges), cap 80 nodes → plus one synthetic node `+N개 더` (N = hidden count).
- `localNeighbourhood(data, focus)` → focus + depth-1 neighbours via claim edges (research + prerequisite + structural), excluding CITES unless toggled.
- `traceLayout(data, options)` → research claims only (INTRODUCES, EXTENDS, ADAPTS, IMPROVES_ON, ADDRESSES, MITIGATES, COMPARED_WITH; CITES only when `showCites`); x = (year − minYear) × 160 px; lanes (y) by the node's first field, stable alphabetical order; nodes without year go to a left "연도 미상" column. Papers are not drawn as separate nodes when the INTRODUCES target exists (put the paper title in the node tooltip/panel).
- `dagreLayout(nodes, edges, direction='TB')` → positions via `@dagrejs/dagre` for atlas and local views.
- `edgeStyle(predicate, status)` → the notation table of 05 §4.3 (solid/dashed/dotted/thick, marker, label, `미검증` badge for proposed, warning for disputed; rejected/deprecated never drawn).
Unit tests: anchor round-trip incl. ids with `.`/`-`; expansion shows children only after expand; 80-node cap and the `+N개 더` count; verifiedOnly removes a proposed edge; trace keeps ADAPTS ViT←Transformer and drops a CITES-only pair (no influence edge is created from CITES — V-CITES-NOT-INFLUENCE); year ordering; dagre gives distinct positions. Build the test data inline in the test file (small object literals), not from the real seed.

## Island (`src/islands/GraphView.tsx` + `src/islands/graph/**`)
- React Flow (`@xyflow/react`) canvas with custom node components; `nodesFocusable` true, `edgesFocusable` false; node `aria-label` per the selector contract; Enter/Space on a node selects it (and toggles expansion for fields).
- Modes: `atlas` (progressive expansion from top fields, type filters, verified-only toggle, node panel), `local` (entity pages: depth-1 neighbourhood, small height), `trace` (custom positions from `traceLayout`, year axis labels, lane labels, `showCites` toggle default off, clicking an edge label navigates to the claim page).
- Node panel `[data-testid=node-panel]`: name (h2), type, status badge, summary (as delivered by graph.json — it is already "준비 중" for unapproved AI summaries in public builds), introduction year, link to entity page, link to wiki if `hasWiki`, and for fields "펼치기/접기".
- `#node-…` in the URL selects that node on load: in atlas mode expand the chain of parent fields of the node (via its `fields`/`parents`) so it is visible, select it, centre it (`fitView` on it). Update the hash when the user selects a node (history.replaceState).
- 목록 보기: an HTML table with the same visible nodes (and, in trace/local, edges as rows with `data-claim-id` and a link to the claim page). Default to list view when `matchMedia('(max-width: 700px)')` matches. The list must be usable without the canvas (keyboard + screen reader).
- Loading/error states: "그래프를 불러오는 중…", and on fetch failure "그래프를 불러오지 못했습니다" with the list of top fields rendered server-side as a fallback (pass top fields as props from the page).
- Styles in `src/styles/graph.css` (import from the island): canvas height 70vh on atlas/trace, 360 px on local; no horizontal page overflow at 390 px width (the canvas itself may pan).

## Pages
- `src/pages/atlas.astro`: h1 "Interactive Atlas", short how-to text, `<GraphView client:only="react" mode="atlas" topFields={…} />` plus a `<noscript>` list of top fields.
- `src/pages/trace.astro`: h1 "연구 계보", legend of edge notation, `<GraphView client:only="react" mode="trace" />`, and the same `<noscript>` fallback (list of verified research claims linking to claim pages).

## Done when (record real outputs in CODEX_PROGRESS.md)
`npx vitest run tests/unit/view.test.ts` passes; `npx prettier --check src tests` passes; `XDG_CONFIG_HOME=/tmp/aixon-astro-config ASTRO_TELEMETRY_DISABLED=1 npx astro check` 0 errors; `XDG_CONFIG_HOME=/tmp/aixon-astro-config ASTRO_TELEMETRY_DISABLED=1 AIXON_BUILD=preview npx astro build` succeeds. Browser checks are done by the orchestrator (you may skip them; say NOT RUN).
