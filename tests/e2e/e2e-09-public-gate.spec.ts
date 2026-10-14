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
import { claimPath, entityPath, graph, humanApproved, wikiPath } from './support/data';

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

const approved = () => graph().claims.filter(humanApproved);
const unapproved = () => graph().claims.filter((claim) => !humanApproved(claim));

test('E2E-9 the fixture has exactly one human-approved claim', () => {
  expect(approved().map((claim) => claim.id)).toEqual(['clm:intro-transformer']);
  expect(unapproved().length).toBeGreaterThan(5);
});

test('E2E-9 only the approved claim has a page; unapproved claims answer 404', async ({
  request,
}) => {
  const folders = fs.existsSync(`${DIST.public}/claims`)
    ? fs.readdirSync(`${DIST.public}/claims`)
    : [];
  expect(folders.sort()).toEqual(
    approved()
      .map((claim) => claim.id.replace(/^clm:/, ''))
      .sort(),
  );

  for (const claim of approved()) {
    expect((await request.get(url(claimPath(claim.id)))).status(), claim.id).toBe(200);
  }
  for (const claim of unapproved()) {
    expect((await request.get(url(claimPath(claim.id)))).status(), claim.id).toBe(404);
  }
});

test('E2E-9 an approval by an agent does not publish a claim', async ({ request }) => {
  const trap = graph().claim('clm:intro-vit');
  expect(trap.review?.decision).toBe('approve');
  expect(String(trap.review?.by)).toMatch(/^agent:/);
  expect((await request.get(url(claimPath(trap.id)))).status()).toBe(404);
  const json = await (await request.get(url('graph.json'))).json();
  expect(json.edges.map((edge: { id: string }) => edge.id)).not.toContain(trap.id);
});

test('E2E-9 the draft wiki is absent, the published and reviewed one is present', async ({
  page,
  request,
}) => {
  expect((await request.get(url(wikiPath('scaled-dot-product-attention')))).status()).toBe(404);

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

test('E2E-9 no emitted file mentions the draft banner or the draft document', () => {
  const pages = htmlFiles(DIST.public);
  expect(pages.length).toBeGreaterThan(0);
  for (const file of pages) {
    const text = fs.readFileSync(file, 'utf8');
    expect(text, file).not.toContain(DRAFT_BANNER);
    expect(text, file).not.toContain(FIXTURE_UNIQUE_WORD);
  }
});

test('E2E-9 graph.json has no unapproved claim edge and says it is public', async ({ request }) => {
  const json = await (await request.get(url('graph.json'))).json();
  expect(json.build).toBe('public');
  const edges = json.edges.filter((edge: { kind: string }) => edge.kind === 'claim');
  expect(edges.map((edge: { id: string }) => edge.id).sort()).toEqual(
    approved().map((claim) => claim.id),
  );
});

test('E2E-9 unapproved AI summaries are replaced by "준비 중"', async ({ page }) => {
  const data = graph();
  const approvedSummary = data.entity('model:transformer');
  await page.goto(url(entityPath('model:transformer')));
  await expect(page.locator('main')).toContainText(String(approvedSummary.summary));

  const hidden = data.entity('model:vit');
  await page.goto(url(entityPath('model:vit')));
  await expect(page.locator('h1')).toHaveText(data.name('model:vit'));
  await expect(page.locator('main')).toContainText('준비 중');
  await expect(page.locator('main')).not.toContainText(String(hidden.summary));
  await expect(page.locator('meta[name=description]')).not.toHaveAttribute(
    'content',
    new RegExp(String(hidden.summary).slice(0, 12)),
  );
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
  expect(locations).toContain(`${SITE}${BASE_PATH}wiki/transformer/`);
  expect(
    locations.filter((location) => location.includes('/scaled-dot-product-attention/')),
  ).toEqual([`${SITE}${BASE_PATH}e/method/scaled-dot-product-attention/`]);
  for (const claim of unapproved())
    expect(locations).not.toContain(`${SITE}${BASE_PATH}${claimPath(claim.id)}`);
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
