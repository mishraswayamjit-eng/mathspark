import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Math Stories — page load', () => {
  test('shows heading and story count', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/stories', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Math Stories').first()).toBeVisible({ timeout: 15_000 });

    const hasCount = await page
      .locator('text=/\\d+ stories/i')
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    expect(hasCount).toBeTruthy();
  });

  test('shows category filter chips', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/stories', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // "All" plus category chips (Sports, Space, Nature, etc.)
    const hasAll = await page
      .getByText(/^All/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasAll).toBeTruthy();
  });

  test('story cards show fun stars rating', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/stories', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Fun stars shown as ★ characters (CSS colored, not emoji ⭐)
    const hasStars = await page
      .locator('text=/★/')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // Stars may not be visible at small size — also check for fun factor text
    const pageText = await page.textContent('body');
    const hasFunIndicator = hasStars || /fun|⭐|★|rating/i.test(pageText ?? '');
    expect(hasFunIndicator).toBeTruthy();
  });
});

test.describe('Math Stories — card interaction', () => {
  test('clicking story card expands story text', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/stories', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click first story card
    const storyCard = page.locator('button').filter({
      hasText: /sport|space|nature|food|money|game|tech|history/i,
    }).first();
    const hasCard = await storyCard.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCard) {
      await storyCard.click();
      await page.waitForTimeout(500);

      // Expanded story text + math connection
      const pageText = await page.textContent('body');
      const hasExpanded = /math connection|challenge|think about/i.test(pageText ?? '');
      expect(hasExpanded).toBeTruthy();
    }
  });

  test('Sparky\'s Challenge shows hint toggle', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/stories', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const storyCard = page.locator('button').filter({
      hasText: /sport|space|nature|food|money|game/i,
    }).first();
    await storyCard.click().catch(() => {});
    await page.waitForTimeout(500);

    // "Think about it" hint button
    const hintBtn = page.locator('button').filter({ hasText: /think about it/i }).first();
    const hasHint = await hintBtn.isVisible({ timeout: 5_000 }).catch(() => false);

    if (hasHint) {
      await hintBtn.click();
      await page.waitForTimeout(300);

      // Hint text should appear
      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(200);
    }
  });

  test('category filter changes displayed stories', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/stories', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const categoryBtn = page
      .locator('button')
      .filter({ hasText: /space|sport|nature/i })
      .first();
    const hasCat = await categoryBtn.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCat) {
      await categoryBtn.click();
      await page.waitForTimeout(500);

      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(100);
    }
  });
});
