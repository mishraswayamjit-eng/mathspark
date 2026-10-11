/**
 * IPM textbook import — the enrichment + fresh-solve helpers.
 *
 * The textbook gives us exam-authentic MCQ STEMS but no teaching layer and
 * printed answers the publisher explicitly did NOT verify. This module keeps the
 * "Truth vs Delivery" split from CLAUDE.md:
 *
 *  - TRUTH: `solveTextbookFresh` decides an answer by self-consistency (Sonnet,
 *    N=3, majority >= 2 with one temp-0 tie-break). No majority -> null, and the
 *    caller REJECTS the question. The import route uses this for answerless rows
 *    and for printed answers that fail `sanityCheck`.
 *  - DELIVERY: `enrichTextbookQuestion` (Opus) generates hints / step-by-step /
 *    misconceptions GROUNDED on the already-verified correct answer. It is told
 *    the answer and must build toward it only — it never restates or changes it.
 */

import { complete } from './complete';
import { gradeDescriptor, kidSafeRules } from './guardrails';
import { asString, extractJson, type AuthoredStep } from './author';

export interface TextbookOptions {
  option1: string;
  option2: string;
  option3: string;
  option4: string;
}

export interface EnrichmentRequest {
  questionText: string;
  options: TextbookOptions;
  /** The verified correct option — delivery is grounded strictly on this. */
  correctAnswer: 'A' | 'B' | 'C' | 'D';
  grade: number;
  topicName: string;
  subTopic: string;
}

export interface Enrichment {
  hint1: string;
  hint2: string;
  hint3: string;
  stepByStep: AuthoredStep[];
  misconceptionA: string;
  misconceptionB: string;
  misconceptionC: string;
  misconceptionD: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
}

const ANSWER_KEYS = ['A', 'B', 'C', 'D'] as const;
const DIFFICULTIES = ['Easy', 'Medium', 'Hard'] as const;

/** Normalize the raw parsed object into an Enrichment (steps + hints + misconceptions). */
function normalizeEnrichment(raw: unknown): Enrichment {
  if (!raw || typeof raw !== 'object') throw new Error('Enrichment is not an object');
  const o = raw as Record<string, unknown>;

  const rawSteps = Array.isArray(o.stepByStep) ? o.stepByStep : [];
  const stepByStep: AuthoredStep[] = rawSteps
    .map((s, i): AuthoredStep | null => {
      if (!s || typeof s !== 'object') return null;
      const so = s as Record<string, unknown>;
      const text = asString(so.text);
      if (!text) return null;
      const latex = asString(so.latex);
      return { step: i + 1, text, ...(latex ? { latex } : {}) };
    })
    .filter((s): s is AuthoredStep => s !== null);

  const difficultyRaw = asString(o.difficulty);
  const difficulty =
    (DIFFICULTIES as readonly string[]).includes(difficultyRaw)
      ? (difficultyRaw as Enrichment['difficulty'])
      : 'Medium';

  return {
    hint1: asString(o.hint1),
    hint2: asString(o.hint2),
    hint3: asString(o.hint3),
    stepByStep,
    misconceptionA: asString(o.misconceptionA),
    misconceptionB: asString(o.misconceptionB),
    misconceptionC: asString(o.misconceptionC),
    misconceptionD: asString(o.misconceptionD),
    difficulty,
  };
}

/**
 * Generate the teaching layer for a verified textbook MCQ. The model is told the
 * correct answer and must build hints / steps / misconceptions toward it only —
 * it must never restate or change the math.
 */
