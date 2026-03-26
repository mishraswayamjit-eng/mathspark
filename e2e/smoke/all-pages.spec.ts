import { test, expect } from '../fixtures/auth';
import { test as publicTest, expect as publicExpect } from '@playwright/test';
import { waitForDataLoad } from '../helpers/wait';

// ─── Helper: collect JS errors during navigation ────────────────────────────

async function expectNoJSErrors(
  page: import('@playwright/test').Page,
  path: string,
  expectedText: string | RegExp,
) {
  const errors: string[] = [];
  page.on('pageerror', (err) => errors.push(err.message));

  await page.goto(path, { waitUntil: 'domcontentloaded' });
  await waitForDataLoad(page);

  await expect(page.getByText(expectedText, { exact: false }).first()).toBeVisible({
    timeout: 15_000,
  });
  expect(errors, `JS errors on ${path}`).toHaveLength(0);
}

// ─── Public pages (no auth) ─────────────────────────────────────────────────

publicTest.describe('Public pages', () => {
  publicTest('/ — landing page', async ({ page }) => {
    await expectNoJSErrors(page, '/', '15 minutes a day');
  });

  publicTest('/auth/login', async ({ page }) => {
    await expectNoJSErrors(page, '/auth/login', 'Parent sign in');
  });

  publicTest('/auth/register', async ({ page }) => {
    await expectNoJSErrors(page, '/auth/register', 'Create your account');
  });

  publicTest('/auth/forgot-password', async ({ page }) => {
    await expectNoJSErrors(page, '/auth/forgot-password', /forgot|reset|password/i);
  });

  publicTest('/pricing', async ({ page }) => {
    await expectNoJSErrors(page, '/pricing', /IPM prep/i);
  });

  publicTest('/student/login', async ({ page }) => {
    await expectNoJSErrors(page, '/student/login', 'Student login');
  });

  publicTest('/start — onboarding', async ({ page }) => {
    await expectNoJSErrors(page, '/start', 'Welcome to MathSpark');
  });
});

// ─── Authenticated pages ────────────────────────────────────────────────────

test.describe('Authenticated pages', () => {
  test('/home', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/home', /good (morning|afternoon|evening)/i);
  });

  test('/chapters', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/chapters', /what shall we practice/i);
  });

  test('/practice', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/practice', 'Practice Hub');
  });

  test('/practice/daily', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/practice/daily', 'Daily Challenge');
  });

  test('/practice/skill-drill', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/practice/skill-drill', 'Skill Drills');
  });

  test('/practice/papers', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/practice/papers', 'Exam Papers');
  });

  test('/progress', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/progress', 'My Progress');
  });

  test('/progress/report', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/progress/report', /report/i);
  });

  test('/flashcards', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/flashcards', "Sparky's Cards");
  });

  test('/profile', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/profile', /aarav/i);
  });

  test('/leaderboard', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/leaderboard', 'League');
  });

  test('/test — mock test hub', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/test', 'IPM Mock Test');
  });

  test('/test/history', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/test/history', 'Test History');
  });

  test('/chat', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/chat', 'Sparky');
  });

  test('/learn/concept-map', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/learn/concept-map', 'Concept Map');
  });

  test('/learn/examples', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/learn/examples', 'Sparky Explains');
  });

  test('/learn/stories', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/learn/stories', 'Math Stories');
  });

  test('/learn/mistakes', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/learn/mistakes', 'Mistake Patterns');
  });

  test('/learn/strategies', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/learn/strategies', 'Strategy Bank');
  });

  test('/exam-prep/predictor', async ({ authenticatedPage: page }) => {
    await expectNoJSErrors(page, '/exam-prep/predictor', 'IPM Exam Predictor');
  });
});

// ─── 404 page ───────────────────────────────────────────────────────────────

publicTest('/nonexistent — 404 page', async ({ page }) => {
  await page.goto('/this-page-does-not-exist', { waitUntil: 'domcontentloaded' });
  await publicExpect(page.getByText('Page not found', { exact: false }).first()).toBeVisible();
});
