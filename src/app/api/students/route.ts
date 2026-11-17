import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { MS_PER_DAY } from '@/lib/timeConstants';
import { logError } from '@/lib/logger';
import bcrypt from 'bcryptjs';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

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
      {
        name: 'string', grade: 'number?', parentEmail: 'string?', examName: 'string?',
        focusTopics: 'array?', confidentTopics: 'array?',
        dailyGoalMins: 'number?', preferredPracticeTime: 'string?', pin: 'string?',
      },
    );

    // Same bounds as PATCH /api/student, so sign-up cannot store what an edit could not.
    const cleanName = name.trim().slice(0, 50);
    if (!cleanName) {
      return NextResponse.json({ error: 'name is required' }, { status: 400 });
    }
    const cleanEmail = typeof parentEmail === 'string' ? parentEmail.trim().toLowerCase().slice(0, 254) : '';
    // Required: the parent email is the only way a child signs in again later
    // (new phone, after logging out, or when the 30-day session ends).
    if (!cleanEmail || !EMAIL_RE.test(cleanEmail)) {
      return NextResponse.json({ error: 'Please check the parent email address.' }, { status: 400 });
    }
    const cleanExamName = typeof examName === 'string' ? examName.trim().slice(0, 100) : '';
    const cleanPracticeTime = typeof preferredPracticeTime === 'string' ? preferredPracticeTime.trim().slice(0, 50) : '';
    const cleanTopics = (list: unknown[]): string[] =>
      list.filter((t): t is string => typeof t === 'string').slice(0, 50).map((t) => t.slice(0, 50));

    // PIN is mandatory — every account must have one so a session can never be
    // issued without a verified PIN (closes the account-takeover hole where any
    // known studentId yielded a login).
    if (typeof pin !== 'string' || !/^\d{4}$/.test(pin)) {
      return NextResponse.json({ error: 'A 4-digit PIN is required' }, { status: 400 });
    }
    const pinHash = await bcrypt.hash(pin, 10);

    const avatarColor = AVATAR_COLORS[Math.floor(Math.random() * AVATAR_COLORS.length)];
    const gradeValue  = typeof grade === 'number' && Math.floor(grade) === grade && grade >= 2 && grade <= 9 ? grade : 4;

    // 7-day trial for new onboarding students
    const trialExpiresAt = new Date(Date.now() + 7 * MS_PER_DAY);

    const student = await prisma.student.create({
      data: {
        name:          cleanName,
        avatarColor,
        grade:         gradeValue,
        trialExpiresAt,
        pinHash,
        ...(cleanEmail ? { parentEmail: cleanEmail } : {}),
        ...(cleanExamName ? { examName: cleanExamName } : {}),
        ...(Array.isArray(focusTopics) ? { focusTopics: JSON.stringify(cleanTopics(focusTopics)) } : {}),
        ...(Array.isArray(confidentTopics) ? { confidentTopics: JSON.stringify(cleanTopics(confidentTopics)) } : {}),
        ...(typeof dailyGoalMins === 'number' && dailyGoalMins > 0 ? { dailyGoalMins: Math.min(600, Math.round(dailyGoalMins)) } : {}),
        ...(cleanPracticeTime ? { preferredPracticeTime: cleanPracticeTime } : {}),
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
    logError('[students] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
