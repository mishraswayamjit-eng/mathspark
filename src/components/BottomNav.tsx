'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

const NAV = [
  { href: '/home',        emoji: '🏠', label: 'Home'     },
  { href: '/practice',    emoji: '⚡', label: 'Practice' },
  { href: '/progress',    emoji: '📊', label: 'Progress' },
  { href: '/flashcards',  emoji: '🃏', label: 'Cards'    },
  { href: '/profile',     emoji: '👤', label: 'Profile'  },
];

export default function BottomNav() {
  const pathname = usePathname();
  const [cardsDue, setCardsDue] = useState(0);

  // Read cached due count from localStorage (set by /flashcards page or /api/flashcards)
  useEffect(() => {
    try {
      const cached = localStorage.getItem('mathspark_cards_due');
      if (cached) setCardsDue(parseInt(cached, 10) || 0);
    } catch { /* ignore */ }
  }, [pathname]); // re-check on navigation

  // Hide on landing, auth, parent, student, pricing, onboarding, seed, test engine pages, and public profiles
  if (
    pathname === '/' ||
    pathname === '/start' ||
    pathname === '/seed' ||
    pathname === '/pricing' ||
    pathname.startsWith('/auth/') ||
    pathname.startsWith('/parent/') ||
    pathname.startsWith('/student/') ||
    pathname.startsWith('/profile/') ||    // public profiles (e.g. /profile/abc123)
    (pathname.startsWith('/test/') && pathname !== '/test/') ||
    pathname.startsWith('/flashcards/session')  // hide during active flashcard sessions
  ) return null;

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white z-50 shadow-[0_-2px_10px_rgba(0,0,0,0.08)] pb-[env(safe-area-inset-bottom)]">
      <div className="max-w-lg mx-auto flex h-16">
        {NAV.map(({ href, emoji, label }) => {
          const active = href === '/practice'
            ? pathname.startsWith('/practice') || pathname.startsWith('/chapters') || pathname.startsWith('/learn') || pathname.startsWith('/exam-prep')
            : href === '/progress'
            ? pathname.startsWith('/progress')
            : href === '/flashcards'
            ? pathname.startsWith('/flashcards')
            : pathname.startsWith(href);
          const baseClass = 'flex-1 flex flex-col items-center justify-center py-2 min-h-[56px] text-xs font-bold transition-colors transition-transform active:scale-95 border-t-4 relative';

          return (
            <Link
              key={href}
              href={href}
              className={`${baseClass} ${
                active
                  ? 'text-duo-green border-duo-green'
                  : 'text-gray-400 border-transparent hover:text-gray-600'
              }`}
            >
              <span className="text-xl mb-0.5 relative">
                {emoji}
                {/* Due badge on Cards tab */}
                {href === '/flashcards' && cardsDue > 0 && (
                  <span className="absolute -top-1.5 -right-3 bg-red-500 text-white text-[9px] font-bold min-w-[16px] h-4 flex items-center justify-center rounded-full px-1 leading-none">
                    {cardsDue > 99 ? '99+' : cardsDue}
                  </span>
                )}
              </span>
              <span>{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
