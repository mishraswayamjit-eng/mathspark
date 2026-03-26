import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Progress Dashboard', () => {
  test('progress page shows heading and mastery data', async ({ authenticatedPage: page }) => {
    await page.goto('/progress', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('My Progress')).toBeVisible();

    // Should show some progress content (mastery bars, topic cards, or stats)
    const hasContent = await page
      .locator('text=/mastery|topics|streak|xp|accuracy|progress/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasContent).toBeTruthy();
  });

  test('progress page shows topic mastery breakdown', async ({ authenticatedPage: page }) => {
    await page.goto('/progress', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Should display topic names from the curriculum
    const topicNames = [
      'Number System',
      'Fractions',
      'Geometry',
      'Data Handling',
    ];

    let foundTopics = 0;
    for (const topic of topicNames) {
      const visible = await page
        .getByText(topic, { exact: false })
        .first()
        .isVisible({ timeout: 5_000 })
        .catch(() => false);
      if (visible) foundTopics++;
    }

    // At least some topics should be visible (student_001 has progress data)
    expect(foundTopics).toBeGreaterThan(0);
  });

  test('progress report page loads', async ({ authenticatedPage: page }) => {
    await page.goto('/progress/report', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Should show report heading with student name
    await expect(
      page.locator('text=/report/i').first(),
    ).toBeVisible({ timeout: 15_000 });
  });

  test('progress page has no JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/progress', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });

  test('streak display is visible on home page', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Home page should show streak or XP information
    const hasStreak = await page
      .locator('text=/streak|🔥|day/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    const hasXP = await page
      .locator('text=/xp|points|score/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // At least one of streak or XP should display
    expect(hasStreak || hasXP).toBeTruthy();
  });
});
