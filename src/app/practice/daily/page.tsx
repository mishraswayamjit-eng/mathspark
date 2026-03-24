'use client';

import { useEffect, useState, useCallback } from 'react';
import Link from 'next/link';
import QuestionCard from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import MisconceptionPopup from '@/components/MisconceptionPopup';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import StreakCounter from '@/components/progress/StreakCounter';
import { useSounds } from '@/hooks/useSounds';
import {
  loadTodaysChallenge,
  getCurrentMonthTheme,
  saveChallengeResult,
  getTodaysChallengeResult,
  type DailyChallenge,
  type ChallengeResult,
} from '@/lib/challenge-selector';
import {
  loadStreak,
  completeChallenge as completeStreakChallenge,
  getStreakMilestone,
  type StreakData,
} from '@/lib/streak';
import type { Question, AnswerKey, StepItem } from '@/types';

// ── Adapt JSON question → QuestionCard's Question type ───────────────────────

function adaptQuestion(
  cq: DailyChallenge['questions'][number],
  challengeId: string,
): Question {
  const opts = cq.options ?? [];
  return {
    id: cq.sourceId || `${challengeId}_Q${cq.questionNumber}`,
    topicId: cq.topicBucket ?? '',
    subTopic: cq.topicBucket ?? '',
    difficulty: 'Medium' as const,
    questionText: cq.questionText,
    questionLatex: '',
    option1: opts[0]?.text ?? '',
    option2: opts[1]?.text ?? '',
    option3: opts[2]?.text ?? '',
    option4: opts[3]?.text ?? '',
    correctAnswer: (cq.correctAnswer ?? 'A') as AnswerKey,
    hint1: cq.hints?.[0] ?? '',
    hint2: cq.hints?.[1] ?? '',
    hint3: cq.hints?.[2] ?? '',
    stepByStep: (cq.stepByStep ?? []).map((s) => ({
      step: s.step,
      text: s.text,
      latex: s.latex,
    })) as StepItem[],
    misconceptionA: '',
    misconceptionB: '',
    misconceptionC: '',
    misconceptionD: '',
    source: 'daily_challenge',
  };
}

// ── Score-based Sparky messages ──────────────────────────────────────────────

function scoreMessage(score: number, total: number): { text: string; emotion: 'happy' | 'celebrating' | 'encouraging' } {
  const pct = (score / total) * 100;
  if (pct === 100) return { text: 'PERFECT! You nailed every single one! 🌟', emotion: 'celebrating' };
  if (pct >= 80) return { text: 'Amazing work! You really know your stuff! 🎉', emotion: 'celebrating' };
  if (pct >= 60) return { text: 'Nice effort! Keep it up and you\'ll master this! 💪', emotion: 'happy' };
  if (pct >= 40) return { text: 'Good start! Every question you practice makes you stronger! 🌱', emotion: 'encouraging' };
  return { text: 'Keep going! Practice makes progress. Try again tomorrow! 💪', emotion: 'encouraging' };
}

// ── Main Component ───────────────────────────────────────────────────────────

