'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import KatexRenderer from '@/components/KatexRenderer';

// ── Types ─────────────────────────────────────────────────────────────────────

interface StepData {
  stepNumber: number;
  instruction: string;
  latex: string;
  sparkyNarration: string;
  revealDelay: number;
}

interface Option {
  id: string;
  text: string;
}

interface TrapWarning {
  exists: boolean;
  text: string;
  sparkyWarning: string;
}

interface FinalAnswer {
  text: string;
  sparkyReaction: string;
}

interface WorkedExample {
  id: string;
  grade: number;
  topic: string;
  subTopic: string;
  difficulty: string;
  questionText: string;
  questionLatex: string;
  options: Option[];
  correctAnswer: string;
  correctAnswerText: string;
  sparkyThinking: string[];
  stepByStep: StepData[];
  finalAnswer: FinalAnswer;
  trapWarning: TrapWarning;
  hints: string[];
  practiceQuestionIds: string[];
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function hasLatex(text: string): boolean {
  return text.includes('\\');
}

const DIFF_COLORS: Record<string, string> = {
  Easy: '#58CC02',
  Medium: '#FF9600',
  Hard: '#FF4B4B',
};

// ── Page ──────────────────────────────────────────────────────────────────────

export default function WorkedExampleDetailPage() {
  const params = useParams<{ exampleId: string }>();
  const exampleId = params.exampleId;

  const [example, setExample] = useState<WorkedExample | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Animation state
  const [revealedSteps, setRevealedSteps] = useState(0);
  const [showThinking, setShowThinking] = useState(false);
  const [showFinal, setShowFinal] = useState(false);
  const [showTrap, setShowTrap] = useState(false);
  const [autoRevealing, setAutoRevealing] = useState(false);

  useEffect(() => {
    fetch(`/api/worked-examples?id=${exampleId}`)
      .then((r) => r.json())
      .then((data) => {
        if (data.example) {
          setExample(data.example);
        } else {
          setError('Example not found.');
        }
      })
      .catch(() => setError('Failed to load example.'))
      .finally(() => setLoading(false));
  }, [exampleId]);

  // Auto-reveal steps with animation delays
  function startAutoReveal() {
    if (!example || autoRevealing) return;
    setAutoRevealing(true);
    setShowThinking(true);

    // Reveal steps one by one with delays
    const steps = example.stepByStep;
    let delay = 1200; // Start after thinking bubble appears

    steps.forEach((step, i) => {
      const stepDelay = (step.revealDelay ?? 1.5) * 1000;
      delay += stepDelay;
      setTimeout(() => {
        setRevealedSteps(i + 1);
      }, delay);
    });

    // Show final answer after all steps
    delay += 1000;
    setTimeout(() => {
      setShowFinal(true);
    }, delay);

    // Show trap warning if exists
    if (example.trapWarning?.exists) {
      delay += 800;
      setTimeout(() => {
        setShowTrap(true);
      }, delay);
    }

    setTimeout(() => {
      setAutoRevealing(false);
    }, delay + 500);
  }

  // Manual reveal: show everything at once
  function revealAll() {
    if (!example) return;
    setShowThinking(true);
    setRevealedSteps(example.stepByStep.length);
    setShowFinal(true);
    if (example.trapWarning?.exists) setShowTrap(true);
  }

  // ── Loading ─────────────────────────────────────────────────────────────────

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pb-24">
        <div className="bg-duo-dark px-4 py-4 flex items-center gap-3">
          <Link href="/learn/examples" className="text-white/60 hover:text-white text-sm">&larr;</Link>
          <h1 className="text-white font-extrabold text-lg">Loading...</h1>
        </div>
        <div className="max-w-lg mx-auto px-4 pt-6 space-y-3">
          <div className="bg-white rounded-2xl p-6 border border-gray-100 animate-pulse h-40" />
          <div className="bg-white rounded-2xl p-6 border border-gray-100 animate-pulse h-60" />
        </div>
      </div>
    );
  }

  if (error || !example) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 px-6">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-red-500">{error || 'Something went wrong.'}</p>
        <Link href="/learn/examples" className="text-sm text-blue-500 underline">Back to Examples</Link>
      </div>
    );
  }

  const correctIdx = ['A', 'B', 'C', 'D'].indexOf(example.correctAnswer);
  const hasStarted = showThinking || revealedSteps > 0;

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div
        className="sticky top-0 z-40 px-4 py-4 flex items-center gap-3 shadow-md"
        style={{ backgroundColor: '#131F24' }}
      >
        <Link href="/learn/examples" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1 min-w-0">
          <h1 className="text-white font-extrabold text-sm truncate">Sparky Explains</h1>
          <p className="text-white/50 text-xs font-medium truncate">
            {example.topic.replace(/_/g, ' ')} &middot; Grade {example.grade}
          </p>
        </div>
        <span
          className="text-[10px] font-extrabold px-2 py-0.5 rounded-full text-white"
          style={{ backgroundColor: DIFF_COLORS[example.difficulty] ?? '#999' }}
        >
          {example.difficulty}
        </span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* ── Question Card ───────────────────────────────────────────────── */}
        <div className="bg-white rounded-2xl p-5 border border-gray-100 shadow-md">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wide">
              Question
            </span>
            <span className="text-[11px] font-medium text-gray-300">{example.subTopic}</span>
          </div>

          <p className="text-lg font-bold text-gray-800 leading-relaxed">
            {hasLatex(example.questionText) ? (
              <KatexRenderer latex={example.questionText} displayMode={false} />
            ) : (
              example.questionText
            )}
          </p>

          {example.questionLatex && (
            <div className="mt-3 overflow-x-auto p-3 bg-gray-50 rounded-xl border border-gray-100">
              <KatexRenderer latex={example.questionLatex} displayMode className="block" />
            </div>
          )}

          {/* Options */}
          <div className="mt-4 space-y-2">
            {example.options.map((opt, i) => (
              <div
                key={opt.id}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl border-2 ${
                  i === correctIdx && (showFinal || revealedSteps === example.stepByStep.length)
                    ? 'bg-green-50 border-duo-green'
                    : 'bg-white border-gray-200'
                }`}
              >
                <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold border-2 ${
                  i === correctIdx && (showFinal || revealedSteps === example.stepByStep.length)
                    ? 'bg-duo-green border-duo-green-dark text-white'
                    : 'bg-gray-100 border-gray-300 text-gray-600'
                }`}>
                  {i === correctIdx && showFinal ? '✓' : opt.id}
                </span>
                <span className="text-sm font-medium text-gray-700">
                  {hasLatex(opt.text) ? <KatexRenderer latex={opt.text} displayMode={false} /> : opt.text}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* ── Start Button ────────────────────────────────────────────────── */}
        {!hasStarted && (
          <div className="flex gap-3">
            <button
              onClick={startAutoReveal}
              className="flex-1 bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-extrabold py-3.5 rounded-2xl transition-colors hover:from-purple-600 hover:to-indigo-600 flex items-center justify-center gap-2"
            >
              <Sparky mood="happy" size={24} />
              Watch Sparky Solve It
            </button>
            <button
              onClick={revealAll}
              className="bg-gray-200 text-gray-600 font-bold px-4 py-3.5 rounded-2xl transition-colors hover:bg-gray-300 text-sm"
            >
              Show All
            </button>
          </div>
        )}

        {/* ── Sparky's Thinking ───────────────────────────────────────────── */}
        {showThinking && example.sparkyThinking.length > 0 && (
          <div className="bg-purple-50 rounded-2xl px-4 py-3 border border-purple-200 animate-fade-in">
            <div className="flex items-start gap-3">
              <Sparky mood="thinking" size={36} />
              <div className="flex-1 space-y-2">
                <p className="text-xs font-extrabold text-purple-500 uppercase tracking-wide">
                  Sparky&apos;s Thinking...
                </p>
                {example.sparkyThinking.map((thought, i) => (
                  <p
                    key={i}
                    className="text-sm text-purple-800 font-medium leading-snug animate-fade-in"
                    style={{ animationDelay: `${i * 300}ms`, animationFillMode: 'backwards' }}
                  >
                    {thought}
                  </p>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── Steps ───────────────────────────────────────────────────────── */}
        {revealedSteps > 0 && (
          <div className="space-y-3">
            {example.stepByStep.slice(0, revealedSteps).map((step, i) => (
              <div
                key={step.stepNumber}
                className="bg-white rounded-2xl p-4 border border-gray-100 shadow-sm animate-fade-in"
                style={{ animationDelay: `${i * 120}ms`, animationFillMode: 'backwards' }}
              >
                <div className="flex items-start gap-3">
                  {/* Step number circle */}
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center text-white text-xs font-extrabold shrink-0">
                    {step.stepNumber}
                  </div>

                  <div className="flex-1 min-w-0 space-y-2">
                    {/* Instruction */}
                    <p className="text-sm font-semibold text-gray-800 leading-snug">
                      {hasLatex(step.instruction) ? (
                        <KatexRenderer latex={step.instruction} displayMode={false} />
                      ) : (
                        step.instruction
                      )}
                    </p>

                    {/* LaTeX formula */}
                    {step.latex && (
                      <div className="bg-indigo-50 rounded-xl px-3 py-2 border border-indigo-200 overflow-x-auto">
                        <KatexRenderer latex={step.latex} displayMode className="block" />
                      </div>
                    )}

                    {/* Sparky narration */}
                    {step.sparkyNarration && (
                      <div className="flex items-start gap-2 bg-purple-50 rounded-xl px-3 py-2 border border-purple-100">
                        <span className="text-sm shrink-0">💬</span>
                        <p className="text-xs font-medium text-purple-700 italic leading-snug">
                          {step.sparkyNarration}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* ── Final Answer ────────────────────────────────────────────────── */}
        {showFinal && example.finalAnswer && (
          <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-2xl p-4 border-2 border-duo-green shadow-md animate-fade-in">
            <div className="flex items-start gap-3">
              <Sparky mood="celebrating" size={40} />
              <div className="flex-1">
                <p className="text-sm font-extrabold text-duo-green mb-1">Answer: {example.correctAnswer}</p>
                <p className="text-sm font-semibold text-gray-800">{example.finalAnswer.text}</p>
                {example.finalAnswer.sparkyReaction && (
                  <p className="text-xs font-medium text-green-600 mt-1.5 italic">
                    {example.finalAnswer.sparkyReaction}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ── Trap Warning ────────────────────────────────────────────────── */}
        {showTrap && example.trapWarning?.exists && (
          <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-2xl p-4 border-2 border-red-300 shadow-md animate-fade-in">
            <div className="flex items-start gap-3">
              <div className="text-2xl shrink-0">⚠️</div>
              <div className="flex-1">
                <p className="text-sm font-extrabold text-red-600 mb-1">Trap Warning!</p>
                <p className="text-sm font-medium text-gray-800">{example.trapWarning.text}</p>
                {example.trapWarning.sparkyWarning && (
                  <div className="flex items-start gap-2 mt-2 bg-white rounded-xl px-3 py-2 border border-red-200">
                    <Sparky mood="encouraging" size={24} />
                    <p className="text-xs font-medium text-red-700 italic leading-snug">
                      {example.trapWarning.sparkyWarning}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ── Hints ───────────────────────────────────────────────────────── */}
        {showFinal && example.hints && example.hints.length > 0 && (
          <div className="bg-blue-50 rounded-2xl p-4 border border-blue-200">
            <p className="text-xs font-extrabold text-blue-500 uppercase tracking-wide mb-2">
              Quick Hints
            </p>
            <div className="space-y-1.5">
              {example.hints.map((hint, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-xs text-blue-400 shrink-0">{i + 1}.</span>
                  <p className="text-sm text-blue-800 font-medium">{hint}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── Navigation ──────────────────────────────────────────────────── */}
        <div className="flex gap-3 pt-2">
          <Link
            href="/learn/examples"
            className="flex-1 bg-duo-blue hover:bg-[#0a8fd4] text-white font-extrabold py-3.5 rounded-2xl text-center transition-colors"
          >
            More Examples →
          </Link>
          <Link
            href="/home"
            className="bg-gray-200 text-gray-600 font-bold px-6 py-3.5 rounded-2xl transition-colors hover:bg-gray-300 text-sm"
          >
            Home
          </Link>
        </div>
      </div>
    </div>
  );
}
