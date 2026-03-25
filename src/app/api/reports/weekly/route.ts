import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { prisma } from '@/lib/db';
import { buildReportEmail, type ReportTopic } from '@/lib/emailReport';
import { TOPIC_ORDER, computeStreak } from '@/lib/sharedUtils';

export const dynamic = 'force-dynamic';

function weeklyCorrectCount(
  attempts: Array<{ isCorrect: boolean; createdAt: Date }>,
): number {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);
  return attempts.filter((a) => a.isCorrect && a.createdAt >= cutoff).length;
}

// GET /api/reports/weekly — called by Vercel Cron (Sunday 04:30 UTC = 10:00 AM IST)
// Protected by Authorization: Bearer {CRON_SECRET}
export async function GET(req: Request) {
  const resend = new Resend(process.env.RESEND_API_KEY);
  // Verify cron secret (mandatory — reject if unset)
  const cronSecret = process.env.CRON_SECRET;
  if (!cronSecret) {
    console.error('[reports/weekly] CRON_SECRET is not set');
    return NextResponse.json({ error: 'Server misconfigured' }, { status: 500 });
  }
  const auth = req.headers.get('authorization');
  if (auth !== `Bearer ${cronSecret}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const appUrl = new URL(req.url).origin;
  const from   = process.env.RESEND_FROM_EMAIL ?? 'MathSpark <onboarding@resend.dev>';

  // Fetch all students with a parent email
  const students = await prisma.student.findMany({
    where: { parentEmail: { not: null } },
    select: { id: true, name: true, parentEmail: true },
  });

  if (students.length === 0) {
    return NextResponse.json({ sent: 0, skipped: 0, failed: 0, message: 'No students with parent email' });
  }

  // Batch-fetch all data upfront (eliminates N+1)
  const studentIds = students.map((s) => s.id);
  const [allTopics, allProgress, allAttempts] = await Promise.all([
    prisma.topic.findMany(),
    prisma.progress.findMany({ where: { studentId: { in: studentIds } } }),
    prisma.attempt.findMany({
      where: { studentId: { in: studentIds } },
      select: { studentId: true, isCorrect: true, createdAt: true },
      orderBy: { createdAt: 'desc' },
    }),
  ]);

  // Group by studentId for O(1) lookup
  const progressByStudent = new Map<string, typeof allProgress>();
  for (const p of allProgress) {
    const arr = progressByStudent.get(p.studentId) ?? [];
    arr.push(p);
    progressByStudent.set(p.studentId, arr);
  }
  const attemptsByStudent = new Map<string, typeof allAttempts>();
  for (const a of allAttempts) {
    const arr = attemptsByStudent.get(a.studentId) ?? [];
    arr.push(a);
    attemptsByStudent.set(a.studentId, arr);
  }

  let sent = 0, skipped = 0, failed = 0;

  for (const student of students) {
    if (!student.parentEmail) { skipped++; continue; }

    try {
      const progress = progressByStudent.get(student.id) ?? [];
      const attempts = attemptsByStudent.get(student.id) ?? [];

      const correctAttempts = attempts.filter((a) => a.isCorrect);
      const progressMap = new Map(progress.map((p) => [p.topicId, p]));
      const topics: ReportTopic[] = allTopics
        .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
        .map((t) => {
          const p = progressMap.get(t.id);
          return { id: t.id, name: t.name, mastery: p?.mastery ?? 'NotStarted', attempted: p?.attempted ?? 0, correct: p?.correct ?? 0 };
        });

      const { subject, html } = buildReportEmail({
        studentId:      student.id,
        studentName:    student.name,
        weeklyCorrect:  weeklyCorrectCount(attempts),
        totalSolved:    correctAttempts.length,
        totalAttempted: attempts.length,
        streakDays:     computeStreak(attempts, true),
        topicsMastered: progress.filter((p) => p.mastery === 'Mastered').length,
        topics,
        appUrl,
      });

      const { error } = await resend.emails.send({
        from,
        to: student.parentEmail,
        subject,
        html,
      });

      if (error) {
        console.error(`Failed for ${student.id}:`, error);
        failed++;
      } else {
        sent++;
      }
    } catch (err) {
      console.error(`Error processing student ${student.id}:`, err);
      failed++;
    }
  }

  return NextResponse.json({ sent, skipped, failed, total: students.length });
}
