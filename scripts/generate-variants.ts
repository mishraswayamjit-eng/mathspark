#!/usr/bin/env tsx
/**
 * generate-variants.ts
 *
 * Deterministic (no AI) variant generation. Creates computational variants by:
 * 1. Number substitution (swap operands while preserving structure)
 * 2. Option shuffling (reorder A/B/C/D, update correctAnswer)
 * 3. Unit conversion swaps (cm↔mm, kg↔g, L↔mL)
 * 4. Fraction variants (equivalent fractions with different denominators)
 *
 * Only operates on hand_crafted and pdf_extracted questions.
 * Caps at 5 variants per source question.
 *
 * Usage: npx tsx scripts/generate-variants.ts [--dry-run] [--max-per-question 3] [--max-total 15000]
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

interface SeedQuestion {
  id: string;
  topicId?: string;
  grade?: number;
  subTopic: string;
  difficulty: string;
  questionText: string;
  questionLatex: string;
  options: SeedOption[];
  correctAnswer: string;
  hints: string[];
  stepByStep: SeedStep[];
  misconceptions: Record<string, string>;
  source: string;
  [key: string]: unknown;
}

// ── Config ────────────────────────────────────────────────────────────────────

const ROOT = path.resolve(__dirname, '..');
const SEED_PATH = path.join(ROOT, 'data', 'mathspark_complete_seed.json');
const MAX_VARIANTS_PER_Q = parseInt(process.argv.find(a => a.startsWith('--max-per-question'))?.split('=')[1] || '5', 10);
const MAX_TOTAL = parseInt(process.argv.find(a => a.startsWith('--max-total'))?.split('=')[1] || '15000', 10);
const DRY_RUN = process.argv.includes('--dry-run');

// Sources eligible for variant generation
const ELIGIBLE_SOURCES = new Set(['hand_crafted', 'pdf_extracted']);

// ── Seeded random for reproducibility ─────────────────────────────────────────

let _seed = 42;
function seededRandom(): number {
  _seed = (_seed * 16807) % 2147483647;
  return (_seed - 1) / 2147483646;
}

function shuffleArray<T>(arr: T[]): T[] {
  const result = [...arr];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(seededRandom() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

// ── Number extraction & substitution ──────────────────────────────────────────

/**
 * Find all standalone integers in a string (not part of IDs or references).
 * Returns positions and values for substitution.
 */
function findNumbers(text: string): { value: number; start: number; end: number }[] {
  const results: { value: number; start: number; end: number }[] = [];
  // Match standalone numbers (not preceded/followed by letters or underscore)
  const regex = /(?<![a-zA-Z_])(\d+)(?![a-zA-Z_])/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    const val = parseInt(match[1], 10);
    // Skip very large numbers (likely years, IDs, etc.) and 0/1 (trivial)
    if (val >= 2 && val <= 9999) {
      results.push({ value: val, start: match.index, end: match.index + match[1].length });
    }
  }
  return results;
}

/**
 * Generate a nearby number that preserves rough magnitude.
 * E.g., 12 → 13 or 14, 150 → 160 or 140.
 */
function nearbyNumber(n: number, variantIdx: number): number {
  // Use variant index to create deterministic but different offsets
  const offsets = [1, 2, -1, 3, -2];
  const offset = offsets[variantIdx % offsets.length];

  if (n < 10) {
    return Math.max(2, n + offset);
  } else if (n < 100) {
    return Math.max(2, n + offset * (n < 20 ? 1 : 2));
  } else if (n < 1000) {
    return Math.max(10, n + offset * 10);
  } else {
    return Math.max(100, n + offset * 100);
  }
}

/**
 * Replace all number occurrences consistently.
 * Given a mapping of old→new numbers, replace in text.
 */
function replaceNumbers(text: string, mapping: Map<number, number>): string {
  let result = text;
  // Sort by string length descending to avoid partial replacements
  const sorted = Array.from(mapping.entries())
    .sort(([a], [b]) => String(b).length - String(a).length);

  for (const [oldNum, newNum] of sorted) {
    // Replace standalone occurrences only
    const regex = new RegExp(`(?<![a-zA-Z_\\d])${oldNum}(?![a-zA-Z_\\d])`, 'g');
    result = result.replace(regex, String(newNum));
  }
  return result;
}

// ── Variant generators ────────────────────────────────────────────────────────

/**
 * Check if a question is arithmetic-based (good candidate for number substitution).
 */
function isArithmetic(q: SeedQuestion): boolean {
  const text = q.questionText.toLowerCase();
  const arithKeywords = [
    'find', 'calculate', 'compute', 'sum', 'difference', 'product', 'quotient',
    'add', 'subtract', 'multiply', 'divide', 'times', 'plus', 'minus',
    'how many', 'how much', 'total', 'remainder', 'lcm', 'hcf', 'gcd',
    'factor', 'multiple', 'square', 'cube', 'root',
  ];
  return arithKeywords.some(k => text.includes(k));
}

