/**
 * Question figures: the picture a question needs, and the pictures that go with
 * each step of its solution.
 *
 * THE CONTRACT. Three things are built against this file and must agree with it:
 *   - the renderer            src/components/figures/
 *   - the offline content     data/question-figures/parts/*.json  (checked by scripts/figures/validate.py)
 *   - the screens             practice, mock tests, review
 * Change a type here and scripts/figures/validate.py must change with it.
 *
 * Rules (enforced offline by the validator, never at runtime):
 *   1. `figure` shows GIVENS ONLY. Every number in it appears in the question
 *      text. The unknown is labelled "?". It must not give the answer away.
 *   2. A step figure may show only numbers stated in the question or in the
 *      steps up to and including that step.
 *   3. Nothing here is generated while a child uses the app, and nothing here
 *      feeds grading, XP or mastery.
 *
 * Labels are plain strings so they can hold units and unknowns: "20 cm", "?",
 * "(25 − y)°", "x". Keep labels short (at most 18 characters).
 */

/** Fields every figure may carry. */
interface FigureBase {
  /**
   * Parts to draw emphasised (thicker, Action Indigo). The keys each figure
   * understands are listed on its type.
   */
  highlight?: string[];
  /** One short line under the figure (at most 70 characters). Same number rules as labels. */
  note?: string;
}

/**
 * A triangle with corners A (top), B (bottom left), C (bottom right).
 * For shape 'right' the right angle is at B and is marked with a small square.
 * highlight keys: 'ab' 'bc' 'ca' (sides), 'a' 'b' 'c' (angles), 'height', 'fill'
 */
export interface TriangleFigure extends FigureBase {
  kind: 'triangle';
  shape: 'scalene' | 'right' | 'isosceles' | 'equilateral';
  /** Labels along the sides. */
  sides?: { ab?: string; bc?: string; ca?: string };
  /** Labels inside the corners. */
  angles?: { a?: string; b?: string; c?: string };
  /** Draws a dashed height from A down to BC with this label. */
  height?: string;
  /** Draws a dashed rectangle around the triangle (for "half of a rectangle"). */
  enclose?: boolean;
}

/**
 * A rectangle or square.
 * highlight keys: 'length' 'breadth' 'border' 'fill'
 */
export interface RectangleFigure extends FigureBase {
  kind: 'rectangle';
  square?: boolean;
  /** Label on the long (top) side. */
  length?: string;
  /** Label on the short (left) side. */
  breadth?: string;
  /** Text in the middle, e.g. "Area = ?". */
  inside?: string;
  /** Width divided by height, for drawing only (1 to 3). Default 1.6, or 1 for a square. */
  proportion?: number;
  /** Draw unit squares: columns across and rows down (each at most 12). */
  grid?: { cols: number; rows: number };
}

/**
 * Any straight-sided shape, given by its corners on a 0-12 grid (x right, y down).
 * Use for L-shapes, trapeziums, parallelograms and other composite shapes.
 * highlight keys: 'e0' 'e1' ... (edge i runs from corner i to corner i + 1), 'fill'
 */
export interface PolygonFigure extends FigureBase {
  kind: 'polygon';
  points: number[][];
  /** One label per edge, null for none. */
  edges?: Array<string | null>;
  /** One label per corner, null for none. */
  corners?: Array<string | null>;
  /** Corners (by index) to mark as right angles. */
  rightAngles?: number[];
  /** Dashed lines between corners, e.g. a diagonal or a cut. */
  dashed?: Array<{ from: number; to: number; label?: string }>;
}

/** highlight keys: 'radius' 'diameter' 'edge' 'fill' */
export interface CircleFigure extends FigureBase {
  kind: 'circle';
  radius?: string;
  diameter?: string;
}

/**
 * Angles at a point.
 *   single         one angle
 *   onLine         angles that together make a straight line (180°)
 *   inRightAngle   angles that together make a right angle (90°)
 *   aroundPoint    angles that together make a full turn (360°)
 *   crossing       two straight lines crossing: exactly four parts, clockwise from the top
 * `size` is how big to DRAW a part, in degrees. It is not shown as a number.
 * Give it only for a part whose size the question states; leave it out for the
 * unknown, which then takes whatever is left.
 * highlight keys: 'p0' 'p1' ...
 */
