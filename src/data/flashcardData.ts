import flashcardJson from '../../data/concept_flashcards_all_grades.json';
import type { FlashCard } from '@/types';

// ── Static flashcard content (1,086 cards across Grades 2–9) ────────────────
// Card content is immutable — only FlashcardProgress (Leitner box state) is in DB.

const ALL_CARDS: FlashCard[] = (flashcardJson as { cards: FlashCard[] }).cards;

export function getAllFlashcards(): FlashCard[] {
  return ALL_CARDS;
}

export function getFlashcardsForGrade(grade: number): FlashCard[] {
  return ALL_CARDS.filter((c) => c.grade === grade);
}

export function getFlashcardsByTopic(grade: number, topicId: string): FlashCard[] {
  return ALL_CARDS.filter((c) => c.grade === grade && c.topicId === topicId);
}

export function getFlashcardById(id: string): FlashCard | undefined {
  return ALL_CARDS.find((c) => c.id === id);
}

/** Map topicName → accent color for card left border */
export function getTopicColor(topicName: string): string {
  const lower = topicName.toLowerCase();
  if (lower.includes('number') || lower.includes('arithmetic') || lower.includes('place value'))
    return '#34D399'; // emerald
  if (lower.includes('algebra') || lower.includes('equation') || lower.includes('expression'))
    return '#60A5FA'; // sky blue
  if (lower.includes('geometry') || lower.includes('angle') || lower.includes('triangle') || lower.includes('quadrilateral') || lower.includes('circle'))
    return '#A78BFA'; // purple
  if (lower.includes('fraction') || lower.includes('decimal'))
    return '#F472B6'; // pink
  if (lower.includes('measurement') || lower.includes('time') || lower.includes('calendar') || lower.includes('unit'))
    return '#FBBF24'; // amber
  if (lower.includes('data') || lower.includes('statistic') || lower.includes('graph'))
    return '#2DD4BF'; // teal
  if (lower.includes('percent') || lower.includes('interest') || lower.includes('ratio') || lower.includes('profit'))
    return '#FB923C'; // orange
  if (lower.includes('mental') || lower.includes('warm') || lower.includes('speed') || lower.includes('puzzle') || lower.includes('magic'))
    return '#E879F9'; // fuchsia
  if (lower.includes('factor') || lower.includes('multiple') || lower.includes('hcf') || lower.includes('lcm'))
    return '#34D399'; // emerald
  if (lower.includes('bodmas') || lower.includes('operation') || lower.includes('sequence'))
    return '#60A5FA'; // sky blue
  return '#94A3B8'; // default gray
}

/** Get unique topics for a grade */
export function getTopicsForGradeFlashcards(grade: number): Array<{ topicId: string; topicName: string; count: number }> {
  const cards = getFlashcardsForGrade(grade);
  const map = new Map<string, { topicId: string; topicName: string; count: number }>();
  for (const c of cards) {
    const existing = map.get(c.topicId);
    if (existing) {
      existing.count++;
    } else {
      map.set(c.topicId, { topicId: c.topicId, topicName: c.topicName, count: 1 });
    }
  }
  return Array.from(map.values()).sort((a, b) => b.count - a.count);
}
