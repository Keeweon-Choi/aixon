/** Small Playwright helpers shared by the specs. Selectors follow specs/site_common.md exactly. */
import { expect, type Locator, type Page } from '@playwright/test';
import { graph, normalize } from './data';

/** Status badge wording: the enum value or the Korean label (docs/02 section 7, docs/05 section 4.3). */
export const STATUS_PATTERN: Record<string, RegExp> = {
  verified: /verified|검증/i,
  disputed: /disputed|논쟁|이견|다툼|상충|반박/i,
  proposed: /proposed|미검증|제안|후보/i,
  rejected: /rejected|기각/i,
};

export const node = (page: Page, id: string): Locator => page.locator(`[data-node-id="${id}"]`);

export const claimElement = (page: Page, id: string): Locator =>
  page.locator(`[data-claim-id="${id}"]`);

/** Wait until the Astro island around `locator` has hydrated (React handlers are attached). */
export async function hydrated(locator: Locator): Promise<void> {
  await locator.first().scrollIntoViewIfNeeded();
  await expect
    .poll(
      () =>
        locator.first().evaluate((element) => {
          const island = element.closest('astro-island');
          return !island || !island.hasAttribute('ssr');
        }),
      { message: 'the Astro island never hydrated' },
    )
    .toBe(true);
}

/** Scroll through the page so every client:visible island hydrates, then wait for all of them. */
export async function hydrateAll(page: Page): Promise<void> {
  await page.evaluate(async () => {
    for (let y = 0; y < document.body.scrollHeight; y += window.innerHeight) {
      window.scrollTo(0, y);
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    window.scrollTo(0, 0);
  });
  await expect
    .poll(() => page.locator('astro-island[ssr]').count(), {
      message: 'islands are still waiting to hydrate',
    })
    .toBe(0);
}

/** Page width facts for the "no horizontal overflow" rule. */
export async function widths(page: Page): Promise<{ scrollWidth: number; innerWidth: number }> {
  return page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    innerWidth: window.innerWidth,
  }));
}

/** Type into the header quick search until results show up (the index loads asynchronously). */
export async function quickSearch(page: Page, query: string): Promise<void> {
  const input = page.locator('#quick-search');
  const results = page.locator('#quick-results a[data-node-id]');
  await expect(async () => {
    await input.fill('');
    await input.fill(query);
    await expect(results.first()).toBeVisible({ timeout: 2000 });
  }).toPass({ timeout: 15_000 });
}

/** Switch a graph view to the table or the canvas; both are required by the contract. */
export async function showView(page: Page, view: 'graph' | 'list'): Promise<void> {
  const list = page.getByTestId('graph-list');
  const showingList = await list.isVisible();
  if ((view === 'list') !== showingList) await page.getByTestId('list-toggle').click();
  if (view === 'list') await expect(list).toBeVisible();
  else await expect(list).toBeHidden();
}

/** Expand a field node (progressive expansion) and wait for aria-expanded to say so. */
export async function expandField(page: Page, id: string): Promise<void> {
  const field = node(page, id);
  await expect(field).toBeVisible();
  if ((await field.getAttribute('aria-expanded')) !== 'true') await field.click();
  await expect(field).toHaveAttribute('aria-expanded', 'true');
}

/** Expand the chain of fields that leads to `id`, then return the node locator. */
export async function revealNode(page: Page, id: string, through?: string): Promise<Locator> {
  const chain = graph().fieldChain(id, through);
  expect(
    chain.length,
    `test data: ${id} declares no fields, so the Atlas has no field to expand to reveal it`,
  ).toBeGreaterThan(0);
  for (const field of chain) await expandField(page, field);
  const target = node(page, id);
  await expect(target).toBeVisible();
  return target;
}

/** Everything the claim page shows for each evidence item. */
export interface ShownEvidence {
  stance: string | null;
  quote: string;
  locator: string;
  href: string | null;
}

export async function shownEvidence(page: Page): Promise<ShownEvidence[]> {
  const items = await page.locator('[data-testid=evidence] [data-stance]').evaluateAll((elements) =>
    elements.map((element) => ({
      stance: element.getAttribute('data-stance'),
      quote: element.querySelector('blockquote')?.textContent ?? '',
      locator: element.querySelector('[data-testid=locator]')?.textContent ?? '',
      href: element.querySelector('a[data-testid=source-link]')?.getAttribute('href') ?? null,
    })),
  );
  return items.map((item) => ({
    ...item,
    quote: normalize(item.quote),
    locator: normalize(item.locator),
  }));
}

/** Text of an `<output>`-like readout, trimmed. */
export async function readout(page: Page, testId: string): Promise<string> {
  return normalize(await page.getByTestId(testId).textContent());
}
