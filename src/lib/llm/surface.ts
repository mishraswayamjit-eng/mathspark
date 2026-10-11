/**
 * Feature 5c — LLM surfacing + plan narration.
 *
 * Reconciles the two governing answers: the NUMBERS come from the deterministic
 * Brain Engine (topic priorities, daily plan, exam readiness); the LLM only
 * decides PRESENTATION — how to order the focus list and how to narrate "why" in
 * a warm, kid-friendly way. It never invents new priorities or changes scores.
 *
 * Gated by AI_SURFACE_ENABLED. On any failure it returns a deterministic plan
 * built straight from the Brain Engine signals (static floor).
 */

import { complete } from './complete';
import { gradeDescriptor, kidSafeRules } from './guardrails';
import { MODELS } from './models';

interface PriorityInput {
  dbTopicId: string;
  topicName: string;
  priority: number;
  reason: string;
}

interface ReadinessInput {
  score: number;
  daysUntilExam: number | null;
  trend: 'improving' | 'stable' | 'declining';
}

export interface SurfaceInput {
  grade: number;
  studentName?: string;
  priorities: PriorityInput[];
  readiness: ReadinessInput | null;
  /** First few daily-plan action labels, for narration context only. */
  planActions: string[];
}

export interface SurfacePlan {
  headline: string;
  narration: string;
  /** dbTopicIds in the LLM's recommended presentation order. */
  orderedTopicIds: string[];
  focusTopicId: string | null;
  generatedBy: 'llm' | 'static';
  generatedAt: string;
}

/** Deterministic fallback: trust the Brain Engine ordering as-is. */
export function staticSurfacePlan(input: SurfaceInput): SurfacePlan {
  const ordered = [...input.priorities]
    .sort((a, b) => b.priority - a.priority)
    .map((p) => p.dbTopicId);
  return {
    headline: input.studentName ? `Let's learn, ${input.studentName}!` : "Let's learn!",
    narration:
      input.priorities[0]?.reason ??
      'Keep practicing a little every day to build your skills!',
    orderedTopicIds: ordered,
    focusTopicId: ordered[0] ?? null,
    generatedBy: 'static',
    generatedAt: new Date().toISOString(),
  };
}

function extractJson(text: string): unknown {
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start < 0 || end <= start) throw new Error('No JSON object in response');
  return JSON.parse(text.slice(start, end + 1));
}

/**
 * Produce the surfacing plan. The LLM receives ONLY verified Brain Engine
 * signals and may reorder/narrate; it may not add topics outside the input set.
 */
export async function generateSurfacePlan(input: SurfaceInput): Promise<SurfacePlan> {
  if (input.priorities.length === 0) return staticSurfacePlan(input);

  const validIds = new Set(input.priorities.map((p) => p.dbTopicId));

  const prioritiesBlock = input.priorities
    .map(
      (p) =>
        `- id=${p.dbTopicId} | ${p.topicName} | priority=${p.priority} | reason=${p.reason}`,
    )
    .join('\n');

  const readinessBlock = input.readiness
    ? `Exam readiness score: ${input.readiness.score}/100; trend: ${input.readiness.trend}; days until exam: ${input.readiness.daysUntilExam ?? 'not set'}.`
    : 'Exam readiness: not available.';

  const system = `You are Sparky, a warm learning coach for a ${gradeDescriptor(input.grade)}. You are given the student's VERIFIED analytics from our deterministic engine. Your job is ONLY to (a) choose a friendly presentation ORDER for the focus topics and (b) write a short, warm "why" narration. You must NOT invent new topics, scores, or facts — use only what is given.

${kidSafeRules(input.grade)}

Return ONLY a JSON object:
{
  "headline": string,            // <= 6 words, encouraging
  "narration": string,           // 1-2 warm sentences explaining what to focus on and why
  "orderedTopicIds": string[]    // a reordering of the given topic ids (use ONLY the provided ids)
}`;

  const userPrompt = `Student: ${input.studentName ?? 'the student'}\n\nTOP FOCUS TOPICS (verified, higher priority = more important):\n${prioritiesBlock}\n\n${readinessBlock}\n\nToday's suggested actions: ${input.planActions.join('; ') || 'none'}\n\nOrder the topic ids for the best learning experience and narrate why.`;

  try {
    const { text } = await complete({
      model: 'sonnet',
      maxTokens: 300,
      system,
      messages: [{ role: 'user', content: userPrompt }],
    });

    const parsed = extractJson(text) as {
      headline?: unknown;
      narration?: unknown;
      orderedTopicIds?: unknown;
    };

    const headline =
      typeof parsed.headline === 'string' && parsed.headline.trim()
        ? parsed.headline.trim()
        : staticSurfacePlan(input).headline;
    const narration =
      typeof parsed.narration === 'string' && parsed.narration.trim()
        ? parsed.narration.trim()
        : input.priorities[0].reason;

    // Keep only valid ids (no hallucinated topics), then append any the LLM
    // dropped so nothing verified is lost.
    const llmOrder = Array.isArray(parsed.orderedTopicIds)
      ? parsed.orderedTopicIds.filter(
          (id): id is string => typeof id === 'string' && validIds.has(id),
        )
      : [];
    const seen = new Set(llmOrder);
    const orderedTopicIds = [
      ...llmOrder,
      ...input.priorities.map((p) => p.dbTopicId).filter((id) => !seen.has(id)),
    ];

    return {
      headline,
      narration,
      orderedTopicIds,
      focusTopicId: orderedTopicIds[0] ?? null,
      generatedBy: 'llm',
      generatedAt: new Date().toISOString(),
    };
  } catch {
    return staticSurfacePlan(input);
  }
}
