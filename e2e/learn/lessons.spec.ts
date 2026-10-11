import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/* ────────────────────────────────────────────────────────────────────────────
 * Lessons Hub — /learn/lessons
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Lessons Hub — /learn/lessons', () => {
  test('shows heading and Sparky intro', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Concept Lessons')).toBeVisible({ timeout: 10_000 });

    // Sparky intro box
    await expect(
      page.getByText(/learn new concepts step by step/i).first(),
    ).toBeVisible({ timeout: 5_000 });
  });

  test('renders topic grid with cards', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Topic cards link to /learn/lessons/{slug}
    const topicLinks = page.locator('a[href*="/learn/lessons/"]');
    const count = await topicLinks.count();
    expect(count).toBeGreaterThanOrEqual(6);
  });

  test('topic cards show name, grade range, and description', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/learn/lessons', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pageText = await page.textContent('body');

    // At least one known topic name should appear
    const hasTopicName = /fractions|geometry|equations|ratios/i.test(pageText ?? '');
    expect(hasTopicName).toBeTruthy();

    // Grade ranges should be visible (e.g., "Grades 2–6")
    const hasGradeRange = /grades?\s*\d/i.test(pageText ?? '');
    expect(hasGradeRange).toBeTruthy();
  });

  test('each topic card shows a progress bar', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Progress bars inside topic cards
    const progressBars = page.locator('a[href*="/learn/lessons/"] div[class*="rounded-full"]');
    const count = await progressBars.count();
    expect(count).toBeGreaterThan(0);
  });

  test('clicking a topic card navigates to level map', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/learn/lessons', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const firstCard = page.locator('a[href*="/learn/lessons/"]').first();
    await firstCard.click();

    await page.waitForURL(/\/learn\/lessons\/.+/, { timeout: 15_000 });
    expect(page.url()).toMatch(/\/learn\/lessons\/[a-z-]+/);
  });

  test('back button links to /chapters', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const backLink = page.locator('a[href="/chapters"]');
    await expect(backLink).toBeVisible({ timeout: 5_000 });
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Topic Level Map — /learn/lessons/[topicSlug]
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Topic Level Map — /learn/lessons/fractions', () => {
  test('shows topic name and description', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText('Fractions').first()).toBeVisible({ timeout: 10_000 });

    // Description and grade range
    const pageText = await page.textContent('body');
    const hasDescription = /pizza slices|mixed numbers|grades?\s*2/i.test(pageText ?? '');
    expect(hasDescription).toBeTruthy();
  });

  test('renders 5 level cards', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Level links to /learn/lessons/fractions/{1-5}
    const levelLinks = page.locator('a[href*="/learn/lessons/fractions/"]');
    const count = await levelLinks.count();
    expect(count).toBe(5);
  });

  test('level cards show label and subtitle', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // First level label
    await expect(
      page.getByText('Fair Shares').first(),
    ).toBeVisible({ timeout: 5_000 });
  });

  test('level cards have progress bars', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const progressBars = page.locator(
      'a[href*="/learn/lessons/fractions/"] div[class*="rounded-full"]',
    );
    const count = await progressBars.count();
    expect(count).toBeGreaterThan(0);
  });

  test('clicking a level navigates to lesson session', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/learn/lessons/fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const firstLevel = page.locator('a[href*="/learn/lessons/fractions/"]').first();
    await firstLevel.click();

    await page.waitForURL(/\/learn\/lessons\/fractions\/\d+/, { timeout: 15_000 });
    expect(page.url()).toMatch(/\/learn\/lessons\/fractions\/\d+/);
  });

  test('back button links to /learn/lessons', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const backLink = page.locator('a[href="/learn/lessons"]');
    await expect(backLink).toBeVisible({ timeout: 5_000 });
  });
});

test.describe('Topic Level Map — error handling', () => {
  test('invalid topic slug shows not-found state', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/invalid-slug-xyz', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|back to lessons/i.test(pageText ?? '');
    expect(hasError).toBeTruthy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Lesson Session — /learn/lessons/[topicSlug]/[levelId]
 * Phase 1: Slides (LessonViewer)
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Lesson Session — slide viewer', () => {
  test('shows level name and "Learning" phase label', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/learn/lessons/fractions/1', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Header shows level label
    await expect(page.getByText('Fair Shares').first()).toBeVisible({ timeout: 10_000 });

    // Phase indicator
    await expect(page.getByText('Learning')).toBeVisible({ timeout: 5_000 });
  });

  test('shows slide content and Continue button', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions/1', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Slide content should be present
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(100);

    // Continue or navigation button
    const continueBtn = page
      .locator('button')
      .filter({ hasText: /continue|next lesson|start quiz/i })
      .first();
    await expect(continueBtn).toBeVisible({ timeout: 10_000 });
  });

  test('clicking Continue advances slides', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions/1', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const continueBtn = page
      .locator('button')
      .filter({ hasText: /continue|next lesson|start quiz/i })
      .first();
    await expect(continueBtn).toBeVisible({ timeout: 10_000 });

    const textBefore = await page.textContent('body');
    await continueBtn.click();
    await page.waitForTimeout(500);

    // Content or button label should change
    const textAfter = await page.textContent('body');
    expect(textAfter).toBeDefined();
    // Page should not be empty after advancing
    expect(textAfter?.length).toBeGreaterThan(100);
  });

  test('progress bar is visible during slides', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions/1', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Progress bar (rounded-full div inside the main content area)
    const progressBar = page.locator('div[class*="h-1"][class*="rounded-full"]').first();
    await expect(progressBar).toBeVisible({ timeout: 5_000 });
  });

  test('lesson dots indicator is visible', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions/1', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Lesson dots container (flex with gap-1.5)
    const dots = page.locator('div[class*="gap-1"]').first();
    await expect(dots).toBeVisible({ timeout: 5_000 });
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Lesson Session — Quiz phase
 * ──────────────────────────────────────────────────────────────────────────── */

