'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

// ── Types ─────────────────────────────────────────────────────────────────────

interface QuickStats {
  streak: number;
  todayCorrect: number;
  totalSolved: number;
  topicsMastered: number;
  weakestTopicId: string | null;
  weakestTopicName: string | null;
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function PracticeHubPage() {
  const router = useRouter();
  const [stats, setStats] = useState<QuickStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(false);

  useEffect(() => {
    const studentId = localStorage.getItem('mathspark_student_id');
    if (!studentId) { router.replace('/start'); return; }

    fetch('/api/dashboard')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        setStats({
          streak: data.stats?.streakDays ?? 0,
          todayCorrect: data.stats?.totalSolved ?? 0,
          totalSolved: data.stats?.totalSolved ?? 0,
          topicsMastered: data.stats?.topicsMastered ?? 0,
          weakestTopicId: data.weakestTopicId ?? null,
          weakestTopicName: data.weakestTopicName ?? null,
        });
      })
      .catch((err) => { logError('[fetch]', err); setFetchError(true); })
      .finally(() => setLoading(false));
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/home" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Practice Hub</h1>
          <p className="text-white/70 text-xs font-medium">Choose your practice mode</p>
        </div>
        <Sparky mood="happy" size={32} />
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* Error banner */}
        {!loading && fetchError && (
          <div className="bg-hint border-2 border-hint-ink/30 rounded-card p-3 flex items-center gap-3">
            <span className="text-sm">⚠️</span>
            <p className="text-hint-ink text-xs font-bold flex-1">Could not load stats.</p>
            <button onClick={() => window.location.reload()} className="text-action text-xs font-extrabold">Retry</button>
          </div>
        )}

        {/* Quick stats bar */}
        {!loading && stats && (
          <div className="flex gap-2">
            {[
              { emoji: '🔥', value: `${stats.streak}d`, label: 'Streak' },
              { emoji: '🎯', value: `${stats.totalSolved}`, label: 'Solved' },
              { emoji: '⭐', value: `${stats.topicsMastered}`, label: 'Mastered' },
            ].map((s) => (
              <div key={s.label} className="flex-1 bg-white rounded-tile p-2.5 border-2 border-line text-center">
                <span className="text-sm">{s.emoji}</span>
                <p className="text-sm font-extrabold text-ink">{s.value}</p>
                <p className="text-xs font-bold text-ink-muted">{s.label}</p>
              </div>
            ))}
          </div>
        )}

        {/* Smart practice CTA */}
        {!loading && stats?.weakestTopicId && (
          <Link
            href={`/practice/${stats.weakestTopicId}`}
            className="block bg-white border-2 border-ink rounded-card p-4 shadow-hard-lg"
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
                <span className="text-2xl">⚡</span>
              </div>
              <div className="flex-1">
                <p className="text-ink font-extrabold text-sm">Smart Practice</p>
                <p className="text-ink-muted text-xs font-medium">
                  Continue with {stats.weakestTopicName ?? 'your weakest topic'}
                </p>
              </div>
              <span className="text-action font-extrabold text-sm shrink-0">Start →</span>
            </div>
          </Link>
        )}

        {/* ── PRACTICE MODES ──────────────────────────────────────── */}

        {/* Daily Challenge */}
        <Link href="/practice/daily"
          className="block bg-white rounded-card p-4 border-2 border-line active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
              <span className="text-3xl">🎯</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-ink text-sm">Daily Challenge</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">5 questions · Build your streak!</p>
              {!loading && stats && stats.streak > 0 && (
                <div className="flex items-center gap-1 mt-1">
                  <span className="text-xs">🔥</span>
                  <span className="text-xs font-extrabold text-ink">{stats.streak} day streak</span>
                </div>
              )}
            </div>
            <span className="text-action font-extrabold text-sm shrink-0">Play →</span>
          </div>
        </Link>

