// ─── Email report HTML generator ────────────────────────────────────────────
// Pure function — no side effects, easy to test/preview.

const TOPIC_SHORT: Record<string, string> = {
  'ch01-05': 'Numbers',      'ch06': 'Factors',       'ch07-08': 'Fractions',
  'ch09-10': 'Operations',   'ch11': 'Decimals',       'ch12': 'Measurement',
  'ch13': 'Algebra',         'ch14': 'Equations',      'ch15': 'Puzzles',
  'ch16': 'Sequences',       'ch17': 'Time',           'ch18': 'Angles',
  'ch19': 'Triangles',       'ch20': 'Quadrilaterals', 'ch21': 'Circle',
  'dh': 'Data Handling',
};

export interface ReportTopic {
  id: string;
  name: string;
  mastery: string;
  attempted: number;
  correct: number;
}

export interface ReportInput {
  studentId: string;
  studentName: string;
  weeklyCorrect: number;  // correct answers in last 7 days
  totalSolved: number;    // all-time correct
  totalAttempted: number; // all-time attempted
  streakDays: number;
  topicsMastered: number;
  topics: ReportTopic[];
  appUrl: string;         // e.g. https://mathspark.vercel.app
}

function topicName(t: ReportTopic): string {
  return TOPIC_SHORT[t.id] ?? t.name;
}
function topicPct(t: ReportTopic): number {
  return t.attempted > 0 ? Math.round((t.correct / t.attempted) * 100) : 0;
}

