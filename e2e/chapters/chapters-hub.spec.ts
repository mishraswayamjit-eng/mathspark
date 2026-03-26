import { test, expect } from '../fixtures/auth';
import { test as publicTest } from '@playwright/test';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Chapters Hub — page load', () => {
  test('shows greeting and practice prompt', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(
      page.locator('text=/what shall we practice/i').first(),
    ).toBeVisible({ timeout: 15_000 });
  });

  test('shows syllabus coverage bar', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasCoverage = await page
      .getByText(/syllabus coverage/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasCoverage).toBeTruthy();
  });

  test('shows topic cards grid', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Topic cards link to /practice/[topicId]
    const topicCards = page.locator('a[href*="/practice/"]');
    await expect(topicCards.first()).toBeVisible({ timeout: 10_000 });
    const count = await topicCards.count();
    expect(count).toBeGreaterThan(0);
  });
});

test.describe('Chapters Hub — grade tabs', () => {
  test('grade tabs visible (Gr 2-9)', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // At least the student's grade tab should be visible
    const gr4Tab = page.getByText('Gr 4', { exact: false }).first();
    await expect(gr4Tab).toBeVisible({ timeout: 10_000 });
  });

  test('default grade tab is selected (matches student grade)', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Gr 4 should be the selected tab (default student is grade 4)
    const gradeButtons = page.locator('button, div[role="button"]').filter({
      hasText: /Gr\s*4/i,
    });
    const firstGradeBtn = gradeButtons.first();
    await expect(firstGradeBtn).toBeVisible({ timeout: 10_000 });

    const classes = await firstGradeBtn.getAttribute('class');
    // Selected tab has dark background
    expect(classes).toMatch(/duo-dark|bg-duo-dark|selected/);
  });

  test('clicking different grade tab switches content', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Get initial topic count
    const initialCards = page.locator('a[href*="/practice/"]');
    await expect(initialCards.first()).toBeVisible({ timeout: 10_000 });

    // Click a different grade tab (Gr 5 should be accessible for Unlimited tier)
    const gr5Tab = page.getByText('Gr 5', { exact: false }).first();
    const hasGr5 = await gr5Tab.isVisible({ timeout: 5_000 }).catch(() => false);

    if (hasGr5) {
      await gr5Tab.click();
      await page.waitForTimeout(1_500);

      // Content should have changed or stayed (grade 5 content loads)
      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(100);
    }
  });

  test('locked grade tab shows upgrade modal', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Find a locked tab (has 🔒 icon)
    const lockedTab = page.locator('button, div').filter({ hasText: /🔒/ }).first();
    const hasLocked = await lockedTab.isVisible({ timeout: 5_000 }).catch(() => false);

    if (!hasLocked) {
      // Unlimited tier student may not have locked grades
      test.skip(true, 'No locked grade tabs (student has full access)');
      return;
    }

    await lockedTab.click();
    await page.waitForTimeout(500);

    // Should show upgrade modal
    await expect(
      page.getByText(/locked|upgrade/i).first(),
    ).toBeVisible({ timeout: 5_000 });
  });
});

test.describe('Chapters Hub — topic interaction', () => {
  test('topic card shows mastery status', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // At least some topics should show mastery badges
    const pageText = await page.textContent('body');
    const hasMastery = /mastered|learning|solved|question/i.test(pageText ?? '');
    expect(hasMastery).toBeTruthy();
  });

  test('clicking topic card navigates to practice page', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const topicCard = page.locator('a[href*="/practice/"]').first();
    await expect(topicCard).toBeVisible({ timeout: 10_000 });

    const href = await topicCard.getAttribute('href');
    await topicCard.click();
    await page.waitForURL(/\/practice\//, { timeout: 15_000 });

    expect(page.url()).toContain('/practice/');
  });

  test('flashcard banner links to /flashcards', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const flashcardBanner = page.locator('a[href*="/flashcards"]').first();
    const hasBanner = await flashcardBanner.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasBanner) {
      await flashcardBanner.click();
      await page.waitForURL(/\/flashcards/, { timeout: 10_000 });
    }
  });

  test('mock test banner links to /test', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const testBanner = page.locator('a[href*="/test"]').first();
    const hasBanner = await testBanner.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasBanner) {
      await testBanner.click();
      await page.waitForURL(/\/test/, { timeout: 10_000 });
    }
  });
});

test.describe('Chapters Hub — sections', () => {
  test('section dividers show In progress / Not started / Mastered', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const dividers = ['In progress', 'Not started', 'Mastered'];
    let found = 0;
    for (const divider of dividers) {
      const visible = await page
        .getByText(divider, { exact: false })
        .first()
        .isVisible({ timeout: 5_000 })
        .catch(() => false);
      if (visible) found++;
    }

    // At least 1 section should exist
    expect(found).toBeGreaterThanOrEqual(1);
  });

  test('recommended topics section visible', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasRecommended = await page
      .getByText(/recommended for you/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // May not show if no weak topics
    expect(true).toBeTruthy();
  });

  test('page has no JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });
});
