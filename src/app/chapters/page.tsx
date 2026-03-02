'use client';

import { Fragment, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { DashboardData, TopicWithProgress } from '@/types';
import Sparky from '@/components/Sparky';
import NudgeBubble from '@/components/NudgeBubble';
import { computeNudge, markMasteryShown, type Nudge } from '@/lib/nudges';
import { getAccessibleGrades, isGradeAccessible } from '@/lib/gradeAccess';

// ── Topic metadata ─────────────────────────────────────────────────────────────

const CH_TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

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
    return CH_TOPIC_ORDER.indexOf(a.id) - CH_TOPIC_ORDER.indexOf(b.id);
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

  const [data,          setData]          = useState<DashboardData | null>(null);
  const [loading,       setLoading]       = useState(true);
  const [hearts,        setHearts]        = useState(5);
  const [nudge,         setNudge]         = useState<Nudge | null>(null);
  const [selectedGrade, setSelectedGrade] = useState<number>(4);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [lockedGradeTarget, setLockedGradeTarget] = useState<number | null>(null);
  const gradeTabsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const id = localStorage.getItem('mathspark_student_id');
    if (!id) { router.replace('/start'); return; }
    setHearts(getHearts());

    // Initialise selectedGrade from localStorage
    const storedGrade = parseInt(localStorage.getItem('mathspark_student_grade') ?? '4', 10);
    if (storedGrade >= 2 && storedGrade <= 9) setSelectedGrade(storedGrade);

    fetch(`/api/dashboard?studentId=${id}`)
      .then((r) => r.json())
      .then((d: DashboardData) => {
        setData(d);
        setLoading(false);
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
  }, [router]);

  if (loading) return <Skeleton />;
  if (!data)   return <Skeleton />;

  const studentName      = data.student.name;
  const studentGrade     = data.student.grade ?? 4;
  const subscriptionTier = data.subscriptionTier ?? 0;
  const streakDays       = data.stats.streakDays;
  const xp               = data.stats.totalSolved * 10;
  const todayCorrect     = data.weeklyData?.[data.weeklyData.length - 1]?.count ?? 0;
  const goalMet          = todayCorrect >= DAILY_GOAL;

  // Accessible grade sets
  const { fullAccess, sampleOnly } = getAccessibleGrades(studentGrade, subscriptionTier);

  // Topics for the selected grade
  const topicsForGrade: TopicWithProgress[] = (() => {
    const allT = data.topics;
    if (selectedGrade === 4) {
      // Grade 4: ch-series + grade4 pool (shown separately at bottom)
      return allT.filter((t) => CH_TOPIC_ORDER.includes(t.id));
    }
    // Other grades: only the gradeN pool topic
    return allT.filter((t) => t.id === `grade${selectedGrade}`);
  })();

  // Grade 4 IPM pool card (separate from ch-series grid)
  const grade4PoolTopic = selectedGrade === 4
    ? data.topics.find((t) => t.id === 'grade4')
    : null;

  // "Also accessible" lower grades (only shown for non-grade-4 selected tabs)
  const lowerGrades = selectedGrade !== 4
    ? fullAccess.filter((g) => g < selectedGrade).sort((a, b) => b - a)
    : [];

  const sortedTopics = sortTopics(topicsForGrade);

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
        <p className="text-sm text-gray-400 font-semibold mt-0.5">
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

          let tabCls = 'flex-shrink-0 flex items-center gap-1.5 px-3 py-2 rounded-full text-xs font-extrabold border-2 transition-all ';
          if (isSelected) {
            tabCls += 'bg-[#131F24] border-[#131F24] text-white';
          } else if (access.full) {
            tabCls += 'bg-white border-gray-200 text-gray-700 hover:border-[#131F24]';
          } else if (access.sample) {
            tabCls += 'bg-white border-blue-200 text-blue-600 hover:border-blue-400';
          } else {
            tabCls += 'bg-gray-50 border-gray-100 text-gray-400 opacity-75';
          }

          return (
            <button
              key={g}
              onClick={() => handleGradeTabClick(g)}
              style={{ minHeight: 0 }}
              className={tabCls}
            >
              <span>{GRADE_EMOJI[g]}</span>
              <span>Gr {g}</span>
              {isEnrolled && !isSelected && (
                <span className="w-1.5 h-1.5 rounded-full bg-[#58CC02]" />
              )}
              {access.sample && <span className="text-[10px]">🔓</span>}
              {access.locked && <span className="text-[10px]">🔒</span>}
            </button>
          );
        })}
      </div>

      {/* ── Syllabus Coverage Bar ────────────────────────────────────────── */}
      {(() => {
        const gradeTopics = selectedGrade === 4
          ? data.topics.filter((t) => CH_TOPIC_ORDER.includes(t.id))
          : data.topics.filter((t) => t.id === `grade${selectedGrade}`);
        const started = gradeTopics.filter((t) => t.attempted >= 5).length;
        const total   = gradeTopics.length || 1;
        const pct     = Math.round(started / total * 100);
        return (
          <div className="px-4 pb-3">
            <div className="flex items-center justify-between text-[11px] font-extrabold text-gray-400 uppercase tracking-wide mb-1.5">
              <span>Syllabus Coverage</span>
              <span>{started} / {total} topics started</span>
            </div>
            <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-700"
                style={{
                  width: `${pct}%`,
                  background: 'linear-gradient(to right, #1CB0F6, #58CC02)',
                }}
              />
            </div>
          </div>
        );
      })()}

      {/* ── Recommended Topics (from weak + low-coverage topics) ──────────── */}
      {selectedGrade === (data.student.grade ?? 4) && (() => {
        const gradeTopics = selectedGrade === 4
          ? data.topics.filter((t) => CH_TOPIC_ORDER.includes(t.id))
          : data.topics.filter((t) => t.id === `grade${selectedGrade}`);
        // Sort by accuracy ascending, pick top 2 weak topics with attempts
        const weak = [...gradeTopics]
          .filter((t) => t.attempted > 0 && t.mastery !== 'Mastered')
          .sort((a, b) => (a.correct / Math.max(a.attempted, 1)) - (b.correct / Math.max(b.attempted, 1)))
          .slice(0, 2);
        if (!weak.length) return null;
        return (
          <div className="px-4 pb-3">
            <p className="text-[11px] font-extrabold uppercase tracking-widest mb-2 text-gray-500">
              🎯 Recommended for You
            </p>
            <div className="space-y-2">
              {weak.map((t) => {
                const pct = t.attempted > 0 ? Math.round(t.correct / t.attempted * 100) : 0;
                const emoji = TOPIC_EMOJI[t.id] ?? '📚';
                return (
                  <button
                    key={t.id}
                    onClick={() => router.push(`/practice/${t.id}`)}
                    className="w-full flex items-center gap-3 bg-[#1a2d35] rounded-xl px-3 py-3 border-l-4 border-[#58CC02] active:scale-[0.98] transition-all text-left"
                  >
                    <span className="text-xl shrink-0">{emoji}</span>
                    <div className="flex-1 min-w-0">
                      <p className="text-white font-extrabold text-sm truncate">{t.name}</p>
                      <p className="text-white/50 text-xs font-medium">
                        {pct}% accuracy · {t.attempted} attempts
                      </p>
                    </div>
                    <span className="text-[#58CC02] text-xs font-extrabold shrink-0">Practice →</span>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })()}

      {/* ── Mock test entry card ────────────────────────────────────────── */}
      <div className="px-4 pt-1">
        <button
          onClick={() => router.push('/test')}
          className="w-full bg-[#1a2f3a] border border-white/10 rounded-2xl px-4 py-3.5 flex items-center gap-3 mb-3 active:scale-[0.98] transition-all"
        >
          <span className="text-2xl">📝</span>
          <div className="text-left flex-1">
            <p className="text-white font-extrabold text-sm leading-tight">IPM Mock Test</p>
            <p className="text-white/50 text-xs">Timed · No hints · Full paper simulation</p>
          </div>
          <span className="text-white/40 text-sm">→</span>
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

            {/* Grade 4 IPM Past Papers card */}
            {grade4PoolTopic && (
              <div className="mt-6">
                <p className="text-[11px] font-extrabold uppercase tracking-widest mb-2 text-gray-500">
                  📄 IPM Past Papers
                </p>
                <button
                  onClick={() => router.push('/practice/grade4')}
                  className="w-full text-left bg-gradient-to-r from-[#131F24] to-[#1a3040] rounded-2xl p-4 flex items-center gap-4 active:scale-[0.98] transition-all"
                >
                  <span className="text-3xl">🏆</span>
                  <div className="flex-1">
                    <p className="text-white font-extrabold text-sm">Grade 4 — IPM Past Papers</p>
                    <p className="text-white/60 text-xs mt-0.5">
                      {grade4PoolTopic.correct} correct · {grade4PoolTopic.mastery === 'Mastered' ? '✅ Mastered' : grade4PoolTopic.mastery === 'Practicing' ? '🟡 In progress' : 'Not started'}
                    </p>
                  </div>
                  <span className="text-white/40 text-sm">→</span>
                </button>
              </div>
            )}
          </>
        ) : (
          // Other grades: single large topic card + lower-grade tiles
          <>
            {/* Main grade topic */}
            {topicsForGrade.length > 0 ? (
              <div className="space-y-3">
                {topicsForGrade.map((topic) => {
                  const access = isGradeAccessible(selectedGrade, studentGrade, subscriptionTier);
                  const isSample = access.sample;
                  return (
                    <button
                      key={topic.id}
                      onClick={() => router.push(`/practice/${topic.id}${isSample ? '?sample=true' : ''}`)}
                      className="w-full text-left bg-gradient-to-r from-[#131F24] to-[#1a3040] rounded-2xl p-5 flex items-center gap-4 active:scale-[0.98] transition-all shadow-lg"
                    >
                      <span className="text-4xl">{GRADE_EMOJI[selectedGrade]}</span>
                      <div className="flex-1">
                        <p className="text-white font-extrabold text-base">{topic.name}</p>
                        <p className="text-white/60 text-xs mt-0.5">
                          {isSample ? '5 free preview questions 🔓' : `${topic.correct} correct · ${
                            topic.mastery === 'Mastered' ? '✅ Mastered' :
                            topic.mastery === 'Practicing' ? '🟡 In progress' : 'Not started'
                          }`}
                        </p>
                      </div>
                      <span className="text-white/40 text-lg">→</span>
                    </button>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <p className="font-semibold">No questions available yet for Grade {selectedGrade}</p>
              </div>
            )}

            {/* Also accessible: lower grades */}
            {lowerGrades.length > 0 && (
              <div className="mt-6">
                <p className="text-[11px] font-extrabold uppercase tracking-widest mb-2 text-gray-500">
                  Also accessible
                </p>
                <div className="grid grid-cols-2 gap-2">
                  {lowerGrades.map((g) => {
                    const t = data.topics.find((x) => x.id === `grade${g}`);
                    return (
                      <button
                        key={g}
                        onClick={() => { setSelectedGrade(g); }}
                        style={{ minHeight: 0 }}
                        className="bg-gray-50 border border-gray-100 rounded-2xl p-3 flex items-center gap-2 active:scale-[0.97] transition-all text-left"
                      >
                        <span className="text-xl">{GRADE_EMOJI[g]}</span>
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-extrabold text-gray-700 truncate">Grade {g}</p>
                          <p className="text-[10px] text-gray-400">
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
              <span className="text-5xl">🔒</span>
              <h3 className="text-xl font-extrabold text-gray-800 mt-2">
                Grade {lockedGradeTarget} is locked
              </h3>
              <p className="text-gray-500 text-sm mt-1">
                Upgrade your plan to access Grade {lockedGradeTarget} {GRADE_EMOJI[lockedGradeTarget]} questions
              </p>
            </div>
            <button
              onClick={() => { setShowUpgradeModal(false); router.push('/pricing'); }}
              className="w-full min-h-[48px] bg-[#1CB0F6] text-white font-extrabold rounded-full text-sm"
            >
              Upgrade Plan 🚀
            </button>
            <button
              onClick={() => setShowUpgradeModal(false)}
              style={{ minHeight: 0 }}
              className="w-full text-center text-gray-400 text-sm font-semibold py-2"
            >
              Not now
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
