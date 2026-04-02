import React from 'react';

interface RectSpec {
  x: number;
  y: number;
  width: number;
  height: number;
  label?: string;
  shaded?: boolean;
}

interface DimensionSpec {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  label: string;
}

interface Props {
  rects: RectSpec[];
  dimensions: DimensionSpec[];
}

const BLUE_FILL = 'rgba(28,176,246,0.2)';
const BLUE = '#1CB0F6';
const GRAY = '#374151';

export default function CompositeShapeDiagram({ rects, dimensions }: Props) {
  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Composite shape with dimensions">
      {rects.map((r, i) => (
        <g key={i}>
          <rect
            x={r.x} y={r.y}
            width={r.width} height={r.height}
            fill={r.shaded ? BLUE_FILL : 'white'}
            stroke={r.shaded ? BLUE : GRAY}
            strokeWidth={r.shaded ? 2 : 1.5}
            rx={2}
          />
          {r.label && (
            <text
              x={r.x + r.width / 2}
              y={r.y + r.height / 2 + 4}
              textAnchor="middle"
              fontSize={9}
              fill="#6B7280"
              fontWeight={600}
            >
              {r.label}
            </text>
          )}
        </g>
      ))}

      {/* Dimension lines */}
      {dimensions.map((d, i) => {
        const isHorizontal = Math.abs(d.y1 - d.y2) < 5;
        const mx = (d.x1 + d.x2) / 2;
        const my = (d.y1 + d.y2) / 2;

        return (
          <g key={`d-${i}`}>
            <line x1={d.x1} y1={d.y1} x2={d.x2} y2={d.y2}
              stroke="#9CA3AF" strokeWidth={1} markerStart="url(#arrowStart)" markerEnd="url(#arrowEnd)" />
            {/* Dimension tick marks */}
            {isHorizontal ? (
              <>
                <line x1={d.x1} y1={d.y1 - 3} x2={d.x1} y2={d.y1 + 3} stroke="#9CA3AF" strokeWidth={1} />
                <line x1={d.x2} y1={d.y2 - 3} x2={d.x2} y2={d.y2 + 3} stroke="#9CA3AF" strokeWidth={1} />
              </>
            ) : (
              <>
                <line x1={d.x1 - 3} y1={d.y1} x2={d.x1 + 3} y2={d.y1} stroke="#9CA3AF" strokeWidth={1} />
                <line x1={d.x2 - 3} y1={d.y2} x2={d.x2 + 3} y2={d.y2} stroke="#9CA3AF" strokeWidth={1} />
              </>
            )}
            <text
              x={isHorizontal ? mx : mx + 8}
              y={isHorizontal ? my - 5 : my + 3}
              textAnchor="middle"
              fontSize={9}
              fill={GRAY}
              fontWeight={600}
            >
              {d.label}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
