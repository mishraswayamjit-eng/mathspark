/**
 * Single source of truth for Anthropic model IDs used across the app.
 *
 * - `haiku`  — cheap/fast; available but not currently wired to any feature.
 * - `sonnet` — stronger reasoning; used for chat, grounded re-expression,
 *              narration, surfacing, stuck-step coaching, and grounded solve.
 * - `opus`   — strongest reasoning; reserved for the highest-stakes UNVERIFIED
 *              math generation (homework fresh-solve + AI question authoring),
 *              where correctness matters most and there is no verified fallback.
 */
export const MODELS = {
  haiku: 'claude-haiku-4-5-20251001',
  sonnet: 'claude-sonnet-4-6',
  opus: 'claude-opus-4-6',
} as const;

export type ModelKey = keyof typeof MODELS;
export type ModelId = (typeof MODELS)[ModelKey];
