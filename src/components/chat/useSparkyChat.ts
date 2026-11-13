'use client';

import { MS_PER_DAY } from '@/lib/timeConstants';
import { logError } from '@/lib/logger';
import { useCallback, useEffect, useRef, useState } from 'react';
import type { ScreenContext } from '@/lib/sparkyContext';

// Shared across the full /chat page AND the floating Sparky widget so both
// surfaces drive one conversation (persisted session id below).
const SESSION_KEY = 'mathspark_chat_session_id';

export interface ChatUiMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  /** Preview of a photo the child sent with this message (this session only). */
  imageUrl?: string;
}

/** A photo waiting to be sent with the next message. */
export interface ChatAttachment {
  /** data: URL for the on-screen preview. */
  previewUrl: string;
  /** The same image as bare base64, for the server. */
  base64: string;
  mediaType: 'image/jpeg';
}

// Photos are shrunk in the browser before upload: plenty for handwriting, small
// enough to send quickly on a phone connection.
const MAX_PHOTO_EDGE = 1600;

function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const el = new Image();
    el.onload = () => resolve(el);
    el.onerror = () => reject(new Error('unreadable image'));
    el.src = url;
  });
}

/** Shrink a picked photo to a JPEG no larger than MAX_PHOTO_EDGE on its long side. */
async function toAttachment(file: File): Promise<ChatAttachment> {
  const objectUrl = URL.createObjectURL(file);
  try {
    const img = await loadImage(objectUrl);
    const longest = Math.max(img.naturalWidth, img.naturalHeight) || 1;
    const scale = Math.min(1, MAX_PHOTO_EDGE / longest);
    const canvas = document.createElement('canvas');
    canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
    canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('no canvas');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    const previewUrl = canvas.toDataURL('image/jpeg', 0.85);
    return { previewUrl, base64: previewUrl.slice(previewUrl.indexOf(',') + 1), mediaType: 'image/jpeg' };
  } finally {
    URL.revokeObjectURL(objectUrl);
  }
}

// ── Quick reply chips — grade-aware ───────────────────────────────────────────

export const QUICK_REPLIES_BASE = [
  { label: 'Quiz me! 🎯',                message: 'Quiz me on something from my recent topics!' },
  { label: 'Help with homework 📝',       message: "I'm stuck on my homework. Can you help me?" },
  { label: 'What should I practice? 🤔', message: 'What topic should I practice next?' },
];

export const QUICK_REPLIES_BY_GRADE: Record<number, Array<{ label: string; message: string }>> = {
  2: [{ label: 'Counting 🔢', message: 'Help me understand counting and numbers!' }, { label: 'Addition ➕', message: 'Can you explain addition with examples?' }],
  3: [{ label: 'Multiplication ✖️', message: 'Help me with multiplication tables!' }, { label: 'Fractions 🍕', message: 'Help me understand fractions!' }],
  4: [{ label: 'Decimals 📊', message: 'Can you explain decimals to me in a simple way?' }, { label: 'BODMAS 🧮', message: 'Can you explain BODMAS with an example?' }],
  5: [{ label: 'Percentages %', message: 'Help me understand percentages!' }, { label: 'Algebra 🔤', message: 'Can you explain algebra basics?' }],
  6: [{ label: 'Ratios ⚖️', message: 'Help me understand ratios and proportions!' }, { label: 'Geometry 📐', message: 'Can you explain geometry concepts?' }],
  7: [{ label: 'Linear equations 📝', message: 'Help me solve linear equations!' }, { label: 'Integers 🔢', message: 'Can you explain integers?' }],
  8: [{ label: 'Quadratics ²', message: 'Help me understand quadratic equations!' }, { label: 'Statistics 📊', message: 'Can you explain statistics?' }],
  9: [{ label: 'Trigonometry 📐', message: 'Help me understand trigonometry!' }, { label: 'Polynomials 🔤', message: 'Can you explain polynomials?' }],
};

export function getQuickReplies(grade: number) {
  return [...QUICK_REPLIES_BASE, ...(QUICK_REPLIES_BY_GRADE[grade] ?? QUICK_REPLIES_BY_GRADE[4])];
}

// ── Proactive nudge logic ─────────────────────────────────────────────────────

