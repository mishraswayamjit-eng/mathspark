'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { track } from '@vercel/analytics';
import QuestionCard from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import AnimatedWalkthrough from '@/components/AnimatedWalkthrough';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import { useSounds } from '@/hooks/useSounds';
import { useConceptSuggestions } from '@/hooks/useConceptSuggestions';
import type { Question, AnswerKey } from '@/types';
import { saveSessionData } from '@/lib/nudges';
import { formatMinutes, isUnlimitedPlan } from '@/lib/usageLimits';
import { isGradeAccessible, getTopicGrade } from '@/lib/gradeAccess';
import { MONETIZATION_ENABLED, UNLIMITED_TIER } from '@/lib/monetization';
import {
  LESSON_SIZE, HEARTS_MAX, XP_CORRECT, XP_REVIEW, AUTO_ADVANCE_MS,
  SPEED_DRILL_MS, MAX_BONUS_PER_LESSON, MAX_BONUS_PER_ORIGIN,
  TOPIC_EMOJI, CARD_ACCENTS,
  type Phase, type TrialStatus, type BonusMode, type QuestionResult, type GradeUpCta,
} from '@/components/practice';
import { HeartsBar, LessonProgressBar, XpFloat } from '@/components/practice';
import { ReviewIntroScreen, NoHeartsScreen, LessonCompleteScreen, LessonIntro, CelebrationCascade, StreakCommitment } from '@/components/practice';
import { CorrectPanel, WrongPanel } from '@/components/practice';
import { logError } from '@/lib/logger';
import { publishScreenContext, clearScreenContext, requestOpenSparky } from '@/lib/sparkyContext';
import FigureView from '@/components/figures/FigureView';
import WorkPane from '@/components/figures/WorkPane';
import StepPlayer, { hasSolutionSteps } from '@/components/figures/StepPlayer';
import TeachPlayer from '@/components/teach/TeachPlayer';
import { useTeachAvailable } from '@/components/teach/player/useTeachAvailable';
import { useTutorVoice } from '@/hooks/useTutorVoice';
import type { TutorEvent } from '@/lib/tutor/reactions';
import TopicLadder from '@/components/practice/TopicLadder';
import VoiceSettingsButton from '@/components/voice/VoiceSettingsButton';
import type { LadderInfo } from '@/lib/practice/ladderTypes';
import { ladderAfterAnswer } from '@/lib/practice/ladder';

/** How long an open question can sit untouched before the tutor says something, once. */
const IDLE_SECONDS = 40;

/**
 * A question as `/api/questions/next` sends it: when the child is practising
 * one topic, it also carries where they are on that topic's ladder.
 */
type PracticeQuestion = Question & { ladder?: LadderInfo };

/** True when ladder `a` shows less progress than ladder `b`. */
function ladderBehind(a: LadderInfo, b: LadderInfo): boolean {
  if (a.complete) return false;
  if (b.complete) return true;
  return a.current < b.current || (a.current === b.current && a.got < b.got);
}

/** The ladder carried by a fetched question, when it has one in the expected shape. */
function ladderOf(q: PracticeQuestion | null): LadderInfo | null {
  return q && q.ladder && Array.isArray(q.ladder.steps) ? q.ladder : null;
}

/**
 * Wide screens: the question (left, a little wider) and the working pane
 * (right) share one centred workspace, the same width as the header content.
 */
const WORKSPACE_COLS = 'lg:grid lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)] lg:items-start lg:gap-5';

/** The words of one option (A to D) of a question. */
function optionText(q: Question, key: AnswerKey): string {
  const idx = 'ABCD'.indexOf(key);
  const text = idx >= 0 ? q[`option${idx + 1}` as keyof Question] : '';
  return typeof text === 'string' ? text : '';
}

// ── Main component ────────────────────────────────────────────────────────────

