import { NextRequest, NextResponse } from 'next/server';

// ── In-memory fallback (single-instance) ──────────────────────────────────
interface Entry { count: number; resetAt: number }
const memMap = new Map<string, Entry>();
const WINDOW_MS = 60_000;
const MEM_LIMIT = 60;
const MAX_ENTRIES = 50_000; // cap to prevent memory leak

function memRateLimit(ip: string): { allowed: boolean; remaining: number } {
  const now = Date.now();
  if (memMap.size >= MAX_ENTRIES) {
    const oldest = memMap.keys().next().value;
    if (oldest) memMap.delete(oldest);
  }
  const entry = memMap.get(ip);
  if (!entry || now >= entry.resetAt) {
    memMap.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return { allowed: true, remaining: MEM_LIMIT - 1 };
  }
  entry.count += 1;
  return { allowed: entry.count <= MEM_LIMIT, remaining: Math.max(0, MEM_LIMIT - entry.count) };
}

// ── Upstash Redis rate limit (multi-instance) ─────────────────────────────
// Dynamic import keeps Node.js-only Upstash code out of the Edge bundle.
async function redisRateLimit(ip: string): Promise<{ allowed: boolean; remaining: number }> {
  const { Ratelimit } = await import('@upstash/ratelimit');
  const { Redis } = await import('@upstash/redis');
  const ratelimit = new Ratelimit({
    redis: new Redis({
      url: process.env.UPSTASH_REDIS_REST_URL!,
      token: process.env.UPSTASH_REDIS_REST_TOKEN!,
    }),
    limiter: Ratelimit.slidingWindow(60, '60 s'),
    analytics: false,
  });
  const { success, remaining } = await ratelimit.limit(ip);
  return { allowed: success, remaining };
}

// ── Security headers ───────────────────────────────────────────────────────
function addSecurityHeaders(res: NextResponse): NextResponse {
  res.headers.set('X-Frame-Options', 'DENY');
  res.headers.set('X-Content-Type-Options', 'nosniff');
  res.headers.set('X-XSS-Protection', '1; mode=block');
  res.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  res.headers.set(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: blob:",
      "font-src 'self'",
      "connect-src 'self'",
      "frame-ancestors 'none'",
    ].join('; '),
  );
  return res;
}

export async function middleware(req: NextRequest) {
  // Only rate-limit API routes
  if (!req.nextUrl.pathname.startsWith('/api/')) {
    const res = NextResponse.next();
    return addSecurityHeaders(res);
  }

  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim()
    ?? req.headers.get('x-real-ip')
    ?? '127.0.0.1';

  let allowed: boolean;
  let remaining: number;

  const useRedis =
    Boolean(process.env.UPSTASH_REDIS_REST_URL) &&
    Boolean(process.env.UPSTASH_REDIS_REST_TOKEN);

  if (useRedis) {
    try {
      ({ allowed, remaining } = await redisRateLimit(ip));
    } catch {
      // Redis unavailable — fall back to memory
      ({ allowed, remaining } = memRateLimit(ip));
    }
  } else {
    ({ allowed, remaining } = memRateLimit(ip));
  }

  if (!allowed) {
    const res = NextResponse.json(
      { error: 'Too many requests — please slow down!' },
      { status: 429 },
    );
    res.headers.set('Retry-After', '60');
    return addSecurityHeaders(res);
  }

  const res = NextResponse.next();
  res.headers.set('X-RateLimit-Remaining', String(remaining));
  return addSecurityHeaders(res);
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|.*\\.png$).*)'],
};
