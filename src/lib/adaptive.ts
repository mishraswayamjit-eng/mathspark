import { prisma } from './db';
import type { Difficulty } from '@/types';

// ── Helpers ───────────────────────────────────────────────────────────────────

const DIFFICULTIES: Difficulty[] = ['Easy', 'Medium', 'Hard'];

function clampDiff(idx: number): Difficulty {
  return DIFFICULTIES[Math.max(0, Math.min(2, idx))];
}

/**
 * Weighted random pick over [Easy, Medium, Hard].
 * Pass probabilities for [Easy, Medium, Hard] — must sum to 1.
 */
function weightedDiff(pEasy: number, pMedium: number, _pHard: number): Difficulty {
  const r = Math.random();
  if (r < pEasy)          return 'Easy';
  if (r < pEasy + pMedium) return 'Medium';
  return 'Hard';
}

/** Prefer hand_crafted questions; random-pick within the preferred set. */
function pickBest<T extends { source: string }>(pool: T[]): T | null {
  if (pool.length === 0) return null;
  const crafted = pool.filter((q) => q.source === 'hand_crafted');
  const candidates = crafted.length > 0 ? crafted : pool;
  return candidates[Math.floor(Math.random() * candidates.length)];
}

// ── Main export ───────────────────────────────────────────────────────────────

/**
 * Adaptive next-question picker.
 *
 * All session context (seen questions, streak) is derived from the database.
 * "Session" = questions answered today (midnight to midnight, local time).
 *
 * Rules:
 *  1. Fetch all questions for the topic + today's attempts in parallel.
 *  2. Exclude questions already answered today.
 *  3. Derive base difficulty from the student's mastery level:
 *       NotStarted → 80% Easy, 20% Medium
 *       Practicing  → 20% Easy, 60% Medium, 20% Hard
 *       Mastered    → 20% Medium, 80% Hard
 *  4. Streak adjustment (from today's attempts):
 *       Last 3 all wrong → drop 1 difficulty level
 *       Last 5 all right → raise 1 difficulty level
 *  5. Prefer hand_crafted over auto_generated at the same difficulty.
 *  6. Fall back to adjacent difficulties, then any unseen, then reset pool.
 */
export async function getNextQuestion(studentId: string, topicId: string) {
  // Session window: midnight today → midnight tomorrow
  const todayStart = new Date();
  todayStart.setHours(0, 0, 0, 0);
  const tomorrowStart = new Date(todayStart);
  tomorrowStart.setDate(tomorrowStart.getDate() + 1);

  // Parallel DB reads
  const [allQuestions, sessionAttempts, progress] = await Promise.all([
    prisma.question.findMany({ where: { topicId } }),

    prisma.attempt.findMany({
      where: {
        studentId,
        createdAt: { gte: todayStart, lt: tomorrowStart },
        question: { topicId },
      },
      orderBy: { createdAt: 'asc' },
      select: { questionId: true, isCorrect: true },
    }),

    prisma.progress.findUnique({
      where: { studentId_topicId: { studentId, topicId } },
    }),
  ]);

  // Filter out already-seen questions
  const seenIds  = new Set(sessionAttempts.map((a) => a.questionId));
  const available = allQuestions.filter((q) => !seenIds.has(q.id));

  // ── Step 3: Base difficulty from mastery ─────────────────────────────────
  const mastery = progress?.mastery ?? 'NotStarted';
  let targetDiff: Difficulty;
  if (mastery === 'NotStarted') {
    targetDiff = weightedDiff(0.8, 0.2, 0.0);
  } else if (mastery === 'Mastered') {
    targetDiff = weightedDiff(0.0, 0.2, 0.8);
  } else {
    // Practicing
    targetDiff = weightedDiff(0.2, 0.6, 0.2);
  }

  // ── Step 4: Streak adjustments ───────────────────────────────────────────
  const recent5 = sessionAttempts.slice(-5);
  const last3   = recent5.slice(-3);
  if (last3.length === 3 && last3.every((a) => !a.isCorrect)) {
    // 3 wrong in a row → easier
    targetDiff = clampDiff(DIFFICULTIES.indexOf(targetDiff) - 1);
  } else if (recent5.length === 5 && recent5.every((a) => a.isCorrect)) {
    // 5 right in a row → harder
    targetDiff = clampDiff(DIFFICULTIES.indexOf(targetDiff) + 1);
  }

  // ── Step 5–6: Pick with fallback ─────────────────────────────────────────
  // Try target difficulty first
  const atTarget = available.filter((q) => q.difficulty === targetDiff);
  const picked   = pickBest(atTarget);
  if (picked) return picked;

  // Fallback: adjacent difficulties (closer first)
  const diffIdx   = DIFFICULTIES.indexOf(targetDiff);
  const fallbacks = [diffIdx - 1, diffIdx + 1, diffIdx - 2, diffIdx + 2]
    .filter((i) => i >= 0 && i < 3)
    .map((i) => DIFFICULTIES[i]);

  for (const d of fallbacks) {
    const pool = available.filter((q) => q.difficulty === d);
    const p    = pickBest(pool);
    if (p) return p;
  }

  // Fallback: any unseen question
  if (available.length > 0) return pickBest(available);

  // Absolute fallback: session exhausted — pick from full set
  return pickBest(allQuestions);
}
