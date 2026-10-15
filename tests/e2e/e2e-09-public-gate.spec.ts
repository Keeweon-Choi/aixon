import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { expect, test } from '@playwright/test';
import {
  BASE_PATH,
  DIST,
  FIXTURE_UNIQUE_WORD,
  GRAPH_FILES,
  SITE,
  WIKI_DIR,
  publicOrigin,
} from './support/env';
import { claimPath, entityPath, graph, wikiPath } from './support/data';

/**
 * The public build of the fixture data (dist-public-e2e, AIXON_BUILD=public) must contain only what
 * a human approved: docs/CONTENT_VALIDATION_PLAN.md E2E-9 and ADR-017.
 */
const DRAFT_BANNER = '검토 전 초안';
const url = (relative: string) => `${publicOrigin}${BASE_PATH}${relative}`;

function htmlFiles(directory: string): string[] {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(directory, entry.name);
    if (entry.isDirectory()) return entry.name === 'pagefind' ? [] : htmlFiles(full);
    return entry.name.endsWith('.html') ? [full] : [];
  });
}

/**
 * ADR-021: the public set of the fixture is decided by tools/public_gate.py (human approvals bound
 * to content hashes). Exactly these four records are public; everything else must be absent.
 */
const PUBLIC = {
  entities: ['model:transformer', 'paper:fixture-attention-2017'],
  claims: ['clm:intro-transformer'],
  wiki: ['transformer'],
};
const GATE_FILE = '.aixon/public-gate-e2e.json';
const SOURCE_TYPES = ['Source', 'Claim'];

const pageEntities = () =>
  [...graph().entities.keys()].filter((id) => !SOURCE_TYPES.includes(graph().types.get(id) ?? ''));
const hiddenEntities = () => pageEntities().filter((id) => !PUBLIC.entities.includes(id));
const hiddenClaims = () =>
  graph()
    .claims.map((claim) => claim.id)
    .filter((id) => !PUBLIC.claims.includes(id));
const wikiSlugs = () =>
  fs
    .readdirSync(WIKI_DIR)
    .filter((name) => name.endsWith('.mdx'))
    .map((name) => name.replace(/\.mdx$/, ''));
const hiddenWiki = () => wikiSlugs().filter((slug) => !PUBLIC.wiki.includes(slug));

interface PublicGraph {
  build: string;
  nodes: Array<{ id: string }>;
  edges: Array<{ id: string; kind: string }>;
}

test('E2E-9 the gate publishes exactly the four human-approved records', () => {
  const gate = JSON.parse(fs.readFileSync(GATE_FILE, 'utf8'));
  expect(gate.errors).toEqual([]);
  expect([...gate.entities].sort()).toEqual([...PUBLIC.entities].sort());
  expect(gate.claims).toEqual(PUBLIC.claims);
  expect(gate.wiki).toEqual(PUBLIC.wiki.map((slug) => `wiki:${slug}`));
  expect(hiddenEntities().length).toBeGreaterThan(5);
  expect(hiddenClaims().length).toBeGreaterThan(5);
  expect(hiddenWiki()).toEqual(['scaled-dot-product-attention']);
});

test('E2E-9 only the approved claim has a page; every other claim answers 404', async ({
  request,
}) => {
  const folders = fs.existsSync(`${DIST.public}/claims`)
    ? fs.readdirSync(`${DIST.public}/claims`)
    : [];
  expect(folders.sort()).toEqual(PUBLIC.claims.map((id) => id.replace(/^clm:/, '')).sort());

  for (const id of PUBLIC.claims) {
    expect((await request.get(url(claimPath(id)))).status(), id).toBe(200);
  }
  for (const id of hiddenClaims()) {
    expect((await request.get(url(claimPath(id)))).status(), id).toBe(404);
  }
});

test('E2E-9 only approved entities and wiki documents have pages; the rest answer 404', async ({
  request,
}) => {
  for (const id of PUBLIC.entities) {
    expect((await request.get(url(entityPath(id)))).status(), id).toBe(200);
  }
  for (const id of hiddenEntities()) {
    expect((await request.get(url(entityPath(id)))).status(), id).toBe(404);
  }
  for (const slug of PUBLIC.wiki) {
    expect((await request.get(url(wikiPath(slug)))).status(), slug).toBe(200);
  }
  for (const slug of hiddenWiki()) {
    expect((await request.get(url(wikiPath(slug)))).status(), slug).toBe(404);
  }
});

test('E2E-9 graph.json and node-index.json list only approved nodes and claims', async ({
  request,
}) => {
  const json = (await (await request.get(url('graph.json'))).json()) as PublicGraph;
  expect(json.build).toBe('public');
  expect(json.nodes.map((item) => item.id).sort()).toEqual([...PUBLIC.entities].sort());
  const claimEdges = json.edges.filter((edge) => edge.kind === 'claim');
  expect(claimEdges.map((edge) => edge.id)).toEqual(PUBLIC.claims);
  const publicIds = new Set(PUBLIC.entities);
  for (const node of json.nodes as Array<{ id: string; fields?: string[]; parents?: string[] }>)
    for (const ref of [...(node.fields ?? []), ...(node.parents ?? [])])
      expect(publicIds.has(ref), `${node.id} references the non-public ${ref}`).toBe(true);

  const index = (await (await request.get(url('node-index.json'))).json()) as Array<{
    id: string;
  }>;
  expect(index.map((item) => item.id).sort()).toEqual([...PUBLIC.entities].sort());
});

