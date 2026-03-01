import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { isClean } from '@/lib/profanityFilter';

// PATCH /api/student — update mutable student fields
export async function PATCH(req: Request) {
  const body = await req.json() as {
    studentId?: string;
    parentEmail?: string;
    parentWhatsApp?: string;
    name?: string;
    displayName?: string;
    avatarColor?: string;
    hiddenFromLeaderboard?: boolean;
    grade?: number;
  };
  const { studentId, parentEmail, parentWhatsApp, name, displayName, avatarColor, hiddenFromLeaderboard, grade } = body;

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  const data: Record<string, unknown> = {};
  if (typeof parentEmail    !== 'undefined') data.parentEmail    = parentEmail    || null;
  if (typeof parentWhatsApp !== 'undefined') data.parentWhatsApp = parentWhatsApp || null;
  if (typeof name           !== 'undefined' && name.trim()) data.name = name.trim();
  if (typeof avatarColor    !== 'undefined') data.avatarColor = avatarColor;
  if (typeof hiddenFromLeaderboard !== 'undefined') data.hiddenFromLeaderboard = hiddenFromLeaderboard;
  if (typeof grade !== 'undefined' && grade >= 2 && grade <= 9) data.grade = grade;

  if (typeof displayName !== 'undefined') {
    const trimmed = displayName.trim().slice(0, 20);
    if (trimmed && !isClean(trimmed)) {
      return NextResponse.json({ error: 'Display name contains inappropriate content.' }, { status: 422 });
    }
    data.displayName = trimmed || null;
  }

  if (Object.keys(data).length === 0) {
    return NextResponse.json({ error: 'No fields to update' }, { status: 400 });
  }

  await prisma.student.update({ where: { id: studentId }, data });
  return NextResponse.json({ success: true });
}
