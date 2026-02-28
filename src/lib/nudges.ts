// src/lib/nudges.ts — Nudge engine for proactive student engagement

export interface Nudge {
  message:      string;
  subtext?:     string;
  mood:         'happy' | 'thinking' | 'encouraging' | 'celebrating';
  actionLabel?: string;
  actionPath?:  string;
}

const TOPIC_SHORT: Record<string, string> = {
  'ch01-05': 'Numbers',    'ch06': 'Factors',       'ch07-08': 'Fractions',
  'ch09-10': 'Operations', 'ch11': 'Decimals',       'ch12': 'Measures',
  'ch13': 'Algebra',       'ch14': 'Equations',      'ch15': 'Puzzles',
  'ch16': 'Sequences',     'ch17': 'Time',            'ch18': 'Angles',
  'ch19': 'Triangles',     'ch20': 'Quadrilaterals', 'ch21': 'Circle',
  'dh': 'Data',
};

// ── Session persistence ───────────────────────────────────────────────────────

export function saveSessionData(topicId: string, accuracy: number): void {
  if (typeof window === 'undefined') return;
  const today = new Date().toDateString();
  localStorage.setItem('mathspark_last_session_topic',    topicId);
  localStorage.setItem('mathspark_last_session_accuracy', String(accuracy));
  localStorage.setItem('mathspark_last_practice_date',    today);
}

function getLastPracticeDate(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('mathspark_last_practice_date');
}

function getLastSessionTopic(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('mathspark_last_session_topic');
}

// Track which mastery celebrations have already been shown
export function getMasteryShown(): Set<string> {
  if (typeof window === 'undefined') return new Set();
  const raw = localStorage.getItem('mathspark_mastery_shown') ?? '[]';
  try { return new Set(JSON.parse(raw) as string[]); } catch { return new Set(); }
}

export function markMasteryShown(topicId: string): void {
  if (typeof window === 'undefined') return;
  const shown = getMasteryShown();
  shown.add(topicId);
  localStorage.setItem('mathspark_mastery_shown', JSON.stringify(Array.from(shown)));
}

// ── Nudge computation ─────────────────────────────────────────────────────────

export interface NudgeInput {
  streakDays:     number;
  topicsMastered: number;
  topics: Array<{
    id:       string;
    name:     string;
    mastery:  string;
    attempted: number;
    correct:   number;
  }>;
}

export function computeNudge(input: NudgeInput): Nudge | null {
  const { streakDays, topicsMastered, topics } = input;

  const today           = new Date().toDateString();
  const lastDate        = getLastPracticeDate();
  const practicedToday  = lastDate === today;
  const lastTopic       = getLastSessionTopic();
  const masteryShown    = getMasteryShown();

  // 1. Mastered celebration — newly mastered topic not yet celebrated
  const newlyMastered = topics.find(
    (t) => t.mastery === 'Mastered' && !masteryShown.has(t.id),
  );
  if (newlyMastered) {
    return {
      message:     `You mastered ${TOPIC_SHORT[newlyMastered.id] ?? newlyMastered.name}! 🏆`,
      subtext:     'Incredible work — you earned a Diamond crown!',
      mood:        'celebrating',
      actionLabel: 'Keep going!',
      actionPath:  '/chapters',
    };
  }

  // 2. Streak danger — has streak but hasn't practiced today
  if (streakDays >= 2 && !practicedToday) {
    return {
      message:     `Your ${streakDays}-day streak is at risk! 🔥`,
      subtext:     'Just one lesson will keep it going!',
      mood:        'encouraging',
      actionLabel: 'Save my streak',
      actionPath:  lastTopic ? `/practice/${lastTopic}` : '/chapters',
    };
  }

  // 3. Close to Champion badge (5 topics mastered)
  if (topicsMastered === 4) {
    return {
      message:     "You're one step from Champion! 🥇",
      subtext:     'Master one more topic to earn the badge!',
      mood:        'encouraging',
      actionLabel: "Let's go!",
      actionPath:  '/chapters',
    };
  }

  // 4. Accuracy drop — topic they're struggling with
  const struggling = topics.find(
    (t) =>
      t.mastery !== 'Mastered' &&
      t.attempted >= 5 &&
      t.correct / t.attempted < 0.5 &&
      t.id === lastTopic,
  );
  if (struggling) {
    return {
      message:     `${TOPIC_SHORT[struggling.id] ?? struggling.name} needs more practice! 💪`,
      subtext:     'Every attempt makes you smarter!',
      mood:        'thinking',
      actionLabel: 'Try again',
      actionPath:  `/practice/${struggling.id}`,
    };
  }

  // 5. Welcome back after a 2+ day gap
  if (lastDate && lastDate !== today) {
    const daysSince = Math.floor(
      (new Date().getTime() - new Date(lastDate).getTime()) / 86_400_000,
    );
    if (daysSince >= 2) {
      return {
        message:     `Welcome back! It's been ${daysSince} days 🌟`,
        subtext:     'Pick up where you left off!',
        mood:        'happy',
        actionLabel: 'Continue',
        actionPath:  lastTopic ? `/practice/${lastTopic}` : '/chapters',
      };
    }
  }

  return null;
}
