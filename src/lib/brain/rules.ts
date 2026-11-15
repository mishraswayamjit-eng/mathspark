// Pure rules of the Brain Engine: no database, no clock of their own.
//
// `engine.ts` gathers the facts (attempts, mastery, mock tests) and calls
// these; the Home nudge strip calls `pickTopNudge` in the browser. Everything
// here is deterministic so it can be unit-tested without a database.

import { MS_PER_DAY, MS_PER_HOUR } from '@/lib/timeConstants';
import { matchesSubTopicKey } from '@/lib/sharedUtils';
import { practiceUrlForNodeId } from './practiceUrl';
import type { Nudge, NudgeKind, TopicMasteryEntry } from './engine';

// ── Speed ─────────────────────────────────────────────────────────────────────

/** A question that takes this long (or longer) scores 0 for speed. */
const SPEED_CEILING_MS = 90_000;
/** Speed when no time was ever recorded: neither fast nor slow. */
export const SPEED_UNKNOWN = 0.5;

/**
 * The speed part of mastery, 0–1, from the time taken on each attempt.
 * A stored time of 0 (every attempt made before the practice page started
 * sending the time) means "not recorded", NOT "instant": those attempts are
 * left out, and with no recorded time at all the result is the neutral 0.5.
 */
export function speedScore(timesMs: number[]): number {
  let sum = 0;
  let known = 0;
  for (let i = 0; i < timesMs.length; i++) {
    const ms = timesMs[i];
    if (typeof ms === 'number' && ms > 0) {
      sum += ms;
      known += 1;
    }
  }
  if (known === 0) return SPEED_UNKNOWN;
  return Math.min(1, Math.max(0, 1 - sum / known / SPEED_CEILING_MS));
}

// ── Streak ────────────────────────────────────────────────────────────────────

/**
 * How many days in a row the child practised, ending YESTERDAY. `computeStreak`
 * (sharedUtils) counts back from today, so it is 0 until today's first answer;
 * this is the run that is still open for today. Same day boundaries as
 * `computeStreak` (the server's local date).
 */
export function streakBeforeToday(
  attempts: Array<{ createdAt: Date }>,
  now: Date = new Date(),
): number {
  const days: Record<string, boolean> = {};
  for (let i = 0; i < attempts.length; i++) {
    days[new Date(attempts[i].createdAt).toDateString()] = true;
  }
  let streak = 0;
  for (let back = 1; back <= 365; back++) {
    const d = new Date(now);
    d.setDate(d.getDate() - back);
    if (days[d.toDateString()]) streak++;
    else break;
  }
  return streak;
}

// ── Accuracy drop, per topic-tree node ────────────────────────────────────────

interface DropNode {
  id: string;
  dbTopicId: string;
  subTopicKey?: string;
}

interface DropAttempt {
  isCorrect: boolean;
  createdAt: Date;
  question: { topicId: string; subTopic: string | null };
}

/** Fewest answers in each week before the two weeks are compared. */
const DROP_MIN_ATTEMPTS = 5;
/** How far accuracy must fall (0–1) to count. */
const DROP_THRESHOLD = 0.15;

/**
 * Nodes whose accuracy this week is clearly below last week's. Each node only
 * counts its OWN questions: for keyed grades that means the sub-topic, not the
 * whole grade. Returned in the order of `nodes`.
 */
export function findAccuracyDropNodeIds(
  nodes: DropNode[],
  attempts: DropAttempt[],
  now: Date = new Date(),
): string[] {
  const oneWeekAgo = now.getTime() - 7 * MS_PER_DAY;
  const twoWeeksAgo = now.getTime() - 14 * MS_PER_DAY;
  const out: string[] = [];

  for (let n = 0; n < nodes.length; n++) {
    const node = nodes[n];
    let recent = 0;
    let recentRight = 0;
    let prior = 0;
    let priorRight = 0;

    for (let i = 0; i < attempts.length; i++) {
      const a = attempts[i];
      if (a.question.topicId !== node.dbTopicId) continue;
      if (node.subTopicKey && !matchesSubTopicKey(a.question.subTopic, node.subTopicKey)) continue;
      const at = new Date(a.createdAt).getTime();
      if (at < twoWeeksAgo) continue;
      if (at >= oneWeekAgo) {
        recent += 1;
        if (a.isCorrect) recentRight += 1;
      } else {
        prior += 1;
        if (a.isCorrect) priorRight += 1;
      }
    }

    if (recent >= DROP_MIN_ATTEMPTS && prior >= DROP_MIN_ATTEMPTS) {
      if (priorRight / prior - recentRight / recent > DROP_THRESHOLD) out.push(node.id);
    }
  }
  return out;
}

