import React from 'react';

interface Props {
  grid: string[][];
  unknownLabel?: string;
}

const BLUE = '#1CB0F6';
const BLUE_FILL = 'rgba(28,176,246,0.2)';
const GRAY = '#374151';

export default function NumberGridDiagram({ grid, unknownLabel = '?' }: Props) {
  const rows = grid.length;
  const cols = grid[0].length;
  const cellSize = Math.min(60, 240 / Math.max(rows, cols));
  const totalW = cols * cellSize;
  const totalH = rows * cellSize;
  const offsetX = (280 - totalW) / 2;
  const offsetY = (160 - totalH) / 2;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Number grid">
      {grid.map((row, ri) =>
        row.map((cell, ci) => {
          const x = offsetX + ci * cellSize;
          const y = offsetY + ri * cellSize;
          const isUnknown = cell === '?';
          return (
            <g key={`${ri}-${ci}`}>
              <rect x={x} y={y} width={cellSize} height={cellSize}
                fill={isUnknown ? BLUE_FILL : 'white'}
                stroke={isUnknown ? BLUE : '#D1D5DB'} strokeWidth={1.5} />
              <text x={x + cellSize / 2} y={y + cellSize / 2 + 5}
                textAnchor="middle" fontSize={cellSize > 40 ? 14 : 11}
                fontWeight={isUnknown ? 700 : 600}
                fill={isUnknown ? BLUE : GRAY}>
                {isUnknown ? unknownLabel : cell}
              </text>
            </g>
          );
        })
      )}
    </svg>
  );
}
