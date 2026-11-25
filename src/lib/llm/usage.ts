import { prisma } from '@/lib/db';
import { MONETIZATION_ENABLED } from '@/lib/monetization';
import { usageDayKey } from '@/lib/sharedUtils';
import type { LlmFeature } from './types';

/** Daily message budget for a student with no active subscription. */
const FREE_DAILY_LIMIT = 5;

/**
 * Daily AI-message budget granted to everyone when monetization is OFF.
 * Matches the top ("Unlimited") plan tier — lifts the paid gate while keeping a
 * sane ceiling so uncapped LLM API cost can't run away.
 */
const MONETIZATION_OFF_DAILY_LIMIT = 100;

/**
 * Which features draw from the shared daily AI budget (DB-backed, counted
 * against `Student.aiChatMessagesUsedToday` / `subscription.aiChatDailyLimit`).
 *
 * Delivery features (misconception, narratives, lesson-reexplain, stuck-coach)
 * are intentionally NOT listed: they are cache-first and/or rare, and are gated
 * by per-route rate limiting instead — so background narration never eats a
 * child's chat budget.
 */
const DB_DAILY_FEATURES: ReadonlySet<LlmFeature> = new Set<LlmFeature>([
  'chat',
  'solve',
]);

/** India is UTC+5:30 all year round. */
const IST_OFFSET_MS = 330 * 60_000;

/** The moment today began in India: the daily budget resets at midnight there. */
function istDayStart(now: Date): Date {
  const shifted = new Date(now.getTime() + IST_OFFSET_MS);
  return new Date(
    Date.UTC(shifted.getUTCFullYear(), shifted.getUTCMonth(), shifted.getUTCDate()) - IST_OFFSET_MS,
  );
}

/** The `UsageLog` row for today: the India-time day, as every other reader and writer uses. */
function usageLogDate(now: Date): Date {
  return usageDayKey(now);
}

export interface UsageResult {
  allowed: boolean;
  remaining: number;
}

/**
 * Per-feature usage check + increment. Generalised from the original
 * `chat/route.ts` implementation.
 *
 * For features in {@link DB_DAILY_FEATURES} this counts one message against the
 * student's shared daily AI budget with a conditional update (only while the
 * count is under the limit). The day runs midnight to midnight in India. For all other
 * features it is a no-op that always allows (gating happens at the route level).
 */
export async function checkAndIncrementUsage(
  studentId: string,
  feature: LlmFeature,
): Promise<UsageResult> {
  if (!DB_DAILY_FEATURES.has(feature)) {
    return { allowed: true, remaining: Number.POSITIVE_INFINITY };
  }

  const now = new Date();
  const dayStart = istDayStart(now);
  const logDate = usageLogDate(now);

  return prisma.$transaction(async (tx) => {
    const student = await tx.student.findUnique({
      where: { id: studentId },
      select: {
        lastActiveDate: true,
        subscription: { select: { aiChatDailyLimit: true } },
      },
    });

    if (!student) return { allowed: false, remaining: 0 };

    const limit = MONETIZATION_ENABLED
      ? (student.subscription?.aiChatDailyLimit ?? FREE_DAILY_LIMIT)
      : MONETIZATION_OFF_DAILY_LIMIT;
    if (limit <= 0) return { allowed: false, remaining: 0 };

    // A new day in India starts the count again. Both writes below carry their
    // own condition, so two requests arriving together cannot both slip past
    // the limit: the database lets only one of them through.
    const lastActive = student.lastActiveDate ? new Date(student.lastActiveDate) : null;
    const isNewDay = !lastActive || lastActive < dayStart;

    let counted = false;
    if (isNewDay) {
      const reset = await tx.student.updateMany({
        where: {
          id: studentId,
          OR: [{ lastActiveDate: null }, { lastActiveDate: { lt: dayStart } }],
        },
        data: { aiChatMessagesUsedToday: 1, lastActiveDate: now },
      });
      counted = reset.count === 1;
    }
    if (!counted) {
      const bumped = await tx.student.updateMany({
        where: { id: studentId, aiChatMessagesUsedToday: { lt: limit } },
        data: { aiChatMessagesUsedToday: { increment: 1 }, lastActiveDate: now },
      });
      if (bumped.count !== 1) return { allowed: false, remaining: 0 };
    }

    const after = await tx.student.findUnique({
      where: { id: studentId },
      select: { aiChatMessagesUsedToday: true },
    });

    await tx.usageLog.upsert({
      where: { studentId_date: { studentId, date: logDate } },
      create: { studentId, date: logDate, aiChatMessages: 1 },
      update: { aiChatMessages: { increment: 1 } },
    });

    const used = after ? after.aiChatMessagesUsedToday : limit;
    return { allowed: true, remaining: Math.max(0, limit - used) };
  });
}

/**
 * Give back one message of the daily budget: used when the model call failed
 * and the child got nothing for it. Never takes the count below zero.
 */
export async function refundUsage(studentId: string, feature: LlmFeature): Promise<void> {
  if (!DB_DAILY_FEATURES.has(feature)) return;

  await prisma.student.updateMany({
    where: { id: studentId, aiChatMessagesUsedToday: { gt: 0 } },
    data: { aiChatMessagesUsedToday: { decrement: 1 } },
  });
  await prisma.usageLog.updateMany({
    where: { studentId, date: usageLogDate(new Date()), aiChatMessages: { gt: 0 } },
    data: { aiChatMessages: { decrement: 1 } },
  });
}