function getOpeningMessage(name: string, grade: number, lastPracticeDate: string | null, streakDays: number): string {
  const today = new Date().toDateString();
  const yesterday = new Date(Date.now() - MS_PER_DAY).toDateString();

  if (!lastPracticeDate) {
    return `Hi ${name}! 🌟 I'm Sparky, your math buddy! I love helping with Grade ${grade} math. What would you like to explore today?`;
  }
  if (lastPracticeDate !== today && lastPracticeDate !== yesterday) {
    return `Hey ${name}! I missed you! 🔥 Want to keep your streak going? Let's solve some math together!`;
  }
  if (streakDays >= 3) {
    return `Hi ${name}! 🔥 You're on a ${streakDays}-day streak — amazing! Ready for some more math magic?`;
  }
  return `Hi ${name}! 🌟 Ready for some math magic today? Ask me anything or I can quiz you!`;
}

// ── Hook ──────────────────────────────────────────────────────────────────────

interface UseSparkyChatOptions {
  /** Called when there is no logged-in student (e.g. redirect to onboarding). */
  onNoStudent?: () => void;
}

export function useSparkyChat(opts: UseSparkyChatOptions = {}) {
  const { onNoStudent } = opts;

  const [studentId,    setStudentId]    = useState<string | null>(null);
  const [studentName,  setStudentName]  = useState('');
  const [studentGrade, setStudentGrade] = useState(4);
  const [sessionId,    setSessionId]    = useState<string | null>(null);
  const [messages,     setMessages]     = useState<ChatUiMessage[]>([]);
  const [input,        setInput]        = useState('');
  const [isLoading,    setIsLoading]    = useState(false);
  const [streamingMsg, setStreamingMsg] = useState('');
  const [rateLimited,  setRateLimited]  = useState(false);
  const [initialized,  setInitialized]  = useState(false);
  const [remaining,    setRemaining]    = useState<number | null>(null);
  const [attachment,   setAttachment]   = useState<ChatAttachment | null>(null);
  const [attachmentNotice, setAttachmentNotice] = useState('');

  const inputRef = useRef<HTMLInputElement>(null);

  // Keep the persisted session id in sync so a new conversation on /chat and the
  // widget (or vice-versa) continue the same thread.
  const persistSession = useCallback((id: string | null) => {
    try {
      if (id) localStorage.setItem(SESSION_KEY, id);
      else localStorage.removeItem(SESSION_KEY);
    } catch { /* ignore */ }
  }, []);

  // Boot: load student + rehydrate the shared session (persisted id first, else
  // most recent) + proactive opening nudge.
  useEffect(() => {
    const sid   = localStorage.getItem('mathspark_student_id');
    const name  = localStorage.getItem('mathspark_student_name') ?? '';
    const grade = parseInt(localStorage.getItem('mathspark_student_grade') ?? '4', 10);
    if (!sid) { onNoStudent?.(); setInitialized(true); return; }
    setStudentId(sid);
    setStudentName(name);
    setStudentGrade(isNaN(grade) ? 4 : grade);

    const persisted = (() => { try { return localStorage.getItem(SESSION_KEY); } catch { return null; } })();
    const url = persisted ? `/api/chat/history?sessionId=${encodeURIComponent(persisted)}` : '/api/chat/history';

    const showOpening = () => {
      const lastPractice = localStorage.getItem('mathspark_last_practice') ?? null;
      const streak = parseInt(localStorage.getItem('mathspark_streak') ?? '0', 10);
      const opening = getOpeningMessage(name || 'friend', isNaN(grade) ? 4 : grade, lastPractice, streak);
      setMessages([{ id: 'opening', role: 'assistant', content: opening }]);
    };

    fetch(url)
      .then((r) => { if (!r.ok) throw new Error('Fetch failed'); return r.json(); })
      .then((session) => {
        if (session?.messages?.length > 0) {
          setSessionId(session.id);
          persistSession(session.id);
          setMessages(session.messages.map((m: { id: string; role: 'user' | 'assistant'; content: string }) => ({
            id: m.id,
            role: m.role,
            content: m.content,
          })));
        } else {
          showOpening();
        }
        setInitialized(true);
      })
      .catch((err) => {
        logError('[sparky] fetch session history', err);
        showOpening();
        setInitialized(true);
      });
  }, []);  // eslint-disable-line react-hooks/exhaustive-deps

  // ── Photo of working ──────────────────────────────────────────────────────

  const attachImage = useCallback(async (file: File) => {
    setAttachmentNotice('');
    if (file.type.indexOf('image/') !== 0) {
      setAttachmentNotice('That file is not a picture. Try a photo of your working.');
      return;
    }
    try {
      setAttachment(await toAttachment(file));
    } catch {
      setAttachmentNotice("I couldn't open that photo. Try taking it again.");
    }
  }, []);

  const clearAttachment = useCallback(() => {
    setAttachment(null);
    setAttachmentNotice('');
  }, []);

  // ── Send message ──────────────────────────────────────────────────────────
  // Resolves with Sparky's full reply (or null if nothing was sent or it did
  // not come through), so voice mode can read the reply aloud.

  const sendMessage = useCallback(async (text: string, context?: ScreenContext | null): Promise<string | null> => {
    const photo = attachment;
    // With a photo and no words, say the obvious thing on the child's behalf.
    const trimmed = text.trim() || (photo ? 'Here is my working. Can you check it? 📷' : '');
    if (!trimmed || isLoading || !studentId) return null;

    setInput('');
    setAttachment(null);
    setAttachmentNotice('');
    setIsLoading(true);
    setStreamingMsg('');

    const userMsgId = `user-${Date.now()}`;
    setMessages((prev) => [...prev, {
      id: userMsgId, role: 'user', content: trimmed,
      ...(photo ? { imageUrl: photo.previewUrl } : {}),
    }]);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          message: trimmed,
          ...(context ? { context } : {}),
          ...(photo ? { imageBase64: photo.base64, imageType: photo.mediaType } : {}),
        }),
      });

      if (res.status === 429) {
        setRateLimited(true);
        // Two distinct 429 reasons: per-minute rate limit vs daily usage budget.
        let content = "You've been chatting a lot today — great work! 🌟 Come back tomorrow for more math adventures!";
        try {
          const body = await res.clone().json();
          if (typeof body?.error === 'string' && body.error) content = body.error;
        } catch { /* keep default */ }
        setMessages((prev) => [...prev, { id: `limit-${Date.now()}`, role: 'assistant', content }]);
        return null;
      }

      // Sparky is not switched on in this environment (no API key on the server).
      // Say so plainly instead of the generic retry message, which would never work.
      if (res.status === 503) {
        setMessages((prev) => [...prev, {
          id: `off-${Date.now()}`,
          role: 'assistant',
          content: "I'm not switched on here yet! 🔌 Ask a grown-up to check Sparky's settings, then try again.",
        }]);
        return null;
      }
      // Session expired: retrying will not help until the child logs in again.
      if (res.status === 401) {
        setMessages((prev) => [...prev, {
          id: `auth-${Date.now()}`,
          role: 'assistant',
          content: "I've lost track of who I'm talking to! 🙈 Please log in again and I'll be right here.",
        }]);
        return null;
      }

      if (!res.ok || !res.body) {
        logError(`[chat] /api/chat returned ${res.status}`);
        throw new Error('API error');
      }

      const remainingHeader = res.headers.get('X-Remaining');
      if (remainingHeader !== null) {
        const n = parseInt(remainingHeader, 10);
        if (!isNaN(n)) setRemaining(n);
      }

      // Reconcile sessionId from the server header. The server is the source of
      // truth: it may start a fresh session (we had none) OR hand back a
      // different id than we sent (e.g. ours expired / belonged to another
      // student). Always adopt the server's id so the widget and /chat page
      // keep driving the same persisted thread.
      const newSessionId = res.headers.get('X-Session-Id');
      if (newSessionId && newSessionId !== sessionId) {
        setSessionId(newSessionId);
        persistSession(newSessionId);
      }

      const reader  = res.body.getReader();
      const decoder = new TextDecoder();
      let fullText  = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        fullText += decoder.decode(value, { stream: true });
        setStreamingMsg(fullText);
      }

      if (fullText) {
        setMessages((prev) => [...prev, { id: `asst-${Date.now()}`, role: 'assistant', content: fullText }]);
      }
      return fullText || null;
    } catch {
      setMessages((prev) => [...prev, {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: "Oops! I had a little brain freeze 🤔 Can you try sending that again?",
      }]);
      return null;
    } finally {
      setIsLoading(false);
      setStreamingMsg('');
      inputRef.current?.focus();
    }
  }, [studentId, sessionId, isLoading, persistSession, attachment]);

  // ── New conversation ──────────────────────────────────────────────────────

  const startNewChat = useCallback(() => {
    setSessionId(null);
    persistSession(null);
    setRateLimited(false);
    setMessages([{
      id: `new-${Date.now()}`,
      role: 'assistant',
      content: `Starting fresh! 🌟 What math topic shall we explore today, ${studentName || 'friend'}?`,
    }]);
  }, [studentName, persistSession]);

  const studentInitial = studentName ? studentName[0].toUpperCase() : '?';

  return {
    studentId, studentName, studentGrade,
    messages, input, setInput,
    isLoading, streamingMsg, rateLimited, initialized, remaining,
    sendMessage, startNewChat,
    studentInitial, inputRef,
    attachment, attachmentNotice, attachImage, clearAttachment,
  };
}
