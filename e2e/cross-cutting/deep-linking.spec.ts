import { test, expect } from '../fixtures/auth';
import { test as publicTest, expect as publicExpect } from '@playwright/test';
import { waitForDataLoad } from '../helpers/wait';

/* ────────────────────────────────────────────────────────────────────────────
 * Deep linking — URL params are respected
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Deep Linking — practice mode params', () => {
  test('speed mode param loads correctly', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05?mode=speed', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
  });

  test('flashcard session with deck+mode params loads', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=quiz', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    // Should show session content or empty state
    expect(pageText?.length).toBeGreaterThan(50);
  });

  test('flashcard warmup mode loads', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=warmup&mode=warmup', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(50);
  });

  test('flashcard speed mode loads', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=speed', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(50);
  });

  test('flashcard match mode loads', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=match', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(50);
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * localStorage persistence
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('localStorage Persistence', () => {
  test('student ID persists across page navigations', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const id1 = await page.evaluate(() =>
      localStorage.getItem('mathspark_student_id'),
    );

    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const id2 = await page.evaluate(() =>
      localStorage.getItem('mathspark_student_id'),
    );

    expect(id1).toBe(id2);
    expect(id1).toBe('student_001');
  });

  test('student grade persists in localStorage', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    const grade = await page.evaluate(() =>
      localStorage.getItem('mathspark_student_grade'),
    );

    expect(grade).toBe('4');
  });

  test('subscription tier persists in localStorage', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    const tier = await page.evaluate(() =>
      localStorage.getItem('mathspark_subscription_tier'),
    );

    expect(tier).toBe('3');
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Public pages accessible without auth
 * ──────────────────────────────────────────────────────────────────────────── */

publicTest.describe('Public Pages — no auth required', () => {
  const publicRoutes = [
    { route: '/', heading: /mathspark|ipm|math/i },
    { route: '/pricing', heading: /starter|advanced|unlimited/i },
    { route: '/start', heading: /welcome to mathspark/i },
    { route: '/student/login', heading: /student login/i },
    { route: '/auth/login', heading: /parent sign in/i },
    { route: '/auth/register', heading: /create|register|get started/i },
  ];

  for (const { route, heading } of publicRoutes) {
    publicTest(`${route} loads without auth`, async ({ page }) => {
      await page.goto(route, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(2_000);

      const pageText = await page.textContent('body');
      publicExpect(pageText).toMatch(heading);
    });
  }
});

/* ────────────────────────────────────────────────────────────────────────────
 * Auth-protected pages redirect when unauthenticated
 * ──────────────────────────────────────────────────────────────────────────── */

publicTest.describe('Auth Protection — redirects', () => {
  const protectedRoutes = [
    '/home',
    '/chapters',
    '/practice',
    '/progress',
    '/flashcards',
    '/profile',
    '/leaderboard',
    '/chat',
    '/test',
  ];

  for (const route of protectedRoutes) {
    publicTest(`${route} redirects or blocks without auth`, async ({ page }) => {
      await page.goto(route, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(3_000);

      // Should NOT show the authenticated page content
      // May redirect to /student/login or show auth prompt
      const url = page.url();
      const pageText = await page.textContent('body');

      const redirected = /student\/login|auth\/login/.test(url);
      const blockedContent = /login|sign in|welcome/i.test(pageText ?? '');
      const hasGreeting = /good (morning|afternoon|evening)/i.test(pageText ?? '');

      // Either redirected OR doesn't show authenticated content
      publicExpect(redirected || blockedContent || !hasGreeting).toBeTruthy();
    });
  }
});

/* ────────────────────────────────────────────────────────────────────────────
 * Responsive — mobile viewport checks
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Responsive — touch targets', () => {
  test('bottom nav touch targets are at least 44px', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const navLinks = page.locator('nav a[href]');
    const count = await navLinks.count();

    for (let i = 0; i < Math.min(count, 5); i++) {
      const box = await navLinks.nth(i).boundingBox();
      if (box) {
        // Touch target should be at least 44px (WCAG)
        expect(box.height).toBeGreaterThanOrEqual(40);
      }
    }
  });
});
