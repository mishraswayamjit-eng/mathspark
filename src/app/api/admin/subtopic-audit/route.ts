/**
 * TEMPORARY admin route — quantify substring cross-contamination in the
 * subTopic ILIKE filter. For each grade's keys, compare loose-substring matches
 * vs word-boundary (prefix) matches and list the contaminant subTopic strings.
 * Read-only. Remove after use.
 */
import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifySecret } from '@/lib/adminAuth';
import { getTopicsForGrade } from '@/data/topicTree';

export const dynamic = 'force-dynamic';
export const maxDuration = 60;

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function matchesBoundary(subTopic: string, key: string): boolean {
  return new RegExp(`(^|[^a-z0-9])${escapeRegExp(key.toLowerCase())}`).test(
    subTopic.toLowerCase(),
  );
}

export async function GET(req: NextRequest) {
  const p = req.nextUrl.searchParams;
  if (!verifySecret(p.get('secret'))) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const grade = parseInt(p.get('grade') ?? '5', 10);
  const dbTopicId = `grade${grade}`;

  const rows = await prisma.question.findMany({
    where: { topicId: dbTopicId },
    select: { subTopic: true, source: true },
  });

  // Distinct subTopic strings + counts
  const distinct = new Map<string, number>();
  for (const r of rows) {
    const st = r.subTopic ?? '';
    distinct.set(st, (distinct.get(st) ?? 0) + 1);
  }

  const keys = getTopicsForGrade(grade)
    .map((t) => t.subTopicKey)
    .filter((k): k is string => !!k);

  const perKey = keys.map((key) => {
    const kl = key.toLowerCase();
    let loose = 0;
    let boundary = 0;
    const contaminants = new Map<string, number>();
    for (const [st, count] of Array.from(distinct.entries())) {
      const stl = st.toLowerCase();
      const looseHit = stl.includes(kl);
      const boundaryHit = matchesBoundary(st, key);
      if (looseHit) loose += count;
      if (boundaryHit) boundary += count;
      if (looseHit && !boundaryHit) {
        contaminants.set(st, (contaminants.get(st) ?? 0) + count);
      }
    }
    return {
      key,
      loose,
      boundary,
      contaminantRows: loose - boundary,
      contaminants: Array.from(contaminants.entries()).map(([st, c]) => ({ subTopic: st, count: c })),
    };
  });

  return NextResponse.json({
    grade,
    totalRows: rows.length,
    distinctSubTopics: distinct.size,
    distinct: Array.from(distinct.entries())
      .sort((a, b) => b[1] - a[1])
      .map(([subTopic, count]) => ({ subTopic, count })),
    perKey,
  });
}
