/**
 * Tell the server that a child opened or finished a piece of learning content.
 *
 * Fire-and-forget: it never throws, never blocks the screen and does nothing on
 * the server. It is a record only. It never affects XP, mastery or grading.
 */

export type ContentKind = 'teach' | 'hands_on' | 'drill' | 'lesson' | 'story' | 'strategy';

export const CONTENT_KINDS: ContentKind[] = ['teach', 'hands_on', 'drill', 'lesson', 'story', 'strategy'];

export function logContentView(kind: ContentKind, refId: string, completed?: boolean): void {
  if (typeof window === 'undefined' || typeof fetch !== 'function') return;
  if (!refId) return;
  try {
    fetch('/api/content-view', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ kind, refId, completed: completed === true }),
      keepalive: true,
    }).catch(() => {
      // A record that did not arrive is not worth interrupting a child for.
    });
  } catch {
    // Same: nothing to do.
  }
}
