'use client';

import React, { Fragment, useEffect, useRef, useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import type { DashboardData, TopicWithProgress } from '@/types';
import Sparky from '@/components/Sparky';
import NudgeBubble from '@/components/NudgeBubble';
import { computeNudge, markMasteryShown, type Nudge } from '@/lib/nudges';
import { getAccessibleGrades, isGradeAccessible } from '@/lib/gradeAccess';
import { getTopicsForGrade, type TopicNode } from '@/data/topicTree';
import { TOPIC_ORDER } from '@/lib/sharedUtils';

// ── Topic metadata ─────────────────────────────────────────────────────────────

const GRADE_EMOJI: Record<number, string> = {
  2: '🌱', 3: '🌿', 4: '🌳', 5: '🍀', 6: '⭐', 7: '🌟', 8: '🏆', 9: '🎯',
};

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
    // Within same mastery group, sort weakest (lowest accuracy) first
    const accA = a.attempted > 0 ? a.correct / a.attempted : 0.5;
    const accB = b.attempted > 0 ? b.correct / b.attempted : 0.5;
    if (Math.abs(accA - accB) > 0.01) return accA - accB;
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

const MasteryBadge = React.memo(function MasteryBadge({ mastery }: { mastery: string }) {
  if (mastery === 'Mastered') {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-extrabold px-2 py-0.5 rounded-full bg-green-100 text-green-700 border border-green-200">
        Mastered ✅
      </span>
    );
  }
  if (mastery === 'Practicing') {
    return (
      <span className="inline-flex items-center gap-1 text-xs font-extrabold px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 border border-amber-200">
        Learning 🟡
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 text-xs font-extrabold px-2 py-0.5 rounded-full bg-gray-100 text-gray-500 border border-gray-200">
      Not started
    </span>
  );
});

const MiniProgressBar = React.memo(function MiniProgressBar({ correct, attempted, mastery }: { correct: number; attempted: number; mastery: string }) {
  const pct = mastery === 'Mastered'
    ? 100
    : attempted > 0
    ? Math.min(100, Math.round((correct / attempted) * 100))
    : 0;

  const barColor =
    mastery === 'Mastered'  ? 'bg-duo-green' :
    mastery === 'Practicing' ? 'bg-duo-orange' :
    'bg-gray-300';

  return (
    <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
      <div
        className={`h-full rounded-full transition-[width] duration-500 ${barColor}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  );
});

const TopicCard = React.memo(function TopicCard({
  topic,
  onClick,
  onFlashcards,
}: {
  topic: TopicWithProgress;
  onClick: () => void;
  onFlashcards?: () => void;
}) {
  const emoji = TOPIC_EMOJI[topic.id] ?? '📚';

  return (
    <div className="w-full text-left bg-white rounded-2xl p-4 shadow-sm border border-gray-100 hover:shadow-md hover:border-duo-blue transition-[colors,border-color,box-shadow] duration-150 flex flex-col gap-2">
      {/* Emoji + mastery badge row */}
      <button onClick={onClick} className="flex items-start justify-between gap-1 active:scale-[0.97] transition-transform">
        <span className="text-3xl leading-none select-none" aria-hidden="true">{emoji}</span>
        <MasteryBadge mastery={topic.mastery} />
      </button>

      {/* Topic name */}
      <button onClick={onClick} className="active:scale-[0.97] transition-transform text-left">
        <p className="text-sm font-extrabold text-gray-800 leading-snug line-clamp-2">
          {topic.name}
        </p>
      </button>

      {/* Questions solved + flashcard link */}
      <div className="flex items-center justify-between">
        <p className="text-xs text-gray-500 font-semibold">
          {topic.correct} question{topic.correct !== 1 ? 's' : ''} solved
        </p>
        {onFlashcards && (
          <button
            onClick={(e) => { e.stopPropagation(); onFlashcards(); }}
            className="text-[10px] font-bold text-emerald-600 bg-emerald-50 border border-emerald-100 rounded-full px-2 py-0.5 hover:bg-emerald-100 transition-colors min-h-0"
          >
            <span aria-hidden="true">🃏 </span>Cards
          </button>
        )}
      </div>

      {/* Mini progress bar */}
      <button onClick={onClick} className="w-full active:scale-[0.97] transition-transform">
        <MiniProgressBar
          correct={topic.correct}
          attempted={topic.attempted}
          mastery={topic.mastery}
        />
      </button>
    </div>
  );
});

// ── Loading skeleton ───────────────────────────────────────────────────────────

function Skeleton() {
  return (
    <div className="min-h-screen bg-white">
      {/* TopBar skeleton */}
      <div className="sticky top-0 z-50 h-14 bg-duo-dark flex items-center justify-between px-4">
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
      {/* Grade tab placeholders */}
      <div className="flex gap-2 px-4 pb-3 overflow-x-auto no-scrollbar">
        {Array.from({ length: 8 }, (_, i) => (
          <div key={i} className="flex-shrink-0 h-8 w-14 rounded-full bg-gray-100 animate-pulse" />
        ))}
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

  const [data,          setData]          = useState<DashboardData | null>(null);
  const [loading,       setLoading]       = useState(true);
  const [hearts,        setHearts]        = useState(5);
  const [nudge,         setNudge]         = useState<Nudge | null>(null);
  // Read from localStorage immediately to avoid Grade 4 flash for non-Grade-4 students
  const [selectedGrade, setSelectedGrade] = useState<number>(() => {
    if (typeof window === 'undefined') return 4;
    const stored = parseInt(localStorage.getItem('mathspark_student_grade') ?? '4', 10);
    return stored >= 2 && stored <= 9 ? stored : 4;
  });
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [lockedGradeTarget, setLockedGradeTarget] = useState<number | null>(null);
  const gradeTabsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setHearts(getHearts());

    const CACHE_KEY = `mathspark_dashboard_${id}`;
    const CACHE_TTL = 5 * 60 * 1000;

    // Check cache first
    try {
      const cached = localStorage.getItem(CACHE_KEY);
      if (cached) {
        const { data: cachedData, ts } = JSON.parse(cached) as { data: DashboardData; ts: number };
        if (Date.now() - ts < CACHE_TTL) {
          setData(cachedData);
          setLoading(false);
          const serverGrade = cachedData.student.grade;
          if (serverGrade >= 2 && serverGrade <= 9) {
            setSelectedGrade(serverGrade);
            localStorage.setItem('mathspark_student_grade', String(serverGrade));
          }
          localStorage.setItem('mathspark_subscription_tier', String(cachedData.subscriptionTier ?? 0));
          const n = computeNudge({
            streakDays:     cachedData.stats.streakDays,
            topicsMastered: cachedData.stats.topicsMastered,
            topics:         cachedData.topics,
          });
          if (n) setNudge(n);
          return;
        }
      }
    } catch { /* ignore parse errors */ }

    // Cache miss — fetch from API
    fetch('/api/dashboard')
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d: DashboardData) => {
        setData(d);
        setLoading(false);
        // Store in cache
        try {
          localStorage.setItem(CACHE_KEY, JSON.stringify({ data: d, ts: Date.now() }));
        } catch { /* ignore storage errors */ }
        // Sync grade from server (source of truth)
        const serverGrade = d.student.grade;
        if (serverGrade >= 2 && serverGrade <= 9) {
          setSelectedGrade(serverGrade);
          localStorage.setItem('mathspark_student_grade', String(serverGrade));
        }
        // Cache subscription tier
        localStorage.setItem('mathspark_subscription_tier', String(d.subscriptionTier ?? 0));
        const n = computeNudge({
          streakDays:     d.stats.streakDays,
          topicsMastered: d.stats.topicsMastered,
          topics:         d.topics,
        });
        if (n) setNudge(n);
      })
      .catch(() => setLoading(false));
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  const studentGrade     = data?.student.grade ?? 4;
  const subscriptionTier = data?.subscriptionTier ?? 0;

  // Accessible grade sets
  const { fullAccess, sampleOnly } = getAccessibleGrades(studentGrade, subscriptionTier);

  // Topics for the selected grade
  const topicsForGrade = useMemo<TopicWithProgress[]>(() => {
    const allT = data?.topics ?? [];
    if (selectedGrade === 4) {
      return allT.filter((t) => TOPIC_ORDER.includes(t.id));
    }
    return allT.filter((t) => t.id === `grade${selectedGrade}`);
  }, [data?.topics, selectedGrade]);

  // Grade 4 IPM pool card (separate from ch-series grid)
  const grade4PoolTopic = useMemo(
    () => selectedGrade === 4 ? (data?.topics ?? []).find((t) => t.id === 'grade4') ?? null : null,
    [data?.topics, selectedGrade],
  );

  // "Also accessible" lower grades (only shown for non-grade-4 selected tabs)
  const lowerGrades = useMemo(
    () => selectedGrade !== 4 ? fullAccess.filter((g) => g < selectedGrade).sort((a, b) => b - a) : [],
    [fullAccess, selectedGrade],
  );

  const sortedTopics = useMemo(() => sortTopics(topicsForGrade), [topicsForGrade]);

  // Syllabus coverage stats (used by the coverage bar)
  const syllabusCoverage = useMemo(() => {
    const started = topicsForGrade.filter((t) => t.attempted >= 5).length;
    const total = topicsForGrade.length || 1;
    const pct = Math.round(started / total * 100);
    return { started, total, pct };
  }, [topicsForGrade]);

  // Weak topics for recommendations
  const weakTopics = useMemo(() => {
    return [...topicsForGrade]
      .filter((t) => t.attempted > 0 && t.mastery !== 'Mastered')
      .sort((a, b) => (a.correct / Math.max(a.attempted, 1)) - (b.correct / Math.max(b.attempted, 1)))
      .slice(0, 2);
  }, [topicsForGrade]);

  if (loading) return <Skeleton />;
  if (!data)   return <Skeleton />;

  const studentName      = data.student.name;
  const streakDays       = data.stats.streakDays;
  const xp               = data.stats.totalLifetimeXP;
  const todayCorrect     = data.weeklyData?.[data.weeklyData.length - 1]?.count ?? 0;
  const goalMet          = todayCorrect >= DAILY_GOAL;

  function handleGradeTabClick(g: number) {
    const access = isGradeAccessible(g, studentGrade, subscriptionTier);
    if (access.locked) {
      setLockedGradeTarget(g);
      setShowUpgradeModal(true);
      return;
    }
    setSelectedGrade(g);
  }

  return (
    <div className="min-h-screen bg-white pb-24 animate-fade-in">
      {/* ── Top bar ─────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-50 h-14 bg-duo-dark/95 backdrop-blur-sm flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="animate-sparky-bounce">
            <Sparky mood="happy" size={30} />
          </div>
          <span className="font-extrabold text-white text-base tracking-tight">MathSpark</span>
        </div>
        <div className="flex items-center gap-3">
          {/* Streak */}
          <div className="flex items-center gap-1 bg-white/15 rounded-full px-2.5 py-1">
            <span className="text-sm" aria-hidden="true">🔥</span>
            <span className="text-white text-xs font-extrabold">{streakDays}</span>
          </div>
          {/* XP */}
          <div className="flex items-center gap-1 bg-white/15 rounded-full px-2.5 py-1">
            <span className="text-sm" aria-hidden="true">💎</span>
            <span className="text-white text-xs font-extrabold">{xp}</span>
          </div>
          {/* Hearts */}
          <div className="flex items-center gap-0.5">
            {[1,2,3,4,5].map((h) => (
              <span
                key={h}
                className="text-sm transition-opacity duration-300"
                style={{ opacity: h <= hearts ? 1 : 0.2 }}
                aria-hidden="true"
              >❤️</span>
            ))}
          </div>
          {/* Avatar */}
          <div className="w-8 h-8 rounded-full bg-duo-gold flex items-center justify-center font-extrabold text-sm text-yellow-900 border-2 border-white">
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
          Hi {studentName}! What shall we practice today? <span aria-hidden="true">🌟</span>
        </h1>
        <p className="text-sm text-gray-500 font-semibold mt-0.5">
          {goalMet
            ? `Daily goal met! 🎯 ${todayCorrect} correct today`
            : `${todayCorrect} / ${DAILY_GOAL} questions correct today`}
        </p>
      </div>

      {/* ── Grade switcher tabs ──────────────────────────────────────────── */}
      <div
        ref={gradeTabsRef}
        className="flex gap-2 px-4 pb-3 overflow-x-auto no-scrollbar"
        style={{ WebkitOverflowScrolling: 'touch' }}
      >
        {[2, 3, 4, 5, 6, 7, 8, 9].map((g) => {
          const access = isGradeAccessible(g, studentGrade, subscriptionTier);
          const isSelected = selectedGrade === g;
          const isEnrolled = g === studentGrade;

          let tabCls = 'flex-shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-full text-xs font-extrabold border-2 transition-colors min-h-0 ';
          if (isSelected) {
            tabCls += 'bg-duo-dark border-duo-dark text-white';
          } else if (access.full) {
            tabCls += 'bg-white border-gray-200 text-gray-700 hover:border-duo-dark';
          } else if (access.sample) {
            tabCls += 'bg-white border-blue-200 text-blue-600 hover:border-blue-400';
          } else {
            tabCls += 'bg-gray-50 border-gray-100 text-gray-500 opacity-75';
          }

          return (
            <button
              key={g}
              onClick={() => handleGradeTabClick(g)}
              className={tabCls}
            >
              <span aria-hidden="true">{GRADE_EMOJI[g]}</span>
              <span>Gr {g}</span>
              {isEnrolled && !isSelected && (
                <span className="w-1.5 h-1.5 rounded-full bg-duo-green" />
              )}
              {access.sample && <span className="text-[10px]">🔓</span>}
              {access.locked && <span className="text-[10px]">🔒</span>}
            </button>
          );
        })}
      </div>

      {/* ── Syllabus Coverage Bar ────────────────────────────────────────── */}
      <div className="px-4 pb-3">
        <div className="flex items-center justify-between text-xs font-extrabold text-gray-500 uppercase tracking-wide mb-1.5">
          <span>Syllabus Coverage</span>
          <span>{syllabusCoverage.started} / {syllabusCoverage.total} topics started</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-[width] duration-700"
            style={{
              width: `${syllabusCoverage.pct}%`,
              background: 'linear-gradient(to right, #1CB0F6, #58CC02)',
            }}
          />
        </div>
      </div>

      {/* ── Recommended Topics (from weak + low-coverage topics) ──────────── */}
      {selectedGrade === (data.student.grade ?? 4) && weakTopics.length > 0 && (
        <div className="px-4 pb-3">
          <p className="text-xs font-extrabold uppercase tracking-widest mb-2 text-gray-500">
            <span aria-hidden="true">🎯 </span>Recommended for You
          </p>
          <div className="space-y-2">
            {weakTopics.map((t) => {
              const pct = t.attempted > 0 ? Math.round(t.correct / t.attempted * 100) : 0;
              const emoji = TOPIC_EMOJI[t.id] ?? '📚';
              return (
                <button
                  key={t.id}
                  onClick={() => router.push(`/practice/${t.id}`)}
                  className="w-full flex items-center gap-3 bg-[#1a2d35] rounded-xl px-3 py-3 border-l-4 border-duo-green active:scale-[0.98] transition-transform text-left"
                >
                  <span className="text-xl shrink-0" aria-hidden="true">{emoji}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-extrabold text-sm truncate">{t.name}</p>
                    <p className="text-white/70 text-xs font-medium">
                      {pct}% accuracy · {t.attempted} attempts
                    </p>
                  </div>
                  <span className="text-duo-green text-xs font-extrabold shrink-0">Practice →</span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* ── Flashcard review banner ─────────────────────────────────────── */}
      <div className="px-4 pt-1">
        <button
          onClick={() => router.push('/flashcards')}
          className="w-full bg-gradient-to-r from-[#1E293B] to-[#1a2d40] border border-duo-green/20 rounded-2xl px-4 py-3.5 flex items-center gap-3 mb-3 active:scale-[0.98] transition-transform"
        >
          <span className="text-2xl" aria-hidden="true">🃏</span>
          <div className="text-left flex-1">
            <p className="text-white font-extrabold text-sm leading-tight">Sparky&apos;s Flashcards</p>
            <p className="text-emerald-400/70 text-xs">Tap · Flip · Master concepts</p>
          </div>
          <span className="text-emerald-400 text-sm font-bold">Review →</span>
        </button>
      </div>

      {/* ── Mock test entry card ────────────────────────────────────────── */}
      <div className="px-4 pt-0">
        <button
          onClick={() => router.push('/test')}
          className="w-full bg-[#1a2f3a] border border-white/10 rounded-2xl px-4 py-3.5 flex items-center gap-3 mb-3 active:scale-[0.98] transition-transform"
        >
          <span className="text-2xl" aria-hidden="true">📝</span>
          <div className="text-left flex-1">
            <p className="text-white font-extrabold text-sm leading-tight">IPM Mock Test</p>
            <p className="text-white/70 text-xs">Timed · No hints · Full paper simulation</p>
          </div>
          <span className="text-white/60 text-sm">→</span>
        </button>
      </div>

      {/* ── Topic content for selected grade ────────────────────────────── */}
      <div className="px-4 pt-0">
        {selectedGrade === 4 ? (
          // Grade 4: ch-series grid + IPM pool card at bottom
          <>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
              {sortedTopics.map((topic, idx) => {
                const prev        = sortedTopics[idx - 1];
                const showDivider = idx === 0 || masteryWeight(topic.mastery) !== masteryWeight(prev.mastery);
                const dividerLabel =
                  topic.mastery === 'Practicing' ? '📖 In progress' :
                  topic.mastery === 'NotStarted' ? '⬜ Not started yet' :
                  '✅ Mastered';

                return (
                  <Fragment key={topic.id}>
                    {showDivider && (
                      <p className="col-span-2 sm:col-span-3 lg:col-span-4 text-xs font-extrabold uppercase tracking-widest mt-4 mb-1 text-gray-500">
                        {dividerLabel}
                      </p>
                    )}
                    <TopicCard
                      topic={topic}
                      onClick={() => router.push(`/practice/${topic.id}`)}
                      onFlashcards={() => router.push(`/flashcards/session?deck=${topic.id}&mode=classic`)}
                    />
                  </Fragment>
                );
              })}
            </div>

            {/* Grade 4 IPM Past Papers card */}
            {grade4PoolTopic && (
              <div className="mt-6">
                <p className="text-xs font-extrabold uppercase tracking-widest mb-2 text-gray-500">
                  <span aria-hidden="true">📄 </span>IPM Past Papers
                </p>
                <button
                  onClick={() => router.push('/practice/grade4')}
                  className="w-full text-left bg-gradient-to-r from-duo-dark to-[#1a3040] rounded-2xl p-4 flex items-center gap-4 active:scale-[0.98] transition-transform"
                >
                  <span className="text-3xl" aria-hidden="true">🏆</span>
                  <div className="flex-1">
                    <p className="text-white font-extrabold text-sm">Grade 4 — IPM Past Papers</p>
                    <p className="text-white/60 text-xs mt-0.5">
                      {grade4PoolTopic.correct} correct · {grade4PoolTopic.mastery === 'Mastered' ? '✅ Mastered' : grade4PoolTopic.mastery === 'Practicing' ? '🟡 In progress' : 'Not started'}
                    </p>
                  </div>
                  <span className="text-white/60 text-sm">→</span>
                </button>
              </div>
            )}
          </>
        ) : (
          // Other grades: topicTree lesson cards + lower-grade tiles
          <>
            {/* Lesson grid from topicTree */}
            {(() => {
              const treeNodes: TopicNode[] = getTopicsForGrade(selectedGrade);
              const access = isGradeAccessible(selectedGrade, studentGrade, subscriptionTier);
              const isSample = access.sample;
              const poolTopic = topicsForGrade[0]; // the single gradeN DB topic (for correct count)

              if (!treeNodes.length) {
                return (
                  <div className="text-center py-12 text-gray-500">
                    <p className="font-semibold">No lessons available yet for Grade {selectedGrade}</p>
                  </div>
                );
              }

              return (
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
                  {treeNodes.map((node) => (
                    <button
                      key={node.id}
                      onClick={() => {
                        const qp = new URLSearchParams();
                        if (node.subTopicKey) qp.set('subTopic', node.subTopicKey);
                        if (isSample) qp.set('sample', 'true');
                        const qs = qp.toString() ? `?${qp.toString()}` : '';
                        router.push(`/practice/${node.dbTopicId}${qs}`);
                      }}
                      className="w-full text-left bg-white rounded-2xl p-4 shadow-sm border border-gray-100 hover:shadow-md hover:border-duo-blue active:scale-[0.97] transition-[colors,border-color,box-shadow,transform] duration-150 flex flex-col gap-2"
                    >
                      <div className="flex items-start justify-between gap-1">
                        <span className="text-3xl leading-none select-none" aria-hidden="true">{node.emoji}</span>
                        {isSample && (
                          <span className="inline-flex items-center text-xs font-extrabold px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 border border-blue-200">
                            Preview 🔓
                          </span>
                        )}
                      </div>
                      <p className="text-sm font-extrabold text-gray-800 leading-snug line-clamp-2">
                        {node.name}
                      </p>
                      <p className="text-xs text-gray-500 font-semibold">
                        {poolTopic ? `${poolTopic.correct} solved in pool` : 'Not started'}
                      </p>
                      <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full bg-duo-blue"
                          style={{ width: poolTopic && poolTopic.mastery === 'Mastered' ? '100%' : poolTopic && poolTopic.mastery === 'Practicing' ? '50%' : '0%' }}
                        />
                      </div>
                    </button>
                  ))}
                </div>
              );
            })()}

            {/* Also accessible: lower grades */}
            {lowerGrades.length > 0 && (
              <div className="mt-6">
                <p className="text-xs font-extrabold uppercase tracking-widest mb-2 text-gray-500">
                  Also accessible
                </p>
                <div className="grid grid-cols-2 gap-2">
                  {lowerGrades.map((g) => {
                    const t = data.topics.find((x) => x.id === `grade${g}`);
                    return (
                      <button
                        key={g}
                        onClick={() => { setSelectedGrade(g); }}
                        className="bg-gray-50 border border-gray-100 rounded-2xl p-3 flex items-center gap-2 active:scale-[0.97] transition-transform text-left min-h-0"
                      >
                        <span className="text-xl" aria-hidden="true">{GRADE_EMOJI[g]}</span>
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-extrabold text-gray-700 truncate">Grade {g}</p>
                          <p className="text-[10px] text-gray-500">
                            {t ? `${t.correct} solved` : 'Not started'}
                          </p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* ── Upgrade modal for locked grades ────────────────────────────── */}
      {showUpgradeModal && lockedGradeTarget && (
        <div className="fixed inset-0 z-[100] flex items-end justify-center bg-black/50 p-4">
          <div className="bg-white rounded-3xl p-6 w-full max-w-sm shadow-2xl space-y-4 animate-slide-up">
            <div className="text-center">
              <span className="text-5xl" aria-hidden="true">🔒</span>
              <h3 className="text-xl font-extrabold text-gray-800 mt-2">
                Grade {lockedGradeTarget} is locked
              </h3>
              <p className="text-gray-500 text-sm mt-1">
                Upgrade your plan to access Grade {lockedGradeTarget} {GRADE_EMOJI[lockedGradeTarget]} questions
              </p>
            </div>
            <button
              onClick={() => { setShowUpgradeModal(false); router.push('/pricing'); }}
              className="w-full min-h-[48px] bg-duo-blue text-white font-extrabold rounded-full text-sm"
            >
              Upgrade Plan 🚀
            </button>
            <button
              onClick={() => setShowUpgradeModal(false)}
              style={{ minHeight: 0 }}
              className="w-full text-center text-gray-500 text-sm font-semibold py-2"
            >
              Not now
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
