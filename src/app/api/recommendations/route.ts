import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { TOPIC_TREE } from '@/data/topicTree';
import { LESSON_TOPICS } from '@/data/lessonTopics';
import { getLesson } from '@/lib/handsOn/partition';
import { hasTeachScript } from '@/lib/teach/lookup';
import {
  getNextActions,
  dayStart,
  masteryOfNode,
  NEXT_ACTION_TYPES,
  NEXT_ACTION_RULE_IDS,
  type NextActionType,
} from '@/lib/brain/nextAction';

export const dynamic = 'force-dynamic';

const NO_STORE = { 'Cache-Control': 'private, no-store' };
const SURFACES = ['home', 'session_end'];
const MS_PER_DAY = 86_400_000;

/**
 * GET /api/recommendations
 *
 * `{ actions: NextAction[] }` for the signed-in child, best first (at most 3).
 * Worked out by fixed rules from the child's own records. Read-only: it does
 * not touch grading, XP or mastery. Empty while a mock test is in progress.
 */
export async function GET() {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: NO_STORE });
  }
  if (!checkRateLimit(`recs:${studentId}`, 60, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429, headers: NO_STORE });
  }

  try {
    const actions = await getNextActions(studentId, { limit: 3 });
    return NextResponse.json({ actions }, { headers: NO_STORE });
  } catch (err) {
    logError('[recommendations GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500, headers: NO_STORE });
  }
}

/** A refId is accepted only when it names real content of the kind the action points at. */
function refIsValid(actionType: NextActionType, refId: string | null): boolean {
  if (actionType === 'lesson') {
    if (!refId) return false;
    for (let i = 0; i < LESSON_TOPICS.length; i++) if (LESSON_TOPICS[i].id === refId) return true;
    return false;
  }
  if (actionType === 'hands_on') return !!refId && getLesson(refId) !== null;
  if (actionType === 'explain') return !!refId && hasTeachScript(refId);
  if (actionType === 'drill') return !!refId && /^[a-z_]{1,60}:L[1-5]$/.test(refId);
  if (actionType === 'strategy') return !!refId && /^STR_\d{1,4}$/.test(refId);
  // review, flashcards, mock, practice carry no content id.
  return refId === null;
}

/**
 * POST /api/recommendations
 * Body: { event: 'shown' | 'taken', surface: 'home' | 'session_end',
 *         actionType, ruleId, nodeId?, refId? }
 *
 * Records that a recommendation was shown or taken. Codes and ids only, each
 * checked against a fixed list. `masteryBefore` is read here from the stored
 * Brain Engine analytics, never taken from the request.
 *
 * "shown" is recorded once per action, per day, per surface. "taken" stamps
 * the row shown in the last 24 hours, or writes a new row if there is none.
 * `completedAt` is set later by POST /api/content-view for content actions;
 * for review, flashcards, mock and practice actions it stays null.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: NO_STORE });
  }
  if (!checkRateLimit(`recs-event:${studentId}`, 60, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429, headers: NO_STORE });
  }

  try {
    let raw: unknown;
    try {
      raw = await req.json();
    } catch {
      return NextResponse.json({ error: 'Request body must be JSON' }, { status: 400, headers: NO_STORE });
    }

    const body = validateBody<{
      event: string;
      surface: string;
      actionType: string;
      ruleId: string;
      nodeId?: string | null;
      refId?: string | null;
    }>(raw, {
      event: 'string',
      surface: 'string',
      actionType: 'string',
      ruleId: 'string',
      nodeId: 'string?',
      refId: 'string?',
    });

    const event = body.event;
    if (event !== 'shown' && event !== 'taken') {
      return NextResponse.json({ error: 'Unknown event' }, { status: 400, headers: NO_STORE });
    }
    if (SURFACES.indexOf(body.surface) === -1) {
      return NextResponse.json({ error: 'Unknown surface' }, { status: 400, headers: NO_STORE });
    }
    const typeIndex = (NEXT_ACTION_TYPES as string[]).indexOf(body.actionType);
    if (typeIndex === -1) {
      return NextResponse.json({ error: 'Unknown actionType' }, { status: 400, headers: NO_STORE });
    }
    const actionType = NEXT_ACTION_TYPES[typeIndex];
    if (NEXT_ACTION_RULE_IDS.indexOf(body.ruleId) === -1) {
      return NextResponse.json({ error: 'Unknown ruleId' }, { status: 400, headers: NO_STORE });
    }

    const nodeId = body.nodeId ? body.nodeId : null;
    if (nodeId !== null) {
      let known = false;
      for (let i = 0; i < TOPIC_TREE.length; i++) {
        if (TOPIC_TREE[i].id === nodeId) { known = true; break; }
      }
      if (!known) {
        return NextResponse.json({ error: 'Unknown nodeId' }, { status: 400, headers: NO_STORE });
      }
    }

    const refId = body.refId ? body.refId : null;
    if ((refId !== null && refId.length > 80) || !refIsValid(actionType, refId)) {
      return NextResponse.json({ error: 'Unknown refId' }, { status: 400, headers: NO_STORE });
    }

    const surface = body.surface;
    const ruleId = body.ruleId;
    const now = new Date();
    const identity = { studentId, ruleId, actionType, surface, nodeId, refId };

    if (event === 'shown') {
      const already = await prisma.recommendationEvent.findFirst({
        where: { ...identity, shownAt: { gte: dayStart(now) } },
        select: { id: true },
      });
      if (already) return NextResponse.json({ ok: true, recorded: false }, { headers: NO_STORE });
    } else {
      const open = await prisma.recommendationEvent.findFirst({
        where: { ...identity, shownAt: { gte: new Date(now.getTime() - MS_PER_DAY) } },
        orderBy: { shownAt: 'desc' },
        select: { id: true, takenAt: true },
      });
      if (open) {
        if (open.takenAt === null) {
          await prisma.recommendationEvent.update({
            where: { id: open.id },
            data: { takenAt: now },
          });
        }
        return NextResponse.json({ ok: true, recorded: open.takenAt === null }, { headers: NO_STORE });
      }
    }

    // A new row. Mastery comes from the stored analytics, never from the client.
    let masteryBefore: number | null = null;
    if (nodeId !== null) {
      const analytics = await prisma.studentAnalytics.findUnique({
        where: { studentId },
        select: { topicMastery: true },
      });
      masteryBefore = analytics ? masteryOfNode(analytics.topicMastery, nodeId) : null;
    }

    await prisma.recommendationEvent.create({
      data: {
        studentId,
        actionType,
        ruleId,
        nodeId,
        refId,
        surface,
        shownAt: now,
        takenAt: event === 'taken' ? now : null,
        masteryBefore,
      },
    });

    return NextResponse.json({ ok: true, recorded: true }, { headers: NO_STORE });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400, headers: NO_STORE });
    }
    logError('[recommendations POST]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500, headers: NO_STORE });
  }
}
