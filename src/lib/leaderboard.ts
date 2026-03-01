import { prisma } from '@/lib/db';
import type { LeagueTierName } from '@/types';

// ── Tier metadata ─────────────────────────────────────────────────────────────

export const TIER_NAMES: Record<number, LeagueTierName> = {
  1: 'Bronze',
  2: 'Silver',
  3: 'Gold',
  4: 'Diamond',
  5: 'Champion',
};

const MAX_LEAGUE_SIZE = 25;

// ── Week bounds (IST-aware) ────────────────────────────────────────────────────
// IST = UTC+5:30 (330 minutes ahead)
// Week runs Monday 00:00 IST → Sunday 23:59:59 IST
// In UTC: Monday ~18:30 previous day → Sunday ~18:29:59

export function getWeekBounds(): { weekStart: Date; weekEnd: Date } {
  const now = new Date();

  // Current day in IST
  const istOffsetMs = 330 * 60 * 1000;
  const nowIST      = new Date(now.getTime() + istOffsetMs);

  // Day of week in IST (0 = Sunday, 1 = Monday … 6 = Saturday)
  const dayOfWeekIST = nowIST.getUTCDay(); // 0–6

  // Days since Monday in IST (Monday = 0, Tuesday = 1, … Sunday = 6)
  const daysSinceMonday = dayOfWeekIST === 0 ? 6 : dayOfWeekIST - 1;

  // Monday 00:00 IST
  const mondayIST = new Date(nowIST);
  mondayIST.setUTCDate(mondayIST.getUTCDate() - daysSinceMonday);
  mondayIST.setUTCHours(0, 0, 0, 0);

  // Sunday 23:59:59 IST = 6 days after Monday 00:00 IST + 23:59:59
  const sundayIST = new Date(mondayIST);
  sundayIST.setUTCDate(sundayIST.getUTCDate() + 6);
  sundayIST.setUTCHours(23, 59, 59, 999);

  // Convert back to UTC for DB storage
  const weekStart = new Date(mondayIST.getTime() - istOffsetMs);
  const weekEnd   = new Date(sundayIST.getTime() - istOffsetMs);

  return { weekStart, weekEnd };
}

// ── Ensure student has a league membership for the current week ───────────────

export async function ensureCurrentWeekLeague(studentId: string) {
  const { weekStart, weekEnd } = getWeekBounds();

  // Check for existing membership this week
  const existing = await prisma.leagueMembership.findFirst({
    where: {
      studentId,
      league: { weekStart },
    },
    include: { league: true },
  });

  if (existing) return existing;

  // Get student's current tier and grade
  const student = await prisma.student.findUnique({
    where:  { id: studentId },
    select: { currentLeagueTier: true, grade: true },
  });
  const tier  = student?.currentLeagueTier ?? 1;
  const grade = student?.grade ?? 4;
  const name  = TIER_NAMES[tier] ?? 'Bronze';

  // Find a non-full league for this tier + grade + week
  const league = await (async () => {
    const candidates = await prisma.league.findMany({
      where:   { tier, grade, weekStart },
      include: { _count: { select: { members: true } } },
    });
    return candidates.find((l) => l._count.members < MAX_LEAGUE_SIZE) ?? null;
  })();

  const leagueId = league
    ? league.id
    : (await prisma.league.create({
        data: { name, tier, grade, weekStart, weekEnd },
      })).id;

  const membership = await prisma.leagueMembership.create({
    data:    { studentId, leagueId },
    include: { league: true },
  });

  return membership;
}

// ── Add XP to weekly league + lifetime total ──────────────────────────────────

export async function addWeeklyXP(studentId: string, xpAmount: number): Promise<void> {
  if (xpAmount <= 0) return;

  const membership = await ensureCurrentWeekLeague(studentId);

  const today = new Date();
  today.setUTCHours(0, 0, 0, 0);

  await Promise.all([
    prisma.leagueMembership.update({
      where: { id: membership.id },
      data:  { weeklyXP: { increment: xpAmount } },
    }),
    prisma.student.update({
      where: { id: studentId },
      data:  { totalLifetimeXP: { increment: xpAmount } },
    }),
    prisma.usageLog.upsert({
      where:  { studentId_date: { studentId, date: today } },
      update: { xpEarned: { increment: xpAmount } },
      create: { studentId, date: today, xpEarned: xpAmount },
    }),
  ]);
}

// ── Compute XP for a single attempt ───────────────────────────────────────────

export function computeXPForAttempt(
  isCorrect:       boolean,
  isBonusQuestion: boolean,
  timeTakenMs:     number,
): number {
  if (!isCorrect)         return 0;
  if (timeTakenMs < 3000) return 0; // anti-spam-tap
  if (isBonusQuestion)    return 10;
  return 20;
}

// ── Weekly cron: process league promotions / demotions + awards ───────────────

