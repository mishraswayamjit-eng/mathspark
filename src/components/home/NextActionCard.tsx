'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import type { NextAction } from '@/lib/brain/nextAction';

/**
 * "What to do next": the first action as one clear card, the next two as small rows.
 *
 * It records that the first action was shown (once per mount) and that an
 * action was taken (on tap). Neither request is waited for, so a tap always
 * goes straight to where it points.
 */

export interface NextActionCardProps {
  actions: NextAction[];
  surface: 'home' | 'session_end';
}

const BUTTON_LABEL: Record<string, string> = {
  lesson: 'Start the lesson',
  hands_on: 'Start the lesson',
  explain: "Let's go",
  review: 'Start the review',
  flashcards: 'Open my cards',
  drill: 'Start the drill',
  strategy: 'Show me the trick',
  mock: 'Start the test',
  practice: "Let's go",
};

const EMOJI: Record<string, string> = {
  lesson: '📘',
  hands_on: '✋',
  explain: '💡',
  review: '🔁',
  flashcards: '🃏',
  drill: '🎯',
  strategy: '✨',
  mock: '📝',
  practice: '🚀',
};

function record(event: 'shown' | 'taken', action: NextAction, surface: 'home' | 'session_end'): void {
  if (typeof window === 'undefined' || typeof fetch !== 'function') return;
  try {
    fetch('/api/recommendations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        event,
        surface,
        actionType: action.actionType,
        ruleId: action.ruleId,
        nodeId: action.nodeId,
        refId: action.refId,
      }),
      keepalive: true,
    }).catch(() => {
      // A record that did not arrive must never get in a child's way.
    });
  } catch {
    // Same: nothing to do.
  }
}

export default function NextActionCard({ actions, surface }: NextActionCardProps) {
  const primary = actions.length > 0 ? actions[0] : null;
  const primaryId = primary ? primary.id : '';
  const shownFor = useRef<string | null>(null);

  // "Shown", once per mount for the first action.
  useEffect(() => {
    if (!primary || shownFor.current !== null) return;
    shownFor.current = primaryId;
    record('shown', primary, surface);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [primaryId, surface]);

  if (!primary) return null;

  const others = actions.slice(1, 3);

  return (
    <section className="w-full space-y-2" aria-label="What to do next">
      <div className="bg-card border-2 border-ink rounded-card p-4 shadow-hard-sm">
        <p className="text-caption text-ink-muted">Next up for you</p>
        <div className="flex items-start gap-3 mt-1">
          <span className="text-3xl flex-shrink-0" aria-hidden="true">{EMOJI[primary.actionType] || '⭐'}</span>
          <div className="flex-1 min-w-0">
            <h2 className="text-title text-ink leading-tight">{primary.title}</h2>
            <p className="text-[16px] font-semibold text-ink-muted leading-snug mt-1">{primary.reason}</p>
            {typeof primary.minutes === 'number' && primary.minutes > 0 && (
              <p className="text-[14px] font-bold text-ink-muted mt-1">
                <span aria-hidden="true">⏱ </span>About {primary.minutes} min
              </p>
            )}
          </div>
        </div>
        <Link
          href={primary.href}
          onClick={() => record('taken', primary, surface)}
          className="ui-btn ui-btn-primary w-full mt-3"
        >
          {BUTTON_LABEL[primary.actionType] || "Let's go"} <span aria-hidden="true">→</span>
        </Link>
      </div>

      {others.map((a) => (
        <Link
          key={a.id}
          href={a.href}
          onClick={() => record('taken', a, surface)}
          className="min-h-[48px] flex items-center gap-3 bg-card border-2 border-line rounded-card px-4 py-2 hover:border-ink transition-colors"
        >
          <span className="text-xl flex-shrink-0" aria-hidden="true">{EMOJI[a.actionType] || '⭐'}</span>
          <span className="flex-1 min-w-0 text-[16px] font-bold text-ink leading-snug">{a.title}</span>
          {typeof a.minutes === 'number' && a.minutes > 0 && (
            <span className="text-[14px] font-bold text-ink-muted flex-shrink-0">{a.minutes} min</span>
          )}
          <span className="text-ink-muted font-bold flex-shrink-0" aria-hidden="true">→</span>
        </Link>
      ))}
    </section>
  );
}
