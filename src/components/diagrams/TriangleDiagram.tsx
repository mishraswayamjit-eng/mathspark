import React from 'react';

interface VertexSpec {
  x: number;
  y: number;
  label?: string;
}

interface Props {
  variant: 'countTriangles' | 'countSquares' | 'labeled' | 'rightTriangle';
  subdivisions?: number;
  answer?: number;
  vertices?: VertexSpec[];
  lines?: Array<{ x1: number; y1: number; x2: number; y2: number }>;
  labels?: Array<{ text: string; x: number; y: number }>;
}

const GRAY = '#374151';
const BLUE = '#1CB0F6';

/**
 * Generates lines for a triangle subdivided into n rows.
 * An equilateral triangle with n subdivisions has:
 * - n(n+2) small triangles
 * - Total triangles count varies by n
 */
function subdividedTriangleLines(n: number) {
  // Equilateral triangle vertices at given scale
  const ax = 140, ay = 15;  // top
  const bx = 40, by = 145;  // bottom-left
  const cx = 240, cy = 145; // bottom-right

  const lines: Array<{ x1: number; y1: number; x2: number; y2: number }> = [];

  // Outer triangle
  lines.push({ x1: ax, y1: ay, x2: bx, y2: by });
  lines.push({ x1: bx, y1: by, x2: cx, y2: cy });
  lines.push({ x1: cx, y1: cy, x2: ax, y2: ay });

  // Horizontal lines (parallel to base)
  for (let i = 1; i < n; i++) {
    const t = i / n;
    const lx = ax + (bx - ax) * t;
    const ly = ay + (by - ay) * t;
    const rx = ax + (cx - ax) * t;
    const ry = ay + (cy - ay) * t;
    lines.push({ x1: lx, y1: ly, x2: rx, y2: ry });
  }

  // Lines parallel to left side (bottom-left to top)
  for (let i = 1; i < n; i++) {
    const t = i / n;
    const baseX = bx + (cx - bx) * t;
    const topX = ax + (cx - ax) * t;
    const topY = ay + (cy - ay) * t;
    // From base point going parallel to left side
    lines.push({ x1: baseX, y1: by, x2: topX, y2: topY });
  }

  // Lines parallel to right side (bottom-right to top)
  for (let i = 1; i < n; i++) {
    const t = i / n;
    const baseX = bx + (cx - bx) * (1 - t);
    const topX = ax + (bx - ax) * t;
    const topY = ay + (by - ay) * t;
    // From base point going parallel to right side
    lines.push({ x1: baseX, y1: by, x2: topX, y2: topY });
  }

  return lines;
}

function CountTrianglesDiagram({ subdivisions = 2, answer }: Props) {
  const lines = subdividedTriangleLines(subdivisions);

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label={`Triangle subdivided into ${subdivisions} rows — count the triangles`}>
      {lines.map((l, i) => (
        <line key={i} x1={l.x1} y1={l.y1} x2={l.x2} y2={l.y2}
          stroke={GRAY} strokeWidth={2} strokeLinecap="round" />
      ))}
      {answer && (
        <text x={140} y={155} textAnchor="middle" fontSize={10} fill="#6B7280" fontWeight={600}>
          Count all triangles!
        </text>
      )}
    </svg>
  );
}

function CountSquaresDiagram({ answer }: Props) {
  // 2×2 grid of squares (gives 4 small + 1 large = 5)
  const sx = 65, sy = 15, size = 60;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Grid of squares — count all squares">
      {/* 2×2 grid */}
      <rect x={sx} y={sy} width={size * 2} height={size * 2} fill="none" stroke={GRAY} strokeWidth={2} />
      <line x1={sx + size} y1={sy} x2={sx + size} y2={sy + size * 2} stroke={GRAY} strokeWidth={2} />
      <line x1={sx} y1={sy + size} x2={sx + size * 2} y2={sy + size} stroke={GRAY} strokeWidth={2} />
      {answer && (
        <text x={140} y={150} textAnchor="middle" fontSize={10} fill="#6B7280" fontWeight={600}>
          Count all squares!
        </text>
      )}
    </svg>
  );
}

function LabeledTriangleDiagram({ vertices, lines, labels }: Props) {
  const verts = vertices ?? [
    { x: 140, y: 15, label: 'A' },
    { x: 40, y: 140, label: 'B' },
    { x: 240, y: 140, label: 'C' },
  ];

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Labeled triangle">
      {/* Triangle sides */}
      {verts.map((v, i) => {
        const next = verts[(i + 1) % verts.length];
        return (
          <line key={i} x1={v.x} y1={v.y} x2={next.x} y2={next.y}
            stroke={GRAY} strokeWidth={2} />
        );
      })}
      {/* Extra lines */}
      {lines?.map((l, i) => (
        <line key={`el-${i}`} x1={l.x1} y1={l.y1} x2={l.x2} y2={l.y2}
          stroke={GRAY} strokeWidth={1.5} strokeDasharray="4,3" />
      ))}
      {/* Vertex labels */}
      {verts.map((v, i) => v.label && (
        <text key={`vl-${i}`} x={v.x} y={v.y - 8} textAnchor="middle"
          fontSize={12} fontWeight={700} fill={GRAY}>{v.label}</text>
      ))}
      {/* Extra labels */}
      {labels?.map((l, i) => (
        <text key={`l-${i}`} x={l.x} y={l.y} fontSize={11} fontWeight={600}
          fill={BLUE} textAnchor="middle">{l.text}</text>
      ))}
    </svg>
  );
}

export default function TriangleDiagram(props: Props) {
  switch (props.variant) {
    case 'countTriangles': return <CountTrianglesDiagram {...props} />;
    case 'countSquares': return <CountSquaresDiagram {...props} />;
    case 'labeled':
    case 'rightTriangle':
      return <LabeledTriangleDiagram {...props} />;
    default: return <CountTrianglesDiagram {...props} />;
  }
}