export async function processWeeklyLeagues(): Promise<{ processed: number }> {
  const { weekStart: currentWeekStart } = getWeekBounds();
  const prevWeekStart = new Date(currentWeekStart.getTime() - 7 * 24 * 60 * 60 * 1000);

  const leagues = await prisma.league.findMany({
    where:   { weekStart: prevWeekStart },
    include: {
      members: {
        orderBy: { weeklyXP: 'desc' },
        include: { student: { select: { id: true, currentLeagueTier: true } } },
      },
    },
  });

  let processed = 0;

  for (const league of leagues) {
    const total        = league.members.length;
    if (total === 0) continue;

    const promoteCount = Math.max(1, Math.floor(total * 0.2));
    const demoteCount  = Math.max(1, Math.floor(total * 0.2));

    const updates = league.members.map((m, idx) => {
      const rank      = idx + 1;
      const promoted  = rank <= promoteCount;
      const demoted   = rank > total - demoteCount;
      const tierDelta = promoted ? 1 : demoted ? -1 : 0;
      const newTier   = Math.min(5, Math.max(1, (m.student.currentLeagueTier ?? 1) + tierDelta));

      return {
        membershipId: m.id,
        rank,
        promoted,
        demoted,
        studentId: m.studentId,
        newTier,
      };
    });

    await prisma.$transaction([
      ...updates.map((u) =>
        prisma.leagueMembership.update({
          where: { id: u.membershipId },
          data:  { rank: u.rank, promoted: u.promoted, demoted: u.demoted },
        }),
      ),
      ...updates.map((u) =>
        prisma.student.update({
          where: { id: u.studentId },
          data:  { currentLeagueTier: u.newTier },
        }),
      ),
    ]);

    await computeAndSaveAwards(league.id, prevWeekStart, league.members);
    processed++;
  }

  return { processed };
}

// ── Compute and save weekly awards for a league ───────────────────────────────

async function computeAndSaveAwards(
  leagueId:   string,
  weekStart:  Date,
  members:    Array<{ studentId: string; weeklyXP: number }>,
) {
  const weekEnd = new Date(weekStart.getTime() + 7 * 24 * 60 * 60 * 1000 - 1);
  const memberIds = members.map((m) => m.studentId);

  const attempts = await prisma.attempt.findMany({
    where: {
      studentId:  { in: memberIds },
      createdAt:  { gte: weekStart, lte: weekEnd },
    },
    select: {
      studentId:   true,
      isCorrect:   true,
      timeTakenMs: true,
      question:    { select: { topicId: true } },
    },
  });

  const awards: Array<{ studentId: string; awardType: string; value: string }> = [];

  // ── most_improved: highest weeklyXP, excluding rank #1 last week ─────────
  const sorted = [...members].sort((a, b) => b.weeklyXP - a.weeklyXP);
  if (sorted.length >= 2) {
    const improved = sorted[1]; // #2 = most improved excluding winner
    awards.push({ studentId: improved.studentId, awardType: 'most_improved', value: `${improved.weeklyXP} XP` });
  }

  // ── speed_demon: most correct answers < 10s (min 5 qualifying) ───────────
  const speedMap: Record<string, number> = {};
  for (const a of attempts) {
    if (a.isCorrect && a.timeTakenMs < 10000 && a.timeTakenMs >= 3000) {
      speedMap[a.studentId] = (speedMap[a.studentId] ?? 0) + 1;
    }
  }
  const speedEntries = Object.entries(speedMap).filter(([, v]) => v >= 5);
  if (speedEntries.length > 0) {
    const [sid, count] = speedEntries.sort((a, b) => b[1] - a[1])[0];
    awards.push({ studentId: sid, awardType: 'speed_demon', value: `${count} fast answers` });
  }

  // ── accuracy_king: highest accuracy, min 5 attempts, ≥ 90% ──────────────
  const accMap: Record<string, { correct: number; total: number }> = {};
  for (const a of attempts) {
    if (!accMap[a.studentId]) accMap[a.studentId] = { correct: 0, total: 0 };
    accMap[a.studentId].total++;
    if (a.isCorrect) accMap[a.studentId].correct++;
  }
  const accEntries = Object.entries(accMap)
    .filter(([, v]) => v.total >= 5 && v.correct / v.total >= 0.9)
    .map(([sid, v]) => ({ sid, pct: v.correct / v.total }))
    .sort((a, b) => b.pct - a.pct);
  if (accEntries.length > 0) {
    const { sid, pct } = accEntries[0];
    awards.push({ studentId: sid, awardType: 'accuracy_king', value: `${Math.round(pct * 100)}% accuracy` });
  }

  // ── explorer: most distinct topics attempted ──────────────────────────────
  const topicMap: Record<string, Set<string>> = {};
  for (const a of attempts) {
    if (!topicMap[a.studentId]) topicMap[a.studentId] = new Set();
    topicMap[a.studentId].add(a.question.topicId);
  }
  const topicEntries = Object.entries(topicMap)
    .map(([sid, s]) => ({ sid, count: s.size }))
    .sort((a, b) => b.count - a.count);
  if (topicEntries.length > 0 && topicEntries[0].count >= 2) {
    const { sid, count } = topicEntries[0];
    awards.push({ studentId: sid, awardType: 'explorer', value: `${count} topics` });
  }

  if (awards.length > 0) {
    await prisma.weeklyAward.createMany({
      data:             awards.map((a) => ({ ...a, weekStart })),
      skipDuplicates:   true,
    });
  }
}
