import { NextResponse } from 'next/server';
import { prisma, USABLE_QUESTION_FILTER } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';
import { parseUnknownArray } from '@/lib/jsonFields';
import { logError } from '@/lib/logger';
import { questionToSpeech, walkthroughStepSpeech } from '@/lib/speech/mathToSpeech';
import type { StepItem } from '@/types';

export const dynamic = 'force-dynamic';

const DEFAULT_LIMIT = 100;
const MAX_LIMIT = 200;

interface NarrationItem {
  questionId: string;
  /** "question" or "step-N" (1-based) — the file name the app will ask for. */
  part: string;
  /** Exactly what the app would say for this part. */
  text: string;
}

function toSteps(raw: string | null): StepItem[] {
  const steps: StepItem[] = [];
  const parsed = parseUnknownArray(raw);
  for (let i = 0; i < parsed.length; i++) {
    const item = parsed[i] as { step?: unknown; text?: unknown; latex?: unknown } | null;
    if (!item || typeof item.text !== 'string') continue;
    steps.push({
      step: typeof item.step === 'number' ? item.step : i + 1,
      text: item.text,
      latex: typeof item.latex === 'string' ? item.latex : undefined,
    });
  }
  return steps;
}

/**
 * GET /api/admin/narration-manifest?secret=&page=0&limit=100&source=&topicId=
 *
 * Read-only export of the narration script for verified questions: one entry
 * for the question and one per solution step, using the same text functions
 * the app speaks with. scripts/generate_narration.py turns each entry into an
 * audio file. Nothing is written and no audio is generated here.
 */
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const page  = Math.max(0, Math.floor(Number(searchParams.get('page') ?? '0')) || 0);
    const limit = Math.min(MAX_LIMIT, Math.max(1, Math.floor(Number(searchParams.get('limit') ?? DEFAULT_LIMIT)) || DEFAULT_LIMIT));
    const source  = searchParams.get('source');
    const topicId = searchParams.get('topicId');

    const where = {
      ...USABLE_QUESTION_FILTER,
      ...(source ? { source } : {}),
      ...(topicId ? { topicId } : {}),
    };

    const rows = await prisma.question.findMany({
      where,
      orderBy: { id: 'asc' },
      skip: page * limit,
      take: limit,
      select: {
        id: true, questionText: true, questionLatex: true,
        option1: true, option2: true, option3: true, option4: true,
        correctAnswer: true, stepByStep: true, interactionType: true,
      },
    });

    const items: NarrationItem[] = [];
    for (let r = 0; r < rows.length; r++) {
      const q = rows[r];
      const questionText = questionToSpeech(q);
      if (questionText) items.push({ questionId: q.id, part: 'question', text: questionText });

      // The walkthrough player only narrates when there are two or more steps.
      const steps = toSteps(q.stepByStep);
      if (steps.length > 1) {
        for (let s = 0; s < steps.length; s++) {
          const text = walkthroughStepSpeech(q, steps, s);
          if (text) items.push({ questionId: q.id, part: `step-${s + 1}`, text });
        }
      }
    }

    return NextResponse.json({
      page,
      limit,
      questions: rows.length,
      done: rows.length < limit,
      items,
    });
  } catch (err) {
    logError('[admin/narration-manifest] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
