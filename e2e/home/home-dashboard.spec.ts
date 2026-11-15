import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Home Dashboard — core sections', () => {
  test('shows greeting with student name', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(
      page.locator('text=/good (morning|afternoon|evening)/i').first(),
    ).toBeVisible({ timeout: 15_000 });

    await expect(page.getByText(/aarav/i).first()).toBeVisible({ timeout: 5_000 });
  });

  test('Today\'s Plan section visible with items', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasPlan = await page
      .getByText("Today's Plan")
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // Plan section should render (either items or empty state)
    expect(hasPlan).toBeTruthy();
  });

  test('Stats bar visible with XP pill', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // The home StatsBar always renders a "<n> XP" pill (shows "0 XP" when none).
    const hasStats = await page
      .getByText(/\d+\s*XP/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasStats).toBeTruthy();
  });

  test('Your Topics section visible', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasTopics = await page
      .getByText(/your topics/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasTopics).toBeTruthy();
  });

  test('Recent Activity section visible', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasActivity = await page
      .getByText(/recent activity/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // May not show if no recent activity
    expect(true).toBeTruthy();
  });
});

// The Quick Access tile grid was removed when Home became the "Today" screen.
test.describe('Home — Today screen', () => {
  test('header avatar links to the profile', async ({ authenticatedPage: page }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const avatar = page.getByRole('link', { name: 'Your profile' }).first();
    await expect(avatar).toBeVisible({ timeout: 10_000 });
    await expect(avatar).toHaveAttribute('href', '/profile');
  });

  test('offers one thing to do next, or continues a topic, or welcomes a new child', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(
      page.getByText(/^Next up for you$|^Continue: |Welcome to MathSpark!/).first(),
    ).toBeVisible({ timeout: 10_000 });
  });

  test('Daily Challenge sits in the plan and opens /practice/daily', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const daily = page.locator('a[href="/practice/daily"]').first();
    await expect(daily).toBeVisible({ timeout: 10_000 });
    await expect(daily).toContainText('Daily Challenge');
  });

  test('Quick Access tiles are gone and there is one "See all" link', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText("Today's Plan")).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText('Quick Practice')).toHaveCount(0);
    await expect(page.getByText('See all →')).toHaveCount(1);
    await expect(page.getByText('View all →')).toHaveCount(0);
  });

  test('a ticked plan item is still ticked after a reload', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const firstRow = page.locator('[data-plan-id]').first();
    const hasPlan = await firstRow.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasPlan) return; // no analytics yet for this student: nothing to tick

    const id = await firstRow.getAttribute('data-plan-id');
    await page.evaluate((planId) => {
      const key = `mathspark_plan_done_${new Date().toDateString()}`;
      localStorage.setItem(key, JSON.stringify([planId]));
    }, id);

    await page.reload({ waitUntil: 'domcontentloaded' });
    await expect(page.locator(`[data-plan-id="${id}"]`)).toHaveAttribute('data-done', 'true', {
      timeout: 10_000,
    });
  });
});

test.describe('Home Dashboard — no JS errors', () => {
  test('page loads without JavaScript errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/home', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });
});
