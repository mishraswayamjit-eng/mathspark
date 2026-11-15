import { NextResponse } from 'next/server';
import { checkRateLimit } from '@/lib/rateLimit';
import {
  DEV_COOKIE_MAX_AGE_S,
  DEV_COOKIE_NAME,
  DEV_COOKIE_PATH,
  devCookieValue,
  isDevPagesKey,
} from '@/app/(app)/dev/gate';

export const dynamic = 'force-dynamic';

// Nothing about this exchange is stored, and the address (which holds the key)
// is not passed on to the next page as a referrer.
const PRIVATE_HEADERS = { 'Cache-Control': 'private, no-store', 'Referrer-Policy': 'no-referrer' };

function notFound(): NextResponse {
  return NextResponse.json({ error: 'Not found' }, { status: 404, headers: PRIVATE_HEADERS });
}

/** Where to go after unlocking: only ever a developer page on this site. */
function destination(next: string | null, requestUrl: string): URL {
  const base = new URL(requestUrl);
  const fallback = new URL('/dev', base);
  if (!next || next.charAt(0) !== '/') return fallback;
  let target: URL;
  try {
    target = new URL(next, base);
  } catch {
    return fallback;
  }
  if (target.origin !== base.origin) return fallback;
  if (target.pathname !== '/dev' && target.pathname.indexOf('/dev/') !== 0) return fallback;
  return target;
}

/**
 * GET /api/dev/unlock?key=...&next=/dev/figures
 *
 * Opens the developer pages in this browser for a few hours. The key is
 * compared with the DEV_PAGES_KEY environment variable; when it matches, an
 * httpOnly cookie is set (holding a value derived from the key, never the key)
 * and the browser is sent on to `next`. A wrong key, or no DEV_PAGES_KEY at
 * all, is answered with "not found".
 */
export async function GET(req: Request) {
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
  if (!checkRateLimit(`dev-unlock:${ip}`, 10, 15 * 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429, headers: PRIVATE_HEADERS });
  }

  const url = new URL(req.url);
  const cookieValue = devCookieValue();
  if (!cookieValue || !isDevPagesKey(url.searchParams.get('key'))) return notFound();

  const res = NextResponse.redirect(destination(url.searchParams.get('next'), req.url), {
    status: 303,
    headers: PRIVATE_HEADERS,
  });
  res.cookies.set({
    name: DEV_COOKIE_NAME,
    value: cookieValue,
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    path: DEV_COOKIE_PATH,
    maxAge: DEV_COOKIE_MAX_AGE_S,
  });
  return res;
}
