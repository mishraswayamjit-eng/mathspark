import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

// Cache parsed JSON in memory
let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'paper-bank.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

interface PaperMeta {
  paperId: string;
  title: string;
  grade: number;
  duration: number;
  totalQuestions: number;
  totalMarks: number;
  variantNumber: number;
  difficultyDistribution: Record<string, number>;
  topicsCovered: string[];
}

// GET /api/papers?grade=6&duration=60
// Returns paper metadata list (no questions — keeps payload small)
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const gradeFilter = searchParams.get('grade');
  const durationFilter = searchParams.get('duration');

  const data = loadData() as {
    meta: Record<string, unknown>;
    papers: Record<string, unknown>[];
  } | null;

  if (!data || !data.papers) {
    return NextResponse.json({ error: 'Paper bank not found' }, { status: 404 });
  }

  let papers = data.papers;

  // Filter by grade
  if (gradeFilter) {
    const g = parseInt(gradeFilter, 10);
    papers = papers.filter((p: Record<string, unknown>) => p.grade === g);
  }

  // Filter by duration
  if (durationFilter) {
    const d = parseInt(durationFilter, 10);
    papers = papers.filter((p: Record<string, unknown>) => p.duration === d);
  }

  // Return only metadata (no questions array)
  const list: PaperMeta[] = papers.map((p: Record<string, unknown>) => ({
    paperId: p.paperId as string,
    title: p.title as string,
    grade: p.grade as number,
    duration: p.duration as number,
    totalQuestions: p.totalQuestions as number,
    totalMarks: p.totalMarks as number,
    variantNumber: p.variantNumber as number,
    difficultyDistribution: p.difficultyDistribution as Record<string, number>,
    topicsCovered: p.topicsCovered as string[],
  }));

  return NextResponse.json({ meta: data.meta, papers: list });
}
