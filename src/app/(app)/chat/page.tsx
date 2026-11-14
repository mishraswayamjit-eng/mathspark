'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import MessageBubble from '@/components/chat/MessageBubble';
import TypingDots from '@/components/chat/TypingDots';
import ChatComposer from '@/components/chat/ChatComposer';
import { useSparkyChat, getQuickReplies } from '@/components/chat/useSparkyChat';
import { useVoiceLoop } from '@/components/chat/useVoiceLoop';
import VisualBoard, { WhiteboardPanel } from '@/components/visuals/VisualBoard';
import { extractVisual, type VisualSpec } from '@/lib/visuals/spec';
import { startersForTopics } from '@/lib/visuals/topicMap';
import { getTopicsForGrade } from '@/data/topicTree';

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
  const voice = useVoiceLoop((text) => sendMessage(text, null, { usePhoto: false }));

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMsg]);

  // ── Whiteboard ────────────────────────────────────────────────────────────
  // The reply being streamed, split into what to read and what to draw.
  const live = extractVisual(streamingMsg);

  // The most recent picture in the conversation.
  const latestVisual = useMemo<VisualSpec | null>(() => {
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role !== 'assistant') continue;
      const found = extractVisual(messages[i].content).visual;
      if (found) return found;
    }
    return null;
  }, [messages]);

  // An earlier picture the child asked to see again; a new message clears it.
  const [pinned, setPinned] = useState<VisualSpec | null>(null);
  useEffect(() => { setPinned(null); }, [messages.length]);

  const boardVisual = pinned ?? live.visual ?? latestVisual;

  // Starter cards for the empty whiteboard, from this grade's own topics.
  const starters = useMemo(
    () => startersForTopics(getTopicsForGrade(studentGrade).map((t) => t.name), 5),
    [studentGrade],
  );

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    // Phones: the usual single column. Wide screens: the page breaks out of the
    // narrow app column into two panels, conversation and whiteboard.
    <div className="bg-paper animate-fade-in h-[calc(100vh-64px)] lg:fixed lg:inset-x-0 lg:top-0 lg:bottom-16 lg:h-auto lg:z-10">
      <div className="h-full mx-auto lg:max-w-6xl lg:grid lg:grid-cols-2 lg:gap-5 lg:p-5">

        {/* ══ Conversation ══ */}
        <div className="h-full min-h-0 flex flex-col bg-paper lg:bg-white lg:border-2 lg:border-ink lg:rounded-card lg:shadow-hard lg:overflow-hidden">

          {/* ── Header ── */}
          <div className="bg-ink px-4 py-3 flex items-center gap-3 flex-shrink-0">
            <button
              onClick={() => router.push('/chapters')}
              className="text-white/70 hover:text-white font-bold text-xl min-h-[48px] min-w-[48px] flex items-center justify-center"
              aria-label="Back"
            >
              ←
            </button>
            <div className="flex items-center gap-2 flex-1">
              <Sparky mood="happy" size={40} />
              <div>
                <p className="font-display text-title text-white leading-tight">Sparky</p>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-success-soft" />
                  <p className="text-white/70 text-xs">Maths tutor · Online</p>
                </div>
              </div>
            </div>
            <button
              onClick={startNewChat}
              className="text-white/70 hover:text-white text-xs font-bold px-3 rounded-full border-2 border-white/30 hover:border-white/60 transition-colors min-h-[48px]"
            >
              New chat
            </button>
          </div>

          {/* ── Messages area ── */}
          <div className="flex-1 min-h-0 overflow-y-auto px-4 py-4 lg:bg-paper">
            {!initialized && (
              <div className="flex flex-col items-center justify-center h-full gap-4">
                <div className="animate-sparky-bounce">
                  <Sparky mood="thinking" size={80} />
                </div>
                <p className="text-ink-muted font-semibold">Loading…</p>
              </div>
            )}

            {initialized && messages.map((msg) => (
              <MessageBubble key={msg.id} msg={msg} studentInitial={studentInitial} onShowVisual={setPinned} />
            ))}

            {/* Reply in progress */}
            {isLoading && (
              <div className="flex items-end gap-2 mb-3">
                <div className="flex-shrink-0">
                  <Sparky mood="thinking" size={36} />
                </div>
                {live.text ? (
                  <div className="max-w-[85%] bg-white rounded-card rounded-bl-sm px-4 py-2.5 border-2 border-line">
                    {live.visual && (
                      <div className="lg:hidden mb-3 pb-3 border-b-2 border-line">
                        <VisualBoard spec={live.visual} />
                      </div>
                    )}
                    <p className="text-[15px] leading-relaxed text-ink font-medium whitespace-pre-wrap [overflow-wrap:anywhere]">{live.text}</p>
                    <span className="inline-block w-1 h-4 bg-action animate-pulse ml-0.5 rounded" />
                  </div>
                ) : (
                  <div className="bg-white rounded-card rounded-bl-sm border-2 border-line">
                    <TypingDots />
                  </div>
                )}
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* ── Quick reply chips ── */}
          {!isLoading && !rateLimited && (
            <div className="px-4 pt-2 pb-2 flex-shrink-0 lg:bg-paper">
              <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
                {getQuickReplies(studentGrade).map((qr) => (
                  <button
                    key={qr.label}
                    onClick={() => sendMessage(qr.message, null, { usePhoto: false })}
                    disabled={isLoading}
                    className="flex-shrink-0 bg-white border-2 border-line text-ink text-[13px] font-bold rounded-full px-3.5 hover:border-ink transition-colors whitespace-nowrap min-h-[48px]"
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

        {/* ══ Whiteboard (wide screens) ══ */}
        <div className="hidden lg:block h-full min-h-0">
          <WhiteboardPanel
            visual={boardVisual}
            starters={starters}
            disabled={isLoading || rateLimited}
            onStarter={(prompt) => { sendMessage(prompt, null, { usePhoto: false }); }}
          />
        </div>
      </div>
    </div>
  );
}
