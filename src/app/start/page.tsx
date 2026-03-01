'use client';

import { useState, useCallback, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import QuestionCard from '@/components/QuestionCard';
import ProgressBar from '@/components/ProgressBar';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import type { Question, AnswerKey, DiagnosticAnswer } from '@/types';

// ── Diagnostic plan — 9 topics, 15 questions total ───────────────────────────
const PLAN = [
  { topicId: 'ch11',    count: 2 },
  { topicId: 'ch09-10', count: 2 },
  { topicId: 'ch07-08', count: 2 },
  { topicId: 'ch06',    count: 2 },
  { topicId: 'ch01-05', count: 2 },
  { topicId: 'ch18',    count: 2 },
  { topicId: 'ch20',    count: 1 },
  { topicId: 'ch13',    count: 1 },
  { topicId: 'ch19',    count: 1 },
];
const TOTAL = PLAN.reduce((s, p) => s + p.count, 0); // 15

const TOPIC_NAMES: Record<string, string> = {
  'ch01-05': 'Number System',
  'ch06':    'Factors & Multiples',
  'ch07-08': 'Fractions',
  'ch09-10': 'Operations & BODMAS',
  'ch11':    'Decimal Fractions',
  'ch13':    'Algebraic Expressions',
  'ch18':    'Angles',
  'ch19':    'Triangles',
  'ch20':    'Quadrilaterals',
};

type Step = 'welcome' | 'name' | 'quiz' | 'results' | 'displayName';
type Diff  = 'Easy' | 'Medium' | 'Hard';

function nextDiff(d: Diff, up: boolean): Diff {
  if (up)  return d === 'Easy' ? 'Medium' : 'Hard';
  return d === 'Hard' ? 'Medium' : 'Easy';
}

// ── Count-up animation ────────────────────────────────────────────────────────
function useCountUp(target: number, active: boolean): number {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (!active) return;
    setValue(0);
    const step = Math.max(1, Math.ceil(target / 30));
    const id = setInterval(() => {
      setValue((v) => {
        const next = v + step;
        if (next >= target) { clearInterval(id); return target; }
        return next;
      });
    }, 40);
    return () => clearInterval(id);
  }, [target, active]);
  return value;
}

// ── Main component ────────────────────────────────────────────────────────────

