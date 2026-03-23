import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'mistake-patterns.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

// GET /api/mistake-patterns                     → all patterns + meta
// GET /api/mistake-patterns?category=wrong_formula → filter by category
// GET /api/mistake-patterns?grade=6              → filter by affected grade
// GET /api/mistake-patterns?frequency=Very+High  → filter by frequency
// GET /api/mistake-patterns?id=MP_001            → single pattern
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get('id');
  const category = searchParams.get('category');
  const grade = searchParams.get('grade');
  const frequency = searchParams.get('frequency');

  const data = loadData() as {
    meta: Record<string, unknown>;
    patterns: Record<string, unknown>[];
  } | null;

  if (!data) {
    return NextResponse.json({ error: 'Mistake patterns not found' }, { status: 404 });
  }

  if (id) {
    const pattern = data.patterns.find((p) => p.id === id);
    if (!pattern) {
      return NextResponse.json({ error: 'Pattern not found' }, { status: 404 });
    }
    return NextResponse.json({ pattern });
  }

  let patterns = data.patterns;
  if (category) {
    patterns = patterns.filter((p) => p.category === category);
  }
  if (grade) {
    const g = Number(grade);
    patterns = patterns.filter((p) => {
      const grades = p.affectedGrades as number[] | undefined;
      return grades && grades.includes(g);
    });
  }
  if (frequency) {
    patterns = patterns.filter((p) => p.frequency === frequency);
  }

  return NextResponse.json({
    meta: data.meta,
    patterns,
    total: patterns.length,
  });
}
