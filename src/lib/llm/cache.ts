import crypto from 'crypto';
import { prisma } from '@/lib/db';
import { logError } from '@/lib/logger';
import type { LlmFeature } from './types';

/** Deterministic cache key for an AiExplanation row. */
export function explanationCacheKey(
  feature: LlmFeature,
  refId: string,
  variant: string,
  grade: number,
): string {
  return crypto
    .createHash('sha256')
    .update(`${feature}|${refId}|${variant}|${grade}`)
    .digest('hex');
}

export interface GetOrCreateExplanationArgs {
  feature: LlmFeature;
  refId: string;
  variant?: string;
  grade: number;
  /** Produces the content + the model id that generated it. */
  generate: () => Promise<{ content: string; model: string }>;
}

export interface ExplanationResult {
  content: string;
  cached: boolean;
}

/**
 * Generate-once / cache / reuse for grounded LLM deliverables.
 *
 * On a cache hit, increments `hitCount` and returns the stored content.
 * On a miss, calls `generate()`, persists the result, and returns it.
 * Returns `null` if generation fails (caller falls back to static content).
 */
export async function getOrCreateExplanation(
  args: GetOrCreateExplanationArgs,
): Promise<ExplanationResult | null> {
  const variant = args.variant ?? '';
  const cacheKey = explanationCacheKey(args.feature, args.refId, variant, args.grade);

  // Cache lookup — a cache miss must never block the feature, so swallow read
  // errors and treat them as a miss.
  try {
    const existing = await prisma.aiExplanation.findUnique({ where: { cacheKey } });
    if (existing) {
      prisma.aiExplanation
        .update({ where: { cacheKey }, data: { hitCount: { increment: 1 } } })
        .catch((err) => logError('[llm.cache] hitCount increment failed', err));
      return { content: existing.content, cached: true };
    }
  } catch (err) {
    logError('[llm.cache] lookup failed', err);
  }

  let generated: { content: string; model: string };
  try {
    generated = await args.generate();
  } catch (err) {
    logError(`[llm.cache] generate failed for ${args.feature}:${args.refId}`, err);
    return null;
  }

  if (!generated.content.trim()) return null;

  // Persist. Use upsert to tolerate a race where two requests miss together.
  try {
    await prisma.aiExplanation.upsert({
      where: { cacheKey },
      create: {
        cacheKey,
        feature: args.feature,
        refId: args.refId,
        variant,
        grade: args.grade,
        content: generated.content,
        model: generated.model,
      },
      update: { hitCount: { increment: 1 } },
    });
  } catch (err) {
    logError('[llm.cache] persist failed', err);
  }

  return { content: generated.content, cached: false };
}
