'use client';

import React, { useState } from 'react';
import type { TileBuildData } from '@/types';
import DuoButton from '@/components/DuoButton';
import KatexRenderer from '@/components/KatexRenderer';
import { isTileBuildCorrect } from '@/lib/interactiveGrading';

interface Props {
  data: TileBuildData;
  answered: boolean;
  onSubmit: (answer: string, isCorrect: boolean) => void;
}

/** Plain text, or KaTeX when the piece contains LaTeX markup. */
function Piece({ text }: { text: string }) {
  if (text.includes('\\')) return <KatexRenderer latex={text} displayMode={false} />;
  return <>{text}</>;
}

/**
 * Build-the-answer question: tap a tile to drop it into the next empty blank,
 * tap a filled blank to send its tile back. Tap-based (not drag) so it works
 * with one thumb and with a keyboard.
 */
export default function TileBuildQuestion({ data, answered, onSubmit }: Props) {
  const blankCount = data.solution.length;

  // filled[b] = index into data.tiles placed in blank b, or null when empty
  const [filled, setFilled] = useState<Array<number | null>>(() => {
    const start: Array<number | null> = [];
    for (let i = 0; i < blankCount; i++) start.push(null);
    return start;
  });
  // Per-blank outcome once checked
  const [result, setResult] = useState<boolean[] | null>(null);

  const locked   = answered || result !== null;
  const allFull  = filled.every((t) => t !== null);
  const usedTile = (tileIdx: number) => filled.indexOf(tileIdx) !== -1;

  function placeTile(tileIdx: number) {
    if (locked || usedTile(tileIdx)) return;
    const firstEmpty = filled.indexOf(null);
    if (firstEmpty === -1) return;
    setFilled((prev) => {
      const next = prev.slice();
      next[firstEmpty] = tileIdx;
      return next;
    });
  }

  function clearBlank(blankIdx: number) {
    if (locked || filled[blankIdx] === null) return;
    setFilled((prev) => {
      const next = prev.slice();
      next[blankIdx] = null;
      return next;
    });
  }

  function handleCheck() {
    if (locked || !allFull) return;
    const texts = filled.map((t) => (t === null ? '' : data.tiles[t]));
    const isCorrect = isTileBuildCorrect(data, texts);
    // When the whole line is right (including an accepted alternative) every blank is right.
    setResult(texts.map((t, i) => isCorrect || t === data.solution[i]));
    onSubmit(JSON.stringify(texts), isCorrect);
  }

  function blankCls(blankIdx: number): string {
    const base =
      'inline-flex items-center justify-center min-w-[52px] min-h-[48px] px-3 rounded-control border-2 text-[17px] font-extrabold transition-colors';
    if (result) {
      return result[blankIdx]
        ? `${base} bg-success-soft border-success text-ink`
        : `${base} bg-retry-soft border-retry text-ink`;
    }
    if (filled[blankIdx] === null) return `${base} bg-soft border-dashed border-ink-muted text-ink-muted`;
    return `${base} bg-white border-ink text-ink shadow-hard-xs`;
  }

  let blankCursor = 0;

  return (
    <div className="space-y-4">
      {data.instruction && (
        <p className="text-sm font-bold text-ink-muted text-center">{data.instruction}</p>
      )}

      {/* The line being built */}
      <div className="ui-card flex flex-wrap items-center justify-center gap-2 text-[19px] font-bold text-ink">
        {data.parts.map((part, i) => {
          if (part !== null) {
            return (
              <span key={`p${i}`} className="leading-normal">
                <Piece text={part} />
              </span>
            );
          }
          const blankIdx = blankCursor;
          blankCursor += 1;
          const tileIdx = filled[blankIdx];
          return (
            <button
              key={`b${i}`}
              type="button"
              onClick={() => clearBlank(blankIdx)}
              disabled={locked || tileIdx === null}
              aria-label={
                tileIdx === null
                  ? `Blank ${blankIdx + 1}, empty`
                  : `Blank ${blankIdx + 1}: ${data.tiles[tileIdx]}. Tap to remove`
              }
              className={blankCls(blankIdx)}
            >
              {tileIdx === null ? <span aria-hidden="true">?</span> : <Piece text={data.tiles[tileIdx]} />}
            </button>
          );
        })}
      </div>

      {/* Tile tray */}
      {!locked && (
        <div className="flex flex-wrap justify-center gap-2.5" role="group" aria-label="Tiles to choose from">
          {data.tiles.map((tile, tileIdx) => {
            const used = usedTile(tileIdx);
            return (
              <button
                key={tileIdx}
                type="button"
                onClick={() => placeTile(tileIdx)}
                disabled={used}
                aria-label={used ? `${tile}, already placed` : `Place ${tile}`}
                className={`min-w-[52px] min-h-[48px] px-3 rounded-control border-2 text-[17px] font-extrabold transition-[transform,box-shadow,opacity] ${
                  used
                    ? 'bg-soft border-line text-ink-muted opacity-40'
                    : 'bg-white border-ink text-ink shadow-hard-sm active:translate-x-[2px] active:translate-y-[2px] active:shadow-hard-xs'
                }`}
              >
                <Piece text={tile} />
              </button>
            );
          })}
        </div>
      )}

      {/* Show the right build when it was not quite right */}
      {result && !result.every(Boolean) && (
        <div className="bg-success-soft border-2 border-success rounded-note px-3 py-2">
          <p className="text-xs font-extrabold text-ink mb-1">Here is how it fits together:</p>
          <p className="text-label text-ink">
            {(() => {
              let b = 0;
              return data.parts.map((part, i) => {
                if (part !== null) return <span key={i}><Piece text={part} /> </span>;
                const text = data.solution[b];
                b += 1;
                return (
                  <span key={i} className="font-extrabold text-success">
                    <Piece text={text} />{' '}
                  </span>
                );
              });
            })()}
          </p>
        </div>
      )}

      {!locked && (
        <DuoButton variant="green" fullWidth onClick={handleCheck} disabled={!allFull}>
          Check
        </DuoButton>
      )}
    </div>
  );
}
