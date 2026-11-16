import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

/**
 * Topic page — /topic/[nodeId]
 * One page per topic: Practise first, then whatever else exists for the topic.
 */
test.describe('Topic page — /topic/gr5_fractions', () => {
  test('shows the topic name and leads with Practise', async ({ authenticatedPage: page }) => {
    await page.goto('/topic/gr5_fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByRole('heading', { level: 1, name: 'Fractions' })).toBeVisible({
      timeout: 15_000,
    });

    // Practise is the first section and says what the practice is
    const firstHeading = page.locator('h2').first();
    await expect(firstHeading).toHaveText('Practise');
    await expect(page.getByText(/warm-up → build → challenge → real exam questions/i)).toBeVisible();

    // It goes to practice on this topic only (the sub-topic is in the link)
    const practise = page.locator('[data-testid="topic-practise"]');
    await expect(practise).toBeVisible();
    await expect(practise).toHaveAttribute('href', /^\/practice\/grade5\?subTopic=fraction/);
  });

  test('lists the lesson, drill, tricks, stories and solved examples for the topic', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/topic/gr5_fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    for (const title of ['Learn it', 'Drill', 'Tricks', 'Stories', 'Solved examples']) {
      await expect(page.getByRole('heading', { level: 2, name: title, exact: true })).toBeVisible({
        timeout: 10_000,
      });
    }

    await expect(page.locator('a[href="/learn/lessons/fractions"]')).toBeVisible();
    await expect(page.locator('a[href^="/learn/hands-on/"]').first()).toBeVisible();
    await expect(page.locator('a[href="/learn/concept-trainer/fractions-g5"]')).toBeVisible();
    await expect(page.locator('a[href^="/practice/skill-drill/fractions_decimals/"]')).toBeVisible();
    await expect(page.locator('a[href^="/learn/strategies?open="]').first()).toBeVisible();
  });

  test('a gap is simply absent: no Flashcards section when no deck is mapped', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/topic/gr5_fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.locator('[data-testid="topic-practise"]')).toBeVisible({ timeout: 15_000 });
    await expect(page.locator('[data-testid="topic-section-flashcards"]')).toHaveCount(0);
  });

  test('the bottom nav is shown', async ({ authenticatedPage: page }) => {
    await page.goto('/topic/gr5_fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(
      page.locator('nav[aria-label="Main"]').getByText('Today', { exact: true }),
    ).toBeVisible({ timeout: 10_000 });
  });

  test('back arrow returns to By topic, or to Learn when opened from Learn', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/topic/gr5_fractions', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('a[aria-label="Back"]')).toHaveAttribute('href', '/chapters');

    await page.goto('/topic/gr5_fractions?from=learn', { waitUntil: 'domcontentloaded' });
    await expect(page.locator('a[aria-label="Back"]')).toHaveAttribute('href', '/learn');
  });
});

test.describe('Topic page — other topics', () => {
  test('a topic with a flashcard deck shows Flashcards', async ({ authenticatedPage: page }) => {
    await page.goto('/topic/gr5_percentage', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.locator('[data-testid="topic-section-flashcards"]')).toBeVisible({
      timeout: 15_000,
    });
    await expect(
      page.locator('a[href^="/flashcards/session?deck=pct"]'),
    ).toBeVisible();
  });

  test('a Grade 4 chapter topic still leads with Practise', async ({ authenticatedPage: page }) => {
    await page.goto('/topic/gr4_fractions', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const practise = page.locator('[data-testid="topic-practise"]');
    await expect(practise).toBeVisible({ timeout: 15_000 });
    await expect(practise).toHaveAttribute('href', '/practice/ch07-08');
  });

  test('an unknown topic shows a friendly message and a way back', async ({
    authenticatedPage: page,
  }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/topic/not-a-real-topic', { waitUntil: 'domcontentloaded' });

    await expect(page.getByText(/couldn.t find that topic/i)).toBeVisible({ timeout: 15_000 });
    await expect(page.getByRole('link', { name: 'See all topics' })).toHaveAttribute('href', '/chapters');
    expect(errors).toHaveLength(0);
  });
});
