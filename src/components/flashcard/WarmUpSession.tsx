'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useFlashcardDeck } from '@/hooks/useFlashcardDeck';
import dynamic from 'next/dynamic';
import Confetti from '@/components/Confetti';
import Sparky from '@/components/Sparky';
import { useSounds } from '@/hooks/useSounds';
import { shuffle } from '@/lib/shuffle';
import type { FlashCard } from '@/types';
import { logError } from '@/lib/logger';

const KatexRenderer = dynamic(() => import('@/components/KatexRenderer'), { ssr: false });

// ── Types ────────────────────────────────────────────────────────────────────

interface CardWithProgress extends FlashCard {
  leitnerBox: number;
  timesSeen: number;
  timesCorrect: number;
  streakOnCard: number;
}

type WarmUpPhase =
  | 'loading'
  | 'breathe'        // calming breath animation
  | 'quickfire'      // rapid mental math cards
  | 'formulas'       // key formula review
  | 'confidence'     // show mastered cards
  | 'ready';         // motivational send-off

interface PhaseConfig {
  phase: WarmUpPhase;
  label: string;
  emoji: string;
  color: string;
}

const PHASE_ORDER: PhaseConfig[] = [
  { phase: 'breathe',    label: 'Calm Your Mind',   emoji: '🧘', color: '#60A5FA' },
  { phase: 'quickfire',  label: 'Quick Fire',       emoji: '⚡', color: '#FBBF24' },
  { phase: 'formulas',   label: 'Formula Flash',    emoji: '📐', color: '#A78BFA' },
  { phase: 'confidence', label: 'You Know This!',   emoji: '💪', color: '#34D399' },
  { phase: 'ready',      label: 'Ready!',           emoji: '🚀', color: '#F472B6' },
];

const BREATH_CYCLES = 3;
const BREATH_INHALE_MS = 4000;
const BREATH_HOLD_MS = 2000;
const BREATH_EXHALE_MS = 4000;

// ── Breathing Circle ─────────────────────────────────────────────────────────

function BreathingCircle({
  breathState,
}: {
  breathState: 'inhale' | 'hold' | 'exhale';
}) {
  const scale = breathState === 'inhale' ? 'scale-125' : breathState === 'hold' ? 'scale-125' : 'scale-75';
  const label = breathState === 'inhale' ? 'Breathe in...' : breathState === 'hold' ? 'Hold...' : 'Breathe out...';
  const duration = breathState === 'inhale' ? 'duration-[4000ms]' : breathState === 'hold' ? 'duration-[2000ms]' : 'duration-[4000ms]';

  return (
    <div className="flex flex-col items-center gap-6">
      <div
        className={`w-32 h-32 rounded-full bg-soft transition-transform ease-in-out ${scale} ${duration}`}
      >
        <div className="w-full h-full rounded-full flex items-center justify-center border-2 border-ink">
          <span className="text-4xl">🧘</span>
        </div>
      </div>
      <p className="font-display text-heading text-ink animate-pulse">{label}</p>
    </div>
  );
}

// ── Card Reveal (for quickfire/formulas/confidence phases) ───────────────────

function CardReveal({
  card,
  showBack,
  phaseColor,
  label,
  onReveal,
  onNext,
}: {
  card: CardWithProgress;
  showBack: boolean;
  phaseColor: string;
  label?: string;
  onReveal: () => void;
  onNext: () => void;
}) {
  return (
    <div className="w-full max-w-sm mx-auto animate-flashcard-slide-up">
      {label && (
        <p className="text-center text-[13px] font-bold text-ink-muted mb-3">
          {label}
        </p>
      )}

      <div
        className="bg-card border-2 border-ink rounded-card shadow-hard-lg p-5 mb-4"
        style={{
          borderLeft: `10px solid ${phaseColor}`,
        }}
      >
        {/* Front */}
        <p className="text-ink text-question leading-relaxed">
          {card.front}
        </p>

        {card.formula && (
          <div className="mt-3">
            <KatexRenderer latex={card.formula} displayMode className="text-ink" />
          </div>
        )}

        {/* Back (revealed) */}
        {showBack && (
          <div className="mt-4 pt-3 border-t-2 border-line animate-fade-in">
            <p className="text-body text-ink bg-soft rounded-note px-3 py-2 font-bold leading-relaxed">
              {card.back}
            </p>
          </div>
        )}
      </div>

      {/* Action buttons */}
      <div className="flex gap-3">
        {!showBack ? (
          <button
            onClick={onReveal}
            className="flex-1 py-3 rounded-control font-extrabold text-sm text-white bg-action border-2 border-ink shadow-hard-sm transition-transform active:scale-[0.97]"
          >
            Show Answer
          </button>
        ) : (
          <button
            onClick={onNext}
            className="flex-1 py-3 rounded-control font-extrabold text-sm text-white bg-action border-2 border-ink shadow-hard-sm transition-transform active:scale-[0.97]"
          >
            Next →
          </button>
        )}
      </div>
    </div>
  );
}

