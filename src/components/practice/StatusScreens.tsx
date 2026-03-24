'use client';

import { useEffect, useState } from 'react';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import ShareSheet from '@/components/ShareSheet';
import type { QuestionResult, GradeUpCta } from './constants';

export function ReviewIntroScreen({ count, onStart }: { count: number; onStart: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] px-6 gap-6 text-center">
      <div className="animate-sparky-bounce">
        <Sparky mood="encouraging" size={120} />
      </div>
      <div className="space-y-2">
        <h2 className="text-2xl font-extrabold text-gray-800">
          Let&#39;s review the tricky ones! 💪
        </h2>
        <p className="text-gray-500 font-medium">
          {count} question{count !== 1 ? 's' : ''} to review — you&#39;ve got this!
        </p>
      </div>
      <DuoButton variant="blue" fullWidth onClick={onStart}>
        Start review →
      </DuoButton>
    </div>
  );
}

export function NoHeartsScreen({
  results,
  onRetry,
  onHome,
}: {
  results: QuestionResult[];
  onRetry: () => void;
  onHome: () => void;
}) {
  const wrong = results.filter((r) => !r.wasCorrect);
  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-white pb-8">
      <div className="animate-sparky-wave">
        <Sparky mood="encouraging" size={120} />
      </div>
      <div className="text-center space-y-2">
        <h2 className="text-2xl font-extrabold text-gray-800">
          Let&#39;s take a break and review! 📚
        </h2>
        <p className="text-gray-500 font-medium">
          You ran out of hearts — that&#39;s okay! Every attempt makes you stronger.
        </p>
      </div>

      {wrong.length > 0 && (
        <div className="w-full space-y-2">
          <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">Questions to revisit</p>
          {wrong.map((r) => (
            <div key={r.questionId} className="bg-red-50 border-2 border-red-100 rounded-2xl px-4 py-3">
              <p className="text-sm text-gray-700 font-medium line-clamp-2">{r.questionText}</p>
              <p className="text-xs text-duo-green font-extrabold mt-1">Answer: {r.correctAnswer}</p>
            </div>
          ))}
        </div>
      )}

      <div className="w-full space-y-3">
        <DuoButton variant="green" fullWidth onClick={onRetry}>
          Try again ↺
        </DuoButton>
        <DuoButton variant="white" fullWidth onClick={onHome}>
          Back to chapters
        </DuoButton>
      </div>
    </div>
  );
}

