import React from 'react';

interface LabelSpec {
  text: string;
  x: number;
  y: number;
}

interface Props {
  variant: 'sector' | 'inscribed' | 'twoCirclesOnDiameter' | 'semicircles' | 'circleInSquare' | 'fourCirclesInSquare' | 'segment' | 'twoDiameters';
  radius?: number;
  angle?: number;
  labels?: LabelSpec[];
  shaded?: string;
  dimensions?: Record<string, string>;
}

const BLUE = '#1CB0F6';
const BLUE_FILL = 'rgba(28,176,246,0.2)';
const GRAY = '#374151';

function polarX(cx: number, r: number, deg: number) {
  return cx + r * Math.cos((deg * Math.PI) / 180);
}
function polarY(cy: number, r: number, deg: number) {
  return cy - r * Math.sin((deg * Math.PI) / 180);
}

function SectorDiagram({ radius = 10, angle = 90, labels, dimensions }: Props) {
  const cx = 140, cy = 90, r = 60;
  const startDeg = 0;
  const endDeg = angle;
  const x1 = polarX(cx, r, startDeg);
  const y1 = polarY(cy, r, startDeg);
  const x2 = polarX(cx, r, endDeg);
  const y2 = polarY(cy, r, endDeg);
  const large = angle > 180 ? 1 : 0;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label={`Circle with ${angle}° sector shaded`}>
      <circle cx={cx} cy={cy} r={r} fill="white" stroke="#9CA3AF" strokeWidth={1.5} />
      <path
        d={`M${cx},${cy} L${x1},${y1} A${r},${r} 0 ${large},0 ${x2},${y2} Z`}
        fill={BLUE_FILL}
        stroke={BLUE}
        strokeWidth={2}
      />
      <circle cx={cx} cy={cy} r={2.5} fill={GRAY} />
      {labels?.map((l, i) => (
        <text key={i} x={l.x} y={l.y} fontSize={12} fontWeight={700} fill={GRAY} textAnchor="middle">{l.text}</text>
      ))}
      {dimensions && Object.entries(dimensions).map(([key, val], i) => (
        <text key={`d-${i}`} x={cx} y={155 - i * 14} fontSize={10} fill="#6B7280" textAnchor="middle">{key} = {val}</text>
      ))}
    </svg>
  );
}

function CircleInSquareDiagram({ radius = 14, labels, dimensions }: Props) {
  const cx = 140, cy = 80, r = 55;
  const side = r * 2 + 8;
  const sx = cx - side / 2, sy = cy - side / 2;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Circle inscribed in square">
      <rect x={sx} y={sy} width={side} height={side} fill={BLUE_FILL} stroke={GRAY} strokeWidth={1.5} rx={2} />
      <circle cx={cx} cy={cy} r={r} fill="white" stroke={BLUE} strokeWidth={2} />
      <circle cx={cx} cy={cy} r={2} fill={GRAY} />
      {labels?.map((l, i) => (
        <text key={i} x={l.x} y={l.y} fontSize={12} fontWeight={700} fill={GRAY} textAnchor="middle">{l.text}</text>
      ))}
      {dimensions && Object.entries(dimensions).map(([key, val], i) => (
        <text key={`d-${i}`} x={cx} y={150 - i * 14} fontSize={10} fill="#6B7280" textAnchor="middle">{key} = {val}</text>
      ))}
    </svg>
  );
}

function FourCirclesInSquareDiagram({ labels }: Props) {
  const s = 120;
  const sx = 70, sy = 20;
  const r = s / 2;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Square with 4 quarter-circles at corners">
      <rect x={sx} y={sy} width={s} height={s} fill={BLUE_FILL} stroke={GRAY} strokeWidth={1.5} />
      {/* Four quarter circles at corners */}
      {[[sx, sy], [sx + s, sy], [sx + s, sy + s], [sx, sy + s]].map(([x, y], i) => (
        <circle key={i} cx={x} cy={y} r={r} fill="white" stroke={BLUE} strokeWidth={1.5} />
      ))}
      {/* Re-draw square outline on top */}
      <rect x={sx} y={sy} width={s} height={s} fill="none" stroke={GRAY} strokeWidth={1.5} />
      {labels?.map((l, i) => (
        <text key={i} x={l.x} y={l.y} fontSize={11} fontWeight={700} fill={GRAY} textAnchor="middle">{l.text}</text>
      ))}
    </svg>
  );
}