// ── Phase Transition Screen ──────────────────────────────────────────────────

function PhaseTransition({
  config,
  phaseIndex,
  total,
  onStart,
}: {
  config: PhaseConfig;
  phaseIndex: number;
  total: number;
  onStart: () => void;
}) {
  return (
    <div className="fixed inset-0 z-50 bg-paper flex flex-col items-center justify-center px-6 animate-fade-in">
      {/* Progress dots */}
      <div className="flex gap-2 mb-8">
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            className="w-2.5 h-2.5 rounded-full transition-[background-color,transform]"
            style={{
              background: i < phaseIndex ? '#4f46e5' : i === phaseIndex ? '#1d2a4d' : '#d3deee',
              transform: i === phaseIndex ? 'scale(1.3)' : 'scale(1)',
            }}
          />
        ))}
      </div>

      <span className="text-5xl mb-4">{config.emoji}</span>
      <h2 className="text-heading text-ink mb-2">{config.label}</h2>
      <p className="text-label text-ink-muted mb-8 text-center max-w-xs">
        {config.phase === 'breathe' && 'Take 3 deep breaths to clear your mind'}
        {config.phase === 'quickfire' && 'Quick mental math — just tap to reveal!'}
        {config.phase === 'formulas' && 'Review key formulas before the exam'}
        {config.phase === 'confidence' && 'Cards you\'ve already mastered — you got this!'}
        {config.phase === 'ready' && 'You\'re prepared. Time to shine!'}
      </p>

      <button
        onClick={onStart}
        className="px-8 py-3 rounded-control font-extrabold text-sm text-white bg-action border-2 border-ink shadow-hard-sm transition-transform active:scale-[0.97]"
      >
        {config.phase === 'ready' ? 'Finish Warm-Up' : 'Start →'}
      </button>
    </div>
  );
}

// ── Main Warm-Up Component ───────────────────────────────────────────────────

interface WarmUpSessionProps {
  deckId: string;
  conceptId?: string | null;
}

