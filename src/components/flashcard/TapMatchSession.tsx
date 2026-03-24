'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useFlashcardDeck } from '@/hooks/useFlashcardDeck';
import dynamic from 'next/dynamic';
import Confetti from '@/components/Confetti';
import Sparky from '@/components/Sparky';
import { useSounds } from '@/hooks/useSounds';
import type { FlashCard } from '@/types';

const KatexRenderer = dynamic(() => import('@/components/KatexRenderer'), { ssr: false });

// ── Types ────────────────────────────────────────────────────────────────────

interface CardWithProgress extends FlashCard {
  leitnerBox: number;
  timesSeen: number;
  timesCorrect: number;
  streakOnCard: number;
}

interface MatchTile {
  id: string;        // unique tile ID
  pairId: string;    // shared between front + back of same card
  text: string;      // display text
  formula?: string;  // optional KaTeX
  type: 'front' | 'back';
}

type Phase = 'loading' | 'memorize' | 'playing' | 'complete';

const PAIR_COUNTS = [6, 8, 10]; // progressive difficulty
const MEMORIZE_MS = 3000;       // brief peek time

// ── Shuffle ──────────────────────────────────────────────────────────────────

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ── Match Complete Screen ────────────────────────────────────────────────────

function MatchComplete({
  pairs,
  moves,
  timeSeconds,
  level,
  onNextLevel,
  onPlayAgain,
  onDone,
}: {
  pairs: number;
  moves: number;
  timeSeconds: number;
  level: number;
  onNextLevel: (() => void) | null;
  onPlayAgain: () => void;
  onDone: () => void;
}) {
  const efficiency = pairs > 0 ? Math.round((pairs / moves) * 100) : 0;
  const stars = efficiency >= 90 ? 3 : efficiency >= 60 ? 2 : 1;
  const mins = Math.floor(timeSeconds / 60);
  const secs = timeSeconds % 60;

  return (
    <div className="fixed inset-0 z-50 bg-[#0F172A] flex flex-col items-center justify-center px-6 animate-fade-in">
      {stars >= 3 && <Confetti />}

      <div className={stars >= 3 ? 'animate-sparky-dance' : 'animate-sparky-bounce'}>
        <Sparky mood={stars >= 3 ? 'celebrating' : stars >= 2 ? 'happy' : 'encouraging'} size={80} />
      </div>

      <h1 className="text-2xl font-black text-[#F1F5F9] mt-3 mb-1">
        {stars >= 3 ? 'Perfect Memory!' : stars >= 2 ? 'Great Matching!' : 'Keep Practicing!'}
      </h1>

      {/* Stars */}
      <div className="flex gap-2 mb-4">
        {[1, 2, 3].map((s) => (
          <span key={s} className={`text-3xl ${s <= stars ? '' : 'opacity-20'}`}>
            ⭐
          </span>
        ))}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-2 w-full max-w-xs mb-6">
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#F1F5F9] tabular-nums">{pairs}</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Pairs</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#FBBF24] tabular-nums">{moves}</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Moves</p>
        </div>
        <div className="bg-[#1E293B] rounded-xl p-2.5 text-center">
          <p className="text-lg font-black text-[#60A5FA] tabular-nums">
            {mins > 0 ? `${mins}m${secs}s` : `${secs}s`}
          </p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Time</p>
        </div>
      </div>

      {/* Buttons */}
      <div className="w-full max-w-xs space-y-3">
        {onNextLevel && (
          <button
            onClick={onNextLevel}
            className="w-full py-3.5 rounded-2xl font-bold text-white text-sm"
            style={{ background: 'linear-gradient(135deg, #8B5CF6, #7C3AED)' }}
          >
            Next Level ({PAIR_COUNTS[level + 1]} pairs) 🚀
          </button>
        )}
        <button
          onClick={onPlayAgain}
          className="w-full py-3.5 rounded-2xl font-bold text-white text-sm bg-[#1E293B] border border-white/10"
        >
          Play Again
        </button>
        <button
          onClick={onDone}
          className="w-full py-3.5 rounded-2xl font-bold text-[#94A3B8] text-sm bg-transparent"
        >
          Done
        </button>
      </div>
    </div>
  );
}

