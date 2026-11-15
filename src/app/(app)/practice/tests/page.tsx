'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

// Practise → Tests: one index for the test engines that already exist. It only
// links to them.

const TESTS = [
  {
    href: '/test',
    emoji: '🏆',
    label: 'Mock tests',
    sub: 'A timed test like the real exam, with no hints. Takes 20 to 60 minutes.',
  },
  {
    href: '/practice/papers',
    emoji: '📝',
    label: 'Exam papers',
    sub: 'Ready-made papers in the IPM format. Choose 15, 30 or 60 minutes.',
  },
  {
    href: '/test/history',
    emoji: '📋',
    label: 'Past results',
    sub: 'See how your earlier tests went. Takes about a minute.',
  },
];

export default function TestsIndexPage() {
  const router = useRouter();

  useEffect(() => {
    if (!localStorage.getItem('mathspark_student_id')) router.replace('/start');
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link
          href="/practice"
          className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center"
          aria-label="Back"
        >
          &larr;
        </Link>
        <h1 className="text-white text-title">Tests</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        <ul className="space-y-3">
          {TESTS.map((t) => (
            <li key={t.href}>
              <Link
                href={t.href}
                className="flex items-center gap-3 bg-white rounded-card border-2 border-line hover:border-ink px-4 py-3 min-h-[76px] transition-colors active:scale-[0.98]"
              >
                <span className="w-11 h-11 rounded-tile bg-soft border-2 border-line flex items-center justify-center text-2xl shrink-0" aria-hidden="true">
                  {t.emoji}
                </span>
                <span className="flex-1 min-w-0">
                  <span className="block font-display text-title text-ink">{t.label}</span>
                  <span className="block text-label text-ink-muted">{t.sub}</span>
                </span>
                <span className="text-2xl leading-none text-ink-muted shrink-0" aria-hidden="true">›</span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
