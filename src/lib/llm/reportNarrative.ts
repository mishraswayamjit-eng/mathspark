import { complete } from './complete';
import { isLlmConfigured } from './client';
import { MODELS } from './models';
import { kidSafeRules } from './guardrails';
import { buildGroundedUserPrompt } from './grounding';
import { logError } from '@/lib/logger';

export interface ReportNarrativeInput {
  studentName: string;
  grade: number;
  weeklyCorrect: number;
  accuracy: number;        // 0-100
  streakDays: number;
  topicsMastered: number;
  strongestTopics: string[];
  weakestTopics: string[];
}

/**
 * The original hardcoded encouragement line — used as the static fallback so
 * the email always has a warm closing even when the LLM is unavailable.
 */
export function staticReportNarrative(studentName: string): string {
  return `Keep encouraging ${studentName} — they're working hard and growing every day! Every question they practice builds math confidence for their future. 🚀`;
}

/**
 * Generate a warm 2–3 sentence parent-facing narrative, grounded in the
 * verified weekly stats. Never invents numbers. Falls back to the static line
 * on missing key or any error.
 */
export async function generateReportNarrative(input: ReportNarrativeInput): Promise<string> {
  if (!isLlmConfigured()) return staticReportNarrative(input.studentName);

  try {
    const system = `You are MathSpark writing a short, warm note to a PARENT about their child's week of math practice. Be specific and encouraging, celebrate effort and strengths first, and gently point to one area to keep practicing. 2–3 sentences. Address the parent (not the child). Do NOT invent any statistics — only reference what is provided.

${kidSafeRules(input.grade)}`;

    const context = [
      `Child's name: ${input.studentName}`,
      `Correct answers this week: ${input.weeklyCorrect}`,
      `Overall accuracy: ${input.accuracy}%`,
      `Day streak: ${input.streakDays}`,
      `Topics mastered: ${input.topicsMastered}`,
      input.strongestTopics.length ? `Strongest topics: ${input.strongestTopics.join(', ')}` : '',
      input.weakestTopics.length ? `Topics to keep practicing: ${input.weakestTopics.join(', ')}` : '',
    ].filter(Boolean).join('\n');

    const userPrompt = buildGroundedUserPrompt({
      task: "Write the parent note (2–3 sentences) using ONLY these verified stats.",
      context,
    });

    const { text } = await complete({
      model: 'haiku',
      maxTokens: 160,
      system,
      messages: [{ role: 'user', content: userPrompt }],
    });

    const trimmed = text.trim();
    return trimmed || staticReportNarrative(input.studentName);
  } catch (err) {
    logError('[reportNarrative] generation failed', err);
    return staticReportNarrative(input.studentName);
  }
}
