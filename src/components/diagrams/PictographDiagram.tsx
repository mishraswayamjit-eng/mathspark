import React from 'react';

interface Props {
  icon: 'candle' | 'star' | 'apple';
  count: number;
  label?: string;
}

const COLORS = {
  candle: { body: '#FF9600', flame: '#FF4B4B', wick: '#374151' },
  star: { fill: '#DAA520' },
  apple: { fill: '#FF4B4B', stem: '#58CC02' },
};

function Candle({ x, y }: { x: number; y: number }) {
  return (
    <g>
      <rect x={x - 4} y={y} width={8} height={22} rx={2} fill={COLORS.candle.body} />
      <line x1={x} y1={y} x2={x} y2={y - 4} stroke={COLORS.candle.wick} strokeWidth={1} />
      <ellipse cx={x} cy={y - 7} rx={4} ry={6} fill={COLORS.candle.flame} />
      <ellipse cx={x} cy={y - 8} rx={2} ry={3} fill="#FFD700" />
    </g>
  );
}

function StarIcon({ x, y }: { x: number; y: number }) {
  const r = 10;
  const points: string[] = [];
  for (let i = 0; i < 5; i++) {
    const outerAngle = (i * 72 - 90) * Math.PI / 180;
    const innerAngle = ((i * 72 + 36) - 90) * Math.PI / 180;
    points.push(`${x + r * Math.cos(outerAngle)},${y + r * Math.sin(outerAngle)}`);
    points.push(`${x + r * 0.4 * Math.cos(innerAngle)},${y + r * 0.4 * Math.sin(innerAngle)}`);
  }
  return <polygon points={points.join(' ')} fill={COLORS.star.fill} />;
}

function AppleIcon({ x, y }: { x: number; y: number }) {
  return (
    <g>
      <circle cx={x - 4} cy={y + 4} r={8} fill={COLORS.apple.fill} />
      <circle cx={x + 4} cy={y + 4} r={8} fill={COLORS.apple.fill} />
      <line x1={x} y1={y - 6} x2={x + 2} y2={y - 10} stroke={COLORS.apple.stem} strokeWidth={2} />
    </g>
  );
}

export default function PictographDiagram({ icon, count, label }: Props) {
  const cols = Math.min(count, 6);
  const rows = Math.ceil(count / cols);
  const gap = 36;
  const totalW = cols * gap;
  const offsetX = (280 - totalW) / 2 + gap / 2;
  const totalH = rows * 40 + (label ? 20 : 0) + 20;

  const renderIcon = (x: number, y: number, key: number) => {
    switch (icon) {
      case 'candle': return <Candle key={key} x={x} y={y} />;
      case 'star': return <StarIcon key={key} x={x} y={y} />;
      case 'apple': return <AppleIcon key={key} x={x} y={y} />;
    }
  };

  return (
    <svg viewBox={`0 0 280 ${totalH}`} className="w-full" role="img" aria-label={`Pictograph showing ${count} ${icon}s`}>
      {label && (
        <text x={140} y={14} textAnchor="middle" fontSize={10} fontWeight={600} fill="#374151">{label}</text>
      )}
      {Array.from({ length: count }, (_, i) => {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = offsetX + col * gap;
        const y = (label ? 30 : 15) + row * 40;
        return renderIcon(x, y, i);
      })}
    </svg>
  );
}
