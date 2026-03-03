'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import FlashCardComponent from '@/components/flashcard/FlashCard';
import ProgressDots from '@/components/flashcard/ProgressDots';
import Confetti from '@/components/Confetti';
import Sparky from '@/components/Sparky';
import QuizBlitzSession from '@/components/flashcard/QuizBlitzSession';
import SpeedRoundSession from '@/components/flashcard/SpeedRoundSession';
import TapMatchSession from '@/components/flashcard/TapMatchSession';
import WarmUpSession from '@/components/flashcard/WarmUpSession';
import { useSounds } from '@/hooks/useSounds';
import type { FlashCard } from '@/types';

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

type SessionPhase = 'loading' | 'reviewing' | 'complete';

const BOX_NAMES = ['New', 'Rookie', 'Rising', 'Strong', 'Expert', 'Master'];
const BOX_COLORS = ['#64748B', '#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6', '#34D399'];

// ── Power-Up Toast ──────────────────────────────────────────────────────────

function PowerUpToast({
  show,
  newBox,
  isMastery,
}: {
  show: boolean;
  newBox: number;
  isMastery: boolean;
}) {
  if (!show) return null;
  return (
    <div className="fixed top-20 left-1/2 -translate-x-1/2 z-[60] animate-slide-down">
      <div
        className="flex items-center gap-2 px-4 py-2.5 rounded-2xl shadow-lg border"
        style={{
          background: isMastery
            ? 'linear-gradient(135deg, #059669, #34D399)'
            : 'linear-gradient(135deg, #1E293B, #334155)',
          borderColor: isMastery ? '#34D399' : BOX_COLORS[newBox] + '40',
        }}
      >
        <span className="text-xl animate-sparky-bounce">
          {isMastery ? '🏅' : '⚡'}
        </span>
        <div>
          <p className="text-white font-black text-sm">
            {isMastery ? 'MASTERED!' : 'Power Up!'}
          </p>
          <p className="text-white/70 text-[10px] font-bold">
            {isMastery ? 'Card reached Master level!' : `→ ${BOX_NAMES[newBox]}`}
          </p>
        </div>
      </div>
    </div>
  );
}

// ── Session Complete Overlay ────────────────────────────────────────────────

