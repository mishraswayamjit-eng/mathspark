import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getWeekBounds, TIER_NAMES } from '@/lib/leaderboard';
import type { LastWeekResult, LeagueData, LeagueMember, WeeklyAwardData } from '@/types';

// GET /api/leaderboard/last-week?studentId=
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
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
                  select: { id: true, name: true, displayName: true, avatarColor: true },
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
      displayName: a.student.displayName ?? a.student.name.split(' ')[0],
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
    const sorted = league.members; // already ordered by weeklyXP desc
    const total  = sorted.length;
    const promoteCount = Math.max(1, Math.floor(total * 0.2));
    const demoteCount  = Math.max(1, Math.floor(total * 0.2));

    const members: LeagueMember[] = sorted.map((m, idx) => ({
      studentId:   m.studentId,
      displayName: m.student.displayName ?? m.student.name.split(' ')[0],
      avatarColor:  m.student.avatarColor,
      weeklyXP:    m.weeklyXP,
      rank:        m.rank ?? idx + 1,
      isMe:        m.studentId === studentId,
      promoted:    m.promoted,
      demoted:     m.demoted,
    }));

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
      : membership.demoted
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
      demoted:  membership.demoted,
      awards,
      myPromotion,
    };

    return NextResponse.json(result);
  } catch (err) {
    console.error('[leaderboard/last-week GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
