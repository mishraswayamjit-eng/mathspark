'use client';

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { logError } from '@/lib/logger';
import { useRouter } from 'next/navigation';
import { StreakProgress } from '@/components/flashcard/StreakMilestone';
import type { FlashcardDeck, FlashcardStats } from '@/types';

// ── Mastery ring SVG ─────────────────────────────────────────────────────────

function MasteryRing({ mastered, total, size = 36 }: { mastered: number; total: number; size?: number }) {
  const pct = total > 0 ? mastered / total : 0;
  const r = (size - 6) / 2;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - pct);
  const color = pct >= 0.7 ? '#12805c' : pct >= 0.3 ? '#f5a400' : '#5d6b8c';
  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#d3deee" strokeWidth={4} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={4}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        className="transition-[stroke-dashoffset] duration-700"
      />
      <text
        x={size / 2} y={size / 2}
        textAnchor="middle" dominantBaseline="central"
        fill="#1d2a4d" fontSize={size * 0.28} fontWeight="bold"
      >
        {Math.round(pct * 100)}%
      </text>
    </svg>
  );
}

// ── Power bar (mini stacked box distribution) ────────────────────────────────

const BOX_BAR_COLORS = ['#5d6b8c', '#5a4300', '#4f46e5', '#0e7490', '#3f37c9', '#12805c'];

function PowerBar({ distribution, total }: { distribution: number[]; total: number }) {
  if (total === 0) return null;
  return (
    <div className="ui-meter w-full flex h-3 mt-1.5">
      {distribution.map((count, i) => {
        if (count === 0) return null;
        return (
          <div
            key={i}
            className="h-full transition-[width] duration-500"
            style={{
              width: `${(count / total) * 100}%`,
              background: BOX_BAR_COLORS[i],
            }}
          />
        );
      })}
    </div>
  );
}

// ── Deck card ────────────────────────────────────────────────────────────────

const DeckCard = React.memo(function DeckCard({
  deck, onClick, onQuiz,
}: {
  deck: FlashcardDeck;
  onClick: () => void;
  onQuiz?: () => void;
}) {
  const isSpecial = ['due', 'quick', 'mental_math'].includes(deck.id);
  const emoji = deck.id === 'due' ? '🔥' : deck.id === 'quick' ? '⚡' : deck.id === 'mental_math' ? '🧠' : '📁';
  return (
    <div
      className="w-full flex flex-col bg-card border-2 border-line rounded-card px-4 py-3.5 transition-colors"
      style={{
        borderLeft: `10px solid ${deck.topicColor}`,
      }}
    >
      <button onClick={onClick} className="flex items-center gap-3 w-full active:scale-[0.98] transition-transform">
        <span className="w-11 h-11 rounded-tile bg-soft text-xl text-center leading-[44px] flex-shrink-0" aria-hidden="true">{emoji}</span>
        <div className="flex-1 text-left min-w-0">
          <p className="font-display text-title text-ink truncate">{deck.name}</p>
          <p className="text-[13px] font-bold text-ink-muted">
            {deck.cardCount} card{deck.cardCount !== 1 ? 's' : ''}
            {deck.dueCount > 0 && !isSpecial && (
              <span className="ml-1 text-hint-ink">· {deck.dueCount} due</span>
            )}
          </p>
        </div>
        {!isSpecial && (
          <MasteryRing mastered={deck.mastered} total={deck.total} />
        )}
        {isSpecial && deck.dueCount > 0 && (
          <span className="bg-star text-ink border-2 border-ink text-xs font-extrabold px-2 py-0.5 rounded-full tabular-nums">
            {deck.dueCount}
          </span>
        )}
      </button>
      {/* Power distribution bar + quiz button for topic decks */}
      {!isSpecial && (
        <div className="flex items-center gap-2 mt-1.5">
          <div className="flex-1">
            {deck.boxDistribution && (
              <PowerBar distribution={deck.boxDistribution} total={deck.total} />
            )}
          </div>
          {onQuiz && deck.cardCount >= 4 && (
            <button
              onClick={(e) => { e.stopPropagation(); onQuiz(); }}
              className="text-xs font-extrabold text-ink bg-card border-2 border-ink px-2.5 py-0.5 rounded-full hover:bg-soft transition-colors whitespace-nowrap min-h-0"
            >
              <span aria-hidden="true">⚡ </span>Quiz
            </button>
          )}
        </div>
      )}
    </div>
  );
});

// ── Page ─────────────────────────────────────────────────────────────────────

