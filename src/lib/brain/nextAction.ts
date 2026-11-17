/**
 * Next best action: what the app suggests a child does next.
 *
 * Everything here is deterministic. No model is called, and nothing here
 * changes grading, XP or mastery: the rules only READ what the child has
 * already done and point at content that already exists.
 *
 * Two halves:
 *   rankNextActions(input)  pure, over plain data, unit-tested
 *   getNextActions(id)      gathers that data for one child and calls it
 *
 * ── The rules, in priority order ────────────────────────────────────────────
 *  1 lesson_after_misses   MISSES_FOR_LESSON (3) or more misses on one sub-topic in
 *                          the last 7 days, and the mapped lesson is not done.
 *                          A hands-on lesson not yet finished comes first; otherwise
 *                          the concept lesson, unless its best quiz score is
 *                          LESSON_PASS_SCORE (70) or more.
 *  2 explain_missed        A question missed in the last 3 days (and not since
 *                          answered correctly) has an "Explain it to me" lesson.
 *                          There is no deep link that opens a lesson for a given
 *                          question yet, so this sends the child to practice on
 *                          that sub-topic (see practiceHref / explainHref).
 *  3 review_idle           A sub-topic that was strong (mastery 0.6+ over 5+ attempts,
 *                          or accuracy 75%+ over 8+ attempts) and has not been
 *                          touched for IDLE_DAYS (14) or more.
 *    review_dropped        Accuracy over the last 7 days is DROP_SIZE (0.2) or more
 *                          below the two weeks before (which were 75%+), with at
 *                          least 4 recent and 5 earlier attempts.
 *  4 flashcards_due        FLASHCARDS_DUE_MIN (10) or more cards the child has
 *                          seen before are due for review.
 *  5 drill_close           Accuracy 60–80% over DRILL_MIN_ATTEMPTS (8) or more
 *                          attempts, a skill drill is mapped, and a session of it
 *                          was not finished in the last 7 days. The link goes to
 *                          the lowest level made for the child's grade, which is
 *                          always open (src/lib/drillUnlock.ts). Higher levels are
 *                          never linked: whether one is unlocked is known only on
 *                          the device.
 *  6 strategy_after_misses MISSES_FOR_STRATEGY (3) or more misses on one sub-topic
 *                          in the last 7 days, rule 1 has no lesson left to offer
 *                          for it (none mapped, or already done), and a strategy
 *                          mapped to the sub-topic has never been opened. The
 *                          first such strategy in the map is suggested.
 *  7 mock_exam_soon        Exam within EXAM_SOON_DAYS (30) and no mock in 3 days.
 *    mock_coverage         COVERAGE_FOR_MOCK (half) of the sub-topics have 5+
 *                          attempts and there has been no mock for 7 days.
 *  8 continue_top          Otherwise: keep going with the top-priority sub-topic.
 *    new_start             A child with no attempts at all gets this one action,
 *                          on the top-priority sub-topic (as Today's Plan does).
 *
 * Ties inside a rule break on a rule-specific score, then exam weight, then node
 * id, so the same data always gives the same list.
 *
 * Then, walking that order:
 *   - an action shown on SUPPRESS_SHOWN_DAYS (2) or more earlier days in the last
 *     3 days and never taken is skipped (continue_top / new_start are the floor
 *     and are never skipped);
 *   - at most one action per sub-topic;
 *   - at most one action per piece of content (two sub-topics can share a drill);
 *   - at most one "learn" action (lesson, hands-on, explain, strategy);
 *   - while a mock test is in progress, nothing is recommended at all.
 */

import { prisma } from '@/lib/db';
import { MS_PER_DAY, MS_PER_HOUR } from '@/lib/timeConstants';
import { matchesSubTopicKey } from '@/lib/sharedUtils';
import { getTopicsForGrade } from '@/data/topicTree';
import { getTopicContent } from '@/data/topicContentMap';
import { LESSON_TOPICS } from '@/data/lessonTopics';
import { hasTeachScript } from '@/lib/teach/lookup';

// ── Thresholds ───────────────────────────────────────────────────────────────

