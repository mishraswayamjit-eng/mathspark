'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { isAppChromeHidden } from '@/lib/navVisibility';

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
 */
function activeTab(pathname: string): TabHref | null {
  if (under(pathname, '/home')) return '/home';

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

export default function BottomNav() {
  const pathname = usePathname();

  // Hide on landing, auth, parent, student, pricing, onboarding, seed, test engine pages, and public profiles
  if (isAppChromeHidden(pathname)) return null;

  const current = activeTab(pathname);

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
