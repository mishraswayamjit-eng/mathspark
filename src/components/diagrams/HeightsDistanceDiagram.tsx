import React from 'react';

interface Props {
  variant: 'cliff-tower' | 'cliff-boat';
  heights: { cliff: number; tower?: number };
  angles: number[];
  labels?: Record<string, string>;
}

const BLUE = '#1CB0F6';
const GRAY = '#374151';

function arcPath(cx: number, cy: number, r: number, startDeg: number, endDeg: number): string {
  const s = (startDeg * Math.PI) / 180;
  const e = (endDeg * Math.PI) / 180;
  const x1 = cx + r * Math.cos(s);
  const y1 = cy - r * Math.sin(s);
  const x2 = cx + r * Math.cos(e);
  const y2 = cy - r * Math.sin(e);
  const largeArc = Math.abs(endDeg - startDeg) > 180 ? 1 : 0;
  return `M${x1},${y1} A${r},${r} 0 ${largeArc},0 ${x2},${y2}`;
}

export default function HeightsDistanceDiagram({ variant, heights, angles, labels = {} }: Props) {
  if (variant === 'cliff-tower') {
    // Left: cliff, Right: tower, dashed sight lines with angles
    const groundY = 130;
    const cliffX = 60;
    const towerX = 220;
    const cliffTop = 40;
    const towerTop = 20;
    const towerBase = groundY;

    return (
      <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Cliff and tower heights diagram">
        {/* Ground line */}
        <line x1={20} y1={groundY} x2={260} y2={groundY} stroke={GRAY} strokeWidth={1.5} />

        {/* Cliff */}
        <rect x={cliffX - 20} y={cliffTop} width={40} height={groundY - cliffTop}
          fill="rgba(28,176,246,0.15)" stroke={GRAY} strokeWidth={1.5} />

        {/* Tower */}
        <rect x={towerX - 15} y={towerTop} width={30} height={towerBase - towerTop}
          fill="rgba(255,150,0,0.15)" stroke={GRAY} strokeWidth={1.5} />

        {/* Horizontal dashed line from cliff top */}
        <line x1={cliffX} y1={cliffTop} x2={towerX} y2={cliffTop}
          stroke="#9CA3AF" strokeWidth={1} strokeDasharray="4,3" />

        {/* Sight line to tower top (angle of elevation) */}
        <line x1={cliffX} y1={cliffTop} x2={towerX} y2={towerTop}
          stroke={BLUE} strokeWidth={1.5} strokeDasharray="5,3" />

        {/* Sight line to tower base (angle of depression) */}
        <line x1={cliffX} y1={cliffTop} x2={towerX} y2={groundY}
          stroke={BLUE} strokeWidth={1.5} strokeDasharray="5,3" />

        {/* Angle arcs */}
        {angles[0] !== undefined && (
          <g>
            <path d={arcPath(cliffX, cliffTop, 25, 330, 360)} fill="none" stroke={BLUE} strokeWidth={1.5} />
            <text x={cliffX + 35} y={cliffTop + 6} fontSize={9} fontWeight={600} fill={BLUE}>{angles[0]}°</text>
          </g>
        )}
        {angles[1] !== undefined && (
          <g>
            <path d={arcPath(cliffX, cliffTop, 30, 0, 25)} fill="none" stroke={BLUE} strokeWidth={1.5} />
            <text x={cliffX + 40} y={cliffTop - 8} fontSize={9} fontWeight={600} fill={BLUE}>{angles[1]}°</text>
          </g>
        )}

        {/* Height labels */}
        <text x={cliffX - 28} y={(cliffTop + groundY) / 2 + 4} textAnchor="middle"
          fontSize={9} fontWeight={600} fill={GRAY}>
          {labels.cliff || `${heights.cliff}m`}
        </text>
        {heights.tower !== undefined && (
          <text x={towerX + 24} y={(towerTop + groundY) / 2 + 4} textAnchor="middle"
            fontSize={9} fontWeight={600} fill={GRAY}>
            {labels.tower || `${heights.tower}m`}
          </text>
        )}
      </svg>
    );
  }

  // cliff-boat variant
  const groundY = 130;
  const cliffX = 60;
  const boatX1 = 170;
  const boatX2 = 230;
  const cliffTop = 30;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Cliff and boat heights diagram">
      {/* Water line */}
      <line x1={20} y1={groundY} x2={260} y2={groundY} stroke="#60A5FA" strokeWidth={2} />
      {/* Water wave hints */}
      <path d="M80,135 Q95,130 110,135 Q125,140 140,135 Q155,130 170,135 Q185,140 200,135 Q215,130 230,135 Q245,140 260,135"
        fill="none" stroke="#93C5FD" strokeWidth={1} />

      {/* Cliff / Rock */}
      <rect x={cliffX - 20} y={cliffTop} width={40} height={groundY - cliffTop}
        fill="rgba(28,176,246,0.15)" stroke={GRAY} strokeWidth={1.5} />

      {/* Boat icons (simple) */}
      <path d={`M${boatX1 - 10},${groundY - 4} Q${boatX1},${groundY + 6} ${boatX1 + 10},${groundY - 4}`}
        fill="#FF9600" stroke="#E08600" strokeWidth={1} />
      <path d={`M${boatX2 - 10},${groundY - 4} Q${boatX2},${groundY + 6} ${boatX2 + 10},${groundY - 4}`}
        fill="#FF9600" stroke="#E08600" strokeWidth={1} />

      {/* Sight lines */}
      <line x1={cliffX} y1={cliffTop} x2={boatX1} y2={groundY - 5}
        stroke={BLUE} strokeWidth={1.5} strokeDasharray="5,3" />
      <line x1={cliffX} y1={cliffTop} x2={boatX2} y2={groundY - 5}
        stroke={BLUE} strokeWidth={1.5} strokeDasharray="5,3" />

      {/* Horizontal dashed from cliff top */}
      <line x1={cliffX} y1={cliffTop} x2={250} y2={cliffTop}
        stroke="#9CA3AF" strokeWidth={1} strokeDasharray="4,3" />

      {/* Angle arcs (depression angles) */}
      {angles[0] !== undefined && (
        <g>
          <path d={arcPath(cliffX, cliffTop, 30, 315, 360)} fill="none" stroke={BLUE} strokeWidth={1.5} />
          <text x={cliffX + 40} y={cliffTop + 10} fontSize={9} fontWeight={600} fill={BLUE}>{angles[0]}°</text>
        </g>
      )}
      {angles[1] !== undefined && (
        <g>
          <path d={arcPath(cliffX, cliffTop, 40, 340, 360)} fill="none" stroke={BLUE} strokeWidth={1.5} />
          <text x={cliffX + 50} y={cliffTop - 2} fontSize={9} fontWeight={600} fill={BLUE}>{angles[1]}°</text>
        </g>
      )}

      {/* Height label */}
      <text x={cliffX - 28} y={(cliffTop + groundY) / 2 + 4} textAnchor="middle"
        fontSize={9} fontWeight={600} fill={GRAY}>
        {labels?.cliff || `${heights.cliff}m`}
      </text>

      {/* Boat labels */}
      <text x={boatX1} y={groundY + 16} textAnchor="middle" fontSize={8} fontWeight={600} fill={GRAY}>
        {labels?.boat1 || 'B₁'}
      </text>
      <text x={boatX2} y={groundY + 16} textAnchor="middle" fontSize={8} fontWeight={600} fill={GRAY}>
        {labels?.boat2 || 'B₂'}
      </text>
    </svg>
  );
}
