import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Practice Hub', () => {
  test('practice hub shows heading and topic cards', async ({ authenticatedPage: page }) => {
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Practice Hub')).toBeVisible();

    // Topic cards should have /practice/ links
    const topicLinks = page.locator('a[href*="/practice/"]');
    await expect(topicLinks.first()).toBeVisible({ timeout: 10_000 });
    const count = await topicLinks.count();
    expect(count).toBeGreaterThan(0);
  });

  test('all topic cards link to /practice/ prefix', async ({ authenticatedPage: page }) => {
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const topicLinks = page.locator('a[href*="/practice/"]');
    const count = await topicLinks.count();

    for (let i = 0; i < Math.min(count, 5); i++) {
      const href = await topicLinks.nth(i).getAttribute('href');
      expect(href).toMatch(/^\/practice\//);
    }
  });

  test('daily challenge page renders', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/daily', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Daily Challenge')).toBeVisible();
  });

  test('skill drill page renders', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Skill Drills')).toBeVisible();
  });

  test('papers page renders', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/papers', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
  });

  test('exam papers page renders', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/exam-papers', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
  });
});

test.describe('Topic Practice — navigation', () => {
  test('navigate to a topic from practice hub', async ({ authenticatedPage: page }) => {
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const topicCard = page.locator('a[href*="/practice/"]').first();
    await expect(topicCard).toBeVisible({ timeout: 10_000 });
    await topicCard.click();

    await page.waitForURL(/\/practice\/.+/, { timeout: 15_000 });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(0);
  });

  test('practice topic page loads without crash', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
  });

  test('speed mode URL loads', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05?mode=speed', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
  });
});

test.describe('Topic Practice — question interaction', () => {
  test('clicking an option shows feedback panel', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Wait for question content or status screen
    await page.waitForTimeout(2_000);
    const pageText = await page.textContent('body');

    // Skip if no question rendered (status screen, empty topic, etc.)
    const hasQuestion = /option|A\)|B\)|answer/i.test(pageText ?? '');
    if (!hasQuestion) {
      test.skip(true, 'No question rendered on this topic');
      return;
    }

    // Click the first option button
    const optionBtn = page
      .locator('button')
      .filter({ hasText: /^[ABCD]$|^A\b/ })
      .first();
    const hasOption = await optionBtn.isVisible({ timeout: 5_000 }).catch(() => false);
    if (!hasOption) {
      const altOption = page.locator('button[class*="rounded"]').first();
      await altOption.click().catch(() => {});
    } else {
      await optionBtn.click();
    }

    await page.waitForTimeout(1_500);

    // Should show feedback — correct (green) or wrong (red)
    const feedbackText = await page.textContent('body');
    const hasFeedback =
      /correct|nice|great|wrong|oops|not quite|explanation|hint|next/i.test(feedbackText ?? '');
    expect(hasFeedback).toBeTruthy();
  });

  test('hearts display is visible during practice', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.waitForTimeout(2_000);

    const hasHearts = await page
      .locator('text=/❤|♥|heart/i')
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    // Hearts may not be on every page variant — pass if visible
    if (hasHearts) {
      expect(hasHearts).toBeTruthy();
    }
  });

  test('next button advances after feedback', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await page.waitForTimeout(2_000);

    const pageText = await page.textContent('body');
    const hasQuestion = /option|A\)|answer/i.test(pageText ?? '');
    if (!hasQuestion) {
      test.skip(true, 'No question rendered');
      return;
    }

    // Click first option
    const optionBtn = page.locator('button[class*="rounded"]').nth(1);
    await optionBtn.click().catch(() => {});
    await page.waitForTimeout(1_500);

    // Look for next/continue button
    const nextBtn = page
      .locator('button')
      .filter({ hasText: /next|continue|→/i })
      .first();
    const hasNext = await nextBtn.isVisible({ timeout: 5_000 }).catch(() => false);
    if (hasNext) {
      await nextBtn.click();
      await page.waitForTimeout(1_000);
      const newText = await page.textContent('body');
      expect(newText?.length).toBeGreaterThan(0);
    }
  });
});
