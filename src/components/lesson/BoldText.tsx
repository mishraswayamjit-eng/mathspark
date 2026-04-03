import React from 'react';
import KatexRenderer from '@/components/KatexRenderer';

function hasLatex(text: string): boolean {
  return /[\\{]/.test(text);
}

export default function BoldText({ text }: { text: string }) {
  // If the entire string is LaTeX, render it directly
  if (hasLatex(text) && !text.includes('**')) {
    return <KatexRenderer latex={text} className="text-sm" />;
  }

  // Split on **...** markers
  const parts = text.split(/(\*\*[^*]+\*\*)/g);

  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          const inner = part.slice(2, -2);
          if (hasLatex(inner)) {
            return <KatexRenderer key={i} latex={inner} className="text-sm font-bold" />;
          }
          return <strong key={i} className="font-extrabold text-gray-900">{inner}</strong>;
        }
        if (hasLatex(part)) {
          return <KatexRenderer key={i} latex={part} className="text-sm" />;
        }
        return <span key={i}>{part}</span>;
      })}
    </>
  );
}
