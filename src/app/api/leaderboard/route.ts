import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { ensureCurrentWeekLeague, getWeekBounds, TIER_NAMES } from '@/lib/leaderboard';
import type { LeagueData, LeagueMember } from '@/types';

// GET /api/leaderboard?studentId=
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
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

    // Sort members by weeklyXP desc for live ranks
    const sorted = [...league.members].sort((a, b) => b.weeklyXP - a.weeklyXP);
    const total  = sorted.length;
    const promoteCount = Math.max(1, Math.floor(total * 0.2));
    const demoteCount  = Math.max(1, Math.floor(total * 0.2));

    const members: LeagueMember[] = sorted.map((m, idx) => ({
      studentId:   m.studentId,
      displayName: m.student.displayName ?? m.student.name.split(' ')[0],
      avatarColor:  m.student.avatarColor,
      weeklyXP:    m.weeklyXP,
      rank:        idx + 1,
      isMe:        m.studentId === studentId,
      promoted:    m.promoted,
      demoted:     m.demoted,
    }));

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
    console.error('[leaderboard GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
