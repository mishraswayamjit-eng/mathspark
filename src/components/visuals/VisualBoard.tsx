'use client';

import { useState } from 'react';
import type { VisualSpec } from '@/lib/visuals/spec';
import { VISUAL_LIBRARY, type WhiteboardStarter } from '@/lib/visuals/topicMap';
import { FractionVisual, NumberLineVisual, PlaceValueVisual, ArrayVisual, BarModelVisual } from './NumberVisuals';
import { BalanceVisual, RectangleVisual, AngleVisual, PercentGridVisual, ContainerVisual } from './ShapeVisuals';
import { PolygonVisual, TilingVisual, TriangleVisual, CircleVisual, BarChartVisual } from './GeometryVisuals';
import SketchPad from './SketchPad';

function renderVisual(spec: VisualSpec) {
  switch (spec.type) {
    case 'fraction':    return <FractionVisual spec={spec} />;
    case 'numberLine':  return <NumberLineVisual spec={spec} />;
    case 'placeValue':  return <PlaceValueVisual spec={spec} />;
    case 'array':       return <ArrayVisual spec={spec} />;
    case 'barModel':    return <BarModelVisual spec={spec} />;
    case 'balance':     return <BalanceVisual spec={spec} />;
    case 'rectangle':   return <RectangleVisual spec={spec} />;
    case 'angle':       return <AngleVisual spec={spec} />;
    case 'percentGrid': return <PercentGridVisual spec={spec} />;
    case 'container':   return <ContainerVisual spec={spec} />;
    case 'polygon':     return <PolygonVisual spec={spec} />;
    case 'tiling':      return <TilingVisual spec={spec} />;
    case 'triangle':    return <TriangleVisual spec={spec} />;
    case 'circle':      return <CircleVisual spec={spec} />;
    case 'barChart':    return <BarChartVisual spec={spec} />;
    default:            return null;
  }
}

/**
 * One interactive visual from Sparky's library, with its heading.
 * The caller supplies the surrounding card. A change of spec remounts the
 * visual, so each new picture starts from the numbers Sparky gave.
 */
export default function VisualBoard({ spec }: { spec: VisualSpec }) {
  const info = VISUAL_LIBRARY[spec.type];
  return (
    <div>
      <div className="mb-4">
        <p className="font-display text-heading text-ink">{spec.title ?? info.name}</p>
        <p className="text-label text-ink-muted mt-0.5">{info.blurb}</p>
      </div>
      <div key={JSON.stringify(spec)} className="animate-fade-in">{renderVisual(spec)}</div>
    </div>
  );
}

interface WhiteboardPanelProps {
  /** The visual to show, or null for the empty state. */
  visual: VisualSpec | null;
  /** Suggestions shown while the board is empty. */
  starters: WhiteboardStarter[];
  onStarter: (prompt: string) => void;
  /** Receives the child's sketch as an image, ready to send to Sparky. */
  onSketch: (file: File) => void;
  disabled?: boolean;
}

/** The whiteboard beside the conversation on wide screens. */
export function WhiteboardPanel({ visual, starters, onStarter, onSketch, disabled }: WhiteboardPanelProps) {
  const [pencil, setPencil] = useState(false);

  return (
    <div className="h-full flex flex-col bg-white border-2 border-line rounded-card overflow-hidden">
      {/* A quiet title row: the board itself is the focus. */}
      <div className="px-5 py-3 flex items-center gap-3 flex-shrink-0 border-b-2 border-line">
        <p className="font-display text-title text-ink flex-1">Whiteboard</p>
        <button
          type="button"
          onClick={() => setPencil(!pencil)}
          aria-pressed={pencil}
          className={`min-h-[48px] px-4 rounded-control border-2 font-extrabold text-[14px] flex items-center gap-2 transition-colors ${
            pencil ? 'bg-action border-ink text-white' : 'bg-white border-line text-ink hover:border-ink'
          }`}
        >
          <span aria-hidden="true">✏️</span>
          {pencil ? 'Pencil on' : 'Sketch'}
        </button>
      </div>

      <SketchPad active={pencil} resetKey={visual ? JSON.stringify(visual) : 'empty'} onSend={onSketch}>
        <div className="px-6 py-6 max-w-[460px] mx-auto">
          {visual ? (
            <VisualBoard spec={visual} />
          ) : pencil ? (
            <div className="min-h-[420px] flex flex-col items-center justify-center text-center gap-2">
              <p className="font-display text-heading text-ink">Sketch your thinking</p>
              <p className="text-label text-ink-muted max-w-[300px]">
                Draw with your finger, a stylus or the mouse, then tap Show Sparky.
              </p>
            </div>
          ) : (
            <div className="space-y-5">
              <div>
                <p className="font-display text-display text-ink">Let&apos;s see the maths</p>
                <p className="text-label text-ink-muted mt-1.5">
                  When Sparky explains something, a picture you can play with appears here. Try one, or tap Sketch and draw your own.
                </p>
              </div>
              <div className="space-y-2.5">
                {starters.map((s) => {
                  const info = VISUAL_LIBRARY[s.kind];
                  return (
                    <button
                      key={s.kind}
                      type="button"
                      disabled={disabled}
                      onClick={() => onStarter(s.prompt)}
                      className="w-full text-left bg-white rounded-card border-2 border-line hover:border-ink p-3 flex items-center gap-3 min-h-[72px] transition-colors disabled:opacity-50"
                    >
                      <span className="w-11 h-11 rounded-tile bg-soft flex items-center justify-center text-xl flex-shrink-0" aria-hidden="true">
                        {info.emoji}
                      </span>
                      <span className="flex-1 min-w-0">
                        <span className="block font-display text-title text-ink">{info.name}</span>
                        <span className="block text-[13px] font-bold text-ink-muted">{s.prompt}</span>
                      </span>
                      <span className="text-2xl leading-none text-ink-muted flex-shrink-0" aria-hidden="true">›</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </SketchPad>
    </div>
  );
}
