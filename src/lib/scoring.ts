// ── Scoring Engine ──────────────────────────────────────────────────────────
// Centralised score calculation with negative marking support.

export interface ScoreResult {
  correct: number;
  wrong: number;
  skipped: number;
  total: number;
  netScore: number;
  maxMarks: number;
  percentage: number;
  negativeDeduction: number;
}

/**
 * Calculate exam score from student answers vs answer key.
 *
 * @param answers      Map of questionNumber → selected option ("A"/"B"/"C"/"D")
 * @param answerKey    Map of questionNumber → correct option
 * @param negativeMarking  Whether wrong answers deduct marks (0.25 per wrong)
 * @param maxMarks     Maximum marks (defaults to total questions)
 */
export function calculateScore(
  answers: Record<string, string>,
  answerKey: Record<string, string>,
  negativeMarking = false,
  maxMarks?: number,
): ScoreResult {
  let correct = 0;
  let wrong = 0;
  let skipped = 0;

  const totalQuestions = Object.keys(answerKey).length;

  for (const [qNum, correctAns] of Object.entries(answerKey)) {
    const studentAns = answers[qNum];
    if (!studentAns) {
      skipped++;
    } else if (studentAns === correctAns) {
      correct++;
    } else {
      wrong++;
    }
  }

  const negativeDeduction = negativeMarking ? wrong * 0.25 : 0;
  const netScore = correct - negativeDeduction;
  const max = maxMarks ?? totalQuestions;
  const percentage = max > 0 ? Math.round((netScore / max) * 100) : 0;

  return {
    correct,
    wrong,
    skipped,
    total: totalQuestions,
    netScore,
    maxMarks: max,
    percentage: Math.max(0, percentage),
    negativeDeduction,
  };
}

/**
 * Score verdict for Sparky messages.
 */
export function getVerdict(percentage: number): {
  label: string;
  sparkyMood: 'celebrating' | 'happy' | 'encouraging' | 'thinking';
} {
  if (percentage >= 90) return { label: 'Outstanding! 🏆', sparkyMood: 'celebrating' };
  if (percentage >= 75) return { label: 'Excellent! ⭐', sparkyMood: 'celebrating' };
  if (percentage >= 60) return { label: 'Good work! 👍', sparkyMood: 'happy' };
  if (percentage >= 40) return { label: 'Keep going! 💪', sparkyMood: 'encouraging' };
  return { label: 'More practice needed 📚', sparkyMood: 'thinking' };
}
