'use client';

import { Fragment, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { DashboardData, TopicWithProgress } from '@/types';
import Sparky from '@/components/Sparky';
import NudgeBubble from '@/components/NudgeBubble';
import { computeNudge, markMasteryShown, type Nudge } from '@/lib/nudges';

// ── Topic metadata ─────────────────────────────────────────────────────────────

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06':    '🔑', 'ch07-08': '🍕', 'ch09-10': '➗',
  'ch11':    '📊', 'ch12':    '📏', 'ch13':    '🔤', 'ch14':    '⚖️',
  'ch15':    '🧩', 'ch16':    '🔢', 'ch17':    '🕐', 'ch18':    '📐',
  'ch19':    '🔺', 'ch20':    '⬜', 'ch21':    '⭕', 'dh':      '📈',
};

const DAILY_GOAL = 10;

// ── Mastery sort weight (Practicing → NotStarted → Mastered) ──────────────────
function masteryWeight(m: string): number {
  if (m === 'Practicing') return 0;
  if (m === 'NotStarted') return 1;
  return 2; // Mastered
}

function sortTopics(topics: TopicWithProgress[]): TopicWithProgress[] {
  return [...topics].sort((a, b) => {
    const wDiff = masteryWeight(a.mastery) - masteryWeight(b.mastery);
    if (wDiff !== 0) return wDiff;
    // Within same mastery group, keep canonical TOPIC_ORDER
    return TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id);
  });
}

function getHearts(): number {
  if (typeof window === 'undefined') return 5;
  const today     = new Date().toDateString();
  const savedDate = localStorage.getItem('mathspark_hearts_date');
  if (savedDate !== today) {
    localStorage.setItem('mathspark_hearts', '5');
    localStorage.setItem('mathspark_hearts_date', today);
    return 5;
  }
  return parseInt(localStorage.getItem('mathspark_hearts') ?? '5', 10);
}

// ── Sub-components ─────────────────────────────────────────────────────────────

