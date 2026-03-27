'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useFlashcardDeck } from '@/hooks/useFlashcardDeck';
import dynamic from 'next/dynamic';
import Confetti from '@/components/Confetti';
import Sparky from '@/components/Sparky';
import { XPPopup } from '@/components/flashcard/StreakMilestone';
import { useSounds } from '@/hooks/useSounds';
import { useConceptSuggestions } from '@/hooks/useConceptSuggestions';
import WhatsNextSheet from '@/components/WhatsNextSheet';
import type { FlashCard } from '@/types';
import type { WhatsNextSuggestion } from '@/lib/whatsNext';

const KatexRenderer = dynamic(() => import('@/components/KatexRenderer'), { ssr: false });

// ── Types ────────────────────────────────────────────────────────────────────

interface CardWithProgress extends FlashCard {
  leitnerBox: number;
  timesSeen: number;
  timesCorrect: number;
  streakOnCard: number;
}

interface BoxTransition {
  cardId: string;
  cardFront: string;
  oldBox: number;
  newBox: number;
  leveledUp: boolean;
  reachedMastery: boolean;
}

type Phase = 'loading' | 'prompt' | 'recording' | 'reveal' | 'complete';

const BOX_NAMES = ['New', 'Rookie', 'Rising', 'Strong', 'Expert', 'Master'];
const BOX_COLORS = ['#64748B', '#EF4444', '#F59E0B', '#3B82F6', '#8B5CF6', '#34D399'];
const THINK_TIME_MS = 15_000; // 15 seconds to think + speak
const PULSE_BARS = 12; // number of bars in the voice visualizer

// ── Microphone Visualizer ─────────────────────────────────────────────────────

function MicVisualizer({ active }: { active: boolean }) {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    if (!active) return;
    const id = setInterval(() => setTick((t) => t + 1), 150);
    return () => clearInterval(id);
  }, [active]);

  return (
    <div className="flex items-center justify-center gap-[3px] h-10">
      {Array.from({ length: PULSE_BARS }).map((_, i) => {
        // Deterministic pseudo-random from tick + index
        const h = active ? 12 + ((tick * 7 + i * 13) % 21) : 4;
        const l = active ? 55 + ((tick * 3 + i * 11) % 16) : 30;
        return (
          <div
            key={i}
            className="w-1 rounded-full transition-[height,background-color] duration-150"
            style={{
              height: `${h}px`,
              background: active ? `hsl(${160 + i * 8}, 80%, ${l}%)` : '#334155',
            }}
          />
        );
      })}
    </div>
  );
}

// ── Voice Complete Screen ────────────────────────────────────────────────────

