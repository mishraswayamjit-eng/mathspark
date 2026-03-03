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
// Data coverage: bodmas, addition_subtraction, perimeter_area (3 stems)

const GRADE2_TOPICS: TopicNode[] = [
  { id: 'gr2_numbers',     name: 'Numbers & Counting',    emoji: '🔢', grade: 2, examWeight: 0.35, dbTopicId: 'grade2', subTopicKey: 'number' },
  { id: 'gr2_addition',    name: 'Addition & Subtraction',emoji: '➕', grade: 2, examWeight: 0.35, dbTopicId: 'grade2', subTopicKey: 'addition' },
  { id: 'gr2_shapes',      name: 'Shapes & Measurement',  emoji: '🔷', grade: 2, examWeight: 0.30, dbTopicId: 'grade2', subTopicKey: 'shape' },
];

// ── Grade 3 ───────────────────────────────────────────────────────────────────
// Data coverage: bodmas, addition_subtraction, factors, fraction_arithmetic, perimeter_area (5 stems → 4 lessons)

const GRADE3_TOPICS: TopicNode[] = [
  { id: 'gr3_numbers',      name: 'Numbers & Operations',    emoji: '🔢', grade: 3, examWeight: 0.30, dbTopicId: 'grade3', subTopicKey: 'number' },
  { id: 'gr3_multiply',     name: 'Multiplication & Factors',emoji: '✖️', grade: 3, examWeight: 0.25, dbTopicId: 'grade3', subTopicKey: 'multiplication' },
  { id: 'gr3_fractions',    name: 'Basic Fractions',         emoji: '🍕', grade: 3, examWeight: 0.25, dbTopicId: 'grade3', subTopicKey: 'fraction' },
  { id: 'gr3_geometry',     name: 'Shapes & Measurement',    emoji: '🔷', grade: 3, examWeight: 0.20, dbTopicId: 'grade3', subTopicKey: 'shape' },
];

// ── Grade 5 ───────────────────────────────────────────────────────────────────
// Data coverage: bodmas, simple_interest, angles, fraction_arithmetic, percentage, perimeter_area, equation, hcf_lcm (8 stems → 6 lessons)

const GRADE5_TOPICS: TopicNode[] = [
  { id: 'gr5_percentages',  name: 'Percentages & Interest',  emoji: '💯', grade: 5, examWeight: 0.22, dbTopicId: 'grade5', subTopicKey: 'percentage' },
  { id: 'gr5_fractions',    name: 'Fractions & HCF/LCM',    emoji: '🍕', grade: 5, examWeight: 0.20, dbTopicId: 'grade5', subTopicKey: 'fraction' },
  { id: 'gr5_decimals',     name: 'Decimals & BODMAS',       emoji: '📊', grade: 5, examWeight: 0.16, dbTopicId: 'grade5', subTopicKey: 'decimal' },
  { id: 'gr5_geometry',     name: 'Area & Perimeter',        emoji: '📐', grade: 5, examWeight: 0.16, dbTopicId: 'grade5', subTopicKey: 'area' },
  { id: 'gr5_algebra',      name: 'Equations & Algebra',     emoji: '🔤', grade: 5, examWeight: 0.14, dbTopicId: 'grade5', subTopicKey: 'algebra' },
  { id: 'gr5_angles',       name: 'Angles & Lines',          emoji: '📏', grade: 5, examWeight: 0.12, dbTopicId: 'grade5', subTopicKey: 'angle' },
];

// ── Grade 6 ───────────────────────────────────────────────────────────────────
// Data coverage: simple_interest, angles, perimeter_area, hcf_lcm, equation, percentage, fraction_arithmetic, bodmas (8 stems → 5 lessons)

const GRADE6_TOPICS: TopicNode[] = [
  { id: 'gr6_percentages',  name: 'Percentages & Interest',  emoji: '💯', grade: 6, examWeight: 0.25, dbTopicId: 'grade6', subTopicKey: 'percentage' },
  { id: 'gr6_integers',     name: 'Integers & BODMAS',       emoji: '🔢', grade: 6, examWeight: 0.20, dbTopicId: 'grade6', subTopicKey: 'integer' },
  { id: 'gr6_algebra',      name: 'Equations & Algebra',     emoji: '🔤', grade: 6, examWeight: 0.20, dbTopicId: 'grade6', subTopicKey: 'algebra' },
  { id: 'gr6_geometry',     name: 'Geometry & Mensuration',  emoji: '📐', grade: 6, examWeight: 0.20, dbTopicId: 'grade6', subTopicKey: 'geometry' },
  { id: 'gr6_fractions',    name: 'Fractions & Rationals',   emoji: '🍕', grade: 6, examWeight: 0.15, dbTopicId: 'grade6', subTopicKey: 'fraction' },
];

