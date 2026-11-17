'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

// Home is rendered on the server, but the browser keeps a copy of it: the
// router shows that copy again on "back" (always) and on a quick return, and a
// tab left open keeps showing it. After a practice session that copy still has
// the old plan, streak and "Next up" card. This asks the server for the page
// again when an old copy is shown. It renders nothing.
//
// `token` is different for every server render. Only this device's clock is
// used to judge age, so a phone with the wrong time cannot cause a loop.

/** A copy shown again (back, or a cached return) is refreshed when older than this. */
const REMOUNT_STALE_MS = 15_000;
/** Coming back to the tab or window refreshes a copy older than this. */
const RETURN_STALE_MS = 60_000;
/** Never ask more often than this. */
const MIN_GAP_MS = 20_000;

let seenToken = '';
let seenAt = 0;
let lastRefreshAt = 0;

export default function HomeRefresher({ token }: { token: string }) {
  const router = useRouter();

  useEffect(() => {
    function refreshIfOlderThan(ms: number): void {
      const now = Date.now();
      if (now - lastRefreshAt < MIN_GAP_MS) return;
      if (now - seenAt < ms) return;
      lastRefreshAt = now;
      router.refresh();
    }

    if (seenToken !== token) {
      // A render this browser has not seen before: it is fresh.
      seenToken = token;
      seenAt = Date.now();
    } else {
      // The same render mounted again: it came from the browser's copy.
      refreshIfOlderThan(REMOUNT_STALE_MS);
    }

    function onPageShow(e: PageTransitionEvent): void {
      // Restored whole from the back/forward cache: always out of date.
      if (e.persisted) refreshIfOlderThan(0);
    }
    function onVisible(): void {
      if (document.visibilityState === 'visible') refreshIfOlderThan(RETURN_STALE_MS);
    }
    function onFocus(): void {
      refreshIfOlderThan(RETURN_STALE_MS);
    }

    window.addEventListener('pageshow', onPageShow);
    window.addEventListener('focus', onFocus);
    document.addEventListener('visibilitychange', onVisible);
    return () => {
      window.removeEventListener('pageshow', onPageShow);
      window.removeEventListener('focus', onFocus);
      document.removeEventListener('visibilitychange', onVisible);
    };
  }, [token, router]);

  return null;
}
