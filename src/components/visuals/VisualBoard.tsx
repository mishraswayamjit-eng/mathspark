'use client';

import type { VisualSpec } from '@/lib/visuals/spec';
import { VISUAL_LIBRARY, type WhiteboardStarter } from '@/lib/visuals/topicMap';
import { FractionVisual, NumberLineVisual, PlaceValueVisual, ArrayVisual, BarModelVisual } from './NumberVisuals';
import { BalanceVisual, RectangleVisual, AngleVisual, PercentGridVisual, ContainerVisual } from './ShapeVisuals';

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
      <div className="flex items-center gap-3 mb-3">
        <span className="w-11 h-11 rounded-tile bg-soft border-2 border-line flex items-center justify-center text-xl flex-shrink-0" aria-hidden="true">
          {info.emoji}
        </span>
        <div className="min-w-0">
          <p className="font-display text-title text-ink truncate">{spec.title ?? info.name}</p>
          <p className="text-caption text-ink-muted truncate">{info.blurb}</p>
        </div>
      </div>
      <div key={JSON.stringify(spec)}>{renderVisual(spec)}</div>
    </div>
  );
}

interface WhiteboardPanelProps {
  /** The visual to show, or null for the empty state. */
  visual: VisualSpec | null;
  /** Suggestions shown while the board is empty. */
  starters: WhiteboardStarter[];
  onStarter: (prompt: string) => void;
  disabled?: boolean;
}

/** The whiteboard beside the conversation on wide screens. */
export function WhiteboardPanel({ visual, starters, onStarter, disabled }: WhiteboardPanelProps) {
  return (
    <div className="h-full flex flex-col bg-white border-2 border-ink rounded-card shadow-hard overflow-hidden">
      <div className="bg-ink px-4 py-3 flex items-center gap-2 flex-shrink-0">
        <span className="text-xl" aria-hidden="true">🧑‍🏫</span>
        <p className="font-display text-title text-white">Whiteboard</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {visual ? (
          <div className="animate-card-pop">
            <VisualBoard spec={visual} />
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <p className="font-display text-heading text-ink">Let&apos;s see the maths</p>
              <p className="text-label text-ink-muted mt-1">
                When Sparky explains something, a picture you can play with appears here. Try one:
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
                    <span className="w-11 h-11 rounded-tile bg-soft border-2 border-line flex items-center justify-center text-xl flex-shrink-0" aria-hidden="true">
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
    </div>
  );
}
