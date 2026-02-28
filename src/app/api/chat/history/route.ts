import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

// GET /api/chat/history?studentId=xxx&sessionId=xxx
// Returns the last session's messages (or a specific session's messages)
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');
  const sessionId = searchParams.get('sessionId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  if (sessionId) {
    // Return specific session
    const session = await prisma.conversationSession.findUnique({
      where: { id: sessionId },
      include: { messages: { orderBy: { createdAt: 'asc' } } },
    });
    if (!session || session.studentId !== studentId) {
      return NextResponse.json({ error: 'Not found' }, { status: 404 });
    }
    return NextResponse.json(session);
  }

  // Return most recent session
  const session = await prisma.conversationSession.findFirst({
    where: { studentId },
    orderBy: { updatedAt: 'desc' },
    include: { messages: { orderBy: { createdAt: 'asc' }, take: 50 } },
  });

  return NextResponse.json(session ?? null);
}
