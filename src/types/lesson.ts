// ── Concept Lessons — type definitions ───────────────────────────────────────

export interface LessonStep {
  text: string;
  notation: string;
  tip?: string;
}

export interface Lesson {
  id: string;
  title: string;
  intro: string;
  visual?: string;
  steps?: LessonStep[];
  explanation?: string[];
  rule?: string;
  tip?: string;
}

export type QuizDifficulty = 'direct' | 'near_transfer' | 'stretch' | 'challenge';

export interface QuizQuestion {
  id: string;
  question: string;
  answer: string;
  hint: string;
  story?: string;
  isWord?: boolean;
  difficulty: QuizDifficulty;
}

export interface LessonLevel {
  id: number;
  label: string;
  emoji: string;
  color: string;
  bgGradient: string;
  subtitle: string;
  lessons: Lesson[];
  quiz: QuizQuestion[];
}

export interface LessonTopic {
  id: string;
  topic: string;
  emoji: string;
  color: string;
  gradeRange: [number, number];
  description: string;
  levels: LessonLevel[];
}

// Lightweight version used for the topic grid (no lesson/quiz data)
export interface LessonTopicMeta {
  id: string;
  topic: string;
  emoji: string;
  color: string;
  gradeRange: [number, number];
  description: string;
}
