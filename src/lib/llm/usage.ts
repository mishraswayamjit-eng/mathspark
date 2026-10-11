import { prisma } from '@/lib/db';
import type { LlmFeature } from './types';

/** Daily message budget for a student with no active subscription. */
const FREE_DAILY_LIMIT = 5;

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

export interface UsageResult {
  allowed: boolean;
  remaining: number;
}

/**
 * Per-feature usage check + increment. Generalised from the original
 * `chat/route.ts` implementation.
 *
 * For features in {@link DB_DAILY_FEATURES} this performs an atomic
 * read-check-increment of the student's shared daily AI budget. For all other
 * features it is a no-op that always allows (gating happens at the route level).
 */
export async function checkAndIncrementUsage(
  studentId: string,
  feature: LlmFeature,
): Promise<UsageResult> {
  if (!DB_DAILY_FEATURES.has(feature)) {
    return { allowed: true, remaining: Number.POSITIVE_INFINITY };
  }

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return prisma.$transaction(async (tx) => {
    const student = await tx.student.findUnique({
      where: { id: studentId },
      select: {
        aiChatMessagesUsedToday: true,
        lastActiveDate: true,
        subscription: { select: { aiChatDailyLimit: true } },
      },
    });

    if (!student) return { allowed: false, remaining: 0 };

    const limit = student.subscription?.aiChatDailyLimit ?? FREE_DAILY_LIMIT;

    // Reset counter if last active date was before today.
    const lastActive = student.lastActiveDate ? new Date(student.lastActiveDate) : null;
    const isNewDay = !lastActive || lastActive < today;
    const usedToday = isNewDay ? 0 : student.aiChatMessagesUsedToday;

    if (usedToday >= limit) return { allowed: false, remaining: 0 };

    await tx.student.update({
      where: { id: studentId },
      data: {
        aiChatMessagesUsedToday: usedToday + 1,
        lastActiveDate: new Date(),
      },
    });

    await tx.usageLog.upsert({
      where: { studentId_date: { studentId, date: today } },
      create: { studentId, date: today, aiChatMessages: 1 },
      update: { aiChatMessages: { increment: 1 } },
    });

    return { allowed: true, remaining: limit - usedToday - 1 };
  });
}
