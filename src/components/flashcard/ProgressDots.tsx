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
      <div className="flex items-center justify-center gap-2 py-2 px-3 bg-card rounded-control">
        <span className="text-xs font-bold text-ink tabular-nums">
          {completed}
        </span>
        <div className="ui-meter w-32 h-3">
          <div
            className="h-full bg-action rounded-full transition-[width] duration-300"
            style={{ width: `${total > 0 ? (completed / total) * 100 : 0}%` }}
          />
        </div>
        <span className="text-xs font-bold text-ink-muted tabular-nums">
          {total}
        </span>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center gap-1 py-2 px-3 flex-wrap bg-card rounded-control">
      {Array.from({ length: total }).map((_, i) => {
        const isDone = i < completed;
        const isCurrent = i === current;
        return (
          <div
            key={i}
            className={`rounded-[4px] border-2 transition-[background-color,width,height] duration-300 ${
              isDone
                ? 'w-3 h-3 bg-action border-action'
                : isCurrent
                ? 'w-3 h-3 bg-card border-ink shadow-hard-xs animate-pulse'
                : 'w-3 h-3 bg-card border-line'
            }`}
          />
        );
      })}
    </div>
  );
}