export default function WarmUpSession({ deckId, conceptId }: WarmUpSessionProps) {
  const router = useRouter();
  const { fetchDeck } = useFlashcardDeck('warmup');
  const { playCorrect, playLevelUp, playMastery } = useSounds();

  const [currentPhase, setCurrentPhase] = useState<WarmUpPhase>('loading');
  const [showTransition, setShowTransition] = useState(false);
  const [phaseIndex, setPhaseIndex] = useState(0);

  // Breathing
  const [breathCycle, setBreathCycle] = useState(0);
  const [breathState, setBreathState] = useState<'inhale' | 'hold' | 'exhale'>('inhale');

  // Card phases
  const [quickfireCards, setQuickfireCards] = useState<CardWithProgress[]>([]);
  const [formulaCards, setFormulaCards] = useState<CardWithProgress[]>([]);
  const [confidenceCards, setConfidenceCards] = useState<CardWithProgress[]>([]);
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showBack, setShowBack] = useState(false);

  // Session tracking
  const [startTime] = useState(() => Date.now());
  const sessionSavedRef = useRef(false);

  // ── Load warm-up deck ──────────────────────────────────────────────────────

  useEffect(() => {
    fetchDeck()
      .then((data) => {
        if (!data || data.cards.length === 0) {
          router.replace('/flashcards');
          return;
        }

        const cards = data.cards as CardWithProgress[];

        // Split cards by category for different phases
        const warmUpCards = cards.filter(
          (c) => c.category === 'warm_up' || c.category === 'mental_math',
        );
        const formulas = cards.filter(
          (c) => c.category === 'formula' || c.category === 'rule',
        );
        const mastered = cards.filter((c) => c.leitnerBox >= 4);
        const tricks = cards.filter((c) => c.category === 'trick');

        // Select cards for each phase
        setQuickfireCards(shuffle(warmUpCards).slice(0, 8));
        setFormulaCards(shuffle([...formulas, ...tricks]).slice(0, 6));
        // Confidence: mastered first, fallback to high-box cards
        const confPool = mastered.length >= 3
          ? shuffle(mastered).slice(0, 4)
          : shuffle(cards.filter((c) => c.leitnerBox >= 2)).slice(0, 4);
        setConfidenceCards(confPool.length > 0 ? confPool : shuffle(cards).slice(0, 3));

        // Start with breathing phase transition
        setPhaseIndex(0);
        setShowTransition(true);
        setCurrentPhase('breathe');
      })
      .catch((err) => { logError('[WarmUp] fetch deck', err); router.replace('/flashcards'); });
  }, [fetchDeck, router]);

  // ── Breathing cycle ────────────────────────────────────────────────────────

  useEffect(() => {
    if (currentPhase !== 'breathe' || showTransition) return;

    if (breathCycle >= BREATH_CYCLES) {
      // Move to next phase
      playLevelUp();
      advanceToNextPhase();
      return;
    }

    // Inhale → Hold → Exhale → next cycle
    const sequence = [
      { state: 'inhale' as const, duration: BREATH_INHALE_MS },
      { state: 'hold' as const, duration: BREATH_HOLD_MS },
      { state: 'exhale' as const, duration: BREATH_EXHALE_MS },
    ];

    let timeout: ReturnType<typeof setTimeout>;
    let currentStep = 0;

    function runStep() {
      if (currentStep >= sequence.length) {
        setBreathCycle((c) => c + 1);
        return;
      }
      setBreathState(sequence[currentStep].state);
      timeout = setTimeout(() => {
        currentStep++;
        runStep();
      }, sequence[currentStep].duration);
    }

    runStep();

    return () => clearTimeout(timeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentPhase, showTransition, breathCycle]);

  // ── Advance to next phase ──────────────────────────────────────────────────

  const advanceToNextPhase = useCallback(() => {
    const nextIdx = phaseIndex + 1;
    if (nextIdx >= PHASE_ORDER.length) {
      setCurrentPhase('ready');
      setShowTransition(true);
      setPhaseIndex(nextIdx - 1);
      return;
    }

    setPhaseIndex(nextIdx);
    setCurrentPhase(PHASE_ORDER[nextIdx].phase);
    setCurrentCardIndex(0);
    setShowBack(false);
    setShowTransition(true);
  }, [phaseIndex]);

  // ── Card navigation ────────────────────────────────────────────────────────

  const getCurrentCards = useCallback((): CardWithProgress[] => {
    if (currentPhase === 'quickfire') return quickfireCards;
    if (currentPhase === 'formulas') return formulaCards;
    if (currentPhase === 'confidence') return confidenceCards;
    return [];
  }, [currentPhase, quickfireCards, formulaCards, confidenceCards]);

  const handleReveal = useCallback(() => {
    setShowBack(true);
    playCorrect();
  }, [playCorrect]);

  const handleNext = useCallback(() => {
    const cards = getCurrentCards();
    const nextIdx = currentCardIndex + 1;

    if (nextIdx >= cards.length) {
      playLevelUp();
      advanceToNextPhase();
      return;
    }

    setCurrentCardIndex(nextIdx);
    setShowBack(false);
  }, [currentCardIndex, getCurrentCards, advanceToNextPhase, playLevelUp]);

  // ── Save session ───────────────────────────────────────────────────────────

  const saveSession = useCallback(() => {
    if (sessionSavedRef.current) return;
    sessionSavedRef.current = true;

    const sid = localStorage.getItem('mathspark_student_id');
    if (!sid) return;

    const duration = Math.round((Date.now() - startTime) / 1000);
    const totalCards = quickfireCards.length + formulaCards.length + confidenceCards.length;

    fetch('/api/flashcards/session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mode: 'warmup',
        cardsReviewed: totalCards,
        cardsCorrect: totalCards, // warm-up = all reviewed
        duration,
      }),
    }).catch((err) => logError('[fetch]', err));
  }, [startTime, quickfireCards.length, formulaCards.length, confidenceCards.length]);

  // ── Render: Loading ────────────────────────────────────────────────────────

  if (currentPhase === 'loading') {
    return (
      <div className="min-h-screen bg-paper flex flex-col items-center justify-center">
        <div className="text-5xl animate-sparky-bounce mb-4">🧘</div>
        <p className="text-ink-muted text-label">Preparing warm-up...</p>
      </div>
    );
  }

  // ── Render: Phase transition screen ────────────────────────────────────────

  if (showTransition) {
    const config = PHASE_ORDER[phaseIndex] ?? PHASE_ORDER[PHASE_ORDER.length - 1];

    if (config.phase === 'ready') {
      // Final "Ready!" screen
      return (
        <div className="fixed inset-0 z-50 bg-paper flex flex-col items-center justify-center px-6 animate-fade-in">
          <Confetti />

          <div className="flex gap-2 mb-6">
            {PHASE_ORDER.map((_, i) => (
              <div key={i} className="w-2.5 h-2.5 rounded-full bg-action" />
            ))}
          </div>

          <div className="animate-sparky-dance">
            <Sparky mood="celebrating" size={100} />
          </div>

          <h1 className="text-display text-ink mt-4 mb-2">
            You&apos;re Ready!
          </h1>
          <p className="text-label text-ink-muted mb-2 text-center max-w-xs">
            Mind is calm, formulas fresh, confidence high.
          </p>
          <p className="text-lg font-black text-ink mb-8">Go crush it! 🌟</p>

          <div className="w-full max-w-xs space-y-3">
            <button
              onClick={() => {
                saveSession();
                playMastery();
                router.push('/test');
              }}
              className="ui-btn ui-btn-primary w-full"
            >
              Start My Exam 🚀
            </button>
            <button
              onClick={() => {
                saveSession();
                router.push(conceptId ? `/learn/concept-map?open=${conceptId}` : '/flashcards');
              }}
              className="ui-btn w-full"
            >
              {conceptId ? 'Back to Concept Map' : 'Back to Cards'}
            </button>
          </div>
        </div>
      );
    }

    return (
      <PhaseTransition
        config={config}
        phaseIndex={phaseIndex}
        total={PHASE_ORDER.length}
        onStart={() => setShowTransition(false)}
      />
    );
  }

  // ── Render: Breathing phase ────────────────────────────────────────────────

  if (currentPhase === 'breathe') {
    return (
      <div className="min-h-screen bg-paper flex flex-col">
        {/* Top bar */}
        <div className="sticky top-0 z-30 bg-ink px-4 py-2.5">
          <div className="flex items-center justify-between max-w-md mx-auto">
            <button onClick={() => router.push('/flashcards')} className="text-white text-sm font-bold">
              ✕
            </button>
            <span className="font-display text-title text-white">🧘 Calm Your Mind</span>
            <span className="text-xs font-bold text-white/70 tabular-nums">
              {breathCycle + 1}/{BREATH_CYCLES}
            </span>
          </div>
        </div>

        <div className="flex-1 flex flex-col items-center justify-center px-6">
          <BreathingCircle breathState={breathState} />

          <p className="text-[13px] font-bold text-ink-muted mt-8">
            Breath {breathCycle + 1} of {BREATH_CYCLES}
          </p>
        </div>
      </div>
    );
  }

  // ── Render: Card phases (quickfire, formulas, confidence) ──────────────────

  const cards = getCurrentCards();
  const currentCard = cards[currentCardIndex];
  const phaseConfig = PHASE_ORDER[phaseIndex];

  if (!currentCard || !phaseConfig) return null;

  const phaseLabels: Record<string, string> = {
    quickfire: 'Quick Fire — Tap to reveal!',
    formulas: 'Key Formulas',
    confidence: 'You\'ve Mastered This!',
  };

  return (
    <div className="min-h-screen bg-paper flex flex-col">
      {/* Top bar */}
      <div className="sticky top-0 z-30 bg-ink px-4 py-2.5">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <button
            onClick={() => {
              saveSession();
              router.push('/flashcards');
            }}
            className="text-white text-sm font-bold"
          >
            ✕
          </button>

          <div className="flex items-center gap-2">
            <span className="text-sm">{phaseConfig.emoji}</span>
            <span className="font-display text-title text-white">
              {phaseConfig.label}
            </span>
          </div>

          <span className="text-xs font-bold text-white/70 tabular-nums">
            {currentCardIndex + 1}/{cards.length}
          </span>
        </div>

        {/* Phase progress bar */}
        <div className="ui-meter max-w-md mx-auto mt-1.5 h-3">
          <div
            className="h-full bg-action rounded-full transition-[width] duration-300"
            style={{
              width: `${((currentCardIndex + 1) / cards.length) * 100}%`,
            }}
          />
        </div>

        {/* Overall phase dots */}
        <div className="flex justify-center gap-1.5 mt-2">
          {PHASE_ORDER.map((p, i) => (
            <div
              key={i}
              className="w-1.5 h-1.5 rounded-full"
              style={{
                background: i < phaseIndex ? '#ffffff' : i === phaseIndex ? '#f5a400' : 'rgba(255,255,255,0.3)',
              }}
            />
          ))}
        </div>
      </div>

      {/* Card area */}
      <div className="flex-1 flex flex-col items-center justify-center px-4 py-6" key={`${currentPhase}-${currentCardIndex}`}>
        {/* Confidence boost: show mastery badge */}
        {currentPhase === 'confidence' && (
          <div className="flex items-center gap-2 mb-4 bg-success-soft border-2 border-success rounded-full px-3 py-1">
            <span className="text-sm">💪</span>
            <span className="text-label text-success">
              Box {currentCard.leitnerBox} — You know this!
            </span>
          </div>
        )}

        <CardReveal
          card={currentCard}
          showBack={showBack}
          phaseColor={phaseConfig.color}
          label={currentPhase === 'quickfire' ? `${currentCard.topicName}` : currentCard.topicName}
          onReveal={handleReveal}
          onNext={handleNext}
        />

        {/* Skip phase */}
        <button
          onClick={() => {
            playLevelUp();
            advanceToNextPhase();
          }}
          className="mt-6 text-[13px] font-bold text-ink-muted hover:text-ink transition-colors min-h-0"
        >
          Skip to next phase →
        </button>
      </div>
    </div>
  );
}
