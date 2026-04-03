import React from 'react';

interface SideLabel {
  text: string;
  side: number; // 0-indexed side between vertex[side] and vertex[side+1]
}

interface Props {
  sides: number;
  labels: SideLabel[];
}

const BLUE = '#1CB0F6';
const GRAY = '#374151';

export default function PolygonDiagram({ sides, labels }: Props) {
  const cx = 140;
  const cy = 80;
  const r = 60;

  // Generate vertices for regular polygon, starting from top
  const vertices: Array<{ x: number; y: number }> = [];
  for (let i = 0; i < sides; i++) {
    const angle = (2 * Math.PI * i) / sides - Math.PI / 2;
    vertices.push({
      x: cx + r * Math.cos(angle),
      y: cy + r * Math.sin(angle),
    });
  }

  // Build polygon points string
  const pointsStr = vertices.map(v => `${v.x},${v.y}`).join(' ');

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label={`${sides}-sided polygon`}>
      <polygon points={pointsStr} fill="rgba(28,176,246,0.1)" stroke={GRAY} strokeWidth={2} />

      {/* Vertex dots */}
      {vertices.map((v, i) => (
        <circle key={i} cx={v.x} cy={v.y} r={2.5} fill={GRAY} />
      ))}

      {/* Side labels */}
      {labels.map((lbl, i) => {
        const v1 = vertices[lbl.side % sides];
        const v2 = vertices[(lbl.side + 1) % sides];
        const mx = (v1.x + v2.x) / 2;
        const my = (v1.y + v2.y) / 2;
        // Push label outward from center
        const dx = mx - cx;
        const dy = my - cy;
        const dist = Math.sqrt(dx * dx + dy * dy) || 1;
        const push = 14;
        const lx = mx + (dx / dist) * push;
        const ly = my + (dy / dist) * push;

        return (
          <text key={i} x={lx} y={ly + 4} textAnchor="middle"
            fontSize={9} fontWeight={600} fill={BLUE}>
            {lbl.text}
          </text>
        );
      })}
    </svg>
  );
}
