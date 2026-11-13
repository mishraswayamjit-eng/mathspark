'use client';

import React from 'react';
import type { Slide } from '@/types/lesson';
import BoldText from './BoldText';
import SlideIllustration from './SlideIllustration';
import KatexRenderer from '@/components/KatexRenderer';

interface SlideRendererProps {
  slide: Slide;
  accentColor: string;
}

function hasLatex(text: string): boolean {
  return /[\\{]/.test(text);
}

function NotationBox({ notation }: { notation: string }) {
  return (
    <div className="bg-soft border-2 border-line rounded-note px-4 py-3 mt-3 text-center w-full">
      {hasLatex(notation) ? (
        <KatexRenderer latex={notation} displayMode className="text-base" />
      ) : (
        <p className="text-base font-bold text-ink font-mono">{notation}</p>
      )}
    </div>
  );
}

export default function SlideRenderer({ slide }: SlideRendererProps) {
  switch (slide.type) {
    case 'intro':
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center px-6 text-center">
          {slide.emoji && (
            <span className="text-[64px] leading-none mb-4" aria-hidden="true">{slide.emoji}</span>
          )}
          {slide.illustration && <SlideIllustration illustration={slide.illustration} />}
          <h2 className="text-heading text-ink mb-3">
            <BoldText text={slide.text} />
          </h2>
          {slide.subtext && (
            <p className="text-sm text-ink-muted leading-relaxed max-w-[320px]">
              <BoldText text={slide.subtext} />
            </p>
          )}
        </div>
      );

    case 'concept':
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center px-6">
          <p className="text-base font-semibold text-ink leading-relaxed text-center mb-4">
            <BoldText text={slide.text} />
          </p>
          {slide.illustration && <SlideIllustration illustration={slide.illustration} />}
          {slide.notation && <NotationBox notation={slide.notation} />}
          {slide.subtext && (
            <p className="text-[13px] font-bold text-ink-muted mt-3 text-center">
              <span aria-hidden="true">💡 </span>
              <BoldText text={slide.subtext} />
            </p>
          )}
        </div>
      );

    case 'rule':
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center px-6">
          <div className="w-full bg-white border-2 border-line rounded-card px-5 py-6 text-center">
            <span className="text-[40px] leading-none mb-3 block" aria-hidden="true">
              {slide.emoji || '📝'}
            </span>
            <p className="text-[13px] font-extrabold text-ink-muted mb-2">Rule</p>
            <p className="text-base font-bold text-ink leading-relaxed">
              <BoldText text={slide.text} />
            </p>
            {slide.notation && <NotationBox notation={slide.notation} />}
          </div>
        </div>
      );

    case 'tip':
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center px-6">
          <div className="w-full bg-hint rounded-card px-5 py-6 text-center">
            <span className="text-[40px] leading-none mb-3 block" aria-hidden="true">
              {slide.emoji || '💡'}
            </span>
            <p className="text-[13px] font-extrabold text-hint-ink mb-2">Tip</p>
            <p className="text-sm font-semibold text-hint-ink leading-relaxed">
              <BoldText text={slide.text} />
            </p>
          </div>
        </div>
      );

    case 'diagram':
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center px-6">
          {slide.illustration && <SlideIllustration illustration={slide.illustration} />}
          <p className="text-sm text-ink-muted text-center mt-2">
            <BoldText text={slide.text} />
          </p>
          {slide.notation && <NotationBox notation={slide.notation} />}
        </div>
      );

    case 'recap':
      return (
        <div className="min-h-[60vh] flex flex-col items-center justify-center px-6 text-center">
          <span className="text-[48px] leading-none mb-4" aria-hidden="true">✅</span>
          <p className="text-[13px] font-extrabold text-ink-muted mb-2">
            Recap
          </p>
          <p className="text-base font-semibold text-ink leading-relaxed max-w-[320px]">
            <BoldText text={slide.text} />
          </p>
          {slide.notation && <NotationBox notation={slide.notation} />}
        </div>
      );

    default:
      return null;
  }
}
