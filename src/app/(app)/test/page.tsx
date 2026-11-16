'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { logError } from '@/lib/logger';
import DuoButton from '@/components/DuoButton';
import { useStudent } from '@/components/shell/StudentProvider';

// Three kinds of test, and no more:
//   quick  a short check across many topics
//   ipm    a full mock built to the shape of the real paper
//   pyq    a real past paper for the child's grade, in the paper's own order

// ── What the server tells this page ───────────────────────────────────────────

interface OpenTest {
  testId: string;
  type: string;
  totalQuestions: number;
  answered: number;
}

interface PastPaper {
  year: number;
  /** Questions of this paper held in the bank. */
  questions: number;
  /** Questions on the real paper. */
  fullSize: number;
  minutes: number;
}

interface TestsInfo {
  grade?: number;
  pastPapers?: PastPaper[];
  inProgress?: OpenTest | null;
}

interface StartBody {
  type: 'quick' | 'ipm' | 'pyq';
  year?: number;
}

type Busy = 'quick' | 'ipm' | number | null;

function testLabel(type: string): string {
  if (type === 'quick') return 'quick test';
  if (type === 'ipm') return 'full mock';
  if (type === 'pyq') return 'past paper';
  return 'test';
}

/** What the full mock promises, said only as strongly as it is true for the grade. */
function mockPromise(grade: number): string {
  if (grade === 5) return 'Built like the real paper: two questions from every chapter.';
  if (grade === 4) return 'Topics balanced the way the real papers balance them.';
  return 'Covers every topic of your grade.';
}

// ── Component ──────────────────────────────────────────────────────────────────

