'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import QuestionCard, { randomCorrect, randomWrong } from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import ProgressBar from '@/components/ProgressBar';
import { SkeletonCard } from '@/components/Skeleton';
import type { Question, AnswerKey } from '@/types';

const STREAK_MSG: Record<number, string> = {
  3: "You're on fire! 🔥",
  5: 'Unstoppable! ⚡',
  10: 'Math wizard! 🧙',
};

export default function PracticePage() {
  const params = useParams();
  const router = useRouter();
  const topicId = params.topicId as string;

  const [studentId,  setStudentId]  = useState<string | null>(null);
  const [topicName,  setTopicName]  = useState('');
  const [question,   setQuestion]   = useState<Question | null>(null);
  const [loading,    setLoading]    = useState(true);
  const [everLoaded, setEverLoaded] = useState(false); // true once first question arrives
  const [answered,   setAnswered]   = useState(false);
  const [selected,   setSelected]   = useState<AnswerKey | null>(null);
  const [feedback,   setFeedback]   = useState('');
  const [hintLevel,  setHintLevel]  = useState(0);
  const [seenIds,    setSeenIds]    = useState<string[]>([]);
  const [cw,         setCw]         = useState(0); // consecutive wrong
  const [cr,         setCr]         = useState(0); // consecutive right
  const [score,      setScore]      = useState({ correct: 0, attempted: 0 });
  const [noMore,     setNoMore]     = useState(false);
  const [saveError,  setSaveError]  = useState<(() => void) | null>(null);

  // ── Load next question ────────────────────────────────────────────────────
  const loadNext = useCallback(async (
    sid: string,
    seen: string[],
    cwCur: number,
    crCur: number,
  ) => {
    setLoading(true);
    setAnswered(false);
    setSelected(null);
    setFeedback('');
    setHintLevel(0);

    const params = new URLSearchParams({
      topicId,
      studentId: sid,
      exclude: seen.join(','),
      cw: String(cwCur),
      cr: String(crCur),
    });

    const res = await fetch(`/api/questions/next?${params}`);
    if (res.status === 404) {
      // Session complete — clear persisted session state
      sessionStorage.removeItem(`mathspark_seen_${topicId}`);
      sessionStorage.removeItem(`mathspark_cw_${topicId}`);
      sessionStorage.removeItem(`mathspark_cr_${topicId}`);
      setNoMore(true);
      setLoading(false);
      return;
    }

    const q = await res.json();
    setQuestion(q);
    setEverLoaded(true);
    setLoading(false);
  }, [topicId]);

  // ── Boot: get student + topic ─────────────────────────────────────────────
  useEffect(() => {
    const sid = localStorage.getItem('mathspark_student_id');
    if (!sid) { router.replace('/start'); return; }
    setStudentId(sid);

    fetch('/api/topics')
      .then((r) => r.json())
      .then((topics: Array<{ id: string; name: string }>) => {
        const t = topics.find((x) => x.id === topicId);
        setTopicName(t?.name ?? topicId);
      });

    // Restore session state from sessionStorage to survive hard refreshes
    const rawSeen = sessionStorage.getItem(`mathspark_seen_${topicId}`);
    const initialSeen: string[] = rawSeen ? JSON.parse(rawSeen) : [];
    const initialCw = parseInt(sessionStorage.getItem(`mathspark_cw_${topicId}`) ?? '0', 10);
    const initialCr = parseInt(sessionStorage.getItem(`mathspark_cr_${topicId}`) ?? '0', 10);

    // Seed React state so subsequent loadNext calls (via Next button) use correct values
    setSeenIds(initialSeen);
    setCw(initialCw);
    setCr(initialCr);

    loadNext(sid, initialSeen, initialCw, initialCr);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicId]);

  // ── Handle answer ─────────────────────────────────────────────────────────
  async function handleAnswer(key: AnswerKey, isCorrect: boolean) {
    if (!question || answered || !studentId) return;
    setAnswered(true);
    setSelected(key);

    const newCr = isCorrect ? cr + 1 : 0;
    const newCw = isCorrect ? 0       : cw + 1;
    const newScore = {
      correct:   score.correct   + (isCorrect ? 1 : 0),
      attempted: score.attempted + 1,
    };

    setCr(newCr);
    setCw(newCw);
    setScore(newScore);

    // Kid-friendly feedback
    let msg = isCorrect ? randomCorrect() : randomWrong();
    if (isCorrect && STREAK_MSG[newCr]) msg = STREAK_MSG[newCr];
    setFeedback(msg);

    // Show hint level 1 automatically on wrong
    if (!isCorrect) setHintLevel(1);

    // Persist session state so a hard refresh doesn't reset progress
    const newSeenIds = [...seenIds, question.id];
    setSeenIds(newSeenIds);
    sessionStorage.setItem(`mathspark_seen_${topicId}`, JSON.stringify(newSeenIds));
    sessionStorage.setItem(`mathspark_cw_${topicId}`, String(newCw));
    sessionStorage.setItem(`mathspark_cr_${topicId}`, String(newCr));

    // Record attempt with retry on failure
    const payload = {
      studentId,
      questionId: question.id,
      topicId,
      selected: key,
      isCorrect,
      hintUsed: hintLevel,
    };

    function recordAttempt(p: typeof payload) {
      fetch('/api/attempts', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(p),
      })
        .then((r) => { if (!r.ok) throw new Error('HTTP ' + r.status); setSaveError(null); })
        .catch(() => { setSaveError(() => () => recordAttempt(p)); });
    }

    recordAttempt(payload);
  }

  // ── Render helpers ────────────────────────────────────────────────────────
  const pct = score.attempted > 0 ? Math.round((score.correct / score.attempted) * 100) : 0;

  if (noMore) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-6 text-center">
        <div className="text-5xl">🏆</div>
        <h2 className="text-2xl font-bold text-gray-800">You practised all questions here!</h2>
        <p className="text-gray-500">Score: {score.correct}/{score.attempted} correct</p>
        <button
          onClick={() => router.push('/chapters')}
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 px-8 rounded-2xl text-lg"
        >
          Back to Chapters 📚
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col px-4 py-5 gap-4">
      {/* Header */}
      <div className="space-y-1">
        <div className="flex items-center justify-between">
          <button
            onClick={() => router.push('/chapters')}
            className="text-gray-400 hover:text-gray-600 text-sm font-medium min-h-[44px] px-2"
          >
            ← Back
          </button>
          <span className="text-sm text-gray-500 font-medium">
            {score.correct}/{score.attempted} correct
          </span>
        </div>
        <h1 className="text-lg font-bold text-gray-800 px-2">{topicName}</h1>
        <ProgressBar value={pct} color="bg-blue-500" height="h-2" />
      </div>

      {/* Question area */}
      {loading && !everLoaded ? (
        <SkeletonCard />
      ) : loading ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-4xl animate-bounce">🤔</div>
        </div>
      ) : question ? (
        <>
          <QuestionCard
            question={question}
            answered={answered}
            selected={selected}
            onAnswer={handleAnswer}
          />

          {/* Feedback banner */}
          {answered && feedback && (
            <div
              className={`rounded-2xl px-4 py-3 text-center font-semibold text-base ${
                selected === question.correctAnswer
                  ? 'bg-green-50 text-green-700 border border-green-200'
                  : 'bg-amber-50 text-amber-700 border border-amber-200'
              }`}
            >
              {feedback}
            </div>
          )}

          {/* Save error banner */}
          {saveError && (
            <div className="mx-4 mt-2 p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-center justify-between text-sm text-amber-700">
              <span>Couldn&apos;t save your answer.</span>
              <button
                onClick={() => { saveError(); setSaveError(null); }}
                className="font-semibold underline ml-2"
              >
                Retry
              </button>
            </div>
          )}

          {/* Hint system (auto-shown on wrong) */}
          {answered && (
            <HintSystem
              hint1={question.hint1}
              hint2={question.hint2}
              hint3={question.hint3}
              level={hintLevel}
              onLevelUp={(n) => setHintLevel(n)}
            />
          )}

          {/* Step-by-step solution */}
          {answered && question.stepByStep?.length > 0 && (
            <StepByStep steps={question.stepByStep} />
          )}

          {/* Misconception note */}
          {answered && selected !== question.correctAnswer && (() => {
            const key = `misconception${selected}` as keyof Question;
            const note = question[key] as string;
            return note ? (
              <div className="rounded-2xl bg-blue-50 border border-blue-100 px-4 py-3 text-sm text-blue-700">
                <span className="font-bold">Why not {selected}?</span> {note}
              </div>
            ) : null;
          })()}

          {/* Next question button */}
          {answered && (
            <button
              onClick={() => loadNext(studentId!, seenIds, cw, cr)}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-2xl text-lg transition-colors"
            >
              Next Question →
            </button>
          )}
        </>
      ) : (
        <p className="text-center text-gray-400 mt-16">No question loaded.</p>
      )}
    </div>
  );
}