export default function DailyChallengePage() {
  const { playCorrect, playWrong, playStreak, playLevelUp } = useSounds();

  // ── State ──────────────────────────────────────────────────────────────────
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [challenge, setChallenge] = useState<DailyChallenge | null>(null);
  const [monthTheme, setMonthTheme] = useState('');
  const [grade, setGrade] = useState(6);
  const [dataLoaded, setDataLoaded] = useState(false);

  // Quiz state
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [selected, setSelected] = useState<AnswerKey | null>(null);
  const [results, setResults] = useState<boolean[]>([]);
  const [hintLevel, setHintLevel] = useState(0);

  // Completion state
  const [phase, setPhase] = useState<'quiz' | 'done' | 'already'>('quiz');
  const [prevResult, setPrevResult] = useState<ChallengeResult | null>(null);
  const [streak, setStreak] = useState<StreakData | null>(null);
  const [showConfetti, setShowConfetti] = useState(false);
  const [newMilestone, setNewMilestone] = useState<string | null>(null);

  // ── Load data ──────────────────────────────────────────────────────────────
  useEffect(() => {
    let cancelled = false;

    async function init() {
      // 1. Determine student grade
      let studentGrade = 6;
      try {
        const res = await fetch('/api/student');
        if (res.ok) {
          const student = await res.json();
          if (student.grade) studentGrade = student.grade;
        }
      } catch { /* use default grade */ }

      if (cancelled) return;
      setGrade(studentGrade);

      // 2. Check if already completed today
      const existing = getTodaysChallengeResult();
      if (existing && existing.grade === studentGrade) {
        setPrevResult(existing);
        setStreak(loadStreak());
        setPhase('already');
        setDataLoaded(true);
        setLoading(false);
        return;
      }

      // 3. Fetch today's single challenge from API
      try {
        const resp = await loadTodaysChallenge(studentGrade);
        if (cancelled) return;
        if (resp) {
          setChallenge(resp.challenge);
          setMonthTheme(getCurrentMonthTheme(resp.meta));
        } else {
          setError(`No daily challenge available for Grade ${studentGrade}.`);
        }
      } catch {
        if (!cancelled) setError('Could not load daily challenges.');
      }

      if (!cancelled) {
        setStreak(loadStreak());
        setDataLoaded(true);
        setLoading(false);
      }
    }

    init();
    return () => { cancelled = true; };
  }, []);

  // ── Handlers ───────────────────────────────────────────────────────────────
  const handleAnswer = useCallback((key: AnswerKey, isCorrect: boolean) => {
    if (answered) return;
    setSelected(key);
    setAnswered(true);
    setResults((prev) => [...prev, isCorrect]);
    if (isCorrect) {
      playCorrect();
    } else {
      playWrong();
      setHintLevel(1);
    }
  }, [answered, playCorrect, playWrong]);

  const handleNext = useCallback(() => {
    if (!challenge) return;
    const nextIdx = currentIdx + 1;

    if (nextIdx >= challenge.questions.length) {
      // All questions done — calculate score
      const finalResults = results;
      const score = finalResults.filter(Boolean).length;
      const total = challenge.questions.length;

      // Update streak
      const updatedStreak = completeStreakChallenge();
      setStreak(updatedStreak);

      // Check milestone
      const milestone = getStreakMilestone(updatedStreak.currentStreak);
      if (milestone) setNewMilestone(milestone);

      // Save result
      saveChallengeResult({
        date: new Date().toISOString().slice(0, 10),
        grade,
        challengeId: challenge.challengeId,
        score,
        total,
      });

      // Celebration
      if (score >= 4) {
        setShowConfetti(true);
        playLevelUp();
      } else if (score >= 3) {
        playStreak();
      }

      setPhase('done');
    } else {
      setCurrentIdx(nextIdx);
      setAnswered(false);
      setSelected(null);
      setHintLevel(0);
    }
  }, [challenge, currentIdx, results, grade, playLevelUp, playStreak]);

  // ── Loading / Error states ─────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-4">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-gray-500 animate-pulse">
          Loading today&apos;s challenge...
        </p>
      </div>
    );
  }

  if (error || (!challenge && dataLoaded && phase === 'quiz')) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-4">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm text-red-500 font-bold">{error || 'Something went wrong.'}</p>
        <button onClick={() => window.location.reload()} className="bg-duo-blue text-white font-extrabold rounded-2xl px-6 py-2.5 text-sm active:scale-95 transition-transform">Retry</button>
        <Link href="/home" className="text-sm text-gray-500 font-semibold">Go Home</Link>
      </div>
    );
  }

  // ── Already completed today ────────────────────────────────────────────────
  if (phase === 'already' && prevResult) {
    return (
      <div className="min-h-screen flex flex-col items-center px-6 py-8 gap-6 max-w-lg mx-auto">
        <div className="text-center space-y-2">
          <div className="text-5xl">✅</div>
          <h1 className="text-xl font-extrabold text-gray-800">
            Today&apos;s Challenge Complete!
          </h1>
          <p className="text-sm text-gray-500">
            You scored <span className="font-extrabold text-duo-green">{prevResult.score}/{prevResult.total}</span>
          </p>
        </div>

        {streak && <StreakCounter streak={streak} />}

        <div className="bg-purple-50 rounded-2xl px-4 py-3 flex items-start gap-3 border border-purple-200">
          <Sparky mood="happy" size={40} />
          <p className="text-sm font-semibold text-purple-800 pt-1">
            Come back tomorrow for a fresh challenge! 🌟
          </p>
        </div>

        {monthTheme && (
          <div className="bg-blue-50 rounded-full px-4 py-1.5 border border-blue-200">
            <span className="text-xs font-bold text-blue-600">{monthTheme}</span>
          </div>
        )}

        <div className="flex flex-col gap-3 w-full mt-2">
          <Link
            href="/home"
            className="w-full bg-duo-green hover:bg-duo-green-dark text-white font-extrabold py-3.5 rounded-2xl text-center transition-colors"
          >
            Back to Home
          </Link>
          <Link
            href="/practice"
            className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-3 rounded-2xl text-center transition-colors"
          >
            Practice More →
          </Link>
        </div>
      </div>
    );
  }

  // ── Done screen (just completed) ──────────────────────────────────────────
  if (phase === 'done') {
    const score = results.filter(Boolean).length;
    const total = challenge?.questions.length ?? 5;
    const { text: sparkyText, emotion } = scoreMessage(score, total);

    return (
      <div className="min-h-screen flex flex-col items-center px-6 py-8 gap-5 max-w-lg mx-auto">
        {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

        {/* Score */}
        <div className="text-center space-y-2 mt-4">
          <div className="text-6xl font-extrabold" style={{ color: score >= 3 ? '#58CC02' : '#FF9600' }}>
            {score}/{total}
          </div>
          <p className="text-sm font-bold text-gray-500">
            {score === total ? 'Perfect Score!' : `${score} correct`}
          </p>
        </div>

        {/* Milestone */}
        {newMilestone && (
          <div className="bg-gradient-to-r from-yellow-100 to-orange-100 rounded-2xl px-5 py-3 border-2 border-yellow-300 text-center">
            <p className="text-lg font-extrabold text-orange-700">{newMilestone}</p>
            <p className="text-xs font-bold text-orange-500 mt-0.5">New Milestone Unlocked!</p>
          </div>
        )}

        {/* Streak */}
        {streak && <StreakCounter streak={streak} />}

        {/* Sparky */}
        <div className="bg-purple-50 rounded-2xl px-4 py-3 flex items-start gap-3 border border-purple-200 w-full">
          <Sparky mood={emotion === 'celebrating' ? 'celebrating' : emotion === 'happy' ? 'happy' : 'encouraging'} size={40} />
          <p className="text-sm font-semibold text-purple-800 pt-1">{sparkyText}</p>
        </div>

        {/* Fun fact */}
        {challenge?.funFact && (
          <div className="bg-blue-50 rounded-2xl px-4 py-3 border border-blue-200 w-full">
            <p className="text-xs font-bold text-blue-500 mb-1">💡 Fun Fact</p>
            <p className="text-sm text-blue-800">{challenge.funFact}</p>
          </div>
        )}

        {/* Result dots */}
        <div className="flex gap-2 justify-center">
          {results.map((correct, i) => (
            <div
              key={i}
              className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-xs ${
                correct ? 'bg-duo-green' : 'bg-duo-red'
              }`}
            >
              {correct ? '✓' : '✗'}
            </div>
          ))}
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-3 w-full mt-2">
          <Link
            href="/home"
            className="w-full bg-duo-green hover:bg-duo-green-dark text-white font-extrabold py-3.5 rounded-2xl text-center transition-colors"
          >
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  // ── Quiz in progress ──────────────────────────────────────────────────────
  if (!challenge) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-4">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm text-gray-500 font-bold">
          No challenge found for Grade {grade} today.
        </p>
        <Link href="/home" className="text-sm text-blue-500 underline">Go Home</Link>
      </div>
    );
  }

  const currentQuestion = challenge.questions[currentIdx];
  const adaptedQuestion = adaptQuestion(currentQuestion, challenge.challengeId);
  const totalQ = challenge.questions.length;
  const progressPct = ((currentIdx + (answered ? 1 : 0)) / totalQ) * 100;

  return (
    <div className="min-h-screen flex flex-col px-4 py-6 max-w-lg mx-auto pb-28 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xl">🎯</span>
          <h1 className="text-lg font-extrabold text-gray-800">Daily Challenge</h1>
        </div>
        {streak && <StreakCounter streak={streak} compact />}
      </div>

      {/* Month theme */}
      {monthTheme && (
        <div className="bg-blue-50 rounded-full px-3 py-1 border border-blue-200 self-start mb-4">
          <span className="text-xs font-bold text-blue-600">{monthTheme}</span>
        </div>
      )}

      {/* Progress bar */}
      <div className="w-full bg-gray-200 rounded-full h-2.5 mb-5 overflow-hidden">
        <div
          className="bg-duo-green h-2.5 rounded-full transition-[width] duration-500 ease-out"
          style={{ width: `${progressPct}%` }}
        />
      </div>

      {/* Question counter */}
      <p className="text-xs font-bold text-gray-500 mb-3 text-center">
        Question {currentIdx + 1} of {totalQ}
      </p>

      {/* Question card */}
      <QuestionCard
        question={adaptedQuestion}
        answered={answered}
        selected={selected}
        onAnswer={handleAnswer}
      />

      {/* Feedback after answer */}
      {answered && (
        <div className="mt-4 space-y-3">
          {/* Correct/wrong message */}
          <div className={`rounded-2xl px-4 py-3 flex items-start gap-3 border ${
            selected === adaptedQuestion.correctAnswer
              ? 'bg-green-50 border-green-200'
              : 'bg-red-50 border-red-200'
          }`}>
            <Sparky
              mood={selected === adaptedQuestion.correctAnswer ? 'celebrating' : 'encouraging'}
              size={36}
            />
            <p className={`text-sm font-semibold pt-1 ${
              selected === adaptedQuestion.correctAnswer ? 'text-green-700' : 'text-red-700'
            }`}>
              {selected === adaptedQuestion.correctAnswer
                ? ['Great job! ⭐', 'You got it! 🎯', 'Excellent! 🧠', 'Well done! 🌟', 'Awesome! 🎉'][
                    Math.floor(Math.random() * 5)
                  ]
                : "Not quite — let's look at the solution!"}
            </p>
          </div>

          {/* Misconception (for wrong answers) */}
          {selected && selected !== adaptedQuestion.correctAnswer && (() => {
            const misconKey = `misconception${selected}` as keyof typeof adaptedQuestion;
            const misconText = adaptedQuestion[misconKey] as string;
            const correctIdx = ['A', 'B', 'C', 'D'].indexOf(adaptedQuestion.correctAnswer);
            const correctText = adaptedQuestion[`option${correctIdx + 1}` as keyof typeof adaptedQuestion] as string;
            return misconText ? (
              <MisconceptionPopup
                text={misconText}
                correctAnswer={adaptedQuestion.correctAnswer}
                correctText={correctText}
              />
            ) : null;
          })()}

          {/* Hints (for wrong answers) */}
          {hintLevel > 0 && (
            <HintSystem
              hint1={adaptedQuestion.hint1}
              hint2={adaptedQuestion.hint2}
              hint3={adaptedQuestion.hint3}
              level={hintLevel}
              onLevelUp={setHintLevel}
            />
          )}

          {/* Step by step solution */}
          {adaptedQuestion.stepByStep.length > 0 && (
            <StepByStep steps={adaptedQuestion.stepByStep} />
          )}

          {/* Next button */}
          <button
            onClick={handleNext}
            className="w-full bg-duo-blue hover:bg-[#0a8fd4] text-white font-extrabold py-3.5 rounded-2xl transition-colors mt-2"
          >
            {currentIdx + 1 >= totalQ ? 'See Results →' : 'Next →'}
          </button>
        </div>
      )}
    </div>
  );
}