export const MISSES_FOR_LESSON = 3;
export const LESSON_PASS_SCORE = 70;
export const IDLE_DAYS = 14;
export const DROP_SIZE = 0.2;
export const FLASHCARDS_DUE_MIN = 10;
export const DRILL_MIN_ATTEMPTS = 8;
export const DRILL_REST_DAYS = 7;
export const MISSES_FOR_STRATEGY = 3;
export const EXAM_SOON_DAYS = 30;
export const COVERAGE_FOR_MOCK = 0.5;
export const SUPPRESS_SHOWN_DAYS = 2;
export const SUPPRESS_WINDOW_DAYS = 3;
/** Fewest answers on a sub-topic before its mastery can make it count as "strong". */
export const STRONG_MIN_ATTEMPTS = 5;
/**
 * Most answers read from the last 21 days. It was 400, which a child answering
 * 20 or more a day fills in under three weeks: a sub-topic practised 12 days
 * ago then fell outside it and was treated as untouched for 21 days.
 */
const RECENT_ATTEMPT_WINDOW = 2000;
export const DEFAULT_LIMIT = 3;

// ── Types ────────────────────────────────────────────────────────────────────

export type NextActionType =
  | 'lesson'
  | 'hands_on'
  | 'explain'
  | 'review'
  | 'flashcards'
  | 'drill'
  | 'strategy'
  | 'mock'
  | 'practice';

export const NEXT_ACTION_TYPES: NextActionType[] = [
  'lesson', 'hands_on', 'explain', 'review', 'flashcards', 'drill', 'strategy', 'mock', 'practice',
];

export const NEXT_ACTION_RULE_IDS: string[] = [
  'lesson_after_misses',
  'explain_missed',
  'review_idle',
  'review_dropped',
  'flashcards_due',
  'drill_close',
  'strategy_after_misses',
  'mock_exam_soon',
  'mock_coverage',
  'continue_top',
  'new_start',
];

export interface NextAction {
  /** Stable identity of the action: ruleId|nodeId|refId. */
  id: string;
  ruleId: string;
  actionType: NextActionType;
  title: string;
  /** One kind sentence a ten-year-old understands. */
  reason: string;
  href: string;
  nodeId?: string;
  refId?: string;
  minutes?: number;
}

/** What is known about one sub-topic (one topic-tree node). */
export interface NodeSignal {
  nodeId: string;
  name: string;
  dbTopicId: string;
  subTopicKey?: string;
  examWeight: number;
  /** Attempts counted by the Brain Engine for this node. */
  attempts: number;
  /** 0–1. */
  accuracy: number;
  /** Brain Engine mastery, 0–1. */
  mastery: number;
  /** Brain Engine priority (higher = practise sooner). 0 when unknown. */
  priority: number;
  /** null when the node has never been attempted. */
  daysSinceLastAttempt: number | null;
  /** Misses in the last 7 days. */
  misses7d: number;
  /** Last 7 days. */
  recentAttempts: number;
  recentCorrect: number;
  /** The two weeks before that (8–21 days ago). */
  priorAttempts: number;
  priorCorrect: number;
  /** A question missed in the last 3 days that has an "Explain it to me" lesson. */
  explainQuestionId?: string;
}

export interface RankInput {
  /** The child's day, as YYYY-MM-DD (see dayKey). */
  today: string;
  nodes: NodeSignal[];
  /** Attempts ever. 0 means a brand-new child. */
  totalAttempts: number;
  /** Concept lesson slug → best quiz score (0–100) over its levels. */
  lessonBest: Record<string, number>;
  /**
   * `${kind}:${refId}` → whole days since that content was finished. A strategy
   * has no finish step, so for `strategy:` it is days since it was first opened.
   */
  contentDone: Record<string, number>;
  /** Flashcards seen before that are due now. */
  flashcardsDue: number;
  /** null when there has been no mock recently (30+ days, or never). */
  daysSinceLastMock: number | null;
  /** null when no exam date is set. */
  daysUntilExam: number | null;
  mockInProgress: boolean;
  /** Recommendations shown lately: one entry per event. */
  history: Array<{ actionId: string; day: string; taken: boolean }>;
  limit?: number;
}

// ── Small pure helpers ───────────────────────────────────────────────────────

/** Identity of an action. The same string is rebuilt from a stored event. */
export function actionKey(ruleId: string, nodeId?: string | null, refId?: string | null): string {
  return `${ruleId}|${nodeId || ''}|${refId || ''}`;
}

