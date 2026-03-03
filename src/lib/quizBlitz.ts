import {
  getFlashcardsForGrade,
  getFlashcardsByTopic,
} from '@/data/flashcardData';
import type { FlashCard } from '@/types';

// ── Types ────────────────────────────────────────────────────────────────────

export interface QuizOption {
  id: string;       // 'A' | 'B' | 'C' | 'D'
  text: string;
  isCorrect: boolean;
}

export interface QuizQuestion {
  cardId: string;
  cardFront: string;
  cardFormula?: string;
  topicName: string;
  difficulty: number;
  options: QuizOption[];
  timeLimitMs: number;
}

// ── Shuffle helper ───────────────────────────────────────────────────────────

function shuffle<T>(arr: T[]): T[] {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// ── MCQ Generation ───────────────────────────────────────────────────────────

/**
 * Generate 4 MCQ options for a flashcard.
 * Correct answer = card's back text.
 * 3 distractors from same-topic or same-grade cards (distinct back text).
 */
export function generateMCQOptions(
  correctCard: FlashCard,
  grade: number,
  usedDistractorIds: Set<string>,
): QuizOption[] {
  const correctText = correctCard.back.trim();

  // Collect distractor candidates (prioritize same topic, same grade)
  const sameTopic = getFlashcardsByTopic(grade, correctCard.topicId).filter(
    (c) => c.id !== correctCard.id && c.back.trim() !== correctText,
  );
  const sameGrade = getFlashcardsForGrade(grade).filter(
    (c) =>
      c.id !== correctCard.id &&
      c.back.trim() !== correctText &&
      c.topicId !== correctCard.topicId,
  );

  // Priority: same topic first, then same grade, avoid already-used
  const pool = [
    ...shuffle(sameTopic.filter((c) => !usedDistractorIds.has(c.id))),
    ...shuffle(sameGrade.filter((c) => !usedDistractorIds.has(c.id))),
    ...shuffle(sameTopic), // fallback: reuse if needed
    ...shuffle(sameGrade),
  ];

  // Pick 3 unique distractors (unique by back text)
  const distractors: FlashCard[] = [];
  const usedTexts = new Set([correctText.toLowerCase()]);

  for (const card of pool) {
    if (distractors.length >= 3) break;
    const text = card.back.trim().toLowerCase();
    if (!usedTexts.has(text)) {
      usedTexts.add(text);
      distractors.push(card);
      usedDistractorIds.add(card.id);
    }
  }

  // Build options array
  const labels = ['A', 'B', 'C', 'D'];
  const rawOptions = [
    { text: correctCard.back, isCorrect: true },
    ...distractors.map((d) => ({ text: d.back, isCorrect: false })),
  ];

  // Pad if we couldn't find enough distractors
  while (rawOptions.length < 4) {
    rawOptions.push({ text: '—', isCorrect: false });
  }

  // Shuffle and assign labels
  const shuffled = shuffle(rawOptions);
  return shuffled.map((opt, i) => ({
    id: labels[i],
    text: opt.text,
    isCorrect: opt.isCorrect,
  }));
}

/**
 * Generate a full set of QuizQuestions from a deck of flashcards.
 */
export function generateQuizQuestions(
  cards: FlashCard[],
  grade: number,
): QuizQuestion[] {
  const usedDistractors = new Set<string>();

  return cards.map((card) => ({
    cardId: card.id,
    cardFront: card.front,
    cardFormula: card.formula,
    topicName: card.topicName,
    difficulty: card.difficulty,
    options: generateMCQOptions(card, grade, usedDistractors),
    timeLimitMs: 12000, // 12 seconds per question
  }));
}

// ── Scoring ──────────────────────────────────────────────────────────────────

const BASE_POINTS = 10;

/** Speed multiplier based on how fast the answer was given */
export function getSpeedMultiplier(timeTakenMs: number): number {
  if (timeTakenMs < 3000) return 2.0;
  if (timeTakenMs < 7000) return 1.5;
  if (timeTakenMs < 10000) return 1.0;
  return 0.5;
}

/** Combo multiplier based on consecutive correct streak */
export function getComboMultiplier(combo: number): number {
  if (combo >= 7) return 2.0;
  if (combo >= 5) return 1.5;
  if (combo >= 3) return 1.2;
  return 1.0;
}

/** Calculate points for a single correct answer */
export function calculatePoints(timeTakenMs: number, combo: number): number {
  return Math.round(BASE_POINTS * getSpeedMultiplier(timeTakenMs) * getComboMultiplier(combo));
}
