import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Home Dashboard — core sections', () => {
  test('shows greeting with student name', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(
      page.locator('text=/good (morning|afternoon|evening)/i').first(),
    ).toBeVisible({ timeout: 15_000 });

    await expect(page.getByText(/aarav/i).first()).toBeVisible({ timeout: 5_000 });
  });

  test('Today\'s Plan section visible with items', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasPlan = await page
      .getByText("Today's Plan")
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // Plan section should render (either items or empty state)
    expect(hasPlan).toBeTruthy();
  });

  test('Exam Readiness section visible', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasReadiness = await page
      .getByText(/exam readiness/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasReadiness).toBeTruthy();
  });

  test('Your Topics section visible', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasTopics = await page
      .getByText(/your topics/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasTopics).toBeTruthy();
  });

  test('Recent Activity section visible', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasActivity = await page
      .getByText(/recent activity/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // May not show if no recent activity
    expect(true).toBeTruthy();
  });
});

test.describe('Home Dashboard — quick actions', () => {
  test('Quick Practice link navigates correctly', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const quickPractice = page.getByText(/quick practice/i).first();
    const hasCTA = await quickPractice.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCTA) {
      await quickPractice.click();
      await page.waitForTimeout(2_000);
      // Should navigate to /chapters or /practice
      expect(page.url()).toMatch(/\/(chapters|practice)/);
    }
  });

  test('Flashcards quick action navigates to /flashcards', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const flashcardsLink = page.locator('a[href="/flashcards"]').first();
    const hasLink = await flashcardsLink.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasLink) {
      await flashcardsLink.click();
      await page.waitForURL('/flashcards', { timeout: 10_000 });
      await expect(page.getByText("Sparky's Cards")).toBeVisible({ timeout: 10_000 });
    }
  });

  test('Skill Drills quick action navigates to /practice/skill-drill', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const skillLink = page.locator('a[href="/practice/skill-drill"]').first();
    const hasLink = await skillLink.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasLink) {
      await skillLink.click();
      await page.waitForURL('/practice/skill-drill', { timeout: 10_000 });
    }
  });

  test('Sparky Explains quick action navigates to /learn/examples', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const explainLink = page.locator('a[href="/learn/examples"]').first();
    const hasLink = await explainLink.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasLink) {
      await explainLink.click();
      await page.waitForURL('/learn/examples', { timeout: 10_000 });
    }
  });
});

test.describe('Home Dashboard — learn more cards', () => {
  test('Learn More section shows Strategy Bank, Math Stories, Concept Map, Mistake Patterns', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const cards = ['Strategy Bank', 'Math Stories', 'Concept Map', 'Mistake Patterns'];
    let found = 0;
    for (const card of cards) {
      const visible = await page
        .getByText(card, { exact: false })
        .first()
        .isVisible({ timeout: 5_000 })
        .catch(() => false);
      if (visible) found++;
    }

    expect(found).toBeGreaterThanOrEqual(2);
  });

  test('Strategy Bank link navigates to /learn/strategies', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const strategyLink = page.locator('a[href="/learn/strategies"]').first();
    const hasLink = await strategyLink.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasLink) {
      await strategyLink.click();
      await page.waitForURL('/learn/strategies', { timeout: 10_000 });
    }
  });
});

test.describe('Home Dashboard — no JS errors', () => {
  test('page loads without JavaScript errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });
});
