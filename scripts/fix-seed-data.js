#!/usr/bin/env node
/**
 * fix-seed-data.js
 *
 * Fixes the seed data for non-Grade-4 questions:
 *   1. Re-tags subTopic to match topicTree subTopicKeys (keyword classification)
 *   2. Reports questions with empty correctAnswer / empty options
 *   3. Writes updated JSON to data/mathspark_complete_seed.json
 *
 * Usage: node scripts/fix-seed-data.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');
const SEED_PATH = path.join(__dirname, '..', 'data', 'mathspark_complete_seed.json');

// ─── SubTopicKey definitions per grade (must match topicTree.ts) ────────────

const GRADE_SUBTOPICS = {
  // Grade 4 pool uses the same subTopicKeys as the ch-series topicTree entries
  // (these questions go to /practice/grade4 with subTopic filters)
  4: [
    { key: 'number',      label: 'Number System & Place Value' },
    { key: 'factor',      label: 'Factors & Multiples' },
    { key: 'fraction',    label: 'Fractions' },
    { key: 'operation',   label: 'Operations & BODMAS' },
    { key: 'decimal',     label: 'Decimal Fractions' },
    { key: 'unit',        label: 'Decimal Units of Measurement' },
    { key: 'algebra',     label: 'Algebraic Expressions' },
    { key: 'equation',    label: 'Equations' },
    { key: 'puzzle',      label: 'Puzzles & Magic Squares' },
    { key: 'sequence',    label: 'Sequence & Series' },
    { key: 'time',        label: 'Measurement of Time & Calendar' },
    { key: 'angle',       label: 'Angles' },
    { key: 'triangle',    label: 'Triangles' },
    { key: 'quadrilateral', label: 'Quadrilaterals' },
    { key: 'circle',      label: 'Circle' },
    { key: 'data',        label: 'Data Handling & Graphs' },
  ],
  2: [
    { key: 'number',      label: 'Numbers & Counting' },
    { key: 'addition',    label: 'Addition & Subtraction' },
    { key: 'shape',       label: 'Shapes & Measurement' },
  ],
  3: [
    { key: 'number',         label: 'Numbers & Operations' },
    { key: 'multiplication', label: 'Multiplication & Factors' },
    { key: 'fraction',       label: 'Basic Fractions' },
    { key: 'shape',          label: 'Shapes & Measurement' },
  ],
  5: [
    { key: 'percentage', label: 'Percentages & Interest' },
    { key: 'fraction',   label: 'Fractions & HCF/LCM' },
    { key: 'decimal',    label: 'Decimals & BODMAS' },
    { key: 'area',       label: 'Area & Perimeter' },
    { key: 'algebra',    label: 'Equations & Algebra' },
    { key: 'angle',      label: 'Angles & Lines' },
  ],
  6: [
    { key: 'percentage', label: 'Percentages & Interest' },
    { key: 'integer',    label: 'Integers & BODMAS' },
    { key: 'algebra',    label: 'Equations & Algebra' },
    { key: 'geometry',   label: 'Geometry & Mensuration' },
    { key: 'fraction',   label: 'Fractions & Rationals' },
  ],
  7: [
    { key: 'algebra',    label: 'Algebra & Equations' },
    { key: 'percentage', label: 'Percentages & Interest' },
    { key: 'ratio',      label: 'Ratio & Proportion' },
    { key: 'area',       label: 'Areas & Volumes' },
    { key: 'triangle',   label: 'Triangles & Angles' },
  ],
  8: [
    { key: 'ratio',         label: 'Ratio, Interest & Percent' },
    { key: 'polynomial',    label: 'Polynomials & Factoring' },
    { key: 'linear',        label: 'Linear Equations' },
    { key: 'mensuration',   label: 'Mensuration & Volumes' },
    { key: 'quadrilateral', label: 'Quadrilaterals & Angles' },
  ],
  9: [
    { key: 'number',      label: 'Number Systems' },
    { key: 'polynomial',  label: 'Polynomials & Equations' },
    { key: 'surface',     label: 'Surface Areas & Volumes' },
    { key: 'coordinate',  label: 'Coordinate Geometry' },
  ],
};

// ─── ID stem → subTopicKey mapping ──────────────────────────────────────────
// Maps the topic stem from auto_generated_v2 IDs to the best topicTree subTopicKey

const ID_STEM_MAP = {
  // Grade 4 pool
  '4:bodmas':                'operation',
  '4:addition_subtraction':  'operation',
  '4:perimeter_area':        'quadrilateral',
  '4:factors':               'factor',
  '4:fraction_arithmetic':   'fraction',
  '4:equation':              'equation',
  '4:angles':                'angle',
  '4:simple_interest':       'decimal',
  '4:percentage':            'decimal',
  '4:hcf_lcm':              'factor',

  // Grade 2
  '2:bodmas':                'number',
  '2:addition_subtraction':  'addition',
  '2:perimeter_area':        'shape',

  // Grade 3
  '3:bodmas':                'number',
  '3:addition_subtraction':  'number',
  '3:factors':               'multiplication',
  '3:fraction_arithmetic':   'fraction',
  '3:perimeter_area':        'shape',

  // Grade 5
  '5:bodmas':                'decimal',
  '5:simple_interest':       'percentage',
  '5:angles':                'angle',
  '5:fraction_arithmetic':   'fraction',
  '5:percentage':            'percentage',
  '5:perimeter_area':        'area',
  '5:equation':              'algebra',
  '5:hcf_lcm':              'fraction',

  // Grade 6
  '6:simple_interest':       'percentage',
  '6:angles':                'geometry',
  '6:perimeter_area':        'geometry',
  '6:hcf_lcm':              'integer',
  '6:equation':              'algebra',
  '6:percentage':            'percentage',
  '6:fraction_arithmetic':   'fraction',
  '6:bodmas':                'integer',

  // Grade 7
  '7:perimeter_area':        'area',
  '7:equation':              'algebra',
  '7:percentage':            'percentage',
  '7:simple_interest':       'percentage',
  '7:hcf_lcm':              'ratio',
  '7:angles':                'triangle',
  '7:bodmas':                'algebra',
  '7:fraction_arithmetic':   'ratio',

  // Grade 8
  '8:perimeter_area':        'mensuration',
  '8:simple_interest':       'ratio',
  '8:percentage':            'ratio',
  '8:equation':              'linear',
  '8:bodmas':                'polynomial',
  '8:hcf_lcm':              'polynomial',
  '8:fraction_arithmetic':   'ratio',
  '8:angles':                'quadrilateral',

  // Grade 9
  '9:percentage':            'number',
  '9:simple_interest':       'number',
  '9:equation':              'polynomial',
  '9:bodmas':                'number',
  '9:perimeter_area':        'surface',
  '9:hcf_lcm':              'number',
  '9:angles':                'coordinate',
  '9:fraction_arithmetic':   'number',
};

// ─── Keyword-based classification (for official_ipm and mega_final) ─────────
// Order matters: first match wins. More specific patterns first.

function buildKeywordClassifier() {
  const rules = {
    4: [
      { key: 'data',          patterns: [/graph|chart|data|table|average|mean|tally|bar|pie|pictograph|frequency/i] },
      { key: 'circle',        patterns: [/circle|radius|diameter|circumference|chord|arc|sector|semi-?circle/i] },
      { key: 'triangle',      patterns: [/triangle|isosceles|equilateral|scalene|angle sum.*triangle|altitude|median.*triangle/i] },
      { key: 'quadrilateral', patterns: [/quadrilateral|rectangle|parallelogram|rhombus|trapez|square.*property|diagonal|perimeter|area/i] },
      { key: 'angle',         patterns: [/angle|degree|complementary|supplementary|adjacent|vertically|protractor|acute|obtuse|reflex|right angle/i] },
      { key: 'time',          patterns: [/time|clock|calendar|hour|minute|second|day|week|month|year|leap|date|schedule/i] },
      { key: 'sequence',      patterns: [/sequence|series|pattern|fibonacci|arithmetic|geometric|next.*term|nth term/i] },
      { key: 'puzzle',        patterns: [/puzzle|magic square|balance|riddle|logic|cryptarithm|match.*stick/i] },
      { key: 'equation',      patterns: [/equation|solve|value of|find.*x|lhs.*rhs|variable.*equation/i] },
      { key: 'algebra',       patterns: [/algebra|expression|coefficient|like term|variable|simplif.*express|substitut/i] },
      { key: 'unit',          patterns: [/\bkg\b|\bcm\b|\bmm\b|\bkm\b|meter|litre|\bml\b|gram|unit.*measurement|convert.*unit|capacity|temperature/i] },
      { key: 'decimal',       patterns: [/decimal|point|tenth|hundredth|decimal.*fraction/i] },
      { key: 'operation',     patterns: [/bodmas|order of operation|bracket|simplif|add|subtract|multiply|divide|sum|differ|product|quotient/i] },
      { key: 'fraction',      patterns: [/fraction|numerator|denominator|mixed|improper|equivalent|half|quarter|third|lcm|hcf|gcd/i] },
      { key: 'factor',        patterns: [/factor|multiple|prime|composite|divisib|common|lcm|hcf|gcd|co-?prime/i] },
      { key: 'number',        patterns: [/number|digit|place value|even|odd|roman|expand|ascend|descend|great|small|compar|count|total|how many/i] },
    ],
    2: [
      { key: 'shape',       patterns: [/shape|triangle|circle|rectangle|square|mirror|symmetry|side|corner|face|edge|figure|line|straight|curve|angle|perimeter|area|pattern.*shape|image|time|clock|day|week|month|year|calendar|hour|minute|measure|weight|height|\bkg\b|\bcm\b|\bm\b|meter|litre|heavy|light|tall|distance/i] },
      { key: 'addition',    patterns: [/add|subtract|plus|minus|take away|sum|differ|more than|less than|remain|left|gave|borrow|carry|altogether|money|coin|rupee|paise|\brs\b|price|cost|buy|sell|shop|pay|change|currency/i] },
      { key: 'number',      patterns: [/number|count|digit|place value|even|odd|great|small|compare|largest|smallest|how many|total|half|double|twice|fraction|divide|multiply|product|bodmas|simplif|pattern|sequence|next|series|logic|arrange|order|missing|puzzle/i] },
    ],
    3: [
      { key: 'shape',          patterns: [/shape|triangle|circle|rectangle|square|perimeter|area|symmetry|face|edge|corner|angle|figure|line|curve|mirror|time|clock|calendar|hour|minute|\bkg\b|\bcm\b|\bm\b|meter|litre|measure|weight|distance|temperature|capacity|graph|chart|data|table|tally|bar|pie|pictograph/i] },
      { key: 'fraction',       patterns: [/fraction|half|quarter|third|numerator|denominator|whole|part|share|equal parts|mixed|divid|quotient|remainder|share equally|split|distribute|group of/i] },
      { key: 'multiplication', patterns: [/multipl|product|times|factor|table|\bdouble\b|triple|twice|thrice/i] },
      { key: 'number',         patterns: [/number|count|digit|place value|even|odd|great|small|compare|add|subtract|sum|differ|bodmas|simplif|roman|expand|ascend|descend/i] },
    ],
    5: [
      { key: 'angle',      patterns: [/angle|degree|complementary|supplementary|adjacent|vertically opposite|straight line|parallel|perpendicular|transversal/i] },
      { key: 'area',       patterns: [/area|perimeter|square.*unit|length.*breadth|rectangle|triangle.*area|circle.*area|circumference|surface/i] },
      { key: 'percentage',  patterns: [/percent|profit|loss|discount|interest|rate|ratio|proportion|marked price|\b%\b/i] },
      { key: 'fraction',   patterns: [/fraction|numerator|denominator|mixed|improper|equivalent|lcm|hcf|gcd|common factor|common multiple|simplif.*frac|graph|chart|data|table|average|mean|median/i] },
      { key: 'algebra',    patterns: [/equation|variable|expression|solve|value of|find.*x|algebra|simplif|substitut|linear/i] },
      { key: 'decimal',    patterns: [/decimal|bodmas|simplif|order of operation|bracket|point.*value|place.*value|\.\d+/i] },
    ],
    6: [
      { key: 'geometry',   patterns: [/angle|triangle|circle|perimeter|area|parallel|perpendicular|line|ray|segment|congruent|symmetry|shape|quadrilateral|polygon|graph|chart|data|table|average|mean|median|mode|frequency|statistic|survey|bar|pie/i] },
      { key: 'percentage', patterns: [/percent|profit|loss|discount|interest|rate|marked price|\b%\b|selling price|cost price|ratio|proportion|unitary|direct|inverse|varies|map|scale|speed.*time|distance.*time/i] },
      { key: 'algebra',    patterns: [/equation|variable|expression|solve|value of|find.*x|algebra|simplif|substitut|linear|polynomial/i] },
      { key: 'fraction',   patterns: [/fraction|numerator|denominator|mixed|improper|rational|lcm|hcf|gcd|common/i] },
      { key: 'integer',    patterns: [/integer|negative|positive|number line|absolute|bodmas|simplif|order of|factor|multiple|prime|composite|even|odd|divisib/i] },
    ],
    7: [
      { key: 'ratio',      patterns: [/ratio|proportion|unitary|direct variation|inverse variation|speed.*time|distance|graph|chart|data|table|average|mean|median|mode|frequency|statistic|survey|exponent|power|index|base|scientific notation|\^|square root|cube root/i] },
      { key: 'triangle',   patterns: [/triangle|congruent|angle.*sum|isosceles|equilateral|scalene|median|altitude|pythagoras|hypotenuse/i] },
      { key: 'percentage', patterns: [/percent|profit|loss|discount|interest|rate|marked price|\b%\b|selling|cost price|simple interest|compound/i] },
      { key: 'area',       patterns: [/area|perimeter|volume|surface|circumference|circle|rectangle|parallelogram|trapez/i] },
      { key: 'algebra',    patterns: [/equation|variable|expression|solve|value of|find.*x|algebra|simplif|substitut|linear|polynomial|factor|identity|bodmas/i] },
    ],
    8: [
      { key: 'quadrilateral', patterns: [/quadrilateral|parallelogram|rectangle|rhombus|trapez|square.*property|diagonal|mid-?point|angle.*sum.*360/i] },
      { key: 'mensuration',   patterns: [/area|perimeter|volume|surface|cube|cuboid|cylinder|cone|sphere|mensuration|capacity/i] },
      { key: 'ratio',         patterns: [/ratio|proportion|variation|percent|profit|loss|discount|interest|rate|\b%\b|selling|cost price|compound|simple interest|graph|chart|data|table|average|mean|median|mode|frequency|statistic|survey|exponent|power|index|base|scientific notation|\^|standard form/i] },
      { key: 'linear',        patterns: [/equation|solve|variable|linear|value of|find.*x|simultaneous|graph.*line|word problem|ages/i] },
      { key: 'polynomial',    patterns: [/polynomial|factor|identity|expression|simplif|expand|algebra|degree|coefficient|term|bodmas|remainder|divisib/i] },
    ],
    9: [
      { key: 'surface',     patterns: [/surface area|volume|cube|cuboid|cylinder|cone|sphere|hemisphere|mensuration|capacity|solid|area|perimeter/i] },
      { key: 'coordinate',  patterns: [/coordinate|plot|point|x-axis|y-axis|origin|quadrant|abscissa|ordinate|graph.*point|distance.*formula|circle|chord|arc|sector|tangent|radius|diameter|cyclic/i] },
      { key: 'polynomial',  patterns: [/polynomial|factor|zero|root|degree|coefficient|remainder|identity|expand|expression|algebra|equation|solve|simplif|variable|bodmas/i] },
      { key: 'number',      patterns: [/number|rational|irrational|real|integer|natural|whole|prime|composite|sqrt|root|decimal.*expand|percent|interest|ratio|proportion|\b%\b|probability|chance|random|event|outcome|graph|chart|data|table|average|mean|median|mode|frequency|statistic|euclid|axiom|postulate|theorem|proof/i] },
    ],
  };
  return rules;
}

// ─── Classification Logic ───────────────────────────────────────────────────

function extractIdStem(id) {
  // VAR_G2_vary_bodmas_V01 → bodmas
  // VAR_G5_vary_simple_interest_V42 → simple_interest
  const m = id.match(/^VAR_G\d+_vary_(.+)_V\d+$/);
  return m ? m[1] : null;
}

function classifyQuestion(q, grade, keywordRules) {
  // Strategy 1: ID stem mapping (most reliable for auto_generated_v2)
  const stem = extractIdStem(q.id);
  if (stem) {
    const mapped = ID_STEM_MAP[`${grade}:${stem}`];
    if (mapped) return { key: mapped, method: 'id_stem' };
  }

  // Strategy 2: Keyword matching on question text + options
  const text = [
    q.questionText || '',
    ...(q.options || []).map(o => typeof o === 'string' ? o : (o.text || '')),
    q.subTopic || '',
  ].join(' ');

  const rules = keywordRules[grade];
  if (rules) {
    for (const rule of rules) {
      for (const pat of rule.patterns) {
        if (pat.test(text)) {
          return { key: rule.key, method: 'keyword' };
        }
      }
    }
  }

  // Strategy 3: Fallback to first subTopic (default bucket)
  const subs = GRADE_SUBTOPICS[grade];
  return { key: subs ? subs[0].key : 'unknown', method: 'fallback' };
}

// ─── Main ───────────────────────────────────────────────────────────────────

function main() {
  console.log('Reading seed data...');
  const raw = fs.readFileSync(SEED_PATH, 'utf-8');
  const data = JSON.parse(raw);
  const questions = data.questions;
  console.log(`Total questions: ${questions.length}`);

  const keywordRules = buildKeywordClassifier();

  // Stats
  const stats = {
    tagged: 0,
    byMethod: { id_stem: 0, keyword: 0, fallback: 0 },
    byGrade: {},
    emptyCorrectAnswer: [],
    emptyOptions: [],
    skippedGrade4Ch: 0,
  };

  for (const q of questions) {
    const topicId = q.topicId || '';

    // Skip ch-series and dh (Grade 4 curriculum) — already properly tagged
    if (topicId.startsWith('ch') || topicId === 'dh') {
      stats.skippedGrade4Ch++;
      continue;
    }

    // Extract grade from topicId (grade2 → 2)
    const gradeMatch = topicId.match(/^grade(\d+)$/);
    if (!gradeMatch) continue;
    const grade = parseInt(gradeMatch[1], 10);

    // Validate data quality
    if (!q.correctAnswer) {
      stats.emptyCorrectAnswer.push({ id: q.id, grade, source: q.source });
    }
    if (!q.options || q.options.length === 0) {
      stats.emptyOptions.push({ id: q.id, grade, source: q.source });
    }

    // Classify
    const { key, method } = classifyQuestion(q, grade, keywordRules);
    const oldSubTopic = q.subTopic;
    const gradeSubtopics = GRADE_SUBTOPICS[grade] || [];
    const label = gradeSubtopics.find(s => s.key === key)?.label || key;

    // Update subTopic to: "{label}" (human readable, contains the subTopicKey)
    q.subTopic = label;

    stats.tagged++;
    stats.byMethod[method]++;

    if (!stats.byGrade[grade]) stats.byGrade[grade] = {};
    if (!stats.byGrade[grade][key]) stats.byGrade[grade][key] = 0;
    stats.byGrade[grade][key]++;
  }

  // ─── Report ─────────────────────────────────────────────────────────────

  console.log('\n' + '='.repeat(70));
  console.log('  SEED DATA FIX REPORT');
  console.log('='.repeat(70));

  console.log(`\nSkipped (Grade 4 ch-series): ${stats.skippedGrade4Ch}`);
  console.log(`Tagged (Grades 2-9 pools):   ${stats.tagged}`);
  console.log(`  By ID stem:   ${stats.byMethod.id_stem}`);
  console.log(`  By keyword:   ${stats.byMethod.keyword}`);
  console.log(`  By fallback:  ${stats.byMethod.fallback}`);

  console.log('\n--- Distribution per grade ---');
  for (const grade of [2, 3, 5, 6, 7, 8, 9]) {
    const dist = stats.byGrade[grade] || {};
    const total = Object.values(dist).reduce((a, b) => a + b, 0);
    console.log(`\nGrade ${grade} (${total} questions):`);
    const subtopics = GRADE_SUBTOPICS[grade] || [];
    for (const { key, label } of subtopics) {
      const count = dist[key] || 0;
      const bar = '█'.repeat(Math.ceil(count / 10));
      console.log(`  ${label.padEnd(30)} ${String(count).padStart(4)}  ${bar}`);
    }
  }

  // Grade 4 pool (non-ch-series)
  if (stats.byGrade[4]) {
    const dist = stats.byGrade[4];
    const total = Object.values(dist).reduce((a, b) => a + b, 0);
    console.log(`\nGrade 4 pool (${total} questions):`);
    for (const [key, count] of Object.entries(dist).sort((a, b) => b[1] - a[1])) {
      console.log(`  ${key.padEnd(30)} ${String(count).padStart(4)}`);
    }
  }

  // Data quality issues
  console.log('\n--- DATA QUALITY ISSUES ---');

  const emptyAnsBySource = {};
  for (const { source } of stats.emptyCorrectAnswer) {
    emptyAnsBySource[source] = (emptyAnsBySource[source] || 0) + 1;
  }
  console.log(`\nEmpty correctAnswer: ${stats.emptyCorrectAnswer.length}`);
  for (const [src, cnt] of Object.entries(emptyAnsBySource).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${src}: ${cnt}`);
  }

  const emptyOptsBySource = {};
  for (const { source } of stats.emptyOptions) {
    emptyOptsBySource[source] = (emptyOptsBySource[source] || 0) + 1;
  }
  console.log(`\nEmpty options: ${stats.emptyOptions.length}`);
  for (const [src, cnt] of Object.entries(emptyOptsBySource).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${src}: ${cnt}`);
  }

  // Overlap: both empty
  const bothBroken = stats.emptyCorrectAnswer.filter(a =>
    stats.emptyOptions.some(o => o.id === a.id)
  );
  console.log(`\nBoth empty (answer + options): ${bothBroken.length}`);

  const totalBroken = new Set([
    ...stats.emptyCorrectAnswer.map(q => q.id),
    ...stats.emptyOptions.map(q => q.id),
  ]).size;
  console.log(`Total unusable questions: ${totalBroken}`);
  console.log(`Usable questions (non-G4-ch): ${stats.tagged - totalBroken}`);

  // ─── Write ──────────────────────────────────────────────────────────────

  if (DRY_RUN) {
    console.log('\n[DRY RUN] No changes written.');
  } else {
    console.log('\nWriting updated seed data...');
    fs.writeFileSync(SEED_PATH, JSON.stringify(data, null, 2), 'utf-8');
    console.log('Done! Updated', SEED_PATH);
  }

  console.log('\n' + '='.repeat(70));
  console.log('NEXT STEPS:');
  console.log('  1. Run: npx prisma db push  (if schema changed)');
  console.log('  2. Re-seed via /seed page');
  console.log('  3. Fill in empty correctAnswer values from IPM answer keys');
  console.log('  4. Fill in empty options for mega_final questions');
  console.log('='.repeat(70));
}

main();
