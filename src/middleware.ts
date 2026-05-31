import { NextRequest, NextResponse } from 'next/server';

const rateLimitMap = new Map<string, { count: number; windowStart: number }>();
const WINDOW_MS = 60_000;
const MAX_REQUESTS = 60;

function addSecurityHeaders(response: NextResponse): NextResponse {
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
  response.headers.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
  response.headers.set(
    'Content-Security-Policy',
    [
      "default-src 'self'",
      "script-src 'self' 'unsafe-inline'",  // unsafe-inline needed for Next.js inline scripts
      "style-src 'self' 'unsafe-inline'",   // unsafe-inline needed for Tailwind
      "img-src 'self' data:",
      "font-src 'self'",
      "connect-src 'self'",
      "frame-ancestors 'none'",
    ].join('; ')
  );
  return response;
}

export function middleware(req: NextRequest) {
  // Only rate-limit API routes
  if (!req.nextUrl.pathname.startsWith('/api')) {
    return addSecurityHeaders(NextResponse.next());
  }

  const ip = req.headers.get('x-forwarded-for')?.split(',')[0].trim() ?? 'unknown';
  const now = Date.now();
  const entry = rateLimitMap.get(ip);

  if (!entry || now - entry.windowStart > WINDOW_MS) {
    rateLimitMap.set(ip, { count: 1, windowStart: now });
    return addSecurityHeaders(NextResponse.next());
  }

  entry.count += 1;
  if (entry.count > MAX_REQUESTS) {
    return addSecurityHeaders(
      NextResponse.json(
        { error: "Too many requests — slow down a little!" },
        { status: 429 }
      )
    );
  }

  return addSecurityHeaders(NextResponse.next());
}

export const config = {
  matcher: '/((?!_next/static|_next/image|favicon.ico|icon-192.png|icon-512.png|sw.js|manifest.json).*)',
};
