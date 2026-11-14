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
  | { type: 'rightTriangle'; base: number; height: number; unit?: string; title?: string }
  | { type: 'circle'; radius: number; unit?: string; title?: string }
  | { type: 'barChart'; bars: BarChartBar[]; unit?: string; showMean?: boolean; title?: string }
  | { type: 'clock'; hour: number; minute: number; title?: string }
  | { type: 'calendar'; year: number; month: number; day?: number; title?: string }
  | { type: 'money'; amount: number; title?: string }
  | { type: 'journey'; speed: number; hours: number; speedB?: number; unit?: string; labelA?: string; labelB?: string; title?: string }
  | { type: 'unitLadder'; quantity: 'length' | 'mass' | 'capacity'; value: number; from: string; to: string; title?: string }
  | { type: 'profitLoss'; cost: number; selling: number; title?: string }
  | { type: 'simpleInterest'; principal: number; rate: number; years: number; title?: string }
  | { type: 'mixedNumber'; whole: number; numerator: number; denominator: number; title?: string }
  | { type: 'fractionSet'; total: number; denominator: number; numerator: number; item?: string; title?: string }
  | { type: 'factorTree'; number: number; title?: string }
  | { type: 'venn'; a: number; b: number; mode: 'factors' | 'primes'; title?: string }
  | { type: 'hundredChart'; mark: 'multiples' | 'primes' | 'squares'; of: number; title?: string }
  | { type: 'placeChart'; number: number; title?: string }
  | { type: 'figurate'; kind: 'square' | 'triangular'; n: number; title?: string }
  | { type: 'areaModel'; a: number; b: number; title?: string }
  | { type: 'counters'; op: 'add' | 'subtract'; a: number; b: number; title?: string }
  | { type: 'magicSquare'; cells: number[]; title?: string }
  | { type: 'pictograph'; rows: BarChartBar[]; each: number; unit?: string; title?: string }
  | { type: 'symmetry'; shape: SymmetryShape; title?: string }
  | { type: 'cuboid'; length: number; width: number; height: number; unit?: string; title?: string }
  | { type: 'coordinateGrid'; points: GridPoint[]; join?: boolean; title?: string }
  | { type: 'quadrilateral'; kind: QuadKind; title?: string }
  | { type: 'parallelLines'; angle: number; title?: string };

export type SymmetryShape =
  | 'equilateral' | 'isosceles' | 'scalene' | 'square' | 'rectangle' | 'rhombus'
  | 'parallelogram' | 'kite' | 'pentagon' | 'hexagon' | 'octagon';

export type QuadKind = 'square' | 'rectangle' | 'parallelogram' | 'rhombus' | 'trapezium' | 'kite';

export interface GridPoint {
  x: number;
  y: number;
  label?: string;
}

