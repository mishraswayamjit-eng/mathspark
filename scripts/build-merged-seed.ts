/**
 * build-merged-seed.ts
 *
 * Merges the existing seed (data/mathspark_complete_seed.json) with the
 * new expanded question bank (MathSpark_Final_Complete.json) to produce
 * a single unified seed file with ~12,500+ questions.
 *
 * Usage:  npx tsx scripts/build-merged-seed.ts
 */

import * as fs from 'fs';
import * as path from 'path';

// ---------------------------------------------------------------------------
// Valid topic IDs (must match prisma/seed.ts and src/app/api/seed/route.ts)
// ---------------------------------------------------------------------------
const VALID_TOPIC_IDS = new Set([
  'ch01-05', 'ch06', 'ch07-08', 'ch09-10',
  'ch11', 'ch12', 'ch13', 'ch14', 'ch15', 'ch16',
  'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'dh',
  'grade2', 'grade3', 'grade4', 'grade5',
  'grade6', 'grade7', 'grade8', 'grade9',
]);

const VALID_ANSWERS = new Set(['A', 'B', 'C', 'D']);
const VALID_DIFFICULTIES = new Set(['Easy', 'Medium', 'Hard']);

// Remap bare chapter IDs to merged-range IDs
const TOPIC_ID_REMAP: Record<string, string> = {
  'ch01': 'ch01-05', 'ch02': 'ch01-05', 'ch03': 'ch01-05',
  'ch04': 'ch01-05', 'ch05': 'ch01-05',
  'ch07': 'ch07-08', 'ch08': 'ch07-08',
  'ch09': 'ch09-10', 'ch10': 'ch09-10',
};

// ---------------------------------------------------------------------------
// Derive topicId from question ID when not explicitly set
// ---------------------------------------------------------------------------
function inferTopicId(q: Record<string, unknown>): string {
  // 1. Explicit topicId field
  if (typeof q.topicId === 'string' && q.topicId) {
    const remapped = TOPIC_ID_REMAP[q.topicId] ?? q.topicId;
    if (VALID_TOPIC_IDS.has(remapped)) return remapped;
  }

  const id = String(q.id ?? '').toUpperCase();

  // 2. Q_DH_ prefix
  if (id.startsWith('Q_DH_')) return 'dh';

  // 3. PYQ_ prefix
  if (id.startsWith('PYQ_')) return 'grade4';

  // 4. EXT_G* or VAR_EXT_G* patterns
  const gradeMatch = id.match(/(?:EXT|VAR_EXT|VAR)_G(\d)/);
  if (gradeMatch) {
    const g = parseInt(gradeMatch[1], 10);
    if (g >= 2 && g <= 9) return `grade${g}`;
  }

  // 5. Q_CH* pattern
  const chMatch = id.match(/^Q_CH(\d+)_/);
  if (chMatch) {
    const n = parseInt(chMatch[1], 10);
    if (n >= 1 && n <= 5) return 'ch01-05';
    if (n === 6) return 'ch06';
    if (n === 7 || n === 8) return 'ch07-08';
    if (n === 9 || n === 10) return 'ch09-10';
    return `ch${String(n).padStart(2, '0')}`;
  }

  // 6. VAR_G* pattern (e.g., VAR_G9_vary_equation_V500)
  const varMatch = id.match(/^VAR_G(\d)/);
  if (varMatch) {
    const g = parseInt(varMatch[1], 10);
    if (g >= 2 && g <= 9) return `grade${g}`;
  }

  // 7. Infer from grade field
  const grade = typeof q.grade === 'number' ? q.grade : 0;
  if (grade >= 2 && grade <= 9) return `grade${grade}`;

  // 8. Default
  return 'ch11';
}

// ---------------------------------------------------------------------------
// Normalize a question to the seed format
// ---------------------------------------------------------------------------
interface SeedQuestion {
  id: string;
  topicId: string;
  subTopic: string;
  difficulty: string;
  questionText: string;
  questionLatex: string;
  options: Array<{ id: string; text: string }>;
  correctAnswer: string;
  hints: string[];
  stepByStep: unknown[];
  misconceptions: Record<string, string>;
  source: string;
  year?: number | null;
  questionNumber?: number | null;
  grade?: number;
}