export default function PracticePage() {
  const params        = useParams();
  const router        = useRouter();
  const searchParams  = useSearchParams();
  const topicId       = params.topicId as string;
  const isSpeedMode   = searchParams.get('mode') === 'speed';
  const isSampleMode  = MONETIZATION_ENABLED && searchParams.get('sample') === 'true';
  const subTopicParam = searchParams.get('subTopic') ?? '';
  const conceptId     = searchParams.get('from') === 'concept' ? searchParams.get('conceptId') : null;
  const SAMPLE_LIMIT  = 5;
  const { playCorrect, playWrong, playStreak, muted, toggleMute } = useSounds();

  // ── Core state ─────────────────────────────────────────────────────────────
  const [studentId,   setStudentId]   = useState<string | null>(null);
  const [topicName,   setTopicName]   = useState('');
  const [shareInfo,   setShareInfo]   = useState({ studentName: '', parentEmail: '', parentWhatsApp: '' });
  const [questions,   setQuestions]   = useState<Question[]>([]);
  const [phase,       setPhase]       = useState<Phase>('loading');
  // Where the child is on this topic's ladder: the latest one the server sent
  // with a question. Null when practice is not on a single topic.
  const [ladder,      setLadder]      = useState<LadderInfo | null>(null);
  // The ladder as moved on by the answer just given, until the server's next
  // one arrives. The next question is fetched while that answer is still being
  // saved, so the ladder that comes with it can be one answer behind.
  const answeredLadderRef = useRef<LadderInfo | null>(null);

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
  const [showXpFloat,      setShowXpFloat]      = useState(false);
  const [showConfetti,     setShowConfetti]     = useState(false);
  const [showMiniConfetti,     setShowMiniConfetti]     = useState(false);
  const [showStreakCommitment, setShowStreakCommitment] = useState(false);

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
  // Confidence check: the child's answer to "Could you solve these?" on the intro.
  // Asked once per topic per day; nudges the difficulty of the first few questions.
  const confidenceRef = useRef<'low' | 'medium' | 'high' | null>(null);
  // What the child built/tapped/dragged on an interactive question (JSON string),
  // captured just before handleAnswer runs so the server can grade the real answer.
  const interactiveAnswerRef = useRef<string | null>(null);
  // Set when the confidence answer arrives while the next question is still being
  // fetched: that fetch was made without the answer, so its result is thrown away.
  const discardPrefetchRef = useRef(false);
  const [askConfidence, setAskConfidence] = useState(false);
  // Feature 1: count wrong attempts per question → trigger stuck-coach on 2nd miss.
  const wrongCountByQuestionRef = useRef<Map<string, number>>(new Map());
  const [showCoach, setShowCoach] = useState(false);
  // Fetch with 5s timeout + retry tracking
  const [fetchRetry, setFetchRetry] = useState(false);

  // Animated walkthrough
  const [showWalkthrough,    setShowWalkthrough]    = useState(false);
  const [walkthroughClosed,  setWalkthroughClosed]  = useState(false);
  const [sparkyToast,        setSparkyToast]        = useState(false);

  // Step player sheet (phones and tablets; wide screens show the steps in the side pane)
  const [showSteps, setShowSteps] = useState(false);
  const resultSheetRef = useRef<HTMLDivElement | null>(null);
  // Working space sheet (phones and tablets): hints and the pencil pad before answering
  const [showWork, setShowWork] = useState(false);
  // "Explain it to me" sheet (phones and tablets, after answering; wide screens play the lesson in the side pane)
  const [showTeach, setShowTeach] = useState(false);
  const showTeachRef = useRef(false);
  showTeachRef.current = showTeach;
  // How many working panes have a lesson playing (0 or 1 in practice).
  const [paneLessons, setPaneLessons] = useState(0);
  const paneLessonsRef = useRef(0);
  const onPaneLesson = useCallback((open: boolean) => {
    paneLessonsRef.current = Math.max(0, paneLessonsRef.current + (open ? 1 : -1));
    setPaneLessons(paneLessonsRef.current);
  }, []);
  // The `teach` link ("let me explain a question you missed"): the session opens
  // on that question with its lesson already playing.
  //   'lesson'  the lesson is on screen, over the question
  //   'after'   the lesson is closed: a similar question is offered
  //   'off'     an ordinary session (always, once the session moves on)
  const [linked, setLinked] = useState<'off' | 'lesson' | 'after'>('off');
  const linkedRef = useRef<'off' | 'lesson' | 'after'>('off');
  linkedRef.current = linked;
  // A lesson is on screen somewhere: the tutor keeps quiet meanwhile.
  const lessonOpen = paneLessons > 0 || showTeach || linked === 'lesson';

  // ── The tutor's reactions ───────────────────────────────────────────────────
  // One short line when a question appears, on a right answer, a miss, a hint,
  // a long pause and the end of the session. Deterministic lines only: whether
  // an answer is right is decided elsewhere and passed in.
  const tutor = useTutorVoice();
  const tutorRef = useRef(tutor);
  tutorRef.current = tutor;
  const [tutorCaption, setTutorCaption] = useState('');
  const tutorTurnRef      = useRef(0);
  const tutorNameRef      = useRef('');
  const tutorTopicRef     = useRef('');
  tutorNameRef.current  = shareInfo.studentName;
  // The topic's name, not its id (the name falls back to the id when it is not found).
  tutorTopicRef.current = topicName !== topicId ? topicName : '';
  const tutorFirstRef     = useRef(true);
  const questionShownAtRef = useRef(0);
  // Time the page was hidden (another tab, a locked screen) while this question
  // was open, so it is not counted as time spent on the question.
  const hiddenMsRef       = useRef(0);
  const hiddenSinceRef    = useRef(0);
  const missesInARowRef   = useRef(0);
  const idleSaidForRef    = useRef<string | null>(null);
  const sessionEndSaidRef = useRef(false);
  const tutorReact = useCallback((event: TutorEvent) => {
    // Never over a lesson. (A new question always closes the lesson sheet.)
    if (paneLessonsRef.current > 0) return;
    // The session opened straight on a lesson: it is the one talking.
    if (linkedRef.current === 'lesson') return;
    if (showTeachRef.current && event.kind !== 'question') return;
    tutorTurnRef.current += 1;
    const line = tutorRef.current.react(event, {
      name: tutorNameRef.current || undefined,
      topicName: tutorTopicRef.current || undefined,
      turn: tutorTurnRef.current,
    });
    // A new question clears the last line even when the tutor has nothing to say.
    if (line || event.kind === 'question') setTutorCaption(line);
  }, []);
  // True from the start of the review round until the lesson is restarted. The
  // phase alone cannot say this: answering a review question moves it to 'result'.
  const [inReview, setInReview] = useState(false);

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

  // Concept journey "What's Next" suggestions
  const practiceAccuracy = results.length > 0
    ? Math.round((results.filter((r) => r.wasCorrect).length / results.length) * 100)
    : 0;
  const whatsNextSuggestions = useConceptSuggestions(
    conceptId, 'practice', phase === 'complete', practiceAccuracy,
  );

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
      const subTopicEncoded = subTopicParam ? `&subTopic=${encodeURIComponent(subTopicParam)}` : '';
      const confidence = confidenceRef.current;
      const confidenceEncoded = confidence === 'low' || confidence === 'high' ? `&confidence=${confidence}` : '';
      const url = `/api/questions/next?topicId=${topicId}${subTopicEncoded}${confidenceEncoded}${excludeParam ? `&exclude=${excludeParam}` : ''}`;
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 5000);
      const res = await fetch(url, { signal: controller.signal });
      clearTimeout(timer);
      if (!res.ok) return null;
      const q = (await res.json()) as PracticeQuestion;
      // Keep the newest ladder the server sent (display only).
      const nextLadder = ladderOf(q);
      if (nextLadder) {
        const answered = answeredLadderRef.current;
        answeredLadderRef.current = null;
        // Only the first ladder after an answer can be behind; after that the server's is the truth.
        if (!answered || !ladderBehind(nextLadder, answered)) setLadder(nextLadder);
      }
      // Client-side duplicate guard: reject if we've already shown this question
      if (seenQuestionIdsRef.current.has(q.id)) return null;
      return q;
    } catch {
      return null;
    }
  }, [topicId, subTopicParam]);

  // Ask the confidence question at most once per topic per day.
  useEffect(() => {
    try {
      const askedOn = localStorage.getItem(`mathspark_confidence_${topicId}`);
      setAskConfidence(askedOn !== new Date().toDateString());
    } catch {
      setAskConfidence(false);
    }
  }, [topicId]);

  // Kick off a background prefetch of the next question.
  const prefetchNext = useCallback(() => {
    if (isFetchingRef.current || prefetchRef.current) return;
    isFetchingRef.current = true;
    const run = () => {
      fetchOneAdaptive().then((q) => {
        // Picked before the child answered the confidence question: fetch again with it.
        if (discardPrefetchRef.current) {
          discardPrefetchRef.current = false;
          run();
          return;
        }
        // Reject the prefetch if it's already in our seen set (race with DB timing)
        if (q && seenQuestionIdsRef.current.has(q.id)) {
          prefetchRef.current  = null;
        } else {
          prefetchRef.current  = q;
        }
        isFetchingRef.current = false;
      });
    };
    run();
  }, [fetchOneAdaptive]);

  // BUG 1 FIX: Register each new question in the seen-IDs set the moment it is displayed.
  useEffect(() => {
    const id = phase === 'reviewing' ? reviewQueue[reviewIndex]?.id : questions[qIndex]?.id;
    if (id) seenQuestionIdsRef.current.add(id);
  }, [phase, reviewQueue, reviewIndex, questions, qIndex]);

  // BUG 2 FIX: Reset the advance guard when a new answering phase begins.
  // A review question counts too: without this the guard set by the last lesson
  // question would still be up, and Continue would do nothing during the review.
  useEffect(() => {
    if (phase === 'answering' || phase === 'reviewing') {
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
    questionId: string; topicId: string;
    selected: string; isCorrect: boolean; hintUsed: number;
    misconceptionType?: string | null;
    isBonusQuestion?: boolean;
    parentQuestionId?: string | null;
    /** JSON answer of an interactive question, graded by the server. */
    interactiveAnswer?: string;
    /**
     * Time from the question appearing to the answer being chosen. Stored for
     * the mastery "speed" figure only: XP is decided by the server's own timer.
     */
    timeTakenMs?: number;
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
      .catch((err) => logError('[fetch]', err));
  }

  function submitAttempt(payload: AttemptPayload, onXpAwarded?: (xp: number) => void) {
    if (navigator.onLine) {
      fetch('/api/attempts', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(payload),
      })
        .then((r) => r.ok ? r.json() : null)
        .then((data) => { if (onXpAwarded && data?.xpAwarded) onXpAwarded(data.xpAwarded); })
        .catch((err) => { logError('[practice] save attempt', err); queueAttempt(payload); });
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
          body:    JSON.stringify({}),
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
        navigator.sendBeacon('/api/usage/heartbeat', '{}');
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
    // Pick a random answer that is NOT the correct one
    const wrongOptions = (['A', 'B', 'C', 'D'] as AnswerKey[]).filter((k) => k !== q.correctAnswer);
    const wrongKey = wrongOptions[Math.floor(Math.random() * wrongOptions.length)];
    handleAnswer(wrongKey, false, true);
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
    saveSessionData(topicId, accuracy, subTopicParam);
    track('lesson_completed', { topicId, accuracy });
  }, [phase, results, reviewResults, topicId, subTopicParam]);

  // ── Helpers ────────────────────────────────────────────────────────────────
  // Still reviewing while the result of a review question is showing, so the
  // result panel shows that question and Continue moves on through the review.
  const isReviewing      = phase === 'reviewing' || (phase === 'result' && inReview);
  const currentQuestion  = isReviewing ? reviewQueue[reviewIndex] : questions[qIndex];
  const currentSlotIndex = isReviewing ? reviewIndex : qIndex;

  // ── Publish screen context for the Sparky widget ────────────────────────────
  // SAFETY: text only — NEVER the correctAnswer — so Sparky can guide without
  // ever being handed the answer on a live graded question.
  // The question the child is actually looking at: a "try a similar one" question
  // sits on top of the main one, and no question shows on the intro or finish screens.
  const bonusShown = (bonusMode === 'answering' || bonusMode === 'result') && bonusQuestion !== null;
  const mainShown = phase === 'answering' || phase === 'result' || phase === 'reviewing';
  const shownQuestion = bonusShown ? bonusQuestion : mainShown ? currentQuestion : null;
  const shownPick = bonusShown ? (bonusMode === 'result' ? bonusSelected : null) : (phase === 'result' ? selected : null);
  const shownRight = bonusShown ? bonusCorrect : lastCorrect;
  useEffect(() => {
    if (!shownQuestion) {
      clearScreenContext();
      return;
    }
    const options = [shownQuestion.option1, shownQuestion.option2, shownQuestion.option3, shownQuestion.option4];
    const pickIndex = shownPick ? 'ABCD'.indexOf(shownPick) : -1;
    publishScreenContext({
      screen: 'practice',
      topicName: topicName || undefined,
      questionText: shownQuestion.questionText,
      // Interactive questions (tap, drag, build) have no A-D choices to list.
      options: shownQuestion.interactionType ? undefined : options,
      chosen: pickIndex >= 0 && !shownQuestion.interactionType ? options[pickIndex] : undefined,
      outcome: shownPick ? (shownRight ? 'right' : 'not yet') : undefined,
    });
  }, [shownQuestion, shownPick, shownRight, topicName]);

  // Clear context when leaving the practice page.
  useEffect(() => () => clearScreenContext(), []);

  // ── Step player sheet ───────────────────────────────────────────────────────
  // A different question on screen: put the sheet away.
  const shownQuestionId = shownQuestion ? shownQuestion.id : null;
  useEffect(() => { setShowSteps(false); setShowTeach(false); }, [shownQuestionId]);

  // Does the question on screen have an "Explain it to me" lesson? One light
  // call per question (yes or no, never the lesson itself); the working pane
  // asks the same thing and shares the answer.
  const teachAvailable = useTeachAvailable(shownQuestionId) === 'yes';

  // The working space sheet is for before answering: put it away for a new
  // question and as soon as this one is answered (a speed drill can time out under it).
  const shownAnswered = bonusShown ? bonusMode === 'result' : phase === 'result';
  useEffect(() => { setShowWork(false); }, [shownQuestionId, shownAnswered]);

  // Escape closes whichever sheet is open.
  useEffect(() => {
    if (!showSteps && !showWork && !showTeach && linked !== 'lesson') return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setShowSteps(false);
        setShowWork(false);
        setShowTeach(false);
        setLinked((l) => (l === 'lesson' ? 'after' : l));
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [showSteps, showWork, showTeach, linked]);

  // ── The tutor reacts ────────────────────────────────────────────────────────
  // A question appears.
  useEffect(() => {
    if (!shownQuestionId || shownAnswered) return;
    questionShownAtRef.current = Date.now();
    hiddenMsRef.current = 0;
    hiddenSinceRef.current = document.hidden ? Date.now() : 0;
    const first = tutorFirstRef.current;
    tutorFirstRef.current = false;
    tutorReact({ kind: 'question', first });
  }, [shownQuestionId, shownAnswered, tutorReact]);

  // Keep a running total of the time the page is hidden, for the time taken per question.
  useEffect(() => {
    const onVisibility = () => {
      if (document.hidden) {
        hiddenSinceRef.current = Date.now();
      } else if (hiddenSinceRef.current) {
        hiddenMsRef.current += Date.now() - hiddenSinceRef.current;
        hiddenSinceRef.current = 0;
      }
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => document.removeEventListener('visibilitychange', onVisibility);
  }, []);

  // A long pause on an open question: one nudge per question, after about 40
  // seconds with no tap or key press. Not while a lesson plays. And not once
  // the child has started writing on the pencil pad (a canvas): from then on
  // the board coach is the one who speaks about a pause, so the two never
  // talk over each other.
  useEffect(() => {
    if (!shownQuestionId || shownAnswered || lessonOpen) return;
    if (idleSaidForRef.current === shownQuestionId) return;
    const id = shownQuestionId;
    let timer: ReturnType<typeof setTimeout> | null = null;
    const arm = (e?: Event) => {
      if (timer) clearTimeout(timer);
      timer = null;
      const target = e && e.type === 'pointerdown' ? (e.target as HTMLElement | null) : null;
      if (target && target.tagName === 'CANVAS') idleSaidForRef.current = id;
      if (idleSaidForRef.current === id) return;
      timer = setTimeout(() => {
        timer = null;
        idleSaidForRef.current = id;
        tutorReact({ kind: 'idle', seconds: IDLE_SECONDS });
      }, IDLE_SECONDS * 1000);
    };
    window.addEventListener('pointerdown', arm);
    window.addEventListener('keydown', arm);
    arm();
    return () => {
      if (timer) clearTimeout(timer);
      window.removeEventListener('pointerdown', arm);
      window.removeEventListener('keydown', arm);
    };
  }, [shownQuestionId, shownAnswered, lessonOpen, tutorReact]);

  // The session ends (the lesson is finished, or the hearts have run out).
  useEffect(() => {
    if (phase === 'answering' || phase === 'reviewing') sessionEndSaidRef.current = false;
    if (phase !== 'complete' && phase !== 'no_hearts') return;
    if (sessionEndSaidRef.current) return;
    sessionEndSaidRef.current = true;
    const all = results.concat(reviewResults);
    let right = 0;
    for (let i = 0; i < all.length; i++) {
      if (all[i].wasCorrect) right += 1;
    }
    tutorReact({ kind: 'sessionEnd', correct: right, total: all.length });
  }, [phase, results, reviewResults, tutorReact]);

  // A lesson opens: the tutor stops talking at once.
  useEffect(() => {
    if (lessonOpen) tutorRef.current.stop();
  }, [lessonOpen]);

  // Wide screens: the result panel sits in the page under the options, so bring it into view.
  useEffect(() => {
    if (phase !== 'result') return;
    const el = resultSheetRef.current;
    if (!el || !window.matchMedia('(min-width: 1024px)').matches) return;
    el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }, [phase]);

  // ── Boot ───────────────────────────────────────────────────────────────────
  // Fetch one adaptive question at a time. Questions are served by the adaptive
  // engine (/api/questions/next): streak/difficulty use today's DB attempts, while
  // repeats are avoided across a rolling multi-day window (plus this session's set).
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

    // The `teach` link ("let me explain a question you missed") is used once. It
    // is taken out of the address straight away (no navigation, no reload), so a
    // reload or coming back starts ordinary practice, not the same lesson again.
    // Done a tick later, once the router is certainly ready to be told.
    const teachId = searchParams.get('teach') ?? '';
    if (searchParams.get('teach') !== null) {
      const bootPath = window.location.pathname;
      setTimeout(() => {
        if (window.location.pathname !== bootPath) return; // already on another screen
        const rest = new URLSearchParams(window.location.search);
        if (!rest.has('teach')) return;
        rest.delete('teach');
        const restQs = rest.toString();
        window.history.replaceState(null, '', `${bootPath}${restQs ? `?${restQs}` : ''}`);
      }, 0);
    }
    // Not in a speed drill: its timer would run under the lesson.
    const wantLinked = teachId !== '' && teachId.length <= 50 && !isSpeedMode;

    // First question from the adaptive engine
    const fetchFirst = (): Promise<PracticeQuestion> =>
      fetch(`/api/questions/next?topicId=${topicId}${subTopicParam ? `&subTopic=${encodeURIComponent(subTopicParam)}` : ''}`)
        .then((r) => { if (!r.ok) throw new Error('fetch failed'); return r.json() as Promise<PracticeQuestion>; });

    // With a `teach` link, the question to explain comes first. If it cannot be
    // served (unknown, switched off, no lesson, a test in progress, or the
    // request itself fails), ordinary practice starts instead, with no message.
    const loadFirst = async (): Promise<{ q: Question; linked: boolean }> => {
      if (wantLinked) {
        try {
          const r = await fetch(
            `/api/questions/explain?questionId=${encodeURIComponent(teachId)}` +
            `&topicId=${encodeURIComponent(topicId)}` +
            (subTopicParam ? `&subTopic=${encodeURIComponent(subTopicParam)}` : ''),
          );
          if (r.ok) {
            const q = (await r.json()) as Question;
            if (q && q.id === teachId) return { q, linked: true };
          }
        } catch { /* ordinary practice below */ }
      }
      const q = await fetchFirst();
      const firstLadder = ladderOf(q);
      if (firstLadder) setLadder(firstLadder);
      return { q, linked: false };
    };

    Promise.all([
      // Gate check — fails open (allowed: true) so API errors never block students
      fetch('/api/usage/check')
        .then((r) => r.ok ? r.json() : { allowed: true, used: 0, limit: 0, trial: null })
        .catch((err) => { logError('[practice] usage check', err); return { allowed: true, used: 0, limit: 0, trial: null }; }),
      fetch('/api/topics').then((r) => { if (!r.ok) throw new Error('Topics fetch failed'); return r.json(); }),
      loadFirst(),
    ])
      .then(([usageData, topics, first]: [{ allowed: boolean; used: number; limit: number; trial: TrialStatus | null }, Array<{ id: string; name: string }>, { q: Question; linked: boolean }]) => {
        const firstQ = first.q;
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
        if (first.linked) {
          // The child asked Sparky to explain this one: no intro screen, straight
          // to the question with its lesson playing. The lesson shows the whole
          // solution, so it counts as the strongest hint, exactly as when
          // "Explain it to me" is taken before answering in the working space.
          tookLessonBeforeAnswer();
          setLinked('lesson');
          setPhase('answering');
        } else {
          setPhase('intro');
        }
        // Immediately prefetch the second question
        prefetchNext();
      })
      .catch((err) => { logError('[practice] init fetch', err); setPhase('error'); });

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
    // Moving on from the explained question: an ordinary session from here.
    setLinked('off');

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
          }).catch((err) => {
            logError('[practice] fetch adaptive question', err);
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
  // `timedOut` is set when a speed drill ran out of time and no option was really chosen.
  function handleAnswer(key: AnswerKey, correct: boolean, timedOut?: boolean) {
    if (!currentQuestion) return;
    setSelected(key);
    setLastCorrect(correct);
    setPhase('result');

    // Move the topic ladder on straight away, so the strip keeps up with the child.
    if (ladder && !isReviewing) {
      const moved = ladderAfterAnswer(ladder, correct);
      answeredLadderRef.current = moved;
      setLadder(moved);
    }

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

    // Sounds + mini confetti
    if (correct) {
      if (newStreak === 3 || newStreak === 5) playStreak();
      else playCorrect();
      setShowMiniConfetti(true);
    } else {
      playWrong();
      // Auto-show hint level 1 after a wrong answer (keeping any further hints
      // the child already opened in the working space)
      setHintLevel((l) => Math.max(l, 1));
      // Feature 1: fire Socratic stuck-coach on the 2nd+ wrong attempt.
      const prevWrong = wrongCountByQuestionRef.current.get(currentQuestion.id) ?? 0;
      const nextWrong = prevWrong + 1;
      wrongCountByQuestionRef.current.set(currentQuestion.id, nextWrong);
      setShowCoach(nextWrong >= 2);
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

    // The tutor reacts in one short line. It is told the outcome; it never decides it.
    if (correct) {
      missesInARowRef.current = 0;
      tutorReact({
        kind: 'correct',
        streak: newStreak,
        usedHint: hintUsed || hintLevel > 0,
        secondsTaken: secondsOnQuestion(),
      });
    } else {
      missesInARowRef.current += 1;
      // No option was really chosen when the time ran out, or on a tap, drag or build question.
      const reallyChose = !timedOut && !currentQuestion.interactionType;
      tutorReact({
        kind: 'miss',
        chosenText: reallyChose ? optionText(currentQuestion, key) : '',
        misconception: reallyChose && misconceptionType ? misconceptionType : undefined,
        missesInARow: missesInARowRef.current,
      });
    }

    // Record attempt (offline-aware); show XP float only when server confirms XP was awarded
    if (studentId) {
      submitAttempt(
        {
          questionId: currentQuestion.id,
          topicId,
          selected: key,
          isCorrect: correct,
          hintUsed: hintLevel,
          misconceptionType,
          timeTakenMs: msOnQuestion(),
          ...(currentQuestion.interactionType && interactiveAnswerRef.current
            ? { interactiveAnswer: interactiveAnswerRef.current }
            : {}),
        },
        correct
          ? (awarded) => {
              if (awarded > 0) {
                setShowXpFloat(true);
                setTimeout(() => setShowXpFloat(false), 1500);
              }
            }
          : undefined,
      );
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

    // Auto-advance for correct answers, on phones and tablets only. On wide screens
    // the step-by-step pane is open beside the question, so the child moves on
    // with Continue when they have finished reading it.
    const wideScreen = typeof window !== 'undefined' && window.matchMedia('(min-width: 1024px)').matches;
    if (correct && !wideScreen) {
      advanceTimer.current = setTimeout(() => advance(newHearts), AUTO_ADVANCE_MS);
    }
  }

  function handleGotIt() {
    advance(hearts);
  }

  /** Whole seconds since the question on screen appeared. */
  function secondsOnQuestion(): number {
    if (!questionShownAtRef.current) return 0;
    return Math.max(0, Math.round((Date.now() - questionShownAtRef.current) / 1000));
  }

  /**
   * Milliseconds the question on screen has been open, leaving out time the
   * page was hidden, kept within 0 to 10 minutes. 0 means "not known" (the
   * engine leaves such attempts out of the speed figure).
   */
  function msOnQuestion(): number {
    if (!questionShownAtRef.current) return 0;
    const now = Date.now();
    const hidden = hiddenMsRef.current + (hiddenSinceRef.current ? now - hiddenSinceRef.current : 0);
    const ms = Math.round(now - questionShownAtRef.current - hidden);
    return Math.min(600_000, Math.max(0, ms));
  }

  // A hint is opened (main question / bonus question): the same state as before, and the tutor says a line.
  function openHint(n: number) {
    setHintLevel(n);
    setHintUsed(true);
    tutorReact({ kind: 'hint', level: n });
  }

  function openBonusHint(n: number) {
    setBonusHintLevel(n);
    setBonusHintUsed(true);
    tutorReact({ kind: 'hint', level: n });
  }

  // "Explain it to me" taken before answering. The lesson shows the whole
  // solution, so it counts like "show me how": the hint is marked as used at
  // the highest level (no heart is lost on a later miss). Nothing else changes
  // in what is sent to the server. The tutor says nothing: the lesson is about to talk.
  function tookLessonBeforeAnswer() {
    setHintLevel(3);
    setHintUsed(true);
  }

  function tookBonusLessonBeforeAnswer() {
    setBonusHintLevel(3);
    setBonusHintUsed(true);
  }

  // Reading the steps or using the working space after a right answer: stay on
  // this question until the child presses Continue.
  function pauseAutoAdvance() {
    if (advanceTimer.current) {
      clearTimeout(advanceTimer.current);
      advanceTimer.current = null;
    }
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
      .catch((err) => { logError('[practice] fetch similar question', err); setBonusMode('unavailable'); });
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

    if (correct) playCorrect(); else { playWrong(); setBonusHintLevel((l) => Math.max(l, 1)); }

    // The tutor reacts in one short line, as on a main question.
    if (correct) {
      missesInARowRef.current = 0;
      tutorReact({
        kind: 'correct',
        streak: newStreak,
        usedHint: bonusHintUsed || bonusHintLevel > 0,
        secondsTaken: secondsOnQuestion(),
      });
    } else {
      missesInARowRef.current += 1;
      const bonusNote = bonusQuestion[`misconception${key}` as keyof Question];
      tutorReact({
        kind: 'miss',
        chosenText: optionText(bonusQuestion, key),
        misconception: typeof bonusNote === 'string' && bonusNote ? bonusNote : undefined,
        missesInARow: missesInARowRef.current,
      });
    }

    // Track bonus questions toward trial count
    sessionQuestionsAnsweredRef.current += 1;
    setSessionQuestionsAnswered(sessionQuestionsAnsweredRef.current);

    if (studentId) {
      submitAttempt({
        questionId:      bonusQuestion.id,
        topicId,
        selected:        key,
        isCorrect:       correct,
        hintUsed:        bonusHintLevel,
        timeTakenMs:     msOnQuestion(),
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
    setInReview(false);
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
    setLinked('off');
    setSpeedTimedOut(false);
    setSpeedRemaining(SPEED_DRILL_MS);
    if (speedTimerRef.current) { clearInterval(speedTimerRef.current); speedTimerRef.current = null; }
    sessionSavedRef.current = false;
    prefetchRef.current      = null;
    isFetchingRef.current    = false;
    isAdvancingRef.current   = false;
    seenQuestionIdsRef.current = new Set();
    missesInARowRef.current = 0;

    setPhase('loading');
    fetchOneAdaptive().then((q) => {
      if (!q) { router.replace('/chapters'); return; }
      setQuestions([q]);
      setPhase('answering');
      prefetchNext();
    });
  }

  // ── Full-screen phases ─────────────────────────────────────────────────────

  if (phase === 'error') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-paper pb-8">
        <div className="animate-sparky-bounce">
          <Sparky mood="thinking" size={120} />
        </div>
        <div className="text-center space-y-2">
          <h2 className="text-heading text-ink">📭 No questions available yet</h2>
          <p className="text-ink-muted font-semibold">
            This lesson doesn&apos;t have questions yet. Check back soon!
          </p>
        </div>
        <DuoButton variant="white" fullWidth onClick={() => router.push('/practice')}>
          Back to Chapters →
        </DuoButton>
      </div>
    );
  }

  if (phase === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-paper gap-4 px-6">
        {fetchRetry ? (
          <>
            <Sparky mood="encouraging" size={100} />
            <p className="text-ink font-bold text-center">Oops! Let&apos;s try again 🔄</p>
            <DuoButton variant="blue" onClick={() => {
              setFetchRetry(false);
              isAdvancingRef.current = false;
              fetchOneAdaptive().then((q) => {
                if (!q) { setShowConfetti(true); setPhase('complete'); return; }
                setQuestions((prev) => [...prev, q]);
                setQIndex((prev) => prev + 1);
                setPhase('answering');
              }).catch((err) => { logError('[practice] retry fetch adaptive', err); setFetchRetry(true); });
            }}>
              Retry →
            </DuoButton>
          </>
        ) : (
          <>
            <div className="animate-sparky-bounce">
              <Sparky mood="thinking" size={100} />
            </div>
            <p className="text-ink-muted font-semibold">Loading your lesson…</p>
          </>
        )}
      </div>
    );
  }

  if (phase === 'intro') {
    return (
      <LessonIntro
        topicName={topicName}
        topicEmoji={TOPIC_EMOJI[topicId] ?? '📚'}
        questionCount={LESSON_SIZE}
        onStart={() => setPhase('answering')}
        onConfidence={askConfidence ? (confidence) => {
          confidenceRef.current = confidence;
          try { localStorage.setItem(`mathspark_confidence_${topicId}`, new Date().toDateString()); } catch { /* storage unavailable */ }
          // The second question was picked before we knew this: pick it again with the signal.
          if (confidence !== 'medium') {
            if (isFetchingRef.current) {
              discardPrefetchRef.current = true;   // the fetch in flight did not know this
            } else {
              prefetchRef.current = null;
              prefetchNext();
            }
          }
        } : undefined}
      />
    );
  }

  if (phase === 'no_hearts') {
    return (
      <NoHeartsScreen
        results={results}
        onRetry={resetLesson}
        onHome={() => router.push('/practice')}
      />
    );
  }

  if (phase === 'review_intro') {
    return (
      <ReviewIntroScreen
        count={reviewQueueRef.current.length}
        onStart={() => { setInReview(true); setPhase('reviewing'); }}
      />
    );
  }

  if (phase === 'complete') {
    if (showStreakCommitment) {
      return (
        <StreakCommitment
          onDone={() => {
            setShowStreakCommitment(false);
            router.push(conceptId ? `/learn/concept-map?open=${conceptId}` : '/chapters');
          }}
        />
      );
    }

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
    const subTier = MONETIZATION_ENABLED
      ? parseInt(
          typeof window !== 'undefined' ? (localStorage.getItem('mathspark_subscription_tier') ?? '0') : '0',
          10,
        )
      : UNLIMITED_TIER;

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
      <CelebrationCascade
        mainResults={results}
        reviewResults={reviewResults}
        totalXp={xp}
        streak={streak}
        hasReviewMistakes={hasReviewMistakes}
        gradeUpCta={gradeUpCta}
        topicId={topicId}
        topicName={topicName}
        onComplete={() => {
          // Show streak commitment if not yet set
          if (typeof window !== 'undefined' && !localStorage.getItem('mathspark_streakGoalSet')) {
            setShowStreakCommitment(true);
          } else {
            router.push(conceptId ? `/learn/concept-map?open=${conceptId}` : '/chapters');
          }
        }}
        whatsNextSuggestions={whatsNextSuggestions}
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
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-paper pb-8">
        <div className="animate-sparky-bounce">
          <Sparky mood="encouraging" size={120} />
        </div>
        <div className="text-center space-y-3">
          <h2 className="text-heading text-ink">
            Daily practice limit reached! ⏰
          </h2>
          <p className="text-ink-muted font-semibold leading-relaxed">
            You&apos;ve practiced for{' '}
            <span className="font-extrabold text-ink">{formatMinutes(usageInfo.used)}</span>
            {!isUnlimitedPlan(tierLimit) && tierLimit > 0 && (
              <> out of <span className="font-extrabold text-ink">{formatMinutes(tierLimit)}</span></>
            )}{' '}
            today. Come back tomorrow — every day you practice, you get stronger! 💪
          </p>
          {!isUnlimitedPlan(tierLimit) && (
            <div className="bg-hint border-2 border-hint-ink/30 rounded-card px-4 py-3 text-left">
              <p className="text-caption text-hint-ink mb-1">Want more practice time?</p>
              <p className="text-sm font-semibold text-hint-ink">Upgrade your plan to unlock longer daily sessions and unlimited practice.</p>
            </div>
          )}
        </div>
        <div className="w-full max-w-sm space-y-3">
          {!isUnlimitedPlan(tierLimit) && (
            <DuoButton variant="blue" fullWidth onClick={() => router.push('/pricing')}>
              Upgrade Plan 🚀
            </DuoButton>
          )}
          <DuoButton variant="white" fullWidth onClick={() => router.push('/practice')}>
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
      <div className="flex flex-col items-center justify-center min-h-screen px-6 gap-6 bg-paper pb-8">
        <div className="animate-sparky-bounce">
          <Sparky mood="encouraging" size={120} />
        </div>
        <div className="text-center space-y-3">
          <h2 className="text-heading text-ink">
            {wasExhaustedAtBoot ? 'Come back tomorrow! ⏰' : 'Amazing start! 🎉'}
          </h2>
          <p className="text-ink-muted font-semibold leading-relaxed">
            {wasExhaustedAtBoot
              ? "You've used your free daily question. Subscribe to practice anytime!"
              : `You've answered ${totalUsed} questions — your free trial is complete! Subscribe to keep your streak going.`
            }
          </p>
          <div className="bg-hint border-2 border-hint-ink/30 rounded-card px-4 py-3 text-left">
            <p className="text-caption text-hint-ink mb-2">Unlock with a subscription:</p>
            <ul className="space-y-1.5 text-sm font-semibold text-hint-ink">
              {['Unlimited daily practice', 'Hints + step-by-step solutions', 'Progress tracking & badges', 'Full IPM mock tests'].map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="text-success">✅</span> {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
        <div className="w-full max-w-sm space-y-3">
          <DuoButton variant="blue" fullWidth onClick={() => router.push('/pricing')}>
            Upgrade Now 🚀
          </DuoButton>
          <DuoButton variant="white" fullWidth onClick={() => router.push('/practice')}>
            {wasExhaustedAtBoot ? 'Back to chapters' : 'Come back tomorrow for 1 free question'}
          </DuoButton>
        </div>
      </div>
    );
  }

  // ── Question screen (answering | result | reviewing) ──────────────────────

  if (!currentQuestion) return null;

  const accentCls = CARD_ACCENTS[currentSlotIndex % CARD_ACCENTS.length];
  // Bonus helpers
  const bonusOptKey      = bonusSelected ? `misconception${bonusSelected}` as keyof Question : null;
  const bonusMisconText  = bonusOptKey && bonusQuestion ? bonusQuestion[bonusOptKey] as string : '';
  const bonusCorrectText = bonusQuestion ? bonusQuestion[`option${['A','B','C','D'].indexOf(bonusQuestion.correctAnswer) + 1}` as keyof Question] as string : '';
  const canOneMore = bonusOriginRef.current
    ? (bonusCountByOriginRef.current.get(bonusOriginRef.current.id) ?? 0) < MAX_BONUS_PER_ORIGIN &&
      bonusServedRef.current < MAX_BONUS_PER_LESSON
    : false;

  // The second pane: the figure or working space, then the steps once answered.
  const mainFigure  = currentQuestion.visual && currentQuestion.visual.figure ? currentQuestion.visual.figure : null;
  const bonusFigure = bonusQuestion && bonusQuestion.visual && bonusQuestion.visual.figure ? bonusQuestion.visual.figure : null;

  // The tutor's last line, in a speech bubble joined to a small Sparky. The line
  // shows whether or not the voice is on. The bubble always has room for two
  // lines, so the question below does not move when the line changes; a longer
  // line wraps and the bubble grows. With nothing to say, the bubble holds a
  // quiet standing line (never spoken, never announced) instead of a bare face.
  const tutorRow = (
    <div className="flex items-center gap-3">
      <div className="flex-shrink-0" aria-hidden="true">
        <Sparky mood={tutor.speaking ? 'happy' : 'thinking'} size={40} />
      </div>
      <div className="relative flex-1 min-w-0 min-h-[60px] flex items-center bg-white border-2 border-line rounded-control px-3 py-2">
        {/* The bubble's tail, pointing at Sparky */}
        <span
          className="absolute -left-[7px] top-1/2 -mt-1.5 w-3 h-3 bg-white border-l-2 border-b-2 border-line rotate-45"
          aria-hidden="true"
        />
        <p
          className={tutorCaption ? 'text-[15px] font-bold text-ink leading-snug [overflow-wrap:anywhere]' : 'sr-only'}
          aria-live="polite"
        >
          {tutorCaption}
        </p>
        {!tutorCaption && (
          <p className="text-[15px] font-semibold text-ink-muted leading-snug">
            I&apos;m here if you need me.
          </p>
        )}
      </div>
    </div>
  );

  // The tutor's voice: on or off, and which voice. A small group at the right of
  // the label row above the question, so it never competes with the question.
  const voiceControls = (
    <div className="flex-shrink-0 flex items-center gap-2" role="group" aria-label="Sparky's voice">
      <button
        type="button"
        role="switch"
        aria-checked={tutor.enabled}
        aria-label="Sparky's voice"
        title={tutor.enabled ? 'Sparky reads out loud' : 'Sparky is quiet'}
        onClick={() => tutor.setEnabled(!tutor.enabled)}
        className={`min-h-[48px] min-w-[48px] px-3 rounded-tile border-2 border-line font-extrabold text-[13px] flex items-center justify-center gap-1.5 hover:border-ink transition-colors ${
          tutor.enabled ? 'bg-white text-ink' : 'bg-soft text-ink-muted'
        }`}
      >
        <span className="text-lg leading-none" aria-hidden="true">{tutor.enabled ? '🗣️' : '🤫'}</span>
        <span className="hidden sm:inline whitespace-nowrap">Voice {tutor.enabled ? 'on' : 'off'}</span>
      </button>
      <VoiceSettingsButton />
    </div>
  );

  return (
    // Phones and tablets: the usual single column. Wide screens: the question
    // screen breaks out of the narrow app column (32rem) into one centred
    // workspace of two panels: 60rem from 1024px, 72rem from 1280px. The header,
    // the progress bar and the panels all share its edges.
    // No entry animation here: a page-level container must never start invisible.
    <div className="flex flex-col bg-paper min-h-screen lg:-mx-56 xl:-mx-80">
      {/* Confetti (full — lesson complete) */}
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}
      {/* Mini confetti — per correct answer */}
      {showMiniConfetti && <Confetti variant="mini" onDone={() => setShowMiniConfetti(false)} />}

      {/* XP Float */}
      {showXpFloat && <XpFloat amount={isReviewing ? XP_REVIEW : XP_CORRECT} />}

      {/* ── Dark header ── */}
      <div className="bg-ink px-4 py-3 flex items-center gap-3 sticky top-0 z-30 flex-shrink-0">
        <button
          onClick={() => router.push('/practice')}
          className="text-white/70 hover:text-white font-bold text-xl min-h-[44px] min-w-[44px] flex items-center justify-center flex-shrink-0"
          aria-label="Back"
        >
          ←
        </button>
        <div className="flex-1 min-w-0">
          <p className="text-white font-display font-semibold text-lg leading-tight truncate">{topicName}</p>
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

      {/* ── Where the child is on this topic's ladder (only when the server sends one) ──
          Not repeated on the bonus question's own screen: a bonus question is a
          side step, and the ladder does not move while it is open. */}
      {ladder && <TopicLadder ladder={ladder} />}

      {/* ── Offline banner ── */}
      {!isOnline && (
        <div className="bg-hint border-b-2 border-hint-ink/30 px-4 py-2 text-xs font-bold text-hint-ink text-center">
          📶 You&apos;re offline — practising with cached questions!
        </div>
      )}

      {/* ── Progress bar / Review badge ── */}
      {isReviewing ? (
        <div className="bg-soft px-4 py-2 flex items-center gap-2 border-b-2 border-line">
          <span className="text-ink text-sm font-extrabold">📚 Review mode</span>
          <span className="text-ink-muted text-xs font-semibold">{reviewIndex + 1} / {reviewQueue.length}</span>
        </div>
      ) : (
        <LessonProgressBar total={LESSON_SIZE} currentIdx={qIndex} results={results} />
      )}

      {/* Speed drill timer bar */}
      {isSpeedMode && phase === 'answering' && (
        <div className="h-2 bg-soft relative">
          <div
            className={`h-full transition-[width] duration-200 ${
              speedRemaining > 60_000 ? 'bg-action' :
              speedRemaining > 30_000 ? 'bg-star' : 'bg-hint-ink'
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
            <div className="bg-soft border-b-2 border-line px-4 py-2 text-xs font-bold text-ink text-center flex items-center justify-center gap-2">
              🎁 Your free daily question — <button onClick={() => router.push('/pricing')} className="underline">Upgrade for unlimited</button>
            </div>
          );
        }
        if (questionsLeft <= 3 && questionsLeft > 0) {
          return (
            <div className="bg-hint border-b-2 border-hint-ink/30 px-4 py-2 text-xs font-bold text-hint-ink text-center flex items-center justify-center gap-2">
              ⚡ {questionsLeft} free question{questionsLeft > 1 ? 's' : ''} left — <button onClick={() => router.push('/pricing')} className="underline">Upgrade to continue</button>
            </div>
          );
        }
        return null;
      })()}

      {/* ── Two panels on wide screens: question (left), working pane (right) ──
          The page itself scrolls; neither panel has a scrollbar of its own while
          the question is open. */}
      <div className={`flex-1 flex flex-col ${WORKSPACE_COLS} lg:px-4 lg:pt-5 lg:pb-24`}>
      <div className="flex-1 flex flex-col min-w-0 lg:gap-4">

      {/* ── Question area (scrollable, padded for bottom panel) ── */}
      <div
        className={`flex-1 overflow-y-auto px-4 pt-4 space-y-4 lg:flex-none lg:overflow-visible lg:px-0 lg:pt-0 lg:pb-0 ${
          phase === 'result' ? 'pb-[72vh]' : 'pb-20'
        }`}
      >
        {tutorRow}

        {/* After the lesson from a `teach` link: a similar question is offered first.
            The explained question stays below for a child who would rather answer it. */}
        {linked === 'after' && phase === 'answering' && (
          <div className="bg-hint border-2 border-ink rounded-card px-4 py-3 space-y-3" role="group" aria-label="Your turn">
            <p className="text-[16px] font-extrabold text-ink leading-snug">
              <span aria-hidden="true">🌟</span> Now it&apos;s your turn!
            </p>
            <p className="text-[15px] font-semibold text-ink leading-relaxed">
              Try a question just like the one Sparky explained, or have a go at this one below.
            </p>
            <button
              type="button"
              onClick={() => requestBonus(currentQuestion, false)}
              disabled={bonusMode !== 'off'}
              className="ui-btn ui-btn-primary w-full"
            >
              Try one like it <span aria-hidden="true">→</span>
            </button>
            <div className="flex flex-col sm:flex-row gap-2">
              <button type="button" onClick={() => setLinked('lesson')} className="ui-btn flex-1 text-sm">
                <span aria-hidden="true">🎓</span> Watch it again
              </button>
              <button type="button" onClick={handleGotIt} className="ui-btn flex-1 text-sm">
                Next question <span aria-hidden="true">→</span>
              </button>
            </div>
          </div>
        )}

        {/* Label row: which question this is (left), the tutor's voice controls (right) */}
        <div className="flex items-center gap-2">
          <div className="flex-1 min-w-0">
            <div className={`inline-flex items-center gap-2 text-[13px] font-extrabold px-3 py-1 rounded-full border-2 ${accentCls}`}>
              {isReviewing
                ? `🔁 Review question ${reviewIndex + 1} of ${reviewQueue.length}`
                : isSpeedMode
                ? `⚡ Speed Drill — Q${qIndex + 1} of ${LESSON_SIZE}`
                : `Question ${qIndex + 1} of ${LESSON_SIZE}`}
              {streak >= 3 && !isReviewing && (
                <span className="text-ink font-extrabold">🔥 {streak}</span>
              )}
            </div>
          </div>
          {voiceControls}
        </div>

        {/* On phones and tablets the question's figure sits between the question and the
            options; wide screens show it in the side pane. */}
        <QuestionCard
          question={currentQuestion}
          answered={phase === 'result'}
          selected={selected}
          onAnswer={handleAnswer}
          onInteractiveAnswer={(answer) => { interactiveAnswerRef.current = answer; }}
          figureSlot={mainFigure ? (
            <div className="lg:hidden bg-white border-2 border-line rounded-card p-3">
              <FigureView spec={mainFigure} />
            </div>
          ) : undefined}
        />

        {/* Hints and the pencil pad before answering (phones and tablets; wide screens have the side pane) */}
        {phase !== 'result' && (
          <button
            type="button"
            onClick={() => setShowWork(true)}
            className="lg:hidden ui-btn w-full text-sm"
          >
            <span aria-hidden="true">✏️</span> Working space
          </button>
        )}
      </div>

      {/* ── Result panel: a sheet that slides up on phones and tablets; in the page under the options on wide screens ── */}
      {phase === 'result' && (
        <div
          ref={resultSheetRef}
          className={`fixed bottom-0 left-0 right-0 max-w-lg mx-auto z-[60] max-h-[72vh] animate-slide-up overflow-y-auto rounded-t-card border-2 border-b-0 border-ink lg:static lg:z-auto lg:max-w-none lg:mx-0 lg:max-h-none lg:overflow-visible lg:rounded-card lg:border-b-2 lg:scroll-mb-24 ${
            lastCorrect
              ? 'bg-success-soft'
              : 'bg-retry-soft'
          }`}
        >
          {/* Phones and tablets: the steps open in a sheet. Wide screens have them in the side pane. */}
          {/* "Explain it to me" sits beside it when this question has a lesson. */}
          {(teachAvailable || hasSolutionSteps(currentQuestion)) && (
            <div className="lg:hidden px-4 pt-4 flex gap-2">
              {teachAvailable && (
                <button
                  type="button"
                  onClick={() => { pauseAutoAdvance(); setShowTeach(true); }}
                  className="ui-btn ui-btn-primary flex-1 text-sm"
                >
                  <span aria-hidden="true">🎓</span> Explain it to me
                </button>
              )}
              {hasSolutionSteps(currentQuestion) && (
                <button
                  type="button"
                  onClick={() => { pauseAutoAdvance(); setShowSteps(true); }}
                  className="ui-btn flex-1 text-sm"
                >
                  <span aria-hidden="true">📖</span> See the steps
                </button>
              )}
            </div>
          )}
          {lastCorrect ? (
            <CorrectPanel
              feedback={feedback}
              streak={streak}
              xpEarned={isReviewing ? XP_REVIEW : XP_CORRECT}
              question={currentQuestion}
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
              onHintLevelUp={openHint}
              onWatchSolution={() => setShowWalkthrough(true)}
              onTrySimilar={() => requestBonus(currentQuestion, false)}
              canTrySimilar={bonusMode === 'off'}
              showCoach={showCoach}
            />
          )}
        </div>
      )}
      </div>

      {/* ── Working pane (wide screens) ──
          `active` goes false while a bonus question or the walkthrough covers it, so a lesson here stops.
          While the question is open the pane is part of the page and scrolls with
          it (no scrollbar of its own). Once answered, the page grows a long
          result panel on the left, so the pane (now the solution) stays in view
          beside it, and only scrolls inside itself if it is taller than the window. */}
      <aside
        className={`hidden lg:block bg-white border-2 border-line rounded-card p-4 ${
          phase === 'result' ? 'lg:sticky lg:top-[84px] lg:max-h-[calc(100vh-164px)] lg:overflow-y-auto' : ''
        }`}
        onPointerDown={pauseAutoAdvance}
        onKeyDown={pauseAutoAdvance}
      >
        <WorkPane
          key={currentQuestion.id}
          question={currentQuestion}
          stage={phase === 'result' ? 'answered' : 'answering'}
          mode="practice"
          hintLevel={hintLevel}
          onHintLevelUp={openHint}
          onLessonBeforeAnswer={tookLessonBeforeAnswer}
          onLessonChange={onPaneLesson}
          active={bonusMode === 'off' && !showWalkthrough}
        />
      </aside>
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
          className="lg:hidden fixed right-3 z-[65] animate-slide-up"
          style={{ bottom: 'calc(72vh + 12px)', animationDelay: '1.2s', animationFillMode: 'backwards' }}
        >
          <button
            onClick={() => requestOpenSparky()}
            className="flex flex-col items-end gap-1"
            aria-label="Ask Sparky"
          >
            <div className="bg-white rounded-control px-3 py-2 border-2 border-ink shadow-hard-sm max-w-[130px]">
              <p className="text-xs font-bold text-ink text-center leading-snug">
                {lastCorrect ? 'Keep it up! 🎉' : 'Need help? 💬'}
              </p>
            </div>
            <div className={`rounded-full p-1.5 border-2 border-ink ${lastCorrect ? 'bg-success' : 'bg-action'}`}>
              <Sparky mood={lastCorrect ? 'celebrating' : 'encouraging'} size={32} />
            </div>
          </button>
        </div>
      )}

      {/* ── Bonus "Repeat Similar" overlay ─────────────────────────────────── */}
      {bonusMode !== 'off' && (
        // Phones and tablets: a full-height column whose question area scrolls.
        // Wide screens: the whole screen scrolls as one page (no panel has its own
        // scrollbar while the question is open), under a header that stays put.
        // No entry animation: a full-screen container must never start invisible.
        <div
          className="fixed inset-0 bg-paper z-[80] flex flex-col max-w-lg mx-auto lg:max-w-none lg:overflow-y-auto"
        >
          {/* Header: the bar runs the full width; what is in it lines up with the workspace below */}
          <div className="bg-ink flex-shrink-0 lg:sticky lg:top-0 lg:z-10">
            <div className="px-4 py-3 flex items-center gap-3 lg:w-full lg:max-w-[60rem] xl:max-w-[72rem] lg:mx-auto">
              <button
                onClick={handleBonusGotIt}
                className="text-white/70 hover:text-white font-bold text-sm min-h-[44px] min-w-[44px] flex items-center gap-1 flex-shrink-0"
              >
                ← Back
              </button>
              <div className="flex-1 min-w-0">
                <p className="text-white font-display font-semibold text-lg leading-tight truncate">{topicName}</p>
              </div>
              <HeartsBar hearts={hearts} />
            </div>
          </div>

          {/* Searching */}
          {bonusMode === 'searching' && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4 px-6">
              <div className="animate-sparky-bounce">
                <Sparky mood="thinking" size={80} />
              </div>
              <p className="text-ink-muted font-semibold text-center">Finding a similar question…</p>
            </div>
          )}

          {/* Unavailable */}
          {bonusMode === 'unavailable' && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4 px-6">
              <Sparky mood="encouraging" size={80} />
              <p className="text-ink font-bold text-center text-lg leading-snug">
                You&apos;ve practiced all similar questions!<br />Let&apos;s keep going 💪
              </p>
              <DuoButton variant="green" onClick={handleBonusGotIt}>
                Next Question →
              </DuoButton>
            </div>
          )}

          {/* Bonus question screen. Wide screens: the question (left) and its working pane (right)
              in the same centred workspace as the lesson, scrolling together with the page. */}
          {(bonusMode === 'answering' || bonusMode === 'result') && bonusQuestion && (
            <div className={`flex-1 min-h-0 flex flex-col lg:flex-none ${WORKSPACE_COLS} lg:w-full lg:max-w-[60rem] xl:max-w-[72rem] lg:mx-auto lg:px-4 lg:pt-5 lg:pb-10`}>
              <div className="flex-1 min-h-0 flex flex-col min-w-0 lg:gap-4">
              <div
                className={`flex-1 overflow-y-auto px-4 pt-4 space-y-4 lg:flex-none lg:overflow-visible lg:px-0 lg:pt-0 lg:pb-0 ${
                  bonusMode === 'result' ? 'pb-[200px]' : 'pb-20'
                }`}
              >
                {tutorRow}

                {/* Label row: the one bonus marker (left), the tutor's voice controls (right).
                    It sits where "Question 3 of 10" sits in the lesson. */}
                <div className="flex items-center gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="inline-block text-[13px] font-extrabold leading-snug px-3 py-1.5 rounded-control bg-hint text-hint-ink border-2 border-star">
                      <span aria-hidden="true">⭐ </span>Bonus Question — Same concept, different numbers!
                    </p>
                  </div>
                  {voiceControls}
                </div>

                {/* The question card, exactly as in the lesson. Its figure sits between the question
                    and the options on phones and tablets; wide screens show it in the side pane. */}
                <QuestionCard
                  question={bonusQuestion}
                  answered={bonusMode === 'result'}
                  selected={bonusSelected}
                  onAnswer={(key) => handleBonusAnswer(key)}
                  figureSlot={bonusFigure ? (
                    <div className="lg:hidden bg-white border-2 border-line rounded-card p-3">
                      <FigureView spec={bonusFigure} />
                    </div>
                  ) : undefined}
                />

                {/* Hints and the pencil pad before answering (phones and tablets) */}
                {bonusMode === 'answering' && (
                  <button
                    type="button"
                    onClick={() => setShowWork(true)}
                    className="lg:hidden ui-btn w-full text-sm"
                  >
                    <span aria-hidden="true">✏️</span> Working space
                  </button>
                )}

                {/* Wrong bonus: misconception + hints + solution */}
                {bonusMode === 'result' && !bonusCorrect && (
                  <>
                    {bonusMisconText && (
                      <div className="bg-soft border-2 border-line rounded-card px-4 py-3">
                        <p className="text-caption text-ink-muted mb-1">💡 Common mistake</p>
                        <p className="text-sm text-ink font-semibold leading-snug">{bonusMisconText}</p>
                      </div>
                    )}
                    <HintSystem
                      hint1={bonusQuestion.hint1}
                      hint2={bonusQuestion.hint2}
                      hint3={bonusQuestion.hint3}
                      level={bonusHintLevel}
                      onLevelUp={openBonusHint}
                      spoken={bonusQuestion.speech ? bonusQuestion.speech.hints : undefined}
                    />
                    <StepByStep steps={bonusQuestion.stepByStep} />
                  </>
                )}
              </div>

              {/* Bonus bottom panel */}
              {bonusMode === 'result' && (
                <div
                  className={`fixed bottom-0 left-0 right-0 max-w-lg mx-auto z-[90] animate-slide-up lg:static lg:z-auto lg:max-w-none lg:mx-0 lg:flex-shrink-0 lg:border-2 lg:rounded-card ${
                    bonusCorrect
                      ? 'bg-success-soft border-t-2 border-ink'
                      : 'bg-retry-soft border-t-2 border-ink'
                  }`}
                  style={{ minHeight: '160px' }}
                >
                  <div className="px-4 pt-4 pb-6 space-y-3">
                    <p className={`font-extrabold text-base ${bonusCorrect ? 'text-success' : 'text-retry'}`}>
                      {bonusFeedback}
                    </p>
                    {bonusCorrect && (
                      <p className="text-ink text-xs font-bold">
                        ✅ {bonusQuestion.correctAnswer}: {bonusCorrectText}
                      </p>
                    )}
                    {teachAvailable && (
                      <button
                        type="button"
                        onClick={() => setShowTeach(true)}
                        className="lg:hidden w-full min-h-[48px] bg-action border-2 border-ink shadow-hard-sm text-white font-extrabold text-sm rounded-control flex items-center justify-center gap-2"
                      >
                        <span aria-hidden="true">🎓</span> Explain it to me
                      </button>
                    )}
                    {hasSolutionSteps(bonusQuestion) && (
                      <button
                        type="button"
                        onClick={() => setShowSteps(true)}
                        className="lg:hidden w-full min-h-[48px] bg-white border-2 border-ink shadow-hard-sm text-ink font-extrabold text-sm rounded-control flex items-center justify-center gap-2"
                      >
                        <span aria-hidden="true">📖</span> See the steps
                      </button>
                    )}
                    {!bonusCorrect && canOneMore && (
                      <button
                        onClick={handleBonusOneMore}
                        className="w-full min-h-[48px] bg-white border-2 border-ink shadow-hard-sm text-ink font-extrabold text-sm rounded-control flex items-center justify-center gap-2"
                      >
                        🔄 One More?
                      </button>
                    )}
                    <button
                      onClick={handleBonusGotIt}
                      className={`w-full min-h-[48px] rounded-control border-2 border-ink shadow-hard-sm font-extrabold text-sm flex items-center justify-center gap-2 ${
                        bonusCorrect
                          ? 'bg-success text-white'
                          : 'bg-action text-white'
                      }`}
                    >
                      Back to Lesson →
                    </button>
                  </div>
                </div>
              )}
              </div>

              {/* Working pane for the bonus question (wide screens): part of the page while the
                  question is open; once answered it stays in view beside the result, under the header. */}
              <aside
                className={`hidden lg:block bg-white border-2 border-line rounded-card p-4 ${
                  bonusMode === 'result' ? 'lg:sticky lg:top-[84px] lg:max-h-[calc(100vh-100px)] lg:overflow-y-auto' : ''
                }`}
              >
                <WorkPane
                  key={bonusQuestion.id}
                  question={bonusQuestion}
                  stage={bonusMode === 'result' ? 'answered' : 'answering'}
                  mode="practice"
                  hintLevel={bonusHintLevel}
                  onHintLevelUp={openBonusHint}
                  onLessonBeforeAnswer={tookBonusLessonBeforeAnswer}
                  onLessonChange={onPaneLesson}
                />
              </aside>
            </div>
          )}
        </div>
      )}

      {/* ── Working space sheet (phones and tablets, before answering) ──
          Kept mounted while closed so pencil-pad working is still there when it opens again. */}
      {shownQuestion && !shownAnswered && (
        <div
          className={`lg:hidden fixed inset-0 z-[95] ${showWork ? 'flex flex-col justify-end' : 'hidden'}`}
          role="dialog"
          aria-modal="true"
          aria-label="Working space"
        >
          <div className="absolute inset-0 bg-ink/60" onClick={() => setShowWork(false)} aria-hidden="true" />
          <div className="relative w-full max-w-lg mx-auto max-h-[88vh] overflow-y-auto bg-white rounded-t-card border-2 border-b-0 border-ink px-4 pt-3 pb-8 animate-slide-up">
            <div className="flex justify-end mb-1">
              <button
                type="button"
                onClick={() => setShowWork(false)}
                aria-label="Close the working space"
                className="w-12 h-12 flex-shrink-0 rounded-tile bg-white border-2 border-line flex items-center justify-center text-ink font-bold text-lg hover:border-ink"
              >
                <span aria-hidden="true">✕</span>
              </button>
            </div>
            <WorkPane
              key={shownQuestion.id}
              question={shownQuestion}
              stage="answering"
              mode="practice"
              hintLevel={bonusShown ? bonusHintLevel : hintLevel}
              onHintLevelUp={bonusShown ? openBonusHint : openHint}
              onLessonBeforeAnswer={bonusShown ? tookBonusLessonBeforeAnswer : tookLessonBeforeAnswer}
              onLessonChange={onPaneLesson}
              active={showWork}
            />
          </div>
        </div>
      )}

      {/* ── Step player sheet (phones and tablets) ── */}
      {showSteps && shownQuestion && (
        <div
          className="lg:hidden fixed inset-0 z-[95] flex flex-col justify-end"
          role="dialog"
          aria-modal="true"
          aria-label="Step by step solution"
        >
          <div className="absolute inset-0 bg-ink/60" onClick={() => setShowSteps(false)} aria-hidden="true" />
          <div className="relative w-full max-w-lg mx-auto max-h-[88vh] overflow-y-auto bg-white rounded-t-card border-2 border-b-0 border-ink px-4 pt-3 pb-8 animate-slide-up">
            <div className="flex items-center justify-between gap-3 mb-3">
              <p className="font-display text-title text-ink">
                <span aria-hidden="true">📖</span> Step by step
              </p>
              <button
                type="button"
                autoFocus
                onClick={() => setShowSteps(false)}
                aria-label="Close the steps"
                className="w-12 h-12 flex-shrink-0 rounded-tile bg-white border-2 border-line flex items-center justify-center text-ink font-bold text-lg hover:border-ink"
              >
                <span aria-hidden="true">✕</span>
              </button>
            </div>
            <StepPlayer key={shownQuestion.id} question={shownQuestion} />
          </div>
        </div>
      )}

      {/* ── "Explain it to me" sheet (phones and tablets, after answering) ──
          Full height, built like the steps sheet. The lesson only exists while the
          sheet is open, so closing it stops the voice. */}
      {showTeach && shownQuestion && shownAnswered && (
        <div
          className="lg:hidden fixed inset-0 z-[95] flex flex-col justify-end"
          role="dialog"
          aria-modal="true"
          aria-label="Explain it to me"
        >
          <div className="absolute inset-0 bg-ink/60" onClick={() => setShowTeach(false)} aria-hidden="true" />
          <div className="relative w-full max-w-lg mx-auto h-[94vh] overflow-y-auto bg-white rounded-t-card border-2 border-b-0 border-ink px-4 pt-3 pb-8 animate-slide-up">
            <TeachPlayer
              key={shownQuestion.id}
              questionId={shownQuestion.id}
              onClose={() => setShowTeach(false)}
              closeLabel="Back to the question"
              fallback={<StepPlayer question={shownQuestion} />}
            />
          </div>
        </div>
      )}

      {/* ── The lesson from a `teach` link (every screen size) ──
          The session opened on a question the child asked Sparky to explain, so
          the lesson is already playing over it. Closing it (the cross, Escape, or
          the button at its end) brings up the offer of a similar question. The
          lesson only exists while this is open, so closing it stops the voice. */}
      {linked === 'lesson' && phase === 'answering' && (
        <div
          className="fixed inset-0 z-[95] flex flex-col justify-end lg:justify-center"
          role="dialog"
          aria-modal="true"
          aria-label="Explain it to me"
        >
          <div className="absolute inset-0 bg-ink/60" aria-hidden="true" />
          <div className="relative w-full max-w-lg mx-auto h-[94vh] overflow-y-auto bg-white rounded-t-card border-2 border-b-0 border-ink px-4 pt-3 pb-8 animate-slide-up lg:max-w-2xl lg:h-auto lg:max-h-[92vh] lg:rounded-card lg:border-b-2">
            <TeachPlayer
              key={currentQuestion.id}
              questionId={currentQuestion.id}
              onClose={() => setLinked('after')}
              closeLabel="Now let me try"
              fallback={<StepPlayer question={currentQuestion} />}
            />
          </div>
        </div>
      )}
    </div>
  );
}
