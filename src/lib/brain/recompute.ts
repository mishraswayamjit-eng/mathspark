import { prisma } from '@/lib/db';
import {
  computeTopicMastery,
  computeExamReadiness,
  computeTopicPriorities,
  generateDailyPlan,
  generateNudges,
} from './engine';
import { isAiSurfaceEnabled } from '@/lib/llm/featureFlags';
import { isLlmConfigured } from '@/lib/llm/client';
import { generateSurfacePlan } from '@/lib/llm/surface';
import { logError } from '@/lib/logger';

export async function recomputeStudentAnalytics(studentId: string): Promise<void> {
  // Fetch student once — all child functions receive it as a parameter
  const student = await prisma.student.findUnique({
    where: { id: studentId },
    select: {
      name: true,
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

  // Feature 5c: LLM surfacing/narration over the VERIFIED signals above.
  // Numbers come from the engine; the LLM only orders + narrates. Gated + safe:
  // any failure leaves surfacePlan untouched (Home falls back to raw signals).
  let surfacePlan: object | undefined;
  if (isAiSurfaceEnabled() && isLlmConfigured()) {
    try {
      surfacePlan = await generateSurfacePlan({
        grade: student.grade,
        studentName: student.name,
        priorities: priorities.map((p) => ({
          dbTopicId: p.dbTopicId,
          topicName: p.topicName,
          priority: p.priority,
          reason: p.reason,
        })),
        readiness: {
          score: readiness.score,
          daysUntilExam: readiness.daysUntilExam,
          trend: readiness.trend,
        },
        planActions: plan.slice(0, 3).map((p) => p.action),
      });
    } catch (err) {
      logError('[brain/recompute] surface plan', err);
    }
  }

  await prisma.studentAnalytics.upsert({
    where:  { studentId },
    create: {
      studentId,
      topicMastery:    masteries  as object[],
      examReadiness:   readiness  as object,
      topicPriorities: priorities as object[],
      dailyPlan:       plan       as object[],
      nudges:          nudges     as object[],
      ...(surfacePlan ? { surfacePlan } : {}),
    },
    update: {
      topicMastery:    masteries  as object[],
      examReadiness:   readiness  as object,
      topicPriorities: priorities as object[],
      dailyPlan:       plan       as object[],
      nudges:          nudges     as object[],
      ...(surfacePlan ? { surfacePlan } : {}),
      lastComputedAt:  new Date(),
    },
  });
}
