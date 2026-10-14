import { expect, test } from '@playwright/test';
import { graph, nodeAnchor } from './support/data';
import { claimElement, expandField, node, showView } from './support/ui';

/**
 * Not a scenario of docs/CONTENT_VALIDATION_PLAN.md: it exercises the Atlas controls of the
 * selector contract (progressive expansion, type filters, verified-only, list toggle, #node- anchor)
 * on the fixture graph, whose shape is known.
 */
const ML = 'field:machine-learning';
const CV = 'field:computer-vision';
const NLP = 'field:natural-language-processing';
const DL = 'field:deep-learning';
const VISION_TRANSFORMERS = 'field:vision-transformers';
const MACHINE_TRANSLATION = 'field:machine-translation';

test.beforeEach(async ({ page }) => {
  await page.goto('atlas/');
  await expect(page.locator('[data-testid=graph-view][data-mode=atlas]')).toBeVisible();
});

test('E2E-11 the Atlas starts with the top fields only', async ({ page }) => {
  for (const id of [ML, CV, NLP]) {
    await expect(node(page, id)).toBeVisible();
    await expect(node(page, id)).toHaveAttribute('aria-expanded', 'false');
  }
  for (const id of [DL, VISION_TRANSFORMERS, MACHINE_TRANSLATION, 'model:vit', 'concept:softmax']) {
    await expect(node(page, id), `${id} is hidden until its field is expanded`).toHaveCount(0);
  }
});

test('E2E-11 expanding a field reveals its subfields and members, collapsing hides them', async ({
  page,
}) => {
  await expandField(page, CV);
  await expect(node(page, VISION_TRANSFORMERS)).toBeVisible();
  await expect(node(page, 'model:convnet'), 'a direct member').toBeVisible();
  await expect(node(page, 'model:vit')).toHaveCount(0);

  await expandField(page, VISION_TRANSFORMERS);
  await expect(node(page, 'model:vit')).toBeVisible();

  await node(page, CV).click();
  await expect(node(page, CV)).toHaveAttribute('aria-expanded', 'false');
  await expect(node(page, 'model:convnet')).toHaveCount(0);
});

test('E2E-11 selecting a node fills the panel with its name and links', async ({ page }) => {
  const data = graph();
  await expandField(page, CV);
  await expandField(page, VISION_TRANSFORMERS);
  await node(page, 'model:vit').click();
  const panel = page.getByTestId('node-panel');
  await expect(panel.locator('h2')).toHaveText(data.name('model:vit'));
  await expect(panel.getByTestId('panel-entity-link')).toHaveAttribute(
    'href',
    /\/e\/model\/vit\/$/,
  );
  await expect(panel.getByTestId('panel-wiki-link'), 'ViT has no wiki in the fixture').toHaveCount(
    0,
  );

  await expandField(page, NLP);
  await expandField(page, MACHINE_TRANSLATION);
  await node(page, 'method:scaled-dot-product-attention').click();
  await expect(panel.locator('h2')).toHaveText(data.name('method:scaled-dot-product-attention'));
  await expect(panel.getByTestId('panel-wiki-link'), 'SDPA has a wiki').toHaveAttribute(
    'href',
    /\/wiki\/scaled-dot-product-attention\/$/,
  );
});

test('E2E-11 an #node- anchor opens the Atlas with the chain of fields expanded', async ({
  page,
}) => {
  await page.goto(`atlas/${nodeAnchor('concept:softmax')}`);
  await expect(node(page, 'concept:softmax')).toBeVisible();
  await expect(node(page, ML)).toHaveAttribute('aria-expanded', 'true');
  await expect(node(page, DL)).toHaveAttribute('aria-expanded', 'true');
  await expect(page.getByTestId('node-panel').locator('h2')).toHaveText(
    graph().name('concept:softmax'),
  );
});

test('E2E-11 the node type filters hide and show nodes', async ({ page }) => {
  await expandField(page, CV);
  await expect(node(page, 'model:convnet')).toBeVisible();
  const models = page.getByTestId('type-filter-Model');
  await models.uncheck();
  await expect(node(page, 'model:convnet')).toHaveCount(0);
  await expect(node(page, CV), 'fields are not models').toBeVisible();
  await models.check();
  await expect(node(page, 'model:convnet')).toBeVisible();
});

test('E2E-11 "검증된 관계만" drops proposed relations and keeps verified ones', async ({
  page,
}) => {
  const proposed = 'clm:prereq-multi-head-attention-vit';
  const verified = 'clm:prereq-transformer-vit';
  await expandField(page, CV);
  await expandField(page, VISION_TRANSFORMERS);
  await expandField(page, NLP);
  await expandField(page, MACHINE_TRANSLATION);
  await expect(claimElement(page, proposed).first()).toBeVisible();
  await expect(claimElement(page, verified).first()).toBeVisible();

  await page.getByTestId('verified-only').check();
  await expect(claimElement(page, proposed)).toHaveCount(0);
  await expect(claimElement(page, verified).first()).toBeVisible();

  await page.getByTestId('verified-only').uncheck();
  await expect(claimElement(page, proposed).first()).toBeVisible();
});

test('E2E-11 the list toggle shows the same nodes as a table and back', async ({ page }) => {
  await expandField(page, CV);
  await showView(page, 'list');
  const rows = page.locator('[data-testid=graph-list] tr[data-node-id]');
  await expect(rows.first()).toBeVisible();
  const ids = await rows.evaluateAll((items) =>
    items.map((item) => item.getAttribute('data-node-id')),
  );
  expect(ids).toEqual(expect.arrayContaining([CV, VISION_TRANSFORMERS, 'model:convnet']));
  await showView(page, 'graph');
  await expect(node(page, CV)).toBeVisible();
});
