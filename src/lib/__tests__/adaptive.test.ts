import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the db module
vi.mock('../db', () => import('../__mocks__/db'));

import { getNextQuestion, getNextQuestionWithLadder } from '../adaptive';
import { prisma } from '../__mocks__/db';

beforeEach(() => {
  vi.clearAllMocks();
});

function makeQuestion(id: string, difficulty: string, source = 'auto_generated', subTopic = 'basics') {
  return { id, topicId: 'ch11', subTopic, difficulty, source };
}

/**
 * For tests that call getNextQuestion many times. Each call reads attempts
 * twice (the session, then the misconception-tagged ones), so a queue of two
 * `mockResolvedValueOnce` values only covers the FIRST call: every later call
 * got `undefined` and threw. This answers every call, telling the two reads
 * apart by their `where`.
 */
function mockAttemptReads(session: Array<{ questionId: string; isCorrect: boolean }>) {
  prisma.attempt.findMany.mockImplementation(
    (args?: { where?: { misconceptionType?: unknown } }) =>
      Promise.resolve(args && args.where && args.where.misconceptionType ? [] : session),
  );
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
    mockAttemptReads([]);
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
    mockAttemptReads([]);
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
    mockAttemptReads([]);
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
    mockAttemptReads([
      { questionId: 'a', isCorrect: false },
      { questionId: 'b', isCorrect: false },
      { questionId: 'c', isCorrect: false },
    ]);
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
    mockAttemptReads([
      { questionId: 'a', isCorrect: true },
      { questionId: 'b', isCorrect: true },
      { questionId: 'c', isCorrect: true },
      { questionId: 'd', isCorrect: true },
      { questionId: 'e', isCorrect: true },
    ]);
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

// ── Topic ladder: focused practice on one topic of a keyed grade ─────────────

const HCF = 'Grade 5 — HCF and LCM';
const GEN = 'variant_generator_phase1';
const REAL = 'g5_final_2019';

interface LadderRow {
  id: string;
  topicId: string;
  subTopic: string;
  difficulty: string;
  source: string;
}

function hcfQuestion(id: string, difficulty: string, source: string = GEN, subTopic: string = HCF): LadderRow {
  return { id, topicId: 'grade5', subTopic, difficulty, source };
}

/** Two Easy, one Medium, one Hard, and three real paper questions. */
function hcfPool(): LadderRow[] {
  return [
    hcfQuestion('e1', 'Easy'),
    hcfQuestion('e2', 'Easy'),
    hcfQuestion('m1', 'Medium'),
    hcfQuestion('h1', 'Hard'),
    hcfQuestion('x1', 'Medium', REAL),
    hcfQuestion('x2', 'Medium', REAL),
    hcfQuestion('x3', 'Medium', REAL),
  ];
}

interface LadderAnswer {
  questionId: string;
  isCorrect: boolean;
  question: { subTopic: string; difficulty: string; source: string };
}

function hcfAnswer(questionId: string, difficulty: string, isCorrect: boolean, source: string = GEN): LadderAnswer {
  return { questionId, isCorrect, question: { subTopic: HCF, difficulty, source } };
}

/** `n` right answers on earlier questions (not in the pool) of one difficulty. */
function hcfRights(prefix: string, difficulty: string, n: number): LadderAnswer[] {
  const out: LadderAnswer[] = [];
  for (let i = 1; i <= n; i++) out.push(hcfAnswer(prefix + i, difficulty, true));
  return out;
}

/**
 * The ladder path reads: the topic's questions (light), the child's answers on
 * the topic, the child's last 10 answers in the grade (`take: 10`), then the
 * chosen question in full.
 */
function mockLadderReads(pool: LadderRow[], answers: LadderAnswer[], earlier: boolean[] = []) {
  prisma.question.findMany.mockResolvedValue(pool);
  prisma.question.findUnique.mockImplementation((args: { where: { id: string } }) =>
    Promise.resolve(pool.filter((row) => row.id === args.where.id)[0] ?? null),
  );
  prisma.attempt.findMany.mockImplementation((args?: { take?: number }) =>
    Promise.resolve(args && args.take === 10 ? earlier.map((ok) => ({ isCorrect: ok })) : answers),
  );
}

describe('getNextQuestionWithLadder', () => {
  it('starts a topic on Warm-up with an Easy question and reports the ladder', async () => {
    mockLadderReads(hcfPool(), []);

    const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'hcf');
    expect(picked.question).not.toBeNull();
    expect(picked.question!.difficulty).toBe('Easy');
    expect(picked.ladder).not.toBeNull();
    expect(picked.ladder!.topicLabel).toBe('HCF & LCM');
    expect(picked.ladder!.current).toBe(0);
    expect(picked.ladder!.got).toBe(0);
    expect(picked.ladder!.needed).toBe(3);
    expect(picked.ladder!.steps.map((s) => s.label)).toEqual(['Warm-up', 'Build', 'Challenge', 'Real exam']);
  });

  it('getNextQuestion returns the same pick without the ladder', async () => {
    mockLadderReads(hcfPool(), hcfRights('old-e', 'Easy', 3));

    const question = await getNextQuestion('s1', 'grade5', [], 'hcf');
    expect(question!.id).toBe('m1');
  });

  it('moves to Medium once three Warm-up questions are right', async () => {
    mockLadderReads(hcfPool(), hcfRights('old-e', 'Easy', 3));

    const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'hcf');
    expect(picked.question!.id).toBe('m1');
    expect(picked.ladder!.current).toBe(1);
    expect(picked.ladder!.steps[0].done).toBe(true);
  });

  it('finishes on real exam questions', async () => {
    const answers = hcfRights('old-e', 'Easy', 3).concat(hcfRights('old-m', 'Medium', 3), hcfRights('old-h', 'Hard', 3));
    mockLadderReads(hcfPool(), answers);

    const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'hcf');
    expect(picked.question!.source).toBe(REAL);
    expect(picked.ladder!.current).toBe(3);
    expect(picked.ladder!.steps[3].label).toBe('Real exam');
  });

  it('says Exam-style when the real exam questions have run out, and serves the hardest left', async () => {
    const answers = hcfRights('old-e', 'Easy', 3).concat(hcfRights('old-m', 'Medium', 3), hcfRights('old-h', 'Hard', 3));
    mockLadderReads(hcfPool(), answers);

    const picked = await getNextQuestionWithLadder('s1', 'grade5', ['x1', 'x2', 'x3'], 'hcf');
    expect(picked.question!.id).toBe('h1');
    expect(picked.ladder!.steps[3].label).toBe('Exam-style');
  });

  it('never repeats a question: falls forward when the step has run out', async () => {
    mockLadderReads(hcfPool(), [hcfAnswer('e1', 'Easy', false), hcfAnswer('e2', 'Easy', false)]);

    const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'hcf');
    expect(picked.question!.id).toBe('m1');
    expect(picked.ladder!.current).toBe(0);
  });

  it('serves a seen question again only when the whole topic has been seen', async () => {
    const pool = [hcfQuestion('e1', 'Easy'), hcfQuestion('e2', 'Easy')];
    mockLadderReads(pool, [hcfAnswer('e1', 'Easy', true), hcfAnswer('e2', 'Easy', true)]);

    const again = await getNextQuestionWithLadder('s1', 'grade5', ['e1'], 'hcf');
    expect(again.question!.id).toBe('e2');

    const none = await getNextQuestionWithLadder('s1', 'grade5', ['e1', 'e2'], 'hcf');
    expect(none.question).toBeNull();
  });

  it('a child who is already doing well skips Warm-up', async () => {
    mockLadderReads(hcfPool(), [], [true, true, true, true, true]);

    const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'hcf');
    expect(picked.question!.id).toBe('m1');
    expect(picked.ladder!.current).toBe(1);
    expect(picked.ladder!.steps[0].done).toBe(true);
  });

  it('reaches generated questions whose topic is only in their id, and only this topic’s', async () => {
    const pool = [
      hcfQuestion('VAR_G5_vary_hcf_lcm_V81', 'Easy', 'auto_generated_v2', 'Auto-generated variant'),
      hcfQuestion('VAR_G5_vary_angles_V03', 'Easy', 'auto_generated_v2', 'Auto-generated variant'),
      hcfQuestion('m1', 'Medium'),
    ];
    mockLadderReads(pool, []);

    for (let i = 0; i < 10; i++) {
      const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'hcf');
      expect(picked.question!.id).toBe('VAR_G5_vary_hcf_lcm_V81');
    }
  });

  it('a question that names its own topic is served only there, whatever its label matches', async () => {
    // "Fraction addition" matches the key "addition" by its label, but it is a
    // Fractions question (nodeId). Addition & Subtraction must never serve it.
    const pool = [
      { ...hcfQuestion('fa', 'Easy', GEN, 'Grade 5 — Fraction addition'), nodeId: 'gr5_fractions' },
      { ...hcfQuestion('a1', 'Easy', GEN, 'Grade 5 — Addition and subtraction'), nodeId: 'gr5_operations1' },
    ];
    mockLadderReads(pool, []);

    for (let i = 0; i < 10; i++) {
      const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'addition');
      expect(picked.question!.id).toBe('a1');
    }

    // The same holds with the ladder switched off (the scoped pick).
    prisma.question.findMany.mockResolvedValue(pool);
    mockAttemptReads([]);
    prisma.progress.findUnique.mockResolvedValue(null);
    process.env.TOPIC_LADDER = 'off';
    try {
      for (let i = 0; i < 10; i++) {
        const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'addition');
        expect(picked.question!.id).toBe('a1');
      }
    } finally {
      delete process.env.TOPIC_LADDER;
    }
  });

  it('has no ladder for a chapter topic, for whole-grade practice, or for an unknown topic key', async () => {
    prisma.question.findMany.mockResolvedValue([makeQuestion('q1', 'Easy'), makeQuestion('q2', 'Medium')]);
    mockAttemptReads([]);
    prisma.progress.findUnique.mockResolvedValue(null);

    const chapter = await getNextQuestionWithLadder('s1', 'ch11');
    expect(chapter.question).not.toBeNull();
    expect(chapter.ladder).toBeNull();

    prisma.question.findMany.mockResolvedValue(hcfPool());
    const wholeGrade = await getNextQuestionWithLadder('s1', 'grade5');
    expect(wholeGrade.question).not.toBeNull();
    expect(wholeGrade.ladder).toBeNull();

    const unknownKey = await getNextQuestionWithLadder('s1', 'grade5', [], 'zzz');
    expect(unknownKey.question).toBeNull();
    expect(unknownKey.ladder).toBeNull();
  });

  it('TOPIC_LADDER=off switches the ladder off', async () => {
    prisma.question.findMany.mockResolvedValue(hcfPool());
    mockAttemptReads([]);
    prisma.progress.findUnique.mockResolvedValue(null);

    process.env.TOPIC_LADDER = 'off';
    try {
      const picked = await getNextQuestionWithLadder('s1', 'grade5', [], 'hcf');
      expect(picked.question).not.toBeNull();
      expect(picked.ladder).toBeNull();
    } finally {
      delete process.env.TOPIC_LADDER;
    }
  });
});
