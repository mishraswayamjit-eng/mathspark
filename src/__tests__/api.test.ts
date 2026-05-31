import { vi, describe, it, expect, beforeEach } from 'vitest';

// ---------------------------------------------------------------------------
// Mock next/server so NextResponse is available outside the Next.js runtime.
// ---------------------------------------------------------------------------
vi.mock('next/server', () => {
  return {
    NextResponse: {
      json: (body: unknown, init?: ResponseInit) => {
        const status = init?.status ?? 200;
        return {
          status,
          json: async () => body,
        };
      },
    },
  };
});

// ---------------------------------------------------------------------------
// Mock @/lib/db — each route imports prisma from here
// ---------------------------------------------------------------------------
vi.mock('@/lib/db', () => ({
  prisma: {
    topic: { findMany: vi.fn() },
    attempt: {
      create: vi.fn(),
      findMany: vi.fn(),
    },
    progress: {
      upsert: vi.fn(),
      findUnique: vi.fn(),
    },
    question: { findFirst: vi.fn() },
  },
}));

// ---------------------------------------------------------------------------
// Mock @/lib/mastery so POST /api/attempts doesn't call through to Prisma twice
// ---------------------------------------------------------------------------
vi.mock('@/lib/mastery', () => ({
  updateProgress: vi.fn(),
  calculateMastery: vi.fn(),
}));

// ---------------------------------------------------------------------------
// Mock @/lib/adaptive so GET /api/questions/next is isolated
// ---------------------------------------------------------------------------
vi.mock('@/lib/adaptive', () => ({
  getNextQuestion: vi.fn(),
}));

import { prisma } from '@/lib/db';
import { updateProgress } from '@/lib/mastery';
import { getNextQuestion } from '@/lib/adaptive';

// Route handlers — imported AFTER mocks are registered
import { GET as getTopics } from '@/app/api/topics/route';
import { POST as postAttempt } from '@/app/api/attempts/route';
import { GET as getNextQ } from '@/app/api/questions/next/route';

const mockTopicFindMany = prisma.topic.findMany as ReturnType<typeof vi.fn>;
const mockAttemptCreate = prisma.attempt.create as ReturnType<typeof vi.fn>;
const mockUpdateProgress = updateProgress as ReturnType<typeof vi.fn>;
const mockGetNextQuestion = getNextQuestion as ReturnType<typeof vi.fn>;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const TOPIC_ORDER = [
  'ch01-05', 'ch06', 'ch07-08', 'ch09-10', 'ch11', 'ch12',
  'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch20', 'ch21', 'dh',
];

const makeTopic = (id: string) => ({ id, name: `Topic ${id}`, chapterNumber: id });

