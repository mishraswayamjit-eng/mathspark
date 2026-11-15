// SERVER ONLY: reads DEV_PAGES_KEY and uses Node's crypto. Never import this
// from a client component.
//
// The gate for the developer pages (/dev, /dev/figures, /dev/voice, /dev/teach)
// on a production build. The key lives only in the DEV_PAGES_KEY environment
// variable. /api/dev/unlock checks a key given in the link and sets a cookie;
// the /dev layout checks that cookie. The cookie never holds the key itself,
// only a value derived from it, so changing the key closes every open browser.

import crypto from 'crypto';

export const DEV_COOKIE_NAME = 'ms_dev_pages';
/** The cookie only goes to the developer pages. */
export const DEV_COOKIE_PATH = '/dev';
/** How long an unlocked browser stays unlocked: 4 hours. */
export const DEV_COOKIE_MAX_AGE_S = 4 * 60 * 60;

/** Fixed label mixed into the derived value. Not a secret. */
const DERIVE_LABEL = 'mathspark-dev-pages-v1';

function configuredKey(): string {
  return process.env.DEV_PAGES_KEY ?? '';
}

/** HMAC-SHA-256 of the fixed label, keyed with the given key: 64 hex characters. */
function derive(key: string): string {
  return crypto.createHmac('sha256', key).update(DERIVE_LABEL).digest('hex');
}

/** Constant-time comparison of two strings. */
function safeEqual(a: string, b: string): boolean {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) return false;
  return crypto.timingSafeEqual(bufA, bufB);
}

/** False when DEV_PAGES_KEY is not set: the pages are then closed in production. */
export function devPagesConfigured(): boolean {
  return configuredKey() !== '';
}

/**
 * Is this the key in DEV_PAGES_KEY? Both sides are derived first, so the
 * comparison is constant-time and always over the same length.
 */
export function isDevPagesKey(provided: string | null | undefined): boolean {
  const expected = configuredKey();
  if (!provided || !expected) return false;
  return safeEqual(derive(provided), derive(expected));
}

/** The value the unlock cookie holds, or null when no key is configured. */
export function devCookieValue(): string | null {
  const expected = configuredKey();
  return expected ? derive(expected) : null;
}

/** Does this cookie value unlock the pages? */
export function isDevCookieValid(value: string | null | undefined): boolean {
  const expected = devCookieValue();
  if (!value || !expected) return false;
  return safeEqual(value, expected);
}
