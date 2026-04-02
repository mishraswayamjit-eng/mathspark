import React from 'react';

interface Props {
  variant: 'letter' | 'shape' | 'arrow' | 'symmetry';
  content: string;
  axis: 'vertical' | 'horizontal';
}

const BLUE = '#1CB0F6';
const GRAY = '#374151';

function LetterMirror({ content, axis }: Props) {
  const isVertical = axis === 'vertical';

  return (
    <svg viewBox="0 0 280 100" className="w-full" role="img" aria-label={`Mirror image of "${content}"`}>
      {/* Original */}
      <text x={isVertical ? 90 : 140} y={isVertical ? 55 : 40}
        textAnchor="middle" fontSize={28} fontWeight={700} fill={GRAY}>
        {content}
      </text>

      {/* Mirror line */}
      {isVertical ? (
        <line x1={140} y1={10} x2={140} y2={90} stroke={BLUE} strokeWidth={2} strokeDasharray="6,4" />
      ) : (
        <line x1={30} y1={50} x2={250} y2={50} stroke={BLUE} strokeWidth={2} strokeDasharray="6,4" />
      )}

      {/* Reflected (using CSS transform in SVG) */}
      <g transform={isVertical ? 'translate(280,0) scale(-1,1)' : 'translate(0,100) scale(1,-1)'}>
        <text
          x={isVertical ? 90 : 140}
          y={isVertical ? 55 : 40}
          textAnchor="middle"
          fontSize={28}
          fontWeight={700}
          fill={BLUE}
          opacity={0.5}
        >
          {content}
        </text>
      </g>

      {/* Labels */}
      <text x={isVertical ? 65 : 140} y={isVertical ? 95 : 18}
        textAnchor="middle" fontSize={9} fill="#6B7280" fontWeight={600}>
        Original
      </text>
      <text x={isVertical ? 215 : 140} y={isVertical ? 95 : 95}
        textAnchor="middle" fontSize={9} fill={BLUE} fontWeight={600}>
        Mirror
      </text>
    </svg>
  );
}

function ArrowMirror({ content }: Props) {
  // content is space-separated arrows like "↗ ↙ ↑ →"
  const arrows = content.split(' ');

  return (
    <svg viewBox="0 0 280 80" className="w-full" role="img" aria-label="Mirror image of arrows">
      {/* Mirror line in center */}
      <line x1={140} y1={5} x2={140} y2={75} stroke={BLUE} strokeWidth={2} strokeDasharray="6,4" />

      {arrows.map((arrow, i) => (
        <g key={i}>
          <rect
            x={20 + i * 60} y={20}
            width={50} height={40}
            rx={8}
            fill="white"
            stroke="#D1D5DB"
            strokeWidth={1.5}
          />
          <text
            x={45 + i * 60} y={48}
            textAnchor="middle"
            fontSize={22}
            fill={GRAY}
          >
            {arrow}
          </text>
        </g>
      ))}
    </svg>
  );
}

function SymmetryDiagram({ content }: Props) {
  // Show multiple figures and ask which is symmetrical
  const items = content.split(' ');

  return (
    <svg viewBox="0 0 280 80" className="w-full" role="img" aria-label="Which figure is symmetrical?">
      {items.map((item, i) => {
        const x = 30 + i * (220 / items.length);
        return (
          <g key={i}>
            <rect x={x - 20} y={10} width={40} height={55} rx={8}
              fill="white" stroke="#D1D5DB" strokeWidth={1.5} />
            <text x={x} y={44} textAnchor="middle" fontSize={20} fontWeight={700} fill={GRAY}>
              {item}
            </text>
            {/* Dotted center line to test symmetry */}
            <line x1={x} y1={15} x2={x} y2={60} stroke={BLUE} strokeWidth={0.5} strokeDasharray="2,2" opacity={0.4} />
          </g>
        );
      })}
    </svg>
  );
}

function ShapeMirror({ content, axis }: Props) {
  const isVertical = axis === 'vertical';

  // Generic L-shape or T-shape representation
  const isL = content.toLowerCase().includes('l');

  return (
    <svg viewBox="0 0 280 100" className="w-full" role="img" aria-label={`Mirror of ${content}`}>
      {/* Mirror line */}
      {isVertical ? (
        <line x1={140} y1={10} x2={140} y2={90} stroke={BLUE} strokeWidth={2} strokeDasharray="6,4" />
      ) : (
        <line x1={30} y1={50} x2={250} y2={50} stroke={BLUE} strokeWidth={2} strokeDasharray="6,4" />
      )}

      {/* Original shape */}
      {isL ? (
        <g>
          <rect x={50} y={20} width={20} height={60} fill={GRAY} rx={2} />
          <rect x={50} y={60} width={50} height={20} fill={GRAY} rx={2} />
        </g>
      ) : (
        <g>
          <rect x={60} y={20} width={50} height={15} fill={GRAY} rx={2} />
          <rect x={75} y={35} width={20} height={45} fill={GRAY} rx={2} />
        </g>
      )}

      {/* Reflected shape */}
      {isL ? (
        <g>
          <rect x={210} y={20} width={20} height={60} fill={BLUE} rx={2} opacity={0.4} />
          <rect x={180} y={60} width={50} height={20} fill={BLUE} rx={2} opacity={0.4} />
        </g>
      ) : (
        <g>
          <rect x={170} y={20} width={50} height={15} fill={BLUE} rx={2} opacity={0.4} />
          <rect x={185} y={35} width={20} height={45} fill={BLUE} rx={2} opacity={0.4} />
        </g>
      )}
    </svg>
  );
}

export default function MirrorDiagram(props: Props) {
  switch (props.variant) {
    case 'letter': return <LetterMirror {...props} />;
    case 'arrow': return <ArrowMirror {...props} />;
    case 'symmetry': return <SymmetryDiagram {...props} />;
    case 'shape': return <ShapeMirror {...props} />;
    default: return <LetterMirror {...props} />;
  }
}
