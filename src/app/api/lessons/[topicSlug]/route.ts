export const dynamic = 'force-dynamic';

import fs from 'fs';
import path from 'path';
import { NextResponse } from 'next/server';

const cache = new Map<string, unknown>();
const SLUG_RE = /^[a-z0-9-]+$/;

function loadTopic(slug: string) {
  if (cache.has(slug)) return cache.get(slug);
  const filePath = path.join(process.cwd(), 'data', 'lessons', `${slug}.json`);
  if (!fs.existsSync(filePath)) return null;
  const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  cache.set(slug, data);
  return data;
}

export async function GET(
  _req: Request,
  { params }: { params: { topicSlug: string } },
) {
  const { topicSlug } = params;

  if (!SLUG_RE.test(topicSlug)) {
    return NextResponse.json({ error: 'Invalid slug' }, { status: 400 });
  }

  const data = loadTopic(topicSlug);
  if (!data) {
    return NextResponse.json({ error: 'Topic not found' }, { status: 404 });
  }

  return NextResponse.json(data);
}
