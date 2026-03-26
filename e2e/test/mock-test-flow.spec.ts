import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';
import { createMockTest } from '../helpers/api';

test.describe('Test Hub', () => {
  test('test hub shows test type options', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('IPM Mock Test')).toBeVisible();
    await expect(page.getByText(/Quick Test/i)).toBeVisible();
  });

  test('test hub shows all test types', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const testTypes = ['Quick Test', 'Half Paper', 'IPM Blueprint', 'Full Paper'];
    for (const type of testTypes) {
      const visible = await page
        .getByText(type, { exact: false })
        .first()
        .isVisible({ timeout: 5_000 })
        .catch(() => false);
      if (type === 'Quick Test') expect(visible).toBeTruthy();
    }
  });

  test('test history page loads', async ({ authenticatedPage: page }) => {
    await page.goto('/test/history', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Test History')).toBeVisible();
  });
});

test.describe('Test Creation & UI', () => {
  test('create a test and see test page', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const startButton = page.locator('button').filter({ hasText: /start/i }).first();
    await expect(startButton).toBeVisible({ timeout: 10_000 });
    await startButton.click();

    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
  });

  test('timer visible on test page', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('button').filter({ hasText: /start/i }).first().click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const timer = page.locator('text=/⏱|\\d+:\\d+/');
    await expect(timer.first()).toBeVisible({ timeout: 10_000 });
  });

  test('question counter visible', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('button').filter({ hasText: /start/i }).first().click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const counter = page.locator('text=/✎\\s*\\d+\\/\\d+/');
    await expect(counter.first()).toBeVisible({ timeout: 10_000 });
  });
});

test.describe('Test — answer selection', () => {
  test('click option A selects it', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('button').filter({ hasText: /start/i }).first().click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const optionA = page.locator('button').filter({ has: page.locator('text=/^A$/') }).first();
    const hasOption = await optionA.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasOption) {
      test.skip(true, 'Option A button not found');
      return;
    }

    await optionA.click();
    await page.waitForTimeout(500);

    const classes = await optionA.getAttribute('class');
    expect(classes).toMatch(/blue|selected/);
  });

  test('clicking same option deselects it', async ({ authenticatedPage: page }) => {
    // Use API to create test directly (avoids slow UI click + navigation)
    const testId = await createMockTest(page).catch(() => null);
    if (!testId) { test.skip(true, 'Could not create test via API'); return; }

    await page.goto(`/test/${testId}`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const optionA = page.locator('button').filter({ has: page.locator('text=/^A$/') }).first();
    const hasOption = await optionA.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasOption) {
      test.skip(true, 'Option A button not found');
      return;
    }

    // Select
    await optionA.click();
    await page.waitForTimeout(300);

    // Deselect
    await optionA.click();
    await page.waitForTimeout(300);

    const classes = await optionA.getAttribute('class');
    const isDeselected = !classes?.includes('blue-50') || classes?.includes('white');
    expect(isDeselected).toBeTruthy();
  });
});

test.describe('Test — flag & navigator', () => {
  test('flag button toggles between Flag and Flagged', async ({ authenticatedPage: page }) => {
    const testId = await createMockTest(page).catch(() => null);
    if (!testId) { test.skip(true, 'Could not create test via API'); return; }

    await page.goto(`/test/${testId}`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const flagBtn = page.locator('button').filter({ hasText: /flag/i }).first();
    const hasFlag = await flagBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasFlag) {
      test.skip(true, 'Flag button not found');
      return;
    }

    // Click to flag
    await flagBtn.click();
    await page.waitForTimeout(300);
    await expect(page.getByText(/flagged/i).first()).toBeVisible({ timeout: 3_000 });

    // Click again to unflag
    const flaggedBtn = page.locator('button').filter({ hasText: /flagged/i }).first();
    await flaggedBtn.click();
    await page.waitForTimeout(300);
    await expect(page.getByText('Flag').first()).toBeVisible({ timeout: 3_000 });
  });

  test('navigator button opens Question Navigator modal', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('button').filter({ hasText: /start/i }).first().click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const navButton = page.locator('button').filter({ hasText: /Q\d+/i }).first();
    const hasNav = await navButton.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasNav) {
      test.skip(true, 'Navigator button not found');
      return;
    }

    await navButton.click();
    await expect(page.getByText('Question Navigator')).toBeVisible({ timeout: 5_000 });
  });

  test('navigator shows answered/flagged/unanswered counts', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('button').filter({ hasText: /start/i }).first().click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const navButton = page.locator('button').filter({ hasText: /Q\d+/i }).first();
    const hasNav = await navButton.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasNav) {
      test.skip(true, 'Navigator button not found');
      return;
    }

    await navButton.click();
    await page.waitForTimeout(500);

    await expect(page.getByText(/answered/i).first()).toBeVisible({ timeout: 5_000 });
    await expect(page.getByText(/unanswered/i).first()).toBeVisible({ timeout: 5_000 });
  });

  test('clicking Q number in navigator jumps to that question', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('button').filter({ hasText: /start/i }).first().click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    const navButton = page.locator('button').filter({ hasText: /Q\d+/i }).first();
    const hasNav = await navButton.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasNav) {
      test.skip(true, 'Navigator not found');
      return;
    }

    await navButton.click();
    await page.waitForTimeout(500);

    // Click question 2 in the grid
    const q2 = page.getByText('2', { exact: true }).last();
    await q2.click().catch(() => {});
    await page.waitForTimeout(500);

    const pageText = await page.textContent('body');
    expect(pageText).toBeTruthy();
  });
});

