import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { MS_PER_DAY } from '@/lib/timeConstants';
import bcrypt from 'bcryptjs';

const AVATAR_COLORS = [
  '#FF9600', '#58CC02', '#1CB0F6', '#FF4B4B',
  '#9B59B6', '#00BCD4', '#FFC800', '#FF69B4',
  '#3B82F6', '#10B981', '#F59E0B', '#EF4444',
];

// POST /api/students   body: { name: string; grade?: number; parentEmail?: string }
export async function POST(req: Request) {
  try {
    // Rate limit: 5 student creations per IP per 10 minutes
    const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
    if (!checkRateLimit(`create-student:${ip}`, 5, 600_000)) {
      return NextResponse.json({ error: 'Too many requests. Try again later.' }, { status: 429 });
    }

    const { name, grade, parentEmail, examName, focusTopics, confidentTopics, dailyGoalMins, preferredPracticeTime, pin } = validateBody<{
      name: string; grade?: number; parentEmail?: string; examName?: string;
      focusTopics?: unknown[]; confidentTopics?: unknown[];
      dailyGoalMins?: number; preferredPracticeTime?: string; pin?: string;
    }>(
      await req.json(),
      { name: 'string', grade: 'number?', parentEmail: 'string?', examName: 'string?', dailyGoalMins: 'number?', preferredPracticeTime: 'string?', pin: 'string?' },
    );

    if (!name.trim()) {
      return NextResponse.json({ error: 'name is required' }, { status: 400 });
    }

    // Validate PIN if provided — must be exactly 4 digits
    let pinHash: string | undefined;
    if (pin !== undefined && pin !== null && pin !== '') {
      if (typeof pin !== 'string' || !/^\d{4}$/.test(pin)) {
        return NextResponse.json({ error: 'PIN must be exactly 4 digits' }, { status: 400 });
      }
      pinHash = await bcrypt.hash(pin, 10);
    }

    const avatarColor = AVATAR_COLORS[Math.floor(Math.random() * AVATAR_COLORS.length)];
    const gradeValue  = typeof grade === 'number' && grade >= 2 && grade <= 9 ? grade : 4;

    // 7-day trial for new onboarding students
    const trialExpiresAt = new Date(Date.now() + 7 * MS_PER_DAY);

    const student = await prisma.student.create({
      data: {
        name:          name.trim(),
        avatarColor,
        grade:         gradeValue,
        trialExpiresAt,
        ...(pinHash ? { pinHash } : {}),
        ...(parentEmail && typeof parentEmail === 'string' && parentEmail.trim()
          ? { parentEmail: parentEmail.trim() }
          : {}),
        ...(examName && typeof examName === 'string' ? { examName } : {}),
        ...(Array.isArray(focusTopics) ? { focusTopics: JSON.stringify(focusTopics) } : {}),
        ...(Array.isArray(confidentTopics) ? { confidentTopics: JSON.stringify(confidentTopics) } : {}),
        ...(typeof dailyGoalMins === 'number' && dailyGoalMins > 0 ? { dailyGoalMins } : {}),
        ...(preferredPracticeTime && typeof preferredPracticeTime === 'string' ? { preferredPracticeTime } : {}),
      },
    });

    return NextResponse.json({
      id: student.id,
      name: student.name,
      grade: student.grade,
      avatarColor: student.avatarColor,
      trialExpiresAt: student.trialExpiresAt,
    }, { status: 201 });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    console.error('[students] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
