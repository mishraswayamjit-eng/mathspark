/**
 * Sparky's whiteboard: the library of interactive visuals the tutor can show.
 *
 * The model never writes HTML or code. It names one visual from this library
 * and gives a few numbers, as a single tag at the start of its reply:
 *
 *     <visual>{"type":"fraction","shape":"bar","parts":8,"shaded":3}</visual>
 *
 * The tag travels inside the reply text (so it is saved and reloaded with the
 * conversation, with no database change). The app strips it out of the visible
 * text, validates and clamps every field here, and draws the visual with its
 * own components in the app's design system.
 *
 * This is a teaching aid in chat only. It never feeds grading, XP or mastery.
 */

export type VisualSpec =
  | { type: 'fraction'; shape: 'bar' | 'circle'; parts: number; shaded: number; compare?: { parts: number; shaded: number }; title?: string }
  | { type: 'numberLine'; min: number; max: number; step: number; point?: number; jumpFrom?: number; jumpTo?: number; title?: string }
  | { type: 'placeValue'; number: number; title?: string }
  | { type: 'array'; rows: number; cols: number; title?: string }
  | { type: 'barModel'; bars: BarModelBar[]; unit?: string; title?: string }
  | { type: 'balance'; leftX: number; leftUnits: number; rightX: number; rightUnits: number; variable?: string; title?: string }
  | { type: 'rectangle'; width: number; height: number; unit?: string; title?: string }
  | { type: 'angle'; degrees: number; title?: string }
  | { type: 'percentGrid'; percent: number; title?: string }
  | { type: 'container'; capacity: number; filled: number; unit?: string; title?: string }
  | { type: 'polygon'; sides: number; title?: string }
  | { type: 'tiling'; sides: number; count: number; title?: string }
  | { type: 'triangle'; angleA: number; angleB: number; title?: string }
  | { type: 'circle'; radius: number; unit?: string; title?: string }
  | { type: 'barChart'; bars: BarChartBar[]; unit?: string; showMean?: boolean; title?: string };

export type VisualKind = VisualSpec['type'];

export interface BarModelSegment {
  /** Size of the piece. Use 0 with `unknown: true` for the piece being found. */
  value: number;
  label?: string;
  /** Draw as the unknown ("?") the child is finding. */
  unknown?: boolean;
}

export interface BarChartBar {
  label: string;
  value: number;
}

export interface BarModelBar {
  label?: string;
  segments: BarModelSegment[];
}

// ── Validation ───────────────────────────────────────────────────────────────

function num(v: unknown): number | null {
  return typeof v === 'number' && isFinite(v) ? v : null;
}

function int(v: unknown, min: number, max: number): number | null {
  const n = num(v);
  if (n === null) return null;
  return Math.min(max, Math.max(min, Math.round(n)));
}

function text(v: unknown, maxLen: number): string | undefined {
  if (typeof v !== 'string') return undefined;
  const cleaned = v.replace(/[<>]/g, '').trim().slice(0, maxLen);
  return cleaned || undefined;
}

