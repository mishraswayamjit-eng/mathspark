import { NextResponse } from 'next/server';
import { processWeeklyLeagues } from '@/lib/leaderboard';

// GET /api/cron/process-leagues
// Protected by CRON_SECRET header (set in Vercel cron config)
export async function GET(req: Request) {
  const secret = req.headers.get('authorization');

  if (secret !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const result = await processWeeklyLeagues();
    return NextResponse.json({ success: true, ...result });
  } catch (err) {
    console.error('[cron/process-leagues]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
