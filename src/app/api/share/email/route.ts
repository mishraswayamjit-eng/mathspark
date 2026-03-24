import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { escapeHtml } from '@/lib/emailReport';
import { validateBody, ValidationError } from '@/lib/validateBody';
import type {
  LessonCardData, MockTestCardData, BadgeCardData,
  StreakCardData, MasteredCardData,
} from '@/components/ShareCard';

const FROM    = process.env.RESEND_FROM_EMAIL ?? 'MathSpark <achievements@mathspark.in>';
const APP_URL = process.env.NEXT_PUBLIC_APP_URL ?? 'https://mathspark.in';

// POST /api/share/email
// Body: { cardType, cardData }
// Sends a beautifully formatted HTML achievement email to the parent.
export async function POST(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Rate limit: 5 share emails per 10 minutes per student
    if (!checkRateLimit(`share-email:${studentId}`, 5, 600_000)) {
      return NextResponse.json({ error: 'Too many share emails. Try again later.' }, { status: 429 });
    }

    const resend = new Resend(process.env.RESEND_API_KEY);
    const { cardType, cardData } = validateBody<{
      cardType: string;
      cardData: Record<string, unknown>;
    }>(
      await req.json(),
      { cardType: 'string', cardData: 'object' },
    );

    if (!cardType) {
      return NextResponse.json({ error: 'cardType required' }, { status: 400 });
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

    const { subject, html } = buildShareEmail(cardType, cardData, escapeHtml(student.name), studentId);

    await resend.emails.send({ from: FROM, to: student.parentEmail, subject, html });

    return NextResponse.json({ success: true, sentTo: student.parentEmail });
  } catch (err) {
    if (err instanceof ValidationError) {
      return NextResponse.json({ error: err.message }, { status: 400 });
    }
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
  const esc = escapeHtml; // shorthand

  let subject = `🌟 ${studentName}'s MathSpark Achievement!`;
  let headline = '';
  let statsHtml = '';
  let footerNote = '';

  if (cardType === 'lesson') {
    const d = cardData as unknown as LessonCardData;
    const pct = Math.round((d.correct / d.total) * 100);
    const name = esc(String(d.studentName ?? studentName));
    const topic = esc(String(d.topicName ?? ''));
    subject   = `🏆 ${name} completed a lesson on MathSpark!`;
    headline  = `${name} just completed a lesson! 🏆`;
    footerNote = `They've been working hard on <strong>${topic}</strong> — keep encouraging them!`;
    statsHtml  = statRow('📐 Topic',    esc(String(d.topicEmoji ?? '')) + ' ' + topic)
               + statRow('🎯 Score',    `${Number(d.correct) || 0} / ${Number(d.total) || 0} correct`)
               + statRow('📊 Accuracy', `${pct}%`)
               + statRow('⭐ XP Earned', `+${Number(d.xp) || 0} XP`);
  } else if (cardType === 'mocktest') {
    const d = cardData as unknown as MockTestCardData;
    const timeMin = Math.round((Number(d.timeUsedMs) || 0) / 60_000);
    const name = esc(String(d.studentName ?? studentName));
    subject   = `📝 ${name} took an IPM Mock Test — ${Number(d.pct) || 0}%!`;
    headline  = `${name} just took an IPM Mock Test! 📝`;
    footerNote = `They scored <strong>${Number(d.score) || 0}/${Number(d.totalQ) || 0}</strong> — great preparation for the IPM exam!`;
    statsHtml  = statRow('🎯 Score',       `${Number(d.score) || 0} / ${Number(d.totalQ) || 0}  (${Number(d.pct) || 0}%)`)
               + statRow('📊 Grade',       esc(String(d.gradeLabel ?? '')))
               + statRow('⏱ Time taken',  `${timeMin} min`)
               + statRow('💪 Strongest',   esc(String(d.strongTopic ?? '')))
               + statRow('📚 Focus area',  esc(String(d.weakTopic ?? '')));
  } else if (cardType === 'badge') {
    const d = cardData as unknown as BadgeCardData;
    const name = esc(String(d.studentName ?? studentName));
    const badge = esc(String(d.badgeName ?? ''));
    subject   = `🏅 ${name} earned the ${badge} badge!`;
    headline  = `${name} earned a new badge! 🏅`;
    footerNote = `Every badge is a real achievement — they're making great progress!`;
    statsHtml  = statRow('🏅 Badge',       esc(String(d.badgeEmoji ?? '')) + ' ' + badge)
               + statRow('📋 Description', esc(String(d.badgeDesc ?? '')))
               + statRow('📅 Date',        esc(String(d.date ?? '')));
  } else if (cardType === 'streak') {
    const d = cardData as unknown as StreakCardData;
    const name = esc(String(d.studentName ?? studentName));
    const days = Number(d.streakDays) || 0;
    subject   = `🔥 ${name} is on a ${days}-day streak!`;
    headline  = `${name} is on a ${days}-day streak! 🔥`;
    footerNote = `Consistent daily practice is the secret to IPM success. They're building an amazing habit!`;
    statsHtml  = statRow('🔥 Streak',  `${days} days in a row!`)
               + statRow('📅 Date',    esc(String(d.date ?? '')));
  } else if (cardType === 'mastered') {
    const d = cardData as unknown as MasteredCardData;
    const name = esc(String(d.studentName ?? studentName));
    const topic = esc(String(d.topicName ?? ''));
    subject   = `🏆 ${name} mastered ${topic} on MathSpark!`;
    headline  = `${name} mastered ${topic}! 🏆`;
    footerNote = `Mastering a topic means scoring 80%+ consistently. This is a huge milestone!`;
    statsHtml  = statRow('📐 Topic',       esc(String(d.topicEmoji ?? '')) + ' ' + topic)
               + statRow('✅ Questions',   `${Number(d.questionsTotal) || 0} solved`)
               + statRow('📊 Accuracy',    `${Number(d.accuracy) || 0}%`)
               + statRow('📅 Days practiced', `${Number(d.daysPracticed) || 0} days`);
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
