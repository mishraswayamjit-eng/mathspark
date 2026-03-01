import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/questions/preview
// Returns 3 random Easy questions for the landing page free trial widget.
// No authentication required.
export async function GET() {
  try {
    const count   = await prisma.question.count({ where: { difficulty: 'Medium', source: 'hand_crafted' } });
    const skip    = Math.max(0, Math.floor(Math.random() * Math.max(1, count - 3)));
    const questions = await prisma.question.findMany({
      where:  { difficulty: 'Medium', source: 'hand_crafted' },
      select: {
        id:            true,
        questionText:  true,
        questionLatex: true,
        option1:       true,
        option2:       true,
        option3:       true,
        option4:       true,
        correctAnswer: true,
        hint1:         true,
        topicId:       true,
      },
      skip,
      take:  3,
    });

    return NextResponse.json({ questions });
  } catch {
    return NextResponse.json({ error: 'Failed to load questions' }, { status: 500 });
  }
}
