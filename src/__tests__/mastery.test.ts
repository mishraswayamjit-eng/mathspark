import { vi, describe, it, expect, beforeEach } from 'vitest';

vi.mock('@/lib/db', () => ({
  prisma: {
    attempt: { findMany: vi.fn() },
    progress: { upsert: vi.fn(), findUnique: vi.fn() },
  },
}));

import { prisma } from '@/lib/db';
import { calculateMastery, updateProgress } from '@/lib/mastery';

const mockAttemptFindMany = prisma.attempt.findMany as ReturnType<typeof vi.fn>;
const mockProgressUpsert = prisma.progress.upsert as ReturnType<typeof vi.fn>;
const mockProgressFindUnique = prisma.progress.findUnique as ReturnType<typeof vi.fn>;

// Build a fake attempt record
const attempt = (isCorrect: boolean, createdAt: Date = new Date()) => ({
  id: Math.random().toString(36).slice(2),
  isCorrect,
  createdAt,
  studentId: 'stu1',
  questionId: 'q1',
  selected: 'A',
  hintUsed: 0,
  timeTakenMs: 0,
});

beforeEach(() => {
  vi.clearAllMocks();
  vi.restoreAllMocks();
});

describe('calculateMastery', () => {
  it('returns NotStarted when there are no attempts', async () => {
    mockAttemptFindMany.mockResolvedValueOnce([]);
    const result = await calculateMastery('stu1', 'ch11');
    expect(result).toBe('NotStarted');
  });

  it('returns Mastered when >= 80% correct (8/10)', async () => {
    const attempts = [
      ...Array(8).fill(null).map(() => attempt(true)),
      ...Array(2).fill(null).map(() => attempt(false)),
    ];
    mockAttemptFindMany.mockResolvedValueOnce(attempts);
    const result = await calculateMastery('stu1', 'ch11');
    expect(result).toBe('Mastered');
  });

  it('returns Mastered when 10/10 correct', async () => {
    const attempts = Array(10).fill(null).map(() => attempt(true));
    mockAttemptFindMany.mockResolvedValueOnce(attempts);
    const result = await calculateMastery('stu1', 'ch11');
    expect(result).toBe('Mastered');
  });

  it('returns Practicing when >= 40% correct (4/10)', async () => {
    const attempts = [
      ...Array(4).fill(null).map(() => attempt(true)),
      ...Array(6).fill(null).map(() => attempt(false)),
    ];
    mockAttemptFindMany.mockResolvedValueOnce(attempts);
    const result = await calculateMastery('stu1', 'ch11');
    expect(result).toBe('Practicing');
  });

  it('returns Practicing at exactly 40% (4/10)', async () => {
    const attempts = [
      ...Array(4).fill(null).map(() => attempt(true)),
      ...Array(6).fill(null).map(() => attempt(false)),
    ];
    mockAttemptFindMany.mockResolvedValueOnce(attempts);
    const result = await calculateMastery('stu1', 'ch11');
    expect(result).toBe('Practicing');
  });

  it('returns NotStarted when < 40% correct (3/10)', async () => {
    const attempts = [
      ...Array(3).fill(null).map(() => attempt(true)),
      ...Array(7).fill(null).map(() => attempt(false)),
    ];
    mockAttemptFindMany.mockResolvedValueOnce(attempts);
    const result = await calculateMastery('stu1', 'ch11');
    expect(result).toBe('NotStarted');
  });

  it('returns NotStarted when 0/10 correct', async () => {
    const attempts = Array(10).fill(null).map(() => attempt(false));
    mockAttemptFindMany.mockResolvedValueOnce(attempts);
    const result = await calculateMastery('stu1', 'ch11');
    expect(result).toBe('NotStarted');
  });

  it('uses only last 10 attempts — recent 10 all correct → Mastered even if older 5 were wrong', async () => {
    // The implementation passes `take: 10` and `orderBy: createdAt desc` to Prisma,
    // so the mock should return only the 10 most recent attempts (already sliced by Prisma).
    // We simulate this by returning exactly 10 correct attempts (what Prisma would return).
    const recentTen = Array(10).fill(null).map(() => attempt(true));
    mockAttemptFindMany.mockResolvedValueOnce(recentTen);

    const result = await calculateMastery('stu1', 'ch11');

    expect(result).toBe('Mastered');

    // Verify the Prisma call had take:10 and desc order
    const call = mockAttemptFindMany.mock.calls[0][0];
    expect(call.take).toBe(10);
    expect(call.orderBy).toEqual({ createdAt: 'desc' });
  });

  it('queries with correct studentId and topicId', async () => {
    mockAttemptFindMany.mockResolvedValueOnce([]);
    await calculateMastery('stu-xyz', 'ch14');

    const call = mockAttemptFindMany.mock.calls[0][0];
    expect(call.where.studentId).toBe('stu-xyz');
    expect(call.where.question.topicId).toBe('ch14');
  });
});

describe('updateProgress', () => {
  it('upserts progress with correct mastery and counts', async () => {
    const allAttempts = [
      ...Array(8).fill(null).map(() => ({ isCorrect: true })),
      ...Array(2).fill(null).map(() => ({ isCorrect: false })),
    ];

    // calculateMastery call returns 8 correct → Mastered
    mockAttemptFindMany.mockResolvedValueOnce(
      allAttempts.map((a) => ({ ...a, id: Math.random().toString(), createdAt: new Date() })),
    );
    // all-attempts call (no take limit) also returns 10
    mockAttemptFindMany.mockResolvedValueOnce(allAttempts);
    // SRS: not previously mastered → start interval at 1
    mockProgressFindUnique.mockResolvedValueOnce({ mastery: 'Practicing', reviewInterval: 1 });
    mockProgressUpsert.mockResolvedValueOnce({});

    await updateProgress('stu1', 'ch11');

    expect(mockProgressUpsert).toHaveBeenCalledOnce();
    const upsertCall = mockProgressUpsert.mock.calls[0][0];
    expect(upsertCall.update.mastery).toBe('Mastered');
    expect(upsertCall.update.attempted).toBe(10);
    expect(upsertCall.update.correct).toBe(8);
    // SRS fields should be present
    expect(upsertCall.update.reviewInterval).toBe(1);
    expect(upsertCall.update.nextReviewAt).toBeInstanceOf(Date);
  });

  it('sets mastery=NotStarted and correct=0 when all attempts are wrong', async () => {
    const allWrong = Array(5).fill(null).map(() => ({ isCorrect: false }));
    const allWrongFull = allWrong.map((a) => ({
      ...a,
      id: Math.random().toString(),
      createdAt: new Date(),
    }));

    mockAttemptFindMany.mockResolvedValueOnce(allWrongFull);
    mockAttemptFindMany.mockResolvedValueOnce(allWrong);
    mockProgressUpsert.mockResolvedValueOnce({});

    await updateProgress('stu1', 'ch11');

    const upsertCall = mockProgressUpsert.mock.calls[0][0];
    expect(upsertCall.update.mastery).toBe('NotStarted');
    expect(upsertCall.update.correct).toBe(0);
    expect(upsertCall.update.attempted).toBe(5);
  });

  it('uses the correct composite key in the upsert where clause', async () => {
    mockAttemptFindMany.mockResolvedValue([]);
    mockProgressUpsert.mockResolvedValueOnce({});

    await updateProgress('stu-abc', 'ch06');

    const upsertCall = mockProgressUpsert.mock.calls[0][0];
    expect(upsertCall.where).toEqual({
      studentId_topicId: { studentId: 'stu-abc', topicId: 'ch06' },
    });
  });
});
