import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'strategy-bank.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

// GET /api/strategies             → all strategies + meta
// GET /api/strategies?category=x  → filter by category
// GET /api/strategies?id=STR_001  → single strategy
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get('id');
  const category = searchParams.get('category');

  const data = loadData() as {
    meta: Record<string, unknown>;
    strategies: Record<string, unknown>[];
  } | null;

  if (!data) {
    return NextResponse.json({ error: 'Strategy bank not found' }, { status: 404 });
  }

  if (id) {
    const strategy = data.strategies.find((s) => s.id === id);
    if (!strategy) {
      return NextResponse.json({ error: 'Strategy not found' }, { status: 404 });
    }
    return NextResponse.json({ strategy });
  }

  let strategies = data.strategies;
  if (category) {
    strategies = strategies.filter((s) => s.category === category);
  }

  return NextResponse.json({
    meta: data.meta,
    strategies,
    total: strategies.length,
  });
}
