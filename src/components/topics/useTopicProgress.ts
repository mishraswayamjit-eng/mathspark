'use client';

import { useEffect, useState } from 'react';
import { logError } from '@/lib/logger';
import type { TopicProgress } from '@/components/topics/TopicList';

// Progress for the topic list, from /api/dashboard (the same source, and the
// same five-minute device cache, that Practise → By topic uses).

const CACHE_TTL_MS = 5 * 60 * 1000;

interface ProgressRow {
  id: string;
  mastery: string;
  attempted: number;
  correct: number;
}

/** /api/dashboard `topics` → progress keyed by database topic id. */
export function progressByTopicId(topics: ProgressRow[] | null | undefined): Record<string, TopicProgress> {
  const out: Record<string, TopicProgress> = {};
  if (!topics) return out;
  for (let i = 0; i < topics.length; i++) {
    const t = topics[i];
    out[t.id] = { mastery: t.mastery, attempted: t.attempted, correct: t.correct };
  }
  return out;
}

interface DashboardSlice {
  topics?: ProgressRow[];
}

/**
 * The signed-in child's progress by database topic id. Null until it is known,
 * and it stays null if it cannot be loaded (the list then shows no numbers).
 */
export function useTopicProgress(): Record<string, TopicProgress> | null {
  const [progress, setProgress] = useState<Record<string, TopicProgress> | null>(null);

  useEffect(() => {
    let cancelled = false;

    function load(): void {
      let studentId: string | null = null;
      try { studentId = localStorage.getItem('mathspark_student_id'); } catch { /* storage unavailable */ }
      if (!studentId) return;

      const cacheKey = `mathspark_dashboard_${studentId}`;
      try {
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
          const parsed = JSON.parse(cached) as { data?: DashboardSlice; ts?: number } | null;
          if (parsed && parsed.data && typeof parsed.ts === 'number' && Date.now() - parsed.ts < CACHE_TTL_MS) {
            setProgress(progressByTopicId(parsed.data.topics));
            return;
          }
        }
      } catch { /* unreadable cache: fetch instead */ }

      fetch('/api/dashboard')
        .then((r) => {
          if (!r.ok) throw new Error('dashboard not available');
          return r.json() as Promise<DashboardSlice>;
        })
        .then((data) => {
          if (cancelled) return;
          setProgress(progressByTopicId(data.topics));
          try {
            localStorage.setItem(cacheKey, JSON.stringify({ data, ts: Date.now() }));
          } catch { /* storage full or unavailable */ }
        })
        .catch((err) => {
          // The list still works without numbers.
          logError('[topics] progress', err);
        });
    }

    load();
    return () => { cancelled = true; };
  }, []);

  return progress;
}
