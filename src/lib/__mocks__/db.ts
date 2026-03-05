import { vi } from 'vitest';

export const prisma = {
  attempt: {
    findMany: vi.fn(),
    count: vi.fn(),
    create: vi.fn(),
    groupBy: vi.fn(),
  },
  progress: {
    findUnique: vi.fn(),
    findMany: vi.fn(),
    upsert: vi.fn(),
    count: vi.fn(),
  },
  question: {
    findMany: vi.fn(),
  },
  student: {
    findUnique: vi.fn(),
    update: vi.fn(),
  },
  leagueMembership: {
    findFirst: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
  },
  league: {
    findMany: vi.fn(),
    create: vi.fn(),
  },
  usageLog: {
    upsert: vi.fn(),
  },
  weeklyAward: {
    createMany: vi.fn(),
    findMany: vi.fn(),
  },
  flashcardSession: {
    findMany: vi.fn(),
    create: vi.fn(),
  },
  $transaction: vi.fn(),
};

export const USABLE_QUESTION_FILTER = {
  correctAnswer: { not: '' },
  option1: { not: '' },
};
