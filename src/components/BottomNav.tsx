'use client';

import { Suspense } from 'react';
import Link from 'next/link';
import { usePathname, useSearchParams } from 'next/navigation';
import { isBottomNavHidden, isTopicPagePath } from '@/lib/navVisibility';

type TabHref = '/home' | '/learn' | '/practice' | '/progress';

const NAV: { href: TabHref; emoji: string; label: string }[] = [
  { href: '/home',     emoji: '🏠', label: 'Today'    },
  { href: '/learn',    emoji: '📖', label: 'Learn'    },
  { href: '/practice', emoji: '⚡', label: 'Practise' },
  { href: '/progress', emoji: '📊', label: 'Progress' },
];

/** True when `pathname` is `base` itself or anything beneath it. */
function under(pathname: string, base: string): boolean {
  return pathname === base || pathname.startsWith(base + '/');
}

/**
 * Which tab a route belongs to. Routes with no tab (Sparky chat, homework
 * helper) return null, so no tab is lit.
 *
 * `from` is the page's `?from=` hint. Only a topic page reads it: a topic
 * opened from the Learn tab keeps Learn lit; otherwise Practise is.
 */
function activeTab(pathname: string, from: string | null): TabHref | null {
  if (under(pathname, '/home')) return '/home';

  if (isTopicPagePath(pathname)) return from === 'learn' ? '/learn' : '/practice';

  // Strategy Bank and Mistake Patterns live under /learn in the URL, but they
  // are reached from Practise → Exam tips and their back arrows return there.
  if (under(pathname, '/learn/strategies') || under(pathname, '/learn/mistakes')) return '/practice';
  if (under(pathname, '/learn')) return '/learn';

  if (
    under(pathname, '/practice') ||
    under(pathname, '/chapters') ||
    under(pathname, '/flashcards') ||
    under(pathname, '/test') ||
    under(pathname, '/exam-prep')
  ) return '/practice';

  if (
    under(pathname, '/progress') ||
    under(pathname, '/leaderboard') ||
    under(pathname, '/profile')
  ) return '/progress';

  return null;
}

function NavBar({ from }: { from: string | null }) {
  const pathname = usePathname();

  // Hide on landing, auth, parent, student, pricing, onboarding, seed, test engine pages,
  // public profiles, and during a practice session (/practice/<topicId>)
  if (isBottomNavHidden(pathname)) return null;

  const current = activeTab(pathname, from);

  return (
    <nav aria-label="Main" className="fixed bottom-0 left-0 right-0 bg-white z-50 border-t-2 border-ink pb-[env(safe-area-inset-bottom)]">
      <div className="max-w-lg mx-auto flex h-16">
        {NAV.map(({ href, emoji, label }) => {
          const active = current === href;
          const baseClass = 'flex-1 flex flex-col items-center justify-center py-2 min-h-[56px] text-[13px] font-bold transition-colors transition-transform active:scale-95 border-t-4 relative';

          return (
            <Link
              key={href}
              href={href}
              aria-current={active ? 'page' : undefined}
              className={`${baseClass} ${
                active
                  ? 'text-action border-action font-extrabold'
                  : 'text-gray-500 border-transparent hover:text-ink'
              }`}
            >
              <span className="text-xl mb-0.5" aria-hidden="true">{emoji}</span>
              <span>{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

/** Reads the `?from=` hint. Kept apart so only this part waits on the query string. */
function NavBarWithOrigin() {
  const searchParams = useSearchParams();
  return <NavBar from={searchParams.get('from')} />;
}

export default function BottomNav() {
  // If the query string is not available yet, the bar still shows (Practise is
  // lit on a topic page until the hint is known).
  return (
    <Suspense fallback={<NavBar from={null} />}>
      <NavBarWithOrigin />
    </Suspense>
  );
}
