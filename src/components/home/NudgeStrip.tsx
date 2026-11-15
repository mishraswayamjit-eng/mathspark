'use client';

// One short note from Sparky on the Home page.
//
// The Brain Engine works out up to three nudges (`generateNudges`); this shows
// the single one that wins (`pickTopNudge`, order in `NUDGE_PRIORITY`). A nudge
// the child puts away stays away for the rest of the day on this device.
// Nothing is rendered until the browser's storage has been read, so a nudge
// already put away never flashes up.

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import type { Nudge } from '@/lib/brain/engine';
import { pickTopNudge } from '@/lib/brain/rules';

const DISMISSED_KEY = 'mathspark_nudges_dismissed';
/** Written by the practice page when a lesson is finished. */
const LAST_PRACTICE_KEY = 'mathspark_last_practice_date';

interface DismissedToday {
  date: string;
  ids: string[];
}

/** The ids put away today. Yesterday's list is ignored. */
function readDismissed(today: string): string[] {
  try {
    const raw = localStorage.getItem(DISMISSED_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as Partial<DismissedToday> | null;
    if (!parsed || parsed.date !== today || !Array.isArray(parsed.ids)) return [];
    return parsed.ids.filter((id): id is string => typeof id === 'string');
  } catch {
    return [];
  }
}

function writeDismissed(today: string, ids: string[]): void {
  try {
    const value: DismissedToday = { date: today, ids };
    localStorage.setItem(DISMISSED_KEY, JSON.stringify(value));
  } catch {
    // Storage is full or switched off: the nudge is still hidden for this visit.
  }
}

export default function NudgeStrip({ nudges }: { nudges: Nudge[] }) {
  const [checked, setChecked] = useState(false);
  const [dismissedIds, setDismissedIds] = useState<string[]>([]);
  const [practisedToday, setPractisedToday] = useState(false);
  // Put away during this visit: nothing else takes its place straight away.
  const [closed, setClosed] = useState(false);

  useEffect(() => {
    const today = new Date().toDateString();
    setDismissedIds(readDismissed(today));
    try {
      setPractisedToday(localStorage.getItem(LAST_PRACTICE_KEY) === today);
    } catch {
      setPractisedToday(false);
    }
    setChecked(true);
  }, []);

  if (!checked || closed) return null;
  if (!Array.isArray(nudges) || nudges.length === 0) return null;

  const nudge = pickTopNudge(nudges, { dismissedIds, practisedToday });
  if (!nudge) return null;

  const nudgeId = nudge.id;
  function dismiss() {
    const today = new Date().toDateString();
    const ids = readDismissed(today);
    if (ids.indexOf(nudgeId) === -1) ids.push(nudgeId);
    writeDismissed(today, ids);
    setDismissedIds(ids);
    setClosed(true);
  }

  return (
    <section
      aria-label="A note from Sparky"
      className="bg-card rounded-card border-2 border-line p-3 flex items-start gap-3 animate-fade-in"
    >
      <div className="shrink-0 pt-1" aria-hidden="true">
        <Sparky mood={nudge.sparkyEmotion} size={44} />
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-base font-bold leading-snug text-ink">{nudge.message}</p>
        <Link
          href={nudge.actionUrl}
          className="mt-2 inline-flex items-center justify-center min-h-[48px] px-5 rounded-full border-2 border-ink bg-action text-white text-sm font-extrabold active:scale-[0.98] transition-transform"
        >
          {nudge.actionLabel}
        </Link>
      </div>

      <button
        type="button"
        onClick={dismiss}
        aria-label="Not now"
        className="shrink-0 min-h-[48px] min-w-[48px] flex items-center justify-center rounded-full text-xl font-bold leading-none text-ink-muted active:scale-[0.98] transition-transform"
      >
        <span aria-hidden="true">×</span>
      </button>
    </section>
  );
}
