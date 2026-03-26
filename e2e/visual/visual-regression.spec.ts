import { test, expect } from '../fixtures/auth';
import { test as publicTest, expect as publicExpect } from '@playwright/test';
import { waitForDataLoad } from '../helpers/wait';

// Visual regression tests — Chromium only (cross-browser pixel diffs are noise).
// Run with: npm run test:e2e:visual
// Update snapshots: npm run test:e2e:update-snapshots

// Dynamic content masks — hide dates, streaks, scores that change between runs.
const DYNAMIC_MASKS = (page: import('@playwright/test').Page) => [
  page.locator('text=/\\d+ day streak/i'),
  page.locator('text=/\\d+ XP/i'),
  page.locator('text=/good (morning|afternoon|evening)/i'),
  page.locator('text=/\\d{1,2}:\\d{2}/'), // times
];

// ─── Public pages ───────────────────────────────────────────────────────────

publicTest.describe('Visual — Public pages', () => {
  publicTest.use({ viewport: { width: 430, height: 932 } });

  publicTest('landing page', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle' });
    await publicExpect(page).toHaveScreenshot('landing.png', {
      maxDiffPixelRatio: 0.01,
      mask: [page.locator('text=/\\d+ students/i')],
    });
  });

  publicTest('student login page', async ({ page }) => {
    await page.goto('/student/login', { waitUntil: 'networkidle' });
    await publicExpect(page).toHaveScreenshot('student-login.png', {
      maxDiffPixelRatio: 0.01,
    });
  });

  publicTest('pricing page', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'networkidle' });
    await publicExpect(page).toHaveScreenshot('pricing.png', {
      maxDiffPixelRatio: 0.01,
    });
  });
});

// ─── Authenticated pages ────────────────────────────────────────────────────

test.describe('Visual — Authenticated pages', () => {
  test('home page', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page).toHaveScreenshot('home.png', {
      maxDiffPixelRatio: 0.01,
      mask: DYNAMIC_MASKS(page),
    });
  });

  test('chapters page', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page).toHaveScreenshot('chapters.png', {
      maxDiffPixelRatio: 0.01,
      mask: DYNAMIC_MASKS(page),
    });
  });

  test('practice hub', async ({ authenticatedPage: page }) => {
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page).toHaveScreenshot('practice-hub.png', {
      maxDiffPixelRatio: 0.01,
      mask: DYNAMIC_MASKS(page),
    });
  });

  test('flashcards hub', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page).toHaveScreenshot('flashcards-hub.png', {
      maxDiffPixelRatio: 0.01,
      mask: DYNAMIC_MASKS(page),
    });
  });

  test('progress page', async ({ authenticatedPage: page }) => {
    await page.goto('/progress', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page).toHaveScreenshot('progress.png', {
      maxDiffPixelRatio: 0.01,
      mask: DYNAMIC_MASKS(page),
    });
  });

  test('leaderboard page', async ({ authenticatedPage: page }) => {
    await page.goto('/leaderboard', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page).toHaveScreenshot('leaderboard.png', {
      maxDiffPixelRatio: 0.01,
      mask: DYNAMIC_MASKS(page),
    });
  });

  test('test hub', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page).toHaveScreenshot('test-hub.png', {
      maxDiffPixelRatio: 0.01,
    });
  });
});
