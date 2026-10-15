import { expect, test } from '@playwright/test';
import { spawn, type ChildProcess } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

let serverProcess: ChildProcess;
let root = '';
let url = '';

function cleanEnvironment() {
  return Object.fromEntries(
    Object.entries(process.env).filter(
      ([key]) => key !== 'CLAUDECODE' && key !== 'AI_AGENT' && !key.startsWith('CODEX_'),
    ),
  );
}

test.beforeAll(async () => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), 'aixon-review-e2e-'));
  const graph = path.join(root, 'graph.yaml');
  const wiki = path.join(root, 'wiki');
  const review = path.join(root, 'review');
  fs.copyFileSync(path.join(process.cwd(), 'tools/fixtures/mini_graph.yaml'), graph);
  fs.mkdirSync(wiki);
  fs.mkdirSync(review);
  serverProcess = spawn(
    'python3',
    [
      'tools/review_server.py',
      '--graph',
      graph,
      '--wiki-dir',
      wiki,
      '--review-dir',
      review,
      '--port',
      '0',
      '--by',
      'human:default',
    ],
    { cwd: process.cwd(), env: cleanEnvironment(), stdio: ['ignore', 'pipe', 'pipe'] },
  );
  url = await new Promise<string>((resolve, reject) => {
    let output = '';
    const timer = setTimeout(
      () => reject(new Error(`review server did not start: ${output}`)),
      10_000,
    );
    serverProcess.stdout?.on('data', (chunk) => {
      output += String(chunk);
      const match = output.match(/http:\/\/127\.0\.0\.1:\d+\/\?token=\S+/);
      if (match) {
        clearTimeout(timer);
        resolve(match[0]);
      }
    });
    serverProcess.once('exit', (code) => {
      clearTimeout(timer);
      reject(new Error(`review server exited ${code}: ${output}`));
    });
  });
});

test.afterAll(() => {
  serverProcess?.kill();
  if (root) fs.rmSync(root, { recursive: true, force: true });
});

test('local review app records a human approval', async ({ page }) => {
  await page.goto(url);
  await page.getByLabel('찾기').fill('concept:algebra');
  await page.getByRole('button', { name: /Algebra/ }).click();
  await page.keyboard.press('a');
  await page.getByLabel('검토자').fill('human:e2e-tester');
  await page.getByRole('button', { name: '결정 기록' }).click();
  await expect(page.locator('#message')).toContainText('기록 완료');
  await expect(page.locator('#queue')).toContainText('approved');
});
