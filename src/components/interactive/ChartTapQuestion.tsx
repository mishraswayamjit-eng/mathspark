'use client';

import React, { useState } from 'react';
import type { ChartTapData } from '@/types';
import QuestionDiagram from '@/components/diagrams/QuestionDiagram';
import DuoButton from '@/components/DuoButton';

interface Props {
  data: ChartTapData;
  questionId: string;
  answered: boolean;
  onSubmit: (answer: string, isCorrect: boolean) => void;
}

export default function ChartTapQuestion({ data, questionId, answered, onSubmit }: Props) {
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null);
  const [result, setResult] = useState<'correct' | 'wrong' | null>(null);

  const handleCheck = () => {
    if (answered || !selectedRegion) return;
    const isCorrect = selectedRegion === data.correctRegion;
    setResult(isCorrect ? 'correct' : 'wrong');
    onSubmit(JSON.stringify(selectedRegion), isCorrect);
  };

  const getRegionStyle = (regionId: string) => {
    if (result) {
      if (regionId === data.correctRegion) {
        return 'border-2 border-duo-green bg-green-100/40';
      }
      if (regionId === selectedRegion && regionId !== data.correctRegion) {
        return 'border-2 border-duo-red bg-red-100/40';
      }
      return 'border border-transparent';
    }
    if (regionId === selectedRegion) {
      return 'border-2 border-duo-blue bg-blue-100/30';
    }
    return 'border border-gray-200/50 hover:border-duo-blue/50 hover:bg-blue-50/20';
  };

  return (
    <div className="space-y-3">
      {/* Diagram with tappable overlay */}
      <div className="relative">
        {/* Underlying diagram (pure renderer, unchanged) */}
        <QuestionDiagram questionId={questionId} />

        {/* Tappable hit zones overlay */}
        <div className="absolute inset-0">
          {data.regions.map((region) => (
            <button
              key={region.id}
              disabled={answered}
              onClick={() => !answered && setSelectedRegion(region.id)}
              className={`absolute rounded-lg transition-colors ${getRegionStyle(region.id)}`}
              style={{
                left: `${region.x}%`,
                top: `${region.y}%`,
                width: `${region.width}%`,
                height: `${region.height}%`,
                minWidth: '44px',
                minHeight: '44px',
              }}
              aria-label={`Select ${region.label}`}
            >
              {/* Label shown on hover / for a11y */}
              <span className="sr-only">{region.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Region labels as tappable chips */}
      <div className="flex flex-wrap gap-2 justify-center">
        {data.regions.map((region) => {
          const isSelected = selectedRegion === region.id;
          let chipCls = 'px-3 py-1.5 rounded-full text-xs font-extrabold border-2 transition-colors min-h-[36px] ';
          if (result) {
            if (region.id === data.correctRegion) {
              chipCls += 'bg-green-100 border-duo-green text-green-800';
            } else if (region.id === selectedRegion) {
              chipCls += 'bg-red-100 border-duo-red text-red-800';
            } else {
              chipCls += 'bg-gray-50 border-gray-200 text-gray-400';
            }
          } else if (isSelected) {
            chipCls += 'bg-blue-100 border-duo-blue text-blue-800';
          } else {
            chipCls += 'bg-white border-gray-200 text-gray-700 hover:border-duo-blue';
          }

          return (
            <button
              key={region.id}
              disabled={answered}
              onClick={() => !answered && setSelectedRegion(region.id)}
              className={chipCls}
            >
              {region.label}
            </button>
          );
        })}
      </div>

      {!answered && (
        <DuoButton
          variant="green"
          fullWidth
          onClick={handleCheck}
          disabled={!selectedRegion}
        >
          Check Answer
        </DuoButton>
      )}
    </div>
  );
}
