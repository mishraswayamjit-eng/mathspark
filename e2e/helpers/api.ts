import type { Page } from '@playwright/test';

const BASE = 'http://localhost:3000';

/** Get the auth cookie value from the page context. */
function getToken(cookies: { name: string; value: string }[]): string {
  const token = cookies.find((c) => c.name === 'mathspark_student_token')?.value;
  if (!token) throw new Error('No auth cookie found');
  return token;
}

/**
 * Create a mock test via the API (requires authenticated cookie on the page).
 * Returns the testId.
 */
export async function createMockTest(
  page: Page,
  options: { type?: string; questionCount?: number } = {},
): Promise<string> {
  const { type = 'quick', questionCount = 5 } = options;
  const cookies = await page.context().cookies();
  const token = getToken(cookies);

  const res = await page.request.post(`${BASE}/api/mock-tests`, {
    headers: { Cookie: `mathspark_student_token=${token}` },
    data: { type, questionCount },
  });

  if (!res.ok()) throw new Error(`createMockTest failed: ${res.status()}`);
  const body = await res.json();
  return body.testId ?? body.id;
}

/**
 * Submit answers for a mock test via the API.
 */
export async function submitMockTest(
  page: Page,
  testId: string,
  answers: Record<string, string>,
): Promise<void> {
  const cookies = await page.context().cookies();
  const token = getToken(cookies);

  const res = await page.request.post(`${BASE}/api/mock-tests/${testId}/submit`, {
    headers: { Cookie: `mathspark_student_token=${token}` },
    data: { answers },
  });

  if (!res.ok()) throw new Error(`submitMockTest failed: ${res.status()}`);
}

/**
 * Submit answers for ALL questions in a mock test via the API.
 * Fetches the test, builds an answer map (all option1), then submits.
 * Returns the answers map for verification.
 */
export async function submitTestAnswers(
  page: Page,
  testId: string,
): Promise<Record<string, string>> {
  const cookies = await page.context().cookies();
  const token = getToken(cookies);

  // Fetch the test to get question IDs
  const testRes = await page.request.get(`${BASE}/api/mock-tests/${testId}`, {
    headers: { Cookie: `mathspark_student_token=${token}` },
  });

  if (!testRes.ok()) throw new Error(`getTest failed: ${testRes.status()}`);
  const testData = await testRes.json();

  const questions = testData.questions ?? testData.test?.questions ?? [];
  const answers: Record<string, string> = {};
  for (const q of questions) {
    const qId = q.id ?? q.questionId;
    if (qId) answers[qId] = q.option1 ?? 'A';
  }

  await submitMockTest(page, testId, answers);
  return answers;
}

/**
 * GET test results after submission.
 * Returns the response body JSON.
 */
export async function getTestResults(
  page: Page,
  testId: string,
): Promise<Record<string, unknown>> {
  const cookies = await page.context().cookies();
  const token = getToken(cookies);

  const res = await page.request.get(`${BASE}/api/mock-tests/${testId}/response`, {
    headers: { Cookie: `mathspark_student_token=${token}` },
  });

  if (!res.ok()) throw new Error(`getTestResults failed: ${res.status()}`);
  return (await res.json()) as Record<string, unknown>;
}

/**
 * Fetch a flashcard deck for verification purposes.
 */
export async function fetchFlashcardDeck(
  page: Page,
  deckId: string,
): Promise<Record<string, unknown>> {
  const cookies = await page.context().cookies();
  const token = getToken(cookies);

  const res = await page.request.get(`${BASE}/api/flashcards/deck/${deckId}`, {
    headers: { Cookie: `mathspark_student_token=${token}` },
  });

  if (!res.ok()) throw new Error(`fetchFlashcardDeck failed: ${res.status()}`);
  return (await res.json()) as Record<string, unknown>;
}
