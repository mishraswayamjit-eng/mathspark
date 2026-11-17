'use client';

import { useCallback, useEffect, useLayoutEffect, useState } from 'react';
import Link from 'next/link';

// The plan itself is rendered on the server. Which rows the child has ticked
// today lives in localStorage (per device, per day), which the server cannot
// see. To avoid a visible swap:
//  - every "ticked" style hangs off the row's `data-done` attribute, and
//  - on a full page load a tiny inline script in the page (HomeRestoreScript)
//    sets that attribute before first paint; on in-app navigation the layout
//    effect below does the same before the browser paints.
// `suppressHydrationWarning` marks the few spots that script may have touched.

export interface PlanRow {
  id: string;
  action: string;
  type: string;
  targetUrl: string;
  reason: string;
  estimatedMins: number;
}

const useIsoLayoutEffect = typeof window !== 'undefined' ? useLayoutEffect : useEffect;

function planKey(): string {
  return `mathspark_plan_done_${new Date().toDateString()}`;
}

function readDone(): string[] {
  try {
    const parsed: unknown = JSON.parse(localStorage.getItem(planKey()) ?? '[]');
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((v): v is string => typeof v === 'string');
  } catch {
    // Unreadable or blocked storage: start with nothing ticked.
    return [];
  }
}

function iconFor(type: string): string {
  return type === 'mock' ? '📝' : type === 'explore' ? '🔍' : type === 'flashcards' ? '🧠' : '⚡';
}

export default function TodayPlan({ items }: { items: PlanRow[] }) {
  const [done, setDone] = useState<string[]>([]);

  useIsoLayoutEffect(() => {
    const saved = readDone();
    if (saved.length > 0) setDone(saved);
  }, []);

  // Opening a row ticks it. It only ever ticks: opening a finished row again
  // (to practise some more) must not take the tick away.
  const markDone = useCallback((id: string) => {
    setDone((prev) => {
      if (prev.indexOf(id) !== -1) return prev;
      const next = prev.concat(id);
      try {
        localStorage.setItem(planKey(), JSON.stringify(next));
      } catch {
        // Storage full or blocked: the tick still shows for this visit.
      }
      return next;
    });
  }, []);

  const doneCount = items.filter((item) => done.indexOf(item.id) !== -1).length;
  const allDone = items.length > 0 && doneCount >= items.length;

  return (
    <section className="bg-card rounded-card p-4 border-2 border-line">
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-title text-ink">Today&apos;s Plan</h2>
        {items.length > 0 && (
          <span className="text-xs font-bold text-ink-muted" data-plan-count suppressHydrationWarning>
            {`${doneCount}/${items.length} done`}
          </span>
        )}
      </div>

      <p
        className="text-success font-extrabold text-[15px] py-1"
        data-plan-alldone
        hidden={!allDone}
        suppressHydrationWarning
      >
        <span aria-hidden="true">🌟 </span>All done today!
      </p>

      {items.length === 0 && (
        <p className="py-3 text-ink-muted text-sm font-medium">
          Start practicing to build your plan!
        </p>
      )}

      {items.map((item) => {
        const isDone = done.indexOf(item.id) !== -1;
        return (
          <Link
            key={item.id}
            href={item.targetUrl}
            onClick={() => markDone(item.id)}
            data-plan-id={item.id}
            data-done={isDone ? 'true' : undefined}
            suppressHydrationWarning
            className="group flex items-center gap-3 py-3 min-h-[56px] border-b-2 border-line data-[done=true]:opacity-50"
          >
            <span className="w-6 h-6 rounded-full border-2 border-line shrink-0 flex items-center justify-center text-xs text-white group-data-[done=true]:bg-success group-data-[done=true]:border-success">
              <span className="hidden group-data-[done=true]:inline" aria-hidden="true">✓</span>
            </span>
            {/* The tick is a picture; this says it in words to a screen reader. */}
            <span className="sr-only hidden group-data-[done=true]:inline">Done: </span>
            <span className="text-lg shrink-0" aria-hidden="true">{iconFor(item.type)}</span>
            <span className="flex-1 min-w-0">
              <span className="block text-sm font-bold text-ink truncate group-data-[done=true]:line-through">
                {item.action}
              </span>
              <span className="block text-xs text-ink-muted font-medium truncate">{item.reason}</span>
            </span>
            <span className="text-xs font-extrabold text-ink-muted bg-soft rounded-full px-2 py-0.5 shrink-0">
              {`${item.estimatedMins}min`}
            </span>
          </Link>
        );
      })}

      {/* Daily Challenge: always on offer, never hides "Continue" in the hero. */}
      <Link href="/practice/daily" className="flex items-center gap-3 py-3 min-h-[56px]">
        <span className="w-6 shrink-0 text-center text-lg" aria-hidden="true">🎯</span>
        <span className="flex-1 min-w-0">
          <span className="block text-sm font-bold text-ink truncate">Daily Challenge</span>
          <span className="block text-xs text-ink-muted font-medium truncate">5 questions · Build your streak!</span>
        </span>
        <span className="text-action font-extrabold text-sm shrink-0">Play →</span>
      </Link>
    </section>
  );
}
