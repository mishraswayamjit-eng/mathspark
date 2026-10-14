import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';
import { gradeInRange } from '@/lib/sharedUtils';

export const dynamic = 'force-dynamic';

let cached: Record<string, unknown> | null = null;

function loadData() {
  if (cached) return cached;
  const filePath = path.join(process.cwd(), 'data', 'skill-drills.json');
  if (!fs.existsSync(filePath)) return null;
  cached = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  return cached;
}

// GET /api/skill-drills?topic=algebra_equations&level=L2&session=1
// Without params: returns topics + meta (no sessions/questions)
// With topic+level: returns sessions list for that topic/level (no questions)
// With topic+level+session: returns full session with questions
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const topicId = searchParams.get('topic');
  const levelId = searchParams.get('level');
  const sessionNum = searchParams.get('session');
  const gradeParam = searchParams.get('grade');
  const grade = gradeParam ? parseInt(gradeParam, 10) : NaN;

  const data = loadData() as {
    meta: Record<string, unknown>;
    topics: Record<string, Record<string, unknown>>;
    sessions: Record<string, unknown>[];
  } | null;

  if (!data) {
    return NextResponse.json({ error: 'Skill drills not found' }, { status: 404 });
  }

  // No params — return topics + meta only
  if (!topicId) {
    if (Number.isNaN(grade)) {
      return NextResponse.json({ meta: data.meta, topics: data.topics });
    }
    // Keep only levels whose gradeRange covers the grade; drop topics left empty.
    const topics: Record<string, Record<string, unknown>> = {};
    for (const [key, topic] of Object.entries(data.topics)) {
      const levels = topic.levels as Record<string, { gradeRange?: unknown }> | undefined;
      if (!levels) {
        topics[key] = topic;
        continue;
      }
      const keptLevels = Object.fromEntries(
        Object.entries(levels).filter(([, lv]) => gradeInRange(lv.gradeRange, grade)),
      );
      if (Object.keys(keptLevels).length > 0) {
        topics[key] = { ...topic, levels: keptLevels };
      }
    }
    return NextResponse.json({ meta: data.meta, topics });
  }

  // Topic + level — return matching sessions (without questions)
  if (topicId && levelId && !sessionNum) {
    const sessions = data.sessions
      .filter(
        (s: Record<string, unknown>) =>
          s.topicId === topicId &&
          s.levelId === levelId &&
          (Number.isNaN(grade) || gradeInRange(s.gradeRange, grade)),
      )
      .map((s: Record<string, unknown>) => {
        const { questions, answerKey, ...rest } = s;
        return rest;
      });
    return NextResponse.json({ sessions });
  }

  // Full session with questions
  if (topicId && levelId && sessionNum) {
    const session = data.sessions.find(
      (s: Record<string, unknown>) =>
        s.topicId === topicId &&
        s.levelId === levelId &&
        s.sessionNumber === parseInt(sessionNum, 10),
    );
    if (!session) {
      return NextResponse.json({ error: 'Session not found' }, { status: 404 });
    }
    return NextResponse.json({ session });
  }

  return NextResponse.json({ error: 'Invalid params' }, { status: 400 });
}
