import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';
import { logError } from '@/lib/logger';
import { matchesSubTopicKey } from '@/lib/sharedUtils';
import { TOPIC_TREE, type TopicNode } from '@/data/topicTree';

export const dynamic = 'force-dynamic';

const NO_STORE = { 'Cache-Control': 'private, no-store' };
const MS_PER_DAY = 86_400_000;
const WINDOW_DAYS = 7;
/** Fewest answers needed on each side of the moment for a change to count. */
const MIN_ATTEMPTS_EACH_SIDE = 3;
const MAX_EVENTS = 5000;
const MAX_ATTEMPTS = 50000;

interface RuleTotals {
  shown: number;
  taken: number;
  completed: number;
  masteryBeforeSum: number;
  masteryBeforeCount: number;
  changeTakenSum: number;
  changeTakenCount: number;
  changeNotTakenSum: number;
  changeNotTakenCount: number;
}

interface AttemptRow {
  ms: number;
  isCorrect: boolean;
  topicId: string;
  subTopic: string;
}

function emptyTotals(): RuleTotals {
  return {
    shown: 0, taken: 0, completed: 0,
    masteryBeforeSum: 0, masteryBeforeCount: 0,
    changeTakenSum: 0, changeTakenCount: 0,
    changeNotTakenSum: 0, changeNotTakenCount: 0,
  };
}

function round(v: number, places: number): number {
  const f = Math.pow(10, places);
  return Math.round(v * f) / f;
}

/**
 * Accuracy on one sub-topic in the 7 days after a moment, minus the 7 days
 * before it. null when either side has too few answers to say anything.
 */
function accuracyChange(rows: AttemptRow[], node: TopicNode, anchorMs: number): number | null {
  let beforeN = 0;
  let beforeRight = 0;
  let afterN = 0;
  let afterRight = 0;
  const from = anchorMs - WINDOW_DAYS * MS_PER_DAY;
  const to = anchorMs + WINDOW_DAYS * MS_PER_DAY;
  for (let i = 0; i < rows.length; i++) {
    const r = rows[i];
    if (r.ms < from || r.ms > to) continue;
    if (r.topicId !== node.dbTopicId) continue;
    if (node.subTopicKey && !matchesSubTopicKey(r.subTopic, node.subTopicKey)) continue;
    if (r.ms <= anchorMs) {
      beforeN += 1;
      if (r.isCorrect) beforeRight += 1;
    } else {
      afterN += 1;
      if (r.isCorrect) afterRight += 1;
    }
  }
  if (beforeN < MIN_ATTEMPTS_EACH_SIDE || afterN < MIN_ATTEMPTS_EACH_SIDE) return null;
  return afterRight / afterN - beforeRight / beforeN;
}

