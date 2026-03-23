import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'paper-bank.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

// GET /api/papers/[paperId]
// Returns a single paper with all questions
export async function GET(
  _req: Request,
  { params }: { params: Promise<{ paperId: string }> },
) {
  const { paperId } = await params;

  const data = loadData() as {
    meta: Record<string, unknown>;
    papers: Record<string, unknown>[];
  } | null;

  if (!data || !data.papers) {
    return NextResponse.json({ error: 'Paper bank not found' }, { status: 404 });
  }

  const paper = data.papers.find(
    (p: Record<string, unknown>) => p.paperId === paperId,
  );

  if (!paper) {
    return NextResponse.json({ error: `Paper ${paperId} not found` }, { status: 404 });
  }

  return NextResponse.json({ paper });
}
