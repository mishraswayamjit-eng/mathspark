import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

export const revalidate = 3600; // Revalidate topics once per hour

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
    console.error('[GET /api/topics]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