/**
 * GET /api/recommendations/review?secret=SEED_SECRET&days=30
 *
 * Owner review of the next-best-action rules. Totals per rule only: no child
 * names, no child ids. Worked out on demand from RecommendationEvent and Attempt.
 *
 * Per rule:
 *   shown, taken, completed
 *   takeUpRate       taken / shown
 *   completionRate   completed / taken (content actions only can complete)
 *   meanMasteryBefore  mean stored Brain Engine mastery when the row was written
 *   changeTaken / changeNotTaken
 *     Mean change on the recommended sub-topic over the 7 days after the child
 *     took the action (or, for the comparison group, after it was shown and not
 *     taken), against the 7 days before. Mastery history is not stored, so the
 *     change is measured as answer ACCURACY on that sub-topic (-1 to 1), from the
 *     Attempt table. Only events at least 7 days old with 3+ answers on each
 *     side are counted; `n` says how many that was.
 *
 * This compares children who chose to take an action with those who did not,
 * so it shows association, not proof that an action helps.
 */
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: NO_STORE });
  }

  const daysParam = parseInt(searchParams.get('days') || '30', 10);
  const days = isNaN(daysParam) ? 30 : Math.max(1, Math.min(90, daysParam));

  try {
    const nowMs = Date.now();
    const since = new Date(nowMs - days * MS_PER_DAY);

    const events = await prisma.recommendationEvent.findMany({
      where: { shownAt: { gte: since } },
      select: {
        studentId: true,
        ruleId: true,
        nodeId: true,
        shownAt: true,
        takenAt: true,
        completedAt: true,
        masteryBefore: true,
      },
      orderBy: { shownAt: 'desc' },
      take: MAX_EVENTS,
    });

    const nodeById: Record<string, TopicNode> = {};
    for (let i = 0; i < TOPIC_TREE.length; i++) nodeById[TOPIC_TREE[i].id] = TOPIC_TREE[i];

    // Events old enough to have a full 7 days after them, on a known sub-topic.
    const studentSeen: Record<string, boolean> = {};
    const studentIds: string[] = [];
    let earliestAnchor = nowMs;
    for (let i = 0; i < events.length; i++) {
      const e = events[i];
      if (!e.nodeId || !nodeById[e.nodeId]) continue;
      const anchor = new Date(e.takenAt || e.shownAt).getTime();
      if (anchor + WINDOW_DAYS * MS_PER_DAY > nowMs) continue;
      if (anchor < earliestAnchor) earliestAnchor = anchor;
      if (!studentSeen[e.studentId]) {
        studentSeen[e.studentId] = true;
        studentIds.push(e.studentId);
      }
    }

    const attemptsByStudent: Record<string, AttemptRow[]> = {};
    let attemptsCapped = false;
    if (studentIds.length > 0) {
      const attempts = await prisma.attempt.findMany({
        where: {
          studentId: { in: studentIds },
          createdAt: { gte: new Date(earliestAnchor - WINDOW_DAYS * MS_PER_DAY) },
        },
        select: {
          studentId: true,
          isCorrect: true,
          createdAt: true,
          question: { select: { topicId: true, subTopic: true } },
        },
        orderBy: { createdAt: 'desc' },
        take: MAX_ATTEMPTS,
      });
      attemptsCapped = attempts.length >= MAX_ATTEMPTS;
      for (let i = 0; i < attempts.length; i++) {
        const a = attempts[i];
        if (!attemptsByStudent[a.studentId]) attemptsByStudent[a.studentId] = [];
        attemptsByStudent[a.studentId].push({
          ms: new Date(a.createdAt).getTime(),
          isCorrect: a.isCorrect,
          topicId: a.question.topicId,
          subTopic: a.question.subTopic,
        });
      }
    }

    const totals: Record<string, RuleTotals> = {};
    for (let i = 0; i < events.length; i++) {
      const e = events[i];
      if (!totals[e.ruleId]) totals[e.ruleId] = emptyTotals();
      const t = totals[e.ruleId];

      t.shown += 1;
      if (e.takenAt) t.taken += 1;
      if (e.completedAt) t.completed += 1;
      if (typeof e.masteryBefore === 'number') {
        t.masteryBeforeSum += e.masteryBefore;
        t.masteryBeforeCount += 1;
      }

      const node = e.nodeId ? nodeById[e.nodeId] : undefined;
      if (!node) continue;
      const anchor = new Date(e.takenAt || e.shownAt).getTime();
      if (anchor + WINDOW_DAYS * MS_PER_DAY > nowMs) continue;
      const change = accuracyChange(attemptsByStudent[e.studentId] || [], node, anchor);
      if (change === null) continue;
      if (e.takenAt) {
        t.changeTakenSum += change;
        t.changeTakenCount += 1;
      } else {
        t.changeNotTakenSum += change;
        t.changeNotTakenCount += 1;
      }
    }

    const rules = Object.keys(totals).sort().map((ruleId) => {
      const t = totals[ruleId];
      return {
        ruleId,
        shown: t.shown,
        taken: t.taken,
        completed: t.completed,
        takeUpRate: t.shown > 0 ? round(t.taken / t.shown, 3) : null,
        completionRate: t.taken > 0 ? round(t.completed / t.taken, 3) : null,
        meanMasteryBefore: t.masteryBeforeCount > 0 ? round(t.masteryBeforeSum / t.masteryBeforeCount, 3) : null,
        changeTaken: {
          mean: t.changeTakenCount > 0 ? round(t.changeTakenSum / t.changeTakenCount, 3) : null,
          n: t.changeTakenCount,
        },
        changeNotTaken: {
          mean: t.changeNotTakenCount > 0 ? round(t.changeNotTakenSum / t.changeNotTakenCount, 3) : null,
          n: t.changeNotTakenCount,
        },
      };
    });

    return NextResponse.json({
      days,
      events: events.length,
      eventsCapped: events.length >= MAX_EVENTS,
      attemptsCapped,
      measure: 'change = accuracy on the sub-topic in the 7 days after, minus the 7 days before (-1 to 1)',
      rules,
    }, { headers: NO_STORE });
  } catch (err) {
    logError('[recommendations/review GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500, headers: NO_STORE });
  }
}
