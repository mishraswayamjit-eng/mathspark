import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';

// GET /api/student/lookup?email=parent@email.com
// Used by student login page to find children for a given parent email
export async function GET(req: Request) {
  try {
    const ip = req.headers.get('x-forwarded-for')?.split(',')[0] ?? 'unknown';
    if (!checkRateLimit(`lookup:${ip}`, 3, 60_000)) {
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
