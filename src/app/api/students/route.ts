import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

const AVATAR_COLORS = [
  '#FF9600', '#58CC02', '#1CB0F6', '#FF4B4B',
  '#9B59B6', '#00BCD4', '#FFC800', '#FF69B4',
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
];

// POST /api/students   body: { name: string; grade?: number; parentEmail?: string }
export async function POST(req: Request) {
  const { name, grade, parentEmail } = await req.json();

  if (!name || typeof name !== 'string' || !name.trim()) {
    return NextResponse.json({ error: 'name is required' }, { status: 400 });
  }

  const avatarColor = AVATAR_COLORS[Math.floor(Math.random() * AVATAR_COLORS.length)];
  const gradeValue  = typeof grade === 'number' && grade >= 2 && grade <= 9 ? grade : 4;

  // 7-day trial for new onboarding students
  const trialExpiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);

  const student = await prisma.student.create({
    data: {
      name:          name.trim(),
      avatarColor,
      grade:         gradeValue,
      trialExpiresAt,
      ...(parentEmail && typeof parentEmail === 'string' && parentEmail.trim()
        ? { parentEmail: parentEmail.trim() }
        : {}),
    },
  });

  return NextResponse.json(student, { status: 201 });
}
