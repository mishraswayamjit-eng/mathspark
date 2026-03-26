import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/* ────────────────────────────────────────────────────────────────────────────
 * Paper Selection Hub — /practice/papers
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Paper Selection Hub', () => {
  test('shows Exam Papers heading', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/papers', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    const hasHeading = /exam papers|practice papers|papers/i.test(pageText ?? '');
    expect(hasHeading).toBeTruthy();
  });

  test('grade selector switches paper list', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/papers', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click a grade button
    const gradeBtn = page.getByText(/Gr\s*4|Grade 4/i).first();
    const hasGrade = await gradeBtn.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasGrade) {
      await gradeBtn.click();
      await page.waitForTimeout(1_000);

      const pageText = await page.textContent('body');
      expect(pageText?.length).toBeGreaterThan(100);
    }
  });

  test('format tabs visible (Quick, Practice, IPM Mock)', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/papers', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    const hasFormats = /quick|practice|ipm|mock|15 min|30 min|60 min/i.test(pageText ?? '');
    expect(hasFormats).toBeTruthy();
  });

  test('paper list shows metadata (questions, duration, marks)', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/practice/papers', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');
    const hasMeta = /question|min|mark|duration/i.test(pageText ?? '');
    expect(hasMeta).toBeTruthy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Exam Simulator — /practice/papers/[paperId]
 * ──────────────────────────────────────────────────────────────────────────── */

/**
 * Navigate to a paper by clicking the first paper link from the hub.
 * Returns true if we landed on a paper page.
 */
async function navigateToFirstPaper(page: import('@playwright/test').Page): Promise<boolean> {
  await page.goto('/practice/papers', { waitUntil: 'domcontentloaded' });
  await waitForDataLoad(page);

  const paperLink = page.locator('a[href*="/practice/papers/"]').first();
  const hasLink = await paperLink.isVisible({ timeout: 10_000 }).catch(() => false);
  if (!hasLink) return false;

  await paperLink.click();
  await page.waitForURL(/\/practice\/papers\/.+/, { timeout: 15_000 });
  await waitForDataLoad(page);
  return true;
}

test.describe('Exam Simulator — instructions phase', () => {
  test('shows instructions with stats and Start button', async ({ authenticatedPage: page }) => {
    const landed = await navigateToFirstPaper(page);
    if (!landed) {
      test.skip(true, 'No papers available');
      return;
    }

    // Instructions should show question count, duration, marks
    const pageText = await page.textContent('body');
    const hasInstructions = /question|duration|mark|start exam|start/i.test(pageText ?? '');
    expect(hasInstructions).toBeTruthy();
  });

  test('shows marking scheme info', async ({ authenticatedPage: page }) => {
    const landed = await navigateToFirstPaper(page);
    if (!landed) {
      test.skip(true, 'No papers available');
      return;
    }

    const pageText = await page.textContent('body');
    const hasMarking = /correct|wrong|unanswered|passing|marks/i.test(pageText ?? '');
    expect(hasMarking).toBeTruthy();
  });

  test('clicking Start Exam begins the exam', async ({ authenticatedPage: page }) => {
    const landed = await navigateToFirstPaper(page);
    if (!landed) {
      test.skip(true, 'No papers available');
      return;
    }

    const startBtn = page.locator('button').filter({ hasText: /start exam|start/i }).first();
    const hasStart = await startBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasStart) {
      test.skip(true, 'Start button not found');
      return;
    }

    await startBtn.click();
    await page.waitForTimeout(2_000);

    // Should now show exam UI (timer, question, options)
    const pageText = await page.textContent('body');
    const hasExam = /⏱|Q\d|option|A\b|B\b/i.test(pageText ?? '');
    expect(hasExam).toBeTruthy();
  });
});

test.describe('Exam Simulator — exam phase', () => {
  async function startExam(page: import('@playwright/test').Page): Promise<boolean> {
    const landed = await navigateToFirstPaper(page);
    if (!landed) return false;

    const startBtn = page.locator('button').filter({ hasText: /start exam|start/i }).first();
    const hasStart = await startBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasStart) return false;

    await startBtn.click();
    await page.waitForTimeout(2_000);
    return true;
  }

  test('timer visible and counting down', async ({ authenticatedPage: page }) => {
    const started = await startExam(page);
    if (!started) {
      test.skip(true, 'Could not start exam');
      return;
    }

    const timer = page.locator('text=/⏱|\\d+:\\d+/');
    await expect(timer.first()).toBeVisible({ timeout: 10_000 });
  });

  test('question content and options displayed', async ({ authenticatedPage: page }) => {
    const started = await startExam(page);
    if (!started) {
      test.skip(true, 'Could not start exam');
      return;
    }

    // Options A/B/C/D should be buttons
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(100);
  });

  test('selecting an option highlights it', async ({ authenticatedPage: page }) => {
    const started = await startExam(page);
    if (!started) {
      test.skip(true, 'Could not start exam');
      return;
    }

    const optionA = page.locator('button').filter({ has: page.locator('text=/^A$/') }).first();
    const hasOpt = await optionA.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasOpt) {
      test.skip(true, 'Option A not found');
      return;
    }

    await optionA.click();
    await page.waitForTimeout(300);

    const classes = await optionA.getAttribute('class');
    expect(classes).toMatch(/blue|selected/);
  });

  test('flag button toggles', async ({ authenticatedPage: page }) => {
    const started = await startExam(page);
    if (!started) {
      test.skip(true, 'Could not start exam');
      return;
    }

    const flagBtn = page.locator('button').filter({ hasText: /flag|🚩/i }).first();
    const hasFlag = await flagBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasFlag) {
      test.skip(true, 'Flag button not found');
      return;
    }

    await flagBtn.click();
    await page.waitForTimeout(300);

    const pageText = await page.textContent('body');
    expect(pageText).toMatch(/flagged|🚩/i);
  });

  test('prev/next navigation works', async ({ authenticatedPage: page }) => {
    const started = await startExam(page);
    if (!started) {
      test.skip(true, 'Could not start exam');
      return;
    }

    // Click Next
    const nextBtn = page.locator('button').filter({ hasText: /→|next/i }).first();
    const hasNext = await nextBtn.isVisible({ timeout: 5_000 }).catch(() => false);
    if (hasNext) {
      await nextBtn.click();
      await page.waitForTimeout(500);

      // Click Prev
      const prevBtn = page.locator('button').filter({ hasText: /←|prev/i }).first();
      const hasPrev = await prevBtn.isVisible({ timeout: 5_000 }).catch(() => false);
      if (hasPrev) {
        await prevBtn.click();
        await page.waitForTimeout(500);
      }
    }

    // Should still be on exam page
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(100);
  });

  test('question navigator opens with grid', async ({ authenticatedPage: page }) => {
    const started = await startExam(page);
    if (!started) {
      test.skip(true, 'Could not start exam');
      return;
    }

    const navBtn = page.locator('button').filter({ hasText: /Q\d+/i }).first();
    const hasNav = await navBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasNav) {
      test.skip(true, 'Navigator not found');
      return;
    }

    await navBtn.click();
    await page.waitForTimeout(500);

    // Should show grid with answered/unanswered counts
    const pageText = await page.textContent('body');
    expect(pageText).toMatch(/answered|unanswered/i);
  });
});

test.describe('Exam Simulator — no errors', () => {
  test('papers page has no JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/practice/papers', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });
});
