import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

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
    return NextResponse.json({ meta: data.meta, topics: data.topics });
  }

  // Topic + level — return matching sessions (without questions)
  if (topicId && levelId && !sessionNum) {
    const sessions = data.sessions
      .filter((s: Record<string, unknown>) => s.topicId === topicId && s.levelId === levelId)
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
