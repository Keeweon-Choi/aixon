import { expect, test } from '@playwright/test';
import { BASE_PATH, QUICK_QUERY } from './support/env';
import { entityPath, graph, nodeAnchor, wikiFrontmatter } from './support/data';
import { quickSearch } from './support/ui';

const SDPA = 'method:scaled-dot-product-attention';
const SOFTMAX = 'concept:softmax';

test('E2E-1 Graph → Wiki → Related → Graph @seed', async ({ page }) => {
  const data = graph();

  await test.step('home → quick search → Scaled Dot-Product Attention entity page', async () => {
    await page.goto('./');
    await quickSearch(page, QUICK_QUERY.main);
    await page.locator(`#quick-results a[data-node-id="${SDPA}"]`).click();
    await expect(page).toHaveURL(new RegExp(`/${entityPath(SDPA)}$`));
    await expect(page.locator('h1')).toHaveText(data.name(SDPA));
  });

  await test.step('entity page → "Wiki 읽기" → wiki page', async () => {
    await page.getByTestId('wiki-link').click();
    await expect(page).toHaveURL(/\/wiki\/scaled-dot-product-attention\/$/);
    const title = String(wikiFrontmatter('scaled-dot-product-attention').title);
    await expect(page.locator('h1')).toHaveText(title);
  });

  await test.step('the wiki links to its entity page and its Atlas node', async () => {
    await expect(page.getByTestId('wiki-entity-link')).toHaveAttribute(
      'href',
      `${BASE_PATH}${entityPath(SDPA)}`,
    );
    await expect(page.getByTestId('wiki-atlas-link')).toHaveAttribute(
      'href',
      `${BASE_PATH}atlas/${nodeAnchor(SDPA)}`,
    );
  });

  await test.step('the wiki shows KaTeX math, a code block and the draft banner', async () => {
    await expect(page.locator('main .katex').first()).toBeVisible();
    await expect(page.locator('.katex-error')).toHaveCount(0);
    await expect(page.locator('main pre code').first()).toBeVisible();
    await expect(page.getByTestId('status-banner')).toContainText('검토 전 초안');
  });

  await test.step('switching 직관 / 기초 / 심화 changes the visible sections', async () => {
    const level = (value: string) => page.locator(`input[name=wiki-level][value=${value}]`);
    const section = (value: string) =>
      page.locator(`section.wiki-section[data-level="${value}"]`).first();
    const visibleCount = () => page.locator('section.wiki-section[data-level]:visible').count();

    await expect(level('fundamentals'), 'default level is 기초').toBeChecked();
    await expect(section('intuition')).toBeVisible();
    await expect(section('fundamentals')).toBeVisible();
    await expect(section('deep')).toBeHidden();
    const atFundamentals = await visibleCount();

    await level('intuition').check();
    await expect(section('fundamentals')).toBeHidden();
    await expect(section('deep')).toBeHidden();
    await expect(section('intuition')).toBeVisible();
    const atIntuition = await visibleCount();

    await level('deep').check();
    await expect(section('deep')).toBeVisible();
    await expect(section('fundamentals')).toBeVisible();
    const atDeep = await visibleCount();

    expect(atIntuition).toBeLessThan(atFundamentals);
    expect(atFundamentals).toBeLessThan(atDeep);
  });

  await test.step('the generated "관련 개념" and "참고문헌과 근거" lists are filled', async () => {
    await expect(page.getByTestId('related').locator('a').first()).toBeVisible();
    await expect(page.getByTestId('references').locator('li').first()).toBeVisible();
  });

  await test.step('wiki → "아틀라스에서 보기" selects the same node in the Atlas, then back', async () => {
    await page.getByTestId('wiki-atlas-link').click();
    await expect(page).toHaveURL(new RegExp(`/atlas/${nodeAnchor(SDPA)}$`));
    await expect(page.getByTestId('node-panel').locator('h2')).toHaveText(data.name(SDPA));
    await page.goBack();
    await page.getByTestId('wiki-entity-link').click();
    await expect(page).toHaveURL(new RegExp(`/${entityPath(SDPA)}$`));
    await page.goBack();
  });

  await test.step('ConceptLink "softmax" → softmax entity page', async () => {
    await page.locator(`a[data-concept-id="${SOFTMAX}"]:visible`).first().click();
    await expect(page).toHaveURL(new RegExp(`/${entityPath(SOFTMAX)}$`));
    await expect(page.locator('h1')).toHaveText(data.name(SOFTMAX));
  });

  await test.step('"그래프에서 보기" → Atlas with softmax selected', async () => {
    const atlasLink = page.getByTestId('atlas-link');
    await expect(atlasLink).toHaveAttribute('href', `${BASE_PATH}atlas/${nodeAnchor(SOFTMAX)}`);
    await atlasLink.click();
    await expect(page).toHaveURL(new RegExp(`/atlas/${nodeAnchor(SOFTMAX)}$`));
    await expect(page.locator('[data-testid=graph-view][data-mode=atlas]')).toBeVisible();
    await expect(page.getByTestId('node-panel').locator('h2')).toHaveText(data.name(SOFTMAX));
    const panel = await page.getByTestId('node-panel').innerText();
    expect(panel, 'the type is shown in Korean').toContain('개념');
    expect(panel, 'no raw type or status value').not.toMatch(/\bConcept\b|\bactive\b/);
  });
});

