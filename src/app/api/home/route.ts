import { NextResponse } from 'next/server';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { logError } from '@/lib/logger';
import { loadHomeData } from '@/lib/student/homeData';
import { loadStudentBootstrap } from '@/lib/student/bootstrap';

export const dynamic = 'force-dynamic';
// NOTE: maxDuration is ignored on Vercel Hobby (10s hard limit). Only effective on Pro+.
export const maxDuration = 30;

// Per-child data: never stored by the browser or any shared cache.
const NO_STORE = { 'Cache-Control': 'private, no-store' };

// GET /api/home          → the full Home payload (see HomeData in src/lib/student/homeData.ts)
// GET /api/home?shell=1  → { student: StudentBootstrap } only: the small payload
//                          the app shell refreshes in the background.
export async function GET(req: Request) {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: NO_STORE });
    }

    const wantsShell = new URL(req.url).searchParams.get('shell') === '1';
    if (wantsShell) {
      const student = await loadStudentBootstrap(studentId);
      if (!student) {
        return NextResponse.json({ error: 'Student not found' }, { status: 404, headers: NO_STORE });
      }
      return NextResponse.json({ student }, { headers: NO_STORE });
    }

    const data = await loadHomeData(studentId);
    if (!data) {
      return NextResponse.json({ error: 'Student not found' }, { status: 404, headers: NO_STORE });
    }
    return NextResponse.json(data, { headers: NO_STORE });
  } catch (err) {
    logError('[api/home]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500, headers: NO_STORE });
  }
}
