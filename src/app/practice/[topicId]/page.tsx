'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { track } from '@vercel/analytics';
import QuestionCard from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import KatexRenderer from '@/components/KatexRenderer';
import StepByStep from '@/components/StepByStep';
import AnimatedWalkthrough from '@/components/AnimatedWalkthrough';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import { useSounds } from '@/hooks/useSounds';
import type { Question, AnswerKey } from '@/types';
import { saveSessionData } from '@/lib/nudges';
import { formatMinutes, isUnlimitedPlan } from '@/lib/usageLimits';
import ShareSheet from '@/components/ShareSheet';
import { isGradeAccessible, getTopicGrade } from '@/lib/gradeAccess';

// ── Constants ─────────────────────────────────────────────────────────────────

const LESSON_SIZE    = 10;
const HEARTS_MAX     = 5;
const XP_CORRECT     = 20;
const XP_REVIEW      = 10;
const AUTO_ADVANCE_MS = 2000;
const SPEED_DRILL_MS  = 90_000; // 90 seconds per question
const MAX_BONUS_PER_LESSON = 5;
const MAX_BONUS_PER_ORIGIN = 2;

// ── Types ─────────────────────────────────────────────────────────────────────

type Phase =
  | 'loading'
  | 'answering'
  | 'result'
  | 'no_hearts'
  | 'review_intro'
  | 'reviewing'
  | 'complete'
  | 'usage_limit'
  | 'trial_limit';

interface TrialStatus {
  isSubscribed:      boolean;
  lifetimeQuestions: number;
  todayQuestions:    number;
}

type BonusMode = 'off' | 'searching' | 'answering' | 'result' | 'unavailable';

interface QuestionResult {
  questionId:    string;
  questionText:  string;
  wasCorrect:    boolean;
  selectedAnswer: AnswerKey;
  correctAnswer:  AnswerKey;
}

// ── Card accent colors (visual variety per question slot) ─────────────────────

const TOPIC_EMOJI: Record<string, string> = {
  'ch01-05': '🔢', 'ch06': '🔑', 'ch07-08': '🍕', 'ch09-10': '➗',
  'ch11': '📊', 'ch12': '📏', 'ch13': '🔤', 'ch14': '⚖️',
  'ch15': '🧩', 'ch16': '🔢', 'ch17': '🕐', 'ch18': '📐',
  'ch19': '🔺', 'ch20': '⬜', 'ch21': '⭕', 'dh': '📈',
};

const CARD_ACCENTS = [
  'bg-blue-50 text-blue-700 border-blue-200',
  'bg-purple-50 text-purple-700 border-purple-200',
  'bg-amber-50 text-amber-700 border-amber-200',
  'bg-emerald-50 text-emerald-700 border-emerald-200',
  'bg-rose-50 text-rose-700 border-rose-200',
  'bg-cyan-50 text-cyan-700 border-cyan-200',
  'bg-orange-50 text-orange-700 border-orange-200',
  'bg-indigo-50 text-indigo-700 border-indigo-200',
  'bg-pink-50 text-pink-700 border-pink-200',
  'bg-teal-50 text-teal-700 border-teal-200',
];

// ── Sub-components ────────────────────────────────────────────────────────────

function HeartsBar({ hearts, max = HEARTS_MAX }: { hearts: number; max?: number }) {
  return (
    <div className="flex items-center gap-0.5">
      {Array.from({ length: max }, (_, i) => (
        <span
          key={i}
          className="text-base transition-all duration-300"
          style={{ opacity: i < hearts ? 1 : 0.18, filter: i < hearts ? 'none' : 'grayscale(1)' }}
        >
          ❤️
        </span>
      ))}
    </div>
  );
}

