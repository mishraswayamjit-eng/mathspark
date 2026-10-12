import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';

export const dynamic = 'force-dynamic';
export const maxDuration = 300;

// ── TEMPORARY admin route: strip leaked model self-talk from stepByStep ──────
// GET  ?secret=xxx[&topicId=grade5][&source=ai_generated][&limit=50]  → dry-run report
// POST ?secret=xxx[&topicId=grade5][&source=ai_generated]             → apply fixes
//
// Only the stepByStep field is touched. Each step's text is truncated at the
// first self-talk marker ("Wait", "Hmm", "let me recheck/verify/double-check",
// "re-examining"); a step left empty is dropped; remaining steps are renumbered.
// The answer, options, hints and all computation steps are never modified.

interface Step {
  step: number;
  text: string;
  latex?: string;
}

// Markers that signal leaked chain-of-thought / self-correction.
const SELF_TALK =
  /\b(wait|hmm+)\b|let me (re-?check|check|verify|double[\s-]?check)|re-?examin/i;

/** Returns a cleaned step array, or null if nothing changed. */
function cleanSteps(raw: unknown): Step[] | null {
  if (!Array.isArray(raw)) return null;
  let changed = false;
  const out: Step[] = [];

  for (const s of raw) {
    if (!s || typeof s !== 'object') continue;
    const so = s as Record<string, unknown>;
    const text = typeof so.text === 'string' ? so.text : '';
    const latex = typeof so.latex === 'string' ? so.latex : '';

    const m = SELF_TALK.exec(text);
    if (m) {
      changed = true;
      // Keep only the content before the marker, trimmed of dangling joiners.
      const kept = text.slice(0, m.index).replace(/[\s\u2014\-:;,.]+$/, '').trim();
      if (kept) {
        out.push({ step: out.length + 1, text: kept, ...(latex ? { latex } : {}) });
      }
      // else: whole step was self-talk → drop it (and its latex).
    } else {
      out.push({ step: out.length + 1, text, ...(latex ? { latex } : {}) });
    }
  }

  return changed ? out : null;
}

async function loadCandidates(topicId: string, source: string) {
  const rows = await prisma.question.findMany({
    where: { topicId, source },
    select: { id: true, stepByStep: true },
  });
  const affected: Array<{ id: string; before: Step[]; after: Step[] }> = [];
  for (const r of rows) {
    let parsed: unknown;
    try {
      parsed = JSON.parse(r.stepByStep || '[]');
    } catch {
      continue; // leave unparseable rows untouched
    }
    const cleaned = cleanSteps(parsed);
    if (cleaned) {
      affected.push({ id: r.id, before: parsed as Step[], after: cleaned });
    }
  }
  return { scanned: rows.length, affected };
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const topicId = searchParams.get('topicId') ?? 'grade5';
  const source = searchParams.get('source') ?? 'ai_generated';
  const limit = Math.min(Math.max(parseInt(searchParams.get('limit') ?? '50', 10), 1), 500);

  const { scanned, affected } = await loadCandidates(topicId, source);
  return NextResponse.json({
    mode: 'dry-run',
    topicId,
    source,
    scanned,
    affectedCount: affected.length,
    sample: affected.slice(0, limit).map((a) => ({
      id: a.id,
      beforeText: a.before.map((s) => s.text),
      afterText: a.after.map((s) => s.text),
    })),
  });
}

export async function POST(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const topicId = searchParams.get('topicId') ?? 'grade5';
  const source = searchParams.get('source') ?? 'ai_generated';

  const { scanned, affected } = await loadCandidates(topicId, source);
  let updated = 0;
  for (const a of affected) {
    await prisma.question.update({
      where: { id: a.id },
      data: { stepByStep: JSON.stringify(a.after) },
    });
    updated += 1;
  }
  return NextResponse.json({ mode: 'apply', topicId, source, scanned, updated });
}
