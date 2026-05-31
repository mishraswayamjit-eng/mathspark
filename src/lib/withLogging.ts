import { NextRequest, NextResponse } from 'next/server';
import { logger } from './logger';

type RouteHandler = (req: NextRequest, ctx?: unknown) => Promise<NextResponse> | NextResponse;

export function withLogging(handler: RouteHandler, routeName: string): RouteHandler {
  return async function logged(req: NextRequest, ctx?: unknown) {
    const start = Date.now();
    let status = 500;
    try {
      const res = await handler(req, ctx);
      status = res.status;
      return res;
    } catch (err) {
      logger.error('Unhandled route error', { route: routeName, error: String(err) });
      return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
    } finally {
      const ms = Date.now() - start;
      logger.info('api request', {
        method: req.method,
        route: routeName,
        status,
        ms,
      });
    }
  };
}