function SessionComplete({
  cardsReviewed,
  cardsCorrect,
  duration,
  transitions,
  onDone,
  onRestart,
}: {
  cardsReviewed: number;
  cardsCorrect: number;
  duration: number;
  transitions: BoxTransition[];
  onDone: () => void;
  onRestart: () => void;
}) {
  const pct = cardsReviewed > 0 ? Math.round((cardsCorrect / cardsReviewed) * 100) : 0;
  const mins = Math.floor(duration / 60);
  const secs = duration % 60;

  const promoted = transitions.filter((t) => t.leveledUp);
  const mastered = transitions.filter((t) => t.reachedMastery);
  const reset = transitions.filter((t) => t.newBox < t.oldBox && t.oldBox > 0);
  const hasMilestone = mastered.length > 0;

  return (
    <div className="fixed inset-0 z-50 bg-[#0F172A] flex flex-col items-center justify-center px-6 animate-fade-in overflow-y-auto">
      {hasMilestone && <Confetti />}

      {/* Sparky */}
      <div className="mb-3">
        <div className={hasMilestone ? 'animate-sparky-dance' : 'animate-sparky-bounce'}>
          <Sparky mood={pct >= 70 ? 'celebrating' : pct >= 40 ? 'happy' : 'encouraging'} size={80} />
        </div>
      </div>

      <h1 className="text-2xl font-black text-[#F1F5F9] mb-1">
        {hasMilestone
          ? 'Cards Mastered!'
          : pct >= 80
          ? 'Amazing Review!'
          : pct >= 50
          ? 'Great Practice!'
          : 'Keep Going!'}
      </h1>
      <p className="text-sm text-[#94A3B8] mb-6">
        {hasMilestone
          ? `${mastered.length} card${mastered.length > 1 ? 's' : ''} reached Master level!`
          : pct >= 80
          ? "You're really mastering these concepts!"
          : pct >= 50
          ? 'Nice progress — keep reviewing!'
          : "Practice makes perfect — you'll get there!"}
      </p>

      {/* Stats grid */}
      <div className="grid grid-cols-3 gap-3 w-full max-w-xs mb-5">
        <div className="bg-[#1E293B] rounded-2xl p-3 text-center">
          <p className="text-2xl font-black text-[#F1F5F9] tabular-nums">{cardsReviewed}</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider mt-0.5">Cards</p>
        </div>
        <div className="bg-[#1E293B] rounded-2xl p-3 text-center">
          <p className="text-2xl font-black text-[#34D399] tabular-nums">{pct}%</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider mt-0.5">Got It</p>
        </div>
        <div className="bg-[#1E293B] rounded-2xl p-3 text-center">
          <p className="text-2xl font-black text-[#60A5FA] tabular-nums">
            {mins > 0 ? `${mins}m` : `${secs}s`}
          </p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider mt-0.5">Time</p>
        </div>
      </div>

      {/* Box transitions report */}
      {(promoted.length > 0 || reset.length > 0) && (
        <div className="w-full max-w-xs mb-5 space-y-2">
          {promoted.length > 0 && (
            <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl px-3 py-2.5">
              <p className="text-xs font-bold text-emerald-400 mb-1.5">
                ⬆️ {promoted.length} card{promoted.length > 1 ? 's' : ''} leveled up
              </p>
              {promoted.slice(0, 5).map((t) => (
                <div key={t.cardId} className="flex items-center gap-2 py-0.5">
                  <span className="text-[10px] text-[#94A3B8] truncate flex-1">{t.cardFront}</span>
                  <div className="flex items-center gap-1 flex-shrink-0">
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
                </div>
              ))}
              {promoted.length > 5 && (
                <p className="text-[10px] text-emerald-400/60 mt-1">
                  +{promoted.length - 5} more
                </p>
              )}
            </div>
          )}

          {reset.length > 0 && (
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-xl px-3 py-2.5">
              <p className="text-xs font-bold text-blue-400 mb-1">
                🔄 {reset.length} card{reset.length > 1 ? 's' : ''} need more practice
              </p>
              <p className="text-[10px] text-blue-400/60">
                These reset to Rookie — you&apos;ll see them again soon!
              </p>
            </div>
          )}
        </div>
      )}

      {/* Action buttons */}
      <div className="w-full max-w-xs space-y-3 pb-8">
        <button
          onClick={onRestart}
          className="w-full py-3.5 rounded-2xl font-bold text-white text-sm"
          style={{ background: 'linear-gradient(135deg, #34D399, #059669)' }}
        >
          Review Again
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

// ── Main Session Page ────────────────────────────────────────────────────────

export default function FlashcardSessionPage() {
  const searchParams = useSearchParams();
  const deckId = searchParams.get('deck') ?? 'quick';
  const mode = searchParams.get('mode') ?? 'classic';

  // ── Quiz Blitz Mode ────────────────────────────────────────────────────────
  if (mode === 'quiz') {
    return <QuizBlitzSession deckId={deckId} />;
  }

  // ── Speed Round Mode ──────────────────────────────────────────────────────
  if (mode === 'speed') {
    return <SpeedRoundSession deckId={deckId} />;
  }

  // ── Tap Match Mode ────────────────────────────────────────────────────────
  if (mode === 'match') {
    return <TapMatchSession deckId={deckId} />;
  }

  // ── Pre-Exam Warm-Up Mode ─────────────────────────────────────────────────
  if (mode === 'warmup') {
    return <WarmUpSession deckId={deckId} />;
  }

  // ── Classic Flip Mode (below) ──────────────────────────────────────────────
  return <ClassicFlipSession deckId={deckId} />;
}

// ── Classic Flip Session Component ───────────────────────────────────────────

function ClassicFlipSession({ deckId }: { deckId: string }) {
  const router = useRouter();
  const { playCorrect, playWrong, playLevelUp, playMastery } = useSounds();

  const [phase, setPhase] = useState<SessionPhase>('loading');
  const [cards, setCards] = useState<CardWithProgress[]>([]);
  const [deckName, setDeckName] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [startTime] = useState(() => Date.now());
  const sessionSavedRef = useRef(false);

  // Celebration state
  const [transitions, setTransitions] = useState<BoxTransition[]>([]);
  const [showToast, setShowToast] = useState(false);
  const [toastBox, setToastBox] = useState(0);
  const [toastIsMastery, setToastIsMastery] = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);
  const [sessionStreak, setSessionStreak] = useState(0);

  // ── Load deck ──────────────────────────────────────────────────────────────

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
          setCards(data.cards);
          setDeckName(data.deckName ?? 'Flashcards');
          setPhase('reviewing');
        } else {
          setDeckName(data.deckName ?? 'Empty');
          setPhase('complete');
        }
      })
      .catch(() => {
        router.replace('/flashcards');
      });
  }, [router, deckId]);

  // ── Save session on complete ───────────────────────────────────────────────

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
        mode: 'classic',
        cardsReviewed: completed,
        cardsCorrect: correctCount,
        duration,
      }),
    }).catch(() => {});
  }, [startTime, completed, correctCount]);

  // ── Card response handlers ────────────────────────────────────────────────

  const handleResponse = useCallback(
    (correct: boolean) => {
      const card = cards[currentIndex];
      if (!card) return;

      const sid = localStorage.getItem('mathspark_student_id');

      // Update progress and handle celebration based on response
      if (sid) {
        fetch('/api/flashcards/progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            studentId: sid,
            cardId: card.id,
            correct,
          }),
        })
          .then((r) => r.json())
          .then((data) => {
            if (!data.ok) return;

            // Track transition
            const transition: BoxTransition = {
              cardId: card.id,
              cardFront: card.front.length > 40 ? card.front.slice(0, 40) + '...' : card.front,
              oldBox: data.oldBox,
              newBox: data.newBox,
              leveledUp: data.leveledUp,
              reachedMastery: data.reachedMastery,
            };
            setTransitions((prev) => [...prev, transition]);

            // Celebrations
            if (data.reachedMastery) {
              // Mastery! Big celebration
              playMastery();
              setShowConfetti(true);
              setToastBox(data.newBox);
              setToastIsMastery(true);
              setShowToast(true);
              setTimeout(() => setShowToast(false), 2200);
              setTimeout(() => setShowConfetti(false), 2000);
            } else if (data.leveledUp) {
              // Level up
              playLevelUp();
              setToastBox(data.newBox);
              setToastIsMastery(false);
              setShowToast(true);
              setTimeout(() => setShowToast(false), 1600);
            } else if (correct) {
              playCorrect();
            } else {
              playWrong();
            }
          })
          .catch(() => {});
      }

      // Update session streak
      if (correct) {
        setSessionStreak((prev) => prev + 1);
      } else {
        setSessionStreak(0);
      }

      const newCompleted = completed + 1;
      const newCorrect = correct ? correctCount + 1 : correctCount;
      setCompleted(newCompleted);
      setCorrectCount(newCorrect);

      if (currentIndex + 1 >= cards.length) {
        // Small delay to let final celebration play
        setTimeout(() => setPhase('complete'), correct ? 600 : 300);
      } else {
        setCurrentIndex((prev) => prev + 1);
      }
    },
    [cards, currentIndex, completed, correctCount, playCorrect, playWrong, playLevelUp, playMastery],
  );

  const handleNailedIt = useCallback(() => handleResponse(true), [handleResponse]);
  const handleStillLearning = useCallback(() => handleResponse(false), [handleResponse]);

  // Save session when phase becomes complete
  useEffect(() => {
    if (phase === 'complete' && completed > 0) {
      saveSession();
    }
  }, [phase, completed, saveSession]);

  // ── Keyboard shortcuts (desktop) ──────────────────────────────────────────

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (phase !== 'reviewing') return;
      if (e.key === 'ArrowRight' || e.key === 'd') handleNailedIt();
      else if (e.key === 'ArrowLeft' || e.key === 'a') handleStillLearning();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [phase, handleNailedIt, handleStillLearning]);

  // ── Render ────────────────────────────────────────────────────────────────

  // Loading
  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center">
        <div className="text-5xl animate-sparky-bounce mb-4">🃏</div>
        <p className="text-[#94A3B8] text-sm">Shuffling cards...</p>
      </div>
    );
  }

  // Complete
  if (phase === 'complete') {
    const duration = Math.round((Date.now() - startTime) / 1000);
    return (
      <SessionComplete
        cardsReviewed={completed}
        cardsCorrect={correctCount}
        duration={duration}
        transitions={transitions}
        onDone={() => router.push('/flashcards')}
        onRestart={() => {
          sessionSavedRef.current = false;
          setCurrentIndex(0);
          setCompleted(0);
          setCorrectCount(0);
          setTransitions([]);
          setSessionStreak(0);
          setPhase('loading');

          const sid = localStorage.getItem('mathspark_student_id');
          const grade = localStorage.getItem('mathspark_student_grade') || '4';
          if (!sid) return;

          fetch(`/api/flashcards/deck?studentId=${sid}&grade=${grade}&deck=${encodeURIComponent(deckId)}`)
            .then((r) => r.json())
            .then((data) => {
              if (data.cards?.length > 0) {
                setCards(data.cards);
                setPhase('reviewing');
              } else {
                setPhase('complete');
              }
            })
            .catch(() => router.replace('/flashcards'));
        }}
      />
    );
  }

  // Reviewing
  const currentCard = cards[currentIndex];
  const remaining = cards.length - currentIndex - 1;

  return (
    <div className="min-h-screen bg-[#0F172A] flex flex-col">
      {/* ── Celebration overlays ───────────────────────────────────────────── */}
      {showConfetti && <Confetti />}
      <PowerUpToast show={showToast} newBox={toastBox} isMastery={toastIsMastery} />

      {/* ── Top bar ──────────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-30 bg-[#0F172A]/95 backdrop-blur-md border-b border-white/5 px-4 py-3">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <button
            onClick={() => {
              if (completed > 0) saveSession();
              router.push('/flashcards');
            }}
            className="text-[#94A3B8] text-sm font-bold"
          >
            ✕
          </button>
          <h2 className="text-[#F1F5F9] font-bold text-sm truncate max-w-[200px]">
            {deckName}
          </h2>
          <div className="flex items-center gap-2">
            {sessionStreak >= 3 && (
              <span className="text-xs font-bold text-amber-400 animate-pulse">
                🔥{sessionStreak}
              </span>
            )}
            <span className="text-xs text-[#64748B] tabular-nums">
              {currentIndex + 1}/{cards.length}
            </span>
          </div>
        </div>

        {/* Progress */}
        <div className="max-w-md mx-auto mt-1">
          <ProgressDots total={cards.length} current={currentIndex} completed={completed} />
        </div>
      </div>

      {/* ── Card area ─────────────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col items-center justify-center px-4 py-6 max-w-md mx-auto w-full">
        {/* Power Level indicator */}
        {currentCard && (
          <div className="mb-3 flex items-center gap-2">
            <span className="text-xs font-bold" style={{ color: BOX_COLORS[currentCard.leitnerBox || 0] }}>
              {BOX_NAMES[currentCard.leitnerBox || 0]}
            </span>
            <div className="flex gap-0.5">
              {[1, 2, 3, 4, 5].map((lvl) => (
                <div
                  key={lvl}
                  className="w-5 h-1.5 rounded-full transition-all duration-300"
                  style={{
                    background: lvl <= (currentCard.leitnerBox || 0)
                      ? BOX_COLORS[currentCard.leitnerBox || 0]
                      : 'rgba(255,255,255,0.1)',
                  }}
                />
              ))}
            </div>
            {currentCard.timesSeen > 0 && (
              <span className="text-[10px] text-[#64748B] ml-1">
                Seen {currentCard.timesSeen}x
              </span>
            )}
          </div>
        )}

        {/* Flash card */}
        {currentCard && (
          <div key={currentCard.id} className="w-full animate-flashcard-slide-up">
            <FlashCardComponent
              card={currentCard}
              onSwipeRight={handleNailedIt}
              onSwipeLeft={handleStillLearning}
              deckSize={Math.min(remaining, 2)}
              showConfidenceSlot
            />
          </div>
        )}

        {/* ── Confidence buttons (below card) ───────────────────────────────── */}
        <div className="mt-6 flex items-center gap-3 w-full max-w-[400px]">
          <button
            onClick={handleStillLearning}
            className="flex-1 py-3.5 rounded-2xl font-bold text-sm text-blue-400 bg-blue-500/10 border border-blue-500/20 active:scale-[0.97] transition-all"
          >
            Still learning 📚
          </button>
          <button
            onClick={handleNailedIt}
            className="flex-1 py-3.5 rounded-2xl font-bold text-sm text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 active:scale-[0.97] transition-all"
          >
            Nailed it! 🎯
          </button>
        </div>

        {/* Keyboard hint (desktop only) */}
        <p className="mt-3 text-[10px] text-[#475569] hidden sm:block">
          ← A = Still learning &nbsp;·&nbsp; D → = Nailed it &nbsp;·&nbsp; Tap card to flip
        </p>
      </div>
    </div>
  );
}
