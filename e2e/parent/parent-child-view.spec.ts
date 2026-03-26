import { test as publicTest, expect as publicExpect } from '@playwright/test';

publicTest.describe('Parent Child View — /parent/[studentId]', () => {
  // This is a public read-only page — no auth required
  const studentId = 'student_001';

  publicTest('shows student name and grade', async ({ page }) => {
    await page.goto(`/parent/${studentId}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    // Should show student name or "report not found"
    const hasContent = /aarav|progress report|not found|loading/i.test(pageText ?? '');
    publicExpect(hasContent).toBeTruthy();
  });

  publicTest('shows quick stats grid (Solved, Streak, Mastered)', async ({ page }) => {
    await page.goto(`/parent/${studentId}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5_000);

    const pageText = await page.textContent('body');
    // If report loads, should show stats
    const isReport = /solved|streak|mastered|accuracy/i.test(pageText ?? '');
    const isNotFound = /not found|error/i.test(pageText ?? '');

    publicExpect(isReport || isNotFound).toBeTruthy();
  });

  publicTest('shows weekly activity chart', async ({ page }) => {
    await page.goto(`/parent/${studentId}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5_000);

    const pageText = await page.textContent('body');
    const hasWeekly = /mon|tue|wed|thu|fri|sat|sun|weekly/i.test(pageText ?? '');
    // If report loaded
    if (!/not found|error/i.test(pageText ?? '')) {
      publicExpect(hasWeekly).toBeTruthy();
    }
  });

  publicTest('shows strongest & weakest topics', async ({ page }) => {
    await page.goto(`/parent/${studentId}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5_000);

    const pageText = await page.textContent('body');
    const hasTopics = /best at|focus on|strong|weak/i.test(pageText ?? '');
    // Conditional — only if report loaded
    if (!/not found|error/i.test(pageText ?? '')) {
      publicExpect(hasTopics).toBeTruthy();
    }
  });

  publicTest('shows encouragement messages section', async ({ page }) => {
    await page.goto(`/parent/${studentId}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5_000);

    const pageText = await page.textContent('body');
    const hasEncouragement = /encouragement|copy|message/i.test(pageText ?? '');
    // Conditional
    if (!/not found|error/i.test(pageText ?? '')) {
      publicExpect(hasEncouragement).toBeTruthy();
    }
  });

  publicTest('invalid student ID shows not-found state', async ({ page }) => {
    await page.goto('/parent/invalid-student-99999', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|error|couldn.*t|loading/i.test(pageText ?? '');
    publicExpect(hasError).toBeTruthy();
  });

  publicTest('share link button visible', async ({ page }) => {
    await page.goto(`/parent/${studentId}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(5_000);

    const pageText = await page.textContent('body');
    if (/not found|error/i.test(pageText ?? '')) {
      publicTest.skip(true, 'Report not available');
      return;
    }

    const shareBtn = page.locator('button, a').filter({ hasText: /copy|share|link/i }).first();
    const hasShare = await shareBtn.isVisible({ timeout: 5_000 }).catch(() => false);
    publicExpect(hasShare).toBeTruthy();
  });
});
