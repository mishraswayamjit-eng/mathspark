'use client';

import KatexRenderer from '@/components/KatexRenderer';
import StepByStep from '@/components/StepByStep';
import HintSystem from '@/components/HintSystem';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';
import type { Question, AnswerKey } from '@/types';

export function CorrectPanel({
  feedback,
  streak,
  onContinue,
  onWatchSolution,
  onTrySimilar,
  canTrySimilar,
}: {
  feedback:        string;
  streak:          number;
  onContinue:      () => void;
  onWatchSolution: () => void;
  onTrySimilar:    () => void;
  canTrySimilar:   boolean;
}) {
  return (
    <div className="px-4 pt-4 pb-6 space-y-3">
      <div className="flex items-center gap-3">
        <div className="animate-sparky-dance flex-shrink-0">
          <Sparky mood="celebrating" size={56} />
        </div>
        <div>
          {streak >= 3 && (
            <p className="text-xs font-extrabold text-white/80 uppercase tracking-wide mb-0.5">
              🔥 {streak} in a row!
            </p>
          )}
          <p className="text-lg font-extrabold text-white leading-tight">{feedback}</p>
        </div>
      </div>
      <button
        onClick={onWatchSolution}
        className="btn-sparkle w-full min-h-[44px] bg-white/20 border border-white/40 text-white font-extrabold text-sm rounded-2xl py-2 flex items-center justify-center gap-2"
      >
        <span className="sparkle-icon">🎬</span> Watch Solution
      </button>
      {canTrySimilar && (
        <button
          onClick={onTrySimilar}
          className="w-full min-h-[44px] bg-white/10 border border-white/30 text-white font-extrabold text-sm rounded-2xl py-2 flex items-center justify-center gap-2"
        >
          🔄 Try a Similar Question
        </button>
      )}
      <DuoButton variant="white" fullWidth onClick={onContinue}>
        Continue →
      </DuoButton>
    </div>
  );
}

export function WrongPanel({
  question,
  selected,
  onGotIt,
  hintLevel,
  onHintLevelUp,
  onWatchSolution,
  onTrySimilar,
  canTrySimilar,
}: {
  question:        Question;
  selected:        AnswerKey | null;
  onGotIt:         () => void;
  hintLevel:       number;
  onHintLevelUp:   (n: number) => void;
  onWatchSolution: () => void;
  onTrySimilar:    () => void;
  canTrySimilar:   boolean;
}) {
  const optionKey     = selected ? (`misconception${selected}` as keyof Question) : null;
  const misconception = optionKey ? (question[optionKey] as string) : '';
  const correctIdx    = ['A', 'B', 'C', 'D'].indexOf(question.correctAnswer);
  const correctText   = question[`option${correctIdx + 1}` as keyof Question] as string;
  const textHasLatex  = correctText.includes('\\');

  return (
    <div className="px-4 pt-4 pb-6 space-y-3">
      {/* Header row */}
      <div className="flex items-center gap-3">
        <div className="flex-shrink-0">
          <Sparky mood="encouraging" size={56} />
        </div>
        <div>
          <p className="text-sm font-extrabold text-duo-red uppercase tracking-wide">
            No worries! Here&#39;s how it works…
          </p>
          <div className="bg-white rounded-xl px-3 py-2 border border-red-100 mt-1.5">
            <p className="text-xs text-gray-500 font-semibold">Correct answer ({question.correctAnswer})</p>
            {textHasLatex ? (
              <div className="mt-1"><KatexRenderer latex={correctText} displayMode={false} /></div>
            ) : (
              <p className="text-sm text-gray-800 font-bold leading-snug">{correctText}</p>
            )}
          </div>
        </div>
      </div>

      {/* Misconception box */}
      {misconception && (
        <div className="bg-blue-50 border border-blue-200 rounded-2xl px-4 py-3">
          <p className="text-xs font-extrabold text-blue-700 uppercase tracking-wide mb-1">
            💡 Common mistake
          </p>
          <p className="text-sm text-gray-700 font-medium leading-snug">{misconception}</p>
        </div>
      )}

      {/* Step-by-step inline */}
      <StepByStep steps={question.stepByStep} />

      {/* Hints */}
      <HintSystem
        hint1={question.hint1}
        hint2={question.hint2}
        hint3={question.hint3}
        level={hintLevel}
        onLevelUp={onHintLevelUp}
      />

      {/* Action strip */}
      <div className="space-y-2 pt-1">
        {canTrySimilar && (
          <button
            onClick={onTrySimilar}
            className="w-full min-h-[48px] bg-duo-green hover:bg-[#5bd800] text-white font-extrabold text-sm rounded-2xl py-3 flex items-center justify-center gap-2 shadow-sm"
          >
            🔄 Try a Similar Question
          </button>
        )}
        <button
          onClick={onWatchSolution}
          className="btn-sparkle w-full min-h-[44px] bg-gradient-to-r from-violet-500 to-indigo-500 text-white font-extrabold text-sm rounded-2xl py-2 flex items-center justify-center gap-2 shadow-md"
        >
          <span className="sparkle-icon">🎬</span> Watch Solution
        </button>
        <button
          onClick={onGotIt}
          className="w-full min-h-[44px] border border-gray-200 text-gray-500 font-semibold text-sm rounded-2xl py-2 flex items-center justify-center bg-white"
        >
          Got it, move on →
        </button>
      </div>
    </div>
  );
}
