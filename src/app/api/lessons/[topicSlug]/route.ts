export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { loadTopic, LESSON_SLUG_RE } from '@/lib/lessonData';

export async function GET(
  _req: Request,
  { params }: { params: { topicSlug: string } },
) {
  const { topicSlug } = params;

  if (!LESSON_SLUG_RE.test(topicSlug)) {
    return NextResponse.json({ error: 'Invalid slug' }, { status: 400 });
  }

  const data = loadTopic(topicSlug);
  if (!data) {
    return NextResponse.json({ error: 'Topic not found' }, { status: 404 });
  }

  return NextResponse.json(data);
}
