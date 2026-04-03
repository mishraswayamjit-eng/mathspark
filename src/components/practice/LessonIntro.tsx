'use client';

import { useEffect, useRef } from 'react';
import Sparky from '@/components/Sparky';
import DuoButton from '@/components/DuoButton';

interface LessonIntroProps {
  topicName: string;
  topicEmoji: string;
  questionCount: number;
  onStart: () => void;
}

export default function LessonIntro({ topicName, topicEmoji, questionCount, onStart }: LessonIntroProps) {
  const onStartRef = useRef(onStart);
  onStartRef.current = onStart;

  // Auto-start after 3s if user doesn't tap
  useEffect(() => {
    const t = setTimeout(() => onStartRef.current(), 3000);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] px-6 gap-5 text-center animate-fade-in">
      <div className="animate-sparky-bounce">
        <Sparky mood="happy" size={80} />
      </div>

      <div className="animate-pop-in text-5xl" aria-hidden="true">
        {topicEmoji}
      </div>

      <h1 className="text-2xl font-extrabold text-gray-800">
        {topicName}
      </h1>

      <p className="text-sm text-gray-500 font-semibold">
        {questionCount} questions · Earn up to {questionCount * 20} XP
      </p>

      <div className="w-full max-w-xs mt-2">
        <DuoButton variant="green" fullWidth onClick={onStart}>
          Start
        </DuoButton>
      </div>
    </div>
  );
}
