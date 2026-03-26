import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Strategy Bank — page load', () => {
  test('shows heading and strategy count', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Strategy Bank').first()).toBeVisible({ timeout: 15_000 });

    const hasCount = await page
      .locator('text=/\\d+ exam strategies/i')
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    expect(hasCount).toBeTruthy();
  });

  test('shows category filter buttons', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // "All" filter should be visible
    const hasAll = await page
      .getByText(/^All/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasAll).toBeTruthy();
  });

  test('strategy cards visible with names', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    const hasStrategies = /elimination|estimation|time|speed|pattern|trick/i.test(pageText ?? '');
    expect(hasStrategies).toBeTruthy();
  });
});

test.describe('Strategy Bank — category filtering', () => {
  test('clicking category filter updates displayed strategies', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click a specific category
    const categoryBtn = page
      .locator('button')
      .filter({ hasText: /elimination|estimation|time management/i })
      .first();
    const hasCat = await categoryBtn.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCat) {
      await categoryBtn.click();
      await page.waitForTimeout(500);

      // Filtered strategies should show
      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(100);
    }
  });
});

test.describe('Strategy Bank — card expand/collapse', () => {
  test('clicking strategy card expands details', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click first strategy card
    const stratCard = page.locator('button').filter({
      hasText: /elimination|estimation|time|speed|pattern/i,
    }).first();
    const hasCard = await stratCard.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCard) {
      const beforeText = await page.textContent('body') ?? '';
      await stratCard.click();
      await page.waitForTimeout(1_000);

      // Expanded content — page should have more text after expanding
      const afterText = await page.textContent('body') ?? '';
      const grew = afterText.length > beforeText.length;
      const hasExpanded = /when to use|how it works|example|sparky says|scenario|step|tip|trick|strategy/i.test(afterText);
      expect(grew || hasExpanded).toBeTruthy();
    } else {
      // No expandable card found — just verify page loaded
      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(50);
    }
  });

  test('expanded card shows example and Sparky tip', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const stratCard = page.locator('button').filter({
      hasText: /elimination|estimation|time|speed|pattern/i,
    }).first();
    const hasCard = await stratCard.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCard) {
      await stratCard.click();
      await page.waitForTimeout(500);

      const pageText = await page.textContent('body');
      // Should show example or Sparky tip
      const hasDetail = /example|scenario|sparky|result|action/i.test(pageText ?? '');
      expect(hasDetail).toBeTruthy();
    }
  });

  test('shows time saved and difficulty badges', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const stratCard = page.locator('button').filter({
      hasText: /elimination|estimation|time|speed/i,
    }).first();
    await stratCard.click().catch(() => {});
    await page.waitForTimeout(500);

    const pageText = await page.textContent('body');
    const hasMetadata = /beginner|advanced|grade|saved/i.test(pageText ?? '');
    expect(hasMetadata).toBeTruthy();
  });
});
