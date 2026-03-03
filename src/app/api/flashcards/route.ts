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
    const boxDist = [0, 0, 0, 0, 0, 0]; // index 0=unseen, 1-5=box levels
    for (const card of topicCards) {
      const p = progressMap.get(card.id);
      if (!p || new Date(p.nextReviewAt) <= now) dueCount++;
      if (p && p.leitnerBox >= 4) mastered++;
      boxDist[p?.leitnerBox ?? 0]++;
    }
    return {
      id: t.topicId,
      name: t.topicName,
      cardCount: topicCards.length,
      dueCount,
      mastered,
      total: topicCards.length,
      topicColor: getTopicColor(t.topicName),
      boxDistribution: boxDist,
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

  // ── Flashcard study streak ─────────────────────────────────────────────
  // Count consecutive days with at least 1 flashcard session (backwards from today)
  const sessions = await prisma.flashcardSession.findMany({
    where: { studentId },
    orderBy: { createdAt: 'desc' },
    select: { createdAt: true },
    take: 60, // ~2 months of daily sessions max
  });

  let studyStreak = 0;
  if (sessions.length > 0) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // Build set of unique session dates (YYYY-MM-DD)
    const sessionDates = new Set(
      sessions.map((s) => {
        const d = new Date(s.createdAt);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      }),
    );

    // Walk backwards from today
    const checkDate = new Date(today);
    for (let i = 0; i < 60; i++) {
      const key = `${checkDate.getFullYear()}-${String(checkDate.getMonth() + 1).padStart(2, '0')}-${String(checkDate.getDate()).padStart(2, '0')}`;
      if (sessionDates.has(key)) {
        studyStreak++;
      } else if (i === 0) {
        // Today doesn't have a session — still check yesterday
        // (streak only counts if they studied today or yesterday)
      } else {
        break;
      }
      checkDate.setDate(checkDate.getDate() - 1);
    }
  }

  // ── Daily new card cap info ────────────────────────────────────────────
  const todayStart = new Date(now);
  todayStart.setHours(0, 0, 0, 0);
  const newCardsToday = await prisma.flashcardProgress.count({
    where: {
      studentId,
      lastSeenAt: { gte: todayStart },
      timesSeen: 1,
    },
  });

  return NextResponse.json({
    decks: [...specialDecks, ...decks],
    stats: {
      totalCards: gradeCards.length,
      totalSeen,
      totalMastered,
      studyStreak,
      newCardsToday,
      maxNewPerDay: 5,
    },
  });
}
