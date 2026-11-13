/**
 * Single source of truth for Anthropic model IDs used across the app.
 *
 * - `haiku`  — cheap/fast; available but not currently wired to any feature.
 * - `sonnet` — stronger reasoning; used for chat, grounded re-expression,
 *              narration, surfacing, stuck-step coaching, and grounded solve.
 * - `opus`   — strongest reasoning; reserved for the highest-stakes UNVERIFIED
 *              math generation (homework fresh-solve + AI question authoring),
 *              where correctness matters most and there is no verified fallback.
 * - `chat`   — Sparky, the conversational tutor. Claude Opus 5.5: it reasons
 *              before it answers (thinking is always on), which is what makes
 *              its checking of a child's answer reliable. Chat only: the other
 *              features send a `temperature`, which this model does not accept.
 */
export const MODELS = {
  haiku: 'claude-haiku-4-5-20251001',
  sonnet: 'claude-sonnet-4-6',
  opus: 'claude-opus-4-6',
  chat: 'claude-opus-5-5',
} as const;

export type ModelKey = keyof typeof MODELS;
export type ModelId = (typeof MODELS)[ModelKey];
