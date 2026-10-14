import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the db module
vi.mock('../db', () => import('../__mocks__/db'));

import { getNextQuestion } from '../adaptive';
import { prisma } from '../__mocks__/db';

beforeEach(() => {
  vi.clearAllMocks();
});

function makeQuestion(id: string, difficulty: string, source = 'auto_generated', subTopic = 'basics') {
  return { id, topicId: 'ch11', subTopic, difficulty, source };
}

describe('getNextQuestion', () => {
  it('returns a question from the pool', async () => {
    prisma.question.findMany.mockResolvedValue([
      makeQuestion('q1', 'Easy'),
      makeQuestion('q2', 'Medium'),
    ]);
    prisma.attempt.findMany
      .mockResolvedValueOnce([]) // session attempts
      .mockResolvedValueOnce([]); // misconception attempts
    prisma.progress.findUnique.mockResolvedValue(null);

    const result = await getNextQuestion('s1', 'ch11');
    expect(result).not.toBeNull();
    expect(['q1', 'q2']).toContain(result!.id);
  });

  it('NotStarted mastery → predominantly Easy questions', async () => {
    const questions = [
      makeQuestion('q1', 'Easy'),
      makeQuestion('q2', 'Easy'),
      makeQuestion('q3', 'Easy'),
      makeQuestion('q4', 'Medium'),
    ];
    prisma.question.findMany.mockResolvedValue(questions);
    prisma.attempt.findMany
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([]);
    prisma.progress.findUnique.mockResolvedValue(null);

    // Run multiple times to verify trend
    let easyCount = 0;
    for (let i = 0; i < 20; i++) {
      const result = await getNextQuestion('s1', 'ch11');
      if (result?.difficulty === 'Easy') easyCount++;
    }
    // With 80/20 weighting and 3 easy vs 1 medium, should be mostly easy
    expect(easyCount).toBeGreaterThan(10);
  });

  it('Mastered mastery → predominantly Hard questions returned', async () => {
    const questions = [
      makeQuestion('q1', 'Medium'),
      makeQuestion('q2', 'Hard'),
      makeQuestion('q3', 'Hard'),
      makeQuestion('q4', 'Hard'),
    ];
    prisma.question.findMany.mockResolvedValue(questions);
    prisma.attempt.findMany
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([]);
    prisma.progress.findUnique.mockResolvedValue({ mastery: 'Mastered' });

    let hardCount = 0;
    for (let i = 0; i < 20; i++) {
      const result = await getNextQuestion('s1', 'ch11');
      if (result?.difficulty === 'Hard') hardCount++;
    }
    expect(hardCount).toBeGreaterThan(10);
  });

  it('excludes already-seen questions', async () => {
    prisma.question.findMany.mockResolvedValue([
      makeQuestion('q1', 'Easy'),
      makeQuestion('q2', 'Easy'),
    ]);
    prisma.attempt.findMany
      .mockResolvedValueOnce([{ questionId: 'q1', isCorrect: true }])
      .mockResolvedValueOnce([]);
    prisma.progress.findUnique.mockResolvedValue(null);

    const result = await getNextQuestion('s1', 'ch11');
    expect(result?.id).toBe('q2');
  });

  it('prefers hand_crafted over auto_generated', async () => {
    prisma.question.findMany.mockResolvedValue([
      makeQuestion('q1', 'Easy', 'auto_generated'),
      makeQuestion('q2', 'Easy', 'hand_crafted'),
    ]);
    prisma.attempt.findMany
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([]);
    prisma.progress.findUnique.mockResolvedValue(null);

    let handCraftedCount = 0;
    for (let i = 0; i < 20; i++) {
      const result = await getNextQuestion('s1', 'ch11');
      if (result?.id === 'q2') handCraftedCount++;
    }
    // hand_crafted should always be picked when both available at same difficulty
    expect(handCraftedCount).toBe(20);
  });

  it('returns null when pool is exhausted', async () => {
    prisma.question.findMany.mockResolvedValue([
      makeQuestion('q1', 'Easy'),
    ]);
    prisma.attempt.findMany
      .mockResolvedValueOnce([{ questionId: 'q1', isCorrect: true }])
      .mockResolvedValueOnce([]);
    prisma.progress.findUnique.mockResolvedValue(null);

    const result = await getNextQuestion('s1', 'ch11', ['q1']);
    expect(result).toBeNull();
  });

  it('3 wrong in a row → drops difficulty', async () => {
    prisma.question.findMany.mockResolvedValue([
      makeQuestion('q1', 'Easy'),
      makeQuestion('q2', 'Medium'),
      makeQuestion('q3', 'Hard'),
    ]);
    prisma.attempt.findMany
      .mockResolvedValueOnce([
        { questionId: 'a', isCorrect: false },
        { questionId: 'b', isCorrect: false },
        { questionId: 'c', isCorrect: false },
      ])
      .mockResolvedValueOnce([]);
    prisma.progress.findUnique.mockResolvedValue({ mastery: 'Practicing' });

    let easyCount = 0;
    for (let i = 0; i < 20; i++) {
      const result = await getNextQuestion('s1', 'ch11');
      if (result?.difficulty === 'Easy') easyCount++;
    }
    // After 3 wrong, difficulty should shift towards easy
    expect(easyCount).toBeGreaterThan(5);
  });

  it('whole-grade keyed practice rotates away from the over-served sub-topic', async () => {
    // Served pool is tagged with a DIFFERENT sub-topic than the skewed one, so a
    // non-null pick can only come from a less-served key → proves rotation.
    prisma.question.findMany.mockResolvedValue([
      { id: 'm1', topicId: 'grade5', subTopic: 'Grade 5 — Multiplication & Division', difficulty: 'Easy', source: 'auto_generated' },
    ]);
    // Default [] covers every session/misconception read inside pickForSubtopic
    // (rotation may probe several keys before one yields a question).
    prisma.attempt.findMany
      .mockResolvedValue([])
      // 1st call: rotation pre-query → today's attempts all skewed to place value
      .mockResolvedValueOnce([
        { question: { subTopic: 'Grade 5 — Numbers (place value)' } },
        { question: { subTopic: 'Grade 5 — Numbers (place value)' } },
        { question: { subTopic: 'Grade 5 — Numbers (place value)' } },
      ]);
    prisma.progress.findUnique.mockResolvedValue(null);

    const result = await getNextQuestion('s1', 'grade5');
    expect(result).not.toBeNull();
    // Rotation must not land on the over-served 'place value' key.
    expect(result!.subTopic.toLowerCase()).not.toContain('place value');
    expect(result!.id).toBe('m1');
  });

  it('5 right in a row → raises difficulty', async () => {
    prisma.question.findMany.mockResolvedValue([
      makeQuestion('q1', 'Easy'),
      makeQuestion('q2', 'Medium'),
      makeQuestion('q3', 'Hard'),
    ]);
    prisma.attempt.findMany
      .mockResolvedValueOnce([
        { questionId: 'a', isCorrect: true },
        { questionId: 'b', isCorrect: true },
        { questionId: 'c', isCorrect: true },
        { questionId: 'd', isCorrect: true },
        { questionId: 'e', isCorrect: true },
      ])
      .mockResolvedValueOnce([]);
    prisma.progress.findUnique.mockResolvedValue({ mastery: 'Practicing' });

    let hardCount = 0;
    for (let i = 0; i < 20; i++) {
      const result = await getNextQuestion('s1', 'ch11');
      if (result?.difficulty === 'Hard') hardCount++;
    }
    // After 5 right, difficulty should shift towards hard
    expect(hardCount).toBeGreaterThan(5);
  });
});
