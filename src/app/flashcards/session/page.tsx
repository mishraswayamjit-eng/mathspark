'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import FlashCardComponent from '@/components/flashcard/FlashCard';
import ProgressDots from '@/components/flashcard/ProgressDots';
import type { FlashCard } from '@/types';

// ── Card with progress attached by the deck API ────────────────────────────
interface CardWithProgress extends FlashCard {
  leitnerBox: number;
  timesSeen: number;
  timesCorrect: number;
  streakOnCard: number;
}

type SessionPhase = 'loading' | 'reviewing' | 'complete';

// ── Session Complete Overlay ─────────────────────────────────────────────────

function SessionComplete({
  cardsReviewed,
  cardsCorrect,
  duration,
  onDone,
  onRestart,
}: {
  cardsReviewed: number;
  cardsCorrect: number;
  duration: number;
  onDone: () => void;
  onRestart: () => void;
}) {
  const pct = cardsReviewed > 0 ? Math.round((cardsCorrect / cardsReviewed) * 100) : 0;
  const mins = Math.floor(duration / 60);
  const secs = duration % 60;

  return (
    <div className="fixed inset-0 z-50 bg-[#0F172A] flex flex-col items-center justify-center px-6 animate-fade-in">
      {/* Sparky celebration */}
      <div className="text-7xl mb-4 animate-sparky-bounce">
        {pct >= 80 ? '🌟' : pct >= 50 ? '💪' : '📚'}
      </div>

      <h1 className="text-2xl font-black text-[#F1F5F9] mb-1">
        {pct >= 80 ? 'Amazing Review!' : pct >= 50 ? 'Great Practice!' : 'Keep Going!'}
      </h1>
      <p className="text-sm text-[#94A3B8] mb-8">
        {pct >= 80
          ? "You're really mastering these concepts!"
          : pct >= 50
          ? 'Nice progress — keep reviewing!'
          : "Practice makes perfect — you'll get there!"}
      </p>

      {/* Stats grid */}
      <div className="grid grid-cols-3 gap-4 w-full max-w-xs mb-10">
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

      {/* Action buttons */}
      <div className="w-full max-w-xs space-y-3">
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
  const router = useRouter();
  const searchParams = useSearchParams();
  const deckId = searchParams.get('deck') ?? 'quick';

  const [phase, setPhase] = useState<SessionPhase>('loading');
  const [cards, setCards] = useState<CardWithProgress[]>([]);
  const [deckName, setDeckName] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [completed, setCompleted] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [startTime] = useState(() => Date.now());
  const sessionSavedRef = useRef(false);

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
          // No cards available
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
      if (sid) {
        // Fire-and-forget progress update
        fetch('/api/flashcards/progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            studentId: sid,
            cardId: card.id,
            correct,
          }),
        }).catch(() => {});
      }

      const newCompleted = completed + 1;
      const newCorrect = correct ? correctCount + 1 : correctCount;
      setCompleted(newCompleted);
      setCorrectCount(newCorrect);

      if (currentIndex + 1 >= cards.length) {
        // Session complete
        setPhase('complete');
      } else {
        setCurrentIndex((prev) => prev + 1);
      }
    },
    [cards, currentIndex, completed, correctCount],
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
        onDone={() => router.push('/flashcards')}
        onRestart={() => {
          // Reset and reload same deck
          sessionSavedRef.current = false;
          setCurrentIndex(0);
          setCompleted(0);
          setCorrectCount(0);
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
          <span className="text-xs text-[#64748B] tabular-nums">
            {currentIndex + 1}/{cards.length}
          </span>
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
            <span className="text-xs text-[#64748B]">Power Level</span>
            <div className="flex gap-0.5">
              {[1, 2, 3, 4, 5].map((lvl) => (
                <div
                  key={lvl}
                  className={`w-5 h-1.5 rounded-full transition-all ${
                    lvl <= (currentCard.leitnerBox || 0)
                      ? 'bg-[#34D399]'
                      : 'bg-white/10'
                  }`}
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
