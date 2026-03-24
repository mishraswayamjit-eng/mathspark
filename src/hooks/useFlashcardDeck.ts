'use client';

import { useCallback } from 'react';
import { useRouter } from 'next/navigation';

export interface DeckResponse {
  cards: unknown[];
  deckName: string;
  topicColor?: string;
}

/**
 * Shared hook that provides a `fetchDeck` function for loading flashcard decks.
 * Handles auth check + URL building. Consumers handle post-processing.
 *
 * Usage:
 *   const { fetchDeck } = useFlashcardDeck(deckId);
 *   useEffect(() => { fetchDeck().then(data => { ... }); }, [fetchDeck]);
 */
export function useFlashcardDeck(deckId: string, options?: { limit?: number }) {
  const router = useRouter();

  const fetchDeck = useCallback((): Promise<DeckResponse | null> => {
    const sid = localStorage.getItem('mathspark_student_id');
    const grade = localStorage.getItem('mathspark_student_grade') || '4';
    if (!sid) {
      router.replace('/start');
      return Promise.resolve(null);
    }

    const params = new URLSearchParams({ grade, deck: deckId });
    if (options?.limit) params.set('limit', String(options.limit));

    return fetch(`/api/flashcards/deck?${params}`)
      .then((r) => {
        if (!r.ok) throw new Error('Fetch failed');
        return r.json();
      })
      .then((data): DeckResponse => ({
        cards: data.cards ?? [],
        deckName: data.deckName ?? deckId,
        topicColor: data.topicColor,
      }))
      .catch((err) => {
        console.error('[useFlashcardDeck]', err);
        return null;
      });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [deckId]);

  return { fetchDeck };
}
