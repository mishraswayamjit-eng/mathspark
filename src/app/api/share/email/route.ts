import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { prisma } from '@/lib/db';
import type {
  LessonCardData, MockTestCardData, BadgeCardData,
  StreakCardData, MasteredCardData,
} from '@/components/ShareCard';

const resend = new Resend(process.env.RESEND_API_KEY);
const FROM   = process.env.RESEND_FROM_EMAIL ?? 'MathSpark <achievements@mathspark.in>';
const APP_URL = process.env.NEXT_PUBLIC_APP_URL ?? 'https://mathspark.in';

// POST /api/share/email
// Body: { studentId, cardType, cardData }
// Sends a beautifully formatted HTML achievement email to the parent.
export async function POST(req: Request) {
  try {
    const { studentId, cardType, cardData } = await req.json() as {
      studentId: string;
      cardType:  string;
      cardData:  Record<string, unknown>;
    };

    if (!studentId || !cardType) {
      return NextResponse.json({ error: 'studentId and cardType required' }, { status: 400 });
    }

    const student = await prisma.student.findUnique({
      where:  { id: studentId },
      select: { name: true, parentEmail: true },
    });

    if (!student?.parentEmail) {
      return NextResponse.json(
        { error: "No parent email set. Add one in your Profile settings." },
        { status: 400 },
      );
    }

    const { subject, html } = buildShareEmail(cardType, cardData, student.name, studentId);

    await resend.emails.send({ from: FROM, to: student.parentEmail, subject, html });

    return NextResponse.json({ success: true, sentTo: student.parentEmail });
  } catch (err) {
    console.error('[share/email]', err);
    return NextResponse.json({ error: 'Failed to send email. Please try again.' }, { status: 500 });
  }
}

// ── Email builder ─────────────────────────────────────────────────────────────

