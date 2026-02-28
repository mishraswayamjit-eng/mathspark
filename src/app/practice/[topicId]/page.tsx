'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import QuestionCard, { randomCorrect, randomWrong } from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import ProgressBar from '@/components/ProgressBar';
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
  const [answered,   setAnswered]   = useState(false);
  const [selected,   setSelected]   = useState<AnswerKey | null>(null);
  const [feedback,   setFeedback]   = useState('');
  const [hintLevel,  setHintLevel]  = useState(0);
  const [seenIds,    setSeenIds]    = useState<string[]>([]);
  const [cw,         setCw]         = useState(0); // consecutive wrong
  const [cr,         setCr]         = useState(0); // consecutive right
  const [score,      setScore]      = useState({ correct: 0, attempted: 0 });
  const [noMore,     setNoMore]     = useState(false);

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
    if (res.status === 404) { setNoMore(true); setLoading(false); return; }

    const q = await res.json();
    setQuestion(q);
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

    loadNext(sid, [], 0, 0);
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

    // Record attempt
    fetch('/api/attempts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        studentId,
        questionId: question.id,
        topicId,
        selected: key,
        isCorrect,
        hintUsed: hintLevel,
      }),
    }).catch(() => {/* ignore in MVP */});

    setSeenIds((prev) => [...prev, question.id]);
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
      {loading ? (
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
