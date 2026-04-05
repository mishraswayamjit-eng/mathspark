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
      className={`flex items-center gap-3 rounded-2xl px-4 py-3 border-2 transition-[colors,border-color,transform] active:scale-95 text-left w-full min-h-0 ${
        selected
          ? 'bg-green-50 border-duo-green shadow-sm'
          : muted
            ? 'bg-gray-50/60 border-gray-100 text-gray-400'
            : 'bg-white border-gray-200 hover:border-gray-300'
      }`}
    >
      <span className="text-xl leading-none shrink-0" aria-hidden="true">{emoji}</span>
      <span className={`font-bold text-sm flex-1 ${selected ? 'text-gray-800' : muted ? 'text-gray-400' : 'text-gray-700'}`}>
        {name}
      </span>
      {selected && (
        <span className="text-duo-green text-lg leading-none shrink-0" aria-hidden="true">✓</span>
      )}
    </button>
  );
}
