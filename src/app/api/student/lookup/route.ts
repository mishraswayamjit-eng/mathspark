import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';

// GET /api/student/lookup?email=parent@email.com
// Used by student login page to find children for a given parent email
export async function GET(req: Request) {
  try {
    // Dual-window anti-enumeration guard. The query is keyed by email but the
    // limit is per-IP, so enumeration (many distinct emails from one IP) is
    // throttled by the sustained cap while a genuine parent still has burst room
    // to fix a mistyped email. 3/min burst + 10/hour sustained (was 3/min only),
    // cutting max enumeration throughput from ~180/hr to ~10/hr per IP.
    const ip = req.headers.get('x-forwarded-for')?.split(',')[0] ?? 'unknown';
    if (!checkRateLimit(`lookup-burst:${ip}`, 3, 60_000) ||
        !checkRateLimit(`lookup:${ip}`, 10, 60 * 60_000)) {
      return NextResponse.json({ error: 'Too many requests.' }, { status: 429 });
    }

    const { searchParams } = new URL(req.url);
    const email = searchParams.get('email')?.toLowerCase().trim();
    if (!email) return NextResponse.json({ error: 'email required' }, { status: 400 });

    const parent = await prisma.parent.findUnique({
      where:  { email },
      select: {
        id: true,
        deletedAt: true,
        children: {
          where:   { deletedAt: null },
          select:  { id: true, name: true },
          orderBy: { createdAt: 'asc' },
        },
      },
    });

    // Soft-deleted parents are treated as not-found so deleted accounts
    // can't be discovered or used to bypass child-PIN auth.
    if (!parent || parent.deletedAt) return NextResponse.json({ children: [] });

    return NextResponse.json({ children: parent.children });
  } catch (err) {
    logError('[student/lookup] error:', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
