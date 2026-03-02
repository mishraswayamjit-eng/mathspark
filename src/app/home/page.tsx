'use client';

import { useEffect, useState } from 'react';
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

function ReadinessRing({ score, trend }: { score: number; trend: string }) {
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
}

function PlanItem({
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
          item.done ? 'bg-[#58CC02] border-[#58CC02] text-white' : 'border-gray-300'
        }`}
      >
        {item.done && '✓'}
      </div>
      <span className="text-lg shrink-0">{typeIcon}</span>
      <div className="flex-1 min-w-0">
        <p className={`text-sm font-bold truncate ${item.done ? 'line-through text-gray-400' : 'text-gray-800'}`}>
          {item.action}
        </p>
        <p className="text-xs text-gray-400 font-medium truncate">{item.reason}</p>
      </div>
      <span className="text-[10px] font-extrabold text-gray-400 bg-gray-100 rounded-full px-2 py-0.5 shrink-0">
        {item.estimatedMins}min
      </span>
    </Link>
  );
}

function TopicBar({ entry }: { entry: TopicMasteryEntry }) {
  const pct = Math.round(entry.mastery * 100);
  const barColor = pct >= 70 ? '#58CC02' : pct >= 40 ? '#FF9600' : pct > 0 ? '#FF4B4B' : '#e5e7eb';
  return (
    <div className="flex items-center gap-3 py-1.5">
      <span className="text-base shrink-0 w-6 text-center">{entry.emoji}</span>
      <span className="text-xs font-semibold text-gray-700 w-28 truncate">{entry.topicName}</span>
      <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${pct}%`, backgroundColor: barColor }}
        />
      </div>
      <span className="text-[11px] font-extrabold w-9 text-right" style={{ color: barColor }}>
        {pct}%
      </span>
    </div>
  );
}

