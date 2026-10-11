/**
 * Feature 5a — Solve-on-demand.
 *
 * Two paths, both gated by `AI_SOLVE_ENABLED`:
 *
 *  - `solveGrounded(questionId)` — the problem exists in our DB, so the answer is
 *    already verified. We merely RE-EXPRESS the verified answer/steps for the
 *    student (Haiku). Truth is unchanged → no verification needed.
 *
 *  - `solveFresh(problemText)` — homework typed by the student. There is no
 *    verified answer, so we run SELF-CONSISTENCY: N independent Sonnet samples,
 *    require a majority to agree on the final answer, and always append a
 *    "double-check this yourself" disclaimer. Low agreement → flagged + a
 *    gentle suggestion to ask Sparky in Chat.
 *
 * Per CLAUDE.md, fresh solves are NEVER fed into graded practice.
 */

import { parseUnknownArray } from '@/lib/jsonFields';
import { prisma } from '@/lib/db';
import { complete } from './complete';
import { gradeDescriptor, kidSafeRules } from './guardrails';
import { buildGroundedUserPrompt } from './grounding';
import { MODELS } from './models';

export const SOLVE_DISCLAIMER =
  '⚠️ I worked this out step by step, but I can make mistakes — always double-check it yourself!';

export interface SolveResult {
  /** Kid-friendly worked explanation (markdown-ish plain text). */
  explanation: string;
  /** "grounded" (verified DB answer) | "fresh" (self-consistency homework). */
  path: 'grounded' | 'fresh';
  /** The stated final answer (for logging). */
  answer: string;
  /** Agreement ratio for fresh solves (0–1); 1 for grounded. */
  agreement: number;
  /** True when consensus was weak and the result should be reviewed. */
  flagged: boolean;
  /** Model id used. */
  model: string;
}

const OPTION_KEYS = ['option1', 'option2', 'option3', 'option4'] as const;

/**
 * Re-express the verified answer + steps for a DB question. No verification
 * needed — the DB answer is ground truth.
 */
export async function solveGrounded(
  questionId: string,
  grade: number,
): Promise<SolveResult | null> {
  const q = await prisma.question.findUnique({
    where: { id: questionId },
    select: {
      questionText: true,
      option1: true,
      option2: true,
      option3: true,
      option4: true,
      correctAnswer: true,
      stepByStep: true,
    },
  });
  if (!q) return null;

  const correctIdx = ['A', 'B', 'C', 'D'].indexOf(q.correctAnswer);
  const verifiedAnswer =
    correctIdx >= 0 ? (q[OPTION_KEYS[correctIdx]] as string) : q.correctAnswer;

  const steps = parseUnknownArray(q.stepByStep)
    .map((s) => {
      if (!s || typeof s !== 'object') return '';
      const obj = s as { text?: unknown; latex?: unknown };
      const text = typeof obj.text === 'string' ? obj.text : '';
      const latex = typeof obj.latex === 'string' ? obj.latex : '';
      return latex ? `${text} (${latex})` : text;
    })
    .filter((t) => t.length > 0);

  const system = `You are Sparky, a warm math tutor for a ${gradeDescriptor(grade)}. Walk through the SOLUTION below in a few clear, friendly steps so the student understands HOW to get the answer.

${kidSafeRules(grade)}

Keep it short and clear. Number the steps.`;

  const userPrompt = buildGroundedUserPrompt({
    task: 'Explain how to solve this problem step by step for the student.',
    questionText: q.questionText,
    verifiedSteps: steps,
    verifiedAnswer,
  });

  const { text } = await complete({
    model: 'haiku',
    maxTokens: 500,
    system,
    messages: [{ role: 'user', content: userPrompt }],
  });

  return {
    explanation: text.trim(),
    path: 'grounded',
    answer: verifiedAnswer,
    agreement: 1,
    flagged: false,
    model: MODELS.haiku,
  };
}

/** Normalize a final-answer string for voting (case/space/punctuation-insensitive). */
function normalizeAnswer(raw: string): string {
  return raw
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/[.,;:!?'"()]+$/g, '')
    .trim();
}

/** Pull the "FINAL: ..." line the model is asked to emit. */
function extractFinal(text: string): string {
  const m = text.match(/FINAL:\s*(.+?)\s*$/im);
  return m ? m[1].trim() : '';
}

const FRESH_SAMPLES = 3;

/**
 * Solve a fresh homework problem via self-consistency. Requires a majority of
 * samples to agree; otherwise flags the result. Always appends the disclaimer.
 */
export async function solveFresh(
  problemText: string,
  grade: number,
): Promise<SolveResult> {
  const system = `You are Sparky, a careful math tutor for a ${gradeDescriptor(grade)}. Solve the problem step by step. Show your working clearly, then on the LAST line write exactly "FINAL: <your answer>".

${kidSafeRules(grade)}`;

  const userPrompt = `PROBLEM:\n${problemText.slice(0, 2000)}`;

  // Draw N independent samples at a non-zero temperature for diversity.
  const samples = await Promise.all(
    Array.from({ length: FRESH_SAMPLES }, () =>
      complete({
        model: 'sonnet',
        maxTokens: 700,
        temperature: 0.7,
        system,
        messages: [{ role: 'user', content: userPrompt }],
      }).then((r) => r.text),
    ),
  );

  // Tally votes on the normalized final answer.
  const votes = new Map<string, { count: number; display: string; full: string }>();
  for (const text of samples) {
    const final = extractFinal(text);
    if (!final) continue;
    const key = normalizeAnswer(final);
    if (!key) continue;
    const existing = votes.get(key);
    if (existing) existing.count += 1;
    else votes.set(key, { count: 1, display: final, full: text });
  }

  let winner: { count: number; display: string; full: string } | null = null;
  for (const v of Array.from(votes.values())) {
    if (!winner || v.count > winner.count) winner = v;
  }

  const majority = winner && winner.count >= Math.ceil(FRESH_SAMPLES / 2);

  if (majority && winner) {
    const agreement = winner.count / FRESH_SAMPLES;
    return {
      explanation: `${winner.full.trim()}\n\n${SOLVE_DISCLAIMER}`,
      path: 'fresh',
      answer: winner.display,
      agreement,
      flagged: agreement < 1, // perfect agreement = unflagged; partial = review
      model: MODELS.sonnet,
    };
  }

  // No majority → one deterministic tie-break pass, but flag it and be honest.
  const tieBreak = await complete({
    model: 'sonnet',
    maxTokens: 700,
    temperature: 0,
    system,
    messages: [{ role: 'user', content: userPrompt }],
  });
  const final = extractFinal(tieBreak.text);

  return {
    explanation: `${tieBreak.text.trim()}\n\nI wasn't fully sure on this one, so please double-check carefully — or ask Sparky in Chat for another look!\n\n${SOLVE_DISCLAIMER}`,
    path: 'fresh',
    answer: final,
    agreement: winner ? winner.count / FRESH_SAMPLES : 0,
    flagged: true,
    model: MODELS.sonnet,
  };
}
