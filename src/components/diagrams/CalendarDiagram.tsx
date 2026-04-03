import React from 'react';

interface Props {
  month: string;
  year: number;
  startDay: number; // 0=Sun, 1=Mon, ..., 6=Sat
  daysInMonth: number;
  highlight?: number[];
}

const BLUE = '#1CB0F6';
const BLUE_FILL = 'rgba(28,176,246,0.2)';
const GRAY = '#374151';
const DAYS = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

export default function CalendarDiagram({ month, year, startDay, daysInMonth, highlight = [] }: Props) {
  const cellW = 36;
  const cellH = 24;
  const offsetX = (280 - 7 * cellW) / 2;
  const headerH = 22;
  const dayHeaderH = 20;
  const startY = headerH + dayHeaderH;

  const rows: (number | null)[][] = [];
  let week: (number | null)[] = Array(startDay).fill(null);
  for (let d = 1; d <= daysInMonth; d++) {
    week.push(d);
    if (week.length === 7) {
      rows.push(week);
      week = [];
    }
  }
  if (week.length > 0) {
    while (week.length < 7) week.push(null);
    rows.push(week);
  }

  const totalH = startY + rows.length * cellH + 6;

  return (
    <svg viewBox={`0 0 280 ${totalH}`} className="w-full" role="img" aria-label={`${month} ${year} calendar`}>
      {/* Month-Year header */}
      <text x={140} y={15} textAnchor="middle" fontSize={11} fontWeight={700} fill={GRAY}>
        {month} {year}
      </text>

      {/* Weekday headers */}
      {DAYS.map((d, i) => (
        <text key={i} x={offsetX + i * cellW + cellW / 2} y={headerH + 14} textAnchor="middle"
          fontSize={9} fontWeight={600} fill="#6B7280">
          {d}
        </text>
      ))}

      {/* Day cells */}
      {rows.map((row, ri) =>
        row.map((day, ci) => {
          if (day === null) return null;
          const x = offsetX + ci * cellW;
          const y = startY + ri * cellH;
          const isHighlighted = highlight.includes(day);
          return (
            <g key={`${ri}-${ci}`}>
              {isHighlighted && (
                <rect x={x + 2} y={y + 2} width={cellW - 4} height={cellH - 4}
                  rx={4} fill={BLUE_FILL} stroke={BLUE} strokeWidth={1} />
              )}
              <text x={x + cellW / 2} y={y + cellH / 2 + 4} textAnchor="middle"
                fontSize={9} fontWeight={isHighlighted ? 700 : 500}
                fill={isHighlighted ? BLUE : GRAY}>
                {day}
              </text>
            </g>
          );
        })
      )}
    </svg>
  );
}
