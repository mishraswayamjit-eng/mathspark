import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

// GET /api/topics
export async function GET() {
  const topics = await prisma.topic.findMany();
  topics.sort(
    (a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id),
  );
  return NextResponse.json(topics);
}
