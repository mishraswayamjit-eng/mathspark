import { NextResponse } from 'next/server';
import { z } from 'zod';
import { getNextQuestion } from '@/lib/adaptive';

const DifficultyEnum = z.enum(['Easy', 'Medium', 'Hard']);

// Shared schema for POST body
const NextQuestionSchema = z.object({
  topicId:   z.string().min(1),
  studentId: z.string().min(1),
  exclude:   z.array(z.string()).default([]),
  cw:        z.number().int().min(0).max(20).default(0),  // consecutive wrong
  cr:        z.number().int().min(0).max(20).default(0),  // consecutive right
});

// GET /api/questions/next?topicId=&studentId=&exclude=id1,id2&cw=0&cr=0&difficulty=Easy
export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);

    const GetSchema = z.object({
      topicId:    z.string().min(1),
      studentId:  z.string().min(1),
      cw:         z.coerce.number().int().min(0).max(20).default(0),
      cr:         z.coerce.number().int().min(0).max(20).default(0),
      difficulty: DifficultyEnum.optional(),
    });

    const parsed = GetSchema.safeParse({
      topicId:    searchParams.get('topicId')   ?? '',
      studentId:  searchParams.get('studentId') ?? '',
      cw:         searchParams.get('cw')        ?? '0',
      cr:         searchParams.get('cr')        ?? '0',
      difficulty: searchParams.get('difficulty') ?? undefined,
    });

    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }

    const { topicId, studentId, cw, cr } = parsed.data;

    const excludeRaw = searchParams.get('exclude') ?? '';
    const exclude    = excludeRaw ? excludeRaw.split(',').filter(Boolean) : [];

    const question = await getNextQuestion(studentId, topicId, exclude, cw, cr);

    if (!question) {
      return NextResponse.json({ error: 'No more questions available' }, { status: 404 });
    }

    return NextResponse.json({
      ...question,
      stepByStep: typeof question.stepByStep === 'string'
        ? JSON.parse(question.stepByStep)
        : question.stepByStep,
    });
  } catch (err) {
    console.error('[GET /api/questions/next]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

// POST /api/questions/next
// Body: { topicId, studentId, exclude: string[], cw: number, cr: number }
// Avoids URL-length limits when seenIds list grows large (400+ IDs ≈ 5.5 KB)
export async function POST(req: Request) {
  try {
    const parsed = NextQuestionSchema.safeParse(await req.json());
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
    }

    const { topicId, studentId, exclude, cw, cr } = parsed.data;

    const question = await getNextQuestion(studentId, topicId, exclude, cw, cr);
    if (!question) {
      return NextResponse.json({ error: 'No more questions' }, { status: 404 });
    }

    return NextResponse.json({
      ...question,
      stepByStep: typeof question.stepByStep === 'string'
        ? JSON.parse(question.stepByStep)
        : question.stepByStep,
    });
  } catch (err) {
    console.error('[POST /api/questions/next]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