export async function enrichTextbookQuestion(req: EnrichmentRequest): Promise<Enrichment> {
  const options = `A) ${req.options.option1}\nB) ${req.options.option2}\nC) ${req.options.option3}\nD) ${req.options.option4}`;

  const system = `You are an expert IPM (International Primary Math) teacher adding a TEACHING LAYER to an existing exam question for a ${gradeDescriptor(req.grade)}.

You are given a question, its four options, and its VERIFIED correct answer. The answer is already confirmed — your job is ONLY to help a student understand how to reach it.

CRITICAL GROUNDING RULES:
- The correct answer is FIXED and given to you. Build every hint, step, and explanation TOWARD that answer. NEVER contradict it, re-derive a different answer, or change any number in the question.
- hint1 = a strategic nudge (what kind of problem is this?); hint2 = the first concrete procedural step; hint3 = a worked example of a SIMILAR (not identical) problem — never reveal this question's final answer.
- stepByStep must walk through the full solution to the GIVEN correct answer, using latex where it clarifies the math.
- For EACH option, the misconception field names the exact student mistake that would lead someone to pick it. For the correct option, briefly say why it is right.
- Classify the question's difficulty as "Easy", "Medium", or "Hard" for this grade.

${kidSafeRules(req.grade)}

Return ONLY a JSON object (no prose, no markdown fences) with EXACTLY these keys:
{
  "hint1": string, "hint2": string, "hint3": string,
  "stepByStep": [ { "step": number, "text": string, "latex"?: string } ],
  "misconceptionA": string, "misconceptionB": string, "misconceptionC": string, "misconceptionD": string,
  "difficulty": "Easy" | "Medium" | "Hard"
}`;

  const userPrompt = `Topic: ${req.topicName}\nSub-topic: ${req.subTopic || 'general'}\n\nQuestion:\n${req.questionText}\n\nOptions:\n${options}\n\nVERIFIED correct answer: ${req.correctAnswer}\n\nWrite the teaching layer now as a single JSON object.`;

  const { text } = await complete({
    model: 'opus',
    maxTokens: 1600,
    temperature: 0.7,
    system,
    messages: [{ role: 'user', content: userPrompt }],
  });

  return normalizeEnrichment(extractJson(text));
}

export interface FreshSolveResult {
  /** Agreed option, or null when there was no majority (caller must reject). */
  correctKey: 'A' | 'B' | 'C' | 'D' | null;
  /** Fraction of samples backing the winner (0–1). */
  agreement: number;
  /** True when consensus was imperfect (resolved via tie-break). */
  flagged: boolean;
}

const FRESH_SAMPLES = 3;

/** Pull a single option letter (A–D) from a model's "FINAL: X" line. */
function extractKey(text: string): 'A' | 'B' | 'C' | 'D' | null {
  const m = text.match(/FINAL:\s*([A-Da-d])\b/);
  if (!m) return null;
  const k = m[1].toUpperCase();
  return (ANSWER_KEYS as readonly string[]).includes(k) ? (k as 'A' | 'B' | 'C' | 'D') : null;
}

/**
 * Decide the correct option for a textbook MCQ by self-consistency. Mirrors
 * `solveFresh` in solve.ts but constrained to pick one of the four options and to
 * return a key only when a genuine majority agrees — otherwise null so the import
 * route rejects the question rather than exposing a shaky answer to a child.
 */
export async function solveTextbookFresh(
  questionText: string,
  options: TextbookOptions,
  grade: number,
): Promise<FreshSolveResult> {
  const optionBlock = `A) ${options.option1}\nB) ${options.option2}\nC) ${options.option3}\nD) ${options.option4}`;

  const system = `You are a meticulous math checker solving a multiple-choice question for a ${gradeDescriptor(grade)}. Work it out step by step, then on the LAST line write exactly "FINAL: X" where X is the single correct option letter (A, B, C, or D). Exactly one option is correct.`;

  const userPrompt = `Question:\n${questionText}\n\nOptions:\n${optionBlock}`;

  const draw = (temperature: number) =>
    complete({
      model: 'sonnet',
      maxTokens: 700,
      temperature,
      system,
      messages: [{ role: 'user', content: userPrompt }],
    }).then((r) => extractKey(r.text));

  const samples = await Promise.all(
    Array.from({ length: FRESH_SAMPLES }, () => draw(0.7)),
  );

  const tally = new Map<string, number>();
  for (const key of samples) {
    if (!key) continue;
    tally.set(key, (tally.get(key) ?? 0) + 1);
  }

  const pickTop = (): { key: 'A' | 'B' | 'C' | 'D'; count: number } | null => {
    let top: { key: 'A' | 'B' | 'C' | 'D'; count: number } | null = null;
    for (const [key, count] of Array.from(tally.entries())) {
      if (!top || count > top.count) top = { key: key as 'A' | 'B' | 'C' | 'D', count };
    }
    return top;
  };

  const majority = pickTop();
  if (majority && majority.count >= 2) {
    return {
      correctKey: majority.key,
      agreement: majority.count / FRESH_SAMPLES,
      flagged: majority.count < FRESH_SAMPLES,
    };
  }

  // No majority among the samples → one deterministic tie-break vote. Only accept
  // it if it joins an earlier vote to form a real majority; otherwise reject.
  const tieKey = await draw(0);
  if (tieKey) {
    const combined = (tally.get(tieKey) ?? 0) + 1;
    if (combined >= 2) {
      return { correctKey: tieKey, agreement: combined / (FRESH_SAMPLES + 1), flagged: true };
    }
  }

  return { correctKey: null, agreement: majority ? majority.count / FRESH_SAMPLES : 0, flagged: true };
}
