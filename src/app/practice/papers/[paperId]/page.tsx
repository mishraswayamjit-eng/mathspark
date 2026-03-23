'use client';

import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import KatexRenderer from '@/components/KatexRenderer';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import MisconceptionPopup from '@/components/MisconceptionPopup';
import StepByStep from '@/components/StepByStep';
import { useSounds } from '@/hooks/useSounds';
import { calculateScore, getVerdict, type ScoreResult } from '@/lib/scoring';
import { detectMistakes, type MistakePattern, type DetectedMistake, type WrongAnswer } from '@/lib/mistake-detector';

// ── Types ────────────────────────────────────────────────────────────────────

interface PaperQuestion {
  questionNumber: number;
  difficulty: string;
  sourceId: string;
  questionText: string;
  questionLatex: string;
  options: Array<{ id: string; text: string }>;
  correctAnswer: string;
  grade: number;
  subTopic: string;
  topicBucket: string;
  hints: string[];
  stepByStep: Array<{ step: number; text: string; latex: string }>;
  misconceptions: Record<string, string>;
  timeEstimateSeconds: number;
}

interface Paper {
  paperId: string;
  title: string;
  grade: number;
  duration: number;
  totalQuestions: number;
  totalMarks: number;
  instructions: {
    examName: string;
    subtitle: string;
    duration: string;
    totalQuestions: number;
    totalMarks: number;
    rules: string[];
  };
  markingScheme: {
    correct: string;
    wrong: string;
    unanswered: string;
    negativeMarking: boolean;
    maxMarks: number;
    passingMarks: number;
  };
  questions: PaperQuestion[];
  answerKey: Record<string, string>;
  simulatorMetadata: {
    uiFeatures: {
      countdownTimer: boolean;
      questionNavigator: boolean;
      markForReview: boolean;
      questionPalette: Record<string, string>;
      autoSubmitOnTimeout: boolean;
      warningAt: number[];
    };
    analyticsTemplate: {
      sparkyVerdict: Record<string, string>;
    };
  };
}

type Phase = 'loading' | 'instructions' | 'exam' | 'results';

interface ResponseState {
  answer: string | null;
  flagged: boolean;
  timeSpentMs: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function hasLatex(text: string): boolean {
  return text.includes('\\');
}

function formatTime(ms: number): string {
  const totalSec = Math.floor(ms / 1000);
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function formatMs(ms: number): string {
  const s = Math.floor(ms / 1000);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  const rem = s % 60;
  return rem > 0 ? `${m}m ${rem}s` : `${m}m`;
}

// ── Page ─────────────────────────────────────────────────────────────────────

export default function ExamSimulatorPage() {
  const { paperId } = useParams<{ paperId: string }>();
  const { playLevelUp } = useSounds();

  // Core state
  const [phase, setPhase] = useState<Phase>('loading');
  const [paper, setPaper] = useState<Paper | null>(null);
  const [error, setError] = useState('');

  // Exam state
  const [currentQ, setCurrentQ] = useState(0);
  const [responses, setResponses] = useState<ResponseState[]>([]);
  const [startTime, setStartTime] = useState<number>(0);
  const [remaining, setRemaining] = useState<number>(0);
  const [showNav, setShowNav] = useState(false);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [warning, setWarning] = useState('');
  const questionStartRef = useRef<number>(Date.now());

  // Results state
  const [scoreResult, setScoreResult] = useState<ScoreResult | null>(null);
  const [mistakes, setMistakes] = useState<DetectedMistake[]>([]);
  const [showConfetti, setShowConfetti] = useState(false);
  const [resultsTab, setResultsTab] = useState<'score' | 'topics' | 'difficulty' | 'time' | 'mistakes'>('score');
  const [reviewQ, setReviewQ] = useState<number | null>(null);

  // ── Load paper ─────────────────────────────────────────────────────────────
  useEffect(() => {
    fetch(`/api/papers/${paperId}`)
      .then((r) => {
        if (!r.ok) throw new Error('Paper not found');
        return r.json();
      })
      .then((d) => {
        setPaper(d.paper);
        setPhase('instructions');
      })
      .catch(() => setError('Could not load exam paper.'));
  }, [paperId]);

  // ── Timer ──────────────────────────────────────────────────────────────────
  useEffect(() => {
    if (phase !== 'exam' || !paper) return;
    const id = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const left = Math.max(0, paper.duration * 60 * 1000 - elapsed);
      setRemaining(left);

      // Warnings at threshold minutes (show for ~5 seconds)
      const secsLeft = Math.floor(left / 1000);
      if (secsLeft === 60)     setWarning('⚠️ 1 minute remaining!');
      else if (secsLeft === 55) setWarning('');
      else if (secsLeft === 5 * 60)  setWarning('⏰ 5 minutes remaining');
      else if (secsLeft === 5 * 60 - 5) setWarning('');
      else if (secsLeft === 10 * 60) setWarning('⏰ 10 minutes remaining');
      else if (secsLeft === 10 * 60 - 5) setWarning('');

      // Auto-submit on timeout
      if (left === 0) {
        clearInterval(id);
        handleSubmit();
      }
    }, 1000);
    return () => clearInterval(id);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase, startTime, paper]);