export default function StartPage() {
  const router = useRouter();

  const [step,         setStep]        = useState<Step>('welcome');
  const [name,         setName]        = useState('');
  const [studentId,    setStudentId]   = useState<string | null>(null);
  const [loading,      setLoading]     = useState(false);
  const [error,        setError]       = useState('');
  const [pendingRoute, setPendingRoute] = useState<'/chapters' | '/test'>('/chapters');
  const [displayName,  setDisplayName] = useState('');
  const [avatarColor,  setAvatarColor] = useState('#3B82F6');
  const [dnError,      setDnError]     = useState('');

  // Quiz state
  const [question,     setQuestion]     = useState<Question | null>(null);
  const [answered,     setAnswered]     = useState(false);
  const [selected,     setSelected]     = useState<AnswerKey | null>(null);
  const [planIdx,      setPlanIdx]      = useState(0);
  const [countInTopic, setCountInTopic] = useState(0);
  const [difficulty,   setDifficulty]   = useState<Diff>('Medium');
  const [seenIds,      setSeenIds]      = useState<string[]>([]);
  const [answers,      setAnswers]      = useState<DiagnosticAnswer[]>([]);
  const [showConfetti, setShowConfetti] = useState(false);

  // Count-up for results screen
  const totalCorrect = answers.filter((a) => a.isCorrect).length;
  const countUp      = useCountUp(totalCorrect, step === 'results');

  // ── Fetch one diagnostic question ─────────────────────────────────────────
  const fetchQuestion = useCallback(async (
    topicId: string,
    diff: Diff,
    seen: string[],
  ) => {
    setLoading(true);
    setAnswered(false);
    setSelected(null);
    try {
      const params = new URLSearchParams({
        topicId,
        difficulty: diff,
        exclude: seen.join(','),
      });
      const res = await fetch(`/api/diagnostic?${params}`);
      if (!res.ok) { setQuestion(null); return; }
      setQuestion(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  // ── Create student + start quiz ───────────────────────────────────────────
  async function handleStart() {
    if (!name.trim()) return;
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/students', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ name: name.trim() }),
      });
      const student = await res.json();
      localStorage.setItem('mathspark_student_id',   student.id);
      localStorage.setItem('mathspark_student_name', student.name);
      setStudentId(student.id);
      setDisplayName(name.trim().slice(0, 20));
      setAvatarColor(student.avatarColor ?? '#3B82F6');
      setStep('quiz');
      await fetchQuestion(PLAN[0].topicId, 'Medium', []);
    } catch {
      setError('Something went wrong. Please try again!');
    } finally {
      setLoading(false);
    }
  }

  // ── Handle answer ─────────────────────────────────────────────────────────
  async function handleAnswer(key: AnswerKey, isCorrect: boolean) {
    if (!question || answered || !studentId) return;
    setAnswered(true);
    setSelected(key);

    const newAnswers: DiagnosticAnswer[] = [
      ...answers,
      { topicId: PLAN[planIdx].topicId, questionId: question.id, isCorrect },
    ];
    setAnswers(newAnswers);

    // Record attempt (fire-and-forget — also updates mastery via updateProgress)
    fetch('/api/attempts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        studentId,
        questionId: question.id,
        topicId:    question.topicId,
        selected:   key,
        isCorrect,
        hintUsed:   0,
      }),
    }).catch(() => {/* ignore — non-critical */});

    setTimeout(() => advance(isCorrect, newAnswers), 1200);
  }

  // ── Advance to next question or results ───────────────────────────────────
  async function advance(wasCorrect: boolean, currentAnswers: DiagnosticAnswer[]) {
    const newDiff  = nextDiff(difficulty, wasCorrect);
    const newCount = countInTopic + 1;
    const newSeen  = [...seenIds, question!.id];

    if (currentAnswers.length >= TOTAL || planIdx >= PLAN.length) {
      setShowConfetti(true);
      setStep('results');
      return;
    }

    let nextPlanIdx = planIdx;
    let nextCount   = newCount;

    if (newCount >= PLAN[planIdx].count) {
      nextPlanIdx = planIdx + 1;
      nextCount   = 0;
      if (nextPlanIdx >= PLAN.length) {
        setShowConfetti(true);
        setStep('results');
        return;
      }
    }

    setPlanIdx(nextPlanIdx);
    setCountInTopic(nextCount);
    setDifficulty(newDiff);
    setSeenIds(newSeen);
    await fetchQuestion(PLAN[nextPlanIdx].topicId, newDiff, newSeen);
  }

  // ── Compute results for ALL 9 topics ─────────────────────────────────────
  // Strong   = all answered correctly (1/1 or 2/2)
  // Learning = at least one correct but not all (1/2)
  // NotYet   = 0 correct OR not tested
  function computeResults() {
    return PLAN.map(({ topicId }) => {
      const topicAnswers = answers.filter((a) => a.topicId === topicId);
      const correct = topicAnswers.filter((a) => a.isCorrect).length;
      const total   = topicAnswers.length;
      const status: 'Strong' | 'Learning' | 'NotYet' =
        total > 0 && correct === total ? 'Strong'   :
        correct > 0                    ? 'Learning' : 'NotYet';
      return {
        topicId,
        name: TOPIC_NAMES[topicId] ?? topicId,
        correct,
        total,
        status,
      };
    });
  }

  // ── Render ────────────────────────────────────────────────────────────────

  // ── Screen 1: Welcome ─────────────────────────────────────────────────────
  if (step === 'welcome') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 text-center gap-8 bg-gradient-to-b from-[#131F24] to-[#1a7a20]">
        <div className="text-[96px] leading-none select-none" role="img" aria-label="sparkles">
          ✨
        </div>
        <div className="space-y-3">
          <h1 className="text-3xl font-extrabold text-white leading-tight">
            Welcome to MathSpark!
          </h1>
          <p className="text-white/80 text-lg leading-relaxed">
            Let&#39;s find out what you already know —<br />
            it&#39;ll be quick and fun!
          </p>
        </div>
        <div className="w-full space-y-3">
          <DuoButton variant="blue" fullWidth onClick={() => setStep('name')}>
            Let&#39;s Go! 🚀
          </DuoButton>
          <p className="text-white/50 text-sm font-medium">Takes about 5 minutes</p>
        </div>
      </div>
    );
  }

  // ── Screen 2: Name ────────────────────────────────────────────────────────
  if (step === 'name') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-[#131F24]">
        <div className="relative bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-6">
          {/* Sparky peeking over the card */}
          <div className="absolute -top-8 right-4 animate-sparky-wave">
            <Sparky mood="encouraging" size={64} />
          </div>
          <h2 className="text-2xl font-extrabold text-gray-800 text-center pt-4">
            What should I call you? 😊
          </h2>
          <input
            type="text"
            autoFocus
            value={name}
            onChange={(e) => { setName(e.target.value); setError(''); }}
            onKeyDown={(e) => e.key === 'Enter' && name.trim() && handleStart()}
            placeholder="Your first name"
            maxLength={30}
            className="w-full text-2xl font-bold text-center border-b-4 border-[#1CB0F6] bg-transparent outline-none py-2 text-gray-800 placeholder-gray-300"
          />
          {error && <p className="text-[#FF4B4B] text-sm text-center font-semibold">{error}</p>}
          <DuoButton
            variant="green"
            fullWidth
            onClick={handleStart}
            loading={loading}
            disabled={!name.trim()}
          >
            Continue →
          </DuoButton>
        </div>
      </div>
    );
  }

  // ── Screen 3: Diagnostic Quiz ─────────────────────────────────────────────
  if (step === 'quiz') {
    const qNum = answers.length + 1;
    const pct  = (answers.length / TOTAL) * 100;

    return (
      <div className="min-h-screen flex flex-col px-4 py-6 gap-4 bg-white">
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm text-gray-500 font-semibold">
            <span>Question {qNum} of {TOTAL}</span>
            <span>Quick check-in 🔍</span>
          </div>
          <ProgressBar value={pct} height="h-4" />
        </div>

        {loading ? (
          <div className="flex-1 flex flex-col items-center justify-center gap-4">
            <div className="animate-sparky-bounce">
              <Sparky mood="thinking" size={100} />
            </div>
            <p className="text-gray-400 font-semibold">Loading question…</p>
          </div>
        ) : question ? (
          <QuestionCard
            question={question}
            answered={answered}
            selected={selected}
            onAnswer={handleAnswer}
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center gap-4">
            <p className="text-gray-400 font-semibold">Loading question…</p>
          </div>
        )}
      </div>
    );
  }

  // ── Screen 5: Display name + avatar (shown before navigating away) ──────────
  if (step === 'displayName') {
    const AVATAR_COLORS = [
      '#FF9600','#58CC02','#1CB0F6','#FF4B4B',
      '#9B59B6','#00BCD4','#FFC800','#FF69B4',
      '#3B82F6','#10B981','#F59E0B','#EF4444',
    ];
    const initial = displayName ? displayName[0].toUpperCase() : (name[0] ?? '?').toUpperCase();

    async function handleJoinLeague() {
      const trimmed = displayName.trim().slice(0, 20) || name.trim().slice(0, 20);
      if (!trimmed) return;
      if (studentId) {
        await fetch('/api/student', {
          method: 'PATCH',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ studentId, displayName: trimmed, avatarColor }),
        }).catch(() => {/* non-critical */});
      }
      router.push(pendingRoute);
    }

    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-[#131F24]">
        <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-5">
          <div className="text-center">
            <div
              className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-extrabold text-white mx-auto mb-3 border-4 border-white/30 shadow-lg"
              style={{ backgroundColor: avatarColor }}
            >
              {initial}
            </div>
            <h2 className="text-2xl font-extrabold text-gray-800">Join the League! 🏆</h2>
            <p className="text-gray-400 text-sm font-medium mt-1">
              Pick a leaderboard name and colour
            </p>
          </div>

          {/* Display name input */}
          <div>
            <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Your leaderboard name</label>
            <input
              type="text"
              autoFocus
              value={displayName}
              onChange={(e) => { setDisplayName(e.target.value); setDnError(''); }}
              onKeyDown={(e) => e.key === 'Enter' && handleJoinLeague()}
              placeholder={name.trim().slice(0, 20)}
              maxLength={20}
              className="w-full mt-1.5 text-xl font-bold text-center border-b-4 border-[#1CB0F6] bg-transparent outline-none py-2 text-gray-800 placeholder-gray-300"
            />
            {dnError && <p className="text-[#FF4B4B] text-xs font-semibold text-center mt-1">{dnError}</p>}
          </div>

          {/* Colour swatches */}
          <div>
            <label className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Avatar colour</label>
            <div className="flex flex-wrap gap-2 mt-2">
              {AVATAR_COLORS.map((c) => (
                <button
                  key={c}
                  onClick={() => setAvatarColor(c)}
                  style={{ backgroundColor: c, minHeight: 0 }}
                  className={`w-9 h-9 rounded-full transition-all active:scale-95 ${
                    avatarColor === c ? 'ring-4 ring-offset-2 ring-gray-800 scale-110' : ''
                  }`}
                />
              ))}
            </div>
          </div>

          <DuoButton variant="green" fullWidth onClick={handleJoinLeague} loading={loading}>
            Let&apos;s go! 🚀
          </DuoButton>
          <button
            onClick={() => router.push(pendingRoute)}
            style={{ minHeight: 0 }}
            className="w-full text-center text-gray-400 text-sm font-semibold py-1 hover:text-gray-600 transition-colors"
          >
            Skip for now →
          </button>
        </div>
      </div>
    );
  }

  // ── Screen 4: Results ─────────────────────────────────────────────────────
  const results  = computeResults();
  const strong   = results.filter((r) => r.status === 'Strong');
  const learning = results.filter((r) => r.status === 'Learning');
  const notYet   = results.filter((r) => r.status === 'NotYet');

  return (
    <div className="min-h-screen px-4 py-8 flex flex-col gap-6 bg-white pb-12">
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

      {/* Hero */}
      <div className="text-center space-y-4">
        <div className="flex justify-center animate-sparky-dance">
          <Sparky mood="celebrating" size={120} />
        </div>
        <h2 className="text-2xl font-extrabold text-gray-800">
          Wow {name}, you already know so much! 🎉
        </h2>
        {/* Animated count-up */}
        <div className="inline-flex items-baseline gap-2 bg-[#FFF9E6] border-2 border-[#FFC800] rounded-2xl px-6 py-3">
          <span className="text-4xl font-extrabold text-[#131F24] tabular-nums">
            {countUp}
          </span>
          <span className="text-gray-600 font-semibold text-base">
            out of {TOTAL} correct!
          </span>
        </div>
      </div>

      {/* ✅ Green — "You nailed it!" (show first) */}
      {strong.length > 0 && (
        <div>
          <h3 className="text-sm font-extrabold text-[#46a302] uppercase tracking-wide mb-2">
            ✅ You nailed it!
          </h3>
          <div className="space-y-2">
            {strong.map((r) => (
              <div
                key={r.topicId}
                className="bg-green-50 border-2 border-[#58CC02] rounded-2xl px-4 py-3 flex justify-between items-center"
              >
                <span className="font-bold text-gray-800">{r.name}</span>
                <span className="text-[#46a302] font-extrabold">{r.correct}/{r.total}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 🟡 Amber — "Getting there!" */}
      {learning.length > 0 && (
        <div>
          <h3 className="text-sm font-extrabold text-[#cc7800] uppercase tracking-wide mb-2">
            🟡 Getting there!
          </h3>
          <div className="space-y-2">
            {learning.map((r) => (
              <div
                key={r.topicId}
                className="bg-amber-50 border-2 border-[#FF9600] rounded-2xl px-4 py-3 flex justify-between items-center"
              >
                <span className="font-bold text-gray-800">{r.name}</span>
                <span className="text-[#cc7800] font-extrabold">{r.correct}/{r.total}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ⬜ Gray — "Let's explore!" (0 correct or untested) */}
      {notYet.length > 0 && (
        <div>
          <h3 className="text-sm font-extrabold text-gray-400 uppercase tracking-wide mb-2">
            ⬜ Let&#39;s explore!
          </h3>
          <div className="space-y-2">
            {notYet.map((r) => (
              <div
                key={r.topicId}
                className="bg-gray-50 border-2 border-gray-200 rounded-2xl px-4 py-3 flex justify-between items-center"
              >
                <span className="font-bold text-gray-800">{r.name}</span>
                <span className="text-gray-400 font-extrabold text-sm">
                  {r.total > 0 ? `${r.correct}/${r.total}` : 'Not tested yet'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="space-y-3">
        <DuoButton variant="green" fullWidth onClick={() => { setPendingRoute('/chapters'); setStep('displayName'); }}>
          Start Learning 📚
        </DuoButton>
        <DuoButton variant="blue" fullWidth onClick={() => { setPendingRoute('/test'); setStep('displayName'); }}>
          Take a Mock Test 📝
        </DuoButton>
      </div>
    </div>
  );
}
