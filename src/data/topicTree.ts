// Single source of truth for grade → topics mapping.
// Grade 4: each TopicNode maps directly to a DB topicId (ch01-05, ch06, etc.)
// Grades 2-3, 5-9: each TopicNode maps to dbTopicId: 'gradeN' + optional subTopicKey
//   (brain engine does case-insensitive contains match on question.subTopic)

export interface TopicNode {
  id: string;          // unique brain engine ID, e.g. 'gr4_numbers'
  name: string;
  emoji: string;
  grade: number;       // 2–9
  examWeight: number;  // 0.0–1.0 relative IPM importance within grade
  dbTopicId: string;   // actual topicId in Question table
  subTopicKey?: string; // if set, filter by subTopic ILIKE '%key%' within dbTopicId
}

// ── Grade 4 — Full ch-series + IPM pool ──────────────────────────────────────

const GRADE4_TOPICS: TopicNode[] = [
  { id: 'gr4_numbers',    name: 'Number System & Place Value', emoji: '🔢', grade: 4, examWeight: 0.15, dbTopicId: 'ch01-05' },
  { id: 'gr4_factors',    name: 'Factors & Multiples',         emoji: '🔑', grade: 4, examWeight: 0.10, dbTopicId: 'ch06' },
  { id: 'gr4_fractions',  name: 'Fractions',                   emoji: '🍕', grade: 4, examWeight: 0.12, dbTopicId: 'ch07-08' },
  { id: 'gr4_operations', name: 'Operations & BODMAS',         emoji: '➗', grade: 4, examWeight: 0.12, dbTopicId: 'ch09-10' },
  { id: 'gr4_decimals',   name: 'Decimal Fractions',           emoji: '📊', grade: 4, examWeight: 0.10, dbTopicId: 'ch11' },
  { id: 'gr4_units',      name: 'Decimal Units of Measurement',emoji: '📏', grade: 4, examWeight: 0.05, dbTopicId: 'ch12' },
  { id: 'gr4_algebra',    name: 'Algebraic Expressions',       emoji: '🔤', grade: 4, examWeight: 0.08, dbTopicId: 'ch13' },
  { id: 'gr4_equations',  name: 'Equations',                   emoji: '⚖️', grade: 4, examWeight: 0.08, dbTopicId: 'ch14' },
  { id: 'gr4_puzzles',    name: 'Puzzles & Magic Squares',     emoji: '🧩', grade: 4, examWeight: 0.05, dbTopicId: 'ch15' },
  { id: 'gr4_sequences',  name: 'Sequence & Series',           emoji: '🔗', grade: 4, examWeight: 0.05, dbTopicId: 'ch16' },
  { id: 'gr4_time',       name: 'Measurement of Time & Calendar',emoji: '🕐', grade: 4, examWeight: 0.03, dbTopicId: 'ch17' },
  { id: 'gr4_angles',     name: 'Angles',                      emoji: '📐', grade: 4, examWeight: 0.05, dbTopicId: 'ch18' },
  { id: 'gr4_triangles',  name: 'Triangles',                   emoji: '🔺', grade: 4, examWeight: 0.05, dbTopicId: 'ch19' },
  { id: 'gr4_quads',      name: 'Quadrilaterals',              emoji: '⬜', grade: 4, examWeight: 0.03, dbTopicId: 'ch20' },
  { id: 'gr4_circle',     name: 'Circle',                      emoji: '⭕', grade: 4, examWeight: 0.03, dbTopicId: 'ch21' },
  { id: 'gr4_data',       name: 'Data Handling & Graphs',      emoji: '📈', grade: 4, examWeight: 0.06, dbTopicId: 'dh' },
  { id: 'gr4_ipm',        name: 'IPM Past Papers',             emoji: '🎓', grade: 4, examWeight: 0.20, dbTopicId: 'grade4' },
];

// ── Grade 2 ───────────────────────────────────────────────────────────────────

const GRADE2_TOPICS: TopicNode[] = [
  { id: 'gr2_numbers',     name: 'Numbers & Counting',    emoji: '🔢', grade: 2, examWeight: 0.25, dbTopicId: 'grade2', subTopicKey: 'number' },
  { id: 'gr2_addition',    name: 'Addition & Subtraction',emoji: '➕', grade: 2, examWeight: 0.25, dbTopicId: 'grade2', subTopicKey: 'addition' },
  { id: 'gr2_shapes',      name: 'Shapes & Geometry',     emoji: '🔷', grade: 2, examWeight: 0.15, dbTopicId: 'grade2', subTopicKey: 'shape' },
  { id: 'gr2_patterns',    name: 'Patterns & Sequences',  emoji: '🔁', grade: 2, examWeight: 0.15, dbTopicId: 'grade2', subTopicKey: 'pattern' },
  { id: 'gr2_measurement', name: 'Measurement & Time',    emoji: '📏', grade: 2, examWeight: 0.10, dbTopicId: 'grade2', subTopicKey: 'measurement' },
  { id: 'gr2_money',       name: 'Money & Currency',      emoji: '💰', grade: 2, examWeight: 0.10, dbTopicId: 'grade2', subTopicKey: 'money' },
];