test('E2E-1 a 2-character Korean query finds at least one node @seed', async ({ page }) => {
  await page.goto('./');
  await quickSearch(page, QUICK_QUERY.short);
  expect(await page.locator('#quick-results a[data-node-id]').count()).toBeGreaterThanOrEqual(1);
});

test('E2E-1 quick search results are keyboard navigable @seed', async ({ page }) => {
  await page.goto('./');
  await quickSearch(page, QUICK_QUERY.short);
  const links = page.locator('#quick-results a[data-node-id]');
  const hrefs = await links.evaluateAll((anchors) =>
    anchors.map((anchor) => new URL((anchor as HTMLAnchorElement).href).pathname),
  );
  expect(hrefs.length).toBeGreaterThan(0);
  expect(hrefs.length, 'at most 8 results').toBeLessThanOrEqual(8);

  await page.locator('#quick-search').press('ArrowDown');
  await page.locator('#quick-search').press('Enter');
  await expect.poll(() => new URL(page.url()).pathname).not.toBe(BASE_PATH);
  expect(hrefs).toContain(new URL(page.url()).pathname);
  await expect(page.locator('h1')).toBeVisible();
});

test('E2E-1 wiki "관련 개념" respects direction and status @seed', async ({ page }) => {
  const data = graph();
  const MHA = 'method:multi-head-attention';
  await page.goto('wiki/scaled-dot-product-attention/');
  const ids = (selector: string, predicate = '') =>
    page
      .getByTestId('related')
      .locator(`${selector} li[data-node-id]${predicate}`)
      .evaluateAll((items) => [...new Set(items.map((item) => item.getAttribute('data-node-id')))]);
  const sorted = (values: (string | null)[]) => [...values].sort();

  const hard = await ids('[data-testid=related-prerequisites]', '[data-predicate=PREREQUISITE_OF]');
  expect(sorted(hard), 'prerequisites = verified PREREQUISITE_OF claims into SDPA').toEqual(
    sorted(data.hardPrerequisites(SDPA)),
  );
  const soft = await ids(
    '[data-testid=related-prerequisites]',
    '[data-predicate=RECOMMENDED_BEFORE]',
  );
  expect(sorted(soft)).toEqual(sorted(data.softPrerequisites(SDPA)));
  const all = await ids('[data-testid=related-prerequisites]');
  expect(all).not.toContain(MHA);
  for (const unverified of data.unverifiedPrerequisites(SDPA))
    expect(all).not.toContain(unverified);

  expect(await ids('[data-testid=related-dependents]')).toContain(MHA);
  await expect(page.getByTestId('related-prerequisites')).toContainText('먼저 알아야 할 개념');
  await expect(page.getByTestId('related-dependents')).toContainText('바탕으로 하는');
});

test('E2E-1 wiki references and inline citations are human readable @seed', async ({ page }) => {
  await page.goto('wiki/scaled-dot-product-attention/');
  const references = await page.getByTestId('references').innerText();
  expect(references).not.toMatch(/clm:|src:/);
  const cites = await page.locator('sup.cite').allInnerTexts();
  expect(cites.length).toBeGreaterThan(0);
  for (const text of cites) expect(text).not.toMatch(/clm:|src:/);
  // a claim reference reads as the claim's sentence, a source reference as its paper title and version
  const [firstSource] = wikiFrontmatter('scaled-dot-product-attention').sources as string[];
  const source = graph().source(firstSource);
  await expect(page.getByTestId('references')).toContainText(graph().name(String(source.paper)));
  await expect(page.getByTestId('references')).toContainText(String(source.version));
  await expect(page.getByTestId('references')).toContainText('은(는)');
});
