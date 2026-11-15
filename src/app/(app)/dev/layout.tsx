import { cookies } from 'next/headers';
import { notFound } from 'next/navigation';
import { DEV_COOKIE_NAME, isDevCookieValid } from './gate';

// Server component: the gate runs on the server, so nothing about the key is
// ever sent to the browser.
//
// On a production build the developer pages are "not found" unless this
// browser holds the unlock cookie, which GET /api/dev/unlock sets when it is
// given the key from the DEV_PAGES_KEY environment variable:
//   /api/dev/unlock?key=<DEV_PAGES_KEY>&next=/dev
// With DEV_PAGES_KEY unset, no cookie can match and the pages stay closed.
// Outside production (local development) everything is let through.

// Read the cookie on every request; never prerender these pages.
export const dynamic = 'force-dynamic';

export default function DevLayout({ children }: { children: React.ReactNode }) {
  if (process.env.NODE_ENV === 'production') {
    const cookie = cookies().get(DEV_COOKIE_NAME);
    if (!isDevCookieValid(cookie ? cookie.value : null)) notFound();
  }

  return <>{children}</>;
}
