import { expect, test, type Page } from '@playwright/test';
import { claimPath, entityPath, graph, normalize, type Claim } from './support/data';
import { STATUS_PATTERN, shownEvidence } from './support/ui';

/** Compare everything the claim page shows with the claim in the YAML. */
async function expectEvidenceMatches(page: Page, claim: Claim) {
  const data = graph();
  const shown = await shownEvidence(page);
  const quoted = (claim.evidence ?? []).filter((item) => item.quote);
  expect(shown.length, 'one item per evidence entry').toBe((claim.evidence ?? []).length);

  for (const expected of quoted) {
    const match = shown.find(
      (item) => item.stance === expected.stance && item.quote === normalize(expected.quote),
    );
    expect(
      match,
      `evidence "${expected.quote}" (${expected.stance}) is shown verbatim`,
    ).toBeTruthy();
    for (const key of ['section', 'table', 'figure', 'page'] as const) {
      const value = expected.locator?.[key];
      if (value !== undefined) expect(match?.locator).toContain(String(value));
    }
    const source = data.source(String(expected.source));
    const [base, fragment] = String(match?.href).split('#:~:text=');
    expect(base, 'deep link starts with fulltext_url (fallback url)').toBe(
      String(source.fulltext_url ?? source.url),
    );
    const words = decodeURIComponent(fragment.split('&')[0]).split(/\s+/);
    const quoteWords = normalize(expected.quote).split(' ');
    expect(words.length).toBeGreaterThanOrEqual(Math.min(6, quoteWords.length));
    expect(words.length).toBeLessThanOrEqual(10);
    expect(normalize(expected.quote).startsWith(words.join(' '))).toBe(true);
  }
}

test('E2E-3 entity page → verified claim page shows quote, locator, source link and review', async ({
  page,
}) => {
  const data = graph();
  const claim = data.claim('clm:intro-transformer');

  await test.step('entity page lists the claim', async () => {
    await page.goto(entityPath('model:transformer'));
    await page.locator(`[data-testid=entity-claims] a[data-claim-id="${claim.id}"]`).click();
    await expect(page).toHaveURL(new RegExp(`/${claimPath(claim.id)}$`));
  });

  await test.step('claim page: statement, status badge, human review', async () => {
    await expect(page.locator('h1')).not.toBeEmpty();
    const status = page.getByTestId('claim-status');
    await expect(status).toContainText(STATUS_PATTERN[claim.status]);
    await expect(status, 'no bare status word (ADR-022)').not.toContainText(/\bverified\b|검증됨/);
    await expect(status, 'human review state').toContainText('fixture-editor');
    await expect(status, 'human review state').toContainText(/사람 검토/);
  });

  await test.step('evidence: quote, locator and #:~:text= source link match the YAML', async () => {
    await expectEvidenceMatches(page, claim);
  });
});

test('E2E-3 a claim nobody reviewed says so', async ({ page }) => {
  const claim = graph().claim('clm:intro-sdpa');
  await page.goto(claimPath(claim.id));
  await expect(page.getByTestId('claim-status')).toContainText(/사람 검토 대기|검토 대기/);
  await expect(page.getByTestId('claim-status')).not.toContainText('fixture-editor');
});

test('E2E-3 a disputed claim shows supporting and contradicting evidence', async ({ page }) => {
  const claim = graph().claim('clm:transformer-mitigates-sequential');
  await page.goto(claimPath(claim.id));
  await expect(page.getByTestId('claim-status')).toContainText(STATUS_PATTERN.disputed);
  await expect(page.locator('[data-testid=evidence] [data-stance=supports]')).toHaveCount(1);
  await expect(page.locator('[data-testid=evidence] [data-stance=contradicts]')).toHaveCount(1);
  await expectEvidenceMatches(page, claim);
});

test('E2E-3 a proposed claim is labelled as such and is not a prerequisite', async ({ page }) => {
  const data = graph();
  const proposed = data.claim('clm:prereq-multi-head-attention-vit');
  await page.goto(claimPath(proposed.id));
  await expect(page.getByTestId('claim-status')).toContainText(STATUS_PATTERN.proposed);

  await page.goto(entityPath('model:vit'));
  const listed = await page
    .locator('[data-testid=prerequisites] li[data-node-id]')
    .evaluateAll((items) => items.map((item) => item.getAttribute('data-node-id')));
  for (const id of data.hardPrerequisites('model:vit')) expect(listed).toContain(id);
  for (const id of data.unverifiedPrerequisites('model:vit')) expect(listed).not.toContain(id);
  expect(listed).not.toContain(proposed.subject);
});

test('E2E-3 a rejected claim keeps its page with the rejection reason', async ({ page }) => {
  const claim = graph().claim('clm:vit-extends-convnet');
  await page.goto(claimPath(claim.id));
  await expect(page.getByTestId('claim-status')).toContainText(STATUS_PATTERN.rejected);
  await expect(page.locator('main')).toContainText(String(claim.rejected_reason));
});

test('E2E-3 the claim page shows the Korean predicate and field names for qualifiers', async ({
  page,
}) => {
  const data = graph();
  await page.goto(claimPath('clm:vit-adapts-transformer'));
  const qualifiers = data.claim('clm:vit-adapts-transformer').qualifiers ?? {};
  const main = await page.locator('main').innerText();
  expect(main).not.toMatch(/field:|from_field|to_field/);
  expect(main).toContain('적용');
  expect(main).toContain(data.name(String(qualifiers.from_field)));
  expect(main).toContain(data.name(String(qualifiers.to_field)));
});
