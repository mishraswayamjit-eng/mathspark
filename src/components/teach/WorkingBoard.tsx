'use client';

import type { BoardOp } from '@/lib/teach/types';

export interface WorkingBoardProps {
  /** Everything done on the board so far, in order. The board draws the result of all of it. */
  ops: BoardOp[];
  /**
   * Ops from this index onwards are new: they are written or drawn with an
   * animation, one after another. Ops before it are shown as already done.
   */
  animateFrom: number;
  /** How long the new ops have to appear, in milliseconds (the length of the sentence being spoken). */
  beatMs: number;
  /** Extra classes for the outer element. */
  className?: string;
}

/**
 * The teacher's board: lines of working written one under another, with the
 * marks a teacher makes as they talk (arcs, strike-throughs with a note, bars
 * for dividing both sides, a ring round the answer).
 *
 * PLACEHOLDER: the real board replaces the body of this component. The name,
 * the props and the default export are the contract the lesson player builds
 * on, so they must not change.
 */
export default function WorkingBoard({ ops, className }: WorkingBoardProps) {
  const lines: Array<{ id: string; text: string }> = [];
  for (let i = 0; i < ops.length; i++) {
    const op = ops[i];
    if (op.op === 'clear') lines.length = 0;
    if (op.op === 'write') lines.push({ id: op.id, text: op.text });
  }
  return (
    <div className={`rounded-card border-2 border-line bg-white px-5 py-6 space-y-3 ${className ?? ''}`} role="img" aria-label="The working so far">
      {lines.map((l) => (
        <p key={l.id} className="font-display text-heading text-ink">{l.text}</p>
      ))}
    </div>
  );
}
