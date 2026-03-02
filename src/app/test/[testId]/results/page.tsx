'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import KatexRenderer from '@/components/KatexRenderer';
import ShareSheet from '@/components/ShareSheet';
import type { MockTestDetail, MockTestResponse, TopicResult, Recommendation } from '@/types';

// ── Topic metadata ────────────────────────────────────────────────────────────

const TOPIC_NAMES: Record<string, string> = {
  'ch01-05': 'Number System & Place Value', 'ch06': 'Factors & Multiples',
  'ch07-08': 'Fractions',                  'ch09-10': 'Operations & BODMAS',
  'ch11':    'Decimal Fractions',          'ch12': 'Decimal Units',
  'ch13':    'Algebraic Expressions',      'ch14': 'Equations',
  'ch15':    'Puzzles & Magic Squares',    'ch16': 'Sequence & Series',
  'ch17':    'Time & Calendar',            'ch18': 'Angles',
  'ch19':    'Triangles',                  'ch20': 'Quadrilaterals',
  'ch21':    'Circle',                     'dh':   'Data Handling',
  // Grade pool topics
  'grade2':  'Grade 2 Practice',
  'grade3':  'Grade 3 Practice',
  'grade4':  'Grade 4 IPM Pool',
  'grade5':  'Grade 5 Practice',
  'grade6':  'Grade 6 Practice',
  'grade7':  'Grade 7 Practice',
  'grade8':  'Grade 8 Practice',
  'grade9':  'Grade 9 Practice',
};

const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06': '🔑', 'ch07-08': '🍕', 'ch09-10': '➗',
  'ch11': '📊', 'ch12': '📏', 'ch13': '🔤', 'ch14': '⚖️',
  'ch15': '🧩', 'ch16': '🔢', 'ch17': '🕐', 'ch18': '📐',
  'ch19': '🔺', 'ch20': '⬜', 'ch21': '⭕', 'dh': '📈',
  'grade2': '🌱', 'grade3': '🌿', 'grade4': '🎯',
  'grade5': '⭐', 'grade6': '🌟', 'grade7': '🏆',
  'grade8': '🔥', 'grade9': '💎',
};

// ── Helpers ───────────────────────────────────────────────────────────────────

function formatMs(ms: number): string {
  const s = Math.floor(ms / 1000);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  const rem = s % 60;
  return rem > 0 ? `${m}m ${rem}s` : `${m}m`;
}

