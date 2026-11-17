import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the db module before importing mastery
vi.mock('../db', () => import('../__mocks__/db'));

import { calculateMastery, lastTenFirstTries, updateProgress } from '../mastery';
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

  it('counts only the first try at a question on a day (review repeats are ignored)', async () => {
    // Newest first. Five questions missed in the morning, then all five got
    // right in the review round a few minutes later (the answers had been shown).
    const day = '2026-11-17T';
    const firstTries = ['q1', 'q2', 'q3', 'q4', 'q5'].map((questionId, i) => ({
      questionId, isCorrect: false, createdAt: new Date(`${day}04:0${i}:00.000Z`),
    }));
    const reviewTries = ['q1', 'q2', 'q3', 'q4', 'q5'].map((questionId, i) => ({
      questionId, isCorrect: true, createdAt: new Date(`${day}04:3${i}:00.000Z`),
    }));
    prisma.attempt.findMany.mockResolvedValue(reviewTries.reverse().concat(firstTries.reverse()));

    const result = await calculateMastery('s1', 'ch11');
    expect(result).toBe('NotStarted');
  });

  it('a try at the same question on a later day counts again', () => {
    const rows = [
      { questionId: 'q1', isCorrect: true, createdAt: new Date('2026-11-18T05:00:00.000Z') },
      { questionId: 'q1', isCorrect: false, createdAt: new Date('2026-11-17T05:00:00.000Z') },
    ];
    expect(lastTenFirstTries(rows)).toHaveLength(2);
  });

  it('the day changes at midnight in India, not in UTC', () => {
    // 18:00 UTC is 23:30 in India; 19:00 UTC is 00:30 the next day there.
    const rows = [
      { questionId: 'q1', isCorrect: true, createdAt: new Date('2026-11-17T19:00:00.000Z') },
      { questionId: 'q1', isCorrect: false, createdAt: new Date('2026-11-17T18:00:00.000Z') },
    ];
    expect(lastTenFirstTries(rows)).toHaveLength(2);
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