function buildShareEmail(
  cardType: string,
  cardData: Record<string, unknown>,
  studentName: string,
  studentId:   string,
): { subject: string; html: string } {
  const progressUrl = `${APP_URL}/parent/${studentId}`;

  let subject = `🌟 ${studentName}'s MathSpark Achievement!`;
  let headline = '';
  let statsHtml = '';
  let footerNote = '';

  if (cardType === 'lesson') {
    const d = cardData as unknown as LessonCardData;
    const pct = Math.round((d.correct / d.total) * 100);
    subject   = `🏆 ${d.studentName} completed a lesson on MathSpark!`;
    headline  = `${d.studentName} just completed a lesson! 🏆`;
    footerNote = `They've been working hard on <strong>${d.topicName}</strong> — keep encouraging them!`;
    statsHtml  = statRow('📐 Topic',    d.topicEmoji + ' ' + d.topicName)
               + statRow('🎯 Score',    `${d.correct} / ${d.total} correct`)
               + statRow('📊 Accuracy', `${pct}%`)
               + statRow('⭐ XP Earned', `+${d.xp} XP`);
  } else if (cardType === 'mocktest') {
    const d = cardData as unknown as MockTestCardData;
    const timeMin = Math.round(d.timeUsedMs / 60_000);
    subject   = `📝 ${d.studentName} took an IPM Mock Test — ${d.pct}%!`;
    headline  = `${d.studentName} just took an IPM Mock Test! 📝`;
    footerNote = `They scored <strong>${d.score}/${d.totalQ}</strong> — great preparation for the IPM exam!`;
    statsHtml  = statRow('🎯 Score',       `${d.score} / ${d.totalQ}  (${d.pct}%)`)
               + statRow('📊 Grade',       d.gradeLabel)
               + statRow('⏱ Time taken',  `${timeMin} min`)
               + statRow('💪 Strongest',   d.strongTopic)
               + statRow('📚 Focus area',  d.weakTopic);
  } else if (cardType === 'badge') {
    const d = cardData as unknown as BadgeCardData;
    subject   = `🏅 ${d.studentName} earned the ${d.badgeName} badge!`;
    headline  = `${d.studentName} earned a new badge! 🏅`;
    footerNote = `Every badge is a real achievement — they\'re making great progress!`;
    statsHtml  = statRow('🏅 Badge',       d.badgeEmoji + ' ' + d.badgeName)
               + statRow('📋 Description', d.badgeDesc)
               + statRow('📅 Date',        d.date);
  } else if (cardType === 'streak') {
    const d = cardData as unknown as StreakCardData;
    subject   = `🔥 ${d.studentName} is on a ${d.streakDays}-day streak!`;
    headline  = `${d.studentName} is on a ${d.streakDays}-day streak! 🔥`;
    footerNote = `Consistent daily practice is the secret to IPM success. They\'re building an amazing habit!`;
    statsHtml  = statRow('🔥 Streak',  `${d.streakDays} days in a row!`)
               + statRow('📅 Date',    d.date);
  } else if (cardType === 'mastered') {
    const d = cardData as unknown as MasteredCardData;
    subject   = `🏆 ${d.studentName} mastered ${d.topicName} on MathSpark!`;
    headline  = `${d.studentName} mastered ${d.topicName}! 🏆`;
    footerNote = `Mastering a topic means scoring 80%+ consistently. This is a huge milestone!`;
    statsHtml  = statRow('📐 Topic',       d.topicEmoji + ' ' + d.topicName)
               + statRow('✅ Questions',   `${d.questionsTotal} solved`)
               + statRow('📊 Accuracy',    `${d.accuracy}%`)
               + statRow('📅 Days practiced', `${d.daysPracticed} days`);
  }

  const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="margin:0;padding:0;background:#F3F4F6;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:580px;margin:0 auto;padding:32px 16px;">

    <!-- Header -->
    <div style="text-align:center;margin-bottom:24px;">
      <p style="margin:0 0 6px;font-size:13px;color:#6B7280;font-weight:700;letter-spacing:2px;text-transform:uppercase;">MathSpark · Grade 4 IPM Prep</p>
    </div>

    <!-- Card -->
    <div style="background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">

      <!-- Green header band -->
      <div style="background:linear-gradient(135deg,#131F24,#1a3040);padding:28px 28px 24px;">
        <h1 style="margin:0;font-size:22px;color:#fff;font-weight:900;line-height:1.3;">${headline}</h1>
      </div>

      <!-- Stats -->
      <div style="padding:24px 28px;">
        <table style="width:100%;border-collapse:collapse;">
          ${statsHtml}
        </table>

        <p style="margin:20px 0 0;font-size:14px;color:#374151;line-height:1.6;">${footerNote}</p>
      </div>

      <!-- CTA -->
      <div style="padding:0 28px 28px;text-align:center;">
        <a href="${progressUrl}" style="display:inline-block;background:#58CC02;color:#fff;padding:13px 32px;border-radius:100px;font-size:14px;font-weight:800;text-decoration:none;">
          View Full Progress 🎯
        </a>
        <p style="margin:12px 0 0;font-size:12px;color:#9CA3AF;">Tap to see all topics, streaks, and history</p>
      </div>
    </div>

    <!-- Footer -->
    <p style="text-align:center;margin-top:20px;font-size:12px;color:#9CA3AF;">
      MathSpark · Grade 4 Math &amp; IPM Prep ·
      <a href="${APP_URL}" style="color:#9CA3AF;">mathspark.in</a>
    </p>
  </div>
</body>
</html>`;

  return { subject, html };
}

function statRow(label: string, value: string): string {
  return `
  <tr>
    <td style="padding:8px 0;border-bottom:1px solid #F3F4F6;font-size:13px;color:#6B7280;font-weight:600;width:40%;">${label}</td>
    <td style="padding:8px 0;border-bottom:1px solid #F3F4F6;font-size:13px;color:#111827;font-weight:700;">${value}</td>
  </tr>`;
}
