import { prisma } from '@/lib/db';

// ── Feature keys matching the Subscription.features JSON ──────────────────

export type Feature =
  | 'practice'
  | 'chapters'
  | 'hints'
  | 'stepByStep'
  | 'progressTracking'
  | 'diagnosticQuiz'
  | 'adaptiveEngine'
  | 'dashboard'
  | 'misconceptionFeedback'
  | 'badges'
  | 'streaks'
  | 'aiTutor'
  | 'mockTest'
  | 'parentDashboard';

// Minimum plan name required for each feature
const FEATURE_PLAN: Record<Feature, string> = {
  practice:              'Starter',
  chapters:              'Starter',
  hints:                 'Starter',
  stepByStep:            'Starter',
  progressTracking:      'Starter',
  aiTutor:               'Starter',
  diagnosticQuiz:        'Advanced',
  adaptiveEngine:        'Advanced',
  misconceptionFeedback: 'Advanced',
  dashboard:             'Unlimited',
  badges:                'Unlimited',
  streaks:               'Unlimited',
  mockTest:              'Unlimited',
  parentDashboard:       'Unlimited',
};

export interface GateResult {
  allowed:      boolean;
  requiredPlan: string;
  remaining?:   { dailyMinutes: number; aiChats: number };
}

/**
 * Check if a student is allowed to use a feature.
 * Students with no subscription are treated as having no plan (most features blocked).
 * If studentId is null/undefined, basic features are allowed (backward compat for guest users).
 */
export async function checkFeature(studentId: string | null | undefined, feature: Feature): Promise<GateResult> {
  const requiredPlan = FEATURE_PLAN[feature];

  // Guest / no studentId — allow basic features without restriction
  if (!studentId) {
    const basic: Feature[] = ['practice', 'chapters', 'hints', 'stepByStep'];
    return { allowed: basic.includes(feature), requiredPlan };
  }

  const student = await prisma.student.findUnique({
    where:  { id: studentId },
    select: {
      dailyUsageMinutes:       true,
      aiChatMessagesUsedToday: true,
      subscription: {
        select: {
          name:              true,
          tier:              true,
          features:          true,
          dailyLimitMinutes: true,
          aiChatDailyLimit:  true,
        },
      },
    },
  });

  // No subscription — allow Starter-level features freely (backward compatibility)
  if (!student?.subscription) {
    const starterFeatures: Feature[] = ['practice', 'chapters', 'hints', 'stepByStep', 'progressTracking'];
    return { allowed: starterFeatures.includes(feature), requiredPlan };
  }

  const sub = student.subscription;
  let features: Record<string, boolean> = {};
  try { features = JSON.parse(sub.features); } catch { /* ignore */ }

  const allowed = !!features[feature];
  return {
    allowed,
    requiredPlan,
    remaining: {
      dailyMinutes: Math.max(0, sub.dailyLimitMinutes - student.dailyUsageMinutes),
      aiChats:      Math.max(0, sub.aiChatDailyLimit  - student.aiChatMessagesUsedToday),
    },
  };
}

/**
 * Check if a student has exceeded their daily time limit.
 * Returns true if they are allowed to practice.
 */
export async function checkDailyLimit(studentId: string): Promise<{
  allowed:    boolean;
  used:       number;
  limit:      number;
  remaining:  number;
}> {
  const student = await prisma.student.findUnique({
    where:  { id: studentId },
    select: {
      dailyUsageMinutes: true,
      subscription: { select: { dailyLimitMinutes: true } },
    },
  });

  const limit   = student?.subscription?.dailyLimitMinutes ?? 60; // Default: 60 min
  const used    = student?.dailyUsageMinutes ?? 0;
  const remaining = Math.max(0, limit - used);

  return { allowed: remaining > 0, used, limit, remaining };
}
