import React from 'react';

interface PointSpec {
  value: number;
  label: string;
}

interface Props {
  min: number;
  max: number;
  points: PointSpec[];
  step?: number;
}

const GRAY = '#374151';
const BLUE = '#1CB0F6';

export default function NumberLineDiagram({ min, max, points, step }: Props) {
  const padding = 20;
  const w = 260;
  const lineY = 50;
  const range = max - min;
  const effectiveStep = step ?? (range <= 10 ? 1 : range <= 20 ? 2 : 5);

  function xPos(value: number) {
    return padding + ((value - min) / range) * w;
  }

  // Generate tick values
  const ticks: number[] = [];
  for (let v = min; v <= max; v += effectiveStep) {
    ticks.push(v);
  }
  if (ticks[ticks.length - 1] !== max) ticks.push(max);

  return (
    <svg viewBox="0 0 300 90" className="w-full" role="img" aria-label={`Number line from ${min} to ${max}`}>
      {/* Main line */}
      <line x1={padding - 5} y1={lineY} x2={padding + w + 5} y2={lineY}
        stroke={GRAY} strokeWidth={2} />

      {/* Arrow heads */}
      <polygon points={`${padding - 8},${lineY} ${padding - 2},${lineY - 4} ${padding - 2},${lineY + 4}`} fill={GRAY} />
      <polygon points={`${padding + w + 8},${lineY} ${padding + w + 2},${lineY - 4} ${padding + w + 2},${lineY + 4}`} fill={GRAY} />

      {/* Ticks and labels */}
      {ticks.map(v => {
        const x = xPos(v);
        const isZero = v === 0;
        return (
          <g key={v}>
            <line x1={x} y1={lineY - 5} x2={x} y2={lineY + 5}
              stroke={GRAY} strokeWidth={isZero ? 2 : 1} />
            <text x={x} y={lineY + 18} textAnchor="middle"
              fontSize={9} fill="#6B7280" fontWeight={isZero ? 700 : 400}>
              {Number.isInteger(v) ? v : v.toFixed(2)}
            </text>
          </g>
        );
      })}

      {/* Labeled points */}
      {points.map((p, i) => {
        const x = xPos(p.value);
        return (
          <g key={i}>
            <circle cx={x} cy={lineY} r={4} fill={BLUE} />
            <text x={x} y={lineY - 12} textAnchor="middle"
              fontSize={11} fontWeight={700} fill={BLUE}>
              {p.label}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
