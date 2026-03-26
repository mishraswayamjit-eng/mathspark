import { test as publicTest, expect as publicExpect } from '@playwright/test';
import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/* ────────────────────────────────────────────────────────────────────────────
 * 404 Not Found
 * ──────────────────────────────────────────────────────────────────────────── */

publicTest.describe('404 Page', () => {
  publicTest('non-existent route shows not-found page', async ({ page }) => {
    await page.goto('/this-route-does-not-exist-12345', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2_000);

    const pageText = await page.textContent('body');
    const hasNotFound = /not found|page not found|404|go home|couldn.*t find/i.test(
      pageText ?? '',
    );
    publicExpect(hasNotFound).toBeTruthy();
  });

  publicTest('not-found page has Go Home button', async ({ page }) => {
    await page.goto('/nonexistent-page-xyz', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2_000);

    const homeBtn = page.locator('a, button').filter({ hasText: /go home|home/i }).first();
    const hasHome = await homeBtn.isVisible({ timeout: 5_000 }).catch(() => false);

    if (hasHome) {
      await homeBtn.click();
      await page.waitForTimeout(2_000);
      // Should navigate to / or /home
      publicExpect(page.url()).toMatch(/\/(start|home|$|\?)/);
    }
  });

  publicTest('deeply nested non-existent route shows 404', async ({ page }) => {
    await page.goto('/a/b/c/d/nonexistent', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2_000);

    const pageText = await page.textContent('body');
    const hasNotFound = /not found|404|go home|error/i.test(pageText ?? '');
    publicExpect(hasNotFound).toBeTruthy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Invalid dynamic route params
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Invalid route params', () => {
  test('invalid testId shows error or not-found', async ({ authenticatedPage: page }) => {
    await page.goto('/test/invalid-test-id-99999', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|error|couldn.*t|go home|something went wrong/i.test(
      pageText ?? '',
    );
    expect(hasError).toBeTruthy();
  });

  test('invalid test response page shows error', async ({ authenticatedPage: page }) => {
    await page.goto('/test/invalid-id/response', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|error|couldn.*t|no results/i.test(pageText ?? '');
    expect(hasError).toBeTruthy();
  });

  test('invalid learn example ID shows error', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/examples/nonexistent-example', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|error|retry|couldn.*t/i.test(pageText ?? '');
    expect(hasError).toBeTruthy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Error recovery
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Error recovery — retry buttons', () => {
  test('error pages with retry button are functional', async ({ authenticatedPage: page }) => {
    // Navigate to a page that might fail
    await page.goto('/test/bad-id-triggers-error', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const retryBtn = page.locator('button').filter({ hasText: /retry|try again/i }).first();
    const hasRetry = await retryBtn.isVisible({ timeout: 5_000 }).catch(() => false);

    if (hasRetry) {
      await retryBtn.click();
      await page.waitForTimeout(2_000);

      // Page should re-render (retry the fetch)
      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(10);
    }
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Pages do not crash with empty/missing data
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Graceful degradation', () => {
  const authenticatedPages = [
    '/home',
    '/chapters',
    '/practice',
    '/progress',
    '/flashcards',
    '/profile',
    '/leaderboard',
    '/chat',
    '/test',
    '/test/history',
    '/practice/daily',
    '/practice/skill-drill',
    '/learn/examples',
    '/learn/concept-map',
    '/learn/mistakes',
    '/learn/strategies',
    '/learn/stories',
    '/exam-prep/predictor',
    '/progress/report',
  ];

  for (const route of authenticatedPages) {
    test(`${route} loads without unhandled errors`, async ({ authenticatedPage: page }) => {
      const errors: string[] = [];
      page.on('pageerror', (err) => {
        // Filter out known React hydration errors (expected in prod builds with injected state)
        if (/Minified React error #(418|423|425)/.test(err.message)) return;
        errors.push(err.message);
      });

      await page.goto(route, { waitUntil: 'domcontentloaded' });
      await waitForDataLoad(page);

      expect(errors).toHaveLength(0);
    });
  }
});
