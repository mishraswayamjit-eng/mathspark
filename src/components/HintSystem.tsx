'use client';

import Sparky from './Sparky';
import DuoButton from './DuoButton';

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
    <div className="rounded-2xl bg-[#FFF9E6] border-2 border-[#FF9600] p-4 space-y-3 relative">
      {/* Sparky thinking — top right */}
      <div className="absolute -top-5 right-3">
        <Sparky mood="thinking" size={48} />
      </div>

      {/* Level 1 — strategic (auto-shown on wrong) */}
      {level >= 1 && hint1 && (
        <div>
          <p className="text-xs font-extrabold text-[#cc7800] uppercase tracking-wide mb-1">
            💡 Hint
          </p>
          <p className="text-gray-700 text-sm leading-relaxed font-medium">{hint1}</p>
        </div>
      )}

      {/* Level 2 — procedural */}
      {level >= 2 && hint2 && (
        <div className="border-t border-[#FFD9A0] pt-3">
          <p className="text-xs font-extrabold text-[#cc7800] uppercase tracking-wide mb-1">
            📝 Step hint
          </p>
          <p className="text-gray-700 text-sm leading-relaxed font-medium">{hint2}</p>
        </div>
      )}

      {/* Level 3 — worked example */}
      {level >= 3 && hint3 && (
        <div className="border-t border-[#FFD9A0] pt-3">
          <p className="text-xs font-extrabold text-[#cc7800] uppercase tracking-wide mb-1">
            🔍 Worked example
          </p>
          <p className="text-gray-700 text-sm leading-relaxed font-medium">{hint3}</p>
        </div>
      )}

      {/* Buttons to reveal next level */}
      {level === 1 && hint2 && (
        <DuoButton variant="orange" fullWidth onClick={() => onLevelUp(2)}>
          Need more help?
        </DuoButton>
      )}
      {level === 2 && hint3 && (
        <DuoButton variant="orange" fullWidth onClick={() => onLevelUp(3)}>
          Show me how
        </DuoButton>
      )}
    </div>
  );
}
