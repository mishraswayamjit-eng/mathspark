'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import QuestionCard, { randomCorrect, randomWrong } from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import ProgressBar from '@/components/ProgressBar';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import { useSounds } from '@/hooks/useSounds';
import type { Question, AnswerKey } from '@/types';

const STREAK_MSG: Record<number, string> = {
  3: "You're on fire! 🔥",
  5: 'Unstoppable! ⚡',
  10: 'Math wizard! 🧙',
};

export default function PracticePage() {
  const params  = useParams();
  const router  = useRouter();
  const topicId = params.topicId as string;
  const { playCorrect, playWrong, playStreak, muted, toggleMute } = useSounds();

  const [studentId,    setStudentId]    = useState<string | null>(null);
  const [topicName,    setTopicName]    = useState('');
  const [question,     setQuestion]     = useState<Question | null>(null);
  const [loading,      setLoading]      = useState(true);
  const [answered,     setAnswered]     = useState(false);
  const [selected,     setSelected]     = useState<AnswerKey | null>(null);
  const [feedback,     setFeedback]     = useState('');
  const [isCorrect,    setIsCorrect]    = useState<boolean | null>(null);
  const [hintLevel,    setHintLevel]    = useState(0);
  const [seenIds,      setSeenIds]      = useState<string[]>([]);
  const [cw,           setCw]           = useState(0);
  const [cr,           setCr]           = useState(0);
  const [score,        setScore]        = useState({ correct: 0, attempted: 0 });
  const [noMore,       setNoMore]       = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [streakBanner, setStreakBanner] = useState('');

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
    setIsCorrect(null);
    setHintLevel(0);

    const qs = new URLSearchParams({
      topicId,
      studentId: sid,
      exclude: seen.join(','),
      cw: String(cwCur),
      cr: String(crCur),
    });

    const res = await fetch(`/api/questions/next?${qs}`);
    if (res.status === 404) { setNoMore(true); setLoading(false); return; }

    const q = await res.json();
    setQuestion(q);
    setLoading(false);
  }, [topicId]);

  // ── Boot ──────────────────────────────────────────────────────────────────
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
  async function handleAnswer(key: AnswerKey, correct: boolean) {
    if (!question || answered || !studentId) return;
    setAnswered(true);
    setSelected(key);
    setIsCorrect(correct);

    const newCr    = correct ? cr + 1 : 0;
    const newCw    = correct ? 0      : cw + 1;
    const newScore = {
      correct:   score.correct   + (correct ? 1 : 0),
      attempted: score.attempted + 1,
    };

    setCr(newCr);
    setCw(newCw);
    setScore(newScore);

    // Feedback
    let msg = correct ? randomCorrect() : randomWrong();
    if (correct && STREAK_MSG[newCr]) msg = STREAK_MSG[newCr];
    setFeedback(msg);

    // Sounds
    if (correct) {
      if (newCr === 3 || newCr === 5) {
        playStreak();
        setStreakBanner(STREAK_MSG[newCr] ?? '');
        setTimeout(() => setStreakBanner(''), 2000);
      } else {
        playCorrect();
      }
      setShowConfetti(true);
    } else {
      playWrong();
      setHintLevel(1);
    }

    // Record attempt
    fetch('/api/attempts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        studentId,
        questionId: question.id,
        topicId,
        selected: key,
        isCorrect: correct,
        hintUsed: hintLevel,
      }),
    }).catch(() => {/* ignore */});

    setSeenIds((prev) => [...prev, question.id]);
  }

  // ── Render ────────────────────────────────────────────────────────────────
  const pct = score.attempted > 0 ? Math.round((score.correct / score.attempted) * 100) : 0;

  // No more questions
  if (noMore) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-6 text-center bg-white">
        <div className="animate-sparky-dance">
          <Sparky mood="celebrating" size={140} />
        </div>
        <h2 className="text-2xl font-extrabold text-gray-800">You practised all questions here!</h2>
        <p className="text-gray-500 font-semibold">Score: {score.correct}/{score.attempted} correct</p>
        <DuoButton variant="green" fullWidth onClick={() => router.push('/chapters')}>
          Back to Home 📚
        </DuoButton>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-white">
      {/* Confetti */}
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

      {/* Streak banner */}
      {streakBanner && (
        <div className="fixed top-0 left-0 right-0 z-40 flex justify-center pointer-events-none">
          <div className="bg-[#FF9600] text-white font-extrabold px-6 py-3 text-center text-base animate-pop-in shadow-lg max-w-lg w-full">
            {streakBanner}
          </div>
        </div>
      )}

      {/* Dark header */}
      <div className="bg-[#131F24] px-4 py-3 flex items-center gap-3 sticky top-0 z-30">
        <button
          onClick={() => router.push('/chapters')}
          className="text-white/80 hover:text-white font-bold text-xl min-h-[44px] min-w-[44px] flex items-center justify-center"
          aria-label="Back"
        >
          ←
        </button>
        <div className="flex-1 min-w-0">
          <p className="text-white font-extrabold text-sm truncate">{topicName}</p>
          <p className="text-white/60 text-xs">{score.correct}/{score.attempted} correct</p>
        </div>
        <button
          onClick={toggleMute}
          className="text-white/80 hover:text-white text-xl min-h-[44px] min-w-[44px] flex items-center justify-center"
          aria-label={muted ? 'Unmute' : 'Mute'}
        >
          {muted ? '🔇' : '🔊'}
        </button>
      </div>

      {/* Progress bar */}
      <ProgressBar value={pct} height="h-3" />

      {/* Question area */}
      <div className="flex-1 px-4 py-5 space-y-4 pb-0">
        {loading ? (
          <div className="flex flex-col items-center justify-center gap-4 pt-20">
            <div className="animate-sparky-bounce">
              <Sparky mood="thinking" size={100} />
            </div>
            <p className="text-gray-400 font-semibold">Loading question…</p>
          </div>
        ) : question ? (
          <>
            <QuestionCard
              question={question}
              answered={answered}
              selected={selected}
              onAnswer={handleAnswer}
            />

            {/* Hint system and step-by-step — only visible when not showing panel */}
            {answered && !isCorrect && (
              <div className="space-y-3">
                <HintSystem
                  hint1={question.hint1}
                  hint2={question.hint2}
                  hint3={question.hint3}
                  level={hintLevel}
                  onLevelUp={(n) => setHintLevel(n)}
                />
              </div>
            )}

            {answered && question.stepByStep?.length > 0 && (
              <StepByStep steps={question.stepByStep} />
            )}

            {/* Misconception note */}
            {answered && selected !== question.correctAnswer && (() => {
              const k = `misconception${selected}` as keyof Question;
              const note = question[k] as string;
              return note ? (
                <div className="rounded-2xl bg-blue-50 border-2 border-blue-100 px-4 py-3 text-sm text-blue-700 font-medium">
                  <span className="font-extrabold">Why not {selected}?</span> {note}
                </div>
              ) : null;
            })()}
          </>
        ) : (
          <p className="text-center text-gray-400 mt-16">No question loaded.</p>
        )}
      </div>

      {/* Sliding answer panel — animates up from bottom after answer */}
      {answered && question && (
        <div
          className={`fixed bottom-0 left-0 right-0 max-w-lg mx-auto z-[60] animate-slide-up ${
            isCorrect
              ? 'bg-[#58CC02]'
              : 'bg-[#FFF0F0] border-t-2 border-[#FF4B4B]'
          }`}
          style={{ minHeight: '180px' }}
        >
          <div className="px-4 py-4 flex items-start gap-4">
            {/* Sparky */}
            <div className={isCorrect ? 'animate-sparky-dance' : ''}>
              <Sparky
                mood={isCorrect ? 'celebrating' : 'encouraging'}
                size={80}
              />
            </div>
            {/* Text + button */}
            <div className="flex-1 space-y-3">
              <p className={`text-lg font-extrabold ${isCorrect ? 'text-white' : 'text-[#FF4B4B]'}`}>
                {feedback}
              </p>
              {!isCorrect && question.hint1 && (
                <p className="text-sm text-gray-600 font-medium">{question.hint1}</p>
              )}
              <DuoButton
                variant={isCorrect ? 'white' : 'red'}
                fullWidth
                onClick={() => loadNext(studentId!, seenIds, cw, cr)}
              >
                {isCorrect ? 'CONTINUE →' : 'GOT IT'}
              </DuoButton>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
