'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';

const NAV = [
  { href: '/chapters',  emoji: '🏠', label: 'Home'    },
  { href: '/practice',  emoji: '📚', label: 'Learn'   },
  { href: '/chat',      emoji: '💬', label: 'Chat'    },
  { href: '/profile',   emoji: '👤', label: 'Profile' },
];

export default function BottomNav() {
  const pathname = usePathname();
  const router   = useRouter();

  // Hide on landing, onboarding, and admin seed screens
  if (pathname === '/' || pathname === '/start' || pathname === '/seed') return null;

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white z-50 shadow-[0_-2px_10px_rgba(0,0,0,0.08)]">
      <div className="max-w-lg mx-auto flex h-16">
        {NAV.map(({ href, emoji, label }) => {
          const active    = pathname.startsWith(href);
          const baseClass = 'flex-1 flex flex-col items-center justify-center py-2 min-h-[56px] text-xs font-bold transition-colors border-t-4';

          return (
            <Link
              key={href}
              href={href}
              onClick={href === '/practice' ? (e) => {
                if (pathname.startsWith('/practice')) return;
                e.preventDefault();
                router.push('/chapters');
              } : undefined}
              className={`${baseClass} ${
                active
                  ? 'text-[#58CC02] border-[#58CC02]'
                  : 'text-gray-400 border-transparent hover:text-gray-600'
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
