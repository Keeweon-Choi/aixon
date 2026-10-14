import { expect, test } from '@playwright/test';
import { BASE_PATH } from './support/env';
import { claimPath, entityPath, graph, wikiFrontmatter, wikiPath } from './support/data';

const pages = () => [
  {
    label: 'wiki',
    path: wikiPath('scaled-dot-product-attention'),
    h1: String(wikiFrontmatter('scaled-dot-product-attention').title),
  },
  { label: 'entity', path: entityPath('model:vit'), h1: graph().name('model:vit') },
  { label: 'claim', path: claimPath('clm:vit-adapts-transformer'), h1: undefined },
];

for (const target of pages()) {
  test(`E2E-6 ${target.label} page: direct link and reload give the same h1 @seed`, async ({
    page,
  }) => {
    const first = await page.goto(target.path);
    expect(first?.status()).toBe(200);
    const heading = (await page.locator('h1').textContent())?.trim();
    expect(heading).toBeTruthy();
    if (target.h1) expect(heading).toBe(target.h1);

    const second = await page.reload();
    expect(second?.status()).toBe(200);
    await expect(page.locator('h1')).toHaveText(String(heading));
    expect(new URL(page.url()).pathname).toBe(`${BASE_PATH}${target.path}`);
  });
}

test('E2E-6 an unknown path answers 404 with the 404 page @seed', async ({ page }) => {
  for (const path of [
    'wiki/no-such-document/',
    'e/model/no-such-model/',
    'claims/no-such-claim/',
  ]) {
    const response = await page.goto(path);
    expect(response?.status(), path).toBe(404);
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator(`a[href="${BASE_PATH}"]`).first()).toBeVisible();
  }
});
