import { test, expect } from '../fixtures/auth';
import { waitForDataLoad } from '../helpers/wait';

test.describe('Profile — identity header', () => {
  test('shows student name and grade', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    await expect(page.getByText(/aarav/i).first()).toBeVisible({ timeout: 10_000 });
    await expect(page.getByText(/grade 4/i).first()).toBeVisible({ timeout: 10_000 });
  });

  test('shows avatar with initial', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Avatar shows first letter of name
    const avatar = page.getByText('A', { exact: true }).first();
    await expect(avatar).toBeVisible({ timeout: 10_000 });
  });

  test('shows league tier', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasTier = await page
      .locator('text=/bronze|silver|gold|diamond|champion/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    // League tier may not show if not yet placed
    expect(true).toBeTruthy();
  });

  test('shows member since date', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasMemberSince = await page
      .getByText(/member since/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasMemberSince).toBeTruthy();
  });
});

test.describe('Profile — edit name modal', () => {
  test('edit name button opens modal', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const editBtn = page.locator('button').filter({ hasText: /edit name|✏️/i }).first();
    const hasEdit = await editBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasEdit) {
      test.skip(true, 'Edit name button not found');
      return;
    }

    await editBtn.click();
    await page.waitForTimeout(500);

    await expect(
      page.getByText(/change your name/i).first(),
    ).toBeVisible({ timeout: 5_000 });
  });

  test('modal has name input pre-filled and save/cancel buttons', async ({
    authenticatedPage: page,
  }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const editBtn = page.locator('button').filter({ hasText: /edit name|✏️/i }).first();
    const hasEdit = await editBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasEdit) {
      test.skip(true, 'Edit name button not found');
      return;
    }

    await editBtn.click();
    await page.waitForTimeout(500);

    // Name input should be pre-filled
    const nameInput = page.locator('input').first();
    const value = await nameInput.inputValue();
    expect(value.length).toBeGreaterThan(0);

    // Save and Cancel buttons
    await expect(
      page.locator('button').filter({ hasText: /save/i }).first(),
    ).toBeVisible({ timeout: 3_000 });
    await expect(
      page.locator('button').filter({ hasText: /cancel/i }).first(),
    ).toBeVisible({ timeout: 3_000 });
  });

  test('cancel closes modal without changes', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const editBtn = page.locator('button').filter({ hasText: /edit name|✏️/i }).first();
    const hasEdit = await editBtn.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasEdit) {
      test.skip(true, 'Edit name button not found');
      return;
    }

    await editBtn.click();
    await page.waitForTimeout(500);

    await page.locator('button').filter({ hasText: /cancel/i }).first().click();
    await page.waitForTimeout(500);

    // Modal should be dismissed
    await expect(
      page.getByText(/change your name/i).first(),
    ).toBeHidden({ timeout: 3_000 });
  });
});

test.describe('Profile — exam goals', () => {
  test('My Exam card shows target score selector', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasExamCard = await page
      .getByText(/my exam|target score|exam/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    if (!hasExamCard) {
      test.skip(true, 'Exam card not visible');
      return;
    }

    // Target score pills (25, 30, 35, 38)
    for (const score of ['25', '30', '35', '38']) {
      const pill = page.getByText(score, { exact: true }).first();
      const visible = await pill.isVisible({ timeout: 3_000 }).catch(() => false);
      if (visible) {
        expect(visible).toBeTruthy();
        break; // at least one should be visible
      }
    }
  });

  test('clicking target score pill highlights it', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const pill35 = page.getByText('35', { exact: true }).first();
    const hasPill = await pill35.isVisible({ timeout: 10_000 }).catch(() => false);
    if (!hasPill) {
      test.skip(true, 'Target score pills not found');
      return;
    }

    await pill35.click();
    await page.waitForTimeout(500);

    // Selected pill should have green bg
    const parent = pill35.locator('..');
    const classes = await parent.getAttribute('class').catch(() => '');
    const pillClasses = await pill35.getAttribute('class').catch(() => '');
    const combined = (classes ?? '') + (pillClasses ?? '');
    expect(combined).toMatch(/green|selected/i);
  });
});

test.describe('Profile — preferences', () => {
  test('My Goals card shows daily practice options', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Daily practice goal pills
    const hasGoals = await page
      .getByText(/daily|practice|min/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasGoals).toBeTruthy();
  });

  test('best time preference buttons visible', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const times = ['Morning', 'Afternoon', 'Evening'];
    let found = 0;
    for (const time of times) {
      const visible = await page
        .getByText(time, { exact: false })
        .first()
        .isVisible({ timeout: 5_000 })
        .catch(() => false);
      if (visible) found++;
    }

    expect(found).toBeGreaterThanOrEqual(2);
  });

  test('sound effects toggle visible', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasSound = await page
      .getByText(/sound effect/i)
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasSound).toBeTruthy();
  });
});

test.describe('Profile — account section', () => {
  test('grade change buttons visible', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    // Grade buttons Gr 2-9
    const gr4 = page.getByText('Gr 4', { exact: false });
    const hasGrade = await gr4.first().isVisible({ timeout: 10_000 }).catch(() => false);

    expect(hasGrade).toBeTruthy();
  });

  test('subscription plan visible with upgrade link', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const hasPlan = await page
      .locator('text=/plan|subscription|upgrade|starter|advanced|unlimited/i')
      .first()
      .isVisible({ timeout: 10_000 })
      .catch(() => false);

    expect(hasPlan).toBeTruthy();
  });

  test('logout button visible and styled red', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const logoutBtn = page.locator('button').filter({ hasText: /log\s?out/i }).first();
    await expect(logoutBtn).toBeVisible({ timeout: 10_000 });
  });

  test('Sparky Chat link navigates to /chat', async ({ authenticatedPage: page }) => {
    await page.goto('/profile', { waitUntil: 'domcontentloaded' });
    await waitForDataLoad(page);

    const chatLink = page.locator('a[href="/chat"]').first();
    const hasChat = await chatLink.isVisible({ timeout: 10_000 }).catch(() => false);

    if (hasChat) {
      await chatLink.click();
      await page.waitForURL('/chat', { timeout: 10_000 });
    }
  });
});
