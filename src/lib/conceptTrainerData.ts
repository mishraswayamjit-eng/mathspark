import fs from 'fs';
import path from 'path';
import type { ConceptTrainer } from '@/types/conceptTrainer';

/**
 * Shared loader for static concept-trainer JSON (`data/concept-trainers/<slug>.json`).
 * Mirrors `lessonData.ts`: cached, slug-validated fs read. All content is
 * authored/computed offline — no runtime LLM.
 */

const cache = new Map<string, ConceptTrainer | null>();
export const TRAINER_SLUG_RE = /^[a-z0-9-]+$/;

/** Load a trainer's JSON, cached in-memory. Returns null if not found. */
export function loadTrainer(slug: string): ConceptTrainer | null {
  if (!TRAINER_SLUG_RE.test(slug)) return null;
  if (cache.has(slug)) return cache.get(slug) ?? null;

  const filePath = path.join(process.cwd(), 'data', 'concept-trainers', `${slug}.json`);
  if (!fs.existsSync(filePath)) {
    cache.set(slug, null);
    return null;
  }
  const data = JSON.parse(fs.readFileSync(filePath, 'utf-8')) as ConceptTrainer;
  cache.set(slug, data);
  return data;
}