export function buildReportEmail(input: ReportInput): { subject: string; html: string } {
  const {
    studentId, studentName, weeklyCorrect, totalSolved, totalAttempted,
    streakDays, topicsMastered, topics, appUrl,
  } = input;

  const accuracy = totalAttempted > 0
    ? Math.round((totalSolved / totalAttempted) * 100) : 0;

  const attempted = topics.filter((t) => t.attempted > 0);
  const topTopics = [...attempted]
    .sort((a, b) => topicPct(b) - topicPct(a))
    .slice(0, 3);
  const bottomTopics = [...attempted]
    .filter((t) => t.mastery !== 'Mastered')
    .sort((a, b) => topicPct(a) - topicPct(b))
    .slice(0, 3);

  const reportDate = new Date().toLocaleDateString('en-IN', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
  });
  const parentLink = `${appUrl}/parent/${studentId}`;

  const subject = `🌟 ${studentName}'s MathSpark Weekly Report`;

  const topicRow = (t: ReportTopic, i: number, color: string) => `
    <tr>
      <td style="padding:9px 14px;background:${i % 2 === 0 ? (color === 'green' ? '#f4fbef' : '#fffbf2') : '#ffffff'};border-radius:8px;">
        <span style="font-size:14px;color:#333;font-weight:600;">${topicName(t)}</span>
      </td>
      <td style="padding:9px 14px;background:${i % 2 === 0 ? (color === 'green' ? '#f4fbef' : '#fffbf2') : '#ffffff'};border-radius:8px;text-align:right;">
        <span style="font-size:14px;font-weight:900;color:${color === 'green' ? '#46a302' : '#cc7800'};">${topicPct(t)}%</span>
      </td>
    </tr>`;

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>${subject}</title>
</head>
<body style="margin:0;padding:0;background:#eef2f7;font-family:Arial,Helvetica,sans-serif;-webkit-font-smoothing:antialiased;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#eef2f7;padding:28px 0;">
  <tr>
    <td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;background:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.10);">

        <!-- HEADER -->
        <tr>
          <td style="background:linear-gradient(135deg,#58CC02 0%,#46a302 100%);padding:36px 28px 28px;text-align:center;">
            <div style="font-size:44px;line-height:1;margin-bottom:10px;">🌟</div>
            <h1 style="color:#ffffff;font-size:26px;font-weight:900;margin:0 0 6px;letter-spacing:-0.5px;">MathSpark Report</h1>
            <p style="color:rgba(255,255,255,0.80);font-size:13px;margin:0;">${reportDate}</p>
          </td>
        </tr>

        <!-- GREETING -->
        <tr>
          <td style="padding:26px 28px 0;">
            <p style="font-size:16px;color:#1a1a2e;margin:0;line-height:1.7;">
              Hi! Here's how <strong style="color:#46a302;">${studentName}</strong> did this week on MathSpark:
            </p>
          </td>
        </tr>

        <!-- STATS 2×2 GRID -->
        <tr>
          <td style="padding:20px 28px 0;">
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td width="48%" style="background:#f4fbef;border:2px solid #c3eaaa;border-radius:14px;padding:18px 14px;text-align:center;">
                  <div style="font-size:32px;font-weight:900;color:#46a302;line-height:1;">${weeklyCorrect}</div>
                  <div style="font-size:12px;color:#555;font-weight:700;margin-top:5px;">📊 Correct this week</div>
                </td>
                <td width="4%"></td>
                <td width="48%" style="background:#fff8ee;border:2px solid #ffd48a;border-radius:14px;padding:18px 14px;text-align:center;">
                  <div style="font-size:32px;font-weight:900;color:#cc7800;line-height:1;">${accuracy}%</div>
                  <div style="font-size:12px;color:#555;font-weight:700;margin-top:5px;">✅ Overall accuracy</div>
                </td>
              </tr>
              <tr><td colspan="3" style="height:12px;"></td></tr>
              <tr>
                <td width="48%" style="background:#fff2f2;border:2px solid #ffbbbb;border-radius:14px;padding:18px 14px;text-align:center;">
                  <div style="font-size:32px;font-weight:900;color:#cc3333;line-height:1;">${streakDays}</div>
                  <div style="font-size:12px;color:#555;font-weight:700;margin-top:5px;">🔥 Day streak</div>
                </td>
                <td width="4%"></td>
                <td width="48%" style="background:#f0f0ff;border:2px solid #c0c0f0;border-radius:14px;padding:18px 14px;text-align:center;">
                  <div style="font-size:32px;font-weight:900;color:#5551e8;line-height:1;">${topicsMastered}<span style="font-size:18px;color:#aaa;font-weight:700;">/16</span></div>
                  <div style="font-size:12px;color:#555;font-weight:700;margin-top:5px;">⭐ Topics mastered</div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        ${topTopics.length > 0 ? `
        <!-- STRONGEST TOPICS -->
        <tr>
          <td style="padding:22px 28px 0;">
            <h3 style="font-size:13px;font-weight:900;color:#46a302;text-transform:uppercase;letter-spacing:0.8px;margin:0 0 10px;">💪 Strongest Topics</h3>
            <table width="100%" cellpadding="0" cellspacing="4">
              ${topTopics.map((t, i) => topicRow(t, i, 'green')).join('')}
            </table>
          </td>
        </tr>` : ''}

        ${bottomTopics.length > 0 ? `
        <!-- NEEDS PRACTICE -->
        <tr>
          <td style="padding:18px 28px 0;">
            <h3 style="font-size:13px;font-weight:900;color:#cc7800;text-transform:uppercase;letter-spacing:0.8px;margin:0 0 10px;">📈 Needs More Practice</h3>
            <table width="100%" cellpadding="0" cellspacing="4">
              ${bottomTopics.map((t, i) => topicRow(t, i, 'amber')).join('')}
            </table>
          </td>
        </tr>` : ''}

        <!-- ENCOURAGEMENT -->
        <tr>
          <td style="padding:22px 28px 0;">
            <div style="background:#f4fbef;border-left:5px solid #58CC02;border-radius:0 12px 12px 0;padding:16px 18px;">
              <p style="font-size:15px;color:#2d4a1e;margin:0;line-height:1.7;">
                Keep encouraging <strong>${studentName}</strong> — they're working hard and growing every day!
                Every question they practice builds math confidence for their future. 🚀
              </p>
            </div>
          </td>
        </tr>

        <!-- CTA BUTTON -->
        <tr>
          <td style="padding:24px 28px;text-align:center;">
            <a href="${parentLink}"
               style="display:inline-block;background:#58CC02;color:#ffffff;font-size:15px;font-weight:900;text-decoration:none;padding:15px 36px;border-radius:100px;border-bottom:4px solid #46a302;letter-spacing:0.3px;">
              View Full Progress →
            </a>
          </td>
        </tr>

        <!-- DIVIDER -->
        <tr><td style="height:1px;background:#f0f0f0;"></td></tr>

        <!-- FOOTER -->
        <tr>
          <td style="padding:18px 28px;text-align:center;">
            <p style="font-size:12px;color:#aaa;margin:0 0 4px;">MathSpark · Grade 4 Math · India</p>
            <p style="font-size:11px;color:#ccc;margin:0;">
              You're receiving this because a parent email was added to ${studentName}'s MathSpark account.
            </p>
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>`.trim();

  return { subject, html };
}