const SYMMETRY_SHAPES: SymmetryShape[] = ['equilateral', 'isosceles', 'scalene', 'square', 'rectangle', 'rhombus', 'parallelogram', 'kite', 'pentagon', 'hexagon', 'octagon'];
const QUAD_KINDS: QuadKind[] = ['square', 'rectangle', 'parallelogram', 'rhombus', 'trapezium', 'kite'];
const UNIT_NAMES: Record<string, string[]> = {
  length: ['km', 'm', 'cm', 'mm'],
  mass: ['kg', 'g', 'mg'],
  capacity: ['kl', 'l', 'ml'],
};

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

    case 'rightTriangle': {
      const base = int(r.base, 1, 20);
      const height = int(r.height, 1, 20);
      return base === null || height === null ? null : { type: 'rightTriangle', base, height, unit: text(r.unit, 6), title };
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

    case 'clock': {
      const hour = int(r.hour, 0, 23);
      const minute = int(r.minute, 0, 59);
      if (hour === null || minute === null) return null;
      return { type: 'clock', hour: hour % 12 === 0 ? 12 : hour % 12, minute, title };
    }

    case 'calendar': {
      const year = int(r.year, 1900, 2100);
      const month = int(r.month, 1, 12);
      if (year === null || month === null) return null;
      const day = int(r.day, 1, 31);
      return { type: 'calendar', year, month, day: day === null ? undefined : day, title };
    }

    case 'money': {
      const amount = int(r.amount, 1, 5000);
      return amount === null ? null : { type: 'money', amount, title };
    }

    case 'journey': {
      const speed = int(r.speed, 1, 200);
      const hours = int(r.hours, 1, 12);
      if (speed === null || hours === null) return null;
      const speedB = int(r.speedB, 1, 200);
      return {
        type: 'journey', speed, hours, speedB: speedB === null ? undefined : speedB,
        unit: text(r.unit, 6), labelA: text(r.labelA, 12), labelB: text(r.labelB, 12), title,
      };
    }

    case 'unitLadder': {
      const quantity = r.quantity === 'mass' ? 'mass' : r.quantity === 'capacity' ? 'capacity' : 'length';
      const names = UNIT_NAMES[quantity];
      const value = num(r.value);
      if (value === null || value < 0 || value > 1000000) return null;
      const from = typeof r.from === 'string' && names.indexOf(r.from) !== -1 ? r.from : names[0];
      const to = typeof r.to === 'string' && names.indexOf(r.to) !== -1 ? r.to : names[1];
      return { type: 'unitLadder', quantity, value, from, to, title };
    }

    case 'profitLoss': {
      const cost = int(r.cost, 1, 100000);
      const selling = int(r.selling, 0, 100000);
      return cost === null || selling === null ? null : { type: 'profitLoss', cost, selling, title };
    }

    case 'simpleInterest': {
      const principal = int(r.principal, 1, 1000000);
      const rate = int(r.rate, 1, 20);
      const years = int(r.years, 1, 10);
      return principal === null || rate === null || years === null ? null : { type: 'simpleInterest', principal, rate, years, title };
    }

    case 'mixedNumber': {
      const whole = int(r.whole, 0, 5);
      const denominator = int(r.denominator, 2, 12);
      const numerator = int(r.numerator, 0, 11);
      if (whole === null || denominator === null || numerator === null) return null;
      return { type: 'mixedNumber', whole, numerator: Math.min(numerator, denominator - 1), denominator, title };
    }

    case 'fractionSet': {
      const total = int(r.total, 2, 60);
      const denominator = int(r.denominator, 2, 12);
      const numerator = int(r.numerator, 0, 12);
      if (total === null || denominator === null || numerator === null) return null;
      // The set must share out equally, with groups small enough to draw.
      if (total % denominator !== 0 || total / denominator > 12) return null;
      return { type: 'fractionSet', total, denominator, numerator: Math.min(numerator, denominator), item: text(r.item, 14), title };
    }

    case 'factorTree': {
      const number = int(r.number, 2, 200);
      return number === null ? null : { type: 'factorTree', number, title };
    }

    case 'venn': {
      const a = int(r.a, 2, 100);
      const b = int(r.b, 2, 100);
      return a === null || b === null ? null : { type: 'venn', a, b, mode: r.mode === 'primes' ? 'primes' : 'factors', title };
    }

    case 'hundredChart': {
      const of = int(r.of, 2, 12);
      const mark = r.mark === 'primes' ? 'primes' : r.mark === 'squares' ? 'squares' : 'multiples';
      return { type: 'hundredChart', mark, of: of === null ? 2 : of, title };
    }

    case 'placeChart': {
      const number = num(r.number);
      if (number === null || number < 0 || number > 999999999) return null;
      return { type: 'placeChart', number: Math.round(number * 1000) / 1000, title };
    }

    case 'figurate': {
      const n = int(r.n, 1, 10);
      return n === null ? null : { type: 'figurate', kind: r.kind === 'triangular' ? 'triangular' : 'square', n, title };
    }

    case 'areaModel': {
      const a = int(r.a, 1, 99);
      const b = int(r.b, 1, 99);
      return a === null || b === null ? null : { type: 'areaModel', a, b, title };
    }

    case 'counters': {
      const subtract = r.op === 'subtract';
      const a = int(r.a, 0, subtract ? 20 : 10);
      const b = int(r.b, 0, subtract ? 20 : 10);
      if (a === null || b === null) return null;
      return { type: 'counters', op: subtract ? 'subtract' : 'add', a, b: subtract ? Math.min(b, a) : b, title };
    }

    case 'magicSquare': {
      if (!Array.isArray(r.cells) || r.cells.length !== 9) return null;
      const cells: number[] = [];
      for (let i = 0; i < 9; i++) {
        const v = int(r.cells[i], 0, 99);
        if (v === null) return null;
        cells.push(v);
      }
      return { type: 'magicSquare', cells, title };
    }

    case 'pictograph': {
      const each = int(r.each, 1, 1000);
      if (each === null || !Array.isArray(r.rows)) return null;
      const rows: BarChartBar[] = [];
      for (let i = 0; i < r.rows.length && rows.length < 6; i++) {
        const row = r.rows[i] as Record<string, unknown> | null;
        if (!row) continue;
        const value = num(row.value);
        const label = text(row.label, 14);
        // Keep each row short enough to read: at most 12 symbols.
        if (value === null || value < 0 || !label || value / each > 12) continue;
        rows.push({ label, value });
      }
      return rows.length < 2 ? null : { type: 'pictograph', rows, each, unit: text(r.unit, 12), title };
    }

    case 'symmetry': {
      const shape = SYMMETRY_SHAPES.filter((s) => s === r.shape)[0];
      return shape ? { type: 'symmetry', shape, title } : null;
    }

    case 'cuboid': {
      const length = int(r.length, 1, 8);
      const width = int(r.width, 1, 8);
      const height = int(r.height, 1, 8);
      return length === null || width === null || height === null ? null : { type: 'cuboid', length, width, height, unit: text(r.unit, 6), title };
    }

    case 'coordinateGrid': {
      const points: GridPoint[] = [];
      if (Array.isArray(r.points)) {
        for (let i = 0; i < r.points.length && points.length < 8; i++) {
          const p = r.points[i] as Record<string, unknown> | null;
          if (!p) continue;
          const x = int(p.x, -8, 10);
          const y = int(p.y, -8, 10);
          if (x === null || y === null) continue;
          points.push({ x, y, label: text(p.label, 2) });
        }
      }
      // With a negative coordinate the grid runs from -8 to 8, so nothing may sit beyond 8.
      let negative = false;
      for (let i = 0; i < points.length; i++) if (points[i].x < 0 || points[i].y < 0) negative = true;
      if (negative) for (let i = 0; i < points.length; i++) if (points[i].x > 8 || points[i].y > 8) return null;
      return { type: 'coordinateGrid', points, join: r.join === true, title };
    }

    case 'quadrilateral': {
      const kind = QUAD_KINDS.filter((k) => k === r.kind)[0];
      return kind ? { type: 'quadrilateral', kind, title } : null;
    }

    case 'parallelLines': {
      const angle = int(r.angle, 30, 150);
      return angle === null ? null : { type: 'parallelLines', angle: Math.round(angle / 5) * 5, title };
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
