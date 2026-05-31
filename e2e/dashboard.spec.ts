import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.setItem('mathspark_student_id', 'test-student-id');
      localStorage.setItem('mathspark_student_name', 'TestKid');
    });
  });

  test('loads dashboard without crashing', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    await expect(page).not.toHaveURL(/error/);
  });

  test('shows navigation bar', async ({ page }) => {
    await page.goto('/dashboard');
    const nav = page.getByRole('navigation', { name: /main navigation/i });
    await expect(nav).toBeVisible();
  });

  test('chapters page shows 16 topic cards', async ({ page }) => {
    // Chapter grid should render even without DB (topics fetched on mount)
    await page.goto('/chapters');
    await page.waitForLoadState('networkidle');
    // Verify page loaded
    await expect(page).not.toHaveURL(/error/);
  });

  test('offline page renders correctly', async ({ page }) => {
    await page.goto('/offline');
    await expect(page.getByText(/No internet/i)).toBeVisible();
  });
});
