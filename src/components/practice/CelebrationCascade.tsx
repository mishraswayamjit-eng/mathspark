'use client';

import { useEffect, useRef, useState } from 'react';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import ShareSheet from '@/components/ShareSheet';
import WhatsNextSheet from '@/components/WhatsNextSheet';
import type { WhatsNextSuggestion } from '@/lib/whatsNext';
import JustOneMore, { incrementTodayLessons } from './JustOneMore';
import type { QuestionResult, GradeUpCta } from './constants';

type Stage = 1 | 2 | 3 | 4;

interface CelebrationCascadeProps {
  mainResults: QuestionResult[];
  reviewResults: QuestionResult[];
  totalXp: number;
  streak: number;
  onComplete: () => void;
  hasReviewMistakes: boolean;
  onReviewMistakes: () => void;
  gradeUpCta?: GradeUpCta;
  whatsNextSuggestions?: WhatsNextSuggestion[];
  topicId?: string;
  topicName?: string;
  shareData?: {
    studentId: string;
    studentName: string;
    topicName: string;
    topicEmoji: string;
    parentEmail: string;
    parentWhatsApp: string;
  };
}

export default function CelebrationCascade({
  mainResults,
  reviewResults,
  totalXp,
  streak,
  onComplete,
  hasReviewMistakes,
  onReviewMistakes,
  gradeUpCta,
  whatsNextSuggestions,
  topicId,
  topicName,
  shareData,
}: CelebrationCascadeProps) {
  const [stage, setStage] = useState<Stage>(1);
  const [showShare, setShowShare] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const allResults = [...mainResults, ...reviewResults];
  const correct = allResults.filter((r) => r.wasCorrect).length;
  const total = allResults.length;
  const pct = total > 0 ? Math.round((correct / total) * 100) : 100;
  const stars = pct >= 90 ? 3 : pct >= 70 ? 2 : 1;

  // Auto-advance stages 1→2→3→4
  useEffect(() => {
    if (stage < 4) {
      const delay = stage === 1 ? 1500 : 2000;
      timerRef.current = setTimeout(() => setStage((s) => (s + 1) as Stage), delay);
      return () => { if (timerRef.current) clearTimeout(timerRef.current); };
    }
  }, [stage]);

  // Tap to skip to next stage
  const handleTap = () => {
    if (stage < 4) {
      if (timerRef.current) clearTimeout(timerRef.current);
      setStage((s) => (s + 1) as Stage);
    }
  };

  // ── XP count-up for stage 3 ──
  const [displayXp, setDisplayXp] = useState(0);
  useEffect(() => {
    if (stage !== 3) return;
    let cur = 0;
    const step = totalXp / 40;
    const interval = setInterval(() => {
      cur = Math.min(cur + step, totalXp);
      setDisplayXp(Math.round(cur));
      if (cur >= totalXp) clearInterval(interval);
    }, 40);
    return () => clearInterval(interval);
  }, [stage, totalXp]);

  // ── Accuracy ring for stage 1 ──
  const r = 52;
  const circ = 2 * Math.PI * r;
  const [animPct, setAnimPct] = useState(0);
  useEffect(() => {
    if (stage !== 1) return;
    const t = setTimeout(() => setAnimPct(pct), 50);
    return () => clearTimeout(t);
  }, [stage, pct]);
  const dash = circ * (animPct / 100);

  const wrongOnes = allResults.filter((r) => !r.wasCorrect);

  // ── Stage 1: Skill Check ──
  if (stage === 1) {
    return (
      <div
        className="fixed inset-0 z-[70] bg-paper flex flex-col items-center justify-center px-6 animate-fade-in"
        onClick={handleTap}
      >
        <svg width="160" height="160" viewBox="0 0 160 160" className="mb-4">
          <circle cx="80" cy="80" r={r} fill="none" stroke="#d3deee" strokeWidth="12" />
          <circle
            cx="80" cy="80" r={r} fill="none"
            stroke={pct >= 70 ? '#12805c' : '#f5a400'}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={`${dash} ${circ}`}
            transform="rotate(-90 80 80)"
            style={{ transition: 'stroke-dasharray 1s ease-out' }}
          />
          <text x="80" y="74" textAnchor="middle" fontSize="30" fontWeight="900" fill="#1d2a4d">
            {animPct}%
          </text>
          <text x="80" y="96" textAnchor="middle" fontSize="12" fill="#5d6b8c" fontWeight="600">
            {correct}/{total} correct
          </text>
        </svg>

        {/* Stars */}
        <div className="flex gap-3 text-4xl mb-2">
          {[1, 2, 3].map((s, i) => (
            <span
              key={s}
              className="animate-pop-in"
              style={{
                opacity: s <= stars ? 1 : 0.2,
                filter: s <= stars ? 'none' : 'grayscale(1)',
                animationDelay: `${0.3 + i * 0.15}s`,
                animationFillMode: 'backwards',
              }}
            >
              ⭐
            </span>
          ))}
        </div>

        <p className="text-xs font-bold text-ink-muted mt-4">Tap to continue</p>
      </div>
    );
  }

  // ── Stage 2: Lesson Complete ──
  if (stage === 2) {
    return (
      <div
        className="fixed inset-0 z-[70] bg-paper flex flex-col items-center justify-center px-6 animate-stage-crossfade"
        onClick={handleTap}
      >
        <Confetti />

        <div className="animate-sparky-dance">
          <Sparky mood="celebrating" size={140} />
        </div>

        <h1 className="text-display text-ink mt-4 animate-pop-in">
          Lesson Complete!
        </h1>

        <p className="text-sm text-ink-muted font-bold mt-1">
          {pct >= 90 ? 'Amazing! 🏆' : pct >= 70 ? 'Great job! 🌟' : 'Keep practicing! 💪'}
        </p>

        <p className="text-xs font-bold text-ink-muted mt-6">Tap to continue</p>
      </div>
    );
  }

  // ── Stage 3: XP Tally ──
  if (stage === 3) {
    return (
      <div
        className="fixed inset-0 z-[70] bg-paper flex flex-col items-center justify-center px-6 animate-stage-crossfade"
        onClick={handleTap}
      >
        <div className="bg-hint border-2 border-star rounded-card px-10 py-5 text-center animate-pop-in">
          <p className="text-caption text-hint-ink">Total XP earned</p>
          <p className="text-4xl font-extrabold text-ink animate-count-pulse">+{displayXp} <span aria-hidden="true">⭐</span></p>
        </div>

        <div className="mt-4 text-sm text-ink-muted font-semibold space-y-1 text-center">
          <p>{correct} correct × 20 XP</p>
          {reviewResults.length > 0 && (
            <p>{reviewResults.filter((r) => r.wasCorrect).length} review × 10 XP</p>
          )}
        </div>

        <p className="text-xs font-bold text-ink-muted mt-6">Tap to continue</p>
      </div>
    );
  }

  // ── Stage 4: Summary + Actions ──
  return (
    <div className="flex flex-col items-center px-6 py-8 gap-5 bg-paper min-h-screen pb-24 animate-stage-crossfade">
      {showShare && shareData && (
        <ShareSheet
          card={{ type: 'lesson', data: {
            studentName: shareData.studentName,
            topicName: shareData.topicName,
            topicEmoji: shareData.topicEmoji,
            correct,
            total,
            xp: totalXp,
            date: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }),
          }}}
          studentId={shareData.studentId}
          parentEmail={shareData.parentEmail || undefined}
          parentWhatsApp={shareData.parentWhatsApp || undefined}
          onClose={() => setShowShare(false)}
        />
      )}

      {/* Streak */}
      {streak > 0 && (
        <div className="flex items-center gap-2 bg-hint border-2 border-star rounded-full px-4 py-2 animate-pop-in">
          <span className="text-lg" aria-hidden="true">🔥</span>
          <span className="text-lg font-extrabold text-ink">{streak}</span>
          <span className="text-xs text-hint-ink font-bold">question streak</span>
        </div>
      )}

      {/* Wrong answers */}
      {wrongOnes.length > 0 && (
        <div className="w-full space-y-2">
          <p className="text-caption text-ink-muted">
            {hasReviewMistakes ? 'Still needs work' : 'Review at home'}
          </p>
          {wrongOnes.map((r) => (
            <div key={r.questionId} className="bg-white border-2 border-line rounded-note px-4 py-3">
              <p className="text-xs text-ink font-semibold line-clamp-2">{r.questionText}</p>
              <p className="text-sm text-success font-extrabold mt-0.5">Correct: {r.correctAnswer}</p>
            </div>
          ))}
        </div>
      )}

      {/* Just One More prompt */}
      {topicId && topicName && (
        <JustOneMore
          topicId={topicId}
          topicName={topicName}
          streak={streak}
          onAccept={() => {
            incrementTodayLessons();
            window.location.href = `/practice/${topicId}`;
          }}
          onDecline={onComplete}
        />
      )}

      {/* Actions */}
      <div className="w-full space-y-3 mt-2">
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
              className="ui-btn w-full text-sm"
            >
              Upgrade to unlock Grade {gradeUpCta.grade} 🔒
            </button>
          )
        )}

        {whatsNextSuggestions && whatsNextSuggestions.length > 0 ? (
          <WhatsNextSheet suggestions={whatsNextSuggestions} />
        ) : (
          <DuoButton variant="green" fullWidth onClick={onComplete}>
            Continue to chapters 🎯
          </DuoButton>
        )}

        {hasReviewMistakes && (
          <DuoButton variant="blue" fullWidth onClick={onReviewMistakes}>
            Review mistakes 📚
          </DuoButton>
        )}

        {shareData && (
          <button
            onClick={() => setShowShare(true)}
            className="ui-btn w-full text-sm"
          >
            <span aria-hidden="true">📤</span> Share with Parents
          </button>
        )}
      </div>
    </div>
  );
}
