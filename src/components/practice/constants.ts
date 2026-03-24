import type { AnswerKey } from '@/types';

// ── Constants ─────────────────────────────────────────────────────────────────

export const LESSON_SIZE    = 10;
export const HEARTS_MAX     = 5;
export const XP_CORRECT     = 20;
export const XP_REVIEW      = 10;
export const AUTO_ADVANCE_MS = 2000;
export const SPEED_DRILL_MS  = 90_000; // 90 seconds per question
export const MAX_BONUS_PER_LESSON = 5;
export const MAX_BONUS_PER_ORIGIN = 2;

// ── Types ─────────────────────────────────────────────────────────────────────

export type Phase =
  | 'loading'
  | 'answering'
  | 'result'
  | 'no_hearts'
  | 'review_intro'
  | 'reviewing'
  | 'complete'
  | 'usage_limit'
  | 'trial_limit'
  | 'error';

export interface TrialStatus {
  isSubscribed:      boolean;
  lifetimeQuestions: number;
  todayQuestions:    number;
}

export type BonusMode = 'off' | 'searching' | 'answering' | 'result' | 'unavailable';

export interface QuestionResult {
  questionId:    string;
  questionText:  string;
  wasCorrect:    boolean;
  selectedAnswer: AnswerKey;
  correctAnswer:  AnswerKey;
}

export interface GradeUpCta {
  grade:   number;
  type:    'full' | 'sample' | 'locked';
  onPress: () => void;
}

// ── Card accent colors (visual variety per question slot) ─────────────────────

export const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06': '🔑', 'ch07-08': '🍕', 'ch09-10': '➗',
  'ch11': '📊', 'ch12': '📏', 'ch13': '🔤', 'ch14': '⚖️',
  'ch15': '🧩', 'ch16': '🔢', 'ch17': '🕐', 'ch18': '📐',
  'ch19': '🔺', 'ch20': '⬜', 'ch21': '⭕', 'dh': '📈',
};

export const CARD_ACCENTS = [
  'bg-blue-50 text-blue-700 border-blue-200',
  'bg-purple-50 text-purple-700 border-purple-200',
  'bg-amber-50 text-amber-700 border-amber-200',
  'bg-emerald-50 text-emerald-700 border-emerald-200',
  'bg-rose-50 text-rose-700 border-rose-200',
  'bg-cyan-50 text-cyan-700 border-cyan-200',
  'bg-orange-50 text-orange-700 border-orange-200',
  'bg-indigo-50 text-indigo-700 border-indigo-200',
  'bg-pink-50 text-pink-700 border-pink-200',
  'bg-teal-50 text-teal-700 border-teal-200',
];
