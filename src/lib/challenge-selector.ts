'use client';

// ── Daily Challenge Selector ─────────────────────────────────────────────────
// Picks today's challenge from data/daily-challenges.json based on day-of-year

export interface ChallengeQuestion {
  questionNumber: number;
  sourceId: string;
  questionText: string;
  options: Array<{ id: string; text: string }>;
  correctAnswer: string;
  hints: string[];
  stepByStep: Array<{ step: number; text: string; latex?: string }>;
  topicBucket: string;
}

export interface DailyChallenge {
  challengeId: string;
  grade: number;
  day: number;
  questionsCount: number;
  estimatedMinutes: number;
  questions: ChallengeQuestion[];
  answerKey: Record<string, string>;
  funFact: string;
}

export interface DailyChallengeData {
  meta: {
    questionsPerChallenge: number;
    monthlyThemes: Record<string, string>;
    streakMechanics: {
      milestones: Record<string, string>;
    };
  };
  challenges: Record<string, DailyChallenge[]>;
}

/** Response shape from /api/daily-challenge-data?grade=N */
export interface TodaysChallengeResponse {
  meta: DailyChallengeData['meta'];
  challenge: DailyChallenge;
  dayOfYear: number;
  index: number;
}

/**
 * Fetch today's single challenge for the given grade from the server API.
 * Returns null when the API returns 404 (no data for that grade).
 */
export async function loadTodaysChallenge(grade: number): Promise<TodaysChallengeResponse | null> {
  const res = await fetch(`/api/daily-challenge-data?grade=${grade}`);
  if (!res.ok) return null;
  return (await res.json()) as TodaysChallengeResponse;
}

export function getCurrentMonthTheme(meta: DailyChallengeData['meta']): string {
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ];
  const month = monthNames[new Date().getMonth()];
  return meta.monthlyThemes[month] ?? '';
}

const LAST_CHALLENGE_KEY = 'mathspark_last_challenge';

export interface ChallengeResult {
  date: string;
  grade: number;
  challengeId: string;
  score: number;
  total: number;
}

export function saveChallengeResult(result: ChallengeResult) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(LAST_CHALLENGE_KEY, JSON.stringify(result));
  } catch { /* graceful */ }
}

export function getTodaysChallengeResult(): ChallengeResult | null {
  if (typeof window === 'undefined') return null;
  try {
    const raw = localStorage.getItem(LAST_CHALLENGE_KEY);
    if (!raw) return null;
    const result = JSON.parse(raw) as ChallengeResult;
    const today = new Date().toISOString().slice(0, 10);
    if (result.date === today) return result;
    return null;
  } catch {
    return null;
  }
}
