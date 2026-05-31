import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

vi.mock('@/lib/db', () => ({
  prisma: {
    progress: { findUnique: vi.fn() },
    question: { findMany: vi.fn() },
  },
}));

import { prisma } from '@/lib/db';
import { getNextQuestion } from '@/lib/adaptive';

const mockProgress = prisma.progress.findUnique as ReturnType<typeof vi.fn>;
const mockFindMany = prisma.question.findMany as ReturnType<typeof vi.fn>;

const makeQuestion = (id: string, difficulty: string) => ({
  id,
  topicId: 'ch11',
  difficulty,
  subTopic: 'test',
  questionText: 'What is 2+2?',
  questionLatex: '',
  option1: '3',
  option2: '4',
  option3: '5',
  option4: '6',
  correctAnswer: 'B',
  hint1: '',
  hint2: '',
  hint3: '',
  stepByStep: '[]',
  misconceptionA: '',
  misconceptionB: '',
  misconceptionC: '',
  misconceptionD: '',
  source: 'hand_crafted',
});

beforeEach(() => {
  vi.clearAllMocks();
  // Pin to 0.5 → ZPD branch (roll < 0.70), so targetDiff === base every time.
  // This makes difficulty assertions deterministic regardless of the 70/20/10 roll.
  vi.spyOn(Math, 'random').mockReturnValue(0.5);
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('getNextQuestion — difficulty selection', () => {
  it('NotStarted mastery → returns an Easy question', async () => {
    mockProgress.mockResolvedValue(null);
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-easy-1', 'Easy')]);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result?.difficulty).toBe('Easy');
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Easy');
  });

  it('Mastered mastery → returns a Hard question', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Mastered' });
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-hard-1', 'Hard')]);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result?.difficulty).toBe('Hard');
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Hard');
  });

  it('Practicing mastery → returns a Medium question', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' });
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-med-1', 'Medium')]);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result?.difficulty).toBe('Medium');
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Medium');
  });
});

describe('getNextQuestion — streak adjustments', () => {
  it('3 consecutive wrong drops Practicing (Medium) to Easy', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' });
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-easy-2', 'Easy')]);

    const result = await getNextQuestion('stu1', 'ch11', [], 3, 0);

    expect(result?.difficulty).toBe('Easy');
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Easy');
  });

  it('3 consecutive wrong does not drop below Easy', async () => {
    mockProgress.mockResolvedValue(null); // NotStarted → base = Easy
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-easy-3', 'Easy')]);

    await getNextQuestion('stu1', 'ch11', [], 3, 0);

    // Easy − 1 clamps to Easy
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Easy');
  });

  it('5 consecutive right raises Practicing (Medium) to Hard', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' });
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-hard-2', 'Hard')]);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 5);

    expect(result?.difficulty).toBe('Hard');
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Hard');
  });

  it('5 consecutive right does not raise above Hard', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Mastered' }); // base = Hard
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-hard-3', 'Hard')]);

    await getNextQuestion('stu1', 'ch11', [], 0, 5);

    // Hard + 1 clamps to Hard
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Hard');
  });

  it('consecutiveWrong takes precedence over consecutiveRight when both threshold met', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' }); // base = Medium
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-easy-4', 'Easy')]);

    await getNextQuestion('stu1', 'ch11', [], 3, 5);

    // consecutiveWrong fires first → Medium drops to Easy
    expect(mockFindMany.mock.calls[0][0].where.difficulty).toBe('Easy');
  });
});

describe('getNextQuestion — fallback and null', () => {
  it('falls back to any unseen question when base difficulty pool is empty', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' }); // base = Medium
    const fallbackQ = makeQuestion('q-fallback', 'Easy');

    // ZPD branch (roll=0.5): skips non-base block → calls pickFromDifficulty(base)
    // First findMany (Medium difficulty) → empty pool
    mockFindMany.mockResolvedValueOnce([]);
    // Final fallback findMany (no difficulty filter) → returns a question
    mockFindMany.mockResolvedValueOnce([fallbackQ]);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result).not.toBeNull();
    expect(result?.id).toBe('q-fallback');
    expect(mockFindMany).toHaveBeenCalledTimes(2);
    // Second call has no difficulty filter
    expect(mockFindMany.mock.calls[1][0].where.difficulty).toBeUndefined();
  });

  it('returns null when all questions are seen', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' });
    mockFindMany.mockResolvedValue([]); // every pool is empty

    const result = await getNextQuestion('stu1', 'ch11', ['q1', 'q2'], 0, 0);

    expect(result).toBeNull();
  });
});

describe('getNextQuestion — seenIds exclusion', () => {
  it('passes seenIds as notIn filter to Prisma', async () => {
    mockProgress.mockResolvedValue(null);
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-new', 'Easy')]);

    const seenIds = ['q-seen-1', 'q-seen-2'];
    await getNextQuestion('stu1', 'ch11', seenIds, 0, 0);

    expect(mockFindMany.mock.calls[0][0].where.id).toEqual({ notIn: seenIds });
  });

  it('passes empty array when no seenIds provided', async () => {
    mockProgress.mockResolvedValue(null);
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-first', 'Easy')]);

    await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(mockFindMany.mock.calls[0][0].where.id).toEqual({ notIn: [] });
  });

  it('uses default empty seenIds when argument omitted', async () => {
    mockProgress.mockResolvedValue(null);
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-default', 'Easy')]);

    await getNextQuestion('stu1', 'ch11');

    expect(mockFindMany.mock.calls[0][0].where.id).toEqual({ notIn: [] });
  });
});

describe('getNextQuestion — topicId scoping', () => {
  it('filters questions by topicId', async () => {
    mockProgress.mockResolvedValue(null);
    mockFindMany.mockResolvedValueOnce([makeQuestion('q-topic', 'Easy')]);

    await getNextQuestion('stu1', 'ch14', [], 0, 0);

    expect(mockFindMany.mock.calls[0][0].where.topicId).toBe('ch14');
  });
});