/** The day a moment falls on for a child in India (UTC+5:30), as YYYY-MM-DD. */
export function dayKey(d: Date): string {
  return new Date(d.getTime() + 5.5 * MS_PER_HOUR).toISOString().slice(0, 10);
}

/** The first instant (UTC) of the India day that `d` falls on. */
export function dayStart(d: Date): Date {
  return new Date(new Date(`${dayKey(d)}T00:00:00.000Z`).getTime() - 5.5 * MS_PER_HOUR);
}

/**
 * Practice link for a sub-topic. Keyed grades share one DB topic, so the link
 * must carry the sub-topic (same shape as src/app/(app)/chapters/page.tsx).
 * PRIVATE COPY: to be replaced by the shared helper in src/lib/brain/.
 */
function practiceHref(dbTopicId: string, subTopicKey?: string): string {
  const qp = new URLSearchParams();
  if (subTopicKey) qp.set('subTopic', subTopicKey);
  const qs = qp.toString();
  return `/practice/${dbTopicId}${qs ? `?${qs}` : ''}`;
}

/**
 * Where rule 2 sends the child: practice on the sub-topic, opening on the
 * missed question with its "Explain it to me" lesson playing (the practice
 * page reads `teach` and fetches the question from /api/questions/explain).
 * If that question cannot be served, the page falls back to ordinary practice.
 */
function explainHref(dbTopicId: string, subTopicKey: string | undefined, questionId: string): string {
  const qp = new URLSearchParams();
  if (subTopicKey) qp.set('subTopic', subTopicKey);
  qp.set('teach', questionId);
  return `/practice/${dbTopicId}?${qp.toString()}`;
}

function lessonName(slug: string, fallback: string): string {
  for (let i = 0; i < LESSON_TOPICS.length; i++) {
    if (LESSON_TOPICS[i].id === slug) return LESSON_TOPICS[i].topic;
  }
  return fallback;
}

function isLearn(t: NextActionType): boolean {
  return t === 'lesson' || t === 'hands_on' || t === 'explain' || t === 'strategy';
}

function ratio(correct: number, total: number): number {
  return total > 0 ? correct / total : 0;
}

interface Candidate {
  action: NextAction;
  /** Rule order: lower comes first. */
  rank: number;
  /** Within a rule: higher comes first. */
  score: number;
  /** Second tie-break: higher comes first. */
  weight: number;
}

function compareCandidates(a: Candidate, b: Candidate): number {
  if (a.rank !== b.rank) return a.rank - b.rank;
  if (a.score !== b.score) return b.score - a.score;
  if (a.weight !== b.weight) return b.weight - a.weight;
  return a.action.id < b.action.id ? -1 : a.action.id > b.action.id ? 1 : 0;
}

function makeAction(
  ruleId: string,
  actionType: NextActionType,
  title: string,
  reason: string,
  href: string,
  minutes: number,
  nodeId?: string,
  refId?: string,
): NextAction {
  const action: NextAction = {
    id: actionKey(ruleId, nodeId, refId),
    ruleId,
    actionType,
    title,
    reason,
    href,
    minutes,
  };
  if (nodeId) action.nodeId = nodeId;
  if (refId) action.refId = refId;
  return action;
}

/** Action ids shown on enough earlier days, lately, without ever being taken. */
function suppressedIds(input: RankInput): Record<string, boolean> {
  const todayMs = new Date(`${input.today}T00:00:00.000Z`).getTime();
  const earliest = isNaN(todayMs)
    ? ''
    : new Date(todayMs - SUPPRESS_WINDOW_DAYS * MS_PER_DAY).toISOString().slice(0, 10);

  const days: Record<string, Record<string, boolean>> = {};
  const taken: Record<string, boolean> = {};
  for (let i = 0; i < input.history.length; i++) {
    const h = input.history[i];
    if (h.day < earliest || h.day > input.today) continue;
    if (h.taken) taken[h.actionId] = true;
    if (h.day === input.today) continue;
    if (!days[h.actionId]) days[h.actionId] = {};
    days[h.actionId][h.day] = true;
  }

  const out: Record<string, boolean> = {};
  const ids = Object.keys(days);
  for (let i = 0; i < ids.length; i++) {
    const id = ids[i];
    if (!taken[id] && Object.keys(days[id]).length >= SUPPRESS_SHOWN_DAYS) out[id] = true;
  }
  return out;
}

