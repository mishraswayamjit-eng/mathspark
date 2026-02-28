import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { prisma } from '@/lib/db';
import { buildReportEmail, type ReportTopic } from '@/lib/emailReport';

const TOPIC_ORDER = [
  'ch01-05','ch06','ch07-08','ch09-10','ch11','ch12',
  'ch13','ch14','ch15','ch16','ch17','ch18','ch19','ch20','ch21','dh',
];

function weeklyCorrectCount(
  attempts: Array<{ isCorrect: boolean; createdAt: Date }>,
): number {
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - 7);
  return attempts.filter((a) => a.isCorrect && a.createdAt >= cutoff).length;
}

function computeStreak(attempts: Array<{ isCorrect: boolean; createdAt: Date }>): number {
  const days = new Set(
    attempts.filter((a) => a.isCorrect).map((a) => new Date(a.createdAt).toDateString()),
  );
  const today = new Date();
  let streak = 0;
  for (let i = 0; i < 365; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    if (days.has(d.toDateString())) streak++;
    else break;
  }
  return streak;
}

// GET /api/reports/weekly — called by Vercel Cron (Sunday 04:30 UTC = 10:00 AM IST)
// Protected by Authorization: Bearer {CRON_SECRET}
export async function GET(req: Request) {
  const resend = new Resend(process.env.RESEND_API_KEY);
  // Verify cron secret
  const auth = req.headers.get('authorization');
  const cronSecret = process.env.CRON_SECRET;
  if (cronSecret && auth !== `Bearer ${cronSecret}`) {
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

  // Fetch all topics once
  const allTopics = await prisma.topic.findMany();

  let sent = 0, skipped = 0, failed = 0;

  for (const student of students) {
    if (!student.parentEmail) { skipped++; continue; }

    try {
      const [progress, attempts] = await Promise.all([
        prisma.progress.findMany({ where: { studentId: student.id } }),
        prisma.attempt.findMany({
          where: { studentId: student.id },
          select: { isCorrect: true, createdAt: true },
          orderBy: { createdAt: 'desc' },
        }),
      ]);

      const correctAttempts = attempts.filter((a) => a.isCorrect);
      const topics: ReportTopic[] = allTopics
        .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
        .map((t) => {
          const p = progress.find((x) => x.topicId === t.id);
          return { id: t.id, name: t.name, mastery: p?.mastery ?? 'NotStarted', attempted: p?.attempted ?? 0, correct: p?.correct ?? 0 };
        });

      const { subject, html } = buildReportEmail({
        studentId:      student.id,
        studentName:    student.name,
        weeklyCorrect:  weeklyCorrectCount(attempts),
        totalSolved:    correctAttempts.length,
        totalAttempted: attempts.length,
        streakDays:     computeStreak(attempts),
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
