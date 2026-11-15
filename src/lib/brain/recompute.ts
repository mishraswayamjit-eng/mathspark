import { prisma } from '@/lib/db';
import {
  computeTopicMastery,
  computeExamReadiness,
  computeTopicPriorities,
  generateDailyPlan,
  generateNudges,
} from './engine';
import type {
  TopicMasteryEntry,
  ExamReadinessResult,
  TopicPriority,
  DailyPlanItem,
  Nudge,
} from './engine';
import { isAiSurfaceEnabled } from '@/lib/llm/featureFlags';
import { isLlmConfigured } from '@/lib/llm/client';
import { generateSurfacePlan } from '@/lib/llm/surface';
import type { SurfaceInput } from '@/lib/llm/surface';
import { logError } from '@/lib/logger';

/** What one recompute worked out and stored: the same values that are now in the row. */
export interface ComputedAnalytics {
  topicMastery: TopicMasteryEntry[];
  examReadiness: ExamReadinessResult;
  topicPriorities: TopicPriority[];
  dailyPlan: DailyPlanItem[];
  nudges: Nudge[];
  /** Stored as `lastComputedAt`: the moment this recompute STARTED reading. */
  computedAt: Date;
}

export interface RecomputeOptions {
  /**
   * What to do about the Feature 5c narration (an LLM call), when it is switched on:
   * - 'await' (default): generate it first and store it with everything else.
   * - 'background': store the engine's numbers first, then generate and store
   *   the narration without the caller waiting. For request paths that must
   *   not wait on a model (Home).
   * - 'skip': leave the stored narration as it is.
   */
  surface?: 'await' | 'background' | 'skip';
}

/**
 * Generate the 5c narration and store it on its own. Never throws: any failure
 * leaves the stored narration untouched (Home falls back to raw signals).
 */
async function refreshSurfacePlan(studentId: string, input: SurfaceInput): Promise<void> {
  try {
    const surfacePlan: object = await generateSurfacePlan(input);
    await prisma.studentAnalytics.update({
      where: { studentId },
      data:  { surfacePlan },
    });
  } catch (err) {
    logError('[brain/recompute] background surface plan', err);
  }
}

/**
 * Recompute and store one student's analytics. Returns what was stored, so a
 * caller can use it without reading the row again; null when the student does
 * not exist. Throws on database failure.
 */
export async function recomputeStudentAnalytics(
  studentId: string,
  options: RecomputeOptions = {},
): Promise<ComputedAnalytics | null> {
  const surfaceMode = options.surface ?? 'await';
  // Taken BEFORE the attempts are read, and stored as `lastComputedAt`. An
  // answer that arrives while this is running is then newer than the row, so
  // Home knows the row does not include it yet.
  const computedAt = new Date();

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
  if (!student) return null;

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
  const wantsSurface = surfaceMode !== 'skip' && isAiSurfaceEnabled() && isLlmConfigured();
  const surfaceInput: SurfaceInput = {
    grade: student.grade,
    studentName: student.name,
    // Keyed on the topic-tree node id. The database topic id is the same
    // ("grade5") for every node of a keyed grade and would collapse them into one.
    priorities: priorities.map((p) => ({
      topicId: p.topicId,
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
  };

  let surfacePlan: object | undefined;
  if (wantsSurface && surfaceMode === 'await') {
    try {
      surfacePlan = await generateSurfacePlan(surfaceInput);
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
      lastComputedAt:  computedAt,
    },
    update: {
      topicMastery:    masteries  as object[],
      examReadiness:   readiness  as object,
      topicPriorities: priorities as object[],
      dailyPlan:       plan       as object[],
      nudges:          nudges     as object[],
      ...(surfacePlan ? { surfacePlan } : {}),
      lastComputedAt:  computedAt,
    },
  });

  // The narration is an LLM call: here the caller does not wait for it. It is
  // started only after the row exists, and stores itself when it is ready.
  if (wantsSurface && surfaceMode === 'background') {
    void refreshSurfacePlan(studentId, surfaceInput);
  }

  return {
    topicMastery:    masteries,
    examReadiness:   readiness,
    topicPriorities: priorities,
    dailyPlan:       plan,
    nudges,
    computedAt,
  };
}
