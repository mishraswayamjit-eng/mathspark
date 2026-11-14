/**
 * Which whiteboard visuals suit which maths topics.
 *
 * One table drives three things, so they can never drift apart:
 *  - the guidance in Sparky's prompt ("for fractions, use the fraction bar…"),
 *  - the starter cards on the empty whiteboard,
 *  - the label shown for a visual.
 */

import type { VisualKind } from './spec';

export interface VisualInfo {
  kind: VisualKind;
  name: string;
  emoji: string;
  /** What the child can do with it. */
  blurb: string;
}

export const VISUAL_LIBRARY: Record<VisualKind, VisualInfo> = {
  fraction:    { kind: 'fraction',    name: 'Fraction bars',   emoji: '🍕', blurb: 'Shade parts of a whole and compare two fractions' },
  numberLine:  { kind: 'numberLine',  name: 'Number line',     emoji: '📏', blurb: 'Place numbers and hop along the line' },
  placeValue:  { kind: 'placeValue',  name: 'Place-value blocks', emoji: '🧱', blurb: 'Build a number from thousands, hundreds, tens and ones' },
  array:       { kind: 'array',       name: 'Dot array',       emoji: '🔵', blurb: 'See multiplication as rows and columns' },
  barModel:    { kind: 'barModel',    name: 'Bar model',       emoji: '📊', blurb: 'Lay out a word problem as bars and parts' },
  balance:     { kind: 'balance',     name: 'Balance scale',   emoji: '⚖️', blurb: 'Keep both sides equal to solve an equation' },
  rectangle:   { kind: 'rectangle',   name: 'Area and perimeter', emoji: '📐', blurb: 'Stretch a rectangle and watch area and perimeter change' },
  angle:       { kind: 'angle',       name: 'Angle maker',     emoji: '📎', blurb: 'Turn an arm to make acute, right, obtuse and reflex angles' },
  percentGrid: { kind: 'percentGrid', name: 'Hundred grid',    emoji: '💯', blurb: 'See a percentage as squares out of 100' },
  container:   { kind: 'container',   name: 'Measuring jar',   emoji: '🫙', blurb: 'Fill a jar to see how full it is' },
  polygon:     { kind: 'polygon',     name: 'Polygon angles',  emoji: '⬡', blurb: 'Change the number of sides and watch the angles' },
  tiling:      { kind: 'tiling',      name: 'Shapes around a point', emoji: '🐝', blurb: 'Fit shapes around a point until they close up' },
  triangle:    { kind: 'triangle',    name: 'Triangle',        emoji: '🔺', blurb: 'Drag a corner and watch the three angles' },
  circle:      { kind: 'circle',      name: 'Circle',          emoji: '⭕', blurb: 'Grow the radius and see circumference and area' },
  barChart:    { kind: 'barChart',    name: 'Bar chart',       emoji: '📶', blurb: 'Tap the bars and find the average' },
};

export interface TopicVisualRule {
  /** Words that identify the topic in a topic name. */
  keywords: string[];
  /** Topic family, as shown to the model. */
  topic: string;
  /** Best visual first. */
  visuals: VisualKind[];
  /** A request a child could tap to see it in action. */
  starter: string;
}

