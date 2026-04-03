import React from 'react';

interface CurrencyItem {
  type: 'coin' | 'note';
  value: string;
}

interface Props {
  items: CurrencyItem[];
}

const GRAY = '#374151';

function coinColor(value: string): string {
  if (value.includes('p')) return '#B87333'; // copper for paise
  return '#DAA520'; // gold for rupee coins
}

export default function CurrencyDiagram({ items }: Props) {
  const cols = Math.min(items.length, 4);
  const rows = Math.ceil(items.length / cols);
  const cellW = 60;
  const cellH = 50;
  const offsetX = (280 - cols * cellW) / 2;
  const totalH = rows * cellH + 20;

  return (
    <svg viewBox={`0 0 280 ${totalH}`} className="w-full" role="img" aria-label="Currency diagram">
      {items.map((item, i) => {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const cx = offsetX + col * cellW + cellW / 2;
        const cy = 10 + row * cellH + cellH / 2;

        return (
          <g key={i}>
            {item.type === 'coin' ? (
              <>
                <circle cx={cx} cy={cy} r={18} fill={coinColor(item.value)} stroke="#8B6914" strokeWidth={1.5} />
                <text x={cx} y={cy + 4} textAnchor="middle" fontSize={9} fontWeight={700} fill="white">
                  {item.value}
                </text>
              </>
            ) : (
              <>
                <rect x={cx - 24} y={cy - 12} width={48} height={24} rx={3}
                  fill="#4CAF50" stroke="#388E3C" strokeWidth={1.5} />
                <text x={cx} y={cy + 4} textAnchor="middle" fontSize={9} fontWeight={700} fill="white">
                  {item.value}
                </text>
              </>
            )}
            {/* Plus sign between items (not after last) */}
            {i < items.length - 1 && col < cols - 1 && (
              <text x={cx + cellW / 2} y={cy + 4} textAnchor="middle" fontSize={12} fontWeight={700} fill={GRAY}>
                +
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}
