import { expect, test, type Locator } from '@playwright/test';
import {
  claimPath,
  entityPath,
  graph,
  normalize,
  RESEARCH_PREDICATES,
  wikiPath,
} from './support/data';
import { fmt4, softmaxCase } from './support/lab-fixture';
import { claimElement, hydrated, node, revealNode, showView, shownEvidence } from './support/ui';

/**
 * docs/CONTENT_VALIDATION_PLAN.md E2E-10 "Understanding Vision Transformer", real seed only.
 * Steps 1-4 are independent tests so a missing feature in one does not hide the others.
 */
const VIT = 'model:vit';
const TRANSFORMER = 'model:transformer';
const SDPA = 'method:scaled-dot-product-attention';
const CV = 'field:computer-vision';
const ADAPTS = 'clm:vit-adapts-transformer';

test.describe('E2E-10 Understanding Vision Transformer @seed @seed-only', () => {
  test('① Explore: Atlas → 컴퓨터 비전 → Vision Transformer shows the field and the Dosovitskiy 2020 paper', async ({
    page,
  }) => {
    const data = graph();
    const paper = data.introducingPaper(VIT);
    expect(paper, 'test data: a verified INTRODUCES claim for model:vit').toBeTruthy();
    const surname = String((paper!.authors as string[])[0])
      .split(' ')
      .pop() as string;
    const year = String(paper!.earliest_public_date).slice(0, 4);
    const fieldNames = data.fieldChain(VIT, CV).map((id) => data.name(id));
    const showsFieldAndPaper = async (where: Locator, label: string) => {
      await expect
        .soft(where, `${label} names the field`)
        .toContainText(new RegExp(fieldNames.length ? fieldNames.join('|') : data.name(CV)));
      await expect
        .soft(where, `${label} names the paper (${surname} ${year})`)
        .toContainText(new RegExp(`${surname}|${String(paper!.title).slice(0, 20)}`));
      await expect.soft(where, `${label} shows the year`).toContainText(year);
    };

    await page.goto('atlas/');
    await expect(page.locator('[data-testid=graph-view][data-mode=atlas]')).toBeVisible();
    const [topField] = data.fieldChain(VIT, CV);
    await expect(node(page, topField), 'fields start collapsed').toHaveAttribute(
      'aria-expanded',
      'false',
    );

    const vit = await revealNode(page, VIT, CV);
    await vit.click();
    const panel = page.getByTestId('node-panel');
    await expect(panel.locator('h2')).toHaveText(data.name(VIT));
    await showsFieldAndPaper(panel, 'the node panel');

    await panel.getByTestId('panel-entity-link').click();
    await expect(page).toHaveURL(new RegExp(`/${entityPath(VIT)}$`));
    await showsFieldAndPaper(page.locator('main'), 'the entity page');
  });

  test('② Trace: ADAPTS edge → claim page with quote, locator and arXiv link; CITES is no influence', async ({
    page,
  }) => {
    const data = graph();
    const claim = data.claim(ADAPTS);
    await page.goto('trace/');
    await expect(page.locator('[data-testid=graph-view][data-mode=trace]')).toBeVisible();

    await test.step('years: Transformer is older than ViT', async () => {
      await showView(page, 'graph');
      const years = { [TRANSFORMER]: data.introYear(TRANSFORMER), [VIT]: data.introYear(VIT) };
      expect(years[TRANSFORMER]).toBeLessThan(years[VIT] as number);
      for (const id of [TRANSFORMER, VIT]) {
        await expect(node(page, id)).toHaveAttribute('data-year', String(years[id]));
      }
    });

    await test.step('nothing but real research claims is drawn; CITES never', async () => {
      await showView(page, 'list');
      await expect(page.locator('tr[data-claim-id]').first()).toBeVisible();
      const shown = await page
        .locator('[data-claim-id]')
        .evaluateAll((elements) =>
          elements.map((element) => element.getAttribute('data-claim-id')),
        );
      const drawable = data.claims
        .filter((item) => RESEARCH_PREDICATES.includes(item.predicate))
        .filter((item) => !['rejected', 'deprecated'].includes(item.status))
        .map((item) => item.id);
      for (const id of shown) expect(drawable, `${id} is a drawable research claim`).toContain(id);
      const cites = data.claims.filter((item) => item.predicate === 'CITES');
      expect(cites.length).toBeGreaterThan(0);
      for (const item of cites) expect(shown).not.toContain(item.id);
      expect(shown).toContain(ADAPTS);
      await showView(page, 'graph');
    });

    await test.step('edge → claim page', async () => {
      await claimElement(page, ADAPTS).first().click();
      await expect(page).toHaveURL(new RegExp(`/${claimPath(ADAPTS)}$`));
      await expect(page.locator('main')).toContainText('ADAPTS');
      const [evidence] = claim.evidence ?? [];
      const shown = await shownEvidence(page);
      const item = shown.find((entry) => entry.quote === normalize(evidence.quote));
      expect(item, 'the quote of the claim is shown verbatim').toBeTruthy();
      expect(item?.locator).toContain(String(evidence.locator?.section));
      const source = data.source(String(evidence.source));
      expect(item?.href).toContain('arxiv.org');
      expect(item?.href?.startsWith(String(source.fulltext_url))).toBe(true);
      expect(item?.href).toContain('#:~:text=');
    });
  });

  test('③ Learn: the prerequisite lists equal the verified edges and lead from ViT to the SDPA wiki', async ({
    page,
  }) => {
    const data = graph();
    const expectPrerequisites = async (id: string) => {
      const listed = await page
        .locator('[data-testid=prerequisites] li[data-node-id]')
        .evaluateAll((items) => items.map((item) => item.getAttribute('data-node-id')));
      const hard = data.hardPrerequisites(id);
      const allowed = [...hard, ...data.softPrerequisites(id)];
      for (const required of hard)
        expect(listed, `${id}: verified prerequisite listed`).toContain(required);
      for (const shown of listed)
        expect(allowed, `${id}: only verified edges are listed`).toContain(shown);
      for (const unverified of data.unverifiedPrerequisites(id))
        expect(listed).not.toContain(unverified);
    };

    const path = data.prerequisitePath(VIT, SDPA);
    await page.goto(entityPath(path[0]));
    await expectPrerequisites(path[0]);
    for (const next of path.slice(1)) {
      await page
        .locator(`[data-testid=prerequisites] li[data-node-id="${next}"] a`)
        .first()
        .click();
      await expect(page).toHaveURL(new RegExp(`/${entityPath(next)}$`));
      await expect(page.locator('h1')).toHaveText(data.name(next));
      await expectPrerequisites(next);
    }

    await page.getByTestId('wiki-link').click();
    await expect(page).toHaveURL(new RegExp(`/${wikiPath('scaled-dot-product-attention')}$`));
  });

  test('④ Lab: temperature changes the probabilities as in the fixture and the quiz is graded', async ({
    page,
  }) => {
    const data = graph();
    const logits = [3, 1, 0.2, -1, 2.5];
    await page.goto(wikiPath('scaled-dot-product-attention'));
    const temperature = page.getByTestId('temperature');
    await hydrated(temperature);
    for (const [index, z] of logits.entries()) {
      await page.locator(`input[aria-label="logit ${index}"]`).fill(String(z));
    }

    const shown: string[] = [];
    for (const T of [2, 0.05]) {
      await temperature.fill(String(T));
      const expected = softmaxCase(logits, T).p;
      for (const [index, p] of expected.entries()) {
        await expect(page.getByTestId(`prob-${index}`)).toHaveText(fmt4(p));
      }
      shown.push(fmt4(expected[0]));
    }
    expect(shown[0], 'lowering T changes the largest probability').not.toBe(shown[1]);

    for (const item of data.labItems('lab:softmax-temperature')) {
      const slug = item.id.replace(/^ai:/, '');
      const quiz = page.getByTestId(`quiz-${slug}`);
      const result = page.getByTestId(`quiz-result-${slug}`);
      const submit = page.getByTestId(`quiz-submit-${slug}`);
      await quiz.scrollIntoViewIfNeeded();
      if (item.choices) {
        const radios = quiz.locator('input[type=radio]');
        await expect(radios).toHaveCount(item.choices.length);
        await radios.nth((item.answer + 1) % item.choices.length).check();
        await submit.click();
        await expect(result, `${slug} wrong choice`).toContainText('오답');
        await radios.nth(item.answer).check();
      } else {
        const input = quiz.locator('input[type=number]');
        await input.fill(String(item.answer + (item.tolerance ?? 0) + 5));
        await submit.click();
        await expect(result, `${slug} wrong number`).toContainText('오답');
        await input.fill(String(item.answer));
      }
      await submit.click();
      await expect(result, `${slug} right answer`).toContainText('정답');
      await expect(result, `${slug} rationale`).toContainText(normalize(String(item.rationale)));
    }
  });

  test('⑤ Remember: mastery is stored and survives a reload', async () => {
    test.fixme(true, 'P2 (ADR-019)');
  });

  test('⑥ Resume: the plan is recomputed from the stored mastery', async () => {
    test.fixme(true, 'P2 (ADR-019)');
  });
});
