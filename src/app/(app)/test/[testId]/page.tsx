'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { logError } from '@/lib/logger';
import { useParams, useRouter } from 'next/navigation';
import KatexRenderer from '@/components/KatexRenderer';
import QuestionDiagram from '@/components/diagrams/QuestionDiagram';
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
        className="w-full bg-white rounded-t-card border-t-2 border-ink p-6 pb-8 max-h-[70vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-title text-ink">Question Navigator</h3>
          <button onClick={onClose} className="text-ink-muted text-2xl leading-none min-w-[44px] min-h-[44px] flex items-center justify-center">×</button>
        </div>

        {/* Legend */}
        <div className="flex gap-3 mb-4 text-xs font-bold text-ink">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-action inline-block" /> Answered</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-hint border-2 border-hint-ink inline-block" /> Flagged</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-white border-2 border-line inline-block" /> Unanswered</span>
        </div>

        <div className="grid grid-cols-6 gap-2">
          {responses.map((r) => {
            const n = r.questionNumber;
            const isAnswered = !!r.selectedAnswer;
            const isFlagged  = r.flagged;
            const isCurrent  = n === current;

            const circleCls = isCurrent
              ? 'bg-white text-ink border-2 border-ink shadow-hard-xs scale-110'
              : isFlagged
              ? 'bg-hint text-hint-ink border-2 border-hint-ink'
              : isAnswered
              ? 'bg-action text-white border-2 border-action'
              : 'bg-white text-ink-muted border-2 border-line';

            return (
              <button
                key={n}
                onClick={() => { onJump(n); onClose(); }}
                className={`w-11 h-11 rounded-full flex items-center justify-center text-xs font-extrabold transition-colors ${circleCls}`}
              >
                {n}
              </button>
            );
          })}
        </div>

        <div className="mt-4 pt-4 border-t-2 border-line flex gap-3 text-xs text-ink-muted font-semibold">
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
      <div className="bg-white rounded-card border-2 border-ink p-6 w-full max-w-sm space-y-4 shadow-hard-lg">
        <h3 className="text-heading text-ink text-center">Ready to submit?</h3>
        <p className="text-xs text-ink-muted text-center -mt-2">Your answers will be graded after submission.</p>

        <div className="bg-soft rounded-control p-4 space-y-2">
          <div className="flex justify-between text-sm font-bold">
            <span className="text-ink-muted">Questions attempted</span>
            <span className="text-action">{answered}/{responses.length}</span>
          </div>
          <div className="flex justify-between text-sm font-bold">
            <span className="text-ink-muted">Flagged for review</span>
            <span className="text-hint-ink">{flagged}</span>
          </div>
          <div className="flex justify-between text-sm font-bold">
            <span className="text-ink-muted">Unanswered</span>
            <span className="text-ink">{unanswered}</span>
          </div>
        </div>

        {unanswered > 0 && (
          <p className="text-hint-ink text-xs font-semibold text-center">
            ⚠️ You have {unanswered} unanswered question{unanswered !== 1 ? 's' : ''}.
          </p>
        )}

        <div className="flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 min-h-[48px] rounded-control border-2 border-ink bg-white shadow-hard-sm font-extrabold text-ink hover:bg-soft transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={submitting}
            className="flex-1 min-h-[48px] rounded-control bg-action border-2 border-ink shadow-hard-sm font-extrabold text-white disabled:opacity-50 flex items-center justify-center gap-2"
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
  const [showQuitModal,  setShowQuitModal]  = useState(false);
  const [submitting,     setSubmitting]     = useState(false);
  const [submitError,    setSubmitError]    = useState('');
  const [autoSubmitted,  setAutoSubmitted]  = useState(false);
  const [isOffline,      setIsOffline]      = useState(false);

  const questionStartRef = useRef<number>(Date.now());
  const currentNumRef    = useRef(1);
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
        if (firstUnanswered) {
          setCurrentNum(firstUnanswered.questionNumber);
          currentNumRef.current = firstUnanswered.questionNumber;
        }

        setLoading(false);
      } catch {
        router.replace('/test');
      }
    }
    load();
  }, [testId]); // eslint-disable-line react-hooks/exhaustive-deps

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

  // Flush PATCH queue — peek first, only shift on success so offline items stay for retry
  const flushQueue = useCallback(async () => {
    if (flushingRef.current || patchQueueRef.current.length === 0) return;
    flushingRef.current = true;
    while (patchQueueRef.current.length > 0) {
      const fn = patchQueueRef.current[0]; // peek — don't remove yet
      try {
        await fn();
        patchQueueRef.current.shift(); // remove only after confirmed success
      } catch {
        break; // network gone — leave item at front, stop until reconnect
      }
    }
    flushingRef.current = false;
  }, []);

  // Retry queued saves when connectivity returns; track offline state for banner
  useEffect(() => {
    function handleOnline()  { setIsOffline(false); flushQueue(); }
    function handleOffline() { setIsOffline(true); }
    window.addEventListener('online',  handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online',  handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [flushQueue]);

  // Save response (debounced via queue)
  const saveResponse = useCallback((questionNumber: number, data: {
    selectedAnswer?: string | null;
    flagged?: boolean;
    additionalTimeMs?: number;
  }) => {
    patchQueueRef.current.push(() =>
      fetch(`/api/mock-tests/${testId}/response`, {
        method: 'PATCH',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ questionNumber, ...data }),
      }).then((res) => { if (!res.ok) throw new Error(`PATCH failed: ${res.status}`); })
    );
    flushQueue();
  }, [testId, flushQueue]);

  // Navigate to a question
  function navigateTo(num: number) {
    if (!test || num < 1 || num > test.totalQuestions) return;
    // Track time on current question — always record (even sub-second)
    const elapsed = Date.now() - questionStartRef.current;
    if (elapsed > 0) {
      saveResponse(currentNumRef.current, { additionalTimeMs: elapsed });
    }
    questionStartRef.current = Date.now();
    currentNumRef.current = num;
    setCurrentNum(num);
  }

  // Select answer
  function selectAnswer(questionNumber: number, answer: AnswerKey) {
    // Compute toggle from current state once so both UI and server get the same value
    const current = responses.find((r) => r.questionNumber === questionNumber);
    const newSelection = current?.selectedAnswer === answer ? null : answer;
    setResponses((prev) => prev.map((r) =>
      r.questionNumber === questionNumber ? { ...r, selectedAnswer: newSelection } : r,
    ));
    saveResponse(questionNumber, { selectedAnswer: newSelection });
  }

  // Toggle flag
  function toggleFlag(questionNumber: number) {
    // Compute toggle from current state once so both UI and server get the same value
    const current = responses.find((r) => r.questionNumber === questionNumber);
    const newFlagged = !current?.flagged;
    setResponses((prev) => prev.map((r) =>
      r.questionNumber === questionNumber ? { ...r, flagged: newFlagged } : r,
    ));
    saveResponse(questionNumber, { flagged: newFlagged });
  }

  // Submit
  async function handleSubmit() {
    setShowSubmitModal(false);
    setSubmitting(true);
    setSubmitError('');
    // Drain any queued answer saves first
    await flushQueue();
    // Record final time on current question
    const elapsed = Date.now() - questionStartRef.current;
    if (elapsed > 0) {
      await fetch(`/api/mock-tests/${testId}/response`, {
        method: 'PATCH',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ questionNumber: currentNumRef.current, additionalTimeMs: elapsed }),
      }).catch((err) => logError('[test/submit] save final time', err));
    }
    try {
      const res = await fetch(`/api/mock-tests/${testId}/submit`, { method: 'POST' });
      if (!res.ok) throw new Error('Submission failed');
      router.push(`/test/${testId}/results`);
    } catch {
      setSubmitError('Failed to submit — please check your connection and try again.');
      setSubmitting(false);
    }
  }

  if (loading || !test) {
    return (
      <div className="min-h-screen bg-paper flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="w-12 h-12 border-4 border-line border-t-action rounded-full animate-spin mx-auto" />
          <p className="text-ink-muted font-semibold">Loading your test…</p>
        </div>
      </div>
    );
  }

  const currentResponse = responses.find((r) => r.questionNumber === currentNum);
  const currentQuestion = currentResponse?.question;
  if (!currentResponse || !currentQuestion) return null;

  const answered   = responses.filter((r) => r.selectedAnswer).length;
  const totalQ     = test.totalQuestions;

  // Timer color: red < 1 min, amber 1–5 min, orange 5–10 min, gray otherwise
  const timerColor =
    remaining !== null && remaining <= 60_000   ? 'text-hint-ink bg-hint rounded-full px-2 py-0.5' :
    remaining !== null && remaining <= 300_000  ? 'text-hint-ink bg-hint rounded-full px-2 py-0.5' :
    remaining !== null && remaining <= 600_000  ? 'text-hint-ink bg-hint rounded-full px-2 py-0.5' :
    'text-ink';
  const timerPulse = remaining !== null && remaining <= 60_000 ? 'animate-pulse' : '';

  const options: Array<{ key: AnswerKey; text: string }> = [
    { key: 'A', text: currentQuestion.option1 },
    { key: 'B', text: currentQuestion.option2 },
    { key: 'C', text: currentQuestion.option3 },
    { key: 'D', text: currentQuestion.option4 },
  ];

  return (
    <div className="min-h-screen bg-paper flex flex-col max-w-lg mx-auto animate-fade-in">
      {/* ── Top bar ─────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-50 bg-white border-b-2 border-ink px-4 py-3 flex items-center gap-3">
        {/* Exit test */}
        <button
          onClick={() => setShowQuitModal(true)}
          className="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-tile bg-soft border-2 border-line hover:border-ink transition-colors flex-shrink-0"
          aria-label="Exit test"
        >
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" className="text-ink">
            <path d="M4.5 4.5l9 9M13.5 4.5l-9 9" />
          </svg>
        </button>

        {/* Progress bar */}
        <div className="flex-1 h-3 ui-meter">
          <div
            className="h-full bg-action rounded-full transition-[width] duration-500"
            style={{ width: `${(answered / totalQ) * 100}%` }}
          />
        </div>

        {/* Q counter — show as "done" count to avoid confusion with score */}
        <span className="text-xs font-extrabold text-ink-muted flex-shrink-0">✎ {answered}/{totalQ}</span>

        {/* Timer */}
        {remaining !== null && (
          <div className={`flex items-center gap-1 font-extrabold text-sm flex-shrink-0 ${timerColor} ${timerPulse}`}>
            ⏱ {formatTime(remaining)}
          </div>
        )}
      </div>

      {/* Offline banner */}
      {isOffline && (
        <div className="bg-hint text-hint-ink text-xs font-extrabold text-center py-1.5 px-4 flex-shrink-0">
          ⚠️ No internet — answers queued, will sync on reconnect
        </div>
      )}

      {/* Submit error banner */}
      {submitError && (
        <div className="bg-retry-soft text-retry text-xs font-extrabold text-center py-1.5 px-4 flex-shrink-0">
          {submitError}
        </div>
      )}

      {/* ── Question area ────────────────────────────────────────────────── */}
      <div className="flex-1 px-4 pt-4 pb-24 overflow-y-auto">
        {/* Q# + topic + flag */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold text-ink bg-soft border-2 border-line rounded-full px-3 py-1">
              Q{currentNum}
            </span>
            <span className="text-xs text-ink-muted font-semibold">{currentQuestion.difficulty}</span>
          </div>
          <button
            onClick={() => toggleFlag(currentNum)}
            className={`flex items-center gap-1 text-xs font-extrabold px-3 py-1 rounded-full border-2 transition-colors ${
              currentResponse.flagged
                ? 'bg-hint border-hint-ink text-hint-ink'
                : 'bg-white border-line text-ink-muted hover:border-hint-ink hover:text-hint-ink'
            }`}
          >
            🚩 {currentResponse.flagged ? 'Flagged' : 'Flag'}
          </button>
        </div>

        {/* Question text */}
        <div className="bg-white border-2 border-ink shadow-hard-lg rounded-card p-4 mb-4">
          <p className="text-ink text-question">
            {currentQuestion.questionText}
          </p>
          {currentQuestion.questionLatex && (
            <div className="mt-2">
              <KatexRenderer latex={currentQuestion.questionLatex} />
            </div>
          )}
          {/* Diagram (if this question has an associated figure) */}
          <QuestionDiagram questionId={currentQuestion.id} />
        </div>

        {/* Options */}
        <div className="space-y-3">
          {options.map(({ key, text }) => {
            const isSelected = currentResponse.selectedAnswer === key;
            return (
              <button
                key={key}
                onClick={() => selectAnswer(currentNum, key)}
                className={`w-full text-left rounded-control p-4 border-2 font-bold text-base transition-[colors,border-color,transform] duration-150 active:scale-[0.98] min-h-[56px] flex items-center gap-3 ${
                  isSelected
                    ? 'bg-soft border-action text-ink'
                    : 'bg-white border-line text-ink hover:border-ink'
                }`}
              >
                <span className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-sm font-extrabold border-2 ${
                  isSelected
                    ? 'bg-action border-action text-white'
                    : 'bg-soft border-line text-ink'
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
      <div className="fixed bottom-0 left-0 right-0 z-[60] bg-white border-t-2 border-ink pb-[env(safe-area-inset-bottom)]">
      <div className="max-w-lg mx-auto px-4 py-3 flex gap-3">
        <button
          onClick={() => navigateTo(currentNum - 1)}
          disabled={currentNum === 1}
          className="min-h-[48px] px-4 rounded-control border-2 border-ink bg-white shadow-hard-sm font-extrabold text-ink disabled:opacity-30 hover:bg-soft transition-colors"
        >
          ←
        </button>

        <button
          onClick={() => setShowNavigator(true)}
          className="flex-1 min-h-[48px] rounded-control border-2 border-ink bg-white shadow-hard-sm font-bold text-ink hover:bg-soft transition-colors text-sm"
        >
          Q{currentNum}/{totalQ} · {answered} answered
        </button>

        {currentNum === totalQ ? (
          <button
            onClick={() => setShowSubmitModal(true)}
            className="min-h-[48px] px-4 rounded-control bg-action border-2 border-ink shadow-hard-sm font-extrabold text-white text-sm"
          >
            Submit ✓
          </button>
        ) : (
          <button
            onClick={() => navigateTo(currentNum + 1)}
            className="min-h-[48px] px-5 rounded-control bg-action border-2 border-ink shadow-hard-sm font-extrabold text-white text-sm"
          >
            Next →
          </button>
        )}
      </div>
      </div>

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

      {/* Quit confirmation modal */}
      {showQuitModal && (
        <div className="fixed inset-0 z-[90] bg-black/60 flex items-center justify-center px-4">
          <div className="bg-white rounded-card border-2 border-ink p-6 w-full max-w-sm space-y-4 shadow-hard-lg">
            <h3 className="text-heading text-ink text-center">Leave the test?</h3>
            <p className="text-ink-muted text-sm text-center">
              Your progress is saved — you can resume from where you left off.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowQuitModal(false)}
                className="flex-1 min-h-[48px] rounded-control border-2 border-ink bg-white shadow-hard-sm font-extrabold text-ink hover:bg-soft transition-colors"
              >
                Keep going
              </button>
              <button
                onClick={() => router.push('/test')}
                className="flex-1 min-h-[48px] rounded-control bg-ink border-2 border-ink font-extrabold text-white hover:bg-gray-700 transition-colors"
              >
                Leave
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Submitting overlay */}
      {submitting && (
        <div className="fixed inset-0 z-[100] bg-white/90 flex items-center justify-center">
          <div className="text-center space-y-3">
            <div className="w-12 h-12 border-4 border-line border-t-action rounded-full animate-spin mx-auto" />
            <p className="font-extrabold text-ink">Grading your test…</p>
          </div>
        </div>
      )}
    </div>
  );
}
