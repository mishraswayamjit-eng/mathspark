import { PrismaClient } from '@prisma/client';
import { isAiQuestionsServeEnabled } from './llm/featureFlags';

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
 * Feature 5b kill-switch. When `AI_QUESTIONS_SERVE` is off (default), spread this
 * into a Question `where` clause to exclude `source='ai_generated'` questions.
 * When on, returns `{}` so authored questions can be served (still ranked last
 * by the adaptive picker and excluded from mock tests at their own call sites).
 */
export function aiSourceFilter(): { source?: { not: string } } {
  return isAiQuestionsServeEnabled() ? {} : { source: { not: 'ai_generated' } };
}
