'use client';

import { useEffect, useRef, useState } from 'react';
import { computeWhatsNext, type WhatsNextSuggestion } from '@/lib/whatsNext';

interface ConceptData {
  concept: { id: string; name: string };
  dependents: { id: string; name: string; type: string }[];
  links?: {
    practice: { url: string } | null;
    flashcard: { url: string } | null;
    example: { url: string } | null;
  } | null;
  progress?: { mastery: string; attempted: number; correct: number; accuracy: number } | null;
  flashcardProgress?: { totalCards: number; cardsSeen: number; avgBox: number } | null;
}

/**
 * Pre-fetches concept data on mount and computes "What's Next" suggestions
 * when the session completes. Returns [] if no conceptId or data unavailable.
 */
export function useConceptSuggestions(
  conceptId: string | null,
  justCompleted: 'flashcards' | 'practice' | 'examples',
  isComplete: boolean,
  sessionAccuracy?: number,
): WhatsNextSuggestion[] {
  const [suggestions, setSuggestions] = useState<WhatsNextSuggestion[]>([]);
  const conceptDataRef = useRef<ConceptData | null>(null);

  // Pre-fetch concept data on mount so it's ready by completion.
  // AbortController + cleanup prevents (a) stale data from a previous
  // conceptId overwriting the current ref, and (b) state updates after unmount.
  useEffect(() => {
    if (!conceptId) return;
    const controller = new AbortController();
    fetch(`/api/concept-map?id=${conceptId}`, { signal: controller.signal })
      .then((r) => { if (!r.ok) throw new Error('Fetch failed'); return r.json(); })
      .then((data: ConceptData) => {
        if (!controller.signal.aborted) conceptDataRef.current = data;
      })
      .catch((err) => {
        if (err?.name !== 'AbortError') {
          console.error('[useConceptSuggestions] fetch concept data', err);
        }
      });
    return () => controller.abort();
  }, [conceptId]);

  // Compute suggestions when session completes
  useEffect(() => {
    if (!isComplete || !conceptId || !conceptDataRef.current) return;
    const data = conceptDataRef.current;
    const result = computeWhatsNext({
      conceptId,
      conceptName: data.concept.name,
      justCompleted,
      progress: data.progress ?? null,
      flashcardProgress: data.flashcardProgress ?? null,
      sessionAccuracy,
      links: data.links ?? null,
      dependents: data.dependents.map((d) => ({ id: d.id, name: d.name })),
    });
    setSuggestions(result);
  }, [isComplete, conceptId, justCompleted, sessionAccuracy]);

  return suggestions;
}
