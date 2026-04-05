'use client';

import { MS_PER_DAY } from '@/lib/timeConstants';
import { useState, useCallback, useEffect, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import QuestionCard from '@/components/QuestionCard';
import ProgressBar from '@/components/ProgressBar';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import DuoButton from '@/components/DuoButton';
import SparkyBubble from '@/components/SparkyBubble';
import TopicSelectCard from '@/components/TopicSelectCard';
import { getTopicsForGrade } from '@/data/topicTree';
import type { Question, AnswerKey, DiagnosticAnswer } from '@/types';

// ── Diagnostic plan — grade-aware ─────────────────────────────────────────────

interface DiagnosticPlan {
  topicId: string;
  count: number;
}

function getDiagnosticPlan(grade: number): DiagnosticPlan[] {
  if (grade === 4) {
    // Top-5 exam-weight topics, 1 question each
    return [
      { topicId: 'ch01-05', count: 1 },
      { topicId: 'ch09-10', count: 1 },
      { topicId: 'ch07-08', count: 1 },
      { topicId: 'ch11',    count: 1 },
      { topicId: 'ch06',    count: 1 },
    ];
  }
  // All other grades: single grade pool, 5 questions
  return [{ topicId: `grade${grade}`, count: 5 }];
}

const TOTAL = 5;

const TOPIC_NAMES: Record<string, string> = {
  'ch01-05': 'Number System',
  'ch06':    'Factors & Multiples',
  'ch07-08': 'Fractions',
  'ch09-10': 'Operations & BODMAS',
  'ch11':    'Decimal Fractions',
  'ch13':    'Algebraic Expressions',
  'ch18':    'Angles',
  'ch19':    'Triangles',
  'ch20':    'Quadrilaterals',
  'grade2':  'Grade 2 IPM',
  'grade3':  'Grade 3 IPM',
  'grade4':  'Grade 4 IPM',
  'grade5':  'Grade 5 IPM',
  'grade6':  'Grade 6 IPM',
  'grade7':  'Grade 7 IPM',
  'grade8':  'Grade 8 IPM',
  'grade9':  'Grade 9 IPM',
};

const GRADE_EMOJI: Record<number, string> = {
  2: '🌱', 3: '🌿', 4: '🌳', 5: '🍀', 6: '⭐', 7: '🌟', 8: '🏆', 9: '🎯',
};

const GRADE_QUESTION_COUNTS: Record<number, string> = {
  2: '420+', 3: '520+', 4: '1,200+', 5: '680+',
  6: '720+', 7: '780+', 8: '850+',   9: '900+',
};

// ── Step types ────────────────────────────────────────────────────────────────

type Step =
  | 'welcome' | 'gradeSelect' | 'goal' | 'valueProp1'
  | 'confidentTopics' | 'focusTopics' | 'dailyGoal' | 'practiceTime'
  | 'valueProp2' | 'name' | 'pathReady' | 'quiz' | 'results' | 'displayName';

type Diff = 'Easy' | 'Medium' | 'Hard';

// Progress percentages for each step
const STEP_PROGRESS: Record<Step, number> = {
  welcome: 0, gradeSelect: 8, goal: 16, valueProp1: 24,
  confidentTopics: 36, focusTopics: 45, dailyGoal: 55, practiceTime: 65,
  valueProp2: 75, name: 82, pathReady: 90, quiz: 92, results: 100, displayName: 100,
};

function nextDiff(d: Diff, up: boolean): Diff {
  if (up)  return d === 'Easy' ? 'Medium' : 'Hard';
  return d === 'Hard' ? 'Medium' : 'Easy';
}

function useCountUp(target: number, active: boolean): number {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (!active) return;
    setValue(0);
    const step = Math.max(1, Math.ceil(target / 30));
    const id = setInterval(() => {
      setValue((v) => {
        const next = v + step;
        if (next >= target) { clearInterval(id); return target; }
        return next;
      });
    }, 40);
    return () => clearInterval(id);
  }, [target, active]);
  return value;
}

// ── Sparky witty responses ────────────────────────────────────────────────────

const GOAL_RESPONSES: Record<string, string> = {
  IPM:    'IPM warrior mode: activated! 💪',
  School: 'Ace every test — let\'s do this! 📝',
  Fun:    'Math is the best kind of fun! 🎲',
};

const DAILY_GOAL_RESPONSES: Record<number, string> = {
  10: 'That\'s ~50 questions a week! 🔥',
  15: 'That\'s ~75 questions a week! ⚡',
  20: 'That\'s ~100 questions a week — perfect! 🎯',
  30: 'That\'s ~150 questions a week — champion! 🏆',
};

const PRACTICE_TIME_RESPONSES: Record<string, string> = {
  Morning:   'Early bird catches the math worm! 🌅',
  Afternoon: 'The best time to sharpen your brain! ☀️',
  Evening:   'Wind down with some puzzles! 🌙',
};

