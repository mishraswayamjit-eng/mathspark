/**
 * usageLimits.ts — Single source of truth for all plan usage limits.
 *
 * Update the constants here as real-world usage data informs pricing.
 * These values must match (or intentionally override) what is seeded
 * into the Subscription table in prisma/seed.ts.
 *
 * Hard-coding in DB rows AND here creates drift risk, so the heartbeat
 * and check routes import FREE_DAILY_MINUTES from here for the free-tier
 * default, while paid limits come from subscription.dailyLimitMinutes.
 */

// ── Free-tier defaults (no active subscription) ────────────────────────────

export const FREE_DAILY_MINUTES    = 30;   // minutes/day
export const FREE_AI_CHAT_DAILY    = 5;    // AI messages/day

// ── What counts as "effectively unlimited" ─────────────────────────────────
// Unlimited plan seeds dailyLimitMinutes = 1440 (24 h). Any value ≥ this
// threshold is treated as unlimited — no gate, no bar shown.

export const UNLIMITED_THRESHOLD   = 1440;

// ── Upgrade copy shown on the limit screen ─────────────────────────────────
// Keep in sync with the Subscription seed rows + landing page copy.

export interface PlanUpgrade {
  name:       string;
  minutes:    number;   // daily minutes in the next plan
  priceLabel: string;
}

export const UPGRADE_PATHS: Record<number, PlanUpgrade> = {
  0: { name: 'Starter',   minutes: 60,   priceLabel: '₹500/mo' },
  1: { name: 'Advanced',  minutes: 300,  priceLabel: '₹1,500/mo' },
  2: { name: 'Unlimited', minutes: 1440, priceLabel: '₹5,000/mo' },
  // tier 3 (Unlimited) → no upgrade available
};

// ── Pure helper functions ──────────────────────────────────────────────────

/** True when the plan is effectively unlimited (no gate enforcement). */
export function isUnlimitedPlan(limitMinutes: number): boolean {
  return limitMinutes <= 0 || limitMinutes >= UNLIMITED_THRESHOLD;
}

/** Remaining daily minutes. Returns Infinity for unlimited plans. */
export function remainingMinutes(usedMinutes: number, limitMinutes: number): number {
  if (isUnlimitedPlan(limitMinutes)) return Infinity;
  return Math.max(0, limitMinutes - usedMinutes);
}

/** Whether the student may open a new practice session. */
export function isPracticeAllowed(usedMinutes: number, limitMinutes: number): boolean {
  if (isUnlimitedPlan(limitMinutes)) return true;
  return usedMinutes < limitMinutes;
}

/** Usage percentage 0-100 for progress bars. */
export function usagePct(usedMinutes: number, limitMinutes: number): number {
  if (isUnlimitedPlan(limitMinutes)) return 0; // unlimited: show empty bar
  return Math.min(100, Math.round((usedMinutes / limitMinutes) * 100));
}

/** Bar colour class based on usage percentage. */
export function usageBarColor(pct: number): string {
  if (pct >= 100) return 'bg-red-500';
  if (pct >= 75)  return 'bg-amber-500';
  return 'bg-[#58CC02]';
}

/** Human-readable minutes → "2 hr 15 min" or "45 min". */
export function formatMinutes(minutes: number): string {
  if (minutes <= 0) return '0 min';
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m === 0 ? `${h} hr` : `${h} hr ${m} min`;
}