/** Turn untrusted JSON into a safe, clamped spec, or null if it is not usable. */
export function parseVisualSpec(raw: unknown): VisualSpec | null {
  if (!raw || typeof raw !== 'object') return null;
  const r = raw as Record<string, unknown>;
  const title = text(r.title, 60);

  switch (r.type) {
    case 'fraction': {
      const parts = int(r.parts, 1, 12);
      const shaded = int(r.shaded, 0, 12);
      if (parts === null || shaded === null) return null;
      let compare: { parts: number; shaded: number } | undefined;
      const c = r.compare as Record<string, unknown> | undefined;
      if (c && typeof c === 'object') {
        const cp = int(c.parts, 1, 12);
        const cs = int(c.shaded, 0, 12);
        if (cp !== null && cs !== null) compare = { parts: cp, shaded: Math.min(cs, cp) };
      }
      return {
        type: 'fraction',
        shape: r.shape === 'circle' ? 'circle' : 'bar',
        parts,
        shaded: Math.min(shaded, parts),
        compare,
        title,
      };
    }

    case 'numberLine': {
      const min = num(r.min);
      const max = num(r.max);
      const step = num(r.step);
      if (min === null || max === null || step === null || step <= 0 || max <= min) return null;
      // Keep the line readable: at most 40 steps.
      if ((max - min) / step > 40) return null;
      const inRange = (v: unknown): number | undefined => {
        const n = num(v);
        return n !== null && n >= min && n <= max ? n : undefined;
      };
      return {
        type: 'numberLine', min, max, step,
        point: inRange(r.point), jumpFrom: inRange(r.jumpFrom), jumpTo: inRange(r.jumpTo), title,
      };
    }

    case 'placeValue': {
      const number = int(r.number, 0, 9999);
      return number === null ? null : { type: 'placeValue', number, title };
    }

    case 'array': {
      const rows = int(r.rows, 1, 12);
      const cols = int(r.cols, 1, 12);
      return rows === null || cols === null ? null : { type: 'array', rows, cols, title };
    }

    case 'barModel': {
      if (!Array.isArray(r.bars)) return null;
      const bars: BarModelBar[] = [];
      for (let b = 0; b < r.bars.length && bars.length < 3; b++) {
        const bar = r.bars[b] as Record<string, unknown> | null;
        if (!bar || !Array.isArray(bar.segments)) continue;
        const segments: BarModelSegment[] = [];
        for (let s = 0; s < bar.segments.length && segments.length < 12; s++) {
          const seg = bar.segments[s] as Record<string, unknown> | null;
          if (!seg) continue;
          const unknown = seg.unknown === true;
          const value = num(seg.value);
          if (!unknown && (value === null || value <= 0)) continue;
          segments.push({ value: value !== null && value > 0 ? value : 0, label: text(seg.label, 24), unknown });
        }
        if (segments.length > 0) bars.push({ label: text(bar.label, 24), segments });
      }
      return bars.length === 0 ? null : { type: 'barModel', bars, unit: text(r.unit, 12), title };
    }

    case 'balance': {
      const leftX = int(r.leftX, 0, 6);
      const leftUnits = int(r.leftUnits, 0, 30);
      const rightX = int(r.rightX, 0, 6);
      const rightUnits = int(r.rightUnits, 0, 30);
      if (leftX === null || leftUnits === null || rightX === null || rightUnits === null) return null;
      if (leftX + rightX === 0) return null;
      const variable = text(r.variable, 1);
      return { type: 'balance', leftX, leftUnits, rightX, rightUnits, variable: variable && /^[a-z]$/i.test(variable) ? variable : 'x', title };
    }

    case 'rectangle': {
      const width = int(r.width, 1, 20);
      const height = int(r.height, 1, 20);
      return width === null || height === null ? null : { type: 'rectangle', width, height, unit: text(r.unit, 6), title };
    }

    case 'angle': {
      const degrees = int(r.degrees, 0, 360);
      return degrees === null ? null : { type: 'angle', degrees, title };
    }

    case 'percentGrid': {
      const percent = int(r.percent, 0, 100);
      return percent === null ? null : { type: 'percentGrid', percent, title };
    }

    case 'container': {
      const capacity = num(r.capacity);
      const filled = num(r.filled);
      if (capacity === null || filled === null || capacity <= 0 || filled < 0) return null;
      return { type: 'container', capacity, filled: Math.min(filled, capacity), unit: text(r.unit, 6), title };
    }

    case 'polygon': {
      const sides = int(r.sides, 3, 12);
      return sides === null ? null : { type: 'polygon', sides, title };
    }

    case 'tiling': {
      const sides = int(r.sides, 3, 6);
      if (sides === null) return null;
      const count = int(r.count, 0, 6);
      return { type: 'tiling', sides, count: count === null ? 1 : count, title };
    }

    case 'triangle': {
      const angleA = int(r.angleA, 10, 160);
      const angleB = int(r.angleB, 10, 160);
      if (angleA === null || angleB === null || angleA + angleB > 170) return null;
      return { type: 'triangle', angleA, angleB, title };
    }

    case 'circle': {
      const radius = int(r.radius, 1, 20);
      return radius === null ? null : { type: 'circle', radius, unit: text(r.unit, 6), title };
    }

    case 'barChart': {
      if (!Array.isArray(r.bars)) return null;
      const bars: BarChartBar[] = [];
      for (let b = 0; b < r.bars.length && bars.length < 8; b++) {
        const bar = r.bars[b] as Record<string, unknown> | null;
        if (!bar) continue;
        const value = num(bar.value);
        const label = text(bar.label, 14);
        if (value === null || value < 0 || !label) continue;
        bars.push({ label, value });
      }
      return bars.length < 2 ? null : { type: 'barChart', bars, unit: text(r.unit, 10), showMean: r.showMean === true, title };
    }

    default:
      return null;
  }
}

// ── Pulling the tag out of a reply ───────────────────────────────────────────

const OPEN = '<visual>';
const CLOSE = '</visual>';

export interface ExtractedReply {
  /** The reply with the visual tag removed: what the child reads and hears. */
  text: string;
  visual: VisualSpec | null;
  /** True while a tag has started streaming but has not closed yet. */
  pending: boolean;
}

/** Split a reply (complete or still streaming) into its visible text and its visual. */
export function extractVisual(raw: string): ExtractedReply {
  const start = raw.indexOf(OPEN);
  if (start === -1) {
    // A partly streamed opening tag ("<vis") must not flash on screen.
    for (let n = OPEN.length - 1; n > 0; n--) {
      if (raw.slice(-n) === OPEN.slice(0, n)) return { text: raw.slice(0, -n).trim(), visual: null, pending: true };
    }
    return { text: raw, visual: null, pending: false };
  }

  const end = raw.indexOf(CLOSE, start);
  if (end === -1) return { text: raw.slice(0, start).trim(), visual: null, pending: true };

  let visual: VisualSpec | null = null;
  try {
    visual = parseVisualSpec(JSON.parse(raw.slice(start + OPEN.length, end)));
  } catch {
    visual = null;   // malformed: show the reply without a visual
  }
  const text = `${raw.slice(0, start)}${raw.slice(end + CLOSE.length)}`.trim();
  return { text, visual, pending: false };
}
