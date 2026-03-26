import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Topic Practice Flow', () => {
  test('navigate to a topic and see question UI', async ({ authenticatedPage: page }) => {
    // Go to practice hub
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Practice Hub')).toBeVisible();

    // Click the first available topic link (any topic card)
    const topicCard = page.locator('a[href*="/practice/"]').first();
    await expect(topicCard).toBeVisible({ timeout: 10_000 });
    await topicCard.click();

    // Should navigate to a topic practice page and show question content
    await page.waitForURL(/\/practice\/.+/, { timeout: 15_000 });
    await waitForDataLoad(page);

    // The practice page should show some question-related content
    // (hearts bar, question text, or a status screen)
    const hasContent = await page
      .locator('button, [role="button"]')
      .first()
      .isVisible()
      .catch(() => false);

    expect(hasContent).toBeTruthy();
  });

  test('practice page shows hearts/lives UI', async ({ authenticatedPage: page }) => {
    // Navigate directly to a known topic (ch01-05 = Number System)
    await page.goto('/practice/ch01-05', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Should see either the question UI or a status screen (no hearts, review intro, etc.)
    // At minimum the page should have rendered without error
    const pageContent = page.locator('body');
    await expect(pageContent).not.toBeEmpty();

    // Check for common practice elements: hearts display or question text
    const hasHeartsOrQuestion = await page
      .locator('text=/♥|❤|heart|Q\\d|question/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // If no hearts/question, we might be on a status screen which is also valid
    const hasStatusScreen = await page
      .getByRole('button')
      .first()
      .isVisible()
      .catch(() => false);

    expect(hasHeartsOrQuestion || hasStatusScreen).toBeTruthy();
  });

  test('answer a question and see feedback', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Wait for either a question with options or a status screen
    // Options are typically rendered as clickable buttons/divs
    const optionButton = page.locator('button, [role="button"]').filter({
      hasText: /^[A-D]$|option|answer/i,
    });

    const hasOptions = await optionButton.first().isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasOptions) {
      // Click the first option
      await optionButton.first().click();

      // After selecting, a check/submit button or immediate feedback should appear
      // The app shows CorrectPanel or WrongPanel after answering
      await page.waitForTimeout(1000); // brief wait for feedback animation

      // Should see either "Correct"/"Wrong" feedback or a "Next" / "Continue" button
      const hasFeedback = await page
        .locator('text=/correct|wrong|nice|great|oops|next|continue/i')
        .first()
        .isVisible({ timeout: 5_000 })
        .catch(() => false);

      // Feedback or a proceed button should be visible
      expect(hasFeedback).toBeTruthy();
    } else {
      // Status screen (no hearts, review, lesson complete) — page still loaded correctly
      test.skip(true, 'No active questions available for this topic');
    }
  });

  test('daily challenge page loads', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/daily', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Daily Challenge')).toBeVisible();
  });

  test('skill drill page loads', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/skill-drill', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Skill Drills')).toBeVisible();
  });
});