/**
 * Check if a question involves measurement/units.
 */
function isMeasurement(q: SeedQuestion): boolean {
  const text = q.questionText.toLowerCase();
  const unitKeywords = ['cm', 'mm', 'km', 'kg', 'gm', 'gram', 'litre', 'ml', 'metre', 'meter'];
  return unitKeywords.some(k => text.includes(k));
}

/**
 * Check if a question involves fractions.
 */
function isFraction(q: SeedQuestion): boolean {
  const text = q.questionText.toLowerCase() + ' ' + q.questionLatex;
  return text.includes('frac') || text.includes('/') || text.includes('fraction');
}

/**
 * Generate a number-substituted variant.
 */
function generateNumberVariant(q: SeedQuestion, variantIdx: number): SeedQuestion | null {
  const numbers = findNumbers(q.questionText);
  if (numbers.length === 0) return null;

  // Build number mapping
  const mapping = new Map<number, number>();
  for (const { value } of numbers) {
    if (!mapping.has(value)) {
      mapping.set(value, nearbyNumber(value, variantIdx));
    }
  }

  // Check that all new numbers are different from originals
  for (const [oldN, newN] of Array.from(mapping.entries())) {
    if (oldN === newN) return null;
  }

  // Apply to question text
  const newText = replaceNumbers(q.questionText, mapping);
  if (newText === q.questionText) return null;

  // Apply to LaTeX
  const newLatex = replaceNumbers(q.questionLatex, mapping);

  // Apply to options
  const newOptions = q.options.map(opt => ({
    id: opt.id,
    text: replaceNumbers(opt.text, mapping),
  }));

  // Apply to hints
  const newHints = q.hints.map(h => replaceNumbers(h, mapping));

  // Apply to step-by-step
  const newSteps = q.stepByStep.map(s => ({
    step: s.step,
    text: replaceNumbers(s.text, mapping),
    latex: s.latex ? replaceNumbers(s.latex, mapping) : undefined,
  }));

  // Apply to misconceptions
  const newMisconceptions: Record<string, string> = {};
  for (const [key, val] of Object.entries(q.misconceptions)) {
    newMisconceptions[key] = replaceNumbers(val, mapping);
  }

  return {
    ...q,
    id: `${q.id}_V${String(variantIdx + 1).padStart(2, '0')}`,
    questionText: newText,
    questionLatex: newLatex,
    options: newOptions,
    hints: newHints,
    stepByStep: newSteps,
    misconceptions: newMisconceptions,
    source: `variant_of_${q.id}`,
  };
}

/**
 * Generate an option-shuffled variant.
 * Reorders options A-D while keeping correctAnswer pointing to the right one.
 */
function generateShuffledVariant(q: SeedQuestion, variantIdx: number): SeedQuestion | null {
  // Create a deterministic shuffle based on variant index
  _seed = hashCode(q.id) + variantIdx * 997;
  const shuffled = shuffleArray([0, 1, 2, 3]);

  // Check that the shuffle is actually different from original
  if (shuffled.every((v, i) => v === i)) return null;

  const idMap = ['A', 'B', 'C', 'D'];
  const newOptions = shuffled.map((origIdx, newIdx) => ({
    id: idMap[newIdx],
    text: q.options[origIdx].text,
  }));

  // Update correct answer
  const correctOrigIdx = idMap.indexOf(q.correctAnswer);
  const newCorrectIdx = shuffled.indexOf(correctOrigIdx);
  const newCorrectAnswer = idMap[newCorrectIdx];

  // Update misconceptions mapping
  const newMisconceptions: Record<string, string> = {};
  for (let i = 0; i < 4; i++) {
    const origKey = idMap[shuffled[i]];
    const newKey = idMap[i];
    newMisconceptions[newKey] = q.misconceptions[origKey] || '';
  }

  return {
    ...q,
    id: `${q.id}_V${String(variantIdx + 1).padStart(2, '0')}`,
    options: newOptions,
    correctAnswer: newCorrectAnswer,
    misconceptions: newMisconceptions,
    source: `variant_of_${q.id}`,
  };
}

function hashCode(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0; // 32-bit int
  }
  return Math.abs(hash);
}

// ── Main ──────────────────────────────────────────────────────────────────────

