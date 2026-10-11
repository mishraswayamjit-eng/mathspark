/**
 * Helpers for GROUNDING the model in pre-verified data.
 *
 * The governing safety principle (CLAUDE.md "Truth vs Delivery"): the LLM may
 * explain/rephrase/coach, but it is NEVER the arbiter of correctness. Every
 * grounded prompt injects the verified answer/steps and appends a RULES trailer
 * that forbids the model from asserting a different final answer.
 */

export interface GroundingFacts {
  /** The task/instruction for the model (what to produce). */
  task: string;
  /** The verified question text, if relevant. */
  questionText?: string;
  /** The verified correct answer (never to be contradicted). */
  verifiedAnswer?: string;
  /** Verified, ordered solution steps. */
  verifiedSteps?: string[];
  /** Any additional verified context block. */
  context?: string;
  /**
   * When true, the model must guide Socratically and must NOT state the final
   * answer outright (used by stuck-coach). When false, re-expressing the
   * verified answer is permitted.
   */
  withholdFinalAnswer?: boolean;
}

function clip(s: string, max = 2000): string {
  return s.replace(/\u0000/g, '').slice(0, max);
}

/**
 * Build a user prompt that is grounded in verified facts and carries a RULES
 * trailer. The RULES are what make generation reversible/auditable: they pin
 * the model to the verified truth.
 */
export function buildGroundedUserPrompt(facts: GroundingFacts): string {
  const parts: string[] = [];

  parts.push(`TASK:\n${clip(facts.task, 1000)}`);

  if (facts.questionText) {
    parts.push(`QUESTION (verified):\n${clip(facts.questionText)}`);
  }
  if (facts.context) {
    parts.push(`CONTEXT (verified):\n${clip(facts.context)}`);
  }
  if (facts.verifiedSteps && facts.verifiedSteps.length > 0) {
    const steps = facts.verifiedSteps
      .map((s, i) => `${i + 1}. ${clip(s, 500)}`)
      .join('\n');
    parts.push(`VERIFIED SOLUTION STEPS:\n${steps}`);
  }
  if (facts.verifiedAnswer) {
    parts.push(`VERIFIED CORRECT ANSWER:\n${clip(facts.verifiedAnswer, 500)}`);
  }

  // RULES trailer — the guardrail that keeps truth deterministic.
  const rules: string[] = [
    'RULES:',
    '- The VERIFIED facts above are the ground truth. You must NEVER contradict them.',
  ];
  if (facts.withholdFinalAnswer) {
    rules.push(
      '- Do NOT state the final answer. Guide the student toward it with ONE small next step or question.',
    );
  } else if (facts.verifiedAnswer) {
    rules.push(
      '- If you state the answer, it MUST exactly match the VERIFIED CORRECT ANSWER. Never invent a different one.',
    );
  }
  rules.push('- If the verified data is insufficient, say so plainly rather than guessing.');
  parts.push(rules.join('\n'));

  return parts.join('\n\n');
}