function LessonJourney({
  total,
  currentIdx,
  results,
}: {
  total: number;
  currentIdx: number;
  results: QuestionResult[];
}) {
  return (
    <div className="flex items-center px-4 py-3 gap-0">
      {Array.from({ length: total }, (_, i) => {
        const result    = results[i];
        const isDone    = result !== undefined;
        const isCurrent = i === currentIdx;
        const isCorrect = result?.wasCorrect;

        const circleCls = isDone
          ? isCorrect
            ? 'bg-[#58CC02] border-[#46a302] text-white'
            : 'bg-[#FF4B4B] border-[#cc3333] text-white'
          : isCurrent
          ? 'bg-[#1CB0F6] border-[#0a98dc] text-white ring-4 ring-blue-100 animate-pulse'
          : 'bg-white border-gray-200 text-gray-400';

        const lineCls = i < currentIdx || isDone ? 'bg-[#58CC02]' : 'bg-gray-200';

        return (
          <div key={i} className="flex items-center flex-1 min-w-0">
            {i > 0 && (
              <div className={`h-1 flex-1 rounded-full transition-colors duration-500 ${lineCls}`} />
            )}
            <div
              className={`w-7 h-7 rounded-full border-2 flex items-center justify-center text-[10px] font-extrabold flex-shrink-0 transition-all duration-300 ${circleCls}`}
            >
              {isDone ? (isCorrect ? '✓' : '✗') : i + 1}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function XpFloat({ amount }: { amount: number }) {
  return (
    <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[70] pointer-events-none">
      <span className="animate-xp-float text-2xl font-extrabold text-[#FFC800] drop-shadow-lg whitespace-nowrap">
        +{amount} XP ⭐
      </span>
    </div>
  );
}

function ReviewIntroScreen({ count, onStart }: { count: number; onStart: () => void }) {
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

function NoHeartsScreen({
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
          <p className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">Questions to revisit</p>
          {wrong.map((r) => (
            <div key={r.questionId} className="bg-red-50 border-2 border-red-100 rounded-2xl px-4 py-3">
              <p className="text-sm text-gray-700 font-medium line-clamp-2">{r.questionText}</p>
              <p className="text-xs text-[#58CC02] font-extrabold mt-1">Answer: {r.correctAnswer}</p>
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

interface GradeUpCta {
  grade:   number;
  type:    'full' | 'sample' | 'locked';
  onPress: () => void;
}

function LessonCompleteScreen({
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
  const circ = 2 * Math.PI * r; // 326.7
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
          <span key={s} className="transition-all" style={{ opacity: s <= stars ? 1 : 0.2, filter: s <= stars ? 'none' : 'grayscale(1)' }}>
            ⭐
          </span>
        ))}
      </div>

      {/* XP */}
      <div className="bg-[#FFF9E6] border-2 border-[#FFC800] rounded-2xl px-8 py-3 text-center">
        <p className="text-xs text-amber-700 font-extrabold uppercase tracking-wide">Total XP earned</p>
        <p className="text-3xl font-extrabold text-[#131F24]">+{displayXp} ⭐</p>
      </div>

      {/* Wrong answers to revisit */}
      {wrongOnes.length > 0 && (
        <div className="w-full space-y-2">
          <p className="text-xs font-extrabold text-gray-400 uppercase tracking-wide">
            {hasReviewMistakes ? 'Still needs work' : 'Review at home'}
          </p>
          {wrongOnes.map((r) => (
            <div key={r.questionId} className="bg-red-50 border border-red-100 rounded-xl px-4 py-3">
              <p className="text-xs text-gray-700 font-medium line-clamp-2">{r.questionText}</p>
              <p className="text-xs text-[#58CC02] font-extrabold mt-0.5">Correct: {r.correctAnswer}</p>
            </div>
          ))}
        </div>
      )}

      <div className="w-full space-y-3">
        {/* Grade level-up CTA — shown first when pct >= 80 */}
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

// ── Correct / Wrong sliding panels ────────────────────────────────────────────

function CorrectPanel({
  feedback,
  streak,
  onContinue,
  onWatchSolution,
  onTrySimilar,
  canTrySimilar,
}: {
  feedback:        string;
  streak:          number;
  onContinue:      () => void;
  onWatchSolution: () => void;
  onTrySimilar:    () => void;
  canTrySimilar:   boolean;
}) {
  return (
    <div className="px-4 pt-4 pb-6 space-y-3">
      <div className="flex items-center gap-3">
        <div className="animate-sparky-dance flex-shrink-0">
          <Sparky mood="celebrating" size={56} />
        </div>
        <div>
          {streak >= 3 && (
            <p className="text-xs font-extrabold text-white/80 uppercase tracking-wide mb-0.5">
              🔥 {streak} in a row!
            </p>
          )}
          <p className="text-lg font-extrabold text-white leading-tight">{feedback}</p>
        </div>
      </div>
      <button
        onClick={onWatchSolution}
        className="btn-sparkle w-full min-h-[44px] bg-white/20 border border-white/40 text-white font-extrabold text-sm rounded-2xl py-2 flex items-center justify-center gap-2"
      >
        <span className="sparkle-icon">🎬</span> Watch Solution
      </button>
      {canTrySimilar && (
        <button
          onClick={onTrySimilar}
          className="w-full min-h-[44px] bg-white/10 border border-white/30 text-white font-extrabold text-sm rounded-2xl py-2 flex items-center justify-center gap-2"
        >
          🔄 Try a Similar Question
        </button>
      )}
      <DuoButton variant="white" fullWidth onClick={onContinue}>
        Continue →
      </DuoButton>
    </div>
  );
}

function WrongPanel({
  question,
  selected,
  onGotIt,
  hintLevel,
  onHintLevelUp,
  onWatchSolution,
  onTrySimilar,
  canTrySimilar,
}: {
  question:        Question;
  selected:        AnswerKey | null;
  onGotIt:         () => void;
  hintLevel:       number;
  onHintLevelUp:   (n: number) => void;
  onWatchSolution: () => void;
  onTrySimilar:    () => void;
  canTrySimilar:   boolean;
}) {
  const optionKey     = selected ? (`misconception${selected}` as keyof Question) : null;
  const misconception = optionKey ? (question[optionKey] as string) : '';
  const correctIdx    = ['A', 'B', 'C', 'D'].indexOf(question.correctAnswer);
  const correctText   = question[`option${correctIdx + 1}` as keyof Question] as string;
  const textHasLatex  = correctText.includes('\\');

  return (
    <div className="px-4 pt-4 pb-6 space-y-3">
      {/* Header row */}
      <div className="flex items-center gap-3">
        <div className="flex-shrink-0">
          <Sparky mood="encouraging" size={56} />
        </div>
        <div>
          <p className="text-sm font-extrabold text-[#FF4B4B] uppercase tracking-wide">
            No worries! Here&#39;s how it works…
          </p>
          <div className="bg-white rounded-xl px-3 py-2 border border-red-100 mt-1.5">
            <p className="text-xs text-gray-500 font-semibold">Correct answer ({question.correctAnswer})</p>
            {textHasLatex ? (
              <div className="mt-1"><KatexRenderer latex={correctText} displayMode={false} /></div>
            ) : (
              <p className="text-sm text-gray-800 font-bold leading-snug">{correctText}</p>
            )}
          </div>
        </div>
      </div>

      {/* Misconception box */}
      {misconception && (
        <div className="bg-blue-50 border border-blue-200 rounded-2xl px-4 py-3">
          <p className="text-[11px] font-extrabold text-blue-700 uppercase tracking-wide mb-1">
            💡 Common mistake
          </p>
          <p className="text-sm text-gray-700 font-medium leading-snug">{misconception}</p>
        </div>
      )}

      {/* Step-by-step inline */}
      <StepByStep steps={question.stepByStep} />

      {/* Hints */}
      <HintSystem
        hint1={question.hint1}
        hint2={question.hint2}
        hint3={question.hint3}
        level={hintLevel}
        onLevelUp={onHintLevelUp}
      />

      {/* Action strip */}
      <div className="space-y-2 pt-1">
        {canTrySimilar && (
          <button
            onClick={onTrySimilar}
            className="w-full min-h-[48px] bg-[#58CC02] hover:bg-[#5bd800] text-white font-extrabold text-sm rounded-2xl py-3 flex items-center justify-center gap-2 shadow-sm"
          >
            🔄 Try a Similar Question
          </button>
        )}
        <button
          onClick={onWatchSolution}
          className="btn-sparkle w-full min-h-[44px] bg-gradient-to-r from-violet-500 to-indigo-500 text-white font-extrabold text-sm rounded-2xl py-2 flex items-center justify-center gap-2 shadow-md"
        >
          <span className="sparkle-icon">🎬</span> Watch Solution
        </button>
        <button
          onClick={onGotIt}
          className="w-full min-h-[44px] border border-gray-200 text-gray-500 font-semibold text-sm rounded-2xl py-2 flex items-center justify-center bg-white"
        >
          Got it, move on →
        </button>
      </div>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export default function PracticePage() {
  const params        = useParams();
  const router        = useRouter();
  const searchParams  = useSearchParams();
  const topicId       = params.topicId as string;
  const isSpeedMode   = searchParams.get('mode') === 'speed';
  const isSampleMode  = searchParams.get('sample') === 'true';
  const SAMPLE_LIMIT  = 5;
  const { playCorrect, playWrong, playStreak, muted, toggleMute } = useSounds();

  // ── Core state ─────────────────────────────────────────────────────────────
  const [studentId,   setStudentId]   = useState<string | null>(null);
  const [topicName,   setTopicName]   = useState('');
  const [shareInfo,   setShareInfo]   = useState({ studentName: '', parentEmail: '', parentWhatsApp: '' });
  const [questions,   setQuestions]   = useState<Question[]>([]);
  const [phase,       setPhase]       = useState<Phase>('loading');

  // Current question tracking
  const [qIndex,      setQIndex]      = useState(0);
  const [selected,    setSelected]    = useState<AnswerKey | null>(null);
  const [lastCorrect, setLastCorrect] = useState(false);
  const [hintLevel,   setHintLevel]   = useState(0);
  const [hintUsed,    setHintUsed]    = useState(false); // for this question

  // Lives / XP / Streak
  const [hearts,   setHearts]   = useState(HEARTS_MAX);
  const [xp,       setXp]       = useState(0);
  const [streak,   setStreak]   = useState(0);
  const [feedback, setFeedback] = useState('');

  // Results tracking
  const [results,       setResults]       = useState<QuestionResult[]>([]);
  const reviewQueueRef                    = useRef<Question[]>([]);
  const [reviewQueue,   setReviewQueue]   = useState<Question[]>([]);
  const [reviewIndex,   setReviewIndex]   = useState(0);
  const [reviewResults, setReviewResults] = useState<QuestionResult[]>([]);

  // Animations
  const [showXpFloat,  setShowXpFloat]  = useState(false);
  const [showConfetti, setShowConfetti] = useState(false);

  // Similar question (fetched on wrong answer for "Practice Similar" button)
  // similarQ removed — replaced by bonus question system

  // Speed drill timer
  const [speedRemaining,   setSpeedRemaining]   = useState<number>(SPEED_DRILL_MS);
  const [speedTimedOut,    setSpeedTimedOut]    = useState(false);
  const speedTimerRef      = useRef<ReturnType<typeof setInterval> | null>(null);
  const currentQuestionRef = useRef<Question | null>(null);

  // Offline resilience
  const [isOnline, setIsOnline] = useState(true);

  const advanceTimer    = useRef<ReturnType<typeof setTimeout> | null>(null);
  const sessionSavedRef = useRef(false);

  // ── Adaptive fetching refs ──────────────────────────────────────────────────
  // Stable ref for studentId so callbacks never capture a stale closure.
  const studentIdRef      = useRef<string | null>(null);
  // Pre-fetched next question (filled immediately after user answers).
  const prefetchRef       = useRef<Question | null>(null);
  const isFetchingRef     = useRef(false);
  // BUG 2 FIX: Guard against double-advance (two "Got it!" buttons, timer + tap, etc.)
  const isAdvancingRef    = useRef(false);
  // BUG 1 FIX: Track every question ID served in this lesson so we never repeat.
  const seenQuestionIdsRef = useRef<Set<string>>(new Set());
  // Fetch with 5s timeout + retry tracking
  const [fetchRetry, setFetchRetry] = useState(false);

  // Animated walkthrough
  const [showWalkthrough,    setShowWalkthrough]    = useState(false);
  const [walkthroughClosed,  setWalkthroughClosed]  = useState(false);
  const [sparkyToast,        setSparkyToast]        = useState(false);

  // ── Bonus "Repeat Similar" question system ──────────────────────────────────
  const [bonusMode,      setBonusMode]      = useState<BonusMode>('off');
  const [bonusQuestion,  setBonusQuestion]  = useState<Question | null>(null);
  const [bonusSelected,  setBonusSelected]  = useState<AnswerKey | null>(null);
  const [bonusCorrect,   setBonusCorrect]   = useState(false);
  const [bonusFeedback,  setBonusFeedback]  = useState('');
  const [bonusHintLevel, setBonusHintLevel] = useState(0);
  const [bonusHintUsed,  setBonusHintUsed]  = useState(false);
  const bonusServedRef         = useRef(0);
  const bonusCountByOriginRef  = useRef(new Map<string, number>());
  const bonusOriginRef         = useRef<Question | null>(null);
  const bonusOriginCorrectRef  = useRef(false);

  // ── Usage tracking ──────────────────────────────────────────────────────────
  const [usageInfo, setUsageInfo] = useState<{ used: number; limit: number }>({ used: 0, limit: 0 });
  const heartbeatRef      = useRef<ReturnType<typeof setInterval> | null>(null);
  const heartbeatPhaseRef = useRef(false);

  // ── Trial gate ──────────────────────────────────────────────────────────────
  const [trialStatus, setTrialStatus]           = useState<TrialStatus | null>(null);
  const trialStatusRef                          = useRef<TrialStatus | null>(null);
  const [sessionQuestionsAnswered, setSessionQuestionsAnswered] = useState(0);
  const sessionQuestionsAnsweredRef             = useRef(0);

  // Fetch one adaptive question from the server.
  // Passes the full set of seen question IDs so the server excludes them too.
  const fetchOneAdaptive = useCallback(async (): Promise<Question | null> => {
    const sid = studentIdRef.current;
    if (!sid) return null;
    try {
      const excludeParam = Array.from(seenQuestionIdsRef.current).join(',');
      const url = `/api/questions/next?topicId=${topicId}&studentId=${sid}${excludeParam ? `&exclude=${excludeParam}` : ''}`;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 5000);
      const res = await fetch(url, { signal: controller.signal });
      clearTimeout(timer);
      if (!res.ok) return null;
      const q = (await res.json()) as Question;
      // Client-side duplicate guard: reject if we've already shown this question
      if (seenQuestionIdsRef.current.has(q.id)) return null;
      return q;
    } catch {
      return null;
    }
  }, [topicId]);

  // Kick off a background prefetch of the next question.
  const prefetchNext = useCallback(() => {
    if (isFetchingRef.current || prefetchRef.current) return;
    isFetchingRef.current = true;
    fetchOneAdaptive().then((q) => {
      // Reject the prefetch if it's already in our seen set (race with DB timing)
      if (q && seenQuestionIdsRef.current.has(q.id)) {
        prefetchRef.current  = null;
      } else {
        prefetchRef.current  = q;
      }
      isFetchingRef.current = false;
    });
  }, [fetchOneAdaptive]);

  // BUG 1 FIX: Register each new question in the seen-IDs set the moment it is displayed.
  useEffect(() => {
    const id = phase === 'reviewing' ? reviewQueue[reviewIndex]?.id : questions[qIndex]?.id;
    if (id) seenQuestionIdsRef.current.add(id);
  }, [phase, reviewQueue, reviewIndex, questions, qIndex]);

  // BUG 2 FIX: Reset the advance guard when a new answering phase begins.
  useEffect(() => {
    if (phase === 'answering') {
      isAdvancingRef.current = false;
      setFetchRetry(false);
    }
  }, [phase, qIndex, reviewIndex]);

  // Keep heartbeatPhaseRef in sync so the interval callback knows whether to fire.
  useEffect(() => {
    heartbeatPhaseRef.current = ['answering', 'result', 'review_intro', 'reviewing'].includes(phase);
  }, [phase]);

  // ── Offline attempt queue helpers ──────────────────────────────────────────
  interface AttemptPayload {
    studentId: string; questionId: string; topicId: string;
    selected: string; isCorrect: boolean; hintUsed: number;
    misconceptionType?: string | null;
    isBonusQuestion?: boolean;
    parentQuestionId?: string | null;
  }

  function queueAttempt(p: AttemptPayload) {
    const q: AttemptPayload[] = JSON.parse(localStorage.getItem('mathspark_attempt_queue') ?? '[]');
    localStorage.setItem('mathspark_attempt_queue', JSON.stringify([...q, p]));
  }

  function flushAttemptQueue() {
    const q: AttemptPayload[] = JSON.parse(localStorage.getItem('mathspark_attempt_queue') ?? '[]');
    if (!q.length) return;
    Promise.all(
      q.map((p) =>
        fetch('/api/attempts', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify(p),
        }),
      ),
    )
      .then(() => localStorage.removeItem('mathspark_attempt_queue'))
      .catch(() => {});
  }

  function submitAttempt(payload: AttemptPayload) {
    if (navigator.onLine) {
      fetch('/api/attempts', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(payload),
      }).catch(() => queueAttempt(payload));
    } else {
      queueAttempt(payload);
    }
  }

  // ── Online / offline listeners ─────────────────────────────────────────────
  useEffect(() => {
    const goOffline = () => setIsOnline(false);
    const goOnline  = () => { setIsOnline(true); flushAttemptQueue(); };
    window.addEventListener('offline', goOffline);
    window.addEventListener('online',  goOnline);
    return () => {
      window.removeEventListener('offline', goOffline);
      window.removeEventListener('online',  goOnline);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Usage heartbeat: 60s interval, counts practice minutes ─────────────────
  useEffect(() => {
    if (!studentId) return;

    const interval = setInterval(async () => {
      // Only send heartbeat when actively in lesson (not on loading/limit/complete)
      if (!heartbeatPhaseRef.current) return;
      try {
        const res = await fetch('/api/usage/heartbeat', {
          method:  'POST',
          headers: { 'content-type': 'application/json' },
          body:    JSON.stringify({ studentId }),
        });
        if (res.ok) {
          const data = await res.json() as { allowed: boolean; used: number; limit: number };
          setUsageInfo({ used: data.used, limit: data.limit });
          if (!data.allowed) setPhase('usage_limit');
        }
      } catch { /* ignore transient network errors */ }
    }, 60_000);

    heartbeatRef.current = interval;
    return () => {
      clearInterval(interval);
      heartbeatRef.current = null;
      // Best-effort beacon on tab close/navigate so the last partial minute is counted
      if (heartbeatPhaseRef.current && navigator.sendBeacon) {
        navigator.sendBeacon('/api/usage/heartbeat', JSON.stringify({ studentId }));
      }
    };
  }, [studentId]); // run once per student session

  // ── Speed drill countdown ──────────────────────────────────────────────────
  useEffect(() => {
    if (!isSpeedMode || phase !== 'answering') {
      if (speedTimerRef.current) { clearInterval(speedTimerRef.current); speedTimerRef.current = null; }
      return;
    }
    setSpeedRemaining(SPEED_DRILL_MS);
    setSpeedTimedOut(false);
    const start = Date.now();
    speedTimerRef.current = setInterval(() => {
      const elapsed = Date.now() - start;
      const left    = Math.max(0, SPEED_DRILL_MS - elapsed);
      setSpeedRemaining(left);
      if (left <= 0) {
        clearInterval(speedTimerRef.current!);
        speedTimerRef.current = null;
        setSpeedTimedOut(true); // Handled via effect below
      }
    }, 200);
    return () => { if (speedTimerRef.current) { clearInterval(speedTimerRef.current); speedTimerRef.current = null; } };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSpeedMode, phase, qIndex, reviewIndex]);

  // Keep a stable ref to current question for timeout handler
  useEffect(() => { currentQuestionRef.current = currentQuestion ?? null; });

  // When speed timer expires, auto-submit a wrong answer
  useEffect(() => {
    if (!speedTimedOut || phase !== 'answering') return;
    setSpeedTimedOut(false);
    const q = currentQuestionRef.current;
    if (!q) return;
    // Pick an answer that is NOT the correct one
    const wrongKey = (['A', 'B', 'C', 'D'] as AnswerKey[]).find((k) => k !== q.correctAnswer) ?? 'A';
    handleAnswer(wrongKey, false);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [speedTimedOut]);

  // ── Save session data when lesson completes ────────────────────────────────
  useEffect(() => {
    if (phase !== 'complete' || sessionSavedRef.current) return;
    sessionSavedRef.current = true;
    const allResults = [...results, ...reviewResults];
    const correct    = allResults.filter((r) => r.wasCorrect).length;
    const accuracy   = allResults.length > 0
      ? Math.round((correct / allResults.length) * 100)
      : 0;
    saveSessionData(topicId, accuracy);
    track('lesson_completed', { topicId, accuracy });
  }, [phase, results, reviewResults, topicId]);

  // ── Helpers ────────────────────────────────────────────────────────────────
  const isReviewing      = phase === 'reviewing';
  const currentQuestion  = isReviewing ? reviewQueue[reviewIndex] : questions[qIndex];
  const currentSlotIndex = isReviewing ? reviewIndex : qIndex;

  // ── Boot ───────────────────────────────────────────────────────────────────
  // Fetch one adaptive question at a time. Questions are served by the adaptive
  // engine (/api/questions/next) which reads today's DB attempts to determine
  // difficulty, avoid repeats, and honour streak adjustments.
  useEffect(() => {
    const sid = localStorage.getItem('mathspark_student_id');
    if (!sid) { router.replace('/start'); return; }
    setStudentId(sid);
    studentIdRef.current = sid;
    setShareInfo({
      studentName:    localStorage.getItem('mathspark_student_name')    ?? '',
      parentEmail:    localStorage.getItem('mathspark_parent_email')    ?? '',
      parentWhatsApp: localStorage.getItem('mathspark_parent_whatsapp') ?? '',
    });

    Promise.all([
      // Gate check — fails open (allowed: true) so API errors never block students
      fetch(`/api/usage/check?studentId=${sid}`)
        .then((r) => r.ok ? r.json() : { allowed: true, used: 0, limit: 0, trial: null })
        .catch(() => ({ allowed: true, used: 0, limit: 0, trial: null })),
      fetch('/api/topics').then((r) => r.json()),
      // First question from the adaptive engine
      fetch(`/api/questions/next?topicId=${topicId}&studentId=${sid}`)
        .then((r) => { if (!r.ok) throw new Error('fetch failed'); return r.json() as Promise<Question>; }),
    ])
      .then(([usageData, topics, firstQ]: [{ allowed: boolean; used: number; limit: number; trial: TrialStatus | null }, Array<{ id: string; name: string }>, Question]) => {
        const t = topics.find((x) => x.id === topicId);
        setTopicName(t?.name ?? topicId);
        setUsageInfo({ used: usageData.used, limit: usageData.limit });

        // Store trial status
        const trialData = usageData.trial ?? null;
        trialStatusRef.current = trialData;
        setTrialStatus(trialData);

        // Trial gate: soft-blocked (exhausted + already used daily free question)
        if (trialData && !trialData.isSubscribed) {
          const softBlocked = trialData.lifetimeQuestions >= 10 && trialData.todayQuestions >= 1;
          if (softBlocked) {
            setPhase('trial_limit');
            return;
          }
        }

        if (!usageData.allowed) {
          setPhase('usage_limit');
          return;
        }
        setQuestions([firstQ]);
        setPhase('answering');
        // Immediately prefetch the second question
        prefetchNext();
      })
      .catch(() => router.replace('/chapters'));

    return () => {
      if (advanceTimer.current) clearTimeout(advanceTimer.current);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicId]);

  // ── Advance to next question ───────────────────────────────────────────────
  // Questions are fetched one at a time from the adaptive engine.
  // We pre-fetch the next question as soon as the user answers, so the advance
  // is instant in the common case; a brief loading screen covers the rare miss.
  const advance = useCallback((heartsNow: number) => {
    // BUG 2 FIX: Prevent double-advance from two "Got it!" buttons, timer+tap, etc.
    if (isAdvancingRef.current) return;
    isAdvancingRef.current = true;

    // Sample mode gate: max 5 questions
    if (isSampleMode && sessionQuestionsAnsweredRef.current >= SAMPLE_LIMIT) {
      setPhase('trial_limit');
      return;
    }

    // Trial gate: if student has used 10+ questions total, show trial_limit
    const ts = trialStatusRef.current;
    if (ts && !ts.isSubscribed) {
      const lifetimeNow = ts.lifetimeQuestions + sessionQuestionsAnsweredRef.current;
      if (lifetimeNow >= 10) {
        setPhase('trial_limit');
        return;
      }
    }

    if (advanceTimer.current) clearTimeout(advanceTimer.current);
    setSelected(null);
    setLastCorrect(false);
    setHintLevel(0);
    setHintUsed(false);
    setShowWalkthrough(false);
    setWalkthroughClosed(false);
    setSparkyToast(false);
    setBonusMode('off');
    setBonusQuestion(null);
    setBonusSelected(null);
    bonusOriginRef.current = null;

    if (isReviewing) {
      const nextRev = reviewIndex + 1;
      if (nextRev >= reviewQueueRef.current.length) {
        setShowConfetti(true);
        setPhase('complete');
      } else {
        setReviewIndex(nextRev);
        setPhase('reviewing');
      }
    } else {
      if (heartsNow <= 0) {
        setPhase('no_hearts');
        return;
      }
      const nextIdx = qIndex + 1;
      if (nextIdx >= LESSON_SIZE) {
        // Lesson complete
        if (reviewQueueRef.current.length > 0) {
          setPhase('review_intro');
        } else {
          setShowConfetti(true);
          setPhase('complete');
        }
      } else {
        // BUG 1 FIX: Validate the prefetched question is not a duplicate before using it.
        const prefetched = prefetchRef.current;
        const prefetchedIsValid = prefetched && !seenQuestionIdsRef.current.has(prefetched.id);
        prefetchRef.current   = null;
        isFetchingRef.current = false;

        if (prefetchedIsValid) {
          setQuestions((prev) => [...prev, prefetched!]);
          setQIndex(nextIdx);
          setPhase('answering');
        } else {
          // Fetch now (loading state covers the gap)
          setPhase('loading');
          fetchOneAdaptive().then((q) => {
            if (!q) {
              // Topic exhausted — end lesson with a celebration
              setShowConfetti(true);
              setPhase('complete');
              return;
            }
            setQuestions((prev) => [...prev, q]);
            setQIndex(nextIdx);
            setPhase('answering');
          }).catch(() => {
            // Fetch failed — show retry option instead of a dead screen
            setFetchRetry(true);
            setPhase('loading');
            isAdvancingRef.current = false;
          });
        }
      }
    }
  }, [isReviewing, reviewIndex, qIndex, fetchOneAdaptive]);

  // ── Handle answer ──────────────────────────────────────────────────────────
  function handleAnswer(key: AnswerKey, correct: boolean) {
    if (!currentQuestion) return;
    setSelected(key);
    setLastCorrect(correct);
    setPhase('result');

    const newStreak   = correct ? streak + 1 : 0;
    const earnedXp    = correct ? (isReviewing ? XP_REVIEW : XP_CORRECT) : 0;
    const newXp       = xp + earnedXp;
    const heartLost   = !correct && !hintUsed;
    const newHearts   = heartLost ? hearts - 1 : hearts;

    setStreak(newStreak);
    setXp(newXp);
    if (heartLost) setHearts(newHearts);

    // Feedback message
    const CORRECT_MSGS = ['Great job! ⭐', 'You got it! 🎯', 'Excellent! 🧠', 'Well done! 🌟', 'Awesome! 🎉'];
    let msg = correct
      ? CORRECT_MSGS[Math.floor(Math.random() * CORRECT_MSGS.length)]
      : "Not quite — let's think about this together! 💭";
    if (correct && newStreak === 3) msg = "You're on fire! 🔥";
    if (correct && newStreak === 5) msg = 'Unstoppable! ⚡';
    if (correct && newStreak === 10) msg = 'Math wizard! 🧙';
    setFeedback(msg);

    // Sounds
    if (correct) {
      if (newStreak === 3 || newStreak === 5) playStreak();
      else playCorrect();
      setShowXpFloat(true);
      setTimeout(() => setShowXpFloat(false), 1500);
    } else {
      playWrong();
      // Auto-show hint level 1 after a wrong answer
      setHintLevel(1);
    }

    // Queue wrong answer for review (main lesson only)
    if (!correct && !isReviewing) {
      const updated = [...reviewQueueRef.current, currentQuestion];
      reviewQueueRef.current = updated;
      setReviewQueue(updated);
    }

    // Track result
    const result: QuestionResult = {
      questionId:     currentQuestion.id,
      questionText:   currentQuestion.questionText,
      wasCorrect:     correct,
      selectedAnswer: key,
      correctAnswer:  currentQuestion.correctAnswer,
    };
    if (isReviewing) setReviewResults((prev) => [...prev, result]);
    else             setResults((prev) => [...prev, result]);

    // Compute misconception text for the chosen wrong answer
    const misconceptionKey  = `misconception${key}` as keyof Question;
    const misconceptionType = !correct ? ((currentQuestion[misconceptionKey] as string) || null) : null;

    // Record attempt (offline-aware)
    if (studentId) {
      submitAttempt({
        studentId,
        questionId: currentQuestion.id,
        topicId,
        selected: key,
        isCorrect: correct,
        hintUsed: hintLevel,
        misconceptionType,
      });
    }

    // Track session question count (for trial gate)
    sessionQuestionsAnsweredRef.current += 1;
    setSessionQuestionsAnswered(sessionQuestionsAnsweredRef.current);

    // Analytics
    track('question_answered', { topicId, correct });

    // Pre-fetch next adaptive question now (during result display window)
    // so advance() finds it ready and shows no loading gap.
    if (!isReviewing && qIndex + 1 < LESSON_SIZE) {
      prefetchNext();
    }

    // Auto-advance for correct answers
    if (correct) {
      advanceTimer.current = setTimeout(() => advance(newHearts), AUTO_ADVANCE_MS);
    }
  }

  function handleGotIt() {
    advance(hearts);
  }

  // ── Bonus "Repeat Similar" system ─────────────────────────────────────────

  function requestBonus(originQuestion: Question, wasOriginCorrect: boolean) {
    const originCount = bonusCountByOriginRef.current.get(originQuestion.id) ?? 0;
    if (originCount >= MAX_BONUS_PER_ORIGIN) return;
    if (bonusServedRef.current >= MAX_BONUS_PER_LESSON) return;

    if (advanceTimer.current) clearTimeout(advanceTimer.current);
    bonusOriginRef.current       = originQuestion;
    bonusOriginCorrectRef.current = wasOriginCorrect;
    setBonusMode('searching');
    track('similar_question_requested', { topicId, questionId: originQuestion.id });

    const excludeParam = Array.from(seenQuestionIdsRef.current).join(',');
    fetch(
      `/api/questions/similar` +
      `?questionId=${originQuestion.id}` +
      `&subTopic=${encodeURIComponent(originQuestion.subTopic)}` +
      `&topicId=${originQuestion.topicId}` +
      `&difficulty=${originQuestion.difficulty}` +
      `&wasCorrect=${wasOriginCorrect}` +
      `&exclude=${excludeParam}`,
    )
      .then((r) => (r.ok ? r.json() : null))
      .then((q: Question | null) => {
        if (!q) {
          setBonusMode('unavailable');
          track('similar_question_unavailable', {
            topicId, questionId: originQuestion.id, subTopic: originQuestion.subTopic,
          });
          return;
        }
        seenQuestionIdsRef.current.add(q.id);
        setBonusQuestion(q);
        setBonusSelected(null);
        setBonusCorrect(false);
        setBonusFeedback('');
        setBonusHintLevel(0);
        setBonusHintUsed(false);
        setBonusMode('answering');
        bonusServedRef.current += 1;
        bonusCountByOriginRef.current.set(
          originQuestion.id,
          (bonusCountByOriginRef.current.get(originQuestion.id) ?? 0) + 1,
        );
        track('similar_question_served', {
          topicId, originalId: originQuestion.id, bonusId: q.id,
        });
      })
      .catch(() => setBonusMode('unavailable'));
  }

  function handleBonusAnswer(key: AnswerKey) {
    if (!bonusQuestion) return;
    const correct   = key === bonusQuestion.correctAnswer;
    const newStreak = correct ? streak + 1 : 0;
    const earnedXp  = correct ? XP_CORRECT : 0;
    const heartLost = !correct && !bonusHintUsed;
    const newHearts = heartLost ? hearts - 1 : hearts;

    setBonusSelected(key);
    setBonusCorrect(correct);
    setBonusMode('result');
    setStreak(newStreak);
    setXp((x) => x + earnedXp);
    if (heartLost) setHearts(newHearts);

    const CORRECT_MSGS = ['Great job! ⭐', 'You got it! 🎯', 'Excellent! 🧠', 'Well done! 🌟', 'Awesome! 🎉'];
    let msg = correct
      ? CORRECT_MSGS[Math.floor(Math.random() * CORRECT_MSGS.length)]
      : "Not quite — let's think about this together! 💭";
    if (correct && newStreak === 3) msg = "You're on fire! 🔥";
    if (correct && newStreak === 5) msg = 'Unstoppable! ⚡';
    setBonusFeedback(msg);

    if (correct) playCorrect(); else { playWrong(); setBonusHintLevel(1); }

    // Track bonus questions toward trial count
    sessionQuestionsAnsweredRef.current += 1;
    setSessionQuestionsAnswered(sessionQuestionsAnsweredRef.current);

    if (studentId) {
      submitAttempt({
        studentId,
        questionId:      bonusQuestion.id,
        topicId,
        selected:        key,
        isCorrect:       correct,
        hintUsed:        bonusHintLevel,
        isBonusQuestion: true,
        parentQuestionId: bonusOriginRef.current?.id ?? null,
      });
    }
  }

  function handleBonusGotIt() {
    setBonusMode('off');
    setBonusQuestion(null);
    setBonusSelected(null);
    bonusOriginRef.current = null;
    advance(hearts);
  }

  function handleBonusOneMore() {
    if (!bonusOriginRef.current) return;
    const originId    = bonusOriginRef.current.id;
    const originCount = bonusCountByOriginRef.current.get(originId) ?? 0;
    if (originCount >= MAX_BONUS_PER_ORIGIN || bonusServedRef.current >= MAX_BONUS_PER_LESSON) {
      handleBonusGotIt();
      return;
    }
    requestBonus(bonusOriginRef.current, bonusOriginCorrectRef.current);
  }

  // ── Reset / retry ──────────────────────────────────────────────────────────
  function resetLesson() {
    setQIndex(0);
    setHearts(HEARTS_MAX);
    setXp(0);
    setStreak(0);
    setSelected(null);
    setLastCorrect(false);
    setHintLevel(0);
    setHintUsed(false);
    setResults([]);
    setReviewResults([]);
    reviewQueueRef.current = [];
    setReviewQueue([]);
    setReviewIndex(0);
    setShowConfetti(false);
    setShowWalkthrough(false);
    setWalkthroughClosed(false);
    setSparkyToast(false);
    setBonusMode('off');
    setBonusQuestion(null);
    setBonusSelected(null);
    bonusServedRef.current = 0;
    bonusCountByOriginRef.current.clear();
    bonusOriginRef.current = null;
    setSpeedTimedOut(false);
    setSpeedRemaining(SPEED_DRILL_MS);
    if (speedTimerRef.current) { clearInterval(speedTimerRef.current); speedTimerRef.current = null; }
    sessionSavedRef.current = false;
    prefetchRef.current      = null;
    isFetchingRef.current    = false;
    isAdvancingRef.current   = false;
    seenQuestionIdsRef.current = new Set();

    setPhase('loading');
    fetchOneAdaptive().then((q) => {
      if (!q) { router.replace('/chapters'); return; }
      setQuestions([q]);
      setPhase('answering');
      prefetchNext();
    });
  }

  // ── Full-screen phases ─────────────────────────────────────────────────────

  if (phase === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white gap-4 px-6">
        {fetchRetry ? (
          <>
            <Sparky mood="encouraging" size={100} />
            <p className="text-gray-600 font-bold text-center">Oops! Let&apos;s try again 🔄</p>
            <DuoButton variant="blue" onClick={() => {
              setFetchRetry(false);
              isAdvancingRef.current = false;
              fetchOneAdaptive().then((q) => {
                if (!q) { setShowConfetti(true); setPhase('complete'); return; }
                setQuestions((prev) => [...prev, q]);
                setQIndex((prev) => prev + 1);
                setPhase('answering');
              }).catch(() => setFetchRetry(true));
            }}>
              Retry →
            </DuoButton>
          </>
        ) : (
          <>
            <div className="animate-sparky-bounce">
              <Sparky mood="thinking" size={100} />
            </div>
            <p className="text-gray-400 font-semibold">Loading your lesson…</p>
          </>
        )}
      </div>
    );
  }

  if (phase === 'no_hearts') {
    return (
      <NoHeartsScreen
        results={results}
        onRetry={resetLesson}
        onHome={() => router.push('/chapters')}
      />
    );
  }

  if (phase === 'review_intro') {
    return (
      <ReviewIntroScreen
        count={reviewQueueRef.current.length}
        onStart={() => { setPhase('reviewing'); }}
      />
    );
  }

  if (phase === 'complete') {
    const hasReviewMistakes = reviewResults.some((r) => !r.wasCorrect);

    // Compute grade progression CTA
    const allR         = [...results, ...reviewResults];
    const correctCount = allR.filter((r) => r.wasCorrect).length;
    const pctScore     = allR.length > 0 ? Math.round((correctCount / allR.length) * 100) : 100;
    const topicGrade   = getTopicGrade(topicId);
    const studentGrade = parseInt(
      typeof window !== 'undefined' ? (localStorage.getItem('mathspark_student_grade') ?? '4') : '4',
      10,
    );
    const subTier = parseInt(
      typeof window !== 'undefined' ? (localStorage.getItem('mathspark_subscription_tier') ?? '0') : '0',
      10,
    );

    let gradeUpCta: GradeUpCta | undefined;
    if (pctScore >= 80 && topicGrade < 9) {
      const nextGrade = topicGrade + 1;
      const access    = isGradeAccessible(nextGrade, studentGrade, subTier);
      if (access.full) {
        gradeUpCta = { grade: nextGrade, type: 'full', onPress: () => router.push(`/practice/grade${nextGrade}`) };
      } else if (access.sample) {
        gradeUpCta = { grade: nextGrade, type: 'sample', onPress: () => router.push(`/practice/grade${nextGrade}?sample=true`) };
      } else {
        gradeUpCta = { grade: nextGrade, type: 'locked', onPress: () => router.push('/pricing') };
      }
    }

    return (
      <LessonCompleteScreen
        mainResults={results}
        reviewResults={reviewResults}
        totalXp={xp}
        hasReviewMistakes={hasReviewMistakes}
        gradeUpCta={gradeUpCta}
        onContinue={() => router.push('/chapters')}
        shareData={studentId ? {
          studentId,
          studentName:    shareInfo.studentName,
          topicName,
          topicEmoji:     TOPIC_EMOJI[topicId] ?? '📚',
          parentEmail:    shareInfo.parentEmail,
          parentWhatsApp: shareInfo.parentWhatsApp,
        } : undefined}
        onReviewMistakes={() => {
          // Restart lesson in review-only mode with wrong ones
          const wrongs = [...results, ...reviewResults].filter((r) => !r.wasCorrect);
          const wrongQs = wrongs
            .map((r) => questions.find((q) => q.id === r.questionId) ?? reviewQueue.find((q) => q.id === r.questionId))
            .filter(Boolean) as Question[];
          reviewQueueRef.current = wrongQs;
          setReviewQueue(wrongQs);
          setReviewResults([]);
          setReviewIndex(0);
          setShowConfetti(false);
          setPhase('review_intro');
        }}
      />
    );
  }

  if (phase === 'usage_limit') {
    const tierLimit = usageInfo.limit;
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-white pb-8">
        <div className="animate-sparky-bounce">
          <Sparky mood="encouraging" size={120} />
        </div>
        <div className="text-center space-y-3">
          <h2 className="text-2xl font-extrabold text-gray-800">
            Daily practice limit reached! ⏰
          </h2>
          <p className="text-gray-500 font-medium leading-relaxed">
            You&apos;ve practiced for{' '}
            <span className="font-extrabold text-gray-700">{formatMinutes(usageInfo.used)}</span>
            {!isUnlimitedPlan(tierLimit) && tierLimit > 0 && (
              <> out of <span className="font-extrabold text-gray-700">{formatMinutes(tierLimit)}</span></>
            )}{' '}
            today. Come back tomorrow — every day you practice, you get stronger! 💪
          </p>
          {!isUnlimitedPlan(tierLimit) && (
            <div className="bg-amber-50 border border-amber-200 rounded-2xl px-4 py-3 text-left">
              <p className="text-xs font-extrabold text-amber-700 uppercase tracking-wide mb-1">Want more practice time?</p>
              <p className="text-sm text-gray-600">Upgrade your plan to unlock longer daily sessions and unlimited practice.</p>
            </div>
          )}
        </div>
        <div className="w-full max-w-sm space-y-3">
          {!isUnlimitedPlan(tierLimit) && (
            <DuoButton variant="blue" fullWidth onClick={() => router.push('/parent/dashboard')}>
              Upgrade Plan 🚀
            </DuoButton>
          )}
          <DuoButton variant="white" fullWidth onClick={() => router.push('/chapters')}>
            Back to chapters
          </DuoButton>
        </div>
      </div>
    );
  }

  if (phase === 'trial_limit') {
    const wasExhaustedAtBoot = (trialStatus?.lifetimeQuestions ?? 0) >= 10;
    const totalUsed = (trialStatus?.lifetimeQuestions ?? 0) + sessionQuestionsAnswered;
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-white pb-8">
        <div className="animate-sparky-bounce">
          <Sparky mood="encouraging" size={120} />
        </div>
        <div className="text-center space-y-3">
          <h2 className="text-2xl font-extrabold text-gray-800">
            {wasExhaustedAtBoot ? 'Come back tomorrow! ⏰' : 'Amazing start! 🎉'}
          </h2>
          <p className="text-gray-500 font-medium leading-relaxed">
            {wasExhaustedAtBoot
              ? "You've used your free daily question. Subscribe to practice anytime!"
              : `You've answered ${totalUsed} questions — your free trial is complete! Subscribe to keep your streak going.`
            }
          </p>
          <div className="bg-amber-50 border border-amber-200 rounded-2xl px-4 py-3 text-left">
            <p className="text-xs font-extrabold text-amber-700 uppercase tracking-wide mb-2">Unlock with a subscription:</p>
            <ul className="space-y-1.5 text-sm text-gray-600">
              {['Unlimited daily practice', 'Hints + step-by-step solutions', 'Progress tracking & badges', 'Full IPM mock tests'].map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="text-[#58CC02]">✅</span> {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className="w-full max-w-sm space-y-3">
          <DuoButton variant="blue" fullWidth onClick={() => router.push('/pricing')}>
            Upgrade Now 🚀
          </DuoButton>
          <DuoButton variant="white" fullWidth onClick={() => router.push('/chapters')}>
            {wasExhaustedAtBoot ? 'Back to chapters' : 'Come back tomorrow for 1 free question'}
          </DuoButton>
        </div>
      </div>
    );
  }

  // ── Question screen (answering | result | reviewing) ──────────────────────

  if (!currentQuestion) return null;

  const accentCls = CARD_ACCENTS[currentSlotIndex % CARD_ACCENTS.length];
  const pct = isReviewing
    ? Math.round((reviewResults.length / reviewQueue.length) * 100)
    : Math.round((qIndex / LESSON_SIZE) * 100);

  // Bonus helpers
  const bonusOptKey      = bonusSelected ? `misconception${bonusSelected}` as keyof Question : null;
  const bonusMisconText  = bonusOptKey && bonusQuestion ? bonusQuestion[bonusOptKey] as string : '';
  const bonusCorrectText = bonusQuestion ? bonusQuestion[`option${['A','B','C','D'].indexOf(bonusQuestion.correctAnswer) + 1}` as keyof Question] as string : '';
  const canOneMore = bonusOriginRef.current
    ? (bonusCountByOriginRef.current.get(bonusOriginRef.current.id) ?? 0) < MAX_BONUS_PER_ORIGIN &&
      bonusServedRef.current < MAX_BONUS_PER_LESSON
    : false;

  return (
    <div className="flex flex-col bg-white min-h-screen">
      {/* Confetti */}
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

      {/* XP Float */}
      {showXpFloat && <XpFloat amount={isReviewing ? XP_REVIEW : XP_CORRECT} />}

      {/* ── Dark header ── */}
      <div className="bg-[#131F24] px-4 py-3 flex items-center gap-3 sticky top-0 z-30 flex-shrink-0">
        <button
          onClick={() => router.push('/chapters')}
          className="text-white/70 hover:text-white font-bold text-xl min-h-[44px] min-w-[44px] flex items-center justify-center flex-shrink-0"
          aria-label="Back"
        >
          ←
        </button>
        <div className="flex-1 min-w-0">
          <p className="text-white font-extrabold text-sm truncate">{topicName}</p>
        </div>
        <HeartsBar hearts={hearts} />
        <button
          onClick={toggleMute}
          className="text-white/70 hover:text-white text-lg min-h-[44px] min-w-[44px] flex items-center justify-center ml-1"
          aria-label={muted ? 'Unmute' : 'Mute'}
        >
          {muted ? '🔇' : '🔊'}
        </button>
      </div>

      {/* ── Offline banner ── */}
      {!isOnline && (
        <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 text-xs font-bold text-amber-700 text-center">
          📶 You&apos;re offline — practising with cached questions!
        </div>
      )}

      {/* ── Journey circles / Review badge ── */}
      {isReviewing ? (
        <div className="bg-[#EEF6FF] px-4 py-2 flex items-center gap-2 border-b border-blue-100">
          <span className="text-[#1CB0F6] text-sm font-extrabold">📚 Review mode</span>
          <span className="text-gray-400 text-xs font-semibold">{reviewIndex + 1} / {reviewQueue.length}</span>
        </div>
      ) : (
        <LessonJourney total={LESSON_SIZE} currentIdx={qIndex} results={results} />
      )}

      {/* Progress bar */}
      <div className="h-1.5 bg-gray-100">
        <div
          className="h-1.5 bg-gradient-to-r from-[#58CC02] to-[#89E219] transition-all duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>

      {/* Speed drill timer bar */}
      {isSpeedMode && phase === 'answering' && (
        <div className="h-2 bg-gray-100 relative">
          <div
            className={`h-full transition-all duration-200 ${
              speedRemaining > 60_000 ? 'bg-[#58CC02]' :
              speedRemaining > 30_000 ? 'bg-[#FF9600]' : 'bg-[#FF4B4B]'
            }`}
            style={{ width: `${(speedRemaining / SPEED_DRILL_MS) * 100}%` }}
          />
        </div>
      )}

      {/* ── Trial banner ── */}
      {trialStatus && !trialStatus.isSubscribed && (() => {
        const lifetimeNow = trialStatus.lifetimeQuestions + sessionQuestionsAnswered;
        const questionsLeft = Math.max(0, 10 - lifetimeNow);
        if (trialStatus.lifetimeQuestions >= 10) {
          return (
            <div className="bg-blue-50 border-b border-blue-200 px-4 py-2 text-xs font-bold text-blue-700 text-center flex items-center justify-center gap-2">
              🎁 Your free daily question — <button onClick={() => router.push('/pricing')} className="underline">Upgrade for unlimited</button>
            </div>
          );
        }
        if (questionsLeft <= 3 && questionsLeft > 0) {
          return (
            <div className="bg-orange-50 border-b border-orange-200 px-4 py-2 text-xs font-bold text-orange-700 text-center flex items-center justify-center gap-2">
              ⚡ {questionsLeft} free question{questionsLeft > 1 ? 's' : ''} left — <button onClick={() => router.push('/pricing')} className="underline">Upgrade to continue</button>
            </div>
          );
        }
        return null;
      })()}

      {/* ── Question area (scrollable, padded for bottom panel) ── */}
      <div
        className="flex-1 overflow-y-auto px-4 py-4 space-y-4"
        style={{ paddingBottom: phase === 'result' ? '72vh' : '80px' }}
      >
        {/* Question label with color accent */}
        <div className={`inline-flex items-center gap-2 text-xs font-extrabold px-3 py-1.5 rounded-full border ${accentCls}`}>
          {isReviewing
            ? `🔁 Review question ${reviewIndex + 1} of ${reviewQueue.length}`
            : isSpeedMode
            ? `⚡ Speed Drill — Q${qIndex + 1} of ${LESSON_SIZE}`
            : `Question ${qIndex + 1} of ${LESSON_SIZE}`}
          {streak >= 3 && !isReviewing && (
            <span className="text-orange-500 font-extrabold">🔥 {streak}</span>
          )}
        </div>

        <QuestionCard
          question={currentQuestion}
          answered={phase === 'result'}
          selected={selected}
          onAnswer={handleAnswer}
        />
      </div>

      {/* ── Animated Walkthrough overlay ── */}
      {showWalkthrough && (
        <AnimatedWalkthrough
          question={currentQuestion}
          studentAnswer={selected}
          onClose={() => {
            setShowWalkthrough(false);
            setWalkthroughClosed(true);
          }}
          onSimilar={() => requestBonus(currentQuestion, lastCorrect)}
        />
      )}

      {/* ── Sparky chat bubble (floating RHS, visible during result phase) ── */}
      {phase === 'result' && (
        <div
          className="fixed right-3 z-[65] animate-slide-up"
          style={{ bottom: 'calc(72vh + 12px)', animationDelay: '1.2s', animationFillMode: 'backwards' }}
        >
          <button
            onClick={() => router.push('/chat')}
            className="flex flex-col items-end gap-1"
            aria-label="Ask Sparky"
          >
            <div className="bg-white rounded-2xl shadow-xl px-3 py-2 border border-gray-100 max-w-[130px]">
              <p className="text-xs font-bold text-gray-700 text-center leading-snug">
                {lastCorrect ? 'Keep it up! 🎉' : 'Need help? 💬'}
              </p>
            </div>
            <div className={`rounded-full p-1.5 shadow-lg ${lastCorrect ? 'bg-[#58CC02]' : 'bg-[#1CB0F6]'}`}>
              <Sparky mood={lastCorrect ? 'celebrating' : 'encouraging'} size={32} />
            </div>
          </button>
        </div>
      )}

      {/* ── Sliding bottom panel ── */}
      {phase === 'result' && (
        <div
          className={`fixed bottom-0 left-0 right-0 max-w-lg mx-auto z-[60] animate-slide-up overflow-y-auto ${
            lastCorrect
              ? 'bg-[#58CC02]'
              : 'bg-[#FFF0F0] border-t-2 border-[#FF4B4B]'
          }`}
          style={{ maxHeight: '72vh' }}
        >
          {lastCorrect ? (
            <CorrectPanel
              feedback={feedback}
              streak={streak}
              onContinue={() => {
                if (advanceTimer.current) clearTimeout(advanceTimer.current);
                advance(hearts);
              }}
              onWatchSolution={() => {
                if (advanceTimer.current) clearTimeout(advanceTimer.current);
                setShowWalkthrough(true);
              }}
              onTrySimilar={() => {
                if (advanceTimer.current) clearTimeout(advanceTimer.current);
                requestBonus(currentQuestion, true);
              }}
              canTrySimilar={bonusMode === 'off'}
            />
          ) : (
            <WrongPanel
              question={currentQuestion}
              selected={selected}
              onGotIt={handleGotIt}
              hintLevel={hintLevel}
              onHintLevelUp={(n) => { setHintLevel(n); setHintUsed(true); }}
              onWatchSolution={() => setShowWalkthrough(true)}
              onTrySimilar={() => requestBonus(currentQuestion, false)}
              canTrySimilar={bonusMode === 'off'}
            />
          )}
        </div>
      )}

      {/* ── Bonus "Repeat Similar" overlay ─────────────────────────────────── */}
      {bonusMode !== 'off' && (
        <div
          className="fixed inset-0 bg-white z-[80] flex flex-col max-w-lg mx-auto animate-slide-from-right"
        >
          {/* Header */}
          <div className="bg-[#131F24] px-4 py-3 flex items-center gap-3 flex-shrink-0">
            <button
              onClick={handleBonusGotIt}
              className="text-white/70 hover:text-white font-bold text-sm min-h-[44px] min-w-[44px] flex items-center gap-1"
            >
              ← Back
            </button>
            <div className="flex-1 min-w-0">
              <p className="text-white font-extrabold text-sm truncate">{topicName}</p>
            </div>
            <HeartsBar hearts={hearts} />
          </div>

          {/* Amber bonus banner */}
          <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 flex items-center gap-2 flex-shrink-0">
            <span>⭐</span>
            <p className="text-amber-700 font-extrabold text-sm">Bonus Question — Same concept, different numbers!</p>
          </div>

          {/* Searching */}
          {bonusMode === 'searching' && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4 px-6">
              <div className="animate-sparky-bounce">
                <Sparky mood="thinking" size={80} />
              </div>
              <p className="text-gray-500 font-semibold text-center">Finding a similar question…</p>
            </div>
          )}

          {/* Unavailable */}
          {bonusMode === 'unavailable' && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4 px-6">
              <Sparky mood="encouraging" size={80} />
              <p className="text-gray-700 font-bold text-center text-lg leading-snug">
                You&apos;ve practiced all similar questions!<br />Let&apos;s keep going 💪
              </p>
              <DuoButton variant="green" onClick={handleBonusGotIt}>
                Next Question →
              </DuoButton>
            </div>
          )}

          {/* Bonus question screen */}
          {(bonusMode === 'answering' || bonusMode === 'result') && bonusQuestion && (
            <>
              <div
                className="flex-1 overflow-y-auto px-4 py-4 space-y-4"
                style={{ paddingBottom: bonusMode === 'result' ? '200px' : '80px' }}
              >
                {/* Bonus label */}
                <div className="inline-flex items-center gap-2 text-xs font-extrabold px-3 py-1.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                  ⭐ Bonus Question
                </div>

                {/* Question card — amber border */}
                <div className="relative">
                  <div className="absolute -top-2 -left-1 z-10 bg-amber-400 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full shadow-sm">
                    ⭐ Bonus
                  </div>
                  <div className="border-2 border-amber-300 rounded-2xl overflow-hidden">
                    <QuestionCard
                      question={bonusQuestion}
                      answered={bonusMode === 'result'}
                      selected={bonusSelected}
                      onAnswer={(key) => handleBonusAnswer(key)}
                    />
                  </div>
                </div>

                {/* Wrong bonus: misconception + hints + solution */}
                {bonusMode === 'result' && !bonusCorrect && (
                  <>
                    {bonusMisconText && (
                      <div className="bg-blue-50 border border-blue-200 rounded-2xl px-4 py-3">
                        <p className="text-[11px] font-extrabold text-blue-700 uppercase tracking-wide mb-1">💡 Common mistake</p>
                        <p className="text-sm text-gray-700 font-medium leading-snug">{bonusMisconText}</p>
                      </div>
                    )}
                    <HintSystem
                      hint1={bonusQuestion.hint1}
                      hint2={bonusQuestion.hint2}
                      hint3={bonusQuestion.hint3}
                      level={bonusHintLevel}
                      onLevelUp={(n) => { setBonusHintLevel(n); setBonusHintUsed(true); }}
                    />
                    <StepByStep steps={bonusQuestion.stepByStep} />
                  </>
                )}
              </div>

              {/* Bonus bottom panel */}
              {bonusMode === 'result' && (
                <div
                  className={`fixed bottom-0 left-0 right-0 max-w-lg mx-auto z-[90] animate-slide-up ${
                    bonusCorrect
                      ? 'bg-[#58CC02]'
                      : 'bg-[#FFF0F0] border-t-2 border-[#FF4B4B]'
                  }`}
                  style={{ minHeight: '160px' }}
                >
                  <div className="px-4 pt-4 pb-6 space-y-3">
                    <p className={`font-extrabold text-base ${bonusCorrect ? 'text-white' : 'text-[#FF4B4B]'}`}>
                      {bonusFeedback}
                    </p>
                    {bonusCorrect && (
                      <p className="text-white/80 text-xs font-semibold">
                        ✅ {bonusQuestion.correctAnswer}: {bonusCorrectText}
                      </p>
                    )}
                    {!bonusCorrect && canOneMore && (
                      <button
                        onClick={handleBonusOneMore}
                        className="w-full min-h-[48px] bg-white/30 border border-white/40 text-[#FF4B4B] font-extrabold text-sm rounded-2xl flex items-center justify-center gap-2"
                      >
                        🔄 One More?
                      </button>
                    )}
                    <button
                      onClick={handleBonusGotIt}
                      className={`w-full min-h-[48px] rounded-2xl font-extrabold text-sm flex items-center justify-center gap-2 ${
                        bonusCorrect
                          ? 'bg-white/20 text-white border border-white/40'
                          : 'bg-white text-gray-700'
                      }`}
                    >
                      Back to Lesson →
                    </button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
