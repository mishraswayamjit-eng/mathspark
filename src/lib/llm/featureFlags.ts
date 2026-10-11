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
