'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import QuestionCard, { randomCorrect, randomWrong } from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import ProgressBar from '@/components/ProgressBar';
import ChatWidget from '@/components/ChatWidget';
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

  const [studentId,   setStudentId]   = useState<string | null>(null);
  const [studentName, setStudentName] = useState('');
  const [topicName,   setTopicName]   = useState('');
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
  const [noMore,       setNoMore]       = useState(false);
  const [attemptError, setAttemptError] = useState(false);

  // Flag this question
  const [showFlagForm, setShowFlagForm]   = useState(false);
  const [flagReason,   setFlagReason]     = useState<'wrong_answer' | 'confusing' | 'too_hard' | 'other'>('other');
  const [flagSent,     setFlagSent]       = useState(false);

  // ── Timer ref: tracks when the current question was shown ─────────────────
  const startTimeRef = useRef<number>(Date.now());

  // ── Prefetch refs ──────────────────────────────────────────────────────────
  const prefetchedRef   = useRef<Question | null>(null);
  const prefetchingRef  = useRef(false);

  // ── Timed exam mode ────────────────────────────────────────────────────────
  const [timedMode, setTimedMode] = useState(false);
  const [timeLeft,  setTimeLeft]  = useState(60);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // ── Prefetch next question in the background ───────────────────────────────
  const prefetchNext = useCallback(async (
    sid: string,
    seen: string[],
    cwCur: number,
    crCur: number,
  ) => {
    if (prefetchingRef.current) return;
    prefetchingRef.current = true;
    try {
      const res = await fetch('/api/questions/next', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ topicId, studentId: sid, exclude: seen, cw: cwCur, cr: crCur }),
      });
      if (res.ok) {
        prefetchedRef.current = await res.json();
      }
    } catch { /* silent */ }
    prefetchingRef.current = false;
  }, [topicId]);

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
    setShowFlagForm(false);
    setFlagSent(false);

    // Use prefetched question if available
    if (prefetchedRef.current) {
      const q = prefetchedRef.current;
      prefetchedRef.current = null;
      setQuestion(q);
      startTimeRef.current = Date.now();
      setLoading(false);
      return;
    }

    const res = await fetch('/api/questions/next', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        topicId,
        studentId: sid,
        exclude: seen,
        cw: cwCur,
        cr: crCur,
      }),
    });
    if (res.status === 404) {
      sessionStorage.removeItem(`mathspark_session_${topicId}`);
      setNoMore(true);
      setLoading(false);
      return;
    }
    if (!res.ok) {
      // Already handled 404 above; treat other errors as retriable
      setFeedback("Hmm, couldn't load the next question. Tap 'Next' to try again.");
      setLoading(false);
      return;
    }

    const q = await res.json();
    setQuestion(q);
    startTimeRef.current = Date.now();
    setLoading(false);
  }, [topicId]);

  // ── Timed mode countdown ───────────────────────────────────────────────────
  useEffect(() => {
    if (!timedMode || !question || answered) return;
    setTimeLeft(60);
    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current!);
          // Time's up — treat as wrong answer (only if not already answered)
          if (!answered) handleAnswer(question.correctAnswer === 'A' ? 'B' : 'A', false);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [question, timedMode]);

  // ── Boot: get student + topic ─────────────────────────────────────────────
  useEffect(() => {
    const sid = localStorage.getItem('mathspark_student_id');
    if (!sid) { router.replace('/start'); return; }
    setStudentId(sid);
    setStudentName(localStorage.getItem('mathspark_student_name') ?? '');

    fetch('/api/topics')
      .then((r) => r.json())
      .then((topics: Array<{ id: string; name: string }>) => {
        const t = topics.find((x) => x.id === topicId);
        setTopicName(t?.name ?? topicId);
      });

    // Restore session state (survives page refresh within the same tab)
    const sessionKey = `mathspark_session_${topicId}`;
    let initialSeen: string[] = [];
    let initialCw = 0;
    let initialCr = 0;
    try {
      const saved = sessionStorage.getItem(sessionKey);
      if (saved) {
        const parsed = JSON.parse(saved);
        initialSeen = parsed.seenIds ?? [];
        initialCw   = parsed.cw   ?? 0;
        initialCr   = parsed.cr   ?? 0;
        setSeenIds(initialSeen);
        setCw(initialCw);
        setCr(initialCr);
      }
    } catch { /* ignore parse errors */ }

    loadNext(sid, initialSeen, initialCw, initialCr);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicId]);

  // ── Handle answer ─────────────────────────────────────────────────────────
  async function handleAnswer(key: AnswerKey, isCorrect: boolean) {
    if (!question || answered || !studentId) return;
    if (timerRef.current) clearInterval(timerRef.current);
    setAttemptError(false);
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
    const timeTakenMs = Date.now() - startTimeRef.current;
    fetch('/api/attempts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        studentId,
        questionId: question.id,
        topicId,
        selected: key,
        hintUsed: hintLevel,
        timeTakenMs,
      }),
    }).catch(() => { setAttemptError(true); });
    localStorage.setItem('mathspark_last_practice', new Date().toISOString().slice(0, 10));

    const newSeenIds = [...seenIds, question.id];
    setSeenIds(newSeenIds);

    // Persist session state so it survives a hard refresh
    sessionStorage.setItem(`mathspark_session_${topicId}`, JSON.stringify({
      seenIds: newSeenIds,
      cw: newCw,
      cr: newCr,
    }));

    prefetchNext(studentId!, newSeenIds, newCw, newCr);
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
          <div className="flex items-center gap-2">
            <button
              onClick={() => setTimedMode((m) => !m)}
              className={`text-xs font-medium px-2 py-1 rounded-lg min-h-[44px] transition-colors ${
                timedMode ? 'bg-amber-100 text-amber-700' : 'text-gray-400 hover:text-gray-600'
              }`}
              aria-label={timedMode ? 'Disable timed mode' : 'Enable timed mode (60s per question)'}
            >
              {timedMode ? '⏱️ Timed' : '⏱️'}
            </button>
            <span className="text-sm text-gray-500 font-medium">
              {score.correct}/{score.attempted} correct
            </span>
          </div>
        </div>
        <h1 className="text-lg font-bold text-gray-800 px-2">{topicName}</h1>
        <ProgressBar value={pct} color="bg-blue-500" height="h-2" />
        {timedMode && !answered && (
          <div className={`text-center text-sm font-bold ${timeLeft <= 10 ? 'text-red-500' : 'text-gray-400'}`}>
            {timeLeft}s
          </div>
        )}
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

          {/* Attempt save error banner */}
          {attemptError && (
            <div className="text-xs text-amber-600 text-center">
              Couldn&apos;t save your answer — tap Next to continue.
            </div>
          )}

          {/* Next question button */}
          {answered && (
            <button
              onClick={() => loadNext(studentId!, seenIds, cw, cr)}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 rounded-2xl text-lg transition-colors"
            >
              Next Question →
            </button>
          )}

          {/* Flag this question */}
          {answered && !flagSent && (
            <div className="text-center">
              {!showFlagForm ? (
                <button
                  onClick={() => setShowFlagForm(true)}
                  className="text-xs text-gray-300 hover:text-gray-400 transition-colors py-2"
                >
                  Something wrong with this question? 🚩
                </button>
              ) : (
                <div className="bg-gray-50 rounded-xl p-3 text-left">
                  <p className="text-xs font-semibold text-gray-500 mb-2">What&apos;s the issue?</p>
                  <div className="space-y-1 mb-3">
                    {([
                      ['wrong_answer', 'The answer seems wrong'],
                      ['confusing',    'The question is confusing'],
                      ['too_hard',     'Way too hard for Grade 4'],
                      ['other',        'Something else'],
                    ] as const).map(([val, label]) => (
                      <label key={val} className="flex items-center gap-2 text-xs text-gray-600 cursor-pointer">
                        <input
                          type="radio"
                          name="flagReason"
                          value={val}
                          checked={flagReason === val}
                          onChange={() => setFlagReason(val)}
                          className="accent-blue-500"
                        />
                        {label}
                      </label>
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setShowFlagForm(false)}
                      className="flex-1 text-xs text-gray-400 py-2 rounded-lg border border-gray-200"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={async () => {
                        if (!question || !studentId) return;
                        await fetch('/api/questions/flag', {
                          method: 'POST',
                          headers: { 'content-type': 'application/json' },
                          body: JSON.stringify({ questionId: question.id, studentId, reason: flagReason }),
                        }).catch(() => {});
                        setFlagSent(true);
                        setShowFlagForm(false);
                      }}
                      className="flex-1 text-xs bg-amber-500 hover:bg-amber-600 text-white py-2 rounded-lg font-semibold"
                    >
                      Send report 🚩
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
          {answered && flagSent && (
            <p className="text-xs text-center text-green-600">Thanks for the report! We&apos;ll review it. ✅</p>
          )}
        </>
      ) : (
        <p className="text-center text-gray-400 mt-16">No question loaded.</p>
      )}

      {/* Spark AI learning companion — floating chat bubble */}
      <ChatWidget
        studentName={studentName}
        topicName={topicName}
        questionText={question?.questionText ?? ''}
      />
    </div>
  );
}
