'use client';

import { useEffect, useRef, useState } from 'react';
import type { LadderInfo } from '@/lib/practice/ladderTypes';

interface TopicLadderProps {
  ladder: LadderInfo;
}

/** What changed since the ladder we showed last, if anything worth saying. */
type Moment =
  | { kind: 'none' }
  | { kind: 'finished'; label: string; index: number }
  | { kind: 'refresher' };

const NO_MOMENT: Moment = { kind: 'none' };

/**
 * The topic's four steps as a small path, for the top of the practice screen:
 * Warm-up, Build, Challenge, Exam. Finished steps are ticked, the current one
 * is highlighted, and one line of words says how far through it the child is.
 * When a step has just been finished the line turns into a small cheer until
 * the next question arrives.
 *
 * It only shows what the server worked out; it decides nothing. Not
 * interactive. Nothing here starts hidden, and the one animation (a pop on the
 * newly ticked step) is scale-only and is switched off by the global
 * reduced-motion rule.
 */
export default function TopicLadder({ ladder }: TopicLadderProps) {
  const previous = useRef<LadderInfo | null>(null);
  const [moment, setMoment] = useState<Moment>(NO_MOMENT);

  useEffect(() => {
    const before = previous.current;
    previous.current = ladder;
    if (!before || before.topicLabel !== ladder.topicLabel) {
      setMoment(NO_MOMENT);
      return;
    }
    // The same ladder passed again (a re-render): leave the message as it is.
    if (
      before.current === ladder.current &&
      before.got === ladder.got &&
      before.needed === ladder.needed &&
      before.complete === ladder.complete
    ) {
      return;
    }
    const finishedStep = before.steps[before.current];
    if (finishedStep && !before.complete && (ladder.current > before.current || ladder.complete)) {
      setMoment({ kind: 'finished', label: finishedStep.label, index: before.current });
    } else if (ladder.current < before.current) {
      setMoment({ kind: 'refresher' });
    } else {
      setMoment(NO_MOMENT);
    }
  }, [ladder]);

  const steps = ladder.steps;
  const currentStep = steps[ladder.current];
  const currentLabel = currentStep ? currentStep.label : '';
  const left = Math.max(0, ladder.needed - ladder.got);

  let line: string;
  let cheer = false;
  if (ladder.complete) {
    line = 'You finished every step of ' + ladder.topicLabel + '!';
    cheer = true;
  } else if (moment.kind === 'finished') {
    line = moment.label + ' done! Next step: ' + currentLabel + '.';
    cheer = true;
  } else if (moment.kind === 'refresher') {
    line = 'Let’s practise ' + currentLabel + ' a little more. ' + left + ' right and you move up again.';
  } else if (ladder.got === 0) {
    line = 'Get ' + ladder.needed + ' right to finish ' + currentLabel + '.';
  } else {
    line = ladder.got + ' of ' + ladder.needed + ' right to finish ' + currentLabel + '.';
  }

  return (
    <div
      role="group"
      aria-label={'Your steps in ' + ladder.topicLabel}
      className="w-full min-w-0 bg-card border-2 border-line rounded-card px-2 py-2"
    >
      <ol className="grid grid-cols-4 list-none m-0 p-0">
        {steps.map((step, i) => {
          const isCurrent = i === ladder.current && !ladder.complete;
          const reached = ladder.complete || i <= ladder.current;
          const justDone = moment.kind === 'finished' && moment.index === i;
          const dot = step.done
            ? 'bg-success border-success text-card'
            : isCurrent
              ? 'bg-card border-action text-action'
              : 'bg-soft border-line text-ink-muted';
          const status = step.done ? 'done' : isCurrent ? 'you are here' : 'coming up';
          return (
            <li
              key={step.id}
              className="relative min-w-0 flex flex-col items-center"
              aria-current={isCurrent ? 'step' : undefined}
            >
              {i > 0 && (
                <span
                  aria-hidden="true"
                  className={'absolute top-3 left-0 right-1/2 h-0.5 -translate-y-1/2 ' + (reached ? 'bg-success' : 'bg-line')}
                />
              )}
              {i < steps.length - 1 && (
                <span
                  aria-hidden="true"
                  className={
                    'absolute top-3 left-1/2 right-0 h-0.5 -translate-y-1/2 ' +
                    (ladder.complete || i < ladder.current ? 'bg-success' : 'bg-line')
                  }
                />
              )}
              <span
                aria-hidden="true"
                className={
                  'relative z-10 flex h-6 w-6 items-center justify-center rounded-full border-2 text-xs font-extrabold leading-none ' +
                  dot +
                  (justDone ? ' animate-pop-in' : '')
                }
              >
                {step.done ? '✓' : i + 1}
              </span>
              <span
                className={
                  'mt-1 block w-full truncate px-0.5 text-center text-[11px] leading-tight ' +
                  (isCurrent ? 'font-extrabold text-ink' : 'font-bold text-ink-muted')
                }
              >
                {step.label}
                <span className="sr-only">{', ' + status}</span>
              </span>
            </li>
          );
        })}
      </ol>
      <p aria-live="polite" className="mt-1.5 text-center text-sm font-bold leading-snug text-ink">
        {cheer && <span aria-hidden="true">{'⭐ '}</span>}
        {line}
      </p>
    </div>
  );
}
