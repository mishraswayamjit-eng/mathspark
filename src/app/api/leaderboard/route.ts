import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { ensureCurrentWeekLeague, getWeekBounds, TIER_NAMES, buildLeagueMembers } from '@/lib/leaderboard';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { logError } from '@/lib/logger';
import type { LeagueData, LeagueMember } from '@/types';

// GET /api/leaderboard
export async function GET() {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    // Ensure the student has a league for this week
    await ensureCurrentWeekLeague(studentId);

    const { weekStart, weekEnd } = getWeekBounds();

    // Get the student's current membership
    const membership = await prisma.leagueMembership.findFirst({
      where:   { studentId, league: { weekStart } },
      include: { league: { include: { members: { include: { student: { select: { id: true, name: true, displayName: true, avatarColor: true, hiddenFromLeaderboard: true } } } } } } },
    });

    if (!membership) {
      return NextResponse.json({ error: 'League not found' }, { status: 404 });
    }

    const { league } = membership;

    // Build ranked members (live ranks by weeklyXP desc)
    const members: LeagueMember[] = buildLeagueMembers(league.members, studentId);
    const total  = members.length;
    const promoteCount = Math.max(1, Math.floor(total * 0.2));
    const demoteCount  = Math.max(1, Math.floor(total * 0.2));

    const myMember = members.find((m) => m.isMe);

    const data: LeagueData = {
      leagueId:     league.id,
      leagueName:   TIER_NAMES[league.tier] ?? 'Bronze',
      tier:         league.tier as 1 | 2 | 3 | 4 | 5,
      weekStart:    weekStart.toISOString(),
      weekEnd:      weekEnd.toISOString(),
      members,
      myRank:       myMember?.rank ?? total,
      myWeeklyXP:   membership.weeklyXP,
      totalMembers: total,
      promoteCount,
      demoteCount,
    };

    return NextResponse.json(data);
  } catch (err) {
    logError('[leaderboard GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
