import { SignJWT, jwtVerify } from 'jose';
import { cookies } from 'next/headers';
import { prisma } from '@/lib/db';
import { logError } from '@/lib/logger';

const COOKIE_NAME = 'mathspark_student_token';
const EXPIRY = '30d';

function getSecret(): Uint8Array {
  const secret = process.env.NEXTAUTH_SECRET;
  if (!secret) throw new Error('NEXTAUTH_SECRET is not set');
  return new TextEncoder().encode(secret);
}

/** Sign a JWT containing the studentId. */
export async function createStudentToken(studentId: string): Promise<string> {
  return new SignJWT({ studentId })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime(EXPIRY)
    .sign(getSecret());
}

/** Verify a JWT and return the studentId, or null if invalid/expired. */
export async function verifyStudentToken(token: string): Promise<string | null> {
  try {
    const { payload } = await jwtVerify(token, getSecret());
    return (payload.studentId as string) ?? null;
  } catch {
    return null;
  }
}

/**
 * Read the httpOnly cookie, verify the JWT, return the studentId.
 * Returns null if no cookie or invalid token.
 * Use in API route handlers: `const studentId = await getAuthenticatedStudentId();`
 */
export async function getAuthenticatedStudentId(): Promise<string | null> {
  const cookieStore = cookies();
  const token = cookieStore.get(COOKIE_NAME)?.value;
  if (!token) return null;
  const studentId = await verifyStudentToken(token);
  if (!studentId) return null;
  return (await isActiveStudent(studentId)) ? studentId : null;
}

// A child a parent has removed keeps a signed cookie for up to 30 days, so the
// token alone is not enough: the account must still exist and not be removed.
// The answer is remembered per server instance for a minute, so this costs one
// small indexed read per child per minute, not one per request.
const ACTIVE_TTL_MS = 60_000;
const ACTIVE_CACHE_MAX = 5000;
let activeCache: Record<string, { ok: boolean; at: number }> = {};
let activeCacheSize = 0;

async function readActive(studentId: string): Promise<boolean> {
  const row = await prisma.student.findFirst({
    where: { id: studentId, deletedAt: null },
    select: { id: true },
  });
  return !!row;
}

async function isActiveStudent(studentId: string): Promise<boolean> {
  const now = Date.now();
  const hit = activeCache[studentId];
  if (hit && now - hit.at < ACTIVE_TTL_MS) return hit.ok;
  let ok: boolean;
  try {
    ok = await readActive(studentId);
  } catch (err) {
    // The database could not be reached. Never answer "active" on a guess: a
    // removed child's cookie must not start working because a read failed.
    logError('[studentAuth] could not check that the account is active:', err);
    // An earlier answer for this child, even an old one, is better than a guess.
    if (hit) return hit.ok;
    // No earlier answer: try once more, then give up. Giving up throws, so the
    // route answers with a server error (which is the truth) instead of either
    // signing the child out or letting a removed account in.
    try {
      ok = await readActive(studentId);
    } catch (again) {
      logError('[studentAuth] second check failed:', again);
      throw new Error('Could not confirm that the account is active');
    }
  }
  if (!hit) {
    if (activeCacheSize >= ACTIVE_CACHE_MAX) {
      activeCache = {};
      activeCacheSize = 0;
    }
    activeCacheSize += 1;
  }
  activeCache[studentId] = { ok, at: now };
  return ok;
}

export { COOKIE_NAME };
