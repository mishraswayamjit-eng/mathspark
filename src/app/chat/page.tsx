'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Sparky from '@/components/Sparky';
import type { ChatMessage } from '@/types';

// ── Quick reply chips ─────────────────────────────────────────────────────────

const QUICK_REPLIES = [
  { label: 'Quiz me! 🎯',            message: 'Quiz me on something from my recent topics!' },
  { label: 'Explain decimals 📊',    message: 'Can you explain decimals to me in a simple way?' },
  { label: 'Help with homework 📝',  message: "I'm stuck on my homework. Can you help me?" },
  { label: 'What should I practice? 🤔', message: 'What topic should I practice next?' },
  { label: 'Fractions 🍕',           message: 'Help me understand fractions better!' },
  { label: 'BODMAS 🧮',              message: 'Can you explain BODMAS with an example?' },
];

// ── Proactive nudge logic ─────────────────────────────────────────────────────

function getOpeningMessage(name: string, lastPracticeDate: string | null, streakDays: number): string {
  const today = new Date().toDateString();
  const yesterday = new Date(Date.now() - 86400000).toDateString();

  if (!lastPracticeDate) {
    return `Hi ${name}! 🌟 I'm Sparky, your math buddy! I love helping with Grade 4 math. What would you like to explore today?`;
  }
  if (lastPracticeDate !== today && lastPracticeDate !== yesterday) {
    return `Hey ${name}! I missed you! 🔥 Want to keep your streak going? Let's solve some math together!`;
  }
  if (streakDays >= 3) {
    return `Hi ${name}! 🔥 You're on a ${streakDays}-day streak — amazing! Ready for some more math magic?`;
  }
  return `Hi ${name}! 🌟 Ready for some math magic today? Ask me anything or I can quiz you!`;
}

// ── Typing indicator ──────────────────────────────────────────────────────────

function TypingDots() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="w-2 h-2 rounded-full bg-gray-400"
          style={{ animation: `bounce 1.2s ease-in-out ${i * 0.2}s infinite` }}
        />
      ))}
    </div>
  );
}

// ── Message bubble ────────────────────────────────────────────────────────────

interface BubbleProps {
  msg: { role: 'user' | 'assistant'; content: string };
  studentInitial: string;
}

