import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

export const dynamic = 'force-dynamic';

let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'worked-examples.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

interface Example {
  id: string;
  grade: number;
  topic: string;
  subTopic: string;
  difficulty: string;
  questionText: string;
  correctAnswer: string;
  correctAnswerText: string;
  [key: string]: unknown;
}

// GET /api/worked-examples               → topics + example list (no steps)
// GET /api/worked-examples?id=WE_0001    → full example with steps
// GET /api/worked-examples?topic=algebra  → examples for that topic
// GET /api/worked-examples?grade=5        → examples for that grade
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const exampleId = searchParams.get('id');
  const topicFilter = searchParams.get('topic');
  const gradeFilter = searchParams.get('grade');

  const data = loadData() as {
    meta: Record<string, unknown>;
    examples: Example[];
  } | null;

  if (!data) {
    return NextResponse.json({ error: 'Worked examples not found' }, { status: 404 });
  }

  // Single example by ID — return full detail
  if (exampleId) {
    const example = data.examples.find((e) => e.id === exampleId);
    if (!example) {
      return NextResponse.json({ error: 'Example not found' }, { status: 404 });
    }
    return NextResponse.json({ example });
  }

  let examples = data.examples;

  // Filter by grade first: the topic summary below counts the examples of the
  // chosen grade, so the page only offers topics that have something to show.
  if (gradeFilter) {
    const grade = parseInt(gradeFilter, 10);
    examples = examples.filter((e) => e.grade === grade);
  }
  const forGrade = examples;

  // Filter by topic
  if (topicFilter) {
    examples = examples.filter((e) => e.topic === topicFilter);
  }

  // Return lightweight list (no steps/sparkyThinking/voiceScript)
  const list = examples.map((e) => ({
    id: e.id,
    grade: e.grade,
    topic: e.topic,
    subTopic: e.subTopic,
    difficulty: e.difficulty,
    questionText: e.questionText,
    correctAnswer: e.correctAnswer,
    correctAnswerText: e.correctAnswerText,
  }));

  // Build topic summary
  const topicMap = new Map<string, number>();
  for (const e of forGrade) {
    topicMap.set(e.topic, (topicMap.get(e.topic) ?? 0) + 1);
  }
  const topics = Array.from(topicMap.entries())
    .map(([topic, count]) => ({ topic, count }))
    .sort((a, b) => b.count - a.count);

  return NextResponse.json({
    meta: data.meta,
    topics,
    examples: list,
    total: list.length,
  });
}
