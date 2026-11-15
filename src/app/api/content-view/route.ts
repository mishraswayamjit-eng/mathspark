import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';

export const dynamic = 'force-dynamic';

const NO_STORE = { 'Cache-Control': 'private, no-store' };
const MS_PER_DAY = 86_400_000;
const REF_MAX = 80;

/** Content kind → the recommendation action type that points at it. */
const KIND_TO_ACTION: Record<string, string> = {
  teach: 'explain',
  hands_on: 'hands_on',
  drill: 'drill',
  lesson: 'lesson',
  story: 'story',
  strategy: 'strategy',
};

/**
 * POST /api/content-view
 * Body: { kind: 'teach' | 'hands_on' | 'drill' | 'lesson' | 'story' | 'strategy',
 *         refId: string, completed?: boolean }
 *
 * Remembers that the signed-in child opened (and, with `completed`, finished) a
 * piece of learning content: one row per child per piece of content. It is a
 * record only and never changes XP, mastery or grading.
 *
 * When the content is finished, a recommendation for the same content that the
 * child took in the last 7 days is marked completed. A strategy has no finish
 * step, so opening it counts for that purpose.
 */
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: NO_STORE });
  }
  if (!checkRateLimit(`content-view:${studentId}`, 60, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429, headers: NO_STORE });
  }

  try {
    let raw: unknown;
    try {
      raw = await req.json();
    } catch {
      return NextResponse.json({ error: 'Request body must be JSON' }, { status: 400, headers: NO_STORE });
    }

    const body = validateBody<{ kind: string; refId: string; completed?: boolean | null }>(raw, {
      kind: 'string',
      refId: 'string',
      completed: 'boolean?',
    });

    const kind = body.kind;
    if (!Object.prototype.hasOwnProperty.call(KIND_TO_ACTION, kind)) {
      return NextResponse.json({ error: 'Unknown kind' }, { status: 400, headers: NO_STORE });
    }
    const refId = body.refId.trim();
    // An id, never a sentence: short, no spaces.
    if (!refId || refId.length > REF_MAX || /\s/.test(refId)) {
      return NextResponse.json({ error: 'Invalid refId' }, { status: 400, headers: NO_STORE });
    }
    const completed = body.completed === true;
    const now = new Date();

    await prisma.contentView.upsert({
      where: { studentId_kind_refId: { studentId, kind, refId } },
      create: { studentId, kind, refId, completedAt: completed ? now : null },
      update: completed ? { completedAt: now } : {},
    });

    if (completed || kind === 'strategy') {
      await prisma.recommendationEvent.updateMany({
        where: {
          studentId,
          actionType: KIND_TO_ACTION[kind],
          refId,
          takenAt: { gte: new Date(now.getTime() - 7 * MS_PER_DAY) },
          completedAt: null,
        },
        data: { completedAt: now },
      });
    }

    return NextResponse.json({ ok: true }, { headers: NO_STORE });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400, headers: NO_STORE });
    }
    logError('[content-view POST]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500, headers: NO_STORE });
  }
}