function MessageBubble({ msg, studentInitial }: BubbleProps) {
  const isUser = msg.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end items-end gap-2 mb-3">
        <div className="max-w-[78%] bg-[#58CC02] text-white rounded-2xl rounded-br-sm px-4 py-2.5 shadow-sm">
          <p className="text-sm leading-relaxed font-medium">{msg.content}</p>
        </div>
        <div className="w-8 h-8 rounded-full bg-[#1CB0F6] flex items-center justify-center text-white font-extrabold text-sm flex-shrink-0">
          {studentInitial}
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-end gap-2 mb-3">
      <div className="flex-shrink-0">
        <Sparky mood="happy" size={36} />
      </div>
      <div className="max-w-[78%] bg-white rounded-2xl rounded-bl-sm px-4 py-2.5 shadow-sm border border-gray-100">
        <p className="text-sm leading-relaxed text-gray-800 font-medium whitespace-pre-wrap">{msg.content}</p>
      </div>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export default function ChatPage() {
  const router = useRouter();

  const [studentId,    setStudentId]    = useState<string | null>(null);
  const [studentName,  setStudentName]  = useState('');
  const [sessionId,    setSessionId]    = useState<string | null>(null);
  const [messages,     setMessages]     = useState<Array<{ role: 'user' | 'assistant'; content: string; id: string }>>([]);
  const [input,        setInput]        = useState('');
  const [isLoading,    setIsLoading]    = useState(false);
  const [streamingMsg, setStreamingMsg] = useState('');
  const [rateLimited,  setRateLimited]  = useState(false);
  const [initialized,  setInitialized]  = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef       = useRef<HTMLInputElement>(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMsg]);

  // Boot: load student + session history + proactive nudge
  useEffect(() => {
    const sid  = localStorage.getItem('mathspark_student_id');
    const name = localStorage.getItem('mathspark_student_name') ?? '';
    if (!sid) { router.replace('/start'); return; }
    setStudentId(sid);
    setStudentName(name);

    // Try to load recent session history
    fetch(`/api/chat/history?studentId=${sid}`)
      .then((r) => r.json())
      .then((session) => {
        if (session?.messages?.length > 0) {
          setSessionId(session.id);
          setMessages(session.messages.map((m: { id: string; role: 'user' | 'assistant'; content: string }) => ({
            id: m.id,
            role: m.role,
            content: m.content,
          })));
        } else {
          // No history — show proactive opening message
          const lastPractice = localStorage.getItem('mathspark_last_practice') ?? null;
          const streak = parseInt(localStorage.getItem('mathspark_streak') ?? '0', 10);
          const opening = getOpeningMessage(name || 'friend', lastPractice, streak);
          setMessages([{ id: 'opening', role: 'assistant', content: opening }]);
        }
        setInitialized(true);
      })
      .catch(() => {
        // Fallback opening on error
        const opening = getOpeningMessage(name || 'friend', null, 0);
        setMessages([{ id: 'opening', role: 'assistant', content: opening }]);
        setInitialized(true);
      });
  }, [router]);

  // ── Send message ──────────────────────────────────────────────────────────

  const sendMessage = useCallback(async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading || !studentId) return;

    setInput('');
    setIsLoading(true);
    setStreamingMsg('');

    // Optimistically add user message
    const userMsgId = `user-${Date.now()}`;
    setMessages((prev) => [...prev, { id: userMsgId, role: 'user', content: trimmed }]);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          studentId,
          sessionId,
          message: trimmed,
        }),
      });

      if (res.status === 429) {
        setRateLimited(true);
        setMessages((prev) => [...prev, {
          id: `limit-${Date.now()}`,
          role: 'assistant',
          content: "You've been chatting a lot today — great work! 🌟 Come back tomorrow for more math adventures!",
        }]);
        return;
      }

      if (!res.ok || !res.body) {
        throw new Error('API error');
      }

      // Capture sessionId from header
      const newSessionId = res.headers.get('X-Session-Id');
      if (newSessionId && !sessionId) setSessionId(newSessionId);

      // Stream the response
      const reader  = res.body.getReader();
      const decoder = new TextDecoder();
      let fullText  = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        fullText += decoder.decode(value, { stream: true });
        setStreamingMsg(fullText);
      }

      // Move streaming text into messages list
      if (fullText) {
        setMessages((prev) => [...prev, {
          id: `asst-${Date.now()}`,
          role: 'assistant',
          content: fullText,
        }]);
      }
    } catch {
      setMessages((prev) => [...prev, {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: "Oops! I had a little brain freeze 🤔 Can you try sending that again?",
      }]);
    } finally {
      setIsLoading(false);
      setStreamingMsg('');
      inputRef.current?.focus();
    }
  }, [studentId, sessionId, isLoading]);

  // ── New conversation ──────────────────────────────────────────────────────

  function startNewChat() {
    setSessionId(null);
    setMessages([{
      id: `new-${Date.now()}`,
      role: 'assistant',
      content: `Starting fresh! 🌟 What math topic shall we explore today, ${studentName || 'friend'}?`,
    }]);
  }

  const studentInitial = studentName ? studentName[0].toUpperCase() : '?';

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="flex flex-col bg-[#F0F4F8]" style={{ height: 'calc(100vh - 64px)' }}>

      {/* ── Header ── */}
      <div className="bg-[#131F24] px-4 py-3 flex items-center gap-3 flex-shrink-0 shadow-md">
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
              <div className="w-1.5 h-1.5 rounded-full bg-[#58CC02]" />
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
            <p className="text-gray-400 font-semibold">Loading…</p>
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
              <span className="inline-block w-1 h-4 bg-[#58CC02] animate-pulse ml-0.5 rounded" />
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
            {QUICK_REPLIES.map((qr) => (
              <button
                key={qr.label}
                onClick={() => sendMessage(qr.message)}
                disabled={isLoading}
                className="flex-shrink-0 bg-white border-2 border-[#1CB0F6] text-[#1CB0F6] text-xs font-bold rounded-full px-3 py-2 hover:bg-[#1CB0F6] hover:text-white transition-colors whitespace-nowrap min-h-[36px]"
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
          <p className="text-center text-gray-400 text-sm font-medium py-2">
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
              className="flex-1 bg-gray-100 rounded-full px-4 py-2.5 text-sm text-gray-800 outline-none focus:ring-2 focus:ring-[#58CC02] font-medium placeholder-gray-400 min-h-[44px]"
            />
            <button
              onClick={() => sendMessage(input)}
              disabled={isLoading || !input.trim()}
              className="w-11 h-11 rounded-full bg-[#58CC02] disabled:bg-gray-200 flex items-center justify-center transition-colors flex-shrink-0"
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
