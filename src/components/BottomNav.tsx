'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useState } from 'react';

const NAV = [
  { href: '/chapters',  emoji: '🏠', label: 'Home'    },
  { href: '/practice',  emoji: '📚', label: 'Learn'   },
  { href: '#chat',      emoji: '💬', label: 'Chat'    },
  { href: '/dashboard', emoji: '👤', label: 'Profile' },
];

export default function BottomNav() {
  const pathname = usePathname();
  const router   = useRouter();
  const [toast, setToast] = useState(false);

  // Hide on landing, onboarding, and admin seed screens
  if (pathname === '/' || pathname === '/start' || pathname === '/seed') return null;

  function handleChatClick(e: React.MouseEvent) {
    e.preventDefault();
    setToast(true);
    setTimeout(() => setToast(false), 2500);
  }

  return (
    <>
      {toast && (
        <div className="fixed bottom-20 left-1/2 -translate-x-1/2 z-50 pointer-events-none">
          <div className="bg-gray-800 text-white rounded-full px-4 py-2 shadow-lg text-sm font-bold whitespace-nowrap animate-pop-in">
            Coming soon! 🚀
          </div>
        </div>
      )}
      <nav className="fixed bottom-0 left-0 right-0 bg-white z-50 shadow-[0_-2px_10px_rgba(0,0,0,0.08)]">
        <div className="max-w-lg mx-auto flex h-16">
          {NAV.map(({ href, emoji, label }) => {
            const isChat   = href === '#chat';
            const active   = !isChat && pathname.startsWith(href);
            const baseClass = `flex-1 flex flex-col items-center justify-center py-2 min-h-[56px] text-xs font-bold transition-colors border-t-4`;

            if (isChat) {
              return (
                <button
                  key={href}
                  onClick={handleChatClick}
                  className={`${baseClass} border-transparent text-gray-400 hover:text-gray-600 bg-transparent`}
                >
                  <span className="text-xl mb-0.5">{emoji}</span>
                  <span>{label}</span>
                </button>
              );
            }

            return (
              <Link
                key={href}
                href={href}
                onClick={href === '/practice' ? (e) => {
                  // If no topicId context, go to chapters
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
    </>
  );
}
