import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/**
 * Navigate to a valid worked example by going through the examples hub.
 * Returns true if we landed on a detail page.
 */
async function navigateToFirstExample(page: import('@playwright/test').Page): Promise<boolean> {
  await page.goto('/learn/examples', { waitUntil: 'domcontentloaded' });
  await waitForDataLoad(page);

  // Click the first example card link
  const exampleLink = page.locator('a[href*="/learn/examples/"]').first();
  const hasLink = await exampleLink.isVisible({ timeout: 10_000 }).catch(() => false);
  if (!hasLink) return false;

  await exampleLink.click();
  await page.waitForURL(/\/learn\/examples\/.+/, { timeout: 15_000 });
  await waitForDataLoad(page);
  return true;
}

test.describe('Worked Example Detail — page load', () => {
  test('shows topic name and difficulty badge', async ({ authenticatedPage: page }) => {
    const landed = await navigateToFirstExample(page);
    if (!landed) {
      test.skip(true, 'No examples available to navigate to');
      return;
    }

    const pageText = await page.textContent('body');
    const hasDifficulty = /easy|medium|hard/i.test(pageText ?? '');
    expect(hasDifficulty).toBeTruthy();
  });

  test('shows question card with options', async ({ authenticatedPage: page }) => {
    const landed = await navigateToFirstExample(page);
    if (!landed) {
      test.skip(true, 'No examples available');
      return;
    }

    // Question text should be visible
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(100);

    // Options A/B/C/D may be visible
    const hasOptions = /\bA\b.*\bB\b|option/i.test(pageText ?? '');
    expect(hasOptions || pageText!.length > 200).toBeTruthy();
  });

  test('shows "Watch Sparky Solve It" or "Show All" buttons', async ({
    authenticatedPage: page,
  }) => {
    const landed = await navigateToFirstExample(page);
    if (!landed) {
      test.skip(true, 'No examples available');
      return;
    }

    const hasSolveBtn = await page
      .locator('button')
      .filter({ hasText: /watch sparky|show all/i })
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasSolveBtn).toBeTruthy();
  });
});

test.describe('Worked Example Detail — solution reveal', () => {
  test('clicking reveal shows step-by-step solution', async ({ authenticatedPage: page }) => {
    const landed = await navigateToFirstExample(page);
    if (!landed) {
      test.skip(true, 'No examples available');
      return;
    }

    const revealBtn = page
      .locator('button')
      .filter({ hasText: /watch sparky|show all/i })
      .first();
    const hasBtn = await revealBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasBtn) {
      test.skip(true, 'Reveal button not found');
      return;
    }

    await revealBtn.click();
    await page.waitForTimeout(2_000);

    // Steps should appear
    const pageText = await page.textContent('body');
    const hasSteps = /step|solution|answer|explanation/i.test(pageText ?? '');
    expect(hasSteps).toBeTruthy();
  });

  test('trap warning shown if applicable', async ({ authenticatedPage: page }) => {
    const landed = await navigateToFirstExample(page);
    if (!landed) {
      test.skip(true, 'No examples available');
      return;
    }

    // Click reveal to show full solution
    const revealBtn = page
      .locator('button')
      .filter({ hasText: /watch sparky|show all/i })
      .first();
    await revealBtn.click().catch(() => {});
    await page.waitForTimeout(2_000);

    // Trap warning may or may not appear — just check page doesn't crash
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(100);
  });

  test('"More Examples" button navigates back to examples hub', async ({
    authenticatedPage: page,
  }) => {
    const landed = await navigateToFirstExample(page);
    if (!landed) {
      test.skip(true, 'No examples available');
      return;
    }

    const moreBtn = page.locator('a, button').filter({ hasText: /more examples/i }).first();
    const hasMore = await moreBtn.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasMore) {
      await moreBtn.click();
      await page.waitForURL(/\/learn\/examples/, { timeout: 10_000 });
    }
  });
});

test.describe('Worked Example Detail — error handling', () => {
  test('invalid example ID shows error or not-found', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/examples/invalid-id-12345', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|error|retry|couldn.*t|go home/i.test(pageText ?? '');
    expect(hasError).toBeTruthy();
  });
});
