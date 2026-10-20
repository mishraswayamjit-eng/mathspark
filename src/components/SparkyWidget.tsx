'use client';

import { useEffect, useRef, useState } from 'react';
import { usePathname } from 'next/navigation';
import Sparky from '@/components/Sparky';
import MessageBubble from '@/components/chat/MessageBubble';
import TypingDots from '@/components/chat/TypingDots';
import { useSparkyChat, getQuickReplies } from '@/components/chat/useSparkyChat';
import { useScreenContext, subscribeOpenSparky, type ScreenContext } from '@/lib/sparkyContext';
import { isAppChromeHidden } from '@/lib/navVisibility';

// ── Per-screen suggestion chips ───────────────────────────────────────────────

interface Suggestion { label: string; message: string }

function getSuggestions(ctx: ScreenContext | null, grade: number): Suggestion[] {
  if (ctx?.screen === 'practice' && ctx.questionText) {
    return [
      { label: 'Explain this 🧠', message: 'Can you help me understand this question?' },
      { label: 'Give me a hint 💡', message: 'Can you give me a hint for this question?' },
      { label: "I'm stuck 😅",     message: "I'm stuck on this question. Can you guide me?" },
    ];
  }
  if (ctx?.screen === 'lesson' || ctx?.screen === 'learn') {
    return [
      { label: 'Explain simply ✨',   message: 'Can you explain this topic to me simply?' },
      { label: 'Give an example 📘',  message: 'Can you give me an example for this topic?' },
    ];
  }
  // Fallback: existing grade-aware quick replies.
  return getQuickReplies(grade);
}

// ── Inner widget (only mounted when visible — so the chat hook/history fetch
//    never runs pre-login or on the full /chat page) ──────────────────────────

function SparkyWidgetInner() {
  const pathname = usePathname();
  const ctx = useScreenContext();

  const {
    studentGrade,
    messages, input, setInput,
    isLoading, streamingMsg, rateLimited, initialized, remaining,
    sendMessage, startNewChat,
    studentInitial, inputRef,
  } = useSparkyChat();

  const [open, setOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-close the sheet whenever the student navigates to another page.
  useEffect(() => { setOpen(false); }, [pathname]);

  // Let pages (e.g. the practice result bubble) open the widget.
  useEffect(() => subscribeOpenSparky(() => setOpen(true)), []);

  // Scroll to bottom when messages change (only matters while open).
  useEffect(() => {
    if (open) messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMsg, open]);

  const suggestions = getSuggestions(ctx, studentGrade);

  return (
    <>
      {/* ── Floating action button ── */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          aria-label="Ask Sparky"
          className="fixed right-4 z-[55] bg-duo-green rounded-full p-1.5 shadow-xl active:scale-95 transition-transform"
          style={{ bottom: 'calc(64px + env(safe-area-inset-bottom, 0px) + 12px)' }}
        >
          <Sparky mood="happy" size={44} />
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-duo-blue rounded-full border-2 border-white flex items-center justify-center">
            <span className="text-white text-[9px] font-extrabold" aria-hidden="true">?</span>
          </span>
        </button>
      )}

      {/* ── Bottom sheet ── */}
      {open && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-[68] bg-black/30 animate-fade-in"
            onClick={() => setOpen(false)}
            aria-hidden="true"
          />

          {/* Sheet */}
          <div
            className="fixed bottom-0 left-0 right-0 max-w-lg mx-auto z-[70] flex flex-col bg-[#F0F4F8] rounded-t-2xl shadow-2xl animate-slide-up"
            style={{ height: 'min(85dvh, 640px)', paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}
            role="dialog"
            aria-label="Sparky chat"
          >
            {/* Header */}
            <div className="bg-duo-dark px-4 py-3 flex items-center gap-2 flex-shrink-0 rounded-t-2xl">
              <Sparky mood="happy" size={34} />
              <div className="flex-1 min-w-0">
                <p className="text-white font-extrabold text-sm leading-tight">Sparky</p>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-duo-green" />
                  <p className="text-white/60 text-xs truncate">
                    {ctx?.topicName ? `Helping with ${ctx.topicName}` : 'Math Tutor · Online'}
                  </p>
                </div>
              </div>
              <button
                onClick={startNewChat}
                className="text-white/70 hover:text-white text-xs font-bold px-2.5 py-1.5 rounded-full border border-white/20 hover:border-white/40 transition-colors min-h-[36px]"
              >
                New
              </button>
              <button
                onClick={() => setOpen(false)}
                aria-label="Close"
                className="text-white/70 hover:text-white text-xl font-bold min-h-[44px] min-w-[36px] flex items-center justify-center"
              >
                ✕
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-4">
              {!initialized && (
                <div className="flex flex-col items-center justify-center h-full gap-3">
                  <div className="animate-sparky-bounce">
                    <Sparky mood="thinking" size={64} />
                  </div>
                  <p className="text-gray-500 font-semibold text-sm">Loading…</p>
                </div>
              )}

              {initialized && messages.map((msg) => (
                <MessageBubble key={msg.id} msg={msg} studentInitial={studentInitial} />
              ))}

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

            {/* Suggestion chips */}
            {!isLoading && !rateLimited && (
              <div className="px-4 pb-2 flex-shrink-0">
                <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
                  {suggestions.map((s) => (
                    <button
                      key={s.label}
                      onClick={() => sendMessage(s.message, ctx)}
                      disabled={isLoading}
                      className="flex-shrink-0 bg-white border-2 border-duo-blue text-duo-blue text-xs font-bold rounded-full px-3 py-2 hover:bg-duo-blue hover:text-white transition-colors whitespace-nowrap min-h-[36px]"
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="bg-white px-4 py-3 flex-shrink-0 shadow-[0_-2px_10px_rgba(0,0,0,0.06)]">
              {rateLimited ? (
                <p className="text-center text-gray-500 text-sm font-medium py-2">
                  Daily limit reached 🌟 See you tomorrow!
                </p>
              ) : (
                <>
                  {remaining !== null && remaining <= 5 && (
                    <p className="text-center text-duo-orange text-xs font-bold mb-2">
                      ⚡ {remaining} {remaining === 1 ? 'chat' : 'chats'} left today
                    </p>
                  )}
                  <div className="flex items-center gap-3">
                    <input
                      ref={inputRef}
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(input, ctx); } }}
                      placeholder="Ask Sparky anything math…"
                      disabled={isLoading}
                      className="flex-1 bg-gray-100 rounded-full px-4 py-2.5 text-sm text-gray-800 outline-none focus:ring-2 focus:ring-duo-green font-medium placeholder-gray-400 min-h-[44px]"
                    />
                    <button
                      onClick={() => sendMessage(input, ctx)}
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
                </>
              )}
            </div>
          </div>
        </>
      )}
    </>
  );
}

// ── Outer gate — decides visibility; keeps the hook out of the tree entirely
//    when the widget should not show (no pre-login flash, no double fetch on
//    the full /chat page). ──────────────────────────────────────────────────

export default function SparkyWidget() {
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);
  const [studentId, setStudentId] = useState<string | null>(null);

  // Re-check login on every navigation so the widget appears right after
  // onboarding (which sets the id then client-navigates — no full reload).
  useEffect(() => {
    setMounted(true);
    try { setStudentId(localStorage.getItem('mathspark_student_id')); } catch { /* ignore */ }
  }, [pathname]);

  if (!mounted || !studentId) return null;
  // Hide on the same routes as the bottom nav, plus the full /chat page itself.
  if (isAppChromeHidden(pathname) || pathname === '/chat' || pathname.startsWith('/chat/')) return null;

  return <SparkyWidgetInner />;
}
