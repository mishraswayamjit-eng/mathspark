import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

export const dynamic = 'force-dynamic';

// GET /api/chat/history?sessionId=xxx
export async function GET(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(req.url);
  const sessionId = searchParams.get('sessionId');

  if (sessionId) {
    // Return specific session
    const session = await prisma.conversationSession.findUnique({
      where: { id: sessionId },
      include: { messages: { orderBy: { createdAt: 'asc' }, take: 100 } },
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
