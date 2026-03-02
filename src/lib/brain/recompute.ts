import { prisma } from '@/lib/db';
import {
  computeTopicMastery,
  computeExamReadiness,
  computeTopicPriorities,
  generateDailyPlan,
  generateNudges,
} from './engine';

export async function recomputeStudentAnalytics(studentId: string): Promise<void> {
  const masteries = await computeTopicMastery(studentId);

  const [readiness, priorities, plan, nudges] = await Promise.all([
    computeExamReadiness(studentId, masteries),
    computeTopicPriorities(studentId, masteries),
    generateDailyPlan(studentId, masteries),
    generateNudges(studentId, masteries),
  ]);

  await prisma.studentAnalytics.upsert({
    where: { studentId },
    create: {
      studentId,
      topicMastery:    masteries    as object[],
      examReadiness:   readiness    as object,
      topicPriorities: priorities   as object[],
      dailyPlan:       plan         as object[],
      nudges:          nudges       as object[],
    },
    update: {
      topicMastery:    masteries    as object[],
      examReadiness:   readiness    as object,
      topicPriorities: priorities   as object[],
      dailyPlan:       plan         as object[],
      nudges:          nudges       as object[],
      lastComputedAt:  new Date(),
    },
  });
}
