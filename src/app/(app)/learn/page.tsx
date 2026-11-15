'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import AvatarLink from '@/components/shell/AvatarLink';

// The Learn tab: one calm index of everything that teaches. It only links to
// the existing pages; nothing is fetched and nothing is counted here.

interface LearnCard {
  href: string;
  emoji: string;
  label: string;
  sub: string;
}

const SECTIONS: { title: string; cards: LearnCard[] }[] = [
  {
    title: 'Lessons',
    cards: [
      { href: '/learn/lessons',         emoji: '📖', label: 'Concept Lessons',  sub: 'Learn a new idea step by step' },
      { href: '/learn/hands-on',        emoji: '🖐️', label: 'Hands-on Lessons', sub: 'Colour and build the answer yourself' },
      { href: '/learn/concept-trainer', emoji: '🎯', label: 'Concept Trainer',  sub: 'Think it through in three steps' },
    ],
  },
  {
    title: 'Worked examples',
    cards: [
      { href: '/learn/examples', emoji: '💡', label: 'Solved examples', sub: 'Watch Sparky solve a question, one step at a time' },
    ],
  },
  {
    title: 'Stories',
    cards: [
      { href: '/learn/stories', emoji: '📚', label: 'Math Stories', sub: 'Maths in the real world' },
    ],
  },
  {
    title: 'Concept map',
    cards: [
      { href: '/learn/concept-map', emoji: '🗺️', label: 'Concept Map', sub: 'See how the ideas in maths join up' },
    ],
  },
];

export default function LearnIndexPage() {
  const router = useRouter();

  useEffect(() => {
    if (!localStorage.getItem('mathspark_student_id')) router.replace('/start');
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 min-h-[80px] flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <h1 className="text-white text-title">Learn</h1>
          <p className="text-white/70 text-[13px] font-semibold">Pick something new to learn</p>
        </div>
        <AvatarLink />
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-6">
        {SECTIONS.map((section) => (
          <section key={section.title}>
            <h2 className="text-heading text-ink mb-3">{section.title}</h2>
            <ul className="space-y-3">
              {section.cards.map((c) => (
                <li key={c.href}>
                  <Link
                    href={c.href}
                    className="flex items-center gap-3 bg-white rounded-card border-2 border-line hover:border-ink px-4 py-3 min-h-[76px] transition-colors active:scale-[0.98]"
                  >
                    <span className="w-11 h-11 rounded-tile bg-soft border-2 border-line flex items-center justify-center text-2xl shrink-0" aria-hidden="true">
                      {c.emoji}
                    </span>
                    <span className="flex-1 min-w-0">
                      <span className="block font-display text-title text-ink">{c.label}</span>
                      <span className="block text-label text-ink-muted">{c.sub}</span>
                    </span>
                    <span className="text-2xl leading-none text-ink-muted shrink-0" aria-hidden="true">›</span>
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}
