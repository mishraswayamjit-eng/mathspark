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
  /** The group it is listed under on the whiteboard. */
  family: string;
  name: string;
  emoji: string;
  /** What the child can do with it. */
  blurb: string;
  /** A request that opens it, used by the library list on the whiteboard. */
  try: string;
}

export const VISUAL_LIBRARY: Record<VisualKind, VisualInfo> = {
  fraction:    { kind: 'fraction', family: 'Fractions and decimals',    name: 'Fraction bars',   emoji: '🍕', blurb: 'Shade parts of a whole and compare two fractions', try: 'Show me 3/8 on a fraction bar' },
  numberLine:  { kind: 'numberLine', family: 'Numbers',  name: 'Number line',     emoji: '📏', blurb: 'Place numbers and hop along the line', try: 'Show me 8 − 13 as hops on a number line' },
  placeValue:  { kind: 'placeValue', family: 'Numbers',  name: 'Place-value blocks', emoji: '🧱', blurb: 'Build a number from thousands, hundreds, tens and ones', try: 'Build the number 2,346 with blocks' },
  array:       { kind: 'array', family: 'Numbers',       name: 'Dot array',       emoji: '🔵', blurb: 'See multiplication as rows and columns', try: 'Show me 6 × 7 as an array' },
  barModel:    { kind: 'barModel', family: 'Word problems and algebra',    name: 'Bar model',       emoji: '📊', blurb: 'Lay out a word problem as bars and parts', try: 'Show me how to split 40 sweets in the ratio 3 : 5 with a bar model' },
  balance:     { kind: 'balance', family: 'Word problems and algebra',     name: 'Balance scale',   emoji: '⚖️', blurb: 'Keep both sides equal to solve an equation', try: 'Show me how to solve 2x + 3 = 11 on a balance' },
  rectangle:   { kind: 'rectangle', family: 'Shapes and space',   name: 'Area and perimeter', emoji: '▭', blurb: 'Stretch a rectangle and watch area and perimeter change', try: 'Show me a 6 by 4 rectangle and its area and perimeter' },
  angle:       { kind: 'angle', family: 'Shapes and space',       name: 'Angle maker',     emoji: '📎', blurb: 'Turn an arm to make acute, right, obtuse and reflex angles', try: 'Show me a 120° angle and tell me what kind it is' },
  percentGrid: { kind: 'percentGrid', family: 'Fractions and decimals', name: 'Hundred grid',    emoji: '💯', blurb: 'See a percentage as squares out of 100', try: 'Show me what 35% looks like on a hundred grid' },
  container:   { kind: 'container', family: 'Time, money and measures',   name: 'Measuring jar',   emoji: '🫙', blurb: 'Fill a jar to see how full it is', try: 'Show me a 500 ml jar with 350 ml in it' },
  polygon:     { kind: 'polygon', family: 'Shapes and space',     name: 'Polygon angles',  emoji: '⬡', blurb: 'Change the number of sides and watch the angles', try: 'Show me the angles inside a regular hexagon' },
  tiling:      { kind: 'tiling', family: 'Shapes and space',      name: 'Shapes around a point', emoji: '🐝', blurb: 'Fit shapes around a point until they close up', try: 'How many hexagons fit around a point?' },
  triangle:    { kind: 'triangle', family: 'Shapes and space',    name: 'Triangle',        emoji: '🔺', blurb: 'Drag a corner and watch the three angles', try: 'Show me a triangle and why its angles add up to 180°' },
  rightTriangle: { kind: 'rightTriangle', family: 'Shapes and space', name: 'Right-angled triangle', emoji: '📐', blurb: 'Change the base and height; see the area and the longest side', try: 'Show me a right-angled triangle with base 4 cm and height 3 cm' },
  circle:      { kind: 'circle', family: 'Shapes and space',      name: 'Circle',          emoji: '⭕', blurb: 'Grow the radius and see circumference and area', try: 'Show me a circle with radius 7 cm and its circumference' },
  clock: { kind: 'clock', family: 'Time, money and measures', name: 'Clock', emoji: '🕒', blurb: 'Set the hands and read the time', try: 'Show me 3:40 on a clock' },
  calendar: { kind: 'calendar', family: 'Time, money and measures', name: 'Calendar', emoji: '📅', blurb: 'Find the day of any date and count the days in a month', try: 'Show me the calendar for August 2026' },
  money: { kind: 'money', family: 'Time, money and measures', name: 'Notes and coins', emoji: '💰', blurb: 'Make an amount with rupee notes and coins', try: 'Show me how to make ₹376 with notes and coins' },
  journey: { kind: 'journey', family: 'Time, money and measures', name: 'Speed and distance', emoji: '🚗', blurb: 'Watch a journey and see distance = speed × time', try: 'Show me a car travelling at 60 km/h for 4 hours' },
  unitLadder: { kind: 'unitLadder', family: 'Time, money and measures', name: 'Unit converter', emoji: '📏', blurb: 'Change between km, m, cm and mm, or kg and g, or l and ml', try: 'Show me how to change 2.5 km into metres' },
  profitLoss: { kind: 'profitLoss', family: 'Time, money and measures', name: 'Profit and loss', emoji: '🏷️', blurb: 'Compare cost price and selling price', try: 'Show me the profit when cost price is ₹400 and selling price is ₹500' },
  simpleInterest: { kind: 'simpleInterest', family: 'Time, money and measures', name: 'Simple interest', emoji: '🏦', blurb: 'Watch interest add up year by year', try: 'Show me the simple interest on ₹2,000 at 5% for 3 years' },
  mixedNumber: { kind: 'mixedNumber', family: 'Fractions and decimals', name: 'Mixed numbers', emoji: '🍰', blurb: 'Build wholes and parts; see the improper fraction', try: 'Show me 2 3/4 as a picture' },
  fractionSet: { kind: 'fractionSet', family: 'Fractions and decimals', name: 'Fraction of a set', emoji: '🫘', blurb: 'Share a set into equal groups and take some of them', try: 'Show me 3/4 of 20' },
  factorTree: { kind: 'factorTree', family: 'Numbers', name: 'Factor tree', emoji: '🌳', blurb: 'Split a number down to its prime factors', try: 'Show me the factor tree of 60' },
  venn: { kind: 'venn', family: 'Numbers', name: 'HCF and LCM circles', emoji: '⭕', blurb: 'Sort the factors of two numbers to find the HCF and LCM', try: 'Show me the HCF and LCM of 12 and 18' },
  hundredChart: { kind: 'hundredChart', family: 'Numbers', name: 'Hundred chart', emoji: '🔢', blurb: 'See multiples, primes and square numbers from 1 to 100', try: 'Show me the multiples of 7 on a hundred chart' },
  placeChart: { kind: 'placeChart', family: 'Numbers', name: 'Place-value chart', emoji: '🏛️', blurb: 'Read each digit in lakhs, thousands, ones and decimals', try: 'Show me 23,45,678 on a place-value chart' },
  figurate: { kind: 'figurate', family: 'Numbers', name: 'Square and triangular numbers', emoji: '🔺', blurb: 'Grow dot patterns and see the number sequence', try: 'Show me why 25 is a square number' },
  areaModel: { kind: 'areaModel', family: 'Numbers', name: 'Multiplication boxes', emoji: '🧮', blurb: 'Split a big multiplication into easy parts', try: 'Show me 23 × 14 with boxes' },
  counters: { kind: 'counters', family: 'Numbers', name: 'Ten frames', emoji: '🟣', blurb: 'Add and take away with counters; make ten', try: 'Show me 8 + 5 on ten frames' },
  magicSquare: { kind: 'magicSquare', family: 'Word problems and algebra', name: 'Magic square', emoji: '✨', blurb: 'Fill the boxes so every line adds to the same number', try: 'Give me a magic square to solve' },
  pictograph: { kind: 'pictograph', family: 'Data', name: 'Pictograph', emoji: '🖼️', blurb: 'Read data shown with symbols', try: 'Show me a pictograph of books read: Asha 30, Ravi 45, Meena 20' },
  symmetry: { kind: 'symmetry', family: 'Shapes and space', name: 'Lines of symmetry', emoji: '🦋', blurb: 'Find the mirror lines of a shape', try: 'Show me the lines of symmetry of a rectangle' },
  cuboid: { kind: 'cuboid', family: 'Shapes and space', name: 'Cuboid', emoji: '🧊', blurb: 'Build a box from cubes; find volume and surface area', try: 'Show me the volume of a 4 by 3 by 2 cuboid' },
  coordinateGrid: { kind: 'coordinateGrid', family: 'Shapes and space', name: 'Coordinate grid', emoji: '🎯', blurb: 'Plot points and read their coordinates', try: 'Show me the point (3, 4) on a grid' },
  quadrilateral: { kind: 'quadrilateral', family: 'Shapes and space', name: 'Quadrilaterals', emoji: '🔷', blurb: 'Compare squares, rhombuses, kites and more', try: 'Show me a parallelogram and its properties' },
  parallelLines: { kind: 'parallelLines', family: 'Shapes and space', name: 'Parallel lines', emoji: '🛤️', blurb: 'Tilt a crossing line and watch the equal angles', try: 'Show me the angles when a line crosses two parallel lines' },
  barChart:    { kind: 'barChart', family: 'Data',    name: 'Bar chart',       emoji: '📶', blurb: 'Tap the bars and find the average', try: 'Show me a bar chart of 4, 7 and 10 and their average' },
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
  { keywords: ['decimal units', 'units', 'capacity'], topic: 'Measurement and units',   visuals: ['unitLadder', 'container', 'numberLine'], starter: 'Show me how to change 2.5 km into metres' },
  { keywords: ['decimal'],                               topic: 'Decimals',                          visuals: ['placeChart', 'numberLine', 'percentGrid'], starter: 'Show me where 0.7 sits on a number line' },
  { keywords: ['fraction'],                              topic: 'Fractions',                         visuals: ['fraction', 'mixedNumber', 'fractionSet', 'numberLine', 'barModel'], starter: 'Show me 3/4 and 2/3 and help me see which is bigger' },
  { keywords: ['profit', 'loss', 'discount'],            topic: 'Profit, loss and discount',         visuals: ['profitLoss', 'percentGrid', 'barModel'], starter: 'Show me the profit when cost price is ₹400 and selling price is ₹500' },
  { keywords: ['interest'],                              topic: 'Simple interest',                   visuals: ['simpleInterest', 'percentGrid'],         starter: 'Show me the simple interest on ₹2,000 at 5% for 3 years' },
  { keywords: ['percent', 'money'],                      topic: 'Percentage and money',              visuals: ['percentGrid', 'money', 'barModel'],      starter: 'Show me what 35% looks like' },
  { keywords: ['ratio', 'proportion', 'unitary'],        topic: 'Ratio, proportion and unitary method', visuals: ['barModel', 'fractionSet'],            starter: 'Show me how to split 40 sweets in the ratio 3 : 5' },
  { keywords: ['coordinate'],                            topic: 'Coordinate geometry',               visuals: ['coordinateGrid'],                        starter: 'Show me the point (3, 4) on a grid' },
  { keywords: ['polynomial', 'factoring'],               topic: 'Polynomials',                       visuals: ['areaModel', 'balance'],                  starter: 'Show me 23 × 14 with boxes' },
  { keywords: ['equation', 'algebra', 'expression', 'linear'], topic: 'Algebra and equations',      visuals: ['balance', 'barModel', 'areaModel'],      starter: 'Show me how to solve 2x + 3 = 11 on a balance' },
  { keywords: ['puzzle', 'magic'],                       topic: 'Puzzles and magic squares',         visuals: ['magicSquare', 'hundredChart'],           starter: 'Give me a magic square to solve' },
  { keywords: ['hcf', 'lcm'],                            topic: 'HCF and LCM',                       visuals: ['venn', 'factorTree', 'hundredChart'],    starter: 'Show me the HCF and LCM of 12 and 18' },
  { keywords: ['factor', 'multiple', 'prime', 'divisib'], topic: 'Factors, multiples and primes',    visuals: ['factorTree', 'hundredChart', 'venn', 'array'], starter: 'Show me the factor tree of 60' },
  { keywords: ['square number', 'root', 'square'],       topic: 'Square numbers and roots',          visuals: ['figurate', 'array', 'hundredChart'],     starter: 'Show me why 25 is a square number' },
  { keywords: ['place value', 'number system', 'numeration', 'counting'], topic: 'Numbers and place value', visuals: ['placeChart', 'placeValue', 'numberLine', 'hundredChart'], starter: 'Show me 23,45,678 on a place-value chart' },
  { keywords: ['multiplication', 'division', 'table'],   topic: 'Multiplication and division',       visuals: ['array', 'areaModel', 'numberLine'],      starter: 'Show me 6 × 7 as an array' },
  { keywords: ['integer'],                               topic: 'Integers',                          visuals: ['numberLine'],                            starter: 'Show me 8 − 13 as hops on a number line' },
  { keywords: ['addition', 'subtraction', 'operation', 'bodmas'], topic: 'Addition, subtraction and order of operations', visuals: ['numberLine', 'counters', 'barModel', 'placeValue'], starter: 'Show me 8 + 5 on ten frames' },
  { keywords: ['volume', 'surface'],                     topic: 'Volume and surface area',           visuals: ['cuboid', 'rectangle'],                   starter: 'Show me the volume of a 4 by 3 by 2 cuboid' },
  { keywords: ['area', 'perimeter', 'mensuration'],      topic: 'Perimeter, area and mensuration',   visuals: ['rectangle', 'rightTriangle', 'circle', 'cuboid'], starter: 'Show me a 6 by 4 rectangle and its area and perimeter' },
  { keywords: ['triangle'],                              topic: 'Triangles',                         visuals: ['triangle', 'rightTriangle', 'symmetry', 'angle'], starter: 'Show me a triangle and why its angles add up to 180°' },
  { keywords: ['circle'],                                topic: 'Circles',                           visuals: ['circle'],                                starter: 'Show me a circle with radius 7 cm and its circumference' },
  { keywords: ['quadrilateral', 'polygon'],              topic: 'Quadrilaterals and polygons',       visuals: ['quadrilateral', 'polygon', 'symmetry', 'tiling'], starter: 'Show me a parallelogram and its properties' },
  { keywords: ['angle', 'line'],                         topic: 'Angles and lines',                  visuals: ['angle', 'parallelLines', 'polygon', 'triangle'], starter: 'Show me the angles when a line crosses two parallel lines' },
  { keywords: ['shape', 'geometry', 'symmetry'],         topic: 'Shapes and geometry',               visuals: ['symmetry', 'quadrilateral', 'rectangle', 'cuboid', 'angle'], starter: 'Show me the lines of symmetry of a rectangle' },
  { keywords: ['speed', 'distance'],                     topic: 'Time, distance and speed',          visuals: ['journey', 'barModel'],                   starter: 'Show me a car travelling at 60 km/h for 4 hours' },
  { keywords: ['time', 'calendar', 'clock'],             topic: 'Time and calendar',                 visuals: ['clock', 'calendar', 'numberLine'],       starter: 'Show me 3:40 on a clock' },
  { keywords: ['sequence', 'series', 'pattern'],         topic: 'Sequences and patterns',            visuals: ['figurate', 'numberLine', 'hundredChart'], starter: 'Show me the pattern 3, 7, 11, 15 on a number line' },
  { keywords: ['data', 'graph', 'statistic', 'average', 'probability'], topic: 'Data handling and averages', visuals: ['barChart', 'pictograph', 'barModel'], starter: 'Show me a bar chart of 4, 7 and 10 and their average' },
  { keywords: ['number'],                                topic: 'Numbers',                           visuals: ['placeChart', 'numberLine', 'hundredChart', 'counters'], starter: 'Show me the multiples of 7 on a hundred chart' },
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

export const VISUAL_FAMILIES = ['Numbers', 'Fractions and decimals', 'Time, money and measures', 'Shapes and space', 'Word problems and algebra', 'Data'];

/** Every visual in the library, grouped by family, for the whiteboard's "All pictures" list. */
export function visualsByFamily(): Array<{ family: string; visuals: VisualInfo[] }> {
  const kinds = Object.keys(VISUAL_LIBRARY) as VisualKind[];
  const out: Array<{ family: string; visuals: VisualInfo[] }> = [];
  for (let f = 0; f < VISUAL_FAMILIES.length; f++) {
    const visuals: VisualInfo[] = [];
    for (let i = 0; i < kinds.length; i++) {
      if (VISUAL_LIBRARY[kinds[i]].family === VISUAL_FAMILIES[f]) visuals.push(VISUAL_LIBRARY[kinds[i]]);
    }
    if (visuals.length > 0) out.push({ family: VISUAL_FAMILIES[f], visuals });
  }
  return out;
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

rightTriangle: a right-angled triangle from its two shorter sides, for area of a triangle (half of a rectangle), base and height, and the longest side. {"type":"rightTriangle","base":1-20,"height":1-20,"unit":"cm"}. The child can change both sides and switch between area and the longest side. Use whole-number triples (3-4-5, 6-8-10, 5-12-13) when the longest side matters.

circle: a circle with its radius and diameter drawn. {"type":"circle","radius":1-20,"unit":"cm"}. Shows circumference and area using π ≈ 3.14 (say so if the child's book uses 22/7).

clock: an analogue clock. {"type":"clock","hour":1-12,"minute":0-59}. The child sets the hands; it reads the time in words and gives the angle between the hands.

calendar: one month. {"type":"calendar","year":2026,"month":1-12,"day":optional date to mark}. The child taps a date to see its weekday; shows days in the month and leap years.

money: Indian notes and coins. {"type":"money","amount":1-5000}. The child builds the amount in rupees from ₹500, 200, 100, 50, 20, 10, 5, 2, 1 and tries to use the fewest.

journey: speed, distance and time on a road. {"type":"journey","speed":60,"hours":4,"unit":"km"}. Add "speedB" (and "labelA", "labelB") for a second traveller starting from the same place at the same time, to compare or find the gap. The child slides time and speed.

unitLadder: converting metric units. {"type":"unitLadder","quantity":"length" (km, m, cm, mm) or "mass" (kg, g, mg) or "capacity" (kl, l, ml),"value":2.5,"from":"km","to":"m"}.

profitLoss: cost price and selling price as two bars, with profit or loss and its percentage. {"type":"profitLoss","cost":400,"selling":500}.

simpleInterest: bars growing by the same interest each year. {"type":"simpleInterest","principal":2000,"rate":1-20,"years":1-10}.

mixedNumber: wholes and a part, with the matching improper fraction. {"type":"mixedNumber","whole":0-5,"numerator":n,"denominator":2-12}.

fractionSet: a fraction of a quantity, as a set shared into equal groups. {"type":"fractionSet","total":20,"denominator":4,"numerator":3,"item":"marbles"}. The denominator must divide the total, with at most 12 in a group.

factorTree: prime factorisation as a tree. {"type":"factorTree","number":2-200}.

venn: two overlapping circles sorting the factors of two numbers, for HCF and LCM. {"type":"venn","a":12,"b":18,"mode":"factors" or "primes"}; numbers up to 100. "primes" shows prime factors, which gives both HCF and LCM.

hundredChart: the numbers 1 to 100 with a pattern marked. {"type":"hundredChart","mark":"multiples","of":2-12} or "mark":"primes" or "squares". For multiples, skip counting, common multiples by eye, primes.

placeChart: the Indian place-value chart (crores, lakhs, thousands, ones, and decimal places). {"type":"placeChart","number":2345678.25}; up to 99,99,99,999 and three decimal places. The child taps a digit to see its place and value. Use this for big numbers and decimals; use placeValue blocks for numbers up to 9999.

figurate: dot patterns for square and triangular numbers. {"type":"figurate","kind":"square" or "triangular","n":1-10}. Good for square roots and for sequences.

areaModel: multiplication as a rectangle split into tens and ones. {"type":"areaModel","a":23,"b":14}; both up to 99. Also shows why (a + b)(c + d) has four parts.

counters: ten frames for adding and taking away within 20. {"type":"counters","op":"add","a":8,"b":5} (each up to 10) or "op":"subtract" (a up to 20). For Grades 2 and 3.

magicSquare: a 3 by 3 puzzle. {"type":"magicSquare","cells":[2,0,6,9,5,0,4,3,0]}; nine numbers row by row, 0 for a box the child must fill. Give a square that has exactly one solution.

pictograph: data shown with symbols. {"type":"pictograph","each":10,"unit":"books","rows":[{"label":"Asha","value":30},{"label":"Ravi","value":45}]}. 2 to 6 rows, at most 12 symbols in a row; part symbols are drawn for remainders.

symmetry: a shape with its mirror lines. {"type":"symmetry","shape":"equilateral" | "isosceles" | "scalene" | "square" | "rectangle" | "rhombus" | "parallelogram" | "kite" | "pentagon" | "hexagon" | "octagon"}.

cuboid: a box built from unit cubes, for volume and surface area. {"type":"cuboid","length":1-8,"width":1-8,"height":1-8,"unit":"cm"}.

coordinateGrid: points on x and y axes. {"type":"coordinateGrid","points":[{"x":3,"y":4,"label":"A"}],"join":true to draw the shape they make}. Up to 8 points; 0 to 10 when all are positive, otherwise -8 to 8. The child taps to place a point of their own.

quadrilateral: one named quadrilateral with its angles, properties and diagonals. {"type":"quadrilateral","kind":"square" | "rectangle" | "parallelogram" | "rhombus" | "trapezium" | "kite"}.

parallelLines: two parallel lines cut by a third line, with all eight angles marked. {"type":"parallelLines","angle":30-150}. For corresponding, alternate and vertically opposite angles.

barChart: a bar chart for data handling and averages. {"type":"barChart","unit":"runs","showMean":true,"bars":[{"label":"Mon","value":4},{"label":"Tue","value":7}]}. 2 to 8 bars. With "showMean" a line marks the average.

Sketching together

The whiteboard also has a pencil. The child can draw over your picture, or on a blank board, with a finger, a stylus or the mouse, and send you the sketch. It arrives as a photo of the whole whiteboard: your picture as it stands now (including anything the child has dragged or changed), with their pencil marks on top. Read the marks against the picture: where a hop starts and lands on the number line, which parts are ringed or shaded, what has been written beside it. Treat it like any photo of working: say what you see, build on it, and correct it kindly. If the marks are unclear, say what you can make out and ask one short question; do not ask the child to draw it again. Invite sketching when it helps the child think ("sketch where you think 3/4 goes on the line and show me", "draw the triangle you are imagining"). You cannot draw freehand yourself; answer a sketch with words and, when useful, a picture from the library.

Which picture for which topic (best first)
${topicLines}

If nothing in the library fits the idea, do not force one: explain in words and lay the working out clearly.`;
}