/** Build a mock POST Request with a JSON body. */
function makePostRequest(url: string, body: unknown): Request {
  return new Request(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

/** Build a mock GET Request with query params. */
function makeGetRequest(url: string): Request {
  return new Request(url);
}

const makeQuestion = (id: string, difficulty = 'Medium') => ({
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

// ---------------------------------------------------------------------------
// GET /api/topics
// ---------------------------------------------------------------------------
describe('GET /api/topics', () => {
  it('returns all 16 topics with status 200', async () => {
    const mockTopics = TOPIC_ORDER.map(makeTopic);
    mockTopicFindMany.mockResolvedValueOnce(mockTopics);

    const res = await getTopics();

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body).toHaveLength(16);
  });

  it('returns topics sorted in curriculum order', async () => {
    // Return topics in scrambled order; the route should sort them
    const scrambled = [...TOPIC_ORDER].reverse().map(makeTopic);
    mockTopicFindMany.mockResolvedValueOnce(scrambled);

    const res = await getTopics();
    const body = await res.json();

    const returnedIds = body.map((t: { id: string }) => t.id);
    expect(returnedIds).toEqual(TOPIC_ORDER);
  });

  it('returns empty array when no topics exist', async () => {
    mockTopicFindMany.mockResolvedValueOnce([]);

    const res = await getTopics();
    const body = await res.json();

    expect(res.status).toBe(200);
    expect(body).toEqual([]);
  });

  it('calls prisma.topic.findMany once', async () => {
    mockTopicFindMany.mockResolvedValueOnce([]);
    await getTopics();
    expect(mockTopicFindMany).toHaveBeenCalledOnce();
  });
});

// ---------------------------------------------------------------------------
// POST /api/attempts
// ---------------------------------------------------------------------------
describe('POST /api/attempts', () => {
  const validPayload = {
    studentId: 'stu1',
    questionId: 'q1',
    topicId: 'ch11',
    selected: 'A',
    isCorrect: true,
    hintUsed: 1,
    timeTakenMs: 5000,
  };

  it('returns 201 and the created attempt on valid payload', async () => {
    const createdAttempt = { id: 'att1', ...validPayload };
    mockAttemptCreate.mockResolvedValueOnce(createdAttempt);
    mockUpdateProgress.mockResolvedValueOnce(undefined);

    const req = makePostRequest('http://localhost/api/attempts', validPayload);
    const res = await postAttempt(req);

    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.id).toBe('att1');
  });

  it('calls updateProgress with studentId and topicId', async () => {
    mockAttemptCreate.mockResolvedValueOnce({ id: 'att2', ...validPayload });
    mockUpdateProgress.mockResolvedValueOnce(undefined);

    const req = makePostRequest('http://localhost/api/attempts', validPayload);
    await postAttempt(req);

    expect(mockUpdateProgress).toHaveBeenCalledOnce();
    expect(mockUpdateProgress).toHaveBeenCalledWith('stu1', 'ch11');
  });

  it('returns 400 when studentId is missing', async () => {
    const { studentId: _, ...noStudentId } = validPayload;
    const req = makePostRequest('http://localhost/api/attempts', noStudentId);
    const res = await postAttempt(req);

    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error).toBeTruthy();
  });

  it('returns 400 when questionId is missing', async () => {
    const { questionId: _, ...noQId } = validPayload;
    const req = makePostRequest('http://localhost/api/attempts', noQId);
    const res = await postAttempt(req);

    expect(res.status).toBe(400);
  });

  it('returns 400 when topicId is missing', async () => {
    const { topicId: _, ...noTopicId } = validPayload;
    const req = makePostRequest('http://localhost/api/attempts', noTopicId);
    const res = await postAttempt(req);

    expect(res.status).toBe(400);
  });

  it('returns 400 when selected is missing', async () => {
    const { selected: _, ...noSelected } = validPayload;
    const req = makePostRequest('http://localhost/api/attempts', noSelected);
    const res = await postAttempt(req);

    expect(res.status).toBe(400);
  });

  it('defaults hintUsed=0 and timeTakenMs=0 when omitted', async () => {
    const minimalPayload = {
      studentId: 'stu1',
      questionId: 'q1',
      topicId: 'ch11',
      selected: 'B',
      isCorrect: false,
    };
    mockAttemptCreate.mockResolvedValueOnce({ id: 'att3', ...minimalPayload });
    mockUpdateProgress.mockResolvedValueOnce(undefined);

    const req = makePostRequest('http://localhost/api/attempts', minimalPayload);
    await postAttempt(req);

    const createCall = mockAttemptCreate.mock.calls[0][0];
    expect(createCall.data.hintUsed).toBe(0);
    expect(createCall.data.timeTakenMs).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// GET /api/questions/next
// ---------------------------------------------------------------------------
describe('GET /api/questions/next', () => {
  it('returns 200 with question data when getNextQuestion returns a question', async () => {
    const q = makeQuestion('q-test-1');
    mockGetNextQuestion.mockResolvedValueOnce(q);

    const req = makeGetRequest(
      'http://localhost/api/questions/next?topicId=ch11&studentId=stu1',
    );
    const res = await getNextQ(req);

    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.id).toBe('q-test-1');
  });

  it('parses stepByStep JSON string into an array', async () => {
    const steps = [{ step: 1, text: 'First step' }];
    const q = { ...makeQuestion('q-steps'), stepByStep: JSON.stringify(steps) };
    mockGetNextQuestion.mockResolvedValueOnce(q);

    const req = makeGetRequest(
      'http://localhost/api/questions/next?topicId=ch11&studentId=stu1',
    );
    const res = await getNextQ(req);
    const body = await res.json();

    expect(Array.isArray(body.stepByStep)).toBe(true);
    expect(body.stepByStep).toEqual(steps);
  });

  it('returns 404 when getNextQuestion returns null', async () => {
    mockGetNextQuestion.mockResolvedValueOnce(null);

    const req = makeGetRequest(
      'http://localhost/api/questions/next?topicId=ch11&studentId=stu1',
    );
    const res = await getNextQ(req);

    expect(res.status).toBe(404);
    const body = await res.json();
    expect(body.error).toBeTruthy();
  });

  it('returns 400 when topicId is missing', async () => {
    const req = makeGetRequest(
      'http://localhost/api/questions/next?studentId=stu1',
    );
    const res = await getNextQ(req);

    expect(res.status).toBe(400);
  });

  it('returns 400 when studentId is missing', async () => {
    const req = makeGetRequest(
      'http://localhost/api/questions/next?topicId=ch11',
    );
    const res = await getNextQ(req);

    expect(res.status).toBe(400);
  });

  it('passes parsed exclude list as seenIds to getNextQuestion', async () => {
    const q = makeQuestion('q-excl');
    mockGetNextQuestion.mockResolvedValueOnce(q);

    const req = makeGetRequest(
      'http://localhost/api/questions/next?topicId=ch11&studentId=stu1&exclude=q1,q2,q3',
    );
    await getNextQ(req);

    expect(mockGetNextQuestion).toHaveBeenCalledWith(
      'stu1',
      'ch11',
      ['q1', 'q2', 'q3'],
      0,
      0,
    );
  });

  it('passes cw and cr as consecutiveWrong and consecutiveRight', async () => {
    const q = makeQuestion('q-streak');
    mockGetNextQuestion.mockResolvedValueOnce(q);

    const req = makeGetRequest(
      'http://localhost/api/questions/next?topicId=ch11&studentId=stu1&cw=3&cr=0',
    );
    await getNextQ(req);

    expect(mockGetNextQuestion).toHaveBeenCalledWith('stu1', 'ch11', [], 3, 0);
  });

  it('defaults cw=0 and cr=0 when omitted', async () => {
    const q = makeQuestion('q-defaults');
    mockGetNextQuestion.mockResolvedValueOnce(q);

    const req = makeGetRequest(
      'http://localhost/api/questions/next?topicId=ch11&studentId=stu1',
    );
    await getNextQ(req);

    expect(mockGetNextQuestion).toHaveBeenCalledWith('stu1', 'ch11', [], 0, 0);
  });
});
