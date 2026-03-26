import type { Page } from '@playwright/test';

const BASE = 'http://localhost:3000';

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
  const token = cookies.find((c) => c.name === 'mathspark_student_token')?.value;

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
  const token = cookies.find((c) => c.name === 'mathspark_student_token')?.value;

  const res = await page.request.post(`${BASE}/api/mock-tests/${testId}/submit`, {
    headers: { Cookie: `mathspark_student_token=${token}` },
    data: { answers },
  });

  if (!res.ok()) throw new Error(`submitMockTest failed: ${res.status()}`);
}
