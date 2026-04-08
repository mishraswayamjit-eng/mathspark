import { NextResponse } from 'next/server';
import { processWeeklyLeagues } from '@/lib/leaderboard';
import { verifyCronSecret } from '@/lib/adminAuth';

// GET /api/cron/process-leagues
// Protected by CRON_SECRET header (set in Vercel cron config)
export async function GET(req: Request) {
  if (!verifyCronSecret(req.headers.get('authorization'))) {
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
