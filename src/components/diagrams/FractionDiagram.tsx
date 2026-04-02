import React from 'react';

interface Props {
  shape: 'rectangle' | 'circle' | 'triangle';
  totalParts: number;
  shadedParts: number;
  columns?: number;
  label?: string;
}

const SHADED = '#1CB0F6';
const SHADED_LIGHT = 'rgba(28,176,246,0.2)';
const UNSHADED = '#F3F4F6';
const STROKE = '#9CA3AF';

function RectGrid({ totalParts, shadedParts, columns = 4 }: Props) {
  const rows = Math.ceil(totalParts / columns);
  const cellW = 240 / columns;
  const cellH = Math.min(40, 120 / rows);
  const w = columns * cellW;
  const h = rows * cellH;

  return (
    <svg viewBox={`0 0 ${w + 8} ${h + 8}`} className="w-full" role="img" aria-label={`Rectangle divided into ${totalParts} equal parts with ${shadedParts} shaded`}>
      {Array.from({ length: totalParts }, (_, i) => {
        const col = i % columns;
        const row = Math.floor(i / columns);
        const filled = i < shadedParts;
        return (
          <rect
            key={i}
            x={4 + col * cellW}
            y={4 + row * cellH}
            width={cellW - 2}
            height={cellH - 2}
            rx={3}
            fill={filled ? SHADED_LIGHT : UNSHADED}
            stroke={filled ? SHADED : STROKE}
            strokeWidth={1.5}
          />
        );
      })}
    </svg>
  );
}

function CirclePie({ totalParts, shadedParts }: Props) {
  const cx = 70, cy = 70, r = 60;
  const angleStep = (2 * Math.PI) / totalParts;

  function slicePath(i: number) {
    const a1 = i * angleStep - Math.PI / 2;
    const a2 = (i + 1) * angleStep - Math.PI / 2;
    const x1 = cx + r * Math.cos(a1);
    const y1 = cy + r * Math.sin(a1);
    const x2 = cx + r * Math.cos(a2);
    const y2 = cy + r * Math.sin(a2);
    const large = angleStep > Math.PI ? 1 : 0;
    return `M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${large},1 ${x2},${y2} Z`;
  }

  return (
    <svg viewBox="0 0 140 140" className="w-full max-w-[140px] mx-auto" role="img" aria-label={`Circle divided into ${totalParts} equal parts with ${shadedParts} shaded`}>
      {Array.from({ length: totalParts }, (_, i) => (
        <path
          key={i}
          d={slicePath(i)}
          fill={i < shadedParts ? SHADED_LIGHT : UNSHADED}
          stroke={i < shadedParts ? SHADED : STROKE}
          strokeWidth={1.5}
        />
      ))}
    </svg>
  );
}

function TriangleFraction({ totalParts, shadedParts }: Props) {
  // Simple row-based triangle: row n has n cells
  const rows = Math.ceil(Math.sqrt(totalParts));
  const size = 140;
  let idx = 0;

  return (
    <svg viewBox={`0 0 ${size} ${size}`} className="w-full max-w-[140px] mx-auto" role="img" aria-label={`Triangle divided into ${totalParts} equal parts with ${shadedParts} shaded`}>
      {Array.from({ length: rows }, (_, row) => {
        const cellsInRow = row + 1;
        const rowY = 10 + (row * (size - 20)) / rows;
        const rowH = (size - 20) / rows;
        const rowW = ((row + 1) / rows) * (size - 20);
        const startX = (size - rowW) / 2;
        const cellW = rowW / cellsInRow;

        return Array.from({ length: cellsInRow }, (_, col) => {
          if (idx >= totalParts) return null;
          const filled = idx < shadedParts;
          idx++;
          return (
            <rect
              key={`${row}-${col}`}
              x={startX + col * cellW}
              y={rowY}
              width={cellW - 2}
              height={rowH - 2}
              rx={2}
              fill={filled ? SHADED_LIGHT : UNSHADED}
              stroke={filled ? SHADED : STROKE}
              strokeWidth={1.5}
            />
          );
        });
      })}
    </svg>
  );
}

export default function FractionDiagram(props: Props) {
  return (
    <div>
      {props.shape === 'rectangle' && <RectGrid {...props} />}
      {props.shape === 'circle' && <CirclePie {...props} />}
      {props.shape === 'triangle' && <TriangleFraction {...props} />}
      {props.label && (
        <p className="text-center text-xs font-semibold text-gray-500 mt-1">{props.label}</p>
      )}
    </div>
  );
}