export interface AnglesFigure extends FigureBase {
  kind: 'angles';
  layout: 'single' | 'onLine' | 'inRightAngle' | 'aroundPoint' | 'crossing';
  parts: Array<{ label: string; size?: number }>;
}

/** highlight keys: 'hour' 'minute' 'angle' */
export interface ClockFigure extends FigureBase {
  kind: 'clock';
  /** 1 to 12. */
  hour: number;
  /** 0 to 59. */
  minute: number;
  /** Shade the angle between the hands. */
  showAngle?: boolean;
}

export type CompassPoint = 'N' | 'NE' | 'E' | 'SE' | 'S' | 'SW' | 'W' | 'NW';

/**
 * A compass with an arrow for the direction faced, and turns drawn as arcs in order.
 * highlight keys: 'start' 't0' 't1' ... 'end'
 */
export interface CompassFigure extends FigureBase {
  kind: 'compass';
  facing: CompassPoint;
  turns?: Array<{ degrees: number; direction: 'clockwise' | 'anticlockwise' }>;
  /** Draw the arrow for the direction faced after all the turns. */
  showEnd?: boolean;
}

/**
 * One to four fraction strips or circles, one under the other.
 * highlight keys: 'b0' 'b1' ...
 */
export interface FractionBarsFigure extends FigureBase {
  kind: 'fractionBars';
  shape?: 'bar' | 'circle';
  /** parts 1 to 24; shaded 0 to parts. */
  bars: Array<{ parts: number; shaded: number; label?: string }>;
}

/**
 * A set of counters, optionally shared into equal groups with some groups shaded.
 * Used for a fraction or a share of a quantity.
 * highlight keys: 'shaded'
 */
export interface SetFigure extends FigureBase {
  kind: 'set';
  /** 1 to 60. */
  total: number;
  /** Number of equal groups to box the counters into. Must divide `total`. */
  groups?: number;
  shadedGroups?: number;
  /** What the counters are, e.g. "marbles". */
  item?: string;
}

/**
 * Bars cut into labelled pieces: ratio, unitary method, ages, "more than / less than".
 * `units` is the drawn width of a piece relative to the others; it is never shown.
 * Draw an unknown piece the same width as its neighbours unless the question says otherwise.
 * highlight keys: 'b0s0' (bar 0, segment 0) ..., 'b0' (a whole bar)
 */
export interface BarModelFigure extends FigureBase {
  kind: 'barModel';
  /** One to three bars. */
  bars: Array<{
    label?: string;
    /** One to twelve pieces. */
    segments: Array<{ units: number; label?: string; tone?: 'a' | 'b' | 'c' | 'unknown' }>;
    /** A brace over the whole bar with this label, e.g. "40 sweets". */
    brace?: string;
  }>;
}

/**
 * highlight keys: 'p0' 'p1' ... (points), 'h0' 'h1' ... (hops)
 */
export interface NumberLineFigure extends FigureBase {
  kind: 'numberLine';
  min: number;
  max: number;
  /** Gap between ticks. At most 40 ticks. */
  step: number;
  points?: Array<{ at: number; label?: string }>;
  hops?: Array<{ from: number; to: number; label?: string }>;
}

/**
 * A road with two to four places and a labelled stretch between each pair.
 * highlight keys: 'l0' 'l1' ... (legs)
 */
export interface JourneyFigure extends FigureBase {
  kind: 'journey';
  places: string[];
  /** One per stretch (places.length − 1). `top` e.g. "60 km/h", `bottom` e.g. "3 h". */
  legs: Array<{ top?: string; bottom?: string }>;
}

/**
 * A number in the Indian place-value chart.
 * highlight keys: 'd0' 'd1' ... (digits, counted from the left, ignoring the decimal point)
 */