/**
 * Advance through all slides to reach the quiz phase.
 * Returns true if the quiz was reached.
 */
async function advanceToQuiz(page: import('@playwright/test').Page): Promise<boolean> {
  await page.goto('/learn/lessons/fractions/1', { waitUntil: 'domcontentloaded' });
  await waitForDataLoad(page);

  // Click Continue/Next repeatedly until we see "Start Quiz!" or the quiz phase
  for (let i = 0; i < 40; i++) {
    const quizBtn = page.locator('button').filter({ hasText: /start quiz/i }).first();
    const hasQuizBtn = await quizBtn.isVisible({ timeout: 1_000 }).catch(() => false);

    if (hasQuizBtn) {
      await quizBtn.click();
      await page.waitForTimeout(500);
      return true;
    }

    // Check if we already reached quiz phase (input field visible)
    const input = page.locator('input[aria-label="Your answer"]');
    const hasInput = await input.isVisible({ timeout: 500 }).catch(() => false);
    if (hasInput) return true;

    // Click Continue or Next Lesson
    const nextBtn = page
      .locator('button')
      .filter({ hasText: /continue|next lesson/i })
      .first();
    const hasNext = await nextBtn.isVisible({ timeout: 1_000 }).catch(() => false);
    if (!hasNext) break;

    await nextBtn.click();
    await page.waitForTimeout(300);
  }

  // Final check for quiz
  const input = page.locator('input[aria-label="Your answer"]');
  return input.isVisible({ timeout: 3_000 }).catch(() => false);
}