export function LessonCompleteScreen({
  mainResults,
  reviewResults,
  totalXp,
  hasReviewMistakes,
  onContinue,
  onReviewMistakes,
  shareData,
  gradeUpCta,
}: {
  mainResults:       QuestionResult[];
  reviewResults:     QuestionResult[];
  totalXp:           number;
  hasReviewMistakes: boolean;
  onContinue:        () => void;
  onReviewMistakes:  () => void;
  gradeUpCta?:       GradeUpCta;
  shareData?: {
    studentId:    string;
    studentName:  string;
    topicName:    string;
    topicEmoji:   string;
    parentEmail:  string;
    parentWhatsApp: string;
  };
}) {
  const allResults  = [...mainResults, ...reviewResults];
  const correct     = allResults.filter((r) => r.wasCorrect).length;
  const total       = allResults.length;
  const pct         = total > 0 ? Math.round((correct / total) * 100) : 100;
  const stars       = pct >= 90 ? 3 : pct >= 70 ? 2 : 1;
  const message     = pct >= 90 ? 'Amazing! 🏆' : pct >= 70 ? 'Great job! 🌟' : 'Keep practicing! 💪';

  // XP count-up animation
  const [displayXp, setDisplayXp] = useState(0);
  useEffect(() => {
    let cur = 0;
    const step = totalXp / 40;
    const interval = setInterval(() => {
      cur = Math.min(cur + step, totalXp);
      setDisplayXp(Math.round(cur));
      if (cur >= totalXp) clearInterval(interval);
    }, 40);
    return () => clearInterval(interval);
  }, [totalXp]);

  // Accuracy ring
  const r    = 52;
  const circ = 2 * Math.PI * r;
  const dash = circ * (pct / 100);

  const wrongOnes = allResults.filter((r) => !r.wasCorrect);
  const [showShare, setShowShare] = useState(false);

  return (
    <div className="flex flex-col items-center px-6 py-8 gap-6 bg-white min-h-screen pb-24">
      {showShare && shareData && (
        <ShareSheet
          card={{ type: 'lesson', data: {
            studentName: shareData.studentName,
            topicName:   shareData.topicName,
            topicEmoji:  shareData.topicEmoji,
            correct,
            total,
            xp:          totalXp,
            date:        new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }),
          }}}
          studentId={shareData.studentId}
          parentEmail={shareData.parentEmail || undefined}
          parentWhatsApp={shareData.parentWhatsApp || undefined}
          onClose={() => setShowShare(false)}
        />
      )}
      <Confetti />

      {/* Sparky celebrating */}
      <div className="animate-sparky-dance">
        <Sparky mood="celebrating" size={140} />
      </div>

      <h1 className="text-2xl font-extrabold text-gray-800 text-center">{message}</h1>

      {/* Accuracy ring */}
      <svg width="140" height="140" viewBox="0 0 140 140">
        <circle cx="70" cy="70" r={r} fill="none" stroke="#e5e7eb" strokeWidth="12" />
        <circle
          cx="70" cy="70" r={r} fill="none"
          stroke={pct >= 70 ? '#58CC02' : '#FF9600'}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={`${dash} ${circ}`}
          transform="rotate(-90 70 70)"
          style={{ transition: 'stroke-dasharray 1s ease-out' }}
        />
        <text x="70" y="64" textAnchor="middle" fontSize="26" fontWeight="900" fill="#131F24">
          {pct}%
        </text>
        <text x="70" y="84" textAnchor="middle" fontSize="11" fill="#9ca3af" fontWeight="600">
          {correct}/{total} correct
        </text>
      </svg>

      {/* Stars */}
      <div className="flex gap-3 text-4xl">
        {[1, 2, 3].map((s) => (
          <span key={s} className="transition-opacity" style={{ opacity: s <= stars ? 1 : 0.2, filter: s <= stars ? 'none' : 'grayscale(1)' }}>
            ⭐
          </span>
        ))}
      </div>

      {/* XP */}
      <div className="bg-[#FFF9E6] border-2 border-duo-gold rounded-2xl px-8 py-3 text-center">
        <p className="text-xs text-amber-700 font-extrabold uppercase tracking-wide">Total XP earned</p>
        <p className="text-3xl font-extrabold text-duo-dark">+{displayXp} ⭐</p>
      </div>

      {/* Wrong answers to revisit */}
      {wrongOnes.length > 0 && (
        <div className="w-full space-y-2">
          <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">
            {hasReviewMistakes ? 'Still needs work' : 'Review at home'}
          </p>
          {wrongOnes.map((r) => (
            <div key={r.questionId} className="bg-red-50 border border-red-100 rounded-xl px-4 py-3">
              <p className="text-xs text-gray-700 font-medium line-clamp-2">{r.questionText}</p>
              <p className="text-xs text-duo-green font-extrabold mt-0.5">Correct: {r.correctAnswer}</p>
            </div>
          ))}
        </div>
      )}

      <div className="w-full space-y-3">
        {/* Grade level-up CTA */}
        {gradeUpCta && (
          gradeUpCta.type === 'full' ? (
            <DuoButton variant="blue" fullWidth onClick={gradeUpCta.onPress}>
              Level Up to Grade {gradeUpCta.grade}! 🚀
            </DuoButton>
          ) : gradeUpCta.type === 'sample' ? (
            <DuoButton variant="blue" fullWidth onClick={gradeUpCta.onPress}>
              Try Grade {gradeUpCta.grade} — 5 Free Questions 🔓
            </DuoButton>
          ) : (
            <button
              onClick={gradeUpCta.onPress}
              className="w-full min-h-[48px] rounded-full border-2 border-amber-200 font-extrabold text-amber-600 text-sm hover:bg-amber-50 transition-colors"
            >
              Upgrade to unlock Grade {gradeUpCta.grade} 🔒
            </button>
          )
        )}

        <DuoButton variant="green" fullWidth onClick={onContinue}>
          Continue to chapters 🎯
        </DuoButton>
        {hasReviewMistakes && (
          <DuoButton variant="blue" fullWidth onClick={onReviewMistakes}>
            Review mistakes 📚
          </DuoButton>
        )}
        {shareData && (
          <button
            onClick={() => setShowShare(true)}
            className="w-full min-h-[48px] rounded-full border-2 border-gray-200 font-extrabold text-gray-500 text-sm hover:bg-gray-50 transition-colors flex items-center justify-center gap-2"
          >
            📤 Share with Parents
          </button>
        )}
      </div>
    </div>
  );
}
