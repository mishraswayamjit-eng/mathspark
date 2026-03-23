'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import TimerCircle from './TimerCircle';
import ProgressDots from './ProgressDots';
import Confetti from '@/components/Confetti';
import Sparky from '@/components/Sparky';
import { useSounds } from '@/hooks/useSounds';
import {
  generateQuizQuestions,
  calculatePoints,
  getComboMultiplier,
  type QuizQuestion,
  type QuizOption,
} from '@/lib/quizBlitz';
import type { FlashCard } from '@/types';

const KatexRenderer = dynamic(() => import('@/components/KatexRenderer'), { ssr: false });

// ── Types ────────────────────────────────────────────────────────────────────

interface CardWithProgress extends FlashCard {
  leitnerBox: number;
  timesSeen: number;
  timesCorrect: number;
  streakOnCard: number;
}

interface BoxTransition {
  cardId: string;
  cardFront: string;
  oldBox: number;
  newBox: number;
  leveledUp: boolean;
  reachedMastery: boolean;
}

type Phase = 'loading' | 'playing' | 'feedback' | 'complete';

const OPTION_LABELS = ['A', 'B', 'C', 'D'];
const BOX_NAMES = ['New', 'Rookie', 'Rising', 'Strong', 'Expert', 'Master'];
const BOX_COLORS = ['#64748B', '#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6', '#34D399'];

// ── Quiz Complete Screen ─────────────────────────────────────────────────────

