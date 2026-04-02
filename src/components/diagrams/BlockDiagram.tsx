import React from 'react';

interface Props {
  layers: number[][];
  answer: number;
}

const GREEN = '#58CC02';
const GREEN_DARK = '#3ea802';
const GRAY = '#374151';

export default function BlockDiagram({ layers, answer }: Props) {
  // Isometric 3D block rendering
  const bw = 18, bh = 14, bd = 10; // block width, height, depth
  const maxCols = Math.max(...layers.map(row => Math.max(...row)));
  const maxRows = layers[0].length;
  const numLayers = layers.length;

  // Center the drawing
  const totalW = (maxCols + maxRows) * bw / 2 + 40;
  const totalH = numLayers * bh + maxRows * bd / 2 + maxCols * bd / 2 + 20;
  const offsetX = totalW / 2;
  const offsetY = 10;

  function isoX(col: number, row: number) {
    return offsetX + (col - row) * bw / 2;
  }
  function isoY(col: number, row: number, layer: number) {
    return offsetY + (col + row) * bd / 2 + (numLayers - 1 - layer) * bh;
  }

  function Block({ col, row, layer }: { col: number; row: number; layer: number }) {
    const x = isoX(col, row);
    const y = isoY(col, row, layer);

    // Top face
    const topPoints = [
      `${x},${y}`,
      `${x + bw / 2},${y - bd / 2}`,
      `${x + bw},${y}`,
      `${x + bw / 2},${y + bd / 2}`,
    ].join(' ');

    // Left face
    const leftPoints = [
      `${x},${y}`,
      `${x + bw / 2},${y + bd / 2}`,
      `${x + bw / 2},${y + bd / 2 + bh}`,
      `${x},${y + bh}`,
    ].join(' ');

    // Right face
    const rightPoints = [
      `${x + bw},${y}`,
      `${x + bw / 2},${y + bd / 2}`,
      `${x + bw / 2},${y + bd / 2 + bh}`,
      `${x + bw},${y + bh}`,
    ].join(' ');

    return (
      <g>
        <polygon points={topPoints} fill="#7CDB3C" stroke={GREEN_DARK} strokeWidth={0.5} />
        <polygon points={leftPoints} fill={GREEN} stroke={GREEN_DARK} strokeWidth={0.5} />
        <polygon points={rightPoints} fill="#4CAF00" stroke={GREEN_DARK} strokeWidth={0.5} />
      </g>
    );
  }

  const blocks: React.ReactNode[] = [];
  // Render from back to front, bottom to top for correct z-ordering
  for (let layer = 0; layer < numLayers; layer++) {
    const rowData = layers[layer];
    for (let row = rowData.length - 1; row >= 0; row--) {
      for (let col = 0; col < rowData[row]; col++) {
        blocks.push(
          <Block key={`${layer}-${row}-${col}`} col={col} row={row} layer={layer} />
        );
      }
    }
  }

  return (
    <svg viewBox={`0 0 ${totalW} ${totalH + 20}`} className="w-full" role="img" aria-label={`3D block figure (${answer} blocks)`}>
      {blocks}
      <text x={totalW / 2} y={totalH + 15} textAnchor="middle" fontSize={10} fill="#6B7280" fontWeight={600}>
        How many blocks?
      </text>
    </svg>
  );
}
