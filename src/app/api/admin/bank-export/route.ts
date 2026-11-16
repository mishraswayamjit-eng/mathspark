import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';
import { logError } from '@/lib/logger';
import seedIdList from '@/data/bank/seedIds.json';
// The reverse of the bank → database mapping lives beside the mapping itself.
import { rowToBankQuestion } from '../../../../../scripts/bank/bankRows.mjs';
import type { ExportedBankQuestion } from '../../../../../scripts/bank/bankRows.mjs';

export const dynamic = 'force-dynamic';

// Every id held in the question bank (src/data/bank/seedIds.json). A question
// in the database whose id is not here exists only in the database.
const BANK_IDS: { [id: string]: true } = {};
for (let i = 0; i < (seedIdList as string[]).length; i++) BANK_IDS[(seedIdList as string[])[i]] = true;

// Questions the app creates in code (the seed route's interactive set). They
// are not bank questions and carry data the bank shape cannot hold.
const CODE_SEEDED_SOURCE = 'interactive_seed';

const FETCH_CHUNK = 500;
const MAX_LIMIT = 1000;

function wholeNumber(raw: string | null): number | null {
  if (raw === null || raw.trim() === '') return null;
  const value = Number(raw);
  return isFinite(value) && Math.floor(value) === value ? value : null;
}

// ── GET /api/admin/bank-export?secret=xxx[&grade=5][&offset=0&limit=300] ────
//
// "Bring them home": every question that is in the database and not in the
// question bank, written in the bank's own shape, as a downloadable file:
//
//   { exportedAt, grade, count, total, offset, nextOffset, codeSeededSkipped,
//     questions: [ { id, node: null, topicId, subTopic, difficulty, questionText,
//                    questionLatex, options: [{id,text}×4], correctAnswer, hints,
//                    stepByStep, misconceptions: {A,B,C,D}, source, year?, questionNumber? } ] }
//
// Questions are sorted by id. Without `limit` the whole set is returned in one
// answer; with it, one slice (the /seed screen asks in slices and joins them,
// so a large grade never exceeds the size limit of one answer). Read-only.

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const gradeRaw = searchParams.get('grade');
  const grade = wholeNumber(gradeRaw);
  if (gradeRaw !== null && gradeRaw !== '' && (grade === null || grade < 2 || grade > 9)) {
    return NextResponse.json({ error: 'grade must be a whole number from 2 to 9' }, { status: 400 });
  }
  const offset = Math.max(0, wholeNumber(searchParams.get('offset')) ?? 0);
  const limitRaw = wholeNumber(searchParams.get('limit'));
  const limit = limitRaw === null ? null : Math.min(MAX_LIMIT, Math.max(1, limitRaw));

  try {
    // 1. Ids only, to find the ones the bank does not hold.
    const light = await prisma.question.findMany({
      where: grade === null ? {} : { topic: { grade } },
      select: { id: true, source: true },
    });
    const databaseOnly: string[] = [];
    let codeSeededSkipped = 0;
    for (let i = 0; i < light.length; i++) {
      if (BANK_IDS[light[i].id] === true) continue;
      if (light[i].source === CODE_SEEDED_SOURCE) { codeSeededSkipped++; continue; }
      databaseOnly.push(light[i].id);
    }
    databaseOnly.sort();

    // 2. The slice asked for, in full.
    const wanted = limit === null ? databaseOnly.slice(offset) : databaseOnly.slice(offset, offset + limit);
    const questions: ExportedBankQuestion[] = [];
    for (let start = 0; start < wanted.length; start += FETCH_CHUNK) {
      const rows = await prisma.question.findMany({
        where: { id: { in: wanted.slice(start, start + FETCH_CHUNK) } },
        select: {
          id: true, topicId: true, subTopic: true, difficulty: true,
          questionText: true, questionLatex: true,
          option1: true, option2: true, option3: true, option4: true,
          correctAnswer: true, hint1: true, hint2: true, hint3: true,
          stepByStep: true,
          misconceptionA: true, misconceptionB: true, misconceptionC: true, misconceptionD: true,
          source: true, year: true, questionNumber: true,
        },
      });
      for (let r = 0; r < rows.length; r++) questions.push(rowToBankQuestion(rows[r]));
    }
    questions.sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

    const end = offset + wanted.length;
    const exportedAt = new Date().toISOString();
    const body = {
      exportedAt,
      grade,
      count: questions.length,
      total: databaseOnly.length,
      offset,
      nextOffset: end < databaseOnly.length ? end : null,
      codeSeededSkipped,
      questions,
    };

    const name = `bank-export-${grade === null ? 'all-grades' : `grade${grade}`}-${exportedAt.slice(0, 10)}.json`;
    return new NextResponse(JSON.stringify(body), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Disposition': `attachment; filename="${name}"`,
        'Cache-Control': 'no-store',
      },
    });
  } catch (err) {
    logError('[bank-export] failed', err);
    return NextResponse.json(
      { error: `Export failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}