function TwoCirclesOnDiameterDiagram({ labels, dimensions }: Props) {
  const cx = 140, cy = 80, R = 60, r = 30;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Large circle with two smaller circles on diameter">
      <circle cx={cx} cy={cy} r={R} fill={BLUE_FILL} stroke={BLUE} strokeWidth={2} />
      <circle cx={cx - r} cy={cy} r={r} fill="white" stroke="#9CA3AF" strokeWidth={1.5} />
      <circle cx={cx + r} cy={cy} r={r} fill="white" stroke="#9CA3AF" strokeWidth={1.5} />
      <line x1={cx - R} y1={cy} x2={cx + R} y2={cy} stroke={GRAY} strokeWidth={1} strokeDasharray="4,3" />
      <circle cx={cx} cy={cy} r={2} fill={GRAY} />
      {labels?.map((l, i) => (
        <text key={i} x={l.x} y={l.y} fontSize={12} fontWeight={700} fill={GRAY} textAnchor="middle">{l.text}</text>
      ))}
      {dimensions && Object.entries(dimensions).map(([key, val], i) => (
        <text key={`d-${i}`} x={cx} y={150 - i * 14} fontSize={10} fill="#6B7280" textAnchor="middle">{key} = {val}</text>
      ))}
    </svg>
  );
}

function SemicirclesDiagram({ labels, dimensions }: Props) {
  // Yin-yang style: large semicircle with 3 smaller semicircles
  const cx = 140, cy = 80, R = 60;

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Semicircle diagram (Yin-Yang style)">
      {/* Large semicircle (upper half) */}
      <path
        d={`M${cx - R},${cy} A${R},${R} 0 1,1 ${cx + R},${cy} Z`}
        fill={BLUE_FILL}
        stroke={BLUE}
        strokeWidth={2}
      />
      {/* Lower half outline */}
      <path
        d={`M${cx - R},${cy} A${R},${R} 0 1,0 ${cx + R},${cy}`}
        fill="none"
        stroke="#9CA3AF"
        strokeWidth={1.5}
      />
      {/* Small semicircles along the diameter */}
      <path d={`M${cx - R},${cy} A${R / 3},${R / 3} 0 1,1 ${cx - R / 3},${cy}`} fill="white" stroke="#9CA3AF" strokeWidth={1} />
      <path d={`M${cx - R / 3},${cy} A${R / 3},${R / 3} 0 1,0 ${cx + R / 3},${cy}`} fill={BLUE_FILL} stroke={BLUE} strokeWidth={1} />
      <path d={`M${cx + R / 3},${cy} A${R / 3},${R / 3} 0 1,1 ${cx + R},${cy}`} fill="white" stroke="#9CA3AF" strokeWidth={1} />
      {labels?.map((l, i) => (
        <text key={i} x={l.x} y={l.y} fontSize={12} fontWeight={700} fill={GRAY} textAnchor="middle">{l.text}</text>
      ))}
      {dimensions && Object.entries(dimensions).map(([key, val], i) => (
        <text key={`d-${i}`} x={cx} y={155 - i * 14} fontSize={10} fill="#6B7280" textAnchor="middle">{key} = {val}</text>
      ))}
    </svg>
  );
}

