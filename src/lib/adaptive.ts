import { prisma, USABLE_QUESTION_FILTER, aiSourceFilter } from './db';
import { isEqualSurfacingEnabled } from './llm/featureFlags';
import { matchesSubTopicKey } from './sharedUtils';
import { getTopicsForGrade } from '@/data/topicTree';
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

/**
 * Prefer higher-quality sources. Priority:
 *   hand_crafted > pdf_extracted > variant_of_* > other real
 *     > ipm_textbook > ai_generated (last)
 *
 * IPM-textbook questions are real exam stems, so they outrank synthetic
 * `ai_generated` questions — but they sit below our curated/seed sources since
 * their teaching layer is LLM-generated. Authored questions remain last-resort.
 *
 * When `EQUAL_SURFACING` is on, this tiering is bypassed: every eligible question
 * (the pool is already serve-flag filtered upstream) is equally likely, so AI and
 * real exam questions surface the same.
 */
function pickBest<T extends { source: string }>(pool: T[]): T | null {
  if (pool.length === 0) return null;

  if (isEqualSurfacingEnabled()) return pool[Math.floor(Math.random() * pool.length)];

  const crafted = pool.filter((q) => q.source === 'hand_crafted');
  if (crafted.length > 0) return crafted[Math.floor(Math.random() * crafted.length)];

  const extracted = pool.filter((q) => q.source === 'pdf_extracted');
  if (extracted.length > 0) return extracted[Math.floor(Math.random() * extracted.length)];

  const variants = pool.filter((q) => q.source.startsWith('variant_of_'));
  if (variants.length > 0) return variants[Math.floor(Math.random() * variants.length)];

  // Prefer any other real (non-generated) source first.
  const GENERATED = new Set(['ipm_textbook', 'ai_generated']);
  const otherReal = pool.filter((q) => !GENERATED.has(q.source));
  if (otherReal.length > 0) return otherReal[Math.floor(Math.random() * otherReal.length)];

  // Real exam stems (textbook) beat synthetic authored questions.
  const textbook = pool.filter((q) => q.source === 'ipm_textbook');
  if (textbook.length > 0) return textbook[Math.floor(Math.random() * textbook.length)];

  return pool[Math.floor(Math.random() * pool.length)];
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
export async function getNextQuestion(
  studentId: string,
  topicId: string,
  clientExcludeIds: string[] = [],
  subTopicKey: string = '',
) {
  // Session window: midnight today → midnight tomorrow
  const todayStart = new Date();
  todayStart.setHours(0, 0, 0, 0);
  const tomorrowStart = new Date(todayStart);
  tomorrowStart.setDate(tomorrowStart.getDate() + 1);

  // Scoped selection for a single sub-topic key (empty key = whole pool). This is
  // the original `getNextQuestion` body verbatim — same queries, same order.
  async function pickForSubtopic(key: string) {
    // Build optional subTopic filter. The DB `contains` is a cheap SUPERSET used to
    // keep `take: 200` relevant; precise word-boundary matching is applied in-app
    // below so keys like "ratio" don't leak "Ope(ratio)ns" / "angle" → "Tri(angle)s".
    const subTopicFilter = key
      ? { subTopic: { contains: key, mode: 'insensitive' as const } }
      : {};

    // Parallel DB reads
    const [fetchedQuestions, sessionAttempts, progress, misconceptionAttempts] = await Promise.all([
      prisma.question.findMany({
        where: { topicId, ...subTopicFilter, ...USABLE_QUESTION_FILTER, ...aiSourceFilter() },
        take: 200,
      }),

      prisma.attempt.findMany({
        where: {
          studentId,
          createdAt: { gte: todayStart, lt: tomorrowStart },
          question: { topicId, ...subTopicFilter },
        },
        orderBy: { createdAt: 'asc' },
        select: { questionId: true, isCorrect: true },
      }),

      prisma.progress.findUnique({
        where: { studentId_topicId: { studentId, topicId } },
      }),

      // Track subTopics where the student has 3+ misconception-tagged wrong attempts
      prisma.attempt.findMany({
        where: {
          studentId,
          misconceptionType: { not: null },
          question: { topicId, ...subTopicFilter },
        },
        select: { question: { select: { subTopic: true } } },
      }),
    ]);

    // Precise word-boundary filter on the served pool (the DB query above only
    // narrowed it to a substring superset).
    const allQuestions = key
      ? fetchedQuestions.filter((q) => matchesSubTopicKey(q.subTopic, key))
      : fetchedQuestions;

    // Compute boosted subTopics (3+ misconception attempts → higher priority)
    const subTopicMiscCounts = new Map<string, number>();
    for (const a of misconceptionAttempts) {
      const st = a.question.subTopic;
      subTopicMiscCounts.set(st, (subTopicMiscCounts.get(st) ?? 0) + 1);
    }
    const boostedSubTopics = new Set(
      Array.from(subTopicMiscCounts.entries())
        .filter(([, count]) => count >= 3)
        .map(([st]) => st),
    );

    // Filter out already-seen questions (DB attempts + client-provided IDs)
    const seenIds  = new Set([
      ...sessionAttempts.map((a) => a.questionId),
      ...clientExcludeIds,
    ]);
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

    // ── Step 5–6: Pick with fallback (boosted subTopics get priority) ─────────
    function pickWithBoost(pool: typeof available) {
      if (boostedSubTopics.size > 0) {
        const boosted = pool.filter((q) => boostedSubTopics.has(q.subTopic));
        if (boosted.length > 0) return pickBest(boosted);
      }
      return pickBest(pool);
    }

    // Try target difficulty first
    const atTarget = available.filter((q) => q.difficulty === targetDiff);
    const picked   = pickWithBoost(atTarget);
    if (picked) return picked;

    // Fallback: adjacent difficulties (closer first)
    const diffIdx   = DIFFICULTIES.indexOf(targetDiff);
    const fallbacks = [diffIdx - 1, diffIdx + 1, diffIdx - 2, diffIdx + 2]
      .filter((i) => i >= 0 && i < 3)
      .map((i) => DIFFICULTIES[i]);

    for (const d of fallbacks) {
      const pool = available.filter((q) => q.difficulty === d);
      const p    = pickWithBoost(pool);
      if (p) return p;
    }

    // Fallback: any unseen question
    if (available.length > 0) return pickWithBoost(available);

    // Absolute fallback: session exhausted — pick from full set but still
    // respect client-provided IDs (those are in-flight in the current lesson)
    const clientExclude = new Set(clientExcludeIds);
    const notInLesson   = allQuestions.filter((q) => !clientExclude.has(q.id));
    if (notInLesson.length > 0) return pickBest(notInLesson);

    // Truly exhausted — caller will show completion screen
    return null;
  }

  // ── Keyed-grade rotation ──────────────────────────────────────────────────
  // Keyed grades (grade2/3/5/… ) share ONE dbTopicId across all sub-topics. With
  // no sub-topic filter, `take: 200` only ever reaches the first ~200 rows of a
  // multi-thousand-row pool, so a few topics dominate. Rotate to the least-served
  // sub-topic today, then reuse the (correct) scoped selection above.
  const gradeMatch = /^grade(\d+)$/.exec(topicId);
  if (gradeMatch && !subTopicKey) {
    const gradeNum = Number(gradeMatch[1]);
    const keys = getTopicsForGrade(gradeNum)
      .map((n) => n.subTopicKey)
      .filter((k): k is string => Boolean(k));

    if (keys.length > 1) {
      // One extra small indexed query: today's attempts for this grade pool.
      const todays = await prisma.attempt.findMany({
        where: { studentId, createdAt: { gte: todayStart, lt: tomorrowStart }, question: { topicId } },
        select: { question: { select: { subTopic: true } } },
      });

      // Tally served-count per key via precise word-boundary matching.
      const served = new Map<string, number>(keys.map((k) => [k, 0]));
      for (const a of todays) {
        const st = a.question.subTopic;
        for (const k of keys) if (matchesSubTopicKey(st, k)) served.set(k, served.get(k)! + 1);
      }

      // Least-served first, random tie-break → round-robin rotation.
      const ordered = keys
        .map((k) => ({ k, n: served.get(k)!, r: Math.random() }))
        .sort((a, b) => a.n - b.n || a.r - b.r)
        .map((x) => x.k);

      for (const k of ordered) {
        const q = await pickForSubtopic(k);
        if (q) return q; // first non-exhausted sub-topic wins
      }
      // Every sub-topic exhausted → fall through to whole-pool (original behavior).
    }
  }

  return pickForSubtopic(subTopicKey); // ch-series, focused path, and safety fallback
}
