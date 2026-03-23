// ── Mistake Pattern Detector ────────────────────────────────────────────────
// Matches wrong answers to known mistake patterns from mistake-patterns.json.

export interface MistakePattern {
  id: string;
  name: string;
  emoji: string;
  category: string;
  description: string;
  whyItHappens: string;
  howToFix: string;
  example: {
    question: string;
    wrongAnswer: string;
    rightAnswer: string;
    wrongThinking: string;
    rightThinking: string;
  } | null;
  frequency: string;
  affectedTopics: string[];
  affectedGrades: number[];
  keywords: string[];
  sparkyMessage: string;
  difficulty: number;
}

export interface DetectedMistake {
  patternId: string;
  patternName: string;
  emoji: string;
  occurrences: number;
  sparkyMessage: string;
  howToFix: string;
  category: string;
}

export interface WrongAnswer {
  questionNumber: number;
  chosenOption: string;
  correctOption: string;
  misconceptionText: string;
  topicBucket: string;
}

/**
 * Detect mistake patterns from wrong answers by matching misconception text
 * and topic against known patterns.
 */
export function detectMistakes(
  wrongAnswers: WrongAnswer[],
  patterns: MistakePattern[],
  grade?: number,
): DetectedMistake[] {
  const counts = new Map<string, number>();

  for (const wrong of wrongAnswers) {
    const misconLower = wrong.misconceptionText.toLowerCase();
    const topicLower = wrong.topicBucket.toLowerCase();

    for (const pattern of patterns) {
      // Filter by grade if available
      if (grade && pattern.affectedGrades.length > 0 && !pattern.affectedGrades.includes(grade)) {
        continue;
      }

      // Match by keywords in misconception text
      const matched = pattern.keywords.some((kw) =>
        misconLower.includes(kw.toLowerCase()),
      );

      // Also match by affected topic overlap
      const topicMatch = pattern.affectedTopics.some((t) =>
        topicLower.includes(t.toLowerCase()) || t.toLowerCase().includes(topicLower),
      );

      if (matched || (topicMatch && misconLower.length > 10)) {
        counts.set(pattern.id, (counts.get(pattern.id) ?? 0) + 1);
      }
    }
  }

  // Build result sorted by occurrences descending
  const results: DetectedMistake[] = [];
  for (const [patternId, occurrences] of counts.entries()) {
    const p = patterns.find((pat) => pat.id === patternId);
    if (!p) continue;
    results.push({
      patternId: p.id,
      patternName: p.name,
      emoji: p.emoji,
      occurrences,
      sparkyMessage: p.sparkyMessage,
      howToFix: p.howToFix,
      category: p.category,
    });
  }

  return results.sort((a, b) => b.occurrences - a.occurrences);
}
