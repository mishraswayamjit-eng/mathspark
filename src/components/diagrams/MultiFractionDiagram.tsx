import React from 'react';
import FractionDiagram from './FractionDiagram';

interface FigureSpec {
  shape: 'rectangle' | 'circle' | 'triangle';
  totalParts: number;
  shadedParts: number;
  columns?: number;
  label: string;
}

interface Props {
  figures: FigureSpec[];
  highlightIndex?: number;
}

export default function MultiFractionDiagram({ figures, highlightIndex }: Props) {
  return (
    <div className="grid grid-cols-2 gap-2" role="img" aria-label="Multiple fraction figures for comparison">
      {figures.map((fig, i) => (
        <div
          key={i}
          className={`rounded-lg border-2 p-2 ${
            highlightIndex === i
              ? 'border-action bg-soft'
              : 'border-line bg-white'
          }`}
        >
          <FractionDiagram
            shape={fig.shape}
            totalParts={fig.totalParts}
            shadedParts={fig.shadedParts}
            columns={fig.columns}
          />
          <p className="text-center text-xs font-bold text-ink-muted mt-1">
            {fig.label}
          </p>
        </div>
      ))}
    </div>
  );
}
