'use client';

import React from 'react';
import type { SlideIllustration as SlideIllustrationT } from '@/types/lesson';
import FractionDiagram from '@/components/diagrams/FractionDiagram';
import MultiFractionDiagram from '@/components/diagrams/MultiFractionDiagram';
import NumberLineDiagram from '@/components/diagrams/NumberLineDiagram';
import ClockDiagram from '@/components/diagrams/ClockDiagram';
import AngleDiagram from '@/components/diagrams/AngleDiagram';
import TriangleDiagram from '@/components/diagrams/TriangleDiagram';
import CircleDiagram from '@/components/diagrams/CircleDiagram';
import BalanceDiagram from '@/components/diagrams/BalanceDiagram';
import PatternDiagram from '@/components/diagrams/PatternDiagram';
import PolygonDiagram from '@/components/diagrams/PolygonDiagram';
import PictographDiagram from '@/components/diagrams/PictographDiagram';
import CompositeShapeDiagram from '@/components/diagrams/CompositeShapeDiagram';
import VennDiagram from '@/components/diagrams/VennDiagram';

interface Props {
  illustration: SlideIllustrationT;
}

// Diagram components accept Record<string, unknown> from lesson JSON data.
// Each component handles its own prop validation internally.
type DiagramProps = Record<string, unknown>;

function renderDiagram(illustration: SlideIllustrationT) {
  const p = illustration.props as DiagramProps;

  switch (illustration.type) {
    case 'fraction':
      return <FractionDiagram {...p} />;
    case 'multiFraction':
      return <MultiFractionDiagram {...p} />;
    case 'numberLine':
      return <NumberLineDiagram {...p} />;
    case 'clock':
      return <ClockDiagram {...p} />;
    case 'angle':
      return <AngleDiagram {...p} />;
    case 'triangle':
      return <TriangleDiagram {...p} />;
    case 'circle':
      return <CircleDiagram {...p} />;
    case 'balance':
      return <BalanceDiagram {...p} />;
    case 'pattern':
      return <PatternDiagram {...p} />;
    case 'polygon':
      return <PolygonDiagram {...p} />;
    case 'pictograph':
      return <PictographDiagram {...p} />;
    case 'compositeShape':
      return <CompositeShapeDiagram {...p} />;
    case 'venn':
      return <VennDiagram {...p} />;
    case 'emoji':
      return (
        <div className="flex items-center justify-center">
          <span className="text-[80px] leading-none" aria-hidden="true">
            {(p as { emoji?: string }).emoji || '📖'}
          </span>
        </div>
      );
    default:
      return null;
  }
}

export default function SlideIllustration({ illustration }: Props) {
  return (
    <div className="max-w-[280px] mx-auto my-4">
      <div className="rounded-xl border border-gray-100 bg-gray-50 p-3">
        {renderDiagram(illustration)}
      </div>
    </div>
  );
}
