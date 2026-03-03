import { prisma } from '@/lib/db';
import {
  computeTopicMastery,
  computeExamReadiness,
  computeTopicPriorities,
  generateDailyPlan,
  generateNudges,
} from './engine';

export async function recomputeStudentAnalytics(studentId: string): Promise<void> {
  // Fetch student once — all child functions receive it as a parameter
  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: {
      grade: true,
      examDate: true,
      focusTopics: true,
      currentStreak: true,
    },
  });
  if (!student) return;

  const masteries = await computeTopicMastery(studentId, student);

  const [readiness, priorities, plan, nudges] = await Promise.all([
    computeExamReadiness(studentId, student, masteries),
    computeTopicPriorities(studentId, student, masteries),
    generateDailyPlan(studentId, student, masteries),
    generateNudges(studentId, student, masteries),
  ]);

  await prisma.studentAnalytics.upsert({
    where:  { studentId },
    create: {
      studentId,
      topicMastery:    masteries  as object[],
      examReadiness:   readiness  as object,
      topicPriorities: priorities as object[],
      dailyPlan:       plan       as object[],
      nudges:          nudges     as object[],
    },
    update: {
      topicMastery:    masteries  as object[],
      examReadiness:   readiness  as object,
      topicPriorities: priorities as object[],
      dailyPlan:       plan       as object[],
      nudges:          nudges     as object[],
      lastComputedAt:  new Date(),
    },
  });
}
