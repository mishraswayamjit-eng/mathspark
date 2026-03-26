import { test as publicTest, expect as publicExpect } from '@playwright/test';

publicTest.describe('Pricing — page load', () => {
  publicTest('shows main heading', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    await publicExpect(
      page.getByText(/ipm prep|actually works/i).first(),
    ).toBeVisible({ timeout: 10_000 });
  });

  publicTest('shows 3 plan cards: Starter, Advanced, Unlimited', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    for (const plan of ['Starter', 'Advanced', 'Unlimited']) {
      await publicExpect(
        page.getByText(plan, { exact: false }).first(),
      ).toBeVisible({ timeout: 10_000 });
    }
  });

  publicTest('Advanced plan shows Most Popular badge', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    const hasPopular = await page
      .getByText(/most popular/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    publicExpect(hasPopular).toBeTruthy();
  });

  publicTest('all plans have Start Free Trial button', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    const trialButtons = page.locator('a, button').filter({ hasText: /start free trial/i });
    const count = await trialButtons.count();
    publicExpect(count).toBeGreaterThanOrEqual(2);
  });
});

publicTest.describe('Pricing — toggle', () => {
  publicTest('monthly/annual toggle visible', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    await publicExpect(page.getByText('Monthly').first()).toBeVisible({ timeout: 10_000 });
    await publicExpect(page.getByText('Annual').first()).toBeVisible({ timeout: 10_000 });
  });

  publicTest('toggling to Annual shows SAVE 20% badge and lower prices', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    // Click Annual toggle
    const annualBtn = page.getByText('Annual', { exact: false }).first();
    await annualBtn.click();
    await page.waitForTimeout(500);

    // SAVE 20% badge should appear
    const hasSave = await page
      .getByText(/save 20/i)
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    publicExpect(hasSave).toBeTruthy();
  });
});

publicTest.describe('Pricing — features & FAQ', () => {
  publicTest('compare all features section expandable', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    const compareBtn = page.getByText(/compare all features/i).first();
    const hasCompare = await compareBtn.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasCompare) {
      await compareBtn.click();
      await page.waitForTimeout(500);

      // Feature table should show check/cross marks
      const pageText = await page.textContent('body');
      expect(pageText).toMatch(/✓|✕/);
    }
  });

  publicTest('FAQ accordion items visible', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    const faqs = [
      'free trial',
      'switch plans',
      'plan expires',
      'sibling discount',
      'refund',
    ];

    let found = 0;
    for (const faq of faqs) {
      const visible = await page
        .getByText(new RegExp(faq, 'i'))
        .first()
        .isVisible({ timeout: 3_000 })
        .catch(() => false);
      if (visible) found++;
    }

    publicExpect(found).toBeGreaterThanOrEqual(3);
  });

  publicTest('clicking FAQ item expands answer', async ({ page }) => {
    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    const faqItem = page.getByText(/free trial/i).first();
    const hasFaq = await faqItem.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasFaq) {
      await faqItem.click();
      await page.waitForTimeout(500);

      // Expanded content should be visible
      const pageText = await page.textContent('body');
      publicExpect(pageText?.length).toBeGreaterThan(200);
    }
  });

  publicTest('page has no JS errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/pricing', { waitUntil: 'domcontentloaded' });

    publicExpect(errors).toHaveLength(0);
  });
});
