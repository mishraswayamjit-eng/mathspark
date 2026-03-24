import { MS_PER_HOUR } from '@/lib/timeConstants';
import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { prisma } from '@/lib/db';
import { buildReportEmail, type ReportTopic } from '@/lib/emailReport';
import { TOPIC_ORDER, computeStreak } from '@/lib/sharedUtils';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';

export const dynamic = 'force-dynamic';

function weeklyCorrectCount(
  attempts: Array<{ isCorrect: boolean; createdAt: Date }>,
): number {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);
  return attempts.filter((a) => a.isCorrect && a.createdAt >= cutoff).length;
}

// POST /api/reports/send — on-demand email to parent
// Authenticated via cookie — no body needed
// Rate-limit: 1 email per 24 hours per student (tracked via DB lastReportSentAt)
export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const resend = new Resend(process.env.RESEND_API_KEY);

  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: { id: true, name: true, parentEmail: true, lastReportSentAt: true },
  });
  if (!student) return NextResponse.json({ error: 'Student not found' }, { status: 404 });

  if (!student.parentEmail) {
    return NextResponse.json({ error: 'No parent email configured' }, { status: 400 });
  }

  // Rate limit: 1 send per 24 hours
  if (student.lastReportSentAt) {
    const hoursSince = (Date.now() - student.lastReportSentAt.getTime()) / MS_PER_HOUR;
    if (hoursSince < 24) {
      const hoursLeft = Math.ceil(24 - hoursSince);
      return NextResponse.json(
        { error: `Report already sent. Try again in ${hoursLeft} hour${hoursLeft === 1 ? '' : 's'}.` },
        { status: 429 },
      );
    }
  }

  // Fetch data
  const [progress, attempts, allTopics] = await Promise.all([
    prisma.progress.findMany({ where: { studentId } }),
    prisma.attempt.findMany({
      where: { studentId },
      select: { isCorrect: true, createdAt: true },
      orderBy: { createdAt: 'desc' },
    }),
    prisma.topic.findMany(),
  ]);

  const correctAttempts = attempts.filter((a) => a.isCorrect);
  const topics: ReportTopic[] = allTopics
    .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
    .map((t) => {
      const p = progress.find((x) => x.topicId === t.id);
      return { id: t.id, name: t.name, mastery: p?.mastery ?? 'NotStarted', attempted: p?.attempted ?? 0, correct: p?.correct ?? 0 };
    });

  const appUrl = new URL(req.url).origin;

  const { subject, html } = buildReportEmail({
    studentId,
    studentName:    student.name,
    weeklyCorrect:  weeklyCorrectCount(attempts),
    totalSolved:    correctAttempts.length,
    totalAttempted: attempts.length,
    streakDays:     computeStreak(attempts, true),
    topicsMastered: progress.filter((p) => p.mastery === 'Mastered').length,
    topics,
    appUrl,
  });

  const from = process.env.RESEND_FROM_EMAIL ?? 'MathSpark <onboarding@resend.dev>';

  const { error } = await resend.emails.send({ from, to: student.parentEmail, subject, html });
  if (error) {
    console.error('Resend error:', error);
    return NextResponse.json({ error: 'Failed to send email. Please try again.' }, { status: 500 });
  }

  // Update rate-limit timestamp
  await prisma.student.update({
    where: { id: studentId },
    data: { lastReportSentAt: new Date() },
  });

  return NextResponse.json({ success: true, sentTo: student.parentEmail });
}
