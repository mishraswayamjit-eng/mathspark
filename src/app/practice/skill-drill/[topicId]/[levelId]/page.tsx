'use client';

import { useEffect, useState, useCallback } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import QuestionCard from '@/components/QuestionCard';
import HintSystem from '@/components/HintSystem';
import StepByStep from '@/components/StepByStep';
import MisconceptionPopup from '@/components/MisconceptionPopup';
import Sparky from '@/components/Sparky';
import Confetti from '@/components/Confetti';
import { useSounds } from '@/hooks/useSounds';
import type { Question, AnswerKey, StepItem } from '@/types';

// ── Types ─────────────────────────────────────────────────────────────────────

interface DrillQuestion {
  questionNumber: number;
  difficulty: string;
  sourceId: string;
  questionText: string;
  questionLatex: string;
  options: { id: string; text: string }[];
  correctAnswer: string;
  hints: string[];
  stepByStep: { step: number; text: string; latex: string }[];
  misconceptions: Record<string, string>;
  progressPosition: number;
}

interface DrillSession {
  sessionId: string;
  topicId: string;
  levelId: string;
  sessionNumber: number;
  totalQuestions: number;
  passingScore: number;
  masteryScore: number;
  unlockNextLevel: number;
  questions: DrillQuestion[];
  answerKey: Record<string, string>;
}

interface SessionListItem {
  sessionId: string;
  topicId: string;
  levelId: string;
  sessionNumber: number;
  totalQuestions: number;
  passingScore: number;
  masteryScore: number;
  unlockNextLevel: number;
}

interface TopicInfo {
  topicId: string;
  displayName: string;
  icon: string;
  description: string;
  levels: Record<string, {
    levelId: string;
    name: string;
    label: string;
    color: string;
    sessionsAvailable: number;
  }>;
}

interface LevelMeta {
  label: string;
  emoji: string;
  description: string;
}

// ── Progress helpers ──────────────────────────────────────────────────────────

interface LevelProgress {
  bestScore: number;
  sessions: Record<string, number>;
  unlocked: boolean;
}

type DrillProgressMap = Record<string, Record<string, LevelProgress>>;

const STORAGE_KEY = 'mathspark_drill_progress';

function loadProgress(): DrillProgressMap {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw) as DrillProgressMap;
  } catch { /* ignore */ }
  return {};
}

