import React from 'react';

interface Figure {
  cells: Array<[number, number]>;
  label: string;
}

interface Props {
  figures: Figure[];
}

const GREEN = '#58CC02';
const GRAY = '#374151';

export default function TetrominoDiagram({ figures }: Props) {
  const cellSize = 16;
  const figW = 130;
  const figH = 70;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Tetromino shapes">
      {figures.map((fig, fi) => {
        const col = fi % 2;
        const row = Math.floor(fi / 2);
        const baseX = 10 + col * figW;
        const baseY = 5 + row * figH;

        // Center the shape within its quadrant
        const minR = Math.min(...fig.cells.map(c => c[0]));
        const maxR = Math.max(...fig.cells.map(c => c[0]));
        const minC = Math.min(...fig.cells.map(c => c[1]));
        const maxC = Math.max(...fig.cells.map(c => c[1]));
        const shapeW = (maxC - minC + 1) * cellSize;
        const shapeH = (maxR - minR + 1) * cellSize;
        const ox = baseX + (figW - shapeW) / 2 - minC * cellSize;
        const oy = baseY + 12 + (figH - 22 - shapeH) / 2 - minR * cellSize;

        return (
          <g key={fi}>
            <text x={baseX + figW / 2} y={baseY + 10} textAnchor="middle"
              fontSize={10} fontWeight={700} fill={GRAY}>
              {fig.label}
            </text>
            {fig.cells.map(([r, c], ci) => (
              <rect key={ci}
                x={ox + c * cellSize} y={oy + r * cellSize}
                width={cellSize} height={cellSize}
                fill={GREEN} stroke="white" strokeWidth={1.5} rx={2} />
            ))}
          </g>
        );
      })}
    </svg>
  );
}
