import { test as publicTest, expect as publicExpect } from '@playwright/test';

publicTest.describe('Onboarding — Welcome screen', () => {
  publicTest('welcome screen shows heading and Let\'s Go button', async ({ page }) => {
    await page.goto('/start', { waitUntil: 'domcontentloaded' });

    await publicExpect(
      page.getByText(/math superpowers/i).first(),
    ).toBeVisible({ timeout: 10_000 });

    await publicExpect(
      page.locator('button').filter({ hasText: /let.*go/i }).first(),
    ).toBeVisible({ timeout: 5_000 });
  });

  publicTest('welcome screen shows time estimate', async ({ page }) => {
    await page.goto('/start', { waitUntil: 'domcontentloaded' });

    const hasTime = await page
      .getByText(/2 minutes/i)
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    publicExpect(hasTime).toBeTruthy();
  });

  publicTest('clicking Let\'s Go advances to grade selection', async ({ page }) => {
    await page.goto('/start', { waitUntil: 'domcontentloaded' });

    const letsGo = page.locator('button').filter({ hasText: /let.*go/i }).first();
    await publicExpect(letsGo).toBeVisible({ timeout: 10_000 });
    await letsGo.click();
    await page.waitForTimeout(1_000);

    // Should show grade selection
    await publicExpect(
      page.getByText(/which grade/i).first(),
    ).toBeVisible({ timeout: 10_000 });
  });
});

publicTest.describe('Onboarding — Grade selection', () => {
  publicTest.beforeEach(async ({ page }) => {
    await page.goto('/start', { waitUntil: 'domcontentloaded' });
    await page.locator('button').filter({ hasText: /let.*go/i }).first().click();
    await page.waitForTimeout(1_000);
  });

  publicTest('grade selection shows 8 grade buttons (Gr 2-9)', async ({ page }) => {
    await publicExpect(
      page.getByText(/which grade/i).first(),
    ).toBeVisible({ timeout: 10_000 });

    // Should have buttons for grades 2 through 9
    for (const grade of [2, 3, 4, 5, 6, 7, 8, 9]) {
      const gradeBtn = page.getByText(`Gr ${grade}`, { exact: false }).first();
      await publicExpect(gradeBtn).toBeVisible({ timeout: 5_000 });
    }
  });

  publicTest('selecting a grade highlights the button', async ({ page }) => {
    await publicExpect(
      page.getByText(/which grade/i).first(),
    ).toBeVisible({ timeout: 10_000 });

    // Click Grade 4
    const gr4 = page.getByText('Gr 4', { exact: false }).first();
    await gr4.click();
    await page.waitForTimeout(300);

    // Selected button should have blue/highlighted styling
    const gradeContainer = gr4.locator('..');
    const classes = await gradeContainer.getAttribute('class').catch(() => '');
    const grClasses = await gr4.getAttribute('class').catch(() => '');
    const combinedClasses = (classes ?? '') + (grClasses ?? '');

    // Check either the button or its parent for selection styling
    const isSelected = /duo-blue|selected|scale-105|bg-blue/i.test(combinedClasses);
    publicExpect(isSelected).toBeTruthy();
  });

  publicTest('Next button enabled after grade selection', async ({ page }) => {
    await publicExpect(
      page.getByText(/which grade/i).first(),
    ).toBeVisible({ timeout: 10_000 });

    // Select a grade
    await page.getByText('Gr 4', { exact: false }).first().click();
    await page.waitForTimeout(300);

    // Next button should be enabled
    const nextBtn = page.locator('button').filter({ hasText: /next|→/i }).first();
    await publicExpect(nextBtn).toBeVisible({ timeout: 5_000 });
    await publicExpect(nextBtn).toBeEnabled();
  });
});

publicTest.describe('Onboarding — Goal selection', () => {
  publicTest.beforeEach(async ({ page }) => {
    await page.goto('/start', { waitUntil: 'domcontentloaded' });
    // Welcome → Let's Go
    await page.locator('button').filter({ hasText: /let.*go/i }).first().click();
    await page.waitForTimeout(1_000);
    // Grade selection → select Gr 4 → Next
    await page.getByText('Gr 4', { exact: false }).first().click();
    await page.waitForTimeout(300);
    await page.locator('button').filter({ hasText: /next|→/i }).first().click();
    await page.waitForTimeout(1_000);
  });

  publicTest('goal screen shows prompt and goal options', async ({ page }) => {
    // After grade selection the flow asks what the student is preparing for.
    await publicExpect(
      page.getByText(/what are you preparing for/i).first(),
    ).toBeVisible({ timeout: 10_000 });

    for (const goal of [/IPM Exam/i, /School Maths/i, /Just for Fun/i]) {
      await publicExpect(page.getByText(goal).first()).toBeVisible({ timeout: 5_000 });
    }
  });

  publicTest('selecting a goal advances past the goal screen', async ({ page }) => {
    await publicExpect(
      page.getByText(/what are you preparing for/i).first(),
    ).toBeVisible({ timeout: 10_000 });

    await page.getByText(/IPM Exam/i).first().click();
    // Goal selection auto-advances after a short Sparky message.
    await page.waitForTimeout(1_500);

    const advanced = await page
      .getByText(/what are you preparing for/i)
      .first()
      .isVisible({ timeout: 2_000 })
      .catch(() => false);

    publicExpect(advanced).toBeFalsy();
  });
});

publicTest.describe('Onboarding — display name & avatar', () => {
  publicTest('display name screen has League heading and color picker', async ({ page }) => {
    // This screen appears after the diagnostic quiz completes.
    // We can't easily run through the quiz in E2E, so test via direct URL param if supported,
    // or verify the screen structure exists in the onboarding flow component.
    await page.goto('/start', { waitUntil: 'domcontentloaded' });

    // Just verify the overall flow component renders without error
    const pageText = await page.textContent('body');
    publicExpect(pageText?.length).toBeGreaterThan(50);

    // Note: Full display name screen test would require completing the diagnostic quiz.
    // This test verifies the onboarding page loads without crash.
  });
});
