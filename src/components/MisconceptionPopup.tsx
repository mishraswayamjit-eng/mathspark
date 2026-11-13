'use client';

import KatexRenderer from './KatexRenderer';

interface MisconceptionPopupProps {
  /** The misconception text for the selected wrong answer. */
  text: string;
  /** The correct answer letter (A/B/C/D) to display. */
  correctAnswer: string;
  /** The text of the correct option. */
  correctText: string;
}

/** Returns true if a string contains LaTeX markup (backslash commands). */
function hasLatex(text: string): boolean {
  return text.includes('\\');
}

/**
 * MisconceptionPopup — Explains why the chosen wrong answer is wrong.
 * Shown after a student selects an incorrect option.
 * Reusable across practice, daily challenge, exam review, etc.
 */
export default function MisconceptionPopup({
  text,
  correctAnswer,
  correctText,
}: MisconceptionPopupProps) {
  if (!text) return null;

  return (
    <div className="bg-white border-2 border-line rounded-card px-4 py-3 space-y-2 animate-fade-in">
      {/* Correct answer callout */}
      <div className="flex items-center gap-2">
        <span className="w-6 h-6 rounded-full bg-success text-white flex items-center justify-center text-xs font-extrabold flex-shrink-0">
          {correctAnswer}
        </span>
        <span className="text-sm font-bold text-ink">
          {hasLatex(correctText) ? (
            <KatexRenderer latex={correctText} displayMode={false} />
          ) : (
            correctText
          )}
        </span>
      </div>

      {/* Misconception explanation */}
      <div>
        <p className="text-caption text-ink-muted mb-1">
          💡 Common mistake
        </p>
        <p className="text-sm text-ink font-semibold leading-snug">
          {hasLatex(text) ? (
            <KatexRenderer latex={text} displayMode={false} />
          ) : (
            text
          )}
        </p>
      </div>
    </div>
  );
}