export default function TestConfigPage() {
  const router = useRouter();
  const { student } = useStudent();

  const [grade,        setGrade]        = useState<number>(student ? student.grade : 4);
  const [pastPapers,   setPastPapers]   = useState<PastPaper[] | null>(null);
  const [openTest,     setOpenTest]     = useState<OpenTest | null>(null);
  const [pendingStart, setPendingStart] = useState<StartBody | null>(null);
  const [busy,         setBusy]         = useState<Busy>(null);
  const [ending,       setEnding]       = useState(false);
  const [error,        setError]        = useState('');

  // The child's grade, the real papers that grade can sit, and any test still open.
  useEffect(() => {
    if (!localStorage.getItem('mathspark_student_id')) { router.replace('/start'); return; }
    let alive = true;
    fetch('/api/mock-tests')
      .then((r) => (r.ok ? r.json() : null))
      .then((data: TestsInfo | null) => {
        if (!alive) return;
        if (!data) { setPastPapers([]); return; }
        if (typeof data.grade === 'number') setGrade(data.grade);
        setPastPapers(Array.isArray(data.pastPapers) ? data.pastPapers : []);
        if (data.inProgress) setOpenTest(data.inProgress);
      })
      .catch((err) => {
        logError('[test] could not load the tests', err);
        if (alive) setPastPapers([]);
      });
    return () => { alive = false; };
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  // Creates a test and opens it. `replace` ends the open test first.
  async function createTest(body: StartBody, replace: boolean) {
    setError('');
    try {
      const res = await fetch('/api/mock-tests', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(replace ? { type: body.type, year: body.year, replace: true } : body),
      });
      if (!res.ok) {
        const failure = await res.json().catch(() => null);
        if (res.status === 401) throw new Error('Session expired — please log in again.');
        if (res.status === 429) throw new Error('Too many tests created. Wait a minute and try again.');
        throw new Error(failure?.error || "We couldn't set up that test. Please try again.");
      }
      const { testId } = await res.json();
      router.push(`/test/${testId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "We couldn't finish that. Please try again!");
      setBusy(null);
    }
  }

  // A test is already open: ask before swapping it for a new one.
  function start(body: StartBody) {
    if (busy !== null) return;
    if (openTest) {
      setPendingStart(body);
      return;
    }
    setBusy(body.type === 'pyq' && body.year ? body.year : body.type === 'ipm' ? 'ipm' : 'quick');
    createTest(body, false);
  }

  // End the open test without a score.
  async function endOpenTest() {
    if (!openTest) return;
    setEnding(true);
    setError('');
    try {
      const res = await fetch(`/api/mock-tests/${openTest.testId}/abandon`, { method: 'POST' });
      if (!res.ok) throw new Error('abandon was not accepted');
      setOpenTest(null);
    } catch (err) {
      logError('[test] end open test', err);
      setError("We couldn't end that test just now. Please check your connection and try again.");
    }
    setEnding(false);
  }

  // From the dialog: end the open test and start the one that was asked for.
  async function endAndStartPending() {
    const body = pendingStart;
    if (!body) return;
    setEnding(true);
    setPendingStart(null);
    setOpenTest(null);
    await createTest(body, true);
    setEnding(false);
  }

  const somePaperIsShort = !!pastPapers && pastPapers.some((p) => p.questions < p.fullSize);

  return (
    <div className="min-h-screen bg-paper pb-28">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link
          href="/practice"
          className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center"
          aria-label="Back"
        >
          &larr;
        </Link>
        <div>
          <h1 className="text-white text-title">Tests</h1>
          <p className="text-white/70 text-xs font-bold">Timed · No hints · Your score at the end</p>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-4">

        {/* ── A test still open: carry on with it, or end it ───────────────── */}
        {openTest && (
          <div className="bg-hint border-2 border-ink rounded-card p-4 space-y-3">
            <div>
              <p className="text-ink font-extrabold text-sm">You have a {testLabel(openTest.type)} open</p>
              <p className="text-ink-muted text-xs font-semibold mt-0.5">
                {`${openTest.answered} of ${openTest.totalQuestions} answered · the clock is still running`}
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => router.push(`/test/${openTest.testId}`)}
                disabled={ending}
                className="flex-1 min-h-[48px] rounded-control bg-action border-2 border-ink shadow-hard-sm font-extrabold text-white disabled:opacity-60"
              >
                Carry on
              </button>
              <button
                onClick={() => { endOpenTest(); }}
                disabled={ending}
                className="flex-1 min-h-[48px] rounded-control bg-white border-2 border-ink font-extrabold text-ink disabled:opacity-60"
              >
                {ending ? 'Ending…' : 'End it'}
              </button>
            </div>
          </div>
        )}

        {error && <p className="text-ink text-sm text-center font-semibold">{error}</p>}

        {/* ── 1. Quick test ─────────────────────────────────────────────────── */}
        <section className="bg-white border-2 border-line rounded-card p-4 space-y-3">
          <div className="flex items-start gap-3">
            <span className="text-2xl" aria-hidden="true">⚡</span>
            <div className="flex-1 min-w-0">
              <h2 className="text-title text-ink">Quick test</h2>
              <p className="text-ink-muted text-sm font-bold">15 questions · 20 minutes</p>
              <p className="text-ink-muted text-sm font-medium mt-1">One question each from 15 different topics.</p>
            </div>
          </div>
          <DuoButton variant="green" fullWidth loading={busy === 'quick'} onClick={() => start({ type: 'quick' })}>
            Start quick test
          </DuoButton>
        </section>

        {/* ── 2. Full mock ──────────────────────────────────────────────────── */}
        <section className="bg-white border-2 border-line rounded-card p-4 space-y-3">
          <div className="flex items-start gap-3">
            <span className="text-2xl" aria-hidden="true">🎯</span>
            <div className="flex-1 min-w-0">
              <h2 className="text-title text-ink">Full mock</h2>
              <p className="text-ink-muted text-sm font-bold">40 questions · 60 minutes</p>
              <p className="text-ink-muted text-sm font-medium mt-1">{mockPromise(grade)}</p>
            </div>
          </div>
          <DuoButton variant="blue" fullWidth loading={busy === 'ipm'} onClick={() => start({ type: 'ipm' })}>
            Start full mock
          </DuoButton>
        </section>

        {/* ── 3. Past papers ────────────────────────────────────────────────── */}
        <section className="bg-white border-2 border-line rounded-card p-4 space-y-3">
          <div className="flex items-start gap-3">
            <span className="text-2xl" aria-hidden="true">📜</span>
            <div className="flex-1 min-w-0">
              <h2 className="text-title text-ink">Past papers</h2>
              <p className="text-ink-muted text-sm font-medium mt-1">
                {`The real questions from the actual IPM papers for Grade ${grade}, in the paper's own order.`}
              </p>
            </div>
          </div>

          {pastPapers === null ? (
            <div className="grid grid-cols-2 gap-3" aria-hidden="true">
              {[0, 1, 2, 3].map((i) => (
                <div key={i} className="h-[72px] rounded-control bg-soft border-2 border-line animate-pulse" />
              ))}
            </div>
          ) : pastPapers.length === 0 ? (
            <p className="text-ink-muted text-sm font-semibold">
              {`We don't have past papers for Grade ${grade} yet.`}
            </p>
          ) : (
            <>
              <div className="grid grid-cols-2 gap-3">
                {pastPapers.map((p) => (
                  <button
                    key={p.year}
                    onClick={() => start({ type: 'pyq', year: p.year })}
                    disabled={busy !== null}
                    className="min-h-[72px] rounded-control bg-white border-2 border-ink shadow-hard-sm p-3 text-left active:scale-[0.97] transition-transform disabled:opacity-60"
                  >
                    <span className="flex items-center justify-between">
                      <span className="text-ink font-extrabold text-base">{`IPM ${p.year}`}</span>
                      {busy === p.year ? (
                        <span className="inline-block w-4 h-4 border-2 border-line border-t-action rounded-full animate-spin" />
                      ) : (
                        <span className="text-action text-sm" aria-hidden="true">→</span>
                      )}
                    </span>
                    <span className="block text-ink-muted text-xs font-semibold mt-1">
                      {p.questions < p.fullSize
                        ? `${p.questions} of ${p.fullSize} questions · ${p.minutes} min`
                        : `${p.questions} questions · ${p.minutes} min`}
                    </span>
                  </button>
                ))}
              </div>
              {somePaperIsShort && (
                <p className="text-ink-muted text-xs font-medium">
                  Questions that need a picture are left out for now, so some papers are a little shorter than the real one.
                </p>
              )}
            </>
          )}
        </section>

        {/* Past results */}
        <Link
          href="/test/history"
          className="block w-full text-action text-sm font-extrabold text-center min-h-[48px] leading-[48px]"
        >
          See my past results →
        </Link>
      </div>

      {/* ── Starting a test while another is open ──────────────────────────── */}
      {pendingStart && openTest && (
        <div className="fixed inset-0 z-[90] bg-black/60 flex items-center justify-center px-4">
          <div className="bg-white rounded-card border-2 border-ink p-6 w-full max-w-sm space-y-4 shadow-hard-lg">
            <h3 className="text-heading text-ink text-center">You already have a test open</h3>
            <p className="text-ink-muted text-sm text-center">
              {`Your ${testLabel(openTest.type)} has ${openTest.answered} of ${openTest.totalQuestions} answered. Carry on with it, or end it (no score) and start the new one.`}
            </p>
            <button
              onClick={() => router.push(`/test/${openTest.testId}`)}
              className="w-full min-h-[48px] rounded-control bg-action border-2 border-ink shadow-hard-sm font-extrabold text-white"
            >
              Carry on with it
            </button>
            <button
              onClick={() => { endAndStartPending(); }}
              className="w-full min-h-[48px] rounded-control bg-white border-2 border-ink font-extrabold text-ink"
            >
              End it and start the new one
            </button>
            <button
              onClick={() => setPendingStart(null)}
              className="w-full min-h-[48px] font-extrabold text-ink-muted"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
