import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getWeekBounds, TIER_NAMES, buildLeagueMembers, leagueDemoteCount } from '@/lib/leaderboard';
import { getDisplayName } from '@/lib/sharedUtils';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { logError } from '@/lib/logger';
import type { LastWeekResult, LeagueData, LeagueMember, WeeklyAwardData } from '@/types';

// GET /api/leaderboard/last-week
export async function GET() {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const { weekStart: currentWeekStart } = getWeekBounds();
    const prevWeekStart = new Date(currentWeekStart.getTime() - 7 * 24 * 60 * 60 * 1000);
    const prevWeekEnd   = new Date(currentWeekStart.getTime() - 1);

    // Find the student's membership from last week
    const membership = await prisma.leagueMembership.findFirst({
      where: {
        studentId,
        league: { weekStart: prevWeekStart },
      },
      include: {
        league: {
          include: {
            members: {
              orderBy: { weeklyXP: 'desc' },
              include: {
                student: {
                  select: { id: true, name: true, displayName: true, avatarColor: true, hiddenFromLeaderboard: true },
                },
              },
            },
          },
        },
      },
    });

    // Weekly awards for student
    const rawAwards = await prisma.weeklyAward.findMany({
      where:   { weekStart: prevWeekStart, studentId },
      include: { student: { select: { name: true, displayName: true } } },
    });

    const awards: WeeklyAwardData[] = rawAwards.map((a) => ({
      awardType:   a.awardType as WeeklyAwardData['awardType'],
      value:       a.value,
      studentId:   a.studentId,
      displayName: getDisplayName(a.student.name, a.student.displayName),
    }));

    if (!membership) {
      const result: LastWeekResult = {
        league:      null,
        myRank:      null,
        promoted:    false,
        demoted:     false,
        awards,
        myPromotion: null,
      };
      return NextResponse.json(result);
    }

    const { league } = membership;
    // Hidden children are not shown to league-mates (they still see themself).
    // Rows stored before small leagues stopped moving anyone down may carry a
    // "demoted" flag that changed nothing (lowest tier) or sits beside
    // "promoted"; those are not shown as a move down.
    const visibleMembers = league.members
      .filter((m) => !m.student.hiddenFromLeaderboard || m.studentId === studentId)
      .map((m) => ({ ...m, demoted: m.demoted && !m.promoted && league.tier > 1 }));
    const members: LeagueMember[] = buildLeagueMembers(visibleMembers, studentId);
    const total  = members.length;
    const promoteCount = Math.max(1, Math.floor(total * 0.2));
    const demoteCount  = leagueDemoteCount(total, league.tier);
    const myDemoted    = membership.demoted && !membership.promoted && league.tier > 1;

    const leagueData: LeagueData = {
      leagueId:     league.id,
      leagueName:   TIER_NAMES[league.tier] ?? 'Bronze',
      tier:         league.tier as 1 | 2 | 3 | 4 | 5,
      weekStart:    prevWeekStart.toISOString(),
      weekEnd:      prevWeekEnd.toISOString(),
      members,
      myRank:       membership.rank ?? total,
      myWeeklyXP:   membership.weeklyXP,
      totalMembers: total,
      promoteCount,
      demoteCount,
    };

    // Check for promotion/demotion
    const student = await prisma.student.findUnique({
      where:  { id: studentId },
      select: { currentLeagueTier: true },
    });
    const currentTier = student?.currentLeagueTier ?? 1;
    const prevTier    = membership.promoted
      ? currentTier - 1
      : myDemoted
        ? currentTier + 1
        : currentTier;

    const myPromotion = membership.promoted && prevTier >= 1 && prevTier <= 4
      ? {
          from: TIER_NAMES[prevTier]  ?? 'Bronze',
          to:   TIER_NAMES[currentTier] ?? 'Silver',
        }
      : null;

    const result: LastWeekResult = {
      league:   leagueData,
      myRank:   membership.rank,
      promoted: membership.promoted,
      demoted:  myDemoted,
      awards,
      myPromotion,
    };

    return NextResponse.json(result, { headers: { 'Cache-Control': 'private, no-store' } });
  } catch (err) {
    logError('[leaderboard/last-week GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
