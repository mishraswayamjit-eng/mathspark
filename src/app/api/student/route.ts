import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { isClean } from '@/lib/profanityFilter';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import bcrypt from 'bcryptjs';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const HEX_COLOR_RE = /^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/;

// Keep a sanitized string: trim, cap length. Empty → null.
function cleanStr(v: string, max: number): string | null {
  const t = v.trim().slice(0, max);
  return t || null;
}

// PATCH /api/student — update mutable student fields
export async function PATCH(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    let rawBody: unknown;
    try {
      rawBody = await req.json();
    } catch {
      return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
    }

    const body = validateBody<{
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
      focusTopics?: unknown[];
      confidentTopics?: unknown[];
      city?: string;
      preferredPracticeTime?: string;
      pin?: string;
    }>(rawBody, {
      parentEmail: 'string?', parentWhatsApp: 'string?', name: 'string?',
      displayName: 'string?', avatarColor: 'string?', hiddenFromLeaderboard: 'boolean?',
      grade: 'number?', examName: 'string?', examDate: 'string?', targetScore: 'number?',
      dailyGoalMins: 'number?', sessionLengthMins: 'number?',
      focusTopics: 'array?', confidentTopics: 'array?',
      city: 'string?', preferredPracticeTime: 'string?', pin: 'string?',
    });

    const data: Record<string, unknown> = {};

    // PIN update — must be exactly 4 digits. Clearing is NOT allowed: a PIN is
    // mandatory, so an account can only ever change to a new valid PIN.
    if (typeof body.pin !== 'undefined') {
      if (typeof body.pin === 'string' && /^\d{4}$/.test(body.pin)) {
        data.pinHash = await bcrypt.hash(body.pin, 10);
      } else {
        return NextResponse.json({ error: 'PIN must be exactly 4 digits' }, { status: 400 });
      }
    }

    // parentEmail is an email *sink* (weekly reports are sent here) — it must be a
    // valid, length-bounded address, never arbitrary free text.
    if (typeof body.parentEmail !== 'undefined') {
      const email = (body.parentEmail ?? '').trim().toLowerCase().slice(0, 254);
      if (email && !EMAIL_RE.test(email)) {
        return NextResponse.json({ error: 'Enter a valid parent email address.' }, { status: 400 });
      }
      data.parentEmail = email || null;
    }
    if (typeof body.parentWhatsApp !== 'undefined') {
      const wa = (body.parentWhatsApp ?? '').replace(/[^\d+\s-]/g, '').trim().slice(0, 20);
      data.parentWhatsApp = wa || null;
    }
    if (typeof body.name !== 'undefined') {
      const n = (body.name ?? '').trim().slice(0, 50);
      if (n) data.name = n;
    }
    if (typeof body.avatarColor !== 'undefined') {
      if (!HEX_COLOR_RE.test(body.avatarColor ?? '')) {
        return NextResponse.json({ error: 'Invalid avatar color.' }, { status: 400 });
      }
      data.avatarColor = body.avatarColor;
    }
    if (typeof body.hiddenFromLeaderboard !== 'undefined') data.hiddenFromLeaderboard = body.hiddenFromLeaderboard;
    if (typeof body.grade !== 'undefined' && body.grade >= 2 && body.grade <= 9) data.grade = body.grade;
    if (typeof body.examName !== 'undefined') data.examName = cleanStr(body.examName ?? '', 100);
    if (typeof body.examDate !== 'undefined') {
      if (body.examDate) {
        const d = new Date(body.examDate);
        if (isNaN(d.getTime())) {
          return NextResponse.json({ error: 'Invalid exam date.' }, { status: 400 });
        }
        data.examDate = d;
      } else {
        data.examDate = null;
      }
    }
    if (typeof body.targetScore !== 'undefined') {
      data.targetScore = body.targetScore == null ? null : Math.max(0, Math.min(1000, Math.round(body.targetScore)));
    }
    if (typeof body.dailyGoalMins !== 'undefined' && body.dailyGoalMins > 0) {
      data.dailyGoalMins = Math.min(600, Math.round(body.dailyGoalMins));
    }
    if (typeof body.sessionLengthMins !== 'undefined' && body.sessionLengthMins > 0) {
      data.sessionLengthMins = Math.min(600, Math.round(body.sessionLengthMins));
    }
    if (typeof body.focusTopics !== 'undefined') {
      const list = (body.focusTopics ?? []).filter((t): t is string => typeof t === 'string').slice(0, 50).map((t) => t.slice(0, 50));
      data.focusTopics = JSON.stringify(list);
    }
    if (typeof body.confidentTopics !== 'undefined') {
      const list = (body.confidentTopics ?? []).filter((t): t is string => typeof t === 'string').slice(0, 50).map((t) => t.slice(0, 50));
      data.confidentTopics = JSON.stringify(list);
    }
    if (typeof body.city !== 'undefined') data.city = cleanStr(body.city ?? '', 100);
    if (typeof body.preferredPracticeTime !== 'undefined') data.preferredPracticeTime = cleanStr(body.preferredPracticeTime ?? '', 50);

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
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
    logError('[student] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