// ── Nudges ────────────────────────────────────────────────────────────────────

/**
 * The one place that says which nudge wins. Only ONE nudge is ever on screen;
 * a higher number is shown first. Celebrate first, then today's small
 * invitation, then topic help, then test reminders.
 */
export const NUDGE_PRIORITY: Record<NudgeKind, number> = {
  streak_milestone: 70,
  streak_keep:      60,
  accuracy_drop:    50,
  exam_mock:        40,
  idle_topic:       30,
  explore_topic:    20,
  weekend_mock:     10,
};

/** Streak lengths worth a cheer. */
export const STREAK_MILESTONE_DAYS: number[] = [7, 14, 21, 30, 50, 100];

/** How many nudges are stored (the strip still shows only one). */
const MAX_STORED_NUDGES = 3;
/** A topic counts as "a while ago" after this many days. */
const IDLE_AFTER_DAYS = 14;
/** No practice-test reminder when one was taken this recently. */
const MOCK_QUIET_DAYS = 7;
/** Topic nudges are dropped this long after they were worked out. */
const TOPIC_NUDGE_LIFE_DAYS = 3;
/** From this hour (India time) the "keep it going" invitation may show. */
const EVENING_HOUR_IST = 18;

const IST_OFFSET_MS = 5.5 * MS_PER_HOUR;

/** The moment the current India-time day ends. */
export function endOfIstDay(now: Date): Date {
  const istMs = now.getTime() + IST_OFFSET_MS;
  const startOfIstDay = Math.floor(istMs / MS_PER_DAY) * MS_PER_DAY;
  return new Date(startOfIstDay + MS_PER_DAY - IST_OFFSET_MS);
}

export interface NudgeFacts {
  now: Date;
  /** Per-node mastery for the child's grade, weakest first. */
  masteries: TopicMasteryEntry[];
  /** The node the plan puts first (a topic-tree node id), if any. */
  topPriorityNodeId: string | null;
  /** `computeStreak`: days in a row INCLUDING today (0 until today's first answer). */
  streakToday: number;
  /** `streakBeforeToday`: days in a row ending yesterday. */
  streakBeforeToday: number;
  /** Node ids from `findAccuracyDropNodeIds`. */
  accuracyDropNodeIds: string[];
  /** Whole days until the exam; null when no date is set. */
  daysUntilExam: number | null;
  /** Days since the last practice test was started; null when none was ever taken. */
  daysSinceMock: number | null;
}

function idleDays(entry: TopicMasteryEntry): number {
  return Math.round((1 - entry.recency) * 30);
}

/**
 * Work out today's nudges from facts the engine has already gathered.
 * Seven old rules became seven kinds, reworded for a ten-year-old: an
 * invitation, never a warning. The two practice-test reminders (exam coming,
 * weekend) never show together and stay quiet for a week after a test.
 * Returns at most three, highest priority first.
 */
