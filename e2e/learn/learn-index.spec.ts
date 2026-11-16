import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/**
 * Learn tab — /learn
 * Leads with the same topic list as Practise → By topic; browsing by kind of
 * content stays below as "More ways to learn".
 */
test.describe('Learn tab — /learn', () => {
  test('leads with the topic list', async ({ authenticatedPage: page }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText(/pick something new to learn/i).first()).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByRole('heading', { name: 'Exam topics' })).toBeVisible({ timeout: 10_000 });

    // Each topic opens its topic page, remembering that it was opened from Learn
    const topicLinks = page.locator('a[href^="/topic/"]');
    expect(await topicLinks.count()).toBeGreaterThan(0);
    await expect(topicLinks.first()).toHaveAttribute('href', /\?from=learn$/);
  });

  test('shows the same topics as Practise → By topic', async ({ authenticatedPage: page }) => {
    const topicIds = async (): Promise<string[]> => {
      const hrefs = await page
        .locator('a[href^="/topic/"]')
        .evaluateAll((els) => els.map((el) => el.getAttribute('href') || ''));
      return hrefs.map((h) => h.split('?')[0]);
    };

    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.locator('a[href^="/topic/"]').first()).toBeVisible({ timeout: 15_000 });
    const onLearn = await topicIds();

    await page.goto('/chapters', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);
    await expect(page.locator('a[href^="/topic/"]').first()).toBeVisible({ timeout: 15_000 });
    const onPractise = await topicIds();

    expect(onLearn.length).toBeGreaterThan(0);
    expect(onLearn).toEqual(onPractise);
  });

  test('tapping a topic opens its page with the Learn tab still lit', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await page.locator('a[href^="/topic/"]').first().click();
    await page.waitForURL(/\/topic\/[a-z0-9_]+\?from=learn/, { timeout: 15_000 });

    await expect(page.locator('[data-testid="topic-practise"]')).toBeVisible({ timeout: 10_000 });
    await expect(
      page.locator('nav[aria-label="Main"] a[href="/learn"]'),
    ).toHaveAttribute('aria-current', 'page');
  });

  test('keeps the browse-by-type links under "More ways to learn"', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/learn', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByRole('heading', { name: 'More ways to learn' })).toBeVisible({
      timeout: 10_000,
    });
    for (const href of [
      '/learn/lessons',
      '/learn/hands-on',
      '/learn/concept-trainer',
      '/learn/examples',
      '/learn/stories',
      '/learn/concept-map',
    ]) {
      await expect(page.locator(`main a[href="${href}"]`)).toBeVisible();
    }
  });
});
