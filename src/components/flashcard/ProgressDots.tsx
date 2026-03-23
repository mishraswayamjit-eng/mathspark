'use client';

interface ProgressDotsProps {
  total: number;
  current: number;    // 0-indexed
  completed: number;  // how many are done
}

export default function ProgressDots({ total, current, completed }: ProgressDotsProps) {
  // Cap at 20 visible dots, show condensed version for large decks
  const maxDots = 20;
  const showCondensed = total > maxDots;

  if (showCondensed) {
    return (
      <div className="flex items-center justify-center gap-2 py-2">
        <span className="text-xs font-bold text-[#34D399] tabular-nums">
          {completed}
        </span>
        <div className="w-32 h-1.5 bg-white/10 rounded-full overflow-hidden">
          <div
            className="h-full bg-[#34D399] rounded-full transition-[width] duration-300"
            style={{ width: `${total > 0 ? (completed / total) * 100 : 0}%` }}
          />
        </div>
        <span className="text-xs text-[#64748B] tabular-nums">
          {total}
        </span>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center gap-1.5 py-2 flex-wrap">
      {Array.from({ length: total }).map((_, i) => {
        const isDone = i < completed;
        const isCurrent = i === current;
        return (
          <div
            key={i}
            className={`rounded-full transition-[background-color,width,height] duration-300 ${
              isDone
                ? 'w-2 h-2 bg-[#34D399]'
                : isCurrent
                ? 'w-3 h-3 bg-[#34D399] animate-pulse'
                : 'w-2 h-2 bg-white/20'
            }`}
          />
        );
      })}
    </div>
  );
}
