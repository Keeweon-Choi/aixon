import { expect, test } from '@playwright/test';
import { BASE_PATH } from './support/env';
import { RESEARCH_PREDICATES, claimPath, graph } from './support/data';
import { claimElement, node, showView } from './support/ui';

const TRANSFORMER = 'model:transformer';
const VIT = 'model:vit';
const ADAPTS = 'clm:vit-adapts-transformer';

interface GraphJson {
  build: string;
  nodes: Array<{ id: string }>;
  edges: Array<{ id: string; kind: string; predicate?: string; source: string; target: string }>;
}

test.beforeEach(async ({ page }) => {
  await page.goto('trace/');
  await expect(page.locator('[data-testid=graph-view][data-mode=trace]')).toBeVisible();
});

test('E2E-4 model nodes carry their introduction year', async ({ page }) => {
  const data = graph();
  await showView(page, 'graph');
  for (const id of ['model:convnet', TRANSFORMER, VIT]) {
    await expect(node(page, id), `${id} is drawn`).toBeVisible();
    await expect(node(page, id)).toHaveAttribute('data-year', String(data.introYear(id)));
  }
  expect(Number(await node(page, TRANSFORMER).getAttribute('data-year'))).toBeLessThan(
    Number(await node(page, VIT).getAttribute('data-year')),
  );
});

test('E2E-4 the time axis puts older work to the left', async ({ page }) => {
  await showView(page, 'graph');
  const left = async (id: string) => (await node(page, id).boundingBox())?.x ?? Number.NaN;
  expect(await left('model:convnet')).toBeLessThan(await left(TRANSFORMER));
  expect(await left(TRANSFORMER)).toBeLessThan(await left(VIT));
});

test('E2E-4 clicking an edge opens its claim page, and graph.json agrees', async ({
  page,
  request,
}) => {
  await showView(page, 'graph');
  await claimElement(page, ADAPTS).first().click();
  await expect(page).toHaveURL(new RegExp(`/${claimPath(ADAPTS)}$`));
  await expect(page.locator('h1')).not.toBeEmpty();

  const response = await request.get(`${BASE_PATH}graph.json`);
  expect(response.ok()).toBe(true);
  const json = (await response.json()) as GraphJson;
  const edge = json.edges.find((item) => item.id === ADAPTS);
  expect(edge, 'the clicked claim id exists in graph.json').toBeTruthy();
  expect(edge?.predicate).toBe('ADAPTS');
  expect([edge?.source, edge?.target]).toEqual([VIT, TRANSFORMER]);
});

test('E2E-4 the list view has a row per edge with a link to the claim page', async ({ page }) => {
  await showView(page, 'list');
  const row = page.locator(`tr[data-claim-id="${ADAPTS}"]`);
  await expect(row).toBeVisible();
  await row.locator('a').first().click();
  await expect(page).toHaveURL(new RegExp(`/${claimPath(ADAPTS)}$`));
});

test('E2E-4 only research claims are drawn: no CITES, no rejected, no prerequisites', async ({
  page,
}) => {
  const data = graph();
  await showView(page, 'list');
  await expect(page.locator('tr[data-claim-id]').first()).toBeVisible();
  const shown = await page
    .locator('[data-claim-id]')
    .evaluateAll((elements) => elements.map((element) => element.getAttribute('data-claim-id')));
  expect(shown.length).toBeGreaterThan(0);

  const drawable = data.claims
    .filter((claim) => RESEARCH_PREDICATES.includes(claim.predicate))
    .filter((claim) => !['rejected', 'deprecated'].includes(claim.status));
  for (const id of shown) {
    expect(
      drawable.map((claim) => claim.id),
      `${id} must be a real, drawable research claim`,
    ).toContain(id);
  }
  expect(shown, 'a verified claim is drawn').toContain(ADAPTS);
  expect(shown).not.toContain('clm:vit-extends-convnet');

  // The ViT and ConvNet papers only cite each other: both models are listed, but nothing joins them.
  const cites = data.claims.filter((claim) => claim.predicate === 'CITES');
  expect(cites.length).toBeGreaterThan(0);
  for (const claim of cites) expect(shown).not.toContain(claim.id);
  await expect(node(page, VIT)).toBeVisible();
  await expect(node(page, 'model:convnet')).toBeVisible();
  const joining = drawable.filter(
    (claim) =>
      [claim.subject, claim.object].includes(VIT) &&
      [claim.subject, claim.object].includes('model:convnet'),
  );
  expect(joining).toEqual([]);
});