        {/* Exam Papers */}
        <Link href="/practice/papers"
          className="block bg-white rounded-card p-4 border-2 border-line active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
              <span className="text-3xl">📝</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-ink text-sm">Exam Papers</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">240 papers · 15/30/60 min formats</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs font-bold text-ink bg-soft px-1.5 py-0.5 rounded-full border-2 border-line">IPM Format</span>
                <span className="text-xs font-bold text-ink-muted">Grades 2-9</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Skill Drills */}
        <Link href="/practice/skill-drill"
          className="block bg-white rounded-card p-4 border-2 border-line active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
              <span className="text-3xl">🎯</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-ink text-sm">Skill Drills</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">16 topics · 5 mastery levels</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs font-bold text-ink bg-soft px-1.5 py-0.5 rounded-full border-2 border-line">10 Qs per drill</span>
                <span className="text-xs font-bold text-ink-muted">290 sessions</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Topic Practice */}
        <Link href="/chapters"
          className="block bg-white rounded-card p-4 border-2 border-line active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
              <span className="text-3xl">📚</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-ink text-sm">Topic Practice</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">Practice by chapter · 12,500+ questions</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs font-bold text-ink bg-soft px-1.5 py-0.5 rounded-full border-2 border-line">All Topics</span>
                <span className="text-xs font-bold text-ink-muted">Grades 2-9</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Flashcards */}
        <Link href="/flashcards"
          className="block bg-white rounded-card p-4 border-2 border-line active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
              <span className="text-3xl">🃏</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-ink text-sm">Flashcards</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">1,086 cards · Spaced repetition</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs font-bold text-ink bg-soft px-1.5 py-0.5 rounded-full border-2 border-line">5 game modes</span>
                <span className="text-xs font-bold text-ink-muted">Leitner system</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Mock Test */}
        <Link href="/test"
          className="block bg-white rounded-card p-4 border-2 border-line active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-tile bg-soft border-2 border-line flex items-center justify-center shrink-0">
              <span className="text-3xl">🏆</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-ink text-sm">Mock Test</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">Timed tests · Previous year papers</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs font-bold text-ink bg-soft px-1.5 py-0.5 rounded-full border-2 border-line">Full exam</span>
                <span className="text-xs font-bold text-ink-muted">With results</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* ── LEARN SECTION ───────────────────────────────────────── */}
        <div className="pt-2">
          <h2 className="font-sans text-caption text-ink-muted mb-3">Learn & Prepare</h2>
          <div className="grid grid-cols-2 gap-2">
            {[
              { emoji: '💡', label: 'Sparky Explains',  sub: '212 solved',     href: '/learn/examples',     bg: 'bg-white', border: 'border-line' },
              { emoji: '📖', label: 'Concept Lessons',  sub: 'Step-by-step',   href: '/learn/lessons',      bg: 'bg-white', border: 'border-line' },
              { emoji: '🎯', label: 'Concept Trainer',  sub: 'Think in steps', href: '/learn/concept-trainer', bg: 'bg-white', border: 'border-line' },
              { emoji: '🧠', label: 'Strategy Bank',    sub: '35 exam tips',   href: '/learn/strategies',   bg: 'bg-white', border: 'border-line' },
              { emoji: '📖', label: 'Math Stories',     sub: '30 stories',     href: '/learn/stories',      bg: 'bg-white', border: 'border-line' },
              { emoji: '🗺️', label: 'Concept Map',     sub: '88 concepts',    href: '/learn/concept-map',  bg: 'bg-white', border: 'border-line' },
              { emoji: '🚨', label: 'Mistake Patterns', sub: '50 traps',      href: '/learn/mistakes',     bg: 'bg-white', border: 'border-line' },
              { emoji: '🔮', label: 'IPM Predictor',    sub: '10+ years',     href: '/exam-prep/predictor', bg: 'bg-white', border: 'border-line' },
            ].map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className={`${item.bg} rounded-card p-3 border-2 ${item.border} active:scale-95 transition-transform`}
              >
                <span className="text-xl">{item.emoji}</span>
                <p className="font-extrabold text-ink text-xs mt-1.5 leading-tight">{item.label}</p>
                <p className="text-xs text-ink-muted font-medium">{item.sub}</p>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
