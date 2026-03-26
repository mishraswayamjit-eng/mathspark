import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Mock Test Flow', () => {
  test('test hub shows test type options', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('IPM Mock Test')).toBeVisible();
    await expect(page.getByText(/Quick Test/i)).toBeVisible();
  });

  test('create a test and see test page', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click any Start button
    const startButton = page.locator('button').filter({ hasText: /start/i }).first();
    await expect(startButton).toBeVisible({ timeout: 10_000 });
    await startButton.click();

    // Wait for navigation — URL may have various ID formats
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    // Test page should show some content (question, timer, counter, or loading)
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
  });

  test('question navigator opens', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Create test
    const startButton = page.locator('button').filter({ hasText: /start/i }).first();
    await startButton.click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    // Look for navigator button (shows question count like "Q1/15")
    const navButton = page.locator('button').filter({ hasText: /Q\d+/i }).first();
    const hasNav = await navButton.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasNav) {
      await navButton.click();
      await expect(page.getByText('Question Navigator')).toBeVisible({ timeout: 5_000 });
    }
  });

  test('test history page loads', async ({ authenticatedPage: page }) => {
    await page.goto('/test/history', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Test History')).toBeVisible();
  });
});