export function buildNudges(facts: NudgeFacts): Nudge[] {
  const { now, masteries } = facts;
  const nudges: Nudge[] = [];

  const today = endOfIstDay(now).toISOString();
  const fewDays = new Date(now.getTime() + TOPIC_NUDGE_LIFE_DAYS * MS_PER_DAY).toISOString();
  const ist = new Date(now.getTime() + IST_OFFSET_MS);
  const hourIst = ist.getUTCHours();
  const weekdayIst = ist.getUTCDay();

  const practisedToday = facts.streakToday > 0;
  let hasPractised = false;
  for (let i = 0; i < masteries.length; i++) {
    if (masteries[i].attemptsCount > 0) { hasPractised = true; break; }
  }
  const mockIsDue = facts.daysSinceMock === null || facts.daysSinceMock > MOCK_QUIET_DAYS;
  const usedNodeIds: string[] = [];

  // 1. A streak milestone reached today: celebrate.
  if (STREAK_MILESTONE_DAYS.indexOf(facts.streakToday) !== -1) {
    nudges.push({
      id: `nudge_streak_${facts.streakToday}`,
      kind: 'streak_milestone',
      message: `${facts.streakToday} days in a row! That's brilliant. Well done!`,
      sparkyEmotion: 'celebrating',
      actionUrl: '/progress',
      actionLabel: 'See my progress',
      priority: NUDGE_PRIORITY.streak_milestone,
      expiresAt: today,
    });
  }

  // 2. Evening, a run of days behind them, nothing yet today: a small invitation.
  if (hourIst >= EVENING_HOUR_IST && !practisedToday && facts.streakBeforeToday >= 2) {
    nudges.push({
      id: 'nudge_streak',
      kind: 'streak_keep',
      message: `You've practised ${facts.streakBeforeToday} days in a row! Fancy a quick round today?`,
      sparkyEmotion: 'encouraging',
      actionUrl: practiceUrlForNodeId(facts.topPriorityNodeId) ?? '/chapters',
      actionLabel: 'Quick round',
      priority: NUDGE_PRIORITY.streak_keep,
      expiresAt: today,
    });
  }

  // 3. One topic that went less well this week than last.
  for (let i = 0; i < facts.accuracyDropNodeIds.length; i++) {
    const nodeId = facts.accuracyDropNodeIds[i];
    const url = practiceUrlForNodeId(nodeId);
    let entry: TopicMasteryEntry | null = null;
    for (let j = 0; j < masteries.length; j++) {
      if (masteries[j].topicId === nodeId) { entry = masteries[j]; break; }
    }
    if (!url || !entry) continue;
    nudges.push({
      id: `nudge_drop_${nodeId}`,
      kind: 'accuracy_drop',
      message: `${entry.topicName} felt a bit tricky this week. Shall we try a few together?`,
      sparkyEmotion: 'thinking',
      actionUrl: url,
      actionLabel: "Let's try",
      priority: NUDGE_PRIORITY.accuracy_drop,
      expiresAt: fewDays,
    });
    usedNodeIds.push(nodeId);
    break;
  }

  // 4. Exam within a month (but not tomorrow) and no practice test lately.
  const examSoon =
    facts.daysUntilExam !== null && facts.daysUntilExam >= 2 && facts.daysUntilExam <= 30;
  if (examSoon && hasPractised && mockIsDue) {
    nudges.push({
      id: 'nudge_exam',
      kind: 'exam_mock',
      message: `Your exam is ${facts.daysUntilExam} days away. A practice test is a great way to get ready!`,
      sparkyEmotion: 'encouraging',
      actionUrl: '/test',
      actionLabel: 'Try a practice test',
      priority: NUDGE_PRIORITY.exam_mock,
      expiresAt: today,
    });
  }

  // 5. A topic not visited for a while.
  for (let i = 0; i < masteries.length; i++) {
    const t = masteries[i];
    if (t.attemptsCount <= 0 || idleDays(t) <= IDLE_AFTER_DAYS) continue;
    if (usedNodeIds.indexOf(t.topicId) !== -1) continue;
    const url = practiceUrlForNodeId(t.topicId);
    if (!url) continue;
    nudges.push({
      id: `nudge_idle_${t.topicId}`,
      kind: 'idle_topic',
      message: `It's been a while since ${t.topicName}. Want a quick refresher?`,
      sparkyEmotion: 'happy',
      actionUrl: url,
      actionLabel: 'Quick refresher',
      priority: NUDGE_PRIORITY.idle_topic,
      expiresAt: fewDays,
    });
    usedNodeIds.push(t.topicId);
    break;
  }

  // 6. A topic only just started.
  for (let i = 0; i < masteries.length; i++) {
    const t = masteries[i];
    if (t.attemptsCount <= 0 || t.coverage >= 0.3) continue;
    if (usedNodeIds.indexOf(t.topicId) !== -1) continue;
    const url = practiceUrlForNodeId(t.topicId);
    if (!url) continue;
    nudges.push({
      id: `nudge_explore_${t.topicId}`,
      kind: 'explore_topic',
      message: `You've made a start on ${t.topicName}. Want to see what else is in there?`,
      sparkyEmotion: 'happy',
      actionUrl: url,
      actionLabel: 'Explore',
      priority: NUDGE_PRIORITY.explore_topic,
      expiresAt: fewDays,
    });
    usedNodeIds.push(t.topicId);
    break;
  }

  // 7. Weekend, with no exam reminder already saying the same thing.
  const isWeekend = weekdayIst === 0 || weekdayIst === 6;
  if (isWeekend && hasPractised && mockIsDue && !examSoon) {
    nudges.push({
      id: 'nudge_weekend',
      kind: 'weekend_mock',
      message: "It's the weekend! Got time for a practice test?",
      sparkyEmotion: 'happy',
      actionUrl: '/test',
      actionLabel: 'Try a practice test',
      priority: NUDGE_PRIORITY.weekend_mock,
      expiresAt: today,
    });
  }

  return nudges.sort((a, b) => b.priority - a.priority).slice(0, MAX_STORED_NUDGES);
}

