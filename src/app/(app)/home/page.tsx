'use client';

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { STREAK_MILESTONES } from '@/lib/flashcardXP';
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
  leagueTier: number;
  leagueName: string;
  leagueRank: number | null;
  weeklyXP: number;
  todayXP: number;
  topicsMasteredCount: number;
  topicsExploredCount: number;
  totalTopics: number;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const LEAGUE_EMOJI: Record<number, string> = { 1: '🥉', 2: '🥈', 3: '🥇', 4: '💎', 5: '👑' };

function reframePlanReason(reason: string): string {
  if (reason.includes('Very low accuracy'))             return 'Great topic to build on!';
  if (reason.includes('Not practiced in'))              return "Time to refresh — it's been a while!";
  if (reason.includes('% of question types explored'))  return 'New question types to discover!';
  if (reason.includes('High exam frequency'))           return 'Appears often in exams — high impact!';
  if (reason.includes('You marked this as a focus'))    return 'Your focus area — keep going!';
  if (reason.includes('No mock test in'))               return 'Time for a fresh mock test';
  if (reason.includes('Very few question types'))       return 'New question types to discover!';
  return reason;
}

function isRecentWin(timeAgo: string): boolean {
  if (timeAgo === 'just now') return true;
  if (timeAgo.endsWith('h ago')) {
    const hours = parseInt(timeAgo, 10);
    return !isNaN(hours) && hours <= 12;
  }
  return false;
}

// ── Sub-components ────────────────────────────────────────────────────────────

const StatsBar = React.memo(function StatsBar({
  streak, todayXP, leagueName, leagueTier, leagueRank,
}: {
  streak: number; todayXP: number; leagueName: string; leagueTier: number; leagueRank: number | null;
}) {
  const leagueEmoji = LEAGUE_EMOJI[leagueTier] ?? '🥉';
  return (
    <div className="flex items-center gap-2">
      <div className="flex items-center gap-1.5 bg-orange-50 rounded-full px-3 py-1.5 border border-orange-100">
        <span className="text-sm" aria-hidden="true">🔥</span>
        <span className="text-xs font-extrabold text-orange-600">{streak > 0 ? streak : '—'}</span>
      </div>
      <div className="flex items-center gap-1.5 bg-amber-50 rounded-full px-3 py-1.5 border border-amber-100">
        <span className="text-sm" aria-hidden="true">⭐</span>
        <span className="text-xs font-extrabold text-amber-600">{todayXP} XP</span>
      </div>
      <Link href="/leaderboard" className="flex items-center gap-1.5 bg-blue-50 rounded-full px-3 py-1.5 border border-blue-100">
        <span className="text-sm" aria-hidden="true">{leagueEmoji}</span>
        <span className="text-xs font-extrabold text-blue-600">
          {leagueName}{leagueRank ? ` #${leagueRank}` : ''}
        </span>
      </Link>
    </div>
  );
});

