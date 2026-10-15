import fs from 'node:fs';
import { defineConfig, devices } from '@playwright/test';
import { BASE_PATH, DIST, PORTS, target } from './tests/e2e/support/env';

/**
 * Two targets, chosen with AIXON_E2E_TARGET (see the Makefile):
 *   fixture (default)  the fixture graph + wiki build (dist-e2e) and the fixture public build
 *                      (dist-public-e2e); every spec except the @seed-only ones
 *   seed               the real seed build (dist-seed); only the specs tagged @seed
 * All builds use the base path /aixon/ so GitHub Pages behaviour is exercised.
 */
const astroEnvironment = {
  AIXON_BASE: BASE_PATH,
  XDG_CONFIG_HOME: '/tmp/aixon-astro-config',
  ASTRO_TELEMETRY_DISABLED: '1',
};

function previewServer(outDir: string, port: number) {
  if (!fs.existsSync(`${outDir}/index.html`)) {
    throw new Error(`${outDir}/index.html is missing: run the matching make build target first`);
  }
  return {
    command: `npx astro preview --outDir ${outDir} --port ${port} --host 127.0.0.1 --ignore-lock`,
    url: `http://127.0.0.1:${port}${BASE_PATH}`,
    reuseExistingServer: false,
    timeout: 60_000,
    env: astroEnvironment,
  };
}

const webServer =
  target === 'seed'
    ? [previewServer(DIST.seed, PORTS.seed)]
    : [previewServer(DIST.fixture, PORTS.fixture), previewServer(DIST.public, PORTS.public)];

export default defineConfig({
  testDir: 'tests/e2e',
  testMatch: '**/*.spec.ts',
  outputDir: `test-results/${target}`,
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: process.env.CI ? 2 : 6,
  reporter: [
    ['list'],
    ['json', { outputFile: `playwright-report/${target}.json` }],
    ['html', { outputFolder: `playwright-report/${target}`, open: 'never' }],
  ],
  grep: target === 'seed' ? /@seed/ : undefined,
  grepInvert: target === 'fixture' ? /@seed-only/ : undefined,
  use: {
    baseURL: `http://127.0.0.1:${PORTS[target]}${BASE_PATH}`,
    locale: 'ko-KR',
    actionTimeout: 15_000,
    navigationTimeout: 30_000,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'desktop',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 900 } },
    },
    {
      name: 'mobile',
      // The public gate is browser independent: it runs once, on desktop.
      testIgnore: /e2e-09/,
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 390, height: 844 },
        isMobile: true,
        hasTouch: true,
        deviceScaleFactor: 2,
      },
    },
  ],
  webServer,
});