// ── Grade 3 ───────────────────────────────────────────────────────────────────

const GRADE3_TOPICS: TopicNode[] = [
  { id: 'gr3_numbers',      name: 'Numbers & Place Value',   emoji: '🔢', grade: 3, examWeight: 0.20, dbTopicId: 'grade3', subTopicKey: 'number' },
  { id: 'gr3_multiply',     name: 'Multiplication',          emoji: '✖️', grade: 3, examWeight: 0.20, dbTopicId: 'grade3', subTopicKey: 'multiplication' },
  { id: 'gr3_division',     name: 'Division',                emoji: '➗', grade: 3, examWeight: 0.15, dbTopicId: 'grade3', subTopicKey: 'division' },
  { id: 'gr3_fractions',    name: 'Basic Fractions',         emoji: '🍕', grade: 3, examWeight: 0.15, dbTopicId: 'grade3', subTopicKey: 'fraction' },
  { id: 'gr3_measurement',  name: 'Measurement & Time',      emoji: '📏', grade: 3, examWeight: 0.10, dbTopicId: 'grade3', subTopicKey: 'measurement' },
  { id: 'gr3_geometry',     name: 'Shapes & Geometry',       emoji: '🔷', grade: 3, examWeight: 0.10, dbTopicId: 'grade3', subTopicKey: 'shape' },
  { id: 'gr3_data',         name: 'Data & Graphs',           emoji: '📊', grade: 3, examWeight: 0.10, dbTopicId: 'grade3', subTopicKey: 'data' },
];

// ── Grade 5 ───────────────────────────────────────────────────────────────────

const GRADE5_TOPICS: TopicNode[] = [
  { id: 'gr5_decimals',     name: 'Decimal Operations',      emoji: '📊', grade: 5, examWeight: 0.18, dbTopicId: 'grade5', subTopicKey: 'decimal' },
  { id: 'gr5_fractions',    name: 'Fractions & Mixed Numbers',emoji: '🍕', grade: 5, examWeight: 0.18, dbTopicId: 'grade5', subTopicKey: 'fraction' },
  { id: 'gr5_percentages',  name: 'Percentages & Ratios',    emoji: '💯', grade: 5, examWeight: 0.16, dbTopicId: 'grade5', subTopicKey: 'percentage' },
  { id: 'gr5_geometry',     name: 'Area & Perimeter',        emoji: '📐', grade: 5, examWeight: 0.16, dbTopicId: 'grade5', subTopicKey: 'area' },
  { id: 'gr5_angles',       name: 'Angles & Lines',          emoji: '📏', grade: 5, examWeight: 0.12, dbTopicId: 'grade5', subTopicKey: 'angle' },
  { id: 'gr5_data',         name: 'Data Interpretation',     emoji: '📈', grade: 5, examWeight: 0.10, dbTopicId: 'grade5', subTopicKey: 'data' },
  { id: 'gr5_algebra',      name: 'Algebraic Thinking',      emoji: '🔤', grade: 5, examWeight: 0.10, dbTopicId: 'grade5', subTopicKey: 'algebra' },
];

// ── Grade 6 ───────────────────────────────────────────────────────────────────

const GRADE6_TOPICS: TopicNode[] = [
  { id: 'gr6_integers',     name: 'Integers & Number Line',  emoji: '🔢', grade: 6, examWeight: 0.20, dbTopicId: 'grade6', subTopicKey: 'integer' },
  { id: 'gr6_fractions',    name: 'Fractions & Rationals',   emoji: '🍕', grade: 6, examWeight: 0.18, dbTopicId: 'grade6', subTopicKey: 'fraction' },
  { id: 'gr6_algebra',      name: 'Algebraic Expressions',   emoji: '🔤', grade: 6, examWeight: 0.18, dbTopicId: 'grade6', subTopicKey: 'algebra' },
  { id: 'gr6_geometry',     name: 'Basic Geometry',          emoji: '📐', grade: 6, examWeight: 0.15, dbTopicId: 'grade6', subTopicKey: 'geometry' },
  { id: 'gr6_percentages',  name: 'Percentages & Profit-Loss',emoji: '💯', grade: 6, examWeight: 0.15, dbTopicId: 'grade6', subTopicKey: 'percentage' },
  { id: 'gr6_statistics',   name: 'Statistics & Data',       emoji: '📊', grade: 6, examWeight: 0.07, dbTopicId: 'grade6', subTopicKey: 'statistic' },
  { id: 'gr6_ratio',        name: 'Ratio & Proportion',      emoji: '⚖️', grade: 6, examWeight: 0.07, dbTopicId: 'grade6', subTopicKey: 'ratio' },
];

// ── Grade 7 ───────────────────────────────────────────────────────────────────

