'use client';

import { useState } from 'react';
import KatexRenderer from '@/components/KatexRenderer';
import StepByStep from '@/components/StepByStep';
import HintSystem from '@/components/HintSystem';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';
import type { Question, AnswerKey } from '@/types';

export function CorrectPanel({
  feedback,
  streak,
  xpEarned = 20,
  onContinue,
  onWatchSolution,
  onTrySimilar,
  canTrySimilar,
  question,
}: {
  feedback:        string;
  streak:          number;
  xpEarned?:       number;
  onContinue:      () => void;
  onWatchSolution: () => void;
  onTrySimilar:    () => void;
  canTrySimilar:   boolean;
  question?:       Question;
}) {
  const [showWhy, setShowWhy] = useState(false);

  return (
    <div className="px-4 pt-4 pb-6 space-y-3 border-l-4 border-duo-green">
      <div className="flex items-center gap-3">
        <div className="animate-sparky-dance flex-shrink-0">
          <Sparky mood="celebrating" size={56} />
        </div>
        <div className="flex-1 min-w-0">
          {streak >= 3 && (
            <div className="flex items-center gap-1.5 mb-0.5">
              <span className="animate-pop-in text-base" aria-hidden="true">🔥</span>
              <p className="text-xs font-extrabold text-duo-green-dark uppercase tracking-wide">
                {streak} in a row!
              </p>
            </div>
          )}
          <p className="text-lg font-extrabold text-gray-800 leading-tight">{feedback}</p>
        </div>
        {/* XP badge */}
        <div className="animate-scale-in flex-shrink-0 bg-duo-green/15 rounded-full px-3 py-1">
          <span className="text-sm font-extrabold text-duo-green-dark">+{xpEarned} XP</span>
        </div>
      </div>

      {/* "Why?" collapsible for step-by-step */}
      {question?.stepByStep && question.stepByStep.length > 0 && (
        <div>
          <button
            onClick={() => setShowWhy(!showWhy)}
            className="text-sm font-bold text-duo-green-dark underline underline-offset-2 min-h-[44px] flex items-center"
          >
            {showWhy ? 'Hide explanation ▲' : 'Why? ▼'}
          </button>
          {showWhy && <StepByStep steps={question.stepByStep} />}
        </div>
      )}

      {/* Actions */}
      <DuoButton variant="green" fullWidth onClick={onContinue}>
        Continue →
      </DuoButton>

      <button
        onClick={onWatchSolution}
        className="btn-sparkle w-full min-h-[44px] text-duo-green-dark font-bold text-sm flex items-center justify-center gap-2"
      >
        <span className="sparkle-icon" aria-hidden="true">🎬</span> Watch Solution
      </button>

      {canTrySimilar && (
        <button
          onClick={onTrySimilar}
          className="w-full text-gray-400 font-semibold text-xs flex items-center justify-center gap-1 min-h-[36px]"
        >
          🔄 Try a Similar Question
        </button>
      )}
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
    <div className="px-4 pt-4 pb-6 space-y-3 border-l-4 border-duo-red animate-shake-gentle">
      {/* Header row */}
      <div className="flex items-center gap-3">
        <div className="flex-shrink-0">
          <Sparky mood="encouraging" size={56} />
        </div>
        <div>
          <p className="text-base font-extrabold text-duo-red">
            Not quite!
          </p>
          <div className="bg-white rounded-xl px-3 py-2 border border-duo-red/30 mt-1.5">
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
            <span aria-hidden="true">💡</span> Common mistake
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

      {/* Action strip — simplified to 2 buttons */}
      <div className="space-y-2 pt-1">
        <DuoButton variant="red" fullWidth onClick={onGotIt}>
          Got it →
        </DuoButton>
        <button
          onClick={onWatchSolution}
          className="btn-sparkle w-full min-h-[44px] border border-gray-200 bg-white text-gray-700 font-bold text-sm rounded-2xl py-2 flex items-center justify-center gap-2"
        >
          <span className="sparkle-icon" aria-hidden="true">🎬</span> Watch Solution
        </button>
      </div>
    </div>
  );
}
