import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

const PAGE_SIZE = 200;

function authorize(req: NextRequest): boolean {
  const secret = process.env.SEED_SECRET;
  if (!secret) return false;
  const { searchParams } = new URL(req.url);
  return searchParams.get('secret') === secret;
}

// ── Chapter ID extraction from question IDs ─────────────────────────────────
// Pattern: EXT_G4_WS2_CH12_001 → ch12
function extractChapterFromId(id: string): string | null {
  const m = id.match(/_CH(\d{2})_/i);
  if (!m) return null;
  const num = parseInt(m[1], 10);
  return chapterToTopicId(num);
}

// ── Vary stem extraction from question IDs ──────────────────────────────────
// Pattern: VAR_G4_vary_angles_V01 → ch18
const VARY_STEM_MAP: Record<string, string> = {
  angles: 'ch18',
  measurement: 'ch12', money: 'ch12', currency: 'ch12', metric: 'ch12', unit: 'ch12', weight: 'ch12',
  fraction: 'ch07-08', numerator: 'ch07-08', denominator: 'ch07-08',
  bodmas: 'ch09-10', operation: 'ch09-10',
  hcf: 'ch06', lcm: 'ch06', factor: 'ch06', divisib: 'ch06', prime: 'ch06',
  algebra: 'ch13', expression: 'ch13', substitut: 'ch13',
  equation: 'ch14', age_problem: 'ch14',
  pattern: 'ch16', sequence: 'ch16', series: 'ch16',
  place_value: 'ch01-05', counting: 'ch01-05', comparison: 'ch01-05', roman: 'ch01-05', square_number: 'ch01-05',
  decimal: 'ch11',
  magic_square: 'ch15', puzzle: 'ch15',
  calendar: 'ch17', time: 'ch17', clock: 'ch17',
  perimeter: 'ch20', area: 'ch20', geometry: 'ch20',
  triangle: 'ch19',
  circle: 'ch21', radius: 'ch21', diameter: 'ch21',
  data: 'dh', graph: 'dh', chart: 'dh',
};

function extractVaryStem(id: string): string | null {
  const m = id.match(/^VAR_G4_vary_(.+)_V\d+$/i);
  if (!m) return null;
  const stem = m[1].toLowerCase();
  // Direct match
  if (VARY_STEM_MAP[stem]) return VARY_STEM_MAP[stem];
  // Partial match
  for (const [key, topicId] of Object.entries(VARY_STEM_MAP)) {
    if (stem.includes(key)) return topicId;
  }
  return null;
}

// ── Chapter number → topicId ────────────────────────────────────────────────
function chapterToTopicId(ch: number): string | null {
  if (ch >= 1 && ch <= 5) return 'ch01-05';
  if (ch === 6) return 'ch06';
  if (ch === 7 || ch === 8) return 'ch07-08';
  if (ch === 9 || ch === 10) return 'ch09-10';
  if (ch === 11) return 'ch11';
  if (ch === 12) return 'ch12';
  if (ch === 13) return 'ch13';
  if (ch === 14) return 'ch14';
  if (ch === 15) return 'ch15';
  if (ch === 16) return 'ch16';
  if (ch === 17) return 'ch17';
  if (ch === 18) return 'ch18';
  if (ch === 19) return 'ch19';
  if (ch === 20) return 'ch20';
  if (ch === 21) return 'ch21';
  return null;
}

