/**
 * Safe parsers for Prisma fields that hold JSON as `String` columns.
 *
 * Several Student/Subscription/Question fields predate Prisma `Json` support
 * and are still typed `String @default("[]")` in `schema.prisma`. Until a
 * dedicated migration flips them to `Json`, every read site has to defensively
 * parse + validate the shape. This module centralises that work so a single
 * malformed row in the DB cannot crash a request path.
 *
 * The schema flip itself is a follow-up — see TODO comments on the relevant
 * fields in `prisma/schema.prisma`.
 */

/** Parse a JSON string into a `string[]`, returning `[]` on any failure. */
export function parseStringArray(raw: string | null | undefined): string[] {
  if (!raw) return [];
  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((x): x is string => typeof x === 'string');
  } catch {
    return [];
  }
}

/**
 * Parse a JSON string into a `Record<string, boolean>` (feature flags),
 * returning `{}` on any failure or non-object payload.
 */
export function parseFeatureFlags(raw: string | null | undefined): Record<string, boolean> {
  if (!raw) return {};
  try {
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return {};
    const out: Record<string, boolean> = {};
    for (const [k, v] of Object.entries(parsed)) {
      if (typeof v === 'boolean') out[k] = v;
    }
    return out;
  } catch {
    return {};
  }
}

/**
 * Parse a JSON string into an arbitrary `unknown[]` (e.g. `Question.stepByStep`).
 * Callers must narrow further before use.
 */
export function parseUnknownArray(raw: string | null | undefined): unknown[] {
  if (!raw) return [];
  try {
    const parsed: unknown = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}
