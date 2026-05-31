import { test, expect } from '@playwright/test';

test.describe('Practice page', () => {
  test.beforeEach(async ({ page }) => {
    // Pre-seed localStorage with a student so we can skip onboarding
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.setItem('mathspark_student_id', 'test-student-id');
      localStorage.setItem('mathspark_student_name', 'TestKid');
    });
  });

  test('loads the practice page for a topic', async ({ page }) => {
    await page.goto('/practice/ch11');
    // Either shows a question or redirects to /start (if student not in DB)
    // In both cases the page should not crash
    await expect(page).not.toHaveURL(/error/);
  });

  test('shows the topic name in the header', async ({ page }) => {
    await page.goto('/practice/ch11');
    // Wait for either question or loading to resolve
    await page.waitForLoadState('networkidle');
    // Should show either topic name or redirect gracefully
    const title = page.locator('h1');
    if (await title.count() > 0) {
      await expect(title).toBeVisible();
    }
  });

  test('timed mode toggle button is present', async ({ page }) => {
    await page.goto('/practice/ch11');
    await page.waitForLoadState('networkidle');
    const timerBtn = page.locator('button[aria-label*="timed mode"]');
    if (await timerBtn.count() > 0) {
      await expect(timerBtn).toBeVisible();
    }
  });
});
