/**
 * Structured error logging utility.
 * Currently outputs to console.error in a structured format.
 * TODO: Replace with Sentry SDK integration when ready:
 *   import * as Sentry from '@sentry/nextjs';
 *   Sentry.captureException(err, { extra: { context } });
 */
export function logError(context: string, err: unknown): void {
  const timestamp = new Date().toISOString();
  const message = err instanceof Error ? err.message : String(err);
  const stack = err instanceof Error ? err.stack : undefined;

  console.error(JSON.stringify({
    level: 'error',
    context,
    message,
    ...(stack ? { stack } : {}),
    timestamp,
  }));
}
