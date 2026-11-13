'use client';

import React from 'react';
import Sparky from './Sparky';
import DuoButton from './DuoButton';
import KatexRenderer from './KatexRenderer';

interface HintSystemProps {
  hint1: string;
  hint2: string;
  hint3: string;
  level: number;           // 0 = none shown, 1 = strategic, 2 = procedural, 3 = worked example
  onLevelUp: (next: number) => void;
}

/** Returns true if a string contains LaTeX markup (backslash commands). */
function hasLatex(text: string): boolean {
  return text.includes('\\');
}

/** Renders text with KaTeX support when LaTeX markers are detected. */
function HintText({ text }: { text: string }) {
  if (hasLatex(text)) {
    return <KatexRenderer latex={text} displayMode={false} />;
  }
  return <>{text}</>;
}

const HintSystem = React.memo(function HintSystem({ hint1, hint2, hint3, level, onLevelUp }: HintSystemProps) {
  if (level === 0 || !hint1) return null;

  return (
    <div className="ui-hint space-y-3 relative animate-card-pop">
      {/* Sparky thinking */}
      <div className="absolute -top-5 right-3">
        <Sparky mood="thinking" size={48} />
      </div>

      {/* Level 1 — strategic hint (auto-shown after wrong answer) */}
      {level >= 1 && hint1 && (
        <div className="animate-fade-in">
          <p className="text-sm font-extrabold mb-1">
            💡 Hint
          </p>
          <p className="text-[15px] leading-relaxed font-bold">
            <HintText text={hint1} />
          </p>
        </div>
      )}

      {/* Level 2 — procedural hint */}
      {level >= 2 && hint2 && (
        <div className="border-t-2 border-dashed border-hint-ink/40 pt-3 animate-fade-in">
          <p className="text-sm font-extrabold mb-1">
            📝 Step hint
          </p>
          <p className="text-[15px] leading-relaxed font-bold">
            <HintText text={hint2} />
          </p>
        </div>
      )}

      {/* Level 3 — worked example */}
      {level >= 3 && hint3 && (
        <div className="border-t-2 border-dashed border-hint-ink/40 pt-3 animate-fade-in">
          <p className="text-sm font-extrabold mb-1">
            🔍 Worked example
          </p>
          <p className="text-[15px] leading-relaxed font-bold">
            <HintText text={hint3} />
          </p>
        </div>
      )}

      {/* Progressive reveal buttons */}
      {level === 1 && hint2 && (
        <DuoButton variant="orange" fullWidth onClick={() => onLevelUp(2)}>
          Need more help? 🤔
        </DuoButton>
      )}
      {level === 2 && hint3 && (
        <DuoButton variant="orange" fullWidth onClick={() => onLevelUp(3)}>
          Show me how 📝
        </DuoButton>
      )}
    </div>
  );
});

export default HintSystem;
