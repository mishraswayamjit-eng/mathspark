'use client';

import { useState, useEffect } from 'react';
import KatexRenderer from '@/components/KatexRenderer';
import StepByStep from '@/components/StepByStep';
import HintSystem from '@/components/HintSystem';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';
import AiExplainInline from '@/components/AiExplainInline';
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
    <div className="px-4 pt-4 pb-6 space-y-3 text-success" role="status">
      <div className="flex items-center gap-3">
        <div className="animate-sparky-dance flex-shrink-0">
          <Sparky mood="celebrating" size={56} />
        </div>
        <div className="flex-1 min-w-0">
          {streak >= 3 && (
            <div className="flex items-center gap-1.5 mb-0.5">
              <span className="animate-pop-in text-base" aria-hidden="true">🔥</span>
              <p className="text-sm font-extrabold">
                {streak} in a row!
              </p>
            </div>
          )}
          <h3 className="text-[21px] font-semibold leading-tight">{feedback}</h3>
        </div>
        {/* XP badge */}
        <div className="animate-scale-in flex-shrink-0 bg-white border-2 border-line rounded-xl px-2.5 py-1">
          <span className="text-sm font-extrabold text-ink whitespace-nowrap"><span aria-hidden="true">⭐</span> +{xpEarned} XP</span>
        </div>
      </div>

      {/* "Why?" collapsible for step-by-step */}
      {question?.stepByStep && question.stepByStep.length > 0 && (
        <div>
          <button
            onClick={() => setShowWhy(!showWhy)}
            className="text-sm font-extrabold text-success underline underline-offset-2 min-h-[44px] flex items-center"
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
        className="ui-btn w-full text-sm"
      >
        <span className="sparkle-icon" aria-hidden="true">🎬</span> Watch Solution
      </button>

      {canTrySimilar && (
        <button
          onClick={onTrySimilar}
          className="w-full text-ink-muted font-bold text-sm flex items-center justify-center gap-1 min-h-[44px]"
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
  showCoach = false,
}: {
  question:        Question;
  selected:        AnswerKey | null;
  onGotIt:         () => void;
  hintLevel:       number;
  onHintLevelUp:   (n: number) => void;
  onWatchSolution: () => void;
  onTrySimilar:    () => void;
  canTrySimilar:   boolean;
  /** Feature 1: on the 2nd+ wrong attempt, auto-show Socratic stuck-coaching. */
  showCoach?:      boolean;
}) {
  const optionKey     = selected ? (`misconception${selected}` as keyof Question) : null;
  const misconception = optionKey ? (question[optionKey] as string) : '';

  // Feature 2: fetch a personalized AI nudge that re-expresses the verified
  // misconception. Falls back silently to the static `misconception` text.
  const [aiNudge, setAiNudge] = useState<string | null>(null);
  useEffect(() => {
    if (!selected || !misconception) return;
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch('/api/ai/misconception', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ questionId: question.id, selected }),
        });
        if (!res.ok) return;
        const data = (await res.json()) as { nudge?: string | null };
        if (!cancelled && data.nudge) setAiNudge(data.nudge);
      } catch {
        /* keep static fallback */
      }
    })();
    return () => { cancelled = true; };
  }, [question.id, selected, misconception]);

  const correctIdx    = ['A', 'B', 'C', 'D'].indexOf(question.correctAnswer);
  const correctText   = (correctIdx >= 0 ? (question[`option${correctIdx + 1}` as keyof Question] as string) : '') ?? '';
  const textHasLatex  = correctText.includes('\\');

  return (
    <div className="px-4 pt-4 pb-6 space-y-3 animate-shake-gentle" role="alert">
      {/* Header row */}
      <div className="flex items-center gap-3">
        <div className="flex-shrink-0">
          <Sparky mood="encouraging" size={56} />
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-[21px] font-semibold leading-tight text-retry">
            Not quite. Let&apos;s look again <span aria-hidden="true">🔍</span>
          </h3>
        </div>
      </div>

      {/* Verified correct answer */}
      <div className="bg-success-soft text-success rounded-[10px] px-3 py-2 font-extrabold">
        <p className="text-sm"><span aria-hidden="true">✅</span> Correct answer: option {question.correctAnswer}</p>
        {textHasLatex ? (
          <div className="mt-1"><KatexRenderer latex={correctText} displayMode={false} /></div>
        ) : (
          <p className="text-base leading-snug [overflow-wrap:anywhere]">{correctText}</p>
        )}
      </div>

      {/* Misconception box — shows the personalized AI nudge when available,
          otherwise the verified static misconception text (static floor). */}
      {misconception && (
        <div className="bg-white border-l-[6px] border-action rounded-[10px] px-3 py-2.5">
          <p className="text-sm font-extrabold text-ink mb-1">
            <span aria-hidden="true">🧠</span> Common mistake
          </p>
          <p className="text-[15px] text-ink font-semibold leading-snug">{aiNudge ?? misconception}</p>
        </div>
      )}

      {/* Feature 1: Socratic stuck-coaching — auto-streams on the 2nd+ wrong
          attempt. Grounded in verified steps; never states the final answer. */}
      {showCoach && (
        <AiExplainInline
          key={question.id}
          endpoint="/api/ai/stuck-coach"
          body={{ questionId: question.id }}
          buttonLabel="Feeling stuck? Let Sparky help"
          heading="Sparky's hint"
          autoStart
        />
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
        <DuoButton variant="green" fullWidth onClick={onGotIt}>
          Got it →
        </DuoButton>
        <button
          onClick={onWatchSolution}
          className="ui-btn w-full text-sm"
        >
          <span className="sparkle-icon" aria-hidden="true">🎬</span> Watch Solution
        </button>
      </div>
    </div>
  );
}