// ── Grade 7 ───────────────────────────────────────────────────────────────────
// Data coverage: perimeter_area, equation, percentage, simple_interest, hcf_lcm, angles, bodmas, fraction_arithmetic (8 stems → 5 lessons)

const GRADE7_TOPICS: TopicNode[] = [
  { id: 'gr7_algebra',      name: 'Algebra & Equations',     emoji: '🔤', grade: 7, examWeight: 0.25, dbTopicId: 'grade7', subTopicKey: 'algebra' },
  { id: 'gr7_percentages',  name: 'Percentages & Interest',  emoji: '💯', grade: 7, examWeight: 0.25, dbTopicId: 'grade7', subTopicKey: 'percentage' },
  { id: 'gr7_ratio',        name: 'Ratio & Proportion',      emoji: '⚖️', grade: 7, examWeight: 0.20, dbTopicId: 'grade7', subTopicKey: 'ratio' },
  { id: 'gr7_geometry',     name: 'Areas & Volumes',         emoji: '📐', grade: 7, examWeight: 0.15, dbTopicId: 'grade7', subTopicKey: 'area' },
  { id: 'gr7_triangles',    name: 'Triangles & Angles',      emoji: '🔺', grade: 7, examWeight: 0.15, dbTopicId: 'grade7', subTopicKey: 'triangle' },
];

// ── Grade 8 ───────────────────────────────────────────────────────────────────
// Data coverage: perimeter_area, simple_interest, percentage, equation, bodmas, hcf_lcm, fraction_arithmetic, angles (8 stems → 5 lessons)

const GRADE8_TOPICS: TopicNode[] = [
  { id: 'gr8_ratio',        name: 'Ratio, Interest & Percent',emoji: '⚖️', grade: 8, examWeight: 0.25, dbTopicId: 'grade8', subTopicKey: 'ratio' },
  { id: 'gr8_polynomials',  name: 'Polynomials & Factoring', emoji: '🔢', grade: 8, examWeight: 0.20, dbTopicId: 'grade8', subTopicKey: 'polynomial' },
  { id: 'gr8_linear',       name: 'Linear Equations',        emoji: '📏', grade: 8, examWeight: 0.20, dbTopicId: 'grade8', subTopicKey: 'linear' },
  { id: 'gr8_mensuration',  name: 'Mensuration & Volumes',   emoji: '📦', grade: 8, examWeight: 0.20, dbTopicId: 'grade8', subTopicKey: 'mensuration' },
  { id: 'gr8_quads',        name: 'Quadrilaterals & Angles',  emoji: '⬜', grade: 8, examWeight: 0.15, dbTopicId: 'grade8', subTopicKey: 'quadrilateral' },
];

// ── Grade 9 ───────────────────────────────────────────────────────────────────
// Data coverage: percentage, simple_interest, equation, bodmas, perimeter_area, hcf_lcm, angles, fraction_arithmetic (8 stems → 4 lessons)

const GRADE9_TOPICS: TopicNode[] = [
  { id: 'gr9_number',       name: 'Number Systems',          emoji: '🔢', grade: 9, examWeight: 0.35, dbTopicId: 'grade9', subTopicKey: 'number' },
  { id: 'gr9_polynomials',  name: 'Polynomials & Equations', emoji: '📐', grade: 9, examWeight: 0.25, dbTopicId: 'grade9', subTopicKey: 'polynomial' },
  { id: 'gr9_surface',      name: 'Surface Areas & Volumes', emoji: '📦', grade: 9, examWeight: 0.25, dbTopicId: 'grade9', subTopicKey: 'surface' },
  { id: 'gr9_coordinate',   name: 'Coordinate Geometry',     emoji: '🗺️', grade: 9, examWeight: 0.15, dbTopicId: 'grade9', subTopicKey: 'coordinate' },
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