/** Sub-topics in the order the child should keep going with them. */
function byPriority(nodes: NodeSignal[]): NodeSignal[] {
  return nodes.slice().sort((a, b) => {
    if (a.priority !== b.priority) return b.priority - a.priority;
    if (a.examWeight !== b.examWeight) return b.examWeight - a.examWeight;
    return a.nodeId < b.nodeId ? -1 : a.nodeId > b.nodeId ? 1 : 0;
  });
}

// ── The pure ranking ─────────────────────────────────────────────────────────

export function rankNextActions(input: RankInput): NextAction[] {
  // A test in progress is never interrupted.
  if (input.mockInProgress) return [];

  const limit = Math.max(1, Math.min(5, Math.floor(input.limit || DEFAULT_LIMIT)));
  const nodes = input.nodes;

  // A brand-new child: one gentle place to begin.
  // The top-priority sub-topic, the same one Today's Plan puts first, so the
  // card and the plan never name two different places to start.
  if (input.totalAttempts <= 0) {
    const first = nodes.length > 0 ? byPriority(nodes)[0] : null;
    if (!first) {
      return [makeAction(
        'new_start', 'practice', 'Pick your first topic',
        'Choose any topic you like and try a few questions.',
        '/chapters', 5,
      )];
    }
    return [makeAction(
      'new_start', 'practice', `Start with ${first.name}`,
      "Let's try a few questions together so Sparky can find the best next step for you.",
      practiceHref(first.dbTopicId, first.subTopicKey), 5, first.nodeId,
    )];
  }

  const candidates: Candidate[] = [];

  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    const content = getTopicContent(n.nodeId);

    // ── Rule 1: a lesson after repeated misses ──
    let lessonOffered = false;
    if (n.misses7d >= MISSES_FOR_LESSON) {
      let handsOnId: string | null = null;
      const ids = content.handsOnLessonIds || [];
      for (let k = 0; k < ids.length; k++) {
        if (input.contentDone[`hands_on:${ids[k]}`] === undefined) { handsOnId = ids[k]; break; }
      }
      if (handsOnId) {
        lessonOffered = true;
        candidates.push({
          rank: 1, score: n.misses7d, weight: n.examWeight,
          action: makeAction(
            'lesson_after_misses', 'hands_on', `Hands-on lesson: ${n.name}`,
            `You've been close on ${n.name} a few times — doing it with your hands will help it click.`,
            `/learn/hands-on/${handsOnId}`, 5, n.nodeId, handsOnId,
          ),
        });
      } else if (content.lessonSlug) {
        const best = input.lessonBest[content.lessonSlug];
        if (best === undefined || best < LESSON_PASS_SCORE) {
          lessonOffered = true;
          candidates.push({
            rank: 1, score: n.misses7d, weight: n.examWeight,
            action: makeAction(
              'lesson_after_misses', 'lesson', `Short lesson: ${lessonName(content.lessonSlug, n.name)}`,
              `You've been close on ${n.name} a few times — this short lesson will help it click.`,
              `/learn/lessons/${content.lessonSlug}`, 8, n.nodeId, content.lessonSlug,
            ),
          });
        }
      }
    }

    // ── Rule 2: a recent miss that has an "Explain it to me" lesson ──
    if (n.explainQuestionId) {
      candidates.push({
        rank: 2, score: n.misses7d, weight: n.examWeight,
        action: makeAction(
          'explain_missed', 'explain', `Look again at ${n.name}`,
          `One ${n.name} question was tricky lately, so Sparky will show you how it works and then you can try one like it.`,
          explainHref(n.dbTopicId, n.subTopicKey, n.explainQuestionId), 5, n.nodeId, n.explainQuestionId,
        ),
      });
    }

    // ── Rule 3: a strong sub-topic gone quiet, or one that has slipped ──
    // Mastery alone is not enough: one quick right answer already scores about 0.7.
    const wasStrong =
      (n.mastery >= 0.6 && n.attempts >= STRONG_MIN_ATTEMPTS) || (n.attempts >= 8 && n.accuracy >= 0.75);
    const recentAcc = ratio(n.recentCorrect, n.recentAttempts);
    const priorAcc = ratio(n.priorCorrect, n.priorAttempts);
    const drop = priorAcc - recentAcc;
    if (n.priorAttempts >= 5 && n.recentAttempts >= 4 && priorAcc >= 0.75 && drop >= DROP_SIZE) {
      candidates.push({
        rank: 3, score: 100 + drop, weight: n.examWeight,
        action: makeAction(
          'review_dropped', 'review', `Quick review: ${n.name}`,
          `${n.name} felt a little harder this week, so a short review will bring it right back.`,
          practiceHref(n.dbTopicId, n.subTopicKey), 5, n.nodeId,
        ),
      });
    } else if (wasStrong && n.daysSinceLastAttempt !== null && n.daysSinceLastAttempt >= IDLE_DAYS) {
      candidates.push({
        rank: 3, score: n.mastery, weight: n.examWeight,
        action: makeAction(
          'review_idle', 'review', `Quick review: ${n.name}`,
          `You were doing really well on ${n.name}, and a quick review will keep it fresh.`,
          practiceHref(n.dbTopicId, n.subTopicKey), 5, n.nodeId,
        ),
      });
    }

    // ── Rule 5: nearly there, so drill it ──
    if (
      n.attempts >= DRILL_MIN_ATTEMPTS && n.accuracy >= 0.6 && n.accuracy <= 0.8 &&
      content.drillTopicId && content.drillLevelId
    ) {
      const ref = `${content.drillTopicId}:${content.drillLevelId}`;
      const doneDays = input.contentDone[`drill:${ref}`];
      if (doneDays === undefined || doneDays >= DRILL_REST_DAYS) {
        candidates.push({
          rank: 5, score: n.accuracy, weight: n.examWeight,
          action: makeAction(
            'drill_close', 'drill', `Skill drill: ${n.name}`,
            `You're getting close on ${n.name}, and a quick drill will make it even stronger.`,
            `/practice/skill-drill/${content.drillTopicId}/${content.drillLevelId}`, 6, n.nodeId, ref,
          ),
        });
      }
    }

    // ── Rule 6: the misses go on and there is no lesson left to offer, so a trick ──
    if (n.misses7d >= MISSES_FOR_STRATEGY && !lessonOffered) {
      let strategyId: string | null = null;
      const tricks = content.strategyIds || [];
      for (let k = 0; k < tricks.length; k++) {
        if (input.contentDone[`strategy:${tricks[k]}`] === undefined) { strategyId = tricks[k]; break; }
      }
      if (strategyId) {
        candidates.push({
          rank: 6, score: n.misses7d, weight: n.examWeight,
          action: makeAction(
            'strategy_after_misses', 'strategy', `A neat trick for ${n.name}`,
            `Here's a neat trick that can make ${n.name} feel easier.`,
            `/learn/strategies?open=${strategyId}`, 3, n.nodeId, strategyId,
          ),
        });
      }
    }
  }

  // ── Rule 4: flashcards waiting ──
  if (input.flashcardsDue >= FLASHCARDS_DUE_MIN) {
    candidates.push({
      rank: 4, score: 0, weight: 0,
      action: makeAction(
        'flashcards_due', 'flashcards', 'Flashcards are ready',
        `${input.flashcardsDue} cards are ready for a quick look, and it only takes a few minutes.`,
        '/flashcards/session?deck=due&mode=classic', 5,
      ),
    });
  }

  // ── Rule 7: a practice test ──
  let covered = 0;
  for (let i = 0; i < nodes.length; i++) if (nodes[i].attempts >= 5) covered += 1;
  const coverage = nodes.length > 0 ? covered / nodes.length : 0;
  const sinceMock = input.daysSinceLastMock;
  const examSoon = input.daysUntilExam !== null && input.daysUntilExam >= 0 && input.daysUntilExam <= EXAM_SOON_DAYS;
  if (examSoon && (sinceMock === null || sinceMock >= 3)) {
    candidates.push({
      rank: 7, score: 0, weight: 0,
      action: makeAction(
        'mock_exam_soon', 'mock', 'Try a practice test',
        'Your exam is getting closer, and a practice test shows you just what to expect.',
        '/test', 20,
      ),
    });
  } else if (coverage >= COVERAGE_FOR_MOCK && (sinceMock === null || sinceMock >= 7)) {
    candidates.push({
      rank: 7, score: 0, weight: 0,
      action: makeAction(
        'mock_coverage', 'mock', 'Try a practice test',
        "You've explored lots of topics, so a practice test is a fun way to use them all together.",
        '/test', 20,
      ),
    });
  }

  candidates.sort(compareCandidates);

  // ── Choose ──
  const suppressed = suppressedIds(input);
  const usedNodes: Record<string, boolean> = {};
  const usedContent: Record<string, boolean> = {};
  const out: NextAction[] = [];
  let learnUsed = false;

  for (let i = 0; i < candidates.length && out.length < limit; i++) {
    const a = candidates[i].action;
    if (suppressed[a.id]) continue;
    if (a.nodeId && usedNodes[a.nodeId]) continue;
    // Two sub-topics can share one drill (or lesson): offer it once.
    const contentKey = a.refId ? `${a.actionType}:${a.refId}` : '';
    if (contentKey && usedContent[contentKey]) continue;
    if (isLearn(a.actionType)) {
      if (learnUsed) continue;
      learnUsed = true;
    }
    if (a.nodeId) usedNodes[a.nodeId] = true;
    if (contentKey) usedContent[contentKey] = true;
    out.push(a);
  }

  // ── Rule 8: keep going with the top-priority sub-topic (never suppressed) ──
  if (out.length < limit) {
    const ordered = byPriority(nodes);
    for (let i = 0; i < ordered.length; i++) {
      const n = ordered[i];
      if (usedNodes[n.nodeId]) continue;
      out.push(makeAction(
        'continue_top', 'practice', `Keep going with ${n.name}`,
        `${n.name} is a great one to practise next, and a few questions today will help it grow.`,
        practiceHref(n.dbTopicId, n.subTopicKey), 8, n.nodeId,
      ));
      break;
    }
  }

  return out;
}

