import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/db';

// GET /api/parent/children — list parent's children
export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const children = await prisma.student.findMany({
    where: { parentId: session.user.id },
    select: {
      id:                      true,
      name:                    true,
      grade:                   true,
      createdAt:               true,
      subscriptionId:          true,
      dailyUsageMinutes:       true,
      lastActiveDate:          true,
      aiChatMessagesUsedToday: true,
      subscription: {
        select: { name: true, tier: true, dailyLimitMinutes: true, aiChatDailyLimit: true },
      },
    },
    orderBy: { createdAt: 'asc' },
  });

  return NextResponse.json({ children });
}

// POST /api/parent/children — add a child
export async function POST(req: Request) {
  const session = await getServerSession(authOptions);
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const { name, grade } = await req.json() as { name: string; grade?: number };
    if (!name?.trim()) {
      return NextResponse.json({ error: 'Child name is required.' }, { status: 400 });
    }
    if (!grade || grade < 2 || grade > 9) {
      return NextResponse.json({ error: 'Grade must be between 2 and 9.' }, { status: 400 });
    }

    const count = await prisma.student.count({ where: { parentId: session.user.id } });
    if (count >= 5) {
      return NextResponse.json({ error: 'Maximum 5 children per account.' }, { status: 400 });
    }

    const child = await prisma.student.create({
      data: {
        name:     name.trim().slice(0, 60),
        grade,
        parentId: session.user.id,
      },
    });

    return NextResponse.json({ id: child.id, name: child.name, grade: child.grade }, { status: 201 });
  } catch {
    return NextResponse.json({ error: 'Something went wrong.' }, { status: 500 });
  }
}
