import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { TOPIC_ORDER } from '@/lib/sharedUtils';

// GET /api/topics
export async function GET() {
  try {
    const topics = await prisma.topic.findMany();
    topics.sort(
      (a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id),
    );
    return NextResponse.json(topics, {
      headers: {
        'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
      },
    });
  } catch (err) {
    console.error('[topics] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