function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl p-4 animate-pulse space-y-3 border border-gray-100">
      <div className="h-3 bg-gray-200 rounded w-24" />
      <div className="h-16 bg-gray-200 rounded-xl" />
    </div>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function HomePage() {
  const router = useRouter();
  const [data,    setData]    = useState<HomeData | null>(null);
  const [loading, setLoading] = useState(true);
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

    fetch(`/api/home?studentId=${id}`)
      .then((r) => r.json())
      .then((d: HomeData) => setData(d))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  function togglePlanItem(id: string) {
    const todayKey = `mathspark_plan_done_${new Date().toDateString()}`;
    const next = new Set(planDone);
    if (next.has(id)) next.delete(id); else next.add(id);
    setPlanDone(next);
    localStorage.setItem(todayKey, JSON.stringify(Array.from(next)));
  }

  function dismissNudge() {
    const dismissedKey = `dismissed_nudge_${new Date().toDateString()}`;
    localStorage.setItem(dismissedKey, 'true');
    setNudgeDismissed(true);
  }

  if (loading || !data) {
    return (
      <div className="min-h-screen bg-gray-50 pb-24">
        {/* Header skeleton */}
        <div className="bg-[#131F24] px-4 py-4 flex items-center justify-between animate-pulse">
          <div className="h-5 bg-white/20 rounded w-24" />
          <div className="h-8 bg-white/20 rounded-full w-20" />
          <div className="h-8 bg-white/20 rounded-full w-16" />
        </div>
        <div className="px-4 py-6 space-y-4 max-w-lg mx-auto">
          {[0, 1, 2, 3, 4].map((i) => <SkeletonCard key={i} />)}
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

  // Today's plan with done state applied
  const planWithDone = dailyPlan.map((item) => ({ ...item, done: planDone.has(item.id) }));
  const planDoneCount = planWithDone.filter((i) => i.done).length;
  const allDone = planDoneCount >= planWithDone.length && planWithDone.length > 0;

  // Top mastery entries with attempts (for chart)
  const chartTopics = [...topicMastery]
    .filter((t) => t.attemptsCount > 0)
    .sort((a, b) => b.mastery - a.mastery)
    .slice(0, 5);

  const weakest2 = [...topicMastery]
    .filter((t) => t.attemptsCount > 0)
    .slice(0, 2);

  const activeNudge = nudges[0];
  const topPriorityUrl = topicPriorities[0]?.dbTopicId
    ? `/practice/${topicPriorities[0].dbTopicId}`
    : '/chapters';

  const readinessScore = examReadiness?.score ?? 0;
  const readinessTrend = examReadiness?.trend ?? 'stable';

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">

      {/* ── STICKY HEADER ─────────────────────────────────────────────── */}
      <div className="sticky top-0 z-40 bg-[#131F24] px-4 py-3 flex items-center justify-between shadow-md">
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
            <span className="text-orange-400 text-sm font-extrabold">🔥{streak}</span>
          )}
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* ── GREETING + TRIAL BANNER ────────────────────────────────── */}
        <div>
          <h1 className="text-xl font-extrabold text-gray-800">
            {greeting}, {student.name}! 🌟
          </h1>
          <p className="text-gray-400 text-sm font-medium mt-0.5">
            {todayCorrect > 0 ? `${todayCorrect} correct today · ` : ''}Ready to practice?
          </p>
        </div>

        {student.trialActive && student.trialDaysLeft !== null && (
          <div className="bg-amber-50 border border-amber-200 rounded-2xl px-4 py-2.5 flex items-center justify-between">
            <div>
              <p className="text-amber-800 font-extrabold text-sm">🎉 Pro Trial Active</p>
              <p className="text-amber-600 text-xs font-medium">{student.trialDaysLeft} days left</p>
            </div>
            <Link href="/pricing" className="text-xs font-extrabold text-[#FF9600] bg-amber-100 rounded-full px-3 py-1.5">
              Upgrade →
            </Link>
          </div>
        )}

        {/* ── EXAM READINESS RING ────────────────────────────────────── */}
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
                <Link href="/profile" className="text-sm font-semibold text-[#1CB0F6] hover:underline">
                  Set exam date →
                </Link>
              )}
              {readinessScore === 0 && topicMastery.filter(t => t.attemptsCount > 0).length === 0 && (
                <p className="text-xs text-gray-400 font-medium">Practice to see your score!</p>
              )}
            </div>
          </div>
        </Link>

        {/* ── TODAY'S PLAN ───────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-1">
            <h2 className="font-extrabold text-gray-800 text-sm">Today&apos;s Plan</h2>
            <span className="text-xs font-bold text-gray-400">
              {planDoneCount}/{planWithDone.length} done
            </span>
          </div>

          {allDone ? (
            <div className="py-4 flex flex-col items-center gap-2">
              <div className="animate-sparky-dance">
                <Sparky mood="celebrating" size={60} />
              </div>
              <p className="text-[#58CC02] font-extrabold text-sm">🌟 All done today!</p>
            </div>
          ) : planWithDone.length === 0 ? (
            <div className="py-4 text-center">
              <p className="text-gray-400 text-sm font-medium">Start practicing to build your plan!</p>
              <Link href="/chapters" className="text-[#1CB0F6] font-extrabold text-sm mt-1 block">
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

        {/* ── QUICK ACTIONS ──────────────────────────────────────────── */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { emoji: '⚡', label: 'Quick Practice', sub: '5 min', href: topPriorityUrl, bg: 'bg-blue-50', accent: '#1CB0F6' },
            { emoji: '🧠', label: 'Flashcards',     sub: '3 min', href: '/chapters',    bg: 'bg-purple-50', accent: '#9B59B6' },
            { emoji: '📝', label: 'Mock Test',       sub: '15 min', href: '/test',       bg: 'bg-green-50', accent: '#58CC02' },
          ].map((action) => (
            <Link key={action.label} href={action.href}
              className={`${action.bg} rounded-2xl p-3 flex flex-col items-center gap-1 border border-white shadow-sm active:scale-95 transition-all`}
            >
              <span className="text-2xl">{action.emoji}</span>
              <p className="text-xs font-extrabold text-gray-700 text-center leading-tight">{action.label}</p>
              <p className="text-[10px] text-gray-400 font-semibold">{action.sub}</p>
            </Link>
          ))}
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
                className="inline-block mt-2 text-xs font-extrabold text-[#1CB0F6] bg-blue-50 rounded-full px-3 py-1.5"
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
            <Link href="/chapters" className="text-xs font-extrabold text-[#1CB0F6]">See all →</Link>
          </div>

          {chartTopics.length === 0 ? (
            <div className="py-3 text-center">
              <p className="text-gray-400 text-sm font-medium">No practice yet. Start learning!</p>
              <Link href="/chapters" className="text-[#1CB0F6] font-extrabold text-sm mt-1 block">
                Browse Topics →
              </Link>
            </div>
          ) : (
            <>
              {chartTopics.map((entry) => (
                <TopicBar key={entry.topicId} entry={entry} />
              ))}
              {weakest2.length > 0 && (
                <p className="text-xs font-semibold text-[#FF4B4B] mt-2">
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
              <Link href="/chapters" className="text-xs font-extrabold text-[#1CB0F6]">View all →</Link>
            </div>
            <div className="space-y-2.5">
              {recentActivity.map((act, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-xl bg-blue-50 flex items-center justify-center text-sm shrink-0">
                    📚
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-bold text-gray-700 truncate">{act.topicName}</p>
                    <p className="text-xs text-gray-400 font-medium">{act.correct}/{act.attempted} correct</p>
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
            <h2 className="font-extrabold text-gray-800 text-sm mb-3">🎯 Recommended for You</h2>
            <div className="space-y-2">
              {topicPriorities.slice(0, 2).map((tp) => (
                <Link
                  key={tp.topicId}
                  href={`/practice/${tp.dbTopicId}`}
                  className="flex items-center gap-3 bg-[#1a2d35] rounded-xl px-3 py-3 border-l-4 border-[#58CC02] hover:bg-[#223d4a] transition-colors"
                >
                  <span className="text-xl shrink-0">{tp.emoji}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-extrabold text-sm truncate">{tp.topicName}</p>
                    <p className="text-white/50 text-xs font-medium truncate">{tp.reason}</p>
                  </div>
                  <span className="text-[#58CC02] text-xs font-extrabold shrink-0">Practice →</span>
                </Link>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
