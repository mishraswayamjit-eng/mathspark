'use client';

import type { FigureSpec } from '@/lib/figures/types';

export interface FigureViewProps {
  /** The figure to draw. Already validated offline; draw it as given. */
  spec: FigureSpec;
  /** Extra classes for the outer element. */
  className?: string;
}

/**
 * Draws one question figure: a still picture, never interactive, with nothing
 * on it that the spec does not state.
 *
 * PLACEHOLDER: the real renderer replaces the body of this component. The name,
 * the props and the default export are the contract other screens build on, so
 * they must not change.
 */
export default function FigureView({ spec, className }: FigureViewProps) {
  return (
    <div className={`rounded-card border-2 border-line bg-soft px-4 py-8 text-center text-label text-ink-muted ${className ?? ''}`} role="img" aria-label={`A ${spec.kind} figure`}>
      {spec.note ?? `Figure: ${spec.kind}`}
    </div>
  );
}
