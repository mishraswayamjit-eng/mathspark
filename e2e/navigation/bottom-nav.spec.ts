import { test, expect } from '../fixtures/auth';
import { test as publicTest, expect as publicExpect } from '@playwright/test';
import { waitForDataLoad } from '../helpers/wait';

const NAV_ITEMS = [
  { label: 'Home', href: '/home', heading: /good (morning|afternoon|evening)/i },
  { label: 'Practice', href: '/practice', heading: /practice hub/i },
  { label: 'Progress', href: '/progress', heading: /my progress/i },
  { label: 'Cards', href: '/flashcards', heading: /sparky.*cards/i },
  { label: 'Profile', href: '/profile', heading: /aarav/i },
] as const;

/** Locate the fixed bottom nav bar. */
function bottomNav(page: import('@playwright/test').Page) {
  return page.locator('nav[class*="fixed"], div[class*="fixed bottom"]').last();
}

test.describe('BottomNav — visibility', () => {
  test('shows 5 navigation tabs on /home', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const nav = bottomNav(page);
    for (const item of NAV_ITEMS) {
      await expect(
        nav.getByText(item.label, { exact: true }).first(),
      ).toBeVisible({ timeout: 10_000 });
    }
  });

  test('BottomNav is hidden on landing page', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Home', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('BottomNav is hidden on auth pages', async ({ page }) => {
    await page.goto('/auth/login', { waitUntil: 'domcontentloaded' });

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Home', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('BottomNav is hidden on /start onboarding', async ({ page }) => {
    await page.goto('/start', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1_000);

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Home', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
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

      // Active tab should have duo-green or green in its classes
      const classes = await tab.getAttribute('class');
      expect(classes).toMatch(/duo-green|green/);
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
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Home', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('hidden during flashcard session', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=classic', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    const nav = bottomNav(page);
    const homeLink = nav.getByText('Home', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });
});
