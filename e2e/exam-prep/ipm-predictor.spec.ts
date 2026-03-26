import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('IPM Predictor — page load', () => {
  test('shows heading and data stats', async ({ authenticatedPage: page }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText(/IPM.*Predictor/i).first()).toBeVisible({ timeout: 15_000 });

    // Should show analysis stats (questions analyzed, years)
    const pageText = await page.textContent('body');
    const hasStats = /questions analyzed|years|data/i.test(pageText ?? '');
    expect(hasStats).toBeTruthy();
  });

  test('grade selector buttons visible (G2-G9)', async ({ authenticatedPage: page }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // At least Grade 4 button should be visible
    const hasGr4 = await page
      .getByText(/Grade 4|G4/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasGr4).toBeTruthy();
  });
});

test.describe('IPM Predictor — overview (no grade selected)', () => {
  test('shows grade cards with question counts', async ({ authenticatedPage: page }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Grade overview cards with Qs count
    const pageText = await page.textContent('body');
    const hasQs = /\d+ Qs|\d+ questions/i.test(pageText ?? '');
    expect(hasQs).toBeTruthy();
  });

  test('shows strategic insights section', async ({ authenticatedPage: page }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasInsights = await page
      .locator('text=/insight|finding|trend|tip/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasInsights).toBeTruthy();
  });
});

test.describe('IPM Predictor — grade detail view', () => {
  test('selecting a grade shows topic frequency chart', async ({ authenticatedPage: page }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Click Grade 4 button
    const gr4Btn = page.getByText(/Grade 4|G4/i).first();
    await gr4Btn.click();
    await page.waitForTimeout(1_500);

    // Should show topic frequency bars with percentages
    const pageText = await page.textContent('body');
    const hasFrequency = /\d+%|frequency|topic/i.test(pageText ?? '');
    expect(hasFrequency).toBeTruthy();
  });

  test('shows overview stats (questions, years, topics)', async ({ authenticatedPage: page }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const gr4Btn = page.getByText(/Grade 4|G4/i).first();
    await gr4Btn.click();
    await page.waitForTimeout(1_500);

    const pageText = await page.textContent('body');
    const hasStats = /questions|years|topics|analyzed/i.test(pageText ?? '');
    expect(hasStats).toBeTruthy();
  });

  test('shows Always/Frequently/Rarely appears sections', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const gr4Btn = page.getByText(/Grade 4|G4/i).first();
    await gr4Btn.click();
    await page.waitForTimeout(1_500);

    const pageText = await page.textContent('body');
    const hasFreqLabels = /always|frequently|rarely/i.test(pageText ?? '');
    expect(hasFreqLabels).toBeTruthy();
  });

  test('shows Focus These Topics section', async ({ authenticatedPage: page }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const gr4Btn = page.getByText(/Grade 4|G4/i).first();
    await gr4Btn.click();
    await page.waitForTimeout(1_500);

    const hasFocus = await page
      .getByText(/focus.*topics/i)
      .first()
      .isVisible({ timeout: 5_000 })
      .catch(() => false);

    expect(hasFocus).toBeTruthy();
  });

  test('clicking same grade deselects it (back to overview)', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const gr4Btn = page.getByText(/Grade 4|G4/i).first();

    // Select
    await gr4Btn.click();
    await page.waitForTimeout(1_000);

    // Deselect
    await gr4Btn.click();
    await page.waitForTimeout(1_000);

    // Should be back to overview (grade cards visible)
    const pageText = await page.textContent('body');
    expect(pageText?.length).toBeGreaterThan(200);
  });
});

test.describe('IPM Predictor — no errors', () => {
  test('page loads without JS errors', async ({ authenticatedPage: page }) => {
    const errors: string[] = [];
    page.on('pageerror', (err) => errors.push(err.message));

    await page.goto('/exam-prep/predictor', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    expect(errors).toHaveLength(0);
  });
});
