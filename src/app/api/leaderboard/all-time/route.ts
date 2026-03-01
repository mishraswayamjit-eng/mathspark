import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

// GET /api/leaderboard/all-time?studentId=
export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const studentId = searchParams.get('studentId');

  if (!studentId) {
    return NextResponse.json({ error: 'studentId required' }, { status: 400 });
  }

  try {
    const top = await prisma.student.findMany({
      where:   { hiddenFromLeaderboard: false, totalLifetimeXP: { gt: 0 } },
      orderBy: { totalLifetimeXP: 'desc' },
      take:    50,
      select:  { id: true, name: true, displayName: true, avatarColor: true, totalLifetimeXP: true, currentLeagueTier: true },
    });

    const members = top.map((s, idx) => ({
      studentId:   s.id,
      displayName: s.displayName ?? s.name.split(' ')[0],
      avatarColor:  s.avatarColor,
      totalXP:     s.totalLifetimeXP,
      tier:        s.currentLeagueTier,
      rank:        idx + 1,
      isMe:        s.id === studentId,
    }));

    // If the student isn't in top 50, append their own rank
    const myRankInTop = members.findIndex((m) => m.isMe);
    let myEntry = myRankInTop >= 0 ? members[myRankInTop] : null;

    if (!myEntry) {
      const me = await prisma.student.findUnique({
        where:  { id: studentId },
        select: { id: true, name: true, displayName: true, avatarColor: true, totalLifetimeXP: true, currentLeagueTier: true },
      });
      if (me) {
        const aboveCount = await prisma.student.count({
          where: { hiddenFromLeaderboard: false, totalLifetimeXP: { gt: me.totalLifetimeXP } },
        });
        myEntry = {
          studentId:   me.id,
          displayName: me.displayName ?? me.name.split(' ')[0],
          avatarColor:  me.avatarColor,
          totalXP:     me.totalLifetimeXP,
          tier:        me.currentLeagueTier,
          rank:        aboveCount + 1,
          isMe:        true,
        };
      }
    }

    return NextResponse.json({ members, myEntry });
  } catch (err) {
    console.error('[leaderboard/all-time GET]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
