'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import type { FlashcardDeck, FlashcardStats } from '@/types';

// ── Mastery ring SVG ─────────────────────────────────────────────────────────

function MasteryRing({ mastered, total, size = 36 }: { mastered: number; total: number; size?: number }) {
  const pct = total > 0 ? mastered / total : 0;
  const r = (size - 6) / 2;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - pct);
  const color = pct >= 0.7 ? '#34D399' : pct >= 0.3 ? '#FBBF24' : '#64748B';
  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1E293B" strokeWidth={4} />
      <circle
        cx={size / 2} cy={size / 2} r={r}
        fill="none" stroke={color} strokeWidth={4}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        className="transition-all duration-700"
      />
      <text
        x={size / 2} y={size / 2}
        textAnchor="middle" dominantBaseline="central"
        fill="#F1F5F9" fontSize={size * 0.28} fontWeight="bold"
      >
        {Math.round(pct * 100)}%
      </text>
    </svg>
  );
}

// ── Deck card ────────────────────────────────────────────────────────────────

function DeckCard({
  deck, onClick,
}: {
  deck: FlashcardDeck;
  onClick: () => void;
}) {
  const isSpecial = ['due', 'quick', 'mental_math'].includes(deck.id);
  const emoji = deck.id === 'due' ? '🔥' : deck.id === 'quick' ? '⚡' : deck.id === 'mental_math' ? '🧠' : '📁';
  return (
    <button
      onClick={onClick}
      className="w-full flex items-center gap-3 rounded-2xl px-4 py-3.5 transition-all active:scale-[0.98]"
      style={{
        background: '#1E293B',
        borderLeft: `4px solid ${deck.topicColor}`,
      }}
    >
      <span className="text-xl flex-shrink-0">{emoji}</span>
      <div className="flex-1 text-left min-w-0">
        <p className="text-sm font-bold text-[#F1F5F9] truncate">{deck.name}</p>
        <p className="text-xs text-[#64748B]">
          {deck.cardCount} card{deck.cardCount !== 1 ? 's' : ''}
          {deck.dueCount > 0 && !isSpecial && (
            <span className="ml-1 text-amber-400">· {deck.dueCount} due</span>
          )}
        </p>
      </div>
      {!isSpecial && (
        <MasteryRing mastered={deck.mastered} total={deck.total} />
      )}
      {isSpecial && deck.dueCount > 0 && (
        <span className="bg-red-500/20 text-red-400 text-xs font-bold px-2 py-0.5 rounded-full tabular-nums">
          {deck.dueCount}
        </span>
      )}
    </button>
  );
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function FlashcardsPage() {
  const router = useRouter();
  const [decks, setDecks] = useState<FlashcardDeck[]>([]);
  const [stats, setStats] = useState<FlashcardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const sid = localStorage.getItem('mathspark_student_id');
    const grade = localStorage.getItem('mathspark_student_grade') || '4';
    if (!sid) { router.replace('/start'); return; }

    fetch(`/api/flashcards?studentId=${sid}&grade=${grade}`)
      .then((r) => r.json())
      .then((data) => {
        setDecks(data.decks ?? []);
        setStats(data.stats ?? null);
        // Cache due count for BottomNav badge
        const dueDeck = (data.decks ?? []).find((d: FlashcardDeck) => d.id === 'due');
        if (dueDeck) {
          try { localStorage.setItem('mathspark_cards_due', String(dueDeck.dueCount)); } catch {}
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [router]);

  const specialDecks = decks.filter((d) => ['due', 'quick', 'mental_math'].includes(d.id));
  const topicDecks = decks.filter((d) => !['due', 'quick', 'mental_math'].includes(d.id));

  function openDeck(deckId: string) {
    router.push(`/flashcards/session?deck=${deckId}&mode=classic`);
  }

  return (
    <div className="min-h-screen bg-[#0F172A] pb-24">
      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-30 bg-[#0F172A]/95 backdrop-blur-md border-b border-white/5 px-4 py-3">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <button onClick={() => router.back()} className="text-[#94A3B8] text-sm">
            ← Back
          </button>
          <h1 className="text-[#F1F5F9] font-bold text-lg">🃏 Sparky&apos;s Cards</h1>
          <div className="w-12" />
        </div>
      </div>

      <div className="max-w-md mx-auto px-4 pt-4 space-y-6">
        {/* ── Stats bar ───────────────────────────────────────────────────── */}
        {stats && !loading && (
          <div className="flex items-center justify-around bg-[#1E293B] rounded-2xl px-4 py-3">
            <div className="text-center">
              <p className="text-lg font-bold text-[#F1F5F9] tabular-nums">{stats.totalCards}</p>
              <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Total</p>
            </div>
            <div className="w-px h-8 bg-white/10" />
            <div className="text-center">
              <p className="text-lg font-bold text-[#34D399] tabular-nums">{stats.totalSeen}</p>
              <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Seen</p>
            </div>
            <div className="w-px h-8 bg-white/10" />
            <div className="text-center">
              <p className="text-lg font-bold text-[#60A5FA] tabular-nums">{stats.totalMastered}</p>
              <p className="text-[10px] text-[#64748B] uppercase tracking-wider">Mastered</p>
            </div>
          </div>
        )}

        {/* ── Loading skeleton ────────────────────────────────────────────── */}
        {loading && (
          <div className="space-y-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="h-16 bg-[#1E293B] rounded-2xl animate-pulse" />
            ))}
          </div>
        )}

        {/* ── Special decks ───────────────────────────────────────────────── */}
        {!loading && specialDecks.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-[#64748B] px-1">
              Quick Start
            </h2>
            {specialDecks.map((d) => (
              <DeckCard key={d.id} deck={d} onClick={() => openDeck(d.id)} />
            ))}
          </div>
        )}

        {/* ── Topic decks ─────────────────────────────────────────────────── */}
        {!loading && topicDecks.length > 0 && (
          <div className="space-y-2">
            <h2 className="text-xs font-bold uppercase tracking-wider text-[#64748B] px-1">
              By Topic
            </h2>
            {topicDecks.map((d) => (
              <DeckCard key={d.id} deck={d} onClick={() => openDeck(d.id)} />
            ))}
          </div>
        )}

        {/* ── Empty state ─────────────────────────────────────────────────── */}
        {!loading && decks.length === 0 && (
          <div className="text-center pt-16 space-y-4">
            <p className="text-4xl">🃏</p>
            <p className="text-[#94A3B8] text-sm">
              No flashcards available for your grade yet.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
