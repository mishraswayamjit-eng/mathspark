import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

// Cache the parsed JSON in memory (survives across requests in the same serverless instance)
let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'daily-challenges.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

function getDayOfYear(): number {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const diff = now.getTime() - start.getTime();
  return Math.floor(diff / (1000 * 60 * 60 * 24));
}

// GET /api/daily-challenge-data?grade=6
// Returns only today's challenge for the given grade (small payload)
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const grade = searchParams.get('grade') || '6';

  const data = loadData() as {
    meta: Record<string, unknown>;
    challenges: Record<string, unknown[]>;
  } | null;

  if (!data) {
    return NextResponse.json({ error: 'Daily challenges not found' }, { status: 404 });
  }

  const challenges = data.challenges?.[grade];
  if (!challenges || challenges.length === 0) {
    return NextResponse.json({ error: `No challenges for grade ${grade}` }, { status: 404 });
  }

  const dayOfYear = getDayOfYear();
  const index = (dayOfYear - 1) % challenges.length;
  const todaysChallenge = challenges[index];

  return NextResponse.json({
    meta: data.meta,
    challenge: todaysChallenge,
    dayOfYear,
    index,
  });
}
