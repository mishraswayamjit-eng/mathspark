/**
 * Shared predicate for hiding app chrome (bottom nav, floating widgets) on
 * screens where it would get in the way — landing, auth, onboarding, parent /
 * student portals, pricing, public profiles, and active test / exam / flashcard
 * engine routes.
 *
 * Lifted verbatim from the original BottomNav predicate so both the nav and the
 * Sparky widget hide on exactly the same set of routes (single source of truth).
 */
export function isAppChromeHidden(pathname: string): boolean {
  return (
    pathname === '/' ||
    pathname === '/start' ||
    pathname === '/seed' ||
    pathname === '/pricing' ||
    pathname.startsWith('/auth/') ||
    pathname.startsWith('/parent/') ||
    pathname.startsWith('/student/') ||
    pathname.startsWith('/profile/') ||    // public profiles (e.g. /profile/abc123)
    (pathname.startsWith('/test/') && pathname !== '/test/') ||
    pathname.startsWith('/practice/papers/') ||  // hide during practice paper exams
    pathname.startsWith('/flashcards/session')   // hide during active flashcard sessions
  );
}
