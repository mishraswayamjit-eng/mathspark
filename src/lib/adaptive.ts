import { prisma, USABLE_QUESTION_FILTER, aiSourceFilter } from './db';
import { isEqualSurfacingEnabled } from './llm/featureFlags';
import { matchesSubTopicKey } from './sharedUtils';
import { shuffle } from './shuffle';
import { getTopicsForGrade } from '@/data/topicTree';
import type { Difficulty } from '@/types';
import {
  LADDER_WINDOW_DAYS,
  computeLadder,
  isRealExamSource,
  isStrongStart,
  ladderTiers,
  variantIdPrefixes,
  withServedQuestion,
} from './practice/ladder';

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

// India has one time zone and no daylight saving: UTC + 5:30.
const IST_OFFSET_MS = 330 * 60 * 1000;
const DAY_MS = 24 * 60 * 60 * 1000;

/** Midnight in India at the start of the day `now` falls on, as a real instant. */
function indiaDayStart(now: Date): Date {
  const shifted = new Date(now.getTime() + IST_OFFSET_MS);
  shifted.setUTCHours(0, 0, 0, 0);
  return new Date(shifted.getTime() - IST_OFFSET_MS);
}

/**
 * The topic-tree node a sub-topic key names in a keyed grade ("grade5" +
 * "fraction" → "gr5_fractions"), or '' when there is none (a chapter topic, no
 * key, or a key that is not one of the grade's topics).
 */
function nodeIdForKey(topicId: string, key: string): string {
  const grade = /^grade(\d+)$/.exec(topicId);
  if (!grade || !key) return '';
  const wanted = key.trim().toLowerCase();
  const nodes = getTopicsForGrade(Number(grade[1]));
  for (let i = 0; i < nodes.length; i++) {
    if ((nodes[i].subTopicKey ?? '').toLowerCase() === wanted) return nodes[i].id;
  }
  return '';
}

// ── Main export ───────────────────────────────────────────────────────────────

/**
 * Adaptive next-question picker.
 *
 * All session context (seen questions, streak) is derived from the database.
 * Streak = today's attempts (midnight to midnight, local time); seen-exclusion
 * spans a rolling multi-day window so the same user doesn't get repeats day-to-day.
 *
 * Rules:
 *  1. Fetch all questions for the topic + recent attempts in parallel.
 *  2. Exclude questions answered within the rolling seen window.
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
  // Optional self-reported confidence from the lesson intro ("Could you solve
  // these?"). It only shifts the starting difficulty one level for the first
  // few questions of the day; after that the real streak signal takes over.
  confidence?: 'low' | 'high',
) {
  const picked = await getNextQuestionWithLadder(studentId, topicId, clientExcludeIds, subTopicKey, confidence);
  return picked.question;
}

/**
 * The same pick, plus where the child is on the topic ladder.
 *
 * `ladder` is set only for focused topic practice on a keyed grade (`grade5`
 * with `subTopicKey` naming one of that grade's topics). There the ladder
 * (`src/lib/practice/ladder.ts`) decides the difficulty and source band, so
 * the child meets Easy, then Medium, then Hard, then real exam questions. In
 * every other case `ladder` is null and the pick is exactly the one described
 * above. Set `TOPIC_LADDER=off` to switch the ladder off everywhere.
 */
