import { test, expect } from '@playwright/test';

test.describe('Onboarding flow', () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage to simulate a fresh student
    await page.goto('/');
    await page.evaluate(() => {
      localStorage.removeItem('mathspark_student_id');
      localStorage.removeItem('mathspark_student_name');
    });
  });

  test('redirects to /start when no student is registered', async ({ page }) => {
    await page.goto('/chapters');
    await expect(page).toHaveURL(/\/start/);
  });

  test('shows welcome message and name input on /start', async ({ page }) => {
    await page.goto('/start');
    await expect(page.getByText(/Let's find out what you already know/i)).toBeVisible();
    await expect(page.getByPlaceholder(/name/i)).toBeVisible();
  });

  test('name input accepts text and shows Continue button', async ({ page }) => {
    await page.goto('/start');
    const input = page.getByPlaceholder(/name/i);
    await input.fill('TestKid');
    await expect(page.getByRole('button', { name: /continue|let's go|start/i })).toBeVisible();
  });
});