export interface PlaceChartFigure extends FigureBase {
  kind: 'placeChart';
  /** Digits only, with at most one decimal point: "2345678" or "34.56". At most 9 whole digits and 3 decimals. */
  number: string;
}

/**
 * A grid of unit squares.
 * highlight keys: none
 */
export interface GridFigure extends FigureBase {
  kind: 'grid';
  /** Each at most 12. */
  rows: number;
  cols: number;
  /** Squares to shade, as [row, col] from 0. */
  shaded?: number[][];
  /** Draw a dot at every interior crossing of the grid lines. */
  dots?: boolean;
}

/**
 * A bar chart, or a pictograph when `each` is given (one symbol stands for `each`).
 * highlight keys: 'b0' 'b1' ...
 */
export interface BarChartFigure extends FigureBase {
  kind: 'barChart';
  /** Two to eight bars. */
  bars: Array<{ label: string; value: number }>;
  unit?: string;
  each?: number;
}

/**
 * A small table (at most 6 rows by 5 columns).
 * highlight keys: 'r0' 'r1' ... (rows)
 */
export interface TableFigure extends FigureBase {
  kind: 'table';
  headers?: string[];
  rows: string[][];
}

/**
 * Two overlapping circles with text in each of the three regions.
 * highlight keys: 'left' 'both' 'right'
 */
export interface VennFigure extends FigureBase {
  kind: 'venn';
  leftTitle: string;
  rightTitle: string;
  left: string;
  both: string;
  right: string;
}

/**
 * A balance scale holding one expression on each pan, e.g. "4x + 17" and "25".
 * highlight keys: 'left' 'right'
 */
export interface BalanceFigure extends FigureBase {
  kind: 'balance';
  left: string;
  right: string;
}

/**
 * A factor tree. The renderer works out the tree from `number`.
 * highlight keys: 'primes'
 */
export interface FactorTreeFigure extends FigureBase {
  kind: 'factorTree';
  /** 2 to 1000. */
  number: number;
  /** How many splits to reveal. Leave out to show the whole tree. */
  depth?: number;
}

export type FigureSpec =
  | TriangleFigure | RectangleFigure | PolygonFigure | CircleFigure | AnglesFigure
  | ClockFigure | CompassFigure | FractionBarsFigure | SetFigure | BarModelFigure
  | NumberLineFigure | JourneyFigure | PlaceChartFigure | GridFigure | BarChartFigure
  | TableFigure | VennFigure | BalanceFigure | FactorTreeFigure;

export type FigureKind = FigureSpec['kind'];

/** One step of a computed solution, for questions whose database row has no steps. */
export interface VisualStep {
  text: string;
  figure?: FigureSpec;
}

/** Everything visual attached to one question. Stored offline, keyed by question id. */
export interface QuestionVisual {
  /** Shown before the child answers: givens only. */
  figure?: FigureSpec;
  /**
   * One entry per step of the question's own `stepByStep` (same length, same
   * order). null where a step needs no picture.
   */
  stepFigures?: Array<FigureSpec | null>;
  /**
   * A full solution, used ONLY when the question has no `stepByStep` of its own.
   * These are computed by rule in Python, never written freehand.
   */
  steps?: VisualStep[];
  /** True when the figure legitimately needs numbers from the answer choices ("which of these..."). */
  usesOptions?: boolean;
  /**
   * True when the question cannot be answered without this figure and its text
   * does not hold the figure's data ("what fraction of the figure is unshaded?").
   * The figure is then rebuilt from the answer key, is exempt from the
   * givens-only number check, and is listed separately for human review.
   * Only for origin 'authored'.
   */
  essential?: boolean;
  /** 'rule': produced by a template rule. 'authored': written for this one question. */
  origin: 'rule' | 'authored';
}

/** What a screen receives for one question. */
export interface ServedVisual {
  figure?: FigureSpec;
  /** Present only where the solution may be shown (never during a mock test). */
  stepFigures?: Array<FigureSpec | null>;
  steps?: VisualStep[];
}