/** Ordered: the first rule whose keyword appears in the topic name wins. */
export const TOPIC_VISUAL_RULES: TopicVisualRule[] = [
  { keywords: ['fraction'],                              topic: 'Fractions',                         visuals: ['fraction', 'numberLine', 'barModel'],   starter: 'Show me 3/4 and 2/3 and help me see which is bigger' },
  { keywords: ['decimal'],                               topic: 'Decimals',                          visuals: ['numberLine', 'percentGrid', 'placeValue'], starter: 'Show me where 0.7 sits on a number line' },
  { keywords: ['percent', 'profit', 'loss', 'discount', 'interest'], topic: 'Percentage, profit and loss, simple interest', visuals: ['percentGrid', 'barModel'], starter: 'Show me what 35% looks like' },
  { keywords: ['ratio', 'proportion', 'unitary'],        topic: 'Ratio, proportion and unitary method', visuals: ['barModel'],                         starter: 'Show me how to split 40 sweets in the ratio 3 : 5' },
  { keywords: ['equation', 'algebra', 'expression', 'linear'], topic: 'Algebra and equations',      visuals: ['balance', 'barModel'],                   starter: 'Show me how to solve 2x + 3 = 11 on a balance' },
  { keywords: ['place value', 'number system', 'numbers', 'numeration'], topic: 'Numbers and place value', visuals: ['placeValue', 'numberLine'],       starter: 'Build the number 2,346 with blocks' },
  { keywords: ['multiplication', 'division', 'table', 'factor', 'multiple', 'hcf', 'lcm', 'prime', 'divisib', 'square'], topic: 'Multiplication, division, factors and squares', visuals: ['array', 'numberLine'], starter: 'Show me 6 × 7 as an array' },
  { keywords: ['addition', 'subtraction', 'operation', 'bodmas', 'integer'], topic: 'Addition, subtraction, integers', visuals: ['numberLine', 'barModel', 'placeValue'], starter: 'Show me 8 − 13 as hops on a number line' },
  { keywords: ['area', 'perimeter', 'mensuration', 'rectangle'], topic: 'Perimeter, area and mensuration', visuals: ['rectangle', 'circle'],          starter: 'Show me a 6 by 4 rectangle and its area and perimeter' },
  { keywords: ['triangle'],                              topic: 'Triangles',                         visuals: ['triangle', 'angle'],                     starter: 'Show me a triangle and why its angles add up to 180°' },
  { keywords: ['circle'],                                topic: 'Circles',                           visuals: ['circle'],                                starter: 'Show me a circle with radius 7 cm and its circumference' },
  { keywords: ['polygon', 'quadrilateral'],              topic: 'Polygons and quadrilaterals',       visuals: ['polygon', 'tiling', 'rectangle'],        starter: 'Show me the angles inside a regular hexagon' },
  { keywords: ['angle', 'line', 'geometry'],             topic: 'Angles and lines',                  visuals: ['angle', 'polygon', 'triangle'],          starter: 'Show me a 120° angle and tell me what kind it is' },
  { keywords: ['measurement', 'unit', 'capacity', 'volume', 'time', 'speed', 'distance'], topic: 'Measurement, capacity, speed and time', visuals: ['container', 'numberLine', 'barModel'], starter: 'Show me a 500 ml jar with 350 ml in it' },
  { keywords: ['sequence', 'series', 'pattern'],         topic: 'Sequences and patterns',            visuals: ['numberLine', 'array'],                   starter: 'Show me the pattern 3, 7, 11, 15 on a number line' },
  { keywords: ['data', 'graph', 'statistic', 'average', 'probability'], topic: 'Data handling and averages', visuals: ['barChart', 'barModel', 'percentGrid'], starter: 'Show me a bar chart of 4, 7 and 10 and their average' },
];

/** The visuals that suit a topic name, best first. Empty when nothing fits. */
export function visualsForTopic(topicName: string): VisualKind[] {
  const lower = topicName.toLowerCase();
  for (let i = 0; i < TOPIC_VISUAL_RULES.length; i++) {
    const rule = TOPIC_VISUAL_RULES[i];
    for (let k = 0; k < rule.keywords.length; k++) {
      if (lower.indexOf(rule.keywords[k]) !== -1) return rule.visuals;
    }
  }
  return [];
}

export interface WhiteboardStarter {
  topicName: string;
  kind: VisualKind;
  prompt: string;
}

/** Starter cards for the empty whiteboard: one per visual, from the child's own topics. */
export function startersForTopics(topicNames: string[], limit: number): WhiteboardStarter[] {
  const out: WhiteboardStarter[] = [];
  const used: Partial<Record<VisualKind, boolean>> = {};
  for (let t = 0; t < topicNames.length && out.length < limit; t++) {
    const lower = topicNames[t].toLowerCase();
    for (let i = 0; i < TOPIC_VISUAL_RULES.length; i++) {
      const rule = TOPIC_VISUAL_RULES[i];
      let hit = false;
      for (let k = 0; k < rule.keywords.length; k++) {
        if (lower.indexOf(rule.keywords[k]) !== -1) { hit = true; break; }
      }
      if (!hit) continue;
      const kind = rule.visuals[0];
      if (!used[kind]) {
        used[kind] = true;
        out.push({ topicName: topicNames[t], kind, prompt: rule.starter });
      }
      break;
    }
  }
  return out;
}

