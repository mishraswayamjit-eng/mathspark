'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

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
      .catch((err) => console.error('[fetch]', err))
      .finally(() => setLoading(false));
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link href="/home" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white font-extrabold text-lg">Practice Hub</h1>
          <p className="text-white/70 text-xs font-medium">Choose your practice mode</p>
        </div>
        <Sparky mood="happy" size={32} />
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* Quick stats bar */}
        {!loading && stats && (
          <div className="flex gap-2">
            {[
              { emoji: '🔥', value: `${stats.streak}d`, label: 'Streak' },
              { emoji: '🎯', value: `${stats.totalSolved}`, label: 'Solved' },
              { emoji: '⭐', value: `${stats.topicsMastered}`, label: 'Mastered' },
            ].map((s) => (
              <div key={s.label} className="flex-1 bg-white rounded-xl p-2.5 border border-gray-100 shadow-sm text-center">
                <span className="text-sm">{s.emoji}</span>
                <p className="text-sm font-extrabold text-gray-800">{s.value}</p>
                <p className="text-[10px] font-bold text-gray-500 uppercase">{s.label}</p>
              </div>
            ))}
          </div>
        )}

        {/* Smart practice CTA */}
        {!loading && stats?.weakestTopicId && (
          <Link
            href={`/practice/${stats.weakestTopicId}`}
            className="block bg-gradient-to-r from-duo-dark to-[#1a3040] rounded-2xl p-4 shadow-md"
          >
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-duo-green/20 flex items-center justify-center shrink-0">
                <span className="text-2xl">⚡</span>
              </div>
              <div className="flex-1">
                <p className="text-white font-extrabold text-sm">Smart Practice</p>
                <p className="text-white/70 text-xs font-medium">
                  Continue with {stats.weakestTopicName ?? 'your weakest topic'}
                </p>
              </div>
              <span className="text-duo-green font-extrabold text-sm shrink-0">Start →</span>
            </div>
          </Link>
        )}

        {/* ── PRACTICE MODES ──────────────────────────────────────── */}

        {/* Daily Challenge */}
        <Link href="/practice/daily"
          className="block bg-gradient-to-r from-orange-50 to-yellow-50 rounded-2xl p-4 border border-orange-200 shadow-sm active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-2xl bg-orange-100 border border-orange-200 flex items-center justify-center shrink-0">
              <span className="text-3xl">🎯</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-gray-800 text-sm">Daily Challenge</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">5 questions · Build your streak!</p>
              {!loading && stats && stats.streak > 0 && (
                <div className="flex items-center gap-1 mt-1">
                  <span className="text-xs">🔥</span>
                  <span className="text-[10px] font-extrabold text-orange-600">{stats.streak} day streak</span>
                </div>
              )}
            </div>
            <span className="text-orange-500 font-extrabold text-sm shrink-0">Play →</span>
          </div>
        </Link>

        {/* Exam Papers */}
        <Link href="/practice/papers"
          className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-2xl bg-red-50 border border-red-100 flex items-center justify-center shrink-0">
              <span className="text-3xl">📝</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-gray-800 text-sm">Exam Papers</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">240 papers · 15/30/60 min formats</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-[10px] font-bold text-red-500 bg-red-50 px-1.5 py-0.5 rounded-full border border-red-100">IPM Format</span>
                <span className="text-[10px] font-bold text-gray-500">Grades 2-9</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Skill Drills */}
        <Link href="/practice/skill-drill"
          className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-2xl bg-yellow-50 border border-yellow-100 flex items-center justify-center shrink-0">
              <span className="text-3xl">🎯</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-gray-800 text-sm">Skill Drills</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">16 topics · 5 mastery levels</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-[10px] font-bold text-yellow-600 bg-yellow-50 px-1.5 py-0.5 rounded-full border border-yellow-200">10 Qs per drill</span>
                <span className="text-[10px] font-bold text-gray-500">290 sessions</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Topic Practice */}
        <Link href="/chapters"
          className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center shrink-0">
              <span className="text-3xl">📚</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-gray-800 text-sm">Topic Practice</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">Practice by chapter · 12,500+ questions</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-[10px] font-bold text-blue-500 bg-blue-50 px-1.5 py-0.5 rounded-full border border-blue-100">All Topics</span>
                <span className="text-[10px] font-bold text-gray-500">Grades 2-9</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Flashcards */}
        <Link href="/flashcards"
          className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-2xl bg-purple-50 border border-purple-100 flex items-center justify-center shrink-0">
              <span className="text-3xl">🃏</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-gray-800 text-sm">Flashcards</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">1,086 cards · Spaced repetition</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-[10px] font-bold text-purple-500 bg-purple-50 px-1.5 py-0.5 rounded-full border border-purple-100">5 game modes</span>
                <span className="text-[10px] font-bold text-gray-500">Leitner system</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* Mock Test */}
        <Link href="/test"
          className="block bg-white rounded-2xl p-4 border border-gray-100 shadow-sm active:scale-[0.98] transition-transform"
        >
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-2xl bg-green-50 border border-green-100 flex items-center justify-center shrink-0">
              <span className="text-3xl">🏆</span>
            </div>
            <div className="flex-1">
              <p className="font-extrabold text-gray-800 text-sm">Mock Test</p>
              <p className="text-xs text-gray-500 font-medium mt-0.5">Timed tests · Previous year papers</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-[10px] font-bold text-duo-green bg-green-50 px-1.5 py-0.5 rounded-full border border-green-100">Full exam</span>
                <span className="text-[10px] font-bold text-gray-500">With results</span>
              </div>
            </div>
            <span className="text-gray-500 text-sm shrink-0">→</span>
          </div>
        </Link>

        {/* ── LEARN SECTION ───────────────────────────────────────── */}
        <div className="pt-2">
          <h2 className="text-[10px] font-extrabold text-gray-500 uppercase tracking-wide mb-3">Learn & Prepare</h2>
          <div className="grid grid-cols-2 gap-2">
            {[
              { emoji: '💡', label: 'Sparky Explains',  sub: '212 solved',     href: '/learn/examples',     bg: 'from-indigo-50 to-blue-50', border: 'border-indigo-200' },
              { emoji: '🧠', label: 'Strategy Bank',    sub: '35 exam tips',   href: '/learn/strategies',   bg: 'from-amber-50 to-orange-50', border: 'border-amber-200' },
              { emoji: '📖', label: 'Math Stories',     sub: '30 stories',     href: '/learn/stories',      bg: 'from-cyan-50 to-sky-50', border: 'border-cyan-200' },
              { emoji: '🗺️', label: 'Concept Map',     sub: '88 concepts',    href: '/learn/concept-map',  bg: 'from-violet-50 to-purple-50', border: 'border-violet-200' },
              { emoji: '🚨', label: 'Mistake Patterns', sub: '50 traps',      href: '/learn/mistakes',     bg: 'from-red-50 to-orange-50', border: 'border-red-200' },
              { emoji: '🔮', label: 'IPM Predictor',    sub: '10+ years',     href: '/exam-prep/predictor', bg: 'from-green-50 to-emerald-50', border: 'border-green-200' },
            ].map((item) => (
              <Link
                key={item.label}
                href={item.href}
                className={`bg-gradient-to-br ${item.bg} rounded-2xl p-3 border ${item.border} shadow-sm active:scale-95 transition-transform`}
              >
                <span className="text-xl">{item.emoji}</span>
                <p className="font-extrabold text-gray-800 text-xs mt-1.5 leading-tight">{item.label}</p>
                <p className="text-[10px] text-gray-500 font-medium">{item.sub}</p>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
