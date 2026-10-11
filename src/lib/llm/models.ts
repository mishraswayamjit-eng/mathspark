/**
 * Single source of truth for Anthropic model IDs used across the app.
 *
 * - `haiku`  — cheap/fast; used for grounded re-expression, narration, nudges.
 * - `sonnet` — stronger reasoning; used for stuck-step coaching, homework
 *              self-consistency solving, and AI question authoring.
 */
export const MODELS = {
  haiku: 'claude-haiku-4-5-20251001',
  sonnet: 'claude-sonnet-4-6',
} as const;

export type ModelKey = keyof typeof MODELS;
export type ModelId = (typeof MODELS)[ModelKey];
