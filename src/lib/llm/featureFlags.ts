/**
 * Environment kill-switches for LLM generation features.
 *
 * Delivery features (misconception nudge, narratives, lesson re-explain,
 * stuck-coach) are NOT gated here — they only re-express verified data and
 * degrade gracefully to static fallbacks. Generation features (solve, authored
 * questions, surfacing) ARE gated so they can be disabled instantly via Vercel
 * env vars without a redeploy of logic.
 *
 * All flags default to OFF (must be explicitly set to "true"/"1"/"on").
 */

function flag(name: string): boolean {
  const v = process.env[name];
  if (!v) return false;
  const s = v.trim().toLowerCase();
  return s === 'true' || s === '1' || s === 'on' || s === 'yes';
}

/** Feature 5a: /solve endpoint (grounded + homework self-consistency). */
export function isAiSolveEnabled(): boolean {
  return flag('AI_SOLVE_ENABLED');
}

/** Feature 5b: allow the admin generation endpoint to author questions. */
export function isAiQuestionsEnabled(): boolean {
  return flag('AI_QUESTIONS_ENABLED');
}

/** Feature 5b: serve `source='ai_generated'` questions to students. */
export function isAiQuestionsServeEnabled(): boolean {
  return flag('AI_QUESTIONS_SERVE');
}

/**
 * Feature 5b: run a cheap second-pass sanity self-check before persisting an
 * authored question. Defaults to ON (opt-out) because it is a safety net.
 */
export function isAiQuestionsSanityEnabled(): boolean {
  const v = process.env.AI_QUESTIONS_SANITY;
  if (v === undefined) return true; // default-on
  const s = v.trim().toLowerCase();
  return !(s === 'false' || s === '0' || s === 'off' || s === 'no');
}

/** Feature 5c: LLM-driven surfacing/narration of Brain Engine analytics. */
export function isAiSurfaceEnabled(): boolean {
  return flag('AI_SURFACE_ENABLED');
}

/**
 * IPM-textbook import: serve `source='ipm_textbook'` questions to students.
 * Separate from `AI_QUESTIONS_SERVE` so the imported exam-authentic bank can be
 * toggled independently of synthetic authored questions. Default OFF.
 */
export function isAiTextbookServeEnabled(): boolean {
  return flag('AI_TEXTBOOK_SERVE');
}

/**
 * Equal surfacing: when ON, all *eligible* question sources (hand_crafted,
 * pdf_extracted, variants, ipm_textbook, ai_generated, …) are surfaced with no
 * source-quality tiering — adaptive practice draws uniformly across sources and
 * generated sources become mock-eligible (subject to their own serve flags).
 *
 * It removes source-quality ranking bias in adaptive practice and additionally
 * lifts the mock-test exclusion of `ai_generated` (still requiring its own serve
 * flag). It does NOT bypass any safety gate: verification still runs at
 * import/author time, and a source is eligible only when its serve flag allows it
 * (`AI_QUESTIONS_SERVE` / `AI_TEXTBOOK_SERVE`). Default OFF.
 */
export function isEqualSurfacingEnabled(): boolean {
  return flag('EQUAL_SURFACING');
}
