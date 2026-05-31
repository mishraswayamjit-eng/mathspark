'use client';

import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatWidgetProps {
  studentName: string;
  topicName: string;
  questionText: string;
}

const MAX_USER_MESSAGES = 10;

export default function ChatWidget({ studentName, topicName, questionText }: ChatWidgetProps) {
  const [isOpen,     setIsOpen]     = useState(false);
  const [messages,   setMessages]   = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [userCount,  setUserCount]  = useState(0);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef       = useRef<HTMLInputElement>(null);

  // Reset chat when question changes (new context = fresh conversation)
  useEffect(() => {
    setMessages([]);
    setUserCount(0);
  }, [questionText, topicName]);

  // Scroll to bottom when messages update
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen]);

  // Focus input when panel opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  async function sendMessage() {
    const trimmed = inputValue.trim();
    if (!trimmed || isStreaming || userCount >= MAX_USER_MESSAGES) return;

    const newUserMsg: Message = { role: 'user', content: trimmed };
    const updatedHistory = [...messages];

    setMessages((prev) => [...prev, newUserMsg]);
    setInputValue('');
    setUserCount((c) => c + 1);
    setIsStreaming(true);

    // Add a placeholder assistant message for streaming
    setMessages((prev) => [...prev, { role: 'assistant', content: '' }]);

    try {
      const res = await fetch('/api/chat', {
        method:  'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          studentName,
          topicName,
          questionText,
          message: trimmed,
          history: updatedHistory,
        }),
      });

      if (!res.ok || !res.body) {
        throw new Error(`HTTP ${res.status}`);
      }

      const reader  = res.body.getReader();
      const decoder = new TextDecoder();
      let   buffer  = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        // Process SSE lines
        const lines = buffer.split('\n');
        buffer = lines.pop() ?? '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const data = line.slice(6);
          if (data === '[DONE]') break;

          // Append chunk to the last (assistant) message
          setMessages((prev) => {
            const copy = [...prev];
            const last = copy[copy.length - 1];
            if (last && last.role === 'assistant') {
              copy[copy.length - 1] = { ...last, content: last.content + data };
            }
            return copy;
          });
        }
      }
    } catch {
      setMessages((prev) => {
        const copy = [...prev];
        const last = copy[copy.length - 1];
        if (last && last.role === 'assistant' && last.content === '') {
          copy[copy.length - 1] = {
            role:    'assistant',
            content: "Hmm, Spark is thinking too hard right now! Try again in a moment. 🤔",
          };
        }
        return copy;
      });
    } finally {
      setIsStreaming(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  const isLimitReached = userCount >= MAX_USER_MESSAGES;

  return (
    <>
      {/* ── Floating trigger button ── */}
      <button
        onClick={() => setIsOpen((o) => !o)}
        className="fixed bottom-24 right-4 z-50 flex items-center gap-1.5 bg-duo-blue text-white font-extrabold rounded-full shadow-xl
                   px-4 py-3 text-sm min-h-[48px] transition-transform active:scale-95
                   sm:px-4 sm:py-3"
        aria-label="Ask Spark — your math helper"
      >
        <span aria-hidden="true">✨</span>
        <span className="hidden sm:inline">Ask Spark</span>
      </button>

      {/* ── Chat panel ── */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-24 right-4 z-50 flex flex-col rounded-2xl shadow-2xl border border-gray-200 bg-white overflow-hidden w-[calc(100vw-2rem)] max-w-[320px] sm:w-80"
            style={{ height: '420px' }}
            role="dialog"
            aria-label="Spark — Math Helper Chat"
            initial={{ opacity: 0, y: 16, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 16, scale: 0.95 }}
            transition={{ duration: 0.22, ease: [0.22, 1, 0.36, 1] }}
          >
          {/* Header */}
          <div className="flex items-center justify-between bg-duo-blue px-4 py-3 flex-shrink-0">
            <div className="flex items-center gap-2">
              <span aria-hidden="true" className="text-xl">✨</span>
              <div>
                <p className="text-white font-extrabold text-sm leading-tight">Spark</p>
                <p className="text-white/70 text-[11px] font-semibold leading-tight">Your Math Helper</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white/70 hover:text-white font-bold text-xl min-h-[44px] min-w-[44px] flex items-center justify-center"
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3">
            {messages.length === 0 && (
              <div className="text-center py-6 space-y-2">
                <div className="text-3xl" aria-hidden="true">✨</div>
                <p className="text-sm font-bold text-gray-700">Hi{studentName ? `, ${studentName}` : ''}! I&apos;m Spark.</p>
                <p className="text-xs text-gray-500 leading-relaxed">
                  I&apos;m here to guide you — not give answers!<br />
                  Ask me about any step of this question. 🧮
                </p>
              </div>
            )}

            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'assistant' && (
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-duo-blue flex items-center justify-center text-[10px] mr-1.5 mt-0.5" aria-hidden="true">
                    ✨
                  </div>
                )}
                <div
                  className={`max-w-[80%] rounded-2xl px-3 py-2 text-sm leading-snug ${
                    msg.role === 'user'
                      ? 'bg-duo-blue text-white rounded-br-sm'
                      : 'bg-gray-100 text-gray-800 rounded-bl-sm'
                  }`}
                >
                  {msg.content === '' && msg.role === 'assistant' ? (
                    // Typing indicator
                    <span className="flex gap-1 py-0.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:0ms]" />
                      <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:150ms]" />
                      <span className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce [animation-delay:300ms]" />
                    </span>
                  ) : (
                    msg.content
                  )}
                </div>
              </div>
            ))}

            <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <div className="flex-shrink-0 border-t border-gray-100 px-3 py-2.5 bg-white">
            {isLimitReached ? (
              <p className="text-center text-xs font-semibold text-gray-500 py-1">
                You&apos;ve had a great session! Start a new practice to continue chatting. 🎉
              </p>
            ) : (
              <div className="flex gap-2 items-center">
                <input
                  ref={inputRef}
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={isStreaming}
                  placeholder="Ask Spark a question…"
                  maxLength={500}
                  className="flex-1 text-sm border border-gray-200 rounded-xl px-3 py-2 outline-none
                             focus:border-duo-blue focus:ring-1 focus:ring-duo-blue/30
                             disabled:opacity-50 min-h-[40px]"
                  aria-label="Type your question for Spark"
                />
                <button
                  onClick={sendMessage}
                  disabled={isStreaming || !inputValue.trim()}
                  className="bg-duo-blue text-white font-extrabold rounded-xl px-3 py-2 min-h-[40px] min-w-[40px]
                             flex items-center justify-center text-base
                             disabled:opacity-40 disabled:cursor-not-allowed
                             active:scale-95 transition-transform"
                  aria-label="Send message"
                >
                  {isStreaming ? (
                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" aria-hidden="true" />
                  ) : (
                    <span aria-hidden="true">→</span>
                  )}
                </button>
              </div>
            )}
          </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
