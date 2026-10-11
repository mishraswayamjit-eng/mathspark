/**
 * Feature 5b — persist an AI-authored question.
 *
 * ID scheme: `AIGEN_<topicId>_<cuid>` so authored rows are instantly greppable
 * and distinguishable from the seed corpus. `source='ai_generated'` is the
 * kill-switch handle used by `aiSourceFilter()` + mock-test exclusion.
 */

import { randomUUID } from 'crypto';
import { prisma } from '@/lib/db';
import type { AuthoredQuestion } from './author';

export async function persistAuthoredQuestion(
  topicId: string,
  subTopic: string,
  difficulty: 'Easy' | 'Medium' | 'Hard',
  q: AuthoredQuestion,
): Promise<string> {
  const id = `AIGEN_${topicId}_${randomUUID()}`;

  await prisma.question.create({
    data: {
      id,
      topicId,
      subTopic: subTopic || 'general',
      difficulty,
      questionText: q.questionText,
      questionLatex: '',
      option1: q.option1,
      option2: q.option2,
      option3: q.option3,
      option4: q.option4,
      correctAnswer: q.correctAnswer,
      hint1: q.hint1,
      hint2: q.hint2,
      hint3: q.hint3,
      stepByStep: JSON.stringify(q.stepByStep),
      misconceptionA: q.misconceptionA,
      misconceptionB: q.misconceptionB,
      misconceptionC: q.misconceptionC,
      misconceptionD: q.misconceptionD,
      source: 'ai_generated',
    },
  });

  return id;
}
