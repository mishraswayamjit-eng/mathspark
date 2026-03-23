#!/usr/bin/env tsx
/**
 * merge-questions.ts
 *
 * Reads all JSON files from data/extracted/, validates each question against
 * the seed schema, deduplicates, and merges into data/mathspark_complete_seed.json.
 *
 * Usage: npx tsx scripts/merge-questions.ts
 */

import * as fs from 'fs';
import * as path from 'path';

// ── Types ─────────────────────────────────────────────────────────────────────

interface SeedOption {
  id: string;
  text: string;
}

interface SeedStep {
  step: number;
  text: string;
  latex?: string;
}

interface ExtractedQuestion {
  id: string;
  topicId?: string;
  grade?: number;
  year?: number;
  questionNumber?: number;
  subTopic: string;
  difficulty: string;
  questionText: string;
  questionLatex?: string;
  options: SeedOption[];
  correctAnswer: string;
  hints: string[];
  stepByStep: SeedStep[];
  misconceptions: Record<string, string>;
  source?: string;
  flagged?: boolean;
  flagReason?: string;
  ocrConfidence?: string;
  originalText?: string;
  originalExercise?: string;
}

interface ExtractedFile {
  extractionMeta?: {
    sourceFile?: string;
    grade?: number;
    sourceType?: string;
    batch?: string;
    totalExtracted?: number;
    totalFlagged?: number;
  };
  questions: ExtractedQuestion[];
}

interface SeedFile {
  metadata: Record<string, unknown>;
  questions: Record<string, unknown>[];
}

// ── Constants ─────────────────────────────────────────────────────────────────

const VALID_TOPIC_IDS = new Set([
  'ch01-05', 'ch06', 'ch07-08', 'ch09-10',
  'ch11', 'ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17',
  'ch18', 'ch19', 'ch20', 'ch21', 'dh',
  'grade2', 'grade3', 'grade4', 'grade5', 'grade6', 'grade7', 'grade8', 'grade9',
]);

const VALID_DIFFICULTIES = new Set(['Easy', 'Medium', 'Hard']);
const VALID_ANSWERS = new Set(['A', 'B', 'C', 'D']);

const ROOT = path.resolve(__dirname, '..');
const EXTRACTED_DIR = path.join(ROOT, 'data', 'extracted');
const SEED_PATH = path.join(ROOT, 'data', 'mathspark_complete_seed.json');

// ── Validation ────────────────────────────────────────────────────────────────

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

function validateQuestion(q: ExtractedQuestion, existingIds: Set<string>, batchIds: Set<string>): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Required string fields
  if (!q.id || typeof q.id !== 'string') errors.push('Missing or invalid id');
  if (!q.subTopic || typeof q.subTopic !== 'string') errors.push('Missing subTopic');
  if (!q.questionText || typeof q.questionText !== 'string') errors.push('Missing questionText');

  // Difficulty
  if (!VALID_DIFFICULTIES.has(q.difficulty)) {
    errors.push(`Invalid difficulty: "${q.difficulty}" (must be Easy/Medium/Hard)`);
  }

  // Options: need exactly 4 with id A-D
  if (!Array.isArray(q.options) || q.options.length !== 4) {
    errors.push(`Expected 4 options, got ${q.options?.length ?? 0}`);
  } else {
    const optionIds = q.options.map(o => o.id);
    if (!['A', 'B', 'C', 'D'].every(id => optionIds.includes(id))) {
      errors.push('Options must have ids A, B, C, D');
    }
    for (const opt of q.options) {
      if (!opt.text || typeof opt.text !== 'string') {
        errors.push(`Option ${opt.id} has empty/missing text`);
      }
    }
  }

  // Correct answer
  if (!VALID_ANSWERS.has(q.correctAnswer)) {
    if (q.flagged) {
      warnings.push('Missing correctAnswer (flagged for review)');
    } else {
      errors.push(`Invalid correctAnswer: "${q.correctAnswer}" (must be A/B/C/D)`);
    }
  }

  // Hints: need 3 non-empty
  if (!Array.isArray(q.hints) || q.hints.length < 3) {
    errors.push(`Expected 3 hints, got ${q.hints?.length ?? 0}`);
  } else {
    const emptyHints = q.hints.filter(h => !h || h.trim() === '').length;
    if (emptyHints > 0 && !q.flagged) {
      warnings.push(`${emptyHints} empty hint(s)`);
    }
  }

  // Step-by-step
  if (!Array.isArray(q.stepByStep) || q.stepByStep.length === 0) {
    if (!q.flagged) {
      warnings.push('Empty stepByStep array');
    }
  }

  // Misconceptions
  if (!q.misconceptions || typeof q.misconceptions !== 'object' || Object.keys(q.misconceptions).length === 0) {
    if (!q.flagged) {
      warnings.push('Empty misconceptions object');
    }
  }

  // TopicId
  if (q.topicId && !VALID_TOPIC_IDS.has(q.topicId)) {
    errors.push(`Unknown topicId: "${q.topicId}"`);
  }

  // ID uniqueness
  if (existingIds.has(q.id)) {
    errors.push(`Duplicate ID (exists in seed): ${q.id}`);
  }
  if (batchIds.has(q.id)) {
    errors.push(`Duplicate ID (exists in current batch): ${q.id}`);
  }

  return { valid: errors.length === 0, errors, warnings };
}

