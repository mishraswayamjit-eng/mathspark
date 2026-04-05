'use client';

import Sparky from './Sparky';
import type { SparkyMood } from './Sparky';

interface SparkyBubbleProps {
  message: string;
  size?: number;
  mood?: SparkyMood;
}

export default function SparkyBubble({ message, size = 48, mood = 'happy' }: SparkyBubbleProps) {
  if (!message) return null;

  return (
    <div className="flex items-start gap-3">
      <div className="shrink-0">
        <Sparky mood={mood} size={size} />
      </div>
      <div
        key={message}
        className="bg-gray-100 rounded-2xl px-4 py-2.5 text-sm font-semibold text-gray-700 animate-fade-in max-w-[260px]"
      >
        {message}
      </div>
    </div>
  );
}
