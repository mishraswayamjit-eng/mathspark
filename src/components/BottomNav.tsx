'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const NAV = [
  { href: '/chapters',  emoji: '📚', label: 'Chapters'  },
  { href: '/practice',  emoji: '🎯', label: 'Practice'  },
  { href: '/dashboard', emoji: '📊', label: 'Dashboard' },
];

export default function BottomNav() {
  const pathname = usePathname();

  // Hide on landing, onboarding, and admin seed screens
  if (pathname === '/' || pathname === '/start' || pathname === '/seed') return null;

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50 shadow-lg">
      <div className="max-w-lg mx-auto flex">
        {NAV.map(({ href, emoji, label }) => {
          const active = pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={`flex-1 flex flex-col items-center justify-center py-2 min-h-[56px] text-xs font-semibold transition-colors ${
                active ? 'text-blue-600' : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <span className="text-xl mb-0.5">{emoji}</span>
              <span>{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