const GRADE7_TOPICS: TopicNode[] = [
  { id: 'gr7_algebra',      name: 'Algebra & Equations',     emoji: '🔤', grade: 7, examWeight: 0.22, dbTopicId: 'grade7', subTopicKey: 'algebra' },
  { id: 'gr7_triangles',    name: 'Triangles & Congruence',  emoji: '🔺', grade: 7, examWeight: 0.18, dbTopicId: 'grade7', subTopicKey: 'triangle' },
  { id: 'gr7_exponents',    name: 'Exponents & Powers',      emoji: '⚡', grade: 7, examWeight: 0.15, dbTopicId: 'grade7', subTopicKey: 'exponent' },
  { id: 'gr7_percentages',  name: 'Percentages & Profit-Loss',emoji: '💯', grade: 7, examWeight: 0.15, dbTopicId: 'grade7', subTopicKey: 'percentage' },
  { id: 'gr7_geometry',     name: 'Areas & Volumes',         emoji: '📐', grade: 7, examWeight: 0.15, dbTopicId: 'grade7', subTopicKey: 'area' },
  { id: 'gr7_data',         name: 'Data Handling',           emoji: '📊', grade: 7, examWeight: 0.08, dbTopicId: 'grade7', subTopicKey: 'data' },
  { id: 'gr7_ratio',        name: 'Ratio & Proportion',      emoji: '⚖️', grade: 7, examWeight: 0.07, dbTopicId: 'grade7', subTopicKey: 'ratio' },
];

// ── Grade 8 ───────────────────────────────────────────────────────────────────

const GRADE8_TOPICS: TopicNode[] = [
  { id: 'gr8_polynomials',  name: 'Polynomials & Factoring', emoji: '🔢', grade: 8, examWeight: 0.22, dbTopicId: 'grade8', subTopicKey: 'polynomial' },
  { id: 'gr8_linear',       name: 'Linear Equations',        emoji: '📏', grade: 8, examWeight: 0.20, dbTopicId: 'grade8', subTopicKey: 'linear' },
  { id: 'gr8_quads',        name: 'Quadrilaterals',          emoji: '⬜', grade: 8, examWeight: 0.15, dbTopicId: 'grade8', subTopicKey: 'quadrilateral' },
  { id: 'gr8_mensuration',  name: 'Mensuration & Volumes',   emoji: '📦', grade: 8, examWeight: 0.15, dbTopicId: 'grade8', subTopicKey: 'mensuration' },
  { id: 'gr8_exponents',    name: 'Exponents & Powers',      emoji: '⚡', grade: 8, examWeight: 0.13, dbTopicId: 'grade8', subTopicKey: 'exponent' },
  { id: 'gr8_statistics',   name: 'Statistics & Data',       emoji: '📊', grade: 8, examWeight: 0.08, dbTopicId: 'grade8', subTopicKey: 'statistic' },
  { id: 'gr8_ratio',        name: 'Ratio, Proportion & Variation', emoji: '⚖️', grade: 8, examWeight: 0.07, dbTopicId: 'grade8', subTopicKey: 'ratio' },
];

// ── Grade 9 ───────────────────────────────────────────────────────────────────

const GRADE9_TOPICS: TopicNode[] = [
  { id: 'gr9_number',       name: 'Number Systems',          emoji: '🔢', grade: 9, examWeight: 0.18, dbTopicId: 'grade9', subTopicKey: 'number' },
  { id: 'gr9_polynomials',  name: 'Polynomials',             emoji: '📐', grade: 9, examWeight: 0.18, dbTopicId: 'grade9', subTopicKey: 'polynomial' },
  { id: 'gr9_coordinate',   name: 'Coordinate Geometry',     emoji: '🗺️', grade: 9, examWeight: 0.15, dbTopicId: 'grade9', subTopicKey: 'coordinate' },
  { id: 'gr9_euclid',       name: 'Euclid\'s Geometry',      emoji: '📏', grade: 9, examWeight: 0.12, dbTopicId: 'grade9', subTopicKey: 'euclid' },
  { id: 'gr9_circles',      name: 'Circles',                 emoji: '⭕', grade: 9, examWeight: 0.13, dbTopicId: 'grade9', subTopicKey: 'circle' },
  { id: 'gr9_surface',      name: 'Surface Areas & Volumes', emoji: '📦', grade: 9, examWeight: 0.12, dbTopicId: 'grade9', subTopicKey: 'surface' },
  { id: 'gr9_statistics',   name: 'Statistics',              emoji: '📊', grade: 9, examWeight: 0.06, dbTopicId: 'grade9', subTopicKey: 'statistic' },
  { id: 'gr9_probability',  name: 'Probability',             emoji: '🎲', grade: 9, examWeight: 0.06, dbTopicId: 'grade9', subTopicKey: 'probability' },
];

// ── Combined ──────────────────────────────────────────────────────────────────

export const TOPIC_TREE: TopicNode[] = [
  ...GRADE2_TOPICS,
  ...GRADE3_TOPICS,
  ...GRADE4_TOPICS,
  ...GRADE5_TOPICS,
  ...GRADE6_TOPICS,
  ...GRADE7_TOPICS,
  ...GRADE8_TOPICS,
  ...GRADE9_TOPICS,
];

export function getTopicsForGrade(grade: number): TopicNode[] {
  return TOPIC_TREE.filter((t) => t.grade === grade);
}
