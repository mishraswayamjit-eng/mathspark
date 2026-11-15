import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the db module before importing mastery
vi.mock('../db', () => import('../__mocks__/db'));

import { calculateMastery, updateProgress } from '../mastery';
import { prisma } from '../__mocks__/db';

beforeEach(() => {
  vi.clearAllMocks();
});

describe('calculateMastery', () => {
  it('0 attempts → NotStarted', async () => {
    prisma.attempt.findMany.mockResolvedValue([]);
    const result = await calculateMastery('s1', 'ch11');
    expect(result).toBe('NotStarted');
  });

  it('8/10 correct → Mastered', async () => {
    const attempts = Array.from({ length: 10 }, (_, i) => ({
      isCorrect: i < 8,
    }));
    prisma.attempt.findMany.mockResolvedValue(attempts);
    const result = await calculateMastery('s1', 'ch11');
    expect(result).toBe('Mastered');
  });

  it('4/10 correct → Practicing', async () => {
    const attempts = Array.from({ length: 10 }, (_, i) => ({
      isCorrect: i < 4,
    }));
    prisma.attempt.findMany.mockResolvedValue(attempts);
    const result = await calculateMastery('s1', 'ch11');
    expect(result).toBe('Practicing');
  });

  it('3/10 correct → NotStarted', async () => {
    const attempts = Array.from({ length: 10 }, (_, i) => ({
      isCorrect: i < 3,
    }));
    prisma.attempt.findMany.mockResolvedValue(attempts);
    const result = await calculateMastery('s1', 'ch11');
    expect(result).toBe('NotStarted');
  });

  it('exact 80% threshold → Mastered', async () => {
    const attempts = Array.from({ length: 5 }, (_, i) => ({
      isCorrect: i < 4,
    }));
    prisma.attempt.findMany.mockResolvedValue(attempts);
    const result = await calculateMastery('s1', 'ch11');
    expect(result).toBe('Mastered');
  });
});

describe('updateProgress', () => {
  it('calls upsert with correct mastery + counts', async () => {
    // updateProgress reads everything in ONE batched prisma.$transaction:
    // [the last 10 attempts, the number attempted, the number correct].
    // (This test used to queue two attempt.findMany results, from before the
    // three reads were batched; the mocked $transaction then returned nothing.)
    prisma.$transaction.mockResolvedValue([
      Array.from({ length: 10 }, (_, i) => ({ isCorrect: i < 9 })),
      20,
      15,
    ]);
    prisma.progress.upsert.mockResolvedValue({});

    await updateProgress('s1', 'ch11');

    expect(prisma.progress.upsert).toHaveBeenCalledWith(
      expect.objectContaining({
        where: { studentId_topicId: { studentId: 's1', topicId: 'ch11' } },
        update: { attempted: 20, correct: 15, mastery: 'Mastered' },
        create: { studentId: 's1', topicId: 'ch11', attempted: 20, correct: 15, mastery: 'Mastered' },
      }),
    );
  });
});
