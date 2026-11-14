'use client';

import { useEffect, useRef, useState } from 'react';
import { usePathname } from 'next/navigation';
import Sparky from '@/components/Sparky';
import MessageBubble from '@/components/chat/MessageBubble';
import TypingDots from '@/components/chat/TypingDots';
import ChatComposer from '@/components/chat/ChatComposer';
import { useSparkyChat, getQuickReplies } from '@/components/chat/useSparkyChat';
import { useVoiceLoop } from '@/components/chat/useVoiceLoop';
import VisualBoard from '@/components/visuals/VisualBoard';
import { extractVisual } from '@/lib/visuals/spec';
import { useScreenContext, subscribeOpenSparky, type ScreenContext } from '@/lib/sparkyContext';
import { isAppChromeHidden } from '@/lib/navVisibility';

// ── Per-screen suggestion chips ───────────────────────────────────────────────

interface Suggestion { label: string; message: string }

function getSuggestions(ctx: ScreenContext | null, grade: number): Suggestion[] {
  if (ctx?.screen === 'practice' && ctx.questionText) {
    return [
      { label: 'Give me a hint 💡', message: 'Can you give me a hint for the question on my screen?' },
      { label: "I'm stuck 😅",     message: "I'm stuck on the question on my screen. Can you guide me?" },
      { label: 'Show me a similar one 📘', message: 'Can you show me a worked example of a similar question?' },
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
    attachment, attachmentNotice, attachImage, clearAttachment,
  } = useSparkyChat();

  // Voice conversation: what the child says is sent with the current screen context.
  const voice = useVoiceLoop((text) => sendMessage(text, ctx, { usePhoto: false }));

  const [open, setOpen] = useState(false);
  // On phones the sheet takes about half the screen so the question stays in
  // view; the child can stretch it for a long explanation.
  const [tall, setTall] = useState(false);
  // The question we have already asked Sparky to help with (hides the button until the next question).
  const [helpedQuestion, setHelpedQuestion] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-close the sheet whenever the student navigates to another page.
  useEffect(() => { setOpen(false); }, [pathname]);

  // Closing the widget ends a voice conversation.
  const stopVoice = voice.stop;
  useEffect(() => { if (!open) stopVoice(); }, [open, stopVoice]);

  // Let pages (e.g. the practice result bubble) open the widget.
  useEffect(() => subscribeOpenSparky(() => setOpen(true)), []);

  // Scroll to bottom when messages change (only matters while open).
  useEffect(() => {
    if (open) messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMsg, open]);

  const suggestions = getSuggestions(ctx, studentGrade);

  // The reply being streamed, split into what to read and what to draw.
  const live = extractVisual(streamingMsg);

  // The practice question on screen, if there is one: Sparky offers to help with it by default.
  const screenQuestion = ctx?.screen === 'practice' && ctx.questionText ? ctx.questionText : '';
  const canOfferHelp = screenQuestion !== '' && helpedQuestion !== screenQuestion;

  function helpWithScreenQuestion() {
    if (!screenQuestion || isLoading) return;
    const asked = screenQuestion;
    // Quote the question so the request still makes sense later in the conversation.
    sendMessage(`Please help me with this question: "${asked.slice(0, 600)}"`, ctx, { usePhoto: false })
      .then((reply) => {
        // Hide the button only once Sparky has actually answered; otherwise leave it for a retry.
        if (reply) setHelpedQuestion(asked);
      });
  }

  return (
    <>
      {/* ── Floating action button ── */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          aria-label="Ask Sparky"
          className="fixed right-4 z-[55] bg-white border-2 border-ink rounded-full p-1.5 shadow-hard-sm active:scale-95 transition-transform"
          style={{ bottom: 'calc(64px + env(safe-area-inset-bottom, 0px) + 12px)' }}
        >
          <Sparky mood="happy" size={44} />
          <span className="absolute -top-1 -right-1 w-4 h-4 bg-action rounded-full border-2 border-white flex items-center justify-center">
            <span className="text-white text-[9px] font-extrabold" aria-hidden="true">?</span>
          </span>
        </button>
      )}

      {/* ── Chat panel ──
          No backdrop: the page stays visible and usable behind it.
          Phones and tablets: a sheet over the lower half of the screen (the
          question stays in view above it), stretchable with the header button.
          Wide screens: a panel docked at the right, beside the page. */}
      {open && (
        <>
          <div
            className={`fixed z-[70] flex flex-col bg-paper border-ink animate-slide-up bottom-0 left-0 right-0 max-w-lg mx-auto rounded-t-card border-t-2 border-x-2 ${
              tall ? 'h-[88dvh]' : 'h-[56dvh]'
            } min-[1360px]:left-auto min-[1360px]:right-4 min-[1360px]:bottom-[84px] min-[1360px]:mx-0 min-[1360px]:w-[400px] min-[1360px]:max-w-none min-[1360px]:h-[min(78dvh,700px)] min-[1360px]:rounded-card min-[1360px]:border-2 min-[1360px]:shadow-hard`}
            style={{ paddingBottom: 'env(safe-area-inset-bottom, 0px)' }}
            role="dialog"
            aria-label="Sparky chat"
          >
            {/* Header */}
            <div className="bg-ink px-4 py-3 flex items-center gap-2 flex-shrink-0 rounded-t-2xl">
              <Sparky mood="happy" size={34} />
              <div className="flex-1 min-w-0">
                <p className="text-white font-extrabold text-sm leading-tight">Sparky</p>
                <div className="flex items-center gap-1.5">
                  <div className="w-1.5 h-1.5 rounded-full bg-success-soft" />
                  <p className="text-white/70 text-xs truncate">
                    {ctx?.topicName ? `Helping with ${ctx.topicName}` : 'Math Tutor · Online'}
                  </p>
                </div>
              </div>
              <button
                onClick={startNewChat}
                className="text-white/70 hover:text-white text-xs font-bold px-2.5 py-1.5 rounded-full border-2 border-white/30 hover:border-white/60 transition-colors min-h-[36px]"
              >
                New
              </button>
              <button
                onClick={() => setTall((t) => !t)}
                aria-label={tall ? 'Make the chat smaller' : 'Make the chat taller'}
                aria-pressed={tall}
                className="min-[1360px]:hidden text-white/70 hover:text-white text-xl font-bold min-h-[48px] min-w-[48px] flex items-center justify-center"
              >
                <span aria-hidden="true">{tall ? '▾' : '▴'}</span>
              </button>
              <button
                onClick={() => setOpen(false)}
                aria-label="Close"
                className="text-white/70 hover:text-white text-xl font-bold min-h-[48px] min-w-[48px] flex items-center justify-center"
              >
                ✕
              </button>
            </div>

            {/* The question on screen, with the default action */}
            {screenQuestion && (
              <div className="bg-white border-b-2 border-line px-4 py-3 flex-shrink-0">
                <p className="text-caption text-ink-muted">The question on your screen</p>
                <p className="text-label text-ink mt-0.5 line-clamp-2">{screenQuestion}</p>
                {canOfferHelp && !rateLimited && (
                  <button
                    type="button"
                    onClick={helpWithScreenQuestion}
                    disabled={isLoading}
                    className="ui-btn ui-btn-primary w-full mt-2"
                  >
                    Help me with this question
                  </button>
                )}
              </div>
            )}

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-4">
              {!initialized && (
                <div className="flex flex-col items-center justify-center h-full gap-3">
                  <div className="animate-sparky-bounce">
                    <Sparky mood="thinking" size={64} />
                  </div>
                  <p className="text-ink-muted font-semibold text-sm">Loading…</p>
                </div>
              )}

              {initialized && messages.map((msg) => (
                <MessageBubble key={msg.id} msg={msg} studentInitial={studentInitial} />
              ))}

              {live.text && (
                <div className="flex items-end gap-2 mb-3">
                  <div className="flex-shrink-0">
                    <Sparky mood="thinking" size={36} />
                  </div>
                  <div className={`bg-white rounded-card rounded-bl-sm px-4 py-2.5 border-2 border-line ${live.visual ? 'w-[92%]' : 'max-w-[85%]'}`}>
                    {live.visual && (
                      <div className="mb-3 pb-3 border-b-2 border-line">
                        <VisualBoard spec={live.visual} />
                      </div>
                    )}
                    <p className="text-[15px] leading-relaxed text-ink font-medium whitespace-pre-wrap [overflow-wrap:anywhere]">{live.text}</p>
                    <span className="inline-block w-1 h-4 bg-action animate-pulse ml-0.5 rounded" />
                  </div>
                </div>
              )}

              {isLoading && !live.text && (
                <div className="flex items-end gap-2 mb-3">
                  <Sparky mood="thinking" size={36} />
                  <div className="bg-white rounded-card rounded-bl-sm border-2 border-line">
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
                      onClick={() => sendMessage(s.message, ctx, { usePhoto: false })}
                      disabled={isLoading}
                      className="flex-shrink-0 bg-white border-2 border-line text-ink text-xs font-bold rounded-full px-3 py-2 hover:border-ink transition-colors whitespace-nowrap min-h-[36px]"
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="bg-white px-4 py-3 flex-shrink-0 border-t-2 border-line">
              {rateLimited ? (
                <p className="text-center text-ink-muted text-sm font-medium py-2">
                  Daily limit reached 🌟 See you tomorrow!
                </p>
              ) : (
                <>
                  {remaining !== null && remaining <= 5 && (
                    <p className="text-center text-hint-ink text-xs font-bold mb-2">
                      ⚡ {remaining} {remaining === 1 ? 'chat' : 'chats'} left today
                    </p>
                  )}
                  <ChatComposer
                    input={input}
                    setInput={setInput}
                    onSend={() => { sendMessage(input, ctx); }}
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
