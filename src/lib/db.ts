import { PrismaClient } from '@prisma/client';

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
  correctAnswer: { not: '' },
  option1:       { not: '' },
};