  // ── Start exam ─────────────────────────────────────────────────────────────
  const startExam = useCallback(() => {
    if (!paper) return;
    setResponses(
      paper.questions.map(() => ({ answer: null, flagged: false, timeSpentMs: 0 })),
    );
    setStartTime(Date.now());
    setRemaining(paper.duration * 60 * 1000);
    questionStartRef.current = Date.now();
    setCurrentQ(0);
    setPhase('exam');
  }, [paper]);

  // ── Answer selection ───────────────────────────────────────────────────────
  const selectAnswer = useCallback((optionId: string | null) => {
    setResponses((prev) => {
      const next = [...prev];
      next[currentQ] = { ...next[currentQ], answer: optionId };
      return next;
    });
  }, [currentQ]);

  // ── Navigation ─────────────────────────────────────────────────────────────
  const goToQuestion = useCallback((idx: number) => {
    // Record time on current question
    const elapsed = Date.now() - questionStartRef.current;
    setResponses((prev) => {
      const next = [...prev];
      next[currentQ] = { ...next[currentQ], timeSpentMs: next[currentQ].timeSpentMs + elapsed };
      return next;
    });
    setCurrentQ(idx);
    questionStartRef.current = Date.now();
  }, [currentQ]);

  const toggleFlag = useCallback(() => {
    setResponses((prev) => {
      const next = [...prev];
      next[currentQ] = { ...next[currentQ], flagged: !next[currentQ].flagged };
      return next;
    });
  }, [currentQ]);

