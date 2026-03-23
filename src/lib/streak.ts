'use client';

// ── Streak Management ────────────────────────────────────────────────────────
// All state persisted in localStorage under "mathspark_streak"

export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastCompletedDate: string; // ISO date YYYY-MM-DD
  freezesRemaining: number;
  weekStartDate: string;     // ISO date of current week's Monday
  totalCompleted: number;
}

const STORAGE_KEY = 'mathspark_streak';

function today(): string {
  return new Date().toISOString().slice(0, 10);
}

function yesterday(): string {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return d.toISOString().slice(0, 10);
}

function getMondayOfWeek(): string {
  const d = new Date();
  const day = d.getDay(); // 0=Sun, 1=Mon, ...
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  d.setDate(diff);
  return d.toISOString().slice(0, 10);
}

function defaultStreak(): StreakData {
  return {
    currentStreak: 0,
    longestStreak: 0,
    lastCompletedDate: '',
    freezesRemaining: 1,
    weekStartDate: getMondayOfWeek(),
    totalCompleted: 0,
  };
}

export function loadStreak(): StreakData {
  if (typeof window === 'undefined') return defaultStreak();
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultStreak();
    const data = JSON.parse(raw) as StreakData;
    // Reset freeze on new week
    const currentMonday = getMondayOfWeek();
    if (data.weekStartDate !== currentMonday) {
      data.freezesRemaining = 1;
      data.weekStartDate = currentMonday;
    }
    return data;
  } catch {
    return defaultStreak();
  }
}

function saveStreak(data: StreakData) {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch { /* localStorage full — graceful ignore */ }
}

export function completeChallenge(): StreakData {
  const streak = loadStreak();
  const t = today();
  const y = yesterday();

  // Already completed today — no-op
  if (streak.lastCompletedDate === t) return streak;

  if (streak.lastCompletedDate === y) {
    // Consecutive day — increment
    streak.currentStreak += 1;
  } else if (streak.lastCompletedDate && streak.lastCompletedDate < y) {
    // Missed at least one day
    if (streak.freezesRemaining > 0) {
      // Use freeze — maintain streak
      streak.freezesRemaining -= 1;
      streak.currentStreak += 1;
    } else {
      // Reset streak
      streak.currentStreak = 1;
    }
  } else {
    // First ever completion
    streak.currentStreak = 1;
  }

  streak.lastCompletedDate = t;
  streak.totalCompleted += 1;
  if (streak.currentStreak > streak.longestStreak) {
    streak.longestStreak = streak.currentStreak;
  }

  saveStreak(streak);
  return streak;
}

export function useFreeze(): StreakData {
  const streak = loadStreak();
  if (streak.freezesRemaining > 0) {
    streak.freezesRemaining -= 1;
    saveStreak(streak);
  }
  return streak;
}

const MILESTONES: Record<number, string> = {
  7:   '🌟 1-Week Warrior',
  30:  '💪 Monthly Master',
  100: '🔥 Century Champion',
  365: '🏆 Year-Long Legend',
};

export function getStreakMilestone(streak: number): string | null {
  return MILESTONES[streak] ?? null;
}

export function isTodayCompleted(): boolean {
  const streak = loadStreak();
  return streak.lastCompletedDate === today();
}
