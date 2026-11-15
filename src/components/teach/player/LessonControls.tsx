'use client';

/**
 * The lesson's controls. Every button is at least 48px in both directions.
 * Keyboard (handled by the player): Space pauses, the arrow keys step.
 */

interface LessonControlsProps {
  paused: boolean;
  /** False while there is nothing to pause (the child's turn, the end). */
  canPause: boolean;
  canGoBack: boolean;
  atEnd: boolean;
  muted: boolean;
  slow: boolean;
  onTogglePause: () => void;
  onReplay: () => void;
  onBack: () => void;
  onSkipToEnd: () => void;
  onToggleSlow: () => void;
  onToggleMute: () => void;
}

const ROUND = 'w-12 h-12 flex-shrink-0 rounded-tile border-2 border-line bg-white text-ink text-lg font-bold flex items-center justify-center hover:border-ink disabled:opacity-40 disabled:pointer-events-none';

export default function LessonControls(props: LessonControlsProps) {
  const { paused, canPause, canGoBack, atEnd, muted, slow } = props;
  return (
    <div className="flex flex-wrap items-center gap-2" role="group" aria-label="Lesson controls">
      <button type="button" onClick={props.onBack} disabled={!canGoBack} aria-label="Back one step" className={ROUND}>
        <span aria-hidden="true">⏮</span>
      </button>
      <button
        type="button"
        onClick={props.onTogglePause}
        disabled={!canPause}
        aria-label={paused ? 'Carry on' : 'Pause'}
        className={`${ROUND} ${paused ? 'bg-action text-white border-ink' : ''}`}
      >
        <span aria-hidden="true">{paused ? '▶' : '⏸'}</span>
      </button>
      <button type="button" onClick={props.onReplay} aria-label="Say this step again" className={ROUND}>
        <span aria-hidden="true">↺</span>
      </button>
      <button type="button" onClick={props.onSkipToEnd} disabled={atEnd} aria-label="Skip to the end" className={ROUND}>
        <span aria-hidden="true">⏭</span>
      </button>
      <span className="flex-1" />
      <button
        type="button"
        onClick={props.onToggleSlow}
        aria-pressed={slow}
        aria-label={slow ? 'Slower speed is on. Go back to normal speed' : 'Go a bit slower'}
        className={`min-h-[48px] px-3 flex-shrink-0 rounded-tile border-2 text-[14px] font-extrabold flex items-center gap-1 ${
          slow ? 'bg-soft border-ink text-ink' : 'bg-white border-line text-ink hover:border-ink'
        }`}
      >
        <span aria-hidden="true">🐢</span> {slow ? 'Slower' : 'Normal'}
      </button>
      <button
        type="button"
        onClick={props.onToggleMute}
        aria-pressed={muted}
        aria-label={muted ? 'Turn the voice on' : 'Turn the voice off'}
        className={ROUND}
      >
        <span aria-hidden="true">{muted ? '🔇' : '🔊'}</span>
      </button>
    </div>
  );
}
