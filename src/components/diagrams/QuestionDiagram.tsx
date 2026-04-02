'use client';

import React from 'react';
import { QUESTION_DIAGRAMS } from '@/data/questionDiagrams';
import type { DiagramSpec } from '@/data/questionDiagrams';
import FractionDiagram from './FractionDiagram';
import MultiFractionDiagram from './MultiFractionDiagram';
import BalanceDiagram from './BalanceDiagram';
import AngleDiagram from './AngleDiagram';
import VennDiagram from './VennDiagram';
import CircleDiagram from './CircleDiagram';
import TriangleDiagram from './TriangleDiagram';
import CompositeShapeDiagram from './CompositeShapeDiagram';
import PatternDiagram from './PatternDiagram';
import MirrorDiagram from './MirrorDiagram';
import ClockDiagram from './ClockDiagram';
import NumberLineDiagram from './NumberLineDiagram';
import BlockDiagram from './BlockDiagram';

function renderDiagram(spec: DiagramSpec) {
  switch (spec.type) {
    case 'fraction':
      return <FractionDiagram {...spec.props} />;
    case 'multiFraction':
      return <MultiFractionDiagram {...spec.props} />;
    case 'balance':
      return <BalanceDiagram {...spec.props} />;
    case 'angle':
      return <AngleDiagram {...spec.props} />;
    case 'venn':
      return <VennDiagram {...spec.props} />;
    case 'circle':
      return <CircleDiagram {...spec.props} />;
    case 'triangle':
      return <TriangleDiagram {...spec.props} />;
    case 'compositeShape':
      return <CompositeShapeDiagram {...spec.props} />;
    case 'pattern':
      return <PatternDiagram {...spec.props} />;
    case 'mirror':
      return <MirrorDiagram {...spec.props} />;
    case 'clock':
      return <ClockDiagram {...spec.props} />;
    case 'numberLine':
      return <NumberLineDiagram {...spec.props} />;
    case 'blocks':
      return <BlockDiagram {...spec.props} />;
    default:
      return null;
  }
}

const QuestionDiagram = React.memo(function QuestionDiagram({
  questionId,
}: {
  questionId: string;
}) {
  const spec = QUESTION_DIAGRAMS[questionId];
  if (!spec) return null;

  return (
    <div className="mt-3 flex justify-center">
      <div className="w-full max-w-[280px] rounded-xl border border-gray-100 bg-gray-50 p-3">
        {renderDiagram(spec)}
      </div>
    </div>
  );
});

export default QuestionDiagram;
