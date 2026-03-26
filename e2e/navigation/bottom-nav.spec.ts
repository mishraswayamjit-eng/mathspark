import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('BottomNav', () => {
  const NAV_ITEMS = [
    { label: 'Home', href: '/home' },
    { label: 'Practice', href: '/practice' },
    { label: 'Progress', href: '/progress' },
    { label: 'Cards', href: '/flashcards' },
    { label: 'Profile', href: '/profile' },
  ];

  test('shows 5 navigation tabs on /home', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Target the fixed bottom nav bar specifically
    const bottomNav = page.locator('nav[class*="fixed"], div[class*="fixed bottom"]').last();

    for (const item of NAV_ITEMS) {
      await expect(
        bottomNav.getByText(item.label, { exact: true }).first(),
      ).toBeVisible({ timeout: 10_000 });
    }
  });

  test('Home tab is active on /home', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // The BottomNav is a fixed-bottom nav; target the Home link inside it
    const bottomNav = page.locator('nav[class*="fixed"], div[class*="fixed bottom"]').last();
    const homeTab = bottomNav.locator(`a[href="/home"]`).first();
    await expect(homeTab).toBeVisible();

    // The active tab has duo-green text color
    const classes = await homeTab.getAttribute('class');
    expect(classes).toMatch(/duo-green|green/);
  });

  test('Practice tab is active on /practice', async ({ authenticatedPage: page }) => {
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const bottomNav = page.locator('nav[class*="fixed"], div[class*="fixed bottom"]').last();
    const practiceTab = bottomNav.locator(`a[href="/practice"]`).first();
    await expect(practiceTab).toBeVisible();

    const classes = await practiceTab.getAttribute('class');
    expect(classes).toMatch(/duo-green|green/);
  });

  test('navigating between tabs works', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const bottomNav = page.locator('nav[class*="fixed"], div[class*="fixed bottom"]').last();

    // Click Practice tab
    await bottomNav.locator(`a[href="/practice"]`).first().click();
    await page.waitForURL('/practice', { timeout: 10_000 });
    await expect(page.getByText('Practice Hub')).toBeVisible({ timeout: 10_000 });

    // Click Progress tab
    await bottomNav.locator(`a[href="/progress"]`).first().click();
    await page.waitForURL('/progress', { timeout: 10_000 });
    await expect(page.getByText('My Progress')).toBeVisible({ timeout: 10_000 });

    // Click Cards tab
    await bottomNav.locator(`a[href="/flashcards"]`).first().click();
    await page.waitForURL('/flashcards', { timeout: 10_000 });
    await expect(page.getByText("Sparky's Cards")).toBeVisible({ timeout: 10_000 });
  });

  test('BottomNav is hidden on landing page', async ({ page }) => {
    await page.goto('/', { waitUntil: 'domcontentloaded' });

    const bottomNav = page.locator('nav[class*="fixed"], div[class*="fixed bottom"]');
    const homeLink = bottomNav.getByText('Home', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });

  test('BottomNav is hidden on auth pages', async ({ page }) => {
    await page.goto('/auth/login', { waitUntil: 'domcontentloaded' });

    const bottomNav = page.locator('nav[class*="fixed"], div[class*="fixed bottom"]');
    const homeLink = bottomNav.getByText('Home', { exact: true });
    await expect(homeLink).toBeHidden({ timeout: 5_000 });
  });
});
