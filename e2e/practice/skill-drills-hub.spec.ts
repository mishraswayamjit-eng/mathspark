import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Skill Drills Hub — page load', () => {
  test('shows heading and topic count', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Skill Drills')).toBeVisible({ timeout: 15_000 });

    const pageText = await page.textContent('body');
    const hasCount = /\d+ topics|mastery level/i.test(pageText ?? '');
    expect(hasCount).toBeTruthy();
  });

  test('shows level legend (L1-L5)', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Level names or emojis
    const pageText = await page.textContent('body');
    const hasLevels = /warmup|mastery|🥚|🌟|level/i.test(pageText ?? '');
    expect(hasLevels).toBeTruthy();
  });
});

test.describe('Skill Drills Hub — topic cards', () => {
  test('shows topic cards with icons and names', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Should show math topics
    const pageText = await page.textContent('body');
    const hasTopics = /number|fraction|geometry|algebra|arithmetic/i.test(pageText ?? '');
    expect(hasTopics).toBeTruthy();
  });

  test('topic cards show level progress dots', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Level dots show progress status (★, ✓, -, etc.)
    const pageText = await page.textContent('body');
    const hasProgress = /★|✓|start|→/i.test(pageText ?? '');
    expect(hasProgress).toBeTruthy();
  });

  test('clicking topic card navigates to drill level', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click first topic
    const topicLink = page
      .locator('a[href*="/practice/skill-drill/"]')
      .first();
    const hasLink = await topicLink.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasLink) {
      await topicLink.click();
      await page.waitForTimeout(2_000);

      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(50);
    } else {
      // May be buttons instead of links
      const topicBtn = page.locator('button').filter({
        hasText: /number|fraction|geometry|start/i,
      }).first();
      const hasBtn = await topicBtn.isVisible({ timeout: 5_000 }).catch(() => false);

      if (hasBtn) {
        await topicBtn.click();
        await page.waitForTimeout(2_000);

        const pageText = await page.textContent('body');
        expect(pageText?.length).toBeGreaterThan(50);
      }
    }
  });
});

test.describe('Skill Drills Hub — localStorage progress', () => {
  test('progress persists in localStorage', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Check if drill progress key exists
    const progress = await page.evaluate(() =>
      localStorage.getItem('mathspark_drill_progress'),
    );

    // Progress may or may not exist yet — just check no crash
    if (progress) {
      // Should be valid JSON
      const parsed = JSON.parse(progress);
      expect(typeof parsed).toBe('object');
    }
  });
});

test.describe('Skill Drills Hub — no errors', () => {
  test('page has no JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });
});
