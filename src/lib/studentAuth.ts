import { SignJWT, jwtVerify } from 'jose';
import { cookies } from 'next/headers';

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
  return verifyStudentToken(token);
}

export { COOKIE_NAME };
