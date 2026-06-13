'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import QuestionCard, { randomCorrect, randomWrong } from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import ChatWidget from '@/components/ChatWidget';
import SparkMascot from '@/components/SparkMascot';
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
    const finalPct = score.attempted > 0 ? Math.round((score.correct / score.attempted) * 100) : 0;
    return (
      <motion.div
        className="min-h-screen bg-surface-cream flex flex-col items-center justify-center px-6 gap-5 text-center"
        initial={{ opacity: 0, scale: 0.96 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="animate-spark-pop">
          <SparkMascot expression="cheer" size={92} glow />
        </div>
        <h2 className="font-display text-2xl font-bold text-ink">You finished every question here!</h2>
        <div className="bg-surface-card rounded-spark shadow-soft px-7 py-5">
          <p className="font-display text-4xl font-extrabold text-spark-indigo">{finalPct}%</p>
          <p className="font-body text-sm text-ink-muted mt-1">
            {score.correct} of {score.attempted} correct
          </p>
        </div>
        <button
          onClick={() => router.push('/chapters')}
          className="bg-spark-indigo text-white font-body font-extrabold py-4 px-8 rounded-2xl text-lg shadow-press active:translate-y-0.5 active:shadow-press-sm transition-all"
        >
          Back to Chapters →
        </button>
      </motion.div>
    );
  }

  const isCorrectAnswer = answered && !!question && selected === question.correctAnswer;

  return (
    <motion.div
      className="min-h-screen bg-surface-cream flex flex-col px-4 py-5 gap-5"
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 16 }}
      transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
    >
      {/* Header */}
      <div className="space-y-3">
        <div className="flex items-center gap-3">
          <button
            onClick={() => router.push('/chapters')}
            className="w-10 h-10 flex items-center justify-center rounded-full text-ink-muted hover:bg-surface-muted transition-colors flex-shrink-0"
            aria-label="Back to chapters"
          >
            <span className="text-xl">←</span>
          </button>

          {/* Lesson progress */}
          <div className="flex-1 h-2.5 bg-surface-muted rounded-full overflow-hidden">
            <div
              className="h-full bg-spark-yellow rounded-full transition-all duration-500"
              style={{ width: `${pct}%` }}
              role="progressbar"
              aria-valuenow={pct}
              aria-valuemin={0}
              aria-valuemax={100}
              aria-label="Session accuracy"
            />
          </div>

          <button
            onClick={() => setTimedMode((m) => !m)}
            className={`text-xs font-body font-bold px-2.5 h-10 rounded-full transition-colors flex-shrink-0 ${
              timedMode ? 'bg-spark-amber-soft text-spark-amber' : 'text-ink-faint hover:bg-surface-muted'
            }`}
            aria-label={timedMode ? 'Disable timed mode' : 'Enable timed mode (60s per question)'}
          >
            {timedMode ? '⏱️ Timed' : '⏱️'}
          </button>
        </div>

        <div className="flex items-center justify-between px-1">
          <h1 className="font-display text-lg font-bold text-ink">{topicName}</h1>
          <span className="font-body text-sm font-bold text-ink-muted">
            {score.correct}/{score.attempted}
          </span>
        </div>

        {timedMode && !answered && (
          <div className={`text-center font-body text-sm font-bold ${timeLeft <= 10 ? 'text-spark-coral' : 'text-ink-faint'}`}>
            {timeLeft}s
          </div>
        )}
      </div>

      {/* Question area */}
      {loading ? (
        <div className="flex-1 flex items-center justify-center">
          <SparkMascot expression="idle" size={64} glow className="animate-bounce" />
        </div>
      ) : question ? (
        <>
          <QuestionCard
            question={question}
            answered={answered}
            selected={selected}
            onAnswer={handleAnswer}
          />

          {/* Feedback — restrained Spark reacts after the answer */}
          <AnimatePresence>
            {answered && feedback && (
              <motion.div
                className={`relative flex items-center gap-3 rounded-spark px-4 py-3 shadow-soft overflow-visible ${
                  isCorrectAnswer
                    ? 'bg-spark-green-soft'
                    : 'bg-spark-amber-soft'
                }`}
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2, delay: 0.05 }}
              >
                {/* Gentle sparkle burst on correct */}
                {isCorrectAnswer && (
                  <span aria-hidden="true" className="pointer-events-none absolute left-5 top-1 text-spark-yellow">
                    <span className="absolute animate-sparkle text-sm" style={{ animationDelay: '0ms' }}>✦</span>
                    <span className="absolute animate-sparkle text-xs left-3" style={{ animationDelay: '120ms' }}>✦</span>
                    <span className="absolute animate-sparkle text-[10px] left-6" style={{ animationDelay: '240ms' }}>✦</span>
                  </span>
                )}
                <span className={isCorrectAnswer ? 'animate-spark-pop' : ''}>
                  <SparkMascot expression={isCorrectAnswer ? 'cheer' : 'idle'} size={40} />
                </span>
                <span className={`font-body font-bold text-base ${isCorrectAnswer ? 'text-spark-green' : 'text-spark-amber'}`}>
                  {feedback}
                </span>
              </motion.div>
            )}
          </AnimatePresence>

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
              <div className="rounded-spark bg-spark-indigo-soft px-4 py-3 font-body text-sm text-spark-indigo-dark">
                <span className="font-bold">Why not {selected}?</span> {note}
              </div>
            ) : null;
          })()}

          {/* Attempt save error banner */}
          {attemptError && (
            <div className="font-body text-xs text-spark-amber text-center">
              Couldn&apos;t save your answer — tap Next to continue.
            </div>
          )}

          {/* Next question button — chunky + pressable */}
          {answered && (
            <button
              onClick={() => loadNext(studentId!, seenIds, cw, cr)}
              className="w-full bg-spark-indigo text-white font-body font-extrabold py-4 rounded-2xl text-lg shadow-press active:translate-y-0.5 active:shadow-press-sm transition-all"
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
                  className="font-body text-xs text-ink-faint hover:text-ink-muted transition-colors py-2"
                >
                  Something wrong with this question? 🚩
                </button>
              ) : (
                <div className="bg-surface-card rounded-spark shadow-soft p-4 text-left">
                  <p className="font-body text-xs font-bold text-ink-muted mb-2">What&apos;s the issue?</p>
                  <div className="space-y-1.5 mb-3">
                    {([
                      ['wrong_answer', 'The answer seems wrong'],
                      ['confusing',    'The question is confusing'],
                      ['too_hard',     'Way too hard for Grade 4'],
                      ['other',        'Something else'],
                    ] as const).map(([val, label]) => (
                      <label key={val} className="flex items-center gap-2 font-body text-xs text-ink cursor-pointer">
                        <input
                          type="radio"
                          name="flagReason"
                          value={val}
                          checked={flagReason === val}
                          onChange={() => setFlagReason(val)}
                          className="accent-spark-indigo"
                        />
                        {label}
                      </label>
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setShowFlagForm(false)}
                      className="flex-1 font-body text-xs text-ink-muted py-2.5 rounded-xl border border-surface-muted"
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
                      className="flex-1 font-body text-xs bg-spark-amber text-white py-2.5 rounded-xl font-bold"
                    >
                      Send report 🚩
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
          {answered && flagSent && (
            <p className="font-body text-xs text-center text-spark-green">Thanks for the report! We&apos;ll review it. ✅</p>
          )}
        </>
      ) : (
        <p className="text-center font-body text-ink-faint mt-16">No question loaded.</p>
      )}

      {/* Spark AI learning companion — floating chat bubble */}
      <ChatWidget
        studentName={studentName}
        topicName={topicName}
        questionText={question?.questionText ?? ''}
      />
    </motion.div>
  );
}