/** The whiteboard section of Sparky's prompt, generated from the tables above. */
export function buildWhiteboardGuide(): string {
  const topicLines = TOPIC_VISUAL_RULES
    .map((r) => `- ${r.topic}: ${r.visuals.join(', ')}`)
    .join('\n');

  return `The whiteboard

Beside the chat there is a whiteboard. You can put ONE interactive picture on it with each reply, chosen from a fixed library. The child can drag, tap and change it. Pictures teach faster than words at this age, so use one whenever an idea can be seen: when you introduce a concept, set out a word problem, compare two things, or show where the child's working went off. Skip it for quick facts, for chit-chat, and when the last picture is still the right one.

How to show a picture: start your reply with a single line holding the tag, then write your reply as usual underneath.

<visual>{"type":"fraction","shape":"bar","parts":8,"shaded":3}</visual>

Rules for the tag: one tag at most, at the very start, valid JSON on one line, only the fields listed below, numbers as numbers. The child never sees the tag, so do not mention it or its JSON. Do refer to the picture in your words ("look at the bar on the whiteboard: 3 of the 8 parts are shaded") and give the child something to do with it. The numbers in the picture must be exactly the numbers in your explanation. Add "title" (a few words) to any picture when it helps.

The library

fraction: a whole cut into equal parts, some shaded. {"type":"fraction","shape":"bar" or "circle","parts":1-12,"shaded":0-12}. To compare two fractions add "compare":{"parts":n,"shaded":n}. The child can tap parts to shade them.

numberLine: {"type":"numberLine","min":n,"max":n,"step":n} with at most 40 steps. Optional "point":n marks a value; "jumpFrom":n and "jumpTo":n draw a hop (for adding, subtracting, negative numbers, sequences). Decimals are fine (step 0.1). The child can drag the point.

placeValue: base-ten blocks for a whole number up to 9999. {"type":"placeValue","number":n}. The child can add and remove thousands, hundreds, tens and ones.

array: rows and columns of dots for multiplication, division, factors, square numbers. {"type":"array","rows":1-12,"cols":1-12}. The child can change both.

barModel: bars cut into labelled pieces, for word problems, ratio, unitary method, percentages of an amount, averages. {"type":"barModel","unit":"₹","bars":[{"label":"Asha","segments":[{"value":25,"label":"1 notebook"},{"value":25},{"value":0,"unknown":true,"label":"?"}]}]}. Up to 3 bars and 12 pieces per bar. Piece widths follow their values; mark the piece being found with "unknown":true.

balance: a scale for one-variable equations with whole numbers. {"type":"balance","leftX":2,"leftUnits":3,"rightX":0,"rightUnits":11,"variable":"x"} shows 2x + 3 = 11. Up to 6 x-boxes and 30 unit weights a side. The child removes the same from both sides and shares equally to find x. Choose equations whose answer is a whole number.

rectangle: a rectangle on a square grid, for perimeter and area. {"type":"rectangle","width":1-20,"height":1-20,"unit":"cm"}. The child can stretch it.

angle: one angle the child can turn. {"type":"angle","degrees":0-360}.

percentGrid: a 10 by 10 grid with squares shaded. {"type":"percentGrid","percent":0-100}. Shows the percentage as a fraction and a decimal too.

container: a measuring jar. {"type":"container","capacity":500,"filled":350,"unit":"ml"}.

polygon: a regular polygon with every interior angle marked, the angle sum and the size of each angle. {"type":"polygon","sides":3-12}. The child can change the number of sides.

tiling: copies of one regular polygon fitted around a single point, to see which shapes close up with no gap (triangles, squares and hexagons do; pentagons leave a gap). {"type":"tiling","sides":3-6,"count":how many are placed to start}. The child adds and removes copies and watches the angles add towards 360°.

triangle: a triangle from two of its angles, with all three angles marked. {"type":"triangle","angleA":60,"angleB":70}; the two must add to 170 or less. The child drags the corners; the angles always add to 180°, and the triangle is named by its angles and sides.

circle: a circle with its radius and diameter drawn. {"type":"circle","radius":1-20,"unit":"cm"}. Shows circumference and area using π ≈ 3.14 (say so if the child's book uses 22/7).

barChart: a bar chart for data handling and averages. {"type":"barChart","unit":"runs","showMean":true,"bars":[{"label":"Mon","value":4},{"label":"Tue","value":7}]}. 2 to 8 bars. With "showMean" a line marks the average.

Sketching together

The whiteboard also has a pencil. The child can draw over your picture, or on a blank board, with a finger, a stylus or the mouse, and send you the sketch; it arrives as a photo. Treat it like any photo of working: say what you see, build on it, and correct it kindly. Invite sketching when it helps the child think ("sketch where you think 3/4 goes on the line and show me", "draw the triangle you are imagining"). You cannot draw freehand yourself; answer a sketch with words and, when useful, a picture from the library.

Which picture for which topic (best first)
${topicLines}

If nothing in the library fits the idea, do not force one: explain in words and lay the working out clearly.`;
}
