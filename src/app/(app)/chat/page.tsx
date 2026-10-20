'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import MessageBubble from '@/components/chat/MessageBubble';
import TypingDots from '@/components/chat/TypingDots';
import { useSparkyChat, getQuickReplies } from '@/components/chat/useSparkyChat';

// ── Main component ────────────────────────────────────────────────────────────

export default function ChatPage() {
  const router = useRouter();

  const {
    studentGrade,
    messages, input, setInput,
    isLoading, streamingMsg, rateLimited, initialized,
    sendMessage, startNewChat,
    studentInitial, inputRef,
  } = useSparkyChat({ onNoStudent: () => router.replace('/start') });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMsg]);

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col bg-[#F0F4F8] animate-fade-in" style={{ height: 'calc(100vh - 64px)' }}>

      {/* ── Header ── */}
      <div className="bg-duo-dark px-4 py-3 flex items-center gap-3 flex-shrink-0 shadow-md">
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
              <div className="w-1.5 h-1.5 rounded-full bg-duo-green" />
              <p className="text-white/60 text-xs">Math Tutor · Online</p>
            </div>
          </div>
        </div>
        <button
          onClick={startNewChat}
          className="text-white/70 hover:text-white text-xs font-bold px-3 py-1.5 rounded-full border border-white/20 hover:border-white/40 transition-colors min-h-[36px]"
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
            <p className="text-gray-500 font-semibold">Loading…</p>
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
            <div className="max-w-[78%] bg-white rounded-2xl rounded-bl-sm px-4 py-2.5 shadow-sm border border-gray-100">
              <p className="text-sm leading-relaxed text-gray-800 font-medium whitespace-pre-wrap">{streamingMsg}</p>
              <span className="inline-block w-1 h-4 bg-duo-green animate-pulse ml-0.5 rounded" />
            </div>
          </div>
        )}

        {/* Typing indicator (before first stream chunk) */}
        {isLoading && !streamingMsg && (
          <div className="flex items-end gap-2 mb-3">
            <Sparky mood="thinking" size={36} />
            <div className="bg-white rounded-2xl rounded-bl-sm shadow-sm border border-gray-100">
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
                className="flex-shrink-0 bg-white border-2 border-duo-blue text-duo-blue text-xs font-bold rounded-full px-3 py-2 hover:bg-duo-blue hover:text-white transition-colors whitespace-nowrap min-h-[36px]"
              >
                {qr.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Input area ── */}
      <div className="bg-white px-4 py-3 flex-shrink-0 shadow-[0_-2px_10px_rgba(0,0,0,0.06)] pb-[calc(0.75rem+env(safe-area-inset-bottom,0px))]">
        {rateLimited ? (
          <p className="text-center text-gray-500 text-sm font-medium py-2">
            Daily limit reached 🌟 See you tomorrow!
          </p>
        ) : (
          <div className="flex items-center gap-3">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(input); } }}
              placeholder="Ask Sparky anything math…"
              disabled={isLoading}
              className="flex-1 bg-gray-100 rounded-full px-4 py-2.5 text-sm text-gray-800 outline-none focus:ring-2 focus:ring-duo-green font-medium placeholder-gray-400 min-h-[44px]"
            />
            <button
              onClick={() => sendMessage(input)}
              disabled={isLoading || !input.trim()}
              className="w-11 h-11 rounded-full bg-duo-green disabled:bg-gray-200 flex items-center justify-center transition-colors flex-shrink-0"
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
        )}
      </div>
    </div>
  );
}
