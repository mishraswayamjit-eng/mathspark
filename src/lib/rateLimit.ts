// Simple in-memory rate limiter (per-process, suitable for MVP).
// For production at scale, replace with Upstash Redis.

const store = new Map<string, { count: number; resetAt: number }>();
let callCount = 0;

/**
 * Returns true if the request is allowed, false if rate-limited.
 * @param key     Unique key e.g. `auth:1.2.3.4`
 * @param limit   Max requests in the window
 * @param windowMs Window length in milliseconds
 */
export function checkRateLimit(key: string, limit: number, windowMs: number): boolean {
  const now = Date.now();

  // Periodic cleanup of expired entries to prevent memory leak
  if (++callCount % 100 === 0) {
    for (const [k, v] of Array.from(store)) {
      if (now > v.resetAt) store.delete(k);
    }
  }

  const entry = store.get(key);

  if (!entry || now > entry.resetAt) {
    store.set(key, { count: 1, resetAt: now + windowMs });
    return true;
  }

  if (entry.count >= limit) return false;
  entry.count++;
  return true;
}