// ── Reading stored analytics ─────────────────────────────────────────────────

/** One entry of StudentAnalytics.topicMastery, as far as this module needs it. */
export interface MasterySnapshot {
  nodeId: string;
  mastery: number;
  accuracy: number;
  recency: number;
  attempts: number;
}

function num(v: unknown, fallback: number): number {
  return typeof v === 'number' && isFinite(v) ? v : fallback;
}

/** StudentAnalytics.topicMastery (JSON) → plain entries. Unknown shapes are skipped. */
export function parseMasteryJson(raw: unknown): MasterySnapshot[] {
  if (!Array.isArray(raw)) return [];
  const out: MasterySnapshot[] = [];
  for (let i = 0; i < raw.length; i++) {
    const e = raw[i] as Record<string, unknown> | null;
    if (!e || typeof e !== 'object') continue;
    const id = e.topicId;
    if (typeof id !== 'string') continue;
    out.push({
      nodeId: id,
      mastery: num(e.mastery, 0),
      accuracy: num(e.accuracy, 0),
      recency: num(e.recency, 0),
      attempts: num(e.attemptsCount, 0),
    });
  }
  return out;
}

/** The stored mastery (0–1) of one node, or null when it is not known. */
export function masteryOfNode(raw: unknown, nodeId: string): number | null {
  const entries = parseMasteryJson(raw);
  for (let i = 0; i < entries.length; i++) {
    if (entries[i].nodeId === nodeId) return entries[i].mastery;
  }
  return null;
}

