'use client';

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import type {
  TopicMasteryEntry,
  ExamReadinessResult,
  TopicPriority,
  DailyPlanItem,
  Nudge,
} from '@/lib/brain/engine';

// ── Types ─────────────────────────────────────────────────────────────────────

interface HomeStudent {
  id: string;
  name: string;
  grade: number;
  avatarColor: string;
  trialExpiresAt: string | null;
  trialDaysLeft: number | null;
  trialActive: boolean;
  subscriptionTier: number;
  subscriptionName: string | null;
  examDate: string | null;
  examName: string | null;
  dailyGoalMins: number;
}

interface HomeData {
  student: HomeStudent;
  streak: number;
  todayCorrect: number;
  topicMastery: TopicMasteryEntry[];
  examReadiness: ExamReadinessResult;
  topicPriorities: TopicPriority[];
  dailyPlan: DailyPlanItem[];
  nudges: Nudge[];
  recentActivity: Array<{
    topicId: string; topicName: string;
    correct: number; attempted: number; pct: number; timeAgo: string;
  }>;
}

// ── Sub-components ────────────────────────────────────────────────────────────

const ReadinessRing = React.memo(function ReadinessRing({ score, trend }: { score: number; trend: string }) {
  const r = 50;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - score / 100);
  const color = score >= 70 ? '#58CC02' : score >= 40 ? '#FF9600' : '#FF4B4B';

  return (
    <svg width="120" height="120" viewBox="0 0 120 120" className="shrink-0">
      {/* Background circle */}
      <circle cx="60" cy="60" r={r} stroke="#e5e7eb" strokeWidth="10" fill="none" />
      {/* Progress arc */}
      <circle
        cx="60" cy="60" r={r}
        stroke={color}
        strokeWidth="10"
        fill="none"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform="rotate(-90 60 60)"
        style={{ transition: 'stroke-dashoffset 1s ease' }}
      />
      {/* Score text */}
      <text x="60" y="56" textAnchor="middle" fontSize="22" fontWeight="800" fill={color}>{score}%</text>
      <text x="60" y="72" textAnchor="middle" fontSize="9" fill="#9ca3af">
        {trend === 'improving' ? '⬆ Improving' : trend === 'declining' ? '⬇ Declining' : '➡ Stable'}
      </text>
    </svg>
  );
});

