'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import AvatarLink from '@/components/shell/AvatarLink';
import { logError } from '@/lib/logger';

// ── Types ─────────────────────────────────────────────────────────────────────

/** The part of the /api/dashboard response this page reads. */
interface DashboardSlice {
  weakestTopicId?: string | null;
  weakestTopicName?: string | null;
  /** Optional: where "Smart Practice" should go. Falls back to /practice/<weakestTopicId>. */
  weakestTopicHref?: string;
  /** Optional: the topic name to show. Falls back to weakestTopicName. */
  weakestTopicLabel?: string;
}

interface SmartPick {
  href: string;
  label: string | null;
}

// ── The five ways to practise ─────────────────────────────────────────────────

const CHOICES = [
  { href: '/chapters',             emoji: '📚', label: 'By topic',     sub: 'Choose a chapter' },
  { href: '/practice/skill-drill', emoji: '🎯', label: 'Skill Drills', sub: 'One skill at a time' },
  { href: '/flashcards',           emoji: '🃏', label: 'Flashcards',   sub: 'Quick cards to remember' },
  { href: '/practice/tests',       emoji: '📝', label: 'Tests',        sub: 'Mock tests and papers' },
  { href: '/practice/exam-tips',   emoji: '🧠', label: 'Exam tips',    sub: 'Tricks and traps' },
];

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PracticeHubPage() {
  const router = useRouter();
  const [smart, setSmart] = useState<SmartPick | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    fetch('/api/dashboard')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data: DashboardSlice) => {
        const href = data.weakestTopicHref
          || (data.weakestTopicId ? `/practice/${data.weakestTopicId}` : null);
        if (href) {
          setSmart({ href, label: data.weakestTopicLabel || data.weakestTopicName || null });
        }
      })
      // If this does not load, the card below simply offers "pick a topic".
      .catch((err) => { logError('[practice] fetch dashboard', err); })
      .finally(() => setLoading(false));
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  // The personal card links to the suggested topic, or to the chapter list when
  // there is no suggestion.
  const cardHref = smart ? smart.href : '/chapters';
  const cardTitle = smart ? 'Smart Practice' : 'Start practising';
  const cardSub = smart
    ? `Continue with ${smart.label ?? 'a topic picked for you'}`
    : 'Pick a topic to begin';

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 min-h-[80px] flex items-center gap-3">
        <div className="flex-1 min-w-0">
          <h1 className="text-white text-title">Practise</h1>
          <p className="text-white/70 text-[13px] font-semibold">Pick how you want to practise</p>
        </div>
        <AvatarLink />
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">

        {/* Personal card. The slot is 88px tall before and after the data
            arrives, so the list below never moves. */}
        <div className="h-[88px] mb-6">
          {loading ? (
            <div className="h-full bg-white rounded-card border-2 border-line animate-pulse" />
          ) : (
            <Link
              href={cardHref}
              className="h-full flex items-center gap-3 bg-white border-2 border-ink rounded-card px-4 shadow-hard-lg"
            >
              <span className="w-12 h-12 rounded-tile bg-soft border-2 border-line flex items-center justify-center text-2xl shrink-0" aria-hidden="true">
                ⚡
              </span>
              <span className="flex-1 min-w-0">
                <span className="block font-display text-title text-ink truncate">{cardTitle}</span>
                <span className="block text-label text-ink-muted truncate">{cardSub}</span>
              </span>
              <span className="text-label font-extrabold text-action shrink-0">Start →</span>
            </Link>
          )}
        </div>

        {/* ── The five choices ────────────────────────────────────── */}
        <ul className="space-y-3">
          {CHOICES.map((c) => (
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

        {/* Daily Challenge is featured on Today; this keeps it one tap away. */}
        <Link
          href="/practice/daily"
          className="mt-5 flex items-center gap-2 min-h-[48px] px-4 bg-soft rounded-control border-2 border-line hover:border-ink transition-colors"
        >
          <span aria-hidden="true">🎯</span>
          <span className="flex-1 text-label text-ink">Daily Challenge</span>
          <span className="text-label font-extrabold text-action">Play →</span>
        </Link>
      </div>
    </div>
  );
}