function SegmentDiagram({ angle = 90, labels, dimensions }: Props) {
  const cx = 140, cy = 90, r = 60;
  const a1 = 90 + angle / 2;
  const a2 = 90 - angle / 2;
  const x1 = polarX(cx, r, a1);
  const y1 = polarY(cy, r, a1);
  const x2 = polarX(cx, r, a2);
  const y2 = polarY(cy, r, a2);

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label={`Circle with segment shaded (${angle}°)`}>
      <circle cx={cx} cy={cy} r={r} fill="white" stroke="#9CA3AF" strokeWidth={1.5} />
      {/* Shaded segment: arc + chord */}
      <path
        d={`M${x1},${y1} A${r},${r} 0 0,1 ${x2},${y2} Z`}
        fill={BLUE_FILL}
        stroke={BLUE}
        strokeWidth={2}
      />
      {/* Chord */}
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={BLUE} strokeWidth={1.5} />
      {/* Radii */}
      <line x1={cx} y1={cy} x2={x1} y2={y1} stroke={GRAY} strokeWidth={1} strokeDasharray="4,3" />
      <line x1={cx} y1={cy} x2={x2} y2={y2} stroke={GRAY} strokeWidth={1} strokeDasharray="4,3" />
      <circle cx={cx} cy={cy} r={2} fill={GRAY} />
      {labels?.map((l, i) => (
        <text key={i} x={l.x} y={l.y} fontSize={12} fontWeight={700} fill={GRAY} textAnchor="middle">{l.text}</text>
      ))}
      {dimensions && Object.entries(dimensions).map(([key, val], i) => (
        <text key={`d-${i}`} x={cx} y={155 - i * 14} fontSize={10} fill="#6B7280" textAnchor="middle">{key} = {val}</text>
      ))}
    </svg>
  );
}

function TwoDiametersDiagram({ angle = 120, labels, dimensions }: Props) {
  const cx = 140, cy = 80, r = 60;
  // Two diameters at given angle
  const halfAngle = angle / 2;
  const x1 = polarX(cx, r, 0), y1 = polarY(cy, r, 0);
  const x2 = polarX(cx, r, 180), y2 = polarY(cy, r, 180);
  const x3 = polarX(cx, r, halfAngle), y3 = polarY(cy, r, halfAngle);
  const x4 = polarX(cx, r, 180 + halfAngle), y4 = polarY(cy, r, 180 + halfAngle);

  return (
    <svg viewBox="0 0 280 160" className="w-full" role="img" aria-label="Circle with two diameters">
      <circle cx={cx} cy={cy} r={r} fill="white" stroke="#9CA3AF" strokeWidth={1.5} />
      {/* Two diameters */}
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={GRAY} strokeWidth={1.5} />
      <line x1={x3} y1={y3} x2={x4} y2={y4} stroke={GRAY} strokeWidth={1.5} />
      {/* Shaded opposite segments */}
      <path
        d={`M${x1},${y1} A${r},${r} 0 0,0 ${x3},${y3} L${cx},${cy} Z`}
        fill={BLUE_FILL} stroke={BLUE} strokeWidth={1.5}
      />
      <path
        d={`M${x2},${y2} A${r},${r} 0 0,0 ${x4},${y4} L${cx},${cy} Z`}
        fill={BLUE_FILL} stroke={BLUE} strokeWidth={1.5}
      />
      <circle cx={cx} cy={cy} r={2.5} fill={GRAY} />
      {labels?.map((l, i) => (
        <text key={i} x={l.x} y={l.y} fontSize={12} fontWeight={700} fill={GRAY} textAnchor="middle">{l.text}</text>
      ))}
      {dimensions && Object.entries(dimensions).map(([key, val], i) => (
        <text key={`d-${i}`} x={cx} y={155 - i * 14} fontSize={10} fill="#6B7280" textAnchor="middle">{key} = {val}</text>
      ))}
    </svg>
  );
}

export default function CircleDiagram(props: Props) {
  switch (props.variant) {
    case 'sector': return <SectorDiagram {...props} />;
    case 'circleInSquare': return <CircleInSquareDiagram {...props} />;
    case 'fourCirclesInSquare': return <FourCirclesInSquareDiagram {...props} />;
    case 'twoCirclesOnDiameter': return <TwoCirclesOnDiameterDiagram {...props} />;
    case 'semicircles': return <SemicirclesDiagram {...props} />;
    case 'segment': return <SegmentDiagram {...props} />;
    case 'twoDiameters': return <TwoDiametersDiagram {...props} />;
    default: return <SectorDiagram {...props} />;
  }
}
