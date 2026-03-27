// Pure "What's Next" suggestion engine for concept journey post-completion flow.

// ── Types ────────────────────────────────────────────────────────────────────

export interface WhatsNextSuggestion {
  label: string;
  sublabel: string;
  icon: string;
  url: string;
  color: string; // Tailwind bg class
}

export interface ConceptContext {
  conceptId: string;
  conceptName: string;
  /** What activity was just completed */
  justCompleted: 'flashcards' | 'practice' | 'examples';
  /** Practice progress */
  progress: {
    mastery: string;   // 'NotStarted' | 'Practicing' | 'Mastered'
    attempted: number;
    accuracy: number;  // 0-100
  } | null;
  /** Flashcard progress */
  flashcardProgress: {
    totalCards: number;
    cardsSeen: number;
    avgBox: number;
  } | null;
  /** Session accuracy (current session, 0-100) */
  sessionAccuracy?: number;
  /** Resolved links for this concept */
  links: {
    practice: { url: string } | null;
    flashcard: { url: string } | null;
    example: { url: string } | null;
  } | null;
  /** Dependent concepts the student could unlock next */
  dependents: { id: string; name: string }[];
}

// ── Internal priority type ───────────────────────────────────────────────────

interface RankedSuggestion extends WhatsNextSuggestion {
  priority: number;
  type: string; // for dedup
}

// ── Main function ────────────────────────────────────────────────────────────

export function computeWhatsNext(ctx: ConceptContext): WhatsNextSuggestion[] {
  const suggestions: RankedSuggestion[] = [];
  const { justCompleted, progress, flashcardProgress, sessionAccuracy, links, dependents, conceptId } = ctx;
  const acc = sessionAccuracy ?? progress?.accuracy ?? 0;
  const isMastered = progress?.mastery === 'Mastered';
  const hasPracticed = progress != null && progress.attempted > 0;

  // ── Flashcards just completed ──────────────────────────────────────────────
  if (justCompleted === 'flashcards') {
    if (!hasPracticed && links?.practice) {
      suggestions.push({
        type: 'practice',
        label: 'Practice Questions',
        sublabel: 'Test what you just learned',
        icon: '📝',
        url: links.practice.url,
        color: 'bg-duo-green',
        priority: 10,
      });
    }

    if (hasPracticed && acc < 70 && links?.example) {
      suggestions.push({
        type: 'examples',
        label: 'Watch Examples',
        sublabel: 'See step-by-step solutions',
        icon: '👁️',
        url: links.example.url,
        color: 'bg-amber-500',
        priority: 9,
      });
    }

    if (hasPracticed && !isMastered && links?.practice) {
      suggestions.push({
        type: 'practice',
        label: 'Practice Questions',
        sublabel: `${acc}% accuracy — keep going!`,
        icon: '📝',
        url: links.practice.url,
        color: 'bg-duo-green',
        priority: 7,
      });
    }

    if (isMastered && dependents.length > 0) {
      const next = dependents[0];
      suggestions.push({
        type: 'next_concept',
        label: `Next: ${next.name}`,
        sublabel: 'You unlocked this!',
        icon: '🚀',
        url: `/learn/concept-map?open=${next.id}`,
        color: 'bg-purple-500',
        priority: 10,
      });
    }
  }

  // ── Practice just completed ────────────────────────────────────────────────
  if (justCompleted === 'practice') {
    if (acc < 60 && links?.flashcard) {
      suggestions.push({
        type: 'flashcards',
        label: 'Review Flashcards',
        sublabel: 'Strengthen the basics',
        icon: '🃏',
        url: links.flashcard.url,
        color: 'bg-blue-500',
        priority: 10,
      });
    }

    if (acc < 70 && acc >= 60 && links?.example) {
      suggestions.push({
        type: 'examples',
        label: 'Watch Examples',
        sublabel: 'See how experts solve these',
        icon: '👁️',
        url: links.example.url,
        color: 'bg-amber-500',
        priority: 9,
      });
    }

    if (acc >= 60 && acc < 85 && !isMastered && links?.practice) {
      const needed = Math.max(0, 85 - acc);
      suggestions.push({
        type: 'practice',
        label: 'Keep Practicing',
        sublabel: `${needed}% more for mastery!`,
        icon: '💪',
        url: links.practice.url,
        color: 'bg-duo-green',
        priority: 8,
      });
    }

    if (acc >= 85 && links?.practice) {
      suggestions.push({
        type: 'practice_hard',
        label: 'Hard Challenge',
        sublabel: "You're ready for tough ones!",
        icon: '🔥',
        url: links.practice.url + (links.practice.url.includes('?') ? '&difficulty=hard' : '?difficulty=hard'),
        color: 'bg-red-500',
        priority: 9,
      });
    }

    if (isMastered && dependents.length > 0) {
      const next = dependents[0];
      suggestions.push({
        type: 'next_concept',
        label: `Next: ${next.name}`,
        sublabel: "Explore what's next",
        icon: '🚀',
        url: `/learn/concept-map?open=${next.id}`,
        color: 'bg-purple-500',
        priority: 10,
      });
    }
  }

  // ── Examples just completed ────────────────────────────────────────────────
  if (justCompleted === 'examples') {
    if (links?.practice) {
      suggestions.push({
        type: 'practice',
        label: 'Practice Questions',
        sublabel: 'Put it into action',
        icon: '📝',
        url: links.practice.url,
        color: 'bg-duo-green',
        priority: 10,
      });
    }
    if (links?.flashcard) {
      suggestions.push({
        type: 'flashcards',
        label: 'Study Flashcards',
        sublabel: 'Memorize key concepts',
        icon: '🃏',
        url: links.flashcard.url,
        color: 'bg-blue-500',
        priority: 7,
      });
    }
  }

  // ── Always-present fallback ────────────────────────────────────────────────
  suggestions.push({
    type: 'concept_map',
    label: 'Back to Concept Map',
    sublabel: 'Explore more concepts',
    icon: '🗺️',
    url: `/learn/concept-map?open=${conceptId}`,
    color: 'bg-slate-600',
    priority: 1,
  });

  // ── Deduplicate by type, sort by priority desc, take top 3 ─────────────────
  const seen = new Set<string>();
  const deduped: RankedSuggestion[] = [];
  for (const s of suggestions.sort((a, b) => b.priority - a.priority)) {
    if (!seen.has(s.type)) {
      seen.add(s.type);
      deduped.push(s);
    }
  }

  return deduped.slice(0, 3).map(({ priority, type, ...rest }) => rest);
}
