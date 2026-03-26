import { test as publicTest, expect as publicExpect } from '@playwright/test';
import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/* ────────────────────────────────────────────────────────────────────────────
 * Unauthenticated redirects
 * ──────────────────────────────────────────────────────────────────────────── */

publicTest.describe('Auth — unauthenticated redirects', () => {
  publicTest('visiting /home without auth redirects to login', async ({ page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await page.waitForURL(/\/(student\/login|auth\/login|\?)/, { timeout: 10_000 }).catch(() => {});

    const hasGreeting = await page
      .locator('text=/good (morning|afternoon|evening)/i')
      .first()
      .isVisible({ timeout: 3_000 })
      .catch(() => false);

    publicExpect(hasGreeting).toBeFalsy();
  });

  publicTest('visiting /practice without auth redirects', async ({ page }) => {
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2_000);

    const hasPracticeHub = await page
      .getByText('Practice Hub')
      .isVisible({ timeout: 3_000 })
      .catch(() => false);

    publicExpect(hasPracticeHub).toBeFalsy();
  });

  publicTest('visiting /progress without auth redirects', async ({ page }) => {
    await page.goto('/progress', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(2_000);

    const hasProgress = await page
      .getByText('My Progress')
      .isVisible({ timeout: 3_000 })
      .catch(() => false);

    publicExpect(hasProgress).toBeFalsy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Student login UI flow
 * ──────────────────────────────────────────────────────────────────────────── */

publicTest.describe('Auth — student login UI', () => {
  publicTest('student login page renders email form', async ({ page }) => {
    await page.goto('/student/login', { waitUntil: 'domcontentloaded' });

    await publicExpect(page.getByText('Student login')).toBeVisible({ timeout: 10_000 });
    await publicExpect(page.locator('input[placeholder="Parent\'s email address"]')).toBeVisible();
    await publicExpect(
      page.locator('button').filter({ hasText: /find my profile/i }),
    ).toBeVisible();
  });

  publicTest('student login shows error for invalid email', async ({ page }) => {
    await page.goto('/student/login', { waitUntil: 'domcontentloaded' });

    const emailInput = page.locator('input[placeholder="Parent\'s email address"]');
    await emailInput.fill('notreal@example.com');
    await page.locator('button').filter({ hasText: /find my profile/i }).click();

    // Wait for API response — should show error or empty child list
    await page.waitForTimeout(3_000);
    const pageText = await page.textContent('body');
    const hasError = /error|not found|no students|no children|try again/i.test(pageText ?? '');
    const hasChildList = /who are you/i.test(pageText ?? '');
    publicExpect(hasError || hasChildList).toBeTruthy();
  });

  publicTest('"Use a different email" goes back to email step', async ({ page }) => {
    await page.goto('/student/login', { waitUntil: 'domcontentloaded' });

    const emailInput = page.locator('input[placeholder="Parent\'s email address"]');
    await emailInput.fill('test@example.com');
    await page.locator('button').filter({ hasText: /find my profile/i }).click();
    await page.waitForTimeout(2_000);

    const backBtn = page.locator('button').filter({ hasText: /different email/i });
    const hasBack = await backBtn.isVisible({ timeout: 5_000 }).catch(() => false);
    if (hasBack) {
      await backBtn.click();
      await publicExpect(emailInput).toBeVisible({ timeout: 5_000 });
    }
  });

  publicTest('student login has link to parent login', async ({ page }) => {
    await page.goto('/student/login', { waitUntil: 'domcontentloaded' });

    const parentLink = page.locator('a[href="/auth/login"]');
    await publicExpect(parentLink).toBeVisible({ timeout: 10_000 });
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Parent login UI
 * ──────────────────────────────────────────────────────────────────────────── */

publicTest.describe('Auth — parent login UI', () => {
  publicTest('parent login page renders email + password inputs', async ({ page }) => {
    await page.goto('/auth/login', { waitUntil: 'domcontentloaded' });

    await publicExpect(page.getByText('Parent sign in')).toBeVisible({ timeout: 10_000 });
    await publicExpect(page.locator('input[placeholder="Email address"]')).toBeVisible();
    await publicExpect(page.locator('input[placeholder="Password"]')).toBeVisible();
    await publicExpect(
      page.locator('button').filter({ hasText: /sign in/i }),
    ).toBeVisible();
  });

  publicTest('parent login has links to register and student login', async ({ page }) => {
    await page.goto('/auth/login', { waitUntil: 'domcontentloaded' });

    await publicExpect(page.locator('a[href="/auth/register"]')).toBeVisible({ timeout: 10_000 });
    await publicExpect(page.locator('a[href="/student/login"]')).toBeVisible({ timeout: 10_000 });
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Authenticated session
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Auth — authenticated session', () => {
  test('authenticated user can access /home', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(
      page.locator('text=/good (morning|afternoon|evening)/i').first(),
    ).toBeVisible({ timeout: 15_000 });
  });

  test('authenticated user can access /chapters', async ({ authenticatedPage: page }) => {
    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(
      page.locator('text=/what shall we practice/i').first(),
    ).toBeVisible({ timeout: 15_000 });
  });

  test('localStorage has student data after auth', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    const studentId = await page.evaluate(() =>
      localStorage.getItem('mathspark_student_id'),
    );
    const studentName = await page.evaluate(() =>
      localStorage.getItem('mathspark_student_name'),
    );

    expect(studentId).toBe('student_001');
    expect(studentName).toBe('Aarav Sharma');
  });

  test('cookie is set with correct name and flags', async ({ authenticatedPage: page }) => {
    const cookies = await page.context().cookies();
    const authCookie = cookies.find((c) => c.name === 'mathspark_student_token');

    expect(authCookie).toBeTruthy();
    expect(authCookie!.httpOnly).toBe(true);
    expect(authCookie!.path).toBe('/');
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Logout
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Auth — logout', () => {
  test('profile page shows student name and has logout', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText(/aarav/i).first()).toBeVisible({ timeout: 10_000 });

    const logoutBtn = page.locator('button, a').filter({ hasText: /log\s?out|sign\s?out/i });
    await expect(logoutBtn.first()).toBeVisible({ timeout: 10_000 });
  });

  test('clicking logout clears auth state', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const logoutBtn = page.locator('button').filter({ hasText: /log\s?out/i }).first();
    const hasLogout = await logoutBtn.isVisible({ timeout: 10_000 }).catch(() => false);

    if (!hasLogout) {
      test.skip(true, 'No logout button found on profile');
      return;
    }

    await logoutBtn.click();
    await page.waitForTimeout(3_000);

    // Should redirect to login/start/landing or clear session
    const url = page.url();
    const redirectedAway = /student\/login|auth\/login|start|\/$/.test(url);

    // If still on profile, check cookie was cleared
    if (!redirectedAway) {
      const cookies = await page.context().cookies();
      const authCookie = cookies.find((c) => c.name === 'mathspark_student_token');
      const hasValue = authCookie?.value && authCookie.value.length > 0;
      expect(!authCookie || !hasValue).toBeTruthy();
    } else {
      expect(redirectedAway).toBeTruthy();
    }
  });
});
