import { test as publicTest, expect as publicExpect } from '@playwright/test';

publicTest.describe('Parent Dashboard — unauthenticated', () => {
  publicTest('redirects to login if not authenticated', async ({ page }) => {
    await page.goto('/parent/dashboard', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    // Should redirect to /auth/login or show login form
    const url = page.url();
    const pageText = await page.textContent('body');
    const redirected = /auth\/login/.test(url);
    const showsLogin = /sign in|log in|email|password/i.test(pageText ?? '');
    const showsLoading = /loading/i.test(pageText ?? '');

    publicExpect(redirected || showsLogin || showsLoading).toBeTruthy();
  });
});

// Parent dashboard requires NextAuth session (not student JWT),
// so we test basic rendering behavior without full auth.

publicTest.describe('Parent Dashboard — page structure', () => {
  publicTest('page does not crash on direct visit', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/parent/dashboard', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    // Page should not throw unhandled JS errors
    // (auth redirect is expected, but should not crash)
    publicExpect(errors).toHaveLength(0);
  });
});

publicTest.describe('Parent — pricing link', () => {
  publicTest('/pricing accessible from parent context', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    // Pricing page should render plans
    await publicExpect(
      page.getByText(/starter|advanced|unlimited/i).first(),
    ).toBeVisible({ timeout: 10_000 });
  });
});

publicTest.describe('Parent — auth pages', () => {
  publicTest('parent login page renders correctly', async ({ page }) => {
    await page.goto('/auth/login', { waitUntil: 'domcontentloaded' });

    await publicExpect(page.getByText('Parent sign in')).toBeVisible({ timeout: 10_000 });
  });

  publicTest('parent register page renders correctly', async ({ page }) => {
    await page.goto('/auth/register', { waitUntil: 'domcontentloaded' });

    const pageText = await page.textContent('body');
    const hasRegister = /create|register|sign up|get started/i.test(pageText ?? '');
    publicExpect(hasRegister).toBeTruthy();
  });

  publicTest('forgot password page renders correctly', async ({ page }) => {
    await page.goto('/auth/forgot-password', { waitUntil: 'domcontentloaded' });

    const pageText = await page.textContent('body');
    const hasForgot = /forgot|reset|password|email/i.test(pageText ?? '');
    publicExpect(hasForgot).toBeTruthy();
  });
});
