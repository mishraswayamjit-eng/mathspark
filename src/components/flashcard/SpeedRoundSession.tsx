'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useFlashcardDeck } from '@/hooks/useFlashcardDeck';
import dynamic from 'next/dynamic';
import ProgressDots from './ProgressDots';
import Confetti from '@/components/Confetti';
import Sparky from '@/components/Sparky';
import { useSounds } from '@/hooks/useSounds';
import {
  generateQuizQuestions,
  type QuizQuestion,
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

type Phase = 'loading' | 'countdown' | 'playing' | 'complete';

const OPTION_LABELS = ['A', 'B', 'C', 'D'];
const ROUND_DURATION_MS = 60_000; // 60 seconds

// ── Speed Complete Screen ────────────────────────────────────────────────────

function SpeedComplete({
  answered,
  correctCount,
  maxStreak,
  sessionXP,
  onPlayAgain,
  onDone,
}: {
  answered: number;
  correctCount: number;
  maxStreak: number;
  sessionXP: { total: number; streakMultiplier: number; streakBonus: number } | null;
  onPlayAgain: () => void;
  onDone: () => void;
}) {
  const pct = answered > 0 ? Math.round((correctCount / answered) * 100) : 0;
  const speed = (correctCount / 60).toFixed(1); // cards per second

  return (
    <div className="fixed inset-0 z-50 bg-[#0F172A] flex flex-col items-center justify-center px-6 animate-fade-in">
      {correctCount >= 15 && <Confetti />}

      <div className={correctCount >= 15 ? 'animate-sparky-dance' : 'animate-sparky-bounce'}>
        <Sparky mood={correctCount >= 15 ? 'celebrating' : correctCount >= 8 ? 'happy' : 'encouraging'} size={80} />
      </div>

      <h1 className="text-2xl font-black text-[#F1F5F9] mt-3 mb-1">
        {correctCount >= 20 ? 'Lightning Fast!' : correctCount >= 12 ? 'Speed Demon!' : correctCount >= 6 ? 'Quick Thinker!' : 'Good Effort!'}
      </h1>

      {/* Big number + XP */}
      <p className="text-5xl font-black text-[#FBBF24] tabular-nums mb-0.5">{correctCount}</p>
      <p className="text-xs text-[#64748B] uppercase tracking-wider mb-1">correct in 60s</p>
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
      <div className="grid grid-cols-4 gap-2 w-full max-w-sm mb-6">
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#F1F5F9] tabular-nums">{answered}</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Answered</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#34D399] tabular-nums">{pct}%</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Accuracy</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#FBBF24] tabular-nums">🔥{maxStreak}</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Streak</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#A78BFA] tabular-nums">{speed}</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider">/sec</p>
        </div>
      </div>

      {/* Buttons */}
      <div className="w-full max-w-sm space-y-3">
        <button
          onClick={onPlayAgain}
          className="w-full py-3.5 rounded-2xl font-bold text-white text-sm"
          style={{ background: 'linear-gradient(135deg, #EF4444, #DC2626)' }}
        >
          Go Again 🔥
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

// ── Main Speed Round Component ───────────────────────────────────────────────

interface SpeedRoundSessionProps {
  deckId: string;
}

export default function SpeedRoundSession({ deckId }: SpeedRoundSessionProps) {
  const router = useRouter();
  const { fetchDeck } = useFlashcardDeck(deckId, { limit: 40 });
  const { playCorrect, playWrong, playStreak, playMastery } = useSounds();

  const [phase, setPhase] = useState<Phase>('loading');
  const [questions, setQuestions] = useState<QuizQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  // Global timer
  const [timeRemaining, setTimeRemaining] = useState(ROUND_DURATION_MS);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Stats
  const [correctCount, setCorrectCount] = useState(0);
  const [answered, setAnswered] = useState(0);
  const [streak, setStreak] = useState(0);
  const [maxStreak, setMaxStreak] = useState(0);

  // Countdown before start
  const [countdownNum, setCountdownNum] = useState(3);

  // Feedback flash
  const [flashColor, setFlashColor] = useState<'green' | 'red' | null>(null);

  // Session
  const sessionSavedRef = useRef(false);

  // XP tracking
  const [sessionXP, setSessionXP] = useState<{ total: number; streakMultiplier: number; streakBonus: number } | null>(null);

  // ── Load deck ──────────────────────────────────────────────────────────────

  const loadDeck = useCallback(() => {
    const grade = localStorage.getItem('mathspark_student_grade') || '4';

    fetchDeck()
      .then((data) => {
        if (!data || data.cards.length === 0) {
          setPhase('complete');
        } else {
          const gradeNum = parseInt(grade, 10);
          const qs = generateQuizQuestions(data.cards as CardWithProgress[], gradeNum);
          setQuestions(qs);
          setPhase('countdown');
        }
      })
      .catch(() => router.replace('/flashcards'));
  }, [fetchDeck, router]);

  useEffect(() => { loadDeck(); }, [loadDeck]);

  // ── 3-2-1 Countdown ───────────────────────────────────────────────────────

  useEffect(() => {
    if (phase !== 'countdown') return;

    if (countdownNum <= 0) {
      setPhase('playing');
      return;
    }

    const t = setTimeout(() => setCountdownNum((n) => n - 1), 800);
    return () => clearTimeout(t);
  }, [phase, countdownNum]);

  // ── Global timer ───────────────────────────────────────────────────────────

  useEffect(() => {
    if (phase !== 'playing') return;

    timerRef.current = setInterval(() => {
      setTimeRemaining((prev) => {
        const next = prev - 100;
        if (next <= 0) {
          clearInterval(timerRef.current!);
          setPhase('complete');
          return 0;
        }
        return next;
      });
    }, 100);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [phase]);

  // ── Save session on complete ───────────────────────────────────────────────

  useEffect(() => {
    if (phase !== 'complete' || sessionSavedRef.current) return;
    sessionSavedRef.current = true;

    const sid = localStorage.getItem('mathspark_student_id');
    if (!sid) return;

    playMastery();

    fetch('/api/flashcards/session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mode: 'speed',
        cardsReviewed: answered,
        cardsCorrect: correctCount,
        duration: 60,
      }),
    })
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        if (data.ok && data.xp) {
          setSessionXP({ total: data.xp.total, streakMultiplier: data.xp.streakMultiplier, streakBonus: data.xp.streakBonus });
        }
      })
      .catch((err) => console.error('[fetch]', err));
  }, [phase, answered, correctCount, playMastery]);

  // ── Handle answer ──────────────────────────────────────────────────────────

  const handleAnswer = useCallback(
    (optionId: string) => {
      if (phase !== 'playing') return;

      const q = questions[currentIndex];
      if (!q) return;

      const selected = q.options.find((o) => o.id === optionId);
      const correct = selected?.isCorrect ?? false;

      setAnswered((prev) => prev + 1);

      // Update Leitner (fire-and-forget)
      const sid = localStorage.getItem('mathspark_student_id');
      if (sid) {
        fetch('/api/flashcards/progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ cardId: q.cardId, correct }),
        }).catch((err) => console.error('[fetch]', err));
      }

      if (correct) {
        const newStreak = streak + 1;
        setCorrectCount((prev) => prev + 1);
        setStreak(newStreak);
        setMaxStreak((prev) => Math.max(prev, newStreak));
        setFlashColor('green');

        if (newStreak === 3 || newStreak === 5 || newStreak === 7 || newStreak === 10) {
          playStreak();
        } else {
          playCorrect();
        }
      } else {
        setStreak(0);
        setFlashColor('red');
        playWrong();
      }

      // Flash then instant advance
      setTimeout(() => {
        setFlashColor(null);
        const next = currentIndex + 1;
        if (next >= questions.length) {
          // Ran out of questions — end round
          if (timerRef.current) clearInterval(timerRef.current);
          setPhase('complete');
        } else {
          setCurrentIndex(next);
        }
      }, 300);
    },
    [phase, questions, currentIndex, streak, playCorrect, playWrong, playStreak],
  );

  // ── Keyboard shortcuts ─────────────────────────────────────────────────────

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (phase !== 'playing') return;
      const key = e.key.toUpperCase();
      if (OPTION_LABELS.includes(key)) handleAnswer(key);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [phase, handleAnswer]);

  // ── Render: Loading ────────────────────────────────────────────────────────

  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center">
        <div className="text-5xl animate-sparky-bounce mb-4">🔥</div>
        <p className="text-[#94A3B8] text-sm">Preparing speed round...</p>
      </div>
    );
  }

  // ── Render: Countdown ──────────────────────────────────────────────────────

  if (phase === 'countdown') {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center">
        <p className="text-xs text-[#64748B] uppercase tracking-widest mb-4">Get Ready!</p>
        <div className="animate-combo-bounce" key={countdownNum}>
          <span className="text-8xl font-black text-[#F1F5F9] tabular-nums">
            {countdownNum > 0 ? countdownNum : 'GO!'}
          </span>
        </div>
        <p className="text-sm text-[#94A3B8] mt-6">60 seconds · Answer as many as you can!</p>
      </div>
    );
  }

  // ── Render: Complete ───────────────────────────────────────────────────────

  if (phase === 'complete') {
    return (
      <SpeedComplete
        answered={answered}
        correctCount={correctCount}
        maxStreak={maxStreak}
        sessionXP={sessionXP}
        onPlayAgain={() => {
          sessionSavedRef.current = false;
          setCurrentIndex(0);
          setCorrectCount(0);
          setAnswered(0);
          setStreak(0);
          setMaxStreak(0);
          setTimeRemaining(ROUND_DURATION_MS);
          setCountdownNum(3);
          setFlashColor(null);
          setSessionXP(null);
          setPhase('loading');
          loadDeck();
        }}
        onDone={() => router.push('/flashcards')}
      />
    );
  }

  // ── Render: Playing ────────────────────────────────────────────────────────

  const q = questions[currentIndex];
  if (!q) return null;

  const pct = timeRemaining / ROUND_DURATION_MS;
  const barColor = pct > 0.5 ? '#34D399' : pct > 0.2 ? '#F59E0B' : '#EF4444';
  const seconds = Math.ceil(timeRemaining / 1000);

  // Screen flash overlay
  const flashOverlay = flashColor === 'green'
    ? 'bg-duo-green/10'
    : flashColor === 'red'
    ? 'bg-red-500/10'
    : '';

  return (
    <div className={`min-h-screen bg-[#0F172A] flex flex-col transition-colors duration-150 ${flashOverlay}`}>
      {/* ── Top bar ──────────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-30 bg-[#0F172A]/95 backdrop-blur-md px-4 py-2">
        <div className="flex items-center justify-between max-w-md mx-auto mb-1.5">
          <button
            onClick={() => {
              if (timerRef.current) clearInterval(timerRef.current);
              setPhase('complete');
            }}
            className="text-[#94A3B8] text-sm font-bold"
          >
            ✕
          </button>

          <div className="flex items-center gap-3">
            {/* Timer number */}
            <span className={`text-lg font-black tabular-nums ${seconds <= 10 ? 'text-red-400 animate-timer-urgent' : 'text-[#F1F5F9]'}`}>
              {seconds}s
            </span>

            {/* Score */}
            <span className="text-sm font-bold text-[#FBBF24] tabular-nums">
              ✓ {correctCount}
            </span>

            {/* Streak */}
            {streak >= 3 && (
              <span className="text-sm font-black text-amber-400 animate-pulse tabular-nums">
                🔥{streak}
              </span>
            )}
          </div>

          <span className="text-xs text-[#64748B] tabular-nums">
            #{answered + 1}
          </span>
        </div>

        {/* Timer bar */}
        <div className="max-w-md mx-auto h-1.5 bg-white/5 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-[width] duration-100"
            style={{
              width: `${pct * 100}%`,
              background: barColor,
            }}
          />
        </div>
      </div>

      {/* ── Question area ────────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col items-center px-4 py-3 max-w-md mx-auto w-full">
        {/* Question text */}
        <div className="w-full bg-[#1E293B] rounded-2xl px-5 py-4 mb-4 text-center animate-flashcard-slide-up" key={currentIndex}>
          <p className="text-[#F1F5F9] text-base font-bold leading-relaxed">
            {q.cardFront}
          </p>
          {q.cardFormula && (
            <div className="mt-2">
              <KatexRenderer latex={q.cardFormula} displayMode className="text-[#F1F5F9]" />
            </div>
          )}
        </div>

        {/* ── Options ─────────────────────────────────────────────────────────── */}
        <div className="w-full grid grid-cols-2 gap-2">
          {q.options.map((opt) => (
            <button
              key={opt.id}
              onClick={() => handleAnswer(opt.id)}
              className="flex items-center gap-2 rounded-xl px-3 py-3 border border-white/10 bg-[#1E293B] active:scale-[0.95] transition-[transform,background-color,border-color]"
            >
              <span className="flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center text-xs font-black bg-white/10 text-[#F1F5F9]">
                {opt.id}
              </span>
              <span className="text-xs font-bold text-[#F1F5F9] text-left flex-1 leading-tight">
                {opt.text}
              </span>
            </button>
          ))}
        </div>

        {/* Keyboard hint */}
        <p className="mt-3 text-[10px] text-[#475569] hidden sm:block">
          Press A, B, C, or D · Speed is everything!
        </p>
      </div>
    </div>
  );
}
