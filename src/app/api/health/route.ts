import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';

export const dynamic = 'force-dynamic';

// GET /api/health — basic health check
export async function GET() {
  let db = false;

  try {
    await prisma.$queryRaw`SELECT 1`;
    db = true;
  } catch {
    // DB unreachable
  }

  const envOk =
    !!process.env.NEXTAUTH_SECRET &&
    !!process.env.DATABASE_URL;

  const status = db && envOk ? 'ok' : 'degraded';

  return NextResponse.json(
    {
      status,
      db,
      envOk,
      uptime: process.uptime(),
    },
    { status: status === 'ok' ? 200 : 503 },
  );
}
