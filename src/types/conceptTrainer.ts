/**
 * Concept Trainer — bottom-up, illustrative conceptual exercises that train the
 * *reasoning structure* of a concept rather than drilling answers.
 *
 * Data shape mirrors the concept-lessons pattern (`data/concept-trainers/<slug>.json`
 * → `conceptTrainerData.ts` → `/api/concept-trainers/[slug]`). Every answer and
 * distractor is authored/computed offline and validated by the generator — no
 * runtime LLM is involved, so grading each step's MCQ is fully deterministic.
 */

/** One multiple-choice option for a reasoning step. Feedback names the misconception. */
export interface ConceptChoice {
  letter: string;      // 'A' | 'B' | 'C' | ...
  text: string;
  isCorrect: boolean;
  feedback: string;    // diagnostic — explains WHY, naming the misconception
}

/** One of the "three thinking steps" — an MCQ with a fill-in hint. */
export interface ConceptStep {
  key?: string;        // e.g. 'whole' | 'share' | 'equation'
  prompt: string;
  choices: ConceptChoice[];
  hint: string;
}

/** A line of the worked solution. */
export interface ConceptSolutionStep {
  text: string;
}

// ── Visual models (rendered as pure-CSS) ─────────────────────────────────────

/** Two-part percentage bar: `share%` on the left, the rest on the right. */
export interface BarVisual {
  type: 'bar';
  share: number;       // 0..100
  whole: string;
  left: string;
  right: string;
}

/** Percent ↔ amount correspondence table. */
export interface MappingVisual {
  type: 'mapping';
  rows: Array<[string, string]>;
}

/** A row of equal-capacity groups/boxes working toward a target. */
export interface GroupsVisual {
  type: 'groups';
  caps: number[];
  labels: string[];
  target: string;
  capLabel?: string;
}

export type ConceptVisual = BarVisual | MappingVisual | GroupsVisual;

/** A single micro-item: story → three thinking steps → hint → visual → solution. */
export interface ConceptItem {
  code: string;        // e.g. 'm1-1'
  title: string;
  story: string;
  answer: string;      // canonical short answer (shown in the solution)
  unit?: string;
  steps: ConceptStep[];
  solution: ConceptSolutionStep[];
  check?: string;      // quick self-verification line
  explain?: string;    // the "why it works" prompt
  visual?: ConceptVisual;
}

/** A concept module targeting one reasoning skill / misconception. */
export interface ConceptModule {
  code: string;        // e.g. 'm1'
  number: number;
  title: string;
  skill: string;       // the reasoning skill this module builds
  level?: string;      // e.g. 'Core'
  rule?: string;
  teach?: string[];
  contrast?: string[];
  transfer?: string;
  items: ConceptItem[];
}

/** A full concept trainer (one concept, many modules). */
export interface ConceptTrainer {
  slug: string;
  title: string;
  concept: string;
  gradeRange: [number, number];
  modules: ConceptModule[];
}

/** Lightweight catalog entry for the trainer grid (avoids loading full JSON). */
export interface ConceptTrainerMeta {
  slug: string;
  title: string;
  emoji: string;
  color: string;
  gradeRange: [number, number];
  description: string;
}
