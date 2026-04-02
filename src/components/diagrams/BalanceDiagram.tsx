import React from 'react';

interface Item {
  label: string;
  count?: number;
  shape?: 'circle' | 'triangle' | 'square' | 'star';
}

interface ScaleSpec {
  left: Item[];
  right: Item[];
}

interface Props {
  scales: ScaleSpec[];
}

const COLORS = {
  circle: '#1CB0F6',
  triangle: '#FF9600',
  square: '#58CC02',
  star: '#FF4B4B',
};

function ShapeIcon({ shape, x, y }: { shape: string; x: number; y: number }) {
  const color = COLORS[shape as keyof typeof COLORS] || '#6B7280';
  const r = 8;

  switch (shape) {
    case 'triangle':
      return <polygon points={`${x},${y - r} ${x - r},${y + r} ${x + r},${y + r}`} fill={color} stroke={color} strokeWidth={1} />;
    case 'square':
      return <rect x={x - r} y={y - r} width={r * 2} height={r * 2} rx={2} fill={color} />;
    case 'star':
      return <text x={x} y={y + 5} textAnchor="middle" fontSize={16} fill={color}>★</text>;
    default: // circle
      return <circle cx={x} cy={y} r={r} fill={color} />;
  }
}

function renderItems(items: Item[], baseX: number, y: number) {
  const allIcons: React.ReactNode[] = [];
  let offset = 0;
  for (const item of items) {
    const count = item.count ?? 1;
    for (let i = 0; i < count; i++) {
      allIcons.push(
        <ShapeIcon
          key={`${item.label}-${i}-${offset}`}
          shape={item.shape ?? 'circle'}
          x={baseX + offset * 20 - ((count - 1) * 10)}
          y={y}
        />
      );
      offset++;
    }
  }
  return allIcons;
}

function SingleScale({ scale, y }: { scale: ScaleSpec; y: number }) {
  const cx = 140;
  const beamY = y + 10;
  const panY = beamY + 5;
  const fulcrumTop = beamY;
  const fulcrumBottom = beamY + 22;

  return (
    <g>
      {/* Fulcrum triangle */}
      <polygon
        points={`${cx},${fulcrumBottom} ${cx - 12},${fulcrumBottom} ${cx},${fulcrumTop}`}
        fill="#FF9600"
        stroke="#E08600"
        strokeWidth={1}
      />
      <polygon
        points={`${cx},${fulcrumBottom} ${cx + 12},${fulcrumBottom} ${cx},${fulcrumTop}`}
        fill="#FFB84D"
        stroke="#E08600"
        strokeWidth={1}
      />

      {/* Beam */}
      <line x1={40} y1={beamY} x2={240} y2={beamY} stroke="#374151" strokeWidth={2.5} strokeLinecap="round" />

      {/* Left pan */}
      <path d={`M50,${panY} Q70,${panY + 15} 90,${panY}`} fill="none" stroke="#6B7280" strokeWidth={1.5} />
      <line x1={50} y1={beamY} x2={50} y2={panY} stroke="#6B7280" strokeWidth={1} />
      <line x1={90} y1={beamY} x2={90} y2={panY} stroke="#6B7280" strokeWidth={1} />

      {/* Right pan */}
      <path d={`M190,${panY} Q210,${panY + 15} 230,${panY}`} fill="none" stroke="#6B7280" strokeWidth={1.5} />
      <line x1={190} y1={beamY} x2={190} y2={panY} stroke="#6B7280" strokeWidth={1} />
      <line x1={230} y1={beamY} x2={230} y2={panY} stroke="#6B7280" strokeWidth={1} />

      {/* Items on left pan */}
      {renderItems(scale.left, 70, beamY - 15)}

      {/* Items on right pan */}
      {renderItems(scale.right, 210, beamY - 15)}

      {/* Equals sign */}
      <text x={cx} y={beamY - 18} textAnchor="middle" fontSize={14} fontWeight="bold" fill="#374151">=</text>
    </g>
  );
}

export default function BalanceDiagram({ scales }: Props) {
  const scaleHeight = 65;
  const height = scales.length * scaleHeight + 10;

  return (
    <svg viewBox={`0 0 280 ${height}`} className="w-full" role="img" aria-label="Balance scale diagram">
      {scales.map((scale, i) => (
        <SingleScale key={i} scale={scale} y={i * scaleHeight + 5} />
      ))}
    </svg>
  );
}
