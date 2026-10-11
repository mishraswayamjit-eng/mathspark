import { PrismaClient } from '@prisma/client';
import { isAiQuestionsServeEnabled, isAiTextbookServeEnabled } from './llm/featureFlags';

// Prevent multiple PrismaClient instances in development (Next.js hot-reload)
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['error'] : [],
  });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

/**
 * Shared Prisma `where` clause that excludes broken questions
 * (empty correctAnswer or empty options). Spread into any Question.findMany().
 */
export const USABLE_QUESTION_FILTER = {
  questionText:  { not: '' },
  correctAnswer: { not: '' },
  option1:       { not: '' },
  option2:       { not: '' },
  option3:       { not: '' },
  option4:       { not: '' },
};

/**
 * Generated-content kill-switch. Spread into a Question `where` clause to exclude
 * generated sources unless their serve flag is on:
 *   - `ai_generated`  — excluded unless `AI_QUESTIONS_SERVE` (Feature 5b)
 *   - `ipm_textbook`  — excluded unless `AI_TEXTBOOK_SERVE` (textbook import)
 * Returns `{}` when both are enabled (nothing to exclude). Served rows are still
 * ranked below real sources by the adaptive picker and gated at mock call sites.
 */
export function aiSourceFilter(): { source?: { notIn: string[] } } {
  const excluded: string[] = [];
  if (!isAiQuestionsServeEnabled()) excluded.push('ai_generated');
  if (!isAiTextbookServeEnabled()) excluded.push('ipm_textbook');
  return excluded.length ? { source: { notIn: excluded } } : {};
}