export default function FlashcardsPage() {
  const router = useRouter();
  const [decks, setDecks] = useState<FlashcardDeck[]>([]);
  const [stats, setStats] = useState<FlashcardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(false);

  useEffect(() => {
    const sid = localStorage.getItem('mathspark_student_id');
    const grade = localStorage.getItem('mathspark_student_grade') || '4';
    if (!sid) { router.replace('/start'); return; }

    fetch(`/api/flashcards?grade=${grade}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        setDecks(data.decks ?? []);
        setStats(data.stats ?? null);
        // Cache due count for BottomNav badge
        const dueDeck = (data.decks ?? []).find((d: FlashcardDeck) => d.id === 'due');
        if (dueDeck) {
          try { localStorage.setItem('mathspark_cards_due', String(dueDeck.dueCount)); } catch {}
        }
      })
      .catch((err) => { logError('[fetch]', err); setFetchError(true); })
      .finally(() => setLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const specialDecks = useMemo(
    () => decks.filter((d) => ['due', 'quick', 'mental_math'].includes(d.id)),
    [decks],
  );
  const topicDecks = useMemo(
    () => decks.filter((d) => !['due', 'quick', 'mental_math'].includes(d.id)),
    [decks],
  );

  const openDeck = useCallback((deckId: string, mode: string = 'classic') => {
    router.push(`/flashcards/session?deck=${deckId}&mode=${mode}`);
  }, [router]);

  return (
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-30 bg-ink px-4 py-3">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <button onClick={() => window.history.length > 1 ? router.back() : router.push('/home')} className="text-white text-sm font-bold">
            ← Back
          </button>
          <h1 className="text-white text-title"><span aria-hidden="true">🃏 </span>Sparky&apos;s Cards</h1>
          <div className="w-12" />
        </div>
      </div>

      <div className="max-w-md mx-auto px-4 pt-4 space-y-6">
        {/* ── Stats bar ───────────────────────────────────────────────────── */}
        {stats && !loading && (
          <div className="space-y-3">
            <div className="flex items-center justify-around bg-card border-2 border-ink rounded-card shadow-hard-lg px-4 py-3">
              <div className="text-center">
                <p className="text-lg font-bold text-ink tabular-nums">{stats.totalCards}</p>
                <p className="text-xs font-bold text-ink-muted">Total</p>
              </div>
              <div className="w-0.5 h-8 bg-line" />
              <div className="text-center">
                <p className="text-lg font-bold text-ink tabular-nums">{stats.totalSeen}</p>
                <p className="text-xs font-bold text-ink-muted">Seen</p>
              </div>
              <div className="w-0.5 h-8 bg-line" />
              <div className="text-center">
                <p className="text-lg font-bold text-success tabular-nums">{stats.totalMastered}</p>
                <p className="text-xs font-bold text-ink-muted">Mastered</p>
              </div>
              <div className="w-0.5 h-8 bg-line" />
              <div className="text-center">
                <p className="text-lg font-bold text-ink tabular-nums">
                  {stats.studyStreak > 0 ? `🔥${stats.studyStreak}` : '—'}
                </p>
                <p className="text-xs font-bold text-ink-muted">Streak</p>
              </div>
            </div>

            {/* Daily new card counter */}
            <div className="flex items-center justify-between bg-card border-2 border-line rounded-control px-3 py-2">
              <span className="text-[13px] font-bold text-ink-muted">
                New cards today
              </span>
              <div className="flex items-center gap-1.5">
                <div className="flex gap-0.5">
                  {Array.from({ length: stats.maxNewPerDay }).map((_, i) => (
                    <div
                      key={i}
                      className="w-3 h-1.5 rounded-full transition-[background-color]"
                      style={{
                        background: i < stats.newCardsToday ? '#4f46e5' : '#d3deee',
                      }}
                    />
                  ))}
                </div>
                <span className="text-xs font-bold text-ink-muted tabular-nums">
                  {stats.newCardsToday}/{stats.maxNewPerDay}
                </span>
              </div>
            </div>

            {/* Streak progress toward next milestone */}
            {stats.studyStreak > 0 && stats.milestoneProgress && (
              <StreakProgress
                streak={stats.studyStreak}
                nextMilestone={stats.milestoneProgress.nextMilestone}
                progress={stats.milestoneProgress.progress}
              />
            )}

            {/* Streak multiplier badge */}
            {stats.streakMultiplier > 1 && (
              <div className="flex items-center justify-center gap-1.5 bg-star border-2 border-ink rounded-control px-3 py-1.5">
                <span className="text-xs" aria-hidden="true">🔥</span>
                <span className="text-[13px] font-extrabold text-ink">
                  {stats.streakMultiplier}x XP Multiplier Active
                </span>
              </div>
            )}
          </div>
        )}

        {/* ── Loading skeleton ────────────────────────────────────────────── */}
        {loading && (
          <div className="space-y-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-16 bg-card border-2 border-line rounded-card animate-pulse" />
            ))}
          </div>
        )}

        {/* ── Special decks ───────────────────────────────────────────────── */}
        {!loading && specialDecks.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-title text-ink px-1">
              Quick Start
            </h2>
            {specialDecks.map((d) => (
              <DeckCard key={d.id} deck={d} onClick={() => openDeck(d.id)} />
            ))}
          </div>
        )}

        {/* ── Game Modes ───────────────────────────────────────────────────── */}
        {!loading && decks.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-title text-ink px-1">
              Game Modes
            </h2>

            {/* Quiz Blitz */}
            <button
              onClick={() => openDeck('quick', 'quiz')}
              className="w-full bg-card border-2 border-line rounded-card p-3.5 text-left transition-[transform] active:scale-[0.98]"
            >
              <div className="flex items-center gap-3">
                <span className="w-11 h-11 rounded-tile bg-soft text-2xl text-center leading-[44px] flex-shrink-0 animate-quiz-icon" aria-hidden="true">⚡</span>
                <div className="flex-1">
                  <p className="font-display text-title text-ink">Quiz Blitz</p>
                  <p className="text-[13px] font-bold text-ink-muted">MCQ · Combos · 12s per card</p>
                </div>
                <span className="ui-chip" style={{ minHeight: 'auto' }}>GO</span>
              </div>
            </button>

            {/* Speed Round */}
            <button
              onClick={() => openDeck('quick', 'speed')}
              className="w-full bg-card border-2 border-line rounded-card p-3.5 text-left transition-[transform] active:scale-[0.98]"
            >
              <div className="flex items-center gap-3">
                <span className="w-11 h-11 rounded-tile bg-soft text-2xl text-center leading-[44px] flex-shrink-0" aria-hidden="true">🔥</span>
                <div className="flex-1">
                  <p className="font-display text-title text-ink">Speed Round</p>
                  <p className="text-[13px] font-bold text-ink-muted">60 seconds · Answer as many as you can!</p>
                </div>
                <span className="ui-chip" style={{ minHeight: 'auto' }}>60s</span>
              </div>
            </button>

            {/* Tap Match */}
            <button
              onClick={() => openDeck('quick', 'match')}
              className="w-full bg-card border-2 border-line rounded-card p-3.5 text-left transition-[transform] active:scale-[0.98]"
            >
              <div className="flex items-center gap-3">
                <span className="w-11 h-11 rounded-tile bg-soft text-2xl text-center leading-[44px] flex-shrink-0" aria-hidden="true">🧩</span>
                <div className="flex-1">
                  <p className="font-display text-title text-ink">Tap Match</p>
                  <p className="text-[13px] font-bold text-ink-muted">Match fronts to backs · Memory game</p>
                </div>
                <span className="ui-chip" style={{ minHeight: 'auto' }}>NEW</span>
              </div>
            </button>

            {/* Pre-Exam Warm-Up */}
            <button
              onClick={() => openDeck('warmup', 'warmup')}
              className="w-full bg-card border-2 border-line rounded-card p-3.5 text-left transition-[transform] active:scale-[0.98]"
            >
              <div className="flex items-center gap-3">
                <span className="w-11 h-11 rounded-tile bg-soft text-2xl text-center leading-[44px] flex-shrink-0" aria-hidden="true">🧘</span>
                <div className="flex-1">
                  <p className="font-display text-title text-ink">Pre-Exam Warm-Up</p>
                  <p className="text-[13px] font-bold text-ink-muted">Breathe · Formulas · Confidence boost</p>
                </div>
                <span className="ui-chip" style={{ minHeight: 'auto' }}>ZEN</span>
              </div>
            </button>

            {/* Voice Recall */}
            <div
              className="w-full bg-card border-2 border-line rounded-card p-3.5 text-left opacity-60 cursor-not-allowed"
            >
              <div className="flex items-center gap-3">
                <span className="w-11 h-11 rounded-tile bg-soft text-2xl text-center leading-[44px] flex-shrink-0" aria-hidden="true">🎙️</span>
                <div className="flex-1">
                  <p className="font-display text-title text-ink">Voice Recall</p>
                  <p className="text-[13px] font-bold text-ink-muted">Say it out loud · Active recall</p>
                </div>
                <span className="ui-chip" style={{ minHeight: 'auto' }}>COMING SOON</span>
              </div>
            </div>
          </div>
        )}

        {/* ── Topic decks ─────────────────────────────────────────────────── */}
        {!loading && topicDecks.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-title text-ink px-1">
              By Topic
            </h2>
            {topicDecks.map((d) => (
              <DeckCard
                key={d.id}
                deck={d}
                onClick={() => openDeck(d.id)}
                onQuiz={() => openDeck(d.id, 'quiz')}
              />
            ))}
          </div>
        )}

        {/* ── Error state ─────────────────────────────────────────────────── */}
        {!loading && fetchError && (
          <div className="text-center pt-16 space-y-4">
            <p className="text-4xl" aria-hidden="true">😵</p>
            <p className="text-ink-muted text-label">Could not load flashcards. Check your connection.</p>
            <button onClick={() => window.location.reload()} className="bg-action text-white font-extrabold px-6 py-2.5 rounded-control border-2 border-ink shadow-hard-sm text-sm active:scale-95 transition-transform">
              Retry
            </button>
          </div>
        )}

        {/* ── Empty state ─────────────────────────────────────────────────── */}
        {!loading && !fetchError && decks.length === 0 && (
          <div className="text-center pt-16 space-y-4">
            <p className="text-4xl" aria-hidden="true">🃏</p>
            <p className="text-ink-muted text-label">
              No flashcards available for your grade yet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
