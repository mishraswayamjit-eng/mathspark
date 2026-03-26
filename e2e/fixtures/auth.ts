import { test as base, type BrowserContext, type Page } from '@playwright/test';
import { SignJWT } from 'jose';
import { DEFAULT_STUDENT, type TestStudent } from './test-students';

const COOKIE_NAME = 'mathspark_student_token';

/** Mint a JWT identical to src/lib/studentAuth.ts createStudentToken(). */
async function mintToken(studentId: string): Promise<string> {
  const secret = process.env.NEXTAUTH_SECRET;
  if (!secret) throw new Error('NEXTAUTH_SECRET env var required for E2E tests');
  const key = new TextEncoder().encode(secret);
  return new SignJWT({ studentId })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('30d')
    .sign(key);
}

/** Inject auth cookie + localStorage for a test student. */
async function authenticateContext(
  context: BrowserContext,
  student: TestStudent,
): Promise<void> {
  const token = await mintToken(student.id);

  // Set the httpOnly cookie the API routes read
  await context.addCookies([
    {
      name: COOKIE_NAME,
      value: token,
      domain: 'localhost',
      path: '/',
      httpOnly: true,
      sameSite: 'Lax',
    },
  ]);

  // Set localStorage values the client pages read.
  // We do this via an init script that runs before every page load.
  await context.addInitScript(
    ({ id, name, grade, tier }: TestStudent) => {
      localStorage.setItem('mathspark_student_id', id);
      localStorage.setItem('mathspark_student_name', name);
      localStorage.setItem('mathspark_student_grade', String(grade));
      localStorage.setItem('mathspark_subscription_tier', String(tier));
    },
    student,
  );
}

// ─── Custom fixtures ────────────────────────────────────────────────────────

type AuthFixtures = {
  /** Student profile used for this test. Override via test.use(). */
  studentProfile: TestStudent;
  /** A Page already authenticated as `studentProfile`. */
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  studentProfile: [DEFAULT_STUDENT, { option: true }],

  authenticatedPage: async ({ browser, studentProfile }, use) => {
    const context = await browser.newContext();
    await authenticateContext(context, studentProfile);
    const page = await context.newPage();
    await use(page);
    await context.close();
  },
});

export { expect } from '@playwright/test';
