import type { Page } from '@playwright/test';

/**
 * Wait for skeleton loaders / loading spinners to disappear,
 * indicating the page has finished its initial data fetch.
 */
export async function waitForDataLoad(page: Page, timeout = 15_000): Promise<void> {
  // The app uses animate-pulse skeletons and "Loading..." text
  await Promise.all([
    page
      .locator('[class*="animate-pulse"]')
      .first()
      .waitFor({ state: 'hidden', timeout })
      .catch(() => { /* no skeleton on this page */ }),
    page
      .getByText('Loading...', { exact: false })
      .first()
      .waitFor({ state: 'hidden', timeout })
      .catch(() => { /* no loading text */ }),
  ]);
}

/** Wait for Next.js client hydration. */
export async function waitForHydration(page: Page): Promise<void> {
  await page.waitForFunction(() => {
    return document.querySelector('#__next') !== null
      || document.querySelector('[data-nextjs-scroll-focus-boundary]') !== null
      || document.readyState === 'complete';
  }, { timeout: 10_000 });
}