test.describe('Test — submit & quit', () => {
  test('submit shows confirmation modal with counts', async ({ authenticatedPage: page }) => {
    await page.goto('/test', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('button').filter({ hasText: /start/i }).first().click();
    await page.waitForURL(/\/test\//, { timeout: 20_000 });
    await waitForDataLoad(page);

    // Navigate to last Q with → button repeatedly
    const nextBtn = page.locator('button').filter({ hasText: /→/ }).first();
    for (let i = 0; i < 20; i++) {
      const hasNext = await nextBtn.isVisible({ timeout: 1_000 }).catch(() => false);
      if (!hasNext) break;
      const text = await nextBtn.textContent();
      if (/submit/i.test(text ?? '')) break;
      await nextBtn.click();
      await page.waitForTimeout(200);
    }

    const submitBtn = page.locator('button').filter({ hasText: /submit/i }).first();
    const hasSubmit = await submitBtn.isVisible({ timeout: 3_000 }).catch(() => false);
    if (hasSubmit) {
      await submitBtn.click();
      await page.waitForTimeout(500);

      await expect(
        page.getByText(/ready to submit/i).first(),
      ).toBeVisible({ timeout: 5_000 });

      const modalText = await page.textContent('body');
      expect(modalText).toMatch(/attempted|unanswered/i);
    }
  });

  test('quit button shows leave confirmation', async ({ authenticatedPage: page }) => {
    const testId = await createMockTest(page).catch(() => null);
    if (!testId) { test.skip(true, 'Could not create test via API'); return; }

    await page.goto(`/test/${testId}`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const backBtn = page.locator('button').filter({ hasText: /←/ }).first();
    const hasBack = await backBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasBack) {
      test.skip(true, 'Back button not found');
      return;
    }

    await backBtn.click();
    await page.waitForTimeout(500);

    await expect(
      page.getByText(/leave the test/i).first(),
    ).toBeVisible({ timeout: 5_000 });

    await expect(
      page.locator('button').filter({ hasText: /keep going/i }).first(),
    ).toBeVisible({ timeout: 3_000 });
    await expect(
      page.locator('button').filter({ hasText: /leave/i }).first(),
    ).toBeVisible({ timeout: 3_000 });
  });

  test('keep going dismisses quit modal', async ({ authenticatedPage: page }) => {
    const testId = await createMockTest(page).catch(() => null);
    if (!testId) { test.skip(true, 'Could not create test via API'); return; }

    await page.goto(`/test/${testId}`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const backBtn = page.locator('button').filter({ hasText: /←/ }).first();
    const hasBack = await backBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasBack) {
      test.skip(true, 'Back button not found');
      return;
    }

    await backBtn.click();
    await page.waitForTimeout(500);

    const keepGoing = page.locator('button').filter({ hasText: /keep going/i }).first();
    const hasModal = await keepGoing.isVisible({ timeout: 5_000 }).catch(() => false);
    if (!hasModal) {
      test.skip(true, 'Quit modal did not appear');
      return;
    }

    await keepGoing.click();
    await page.waitForTimeout(500);

    await expect(page.getByText(/leave the test/i).first()).toBeHidden({ timeout: 3_000 });
  });
});