function QuizComplete({
  score,
  totalQuestions,
  correctCount,
  maxCombo,
  duration,
  transitions,
  sessionXP,
  onPlayAgain,
  onDone,
}: {
  score: number;
  totalQuestions: number;
  correctCount: number;
  maxCombo: number;
  duration: number;
  transitions: BoxTransition[];
  sessionXP: { total: number; streakMultiplier: number; streakBonus: number } | null;
  onPlayAgain: () => void;
  onDone: () => void;
}) {
  const pct = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;
  const mins = Math.floor(duration / 60);
  const secs = duration % 60;
  const promoted = transitions.filter((t) => t.leveledUp);
  const mastered = transitions.filter((t) => t.reachedMastery);

  return (
    <div className="fixed inset-0 z-50 bg-[#0F172A] flex flex-col items-center justify-center px-6 animate-fade-in overflow-y-auto">
      {pct >= 80 && <Confetti />}

      <div className={pct >= 70 ? 'animate-sparky-dance' : 'animate-sparky-bounce'}>
        <Sparky mood={pct >= 70 ? 'celebrating' : pct >= 40 ? 'happy' : 'encouraging'} size={80} />
      </div>

      <h1 className="text-2xl font-black text-[#F1F5F9] mt-3 mb-1">
        {pct >= 80 ? 'Quiz Master!' : pct >= 60 ? 'Great Blitz!' : 'Good Try!'}
      </h1>

      {/* Score + XP */}
      <p className="text-4xl font-black text-[#FBBF24] tabular-nums mb-0.5">{score}</p>
      <p className="text-xs text-[#64748B] uppercase tracking-wider mb-1">points</p>
      {sessionXP && sessionXP.total > 0 && (
        <div className="flex items-center gap-1.5 mb-5">
          <span className="text-sm font-black text-[#34D399]">+{sessionXP.total} XP</span>
          {sessionXP.streakBonus > 0 && (
            <span className="text-[10px] text-[#FBBF24]">({sessionXP.streakMultiplier}x streak)</span>
          )}
        </div>
      )}
      {(!sessionXP || sessionXP.total <= 0) && <div className="mb-5" />}

      {/* Stats grid */}
      <div className="grid grid-cols-4 gap-2 w-full max-w-sm mb-5">
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#34D399] tabular-nums">{pct}%</p>
          <p className="text-[9px] text-[#64748B] uppercase tracking-wider">Accuracy</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#F1F5F9] tabular-nums">{correctCount}/{totalQuestions}</p>
          <p className="text-[9px] text-[#64748B] uppercase tracking-wider">Correct</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#FBBF24] tabular-nums">🔥{maxCombo}</p>
          <p className="text-[9px] text-[#64748B] uppercase tracking-wider">Max Combo</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#60A5FA] tabular-nums">
            {mins > 0 ? `${mins}m` : `${secs}s`}
          </p>
          <p className="text-[9px] text-[#64748B] uppercase tracking-wider">Time</p>
        </div>
      </div>

      {/* Transitions */}
      {promoted.length > 0 && (
        <div className="w-full max-w-sm bg-emerald-500/10 border border-emerald-500/20 rounded-xl px-3 py-2.5 mb-3">
          <p className="text-xs font-bold text-emerald-400 mb-1">
            ⬆️ {promoted.length} card{promoted.length > 1 ? 's' : ''} leveled up
          </p>
          {promoted.slice(0, 4).map((t) => (
            <div key={t.cardId} className="flex items-center gap-2 py-0.5">
              <span className="text-[10px] text-[#94A3B8] truncate flex-1">{t.cardFront}</span>
              <span
                className="text-[10px] font-bold px-1.5 py-0.5 rounded"
                style={{ color: BOX_COLORS[t.oldBox], background: BOX_COLORS[t.oldBox] + '20' }}
              >
                {BOX_NAMES[t.oldBox]}
              </span>
              <span className="text-[#64748B] text-[10px]">→</span>
              <span
                className="text-[10px] font-bold px-1.5 py-0.5 rounded"
                style={{ color: BOX_COLORS[t.newBox], background: BOX_COLORS[t.newBox] + '20' }}
              >
                {BOX_NAMES[t.newBox]}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Buttons */}
      <div className="w-full max-w-sm space-y-3 pb-8">
        <button
          onClick={onPlayAgain}
          className="w-full py-3.5 rounded-2xl font-bold text-white text-sm"
          style={{ background: 'linear-gradient(135deg, #FBBF24, #F59E0B)' }}
        >
          Play Again ⚡
        </button>
        <button
          onClick={onDone}
          className="w-full py-3.5 rounded-2xl font-bold text-[#94A3B8] text-sm bg-[#1E293B]"
        >
          Done
        </button>
      </div>
    </div>
  );
}

// ── Main Quiz Blitz Component ────────────────────────────────────────────────

interface QuizBlitzSessionProps {
  deckId: string;
}

export default function QuizBlitzSession({ deckId }: QuizBlitzSessionProps) {
  const router = useRouter();
  const { playCorrect, playWrong, playStreak, playMastery } = useSounds();

  const [phase, setPhase] = useState<Phase>('loading');
  const [deckName, setDeckName] = useState('');
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  // Scoring
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(0);
  const [maxCombo, setMaxCombo] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);

  // Timer
  const [timeRemaining, setTimeRemaining] = useState(0);
  const questionStartRef = useRef(Date.now());
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Feedback state
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);

  // Transitions & session
  const [transitions, setTransitions] = useState<BoxTransition[]>([]);
  const [startTime] = useState(() => Date.now());
  const sessionSavedRef = useRef(false);

  // XP tracking
  const [sessionXP, setSessionXP] = useState<{ total: number; streakMultiplier: number; streakBonus: number } | null>(null);
  const accumulatedBonusRef = useRef(0);

  // Points animation
  const [pointsPopup, setPointsPopup] = useState<{ points: number; key: number } | null>(null);

  // ── Load deck & generate questions ─────────────────────────────────────────

  useEffect(() => {
    const sid = localStorage.getItem('mathspark_student_id');
    const grade = localStorage.getItem('mathspark_student_grade') || '4';
    if (!sid) {
      router.replace('/start');
      return;
    }

    fetch(`/api/flashcards/deck?studentId=${sid}&grade=${grade}&deck=${encodeURIComponent(deckId)}`)
      .then((r) => r.json())
      .then((data) => {
        if (data.cards && data.cards.length > 0) {
          const gradeNum = parseInt(grade, 10);
          const qs = generateQuizQuestions(data.cards, gradeNum);
          setQuestions(qs);
          setDeckName(data.deckName ?? 'Quiz Blitz');
          setPhase('playing');
          setTimeRemaining(qs[0]?.timeLimitMs ?? 12000);
          questionStartRef.current = Date.now();
        } else {
          setDeckName(data.deckName ?? 'Empty');
          setPhase('complete');
        }
      })
      .catch(() => router.replace('/flashcards'));
  }, [router, deckId]);

  // ── Timer tick ─────────────────────────────────────────────────────────────

  useEffect(() => {
    if (phase !== 'playing' || isAnswered) return;

    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        const next = prev - 100;
        if (next <= 0) {
          // Time's up — auto-wrong
          clearInterval(timerRef.current!);
          handleTimeout();
          return 0;
        }
        return next;
      });
    }, 100);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase, isAnswered, currentIndex]);

  // ── Save session ───────────────────────────────────────────────────────────

  const saveSession = useCallback(() => {
    if (sessionSavedRef.current) return;
    sessionSavedRef.current = true;

    const sid = localStorage.getItem('mathspark_student_id');
    if (!sid) return;

    const duration = Math.round((Date.now() - startTime) / 1000);

    fetch('/api/flashcards/session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        studentId: sid,
        mode: 'quiz',
        cardsReviewed: questions.length,
        cardsCorrect: correctCount,
        duration,
        bonusXP: accumulatedBonusRef.current,
      }),
    })
      .then((r) => r.json())
      .then((data) => {
        if (data.ok && data.xp) {
          setSessionXP({ total: data.xp.total, streakMultiplier: data.xp.streakMultiplier, streakBonus: data.xp.streakBonus });
        }
      })
      .catch(() => {});
  }, [startTime, questions.length, correctCount]);

  // ── Handle answer ──────────────────────────────────────────────────────────

  const handleAnswer = useCallback(
    (optionId: string) => {
      if (isAnswered || phase !== 'playing') return;

      if (timerRef.current) clearInterval(timerRef.current);
      setIsAnswered(true);
      setSelectedOption(optionId);

      const q = questions[currentIndex];
      if (!q) return;

      const selected = q.options.find((o) => o.id === optionId);
      const correct = selected?.isCorrect ?? false;
      const timeTaken = Date.now() - questionStartRef.current;

      // Update Leitner progress
      const sid = localStorage.getItem('mathspark_student_id');
      if (sid) {
        fetch('/api/flashcards/progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            studentId: sid,
            cardId: q.cardId,
            correct,
          }),
        })
          .then((r) => r.json())
          .then((data) => {
            if (data.ok) {
              setTransitions((prev) => [
                ...prev,
                {
                  cardId: q.cardId,
                  cardFront: q.cardFront.length > 40 ? q.cardFront.slice(0, 40) + '...' : q.cardFront,
                  oldBox: data.oldBox,
                  newBox: data.newBox,
                  leveledUp: data.leveledUp,
                  reachedMastery: data.reachedMastery,
                },
              ]);
              // Track bonus XP for session multiplier
              const bonus = (data.xpBreakdown?.levelUpBonus ?? 0) + (data.xpBreakdown?.masteryBonus ?? 0);
              if (bonus > 0) accumulatedBonusRef.current += bonus;
            }
          })
          .catch(() => {});
      }

      if (correct) {
        const newCombo = combo + 1;
        const pts = calculatePoints(timeTaken, newCombo);
        setScore((prev) => prev + pts);
        setCombo(newCombo);
        setMaxCombo((prev) => Math.max(prev, newCombo));
        setCorrectCount((prev) => prev + 1);
        setPointsPopup({ points: pts, key: Date.now() });

        // Sound
        if (newCombo === 3 || newCombo === 5 || newCombo === 7) {
          playStreak();
        } else {
          playCorrect();
        }
      } else {
        setCombo(0);
        playWrong();
      }

      // Auto-advance after feedback delay
      setTimeout(() => advanceQuestion(), correct ? 1200 : 1800);
    },
    [isAnswered, phase, questions, currentIndex, combo, playCorrect, playWrong, playStreak],
  );

  // ── Handle timeout ─────────────────────────────────────────────────────────

  const handleTimeout = useCallback(() => {
    if (isAnswered) return;
    setIsAnswered(true);
    setSelectedOption(null); // no selection
    setCombo(0);
    playWrong();

    // Update Leitner as wrong
    const q = questions[currentIndex];
    const sid = localStorage.getItem('mathspark_student_id');
    if (sid && q) {
      fetch('/api/flashcards/progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ studentId: sid, cardId: q.cardId, correct: false }),
      })
        .then((r) => r.json())
        .then((data) => {
          if (data.ok) {
            setTransitions((prev) => [
              ...prev,
              {
                cardId: q.cardId,
                cardFront: q.cardFront.length > 40 ? q.cardFront.slice(0, 40) + '...' : q.cardFront,
                oldBox: data.oldBox,
                newBox: data.newBox,
                leveledUp: false,
                reachedMastery: false,
              },
            ]);
          }
        })
        .catch(() => {});
    }

    setTimeout(() => advanceQuestion(), 1500);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAnswered, questions, currentIndex, playWrong]);

  // ── Advance to next question ───────────────────────────────────────────────

  const advanceQuestion = useCallback(() => {
    const nextIdx = currentIndex + 1;
    if (nextIdx >= questions.length) {
      setPhase('complete');
      return;
    }

    setCurrentIndex(nextIdx);
    setIsAnswered(false);
    setSelectedOption(null);
    setPointsPopup(null);
    setTimeRemaining(questions[nextIdx]?.timeLimitMs ?? 12000);
    questionStartRef.current = Date.now();
  }, [currentIndex, questions]);

  // Save on complete
  useEffect(() => {
    if (phase === 'complete' && questions.length > 0) {
      saveSession();
    }
  }, [phase, questions.length, saveSession]);

  // ── Keyboard shortcuts ─────────────────────────────────────────────────────

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (phase !== 'playing' || isAnswered) return;
      const key = e.key.toUpperCase();
      if (OPTION_LABELS.includes(key)) {
        handleAnswer(key);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [phase, isAnswered, handleAnswer]);

  // ── Render: Loading ────────────────────────────────────────────────────────

  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center">
        <div className="text-5xl animate-sparky-bounce mb-4">⚡</div>
        <p className="text-[#94A3B8] text-sm">Preparing quiz...</p>
      </div>
    );
  }

  // ── Render: Complete ───────────────────────────────────────────────────────

  if (phase === 'complete') {
    const duration = Math.round((Date.now() - startTime) / 1000);
    return (
      <QuizComplete
        score={score}
        totalQuestions={questions.length}
        correctCount={correctCount}
        maxCombo={maxCombo}
        duration={duration}
        transitions={transitions}
        sessionXP={sessionXP}
        onPlayAgain={() => {
          sessionSavedRef.current = false;
          setCurrentIndex(0);
          setScore(0);
          setCombo(0);
          setMaxCombo(0);
          setCorrectCount(0);
          setTransitions([]);
          setIsAnswered(false);
          setSelectedOption(null);
          setSessionXP(null);
          accumulatedBonusRef.current = 0;
          setPhase('loading');

          const sid = localStorage.getItem('mathspark_student_id');
          const grade = localStorage.getItem('mathspark_student_grade') || '4';
          if (!sid) return;

          fetch(`/api/flashcards/deck?studentId=${sid}&grade=${grade}&deck=${encodeURIComponent(deckId)}`)
            .then((r) => r.json())
            .then((data) => {
              if (data.cards?.length > 0) {
                const gradeNum = parseInt(grade, 10);
                const qs = generateQuizQuestions(data.cards, gradeNum);
                setQuestions(qs);
                setPhase('playing');
                setTimeRemaining(qs[0]?.timeLimitMs ?? 12000);
                questionStartRef.current = Date.now();
              } else {
                setPhase('complete');
              }
            })
            .catch(() => router.replace('/flashcards'));
        }}
        onDone={() => router.push('/flashcards')}
      />
    );
  }

  // ── Render: Playing ────────────────────────────────────────────────────────

  const q = questions[currentIndex];
  if (!q) return null;

  const correctOption = q.options.find((o) => o.isCorrect);
  const comboMult = getComboMultiplier(combo);

  return (
    <div className="min-h-screen bg-[#0F172A] flex flex-col">
      {/* ── Top bar ────────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-30 bg-[#0F172A]/95 backdrop-blur-md border-b border-white/5 px-4 py-2.5">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <button
            onClick={() => {
              if (currentIndex > 0) saveSession();
              router.push('/flashcards');
            }}
            className="text-[#94A3B8] text-sm font-bold"
          >
            ✕
          </button>

          <div className="flex items-center gap-3">
            {/* Score */}
            <div className="flex items-center gap-1 relative">
              <span className="text-xs font-bold text-[#FBBF24] tabular-nums">{score} pts</span>
              {/* Points popup */}
              {pointsPopup && (
                <span
                  key={pointsPopup.key}
                  className="absolute -top-5 left-1/2 -translate-x-1/2 text-xs font-black text-[#34D399] animate-xp-float"
                >
                  +{pointsPopup.points}
                </span>
              )}
            </div>

            {/* Combo */}
            {combo >= 3 && (
              <span className="text-xs font-black text-amber-400 animate-pulse tabular-nums">
                🔥{combo} ({comboMult}x)
              </span>
            )}
          </div>

          <span className="text-xs text-[#64748B] tabular-nums">
            {currentIndex + 1}/{questions.length}
          </span>
        </div>

        <div className="max-w-md mx-auto mt-1">
          <ProgressDots total={questions.length} current={currentIndex} completed={currentIndex} />
        </div>
      </div>

      {/* ── Question area ──────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col items-center px-4 py-4 max-w-md mx-auto w-full">
        {/* Timer */}
        <div className="mb-4">
          <TimerCircle
            totalMs={q.timeLimitMs}
            remainingMs={timeRemaining}
            size={52}
          />
        </div>

        {/* Topic + difficulty */}
        <div className="flex items-center gap-2 mb-3">
          <span className="text-[10px] font-bold uppercase tracking-wider text-[#64748B]">
            {q.topicName}
          </span>
          <div className="flex gap-0.5">
            {[1, 2, 3].map((d) => (
              <div
                key={d}
                className={`w-1.5 h-1.5 rounded-full ${d <= q.difficulty ? 'bg-[#F59E0B]' : 'bg-white/10'}`}
              />
            ))}
          </div>
        </div>

        {/* Question text */}
        <div className="w-full bg-[#1E293B] rounded-2xl px-5 py-5 mb-5 text-center">
          <p className="text-[#F1F5F9] text-lg font-bold leading-relaxed">
            {q.cardFront}
          </p>
          {q.cardFormula && (
            <div className="mt-3">
              <KatexRenderer
                latex={q.cardFormula}
                displayMode
                className="text-[#F1F5F9] text-xl"
              />
            </div>
          )}
        </div>

        {/* ── Options ───────────────────────────────────────────────────────── */}
        <div className="w-full space-y-2.5">
          {q.options.map((opt) => {
            let bgClass = 'bg-[#1E293B] border-white/10';
            let textClass = 'text-[#F1F5F9]';
            let labelBg = 'bg-white/10';

            if (isAnswered) {
              if (opt.isCorrect) {
                bgClass = 'bg-emerald-500/20 border-emerald-500/40';
                textClass = 'text-emerald-300';
                labelBg = 'bg-emerald-500/30';
              } else if (selectedOption === opt.id && !opt.isCorrect) {
                bgClass = 'bg-red-500/20 border-red-500/40';
                textClass = 'text-red-300';
                labelBg = 'bg-red-500/30';
              } else {
                bgClass = 'bg-[#1E293B]/50 border-white/5';
                textClass = 'text-[#64748B]';
              }
            }

            return (
              <button
                key={opt.id}
                onClick={() => handleAnswer(opt.id)}
                disabled={isAnswered}
                className={`w-full flex items-center gap-3 rounded-xl px-4 py-3.5 border transition-[colors,border-color,transform] ${bgClass} ${
                  isAnswered ? 'cursor-default' : 'active:scale-[0.97]'
                }`}
              >
                <span
                  className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-sm font-black ${labelBg} ${textClass}`}
                >
                  {opt.id}
                </span>
                <span className={`text-sm font-bold text-left flex-1 ${textClass}`}>
                  {opt.text}
                </span>
                {isAnswered && opt.isCorrect && (
                  <span className="text-emerald-400 flex-shrink-0">✓</span>
                )}
                {isAnswered && selectedOption === opt.id && !opt.isCorrect && (
                  <span className="text-red-400 flex-shrink-0">✗</span>
                )}
              </button>
            );
          })}
        </div>

        {/* Timeout message */}
        {isAnswered && selectedOption === null && (
          <div className="mt-4 text-center">
            <p className="text-sm text-red-400 font-bold">
              Time&apos;s up! Answer was: {correctOption?.text}
            </p>
          </div>
        )}

        {/* Keyboard hint (desktop) */}
        <p className="mt-4 text-[10px] text-[#475569] hidden sm:block">
          Press A, B, C, or D to answer
        </p>
      </div>
    </div>
  );
}
