import { expect, test } from '@playwright/test';
import { FIXTURE_UNIQUE_WORD } from './support/env';
import { wikiFrontmatter } from './support/data';

test('E2E-5 Pagefind finds a word from the wiki body and opens the page', async ({ page }) => {
  await page.goto('search/');
  const input = page.locator('#search input');
  await input.fill(FIXTURE_UNIQUE_WORD);

  const result = page.locator('#search a[href*="/wiki/scaled-dot-product-attention/"]').first();
  await expect(result).toBeVisible();
  await result.click();

  await expect(page).toHaveURL(/\/wiki\/scaled-dot-product-attention\/(\?[^#]*)?(#.*)?$/);
  const title = String(wikiFrontmatter('scaled-dot-product-attention').title);
  await expect(page.locator('h1')).toHaveText(title);
  await expect(page.locator('main')).toContainText(FIXTURE_UNIQUE_WORD);
});
