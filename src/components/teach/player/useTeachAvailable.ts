'use client';

import { useEffect, useState } from 'react';

/**
 * Does this question have an "Explain it to me" lesson?
 *
 * Asks the light `?check=1` form of the lesson route, which answers yes or no
 * without sending the lesson. Each question is asked about once per visit, so
 * the side pane and the result panel can both use this for the same question.
 */

export type TeachAvailability = 'checking' | 'yes' | 'no';

const known: Record<string, boolean> = {};
const pending: Record<string, Promise<boolean>> = {};

function has(map: object, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(map, key);
}

/** Lets the player record what it found out (a 404 means there is no lesson). */
export function rememberTeachAvailability(questionId: string, available: boolean): void {
  known[questionId] = available;
}

function check(questionId: string): Promise<boolean> {
  if (has(known, questionId)) return Promise.resolve(known[questionId]);
  if (has(pending, questionId)) return pending[questionId];

  const asked: Promise<boolean> = fetch(`/api/teach/${encodeURIComponent(questionId)}?check=1`)
    .then((res) => (res.ok ? (res.json() as Promise<{ available?: boolean }>) : null))
    .then((data) => {
      delete pending[questionId];
      // Signed out or over a limit: say no for now, and ask again next time.
      if (!data) return false;
      const yes = data.available === true;
      known[questionId] = yes;
      return yes;
    })
    .catch(() => {
      delete pending[questionId];
      return false;
    });

  pending[questionId] = asked;
  return asked;
}

export function useTeachAvailable(questionId: string | null | undefined): TeachAvailability {
  const [answer, setAnswer] = useState<{ id: string; yes: boolean } | null>(null);

  useEffect(() => {
    if (!questionId) return;
    let live = true;
    check(questionId).then((yes) => {
      if (live) setAnswer({ id: questionId, yes });
    });
    return () => { live = false; };
  }, [questionId]);

  if (!questionId) return 'no';
  if (answer && answer.id === questionId) return answer.yes ? 'yes' : 'no';
  if (has(known, questionId)) return known[questionId] ? 'yes' : 'no';
  return 'checking';
}
