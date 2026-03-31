/**
 * Heuristic difficulty scorer for MathSpark questions.
 * Scores each question 0–10 based on grade, number complexity,
 * operation count, and conceptual keywords, then maps to Easy/Medium/Hard.
 */

type Difficulty = 'Easy' | 'Medium' | 'Hard';

interface QuestionInput {
  id: string;
  topicId: string;
  difficulty: string;
  questionText: string;
  grade: number; // from Topic.grade
}

export interface ScoredQuestion {
  id: string;
  topicId: string;
  oldDifficulty: string;
  newDifficulty: Difficulty;
  score: number;
  changed: boolean;
}

// ── Signal 1: Grade-Level Baseline (0-3 pts) ──────────────────────────

const GRADE_BASELINE: Record<string, number> = {
  grade2: 0, grade3: 0,
  grade4: 1, grade5: 1,
  grade6: 2, grade7: 2,
  grade8: 3, grade9: 3,
};

// Chapter-based topics mapped to grade tiers
function gradeBaseline(topicId: string, grade: number): number {
  if (GRADE_BASELINE[topicId] !== undefined) return GRADE_BASELINE[topicId];
  // ch01-ch12 → tier 1, ch13-ch16 → tier 2, ch17-ch21 → tier 3
  const chMatch = topicId.match(/^ch(\d+)/);
  if (chMatch) {
    const ch = parseInt(chMatch[1], 10);
    if (ch <= 12) return 1;
    if (ch <= 16) return 2;
    return 3;
  }
  // Fallback: use grade field
  if (grade <= 3) return 0;
  if (grade <= 5) return 1;
  if (grade <= 7) return 2;
  return 3;
}

// ── Signal 2: Number Complexity (0-2 pts) ──────────────────────────────

const DECIMAL_FRACTION_RE = /\d+\.\d+|(\d+\s*\/\s*\d+)/;

function numberComplexity(text: string): number {
  if (DECIMAL_FRACTION_RE.test(text)) return 2;

  const numbers = text.match(/-?\d+/g);
  if (!numbers || numbers.length === 0) return 0;

  let max = 0;
  for (const n of numbers) {
    const abs = Math.abs(parseInt(n, 10));
    if (abs > max) max = abs;
  }
  if (max >= 1000) return 2;
  if (max >= 21) return 1;
  return 0;
}

// ── Signal 3: Operation Count (0-2 pts) ────────────────────────────────

const OP_SYMBOLS = /[+\-×÷^√]/g;
const OP_WORDS = /\b(plus|minus|times|divide[ds]?|multiply|multiplied|subtract|add|square root|cube root)\b/gi;
const NESTED_BRACKETS = /\([^()]*\([^()]*\)/;

function operationScore(text: string): number {
  const symCount = (text.match(OP_SYMBOLS) || []).length;
  const wordCount = (text.match(OP_WORDS) || []).length;
  const ops = symCount + wordCount;

  if (ops >= 3 || NESTED_BRACKETS.test(text)) return 2;
  if (ops === 2) return 1;
  return 0;
}

// ── Signal 4: Conceptual Keywords (0-3 pts) ────────────────────────────

const VARIABLE_RE = /\b[xynab]\b/i;
const CONCEPT_KEYWORDS = [
  'solve', 'equation', 'expression', 'simplify', 'prove',
  'similar', 'congruent', 'theorem', 'ratio', 'proportion',
  'percentage', 'probability', 'volume', 'surface area',
  'coordinate', 'bodmas', 'hcf', 'lcm', 'polynomial',
];

function conceptScore(text: string): number {
  const lower = text.toLowerCase();
  let pts = 0;
  if (VARIABLE_RE.test(text)) pts++;
  for (const kw of CONCEPT_KEYWORDS) {
    if (lower.includes(kw)) {
      pts++;
      if (pts >= 3) break;
    }
  }
  return Math.min(pts, 3);
}

// ── Hard Override Rules ────────────────────────────────────────────────

function applyOverrides(
  score: number,
  topicId: string,
  text: string,
): number {
  const lower = text.toLowerCase();

  // grade2 + single op + numbers ≤ 100 → cap at Easy (≤3)
  if (topicId === 'grade2') {
    const ops = (text.match(OP_SYMBOLS) || []).length + (text.match(OP_WORDS) || []).length;
    const nums = text.match(/-?\d+/g) || [];
    const allSmall = nums.every(n => Math.abs(parseInt(n, 10)) <= 100);
    if (ops <= 1 && allSmall) return Math.min(score, 3);
  }

  // grade8-9 + algebraic variable → floor at Medium (≥4)
  if ((topicId === 'grade8' || topicId === 'grade9') && VARIABLE_RE.test(text)) {
    return Math.max(score, 4);
  }

  // ch21 (Circle) or ch19 (Triangles) → floor at Medium
  if (topicId === 'ch21' || topicId === 'ch19') {
    return Math.max(score, 4);
  }

  // ch07-08 (Fractions) with "mixed" or "improper" → floor at Medium
  if (topicId === 'ch07-08' && (lower.includes('mixed') || lower.includes('improper'))) {
    return Math.max(score, 4);
  }

  return score;
}

// ── Score → Difficulty ─────────────────────────────────────────────────

function toDifficulty(score: number): Difficulty {
  if (score <= 3) return 'Easy';
  if (score <= 6) return 'Medium';
  return 'Hard';
}

// ── Public API ─────────────────────────────────────────────────────────

export function scoreQuestion(q: QuestionInput): ScoredQuestion {
  let score = 0;
  score += gradeBaseline(q.topicId, q.grade);
  score += numberComplexity(q.questionText);
  score += operationScore(q.questionText);
  score += conceptScore(q.questionText);

  score = Math.min(score, 10);
  score = applyOverrides(score, q.topicId, q.questionText);

  const newDifficulty = toDifficulty(score);

  return {
    id: q.id,
    topicId: q.topicId,
    oldDifficulty: q.difficulty,
    newDifficulty,
    score,
    changed: q.difficulty !== newDifficulty,
  };
}
