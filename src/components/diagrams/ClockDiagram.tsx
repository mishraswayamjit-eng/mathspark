import React from 'react';

interface Props {
  hour: number;
  minute: number;
}

const GRAY = '#374151';
const BLUE = '#1CB0F6';

export default function ClockDiagram({ hour, minute }: Props) {
  const cx = 70, cy = 70, r = 55;

  // Hour hand angle (from 12 o'clock, clockwise)
  const hourAngle = ((hour % 12) + minute / 60) * 30 - 90;
  const hourRad = (hourAngle * Math.PI) / 180;
  const hourLen = 30;
  const hx = cx + hourLen * Math.cos(hourRad);
  const hy = cy + hourLen * Math.sin(hourRad);

  // Minute hand angle
  const minAngle = minute * 6 - 90;
  const minRad = (minAngle * Math.PI) / 180;
  const minLen = 42;
  const mx = cx + minLen * Math.cos(minRad);
  const my = cy + minLen * Math.sin(minRad);

  return (
    <svg viewBox="0 0 140 140" className="w-full max-w-[140px] mx-auto" role="img" aria-label={`Clock showing ${hour}:${minute.toString().padStart(2, '0')}`}>
      {/* Clock face */}
      <circle cx={cx} cy={cy} r={r} fill="white" stroke={GRAY} strokeWidth={2.5} />

      {/* Hour markers */}
      {Array.from({ length: 12 }, (_, i) => {
        const angle = (i * 30 - 90) * Math.PI / 180;
        const outerR = r - 4;
        const innerR = i % 3 === 0 ? r - 14 : r - 10;
        return (
          <line
            key={i}
            x1={cx + innerR * Math.cos(angle)}
            y1={cy + innerR * Math.sin(angle)}
            x2={cx + outerR * Math.cos(angle)}
            y2={cy + outerR * Math.sin(angle)}
            stroke={GRAY}
            strokeWidth={i % 3 === 0 ? 2.5 : 1}
            strokeLinecap="round"
          />
        );
      })}

      {/* Hour numbers */}
      {[12, 3, 6, 9].map(n => {
        const angle = (n * 30 - 90) * Math.PI / 180;
        const numR = r - 20;
        return (
          <text
            key={n}
            x={cx + numR * Math.cos(angle)}
            y={cy + numR * Math.sin(angle) + 4}
            textAnchor="middle"
            fontSize={10}
            fontWeight={700}
            fill={GRAY}
          >
            {n}
          </text>
        );
      })}

      {/* Hour hand */}
      <line x1={cx} y1={cy} x2={hx} y2={hy}
        stroke={GRAY} strokeWidth={3.5} strokeLinecap="round" />

      {/* Minute hand */}
      <line x1={cx} y1={cy} x2={mx} y2={my}
        stroke={BLUE} strokeWidth={2} strokeLinecap="round" />

      {/* Center dot */}
      <circle cx={cx} cy={cy} r={3} fill={GRAY} />
    </svg>
  );
}
