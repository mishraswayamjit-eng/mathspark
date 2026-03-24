import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'ipm-predictor.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

// GET /api/ipm-predictor              → meta + insights + all grade keys
// GET /api/ipm-predictor?grade=4      → single grade prediction
export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const grade = searchParams.get('grade');

    const data = loadData() as {
      meta: Record<string, unknown>;
      predictions: Record<string, Record<string, unknown>>;
      insights: Record<string, unknown>;
    } | null;

    if (!data) {
      return NextResponse.json({ error: 'IPM Predictor data not found' }, { status: 404 });
    }

    if (grade) {
      const prediction = data.predictions[grade];
      if (!prediction) {
        return NextResponse.json({ error: `No prediction for grade ${grade}` }, { status: 404 });
      }
      return NextResponse.json({
        prediction,
        insights: data.insights,
      });
    }

    // Return overview: meta, insights, and grade summaries (without full topicFrequency)
    const gradeSummaries = Object.entries(data.predictions).map(([g, pred]) => ({
      grade: Number(g),
      totalQuestionsAnalyzed: pred.totalQuestionsAnalyzed,
      yearsAnalyzed: pred.yearsAnalyzed,
      yearRange: pred.yearRange,
      topTopics: ((pred.topicFrequency as { topic: string; percentage: number }[]) ?? [])
        .filter((t) => t.topic !== 'Other')
        .slice(0, 3)
        .map((t) => t.topic),
      focusAreaCount: ((pred.predictedFocusAreas as string[]) ?? []).length,
    }));

    return NextResponse.json({
      meta: data.meta,
      insights: data.insights,
      grades: gradeSummaries,
    });
  } catch (err) {
    console.error('[ipm-predictor]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