// ── Main Tap Match Component ─────────────────────────────────────────────────

interface TapMatchSessionProps {
  deckId: string;
}

export default function TapMatchSession({ deckId }: TapMatchSessionProps) {
  const router = useRouter();
  const { fetchDeck } = useFlashcardDeck(deckId, { limit: 40 });
  const { playCorrect, playWrong, playStreak, playMastery } = useSounds();

  const [phase, setPhase] = useState<Phase>('loading');
  const [level, setLevel] = useState(0); // index into PAIR_COUNTS
  const [tiles, setTiles] = useState<MatchTile[]>([]);
  const [flippedIds, setFlippedIds] = useState<string[]>([]);
  const [matchedPairIds, setMatchedPairIds] = useState<Set<string>>(new Set());
  const [moves, setMoves] = useState(0);
  const [startTime, setStartTime] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [totalPairs, setTotalPairs] = useState(0);
  const [isLocked, setIsLocked] = useState(false); // prevent taps during mismatch animation
  const [consecutiveMatches, setConsecutiveMatches] = useState(0);

  const sessionSavedRef = useRef(false);
  const elapsedRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const allCardsRef = useRef<CardWithProgress[]>([]);

  // ── Load deck ──────────────────────────────────────────────────────────────

  const loadDeck = useCallback(() => {
    fetchDeck()
      .then((data) => {
        if (!data || data.cards.length === 0) {
          setPhase('complete');
        } else {
          allCardsRef.current = data.cards as CardWithProgress[];
          setupLevel(0, data.cards as CardWithProgress[]);
        }
      })
      .catch(() => router.replace('/flashcards'));
  }, [fetchDeck, router, setupLevel]);

  useEffect(() => { loadDeck(); }, [loadDeck]);

  // ── Setup a level ──────────────────────────────────────────────────────────

  const setupLevel = useCallback((lvl: number, cards: CardWithProgress[]) => {
    const pairCount = PAIR_COUNTS[lvl] ?? 6;
    const selected = shuffle(cards).slice(0, pairCount);
    setTotalPairs(selected.length);

    // Create tile pairs: one "front" tile and one "back" tile per card
    const tilePairs: MatchTile[] = [];
    for (const card of selected) {
      tilePairs.push({
        id: `${card.id}_front`,
        pairId: card.id,
        text: card.front,
        formula: card.formula,
        type: 'front',
      });
      tilePairs.push({
        id: `${card.id}_back`,
        pairId: card.id,
        text: card.back,
        type: 'back',
      });
    }

    setTiles(shuffle(tilePairs));
    setFlippedIds([]);
    setMatchedPairIds(new Set());
    setMoves(0);
    setConsecutiveMatches(0);
    setIsLocked(false);
    setLevel(lvl);
    setPhase('memorize');
  }, []);

  // ── Memorize phase (brief peek) ───────────────────────────────────────────

  useEffect(() => {
    if (phase !== 'memorize') return;

    const t = setTimeout(() => {
      setPhase('playing');
      setStartTime(Date.now());
      setElapsed(0);
    }, MEMORIZE_MS);

    return () => clearTimeout(t);
  }, [phase]);

  // ── Elapsed timer ──────────────────────────────────────────────────────────

  useEffect(() => {
    if (phase !== 'playing') {
      if (elapsedRef.current) clearInterval(elapsedRef.current);
      return;
    }

    elapsedRef.current = setInterval(() => {
      setElapsed(Math.floor((Date.now() - startTime) / 1000));
    }, 1000);

    return () => {
      if (elapsedRef.current) clearInterval(elapsedRef.current);
    };
  }, [phase, startTime]);

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
        mode: 'match',
        cardsReviewed: totalPairs * 2,
        cardsCorrect: totalPairs,
        duration: elapsed,
      }),
    }).catch((err) => console.error('[fetch]', err));
  }, [phase, totalPairs, elapsed, playMastery]);

  // ── Handle tile tap ────────────────────────────────────────────────────────

  const handleTap = useCallback(
    (tileId: string) => {
      if (phase !== 'playing' || isLocked) return;

      const tile = tiles.find((t) => t.id === tileId);
      if (!tile) return;

      // Already matched or already flipped
      if (matchedPairIds.has(tile.pairId) || flippedIds.includes(tileId)) return;

      const newFlipped = [...flippedIds, tileId];

      if (newFlipped.length === 1) {
        // First card of pair
        setFlippedIds(newFlipped);
        return;
      }

      if (newFlipped.length === 2) {
        setFlippedIds(newFlipped);
        setMoves((m) => m + 1);

        const [firstId, secondId] = newFlipped;
        const first = tiles.find((t) => t.id === firstId)!;
        const second = tiles.find((t) => t.id === secondId)!;

        if (first.pairId === second.pairId && first.type !== second.type) {
          // Match!
          const newMatched = new Set(matchedPairIds);
          newMatched.add(first.pairId);
          setMatchedPairIds(newMatched);
          setFlippedIds([]);
          const newConsec = consecutiveMatches + 1;
          setConsecutiveMatches(newConsec);

          // Update Leitner (fire-and-forget)
          const sid = localStorage.getItem('mathspark_student_id');
          if (sid) {
            fetch('/api/flashcards/progress', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ cardId: first.pairId, correct: true }),
            }).catch((err) => console.error('[fetch]', err));
          }

          if (newConsec >= 3) {
            playStreak();
          } else {
            playCorrect();
          }

          // Check win
          if (newMatched.size === totalPairs) {
            setTimeout(() => setPhase('complete'), 500);
          }
        } else {
          // Mismatch — flip back after delay
          setConsecutiveMatches(0);
          setIsLocked(true);
          playWrong();

          setTimeout(() => {
            setFlippedIds([]);
            setIsLocked(false);
          }, 800);
        }
      }
    },
    [phase, isLocked, tiles, flippedIds, matchedPairIds, totalPairs, consecutiveMatches, playCorrect, playWrong, playStreak],
  );

  // ── Compute grid columns ───────────────────────────────────────────────────

  const tileCount = tiles.length;
  const gridCols = tileCount <= 12 ? 3 : 4;

  // ── Render: Loading ────────────────────────────────────────────────────────

  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center">
        <div className="text-5xl animate-sparky-bounce mb-4">🧩</div>
        <p className="text-[#94A3B8] text-sm">Preparing match game...</p>
      </div>
    );
  }

  // ── Render: Complete ───────────────────────────────────────────────────────

  if (phase === 'complete') {
    const canNextLevel = level + 1 < PAIR_COUNTS.length && allCardsRef.current.length >= (PAIR_COUNTS[level + 1] ?? 999);

    return (
      <MatchComplete
        pairs={totalPairs}
        moves={moves}
        timeSeconds={elapsed}
        level={level}
        onNextLevel={canNextLevel ? () => {
          sessionSavedRef.current = false;
          setupLevel(level + 1, allCardsRef.current);
        } : null}
        onPlayAgain={() => {
          sessionSavedRef.current = false;
          setupLevel(level, allCardsRef.current);
        }}
        onDone={() => router.push('/flashcards')}
      />
    );
  }

  // ── Render: Memorize + Playing ─────────────────────────────────────────────

  const isMemorize = phase === 'memorize';
  const mins = Math.floor(elapsed / 60);
  const secs = elapsed % 60;

  return (
    <div className="min-h-screen bg-[#0F172A] flex flex-col">
      {/* ── Top bar ──────────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-30 bg-[#0F172A]/95 backdrop-blur-md border-b border-white/5 px-4 py-2.5">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <button
            onClick={() => router.push('/flashcards')}
            className="text-[#94A3B8] text-sm font-bold"
          >
            ✕
          </button>

          <div className="flex items-center gap-3">
            {isMemorize && (
              <span className="text-xs font-bold text-amber-400 animate-pulse">
                👀 Memorize!
              </span>
            )}
            {!isMemorize && (
              <>
                <span className="text-xs font-bold text-[#F1F5F9] tabular-nums">
                  {matchedPairIds.size}/{totalPairs} pairs
                </span>
                <span className="text-xs text-[#64748B] tabular-nums">
                  {moves} moves
                </span>
              </>
            )}
          </div>

          <span className="text-xs font-bold text-[#60A5FA] tabular-nums">
            {mins > 0 ? `${mins}:${secs.toString().padStart(2, '0')}` : `${secs}s`}
          </span>
        </div>

        {/* Progress bar */}
        {!isMemorize && totalPairs > 0 && (
          <div className="max-w-md mx-auto mt-1.5 h-1 bg-white/5 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#34D399] rounded-full transition-[width] duration-300"
              style={{ width: `${(matchedPairIds.size / totalPairs) * 100}%` }}
            />
          </div>
        )}
      </div>

      {/* Level label */}
      <div className="text-center pt-3 pb-2">
        <span className="text-[10px] font-bold uppercase tracking-widest text-[#64748B]">
          Level {level + 1} · {totalPairs} pairs
        </span>
      </div>

      {/* ── Tile grid ────────────────────────────────────────────────────────── */}
      <div className="flex-1 flex items-start justify-center px-3 pb-6">
        <div
          className="grid gap-2 w-full max-w-md"
          style={{
            gridTemplateColumns: `repeat(${gridCols}, 1fr)`,
          }}
        >
          {tiles.map((tile) => {
            const isMatched = matchedPairIds.has(tile.pairId);
            const isFlipped = isMemorize || flippedIds.includes(tile.id) || isMatched;

            return (
              <button
                key={tile.id}
                onClick={() => handleTap(tile.id)}
                disabled={isMemorize || isMatched}
                className={`
                  relative rounded-xl transition-[transform,background-color,border-color,opacity] duration-300 aspect-[3/4]
                  flex items-center justify-center p-2 text-center overflow-hidden min-h-0
                  ${isMatched
                    ? 'bg-duo-green/20 border-2 border-duo-green/40 scale-95'
                    : isFlipped
                    ? 'bg-[#1E293B] border-2 border-[#A78BFA]/40'
                    : 'bg-[#1E293B] border-2 border-white/10 active:scale-95 hover:border-white/20'
                  }
                `}
              >
                {isFlipped ? (
                  <div className="animate-fade-in">
                    {/* Type badge */}
                    <span className={`absolute top-1 right-1.5 text-[8px] font-bold uppercase tracking-wider rounded px-1 ${
                      tile.type === 'front' ? 'text-[#A78BFA] bg-[#A78BFA]/10' : 'text-[#34D399] bg-[#34D399]/10'
                    }`}>
                      {tile.type === 'front' ? 'Q' : 'A'}
                    </span>

                    {tile.formula ? (
                      <KatexRenderer latex={tile.formula} displayMode={false} className="text-[#F1F5F9] text-xs" />
                    ) : (
                      <p className={`text-xs font-bold leading-tight ${
                        isMatched ? 'text-emerald-300' : 'text-[#F1F5F9]'
                      }`}>
                        {tile.text.length > 60 ? tile.text.slice(0, 57) + '...' : tile.text}
                      </p>
                    )}
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-1">
                    <span className="text-2xl">🃏</span>
                    <span className="text-[10px] text-[#475569] font-bold">TAP</span>
                  </div>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
