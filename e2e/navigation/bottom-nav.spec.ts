import { test, expect } from '../fixtures/auth';
import { test as publicTest, expect as publicExpect } from '@playwright/test';
import { waitForDataLoad, carryOnIfOpen } from '../helpers/wait';

const NAV_ITEMS = [
  { label: 'Today', href: '/home', heading: /good (morning|afternoon|evening)/i },
  { label: 'Learn', href: '/learn', heading: /pick something new to learn/i },
  { label: 'Practise', href: '/practice', heading: /pick how you want to practise/i },
  { label: 'Progress', href: '/progress', heading: /my progress/i },
] as const;

// Routes that have no tab of their own, and the tab that lights up for them.
const TAB_FOR_ROUTE = [
  { route: '/learn/lessons', tab: '/learn' },
  { route: '/learn/stories', tab: '/learn' },
  { route: '/learn/concept-map', tab: '/learn' },
  { route: '/chapters', tab: '/practice' },
  { route: '/flashcards', tab: '/practice' },
  { route: '/practice/skill-drill', tab: '/practice' },
  { route: '/practice/tests', tab: '/practice' },
  { route: '/practice/exam-tips', tab: '/practice' },
  { route: '/test', tab: '/practice' },
  { route: '/exam-prep/predictor', tab: '/practice' },
  { route: '/learn/strategies', tab: '/practice' },
  { route: '/leaderboard', tab: '/progress' },
  { route: '/profile', tab: '/progress' },
] as const;

/** Locate the fixed bottom nav bar. */
function bottomNav(page: import('@playwright/test').Page) {
  return page.locator('nav[class*="fixed"], div[class*="fixed bottom"]').last();
}

test.describe('BottomNav — visibility', () => {
  test('shows 4 navigation tabs on /home', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const nav = bottomNav(page);
    for (const item of NAV_ITEMS) {
      await expect(
        nav.getByText(item.label, { exact: true }).first(),
      ).toBeVisible({ timeout: 10_000 });
    }

    // Exactly four tabs, and none of the retired ones
    const tabs = page.locator('nav[aria-label="Main"] a[href]');
    await expect(tabs).toHaveCount(NAV_ITEMS.length);
    for (const retired of ['/chat', '/flashcards', '/profile']) {
      await expect(page.locator(`nav[aria-label="Main"] a[href="${retired}"]`)).toHaveCount(0);
    }
  });

  test('BottomNav is hidden on landing page', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Today', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('BottomNav is hidden on auth pages', async ({ page }) => {
    await page.goto('/auth/login', { waitUntil: 'domcontentloaded' });

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Today', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('BottomNav is hidden on /start onboarding', async ({ page }) => {
    await page.goto('/start', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1_000);

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Today', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('BottomNav is shown on the new index pages', async ({ authenticatedPage: page }) => {
    for (const route of ['/learn', '/practice/tests', '/practice/exam-tips']) {
      await page.goto(route, { waitUntil: 'domcontentloaded' });
      await waitForDataLoad(page);

      await expect(
        page.locator('nav[aria-label="Main"]').getByText('Today', { exact: true }),
      ).toBeVisible({ timeout: 10_000 });
    }
  });
});

test.describe('BottomNav — tab navigation', () => {
  for (const item of NAV_ITEMS) {
    test(`clicking "${item.label}" tab navigates to ${item.href}`, async ({
      authenticatedPage: page,
    }) => {
      // Start from /home
      await page.goto('/home', { waitUntil: 'domcontentloaded' });
      await waitForDataLoad(page);

      if (item.href === '/home') {
        // Already on /home — just verify heading
        await expect(
          page.getByText(item.heading).first(),
        ).toBeVisible({ timeout: 15_000 });
        return;
      }

      const nav = bottomNav(page);
      await nav.locator(`a[href="${item.href}"]`).first().click();
      await page.waitForURL(item.href, { timeout: 10_000 });
      await waitForDataLoad(page);

      await expect(
        page.getByText(item.heading).first(),
      ).toBeVisible({ timeout: 15_000 });
    });
  }
});

test.describe('BottomNav — active state', () => {
  for (const item of NAV_ITEMS) {
    test(`active state is correct on ${item.href}`, async ({ authenticatedPage: page }) => {
      await page.goto(item.href, { waitUntil: 'domcontentloaded' });
      await waitForDataLoad(page);

      const nav = bottomNav(page);
      const tab = nav.locator(`a[href="${item.href}"]`).first();
      await expect(tab).toBeVisible({ timeout: 10_000 });

      // The active tab is marked as the current page
      await expect(tab).toHaveAttribute('aria-current', 'page');
    });
  }

  for (const { route, tab: tabHref } of TAB_FOR_ROUTE) {
    test(`${route} lights up the ${tabHref} tab`, async ({ authenticatedPage: page }) => {
      await page.goto(route, { waitUntil: 'domcontentloaded' });
      await waitForDataLoad(page);

      const tabs = page.locator('nav[aria-label="Main"] a[href]');
      await expect(tabs.first()).toBeVisible({ timeout: 10_000 });

      // Exactly one tab is current, and it is the expected one
      await expect(page.locator('nav[aria-label="Main"] a[aria-current="page"]')).toHaveCount(1);
      await expect(
        page.locator(`nav[aria-label="Main"] a[href="${tabHref}"]`),
      ).toHaveAttribute('aria-current', 'page');
    });
  }
});

test.describe('BottomNav — hidden during immersive flows', () => {
  test('hidden during active test', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const startButton = page.locator('button').filter({ hasText: /start/i }).first();
    const hasStart = await startButton.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasStart) {
      test.skip(true, 'No start button on test hub');
      return;
    }

    await startButton.click();
    await carryOnIfOpen(page);
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Today', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('hidden during flashcard session', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=classic', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Today', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });
});
