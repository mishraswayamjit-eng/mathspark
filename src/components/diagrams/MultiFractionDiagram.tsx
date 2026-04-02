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
          className={`rounded-lg border p-2 ${
            highlightIndex === i
              ? 'border-[#1CB0F6] bg-blue-50'
              : 'border-gray-200 bg-white'
          }`}
        >
          <FractionDiagram
            shape={fig.shape}
            totalParts={fig.totalParts}
            shadedParts={fig.shadedParts}
            columns={fig.columns}
          />
          <p className="text-center text-[10px] font-bold text-gray-600 mt-1">
            {fig.label}
          </p>
        </div>
      ))}
    </div>
  );
}