// ── Choosing the one nudge to show ────────────────────────────────────────────

/**
 * Is this stored value a nudge the strip may show? Stored analytics are JSON,
 * so nothing is taken on trust. Rows written before nudges had a `kind` (old
 * wording, whole-grade links) are not shown.
 */
export function isRenderableNudge(value: unknown): value is Nudge {
  if (!value || typeof value !== 'object') return false;
  const n = value as Record<string, unknown>;
  const id = n.id;
  const message = n.message;
  const actionLabel = n.actionLabel;
  const actionUrl = n.actionUrl;
  const kind = n.kind;
  if (typeof id !== 'string' || !id) return false;
  if (typeof message !== 'string' || !message) return false;
  if (typeof actionLabel !== 'string' || !actionLabel) return false;
  if (typeof actionUrl !== 'string' || actionUrl.charAt(0) !== '/') return false;
  if (typeof kind !== 'string') return false;
  return Object.prototype.hasOwnProperty.call(NUDGE_PRIORITY, kind);
}

export interface PickNudgeOptions {
  /** Defaults to the current time. */
  now?: Date;
  /** Ids the child has put away today. */
  dismissedIds?: string[];
  /** True once the child has finished a lesson today on this device. */
  practisedToday?: boolean;
}

/**
 * The single nudge to show, or null. Order comes from `NUDGE_PRIORITY`, never
 * from the order of the list. Left out: anything dismissed today, anything
 * past its `expiresAt`, and the "keep it going" invitation once the child has
 * already practised today.
 */
export function pickTopNudge(nudges: unknown, options: PickNudgeOptions = {}): Nudge | null {
  if (!Array.isArray(nudges)) return null;
  const nowMs = (options.now ?? new Date()).getTime();
  const dismissed = options.dismissedIds ?? [];

  let best: Nudge | null = null;
  let bestRank = -1;
  for (let i = 0; i < nudges.length; i++) {
    const n: unknown = nudges[i];
    if (!isRenderableNudge(n) || !n.kind) continue;
    if (dismissed.indexOf(n.id) !== -1) continue;
    if (typeof n.expiresAt === 'string') {
      const until = Date.parse(n.expiresAt);
      if (!isNaN(until) && until <= nowMs) continue;
    }
    if (options.practisedToday && n.kind === 'streak_keep') continue;
    const rank = NUDGE_PRIORITY[n.kind];
    if (rank > bestRank) {
      best = n;
      bestRank = rank;
    }
  }
  return best;
}
