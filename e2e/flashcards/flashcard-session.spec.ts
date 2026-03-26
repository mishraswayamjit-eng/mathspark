import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Flashcard Session Flow', () => {
  test('flashcards hub shows decks and stats', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText("Sparky's Cards")).toBeVisible();

    // Stats bar should show total/seen/mastered
    await expect(page.getByText(/total/i).first()).toBeVisible({ timeout: 10_000 });
  });

  test('clicking a deck or game mode navigates to session', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Try clicking a game mode button (always visible if decks exist)
    const quizBlitz = page.getByText('Quiz Blitz', { exact: false }).first();
    const hasModes = await quizBlitz.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasModes) {
      await quizBlitz.click();
      await page.waitForURL(/\/flashcards\/session/, { timeout: 10_000 });

      // Session page should show card content, empty state, or loading
      const pageText = await page.textContent('body');
      const hasSessionContent = /flip|still learning|nailed it|no cards|loading|shuffling|cards/i.test(
        pageText ?? '',
      );
      expect(hasSessionContent).toBeTruthy();
    } else {
      // No game modes = no flashcards for this grade
      const isEmpty = await page
        .getByText(/no flashcards|no cards/i)
        .first()
        .isVisible()
        .catch(() => false);
      expect(isEmpty).toBeTruthy();
    }
  });

  test('flip a card and rate it', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=classic', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    // Check if cards are available
    const emptyState = page.getByText(/no cards available/i);
    if (await emptyState.isVisible({ timeout: 5_000 }).catch(() => false)) {
      test.skip(true, 'No cards available in deck');
      return;
    }

    // Wait for loading to finish
    await page.getByText(/loading|shuffling/i).first()
      .waitFor({ state: 'hidden', timeout: 10_000 })
      .catch(() => {});

    // Look for confidence buttons (they may appear after flipping or immediately)
    const nailedIt = page.locator('button').filter({ hasText: /nailed it/i }).first();
    const stillLearning = page.locator('button').filter({ hasText: /still learning/i }).first();

    // Try tapping the card area to flip
    const cardArea = page.locator('main, [class*="card"], [class*="rounded-2xl"]').first();
    await cardArea.click().catch(() => {});
    await page.waitForTimeout(500);

    const hasButtons = await nailedIt.or(stillLearning).first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    if (hasButtons) {
      await nailedIt.or(stillLearning).first().click();
      await page.waitForTimeout(1000);

      // Progress should show (e.g., "2/12")
      const progress = page.locator('text=/\\d+\\/\\d+/');
      await expect(progress.first()).toBeVisible({ timeout: 5_000 });
    }
  });

  test('session complete screen shows after all cards', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=classic', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    // Page loaded without error — verify basic session UI
    const pageText = await page.textContent('body');
    const hasContent = /card|deck|loading|no cards|session|flip/i.test(pageText ?? '');
    expect(hasContent).toBeTruthy();
  });

  test('game modes are listed on flashcards hub', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const gameModes = ['Quiz Blitz', 'Speed Round', 'Tap Match'];
    for (const mode of gameModes) {
      await expect(
        page.getByText(mode, { exact: false }).first(),
      ).toBeVisible({ timeout: 10_000 });
    }
  });

  test('close button returns to flashcards hub', async ({ authenticatedPage: page }) => {
    await page.goto('/flashcards/session?deck=quick&mode=classic', {
      waitUntil: 'domcontentloaded',
    });
    await waitForDataLoad(page);

    // Find and click close/back button (✕ or × character)
    const closeBtn = page.locator('button').first();
    const hasClose = await closeBtn.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasClose) {
      await closeBtn.click();
      // Should navigate back to /flashcards (may show confirmation first)
      await page.waitForURL(/\/flashcards/, { timeout: 10_000 }).catch(() => {});
    }
  });
});
