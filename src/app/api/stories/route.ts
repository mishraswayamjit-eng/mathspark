import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'math-stories.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

// GET /api/stories                  → all stories + meta
// GET /api/stories?category=sports  → filter by context category
// GET /api/stories?topic=percentage → filter by topic
// GET /api/stories?id=MS_001       → single story
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const id = searchParams.get('id');
  const category = searchParams.get('category');
  const topic = searchParams.get('topic');

  const data = loadData() as {
    meta: Record<string, unknown>;
    stories: Record<string, unknown>[];
  } | null;

  if (!data) {
    return NextResponse.json({ error: 'Math stories not found' }, { status: 404 });
  }

  if (id) {
    const story = data.stories.find((s) => s.id === id);
    if (!story) {
      return NextResponse.json({ error: 'Story not found' }, { status: 404 });
    }
    return NextResponse.json({ story });
  }

  let stories = data.stories;
  if (category) {
    stories = stories.filter((s) => s.contextCategory === category);
  }
  if (topic) {
    stories = stories.filter((s) => s.topicId === topic);
  }

  return NextResponse.json({
    meta: data.meta,
    stories,
    total: stories.length,
  });
}