test('E2E-9 the published wiki has no draft banner; its claim citation links to the claim page', async ({
  page,
}) => {
  await page.goto(url(wikiPath('transformer')));
  await expect(page.locator('h1')).toHaveText('Transformer');
  await expect(page.getByTestId('status-banner')).toContainText('검토 완료');
  await expect(page.getByTestId('status-banner')).not.toContainText(DRAFT_BANNER);
  await expect(page.locator('main')).not.toContainText(DRAFT_BANNER);
  const claimLink = page
    .locator(`a[href="${BASE_PATH}${claimPath('clm:intro-transformer')}"]`)
    .first();
  await expect(claimLink, 'the citation of the approved claim links to its page').toBeVisible();
});

test('E2E-9 no emitted file mentions the draft banner, the draft document or a hidden record', () => {
  const pages = htmlFiles(DIST.public);
  expect(pages.length).toBeGreaterThan(0);
  const hiddenSummaries = hiddenEntities()
    .map((id) => String(graph().entity(id).summary ?? ''))
    .filter(Boolean);
  expect(hiddenSummaries.length).toBeGreaterThan(5);
  const emitted = [...pages, `${DIST.public}/graph.json`, `${DIST.public}/node-index.json`];
  for (const file of emitted) {
    const text = fs.readFileSync(file, 'utf8');
    expect(text, file).not.toContain(DRAFT_BANNER);
    expect(text, file).not.toContain(FIXTURE_UNIQUE_WORD);
    for (const summary of hiddenSummaries) expect(text, file).not.toContain(summary);
  }
});

test('E2E-9 an approved entity shows its summary; the 404 page stands in for a hidden one', async ({
  page,
}) => {
  const data = graph();
  await page.goto(url(entityPath('model:transformer')));
  await expect(page.locator('main')).toContainText(
    String(data.entity('model:transformer').summary),
  );

  const response = await page.goto(url(entityPath('model:vit')));
  expect(response?.status()).toBe(404);
  await expect(page.locator('h1')).toHaveText('페이지를 찾을 수 없습니다');
  await expect(page.locator('body')).not.toContainText(String(data.entity('model:vit').summary));
});

test('E2E-9 robots.txt allows indexing and lists the sitemap; the sitemap omits unpublished pages', async ({
  request,
}) => {
  const robots = await (await request.get(url('robots.txt'))).text();
  expect(robots).not.toMatch(/^Disallow:\s*\/\s*$/m);
  expect(robots).toMatch(/^Allow:\s*\/\s*$/m);
  expect(robots).toContain(`Sitemap: ${SITE}${BASE_PATH}sitemap-index.xml`);

  const index = await (await request.get(url('sitemap-index.xml'))).text();
  const sitemaps = [...index.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);
  expect(sitemaps.length).toBeGreaterThan(0);
  const locations: string[] = [];
  for (const sitemap of sitemaps) {
    const body = await (await request.get(url(sitemap.split('/').pop() as string))).text();
    locations.push(...[...body.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]));
  }
  const at = (relative: string) => `${SITE}${BASE_PATH}${relative}`;
  expect(locations).toContain(at(wikiPath('transformer')));
  for (const id of PUBLIC.entities) expect(locations).toContain(at(entityPath(id)));
  for (const id of PUBLIC.claims) expect(locations).toContain(at(claimPath(id)));
  for (const id of hiddenEntities()) expect(locations).not.toContain(at(entityPath(id)));
  for (const id of hiddenClaims()) expect(locations).not.toContain(at(claimPath(id)));
  for (const slug of hiddenWiki()) expect(locations).not.toContain(at(wikiPath(slug)));
});

test('E2E-9 the search index of the public build does not know the draft', async ({ page }) => {
  await page.goto(url('search/'));
  const input = page.locator('#search input');
  const publishedHit = page.locator('#search a[href*="/wiki/transformer/"]');
  const draftHit = page.locator('#search a[href*="/wiki/scaled-dot-product-attention/"]');

  await input.fill('Transformer');
  await expect(publishedHit.first(), 'the search works and knows the published page').toBeVisible();

  await input.fill(FIXTURE_UNIQUE_WORD);
  await expect(publishedHit, 'the new search replaced the old results').toHaveCount(0);
  await expect(draftHit).toHaveCount(0);
});

test('E2E-9 tools/check_dist.py --mode public accepts the public build', () => {
  const python = fs.existsSync('.venv/bin/python') ? '.venv/bin/python' : 'python3';
  const result = spawnSync(
    python,
    [
      'tools/check_dist.py',
      DIST.public,
      '--base',
      BASE_PATH,
      '--mode',
      'public',
      '--site',
      SITE,
      '--graph',
      GRAPH_FILES.join(','),
      '--wiki-dir',
      WIKI_DIR,
    ],
    { encoding: 'utf8' },
  );
  expect(`${result.stdout}${result.stderr}`, 'check_dist output').toContain('check-dist public');
  expect(result.status, result.stdout).toBe(0);
});