  // ── Submit ─────────────────────────────────────────────────────────────────
  const handleSubmit = useCallback(() => {
    if (!paper) return;

    // Record final question time
    const elapsed = Date.now() - questionStartRef.current;
    const finalResponses = responses.map((r, i) =>
      i === currentQ ? { ...r, timeSpentMs: r.timeSpentMs + elapsed } : r,
    );
    setResponses(finalResponses);

    // Build answers map
    const answersMap: Record<string, string> = {};
    finalResponses.forEach((r, i) => {
      if (r.answer) {
        answersMap[String(i + 1)] = r.answer;
      }
    });

    // Calculate score
    const result = calculateScore(
      answersMap,
      paper.answerKey,
      paper.markingScheme.negativeMarking,
      paper.markingScheme.maxMarks,
    );
    setScoreResult(result);

    // Detect mistake patterns
    const wrongAnswers: WrongAnswer[] = [];
    finalResponses.forEach((r, i) => {
      if (r.answer && r.answer !== paper.answerKey[String(i + 1)]) {
        const q = paper.questions[i];
        wrongAnswers.push({
          questionNumber: i + 1,
          chosenOption: r.answer,
          correctOption: paper.answerKey[String(i + 1)],
          misconceptionText: q.misconceptions?.[r.answer] ?? '',
          topicBucket: q.topicBucket ?? '',
        });
      }
    });

    // Load mistake patterns and detect
    fetch('/api/mistake-patterns')
      .then((r) => r.ok ? r.json() : { patterns: [] })
      .then((d) => {
        const patterns = (d.patterns ?? []) as MistakePattern[];
        setMistakes(detectMistakes(wrongAnswers, patterns, paper.grade));
      })
      .catch(() => {});

    // Celebration
    if (result.percentage >= 80) {
      setShowConfetti(true);
      playLevelUp();
    }

    setShowSubmitModal(false);
    setPhase('results');
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [paper, responses, currentQ]);

  // ── Computed values ────────────────────────────────────────────────────────
  const answeredCount = responses.filter((r) => r.answer).length;
  const flaggedCount = responses.filter((r) => r.flagged).length;

  // Timer color
  const timerColor = remaining < 60000 ? '#FF4B4B'
    : remaining < 5 * 60000 ? '#FF9600'
    : '#ffffff';

  // ── LOADING ────────────────────────────────────────────────────────────────
  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-4">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm text-red-500 font-bold">{error}</p>
        <Link href="/practice/papers" className="text-sm text-blue-500 underline">Back to Papers</Link>
      </div>
    );
  }

  if (phase === 'loading' || !paper) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-6 gap-4">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-gray-500 animate-pulse">Loading exam paper...</p>
      </div>
    );
  }

  // ── INSTRUCTIONS ───────────────────────────────────────────────────────────
  if (phase === 'instructions') {
    return (
      <div className="min-h-screen flex flex-col items-center px-6 py-8 max-w-lg mx-auto">
        <Sparky mood="happy" size={72} />
        <h1 className="text-xl font-extrabold text-gray-800 mt-4 text-center">
          {paper.instructions.examName}
        </h1>
        <p className="text-sm text-gray-500 font-medium mt-1">{paper.instructions.subtitle}</p>

        {/* Stats grid */}
        <div className="grid grid-cols-3 gap-3 w-full mt-6">
          <div className="bg-blue-50 rounded-2xl p-3 text-center border border-blue-100">
            <p className="text-2xl font-extrabold text-duo-blue">{paper.totalQuestions}</p>
            <p className="text-[10px] font-bold text-blue-600">Questions</p>
          </div>
          <div className="bg-orange-50 rounded-2xl p-3 text-center border border-orange-100">
            <p className="text-2xl font-extrabold text-duo-orange">{paper.duration}</p>
            <p className="text-[10px] font-bold text-orange-600">Minutes</p>
          </div>
          <div className="bg-green-50 rounded-2xl p-3 text-center border border-green-100">
            <p className="text-2xl font-extrabold text-duo-green">{paper.totalMarks}</p>
            <p className="text-[10px] font-bold text-green-600">Marks</p>
          </div>
        </div>

        {/* Marking scheme */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm w-full mt-4">
          <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide mb-2">Marking Scheme</p>
          <div className="space-y-1.5 text-sm">
            <p className="flex justify-between"><span className="text-gray-600">Correct</span><span className="font-bold text-duo-green">{paper.markingScheme.correct}</span></p>
            <p className="flex justify-between"><span className="text-gray-600">Wrong</span><span className="font-bold text-duo-red">{paper.markingScheme.wrong}</span></p>
            <p className="flex justify-between"><span className="text-gray-600">Unanswered</span><span className="font-bold text-gray-400">{paper.markingScheme.unanswered}</span></p>
            <p className="flex justify-between"><span className="text-gray-600">Passing</span><span className="font-bold text-gray-800">{paper.markingScheme.passingMarks}/{paper.markingScheme.maxMarks}</span></p>
          </div>
        </div>

        {/* Rules */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm w-full mt-3">
          <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide mb-2">Rules</p>
          <ul className="space-y-1.5">
            {paper.instructions.rules.map((rule, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-600">
                <span className="text-gray-400 shrink-0">•</span>
                <span>{rule}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Negative marking warning */}
        {paper.markingScheme.negativeMarking && (
          <div className="bg-red-50 border border-red-200 rounded-2xl px-4 py-3 w-full mt-3 flex items-start gap-2">
            <span className="text-lg shrink-0">⚠️</span>
            <p className="text-xs text-red-700 font-semibold">
              This paper has negative marking (-0.25 per wrong answer). Leave questions blank if unsure.
            </p>
          </div>
        )}

        {/* Start button */}
        <button
          onClick={startExam}
          className="w-full bg-duo-green hover:bg-duo-green-dark text-white font-extrabold py-4 rounded-2xl text-lg mt-6 transition-colors shadow-md active:scale-[0.98]"
        >
          Start Exam →
        </button>

        <Link href="/practice/papers" className="text-sm text-gray-400 font-bold mt-3 hover:text-gray-600">
          ← Back to papers
        </Link>
      </div>
    );
  }

  // ── RESULTS ────────────────────────────────────────────────────────────────
  if (phase === 'results' && scoreResult) {
    const verdict = getVerdict(scoreResult.percentage);
    const passed = scoreResult.netScore >= (paper.markingScheme.passingMarks ?? 0);

    // Topic breakdown
    const topicMap = new Map<string, { correct: number; total: number; timeMs: number }>();
    responses.forEach((r, i) => {
      const q = paper.questions[i];
      const bucket = q.topicBucket || q.subTopic || 'other';
      if (!topicMap.has(bucket)) topicMap.set(bucket, { correct: 0, total: 0, timeMs: 0 });
      const entry = topicMap.get(bucket)!;
      entry.total++;
      entry.timeMs += r.timeSpentMs;
      if (r.answer === paper.answerKey[String(i + 1)]) entry.correct++;
    });
    const topicResults = Array.from(topicMap.entries())
      .map(([topic, d]) => ({ topic, ...d, pct: Math.round((d.correct / d.total) * 100) }))
      .sort((a, b) => a.pct - b.pct);

    // Difficulty breakdown
    const diffMap = new Map<string, { correct: number; total: number }>();
    responses.forEach((r, i) => {
      const diff = paper.questions[i].difficulty;
      if (!diffMap.has(diff)) diffMap.set(diff, { correct: 0, total: 0 });
      const entry = diffMap.get(diff)!;
      entry.total++;
      if (r.answer === paper.answerKey[String(i + 1)]) entry.correct++;
    });

    // Time analysis
    const avgTimeMs = responses.reduce((s, r) => s + r.timeSpentMs, 0) / responses.length;
    const slowest = responses
      .map((r, i) => ({ idx: i, time: r.timeSpentMs }))
      .sort((a, b) => b.time - a.time)
      .slice(0, 3);

    // Question under review
    const reviewQuestion = reviewQ !== null ? paper.questions[reviewQ] : null;
    const reviewResponse = reviewQ !== null ? responses[reviewQ] : null;

    return (
      <div className="min-h-screen bg-gray-50 pb-24">
        {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

        {/* Header */}
        <div className="bg-duo-dark px-4 py-4">
          <div className="max-w-lg mx-auto flex items-center justify-between">
            <h1 className="text-white font-extrabold text-lg">Exam Results</h1>
            <Link href="/practice/papers" className="text-white/60 text-sm font-bold hover:text-white">
              ← Papers
            </Link>
          </div>
        </div>

        <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">
          {/* Score card */}
          <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm text-center">
            <div className="flex items-center justify-center gap-3 mb-3">
              <Sparky mood={verdict.sparkyMood} size={52} />
              <div>
                <p className={`text-4xl font-extrabold ${passed ? 'text-duo-green' : 'text-duo-orange'}`}>
                  {scoreResult.netScore.toFixed(scoreResult.negativeDeduction > 0 ? 2 : 0)}/{scoreResult.maxMarks}
                </p>
                <p className="text-sm font-bold text-gray-500">{scoreResult.percentage}%</p>
              </div>
            </div>
            <p className={`text-sm font-extrabold ${passed ? 'text-duo-green' : 'text-duo-red'}`}>
              {passed ? 'PASSED' : 'NOT PASSED'} — {verdict.label}
            </p>

            {/* Quick stats */}
            <div className="grid grid-cols-3 gap-2 mt-4">
              <div className="bg-green-50 rounded-xl px-2 py-2">
                <p className="text-lg font-extrabold text-duo-green">{scoreResult.correct}</p>
                <p className="text-[10px] font-bold text-green-600">Correct</p>
              </div>
              <div className="bg-red-50 rounded-xl px-2 py-2">
                <p className="text-lg font-extrabold text-duo-red">{scoreResult.wrong}</p>
                <p className="text-[10px] font-bold text-red-600">Wrong</p>
              </div>
              <div className="bg-gray-50 rounded-xl px-2 py-2">
                <p className="text-lg font-extrabold text-gray-500">{scoreResult.skipped}</p>
                <p className="text-[10px] font-bold text-gray-400">Skipped</p>
              </div>
            </div>

            {/* Negative marking impact */}
            {scoreResult.negativeDeduction > 0 && (
              <p className="text-xs font-bold text-duo-red mt-3">
                -{scoreResult.negativeDeduction.toFixed(2)} from negative marking
              </p>
            )}
          </div>

          {/* Tabs */}
          <div className="flex gap-1 bg-gray-100 rounded-full p-1 overflow-x-auto">
            {([
              { key: 'score', label: 'Overview' },
              { key: 'topics', label: 'Topics' },
              { key: 'difficulty', label: 'Difficulty' },
              { key: 'time', label: 'Time' },
              { key: 'mistakes', label: 'Mistakes' },
            ] as const).map((tab) => (
              <button
                key={tab.key}
                onClick={() => setResultsTab(tab.key)}
                className={`flex-1 px-3 py-2 rounded-full text-xs font-extrabold transition-colors whitespace-nowrap ${
                  resultsTab === tab.key
                    ? 'bg-white text-gray-800 shadow-sm'
                    : 'text-gray-500'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab content */}
          {resultsTab === 'score' && (
            <div className="space-y-3">
              {/* Question dots */}
              <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
                <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide mb-3">Question Results</p>
                <div className="flex flex-wrap gap-1.5">
                  {responses.map((r, i) => {
                    const isCorrect = r.answer === paper.answerKey[String(i + 1)];
                    const isSkipped = !r.answer;
                    return (
                      <button
                        key={i}
                        onClick={() => setReviewQ(reviewQ === i ? null : i)}
                        className={`w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-extrabold transition-[background-color,transform] ${
                          reviewQ === i ? 'ring-2 ring-blue-400 scale-110' :
                          isSkipped ? 'bg-gray-100 text-gray-400' :
                          isCorrect ? 'bg-duo-green text-white' :
                          'bg-duo-red text-white'
                        }`}
                      >
                        {i + 1}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Review selected question */}
              {reviewQuestion && reviewResponse && reviewQ !== null && (
                <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm space-y-3 animate-fade-in">
                  <p className="text-xs font-extrabold text-gray-500">Q{reviewQ + 1} Review</p>
                  <p className="text-sm font-bold text-gray-800">{reviewQuestion.questionText}</p>
                  <div className="space-y-1.5">
                    {reviewQuestion.options.map((opt) => {
                      const isCorrect = opt.id === reviewQuestion.correctAnswer;
                      const isSelected = opt.id === reviewResponse.answer;
                      return (
                        <div
                          key={opt.id}
                          className={`flex items-center gap-2 px-3 py-2 rounded-xl text-sm ${
                            isCorrect ? 'bg-green-50 border border-green-200' :
                            isSelected ? 'bg-red-50 border border-red-200' :
                            'bg-gray-50'
                          }`}
                        >
                          <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-extrabold ${
                            isCorrect ? 'bg-duo-green text-white' :
                            isSelected ? 'bg-duo-red text-white' :
                            'bg-gray-200 text-gray-500'
                          }`}>
                            {isCorrect ? '✓' : isSelected ? '✗' : opt.id}
                          </span>
                          <span className="text-gray-700 font-medium">
                            {hasLatex(opt.text) ? <KatexRenderer latex={opt.text} displayMode={false} /> : opt.text}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                  {/* Misconception */}
                  {reviewResponse.answer && reviewResponse.answer !== reviewQuestion.correctAnswer && reviewQuestion.misconceptions?.[reviewResponse.answer] && (
                    <MisconceptionPopup
                      text={reviewQuestion.misconceptions[reviewResponse.answer]}
                      correctAnswer={reviewQuestion.correctAnswer}
                      correctText={reviewQuestion.options.find((o) => o.id === reviewQuestion.correctAnswer)?.text ?? ''}
                    />
                  )}
                  {/* Step by step */}
                  {reviewQuestion.stepByStep?.length > 0 && (
                    <StepByStep steps={reviewQuestion.stepByStep} />
                  )}
                </div>
              )}
            </div>
          )}

          {resultsTab === 'topics' && (
            <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm space-y-3">
              <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">Topic Accuracy</p>
              {topicResults.map((t) => (
                <div key={t.topic} className="space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-gray-700 truncate max-w-[200px]">{t.topic}</span>
                    <span className="text-xs font-extrabold" style={{ color: t.pct >= 70 ? '#58CC02' : t.pct >= 40 ? '#FF9600' : '#FF4B4B' }}>
                      {t.correct}/{t.total} ({t.pct}%)
                    </span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-[width]"
                      style={{
                        width: `${t.pct}%`,
                        backgroundColor: t.pct >= 70 ? '#58CC02' : t.pct >= 40 ? '#FF9600' : '#FF4B4B',
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}

          {resultsTab === 'difficulty' && (
            <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm space-y-3">
              <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">Difficulty Breakdown</p>
              {['Easy', 'Medium', 'Hard'].map((diff) => {
                const d = diffMap.get(diff);
                if (!d) return null;
                const pct = Math.round((d.correct / d.total) * 100);
                const color = diff === 'Easy' ? '#58CC02' : diff === 'Medium' ? '#FF9600' : '#FF4B4B';
                return (
                  <div key={diff} className="flex items-center gap-3">
                    <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: color }} />
                    <span className="text-sm font-bold text-gray-700 w-16">{diff}</span>
                    <div className="flex-1 h-2.5 bg-gray-100 rounded-full overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${pct}%`, backgroundColor: color }} />
                    </div>
                    <span className="text-xs font-extrabold w-16 text-right" style={{ color }}>
                      {d.correct}/{d.total}
                    </span>
                  </div>
                );
              })}
            </div>
          )}

          {resultsTab === 'time' && (
            <div className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm space-y-3">
              <p className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">Time Analysis</p>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-blue-50 rounded-xl p-3 text-center">
                  <p className="text-lg font-extrabold text-duo-blue">{formatMs(avgTimeMs)}</p>
                  <p className="text-[10px] font-bold text-blue-600">Avg per question</p>
                </div>
                <div className="bg-orange-50 rounded-xl p-3 text-center">
                  <p className="text-lg font-extrabold text-duo-orange">
                    {formatMs(responses.reduce((s, r) => s + r.timeSpentMs, 0))}
                  </p>
                  <p className="text-[10px] font-bold text-orange-600">Total time</p>
                </div>
              </div>
              <p className="text-xs font-extrabold text-gray-500 mt-3">Slowest Questions</p>
              {slowest.map((s) => (
                <div key={s.idx} className="flex items-center justify-between py-1.5">
                  <span className="text-sm font-bold text-gray-700">Q{s.idx + 1}</span>
                  <span className="text-xs font-extrabold text-duo-orange">{formatMs(s.time)}</span>
                </div>
              ))}
            </div>
          )}

          {resultsTab === 'mistakes' && (
            <div className="space-y-3">
              {mistakes.length === 0 ? (
                <div className="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm text-center">
                  <Sparky mood="celebrating" size={48} />
                  <p className="text-sm font-bold text-gray-500 mt-2">
                    {scoreResult.wrong === 0 ? 'Perfect — no mistakes!' : 'No common patterns detected. Keep practicing!'}
                  </p>
                </div>
              ) : (
                mistakes.slice(0, 5).map((m) => (
                  <div key={m.patternId} className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xl">{m.emoji}</span>
                      <div>
                        <p className="text-sm font-extrabold text-gray-800">{m.patternName}</p>
                        <p className="text-[10px] font-bold text-gray-400 uppercase">{m.category.replace(/_/g, ' ')}</p>
                      </div>
                      <span className="ml-auto bg-red-50 text-duo-red text-xs font-extrabold px-2 py-0.5 rounded-full">
                        {m.occurrences}x
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 font-medium">{m.sparkyMessage}</p>
                    <p className="text-xs text-duo-blue font-bold mt-1">💡 {m.howToFix}</p>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-col gap-3 pt-2">
            <button
              onClick={() => { setPhase('instructions'); setReviewQ(null); setResultsTab('score'); }}
              className="w-full bg-duo-blue hover:bg-[#0a8fd4] text-white font-extrabold py-3.5 rounded-2xl transition-colors"
            >
              Retry This Paper
            </button>
            <Link
              href="/practice/papers"
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold py-3 rounded-2xl text-center transition-colors"
            >
              Browse More Papers →
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // ── EXAM ───────────────────────────────────────────────────────────────────
  const question = paper.questions[currentQ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col animate-fade-in">
      {/* Timer bar */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-3 flex items-center justify-between shadow-md">
        <div className="flex items-center gap-3">
          <span className="text-white text-sm font-extrabold">
            Q{currentQ + 1}/{paper.totalQuestions}
          </span>
          <span className="text-xs font-bold text-white/40">
            {answeredCount} answered
          </span>
        </div>

        {/* Timer */}
        <div className="flex items-center gap-2">
          <span className="text-sm font-extrabold" style={{ color: timerColor }}>
            ⏱ {formatTime(remaining)}
          </span>
        </div>

        {/* Navigator toggle */}
        <button
          onClick={() => setShowNav(true)}
          className="bg-white/10 text-white text-xs font-extrabold px-3 py-1.5 rounded-full hover:bg-white/20 transition-colors"
        >
          #{currentQ + 1} ▼
        </button>
      </div>

      {/* Warning banner */}
      {warning && (
        <div className="bg-duo-orange px-4 py-2 text-center">
          <p className="text-white text-xs font-extrabold">{warning}</p>
        </div>
      )}

      {/* Progress bar */}
      <div className="h-1 bg-gray-200">
        <div
          className="h-full bg-duo-green transition-[width] duration-300"
          style={{ width: `${(answeredCount / paper.totalQuestions) * 100}%` }}
        />
      </div>

      {/* Question content */}
      <div className="flex-1 max-w-lg mx-auto w-full px-4 py-5 space-y-4 pb-32">
        {/* Difficulty + topic */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className={`text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full ${
            question.difficulty === 'Easy' ? 'bg-green-50 text-duo-green' :
            question.difficulty === 'Hard' ? 'bg-red-50 text-duo-red' :
            'bg-amber-50 text-duo-orange'
          }`}>
            {question.difficulty}
          </span>
          <span className="text-[10px] font-semibold text-gray-400 truncate">{question.subTopic}</span>
          {responses[currentQ]?.flagged && (
            <span className="text-[10px] font-extrabold text-duo-orange bg-orange-50 px-2 py-0.5 rounded-full">🚩 Flagged</span>
          )}
        </div>

        {/* Question text */}
        <div className="bg-white rounded-2xl p-5 shadow-md border border-gray-100">
          <div className="text-[18px] font-bold text-gray-800 leading-relaxed">
            {hasLatex(question.questionText)
              ? <KatexRenderer latex={question.questionText} displayMode={false} />
              : question.questionText}
          </div>
          {question.questionLatex && (
            <div className="mt-3 overflow-x-auto p-3 bg-gray-50 rounded-xl border border-gray-100">
              <KatexRenderer latex={question.questionLatex} displayMode />
            </div>
          )}
        </div>

        {/* Options */}
        <div className="space-y-3">
          {question.options.map((opt) => {
            const isSelected = responses[currentQ]?.answer === opt.id;
            return (
              <button
                key={opt.id}
                onClick={() => selectAnswer(opt.id)}
                className={`w-full text-left rounded-2xl px-4 py-4 min-h-[56px] border-2 flex items-center gap-3 transition-colors duration-200 shadow-sm ${
                  isSelected
                    ? 'bg-blue-50 border-duo-blue shadow-md'
                    : 'bg-white border-gray-200 hover:border-duo-blue hover:bg-blue-50'
                }`}
              >
                <span className={`w-9 h-9 rounded-full flex-shrink-0 flex items-center justify-center text-sm font-extrabold transition-colors ${
                  isSelected
                    ? 'bg-duo-blue text-white'
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  {opt.id}
                </span>
                <span className="flex-1 text-gray-800 text-base font-semibold leading-snug">
                  {hasLatex(opt.text) ? <KatexRenderer latex={opt.text} displayMode={false} /> : opt.text}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Bottom action bar */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-3 z-30">
        <div className="max-w-lg mx-auto flex items-center gap-2">
          {/* Prev */}
          <button
            onClick={() => currentQ > 0 && goToQuestion(currentQ - 1)}
            disabled={currentQ === 0}
            className="px-4 py-3 rounded-xl text-sm font-extrabold text-gray-500 bg-gray-100 disabled:opacity-30 transition-colors hover:bg-gray-200"
          >
            ←
          </button>

          {/* Flag */}
          <button
            onClick={toggleFlag}
            className={`px-4 py-3 rounded-xl text-sm font-extrabold transition-colors ${
              responses[currentQ]?.flagged
                ? 'bg-duo-orange text-white'
                : 'bg-orange-50 text-duo-orange hover:bg-orange-100'
            }`}
          >
            🚩
          </button>

          {/* Clear */}
          {responses[currentQ]?.answer && (
            <button
              onClick={() => selectAnswer(null)}
              className="px-3 py-3 rounded-xl text-xs font-extrabold text-gray-400 bg-gray-50 hover:bg-gray-100"
            >
              Clear
            </button>
          )}

          <div className="flex-1" />

          {/* Next / Submit */}
          {currentQ < paper.totalQuestions - 1 ? (
            <button
              onClick={() => goToQuestion(currentQ + 1)}
              className="px-6 py-3 rounded-xl text-sm font-extrabold bg-duo-blue text-white hover:bg-[#0a8fd4] transition-colors"
            >
              Next →
            </button>
          ) : (
            <button
              onClick={() => setShowSubmitModal(true)}
              className="px-6 py-3 rounded-xl text-sm font-extrabold bg-duo-green text-white hover:bg-duo-green-dark transition-colors"
            >
              Submit ✓
            </button>
          )}
        </div>
      </div>

      {/* Question Navigator Modal */}
      {showNav && (
        <div className="fixed inset-0 z-[80] bg-black/60 flex items-end" onClick={() => setShowNav(false)}>
          <div
            className="w-full bg-white rounded-t-3xl p-6 pb-8 max-h-[70vh] overflow-y-auto animate-slide-up"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-extrabold text-gray-800 text-lg">Question Navigator</h3>
              <button onClick={() => setShowNav(false)} className="text-gray-400 text-2xl leading-none min-w-[44px] min-h-[44px] flex items-center justify-center">×</button>
            </div>

            <div className="flex gap-3 mb-4 text-xs font-bold">
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-duo-blue inline-block" /> Answered</span>
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-duo-orange inline-block" /> Flagged</span>
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-gray-200 inline-block" /> Unanswered</span>
            </div>

            <div className="grid grid-cols-6 gap-2">
              {responses.map((r, i) => {
                const isAnswered = !!r.answer;
                const isFlagged = r.flagged;
                const isCurrent = i === currentQ;

                return (
                  <button
                    key={i}
                    onClick={() => { goToQuestion(i); setShowNav(false); }}
                    className={`w-11 h-11 rounded-full flex items-center justify-center text-xs font-extrabold transition-[background-color,transform] ${
                      isCurrent ? 'bg-duo-blue text-white ring-4 ring-blue-200 scale-110' :
                      isFlagged ? 'bg-duo-orange text-white' :
                      isAnswered ? 'bg-duo-blue/20 text-duo-blue border-2 border-duo-blue' :
                      'bg-gray-100 text-gray-500 border-2 border-gray-200'
                    }`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100 flex gap-3 text-xs text-gray-500 font-semibold">
              <span>Answered: {answeredCount}/{paper.totalQuestions}</span>
              <span>Flagged: {flaggedCount}</span>
              <span>Unanswered: {paper.totalQuestions - answeredCount}</span>
            </div>

            <button
              onClick={() => { setShowNav(false); setShowSubmitModal(true); }}
              className="w-full mt-4 bg-duo-green hover:bg-duo-green-dark text-white font-extrabold py-3 rounded-2xl transition-colors"
            >
              Submit Exam
            </button>
          </div>
        </div>
      )}

      {/* Submit Confirmation Modal */}
      {showSubmitModal && (
        <div className="fixed inset-0 z-[90] bg-black/60 flex items-center justify-center px-6" onClick={() => setShowSubmitModal(false)}>
          <div
            className="bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl animate-slide-up"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="text-center mb-4">
              <Sparky mood="thinking" size={56} />
              <h3 className="font-extrabold text-gray-800 text-lg mt-2">Submit Exam?</h3>
            </div>

            <div className="space-y-2 mb-5">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Answered</span>
                <span className="font-extrabold text-duo-green">{answeredCount}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Unanswered</span>
                <span className="font-extrabold text-gray-400">{paper.totalQuestions - answeredCount}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Flagged for review</span>
                <span className="font-extrabold text-duo-orange">{flaggedCount}</span>
              </div>
            </div>

            {paper.totalQuestions - answeredCount > 0 && (
              <p className="text-xs text-duo-orange font-bold text-center mb-4">
                You have {paper.totalQuestions - answeredCount} unanswered question{paper.totalQuestions - answeredCount > 1 ? 's' : ''}.
              </p>
            )}

            <div className="flex gap-3">
              <button
                onClick={() => setShowSubmitModal(false)}
                className="flex-1 bg-gray-100 text-gray-700 font-bold py-3 rounded-xl hover:bg-gray-200 transition-colors"
              >
                Go Back
              </button>
              <button
                onClick={handleSubmit}
                className="flex-1 bg-duo-green text-white font-extrabold py-3 rounded-xl hover:bg-duo-green-dark transition-colors"
              >
                Submit ✓
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
