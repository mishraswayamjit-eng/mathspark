/**
 * Feature 5b — AI-authored practice questions.
 *
 * Generates full question objects (text, 4 options, correct key, 3 hints,
 * step-by-step, 4 misconceptions) with Opus. Per the user's decision we TRUST
 * the model directly (no human-review queue) but add traceability + mitigations:
 *  - everything is tagged `source='ai_generated'` on persist (persistAuthored.ts)
 *  - an optional cheap sanity self-check (AI_QUESTIONS_SANITY, default-on)
 *    confirms the stated answer is internally consistent before persisting.
 *  - kill-switchable serving + ranked last + excluded from mock tests.
 */

import { complete } from './complete';
import { kidSafeRules, gradeDescriptor } from './guardrails';
import { MODELS } from './models';

export interface AuthorRequest {
  topicId: string;
  topicName: string;
  subTopic: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  grade: number;
  /** Existing question stems to steer away from (dedup / variety). */
  avoidStems?: string[];
}

export interface AuthoredStep {
  step: number;
  text: string;
  latex?: string;
}

export interface AuthoredQuestion {
  questionText: string;
  option1: string;
  option2: string;
  option3: string;
  option4: string;
  correctAnswer: 'A' | 'B' | 'C' | 'D';
  hint1: string;
  hint2: string;
  hint3: string;
  stepByStep: AuthoredStep[];
  misconceptionA: string;
  misconceptionB: string;
  misconceptionC: string;
  misconceptionD: string;
}

const ANSWER_KEYS = ['A', 'B', 'C', 'D'] as const;

/** Extract the first balanced JSON object from a model response. */
export function extractJson(text: string): unknown {
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start < 0 || end <= start) throw new Error('No JSON object in response');
  return JSON.parse(text.slice(start, end + 1));
}

export function asString(v: unknown): string {
  return typeof v === 'string' ? v.trim() : '';
}

/** Validate + normalize the raw parsed object into an AuthoredQuestion. */
function normalize(raw: unknown): AuthoredQuestion {
  if (!raw || typeof raw !== 'object') throw new Error('Authored question is not an object');
  const o = raw as Record<string, unknown>;

  const questionText = asString(o.questionText);
  const option1 = asString(o.option1);
  const option2 = asString(o.option2);
  const option3 = asString(o.option3);
  const option4 = asString(o.option4);
  const correctAnswer = asString(o.correctAnswer).toUpperCase();

  if (!questionText || !option1 || !option2 || !option3 || !option4) {
    throw new Error('Authored question missing text or options');
  }
  if (!ANSWER_KEYS.includes(correctAnswer as (typeof ANSWER_KEYS)[number])) {
    throw new Error(`Authored question has invalid correctAnswer: ${correctAnswer}`);
  }

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

  return {
    questionText,
    option1,
    option2,
    option3,
    option4,
    correctAnswer: correctAnswer as 'A' | 'B' | 'C' | 'D',
    hint1: asString(o.hint1),
    hint2: asString(o.hint2),
    hint3: asString(o.hint3),
    stepByStep,
    misconceptionA: asString(o.misconceptionA),
    misconceptionB: asString(o.misconceptionB),
    misconceptionC: asString(o.misconceptionC),
    misconceptionD: asString(o.misconceptionD),
  };
}

/** Per-difficulty depth expectations, so the question genuinely makes the student think. */
const DEPTH_BY_DIFFICULTY: Record<AuthorRequest['difficulty'], string> = {
  Easy: '2 clear solution steps, one core concept, with a small reasoning twist — never pure recall.',
  Medium: '3–4 solution steps that combine two sub-skills.',
  Hard: '4+ solution steps combining multiple concepts or requiring a non-obvious insight — true IPM-olympiad depth.',
};

/** Generate a single AI-authored question for the given slot. */
export async function authorQuestion(req: AuthorRequest): Promise<AuthoredQuestion> {
  const system = `You are an expert IPM (International Primary Math) olympiad question author writing original multiple-choice practice for a ${gradeDescriptor(req.grade)}.

Write ONE original, factually-correct, unambiguous question with real DEPTH — it must make the student genuinely THINK, not just recall a fact.

DEPTH REQUIREMENTS:
- Prefer a rich, real-world word problem with an Indian context (rupees, cricket, festivals, trains, markets) over bare computation.
- Depth for THIS question (${req.difficulty}): ${DEPTH_BY_DIFFICULTY[req.difficulty]}
- Each of the 3 wrong options must be the result of a SPECIFIC, plausible student mistake (e.g. forgot to convert units, used the wrong operation, off-by-one). No random or silly distractors.
- Each misconception field names the exact mistake that leads to that option.
- hint1 = strategic nudge; hint2 = the first procedural step; hint3 = a worked example of a SIMILAR (not identical) problem — never reveal this question's final answer.
- stepByStep must show every step a student needs, using latex where it clarifies the math.

${kidSafeRules(req.grade)}

Return ONLY a JSON object (no prose, no markdown fences) with EXACTLY these keys:
{
  "questionText": string,
  "option1": string, "option2": string, "option3": string, "option4": string,
  "correctAnswer": "A" | "B" | "C" | "D",
  "hint1": string, "hint2": string, "hint3": string,
  "stepByStep": [ { "step": number, "text": string, "latex"?: string } ],
  "misconceptionA": string, "misconceptionB": string, "misconceptionC": string, "misconceptionD": string
}
The correctAnswer MUST be the genuinely correct option. Exactly one option is correct.`;

  const avoidBlock =
    req.avoidStems && req.avoidStems.length
      ? `\n\nDo NOT duplicate or lightly reword any of these existing questions:\n${req.avoidStems
          .map((s) => `- ${s.slice(0, 140)}`)
          .join('\n')}`
      : '';

  const userPrompt = `Topic: ${req.topicName}\nSub-topic: ${req.subTopic || 'general'}\nDifficulty: ${req.difficulty}${avoidBlock}\n\nWrite the question now as a single JSON object.`;

  const { text } = await complete({
    model: 'opus',
    maxTokens: 1600,
    temperature: 0.8,
    system,
    messages: [{ role: 'user', content: userPrompt }],
  });

  return normalize(extractJson(text));
}

/**
 * Cheap second-pass sanity check: ask a model to independently solve the
 * question and confirm whether the stated correctAnswer is right. Returns true
 * when consistent. Any parse/response failure returns false (reject → safer).
 */
export async function sanityCheck(
  q: AuthoredQuestion,
  grade: number,
): Promise<boolean> {
  const system = `You are a meticulous math checker. Solve the multiple-choice question yourself, then say whether the claimed correct option is actually correct. Reply with ONLY a JSON object: { "correctKey": "A"|"B"|"C"|"D", "matchesClaim": boolean }.`;

  const options = `A) ${q.option1}\nB) ${q.option2}\nC) ${q.option3}\nD) ${q.option4}`;
  const userPrompt = `Question (Grade ${grade}):\n${q.questionText}\n\nOptions:\n${options}\n\nClaimed correct answer: ${q.correctAnswer}\n\nCheck it.`;

  try {
    const { text } = await complete({
      model: 'opus',
      maxTokens: 300,
      temperature: 0,
      system,
      messages: [{ role: 'user', content: userPrompt }],
    });
    const parsed = extractJson(text) as { correctKey?: unknown; matchesClaim?: unknown };
    const key = asString(parsed.correctKey).toUpperCase();
    return parsed.matchesClaim === true && key === q.correctAnswer;
  } catch {
    return false;
  }
}