// ── SubTopic label + question text keyword mapping ──────────────────────────
const KEYWORD_RULES: Array<{ pattern: RegExp; topicId: string }> = [
  { pattern: /circle|radius|diameter|circumference|chord|arc|sector|semi-?circle/i, topicId: 'ch21' },
  { pattern: /triangle|isosceles|equilateral|scalene|altitude|median.*triangle/i, topicId: 'ch19' },
  { pattern: /quadrilateral|rectangle|parallelogram|rhombus|trapez|perimeter|area/i, topicId: 'ch20' },
  { pattern: /angle|complementary|supplementary|protractor|acute|obtuse|reflex/i, topicId: 'ch18' },
  { pattern: /calendar|clock|hour|minute|second|leap|schedule/i, topicId: 'ch17' },
  { pattern: /sequence|series|pattern|fibonacci|next.*term|nth term/i, topicId: 'ch16' },
  { pattern: /puzzle|magic square|riddle|cryptarithm|match.*stick/i, topicId: 'ch15' },
  { pattern: /equation|solve.*(?:for|x)|value of.*x|lhs.*rhs/i, topicId: 'ch14' },
  { pattern: /algebra|expression|coefficient|like term|substitut/i, topicId: 'ch13' },
  { pattern: /\bkg\b|\bcm\b|\bmm\b|\bkm\b|meter|litre|\bml\b|gram|unit.*measurement|convert.*unit|capacity|temperature|money|currency|cost|price|rupee|score|gross|dozen/i, topicId: 'ch12' },
  { pattern: /decimal|tenth|hundredth/i, topicId: 'ch11' },
  { pattern: /bodmas|order of operation|bracket/i, topicId: 'ch09-10' },
  { pattern: /fraction|numerator|denominator|mixed|improper|equivalent/i, topicId: 'ch07-08' },
  { pattern: /\bhcf\b|\blcm\b|\bgcd\b|factor|multiple|prime|composite|divisib|co-?prime/i, topicId: 'ch06' },
  { pattern: /place value|roman|expand|ascend|descend|comparison|counting|number.*system|even|odd/i, topicId: 'ch01-05' },
  { pattern: /data|graph|chart|table|average|mean|tally|bar|pie|pictograph|frequency/i, topicId: 'dh' },
];

function classifyByKeywords(subTopic: string, questionText: string): string | null {
  const text = `${subTopic} ${questionText}`;
  for (const rule of KEYWORD_RULES) {
    if (rule.pattern.test(text)) return rule.topicId;
  }
  return null;
}

// ── GET: Paginated dry-run / apply ──────────────────────────────────────────
//
// Usage (client loops until done=true):
//   GET /api/admin/redistribute-grade4?secret=xxx&page=0           → dry run
//   GET /api/admin/redistribute-grade4?secret=xxx&page=0&apply=1   → apply

export async function GET(req: NextRequest) {
  if (!authorize(req)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const page  = parseInt(searchParams.get('page') ?? '0', 10);
  const apply = searchParams.get('apply') === '1';

  try {
    const total = page === 0
      ? await prisma.question.count({ where: { topicId: 'grade4' } })
      : 0;

    const questions = await prisma.question.findMany({
      where: { topicId: 'grade4' },
      select: { id: true, subTopic: true, questionText: true },
      orderBy: { id: 'asc' },
      skip: page * PAGE_SIZE,
      take: PAGE_SIZE,
    });

    const done = questions.length < PAGE_SIZE;

    // Classify each question
    const byMethod = { chapter_id: 0, vary_stem: 0, keyword: 0, unclassified: 0 };
    const byTarget: Record<string, string[]> = {}; // topicId → question IDs
    const perTopic: Record<string, number> = {};

    for (const q of questions) {
      let target: string | null = null;
      let method: keyof typeof byMethod = 'unclassified';

      // Tier 1: Chapter ID in question ID
      target = extractChapterFromId(q.id);
      if (target) {
        method = 'chapter_id';
      } else {
        // Tier 2: Vary stem in ID
        target = extractVaryStem(q.id);
        if (target) {
          method = 'vary_stem';
        } else {
          // Tier 3: SubTopic label + question text keywords
          target = classifyByKeywords(q.subTopic ?? '', q.questionText ?? '');
          if (target) {
            method = 'keyword';
          }
        }
      }

      byMethod[method]++;

      if (target) {
        if (!byTarget[target]) byTarget[target] = [];
        byTarget[target].push(q.id);
        perTopic[target] = (perTopic[target] || 0) + 1;
      }
    }

    // Apply updates: one updateMany per target topicId
    let pageUpdated = 0;
    if (apply) {
      for (const [targetTopicId, ids] of Object.entries(byTarget)) {
        const result = await prisma.question.updateMany({
          where: { id: { in: ids } },
          data: { topicId: targetTopicId },
        });
        pageUpdated += result.count;
      }
    }

    return NextResponse.json({
      done,
      nextPage: done ? null : page + 1,
      total: total || undefined,
      pageQuestions: questions.length,
      pageUpdated,
      byMethod,
      perTopic,
    });
  } catch (err) {
    return NextResponse.json(
      { error: `Redistribute failed: ${err instanceof Error ? err.message : String(err)}` },
      { status: 500 },
    );
  }
}
