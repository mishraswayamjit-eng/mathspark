import React from 'react';

interface Props {
  variant: 'symbols' | 'shapes' | 'dots' | 'blocks';
  sequence: string[];
  showQuestion?: boolean;
}

const BLUE = '#1CB0F6';
const GRAY = '#374151';

function SymbolPattern({ sequence, showQuestion }: Props) {
  return (
    <svg viewBox={`0 0 280 60`} className="w-full" role="img" aria-label="Symbol pattern sequence">
      {sequence.map((item, i) => {
        const x = 20 + i * (240 / sequence.length);
        const isQ = item === '?';
        return (
          <g key={i}>
            <rect
              x={x} y={10}
              width={Math.max(30, 220 / sequence.length)}
              height={40}
              rx={6}
              fill={isQ ? 'rgba(28,176,246,0.1)' : 'white'}
              stroke={isQ ? BLUE : '#D1D5DB'}
              strokeWidth={isQ ? 2 : 1}
            />
            <text
              x={x + Math.max(15, 110 / sequence.length)}
              y={37}
              textAnchor="middle"
              fontSize={isQ ? 18 : 16}
              fontWeight={700}
              fill={isQ ? BLUE : GRAY}
            >
              {item}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function ShapePattern({ sequence }: Props) {
  const shapeMap: Record<string, (x: number, y: number) => React.ReactNode> = {
    '●': (x, y) => <circle cx={x} cy={y} r={8} fill={BLUE} />,
    '■': (x, y) => <rect x={x - 8} y={y - 8} width={16} height={16} rx={2} fill="#FF9600" />,
    '▲': (x, y) => <polygon points={`${x},${y - 9} ${x - 9},${y + 7} ${x + 9},${y + 7}`} fill="#58CC02" />,
    '◇': (x, y) => <polygon points={`${x},${y - 9} ${x + 8},${y} ${x},${y + 9} ${x - 8},${y}`} fill="#FF4B4B" />,
    '★': (x, y) => <text x={x} y={y + 5} textAnchor="middle" fontSize={18} fill="#FF4B4B">★</text>,
    '?': (x, y) => (
      <g>
        <circle cx={x} cy={y} r={12} fill="rgba(28,176,246,0.1)" stroke={BLUE} strokeWidth={2} strokeDasharray="4,3" />
        <text x={x} y={y + 5} textAnchor="middle" fontSize={14} fontWeight={700} fill={BLUE}>?</text>
      </g>
    ),
  };

  return (
    <svg viewBox="0 0 280 60" className="w-full" role="img" aria-label="Shape pattern sequence">
      {sequence.map((item, i) => {
        const x = 30 + i * (220 / sequence.length);
        const renderer = shapeMap[item];
        if (renderer) return <g key={i}>{renderer(x, 30)}</g>;
        // Multi-char items: render as text
        return (
          <text key={i} x={x} y={35} textAnchor="middle" fontSize={12} fontWeight={600} fill={GRAY}>
            {item}
          </text>
        );
      })}
    </svg>
  );
}

function DotPattern({ sequence }: Props) {
  return (
    <svg viewBox="0 0 280 80" className="w-full" role="img" aria-label="Dot/number pattern">
      {sequence.map((item, i) => {
        const x = 30 + i * (220 / sequence.length);
        const isQ = item === '?';
        const num = parseInt(item);

        if (isQ) {
          return (
            <g key={i}>
              <circle cx={x} cy={40} r={16} fill="rgba(28,176,246,0.1)" stroke={BLUE} strokeWidth={2} strokeDasharray="4,3" />
              <text x={x} y={45} textAnchor="middle" fontSize={16} fontWeight={700} fill={BLUE}>?</text>
            </g>
          );
        }

        // For small numbers, render as dots; for strings like "★★★★", render as text
        if (!isNaN(num) && num <= 15) {
          // Arrange dots in a roughly triangular pattern
          const dots: React.ReactNode[] = [];
          let count = 0;
          const rows = Math.ceil(Math.sqrt(num));
          for (let r = 0; r < rows && count < num; r++) {
            const inRow = Math.min(r + 1, num - count);
            for (let c = 0; c < inRow; c++) {
              dots.push(
                <circle
                  key={`${i}-${count}`}
                  cx={x - (inRow - 1) * 4 + c * 8}
                  cy={20 + r * 10}
                  r={3}
                  fill={BLUE}
                />
              );
              count++;
            }
          }
          return <g key={i}>{dots}</g>;
        }

        return (
          <text key={i} x={x} y={45} textAnchor="middle" fontSize={12} fontWeight={600} fill={GRAY}>
            {item}
          </text>
        );
      })}
    </svg>
  );
}

function BlockPattern({ sequence }: Props) {
  return (
    <svg viewBox="0 0 280 80" className="w-full" role="img" aria-label="Block pattern sequence">
      {sequence.map((item, i) => {
        const x = 25 + i * (230 / sequence.length);
        const isQ = item === '?';
        const num = parseInt(item);

        if (isQ || isNaN(num)) {
          return (
            <g key={i}>
              <rect x={x - 15} y={15} width={30} height={50} rx={6}
                fill="rgba(28,176,246,0.1)" stroke={BLUE} strokeWidth={2} strokeDasharray="4,3" />
              <text x={x} y={45} textAnchor="middle" fontSize={16} fontWeight={700} fill={BLUE}>?</text>
            </g>
          );
        }

        // Stack blocks
        const blockSize = 10;
        const cols = Math.ceil(Math.sqrt(num));
        const rows = Math.ceil(num / cols);
        let count = 0;

        return (
          <g key={i}>
            {Array.from({ length: rows }, (_, r) =>
              Array.from({ length: cols }, (_, c) => {
                if (count >= num) return null;
                count++;
                return (
                  <rect
                    key={`${i}-${r}-${c}`}
                    x={x - (cols * blockSize) / 2 + c * blockSize}
                    y={60 - (r + 1) * blockSize}
                    width={blockSize - 1}
                    height={blockSize - 1}
                    rx={1}
                    fill="#58CC02"
                    stroke="#3ea802"
                    strokeWidth={0.5}
                  />
                );
              })
            )}
            <text x={x} y={73} textAnchor="middle" fontSize={9} fill="#6B7280" fontWeight={600}>
              {num}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export default function PatternDiagram(props: Props) {
  switch (props.variant) {
    case 'symbols': return <SymbolPattern {...props} />;
    case 'shapes': return <ShapePattern {...props} />;
    case 'dots': return <DotPattern {...props} />;
    case 'blocks': return <BlockPattern {...props} />;
    default: return <ShapePattern {...props} />;
  }
}
