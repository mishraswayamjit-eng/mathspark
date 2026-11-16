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

/** Screens that live directly under /practice/ but are not a practice session. */
const PRACTICE_SECTIONS = ['daily', 'skill-drill', 'exam-tips', 'papers', 'tests', 'exam-papers'];

/**
 * True on a practice session screen, `/practice/<topicId>` (for example
 * `/practice/grade5` or `/practice/ch11`). False on the practice hub and on
 * the other screens under /practice/ (daily challenge, skill drills, exam
 * tips, papers, tests).
 */
export function isPracticeSessionPath(pathname: string): boolean {
  const prefix = '/practice/';
  if (pathname.indexOf(prefix) !== 0) return false;
  const parts = pathname.slice(prefix.length).split('/').filter((p) => p !== '');
  if (parts.length !== 1) return false;
  return PRACTICE_SECTIONS.indexOf(parts[0]) === -1;
}

/**
 * The bottom tab bar is hidden wherever the app chrome is, and also during a
 * practice session, which has its own back arrow. (The Sparky widget keeps
 * running there so the session's own "Ask Sparky" buttons can open the chat;
 * only its floating button is put away.)
 */
export function isBottomNavHidden(pathname: string): boolean {
  return isAppChromeHidden(pathname) || isPracticeSessionPath(pathname);
}
