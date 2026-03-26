import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/* ────────────────────────────────────────────────────────────────────────────
 * Sparky Explains
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Sparky Explains — /learn/examples', () => {
  test('page shows heading and example count', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/examples', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Sparky Explains').first()).toBeVisible({ timeout: 15_000 });

    // Should show example count or description
    const hasCount = await page
      .locator('text=/\\d+ worked examples/i')
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    expect(hasCount).toBeTruthy();
  });

  test('grade filter tabs visible', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/examples', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // "All Grades" or individual grade buttons
    const hasGrades = await page
      .getByText(/all grades|G4|G5/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasGrades).toBeTruthy();
  });

  test('topic filter chips visible', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/examples', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasTopics = await page
      .getByText(/all topics/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasTopics).toBeTruthy();
  });

  test('example cards show difficulty badges', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/examples', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Cards should show Easy/Medium/Hard badges
    const pageText = await page.textContent('body');
    const hasDifficulty = /easy|medium|hard/i.test(pageText ?? '');
    expect(hasDifficulty).toBeTruthy();
  });

  test('clicking grade filter updates example list', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/examples', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click a different grade filter
    const gradeBtn = page.getByText('G5', { exact: false }).first();
    const hasGrade = await gradeBtn.isVisible({ timeout: 5_000 }).catch(() => false);

    if (hasGrade) {
      await gradeBtn.click();
      await page.waitForTimeout(1_000);

      // Page should still have examples (or empty state)
      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(100);
    }
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Concept Map
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Concept Map — /learn/concept-map', () => {
  test('page shows heading with concept count', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/concept-map', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Concept Map').first()).toBeVisible({ timeout: 15_000 });

    // Should show concept/domain/connection counts
    const hasStats = await page
      .locator('text=/\\d+ concepts|\\d+ domains|\\d+ connections/i')
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    expect(hasStats).toBeTruthy();
  });

  test('domain islands visible and expandable', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/concept-map', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Domain headers should be buttons
    const domainHeaders = page.locator('button').filter({ hasText: /concepts|links/ });
    const count = await domainHeaders.count();
    expect(count).toBeGreaterThan(0);

    // Click first domain to expand
    await domainHeaders.first().click();
    await page.waitForTimeout(500);

    // Expanded content should show concept list items
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(200);
  });

  test('grade filters visible', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/concept-map', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasGrades = await page
      .getByText(/all grades|grade 4/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasGrades).toBeTruthy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Mistake Patterns
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Mistake Patterns — /learn/mistakes', () => {
  test('page shows heading and pattern count', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/mistakes', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Mistake Patterns').first()).toBeVisible({ timeout: 15_000 });

    const hasCount = await page
      .locator('text=/\\d+ traps/i')
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    expect(hasCount).toBeTruthy();
  });

  test('category filter buttons visible', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/mistakes', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // "All" filter and category filters
    const hasAll = await page
      .getByText(/^All/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasAll).toBeTruthy();
  });

  test('pattern cards show frequency badges', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/mistakes', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    const hasFrequency = /very high|high|medium|low/i.test(pageText ?? '');
    expect(hasFrequency).toBeTruthy();
  });

  test('clicking pattern card expands details', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/mistakes', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click first pattern card to expand
    const patternCard = page.locator('button').filter({
      hasText: /wrong|error|missing|sign|notation/i,
    }).first();
    const hasCard = await patternCard.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCard) {
      await patternCard.click();
      await page.waitForTimeout(500);

      // Expanded content should show "Why This Happens" and "How to Fix It"
      const pageText = await page.textContent('body');
      const hasExpanded = /why this happens|how to fix/i.test(pageText ?? '');
      expect(hasExpanded).toBeTruthy();
    }
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Strategy Bank & Math Stories
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Strategy Bank — /learn/strategies', () => {
  test('page loads with heading', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/strategies', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(50);

    // Should show strategy/tips content
    const hasContent = /strateg|tip|exam|trick/i.test(pageText ?? '');
    expect(hasContent).toBeTruthy();
  });
});

test.describe('Math Stories — /learn/stories', () => {
  test('page loads with heading', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/stories', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(50);

    // Should show story/math content
    const hasContent = /stor|math|real.world|discover/i.test(pageText ?? '');
    expect(hasContent).toBeTruthy();
  });
});
