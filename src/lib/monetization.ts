/**
 * monetization.ts — Master switch for ALL payment / subscription / trial /
 * usage-limit / grade-lock features.
 *
 * When `MONETIZATION_ENABLED` is false (current default), monetization is fully
 * OFF: every student gets unlimited free access — no trial question caps, no
 * daily-minute limits, no feature/tier gates, no grade locks — and the pricing /
 * upgrade UI is hidden.
 *
 * Flip to `true` and redeploy to restore the full paywall exactly as it was.
 * This is the single point of control: no DB rows, env vars, or schema changes
 * are required to toggle it. The payment routes, Razorpay integration, plan seed
 * data, and `gradeAccess.ts` rules all remain intact and untouched.
 */
export const MONETIZATION_ENABLED = false;

/**
 * The subscription tier reported to clients when monetization is OFF.
 * 3 = "Unlimited" → `gradeAccess` grants full access to every grade, and all
 * tier-gated UI (grade locks, mega test, grade-up CTA) unlocks.
 */
export const UNLIMITED_TIER = 3;