function normalize(raw: Record<string, unknown>): SeedQuestion | null {
  const id = String(raw.id ?? '');
  if (!id) return null;

  const topicId = inferTopicId(raw);

  // Validate options
  const options = Array.isArray(raw.options) ? raw.options as Array<{ id: string; text: string }> : [];
  if (options.length < 4) return null; // need exactly 4 options

  // Validate correctAnswer
  const correctAnswer = String(raw.correctAnswer ?? '');
  if (!VALID_ANSWERS.has(correctAnswer)) return null;

  // Validate difficulty
  let difficulty = String(raw.difficulty ?? 'Medium');
  if (!VALID_DIFFICULTIES.has(difficulty)) difficulty = 'Medium';

  // Pad hints to 3
  const rawHints = Array.isArray(raw.hints) ? raw.hints.map(String) : [];
  const hints = [
    rawHints[0] ?? '',
    rawHints[1] ?? '',
    rawHints[2] ?? '',
  ];

  // stepByStep
  const stepByStep = Array.isArray(raw.stepByStep) ? raw.stepByStep : [];

  // misconceptions
  const rawMisc = (typeof raw.misconceptions === 'object' && raw.misconceptions !== null)
    ? raw.misconceptions as Record<string, string>
    : {};
  const misconceptions: Record<string, string> = {
    A: rawMisc['A'] ?? '',
    B: rawMisc['B'] ?? '',
    C: rawMisc['C'] ?? '',
    D: rawMisc['D'] ?? '',
  };

  return {
    id,
    topicId,
    subTopic: String(raw.subTopic ?? ''),
    difficulty,
    questionText: String(raw.questionText ?? ''),
    questionLatex: String(raw.questionLatex ?? ''),
    options: options.slice(0, 4),
    correctAnswer,
    hints,
    stepByStep,
    misconceptions,
    source: String(raw.source ?? 'auto_generated'),
    year: typeof raw.year === 'number' ? raw.year : null,
    questionNumber: typeof raw.questionNumber === 'number' ? raw.questionNumber : null,
    grade: typeof raw.grade === 'number' ? raw.grade : undefined,
  };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
function main() {
  const ROOT = path.resolve(__dirname, '..');

  // 1. Read existing seed
  const existingSeedPath = path.join(ROOT, 'data', 'mathspark_complete_seed.json');
  let existingQuestions: SeedQuestion[] = [];
  const existingIds = new Set<string>();

  if (fs.existsSync(existingSeedPath)) {
    console.log('Reading existing seed...');
    const existingData = JSON.parse(fs.readFileSync(existingSeedPath, 'utf-8'));
    const rawExisting = existingData.questions ?? existingData.data ?? [];
    console.log(`  Found ${rawExisting.length} questions in existing seed`);

    for (const q of rawExisting) {
      const normalized = normalize(q);
      if (normalized) {
        existingQuestions.push(normalized);
        existingIds.add(normalized.id);
      }
    }
    console.log(`  ${existingQuestions.length} valid questions kept`);
  } else {
    console.log('No existing seed found — starting fresh.');
  }

  // 2. Read new bank
  const newBankPath = path.join(ROOT, 'WOrksheets', 'New files', 'MathSpark_Final_Complete.json');
  if (!fs.existsSync(newBankPath)) {
    console.error(`ERROR: New bank not found at: ${newBankPath}`);
    process.exit(1);
  }

  console.log('\nReading new question bank...');
  const newData = JSON.parse(fs.readFileSync(newBankPath, 'utf-8'));
  const rawNew = newData.questions ?? [];
  console.log(`  Found ${rawNew.length} questions in new bank`);

  // 3. Merge — add new questions that don't already exist
  let added = 0;
  let skippedDup = 0;
  let skippedInvalid = 0;

  for (const q of rawNew) {
    const id = String(q.id ?? '');
    if (existingIds.has(id)) {
      skippedDup++;
      continue;
    }

    const normalized = normalize(q);
    if (!normalized) {
      skippedInvalid++;
      continue;
    }

    existingQuestions.push(normalized);
    existingIds.add(normalized.id);
    added++;
  }

  console.log(`\n--- Merge Summary ---`);
  console.log(`  Existing questions kept: ${existingQuestions.length - added}`);
  console.log(`  New questions added:     ${added}`);
  console.log(`  Skipped (duplicate ID):  ${skippedDup}`);
  console.log(`  Skipped (invalid data):  ${skippedInvalid}`);
  console.log(`  TOTAL:                   ${existingQuestions.length}`);

  // 4. Compute grade distribution
  const gradeDistribution: Record<string, number> = {};
  const topicDistribution: Record<string, number> = {};
  for (const q of existingQuestions) {
    const g = q.grade ?? (q.topicId.startsWith('grade') ? parseInt(q.topicId.replace('grade', ''), 10) : 4);
    gradeDistribution[String(g)] = (gradeDistribution[String(g)] ?? 0) + 1;
    topicDistribution[q.topicId] = (topicDistribution[q.topicId] ?? 0) + 1;
  }

  console.log('\n--- Grade Distribution ---');
  for (const [g, cnt] of Object.entries(gradeDistribution).sort(([a], [b]) => Number(a) - Number(b))) {
    console.log(`  Grade ${g}: ${cnt}`);
  }

  console.log('\n--- Topic Distribution ---');
  for (const [t, cnt] of Object.entries(topicDistribution).sort(([a], [b]) => a.localeCompare(b))) {
    console.log(`  ${t.padEnd(10)} ${String(cnt).padStart(5)}`);
  }

  // 5. Write merged output
  const output = {
    metadata: {
      app: 'MathSpark',
      totalQuestions: existingQuestions.length,
      mergedAt: new Date().toISOString(),
      sources: ['mathspark_complete_seed.json', 'MathSpark_Final_Complete.json'],
      grades: gradeDistribution,
      topicDistribution,
    },
    questions: existingQuestions,
  };

  console.log(`\nWriting merged seed to ${existingSeedPath}...`);
  fs.writeFileSync(existingSeedPath, JSON.stringify(output, null, 0)); // compact to save space
  const sizeMB = (fs.statSync(existingSeedPath).size / (1024 * 1024)).toFixed(1);
  console.log(`  Written! File size: ${sizeMB} MB`);
  console.log(`\n✅ Done! ${existingQuestions.length} questions ready for seeding.\n`);
}

main();
