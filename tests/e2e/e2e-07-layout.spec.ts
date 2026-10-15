import { expect, test, type Page } from '@playwright/test';
import { QUICK_QUERY } from './support/env';
import { claimPath, entityPath, graph, wikiPath } from './support/data';
import { fitView, hydrateAll, node, quickSearch, widths } from './support/ui';

const settled = async () => {};

const PAGES: Array<{ label: string; path: string; ready: (page: Page) => Promise<void> }> = [
  { label: 'home', path: './', ready: settled },
  {
    label: 'wiki',
    path: wikiPath('scaled-dot-product-attention'),
    // The lab is the widest block of the wiki: let it render before measuring.
    ready: hydrateAll,
  },
  {
    label: 'entity',
    path: entityPath('model:vit'),
    ready: async (page) => {
      await graphReady('local')(page);
      await hydrateAll(page);
    },
  },
  { label: 'claim', path: claimPath('clm:vit-adapts-transformer'), ready: settled },
  { label: 'atlas', path: 'atlas/', ready: graphReady('atlas') },
  { label: 'trace', path: 'trace/', ready: graphReady('trace') },
  {
    label: 'coverage',
    path: 'coverage/',
    ready: async (page) => expect(page.getByTestId('coverage-table')).toBeVisible(),
  },
];

function graphReady(mode: string) {
  return async (page: Page) =>
    expect(page.locator(`[data-testid=graph-view][data-mode=${mode}]`)).toBeVisible();
}

for (const entry of PAGES) {
  test(`E2E-7 ${entry.label} has no horizontal overflow @seed`, async ({ page }) => {
    await page.goto(entry.path);
    await entry.ready(page);
    await page.waitForLoadState('networkidle');
    const { scrollWidth, innerWidth } = await widths(page);
    expect(
      scrollWidth,
      `scrollWidth ${scrollWidth} > innerWidth ${innerWidth}`,
    ).toBeLessThanOrEqual(innerWidth);
  });
}

test('E2E-7 on a phone the Atlas starts as a list, on a desktop as a graph @seed', async ({
  page,
  isMobile,
}) => {
  await page.goto('atlas/');
  await graphReady('atlas')(page);
  if (isMobile) {
    await expect(page.getByTestId('graph-list')).toBeVisible();
    await expect(page.getByTestId('list-toggle')).toBeVisible();
  } else {
    await expect(page.getByTestId('graph-list')).toBeHidden();
  }
});

test('E2E-7 the header quick search is usable at this width @seed', async ({ page }) => {
  await page.goto('./');
  const input = page.locator('#quick-search');
  await expect(input).toBeVisible();
  await quickSearch(page, QUICK_QUERY.main);

  const viewport = page.viewportSize();
  const results = page.locator('#quick-results a[data-node-id]').first();
  for (const target of [input, results]) {
    const box = await target.boundingBox();
    expect(box, 'in the layout').toBeTruthy();
    expect(box!.x).toBeGreaterThanOrEqual(0);
    expect(box!.x + box!.width).toBeLessThanOrEqual(viewport!.width);
  }
  const { scrollWidth, innerWidth } = await widths(page);
  expect(scrollWidth, 'the open result list must not widen the page').toBeLessThanOrEqual(
    innerWidth,
  );
});

test('E2E-7 selecting a node shows its panel without scrolling (atlas) @seed', async ({ page }) => {
  const top = graph()
    .ofType('ResearchField')
    .find((field) => !(field.parents ?? []).length);
  await page.goto('atlas/');
  await graphReady('atlas')(page);
  await node(page, String(top?.id)).click();
  const panel = page.getByTestId('node-panel');
  await expect(panel.locator('h2')).toHaveText(graph().name(String(top?.id)));
  await expect(panel.locator('h2')).toBeInViewport({ ratio: 1 });
  await expect(panel.getByTestId('panel-entity-link')).toBeInViewport({ ratio: 1 });
});

test('E2E-7 trace: the panel is in view after a selection and axis labels do not cover nodes @seed', async ({
  page,
  isMobile,
}) => {
  await page.goto('trace/');
  await graphReady('trace')(page);
  if (isMobile) await page.getByTestId('list-toggle').click();
  if (!isMobile) await fitView(page);
  await node(page, 'model:vit').click();
  await expect(page.getByTestId('node-panel').locator('h2')).toBeInViewport({ ratio: 1 });
  if (isMobile) return; // the axis labels belong to the drawn graph

  const boxes = async (selector: string) =>
    page.locator(selector).evaluateAll((elements) =>
      elements.map((element) => {
        const { left, right, top, bottom } = element.getBoundingClientRect();
        return { left, right, top, bottom };
      }),
    );
  const labels = await boxes('[data-testid=trace-labels] span');
  const nodes = await boxes('[data-testid=graph-view] [data-node-id]');
  expect(labels.length).toBeGreaterThan(0);
  for (const label of labels)
    for (const box of nodes)
      expect(
        label.left < box.right &&
          box.left < label.right &&
          label.top < box.bottom &&
          box.top < label.bottom,
        'an axis label overlaps a node',
      ).toBe(false);
});
