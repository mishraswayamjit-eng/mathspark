export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { parseUnknownArray } from '@/lib/jsonFields';
import { logError } from '@/lib/logger';
import { visualFor, visualQuestionIds } from '@/lib/figures/lookup';
import type { FigureSpec, ServedVisual } from '@/lib/figures/types';

const MAX_LIMIT = 30;

interface GalleryStep { step: number; text: string; latex?: string }

/** Every figure kind used anywhere in one question's visual. */
function kindsIn(visual: ServedVisual): string[] {
  const found: string[] = [];
  function note(figure: FigureSpec | null | undefined) {
    if (figure && typeof figure.kind === 'string' && found.indexOf(figure.kind) === -1) found.push(figure.kind);
  }
  note(visual.figure);
  const stepFigures = Array.isArray(visual.stepFigures) ? visual.stepFigures : [];
  for (let i = 0; i < stepFigures.length; i++) note(stepFigures[i]);
  const steps = Array.isArray(visual.steps) ? visual.steps : [];
  for (let i = 0; i < steps.length; i++) note(steps[i] ? steps[i].figure : undefined);
  return found;
}

function parseSteps(raw: string): GalleryStep[] {
  const parsed = parseUnknownArray(raw);
  const out: GalleryStep[] = [];
  for (let i = 0; i < parsed.length; i++) {
    const item = parsed[i];
    if (typeof item === 'string') {
      out.push({ step: i + 1, text: item });
    } else if (item && typeof item === 'object') {
      const rec = item as Record<string, unknown>;
      out.push({
        step: typeof rec.step === 'number' ? rec.step : i + 1,
        text: typeof rec.text === 'string' ? rec.text : '',
        latex: typeof rec.latex === 'string' && rec.latex !== '' ? rec.latex : undefined,
      });
    }
  }
  return out;
}

function wholeNumber(raw: string | null, fallback: number): number {
  const n = raw === null ? NaN : parseInt(raw, 10);
  return isNaN(n) ? fallback : n;
}

/**
 * GET /api/figures/gallery?offset=0&limit=20&kind=triangle
 *
 * Review gallery: every question that has a figure, beside its figure and its
 * step figures. Returns worked solutions, so it is for review screens only.
 */
export async function GET(req: Request) {
  // This route returns answer keys and worked solutions. It is a review tool,
  // so it is switched off on the live site unless FIGURE_GALLERY=on is set there.
  // Preview deployments and local runs keep it.
  if (process.env.VERCEL_ENV === 'production' && process.env.FIGURE_GALLERY !== 'on') {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }

  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  if (!checkRateLimit(`figures-gallery:${studentId}`, 60, 60_000)) {
    return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
  }

  try {
    const { searchParams } = new URL(req.url);
    const offset = Math.max(0, wholeNumber(searchParams.get('offset'), 0));
    const limit = Math.min(MAX_LIMIT, Math.max(1, wholeNumber(searchParams.get('limit'), 20)));
    const kind = (searchParams.get('kind') || '').trim();

    // Walk every visual once: count the kinds, and keep the ids that match the filter.
    const allIds = visualQuestionIds();
    const kindCounts: Record<string, number> = {};
    const ids: string[] = [];
    for (let i = 0; i < allIds.length; i++) {
      const visual = visualFor(allIds[i], { withSolution: true });
      if (!visual) continue;
      const kinds = kindsIn(visual);
      for (let k = 0; k < kinds.length; k++) kindCounts[kinds[k]] = (kindCounts[kinds[k]] || 0) + 1;
      if (kind === '' || kinds.indexOf(kind) !== -1) ids.push(allIds[i]);
    }

    const pageIds = ids.slice(offset, offset + limit);
    const rows = pageIds.length === 0 ? [] : await prisma.question.findMany({
      where: { id: { in: pageIds } },
      select: {
        id: true,
        subTopic: true,
        questionText: true,
        option1: true,
        option2: true,
        option3: true,
        option4: true,
        correctAnswer: true,
        stepByStep: true,
      },
    });
    const byId: Record<string, (typeof rows)[number]> = {};
    for (let i = 0; i < rows.length; i++) byId[rows[i].id] = rows[i];

    const items = pageIds.map((id) => {
      const visual = visualFor(id, { withSolution: true });
      const row = Object.prototype.hasOwnProperty.call(byId, id) ? byId[id] : undefined;
      return {
        id,
        // False when the figure file names a question the database does not hold.
        found: row !== undefined,
        subTopic: row ? row.subTopic : '',
        questionText: row ? row.questionText : '',
        options: row ? [row.option1, row.option2, row.option3, row.option4] : [],
        correctAnswer: row ? row.correctAnswer : '',
        steps: row ? parseSteps(row.stepByStep) : [],
        visual: visual || {},
      };
    });

    return NextResponse.json({ total: ids.length, offset, limit, kind, kindCounts, items });
  } catch (err) {
    logError('[figures/gallery] GET failed', err);
    return NextResponse.json({ error: 'Could not load the gallery' }, { status: 500 });
  }
}