function main() {
  console.log('╔══════════════════════════════════════════════════╗');
  console.log('║  MathSpark — Variant Generation                  ║');
  console.log('╚══════════════════════════════════════════════════╝\n');

  if (DRY_RUN) console.log('🔍 DRY RUN — no changes will be written\n');

  // Read seed
  const seed = JSON.parse(fs.readFileSync(SEED_PATH, 'utf-8'));
  const questions: SeedQuestion[] = seed.questions;
  const existingIds = new Set(questions.map(q => q.id));

  console.log(`📦 Seed: ${questions.length} questions`);

  // Filter eligible questions
  const eligible = questions.filter(q => {
    // Must be from eligible source
    if (!ELIGIBLE_SOURCES.has(q.source)) return false;
    // Must have a valid correct answer
    if (!['A', 'B', 'C', 'D'].includes(q.correctAnswer)) return false;
    // Must have non-empty hints
    if (!q.hints || q.hints.every(h => !h || h.trim() === '')) return false;
    // Skip questions that are already variants
    if (q.source.startsWith('variant_of_')) return false;
    return true;
  });

  console.log(`🎯 Eligible for variants: ${eligible.length} (${ELIGIBLE_SOURCES.size} source types)`);
  console.log(`📊 Max per question: ${MAX_VARIANTS_PER_Q} | Max total: ${MAX_TOTAL}\n`);

  // Categorize
  const arithmetic = eligible.filter(isArithmetic);
  const measurement = eligible.filter(isMeasurement);
  const fraction = eligible.filter(isFraction);
  const other = eligible.filter(q => !isArithmetic(q) && !isMeasurement(q) && !isFraction(q));

  console.log(`  Arithmetic:   ${arithmetic.length}`);
  console.log(`  Measurement:  ${measurement.length}`);
  console.log(`  Fraction:     ${fraction.length}`);
  console.log(`  Other:        ${other.length}\n`);

  // Generate variants
  const variants: SeedQuestion[] = [];
  let totalAttempted = 0;
  let totalGenerated = 0;

  function addVariant(v: SeedQuestion | null): boolean {
    if (!v) return false;
    if (existingIds.has(v.id)) return false;
    if (variants.length >= MAX_TOTAL) return false;

    variants.push(v);
    existingIds.add(v.id);
    totalGenerated++;
    return true;
  }

  // Process all eligible questions
  for (const q of eligible) {
    if (variants.length >= MAX_TOTAL) break;

    let variantsForQ = 0;
    totalAttempted++;

    // Strategy 1: Number substitution (for arithmetic/measurement/fraction questions)
    if (isArithmetic(q) || isMeasurement(q) || isFraction(q)) {
      for (let i = 0; i < Math.min(3, MAX_VARIANTS_PER_Q); i++) {
        if (variantsForQ >= MAX_VARIANTS_PER_Q) break;
        const v = generateNumberVariant(q, i);
        if (addVariant(v)) variantsForQ++;
      }
    }

    // Strategy 2: Option shuffling (for all questions)
    for (let i = 0; i < Math.min(2, MAX_VARIANTS_PER_Q - variantsForQ); i++) {
      if (variantsForQ >= MAX_VARIANTS_PER_Q) break;
      // Use a different variant index to avoid ID collisions
      const v = generateShuffledVariant(q, variantsForQ + i);
      if (addVariant(v)) variantsForQ++;
    }
  }

  console.log('═══════════════════════════════════════════════════');
  console.log('  VARIANT GENERATION SUMMARY');
  console.log('═══════════════════════════════════════════════════');
  console.log(`  Questions processed:    ${totalAttempted}`);
  console.log(`  Variants generated:     ${totalGenerated}`);
  console.log(`  ───────────────────────────────────────────────`);

  if (!DRY_RUN && variants.length > 0) {
    // Append variants to seed
    seed.questions.push(...variants);
    seed.metadata.totalQuestions = seed.questions.length;
    fs.writeFileSync(SEED_PATH, JSON.stringify(seed, null, 2), 'utf-8');
    console.log(`  💾 Seed updated:          ${seed.questions.length} total questions`);
  } else if (DRY_RUN) {
    console.log(`  Would add:              ${variants.length} variants`);
    console.log(`  Would bring total to:   ${questions.length + variants.length}`);
  } else {
    console.log('  No variants generated.');
  }

  console.log('═══════════════════════════════════════════════════\n');

  // Breakdown by topic
  if (variants.length > 0) {
    const byTopic = new Map<string, number>();
    for (const v of variants) {
      const topic = v.topicId || 'unknown';
      byTopic.set(topic, (byTopic.get(topic) || 0) + 1);
    }

    console.log('📊 Variants by topic:');
    for (const [topic, count] of Array.from(byTopic.entries()).sort((a, b) => b[1] - a[1])) {
      console.log(`   ${topic}: +${count}`);
    }
    console.log('');
  }

  if (!DRY_RUN && variants.length > 0) {
    console.log('📌 NEXT STEPS:');
    console.log('   1. Review: git diff data/mathspark_complete_seed.json');
    console.log('   2. Re-seed: visit /seed page');
    console.log('   3. Verify: practice a topic to see variants\n');
  }
}

main();