function saveSessionScore(topicId: string, levelId: string, sessionNum: number, score: number): DrillProgressMap {
  const progress = loadProgress();
  if (!progress[topicId]) progress[topicId] = {};
  if (!progress[topicId][levelId]) progress[topicId][levelId] = { bestScore: 0, sessions: {}, unlocked: true };

  const lp = progress[topicId][levelId];
  const prevBest = lp.sessions[String(sessionNum)] ?? 0;
  if (score > prevBest) lp.sessions[String(sessionNum)] = score;
  lp.bestScore = Math.max(lp.bestScore, score);

  // Unlock next level if score >= unlockNextLevel (8)
  if (score >= 8) {
    const levels = ['L1', 'L2', 'L3', 'L4', 'L5'];
    const idx = levels.indexOf(levelId);
    if (idx >= 0 && idx < levels.length - 1) {
      const nextLevel = levels[idx + 1];
      if (!progress[topicId][nextLevel]) {
        progress[topicId][nextLevel] = { bestScore: 0, sessions: {}, unlocked: true };
      } else {
        progress[topicId][nextLevel].unlocked = true;
      }
    }
  }

  // Ensure L1 is always unlocked
  if (!progress[topicId]['L1']) {
    progress[topicId]['L1'] = { bestScore: 0, sessions: {}, unlocked: true };
  } else {
    progress[topicId]['L1'].unlocked = true;
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  return progress;
}

// ── Adapt question for QuestionCard ───────────────────────────────────────────

function adaptQuestion(q: DrillQuestion, sessionId: string): Question {
  const opts = q.options ?? [];
  return {
    id: q.sourceId || `${sessionId}_Q${q.questionNumber}`,
    topicId: '',
    subTopic: q.difficulty,
    difficulty: (q.difficulty === 'Easy' ? 'Easy' : q.difficulty === 'Hard' ? 'Hard' : 'Medium') as Question['difficulty'],
    questionText: q.questionText,
    questionLatex: q.questionLatex ?? '',
    option1: opts[0]?.text ?? '',
    option2: opts[1]?.text ?? '',
    option3: opts[2]?.text ?? '',
    option4: opts[3]?.text ?? '',
    correctAnswer: (q.correctAnswer ?? 'A') as AnswerKey,
    hint1: q.hints?.[0] ?? '',
    hint2: q.hints?.[1] ?? '',
    hint3: q.hints?.[2] ?? '',
    stepByStep: (q.stepByStep ?? []).map((s) => ({
      step: s.step,
      text: s.text,
      latex: s.latex,
    })) as StepItem[],
    misconceptionA: q.misconceptions?.A ?? '',
    misconceptionB: q.misconceptions?.B ?? '',
    misconceptionC: q.misconceptions?.C ?? '',
    misconceptionD: q.misconceptions?.D ?? '',
    source: 'skill_drill',
  };
}

// ── Score verdict ─────────────────────────────────────────────────────────────

function getVerdict(score: number, total: number, passing: number, mastery: number, unlock: number) {
  if (score >= mastery) return { label: 'MASTERED!', color: '#FF9600', emoji: '🏆', mood: 'celebrating' as const };
  if (score >= unlock) return { label: 'Level Unlocked!', color: '#58CC02', emoji: '🔓', mood: 'celebrating' as const };
  if (score >= passing) return { label: 'Passed!', color: '#58CC02', emoji: '✅', mood: 'happy' as const };
  if (score >= total / 2) return { label: 'Almost there!', color: '#FF9600', emoji: '💪', mood: 'encouraging' as const };
  return { label: 'Keep practicing!', color: '#FF4B4B', emoji: '🌱', mood: 'encouraging' as const };
}

// ── Phase types ───────────────────────────────────────────────────────────────

type Phase = 'sessions' | 'drill' | 'results';

// ── Page Component ────────────────────────────────────────────────────────────

export default function SkillDrillSessionPage() {
  const params = useParams<{ topicId: string; levelId: string }>();
  const topicId = params.topicId;
  const levelId = params.levelId;

  const { playCorrect, playWrong, playLevelUp, playStreak } = useSounds();

  // ── State ────────────────────────────────────────────────────────────────────
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [topicInfo, setTopicInfo] = useState<TopicInfo | null>(null);
  const [levelMeta, setLevelMeta] = useState<Record<string, LevelMeta>>({});
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [progress, setProgress] = useState<DrillProgressMap>({});

  // Drill state
  const [phase, setPhase] = useState<Phase>('sessions');
  const [activeSession, setActiveSession] = useState<DrillSession | null>(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [selected, setSelected] = useState<AnswerKey | null>(null);
  const [results, setResults] = useState<boolean[]>([]);
  const [hintLevel, setHintLevel] = useState(0);
  const [showConfetti, setShowConfetti] = useState(false);

  // ── Load sessions list ───────────────────────────────────────────────────────
  useEffect(() => {
    setProgress(loadProgress());

    Promise.all([
      fetch('/api/skill-drills').then((r) => { if (!r.ok) throw new Error('Skill drills fetch failed'); return r.json(); }),
      fetch(`/api/skill-drills?topic=${topicId}&level=${levelId}`).then((r) => { if (!r.ok) throw new Error('Session fetch failed'); return r.json(); }),
    ])
      .then(([topicsData, sessionsData]) => {
        const t = topicsData.topics?.[topicId] as TopicInfo | undefined;
        setTopicInfo(t ?? null);
        setLevelMeta(topicsData.meta?.levelLabels ?? {});
        setSessions(sessionsData.sessions ?? []);
      })
      .catch(() => setError('Failed to load drill data.'))
      .finally(() => setLoading(false));
  }, [topicId, levelId]);

  // ── Start a session ──────────────────────────────────────────────────────────
  const startSession = useCallback((sessionNum: number) => {
    setLoading(true);
    fetch(`/api/skill-drills?topic=${topicId}&level=${levelId}&session=${sessionNum}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((d: { session: DrillSession }) => {
        if (d.session) {
          setActiveSession(d.session);
          setPhase('drill');
          setCurrentIdx(0);
          setAnswered(false);
          setSelected(null);
          setResults([]);
          setHintLevel(0);
        } else {
          setError('Session not found.');
        }
      })
      .catch(() => setError('Failed to load session.'))
      .finally(() => setLoading(false));
  }, [topicId, levelId]);

  // ── Answer handler ───────────────────────────────────────────────────────────
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

  // ── Next question ────────────────────────────────────────────────────────────
  const handleNext = useCallback(() => {
    if (!activeSession) return;
    const nextIdx = currentIdx + 1;

    if (nextIdx >= activeSession.questions.length) {
      // Done — calculate score and save
      const score = results.filter(Boolean).length;
      const updated = saveSessionScore(topicId, levelId, activeSession.sessionNumber, score);
      setProgress(updated);

      if (score >= activeSession.masteryScore) {
        setShowConfetti(true);
        playLevelUp();
      } else if (score >= activeSession.passingScore) {
        playStreak();
      }
      setPhase('results');
    } else {
      setCurrentIdx(nextIdx);
      setAnswered(false);
      setSelected(null);
      setHintLevel(0);
    }
  }, [activeSession, currentIdx, results, topicId, levelId, playLevelUp, playStreak]);

  // ── Level navigation ─────────────────────────────────────────────────────────
  const allLevels = ['L1', 'L2', 'L3', 'L4', 'L5'];
  const currentLevelIdx = allLevels.indexOf(levelId);

  // ── Render ───────────────────────────────────────────────────────────────────

  const levelInfo = topicInfo?.levels?.[levelId];
  const ll = levelMeta[levelId];
  const topicName = topicInfo?.displayName ?? topicId;
  const topicIcon = topicInfo?.icon ?? '📘';

  // Loading
  if (loading && phase === 'sessions') {
    return (
      <div className="min-h-screen bg-gray-50 pb-24">
        <div className="bg-duo-dark px-4 py-4 flex items-center gap-3">
          <Link href="/practice/skill-drill" className="text-white/60 hover:text-white text-sm">&larr;</Link>
          <h1 className="text-white font-extrabold text-lg">Loading...</h1>
        </div>
        <div className="max-w-lg mx-auto px-4 pt-6 space-y-3">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-20" />
          ))}
        </div>
      </div>
    );
  }

  // Error
  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 px-6">
        <Sparky mood="thinking" size={64} />
        <p className="text-sm font-bold text-red-500">{error}</p>
        <Link href="/practice/skill-drill" className="text-sm text-blue-500 underline">Back to Topics</Link>
      </div>
    );
  }

  // ── RESULTS PHASE ────────────────────────────────────────────────────────────
  if (phase === 'results' && activeSession) {
    const score = results.filter(Boolean).length;
    const total = activeSession.totalQuestions;
    const verdict = getVerdict(score, total, activeSession.passingScore, activeSession.masteryScore, activeSession.unlockNextLevel);
    const pct = Math.round((score / total) * 100);

    return (
      <div className="min-h-screen flex flex-col items-center px-6 py-8 gap-5 max-w-lg mx-auto">
        {showConfetti && <Confetti onDone={() => setShowConfetti(false)} />}

        {/* Score circle */}
        <div className="relative mt-4">
          <svg width="140" height="140" viewBox="0 0 140 140">
            <circle cx="70" cy="70" r="58" stroke="#e5e7eb" strokeWidth="10" fill="none" />
            <circle
              cx="70" cy="70" r="58"
              stroke={verdict.color}
              strokeWidth="10"
              fill="none"
              strokeDasharray={2 * Math.PI * 58}
              strokeDashoffset={2 * Math.PI * 58 * (1 - pct / 100)}
              strokeLinecap="round"
              transform="rotate(-90 70 70)"
              style={{ transition: 'stroke-dashoffset 1s ease' }}
            />
            <text x="70" y="65" textAnchor="middle" fontSize="28" fontWeight="800" fill={verdict.color}>
              {score}/{total}
            </text>
            <text x="70" y="85" textAnchor="middle" fontSize="12" fill="#9ca3af">{pct}%</text>
          </svg>
        </div>

        {/* Verdict */}
        <div className="text-center space-y-1">
          <p className="text-3xl">{verdict.emoji}</p>
          <h2 className="text-xl font-extrabold" style={{ color: verdict.color }}>{verdict.label}</h2>
          <p className="text-xs font-medium text-gray-500">
            {ll?.emoji} {ll?.label} &middot; Session {activeSession.sessionNumber}
          </p>
        </div>

        {/* Scoring breakdown */}
        <div className="bg-white rounded-2xl p-4 border border-gray-100 w-full space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500 font-medium">Pass (7/10)</span>
            <span className={`font-bold ${score >= 7 ? 'text-duo-green' : 'text-gray-500'}`}>
              {score >= 7 ? '✓ Achieved' : `Need ${7 - score} more`}
            </span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500 font-medium">Unlock next (8/10)</span>
            <span className={`font-bold ${score >= 8 ? 'text-duo-green' : 'text-gray-500'}`}>
              {score >= 8 ? '🔓 Unlocked!' : `Need ${8 - score} more`}
            </span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500 font-medium">Mastery (9/10)</span>
            <span className={`font-bold ${score >= 9 ? 'text-duo-orange' : 'text-gray-500'}`}>
              {score >= 9 ? '🏆 Mastered!' : `Need ${9 - score} more`}
            </span>
          </div>
        </div>

        {/* Result dots */}
        <div className="flex gap-2 justify-center flex-wrap">
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

        {/* Sparky */}
        <div className="bg-purple-50 rounded-2xl px-4 py-3 flex items-start gap-3 border border-purple-200 w-full">
          <Sparky mood={verdict.mood} size={40} />
          <p className="text-sm font-semibold text-purple-800 pt-1">
            {score >= 9
              ? 'Amazing! You truly mastered this level!'
              : score >= 8
              ? 'Great work! You unlocked the next level!'
              : score >= 7
              ? 'Nice job! Try again to unlock the next level!'
              : 'Keep practicing! Every attempt makes you stronger!'}
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col gap-3 w-full mt-2">
          {score < activeSession.masteryScore && (
            <button
              onClick={() => startSession(activeSession.sessionNumber)}
              className="w-full bg-duo-blue hover:bg-[#0a8fd4] text-white font-extrabold py-3.5 rounded-2xl transition-colors"
            >
              Retry Session →
            </button>
          )}
          <button
            onClick={() => {
              setPhase('sessions');
              setActiveSession(null);
            }}
            className="w-full bg-duo-green hover:bg-duo-green-dark text-white font-extrabold py-3.5 rounded-2xl transition-colors"
          >
            Back to Sessions
          </button>
          {score >= 8 && currentLevelIdx < 4 && (
            <Link
              href={`/practice/skill-drill/${topicId}/${allLevels[currentLevelIdx + 1]}`}
              className="w-full bg-gradient-to-r from-yellow-400 to-orange-400 text-white font-extrabold py-3.5 rounded-2xl text-center transition-colors"
            >
              {levelMeta[allLevels[currentLevelIdx + 1]]?.emoji} Next Level →
            </Link>
          )}
        </div>
      </div>
    );
  }

  // ── DRILL PHASE ──────────────────────────────────────────────────────────────
  if (phase === 'drill' && activeSession) {
    if (loading) {
      return (
        <div className="min-h-screen flex flex-col items-center justify-center gap-4">
          <Sparky mood="thinking" size={64} />
          <p className="text-sm font-bold text-gray-500 animate-pulse">Loading drill...</p>
        </div>
      );
    }

    const q = activeSession.questions[currentIdx];
    const adapted = adaptQuestion(q, activeSession.sessionId);
    const totalQ = activeSession.questions.length;
    const progressPct = ((currentIdx + (answered ? 1 : 0)) / totalQ) * 100;
    const correctSoFar = results.filter(Boolean).length;

    return (
      <div className="min-h-screen flex flex-col px-4 py-6 max-w-lg mx-auto pb-28">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">{topicIcon}</span>
            <div>
              <h1 className="text-sm font-extrabold text-gray-800 leading-tight">{topicName}</h1>
              <p className="text-[10px] font-bold text-gray-500">
                {ll?.emoji} {ll?.label} &middot; Session {activeSession.sessionNumber}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs font-extrabold text-duo-green bg-green-50 px-2 py-1 rounded-full">
              {correctSoFar}✓
            </span>
            <button
              onClick={() => {
                if (confirm('Quit this drill? Your progress for this session won\'t be saved.')) {
                  setPhase('sessions');
                  setActiveSession(null);
                }
              }}
              className="text-gray-500 hover:text-gray-600 text-xs font-bold"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Progress bar */}
        <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4 overflow-hidden">
          <div
            className="h-2.5 rounded-full transition-[width] duration-500 ease-out"
            style={{ width: `${progressPct}%`, backgroundColor: levelInfo?.color ?? '#58CC02' }}
          />
        </div>

        {/* Question counter */}
        <p className="text-xs font-bold text-gray-500 mb-3 text-center">
          Question {currentIdx + 1} of {totalQ}
        </p>

        {/* Question card */}
        <QuestionCard
          question={adapted}
          answered={answered}
          selected={selected}
          onAnswer={handleAnswer}
        />

        {/* Feedback */}
        {answered && (
          <div className="mt-4 space-y-3">
            <div className={`rounded-2xl px-4 py-3 flex items-start gap-3 border ${
              selected === adapted.correctAnswer
                ? 'bg-green-50 border-green-200'
                : 'bg-red-50 border-red-200'
            }`}>
              <Sparky
                mood={selected === adapted.correctAnswer ? 'celebrating' : 'encouraging'}
                size={36}
              />
              <p className={`text-sm font-semibold pt-1 ${
                selected === adapted.correctAnswer ? 'text-green-700' : 'text-red-700'
              }`}>
                {selected === adapted.correctAnswer
                  ? ['Great job!', 'You got it!', 'Excellent!', 'Well done!', 'Awesome!'][currentIdx % 5]
                  : "Not quite — let's look at the solution!"}
              </p>
            </div>

            {/* Misconception */}
            {selected && selected !== adapted.correctAnswer && (() => {
              const misconKey = `misconception${selected}` as keyof typeof adapted;
              const misconText = adapted[misconKey] as string;
              const correctIdx = ['A', 'B', 'C', 'D'].indexOf(adapted.correctAnswer);
              const correctText = adapted[`option${correctIdx + 1}` as keyof typeof adapted] as string;
              return misconText ? (
                <MisconceptionPopup
                  text={misconText}
                  correctAnswer={adapted.correctAnswer}
                  correctText={correctText}
                />
              ) : null;
            })()}

            {/* Hints */}
            {hintLevel > 0 && (
              <HintSystem
                hint1={adapted.hint1}
                hint2={adapted.hint2}
                hint3={adapted.hint3}
                level={hintLevel}
                onLevelUp={setHintLevel}
              />
            )}

            {/* Steps */}
            {adapted.stepByStep.length > 0 && (
              <StepByStep steps={adapted.stepByStep} />
            )}

            {/* Next button */}
            <button
              onClick={handleNext}
              className="w-full text-white font-extrabold py-3.5 rounded-2xl transition-colors mt-2"
              style={{ backgroundColor: levelInfo?.color ?? '#1CB0F6' }}
            >
              {currentIdx + 1 >= totalQ ? 'See Results →' : 'Next →'}
            </button>
          </div>
        )}
      </div>
    );
  }

  // ── SESSIONS LIST PHASE ──────────────────────────────────────────────────────
  const topicProgress = progress[topicId] ?? {};
  const levelProgress = topicProgress[levelId];
  const isUnlocked = levelId === 'L1' || (levelProgress && levelProgress.unlocked);

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div
        className="px-4 py-4 flex items-center gap-3 shadow-md"
        style={{ backgroundColor: levelInfo?.color ?? '#131F24' }}
      >
        <Link href="/practice/skill-drill" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{topicIcon}</span>
            <h1 className="text-white font-extrabold text-lg leading-tight">{topicName}</h1>
          </div>
          <p className="text-white/60 text-xs font-medium mt-0.5">
            {ll?.emoji} {ll?.label} &middot; {levelInfo?.name ?? levelId}
          </p>
        </div>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Level tabs */}
        <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1">
          {allLevels.map((lvl) => {
            const li = topicInfo?.levels?.[lvl];
            if (!li || li.sessionsAvailable === 0) return null;
            const lm = levelMeta[lvl];
            const isActive = lvl === levelId;
            const tp = topicProgress[lvl];
            const unlocked = lvl === 'L1' || (tp && tp.unlocked);

            return (
              <Link
                key={lvl}
                href={unlocked ? `/practice/skill-drill/${topicId}/${lvl}` : '#'}
                className={`flex items-center gap-1 px-3 py-2 rounded-full border-2 shrink-0 transition-colors ${
                  isActive
                    ? 'text-white font-extrabold shadow-md'
                    : unlocked
                    ? 'bg-white text-gray-600 font-bold border-gray-200 hover:border-gray-400'
                    : 'bg-gray-100 text-gray-300 font-bold border-gray-200 cursor-not-allowed'
                }`}
                style={isActive ? { backgroundColor: li.color, borderColor: li.color } : {}}
                onClick={(e) => { if (!unlocked) e.preventDefault(); }}
              >
                <span className="text-sm">{lm?.emoji}</span>
                <span className="text-xs">{lm?.label}</span>
                {!unlocked && <span className="text-xs">🔒</span>}
              </Link>
            );
          })}
        </div>

        {/* Locked state */}
        {!isUnlocked && (
          <div className="flex flex-col items-center gap-4 py-12">
            <div className="text-6xl">🔒</div>
            <h2 className="text-lg font-extrabold text-gray-600">Level Locked</h2>
            <p className="text-sm text-gray-500 text-center max-w-xs">
              Score 8/10 or higher on the previous level to unlock {ll?.label}!
            </p>
            {currentLevelIdx > 0 && (
              <Link
                href={`/practice/skill-drill/${topicId}/${allLevels[currentLevelIdx - 1]}`}
                className="bg-duo-blue text-white font-extrabold px-6 py-3 rounded-2xl"
              >
                Go to {levelMeta[allLevels[currentLevelIdx - 1]]?.label} →
              </Link>
            )}
          </div>
        )}

        {/* Sessions grid */}
        {isUnlocked && (
          <>
            {/* Level description */}
            <div className="bg-white rounded-2xl p-4 border border-gray-100 mb-4 flex items-start gap-3">
              <Sparky mood="happy" size={36} />
              <div>
                <p className="text-sm font-bold text-gray-700">{ll?.description}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {sessions.length} sessions &middot; 10 questions each &middot; Score 7+ to pass
                </p>
              </div>
            </div>

            <div className="space-y-3">
              {sessions.map((s) => {
                const sessionBest = levelProgress?.sessions?.[String(s.sessionNumber)] ?? 0;
                const attempted = sessionBest > 0;
                const passed = sessionBest >= s.passingScore;
                const mastered = sessionBest >= s.masteryScore;

                return (
                  <button
                    key={s.sessionId}
                    onClick={() => startSession(s.sessionNumber)}
                    className="w-full bg-white rounded-2xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-[box-shadow,transform] active:scale-[0.98] text-left flex items-center gap-4"
                  >
                    {/* Session number circle */}
                    <div
                      className={`w-12 h-12 rounded-full flex items-center justify-center text-lg font-extrabold shrink-0 border-2 ${
                        mastered
                          ? 'bg-gradient-to-br from-yellow-300 to-orange-400 border-yellow-400 text-white'
                          : passed
                          ? 'bg-duo-green border-duo-green-dark text-white'
                          : attempted
                          ? 'bg-blue-100 border-blue-300 text-blue-600'
                          : 'bg-gray-100 border-gray-300 text-gray-500'
                      }`}
                    >
                      {mastered ? '★' : passed ? '✓' : s.sessionNumber}
                    </div>

                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-extrabold text-gray-800">Session {s.sessionNumber}</p>
                      <p className="text-xs text-gray-500 font-medium">
                        {s.totalQuestions} questions &middot;
                        {attempted
                          ? ` Best: ${sessionBest}/${s.totalQuestions}`
                          : ' Not attempted'}
                      </p>
                    </div>

                    {/* Status badge */}
                    <div className="shrink-0">
                      {mastered ? (
                        <span className="text-xs font-extrabold text-duo-orange bg-orange-50 px-2.5 py-1 rounded-full">Mastered</span>
                      ) : passed ? (
                        <span className="text-xs font-extrabold text-duo-green bg-green-50 px-2.5 py-1 rounded-full">Passed</span>
                      ) : attempted ? (
                        <span className="text-xs font-extrabold text-blue-500 bg-blue-50 px-2.5 py-1 rounded-full">Retry →</span>
                      ) : (
                        <span className="text-xs font-extrabold text-gray-500 bg-gray-50 px-2.5 py-1 rounded-full">Start →</span>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