function parsePriorityJson(raw: unknown): Record<string, number> {
  const out: Record<string, number> = {};
  if (!Array.isArray(raw)) return out;
  for (let i = 0; i < raw.length; i++) {
    const e = raw[i] as Record<string, unknown> | null;
    if (!e || typeof e !== 'object') continue;
    const id = e.topicId;
    if (typeof id !== 'string') continue;
    out[id] = num(e.priority, 0);
  }
  return out;
}

// ── The loader ───────────────────────────────────────────────────────────────

/**
 * The next best actions for one child, best first.
 * Nine small reads in one round; no writes. Throws if the database does.
 */
export async function getNextActions(
  studentId: string,
  opts?: { limit?: number },
): Promise<NextAction[]> {
  const now = new Date();
  const nowMs = now.getTime();
  const since21 = new Date(nowMs - 21 * MS_PER_DAY);
  const since30 = new Date(nowMs - 30 * MS_PER_DAY);
  const sinceHistory = new Date(nowMs - (SUPPRESS_WINDOW_DAYS + 1) * MS_PER_DAY);

  const [student, analytics, attempts, lessons, views, flashcardsDue, mocks, events] = await Promise.all([
    prisma.student.findUnique({
      where: { id: studentId },
      select: { grade: true, examDate: true },
    }),
    prisma.studentAnalytics.findUnique({
      where: { studentId },
      select: { topicMastery: true, topicPriorities: true, lastComputedAt: true },
    }),
    prisma.attempt.findMany({
      where: { studentId, createdAt: { gte: since21 } },
      select: {
        questionId: true,
        isCorrect: true,
        createdAt: true,
        question: { select: { topicId: true, subTopic: true } },
      },
      orderBy: { createdAt: 'desc' },
      take: RECENT_ATTEMPT_WINDOW,
    }),
    prisma.lessonProgress.findMany({
      where: { studentId },
      select: { topicSlug: true, quizScore: true },
      take: 200,
    }),
    // Finished content, plus every strategy opened (a strategy is never "finished").
    prisma.contentView.findMany({
      where: { studentId, OR: [{ completedAt: { not: null } }, { kind: 'strategy' }] },
      select: { kind: true, refId: true, startedAt: true, completedAt: true },
      orderBy: { completedAt: 'desc' },
      take: 200,
    }),
    prisma.flashcardProgress.count({
      where: { studentId, timesSeen: { gt: 0 }, nextReviewAt: { lte: now } },
    }),
    prisma.mockTest.findMany({
      where: { studentId, startedAt: { gte: since30 } },
      select: { status: true, startedAt: true, timeLimitMs: true },
      orderBy: { startedAt: 'desc' },
      take: 10,
    }),
    prisma.recommendationEvent.findMany({
      where: { studentId, shownAt: { gte: sinceHistory } },
      select: { ruleId: true, nodeId: true, refId: true, shownAt: true, takenAt: true },
      orderBy: { shownAt: 'desc' },
      take: 200,
    }),
  ]);

  if (!student) return [];

  // ── Mock tests ──
  let mockInProgress = false;
  let daysSinceLastMock: number | null = null;
  for (let i = 0; i < mocks.length; i++) {
    const m = mocks[i];
    const startedMs = new Date(m.startedAt).getTime();
    // A test left open long after its time ran out no longer counts as in progress.
    if (m.status === 'in_progress' && nowMs < startedMs + m.timeLimitMs + 10 * 60_000) mockInProgress = true;
    if (daysSinceLastMock === null) daysSinceLastMock = Math.floor((nowMs - startedMs) / MS_PER_DAY);
  }
  if (mockInProgress) return [];

  // ── Stored analytics ──
  const masteryList = parseMasteryJson(analytics ? analytics.topicMastery : null);
  const masteryById: Record<string, MasterySnapshot> = {};
  let engineAttempts = 0;
  for (let i = 0; i < masteryList.length; i++) {
    masteryById[masteryList[i].nodeId] = masteryList[i];
    engineAttempts += masteryList[i].attempts;
  }
  const priorityById = parsePriorityJson(analytics ? analytics.topicPriorities : null);
  const staleDays = analytics ? Math.max(0, (nowMs - new Date(analytics.lastComputedAt).getTime()) / MS_PER_DAY) : 0;

  // ── Per sub-topic signals ──
  const since7 = nowMs - 7 * MS_PER_DAY;
  const since3 = nowMs - 3 * MS_PER_DAY;
  const tree = getTopicsForGrade(student.grade);
  const nodes: NodeSignal[] = [];

  for (let t = 0; t < tree.length; t++) {
    const node = tree[t];
    const snap = masteryById[node.id];

    let windowCount = 0;
    let windowCorrect = 0;
    let misses7d = 0;
    let recentAttempts = 0;
    let recentCorrect = 0;
    let priorAttempts = 0;
    let priorCorrect = 0;
    let latestMs: number | null = null;
    let explainQuestionId: string | undefined;
    const answeredRight: Record<string, boolean> = {};

    // Newest first, so a later correct answer is seen before the miss it follows.
    for (let i = 0; i < attempts.length; i++) {
      const a = attempts[i];
      if (a.question.topicId !== node.dbTopicId) continue;
      if (node.subTopicKey && !matchesSubTopicKey(a.question.subTopic, node.subTopicKey)) continue;

      const ms = new Date(a.createdAt).getTime();
      if (latestMs === null) latestMs = ms;
      windowCount += 1;
      if (a.isCorrect) windowCorrect += 1;

      if (ms >= since7) {
        recentAttempts += 1;
        if (a.isCorrect) recentCorrect += 1; else misses7d += 1;
      } else {
        priorAttempts += 1;
        if (a.isCorrect) priorCorrect += 1;
      }

      if (a.isCorrect) {
        answeredRight[a.questionId] = true;
      } else if (
        !explainQuestionId && ms >= since3 && !answeredRight[a.questionId] && hasTeachScript(a.questionId)
      ) {
        explainQuestionId = a.questionId;
      }
    }

    let daysSinceLastAttempt: number | null = null;
    if (latestMs !== null) {
      daysSinceLastAttempt = Math.floor((nowMs - latestMs) / MS_PER_DAY);
    } else if (snap && snap.attempts > 0) {
      // Nothing in the last 21 days: fall back on the engine's recency (1 → 0 over 30 days).
      daysSinceLastAttempt = Math.max(21, Math.round((1 - snap.recency) * 30 + staleDays));
    }

    const signal: NodeSignal = {
      nodeId: node.id,
      name: node.name,
      dbTopicId: node.dbTopicId,
      examWeight: node.examWeight,
      attempts: snap ? Math.max(snap.attempts, windowCount) : windowCount,
      accuracy: snap && snap.attempts > 0 ? snap.accuracy : ratio(windowCorrect, windowCount),
      mastery: snap ? snap.mastery : 0,
      priority: priorityById[node.id] || 0,
      daysSinceLastAttempt,
      misses7d,
      recentAttempts,
      recentCorrect,
      priorAttempts,
      priorCorrect,
    };
    if (node.subTopicKey) signal.subTopicKey = node.subTopicKey;
    if (explainQuestionId) signal.explainQuestionId = explainQuestionId;
    nodes.push(signal);
  }

  // ── Lessons and other content already done ──
  const lessonBest: Record<string, number> = {};
  for (let i = 0; i < lessons.length; i++) {
    const l = lessons[i];
    if (lessonBest[l.topicSlug] === undefined || l.quizScore > lessonBest[l.topicSlug]) {
      lessonBest[l.topicSlug] = l.quizScore;
    }
  }

  const contentDone: Record<string, number> = {};
  for (let i = 0; i < views.length; i++) {
    const v = views[i];
    const at = v.completedAt || (v.kind === 'strategy' ? v.startedAt : null);
    if (!at) continue;
    const key = `${v.kind}:${v.refId}`;
    const days = Math.max(0, Math.floor((nowMs - new Date(at).getTime()) / MS_PER_DAY));
    if (contentDone[key] === undefined || days < contentDone[key]) contentDone[key] = days;
  }

  // ── What was shown lately ──
  const history: RankInput['history'] = [];
  for (let i = 0; i < events.length; i++) {
    const e = events[i];
    history.push({
      actionId: actionKey(e.ruleId, e.nodeId, e.refId),
      day: dayKey(new Date(e.shownAt)),
      taken: e.takenAt !== null,
    });
  }

  const daysUntilExam = student.examDate
    ? Math.ceil((new Date(student.examDate).getTime() - nowMs) / MS_PER_DAY)
    : null;

  return rankNextActions({
    today: dayKey(now),
    nodes,
    totalAttempts: Math.max(attempts.length, engineAttempts),
    lessonBest,
    contentDone,
    flashcardsDue,
    daysSinceLastMock,
    daysUntilExam,
    mockInProgress: false,
    history,
    limit: opts && opts.limit ? opts.limit : DEFAULT_LIMIT,
  });
}