function formatTime(ms: number): string {
  const totalSec = Math.floor(ms / 1000);
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function getGradeBand(pct: number): { label: string; color: string } {
  if (pct >= 90) return { label: 'Outstanding! 🏆', color: 'text-[#58CC02]' };
  if (pct >= 80) return { label: 'Excellent! ⭐',   color: 'text-[#58CC02]' };
  if (pct >= 70) return { label: 'Good work! 👍',   color: 'text-[#1CB0F6]' };
  if (pct >= 60) return { label: 'Keep going! 💪',  color: 'text-[#FF9600]' };
  return { label: 'More practice needed 📚', color: 'text-[#FF4B4B]' };
}

// ── Analytics computation ─────────────────────────────────────────────────────

function computeTopicResults(responses: MockTestResponse[]): TopicResult[] {
  const map = new Map<string, { correct: number; total: number; timeMs: number }>();
  for (const r of responses) {
    if (!r.question) continue;
    const tid = r.question.topicId;
    if (!map.has(tid)) map.set(tid, { correct: 0, total: 0, timeMs: 0 });
    const entry = map.get(tid)!;
    entry.total++;
    if (r.isCorrect) entry.correct++;
    entry.timeMs += r.timeTakenMs ?? 0;
  }
  return Array.from(map.entries()).map(([topicId, { correct, total, timeMs }]) => ({
    topicId,
    topicName: TOPIC_NAMES[topicId] ?? topicId,
    correct,
    total,
    accuracy: total > 0 ? correct / total : 0,
    avgTimeMs: total > 0 ? timeMs / total : 0,
  })).sort((a, b) => a.accuracy - b.accuracy);
}

function computeRecommendations(topicResults: TopicResult[]): Recommendation[] {
  const recs: Recommendation[] = [];
  for (const t of topicResults) {
    if (t.accuracy < 0.6) {
      recs.push({ type: 'priority', topicId: t.topicId, topicName: t.topicName, reason: `${Math.round(t.accuracy * 100)}% accuracy — needs focused practice` });
    } else if (t.avgTimeMs > 90_000) {
      recs.push({ type: 'speed', topicId: t.topicId, topicName: t.topicName, reason: `Avg ${formatMs(t.avgTimeMs)} per question — practice for speed` });
    } else if (t.accuracy >= 0.8) {
      recs.push({ type: 'strength', topicId: t.topicId, topicName: t.topicName, reason: `${Math.round(t.accuracy * 100)}% — great work!` });
    }
  }
  // Sort: priority first, then speed, then strength
  return recs.sort((a, b) => {
    const order = { priority: 0, speed: 1, strength: 2 };
    return order[a.type] - order[b.type];
  });
}

// ── Score ring SVG ────────────────────────────────────────────────────────────

function ScoreRing({ pct, score, total }: { pct: number; score: number; total: number }) {
  const r = 54;
  const circ = 2 * Math.PI * r;
  const dash = circ * (pct / 100);
  const color = pct >= 70 ? '#58CC02' : pct >= 40 ? '#FF9600' : '#FF4B4B';
  const trackColor = pct >= 70 ? '#E5F9CC' : pct >= 40 ? '#FFF3CD' : '#FFE4E4';

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width="140" height="140" className="-rotate-90">
        <circle cx="70" cy="70" r={r} fill="none" stroke={trackColor} strokeWidth="12" />
        <circle
          cx="70" cy="70" r={r} fill="none" stroke={color} strokeWidth="12"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          style={{ transition: 'stroke-dasharray 1.2s ease-out' }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-extrabold text-gray-800">{score}</span>
        <span className="text-gray-400 text-sm font-bold">/{total}</span>
      </div>
    </div>
  );
}

// ── Section: Accordion item for question playback ─────────────────────────────

function QuestionAccordion({ r, idx }: { r: MockTestResponse; idx: number }) {
  const [open, setOpen] = useState(false);
  const router = useRouter();
  if (!r.question) return null;

  const q = r.question;
  const options: Array<{ key: string; text: string }> = [
    { key: 'A', text: q.option1 }, { key: 'B', text: q.option2 },
    { key: 'C', text: q.option3 }, { key: 'D', text: q.option4 },
  ];

  const misconception =
    r.selectedAnswer === 'A' ? q.misconceptionA :
    r.selectedAnswer === 'B' ? q.misconceptionB :
    r.selectedAnswer === 'C' ? q.misconceptionC :
    r.selectedAnswer === 'D' ? q.misconceptionD : '';

  return (
    <div className="border-2 border-gray-100 rounded-2xl overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full text-left px-4 py-3 flex items-center gap-3 hover:bg-gray-50 transition-colors"
      >
        <span className="text-xs font-extrabold text-gray-400 w-8 flex-shrink-0">Q{idx + 1}</span>
        <span className="flex-1 text-sm font-semibold text-gray-700 line-clamp-1">{q.questionText}</span>
        <span className="text-xs text-gray-400 flex-shrink-0">{r.timeTakenMs ? formatMs(r.timeTakenMs) : '—'}</span>
        <span className="text-lg flex-shrink-0">{r.isCorrect ? '✅' : r.selectedAnswer ? '❌' : '⬜'}</span>
        <span className="text-gray-300 text-sm">{open ? '▲' : '▼'}</span>
      </button>

      {open && (
        <div className="px-4 pb-4 border-t border-gray-100 pt-3 space-y-3">
          <p className="text-gray-700 text-sm font-medium">{q.questionText}</p>
          {q.questionLatex && <KatexRenderer latex={q.questionLatex} />}

          <div className="space-y-2">
            {options.map(({ key, text }) => {
              const isSelected = r.selectedAnswer === key;
              const isCorrect  = q.correctAnswer === key;
              const cls =
                isCorrect  ? 'bg-green-50 border-[#58CC02] text-green-800' :
                isSelected ? 'bg-red-50 border-[#FF4B4B] text-red-800' :
                             'bg-white border-gray-200 text-gray-600';
              return (
                <div key={key} className={`flex items-center gap-2 px-3 py-2 rounded-xl border-2 text-sm ${cls}`}>
                  <span className="font-extrabold w-5 flex-shrink-0">{key}</span>
                  <span>{text}</span>
                  {isCorrect && <span className="ml-auto text-[#58CC02]">✓</span>}
                  {isSelected && !isCorrect && <span className="ml-auto text-[#FF4B4B]">✗</span>}
                </div>
              );
            })}
          </div>

          {!r.isCorrect && misconception && (
            <div className="bg-blue-50 border-2 border-[#1CB0F6] rounded-xl px-3 py-2">
              <p className="text-xs font-extrabold text-[#1CB0F6] mb-0.5">💡 Common mistake</p>
              <p className="text-xs text-blue-800 font-medium">{misconception}</p>
            </div>
          )}

          <button
            onClick={() => router.push(`/practice/${q.topicId}`)}
            className="w-full min-h-[40px] rounded-xl bg-[#1CB0F6]/10 border-2 border-[#1CB0F6]/30 text-[#1CB0F6] font-bold text-sm hover:bg-[#1CB0F6]/20 transition-colors"
          >
            Practice similar →
          </button>
        </div>
      )}
    </div>
  );
}

// ── Main results page ─────────────────────────────────────────────────────────

export default function TestResultsPage() {
  const router  = useRouter();
  const { testId } = useParams<{ testId: string }>();

  const [test,          setTest]         = useState<MockTestDetail | null>(null);
  const [loading,       setLoading]      = useState(true);
  const [showConfetti,  setShowConfetti] = useState(false);
  const [activeSection, setActiveSection] = useState<string>('topics');
  const [showShare,     setShowShare]    = useState(false);
  const [shareInfo,     setShareInfo]    = useState({ studentId: '', studentName: '', parentEmail: '', parentWhatsApp: '' });

  useEffect(() => {
    setShareInfo({
      studentId:      localStorage.getItem('mathspark_student_id')      ?? '',
      studentName:    localStorage.getItem('mathspark_student_name')    ?? '',
      parentEmail:    localStorage.getItem('mathspark_parent_email')    ?? '',
      parentWhatsApp: localStorage.getItem('mathspark_parent_whatsapp') ?? '',
    });

    async function load() {
      try {
        const res = await fetch(`/api/mock-tests/${testId}`);
        if (!res.ok) { router.replace('/test'); return; }
        const data: MockTestDetail = await res.json();
        setTest(data);
        if ((data.score ?? 0) / data.totalQuestions >= 0.8) {
          setShowConfetti(true);
        }
        setLoading(false);
      } catch {
        router.replace('/test');
      }
    }
    load();
  }, [testId, router]);

  if (loading || !test) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-[#58CC02]/30 border-t-[#58CC02] rounded-full animate-spin" />
      </div>
    );
  }

  const score    = test.score ?? 0;
  const total    = test.totalQuestions;
  const pct      = Math.round((score / total) * 100);
  const grade    = getGradeBand(pct);
  const topicResults = computeTopicResults(test.responses);
  const recommendations = computeRecommendations(topicResults);

  // Difficulty breakdown
  const diffBreakdown = (['Easy', 'Medium', 'Hard'] as const).map((diff) => {
    const relevant = test.responses.filter((r) => r.question?.difficulty === diff);
    const correct  = relevant.filter((r) => r.isCorrect).length;
    return { diff, correct, total: relevant.length };
  });

  // Time used
  const timeUsedMs = test.completedAt && test.startedAt
    ? new Date(test.completedAt).getTime() - new Date(test.startedAt).getTime()
    : null;

  // Slowest questions for time analysis
  const slowest = [...test.responses]
    .filter((r) => r.timeTakenMs > 0)
    .sort((a, b) => b.timeTakenMs - a.timeTakenMs)
    .slice(0, 10);
  const avgTimeMs = test.responses.reduce((s, r) => s + (r.timeTakenMs ?? 0), 0) / total;

  const SECTIONS = [
    { id: 'topics',    label: '📊 Topics'    },
    { id: 'difficulty',label: '📈 Difficulty' },
    { id: 'time',      label: '⏱ Time'       },
    { id: 'playback',  label: '📋 All Qs'    },
    { id: 'plan',      label: '🗺 Study Plan' },
  ];

  return (
    <div className="min-h-screen bg-white pb-8">
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

      {/* ── Share sheet ───────────────────────────────────────────────────── */}
      {showShare && shareInfo.studentId && (
        <ShareSheet
          card={{ type: 'mocktest', data: {
            studentName: shareInfo.studentName || 'Student',
            score,
            totalQ: total,
            pct,
            gradeLabel: grade.label,
            strongTopic: topicResults.length > 0 ? topicResults[topicResults.length - 1].topicName : 'Mixed',
            weakTopic:   topicResults.length > 0 ? topicResults[0].topicName : 'Mixed',
            timeUsedMs:  timeUsedMs ?? 0,
            timeLimitMs: test.timeLimitMs,
          }}}
          studentId={shareInfo.studentId}
          parentEmail={shareInfo.parentEmail || undefined}
          parentWhatsApp={shareInfo.parentWhatsApp || undefined}
          onClose={() => setShowShare(false)}
        />
      )}

      {/* ── Score header ─────────────────────────────────────────────────── */}
      <div className="bg-gradient-to-b from-[#131F24] to-[#1a3040] px-4 pt-8 pb-6 text-center">
        <ScoreRing pct={pct} score={score} total={total} />
        <h1 className={`text-2xl font-extrabold mt-3 ${grade.color}`}>{grade.label}</h1>
        <p className="text-white/70 text-sm font-semibold mt-1">
          {pct}% accuracy
          {timeUsedMs != null && ` · ${formatTime(timeUsedMs)} used`}
        </p>
        <div className="mt-2 flex items-center justify-center gap-2">
          <span className="inline-block bg-white/10 text-white/80 text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wide">
            {test.type === 'quick' ? 'Quick Test' : test.type === 'half' ? 'Half Paper' : test.type === 'ipm' ? 'IPM Blueprint' : test.type === 'pyq' ? 'Past Year Paper' : test.type === 'mega' ? 'Mega Final' : 'Full Paper'}
          </span>
          <button
            onClick={() => setShowShare(true)}
            style={{ minHeight: 0 }}
            className="bg-white/10 hover:bg-white/20 text-white text-xs font-extrabold px-3 py-1 rounded-full transition-colors"
          >
            📤 Share
          </button>
        </div>
      </div>

      {/* ── Section tabs ─────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-40 bg-white border-b border-gray-100 overflow-x-auto">
        <div className="flex px-2 py-2 gap-1 min-w-max">
          {SECTIONS.map((s) => (
            <button
              key={s.id}
              onClick={() => setActiveSection(s.id)}
              className={`px-4 py-2 rounded-full text-xs font-extrabold whitespace-nowrap transition-colors ${
                activeSection === s.id
                  ? 'bg-[#1CB0F6] text-white'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
              }`}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      <div className="px-4 pt-4 space-y-4">

        {/* ── Topics section ────────────────────────────────────────────── */}
        {activeSection === 'topics' && (
          <div className="space-y-3">
            <h2 className="font-extrabold text-gray-800 text-lg">Topic Performance</h2>
            {topicResults.map((t) => (
              <div key={t.topicId} className="bg-white border-2 border-gray-100 rounded-2xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{TOPIC_EMOJI[t.topicId] ?? '📚'}</span>
                    <div>
                      <p className="font-extrabold text-gray-800 text-sm">{t.topicName}</p>
                      <p className="text-xs text-gray-400 font-semibold">{t.correct}/{t.total} correct · avg {formatMs(t.avgTimeMs)}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {t.accuracy < 0.5 && (
                      <span className="text-xs font-extrabold px-2 py-0.5 bg-red-100 text-red-600 rounded-full">Focus 🎯</span>
                    )}
                    <span className={`text-sm font-extrabold ${
                      t.accuracy >= 0.8 ? 'text-[#58CC02]' :
                      t.accuracy >= 0.5 ? 'text-[#FF9600]' : 'text-[#FF4B4B]'
                    }`}>
                      {Math.round(t.accuracy * 100)}%
                    </span>
                  </div>
                </div>
                <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${
                      t.accuracy >= 0.8 ? 'bg-[#58CC02]' :
                      t.accuracy >= 0.5 ? 'bg-[#FF9600]' : 'bg-[#FF4B4B]'
                    }`}
                    style={{ width: `${t.accuracy * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ── Difficulty section ────────────────────────────────────────── */}
        {activeSection === 'difficulty' && (
          <div className="space-y-3">
            <h2 className="font-extrabold text-gray-800 text-lg">Difficulty Breakdown</h2>
            {diffBreakdown.map(({ diff, correct, total: t }) => {
              const pct = t > 0 ? correct / t : 0;
              const insight =
                pct >= 0.8 ? 'Excellent!' :
                pct >= 0.6 ? 'Good'       :
                pct >= 0.4 ? 'Needs work' : 'Focus here';
              const color =
                diff === 'Easy'   ? 'bg-[#58CC02]' :
                diff === 'Medium' ? 'bg-[#FF9600]' : 'bg-[#FF4B4B]';
              return (
                <div key={diff} className="bg-white border-2 border-gray-100 rounded-2xl p-4">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-extrabold text-gray-800">{diff}</span>
                    <span className="text-sm font-bold text-gray-500">{correct}/{t} · {insight}</span>
                  </div>
                  <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${pct * 100}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* ── Time section ─────────────────────────────────────────────── */}
        {activeSection === 'time' && (
          <div className="space-y-4">
            <h2 className="font-extrabold text-gray-800 text-lg">Time Analysis</h2>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-gray-50 rounded-2xl p-4 text-center">
                <p className="text-2xl font-extrabold text-gray-800">{formatMs(avgTimeMs)}</p>
                <p className="text-xs text-gray-400 font-semibold mt-1">avg per question</p>
              </div>
              {timeUsedMs != null && (
                <div className="bg-gray-50 rounded-2xl p-4 text-center">
                  <p className="text-2xl font-extrabold text-gray-800">{formatTime(timeUsedMs)}</p>
                  <p className="text-xs text-gray-400 font-semibold mt-1">total time used</p>
                </div>
              )}
            </div>

            {slowest.length > 0 && (
              <div>
                <p className="font-extrabold text-gray-700 text-sm mb-2">Slowest questions</p>
                <div className="space-y-2">
                  {slowest.map((r) => (
                    <div key={r.id} className="flex items-center gap-3 py-2 border-b border-gray-100">
                      <span className="text-xs font-extrabold text-gray-400 w-8 flex-shrink-0">Q{r.questionNumber}</span>
                      <p className="flex-1 text-xs text-gray-600 line-clamp-1">{r.question?.questionText}</p>
                      <span className="text-xs font-extrabold text-[#FF9600] flex-shrink-0">{formatMs(r.timeTakenMs)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── Question playback ─────────────────────────────────────────── */}
        {activeSection === 'playback' && (
          <div className="space-y-2">
            <h2 className="font-extrabold text-gray-800 text-lg mb-3">All Questions</h2>
            {test.responses.map((r, idx) => (
              <QuestionAccordion key={r.id} r={r} idx={idx} />
            ))}
          </div>
        )}

        {/* ── Study plan ───────────────────────────────────────────────── */}
        {activeSection === 'plan' && (
          <div className="space-y-3">
            <h2 className="font-extrabold text-gray-800 text-lg">Personalised Study Plan</h2>

            {recommendations.filter((r) => r.type === 'priority').length > 0 && (
              <div>
                <p className="text-xs font-extrabold text-[#FF4B4B] uppercase tracking-wide mb-2">🔴 Priority — Practice These First</p>
                <div className="space-y-2">
                  {recommendations.filter((r) => r.type === 'priority').map((rec) => (
                    <div key={rec.topicId} className="bg-red-50 border-2 border-red-100 rounded-2xl p-4 flex items-center gap-3">
                      <div className="flex-1">
                        <p className="font-extrabold text-gray-800 text-sm">{rec.topicName}</p>
                        <p className="text-xs text-gray-500 font-medium">{rec.reason}</p>
                      </div>
                      <DuoButton variant="red" onClick={() => router.push(`/practice/${rec.topicId}`)}>
                        Practice →
                      </DuoButton>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {recommendations.filter((r) => r.type === 'speed').length > 0 && (
              <div>
                <p className="text-xs font-extrabold text-[#FF9600] uppercase tracking-wide mb-2">🟡 Speed Up — You Know This But Need To Be Faster</p>
                <div className="space-y-2">
                  {recommendations.filter((r) => r.type === 'speed').map((rec) => (
                    <div key={rec.topicId} className="bg-amber-50 border-2 border-amber-100 rounded-2xl p-4 flex items-center gap-3">
                      <div className="flex-1">
                        <p className="font-extrabold text-gray-800 text-sm">{rec.topicName}</p>
                        <p className="text-xs text-gray-500 font-medium">{rec.reason}</p>
                      </div>
                      <DuoButton variant="orange" onClick={() => router.push(`/practice/${rec.topicId}?mode=speed`)}>
                        ⚡ Speed
                      </DuoButton>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {recommendations.filter((r) => r.type === 'strength').length > 0 && (
              <div>
                <p className="text-xs font-extrabold text-[#58CC02] uppercase tracking-wide mb-2">🟢 Strengths — Keep It Up!</p>
                <div className="space-y-2">
                  {recommendations.filter((r) => r.type === 'strength').map((rec) => (
                    <div key={rec.topicId} className="bg-green-50 border-2 border-green-100 rounded-2xl p-4">
                      <p className="font-extrabold text-gray-800 text-sm">{rec.topicName}</p>
                      <p className="text-xs text-gray-500 font-medium">{rec.reason}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {recommendations.length === 0 && (
              <div className="bg-green-50 border-2 border-green-100 rounded-2xl p-6 text-center">
                <p className="text-2xl mb-2">🎉</p>
                <p className="font-extrabold text-gray-800">Everything looks balanced!</p>
                <p className="text-sm text-gray-500 mt-1">Keep practicing to maintain your performance.</p>
              </div>
            )}
          </div>
        )}

      </div>

      {/* ── Footer actions ────────────────────────────────────────────────── */}
      <div className="px-4 mt-8 space-y-3">
        <DuoButton variant="green" fullWidth onClick={() => router.push('/test')}>
          Take Another Test 📝
        </DuoButton>
        <button
          onClick={() => router.push('/test/history')}
          className="w-full min-h-[48px] rounded-full border-2 border-gray-200 font-extrabold text-gray-600 text-sm hover:bg-gray-50 transition-colors"
        >
          View All Tests
        </button>
        <button
          onClick={() => router.push('/chapters')}
          className="w-full text-gray-400 text-sm font-semibold text-center py-2 hover:text-gray-600 transition-colors"
        >
          Back to Learning 📚
        </button>
      </div>
    </div>
  );
}
