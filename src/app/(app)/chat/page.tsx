'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import MessageBubble from '@/components/chat/MessageBubble';
import TypingDots from '@/components/chat/TypingDots';
import ChatComposer from '@/components/chat/ChatComposer';
import { useSparkyChat, getQuickReplies } from '@/components/chat/useSparkyChat';
import { useVoiceLoop } from '@/components/chat/useVoiceLoop';

// ── Main component ────────────────────────────────────────────────────────────

export default function ChatPage() {
  const router = useRouter();

  const {
    studentGrade,
    messages, input, setInput,
    isLoading, streamingMsg, rateLimited, initialized,
    sendMessage, startNewChat,
    studentInitial, inputRef,
    attachment, attachmentNotice, attachImage, clearAttachment,
  } = useSparkyChat({ onNoStudent: () => router.replace('/start') });

  // Voice conversation: what the child says is sent like a typed message.
  const voice = useVoiceLoop((text) => sendMessage(text));

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMsg]);

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col bg-paper animate-fade-in" style={{ height: 'calc(100vh - 64px)' }}>

      {/* ── Header ── */}
      <div className="bg-ink px-4 py-3 flex items-center gap-3 flex-shrink-0">
        <button
          onClick={() => router.push('/chapters')}
          className="text-white/70 hover:text-white font-bold text-xl min-h-[44px] min-w-[44px] flex items-center justify-center"
          aria-label="Back"
        >
          ←
        </button>
        <div className="flex items-center gap-2 flex-1">
          <Sparky mood="happy" size={40} />
          <div>
            <p className="text-white font-extrabold text-sm leading-tight">Sparky</p>
            <div className="flex items-center gap-1.5">
              <div className="w-1.5 h-1.5 rounded-full bg-success-soft" />
              <p className="text-white/70 text-xs">Math Tutor · Online</p>
            </div>
          </div>
        </div>
        <button
          onClick={startNewChat}
          className="text-white/70 hover:text-white text-xs font-bold px-3 py-1.5 rounded-full border-2 border-white/30 hover:border-white/60 transition-colors min-h-[36px]"
        >
          New chat
        </button>
      </div>

      {/* ── Messages area ── */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        {!initialized && (
          <div className="flex flex-col items-center justify-center h-full gap-4">
            <div className="animate-sparky-bounce">
              <Sparky mood="thinking" size={80} />
            </div>
            <p className="text-ink-muted font-semibold">Loading…</p>
          </div>
        )}

        {initialized && messages.map((msg) => (
          <MessageBubble key={msg.id} msg={msg} studentInitial={studentInitial} />
        ))}

        {/* Streaming message in progress */}
        {streamingMsg && (
          <div className="flex items-end gap-2 mb-3">
            <div className="flex-shrink-0">
              <Sparky mood="thinking" size={36} />
            </div>
            <div className="max-w-[85%] bg-white rounded-card rounded-bl-sm px-4 py-2.5 border-2 border-line">
              <p className="text-[15px] leading-relaxed text-ink font-medium whitespace-pre-wrap [overflow-wrap:anywhere]">{streamingMsg}</p>
              <span className="inline-block w-1 h-4 bg-action animate-pulse ml-0.5 rounded" />
            </div>
          </div>
        )}

        {/* Typing indicator (before first stream chunk) */}
        {isLoading && !streamingMsg && (
          <div className="flex items-end gap-2 mb-3">
            <Sparky mood="thinking" size={36} />
            <div className="bg-white rounded-card rounded-bl-sm border-2 border-line">
              <TypingDots />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ── Quick reply chips ── */}
      {!isLoading && !rateLimited && (
        <div className="px-4 pb-2 flex-shrink-0">
          <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
            {getQuickReplies(studentGrade).map((qr) => (
              <button
                key={qr.label}
                onClick={() => sendMessage(qr.message)}
                disabled={isLoading}
                className="flex-shrink-0 bg-white border-2 border-line text-ink text-xs font-bold rounded-full px-3 py-2 hover:border-ink transition-colors whitespace-nowrap min-h-[36px]"
              >
                {qr.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Input area ── */}
      <div className="bg-white px-4 py-3 flex-shrink-0 border-t-2 border-line pb-[calc(0.75rem+env(safe-area-inset-bottom,0px))]">
        {rateLimited ? (
          <p className="text-center text-ink-muted text-sm font-medium py-2">
            Daily limit reached 🌟 See you tomorrow!
          </p>
        ) : (
          <ChatComposer
            input={input}
            setInput={setInput}
            onSend={() => { sendMessage(input); }}
            isLoading={isLoading}
            inputRef={inputRef}
            attachment={attachment}
            attachmentNotice={attachmentNotice}
            onAttach={attachImage}
            onClearAttachment={clearAttachment}
            voiceSupported={voice.supported}
            voiceState={voice.state}
            voiceHeard={voice.heard}
            voiceNotice={voice.notice}
            onVoiceStart={voice.start}
            onVoiceStop={voice.stop}
          />
        )}
      </div>
    </div>
  );
}
