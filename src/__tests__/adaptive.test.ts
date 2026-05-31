import { vi, describe, it, expect, beforeEach } from 'vitest';

vi.mock('@/lib/db', () => ({
  prisma: {
    progress: { findUnique: vi.fn() },
    question: { findFirst: vi.fn() },
  },
}));

import { prisma } from '@/lib/db';
import { getNextQuestion } from '@/lib/adaptive';

const mockProgress = prisma.progress.findUnique as ReturnType<typeof vi.fn>;
const mockFindFirst = prisma.question.findFirst as ReturnType<typeof vi.fn>;

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
  vi.restoreAllMocks();
});

describe('getNextQuestion — difficulty selection', () => {
  it('NotStarted mastery → returns an Easy question', async () => {
    mockProgress.mockResolvedValue(null); // no progress record → NotStarted
    const easyQ = makeQuestion('q-easy-1', 'Easy');
    mockFindFirst.mockResolvedValueOnce(easyQ);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result).not.toBeNull();
    expect(result?.difficulty).toBe('Easy');

    // Verify the Prisma call requested Easy difficulty
    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Easy');
  });

  it('Mastered mastery → returns a Hard question', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Mastered' });
    const hardQ = makeQuestion('q-hard-1', 'Hard');
    mockFindFirst.mockResolvedValueOnce(hardQ);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result).not.toBeNull();
    expect(result?.difficulty).toBe('Hard');

    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Hard');
  });

  it('Practicing mastery → returns a Medium question', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' });
    const medQ = makeQuestion('q-med-1', 'Medium');
    mockFindFirst.mockResolvedValueOnce(medQ);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result?.difficulty).toBe('Medium');
    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Medium');
  });
});

describe('getNextQuestion — streak adjustments', () => {
  it('3 consecutive wrong drops Practicing (Medium) to Easy', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' }); // base = Medium
    const easyQ = makeQuestion('q-easy-2', 'Easy');
    mockFindFirst.mockResolvedValueOnce(easyQ);

    const result = await getNextQuestion('stu1', 'ch11', [], 3, 0);

    expect(result?.difficulty).toBe('Easy');
    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Easy');
  });

  it('3 consecutive wrong does not drop below Easy', async () => {
    mockProgress.mockResolvedValue(null); // base = Easy (NotStarted)
    const easyQ = makeQuestion('q-easy-3', 'Easy');
    mockFindFirst.mockResolvedValueOnce(easyQ);

    const result = await getNextQuestion('stu1', 'ch11', [], 3, 0);

    // Easy - 1 clamps to Easy
    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Easy');
    expect(result?.difficulty).toBe('Easy');
  });

  it('5 consecutive right raises Practicing (Medium) to Hard', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' }); // base = Medium
    const hardQ = makeQuestion('q-hard-2', 'Hard');
    mockFindFirst.mockResolvedValueOnce(hardQ);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 5);

    expect(result?.difficulty).toBe('Hard');
    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Hard');
  });

  it('5 consecutive right does not raise above Hard', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Mastered' }); // base = Hard
    const hardQ = makeQuestion('q-hard-3', 'Hard');
    mockFindFirst.mockResolvedValueOnce(hardQ);

    await getNextQuestion('stu1', 'ch11', [], 0, 5);

    // Hard + 1 clamps to Hard
    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Hard');
  });

  it('consecutiveWrong takes precedence over consecutiveRight (wrong >= 3)', async () => {
    // Only one branch fires: the first condition that matches wins.
    // consecutiveWrong=3 fires first in the implementation.
    mockProgress.mockResolvedValue({ mastery: 'Practicing' }); // base = Medium
    const easyQ = makeQuestion('q-easy-4', 'Easy');
    mockFindFirst.mockResolvedValueOnce(easyQ);

    await getNextQuestion('stu1', 'ch11', [], 3, 5);

    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.difficulty).toBe('Easy');
  });
});

describe('getNextQuestion — fallback and null', () => {
  it('falls back to any unseen question when target difficulty is empty', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' }); // target = Medium
    const easyQ = makeQuestion('q-easy-fb', 'Easy');

    // First call (with difficulty filter) returns null
    mockFindFirst.mockResolvedValueOnce(null);
    // Second call (fallback, no difficulty filter) returns an Easy question
    mockFindFirst.mockResolvedValueOnce(easyQ);

    const result = await getNextQuestion('stu1', 'ch11', [], 0, 0);

    expect(result).not.toBeNull();
    expect(result?.id).toBe('q-easy-fb');
    expect(mockFindFirst).toHaveBeenCalledTimes(2);

    // Second call should NOT filter by difficulty
    const fallbackCall = mockFindFirst.mock.calls[1][0];
    expect(fallbackCall.where.difficulty).toBeUndefined();
  });

  it('returns null when all questions are seen (both calls return null)', async () => {
    mockProgress.mockResolvedValue({ mastery: 'Practicing' });
    mockFindFirst.mockResolvedValue(null); // both findFirst calls return null

    const result = await getNextQuestion('stu1', 'ch11', ['q1', 'q2', 'q3'], 0, 0);

    expect(result).toBeNull();
    expect(mockFindFirst).toHaveBeenCalledTimes(2);
  });
});

describe('getNextQuestion — seenIds exclusion', () => {
  it('passes seenIds as notIn filter to Prisma', async () => {
    mockProgress.mockResolvedValue(null); // NotStarted → Easy
    const q = makeQuestion('q-new', 'Easy');
    mockFindFirst.mockResolvedValueOnce(q);

    const seenIds = ['q-seen-1', 'q-seen-2'];
    await getNextQuestion('stu1', 'ch11', seenIds, 0, 0);

    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.id).toEqual({ notIn: seenIds });
  });

  it('passes empty array when no seenIds provided', async () => {
    mockProgress.mockResolvedValue(null);
    const q = makeQuestion('q-first', 'Easy');
    mockFindFirst.mockResolvedValueOnce(q);

    await getNextQuestion('stu1', 'ch11', [], 0, 0);

    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.id).toEqual({ notIn: [] });
  });

  it('uses default empty seenIds when argument omitted', async () => {
    mockProgress.mockResolvedValue(null);
    const q = makeQuestion('q-default', 'Easy');
    mockFindFirst.mockResolvedValueOnce(q);

    await getNextQuestion('stu1', 'ch11');

    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.id).toEqual({ notIn: [] });
  });
});

describe('getNextQuestion — topicId scoping', () => {
  it('filters questions by topicId', async () => {
    mockProgress.mockResolvedValue(null);
    const q = makeQuestion('q-topic', 'Easy');
    mockFindFirst.mockResolvedValueOnce(q);

    await getNextQuestion('stu1', 'ch14', [], 0, 0);

    const call = mockFindFirst.mock.calls[0][0];
    expect(call.where.topicId).toBe('ch14');
  });
});