const HeroCard = React.memo(function HeroCard({
  streak, recentActivity, topicPriorities,
  onDismissMilestone,
}: {
  streak: number;
  recentActivity: HomeData['recentActivity'];
  topicPriorities: TopicPriority[];
  onDismissMilestone: () => void;
}) {
  // Priority 1: Streak milestone
  const milestone = STREAK_MILESTONES.find(m => m.days === streak);
  const todayKey = `mathspark_milestone_${new Date().toDateString()}`;
  const celebrated = typeof window !== 'undefined' && localStorage.getItem(todayKey) === 'true';

  if (milestone && !celebrated) {
    return (
      <div className="bg-gradient-to-r from-amber-50 to-yellow-50 rounded-2xl p-4 border border-amber-200 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="shrink-0 animate-sparky-dance">
            <Sparky mood="celebrating" size={52} />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-lg font-extrabold text-gray-800">
              {milestone.emoji} {milestone.title}
            </p>
            <p className="text-sm text-gray-600 font-medium">
              <span aria-hidden="true">🔥</span> {streak} day streak · {milestone.description}
            </p>
          </div>
          <button
            onClick={(e) => {
              e.preventDefault();
              localStorage.setItem(todayKey, 'true');
              onDismissMilestone();
            }}
            className="text-gray-300 hover:text-gray-500 text-lg leading-none px-1 shrink-0"
          >
            ×
          </button>
        </div>
      </div>
    );
  }

  // Priority 2: Recent win (≥85%, within 12h)
  const recentWin = recentActivity[0];
  if (recentWin && recentWin.pct >= 85 && isRecentWin(recentWin.timeAgo)) {
    return (
      <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-4 border border-green-200 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="shrink-0">
            <Sparky mood="happy" size={52} />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-extrabold text-gray-800">
              You aced {recentWin.topicName}! <span aria-hidden="true">🎉</span>
            </p>
            <p className="text-xs text-gray-500 font-medium">
              {recentWin.correct}/{recentWin.attempted} correct · {recentWin.pct}%
            </p>
          </div>
          <span className="text-2xl shrink-0" aria-hidden="true">🌟</span>
        </div>
      </div>
    );
  }

  // Priority 3: Daily challenge (if streak > 0)
  if (streak > 0) {
    return (
      <Link href="/practice/daily"
        className="block bg-gradient-to-r from-orange-50 to-yellow-50 rounded-2xl p-4 border border-orange-200 shadow-sm"
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
    );
  }

  // Priority 4: Continue learning
  if (topicPriorities[0]?.dbTopicId) {
    const tp = topicPriorities[0];
    return (
      <Link href={`/practice/${tp.dbTopicId}`}
        className="block bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-4 border border-blue-200 shadow-sm"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl" aria-hidden="true">{tp.emoji}</span>
          <div className="flex-1 min-w-0">
            <p className="font-extrabold text-gray-800 text-sm">Continue: {tp.topicName}</p>
            <p className="text-xs text-gray-500 font-medium truncate">
              {reframePlanReason(tp.reason)}
            </p>
          </div>
          <span className="text-duo-blue font-extrabold text-sm shrink-0">Go →</span>
        </div>
      </Link>
    );
  }

  // Priority 5: Fallback — welcome
  return (
    <Link href="/chapters"
      className="block bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-4 border border-blue-200 shadow-sm"
    >
      <div className="flex items-center gap-3">
        <div className="shrink-0">
          <Sparky mood="happy" size={52} />
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-extrabold text-gray-800 text-sm">Welcome to MathSpark!</p>
          <p className="text-xs text-gray-500 font-medium">Start your math journey today</p>
        </div>
        <span className="text-duo-blue font-extrabold text-sm shrink-0">Start →</span>
      </div>
    </Link>
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
        <p className="text-xs text-gray-500 font-medium truncate">{reframePlanReason(item.reason)}</p>
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
  const [heroDismissed, setHeroDismissed] = useState(false);
  const handleDismissMilestone = useCallback(() => setHeroDismissed(prev => !prev), []);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }

    // Restore today's plan done state
    const todayKey = `mathspark_plan_done_${new Date().toDateString()}`;
    const savedDone = JSON.parse(localStorage.getItem(todayKey) ?? '[]') as string[];
    setPlanDone(new Set(savedDone));

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

  // Today's plan with done state applied — cap at 3 items
  const planWithDone = useMemo(
    () => (data?.dailyPlan ?? []).slice(0, 3).map((item) => ({ ...item, done: planDone.has(item.id) })),
    [data?.dailyPlan, planDone],
  );
  const planDoneCount = useMemo(
    () => planWithDone.filter((i) => i.done).length,
    [planWithDone],
  );
  const allDone = planDoneCount >= planWithDone.length && planWithDone.length > 0;

  // 3 most recently active topics for "Your Topics"
  const displayTopics = useMemo(() => {
    if (!data) return [];
    const masteryMap = new Map(data.topicMastery.map(t => [t.topicId, t]));
    const recentTopicEntries: TopicMasteryEntry[] = [];

    // From recent activity order
    for (const act of data.recentActivity) {
      const entry = masteryMap.get(act.topicId);
      if (entry && !recentTopicEntries.some(e => e.topicId === entry.topicId)) {
        recentTopicEntries.push(entry);
      }
      if (recentTopicEntries.length >= 3) break;
    }

    // Pad with highest mastery if fewer than 3
    if (recentTopicEntries.length < 3) {
      const sorted = [...data.topicMastery]
        .filter(t => t.attemptsCount > 0)
        .sort((a, b) => b.mastery - a.mastery);
      for (const entry of sorted) {
        if (!recentTopicEntries.some(e => e.topicId === entry.topicId)) {
          recentTopicEntries.push(entry);
        }
        if (recentTopicEntries.length >= 3) break;
      }
    }
    return recentTopicEntries;
  }, [data]);

  // Quick Access tiles — contextual slots 3-4
  const quickAccessTiles = useMemo(() => {
    if (!data) return [];
    const topPriorityUrl = data.topicPriorities[0]?.dbTopicId
      ? `/practice/${data.topicPriorities[0].dbTopicId}`
      : '/chapters';

    // Read flashcard due count from localStorage
    let flashcardSub = 'Review cards';
    if (typeof window !== 'undefined') {
      const due = localStorage.getItem('mathspark_cards_due');
      if (due && parseInt(due, 10) > 0) flashcardSub = `${due} due`;
    }

    const fixed = [
      { emoji: '🃏', label: 'Flashcards',     sub: flashcardSub, href: '/flashcards',    bg: 'bg-purple-50', accent: '#9B59B6' },
      { emoji: '⚡', label: 'Quick Practice',  sub: '5 min',      href: topPriorityUrl,   bg: 'bg-blue-50',   accent: '#1CB0F6' },
    ];

    // Candidate pool for slots 3-4
    const candidates: Array<{ emoji: string; label: string; sub: string; href: string; bg: string; accent: string }> = [];

    if (data.examReadiness?.daysUntilExam != null && data.examReadiness.daysUntilExam <= 60) {
      candidates.push({ emoji: '📝', label: 'Exam Papers', sub: 'Practice exams', href: '/practice/papers', bg: 'bg-red-50', accent: '#FF4B4B' });
    }
    if (data.topicsExploredCount < data.totalTopics / 2) {
      candidates.push({ emoji: '🗺️', label: 'Concept Map', sub: 'Explore topics', href: '/learn/concept-map', bg: 'bg-violet-50', accent: '#9B59B6' });
    }
    candidates.push(
      { emoji: '📖', label: 'Concept Lessons', sub: 'Step-by-step', href: '/learn/lessons', bg: 'bg-purple-50', accent: '#8B5CF6' },
      { emoji: '🎯', label: 'Skill Drills', sub: 'Level up', href: '/practice/skill-drill', bg: 'bg-yellow-50', accent: '#FF9600' },
      { emoji: '💡', label: 'Sparky Explains', sub: 'Step-by-step', href: '/learn/examples', bg: 'bg-indigo-50', accent: '#6366F1' },
      { emoji: '🧠', label: 'Strategy Bank', sub: 'Exam tips', href: '/learn/strategies', bg: 'bg-amber-50', accent: '#FF9600' },
      { emoji: '🚨', label: 'Mistake Patterns', sub: 'Common traps', href: '/learn/mistakes', bg: 'bg-red-50', accent: '#FF4B4B' },
    );

    return [...fixed, ...candidates.slice(0, 2)];
  }, [data]);

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
          {/* Greeting + pills */}
          <div className="space-y-2.5 animate-pulse">
            <div className="h-5 bg-gray-200 rounded w-48" />
            <div className="h-3.5 bg-gray-200 rounded w-32" />
            <div className="flex gap-2">
              <div className="h-8 bg-gray-200 rounded-full w-16" />
              <div className="h-8 bg-gray-200 rounded-full w-20" />
              <div className="h-8 bg-gray-200 rounded-full w-24" />
            </div>
          </div>
          {/* Hero card */}
          <div className="bg-white rounded-2xl p-4 border border-gray-100 h-20 animate-pulse" />
          {/* Plan card */}
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
          {/* 2×2 grid */}
          <div className="grid grid-cols-2 gap-2 animate-pulse">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-2xl p-3 h-20 border border-gray-100" />
            ))}
          </div>
          {/* Topics card */}
          <div className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse">
            <div className="h-3.5 bg-gray-200 rounded w-20 mb-4" />
            {[0, 1, 2].map((i) => (
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

  const { student, streak, todayCorrect, topicPriorities, recentActivity } = data;

  const gradeColors: Record<number, string> = {
    2: '#58CC02', 3: '#58CC02', 4: '#1CB0F6',
    5: '#FF9600', 6: '#FF9600', 7: '#9B59B6',
    8: '#9B59B6', 9: '#FF4B4B',
  };
  const gradeColor = gradeColors[student.grade] ?? '#1CB0F6';

  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';

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

        {/* ── § 1: GREETING + STATS BAR ────────────────────────────────── */}
        <div>
          <h1 className="text-xl font-extrabold text-gray-800">
            {greeting}, {student.name}! <span aria-hidden="true">🌟</span>
          </h1>
          <p className="text-gray-500 text-sm font-medium mt-0.5">
            {todayCorrect > 0 ? `${todayCorrect} correct today · ` : ''}Ready to practice?
          </p>
          <div className="mt-2.5">
            <StatsBar
              streak={streak}
              todayXP={data.todayXP}
              leagueName={data.leagueName}
              leagueTier={data.leagueTier}
              leagueRank={data.leagueRank}
            />
          </div>
        </div>

        {/* ── TRIAL BANNER (if active) ─────────────────────────────────── */}
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

        {/* ── § 2: HERO CARD (dynamic) ─────────────────────────────────── */}
        <HeroCard
          streak={streak}
          recentActivity={recentActivity}
          topicPriorities={topicPriorities}
          onDismissMilestone={handleDismissMilestone}
        />

        {/* ── § 3: TODAY'S PLAN (max 3) ────────────────────────────────── */}
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

        {/* ── § 4: QUICK ACCESS (2×2 grid) ─────────────────────────────── */}
        <div className="grid grid-cols-2 gap-2">
          {quickAccessTiles.map((action) => (
            <Link key={action.label} href={action.href}
              className={`${action.bg} rounded-2xl p-3 flex flex-col items-center gap-1 border border-white shadow-sm active:scale-95 transition-transform`}
            >
              <span className="text-2xl" aria-hidden="true">{action.emoji}</span>
              <p className="text-xs font-extrabold text-gray-700 text-center leading-tight">{action.label}</p>
              <p className="text-[10px] text-gray-500 font-semibold">{action.sub}</p>
            </Link>
          ))}
        </div>

        {/* ── § 5: YOUR TOPICS (3 bars + summary) ──────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-extrabold text-gray-800 text-sm">Your Topics</h2>
            <Link href="/chapters" className="text-xs font-extrabold text-duo-blue">See all →</Link>
          </div>

          {displayTopics.length === 0 ? (
            <div className="py-3 text-center">
              <p className="text-gray-500 text-sm font-medium">No practice yet. Start learning!</p>
              <Link href="/chapters" className="text-duo-blue font-extrabold text-sm mt-1 block">
                Browse Topics →
              </Link>
            </div>
          ) : (
            <>
              {displayTopics.map((entry) => (
                <TopicBar key={entry.topicId} entry={entry} />
              ))}
              <p className="text-xs font-medium text-gray-500 mt-2">
                {data.topicsExploredCount} of {data.totalTopics} topics explored
                {data.topicsMasteredCount > 0 ? ` · ${data.topicsMasteredCount} mastered` : ''}
              </p>
            </>
          )}
        </div>

        {/* ── § 6: RECENT ACTIVITY (3 items) ───────────────────────────── */}
        {recentActivity.length > 0 && (
          <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-extrabold text-gray-800 text-sm">Recent Activity</h2>
              <Link href="/chapters" className="text-xs font-extrabold text-duo-blue">View all →</Link>
            </div>
            <div className="space-y-2.5">
              {recentActivity.slice(0, 3).map((act, i) => (
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

      </div>
    </div>
  );
}
