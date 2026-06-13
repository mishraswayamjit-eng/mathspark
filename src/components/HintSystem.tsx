'use client';

interface HintSystemProps {
  hint1: string;
  hint2: string;
  hint3: string;
  level: number;             // 0 = none, 1 = strategic, 2 = procedural, 3 = worked
  onLevelUp: (next: number) => void;
}

export default function HintSystem({ hint1, hint2, hint3, level, onLevelUp }: HintSystemProps) {
  if (level === 0 || !hint1) return null;

  return (
    <div className="rounded-spark bg-spark-amber-soft border border-spark-amber/40 p-4 space-y-3">
      {/* Level 1 — strategic (auto-shown on wrong) */}
      {level >= 1 && hint1 && (
        <div>
          <p className="text-xs font-body font-bold text-spark-amber uppercase tracking-wide mb-1">
            💡 Hint
          </p>
          <p className="font-body text-ink text-sm leading-relaxed">{hint1}</p>
        </div>
      )}

      {/* Level 2 — procedural */}
      {level >= 2 && hint2 && (
        <div className="border-t border-spark-amber/30 pt-3">
          <p className="text-xs font-body font-bold text-spark-amber uppercase tracking-wide mb-1">
            📝 Step hint
          </p>
          <p className="font-body text-ink text-sm leading-relaxed">{hint2}</p>
        </div>
      )}

      {/* Level 3 — worked example */}
      {level >= 3 && hint3 && (
        <div className="border-t border-spark-amber/30 pt-3">
          <p className="text-xs font-body font-bold text-spark-amber uppercase tracking-wide mb-1">
            🔍 Worked example
          </p>
          <p className="font-body text-ink text-sm leading-relaxed">{hint3}</p>
        </div>
      )}

      {/* Buttons to reveal next level */}
      {level === 1 && hint2 && (
        <button
          onClick={() => onLevelUp(2)}
          className="w-full py-2.5 rounded-2xl bg-white/70 hover:bg-white text-spark-amber text-sm font-body font-bold transition-colors"
          aria-expanded={level >= 2}
          aria-label="Show hint level 2"
        >
          Need more help?
        </button>
      )}
      {level === 2 && hint3 && (
        <button
          onClick={() => onLevelUp(3)}
          className="w-full py-2.5 rounded-2xl bg-white/70 hover:bg-white text-spark-amber text-sm font-body font-bold transition-colors"
          aria-expanded={level >= 3}
          aria-label="Show hint level 3"
        >
          Show me how
        </button>
      )}
    </div>
  );
}