function VoiceComplete({
  cardsReviewed,
  cardsCorrect,
  duration,
  transitions,
  sessionXP,
  onPlayAgain,
  onDone,
}: {
  cardsReviewed: number;
  cardsCorrect: number;
  duration: number;
  transitions: BoxTransition[];
  sessionXP: { total: number; streakMultiplier: number; streakBonus: number } | null;
  onPlayAgain: () => void;
  onDone: () => void;
  suggestions?: WhatsNextSuggestion[];
}) {
  const pct = cardsReviewed > 0 ? Math.round((cardsCorrect / cardsReviewed) * 100) : 0;
  const mins = Math.floor(duration / 60);
  const secs = duration % 60;
  const promoted = transitions.filter((t) => t.leveledUp);
  const mastered = transitions.filter((t) => t.reachedMastery);

  return (
    <div className="fixed inset-0 z-50 bg-[#0F172A] flex flex-col items-center justify-center px-6 animate-fade-in overflow-y-auto">
      {mastered.length > 0 && <Confetti />}

      <div className={pct >= 70 ? 'animate-sparky-dance' : 'animate-sparky-bounce'}>
        <Sparky mood={pct >= 70 ? 'celebrating' : pct >= 40 ? 'happy' : 'encouraging'} size={80} />
      </div>

      <h1 className="text-2xl font-black text-[#F1F5F9] mt-3 mb-1">
        {pct >= 80 ? 'Voice Master!' : pct >= 60 ? 'Great Recall!' : pct >= 40 ? 'Good Practice!' : 'Keep Speaking!'}
      </h1>
      <p className="text-sm text-[#94A3B8] mb-4">
        {pct >= 80
          ? 'Speaking answers out loud really works!'
          : pct >= 50
          ? 'Active recall is the best way to learn!'
          : 'The more you say it, the better you remember!'}
      </p>

      {/* XP */}
      {sessionXP && sessionXP.total > 0 && (
        <div className="flex items-center gap-1.5 mb-4 animate-pop-in">
          <span className="text-lg font-black text-[#34D399]">+{sessionXP.total} XP</span>
          {sessionXP.streakBonus > 0 && (
            <span className="text-[10px] text-[#FBBF24]">({sessionXP.streakMultiplier}x streak)</span>
          )}
        </div>
      )}

      {/* Stats grid */}
      <div className="grid grid-cols-3 gap-3 w-full max-w-xs mb-5">
        <div className="bg-[#1E293B] rounded-2xl p-3 text-center">
          <p className="text-2xl font-black text-[#F1F5F9] tabular-nums">{cardsReviewed}</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider mt-0.5">Cards</p>
        </div>
        <div className="bg-[#1E293B] rounded-2xl p-3 text-center">
          <p className="text-2xl font-black text-[#34D399] tabular-nums">{pct}%</p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider mt-0.5">Recalled</p>
        </div>
        <div className="bg-[#1E293B] rounded-2xl p-3 text-center">
          <p className="text-2xl font-black text-[#60A5FA] tabular-nums">
            {mins > 0 ? `${mins}m` : `${secs}s`}
          </p>
          <p className="text-[10px] text-[#64748B] uppercase tracking-wider mt-0.5">Time</p>
        </div>
      </div>

      {/* Transitions */}
      {promoted.length > 0 && (
        <div className="w-full max-w-xs bg-duo-green/10 border border-duo-green/20 rounded-xl px-3 py-2.5 mb-4">
          <p className="text-xs font-bold text-emerald-400 mb-1">
            ⬆️ {promoted.length} card{promoted.length > 1 ? 's' : ''} leveled up
          </p>
          {promoted.slice(0, 4).map((t) => (
            <div key={t.cardId} className="flex items-center gap-2 py-0.5">
              <span className="text-[10px] text-[#94A3B8] truncate flex-1">{t.cardFront}</span>
              <span
                className="text-[10px] font-bold px-1.5 py-0.5 rounded"
                style={{ color: BOX_COLORS[t.oldBox], background: BOX_COLORS[t.oldBox] + '20' }}
              >
                {BOX_NAMES[t.oldBox]}
              </span>
              <span className="text-[#64748B] text-[10px]">→</span>
              <span
                className="text-[10px] font-bold px-1.5 py-0.5 rounded"
                style={{ color: BOX_COLORS[t.newBox], background: BOX_COLORS[t.newBox] + '20' }}
              >
                {BOX_NAMES[t.newBox]}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* Buttons */}
      <div className="w-full max-w-xs space-y-3 pb-8">
        <button
          onClick={onPlayAgain}
          className="w-full py-3.5 rounded-2xl font-bold text-white text-sm"
          style={{ background: 'linear-gradient(135deg, #A78BFA, #7C3AED)' }}
        >
          Practice Again 🎙️
        </button>
        {suggestions && suggestions.length > 0 ? (
          <WhatsNextSheet suggestions={suggestions} />
        ) : (
          <button
            onClick={onDone}
            className="w-full py-3.5 rounded-2xl font-bold text-[#94A3B8] text-sm bg-[#1E293B]"
          >
            Done
          </button>
        )}
      </div>
    </div>
  );
}

// ── Main Voice Recall Component ─────────────────────────────────────────────

interface VoiceRecallSessionProps {
  deckId: string;
  conceptId?: string | null;
}

export default function VoiceRecallSession({ deckId, conceptId }: VoiceRecallSessionProps) {
  const router = useRouter();
  const { fetchDeck } = useFlashcardDeck(deckId);
  const { playCorrect, playWrong, playLevelUp, playMastery } = useSounds();

  const [phase, setPhase] = useState<Phase>('loading');
  const [cards, setCards] = useState<CardWithProgress[]>([]);
  const [deckName, setDeckName] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);

  // Stats
  const [completed, setCompleted] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [startTime] = useState(() => Date.now());
  const sessionSavedRef = useRef(false);

  // Recording state
  const [thinkTimer, setThinkTimer] = useState(THINK_TIME_MS);
  const thinkTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const [speechSupported, setSpeechSupported] = useState(false);

  // Celebrations
  const [transitions, setTransitions] = useState<BoxTransition[]>([]);
  const [showToast, setShowToast] = useState(false);
  const [toastIsMastery, setToastIsMastery] = useState(false);
  const [toastBox, setToastBox] = useState(0);

  // XP
  const [accumulatedXP, setAccumulatedXP] = useState(0);
  const [lastXP, setLastXP] = useState(0);
  const [xpTrigger, setXpTrigger] = useState(0);
  const accumulatedBonusRef = useRef(0);
  const [sessionXP, setSessionXP] = useState<{
    total: number; streakMultiplier: number; streakBonus: number;
  } | null>(null);

  // Concept journey suggestions
  const voiceAccuracy = completed > 0 ? Math.round((correctCount / completed) * 100) : 0;
  const whatsNextSuggestions = useConceptSuggestions(
    conceptId ?? null, 'flashcards', phase === 'complete', voiceAccuracy,
  );

  // ── Check Web Speech API support ─────────────────────────────────────────

  useEffect(() => {
    setSpeechSupported(!!(window.SpeechRecognition || window.webkitSpeechRecognition));
  }, []);

  // ── Load deck ────────────────────────────────────────────────────────────

  const loadDeck = useCallback(() => {
    fetchDeck()
      .then((data) => {
        if (!data || data.cards.length === 0) {
          setPhase('complete');
        } else {
          setCards(data.cards as CardWithProgress[]);
          setDeckName(data.deckName ?? 'Voice Recall');
          setPhase('prompt');
        }
      })
      .catch(() => router.replace('/flashcards'));
  }, [fetchDeck, router]);

  useEffect(() => { loadDeck(); }, [loadDeck]);

  // ── Speech Recognition helpers ───────────────────────────────────────────

  const startListening = useCallback(() => {
    if (!speechSupported) return;

    const SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionCtor) return;

    try {
      const recognition = new SpeechRecognitionCtor();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-IN';

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        let text = '';
        for (let i = 0; i < event.results.length; i++) {
          text += event.results[i][0].transcript;
        }
        setTranscript(text);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.start();
      recognitionRef.current = recognition;
      setIsListening(true);
    } catch {
      // Speech recognition not available in this context
      setIsListening(false);
    }
  }, [speechSupported]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch {}
      recognitionRef.current = null;
    }
    setIsListening(false);
  }, []);

  // ── Think timer ──────────────────────────────────────────────────────────

  useEffect(() => {
    if (phase !== 'recording') return;

    thinkTimerRef.current = setInterval(() => {
      setThinkTimer((prev) => {
        const next = prev - 100;
        if (next <= 0) {
          clearInterval(thinkTimerRef.current!);
          // Auto-reveal on timeout
          stopListening();
          setPhase('reveal');
          return 0;
        }
        return next;
      });
    }, 100);

    return () => {
      if (thinkTimerRef.current) clearInterval(thinkTimerRef.current);
    };
  }, [phase, stopListening]);

  // ── Transition: prompt → recording ───────────────────────────────────────

  const startRecording = useCallback(() => {
    setTranscript('');
    setThinkTimer(THINK_TIME_MS);
    setPhase('recording');
    startListening();
  }, [startListening]);

  // ── Transition: recording → reveal ───────────────────────────────────────

  const revealAnswer = useCallback(() => {
    if (thinkTimerRef.current) clearInterval(thinkTimerRef.current);
    stopListening();
    setPhase('reveal');
  }, [stopListening]);

  // ── Handle self-evaluation ───────────────────────────────────────────────

  const handleEvaluate = useCallback(
    (correct: boolean) => {
      const card = cards[currentIndex];
      if (!card) return;

      const sid = localStorage.getItem('mathspark_student_id');

      // Update Leitner progress
      if (sid) {
        fetch('/api/flashcards/progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ cardId: card.id, correct }),
        })
          .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
          .then((data) => {
            if (!data.ok) return;

            const transition: BoxTransition = {
              cardId: card.id,
              cardFront: card.front.length > 40 ? card.front.slice(0, 40) + '...' : card.front,
              oldBox: data.oldBox,
              newBox: data.newBox,
              leveledUp: data.leveledUp,
              reachedMastery: data.reachedMastery,
            };
            setTransitions((prev) => [...prev, transition]);

            // Track XP
            if (data.xpEarned > 0) {
              setAccumulatedXP((prev) => prev + data.xpEarned);
              setLastXP(data.xpEarned);
              setXpTrigger(Date.now());
              const bonus = (data.xpBreakdown?.levelUpBonus ?? 0) + (data.xpBreakdown?.masteryBonus ?? 0);
              if (bonus > 0) accumulatedBonusRef.current += bonus;
            }

            // Celebrations
            if (data.reachedMastery) {
              playMastery();
              setToastIsMastery(true);
              setToastBox(data.newBox);
              setShowToast(true);
              setTimeout(() => setShowToast(false), 2200);
            } else if (data.leveledUp) {
              playLevelUp();
              setToastIsMastery(false);
              setToastBox(data.newBox);
              setShowToast(true);
              setTimeout(() => setShowToast(false), 1600);
            } else if (correct) {
              playCorrect();
            } else {
              playWrong();
            }
          })
          .catch((err) => console.error('[fetch]', err));
      }

      const newCompleted = completed + 1;
      setCompleted(newCompleted);
      if (correct) setCorrectCount((prev) => prev + 1);

      // Next card or complete
      if (currentIndex + 1 >= cards.length) {
        setTimeout(() => setPhase('complete'), 500);
      } else {
        setTimeout(() => {
          setCurrentIndex((prev) => prev + 1);
          setTranscript('');
          setPhase('prompt');
        }, 500);
      }
    },
    [cards, currentIndex, completed, playCorrect, playWrong, playLevelUp, playMastery],
  );

  // ── Save session on complete ─────────────────────────────────────────────

  const saveSession = useCallback(() => {
    if (sessionSavedRef.current) return;
    sessionSavedRef.current = true;

    const sid = localStorage.getItem('mathspark_student_id');
    if (!sid) return;

    const duration = Math.round((Date.now() - startTime) / 1000);

    fetch('/api/flashcards/session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mode: 'voice',
        cardsReviewed: completed,
        cardsCorrect: correctCount,
        duration,
        bonusXP: accumulatedBonusRef.current,
      }),
    })
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        if (data.ok && data.xp) {
          setSessionXP({
            total: data.xp.total,
            streakMultiplier: data.xp.streakMultiplier,
            streakBonus: data.xp.streakBonus,
          });
        }
      })
      .catch((err) => console.error('[fetch]', err));
  }, [startTime, completed, correctCount]);

  useEffect(() => {
    if (phase === 'complete' && completed > 0) {
      saveSession();
    }
  }, [phase, completed, saveSession]);

  // ── Keyboard shortcuts ───────────────────────────────────────────────────

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (phase === 'prompt' && e.key === ' ') {
        e.preventDefault();
        startRecording();
      } else if (phase === 'recording' && e.key === ' ') {
        e.preventDefault();
        revealAnswer();
      } else if (phase === 'reveal') {
        if (e.key === 'ArrowRight' || e.key === 'd') handleEvaluate(true);
        else if (e.key === 'ArrowLeft' || e.key === 'a') handleEvaluate(false);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [phase, startRecording, revealAnswer, handleEvaluate]);

  // ── Cleanup on unmount ───────────────────────────────────────────────────

  useEffect(() => {
    return () => {
      stopListening();
      if (thinkTimerRef.current) clearInterval(thinkTimerRef.current);
    };
  }, [stopListening]);

  // ── Render: Loading ──────────────────────────────────────────────────────

  if (phase === 'loading') {
    return (
      <div className="min-h-screen bg-[#0F172A] flex flex-col items-center justify-center">
        <div className="text-5xl animate-sparky-bounce mb-4">🎙️</div>
        <p className="text-[#94A3B8] text-sm">Preparing voice recall...</p>
      </div>
    );
  }

  // ── Render: Complete ─────────────────────────────────────────────────────

  if (phase === 'complete') {
    const duration = Math.round((Date.now() - startTime) / 1000);
    return (
      <VoiceComplete
        cardsReviewed={completed}
        cardsCorrect={correctCount}
        duration={duration}
        transitions={transitions}
        sessionXP={sessionXP}
        onPlayAgain={() => {
          sessionSavedRef.current = false;
          setCurrentIndex(0);
          setCompleted(0);
          setCorrectCount(0);
          setTransitions([]);
          setAccumulatedXP(0);
          setLastXP(0);
          setSessionXP(null);
          accumulatedBonusRef.current = 0;
          setPhase('loading');
          loadDeck();
        }}
        onDone={() => router.push(conceptId ? `/learn/concept-map?open=${conceptId}` : '/flashcards')}
        suggestions={whatsNextSuggestions}
      />
    );
  }

  // ── Current card ─────────────────────────────────────────────────────────

  const card = cards[currentIndex];
  if (!card) return null;

  const thinkPct = thinkTimer / THINK_TIME_MS;
  const thinkSecs = Math.ceil(thinkTimer / 1000);
  const timerColor = thinkPct > 0.5 ? '#A78BFA' : thinkPct > 0.2 ? '#F59E0B' : '#EF4444';

  return (
    <div className="min-h-screen bg-[#0F172A] flex flex-col">
      {/* ── Power-Up Toast ────────────────────────────────────────────────── */}
      {showToast && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 z-[60] animate-slide-down">
          <div
            className="flex items-center gap-2 px-4 py-2.5 rounded-2xl shadow-lg border"
            style={{
              background: toastIsMastery
                ? 'linear-gradient(135deg, #059669, #34D399)'
                : 'linear-gradient(135deg, #1E293B, #334155)',
              borderColor: toastIsMastery ? '#34D399' : BOX_COLORS[toastBox] + '40',
            }}
          >
            <span className="text-xl animate-sparky-bounce">
              {toastIsMastery ? '🏅' : '⚡'}
            </span>
            <div>
              <p className="text-white font-black text-sm">
                {toastIsMastery ? 'MASTERED!' : 'Power Up!'}
              </p>
              <p className="text-white/70 text-[10px] font-bold">
                {toastIsMastery ? 'Card reached Master level!' : `→ ${BOX_NAMES[toastBox]}`}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ── Top bar ───────────────────────────────────────────────────────── */}
      <div className="sticky top-0 z-30 bg-[#0F172A]/95 backdrop-blur-md border-b border-white/5 px-4 py-3">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <button
            onClick={() => {
              stopListening();
              if (completed > 0) saveSession();
              router.push('/flashcards');
            }}
            className="text-[#94A3B8] text-sm font-bold"
          >
            ✕
          </button>
          <h2 className="text-[#F1F5F9] font-bold text-sm truncate max-w-[180px]">
            🎙️ {deckName}
          </h2>
          <div className="flex items-center gap-2">
            {accumulatedXP > 0 && (
              <span className="text-xs font-bold text-[#34D399] tabular-nums relative">
                {accumulatedXP} XP
                <XPPopup xp={lastXP} triggerKey={xpTrigger} />
              </span>
            )}
            <span className="text-xs text-[#64748B] tabular-nums">
              {currentIndex + 1}/{cards.length}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="max-w-md mx-auto mt-1.5 h-1 bg-white/5 rounded-full overflow-hidden">
          <div
            className="h-full bg-[#A78BFA] rounded-full transition-[width] duration-300"
            style={{ width: `${((currentIndex + (phase === 'reveal' ? 0.5 : 0)) / cards.length) * 100}%` }}
          />
        </div>
      </div>

      {/* ── Card area ─────────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col items-center px-4 py-6 max-w-md mx-auto w-full">
        {/* Power Level */}
        <div className="mb-3 flex items-center gap-2">
          <span className="text-xs font-bold" style={{ color: BOX_COLORS[card.leitnerBox || 0] }}>
            {BOX_NAMES[card.leitnerBox || 0]}
          </span>
          <div className="flex gap-0.5">
            {[1, 2, 3, 4, 5].map((lvl) => (
              <div
                key={lvl}
                className="w-5 h-1.5 rounded-full transition-[background-color] duration-300"
                style={{
                  background: lvl <= (card.leitnerBox || 0)
                    ? BOX_COLORS[card.leitnerBox || 0]
                    : 'rgba(255,255,255,0.1)',
                }}
              />
            ))}
          </div>
        </div>

        {/* Question card (front) */}
        <div
          className="w-full bg-[#1E293B] rounded-2xl px-5 py-6 mb-5 text-center animate-flashcard-slide-up"
          key={`${card.id}-front`}
        >
          <p className="text-[#F1F5F9] text-lg font-bold leading-relaxed">{card.front}</p>
          {card.formula && (
            <div className="mt-3">
              <KatexRenderer latex={card.formula} displayMode className="text-[#F1F5F9] text-xl" />
            </div>
          )}
        </div>

        {/* ── Phase: Prompt ────────────────────────────────────────────────── */}
        {phase === 'prompt' && (
          <div className="flex flex-col items-center gap-4 animate-fade-in">
            <p className="text-sm text-[#94A3B8] text-center">
              Think about the answer, then say it out loud!
            </p>

            <button
              onClick={startRecording}
              className="w-20 h-20 rounded-full flex items-center justify-center animate-voice-pulse transition-transform active:scale-95"
              style={{
                background: 'linear-gradient(135deg, #7C3AED, #A78BFA)',
                boxShadow: '0 0 30px rgba(167,139,250,0.3)',
              }}
            >
              <span className="text-3xl">🎙️</span>
            </button>

            <p className="text-xs text-[#64748B]">
              Tap to start · {speechSupported ? 'Voice capture on' : 'Self-check mode'}
            </p>
          </div>
        )}

        {/* ── Phase: Recording ────────────────────────────────────────────── */}
        {phase === 'recording' && (
          <div className="flex flex-col items-center gap-4 w-full animate-fade-in">
            {/* Timer bar */}
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-[width] duration-100"
                style={{ width: `${thinkPct * 100}%`, background: timerColor }}
              />
            </div>
            <span className="text-xs font-bold tabular-nums" style={{ color: timerColor }}>
              {thinkSecs}s
            </span>

            {/* Mic visualizer */}
            <div className="w-20 h-20 rounded-full flex items-center justify-center animate-voice-pulse"
              style={{
                background: 'linear-gradient(135deg, #7C3AED, #A78BFA)',
                boxShadow: '0 0 40px rgba(167,139,250,0.4)',
              }}
            >
              <span className="text-3xl">{isListening ? '🔊' : '🎙️'}</span>
            </div>

            <MicVisualizer active={isListening || thinkTimer > 0} />

            {/* Transcript */}
            {transcript && (
              <div className="w-full bg-[#1E293B]/60 rounded-xl px-4 py-2.5 border border-purple-500/20">
                <p className="text-xs text-[#64748B] mb-0.5">You said:</p>
                <p className="text-sm text-[#F1F5F9] font-medium italic">&ldquo;{transcript}&rdquo;</p>
              </div>
            )}

            {!speechSupported && (
              <p className="text-xs text-[#94A3B8] text-center">
                Say your answer out loud — speaking helps you remember!
              </p>
            )}

            {/* Ready button */}
            <button
              onClick={revealAnswer}
              className="px-6 py-3 rounded-2xl font-bold text-sm text-white active:scale-[0.97] transition-transform"
              style={{ background: 'linear-gradient(135deg, #A78BFA, #7C3AED)' }}
            >
              Show Answer ✨
            </button>

            <p className="text-[10px] text-[#475569] hidden sm:block">
              Press Space to reveal
            </p>
          </div>
        )}

        {/* ── Phase: Reveal ───────────────────────────────────────────────── */}
        {phase === 'reveal' && (
          <div className="flex flex-col items-center gap-4 w-full animate-fade-in">
            {/* Answer card (back) */}
            <div
              className="w-full bg-gradient-to-br from-[#1E293B] to-[#2D1B69] rounded-2xl px-5 py-5 text-center border border-purple-500/20 animate-pop-in"
            >
              <p className="text-[10px] text-purple-300 uppercase tracking-wider mb-1.5 font-bold">Answer</p>
              <p className="text-[#F1F5F9] text-lg font-bold leading-relaxed">{card.back}</p>
              {card.formula && (
                <div className="mt-2">
                  <KatexRenderer latex={card.formula} displayMode className="text-[#F1F5F9]" />
                </div>
              )}
            </div>

            {/* Transcript comparison (if available) */}
            {transcript && (
              <div className="w-full bg-[#1E293B]/40 rounded-xl px-4 py-2 border border-white/5">
                <p className="text-[10px] text-[#64748B] mb-0.5">You said:</p>
                <p className="text-sm text-[#94A3B8] italic">&ldquo;{transcript}&rdquo;</p>
              </div>
            )}

            <p className="text-sm text-[#94A3B8]">Did you get it right?</p>

            {/* Self-evaluation buttons */}
            <div className="flex items-center gap-3 w-full max-w-[400px]">
              <button
                onClick={() => handleEvaluate(false)}
                className="flex-1 py-3.5 rounded-2xl font-bold text-sm text-blue-400 bg-blue-500/10 border border-blue-500/20 active:scale-[0.97] transition-[transform,background-color,border-color]"
              >
                Not yet 📚
              </button>
              <button
                onClick={() => handleEvaluate(true)}
                className="flex-1 py-3.5 rounded-2xl font-bold text-sm text-emerald-400 bg-duo-green/10 border border-duo-green/20 active:scale-[0.97] transition-[transform,background-color,border-color]"
              >
                Got it! 🎯
              </button>
            </div>

            <p className="text-[10px] text-[#475569] hidden sm:block">
              ← A = Not yet &nbsp;·&nbsp; D → = Got it
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
