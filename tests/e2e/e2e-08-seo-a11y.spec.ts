import { expect, test, type Page } from '@playwright/test';
import { claimPath, entityPath, graph, wikiPath } from './support/data';
import { node, showView } from './support/ui';

const VISITED = [
  { label: 'home', path: './' },
  { label: 'atlas', path: 'atlas/' },
  { label: 'trace', path: 'trace/' },
  { label: 'coverage', path: 'coverage/' },
  { label: 'search', path: 'search/' },
  { label: 'about', path: 'about/' },
  { label: 'field', path: entityPath('field:computer-vision') },
  { label: 'entity', path: entityPath('model:vit') },
  { label: 'claim', path: claimPath('clm:vit-adapts-transformer') },
  { label: 'wiki', path: wikiPath('scaled-dot-product-attention') },
];

for (const entry of VISITED) {
  test(`E2E-8 ${entry.label} page has title, description, lang and one h1`, async ({ page }) => {
    await page.goto(entry.path);
    await page.waitForLoadState('networkidle');
    await expect(page.locator('html')).toHaveAttribute('lang', 'ko');
    expect((await page.title()).trim(), 'title').not.toBe('');
    const description = await page.locator('meta[name=description]').getAttribute('content');
    expect((description ?? '').trim(), 'meta description').not.toBe('');
    await expect(page.locator('h1'), 'exactly one h1 after hydration').toHaveCount(1);
  });
}

test('E2E-8 the 404 page is also a proper page', async ({ page }) => {
  const response = await page.goto('no-such-page/');
  expect(response?.status()).toBe(404);
  await expect(page.locator('html')).toHaveAttribute('lang', 'ko');
  expect((await page.title()).trim()).not.toBe('');
  await expect(page.locator('h1')).toHaveCount(1);
});

/** Every drawn node (graph or list row) must say what it is: "<type> <name> <status>". */
async function expectLabelledNodes(page: Page) {
  const nodes = page.locator('[data-testid=graph-view] [data-node-id]');
  await expect(nodes.first()).toBeVisible();
  const labelled = await nodes.evaluateAll((elements) =>
    elements.map((element) => ({
      id: element.getAttribute('data-node-id') ?? '',
      label: element.getAttribute('aria-label') ?? '',
    })),
  );
  expect(labelled.length).toBeGreaterThan(0);
  for (const { id, label } of labelled) {
    if (!graph().entities.has(id)) continue; // the synthetic "+N개 더" node is not an entity
    expect(label, `${id} aria-label`).toContain(graph().name(id));
    expect(
      label.split(/\s+/).length,
      `${id} aria-label has type, name and status`,
    ).toBeGreaterThanOrEqual(3);
  }
}

test('E2E-8 graph nodes carry an aria-label (atlas, trace, local graph)', async ({ page }) => {
  for (const path of ['atlas/', 'trace/', entityPath('model:vit')]) {
    await page.goto(path);
    await expectLabelledNodes(page);
  }
});

test('E2E-8 list rows carry the same aria-label as graph nodes', async ({ page }) => {
  await page.goto('trace/');
  await showView(page, 'list');
  await expectLabelledNodes(page);
  await expect(node(page, 'model:vit')).toHaveAttribute(
    'aria-label',
    new RegExp(graph().name('model:vit')),
  );
});

test('E2E-8 KaTeX output includes MathML', async ({ page }) => {
  await page.goto(wikiPath('scaled-dot-product-attention'));
  const katex = page.locator('main .katex');
  expect(await katex.count()).toBeGreaterThan(0);
  const withoutMathml = await katex.evaluateAll(
    (elements) => elements.filter((element) => !element.querySelector('math')).length,
  );
  expect(withoutMathml, '.katex elements without <math>').toBe(0);
  await expect(page.locator('.katex-error')).toHaveCount(0);
});
