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

/**
 * The model that looks at the pencil pad for the live board coach
 * (`/api/coach/board`).
 *
 * Default: `sonnet` (Claude Sonnet 4.6). The reasons, in order:
 * - A child is waiting, so the reply must come back in a couple of seconds.
 *   The chat model (Claude Opus 5.5) always thinks before it answers and that
 *   cannot be turned off, so it is too slow here, and a small `max_tokens`
 *   could be used up by the thinking before any reply is written. Sonnet 4.6
 *   does not think unless asked to, and the coach does not ask.
 * - It has to read a child's handwriting and find the line where the working
 *   went astray. `haiku` would be quicker still, but it is the weakest reader
 *   of messy handwriting, and a coach that misreads a 7 as a 1 and "corrects"
 *   a line that was fine does more harm than one that takes a second longer.
 * - The coach sends no `temperature` and no `thinking` setting, so the request
 *   is one every model in `MODELS` accepts.
 *
 * Override with the `AI_BOARD_COACH_MODEL` environment variable (a full model
 * id, for example the `haiku` id above for more speed). If the override is a
 * model that always thinks, the coach's small `max_tokens` will need raising
 * in `boardCoach.ts` as well.
 */
export function boardCoachModel(): string {
  const override = process.env.AI_BOARD_COACH_MODEL;
  return override && override.trim() ? override.trim() : MODELS.sonnet;
}
