'use client';

import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import QuestionCard from '@/components/QuestionCard';
import ProgressBar from '@/components/ProgressBar';
import type { Question, AnswerKey, DiagnosticAnswer } from '@/types';

// ── Diagnostic plan ─────────────────────────────────────────────────────────
// 15 questions covering 9 topics (≥ 6 required by spec)
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

type Step = 'welcome' | 'name' | 'quiz' | 'results';
type Diff  = 'Easy' | 'Medium' | 'Hard';

function nextDiff(d: Diff, up: boolean): Diff {
  if (up)  return d === 'Easy' ? 'Medium' : 'Hard';
  return d === 'Hard' ? 'Medium' : 'Easy';
}

export default function StartPage() {
  const router = useRouter();

  const [step,     setStep]     = useState<Step>('welcome');
  const [name,     setName]     = useState('');
  const [studentId, setStudentId] = useState<string | null>(null);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');

  // Quiz state
  const [question,     setQuestion]     = useState<Question | null>(null);
  const [answered,     setAnswered]     = useState(false);
  const [selected,     setSelected]     = useState<AnswerKey | null>(null);
  const [planIdx,      setPlanIdx]      = useState(0);
  const [countInTopic, setCountInTopic] = useState(0);
  const [difficulty,   setDifficulty]   = useState<Diff>('Medium');
  const [seenIds,      setSeenIds]      = useState<string[]>([]);
  const [answers,      setAnswers]      = useState<DiagnosticAnswer[]>([]);

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
      const q = await res.json();
      setQuestion(q);
    } finally {
      setLoading(false);
    }
  }, []);

  // ── Start onboarding ───────────────────────────────────────────────────────
  async function handleStart() {
    if (!name.trim()) { setError('Please tell us your name!'); return; }
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

    const newAnswers = [...answers, { topicId: PLAN[planIdx].topicId, questionId: question.id, isCorrect }];
    setAnswers(newAnswers);

    // Record attempt (fire-and-forget — doesn't block UX)
    fetch('/api/attempts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        studentId,
        questionId: question.id,
        topicId: question.topicId,
        selected: key,
        isCorrect,
        hintUsed: 0,
      }),
    }).catch(() => {/* ignore */});

    // Auto-advance after short delay
    setTimeout(() => advance(isCorrect, newAnswers), 1200);
  }

  // ── Advance to next question or results ───────────────────────────────────
  async function advance(wasCorrect: boolean, currentAnswers: DiagnosticAnswer[]) {
    const newDiff = nextDiff(difficulty, wasCorrect);
    const newCount = countInTopic + 1;
    const newSeen  = [...seenIds, question!.id];

    if (currentAnswers.length >= TOTAL || planIdx >= PLAN.length) {
      setStep('results');
      return;
    }

    let nextPlanIdx = planIdx;
    let nextCount   = newCount;

    if (newCount >= PLAN[planIdx].count) {
      nextPlanIdx = planIdx + 1;
      nextCount   = 0;
      if (nextPlanIdx >= PLAN.length) { setStep('results'); return; }
    }

    setPlanIdx(nextPlanIdx);
    setCountInTopic(nextCount);
    setDifficulty(newDiff);
    setSeenIds(newSeen);
    await fetchQuestion(PLAN[nextPlanIdx].topicId, newDiff, newSeen);
  }

  // ── Compute results ───────────────────────────────────────────────────────
  function computeResults() {
    return PLAN.map(({ topicId }) => {
      const topicAnswers = answers.filter((a) => a.topicId === topicId);
      const correct = topicAnswers.filter((a) => a.isCorrect).length;
      const total   = topicAnswers.length;
      const ratio   = total > 0 ? correct / total : 0;
      return {
        topicId,
        name: TOPIC_NAMES[topicId] ?? topicId,
        correct,
        total,
        status: ratio >= 0.7 ? 'Strong' : ratio >= 0.4 ? 'Learning' : 'NotYet',
      };
    }).filter((r) => r.total > 0);
  }

  // ── Render ────────────────────────────────────────────────────────────────

  if (step === 'welcome') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 text-center gap-6">
        <div className="text-6xl">🌟</div>
        <h1 className="text-3xl font-bold text-gray-800">Welcome to MathSpark!</h1>
        <p className="text-gray-500 text-lg leading-relaxed">
          Fun math practice for Grade 4.<br />
          Let&#39;s find out what you already know!
        </p>
        <button
          onClick={() => setStep('name')}
          className="w-full max-w-xs bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-2xl text-lg transition-colors"
        >
          Let&#39;s Go! 🚀
        </button>
      </div>
    );
  }

  if (step === 'name') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6">
        <div className="text-5xl">👋</div>
        <h2 className="text-2xl font-bold text-gray-800 text-center">What&#39;s your name?</h2>
        <input
          type="text"
          autoFocus
          value={name}
          onChange={(e) => { setName(e.target.value); setError(''); }}
          onKeyDown={(e) => e.key === 'Enter' && handleStart()}
          placeholder="Your first name"
          maxLength={30}
          className="w-full max-w-xs text-2xl font-medium text-center border-b-2 border-blue-400 bg-transparent outline-none py-2 text-gray-800 placeholder-gray-300"
        />
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button
          onClick={handleStart}
          disabled={loading}
          className="w-full max-w-xs bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white font-bold py-4 rounded-2xl text-lg transition-colors"
        >
          {loading ? 'Setting up...' : 'Continue →'}
        </button>
      </div>
    );
  }

  if (step === 'quiz') {
    const qNum = answers.length + 1;
    const pct  = (answers.length / TOTAL) * 100;

    return (
      <div className="min-h-screen flex flex-col px-4 py-6 gap-4">
        {/* Header */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm text-gray-500">
            <span>Question {qNum} of {TOTAL}</span>
            <span>Quick check-in 🔍</span>
          </div>
          <ProgressBar value={pct} color="bg-blue-500" height="h-2" />
        </div>

        {loading ? (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-4xl animate-bounce">🤔</div>
          </div>
        ) : question ? (
          <QuestionCard
            question={question}
            answered={answered}
            selected={selected}
            onAnswer={handleAnswer}
          />
        ) : (
          <p className="text-center text-gray-400 mt-10">Loading question…</p>
        )}
      </div>
    );
  }

  // Results
  const results = computeResults();
  const strong   = results.filter((r) => r.status === 'Strong');
  const learning = results.filter((r) => r.status === 'Learning');
  const notYet   = results.filter((r) => r.status === 'NotYet');

  return (
    <div className="min-h-screen px-4 py-8 flex flex-col gap-6">
      <div className="text-center space-y-2">
        <div className="text-5xl">🎉</div>
        <h2 className="text-2xl font-bold text-gray-800">Wow, you already know a lot!</h2>
        <p className="text-gray-500">Here&#39;s a snapshot of where you are:</p>
      </div>

      {/* Celebrate strengths first */}
      {strong.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-green-700 uppercase tracking-wide mb-2">
            ✅ Strong Areas
          </h3>
          <div className="space-y-2">
            {strong.map((r) => (
              <div key={r.topicId} className="bg-green-50 border border-green-200 rounded-xl px-4 py-3 flex justify-between items-center">
                <span className="font-medium text-gray-800">{r.name}</span>
                <span className="text-green-600 font-bold">{r.correct}/{r.total}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {learning.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-amber-700 uppercase tracking-wide mb-2">
            🟡 Still Learning
          </h3>
          <div className="space-y-2">
            {learning.map((r) => (
              <div key={r.topicId} className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 flex justify-between items-center">
                <span className="font-medium text-gray-800">{r.name}</span>
                <span className="text-amber-600 font-bold">{r.correct}/{r.total}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {notYet.length > 0 && (
        <div>
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wide mb-2">
            ⬜ Not Yet Started
          </h3>
          <div className="space-y-2">
            {notYet.map((r) => (
              <div key={r.topicId} className="bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 flex justify-between items-center">
                <span className="font-medium text-gray-800">{r.name}</span>
                <span className="text-gray-400 font-bold">{r.correct}/{r.total}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={() => router.push('/chapters')}
        className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-2xl text-lg transition-colors"
      >
        Ready to start! Let&#39;s go! 🚀
      </button>
    </div>
  );
}
