import React from 'react';

interface LineSpec {
  x1: number; y1: number;
  x2: number; y2: number;
  label?: string;
  parallel?: boolean;
}

interface AngleLabel {
  cx: number; cy: number;
  startAngle: number;
  endAngle: number;
  label: string;
  radius?: number;
}

interface PointLabel {
  x: number; y: number;
  label: string;
}

interface Props {
  lines: LineSpec[];
  angles: AngleLabel[];
  points: PointLabel[];
}

const BLUE = '#1CB0F6';

function arcPath(cx: number, cy: number, r: number, startDeg: number, endDeg: number): string {
  const s = (startDeg * Math.PI) / 180;
  const e = (endDeg * Math.PI) / 180;
  const x1 = cx + r * Math.cos(s);
  const y1 = cy - r * Math.sin(s);
  const x2 = cx + r * Math.cos(e);
  const y2 = cy - r * Math.sin(e);
  const sweep = endDeg - startDeg;
  const largeArc = Math.abs(sweep) > 180 ? 1 : 0;
  // For angles drawn counter-clockwise (startDeg < endDeg), sweep flag = 0
  return `M${x1},${y1} A${r},${r} 0 ${largeArc},0 ${x2},${y2}`;
}

function parallelMarkers(x1: number, y1: number, x2: number, y2: number) {
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.sqrt(dx * dx + dy * dy);
  const ux = dx / len;
  const uy = dy / len;
  const px = -uy * 4;
  const py = ux * 4;
  const s = 5;

  return (
    <g>
      <line x1={mx - s * ux + px} y1={my - s * uy + py} x2={mx + px} y2={my + py} stroke={BLUE} strokeWidth={1.5} />
      <line x1={mx + px} y1={my + py} x2={mx + s * ux + px} y2={my + s * uy + py} stroke={BLUE} strokeWidth={1.5} />
    </g>
  );
}

export default function AngleDiagram({ lines, angles, points }: Props) {
  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Angle diagram">
      {/* Lines */}
      {lines.map((l, i) => (
        <g key={`l-${i}`}>
          <line
            x1={l.x1} y1={l.y1} x2={l.x2} y2={l.y2}
            stroke="#374151" strokeWidth={2} strokeLinecap="round"
          />
          {l.parallel && parallelMarkers(l.x1, l.y1, l.x2, l.y2)}
        </g>
      ))}

      {/* Angle arcs */}
      {angles.map((a, i) => {
        const r = a.radius ?? 20;
        const midDeg = (a.startAngle + a.endAngle) / 2;
        const labelR = r + 12;
        const lx = a.cx + labelR * Math.cos((midDeg * Math.PI) / 180);
        const ly = a.cy - labelR * Math.sin((midDeg * Math.PI) / 180);

        return (
          <g key={`a-${i}`}>
            <path
              d={arcPath(a.cx, a.cy, r, a.startAngle, a.endAngle)}
              fill="none"
              stroke={BLUE}
              strokeWidth={2}
            />
            <text
              x={lx} y={ly + 4}
              textAnchor="middle"
              fontSize={10}
              fontWeight={600}
              fill={BLUE}
            >
              {a.label}
            </text>
          </g>
        );
      })}

      {/* Point labels */}
      {points.map((p, i) => (
        <g key={`p-${i}`}>
          <circle cx={p.x} cy={p.y} r={2.5} fill="#374151" />
          <text
            x={p.x}
            y={p.y - 6}
            textAnchor="middle"
            fontSize={11}
            fontWeight={700}
            fill="#374151"
          >
            {p.label}
          </text>
        </g>
      ))}
    </svg>
  );
}
