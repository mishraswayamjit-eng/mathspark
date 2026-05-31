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
    <div className="rounded-2xl bg-amber-50 border border-amber-200 p-4 space-y-3">
      {/* Level 1 — strategic (auto-shown on wrong) */}
      {level >= 1 && hint1 && (
        <div>
          <p className="text-xs font-semibold text-amber-700 uppercase tracking-wide mb-1">
            💡 Hint
          </p>
          <p className="text-gray-700 text-sm leading-relaxed">{hint1}</p>
        </div>
      )}

      {/* Level 2 — procedural */}
      {level >= 2 && hint2 && (
        <div className="border-t border-amber-200 pt-3">
          <p className="text-xs font-semibold text-amber-700 uppercase tracking-wide mb-1">
            📝 Step hint
          </p>
          <p className="text-gray-700 text-sm leading-relaxed">{hint2}</p>
        </div>
      )}

      {/* Level 3 — worked example */}
      {level >= 3 && hint3 && (
        <div className="border-t border-amber-200 pt-3">
          <p className="text-xs font-semibold text-amber-700 uppercase tracking-wide mb-1">
            🔍 Worked example
          </p>
          <p className="text-gray-700 text-sm leading-relaxed">{hint3}</p>
        </div>
      )}

      {/* Buttons to reveal next level */}
      {level === 1 && hint2 && (
        <button
          onClick={() => onLevelUp(2)}
          className="w-full py-2 rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-800 text-sm font-semibold transition-colors"
          aria-expanded={false}
          aria-label="Show hint level 2"
        >
          Need more help?
        </button>
      )}
      {level === 2 && hint3 && (
        <button
          onClick={() => onLevelUp(3)}
          className="w-full py-2 rounded-xl bg-amber-100 hover:bg-amber-200 text-amber-800 text-sm font-semibold transition-colors"
          aria-expanded={false}
          aria-label="Show hint level 3"
        >
          Show me how
        </button>
      )}
    </div>
  );
}
