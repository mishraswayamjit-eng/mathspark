import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import {
  getFlashcardsForGrade,
  getFlashcardsByTopic,
  getAllFlashcards,
} from '@/data/flashcardData';
import type { FlashCard } from '@/types';

export const dynamic = 'force-dynamic';

// Leitner box → review interval in days
const BOX_INTERVALS = [0, 1, 2, 5, 14, 30]; // index 0 unused; box 1→1d, box 2→2d, etc.

/**
 * GET /api/flashcards/deck?studentId=xxx&grade=N&deck=due|quick|mental_math|<topicId>
 *
 * Returns an ordered list of FlashCard objects for the session.
 * - "due": cards where nextReviewAt <= now, ordered by leitnerBox ASC (weakest first)
 * - "quick": 10 smart-selected cards (prioritize box 1-2, mix in unseen)
 * - "mental_math": warm_up + mental_math category cards
 * - <topicId>: all cards for that topic, due ones first
 */
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');
  const grade = parseInt(searchParams.get('grade') ?? '4', 10);
  const deckId = searchParams.get('deck') ?? 'quick';

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  // ── Resolve candidate cards ─────────────────────────────────────────────
  let candidates: FlashCard[];

  if (deckId === 'mental_math') {
    candidates = getFlashcardsForGrade(grade).filter(
      (c) => c.category === 'mental_math' || c.category === 'warm_up',
    );
  } else if (deckId === 'due' || deckId === 'quick') {
    candidates = getFlashcardsForGrade(grade);
  } else {
    // topicId
    candidates = getFlashcardsByTopic(grade, deckId);
    // Fallback: if no topic match for this grade, try all grades
    if (candidates.length === 0) {
      candidates = getAllFlashcards().filter((c) => c.topicId === deckId);
    }
  }

  if (candidates.length === 0) {
    return NextResponse.json({ cards: [], deckName: 'Empty Deck' });
  }

  const cardIds = candidates.map((c) => c.id);

  // ── Fetch progress for these cards ──────────────────────────────────────
  const progress = await prisma.flashcardProgress.findMany({
    where: { studentId, cardId: { in: cardIds } },
  });
  const progressMap = new Map(progress.map((p) => [p.cardId, p]));
  const now = new Date();

  // ── Daily new card cap: max 5 new cards introduced today ────────────────
  const todayStart = new Date(now);
  todayStart.setHours(0, 0, 0, 0);
  const newCardsSeenToday = await prisma.flashcardProgress.count({
    where: {
      studentId,
      lastSeenAt: { gte: todayStart },
      timesSeen: 1, // first-time seen today
    },
  });
  const MAX_NEW_PER_DAY = 5;
  const newCardBudget = Math.max(0, MAX_NEW_PER_DAY - newCardsSeenToday);

  // ── Build ordered deck ──────────────────────────────────────────────────
  let deck: FlashCard[];

  if (deckId === 'due') {
    // Cards due for review: nextReviewAt <= now OR never seen
    deck = candidates
      .filter((c) => {
        const p = progressMap.get(c.id);
        return !p || new Date(p.nextReviewAt) <= now;
      })
      .sort((a, b) => {
        const pa = progressMap.get(a.id);
        const pb = progressMap.get(b.id);
        // Lowest box first (most urgent)
        return (pa?.leitnerBox ?? 0) - (pb?.leitnerBox ?? 0);
      });
    // Cap at 20 per session to avoid anxiety
    deck = deck.slice(0, 20);
  } else if (deckId === 'quick') {
    // Smart selection: prioritize box 1-2 due cards, then unseen, pad with box 3-4
    const due = candidates.filter((c) => {
      const p = progressMap.get(c.id);
      return p && p.leitnerBox <= 2 && new Date(p.nextReviewAt) <= now;
    });
    const unseen = candidates.filter((c) => !progressMap.has(c.id));
    const reinforcement = candidates.filter((c) => {
      const p = progressMap.get(c.id);
      return p && p.leitnerBox >= 3 && new Date(p.nextReviewAt) <= now;
    });

    // Shuffle helpers
    const shuffle = <T,>(arr: T[]): T[] => {
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    };

    // Cap unseen to daily new card budget
    const unseenCap = Math.min(3, newCardBudget);
    deck = [
      ...shuffle(due).slice(0, 5),
      ...shuffle(unseen).slice(0, unseenCap),
      ...shuffle(reinforcement).slice(0, 2),
    ].slice(0, 10);

    // If still < 10, pad with random candidates
    if (deck.length < 10) {
      const usedIds = new Set(deck.map((c) => c.id));
      const remaining = shuffle(candidates.filter((c) => !usedIds.has(c.id)));
      deck = [...deck, ...remaining.slice(0, 10 - deck.length)];
    }

    // Final shuffle so it's not always easy→hard
    deck = shuffle(deck);
  } else {
    // Topic or mental_math: due cards first, then unseen, then rest
    const due: FlashCard[] = [];
    const unseen: FlashCard[] = [];
    const rest: FlashCard[] = [];

    for (const c of candidates) {
      const p = progressMap.get(c.id);
      if (!p) unseen.push(c);
      else if (new Date(p.nextReviewAt) <= now) due.push(c);
      else rest.push(c);
    }

    due.sort((a, b) => (progressMap.get(a.id)?.leitnerBox ?? 0) - (progressMap.get(b.id)?.leitnerBox ?? 0));
    // Cap unseen to daily budget
    const cappedUnseen = unseen.slice(0, newCardBudget);
    deck = [...due, ...cappedUnseen, ...rest].slice(0, 20);
  }

  // ── Attach progress data to each card for the client ────────────────────
  const cardsWithProgress = deck.map((c) => {
    const p = progressMap.get(c.id);
    return {
      ...c,
      leitnerBox: p?.leitnerBox ?? 0,
      timesSeen: p?.timesSeen ?? 0,
      timesCorrect: p?.timesCorrect ?? 0,
      streakOnCard: p?.streakOnCard ?? 0,
    };
  });

  // Derive deck name
  let deckName = 'Flashcards';
  if (deckId === 'due') deckName = 'Due for Review';
  else if (deckId === 'quick') deckName = 'Quick Review';
  else if (deckId === 'mental_math') deckName = 'Mental Math';
  else if (deck.length > 0) deckName = deck[0].topicName;

  return NextResponse.json({
    cards: cardsWithProgress,
    deckName,
    totalInDeck: candidates.length,
    newCardsSeenToday,
    newCardBudget,
  });
}