function MasteryBadge({ mastery }: { mastery: string }) {
  if (mastery === 'Mastered') {
    return (
      <span className="inline-flex items-center gap-1 text-[11px] font-extrabold px-2 py-0.5 rounded-full bg-green-100 text-green-700 border border-green-200">
        Mastered ✅
      </span>
    );
  }
  if (mastery === 'Practicing') {
    return (
      <span className="inline-flex items-center gap-1 text-[11px] font-extrabold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 border border-amber-200">
        Learning 🟡
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-[11px] font-extrabold px-2 py-0.5 rounded-full bg-gray-100 text-gray-500 border border-gray-200">
      Not started
    </span>
  );
}

function MiniProgressBar({ correct, attempted, mastery }: { correct: number; attempted: number; mastery: string }) {
  const pct = mastery === 'Mastered'
    ? 100
    : attempted > 0
    ? Math.min(100, Math.round((correct / attempted) * 100))
    : 0;

  const barColor =
    mastery === 'Mastered'  ? 'bg-[#58CC02]' :
    mastery === 'Practicing' ? 'bg-[#FF9600]' :
    'bg-gray-300';

  return (
    <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
      <div
        className={`h-full rounded-full transition-all duration-500 ${barColor}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

function TopicCard({
  topic,
  onClick,
}: {
  topic: TopicWithProgress;
  onClick: () => void;
}) {
  const emoji = TOPIC_EMOJI[topic.id] ?? '📚';

  return (
    <button
      onClick={onClick}
      className="w-full text-left bg-white rounded-2xl p-4 shadow-sm border border-gray-100 hover:shadow-md hover:border-[#1CB0F6] active:scale-[0.97] transition-all duration-150 flex flex-col gap-2"
    >
      {/* Emoji + mastery badge row */}
      <div className="flex items-start justify-between gap-1">
        <span className="text-3xl leading-none select-none">{emoji}</span>
        <MasteryBadge mastery={topic.mastery} />
      </div>

      {/* Topic name */}
      <p className="text-sm font-extrabold text-gray-800 leading-snug line-clamp-2">
        {topic.name}
      </p>

      {/* Questions solved */}
      <p className="text-[11px] text-gray-400 font-semibold">
        {topic.correct} question{topic.correct !== 1 ? 's' : ''} solved
      </p>

      {/* Mini progress bar */}
      <MiniProgressBar
        correct={topic.correct}
        attempted={topic.attempted}
        mastery={topic.mastery}
      />
    </button>
  );
}

// ── Loading skeleton ───────────────────────────────────────────────────────────

function Skeleton() {
  return (
    <div className="min-h-screen bg-white">
      {/* TopBar skeleton */}
      <div className="sticky top-0 z-50 h-14 bg-[#131F24] flex items-center justify-between px-4">
        <div className="h-5 w-24 rounded-full bg-white/20 animate-pulse" />
        <div className="flex gap-2">
          {[1,2,3,4].map((n) => (
            <div key={n} className="h-6 w-12 rounded-full bg-white/20 animate-pulse" />
          ))}
        </div>
      </div>
      {/* Greeting skeleton */}
      <div className="px-4 pt-5 pb-3">
        <div className="h-7 w-56 rounded-xl bg-gray-100 animate-pulse mb-1" />
        <div className="h-4 w-36 rounded-xl bg-gray-100 animate-pulse" />
      </div>
      {/* Grid skeleton */}
      <div className="px-4 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {Array.from({ length: 16 }, (_, i) => (
          <div key={i} className="rounded-2xl bg-gray-100 animate-pulse h-36" />
        ))}
      </div>
    </div>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────

export default function ChaptersPage() {
  const router = useRouter();

  const [data,    setData]    = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [hearts,  setHearts]  = useState(5);
  const [nudge,   setNudge]   = useState<Nudge | null>(null);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setHearts(getHearts());
    fetch(`/api/dashboard?studentId=${id}`)
      .then((r) => r.json())
      .then((d: DashboardData) => {
        setData(d);
        setLoading(false);
        const n = computeNudge({
          streakDays:     d.stats.streakDays,
          topicsMastered: d.stats.topicsMastered,
          topics:         d.topics,
        });
        if (n) setNudge(n);
      })
      .catch(() => setLoading(false));
  }, [router]);

  if (loading) return <Skeleton />;
  if (!data)   return <Skeleton />;

  const studentName  = data.student.name;
  const streakDays   = data.stats.streakDays;
  const xp           = data.stats.totalSolved * 10;
  const todayCorrect = data.weeklyData?.[data.weeklyData.length - 1]?.count ?? 0;
  const goalMet      = todayCorrect >= DAILY_GOAL;
  const sortedTopics = sortTopics(data.topics);

  return (
    <div className="min-h-screen bg-white pb-24">
      {/* ── Top bar ─────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-50 h-14 bg-[#131F24]/95 backdrop-blur-sm flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="animate-sparky-bounce">
            <Sparky mood="happy" size={30} />
          </div>
          <span className="font-extrabold text-white text-base tracking-tight">MathSpark</span>
        </div>
        <div className="flex items-center gap-3">
          {/* Streak */}
          <div className="flex items-center gap-1 bg-white/15 rounded-full px-2.5 py-1">
            <span className="text-sm">🔥</span>
            <span className="text-white text-xs font-extrabold">{streakDays}</span>
          </div>
          {/* XP */}
          <div className="flex items-center gap-1 bg-white/15 rounded-full px-2.5 py-1">
            <span className="text-sm">💎</span>
            <span className="text-white text-xs font-extrabold">{xp}</span>
          </div>
          {/* Hearts */}
          <div className="flex items-center gap-0.5">
            {[1,2,3,4,5].map((h) => (
              <span
                key={h}
                className="text-sm transition-opacity duration-300"
                style={{ opacity: h <= hearts ? 1 : 0.2 }}
              >❤️</span>
            ))}
          </div>
          {/* Avatar */}
          <div className="w-8 h-8 rounded-full bg-[#FFC800] flex items-center justify-center font-extrabold text-sm text-yellow-900 border-2 border-white">
            {studentName ? studentName[0].toUpperCase() : '?'}
          </div>
        </div>
      </div>

      {/* ── Nudge ───────────────────────────────────────────────────────── */}
      {nudge && (
        <NudgeBubble
          nudge={nudge}
          onDismiss={() => {
            if (nudge.mood === 'celebrating') {
              const topic = data.topics.find(
                (t) => t.mastery === 'Mastered' && nudge.message.includes(t.name),
              );
              if (topic) markMasteryShown(topic.id);
            }
            setNudge(null);
          }}
        />
      )}

      {/* ── Greeting ────────────────────────────────────────────────────── */}
      <div className="px-4 pt-5 pb-2">
        <h1 className="text-xl font-extrabold text-gray-800">
          Hi {studentName}! What shall we practice today? 🌟
        </h1>
        {/* Daily goal mini-strip */}
        <p className="text-sm text-gray-400 font-semibold mt-0.5">
          {goalMet
            ? `Daily goal met! 🎯 ${todayCorrect} correct today`
            : `${todayCorrect} / ${DAILY_GOAL} questions correct today`}
        </p>
      </div>

      {/* ── Topic grid ──────────────────────────────────────────────────── */}
      <div className="px-4 pt-2">
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          {sortedTopics.map((topic, idx) => {
            const prev         = sortedTopics[idx - 1];
            const showDivider  = idx === 0 || masteryWeight(topic.mastery) !== masteryWeight(prev.mastery);
            const dividerLabel =
              topic.mastery === 'Practicing' ? '📖 In progress' :
              topic.mastery === 'NotStarted' ? '⬜ Not started yet' :
              '✅ Mastered';

            return (
              <Fragment key={topic.id}>
                {showDivider && (
                  <p className="col-span-2 sm:col-span-3 lg:col-span-4 text-[11px] font-extrabold uppercase tracking-widest mt-4 mb-1 text-gray-500">
                    {dividerLabel}
                  </p>
                )}
                <TopicCard
                  topic={topic}
                  onClick={() => router.push(`/practice/${topic.id}`)}
                />
              </Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
}
