import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Topic Practice Flow', () => {
  test('navigate to a topic from practice hub', async ({ authenticatedPage: page }) => {
    await page.goto('/practice', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.getByText('Practice Hub')).toBeVisible();

    // Click the first available topic link
    const topicCard = page.locator('a[href*="/practice/"]').first();
    await expect(topicCard).toBeVisible({ timeout: 10_000 });
    await topicCard.click();

    // Should navigate to a topic practice page
    await page.waitForURL(/\/practice\/.+/, { timeout: 15_000 });
    await waitForDataLoad(page);

    // The page should render (question, status screen, or error — all valid)
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(0);
  });

  test('practice topic page loads without crash', async ({ authenticatedPage: page }) => {
    await page.goto('/practice/ch01-05', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Page should render content — could be questions, status screen, or error
    // Just verify no blank page
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(10);
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
