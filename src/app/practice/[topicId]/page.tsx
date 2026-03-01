'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { track } from '@vercel/analytics';
import QuestionCard from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import KatexRenderer from '@/components/KatexRenderer';
import StepByStep from '@/components/StepByStep';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import { useSounds } from '@/hooks/useSounds';
import type { Question, AnswerKey } from '@/types';
import { saveSessionData } from '@/lib/nudges';

// ── Constants ─────────────────────────────────────────────────────────────────

const LESSON_SIZE    = 10;
const HEARTS_MAX     = 5;
const XP_CORRECT     = 20;
const XP_REVIEW      = 10;
const AUTO_ADVANCE_MS = 2000;
const SPEED_DRILL_MS  = 90_000; // 90 seconds per question

// ── Types ─────────────────────────────────────────────────────────────────────

type Phase =
  | 'loading'
  | 'answering'
  | 'result'
  | 'no_hearts'
  | 'review_intro'
  | 'reviewing'
  | 'complete';

interface QuestionResult {
  questionId:    string;
  questionText:  string;
  wasCorrect:    boolean;
  selectedAnswer: AnswerKey;
  correctAnswer:  AnswerKey;
}

// ── Card accent colors (visual variety per question slot) ─────────────────────

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

function LessonCompleteScreen({
  mainResults,
  reviewResults,
  totalXp,
  hasReviewMistakes,
  onContinue,
  onReviewMistakes,
}: {
  mainResults:       QuestionResult[];
  reviewResults:     QuestionResult[];
  totalXp:           number;
  hasReviewMistakes: boolean;
  onContinue:        () => void;
  onReviewMistakes:  () => void;
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

  return (
    <div className="flex flex-col items-center px-6 py-8 gap-6 bg-white min-h-screen pb-24">
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
        <DuoButton variant="green" fullWidth onClick={onContinue}>
          Continue to chapters 🎯
        </DuoButton>
        {hasReviewMistakes && (
          <DuoButton variant="blue" fullWidth onClick={onReviewMistakes}>
            Review mistakes 📚
          </DuoButton>
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
}: {
  feedback:   string;
  streak:     number;
  onContinue: () => void;
}) {
  return (
    <div className="px-4 py-4 flex items-start gap-3">
      <div className="animate-sparky-dance flex-shrink-0">
        <Sparky mood="celebrating" size={72} />
      </div>
      <div className="flex-1 space-y-2">
        {streak >= 3 && (
          <div className="text-xs font-extrabold text-white/80 uppercase tracking-wide">
            🔥 {streak} in a row!
          </div>
        )}
        <p className="text-lg font-extrabold text-white leading-tight">{feedback}</p>
        <DuoButton variant="white" fullWidth onClick={onContinue}>
          CONTINUE →
        </DuoButton>
      </div>
    </div>
  );
}

function WrongPanel({
  correctAnswer,
  correctText,
  onGotIt,
}: {
  correctAnswer: AnswerKey;
  correctText:   string;
  onGotIt:       () => void;
}) {
  const textHasLatex = correctText.includes('\\');
  return (
    <div className="px-4 py-4 flex items-start gap-3">
      <div className="flex-shrink-0">
        <Sparky mood="encouraging" size={72} />
      </div>
      <div className="flex-1 space-y-2">
        <p className="text-sm font-extrabold text-[#FF4B4B] uppercase tracking-wide">
          No worries! Here&#39;s how it works…
        </p>

        {/* Correct answer box */}
        <div className="bg-white rounded-xl px-3 py-2 border border-red-100">
          <p className="text-xs text-gray-500 font-semibold">Correct answer ({correctAnswer})</p>
          {textHasLatex ? (
            <div className="mt-1">
              <KatexRenderer latex={correctText} displayMode={false} />
            </div>
          ) : (
            <p className="text-sm text-gray-800 font-bold leading-snug">{correctText}</p>
          )}
        </div>

        <DuoButton variant="red" fullWidth onClick={onGotIt}>
          Got it!
        </DuoButton>
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
  const { playCorrect, playWrong, playStreak, muted, toggleMute } = useSounds();

  // ── Core state ─────────────────────────────────────────────────────────────
  const [studentId,   setStudentId]   = useState<string | null>(null);
  const [topicName,   setTopicName]   = useState('');
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
  const [similarQ, setSimilarQ] = useState<Question | null>(null);

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

  // ── Offline attempt queue helpers ──────────────────────────────────────────
  interface AttemptPayload {
    studentId: string; questionId: string; topicId: string;
    selected: string; isCorrect: boolean; hintUsed: number;
    misconceptionType?: string | null;
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

    Promise.all([
      fetch('/api/topics').then((r) => r.json()),
      // First question from the adaptive engine
      fetch(`/api/questions/next?topicId=${topicId}&studentId=${sid}`)
        .then((r) => { if (!r.ok) throw new Error('fetch failed'); return r.json() as Promise<Question>; }),
    ])
      .then(([topics, firstQ]: [Array<{ id: string; name: string }>, Question]) => {
        const t = topics.find((x) => x.id === topicId);
        setTopicName(t?.name ?? topicId);
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

    if (advanceTimer.current) clearTimeout(advanceTimer.current);
    setSelected(null);
    setLastCorrect(false);
    setHintLevel(0);
    setHintUsed(false);

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

    // On wrong answer: fetch a similar question in the background
    if (!correct) {
      setSimilarQ(null);
      fetch(
        `/api/questions/similar?subTopic=${encodeURIComponent(currentQuestion.subTopic)}&questionId=${currentQuestion.id}`,
      )
        .then((r) => (r.ok ? r.json() : null))
        .then((q: Question | null) => { if (q) setSimilarQ(q); })
        .catch(() => {});
    }

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
    setSimilarQ(null);
    advance(hearts);
  }

  function handlePracticeSimilar() {
    if (!similarQ) return;
    const q = similarQ;
    setSimilarQ(null);
    if (advanceTimer.current) clearTimeout(advanceTimer.current);
    // Inject the similar question as the next question via the prefetch slot
    prefetchRef.current   = q;
    isFetchingRef.current = false;
    advance(hearts);
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
    setSimilarQ(null);
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
    return (
      <LessonCompleteScreen
        mainResults={results}
        reviewResults={reviewResults}
        totalXp={xp}
        hasReviewMistakes={hasReviewMistakes}
        onContinue={() => router.push('/chapters')}
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

  // ── Question screen (answering | result | reviewing) ──────────────────────

  if (!currentQuestion) return null;

  const accentCls = CARD_ACCENTS[currentSlotIndex % CARD_ACCENTS.length];
  const pct = isReviewing
    ? Math.round((reviewResults.length / reviewQueue.length) * 100)
    : Math.round((qIndex / LESSON_SIZE) * 100);

  const optionKey = `misconception${selected}` as keyof Question;
  const misconceptionText = selected && currentQuestion[optionKey] as string || '';
  const correctOptionText = currentQuestion[`option${['A','B','C','D'].indexOf(currentQuestion.correctAnswer) + 1}` as keyof Question] as string;

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

      {/* ── Question area (scrollable, padded for bottom panel) ── */}
      <div
        className="flex-1 overflow-y-auto px-4 py-4 space-y-4"
        style={{ paddingBottom: phase === 'result' ? '220px' : '80px' }}
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

        {/* Wrong-answer smart feedback */}
        {phase === 'result' && !lastCorrect && (
          <>
            {/* Blue misconception box — shown before hints */}
            {misconceptionText && (
              <div className="bg-blue-50 border border-blue-200 rounded-2xl px-4 py-3">
                <p className="text-[11px] font-extrabold text-blue-700 uppercase tracking-wide mb-1">
                  💡 Common mistake
                </p>
                <p className="text-sm text-gray-700 font-medium leading-snug">
                  {misconceptionText}
                </p>
              </div>
            )}
            <HintSystem
              hint1={currentQuestion.hint1}
              hint2={currentQuestion.hint2}
              hint3={currentQuestion.hint3}
              level={hintLevel}
              onLevelUp={(n) => { setHintLevel(n); setHintUsed(true); }}
            />
            <StepByStep
              steps={currentQuestion.stepByStep}
              onGotIt={() => {
                if (advanceTimer.current) clearTimeout(advanceTimer.current);
                advance(hearts);
                setSimilarQ(null);
              }}
              onPracticeSimilar={similarQ ? handlePracticeSimilar : undefined}
            />
          </>
        )}
      </div>

      {/* ── Sliding bottom panel ── */}
      {phase === 'result' && (
        <div
          className={`fixed bottom-0 left-0 right-0 max-w-lg mx-auto z-[60] animate-slide-up ${
            lastCorrect
              ? 'bg-[#58CC02]'
              : 'bg-[#FFF0F0] border-t-2 border-[#FF4B4B]'
          }`}
          style={{ minHeight: '180px' }}
        >
          {lastCorrect ? (
            <CorrectPanel
              feedback={feedback}
              streak={streak}
              onContinue={() => {
                if (advanceTimer.current) clearTimeout(advanceTimer.current);
                advance(hearts);
              }}
            />
          ) : (
            <WrongPanel
              correctAnswer={currentQuestion.correctAnswer}
              correctText={correctOptionText}
              onGotIt={handleGotIt}
            />
          )}
        </div>
      )}
    </div>
  );
}
