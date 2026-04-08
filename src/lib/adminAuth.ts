import crypto from 'crypto';

/**
 * Timing-safe comparison of a provided secret against SEED_SECRET env var.
 * Prevents timing attacks on admin/seed route authentication.
 */
export function verifySecret(provided: string | null): boolean {
  const expected = process.env.SEED_SECRET ?? '';
  if (!provided || !expected) return false;
  if (provided.length !== expected.length) return false;
  return crypto.timingSafeEqual(Buffer.from(provided), Buffer.from(expected));
}

/**
 * Timing-safe comparison of a provided Bearer token against CRON_SECRET env var.
 * Use for cron-protected routes.
 */
export function verifyCronSecret(authHeader: string | null): boolean {
  const expected = process.env.CRON_SECRET ?? '';
  if (!authHeader || !expected) return false;
  const provided = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : '';
  if (!provided) return false;
  if (provided.length !== expected.length) return false;
  return crypto.timingSafeEqual(Buffer.from(provided), Buffer.from(expected));
}