export async function getNextQuestionWithLadder(
  studentId: string,
  topicId: string,
  clientExcludeIds: string[] = [],
  subTopicKey: string = '',
  confidence?: 'low' | 'high',
) {
  // Session window: midnight today → midnight tomorrow (drives streak/difficulty).
  // "Today" is the child's day in India, not the server's (which runs in UTC).
  const todayStart = indiaDayStart(new Date());
  const tomorrowStart = new Date(todayStart.getTime() + DAY_MS);

  // Seen-exclusion window: a rolling multi-day span so a student practising the
  // same topic across days doesn't get the same questions back. Streak logic still
  // uses today only (below). 14 days is long enough to feel fresh, short enough to
  // avoid starving small sub-topic pools (the absolute fallback re-serves if a pool
  // is genuinely exhausted).
  const SEEN_WINDOW_DAYS = 14;
  const seenWindowStart = new Date(todayStart.getTime() - SEEN_WINDOW_DAYS * DAY_MS);

  // Scoped selection for a single sub-topic key (empty key = whole pool). This is
  // the original `getNextQuestion` body verbatim — same queries, same order.
  async function pickForSubtopic(key: string) {
    // Which questions belong to this key. A question that names its own topic
    // (`nodeId`) is served only there: a "Fraction addition" question belongs to
    // Fractions, though its label also matches the key of Addition & Subtraction.
    // Without a `nodeId` (or when the key names no topic of the grade) the label
    // decides. The DB `contains` is a cheap SUPERSET; precise word-boundary
    // matching is applied in-app (`belongs`) so keys like "ratio" don't leak
    // "Ope(ratio)ns" / "angle" → "Tri(angle)s".
    const ownNodeId = nodeIdForKey(topicId, key);
    const byLabel = { subTopic: { contains: key, mode: 'insensitive' as const } };
    const inKey = !key
      ? {}
      : ownNodeId
        ? {
            OR: [
              { nodeId: ownNodeId },
              { AND: [{ OR: [{ nodeId: null }, { nodeId: '' }] }, byLabel] },
            ],
          }
        : byLabel;
    const belongs = (q: { subTopic: string; nodeId?: string | null }) =>
      !key || (ownNodeId && q.nodeId ? q.nodeId === ownNodeId : matchesSubTopicKey(q.subTopic, key));

    // Parallel DB reads. The topic is read whole but light (three short
    // columns), so a topic of any size is reached; full rows are fetched below
    // only for the questions that can be served now.
    const [lightPool, sessionAttempts, progress, misconceptionAttempts] = await Promise.all([
      prisma.question.findMany({
        where: { topicId, ...inKey, ...USABLE_QUESTION_FILTER, ...aiSourceFilter() },
        select: { id: true, subTopic: true, nodeId: true },
      }),

      prisma.attempt.findMany({
        where: {
          studentId,
          createdAt: { gte: seenWindowStart, lt: tomorrowStart },
          question: { topicId, ...inKey },
        },
        orderBy: { createdAt: 'asc' },
        select: { questionId: true, isCorrect: true, createdAt: true },
      }),

      prisma.progress.findUnique({
        where: { studentId_topicId: { studentId, topicId } },
      }),

      // Track subTopics where the student has 3+ misconception-tagged wrong attempts
      prisma.attempt.findMany({
        where: {
          studentId,
          misconceptionType: { not: null },
          question: { topicId, ...inKey },
        },
        select: { question: { select: { subTopic: true } } },
      }),
    ]);

    // Full rows for at most FULL_READ questions: the ones not seen in the window
    // and not in this lesson, or, when every question has been seen, the ones
    // not in this lesson (the absolute fallback below serves from those).
    const FULL_READ = 200;
    const poolIds = lightPool.filter(belongs).map((q) => q.id);
    const seenBefore = new Set<string>(clientExcludeIds);
    for (const a of sessionAttempts) seenBefore.add(a.questionId);
    let candidateIds = poolIds.filter((id) => !seenBefore.has(id));
    if (candidateIds.length === 0) {
      const inLesson = new Set<string>(clientExcludeIds);
      candidateIds = poolIds.filter((id) => !inLesson.has(id));
    }
    if (candidateIds.length > FULL_READ) candidateIds = shuffle(candidateIds).slice(0, FULL_READ);
    const fetchedQuestions =
      candidateIds.length > 0
        ? await prisma.question.findMany({
            where: { id: { in: candidateIds }, ...USABLE_QUESTION_FILTER, ...aiSourceFilter() },
          })
        : [];
    const allQuestions = fetchedQuestions.filter(belongs);

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

    // Filter out already-seen questions (DB attempts across the seen window +
    // client-provided IDs). The wider window pushes repeats out across days.
    const seenIds  = new Set([
      ...sessionAttempts.map((a) => a.questionId),
      ...clientExcludeIds,
    ]);
    const available = allQuestions.filter((q) => !seenIds.has(q.id));

    // Streak/difficulty is a *today-only* signal. Attempts without a createdAt
    // (unit-test fixtures) are treated as today so test behaviour is unchanged.
    const todayAttempts = sessionAttempts.filter(
      (a) => !a.createdAt || new Date(a.createdAt) >= todayStart,
    );

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

    // ── Step 3b: Self-reported confidence (first few questions today only) ───
    const CONFIDENCE_WINDOW = 4;
    if (confidence && todayAttempts.length < CONFIDENCE_WINDOW) {
      targetDiff = clampDiff(DIFFICULTIES.indexOf(targetDiff) + (confidence === 'high' ? 1 : -1));
    }

    // ── Step 4: Streak adjustments (today only) ──────────────────────────────
    const recent5 = todayAttempts.slice(-5);
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
        select: { question: { select: { subTopic: true, nodeId: true } } },
      });

      // Tally served-count per key: under the topic a question names (`nodeId`)
      // when it names one, else via precise word-boundary matching of its label.
      const served = new Map<string, number>(keys.map((k) => [k, 0]));
      const keyOfNode = new Map<string, string>();
      for (const k of keys) {
        const nid = nodeIdForKey(topicId, k);
        if (nid) keyOfNode.set(nid, k);
      }
      for (const a of todays) {
        const named = a.question.nodeId ? keyOfNode.get(a.question.nodeId) : undefined;
        if (named) {
          served.set(named, served.get(named)! + 1);
          continue;
        }
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
        if (q) return { question: q, ladder: null }; // first non-exhausted sub-topic wins
      }
      // Every sub-topic exhausted → fall through to whole-pool (original behavior).
    }
  }

  // ── Topic ladder (focused practice on a keyed grade) ──────────────────────
  // One topic of a keyed grade: Warm-up → Build → Challenge → Exam. The rules
  // live in `practice/ladder.ts`; here we read the topic's questions and the
  // child's answers, and choose inside the band the ladder asks for. The seen
  // window, the usable-question filter, the generated-source kill-switches and
  // the source ranking (`pickBest`) all still apply.
  async function pickOnLadder(key: string, topicLabel: string, gradeNum: number, ownNodeId: string) {
    // Generated questions whose topic is only in their id (see ladder.ts).
    const idPrefixes = variantIdPrefixes(gradeNum, key);
    const inTopic = {
      topicId,
      OR: [
        { nodeId: ownNodeId },
        { subTopic: { contains: key, mode: 'insensitive' as const } },
        ...idPrefixes.map((p) => ({ id: { startsWith: p } })),
      ],
    };
    // A question that names its own topic (`nodeId`) belongs only there; one
    // without it is placed by its label or its id, as before.
    const belongs = (id: string, subTopic: string, nodeId?: string | null) =>
      nodeId
        ? nodeId === ownNodeId
        : matchesSubTopicKey(subTopic, key) || idPrefixes.some((p) => id.indexOf(p) === 0);

    const ladderWindowStart = new Date(todayStart.getTime() - LADDER_WINDOW_DAYS * DAY_MS);

    const [lightPool, windowAttempts] = await Promise.all([
      // The whole topic, light columns only: the ladder needs every band's size,
      // and `take: 200` on full rows would cut large topics short.
      prisma.question.findMany({
        where: { ...inTopic, ...USABLE_QUESTION_FILTER, ...aiSourceFilter() },
        select: { id: true, subTopic: true, difficulty: true, source: true, nodeId: true },
      }),
      prisma.attempt.findMany({
        where: {
          studentId,
          createdAt: { gte: ladderWindowStart, lt: tomorrowStart },
          question: inTopic,
        },
        orderBy: { createdAt: 'asc' },
        select: {
          questionId: true,
          isCorrect: true,
          createdAt: true,
          question: { select: { subTopic: true, difficulty: true, source: true, nodeId: true } },
        },
      }),
    ]);

    const pool = lightPool.filter((q) => belongs(q.id, q.subTopic, q.nodeId));
    if (pool.length === 0) return null;
    const topicAttempts = windowAttempts.filter((a) => belongs(a.questionId, a.question.subTopic, a.question.nodeId));

    // "Already doing well": the child's last 10 answers in this grade before
    // they began this topic (or up to now, if they have not begun). Fixed once
    // the topic is begun, so the starting step does not move under the child.
    const firstAttempt = topicAttempts.length > 0 ? topicAttempts[0] : null;
    const before = await prisma.attempt.findMany({
      where: {
        studentId,
        createdAt: { lt: firstAttempt ? firstAttempt.createdAt : tomorrowStart },
        question: { topicId },
      },
      orderBy: { createdAt: 'desc' },
      take: 10,
      select: { isCorrect: true },
    });

    const plan = computeLadder({
      topicLabel,
      pool,
      attempts: topicAttempts.map((a) => ({
        questionId: a.questionId,
        isCorrect: a.isCorrect,
        difficulty: a.question.difficulty,
        source: a.question.source,
      })),
      startHigher: isStrongStart(before.map((a) => a.isCorrect)),
    });
    if (!plan) return null;

    // Not seen in the rolling window (shorter than the ladder's), nor in this lesson.
    const seen = new Set<string>(clientExcludeIds);
    for (const a of topicAttempts) {
      if (!a.createdAt || new Date(a.createdAt) >= seenWindowStart) seen.add(a.questionId);
    }
    let tiers = ladderTiers(plan, pool.filter((q) => !seen.has(q.id)));
    if (tiers.length === 0) {
      // Everything seen: serve again rather than stop, but never a question
      // that is already in this lesson.
      const inLesson = new Set<string>(clientExcludeIds);
      tiers = ladderTiers(plan, pool.filter((q) => !inLesson.has(q.id)));
    }
    if (tiers.length === 0) return { question: null, ladder: null }; // truly exhausted

    const chosen = pickBest(tiers[0]);
    const question = chosen ? await prisma.question.findUnique({ where: { id: chosen.id } }) : null;
    if (!question) return null;
    return { question, ladder: withServedQuestion(plan.info, isRealExamSource(question.source)) };
  }

  if (gradeMatch && subTopicKey && process.env.TOPIC_LADDER !== 'off') {
    const gradeNum = Number(gradeMatch[1]);
    const wanted = subTopicKey.trim().toLowerCase();
    const node = getTopicsForGrade(gradeNum).filter(
      (n) => (n.subTopicKey ?? '').toLowerCase() === wanted,
    )[0];
    if (node) {
      const onLadder = await pickOnLadder(wanted, node.name, gradeNum, node.id);
      if (onLadder) return onLadder;
      // No questions for this topic: the scoped pick below decides what happens.
    }
  }

  // ch-series, focused path without a ladder, and safety fallback
  return { question: await pickForSubtopic(subTopicKey), ladder: null };
}
