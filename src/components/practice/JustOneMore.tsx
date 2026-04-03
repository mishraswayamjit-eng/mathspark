'use client';

import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';

interface JustOneMoreProps {
  topicId: string;
  topicName: string;
  streak: number;
  onAccept: () => void;
  onDecline: () => void;
}

const LESSONS_KEY = 'mathspark_today_lessons';
const LESSONS_DATE_KEY = 'mathspark_today_lessons_date';

function getTodayLessons(): number {
  if (typeof window === 'undefined') return 0;
  const today = new Date().toDateString();
  if (localStorage.getItem(LESSONS_DATE_KEY) !== today) {
    localStorage.setItem(LESSONS_KEY, '0');
    localStorage.setItem(LESSONS_DATE_KEY, today);
    return 0;
  }
  return parseInt(localStorage.getItem(LESSONS_KEY) ?? '0', 10);
}

export function incrementTodayLessons(): void {
  if (typeof window === 'undefined') return;
  const today = new Date().toDateString();
  if (localStorage.getItem(LESSONS_DATE_KEY) !== today) {
    localStorage.setItem(LESSONS_KEY, '1');
    localStorage.setItem(LESSONS_DATE_KEY, today);
    return;
  }
  const cur = parseInt(localStorage.getItem(LESSONS_KEY) ?? '0', 10);
  localStorage.setItem(LESSONS_KEY, String(cur + 1));
}

export default function JustOneMore({
  topicName,
  streak,
  onAccept,
  onDecline,
}: JustOneMoreProps) {
  // Only show when streak >= 3 and fewer than 3 lessons today
  if (streak < 3 || getTodayLessons() >= 3) return null;

  return (
    <div className="w-full bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-duo-green rounded-2xl p-4 space-y-3 animate-pop-in">
      <div className="flex items-center gap-3">
        <Sparky mood="encouraging" size={48} />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-extrabold text-gray-800">
            You&apos;re on fire! <span aria-hidden="true">🔥</span>
          </p>
          <p className="text-xs text-gray-600 font-medium">
            One more {topicName} lesson? ~5 min
          </p>
        </div>
      </div>

      <DuoButton variant="green" fullWidth onClick={onAccept}>
        Let&apos;s go! 🚀
      </DuoButton>

      <button
        onClick={onDecline}
        className="w-full text-center text-gray-500 text-sm font-semibold py-1 hover:text-gray-600 transition-colors"
        style={{ minHeight: 0 }}
      >
        Not now
      </button>
    </div>
  );
}
