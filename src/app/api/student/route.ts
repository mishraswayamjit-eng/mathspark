import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { isClean } from '@/lib/profanityFilter';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import bcrypt from 'bcryptjs';

// PATCH /api/student — update mutable student fields
export async function PATCH(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json() as {
      parentEmail?: string;
      parentWhatsApp?: string;
      name?: string;
      displayName?: string;
      avatarColor?: string;
      hiddenFromLeaderboard?: boolean;
      grade?: number;
      examName?: string;
      examDate?: string;
      targetScore?: number;
      dailyGoalMins?: number;
      sessionLengthMins?: number;
      focusTopics?: string[];
      confidentTopics?: string[];
      city?: string;
      preferredPracticeTime?: string;
      pin?: string;
    };

    const data: Record<string, unknown> = {};

    // PIN update — must be exactly 4 digits
    if (typeof body.pin !== 'undefined') {
      if (body.pin === '' || body.pin === null) {
        // Allow clearing PIN
        data.pinHash = null;
      } else if (typeof body.pin === 'string' && /^\d{4}$/.test(body.pin)) {
        data.pinHash = await bcrypt.hash(body.pin, 10);
      } else {
        return NextResponse.json({ error: 'PIN must be exactly 4 digits' }, { status: 400 });
      }
    }

    if (typeof body.parentEmail    !== 'undefined') data.parentEmail    = body.parentEmail    || null;
    if (typeof body.parentWhatsApp !== 'undefined') data.parentWhatsApp = body.parentWhatsApp || null;
    if (typeof body.name           !== 'undefined' && body.name?.trim()) data.name = body.name.trim();
    if (typeof body.avatarColor    !== 'undefined') data.avatarColor = body.avatarColor;
    if (typeof body.hiddenFromLeaderboard !== 'undefined') data.hiddenFromLeaderboard = body.hiddenFromLeaderboard;
    if (typeof body.grade !== 'undefined' && body.grade >= 2 && body.grade <= 9) data.grade = body.grade;
    if (typeof body.examName !== 'undefined') data.examName = body.examName || null;
    if (typeof body.examDate !== 'undefined') {
      data.examDate = body.examDate ? new Date(body.examDate) : null;
    }
    if (typeof body.targetScore !== 'undefined') data.targetScore = body.targetScore ?? null;
    if (typeof body.dailyGoalMins !== 'undefined' && body.dailyGoalMins > 0) data.dailyGoalMins = body.dailyGoalMins;
    if (typeof body.sessionLengthMins !== 'undefined' && body.sessionLengthMins > 0) data.sessionLengthMins = body.sessionLengthMins;
    if (typeof body.focusTopics !== 'undefined') data.focusTopics = JSON.stringify(body.focusTopics ?? []);
    if (typeof body.confidentTopics !== 'undefined') data.confidentTopics = JSON.stringify(body.confidentTopics ?? []);
    if (typeof body.city !== 'undefined') data.city = body.city || null;
    if (typeof body.preferredPracticeTime !== 'undefined') data.preferredPracticeTime = body.preferredPracticeTime || null;

    if (typeof body.displayName !== 'undefined') {
      const trimmed = (body.displayName ?? '').trim().slice(0, 20);
      if (trimmed && !isClean(trimmed)) {
        return NextResponse.json({ error: 'Display name contains inappropriate content.' }, { status: 422 });
      }
      if (trimmed) {
        const taken = await prisma.student.findFirst({
          where:  { displayName: trimmed, id: { not: studentId } },
          select: { id: true },
        });
        if (taken) {
          return NextResponse.json({ error: 'That name is already taken — try adding a number or emoji!' }, { status: 409 });
        }
      }
      data.displayName = trimmed || null;
    }

    if (Object.keys(data).length === 0) {
      return NextResponse.json({ error: 'No fields to update' }, { status: 400 });
    }

    await prisma.student.update({ where: { id: studentId }, data });
    return NextResponse.json({ success: true });
  } catch (err) {
    console.error('[student] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