function getConfidentResponse(count: number): string {
  if (count <= 1) return 'No worries, we\'ll find your strengths! 💡';
  if (count <= 3) return 'Nice! You\'ve got a solid base! 💪';
  return 'Wow, you\'re already a math whiz! 🌟';
}

// ── Onboarding progress bar ─────────────────────────────────────────────────

function OnboardingProgress({ step }: { step: Step }) {
  const pct = STEP_PROGRESS[step];
  return (
    <div className="fixed top-0 left-0 right-0 z-40 px-4 pt-3 pb-1 bg-transparent">
      <div className="w-full bg-white/20 rounded-full h-2 overflow-hidden">
        <div
          className="bg-duo-green h-2 rounded-full transition-[width] duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

// ── Page wrapper with consistent dark bg ──────────────────────────────────────

function OnboardingShell({ children, step, variant = 'dark' }: {
  children: React.ReactNode;
  step: Step;
  variant?: 'dark' | 'white' | 'gradient';
}) {
  const bg = variant === 'gradient'
    ? 'bg-gradient-to-b from-duo-dark to-[#1a7a20]'
    : variant === 'white'
      ? 'bg-white'
      : 'bg-duo-dark';

  return (
    <div className={`min-h-screen flex flex-col ${bg}`}>
      <OnboardingProgress step={step} />
      <div className="flex-1 flex flex-col items-center justify-center px-6 pt-10 pb-8">
        {children}
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// Page component
// ══════════════════════════════════════════════════════════════════════════════

export default function StartPage() {
  const router = useRouter();

  // ── Navigation state ──────────────────────────────────────────────────────
  const [step,          setStep]         = useState<Step>('welcome');
  const [selectedGrade, setSelectedGrade] = useState<number | null>(null);
  const [name,          setName]         = useState('');
  const [parentEmail,   setParentEmail]  = useState('');
  const [studentId,     setStudentId]    = useState<string | null>(null);
  const [loading,       setLoading]      = useState(false);
  const [error,         setError]        = useState('');
  const [pendingRoute,  setPendingRoute] = useState<'/home' | '/test'>('/home');
  const [displayName,   setDisplayName]  = useState('');
  const [avatarColor,   setAvatarColor]  = useState('#3B82F6');
  const [dnError,       setDnError]      = useState('');
  const [trialDaysLeft, setTrialDaysLeft] = useState<number | null>(null);
  const [trialExpiry,   setTrialExpiry]  = useState<string | null>(null);

  // ── Personalization state (collected before account creation) ──────────────
  const [goal,               setGoal]              = useState<string>('');
  const [confidentTopicIds,  setConfidentTopicIds] = useState<string[]>([]);
  const [focusTopicIds,      setFocusTopicIds]     = useState<string[]>([]);
  const [dailyGoal,          setDailyGoal]         = useState<number>(20);
  const [practiceTime,       setPracticeTime]      = useState<string>('');
  const [sparkyMessage,      setSparkyMessage]     = useState<string>('');

  // ── Diagnostic plan (set when grade confirmed) ─────────────────────────────
  const [activePlan, setActivePlan] = useState<DiagnosticPlan[]>([]);

  // ── Quiz state ─────────────────────────────────────────────────────────────
  const [question,     setQuestion]     = useState<Question | null>(null);
  const [answered,     setAnswered]     = useState(false);
  const [selected,     setSelected]     = useState<AnswerKey | null>(null);
  const [planIdx,      setPlanIdx]      = useState(0);
  const [countInTopic, setCountInTopic] = useState(0);
  const [difficulty,   setDifficulty]   = useState<Diff>('Medium');
  const [seenIds,      setSeenIds]      = useState<string[]>([]);
  const [answers,      setAnswers]      = useState<DiagnosticAnswer[]>([]);
  const [showConfetti, setShowConfetti] = useState(false);

  const totalCorrect = answers.filter((a) => a.isCorrect).length;
  const countUp      = useCountUp(totalCorrect, step === 'results');
  const xpCountUp    = useCountUp(50, step === 'results');

  // Grade-specific topics for topic selection steps
  const gradeTopics = useMemo(
    () => (selectedGrade ? getTopicsForGrade(selectedGrade) : []),
    [selectedGrade],
  );

  // ── Fetch one diagnostic question ─────────────────────────────────────────
  const fetchQuestion = useCallback(async (topicId: string, diff: Diff, seen: string[]) => {
    setLoading(true);
    setAnswered(false);
    setSelected(null);
    try {
      const params = new URLSearchParams({
        topicId,
        difficulty: diff,
        exclude: seen.join(','),
      });
      const res = await fetch(`/api/diagnostic?${params}`);
      if (!res.ok) { setQuestion(null); return; }
      setQuestion(await res.json());
    } finally {
      setLoading(false);
    }
  }, []);

  // ── Create student + start quiz ───────────────────────────────────────────
  async function handleCreateStudent() {
    if (!name.trim() || !selectedGrade) return;
    setLoading(true);
    setError('');
    try {
      const res = await fetch('/api/students', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          name:                 name.trim(),
          grade:                selectedGrade,
          parentEmail:          parentEmail.trim() || undefined,
          examName:             goal || undefined,
          focusTopics:          focusTopicIds.length > 0 ? focusTopicIds : undefined,
          confidentTopics:      confidentTopicIds.length > 0 ? confidentTopicIds : undefined,
          dailyGoalMins:        dailyGoal,
          preferredPracticeTime: practiceTime || undefined,
        }),
      });
      const student = await res.json();
      // Set httpOnly cookie for API auth
      await fetch('/api/student/session', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ studentId: student.id }),
      });
      // Keep localStorage for UI display only
      localStorage.setItem('mathspark_student_id',    student.id);
      localStorage.setItem('mathspark_student_name',  student.name);
      localStorage.setItem('mathspark_student_grade', String(selectedGrade));
      setStudentId(student.id);
      setDisplayName(name.trim().slice(0, 20));
      setAvatarColor(student.avatarColor ?? '#3B82F6');

      if (student.trialExpiresAt) {
        const days = Math.max(0, Math.ceil(
          (new Date(student.trialExpiresAt).getTime() - Date.now()) / MS_PER_DAY,
        ));
        setTrialDaysLeft(days);
        setTrialExpiry(new Date(student.trialExpiresAt).toLocaleDateString('en-IN', {
          day: 'numeric', month: 'long', year: 'numeric',
        }));
      }

      // Move to path ready celebration
      setStep('pathReady');
    } catch {
      setError('Something went wrong. Please try again!');
    } finally {
      setLoading(false);
    }
  }

  // ── Start the diagnostic quiz after path ready ─────────────────────────────
  async function startQuiz() {
    if (!selectedGrade) return;
    const plan = getDiagnosticPlan(selectedGrade);
    setActivePlan(plan);
    setStep('quiz');
    await fetchQuestion(plan[0].topicId, 'Medium', []);
  }

  // ── Handle answer ─────────────────────────────────────────────────────────
  async function handleAnswer(key: AnswerKey, isCorrect: boolean) {
    if (!question || answered || !studentId) return;
    setAnswered(true);
    setSelected(key);

    const newAnswers: DiagnosticAnswer[] = [
      ...answers,
      { topicId: activePlan[planIdx].topicId, questionId: question.id, isCorrect },
    ];
    setAnswers(newAnswers);

    fetch('/api/attempts', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({
        questionId: question.id,
        topicId:    question.topicId,
        selected:   key,
        isCorrect,
        hintUsed:   0,
      }),
    }).catch((err) => console.error('[fetch]', err));

    setTimeout(() => advance(isCorrect, newAnswers), 1200);
  }

  // ── Advance to next question or results ───────────────────────────────────
  async function advance(wasCorrect: boolean, currentAnswers: DiagnosticAnswer[]) {
    const newDiff  = nextDiff(difficulty, wasCorrect);
    const newCount = countInTopic + 1;
    const newSeen  = [...seenIds, question!.id];

    if (currentAnswers.length >= TOTAL || planIdx >= activePlan.length) {
      setShowConfetti(true);
      setStep('results');
      return;
    }

    let nextPlanIdx = planIdx;
    let nextCount   = newCount;

    if (newCount >= activePlan[planIdx].count) {
      nextPlanIdx = planIdx + 1;
      nextCount   = 0;
      if (nextPlanIdx >= activePlan.length) {
        setShowConfetti(true);
        setStep('results');
        return;
      }
    }

    setPlanIdx(nextPlanIdx);
    setCountInTopic(nextCount);
    setDifficulty(newDiff);
    setSeenIds(newSeen);
    await fetchQuestion(activePlan[nextPlanIdx].topicId, newDiff, newSeen);
  }

  function computeResults() {
    return activePlan.map(({ topicId }) => {
      const topicAnswers = answers.filter((a) => a.topicId === topicId);
      const correct = topicAnswers.filter((a) => a.isCorrect).length;
      const total   = topicAnswers.length;
      const status: 'Strong' | 'Learning' | 'NotYet' =
        total > 0 && correct === total ? 'Strong'   :
        correct > 0                    ? 'Learning' : 'NotYet';
      return { topicId, name: TOPIC_NAMES[topicId] ?? topicId, correct, total, status };
    });
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 1: Welcome
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'welcome') {
    return (
      <OnboardingShell step="welcome" variant="gradient">
        <div className="flex flex-col items-center text-center gap-8 animate-fade-in">
          <div className="animate-sparky-dance">
            <Sparky mood="celebrating" size={120} />
          </div>
          <div className="space-y-3">
            <h1 className="text-3xl font-extrabold text-white leading-tight">
              Let&apos;s build your math superpowers!
            </h1>
            <p className="text-white/80 text-lg leading-relaxed">
              Quick setup — takes about 2 minutes
            </p>
          </div>
          <div className="w-full max-w-sm space-y-3">
            <DuoButton variant="green" fullWidth onClick={() => setStep('gradeSelect')}>
              Let&apos;s Go!
            </DuoButton>
          </div>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 2: Grade Select
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'gradeSelect') {
    return (
      <OnboardingShell step="gradeSelect">
        <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-5 animate-fade-in">
          <div className="text-center space-y-1">
            <div className="text-5xl" aria-hidden="true">🎓</div>
            <h2 className="text-2xl font-extrabold text-gray-800">Which grade are you in?</h2>
            <p className="text-gray-500 text-sm font-medium">
              We&apos;ll personalise everything for you
            </p>
          </div>

          <div className="grid grid-cols-4 gap-2">
            {[2, 3, 4, 5, 6, 7, 8, 9].map((g) => (
              <button
                key={g}
                onClick={() => setSelectedGrade(g)}
                className={`flex flex-col items-center justify-center rounded-2xl py-3 px-2 border-2 transition-[colors,border-color,box-shadow,transform] active:scale-95 min-h-0 ${
                  selectedGrade === g
                    ? 'bg-duo-blue border-duo-blue-dark text-white shadow-md scale-105'
                    : 'bg-gray-50 border-gray-200 text-gray-700 hover:border-duo-blue'
                }`}
              >
                <span className="text-xl leading-none" aria-hidden="true">{GRADE_EMOJI[g]}</span>
                <span className="text-xs font-extrabold mt-1">Gr {g}</span>
                <span className="text-[10px] font-semibold opacity-60 mt-0.5">
                  {GRADE_QUESTION_COUNTS[g]}
                </span>
              </button>
            ))}
          </div>

          <DuoButton
            variant="green"
            fullWidth
            onClick={() => { if (selectedGrade) setStep('goal'); }}
            disabled={!selectedGrade}
          >
            Next
          </DuoButton>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 3: Goal — "What are you preparing for?"
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'goal') {
    const goals = [
      { label: 'IPM Exam',     value: 'IPM',    emoji: '🎯' },
      { label: 'School Maths', value: 'School', emoji: '📚' },
      { label: 'Just for Fun', value: 'Fun',    emoji: '🎲' },
    ];

    return (
      <OnboardingShell step="goal">
        <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-5 animate-fade-in">
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-extrabold text-gray-800">What are you preparing for?</h2>
          </div>

          {sparkyMessage && (
            <div className="flex justify-center">
              <SparkyBubble message={sparkyMessage} mood="encouraging" />
            </div>
          )}

          <div className="space-y-3">
            {goals.map((g) => (
              <button
                key={g.value}
                onClick={() => {
                  setGoal(g.value);
                  setSparkyMessage(GOAL_RESPONSES[g.value]);
                  setTimeout(() => { setSparkyMessage(''); setStep('valueProp1'); }, 1000);
                }}
                className={`flex items-center gap-3 w-full rounded-2xl px-5 py-4 border-2 transition-[colors,border-color,transform] active:scale-95 min-h-0 ${
                  goal === g.value
                    ? 'bg-duo-blue/10 border-duo-blue text-duo-blue-dark'
                    : 'bg-gray-50 border-gray-200 text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="text-2xl" aria-hidden="true">{g.emoji}</span>
                <span className="font-bold text-base">{g.label}</span>
              </button>
            ))}
          </div>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 4: Value Prop Interstitial 1
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'valueProp1') {
    return (
      <OnboardingShell step="valueProp1" variant="gradient">
        <div className="flex flex-col items-center text-center gap-8 animate-fade-in max-w-sm">
          <div className="animate-sparky-wave">
            <Sparky mood="encouraging" size={100} />
          </div>
          <div className="space-y-3">
            <h2 className="text-2xl font-extrabold text-white leading-tight">
              10,000+ questions from real exams
            </h2>
            <p className="text-white/80 text-base leading-relaxed">
              Practice with actual IPM papers from 2016–2025, topic-wise drills, and smart revision
            </p>
          </div>
          <DuoButton variant="white" fullWidth onClick={() => setStep('confidentTopics')}>
            Continue
          </DuoButton>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 5: Confident Topics — "Which topics feel easy?"
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'confidentTopics') {
    const toggleConfident = (id: string) => {
      setConfidentTopicIds((prev) =>
        prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id],
      );
    };

    return (
      <OnboardingShell step="confidentTopics">
        <div className="bg-white rounded-3xl p-6 w-full max-w-sm shadow-2xl space-y-4 animate-fade-in max-h-[85vh] overflow-y-auto">
          <div className="text-center space-y-1">
            <h2 className="text-xl font-extrabold text-gray-800">Which topics feel easy?</h2>
            <p className="text-gray-500 text-sm font-medium">Tap all that apply</p>
          </div>

          <SparkyBubble
            message={getConfidentResponse(confidentTopicIds.length)}
            mood="happy"
            size={40}
          />

          <div className="space-y-2">
            {gradeTopics.map((t) => (
              <TopicSelectCard
                key={t.id}
                emoji={t.emoji}
                name={t.name}
                selected={confidentTopicIds.includes(t.id)}
                onToggle={() => toggleConfident(t.id)}
              />
            ))}
          </div>

          <div className="space-y-2 pt-2">
            <DuoButton variant="green" fullWidth onClick={() => setStep('focusTopics')}>
              Next
            </DuoButton>
            <button
              onClick={() => { setConfidentTopicIds([]); setStep('focusTopics'); }}
              className="w-full text-center text-gray-500 text-sm font-semibold py-2 hover:text-gray-600 transition-colors"
              style={{ minHeight: 0 }}
            >
              Skip
            </button>
          </div>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 6: Focus Topics — "Which topics do you want to improve?"
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'focusTopics') {
    const toggleFocus = (id: string) => {
      setFocusTopicIds((prev) =>
        prev.includes(id) ? prev.filter((t) => t !== id) : [...prev, id],
      );
    };

    return (
      <OnboardingShell step="focusTopics">
        <div className="bg-white rounded-3xl p-6 w-full max-w-sm shadow-2xl space-y-4 animate-fade-in max-h-[85vh] overflow-y-auto">
          <div className="text-center space-y-1">
            <h2 className="text-xl font-extrabold text-gray-800">Which topics do you want to get better at?</h2>
            <p className="text-gray-500 text-sm font-medium">We&apos;ll focus extra practice here</p>
          </div>

          {focusTopicIds.length > 0 && (
            <SparkyBubble
              message="Great picks! We'll focus extra practice here. 🎯"
              mood="encouraging"
              size={40}
            />
          )}

          <div className="space-y-2">
            {gradeTopics.map((t) => (
              <TopicSelectCard
                key={t.id}
                emoji={t.emoji}
                name={t.name}
                selected={focusTopicIds.includes(t.id)}
                onToggle={() => toggleFocus(t.id)}
                muted={confidentTopicIds.includes(t.id)}
              />
            ))}
          </div>

          <div className="space-y-2 pt-2">
            <DuoButton variant="green" fullWidth onClick={() => setStep('dailyGoal')}>
              Next
            </DuoButton>
            <button
              onClick={() => { setFocusTopicIds([]); setStep('dailyGoal'); }}
              className="w-full text-center text-gray-500 text-sm font-semibold py-2 hover:text-gray-600 transition-colors"
              style={{ minHeight: 0 }}
            >
              Skip
            </button>
          </div>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 7: Daily Goal
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'dailyGoal') {
    const goals = [
      { mins: 10, label: '10 min', desc: 'Quick burst',    emoji: '⚡' },
      { mins: 15, label: '15 min', desc: 'Steady pace',    emoji: '🔥' },
      { mins: 20, label: '20 min', desc: 'Great habit',    emoji: '🎯', recommended: true },
      { mins: 30, label: '30 min', desc: 'Power session',  emoji: '🏆' },
    ];

    return (
      <OnboardingShell step="dailyGoal">
        <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-5 animate-fade-in">
          <div className="text-center space-y-1">
            <h2 className="text-xl font-extrabold text-gray-800">How much practice each day?</h2>
          </div>

          {sparkyMessage && (
            <div className="flex justify-center">
              <SparkyBubble message={sparkyMessage} mood="encouraging" />
            </div>
          )}

          <div className="grid grid-cols-2 gap-3">
            {goals.map((g) => (
              <button
                key={g.mins}
                onClick={() => {
                  setDailyGoal(g.mins);
                  setSparkyMessage(DAILY_GOAL_RESPONSES[g.mins]);
                  setTimeout(() => { setSparkyMessage(''); setStep('practiceTime'); }, 1000);
                }}
                className={`relative flex flex-col items-center gap-1 rounded-2xl px-4 py-4 border-2 transition-[colors,border-color,transform] active:scale-95 min-h-0 ${
                  dailyGoal === g.mins && sparkyMessage
                    ? 'bg-duo-green/10 border-duo-green text-duo-green-dark'
                    : 'bg-gray-50 border-gray-200 text-gray-700 hover:border-gray-300'
                }`}
              >
                {g.recommended && (
                  <span className="absolute -top-2.5 left-1/2 -translate-x-1/2 bg-duo-orange text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full uppercase tracking-wide">
                    Best
                  </span>
                )}
                <span className="text-2xl" aria-hidden="true">{g.emoji}</span>
                <span className="font-extrabold text-base">{g.label}</span>
                <span className="text-xs font-medium text-gray-500">{g.desc}</span>
              </button>
            ))}
          </div>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 8: Practice Time
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'practiceTime') {
    const times = [
      { label: 'Morning',   desc: 'Before school', emoji: '🌅' },
      { label: 'Afternoon', desc: 'After school',  emoji: '☀️' },
      { label: 'Evening',   desc: 'Before bed',    emoji: '🌙' },
    ];

    return (
      <OnboardingShell step="practiceTime">
        <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-5 animate-fade-in">
          <div className="text-center space-y-1">
            <h2 className="text-xl font-extrabold text-gray-800">When do you like to practice?</h2>
          </div>

          {sparkyMessage && (
            <div className="flex justify-center">
              <SparkyBubble message={sparkyMessage} mood="happy" />
            </div>
          )}

          <div className="space-y-3">
            {times.map((t) => (
              <button
                key={t.label}
                onClick={() => {
                  setPracticeTime(t.label);
                  setSparkyMessage(PRACTICE_TIME_RESPONSES[t.label]);
                  setTimeout(() => { setSparkyMessage(''); setStep('valueProp2'); }, 1000);
                }}
                className={`flex items-center gap-3 w-full rounded-2xl px-5 py-4 border-2 transition-[colors,border-color,transform] active:scale-95 min-h-0 ${
                  practiceTime === t.label && sparkyMessage
                    ? 'bg-duo-blue/10 border-duo-blue text-duo-blue-dark'
                    : 'bg-gray-50 border-gray-200 text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="text-2xl" aria-hidden="true">{t.emoji}</span>
                <div className="text-left">
                  <span className="font-bold text-base block">{t.label}</span>
                  <span className="text-xs text-gray-500 font-medium">{t.desc}</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 9: Value Prop Interstitial 2
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'valueProp2') {
    return (
      <OnboardingShell step="valueProp2" variant="gradient">
        <div className="flex flex-col items-center text-center gap-8 animate-fade-in max-w-sm">
          <div className="animate-sparky-bounce">
            <Sparky mood="thinking" size={100} />
          </div>
          <div className="space-y-3">
            <h2 className="text-2xl font-extrabold text-white leading-tight">
              Practice like the real exam
            </h2>
            <p className="text-white/80 text-base leading-relaxed">
              Timed mock tests, topic-wise drills, and smart revision — all personalised for you
            </p>
          </div>
          <DuoButton variant="white" fullWidth onClick={() => setStep('name')}>
            Continue
          </DuoButton>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 10: Name + Create Account
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'name') {
    return (
      <OnboardingShell step="name">
        <div className="relative bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-5 animate-fade-in">
          <div className="absolute -top-8 right-4 animate-sparky-wave">
            <Sparky mood="encouraging" size={64} />
          </div>
          <h2 className="text-2xl font-extrabold text-gray-800 text-center pt-4">
            What should I call you?
          </h2>

          <div>
            <input
              type="text"
              autoFocus
              value={name}
              onChange={(e) => { setName(e.target.value); setError(''); }}
              onKeyDown={(e) => e.key === 'Enter' && name.trim() && handleCreateStudent()}
              placeholder="Your first name"
              aria-label="Your first name"
              maxLength={30}
              className="w-full text-2xl font-bold text-center border-b-4 border-duo-blue bg-transparent outline-none py-2 text-gray-800 placeholder-gray-300"
            />
          </div>

          <details className="group">
            <summary className="text-xs font-extrabold text-gray-500 uppercase tracking-wide cursor-pointer select-none list-none flex items-center gap-1">
              <span className="text-gray-400 group-open:rotate-90 transition-transform">▶</span>
              Add parent email for reports
            </summary>
            <div className="mt-2 space-y-1">
              <input
                type="email"
                value={parentEmail}
                onChange={(e) => setParentEmail(e.target.value)}
                placeholder="parent@email.com"
                aria-label="Parent email"
                className="w-full border-2 border-gray-200 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-800 outline-none focus:border-duo-blue transition-colors"
              />
              <p className="text-xs text-gray-500 font-medium">For weekly progress reports</p>
            </div>
          </details>

          {error && <p className="text-duo-red text-sm text-center font-semibold">{error}</p>}

          <DuoButton variant="green" fullWidth onClick={handleCreateStudent} loading={loading} disabled={!name.trim()}>
            Continue
          </DuoButton>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 11: Path Ready — Celebration
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'pathReady') {
    // Show top focus topics (or first 3 grade topics) as path preview
    const pathTopics = focusTopicIds.length > 0
      ? gradeTopics.filter((t) => focusTopicIds.includes(t.id)).slice(0, 3)
      : gradeTopics.slice(0, 3);

    return (
      <OnboardingShell step="pathReady" variant="white">
        <div className="flex flex-col items-center text-center gap-6 animate-fade-in max-w-sm">
          <Confetti variant="full" onDone={() => {}} />

          <div className="animate-sparky-dance">
            <Sparky mood="celebrating" size={160} />
          </div>

          <div className="space-y-2">
            <h2 className="text-2xl font-extrabold text-gray-800">
              Your learning path is ready!
            </h2>
            <p className="text-gray-500 text-sm font-medium">
              Here&apos;s where we&apos;ll start
            </p>
          </div>

          {pathTopics.length > 0 && (
            <div className="w-full space-y-2">
              {pathTopics.map((t, i) => (
                <div
                  key={t.id}
                  className="flex items-center gap-3 bg-gray-50 rounded-2xl px-4 py-3 border-2 border-gray-100"
                >
                  <span className="text-lg font-extrabold text-duo-green w-7">{i + 1}</span>
                  <span className="text-xl" aria-hidden="true">{t.emoji}</span>
                  <span className="font-bold text-sm text-gray-700">{t.name}</span>
                </div>
              ))}
            </div>
          )}

          <DuoButton variant="green" fullWidth onClick={startQuiz}>
            Let&apos;s see how you do!
          </DuoButton>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 12: Diagnostic Quiz (5 questions)
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'quiz') {
    const qNum = answers.length + 1;
    const pct  = (answers.length / TOTAL) * 100;

    return (
      <div className="min-h-screen flex flex-col px-4 py-6 gap-4 bg-white">
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm text-gray-500 font-semibold">
            <span>Question {qNum} of {TOTAL}</span>
            <span>Quick check-in</span>
          </div>
          <ProgressBar value={pct} height="h-4" />
        </div>

        {loading ? (
          <div className="flex-1 flex flex-col items-center justify-center gap-4">
            <div className="animate-sparky-bounce">
              <Sparky mood="thinking" size={100} />
            </div>
            <p className="text-gray-500 font-semibold">Loading question…</p>
          </div>
        ) : question ? (
          <QuestionCard
            question={question}
            answered={answered}
            selected={selected}
            onAnswer={handleAnswer}
          />
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center gap-4">
            <p className="text-gray-500 font-semibold">Loading question…</p>
          </div>
        )}
      </div>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 14: Display Name + Avatar
  // ═══════════════════════════════════════════════════════════════════════════

  if (step === 'displayName') {
    const AVATAR_COLORS = [
      '#FF9600','#58CC02','#1CB0F6','#FF4B4B',
      '#9B59B6','#00BCD4','#FFC800','#FF69B4',
      '#3B82F6','#58CC02','#F59E0B','#EF4444',
    ];
    const initial = displayName ? displayName[0].toUpperCase() : (name[0] ?? '?').toUpperCase();

    const handleJoinLeague = async () => {
      const trimmed = displayName.trim().slice(0, 20) || name.trim().slice(0, 20);
      if (!trimmed) return;
      if (studentId) {
        await fetch('/api/student', {
          method: 'PATCH',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ displayName: trimmed, avatarColor }),
        }).catch((err) => console.error('[fetch]', err));
      }
      router.push(pendingRoute);
    };

    return (
      <OnboardingShell step="displayName">
        <div className="bg-white rounded-3xl p-8 w-full max-w-sm shadow-2xl space-y-5 animate-fade-in">
          <div className="text-center">
            <div
              className="w-20 h-20 rounded-full flex items-center justify-center text-3xl font-extrabold text-white mx-auto mb-3 border-4 border-white/30 shadow-lg"
              style={{ backgroundColor: avatarColor }}
            >
              {initial}
            </div>
            <h2 className="text-2xl font-extrabold text-gray-800">Join the League!</h2>
            <p className="text-gray-500 text-sm font-medium mt-1">
              Pick a leaderboard name and colour
            </p>
          </div>

          <div>
            <label htmlFor="leaderboard-name" className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">
              Your leaderboard name
            </label>
            <input
              id="leaderboard-name"
              type="text"
              autoFocus
              value={displayName}
              onChange={(e) => { setDisplayName(e.target.value); setDnError(''); }}
              onKeyDown={(e) => e.key === 'Enter' && handleJoinLeague()}
              placeholder={name.trim().slice(0, 20)}
              maxLength={20}
              className="w-full mt-1.5 text-xl font-bold text-center border-b-4 border-duo-blue bg-transparent outline-none py-2 text-gray-800 placeholder-gray-300"
            />
            {dnError && <p className="text-duo-red text-xs font-semibold text-center mt-1">{dnError}</p>}
          </div>

          <div>
            <label className="text-xs font-extrabold text-gray-500 uppercase tracking-wide">
              Avatar colour
            </label>
            <div className="flex flex-wrap gap-2 mt-2">
              {AVATAR_COLORS.map((c) => (
                <button
                  key={c}
                  onClick={() => setAvatarColor(c)}
                  className={`w-11 h-11 rounded-full transition-transform active:scale-95 flex items-center justify-center min-h-0 ${
                    avatarColor === c ? 'ring-4 ring-offset-2 ring-gray-800 scale-110' : ''
                  }`}
                >
                  <span className="w-9 h-9 rounded-full block" style={{ backgroundColor: c }} />
                </button>
              ))}
            </div>
          </div>

          <DuoButton variant="green" fullWidth onClick={handleJoinLeague} loading={loading}>
            Let&apos;s go!
          </DuoButton>
          <button
            onClick={() => router.push(pendingRoute)}
            style={{ minHeight: 0 }}
            className="w-full text-center text-gray-500 text-sm font-semibold py-1 hover:text-gray-600 transition-colors"
          >
            Skip for now
          </button>
        </div>
      </OnboardingShell>
    );
  }

  // ═══════════════════════════════════════════════════════════════════════════
  // Step 13: Results + Reward
  // ═══════════════════════════════════════════════════════════════════════════

  const results  = computeResults();
  const strong   = results.filter((r) => r.status === 'Strong');
  const learning = results.filter((r) => r.status === 'Learning');
  const notYet   = results.filter((r) => r.status === 'NotYet');

  return (
    <div className="min-h-screen px-4 py-8 flex flex-col gap-6 bg-white pb-12 animate-fade-in">
      {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

      {/* Hero */}
      <div className="text-center space-y-4">
        <div className="flex justify-center animate-sparky-dance">
          <Sparky mood="celebrating" size={120} />
        </div>
        <h2 className="text-2xl font-extrabold text-gray-800">
          Wow {name}, you already know so much!
        </h2>
        <div className="inline-flex items-baseline gap-2 bg-[#FFF9E6] border-2 border-duo-gold rounded-2xl px-6 py-3">
          <span className="text-4xl font-extrabold text-duo-dark tabular-nums">{countUp}</span>
          <span className="text-gray-600 font-semibold text-base">out of {TOTAL} correct!</span>
        </div>
      </div>

      {/* XP Reward Banner */}
      <div className="bg-gradient-to-r from-duo-gold/20 to-duo-orange/20 border-2 border-duo-gold rounded-2xl px-4 py-3 text-center">
        <p className="font-extrabold text-amber-800 text-lg">
          <span aria-hidden="true">⭐ </span>+{xpCountUp} XP Welcome Bonus!
        </p>
      </div>

      {/* Trial banner */}
      {trialDaysLeft !== null && trialDaysLeft > 0 && (
        <div className="bg-amber-50 border-2 border-duo-orange rounded-2xl px-4 py-3 text-center">
          <p className="font-extrabold text-amber-800 text-base">7-Day Pro Trial Activated!</p>
          <p className="text-amber-600 text-xs font-medium mt-0.5">
            Expires on {trialExpiry} · {trialDaysLeft} days left
          </p>
        </div>
      )}

      {/* Strong */}
      {strong.length > 0 && (
        <div>
          <h3 className="text-sm font-extrabold text-duo-green-dark uppercase tracking-wide mb-2">
            <span aria-hidden="true">✅ </span>You nailed it!
          </h3>
          <div className="space-y-2">
            {strong.map((r) => (
              <div key={r.topicId} className="bg-green-50 border-2 border-duo-green rounded-2xl px-4 py-3 flex justify-between items-center">
                <span className="font-bold text-gray-800">{r.name}</span>
                <span className="text-duo-green-dark font-extrabold">{r.correct}/{r.total}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Learning */}
      {learning.length > 0 && (
        <div>
          <h3 className="text-sm font-extrabold text-duo-orange-dark uppercase tracking-wide mb-2">
            <span aria-hidden="true">🟡 </span>Getting there!
          </h3>
          <div className="space-y-2">
            {learning.map((r) => (
              <div key={r.topicId} className="bg-amber-50 border-2 border-duo-orange rounded-2xl px-4 py-3 flex justify-between items-center">
                <span className="font-bold text-gray-800">{r.name}</span>
                <span className="text-duo-orange-dark font-extrabold">{r.correct}/{r.total}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Not Yet */}
      {notYet.length > 0 && (
        <div>
          <h3 className="text-sm font-extrabold text-gray-500 uppercase tracking-wide mb-2">
            <span aria-hidden="true">⬜ </span>Let&#39;s explore!
          </h3>
          <div className="space-y-2">
            {notYet.map((r) => (
              <div key={r.topicId} className="bg-gray-50 border-2 border-gray-200 rounded-2xl px-4 py-3 flex justify-between items-center">
                <span className="font-bold text-gray-800">{r.name}</span>
                <span className="text-gray-500 font-extrabold text-sm">
                  {r.total > 0 ? `${r.correct}/${r.total}` : 'Not tested yet'}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="space-y-3">
        <DuoButton variant="green" fullWidth onClick={() => { setPendingRoute('/home'); setStep('displayName'); }}>
          Start Learning
        </DuoButton>
        <DuoButton variant="blue" fullWidth onClick={() => { setPendingRoute('/test'); setStep('displayName'); }}>
          Take a Mock Test
        </DuoButton>
      </div>
    </div>
  );
}