// ── Fuzzy deduplication (Levenshtein) ─────────────────────────────────────────

function levenshteinSimilarity(a: string, b: string): number {
  const la = a.length;
  const lb = b.length;
  if (la === 0 || lb === 0) return 0;

  // Quick length check — if lengths differ by >30%, similarity < 0.7
  if (Math.abs(la - lb) / Math.max(la, lb) > 0.3) return 0;

  // For very long strings, compare normalized substrings to save memory
  const maxLen = 300;
  const sa = a.length > maxLen ? a.substring(0, maxLen) : a;
  const sb = b.length > maxLen ? b.substring(0, maxLen) : b;

  const matrix: number[][] = [];
  for (let i = 0; i <= sa.length; i++) {
    matrix[i] = [i];
    for (let j = 1; j <= sb.length; j++) {
      if (i === 0) {
        matrix[i][j] = j;
      } else {
        const cost = sa[i - 1] === sb[j - 1] ? 0 : 1;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j - 1] + cost,
        );
      }
    }
  }

  const distance = matrix[sa.length][sb.length];
  return 1 - distance / Math.max(sa.length, sb.length);
}

function normalizeText(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// ── Convert extracted format to seed format ───────────────────────────────────

function toSeedFormat(q: ExtractedQuestion): Record<string, unknown> {
  const topicId = q.topicId || inferTopicId(q);

  const seedQ: Record<string, unknown> = {
    id: q.id,
    subTopic: q.subTopic,
    difficulty: q.difficulty,
    questionText: q.questionText,
    questionLatex: q.questionLatex || '',
    options: q.options,
    correctAnswer: q.correctAnswer,
    hints: q.hints,
    stepByStep: q.stepByStep,
    misconceptions: q.misconceptions,
    source: q.source || 'pdf_extracted',
  };

  // Preserve extra fields that exist in the seed format
  if (q.topicId) seedQ.topicId = topicId;
  if (q.grade) seedQ.grade = q.grade;
  if (q.year) seedQ.year = q.year;
  if (q.questionNumber) seedQ.questionNumber = q.questionNumber;

  return seedQ;
}

function inferTopicId(q: ExtractedQuestion): string {
  if (q.topicId) return q.topicId;

  // Try to infer from ID prefix
  const id = q.id.toUpperCase();
  const gradeMatch = id.match(/G(\d)/);
  if (gradeMatch) {
    const g = parseInt(gradeMatch[1], 10);
    if (g >= 2 && g <= 9) return `grade${g}`;
  }

  // Try from grade field
  if (q.grade && q.grade >= 2 && q.grade <= 9 && q.grade !== 4) {
    return `grade${q.grade}`;
  }

  return 'grade4'; // default
}

// ── Main ──────────────────────────────────────────────────────────────────────

function main() {
  console.log('╔══════════════════════════════════════════════════╗');
  console.log('║  MathSpark — Merge & Validate Extracted Questions ║');
  console.log('╚══════════════════════════════════════════════════╝\n');

  // 1. Read seed file
  if (!fs.existsSync(SEED_PATH)) {
    console.error(`❌ Seed file not found: ${SEED_PATH}`);
    process.exit(1);
  }

  const seed: SeedFile = JSON.parse(fs.readFileSync(SEED_PATH, 'utf-8'));
  const existingIds = new Set(seed.questions.map((q: Record<string, unknown>) => q.id as string));
  const existingTexts = new Map<string, string>(); // normalized text → id
  for (const q of seed.questions) {
    const norm = normalizeText(q.questionText as string);
    existingTexts.set(norm, q.id as string);
  }

  console.log(`📦 Seed file: ${seed.questions.length} existing questions`);
  console.log(`📁 Looking in: ${EXTRACTED_DIR}\n`);

  // 2. Find JSON files in extracted/
  if (!fs.existsSync(EXTRACTED_DIR)) {
    console.error(`❌ Extracted directory not found: ${EXTRACTED_DIR}`);
    console.log('   Create it and place JSON files from claude.ai there.');
    process.exit(1);
  }

  const jsonFiles = fs.readdirSync(EXTRACTED_DIR)
    .filter(f => f.endsWith('.json'))
    .sort();

  if (jsonFiles.length === 0) {
    console.log('📭 No JSON files found in data/extracted/');
    console.log('   Upload PDFs to claude.ai, save the output JSON here.');
    process.exit(0);
  }

  console.log(`📄 Found ${jsonFiles.length} JSON file(s):\n`);

  // 3. Process each file
  let totalAdded = 0;
  let totalSkipped = 0;
  let totalFlagged = 0;
  let totalDuplicates = 0;
  let totalErrors = 0;
  let totalEnriched = 0;
  const batchIds = new Set<string>();
  const allNewQuestions: Record<string, unknown>[] = [];

  for (const file of jsonFiles) {
    const filePath = path.join(EXTRACTED_DIR, file);
    console.log(`── ${file} ──────────────────────────────────────`);

    let data: ExtractedFile;
    try {
      const raw = fs.readFileSync(filePath, 'utf-8');
      data = JSON.parse(raw);
    } catch (err) {
      console.log(`  ❌ Failed to parse JSON: ${(err as Error).message}`);
      totalErrors++;
      continue;
    }

    // Handle both formats: {questions: [...]} and bare [...]
    const questions: ExtractedQuestion[] = Array.isArray(data) ? data : data.questions;
    if (!Array.isArray(questions)) {
      console.log('  ❌ No "questions" array found');
      totalErrors++;
      continue;
    }

    if (data.extractionMeta) {
      const m = data.extractionMeta;
      console.log(`  Source: ${m.sourceFile || '?'} | Grade: ${m.grade || '?'} | Type: ${m.sourceType || '?'}`);
    }
    console.log(`  Questions in file: ${questions.length}`);

    let fileAdded = 0;
    let fileSkipped = 0;
    let fileFlagged = 0;
    let fileDuplicates = 0;
    let fileEnriched = 0;

    for (const q of questions) {
      // Check if this is an enrichment of an existing question
      const isEnrichment = existingIds.has(q.id);

      if (isEnrichment) {
        // Enrichment mode: update existing question in-place
        if (!q.correctAnswer || !VALID_ANSWERS.has(q.correctAnswer)) {
          console.log(`  ⚠ Enrichment for ${q.id}: still missing correctAnswer, skipping`);
          fileSkipped++;
          continue;
        }

        // Find and update the existing question in seed
        const existingIdx = seed.questions.findIndex((sq: Record<string, unknown>) => sq.id === q.id);
        if (existingIdx !== -1) {
          const existing = seed.questions[existingIdx] as Record<string, unknown>;
          // Only update fields that were previously empty
          if (!existing.correctAnswer) existing.correctAnswer = q.correctAnswer;
          if (q.hints && q.hints.some(h => h.trim() !== '')) existing.hints = q.hints;
          if (q.stepByStep && q.stepByStep.length > 0) existing.stepByStep = q.stepByStep;
          if (q.misconceptions && Object.keys(q.misconceptions).length > 0) existing.misconceptions = q.misconceptions;
          if (q.questionLatex) existing.questionLatex = q.questionLatex;
          if (q.subTopic && q.subTopic !== existing.subTopic) existing.subTopic = q.subTopic;
          fileEnriched++;
        }
        continue;
      }

      // Validate new question
      const result = validateQuestion(q, existingIds, batchIds);

      if (!result.valid) {
        console.log(`  ❌ ${q.id}: ${result.errors.join('; ')}`);
        fileSkipped++;
        continue;
      }

      if (result.warnings.length > 0) {
        console.log(`  ⚠ ${q.id}: ${result.warnings.join('; ')}`);
      }

      // Flagged questions (OCR/uncertain)
      if (q.flagged) {
        console.log(`  🚩 ${q.id}: FLAGGED — ${q.flagReason || 'no reason given'}`);
        fileFlagged++;
        // Still add flagged questions but mark them
      }

      // Fuzzy dedup against existing seed
      const normText = normalizeText(q.questionText);
      let isDuplicate = false;

      // Exact match
      if (existingTexts.has(normText)) {
        console.log(`  🔄 ${q.id}: Exact duplicate of ${existingTexts.get(normText)}`);
        isDuplicate = true;
      }

      // Fuzzy match (only check if not exact duplicate — expensive operation)
      if (!isDuplicate) {
        for (const [existingNorm, existingId] of Array.from(existingTexts.entries())) {
          // Quick length check first
          if (Math.abs(normText.length - existingNorm.length) > normText.length * 0.2) continue;
          const sim = levenshteinSimilarity(normText, existingNorm);
          if (sim > 0.9) {
            console.log(`  🔄 ${q.id}: ~${(sim * 100).toFixed(0)}% similar to ${existingId}`);
            isDuplicate = true;
            break;
          }
        }
      }

      if (isDuplicate) {
        fileDuplicates++;
        continue;
      }

      // Add to batch
      const seedQ = toSeedFormat(q);
      allNewQuestions.push(seedQ);
      batchIds.add(q.id);
      existingIds.add(q.id);
      existingTexts.set(normText, q.id);
      fileAdded++;
    }

    console.log(`  ✅ Added: ${fileAdded} | ♻ Enriched: ${fileEnriched} | 🔄 Dupes: ${fileDuplicates} | ⏭ Skipped: ${fileSkipped} | 🚩 Flagged: ${fileFlagged}\n`);
    totalAdded += fileAdded;
    totalEnriched += fileEnriched;
    totalDuplicates += fileDuplicates;
    totalSkipped += fileSkipped;
    totalFlagged += fileFlagged;
  }

  // 4. Merge into seed
  if (allNewQuestions.length > 0 || totalEnriched > 0) {
    seed.questions.push(...allNewQuestions);

    // Update metadata
    seed.metadata.totalQuestions = seed.questions.length;

    // Write back
    fs.writeFileSync(SEED_PATH, JSON.stringify(seed, null, 2), 'utf-8');
    console.log(`💾 Seed file updated: ${seed.questions.length} total questions\n`);
  }

  // 5. Print summary
  console.log('═══════════════════════════════════════════════════');
  console.log('  MERGE SUMMARY');
  console.log('═══════════════════════════════════════════════════');
  console.log(`  ✅ New questions added:    ${totalAdded}`);
  console.log(`  ♻  Existing enriched:      ${totalEnriched}`);
  console.log(`  🔄 Duplicates skipped:     ${totalDuplicates}`);
  console.log(`  ⏭  Validation failures:    ${totalSkipped}`);
  console.log(`  🚩 Flagged (needs review): ${totalFlagged}`);
  console.log(`  ❌ File errors:             ${totalErrors}`);
  console.log(`  ───────────────────────────────────────────────`);
  console.log(`  📦 Seed total:             ${seed.questions.length}`);
  console.log('═══════════════════════════════════════════════════\n');

  if (totalFlagged > 0) {
    console.log('💡 TIP: Review flagged questions manually before re-seeding.');
    console.log('   They have been added but may have uncertain answers.\n');
  }

  if (totalAdded > 0 || totalEnriched > 0) {
    console.log('📌 NEXT STEPS:');
    console.log('   1. Review the changes: git diff data/mathspark_complete_seed.json');
    console.log('   2. Re-seed the database: visit /seed page or run prisma db seed');
    console.log('   3. Verify in-app: practice a topic to see new questions\n');
  }
}

main();
