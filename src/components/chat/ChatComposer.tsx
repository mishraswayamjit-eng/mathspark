'use client';

import { useRef } from 'react';
import type { RefObject } from 'react';
import type { ChatAttachment } from '@/components/chat/useSparkyChat';
import type { VoiceState } from '@/components/chat/useVoiceLoop';

interface ChatComposerProps {
  input: string;
  setInput: (value: string) => void;
  onSend: () => void;
  isLoading: boolean;
  inputRef: RefObject<HTMLInputElement>;

  /** Photo waiting to be sent with the next message. */
  attachment: ChatAttachment | null;
  attachmentNotice: string;
  onAttach: (file: File) => void;
  onClearAttachment: () => void;

  /** Voice conversation controls. */
  voiceSupported: boolean;
  voiceState: VoiceState;
  voiceHeard: string;
  voiceNotice: string;
  onVoiceStart: () => void;
  onVoiceStop: () => void;
}

const VOICE_LABEL: Record<Exclude<VoiceState, 'off'>, string> = {
  listening: 'Listening… say your question',
  thinking:  'Sparky is thinking…',
  speaking:  'Sparky is talking…',
};

/**
 * The chat input row shared by the full chat page and the floating widget:
 * photo button, text box, microphone (voice conversation) and send.
 */
export default function ChatComposer({
  input, setInput, onSend, isLoading, inputRef,
  attachment, attachmentNotice, onAttach, onClearAttachment,
  voiceSupported, voiceState, voiceHeard, voiceNotice, onVoiceStart, onVoiceStop,
}: ChatComposerProps) {
  const fileRef = useRef<HTMLInputElement>(null);
  const voiceOn = voiceState !== 'off';
  const voiceLabel = voiceState === 'off' ? '' : VOICE_LABEL[voiceState];
  const canSend = !isLoading && (input.trim().length > 0 || attachment !== null);

  const iconBtn =
    'w-12 h-12 flex-shrink-0 rounded-tile border-2 flex items-center justify-center text-xl transition-colors disabled:opacity-40';

  return (
    <div className="space-y-2">
      {/* Voice status */}
      {voiceOn && (
        <div className="flex items-center gap-2 bg-soft border-2 border-line rounded-control px-3 py-2" aria-live="polite">
          <span className="w-2.5 h-2.5 rounded-full bg-action animate-pulse flex-shrink-0" aria-hidden="true" />
          <p className="flex-1 min-w-0 text-[13px] font-bold text-ink truncate">
            {voiceState === 'listening' && voiceHeard ? voiceHeard : voiceLabel}
          </p>
        </div>
      )}
      {!voiceOn && voiceNotice && (
        <p className="text-[13px] font-bold text-hint-ink bg-hint border-2 border-hint-ink rounded-control px-3 py-2">
          {voiceNotice}
        </p>
      )}

      {/* Photo waiting to be sent */}
      {attachment && (
        <div className="flex items-center gap-3 bg-soft border-2 border-line rounded-control p-2">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={attachment.previewUrl}
            alt="Photo you are about to send"
            className="w-14 h-14 rounded-tile object-cover border-2 border-line flex-shrink-0"
          />
          <p className="flex-1 text-[13px] font-bold text-ink">Photo ready. Add a note or just press send.</p>
          <button
            type="button"
            onClick={onClearAttachment}
            aria-label="Remove photo"
            className={`${iconBtn} bg-white border-line text-ink hover:border-ink`}
          >
            <span aria-hidden="true">✕</span>
          </button>
        </div>
      )}
      {attachmentNotice && (
        <p className="text-[13px] font-bold text-hint-ink bg-hint border-2 border-hint-ink rounded-control px-3 py-2">
          {attachmentNotice}
        </p>
      )}

      <div className="flex items-center gap-2">
        {/* Photo of working */}
        <input
          ref={fileRef}
          type="file"
          accept="image/*"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files && e.target.files[0];
            if (file) onAttach(file);
            e.target.value = '';   // allow picking the same photo again
          }}
        />
        <button
          type="button"
          onClick={() => fileRef.current?.click()}
          disabled={isLoading}
          aria-label="Add a photo of your working"
          className={`${iconBtn} bg-white border-line text-ink hover:border-ink`}
        >
          <span aria-hidden="true">📷</span>
        </button>

        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (canSend) onSend(); } }}
          placeholder="Ask Sparky anything math…"
          aria-label="Message to Sparky"
          disabled={isLoading}
          className="flex-1 min-w-0 bg-white border-2 border-line rounded-control px-4 py-2.5 text-sm text-ink outline-none focus:border-action font-medium placeholder-gray-400 min-h-[48px]"
        />

        {/* Voice conversation */}
        {voiceSupported && (
          <button
            type="button"
            onClick={voiceOn ? onVoiceStop : onVoiceStart}
            disabled={!voiceOn && isLoading}
            aria-label={voiceOn ? 'Stop talking with Sparky' : 'Talk with Sparky'}
            aria-pressed={voiceOn}
            className={`${iconBtn} ${voiceOn ? 'bg-action border-ink text-white' : 'bg-white border-line text-ink hover:border-ink'}`}
          >
            <span aria-hidden="true">{voiceOn ? '⏹' : '🎤'}</span>
          </button>
        )}

        <button
          type="button"
          onClick={onSend}
          disabled={!canSend}
          className="w-12 h-12 rounded-tile bg-action border-2 border-ink disabled:bg-gray-300 disabled:border-gray-300 flex items-center justify-center transition-colors flex-shrink-0"
          aria-label="Send"
        >
          {isLoading ? (
            <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <svg viewBox="0 0 24 24" fill="none" className="w-5 h-5" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          )}
        </button>
      </div>
    </div>
  );
}
