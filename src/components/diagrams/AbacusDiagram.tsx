import React from 'react';

interface Rod {
  label: string;
  beads: number;
}

interface Props {
  rods: Rod[];
}

const BLUE = '#1CB0F6';
const GRAY = '#374151';

export default function AbacusDiagram({ rods }: Props) {
  const rodSpacing = 70;
  const startX = 140 - ((rods.length - 1) * rodSpacing) / 2;
  const frameTop = 20;
  const frameBottom = 140;
  const beadR = 10;
  const beadGap = 22;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Abacus diagram">
      {/* Frame */}
      <rect x={startX - 30} y={frameTop} width={(rods.length - 1) * rodSpacing + 60} height={frameBottom - frameTop}
        fill="none" stroke={GRAY} strokeWidth={2} rx={4} />
      {/* Top bar */}
      <line x1={startX - 30} y1={frameTop + 24} x2={startX - 30 + (rods.length - 1) * rodSpacing + 60} y2={frameTop + 24}
        stroke={GRAY} strokeWidth={2} />

      {rods.map((rod, ri) => {
        const cx = startX + ri * rodSpacing;
        return (
          <g key={ri}>
            {/* Rod */}
            <line x1={cx} y1={frameTop} x2={cx} y2={frameBottom} stroke="#9CA3AF" strokeWidth={2} />
            {/* Label */}
            <text x={cx} y={frameTop + 16} textAnchor="middle" fontSize={10} fontWeight={700} fill={GRAY}>
              {rod.label}
            </text>
            {/* Beads stacked from bottom */}
            {Array.from({ length: rod.beads }, (_, bi) => (
              <circle key={bi} cx={cx} cy={frameBottom - 16 - bi * beadGap} r={beadR}
                fill={BLUE} stroke="#0E8AD0" strokeWidth={1.5} />
            ))}
          </g>
        );
      })}
    </svg>
  );
}
