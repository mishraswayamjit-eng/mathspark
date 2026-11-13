import type { ConceptVisual } from '@/types/conceptTrainer';

/**
 * Pure-CSS renderer for a concept item's visual model. Four shapes:
 *  - `bar`     — a two-part percentage bar (share% | rest%)
 *  - `mapping` — a percent ↔ amount correspondence table
 *  - `groups`  — a row of equal-capacity boxes working toward a target
 *  - `parts`   — a whole cut into N equal segments with k shaded (fractions)
 */
export default function ConceptVisualView({ visual }: { visual: ConceptVisual }) {
  if (visual.type === 'parts') {
    const total = Math.max(1, Math.floor(visual.total));
    const shaded = Math.max(0, Math.min(total, Math.floor(visual.shaded)));
    return (
      <div>
        <div className="flex w-full h-12 rounded-note overflow-hidden border-2 border-line">
          {Array.from({ length: total }, (_, i) => (
            <div
              key={i}
              className={`flex-1 flex items-center justify-center text-xs font-bold ${
                i < shaded ? 'bg-action text-white' : 'bg-soft text-ink-muted'
              } ${i > 0 ? 'border-l-2 border-line' : ''}`}
            >
              {i < shaded ? '●' : ''}
            </div>
          ))}
        </div>
        <p className="text-xs text-ink-muted font-semibold mt-1.5">
          {visual.label ?? `${shaded}/${total} shaded`}
        </p>
      </div>
    );
  }

  if (visual.type === 'bar') {
    const share = Math.max(0, Math.min(100, visual.share));
    return (
      <div>
        <p className="text-xs font-bold text-ink-muted mb-1.5">{visual.whole}</p>
        <div className="flex w-full h-10 rounded-note overflow-hidden border-2 border-line">
          <div
            className="flex items-center justify-center bg-action text-white text-[10px] font-bold px-1 text-center leading-tight"
            style={{ width: `${share}%` }}
          >
            {share}%
          </div>
          <div
            className="flex items-center justify-center bg-soft text-ink text-[10px] font-bold px-1 text-center leading-tight"
            style={{ width: `${100 - share}%` }}
          >
            {100 - share}%
          </div>
        </div>
        <div className="flex justify-between mt-1.5 gap-2">
          <p className="text-xs text-action font-semibold leading-tight">{visual.left}</p>
          <p className="text-xs text-ink-muted font-semibold text-right leading-tight">{visual.right}</p>
        </div>
      </div>
    );
  }

  if (visual.type === 'mapping') {
    return (
      <table className="w-full text-sm border-collapse">
        <tbody>
          {visual.rows.map((row, i) => (
            <tr key={i} className={i === 0 ? 'bg-soft' : ''}>
              <td className="border-2 border-line px-3 py-2 font-bold text-ink w-1/2">{row[0]}</td>
              <td className="border-2 border-line px-3 py-2 text-ink">{row[1]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  // groups
  return (
    <div>
      <p className="text-xs font-bold text-ink mb-2">{visual.target}</p>
      <div className="flex gap-1.5 flex-wrap">
        {visual.caps.map((cap, i) => (
          <div key={i} className="flex flex-col items-center gap-1">
            <div className="w-12 h-12 rounded-tile border-2 border-line bg-soft flex items-center justify-center text-sm font-extrabold text-ink">
              {cap}
            </div>
            {visual.labels[i] && (
              <span className="text-[9px] text-ink-muted font-semibold text-center leading-tight max-w-[3.5rem]">
                {visual.labels[i]}
              </span>
            )}
          </div>
        ))}
      </div>
      {visual.capLabel && (
        <p className="text-xs text-ink-muted font-semibold mt-1.5">{visual.capLabel}</p>
      )}
    </div>
  );
}
