'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import KatexRenderer from '@/components/KatexRenderer';
import type { MockTestDetail, MockTestResponse, AnswerKey } from '@/types';

// ── Timer hook ────────────────────────────────────────────────────────────────

function useTestTimer(startedAt: string | null, timeLimitMs: number | null) {
  const [remaining, setRemaining] = useState<number | null>(null);

  useEffect(() => {
    if (!startedAt || !timeLimitMs) return;
    const tick = () => {
      const elapsed = Date.now() - new Date(startedAt).getTime();
      const left    = Math.max(0, timeLimitMs - elapsed);
      setRemaining(left);
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [startedAt, timeLimitMs]);

  return remaining;
}

function formatTime(ms: number): string {
  const totalSec = Math.floor(ms / 1000);
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

// ── Question navigator ────────────────────────────────────────────────────────

function QuestionNavigator({
  responses,
  current,
  onJump,
  onClose,
}: {
  responses: MockTestResponse[];
  current: number;
  onJump: (n: number) => void;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 z-[80] bg-black/60 flex items-end" onClick={onClose}>
      <div
        className="w-full bg-white rounded-t-3xl p-6 pb-8 max-h-[70vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-extrabold text-gray-800 text-lg">Question Navigator</h3>
          <button onClick={onClose} className="text-gray-400 text-2xl leading-none">×</button>
        </div>

        {/* Legend */}
        <div className="flex gap-3 mb-4 text-xs font-bold">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-[#1CB0F6] inline-block" /> Answered</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-[#FF9600] inline-block" /> Flagged</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-gray-200 inline-block" /> Unanswered</span>
        </div>

        <div className="grid grid-cols-8 gap-2">
          {responses.map((r) => {
            const n = r.questionNumber;
            const isAnswered = !!r.selectedAnswer;
            const isFlagged  = r.flagged;
            const isCurrent  = n === current;

            const circleCls = isCurrent
              ? 'bg-[#1CB0F6] text-white ring-4 ring-blue-200 scale-110'
              : isFlagged
              ? 'bg-[#FF9600] text-white'
              : isAnswered
              ? 'bg-[#1CB0F6]/20 text-[#1CB0F6] border-2 border-[#1CB0F6]'
              : 'bg-gray-100 text-gray-500 border-2 border-gray-200';

            return (
              <button
                key={n}
                onClick={() => { onJump(n); onClose(); }}
                className={`w-9 h-9 rounded-full flex items-center justify-center text-xs font-extrabold transition-all ${circleCls}`}
              >
                {n}
              </button>
            );
          })}
        </div>

        <div className="mt-4 pt-4 border-t border-gray-100 flex gap-3 text-xs text-gray-500 font-semibold">
          <span>Answered: {responses.filter((r) => r.selectedAnswer).length}/{responses.length}</span>
          <span>Flagged: {responses.filter((r) => r.flagged).length}</span>
          <span>Unanswered: {responses.filter((r) => !r.selectedAnswer).length}</span>
        </div>
      </div>
    </div>
  );
}

// ── Submit modal ──────────────────────────────────────────────────────────────

function SubmitModal({
  responses,
  onCancel,
  onConfirm,
  submitting,
}: {
  responses: MockTestResponse[];
  onCancel: () => void;
  onConfirm: () => void;
  submitting: boolean;
}) {
  const answered   = responses.filter((r) => r.selectedAnswer).length;
  const flagged    = responses.filter((r) => r.flagged).length;
  const unanswered = responses.length - answered;

  return (
    <div className="fixed inset-0 z-[90] bg-black/60 flex items-center justify-center px-4">
      <div className="bg-white rounded-3xl p-6 w-full max-w-sm space-y-4 shadow-2xl">
        <h3 className="font-extrabold text-gray-800 text-xl text-center">Ready to submit?</h3>

        <div className="bg-gray-50 rounded-2xl p-4 space-y-2">
          <div className="flex justify-between text-sm font-bold">
            <span className="text-gray-600">Answered</span>
            <span className="text-[#58CC02]">{answered}/{responses.length}</span>
          </div>
          <div className="flex justify-between text-sm font-bold">
            <span className="text-gray-600">Flagged for review</span>
            <span className="text-[#FF9600]">{flagged}</span>
          </div>
          <div className="flex justify-between text-sm font-bold">
            <span className="text-gray-600">Unanswered</span>
            <span className="text-[#FF4B4B]">{unanswered}</span>
          </div>
        </div>

        {unanswered > 0 && (
          <p className="text-amber-600 text-xs font-semibold text-center">
            ⚠️ You have {unanswered} unanswered question{unanswered !== 1 ? 's' : ''}.
          </p>
        )}

        <div className="flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 min-h-[48px] rounded-2xl border-2 border-gray-200 font-extrabold text-gray-600 hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={submitting}
            className="flex-1 min-h-[48px] rounded-2xl bg-[#58CC02] border-b-4 border-[#46a302] font-extrabold text-white disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {submitting ? (
              <span className="inline-block w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : 'Submit Test ✓'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ── Main engine ────────────────────────────────────────────────────────────────

export default function TestEnginePage() {
  const router = useRouter();
  const { testId } = useParams<{ testId: string }>();

  const [test,           setTest]           = useState<MockTestDetail | null>(null);
  const [responses,      setResponses]      = useState<MockTestResponse[]>([]);
  const [currentNum,     setCurrentNum]     = useState(1);
  const [loading,        setLoading]        = useState(true);
  const [showNavigator,  setShowNavigator]  = useState(false);
  const [showSubmitModal,setShowSubmitModal] = useState(false);
  const [submitting,     setSubmitting]     = useState(false);
  const [autoSubmitted,  setAutoSubmitted]  = useState(false);

  const questionStartRef = useRef<number>(Date.now());
  const patchQueueRef    = useRef<Array<() => Promise<void>>>([]);
  const flushingRef      = useRef(false);

  // Load test data
  useEffect(() => {
    async function load() {
      try {
        const res = await fetch(`/api/mock-tests/${testId}`);
        if (!res.ok) { router.replace('/test'); return; }
        const data: MockTestDetail = await res.json();
        if (data.status === 'completed') {
          router.replace(`/test/${testId}/results`);
          return;
        }
        setTest(data);
        setResponses(data.responses);

        // Jump to first unanswered question
        const firstUnanswered = data.responses.find((r) => !r.selectedAnswer);
        if (firstUnanswered) setCurrentNum(firstUnanswered.questionNumber);

        setLoading(false);
      } catch {
        router.replace('/test');
      }
    }
    load();
  }, [testId, router]);

  // Timer
  const remaining = useTestTimer(test?.startedAt ?? null, test?.timeLimitMs ?? null);

  // Auto-submit when time runs out
  useEffect(() => {
    if (remaining === 0 && !autoSubmitted && test && !loading) {
      setAutoSubmitted(true);
      handleSubmit();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [remaining, autoSubmitted, test, loading]);

  // Flush PATCH queue
  async function flushQueue() {
    if (flushingRef.current || patchQueueRef.current.length === 0) return;
    flushingRef.current = true;
    while (patchQueueRef.current.length > 0) {
      const fn = patchQueueRef.current.shift()!;
      await fn().catch(() => {/* silent */});
    }
    flushingRef.current = false;
  }

  // Save response (debounced via queue)
  const saveResponse = useCallback((questionNumber: number, data: {
    selectedAnswer?: string;
    flagged?: boolean;
    additionalTimeMs?: number;
  }) => {
    patchQueueRef.current.push(() =>
      fetch(`/api/mock-tests/${testId}/response`, {
        method: 'PATCH',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ questionNumber, ...data }),
      }).then(() => {/* ok */})
    );
    flushQueue();
  }, [testId]);

  // Navigate to a question
  function navigateTo(num: number) {
    if (!test || num < 1 || num > test.totalQuestions) return;
    // Track time on current question
    const elapsed = Date.now() - questionStartRef.current;
    if (elapsed > 500) {
      saveResponse(currentNum, { additionalTimeMs: elapsed });
    }
    questionStartRef.current = Date.now();
    setCurrentNum(num);
  }

  // Select answer
  function selectAnswer(questionNumber: number, answer: AnswerKey) {
    setResponses((prev) => prev.map((r) =>
      r.questionNumber === questionNumber
        ? { ...r, selectedAnswer: r.selectedAnswer === answer ? null : answer }
        : r,
    ));
    const current = responses.find((r) => r.questionNumber === questionNumber);
    const newAnswer = current?.selectedAnswer === answer ? undefined : answer;
    saveResponse(questionNumber, { selectedAnswer: newAnswer });
  }

  // Toggle flag
  function toggleFlag(questionNumber: number) {
    setResponses((prev) => prev.map((r) =>
      r.questionNumber === questionNumber ? { ...r, flagged: !r.flagged } : r,
    ));
    const current = responses.find((r) => r.questionNumber === questionNumber);
    saveResponse(questionNumber, { flagged: !current?.flagged });
  }

  // Submit
  async function handleSubmit() {
    setShowSubmitModal(false);
    setSubmitting(true);
    // Flush remaining time
    const elapsed = Date.now() - questionStartRef.current;
    if (elapsed > 500) {
      await fetch(`/api/mock-tests/${testId}/response`, {
        method: 'PATCH',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ questionNumber: currentNum, additionalTimeMs: elapsed }),
      }).catch(() => {/* silent */});
    }
    try {
      const res = await fetch(`/api/mock-tests/${testId}/submit`, { method: 'POST' });
      if (!res.ok) throw new Error();
      router.push(`/test/${testId}/results`);
    } catch {
      setSubmitting(false);
    }
  }

  if (loading || !test) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="w-12 h-12 border-4 border-[#1CB0F6]/30 border-t-[#1CB0F6] rounded-full animate-spin mx-auto" />
          <p className="text-gray-400 font-semibold">Loading your test…</p>
        </div>
      </div>
    );
  }

  const currentResponse = responses.find((r) => r.questionNumber === currentNum);
  const currentQuestion = currentResponse?.question;
  if (!currentResponse || !currentQuestion) return null;

  const answered   = responses.filter((r) => r.selectedAnswer).length;
  const totalQ     = test.totalQuestions;

  // Timer color
  const timerColor =
    remaining !== null && remaining <= 60_000   ? 'text-[#FF4B4B]' :
    remaining !== null && remaining <= 300_000  ? 'text-[#FF4B4B]' :
    remaining !== null && remaining <= 600_000  ? 'text-[#FF9600]' :
    'text-gray-700';
  const timerPulse = remaining !== null && remaining <= 60_000 ? 'animate-pulse' : '';

  const options: Array<{ key: AnswerKey; text: string }> = [
    { key: 'A', text: currentQuestion.option1 },
    { key: 'B', text: currentQuestion.option2 },
    { key: 'C', text: currentQuestion.option3 },
    { key: 'D', text: currentQuestion.option4 },
  ];

  return (
    <div className="min-h-screen bg-white flex flex-col max-w-lg mx-auto">
      {/* ── Top bar ─────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-50 bg-white border-b border-gray-100 px-4 py-3 flex items-center gap-3">
        {/* Back / quit */}
        <button
          onClick={() => {
            if (window.confirm('Leave the test? Your progress is saved — you can resume later.')) {
              router.push('/test');
            }
          }}
          className="text-gray-400 text-xl leading-none mr-1 flex-shrink-0"
        >
          ←
        </button>

        {/* Progress bar */}
        <div className="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
          <div
            className="h-full bg-[#1CB0F6] rounded-full transition-all duration-500"
            style={{ width: `${(answered / totalQ) * 100}%` }}
          />
        </div>

        {/* Q counter */}
        <span className="text-xs font-extrabold text-gray-500 flex-shrink-0">{answered}/{totalQ}</span>

        {/* Timer */}
        {remaining !== null && (
          <div className={`flex items-center gap-1 font-extrabold text-sm flex-shrink-0 ${timerColor} ${timerPulse}`}>
            ⏱ {formatTime(remaining)}
          </div>
        )}
      </div>

      {/* ── Question area ────────────────────────────────────────────────── */}
      <div className="flex-1 px-4 pt-4 pb-4 overflow-y-auto">
        {/* Q# + topic + flag */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold text-white bg-[#1CB0F6] rounded-full px-3 py-1">
              Q{currentNum}
            </span>
            <span className="text-xs text-gray-400 font-semibold">{currentQuestion.difficulty}</span>
          </div>
          <button
            onClick={() => toggleFlag(currentNum)}
            className={`flex items-center gap-1 text-xs font-extrabold px-3 py-1 rounded-full border-2 transition-colors ${
              currentResponse.flagged
                ? 'bg-[#FF9600] border-[#FF9600] text-white'
                : 'border-gray-200 text-gray-400 hover:border-[#FF9600] hover:text-[#FF9600]'
            }`}
          >
            🚩 {currentResponse.flagged ? 'Flagged' : 'Flag'}
          </button>
        </div>

        {/* Question text */}
        <div className="bg-gray-50 rounded-2xl p-4 mb-4">
          <p className="text-gray-800 font-semibold text-base leading-relaxed">
            {currentQuestion.questionText}
          </p>
          {currentQuestion.questionLatex && (
            <div className="mt-2">
              <KatexRenderer latex={currentQuestion.questionLatex} />
            </div>
          )}
        </div>

        {/* Options */}
        <div className="space-y-3">
          {options.map(({ key, text }) => {
            const isSelected = currentResponse.selectedAnswer === key;
            return (
              <button
                key={key}
                onClick={() => selectAnswer(currentNum, key)}
                className={`w-full text-left rounded-2xl p-4 border-2 font-semibold text-base transition-all duration-150 active:scale-[0.98] min-h-[56px] flex items-center gap-3 ${
                  isSelected
                    ? 'bg-blue-50 border-[#1CB0F6] text-gray-800'
                    : 'bg-white border-gray-200 text-gray-700 hover:border-[#1CB0F6]/50'
                }`}
              >
                <span className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-sm font-extrabold border-2 ${
                  isSelected
                    ? 'bg-[#1CB0F6] border-[#1CB0F6] text-white'
                    : 'border-gray-300 text-gray-500'
                }`}>
                  {key}
                </span>
                <span className="leading-snug">{text}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Bottom navigation bar ────────────────────────────────────────── */}
      <div className="sticky bottom-0 bg-white border-t border-gray-100 px-4 py-3 flex gap-3">
        <button
          onClick={() => navigateTo(currentNum - 1)}
          disabled={currentNum === 1}
          className="min-h-[48px] px-4 rounded-2xl border-2 border-gray-200 font-extrabold text-gray-500 disabled:opacity-30 hover:border-gray-400 transition-colors"
        >
          ←
        </button>

        <button
          onClick={() => setShowNavigator(true)}
          className="flex-1 min-h-[48px] rounded-2xl border-2 border-gray-200 font-bold text-gray-600 hover:border-[#1CB0F6] transition-colors text-sm"
        >
          Q{currentNum}/{totalQ} · {answered} answered
        </button>

        {currentNum === totalQ ? (
          <button
            onClick={() => setShowSubmitModal(true)}
            className="min-h-[48px] px-4 rounded-2xl bg-[#58CC02] border-b-4 border-[#46a302] font-extrabold text-white text-sm"
          >
            Submit ✓
          </button>
        ) : (
          <button
            onClick={() => navigateTo(currentNum + 1)}
            className="min-h-[48px] px-4 rounded-2xl bg-[#1CB0F6] border-b-4 border-[#0a98dc] font-extrabold text-white"
          >
            →
          </button>
        )}
      </div>

      {/* Submit button (always visible when not on last Q) */}
      {currentNum !== totalQ && (
        <div className="px-4 pb-4 bg-white">
          <button
            onClick={() => setShowSubmitModal(true)}
            className="w-full min-h-[48px] rounded-2xl border-2 border-[#58CC02] text-[#58CC02] font-extrabold text-sm hover:bg-green-50 transition-colors"
          >
            Submit Test ✓
          </button>
        </div>
      )}

      {/* Navigator overlay */}
      {showNavigator && (
        <QuestionNavigator
          responses={responses}
          current={currentNum}
          onJump={navigateTo}
          onClose={() => setShowNavigator(false)}
        />
      )}

      {/* Submit modal */}
      {showSubmitModal && (
        <SubmitModal
          responses={responses}
          onCancel={() => setShowSubmitModal(false)}
          onConfirm={handleSubmit}
          submitting={submitting}
        />
      )}

      {/* Submitting overlay */}
      {submitting && (
        <div className="fixed inset-0 z-[100] bg-white/90 flex items-center justify-center">
          <div className="text-center space-y-3">
            <div className="w-12 h-12 border-4 border-[#58CC02]/30 border-t-[#58CC02] rounded-full animate-spin mx-auto" />
            <p className="font-extrabold text-gray-700">Grading your test…</p>
          </div>
        </div>
      )}
    </div>
  );
}
