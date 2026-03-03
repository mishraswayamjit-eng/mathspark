import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import {
  getFlashcardsForGrade,
  getTopicsForGradeFlashcards,
  getTopicColor,
} from '@/data/flashcardData';

export const dynamic = 'force-dynamic';

// GET /api/flashcards?studentId=xxx&grade=N
// Returns deck list with stats for the flashcard selection screen.
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');
  const grade = parseInt(searchParams.get('grade') ?? '4', 10);

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const gradeCards = getFlashcardsForGrade(grade);
  const gradeCardIds = gradeCards.map((c) => c.id);

  // Fetch all FlashcardProgress for this student + grade's cards
  const progress = await prisma.flashcardProgress.findMany({
    where: { studentId, cardId: { in: gradeCardIds } },
    select: {
      cardId: true,
      leitnerBox: true,
      nextReviewAt: true,
      timesSeen: true,
      timesCorrect: true,
    },
  });

  const progressMap = new Map(progress.map((p) => [p.cardId, p]));
  const now = new Date();

  // ── Compute per-topic deck stats ────────────────────────────────────────
  const topics = getTopicsForGradeFlashcards(grade);

  const decks = topics.map((t) => {
    const topicCards = gradeCards.filter((c) => c.topicId === t.topicId);
    let dueCount = 0;
    let mastered = 0;
    for (const card of topicCards) {
      const p = progressMap.get(card.id);
      if (!p || new Date(p.nextReviewAt) <= now) dueCount++;
      if (p && p.leitnerBox >= 4) mastered++;
    }
    return {
      id: t.topicId,
      name: t.topicName,
      cardCount: topicCards.length,
      dueCount,
      mastered,
      total: topicCards.length,
      topicColor: getTopicColor(t.topicName),
    };
  });

  // ── Special decks ───────────────────────────────────────────────────────

  // "Due for Review" — all cards where nextReviewAt <= now (or never seen)
  let totalDue = 0;
  for (const card of gradeCards) {
    const p = progressMap.get(card.id);
    if (!p || new Date(p.nextReviewAt) <= now) totalDue++;
  }

  // Mental math cards
  const mentalCards = gradeCards.filter(
    (c) => c.category === 'mental_math' || c.category === 'warm_up',
  );

  const specialDecks = [
    {
      id: 'due',
      name: 'Due for Review',
      cardCount: totalDue,
      dueCount: totalDue,
      mastered: 0,
      total: totalDue,
      topicColor: '#EF4444',
    },
    {
      id: 'quick',
      name: 'Quick Review',
      cardCount: Math.min(10, gradeCards.length),
      dueCount: 10,
      mastered: 0,
      total: 10,
      topicColor: '#F59E0B',
    },
    {
      id: 'mental_math',
      name: 'Mental Math',
      cardCount: mentalCards.length,
      dueCount: mentalCards.filter((c) => {
        const p = progressMap.get(c.id);
        return !p || new Date(p.nextReviewAt) <= now;
      }).length,
      mastered: mentalCards.filter((c) => {
        const p = progressMap.get(c.id);
        return p && p.leitnerBox >= 4;
      }).length,
      total: mentalCards.length,
      topicColor: '#E879F9',
    },
  ];

  // ── Global stats ────────────────────────────────────────────────────────
  const totalSeen = progress.filter((p) => p.timesSeen > 0).length;
  const totalMastered = progress.filter((p) => p.leitnerBox >= 4).length;

  return NextResponse.json({
    decks: [...specialDecks, ...decks],
    stats: {
      totalCards: gradeCards.length,
      totalSeen,
      totalMastered,
    },
  });
}
