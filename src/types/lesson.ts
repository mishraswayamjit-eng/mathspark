// ── Concept Lessons — type definitions ───────────────────────────────────────

export interface LessonStep {
  text: string;
  notation: string;
  tip?: string;
}

// ── Slide-based lesson types ─────────────────────────────────────────────────

export type SlideType = 'intro' | 'concept' | 'rule' | 'tip' | 'diagram' | 'recap';

export interface SlideIllustration {
  type: 'fraction' | 'multiFraction' | 'numberLine' | 'clock' | 'angle' |
        'triangle' | 'circle' | 'balance' | 'pattern' | 'polygon' |
        'pictograph' | 'compositeShape' | 'venn' | 'emoji';
  props: Record<string, unknown>;
}

export interface Slide {
  type: SlideType;
  text: string;
  subtext?: string;
  notation?: string;
  illustration?: SlideIllustration;
  emoji?: string;
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
  slides?: Slide[];
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