const PlanItem = React.memo(function PlanItem({
  item, onToggle,
}: {
  item: DailyPlanItem;
  onToggle: (id: string) => void;
}) {
  const typeIcon = item.type === 'mock' ? '📝' : item.type === 'explore' ? '🔍' : item.type === 'flashcards' ? '🧠' : '⚡';
  return (
    <Link href={item.targetUrl} onClick={() => onToggle(item.id)}
      className={`flex items-center gap-3 py-3 border-b border-gray-100 last:border-b-0 transition-opacity ${item.done ? 'opacity-40' : ''}`}
    >
      <div
        className={`w-6 h-6 rounded-full border-2 shrink-0 flex items-center justify-center text-xs transition-colors ${
          item.done ? 'bg-duo-green border-duo-green text-white' : 'border-gray-300'
        }`}
      >
        {item.done && '✓'}
      </div>
      <span className="text-lg shrink-0" aria-hidden="true">{typeIcon}</span>
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-bold truncate ${item.done ? 'line-through text-gray-500' : 'text-gray-800'}`}>
          {item.action}
        </p>
        <p className="text-xs text-gray-500 font-medium truncate">{item.reason}</p>
      </div>
      <span className="text-[10px] font-extrabold text-gray-500 bg-gray-100 rounded-full px-2 py-0.5 shrink-0">
        {item.estimatedMins}min
      </span>
    </Link>
  );
});

const TopicBar = React.memo(function TopicBar({ entry }: { entry: TopicMasteryEntry }) {
  const pct = Math.round(entry.mastery * 100);
  const barColor = pct >= 70 ? '#58CC02' : pct >= 40 ? '#FF9600' : pct > 0 ? '#FF4B4B' : '#e5e7eb';
  return (
    <div className="flex items-center gap-3 py-1.5">
      <span className="text-base shrink-0 w-6 text-center" aria-hidden="true">{entry.emoji}</span>
      <span className="text-xs font-semibold text-gray-700 w-28 truncate">{entry.topicName}</span>
      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-[width] duration-700"
          style={{ width: `${pct}%`, backgroundColor: barColor }}
        />
      </div>
      <span className="text-xs font-extrabold w-9 text-right" style={{ color: barColor }}>
        {pct}%
      </span>
    </div>
  );
});


// ── Page ──────────────────────────────────────────────────────────────────────

export default function HomePage() {
  const router = useRouter();
  const [data,       setData]       = useState<HomeData | null>(null);
  const [loading,    setLoading]    = useState(true);
  const [fetchError, setFetchError] = useState(false);
  const [planDone, setPlanDone] = useState<Set<string>>(new Set());
  const [nudgeDismissed, setNudgeDismissed] = useState(false);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }

    // Restore today's plan done state
    const todayKey = `mathspark_plan_done_${new Date().toDateString()}`;
    const savedDone = JSON.parse(localStorage.getItem(todayKey) ?? '[]') as string[];
    setPlanDone(new Set(savedDone));

    // Nudge dismissal
    const dismissedKey = `dismissed_nudge_${new Date().toDateString()}`;
    setNudgeDismissed(localStorage.getItem(dismissedKey) === 'true');

    const CACHE_KEY = `mathspark_home_${id}`;
    const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

    // Check cache first
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      if (cached) {
        const { data: cachedData, ts } = JSON.parse(cached) as { data: HomeData; ts: number };
        if (Date.now() - ts < CACHE_TTL) {
          setData(cachedData);
          setLoading(false);
          return; // Use cached data, skip fetch
        }
      }
    } catch { /* ignore parse errors */ }

    // Cache miss — fetch from API
    fetch('/api/home')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d: HomeData) => {
        setData(d);
        // Only cache if analytics are populated (avoid caching empty first-load state)
        const hasAnalytics = d.topicMastery && Array.isArray(d.topicMastery) && d.topicMastery.length > 0;
        if (hasAnalytics) {
          try {
            localStorage.setItem(CACHE_KEY, JSON.stringify({ data: d, ts: Date.now() }));
          } catch { /* ignore storage errors */ }
        }
      })
      .catch((err) => { console.error('[fetch]', err); setFetchError(true); })
      .finally(() => setLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const togglePlanItem = useCallback((id: string) => {
    const todayKey = `mathspark_plan_done_${new Date().toDateString()}`;
    setPlanDone((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id); else next.add(id);
      localStorage.setItem(todayKey, JSON.stringify(Array.from(next)));
      return next;
    });
  }, []);

  function dismissNudge() {
    const dismissedKey = `dismissed_nudge_${new Date().toDateString()}`;
    localStorage.setItem(dismissedKey, 'true');
    setNudgeDismissed(true);
  }

  // Today's plan with done state applied
  const planWithDone = useMemo(
    () => (data?.dailyPlan ?? []).map((item) => ({ ...item, done: planDone.has(item.id) })),
    [data?.dailyPlan, planDone],
  );
  const planDoneCount = useMemo(
    () => planWithDone.filter((i) => i.done).length,
    [planWithDone],
  );
  const allDone = planDoneCount >= planWithDone.length && planWithDone.length > 0;

  // Top mastery entries with attempts (for chart)
  const chartTopics = useMemo(
    () => [...(data?.topicMastery ?? [])]
      .filter((t) => t.attemptsCount > 0)
      .sort((a, b) => b.mastery - a.mastery)
      .slice(0, 5),
    [data?.topicMastery],
  );

  const weakest2 = useMemo(
    () => [...(data?.topicMastery ?? [])]
      .filter((t) => t.attemptsCount > 0)
      .slice(0, 2),
    [data?.topicMastery],
  );

  if (!loading && (fetchError || !data)) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-4 pb-24">
        <p className="text-gray-800 font-extrabold text-lg">Something went wrong</p>
        <p className="text-gray-500 text-sm">Could not load your dashboard. Check your connection.</p>
        <button onClick={() => window.location.reload()} className="bg-duo-green text-white font-extrabold px-6 py-2.5 rounded-2xl text-sm active:scale-95 transition-transform">
          Retry
        </button>
      </div>
    );
  }

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-gray-50 pb-24">
        {/* Header */}
        <div className="bg-duo-dark px-4 py-3 flex items-center justify-between">
          <div className="h-4 bg-white/20 rounded w-20 animate-pulse" />
          <div className="h-7 bg-white/20 rounded-full w-16 animate-pulse" />
          <div className="h-8 bg-white/20 rounded-full w-14 animate-pulse" />
        </div>
        <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
          {/* Greeting */}
          <div className="space-y-1.5 animate-pulse">
            <div className="h-5 bg-gray-200 rounded w-48" />
            <div className="h-3.5 bg-gray-200 rounded w-32" />
          </div>
          {/* Readiness ring card */}
          <div className="bg-white rounded-2xl p-4 border border-gray-100 flex items-center gap-4 animate-pulse">
            <div className="w-[120px] h-[120px] rounded-full bg-gray-200 shrink-0" />
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-200 rounded w-28" />
              <div className="h-3.5 bg-gray-200 rounded w-36" />
              <div className="h-3.5 bg-gray-200 rounded w-24" />
            </div>
          </div>
          {/* Today's plan card */}
          <div className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse">
            <div className="h-3.5 bg-gray-200 rounded w-24 mb-4" />
            {[0, 1, 2].map((i) => (
              <div key={i} className="flex items-center gap-3 py-3 border-b border-gray-100 last:border-0">
                <div className="w-6 h-6 rounded-full bg-gray-200 shrink-0" />
                <div className="w-6 h-6 rounded bg-gray-200 shrink-0" />
                <div className="flex-1 space-y-1">
                  <div className="h-3.5 bg-gray-200 rounded w-3/4" />
                  <div className="h-2.5 bg-gray-200 rounded w-1/2" />
                </div>
                <div className="h-5 bg-gray-200 rounded-full w-10 shrink-0" />
              </div>
            ))}
          </div>
          {/* Quick actions */}
          <div className="grid grid-cols-3 gap-3 animate-pulse">
            {[0, 1, 2].map((i) => (
              <div key={i} className="bg-white rounded-2xl p-3 h-20 border border-gray-100" />
            ))}
          </div>
          {/* Strengths & gaps card */}
          <div className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse">
            <div className="h-3.5 bg-gray-200 rounded w-20 mb-4" />
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="flex items-center gap-3 py-1.5">
                <div className="w-6 h-6 rounded bg-gray-200 shrink-0" />
                <div className="w-28 h-3 bg-gray-200 rounded shrink-0" />
                <div className="flex-1 h-2 bg-gray-200 rounded-full" />
                <div className="w-9 h-3 bg-gray-200 rounded shrink-0" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const { student, streak, todayCorrect, topicMastery, examReadiness, topicPriorities, dailyPlan, nudges, recentActivity } = data;

  const gradeColors: Record<number, string> = {
    2: '#58CC02', 3: '#58CC02', 4: '#1CB0F6',
    5: '#FF9600', 6: '#FF9600', 7: '#9B59B6',
    8: '#9B59B6', 9: '#FF4B4B',
  };
  const gradeColor = gradeColors[student.grade] ?? '#1CB0F6';

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';

  const activeNudge = nudges[0];
  const topPriorityUrl = topicPriorities[0]?.dbTopicId
    ? `/practice/${topicPriorities[0].dbTopicId}`
    : '/chapters';

  const readinessScore = examReadiness?.score ?? 0;
  const readinessTrend = examReadiness?.trend ?? 'stable';

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">

      {/* ── STICKY HEADER ─────────────────────────────────────────────── */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-3 flex items-center justify-between shadow-md">
        <span className="text-white font-extrabold text-sm tracking-tight">MathSpark</span>
        <div
          className="text-xs font-extrabold px-3 py-1.5 rounded-full text-white"
          style={{ backgroundColor: gradeColor }}
        >
          Grade {student.grade}
        </div>
        <div className="flex items-center gap-2">
          <div
            className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-extrabold text-white border-2 border-white/30"
            style={{ backgroundColor: student.avatarColor }}
          >
            {student.name[0]?.toUpperCase() ?? '?'}
          </div>
          {streak > 0 && (
            <span className="text-orange-400 text-sm font-extrabold"><span aria-hidden="true">🔥</span>{streak}</span>
          )}
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* ── GREETING + TRIAL BANNER ────────────────────────────────── */}
        <div>
          <h1 className="text-xl font-extrabold text-gray-800">
            {greeting}, {student.name}! <span aria-hidden="true">🌟</span>
          </h1>
          <p className="text-gray-500 text-sm font-medium mt-0.5">
            {todayCorrect > 0 ? `${todayCorrect} correct today · ` : ''}Ready to practice?
          </p>
        </div>

        {student.trialActive && student.trialDaysLeft !== null && (
          <div className="bg-amber-50 border border-amber-200 rounded-2xl px-4 py-2.5 flex items-center justify-between">
            <div>
              <p className="text-amber-800 font-extrabold text-sm"><span aria-hidden="true">🎉 </span>Pro Trial Active</p>
              <p className="text-amber-600 text-xs font-medium">{student.trialDaysLeft} days left</p>
            </div>
            <Link href="/pricing" className="text-xs font-extrabold text-duo-orange bg-amber-100 rounded-full px-3 py-1.5">
              Upgrade →
            </Link>
          </div>
        )}

        {/* ── CONTINUE LEARNING CTA ───────────────────────────────── */}
        {topicPriorities.length > 0 && topicPriorities[0].dbTopicId && (
          <Link
            href={`/practice/${topicPriorities[0].dbTopicId}`}
            className="block bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-4 border border-blue-200 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl" aria-hidden="true">{topicPriorities[0].emoji}</span>
              <div className="flex-1 min-w-0">
                <p className="font-extrabold text-gray-800 text-sm">Continue Learning</p>
                <p className="text-xs text-gray-500 font-medium truncate">
                  {topicPriorities[0].topicName}
                </p>
              </div>
              <span className="text-duo-blue font-extrabold text-sm shrink-0">Go →</span>
            </div>
          </Link>
        )}

        {/* ── EXAM READINESS RING ────────────────────────────────────── */}
        {(() => {
          const hasAttempts = topicMastery.some(t => t.attemptsCount > 0);
          if (!hasAttempts) {
            return (
              <Link href="/chapters">
                <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-center gap-4 cursor-pointer hover:shadow-md transition-shadow">
                  {/* Empty state ring — gray with ? */}
                  <svg width="120" height="120" viewBox="0 0 120 120" className="shrink-0">
                    <circle cx="60" cy="60" r="50" stroke="#e5e7eb" strokeWidth="10" fill="none" />
                    <text x="60" y="56" textAnchor="middle" fontSize="22" fontWeight="800" fill="#d1d5db">?</text>
                    <text x="60" y="72" textAnchor="middle" fontSize="9" fill="#9ca3af">Not started</text>
                  </svg>
                  <div className="flex-1 space-y-1.5">
                    <p className="font-extrabold text-gray-800 text-base leading-tight">Exam Readiness</p>
                    <p className="text-sm font-medium text-gray-500">Answer questions to unlock your readiness score!</p>
                    <span className="inline-block text-xs font-extrabold text-white bg-duo-green rounded-full px-3 py-1.5">
                      Start Practicing →
                    </span>
                  </div>
                </div>
              </Link>
            );
          }
          return (
            <Link href="/chapters">
              <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-center gap-4 cursor-pointer hover:shadow-md transition-shadow">
                <ReadinessRing score={readinessScore} trend={readinessTrend} />
                <div className="flex-1 space-y-1.5">
                  <p className="font-extrabold text-gray-800 text-base leading-tight">Exam Readiness</p>
                  {examReadiness?.predictedMin != null ? (
                    <p className="text-sm font-semibold text-gray-600">
                      📊 Predicted {examReadiness.predictedMin}–{examReadiness.predictedMax} / 40
                    </p>
                  ) : null}
                  {examReadiness?.daysUntilExam != null ? (
                    <p className="text-sm font-semibold text-gray-500">
                      📅 {examReadiness.daysUntilExam} days to exam
                    </p>
                  ) : (
                    <Link href="/profile" className="text-sm font-semibold text-duo-blue hover:underline">
                      Set exam date →
                    </Link>
                  )}
                </div>
              </div>
            </Link>
          );
        })()}

        {/* ── TODAY'S PLAN ───────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-1">
            <h2 className="font-extrabold text-gray-800 text-sm">Today&apos;s Plan</h2>
            <span className="text-xs font-bold text-gray-500">
              {planDoneCount}/{planWithDone.length} done
            </span>
          </div>

          {allDone ? (
            <div className="py-4 flex flex-col items-center gap-2">
              <div className="animate-sparky-dance">
                <Sparky mood="celebrating" size={60} />
              </div>
              <p className="text-duo-green font-extrabold text-sm"><span aria-hidden="true">🌟 </span>All done today!</p>
            </div>
          ) : planWithDone.length === 0 ? (
            <div className="py-4 text-center">
              <p className="text-gray-500 text-sm font-medium">Start practicing to build your plan!</p>
              <Link href="/chapters" className="text-duo-blue font-extrabold text-sm mt-1 block">
                Go to Learn →
              </Link>
            </div>
          ) : (
            <div>
              {planWithDone.map((item) => (
                <PlanItem key={item.id} item={item} onToggle={togglePlanItem} />
              ))}
            </div>
          )}
        </div>

        {/* ── DAILY CHALLENGE CARD ───────────────────────────────────── */}
        <Link href="/practice/daily"
          className="block bg-gradient-to-r from-orange-50 to-yellow-50 rounded-2xl p-4 border border-orange-200 shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="flex items-center gap-3">
            <span className="text-3xl" aria-hidden="true">🎯</span>
            <div className="flex-1 min-w-0">
              <p className="font-extrabold text-gray-800 text-sm">Daily Challenge</p>
              <p className="text-xs text-gray-500 font-medium">5 questions · Build your streak!</p>
            </div>
            {streak > 0 && (
              <div className="flex items-center gap-1 bg-orange-100 rounded-full px-2.5 py-1 border border-orange-200">
                <span className="text-sm" aria-hidden="true">🔥</span>
                <span className="text-xs font-extrabold text-orange-600">{streak}</span>
              </div>
            )}
            <span className="text-duo-orange font-extrabold text-sm shrink-0">Play →</span>
          </div>
        </Link>

        {/* ── QUICK ACTIONS ──────────────────────────────────────────── */}
        <div className="grid grid-cols-3 gap-2">
          {[
            { emoji: '⚡', label: 'Quick Practice', sub: '5 min',      href: topPriorityUrl,           bg: 'bg-blue-50',   accent: '#1CB0F6' },
            { emoji: '📝', label: 'Exam Papers',    sub: '240 papers', href: '/practice/papers',       bg: 'bg-red-50',    accent: '#FF4B4B' },
            { emoji: '🃏', label: 'Flashcards',     sub: '1,086 cards', href: '/flashcards',            bg: 'bg-purple-50', accent: '#9B59B6' },
            { emoji: '🎯', label: 'Skill Drills',   sub: '16 topics',  href: '/practice/skill-drill',  bg: 'bg-yellow-50', accent: '#FF9600' },
            { emoji: '💡', label: 'Sparky Explains', sub: '212 solved', href: '/learn/examples',       bg: 'bg-indigo-50', accent: '#6366F1' },
            { emoji: '🔮', label: 'IPM Predictor',  sub: '10+ years',  href: '/exam-prep/predictor',   bg: 'bg-green-50',  accent: '#58CC02' },
          ].map((action) => (
            <Link key={action.label} href={action.href}
              className={`${action.bg} rounded-2xl p-3 flex flex-col items-center gap-1 border border-white shadow-sm active:scale-95 transition-transform`}
            >
              <span className="text-2xl" aria-hidden="true">{action.emoji}</span>
              <p className="text-xs font-extrabold text-gray-700 text-center leading-tight">{action.label}</p>
              <p className="text-[10px] text-gray-500 font-semibold">{action.sub}</p>
            </Link>
          ))}
        </div>

        {/* ── MY PROGRESS ──────────────────────────────────────────────── */}
        <Link href="/progress"
          className="block bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-4 border border-green-200 shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl" aria-hidden="true">📊</span>
            <div className="flex-1">
              <p className="font-extrabold text-gray-800 text-sm">My Progress</p>
              <p className="text-xs text-gray-500 font-medium">Dashboard, strengths, mistakes & parent report</p>
            </div>
            <span className="text-duo-green font-extrabold text-xs shrink-0">View →</span>
          </div>
        </Link>

        {/* ── LEARN MORE ───────────────────────────────────────────────── */}
        <div className="grid grid-cols-2 gap-2">
          <Link href="/learn/strategies"
            className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-2xl p-3 border border-amber-200 shadow-sm hover:shadow-md transition-shadow"
          >
            <span className="text-xl" aria-hidden="true">🧠</span>
            <p className="font-extrabold text-gray-800 text-xs mt-1.5 leading-tight">Strategy Bank</p>
            <p className="text-[10px] text-gray-500 font-medium">35 exam tips</p>
          </Link>
          <Link href="/learn/stories"
            className="bg-gradient-to-br from-cyan-50 to-sky-50 rounded-2xl p-3 border border-cyan-200 shadow-sm hover:shadow-md transition-shadow"
          >
            <span className="text-xl" aria-hidden="true">📖</span>
            <p className="font-extrabold text-gray-800 text-xs mt-1.5 leading-tight">Math Stories</p>
            <p className="text-[10px] text-gray-500 font-medium">30 real-world stories</p>
          </Link>
          <Link href="/learn/concept-map"
            className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-2xl p-3 border border-violet-200 shadow-sm hover:shadow-md transition-shadow"
          >
            <span className="text-xl" aria-hidden="true">🗺️</span>
            <p className="font-extrabold text-gray-800 text-xs mt-1.5 leading-tight">Concept Map</p>
            <p className="text-[10px] text-gray-500 font-medium">88 concepts</p>
          </Link>
          <Link href="/learn/mistakes"
            className="bg-gradient-to-br from-red-50 to-orange-50 rounded-2xl p-3 border border-red-200 shadow-sm hover:shadow-md transition-shadow"
          >
            <span className="text-xl" aria-hidden="true">🚨</span>
            <p className="font-extrabold text-gray-800 text-xs mt-1.5 leading-tight">Mistake Patterns</p>
            <p className="text-[10px] text-gray-500 font-medium">50 common traps</p>
          </Link>
        </div>

        {/* ── SPARKY'S NUDGE ─────────────────────────────────────────── */}
        {activeNudge && !nudgeDismissed && (
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm flex items-start gap-3">
            <div className="shrink-0">
              <Sparky mood={activeNudge.sparkyEmotion} size={44} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold text-gray-700 leading-snug">{activeNudge.message}</p>
              <Link href={activeNudge.actionUrl}
                className="inline-block mt-2 text-xs font-extrabold text-duo-blue bg-blue-50 rounded-full px-3 py-1.5"
              >
                {activeNudge.actionLabel} →
              </Link>
            </div>
            <button
              onClick={dismissNudge}
              style={{ minHeight: 0 }}
              className="text-gray-300 hover:text-gray-500 text-lg leading-none px-1 shrink-0"
            >
              ×
            </button>
          </div>
        )}

        {/* ── STRENGTHS & GAPS ───────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-extrabold text-gray-800 text-sm">Your Topics</h2>
            <Link href="/chapters" className="text-xs font-extrabold text-duo-blue">See all →</Link>
          </div>

          {chartTopics.length === 0 ? (
            <div className="py-3 text-center">
              <p className="text-gray-500 text-sm font-medium">No practice yet. Start learning!</p>
              <Link href="/chapters" className="text-duo-blue font-extrabold text-sm mt-1 block">
                Browse Topics →
              </Link>
            </div>
          ) : (
            <>
              {chartTopics.map((entry) => (
                <TopicBar key={entry.topicId} entry={entry} />
              ))}
              {weakest2.length > 0 && (
                <p className="text-xs font-semibold text-duo-red mt-2">
                  Focus: {weakest2.map((t) => t.topicName).join(' & ')}
                </p>
              )}
            </>
          )}
        </div>

        {/* ── RECENT ACTIVITY ────────────────────────────────────────── */}
        {recentActivity.length > 0 && (
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-extrabold text-gray-800 text-sm">Recent Activity</h2>
              <Link href="/chapters" className="text-xs font-extrabold text-duo-blue">View all →</Link>
            </div>
            <div className="space-y-2.5">
              {recentActivity.map((act, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-blue-50 flex items-center justify-center text-sm shrink-0" aria-hidden="true">
                    📚
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-gray-700 truncate">{act.topicName}</p>
                    <p className="text-xs text-gray-500 font-medium">{act.correct}/{act.attempted} correct</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-extrabold"
                      style={{ color: act.pct >= 70 ? '#58CC02' : act.pct >= 40 ? '#FF9600' : '#FF4B4B' }}>
                      {act.pct}%
                    </p>
                    <p className="text-[10px] text-gray-300 font-medium">{act.timeAgo}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── TOP RECOMMENDATIONS ────────────────────────────────────── */}
        {topicPriorities.slice(0, 2).length > 0 && (
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
            <h2 className="font-extrabold text-gray-800 text-sm mb-3"><span aria-hidden="true">🎯 </span>Recommended for You</h2>
            <div className="space-y-2">
              {topicPriorities.slice(0, 2).map((tp) => (
                <Link
                  key={tp.topicId}
                  href={`/practice/${tp.dbTopicId}`}
                  className="flex items-center gap-3 bg-[#1a2d35] rounded-xl px-3 py-3 border-l-4 border-duo-green hover:bg-[#223d4a] transition-colors"
                >
                  <span className="text-xl shrink-0" aria-hidden="true">{tp.emoji}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-extrabold text-sm truncate">{tp.topicName}</p>
                    <p className="text-white/70 text-xs font-medium truncate">{tp.reason}</p>
                  </div>
                  <span className="text-duo-green text-xs font-extrabold shrink-0">Practice →</span>
                </Link>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