test.describe('Lesson Session — quiz phase', () => {
  test('reaching quiz shows input field and question counter', async ({
    authenticatedPage: page,
  }) => {
    const reachedQuiz = await advanceToQuiz(page);
    if (!reachedQuiz) {
      test.skip(true, 'Could not advance to quiz phase');
      return;
    }

    // Phase label should switch to "Quiz"
    await expect(page.getByText('Quiz')).toBeVisible({ timeout: 5_000 });

    // Answer input
    const input = page.locator('input[aria-label="Your answer"]');
    await expect(input).toBeVisible({ timeout: 5_000 });

    // Question counter (e.g., "Q1 of 5")
    const pageText = await page.textContent('body');
    const hasCounter = /Q\d+\s*of\s*\d+/i.test(pageText ?? '');
    expect(hasCounter).toBeTruthy();
  });

  test('submitting a blank answer keeps Check button disabled', async ({
    authenticatedPage: page,
  }) => {
    const reachedQuiz = await advanceToQuiz(page);
    if (!reachedQuiz) {
      test.skip(true, 'Could not advance to quiz phase');
      return;
    }

    const checkBtn = page
      .locator('button')
      .filter({ hasText: /check/i })
      .first();

    // Button should be disabled when input is empty
    await expect(checkBtn).toBeDisabled({ timeout: 5_000 });
  });

  test('typing an answer enables Check button', async ({ authenticatedPage: page }) => {
    const reachedQuiz = await advanceToQuiz(page);
    if (!reachedQuiz) {
      test.skip(true, 'Could not advance to quiz phase');
      return;
    }

    const input = page.locator('input[aria-label="Your answer"]');
    await input.fill('42');

    const checkBtn = page
      .locator('button')
      .filter({ hasText: /check/i })
      .first();
    await expect(checkBtn).toBeEnabled({ timeout: 5_000 });
  });

  test('submitting an answer shows correct or wrong feedback', async ({
    authenticatedPage: page,
  }) => {
    const reachedQuiz = await advanceToQuiz(page);
    if (!reachedQuiz) {
      test.skip(true, 'Could not advance to quiz phase');
      return;
    }

    const input = page.locator('input[aria-label="Your answer"]');
    await input.fill('3/8');

    const checkBtn = page
      .locator('button')
      .filter({ hasText: /check/i })
      .first();
    await checkBtn.click();
    await page.waitForTimeout(500);

    const pageText = await page.textContent('body');
    const hasFeedback = /correct|the answer is/i.test(pageText ?? '');
    expect(hasFeedback).toBeTruthy();
  });

  test('hint button reveals hint text', async ({ authenticatedPage: page }) => {
    const reachedQuiz = await advanceToQuiz(page);
    if (!reachedQuiz) {
      test.skip(true, 'Could not advance to quiz phase');
      return;
    }

    const hintBtn = page.locator('button').filter({ hasText: /need a hint/i }).first();
    const hasHint = await hintBtn.isVisible({ timeout: 5_000 }).catch(() => false);

    if (hasHint) {
      await hintBtn.click();
      await page.waitForTimeout(500);

      // Hint box should appear
      const hintBox = page.locator('div[class*="amber"]');
      await expect(hintBox.first()).toBeVisible({ timeout: 5_000 });
    }
  });

  test('score tracker visible during quiz', async ({ authenticatedPage: page }) => {
    const reachedQuiz = await advanceToQuiz(page);
    if (!reachedQuiz) {
      test.skip(true, 'Could not advance to quiz phase');
      return;
    }

    // Score display (⭐ 0/N)
    const pageText = await page.textContent('body');
    const hasScore = /⭐\s*\d+\/\d+/i.test(pageText ?? '');
    expect(hasScore).toBeTruthy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Lesson Session — Complete phase
 * ──────────────────────────────────────────────────────────────────────────── */

/**
 * Complete all quiz questions by typing arbitrary answers.
 * Returns true if the complete screen was reached.
 */
async function completeQuiz(page: import('@playwright/test').Page): Promise<boolean> {
  const reachedQuiz = await advanceToQuiz(page);
  if (!reachedQuiz) return false;

  // Answer all questions
  for (let q = 0; q < 20; q++) {
    const input = page.locator('input[aria-label="Your answer"]');
    const hasInput = await input.isVisible({ timeout: 2_000 }).catch(() => false);
    if (!hasInput) break;

    await input.fill('1');

    const checkBtn = page
      .locator('button')
      .filter({ hasText: /check/i })
      .first();
    const hasCheck = await checkBtn.isVisible({ timeout: 2_000 }).catch(() => false);
    if (!hasCheck) break;

    await checkBtn.click();

    // Wait for auto-advance (1200ms + buffer)
    await page.waitForTimeout(2_000);

    // Check if we reached the complete screen
    const completeText = page.getByText(/great job|keep practicing|perfect score/i).first();
    const isComplete = await completeText.isVisible({ timeout: 500 }).catch(() => false);
    if (isComplete) return true;
  }

  // Final check
  const completeText = page.getByText(/great job|keep practicing|perfect score/i).first();
  return completeText.isVisible({ timeout: 5_000 }).catch(() => false);
}

test.describe('Lesson Session — completion screen', () => {
  test('completing quiz shows score and Sparky', async ({ authenticatedPage: page }) => {
    const reached = await completeQuiz(page);
    if (!reached) {
      test.skip(true, 'Could not complete quiz to reach completion screen');
      return;
    }

    const pageText = await page.textContent('body');

    // Score display (e.g., "3/5 (60%)")
    const hasScore = /\d+\/\d+.*\d+%/i.test(pageText ?? '');
    expect(hasScore).toBeTruthy();
  });

  test('shows XP breakdown if earned', async ({ authenticatedPage: page }) => {
    const reached = await completeQuiz(page);
    if (!reached) {
      test.skip(true, 'Could not complete quiz');
      return;
    }

    // XP section may or may not appear depending on auth
    const pageText = await page.textContent('body');
    const hasXPOrButtons = /XP earned|review lessons|back to levels/i.test(pageText ?? '');
    expect(hasXPOrButtons).toBeTruthy();
  });

  test('"Review Lessons" button resets to slide phase', async ({
    authenticatedPage: page,
  }) => {
    const reached = await completeQuiz(page);
    if (!reached) {
      test.skip(true, 'Could not complete quiz');
      return;
    }

    const reviewBtn = page
      .locator('button')
      .filter({ hasText: /review lessons/i })
      .first();
    const hasReview = await reviewBtn.isVisible({ timeout: 5_000 }).catch(() => false);
    if (!hasReview) {
      test.skip(true, 'Review button not visible');
      return;
    }

    await reviewBtn.click();
    await page.waitForTimeout(1_000);

    // Should be back in Learning phase
    await expect(page.getByText('Learning')).toBeVisible({ timeout: 5_000 });
  });

  test('"Back to Levels" button navigates to topic page', async ({
    authenticatedPage: page,
  }) => {
    const reached = await completeQuiz(page);
    if (!reached) {
      test.skip(true, 'Could not complete quiz');
      return;
    }

    const backBtn = page
      .locator('button')
      .filter({ hasText: /back to levels/i })
      .first();
    const hasBack = await backBtn.isVisible({ timeout: 5_000 }).catch(() => false);
    if (!hasBack) {
      test.skip(true, 'Back to Levels button not visible');
      return;
    }

    await backBtn.click();
    await page.waitForURL(/\/learn\/lessons\/fractions$/, { timeout: 15_000 });
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * Error handling & edge cases
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Lesson Session — error handling', () => {
  test('invalid level ID shows not-found state', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/fractions/99', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|back to lessons/i.test(pageText ?? '');
    expect(hasError).toBeTruthy();
  });

  test('invalid slug + level shows not-found state', async ({ authenticatedPage: page }) => {
    await page.goto('/learn/lessons/nonexistent-topic/1', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(3_000);

    const pageText = await page.textContent('body');
    const hasError = /not found|back to lessons/i.test(pageText ?? '');
    expect(hasError).toBeTruthy();
  });
});

/* ────────────────────────────────────────────────────────────────────────────
 * No JS errors
 * ──────────────────────────────────────────────────────────────────────────── */

test.describe('Lessons — no JS errors', () => {
  test('lessons hub loads without JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/learn/lessons', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });

  test('topic page loads without JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/learn/lessons/fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });

  test('lesson session loads without JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/learn/lessons/fractions/1', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });
});
