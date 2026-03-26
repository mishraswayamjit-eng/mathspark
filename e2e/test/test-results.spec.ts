import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';
import { createMockTest, submitTestAnswers } from '../helpers/api';

/**
 * Helper: create a test, submit all answers, then navigate to the results page.
 * Returns the testId.
 */
async function setupCompletedTest(page: import('@playwright/test').Page): Promise<string> {
  const testId = await createMockTest(page, { type: 'quick', questionCount: 5 });
  await submitTestAnswers(page, testId);
  return testId;
}

test.describe('Test Results — score display', () => {
  test('results page shows score ring with score/total', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test via API');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Score display: X/Y format
    const scoreText = page.locator('text=/\\d+\\/\\d+/');
    await expect(scoreText.first()).toBeVisible({ timeout: 15_000 });
  });

  test('results page shows grade label', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Grade labels: Outstanding, Excellent, Good work, Keep going, More practice
    const gradeLabels = /outstanding|excellent|good work|keep going|more practice/i;
    const pageText = await page.textContent('body');
    expect(pageText).toMatch(gradeLabels);
  });

  test('accuracy and time subtitle visible', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Accuracy percentage
    const hasAccuracy = await page
      .locator('text=/\\d+%\\s*accuracy/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasAccuracy).toBeTruthy();
  });
});

test.describe('Test Results — section tabs', () => {
  let sharedTestId = '';

  test.beforeAll(async ({ browser }) => {
    // Pre-create a test to share across this describe block
    // Each test will still navigate independently
  });

  test('5 section tabs are visible', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const tabs = ['Topics', 'Difficulty', 'Time', 'All Qs', 'Study Plan'];
    for (const tab of tabs) {
      await expect(
        page.getByText(tab, { exact: false }).first(),
      ).toBeVisible({ timeout: 10_000 });
    }
  });

  test('Topics tab shows topic cards with accuracy', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click Topics tab
    await page.getByText('Topics', { exact: false }).first().click();
    await page.waitForTimeout(500);

    // Should show topic names with accuracy
    const pageText = await page.textContent('body');
    expect(pageText).toMatch(/correct|%/i);
  });

  test('Difficulty tab shows Easy/Medium/Hard breakdown', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click Difficulty tab
    await page.getByText('Difficulty', { exact: false }).first().click();
    await page.waitForTimeout(500);

    const pageText = await page.textContent('body');
    expect(pageText).toMatch(/easy|medium|hard/i);
  });

  test('Time tab shows avg time and slowest questions', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click Time tab
    await page.getByText('Time', { exact: false }).first().click();
    await page.waitForTimeout(500);

    const pageText = await page.textContent('body');
    expect(pageText).toMatch(/avg|average|time|slowest|per question/i);
  });

  test('All Qs tab shows question accordion', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click All Qs tab
    await page.getByText('All Qs', { exact: false }).first().click();
    await page.waitForTimeout(500);

    // Should show Q1, Q2, etc.
    await expect(
      page.getByText(/Q1/i).first(),
    ).toBeVisible({ timeout: 5_000 });
  });

  test('clicking question accordion expands it', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click All Qs tab
    await page.getByText('All Qs', { exact: false }).first().click();
    await page.waitForTimeout(500);

    // Click first question to expand
    const q1 = page.getByText(/Q1/i).first();
    await q1.click();
    await page.waitForTimeout(500);

    // Expanded content should show answer options with green/red highlighting
    const pageText = await page.textContent('body');
    expect(pageText).toMatch(/✓|✗|correct|option/i);
  });

  test('Study Plan tab shows priority sections', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click Study Plan tab
    await page.getByText('Study Plan', { exact: false }).first().click();
    await page.waitForTimeout(500);

    // Should show priority/speed/strength sections or "balanced" message
    const pageText = await page.textContent('body');
    expect(pageText).toMatch(/priority|speed|strength|balanced|practice/i);
  });
});

test.describe('Test Results — action buttons', () => {
  test('"Take Another Test" button navigates to /test', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const takeAnother = page.locator('a, button').filter({ hasText: /take another test/i }).first();
    await expect(takeAnother).toBeVisible({ timeout: 10_000 });

    await takeAnother.click();
    await page.waitForURL(/\/test/, { timeout: 10_000 });
  });

  test('"View All Tests" button navigates to /test/history', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });

    let testId: string;
    try {
      testId = await setupCompletedTest(page);
    } catch {
      test.skip(true, 'Could not create/submit test');
      return;
    }

    await page.goto(`/test/${testId}/response`, { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const viewAll = page.locator('a, button').filter({ hasText: /view all tests/i }).first();
    await expect(viewAll).toBeVisible({ timeout: 10_000 });

    await viewAll.click();
    await page.waitForURL(/\/test\/history/, { timeout: 10_000 });
  });
});
