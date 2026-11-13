'use client';

interface TopicSelectCardProps {
  emoji: string;
  name: string;
  selected: boolean;
  onToggle: () => void;
  muted?: boolean;
}

export default function TopicSelectCard({ emoji, name, selected, onToggle, muted }: TopicSelectCardProps) {
  return (
    <button
      onClick={onToggle}
      className={`flex items-center gap-3 rounded-control px-4 py-3 border-2 transition-[colors,border-color,transform] active:scale-95 text-left w-full min-h-0 ${
        selected
          ? 'bg-soft border-action'
          : muted
            ? 'bg-gray-50/60 border-line text-ink-muted'
            : 'bg-white border-line hover:border-ink'
      }`}
    >
      <span className="text-xl leading-none shrink-0" aria-hidden="true">{emoji}</span>
      <span className={`font-bold text-sm flex-1 ${selected ? 'text-ink' : muted ? 'text-ink-muted' : 'text-ink'}`}>
        {name}
      </span>
      {selected && (
        <span className="text-action text-lg leading-none shrink-0" aria-hidden="true">✓</span>
      )}
    </button>
  );
}
