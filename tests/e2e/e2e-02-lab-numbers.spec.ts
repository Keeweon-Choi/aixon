import { expect, test } from '@playwright/test';
import { wikiPath } from './support/data';
import { entropy, fmt4, sdpaCase, softmaxCase } from './support/lab-fixture';
import { hydrated } from './support/ui';

const LOGITS = [3, 1, 0.2, -1, 2.5];

test('E2E-2 Lab numbers equal the numpy fixture to 4 decimals @seed', async ({ page }) => {
  await page.goto(wikiPath('scaled-dot-product-attention'));
  const temperature = page.getByTestId('temperature');
  await hydrated(temperature);

  await test.step('mode A: logits [3, 1, 0.2, -1, 2.5] at T = 1, 2 and 0.05', async () => {
    for (const [index, z] of LOGITS.entries()) {
      await page.locator(`input[aria-label="logit ${index}"]`).fill(String(z));
    }
    for (const T of [1, 2, 0.05]) {
      await temperature.fill(String(T));
      const expected = softmaxCase(LOGITS, T).p;
      for (const [index, p] of expected.entries()) {
        await expect(page.getByTestId(`prob-${index}`), `T=${T} prob-${index}`).toHaveText(fmt4(p));
      }
      await expect(page.getByTestId('max-prob'), `T=${T} max-prob`).toHaveText(
        fmt4(Math.max(...expected)),
      );
      await expect(page.getByTestId('entropy'), `T=${T} entropy`).toHaveText(
        fmt4(entropy(expected)),
      );
    }
  });

  await test.step('mode B: d_k = 512, seed 42, scaling off and on', async () => {
    // The two numbers quoted in docs/CONTENT_VALIDATION_PLAN.md E2E-2 are the fixture's.
    expect(fmt4(sdpaCase(512, false).mean_max_weight)).toBe('0.9548');
    expect(fmt4(sdpaCase(512, true).mean_max_weight)).toBe('0.3646');

    await page.getByTestId('dk').selectOption('512');
    await page.getByTestId('seed').fill('42');
    for (const scaled of [false, true]) {
      await page.getByTestId('scaling').setChecked(scaled);
      await page.getByTestId('compute').click();
      const expected = sdpaCase(512, scaled);
      const label = `scaling ${scaled ? 'on' : 'off'}`;
      await expect(page.getByTestId('mean-max-weight'), label).toHaveText(
        fmt4(expected.mean_max_weight),
      );
      await expect(page.getByTestId('var-qk'), label).toHaveText(fmt4(expected.var_qk));
      await expect(page.getByTestId('jac'), label).toHaveText(fmt4(expected.mean_jacobian_fro));
    }
  });
});
