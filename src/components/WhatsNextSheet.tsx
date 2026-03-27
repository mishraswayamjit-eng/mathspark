'use client';

import Link from 'next/link';
import Sparky from '@/components/Sparky';
import type { WhatsNextSuggestion } from '@/lib/whatsNext';

function ChevronRight() {
  return (
    <svg className="w-5 h-5 text-white/60 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
    </svg>
  );
}

export default function WhatsNextSheet({ suggestions }: { suggestions: WhatsNextSuggestion[] }) {
  if (suggestions.length === 0) return null;

  return (
    <div className="w-full space-y-3">
      {/* Header */}
      <div className="flex items-center gap-2">
        <Sparky mood="happy" size={28} />
        <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">
          What&apos;s Next?
        </p>
      </div>

      {/* Suggestion cards */}
      <div className="space-y-2">
        {suggestions.map((s, i) => (
          <Link
            key={i}
            href={s.url}
            className={`flex items-center gap-3 px-4 py-3 rounded-2xl ${s.color} text-white font-bold text-sm active:opacity-90 transition-opacity min-h-[48px]`}
          >
            <span className="text-xl shrink-0" aria-hidden="true">{s.icon}</span>
            <div className="flex-1 min-w-0">
              <p className="font-extrabold leading-tight">{s.label}</p>
              <p className="text-white/70 text-xs font-medium mt-0.5">{s.sublabel}</p>
            </div>
            <ChevronRight />
          </Link>
        ))}
      </div>
    </div>
  );
}
