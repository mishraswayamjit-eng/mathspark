import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { isLlmConfigured } from '@/lib/llm/client';
import type Anthropic from '@anthropic-ai/sdk';
import type { ChatScreenContext } from '@/lib/llm/guardrails';
import { buildTutorStablePrompt, buildTutorStudentPrompt } from '@/lib/llm/tutorPrompt';
import { streamChat } from '@/lib/llm/complete';
import { checkAndIncrementUsage } from '@/lib/llm/usage';
import type { LlmMessage } from '@/lib/llm/types';
import { PHOTO_NOTE } from '@/lib/chatPhotoNote';

export const dynamic = 'force-dynamic';
// NOTE: maxDuration is ignored on Vercel Hobby (10s hard limit). Only effective on Pro+.
export const maxDuration = 60;

// How many of the most recent messages Sparky sees on each turn.
const HISTORY_WINDOW = 40;
// Room for the model's reasoning plus a full worked explanation.
const MAX_REPLY_TOKENS = 16000;
// Longest typed message we accept (a pasted word problem with working fits easily).
const MAX_MESSAGE_CHARS = 6000;
// A photo arrives as base64 in the JSON body; Vercel caps a request at ~4.5 MB.
const MAX_IMAGE_BASE64_CHARS = 4_000_000;
const IMAGE_TYPES = {
  'image/jpeg': 'image/jpeg',
  'image/png': 'image/png',
  'image/webp': 'image/webp',
} as const;
// Shown if the model declines or returns no text.
const EMPTY_FALLBACK = "Hmm, I couldn't put that one into words. 🤔 Could you ask me in a different way?";
// Shown when the model call fails. Never fed back to the model as if Sparky had said it.
const ERROR_FALLBACK = "I'm having a little trouble thinking right now! 🤔 Could you try again in a moment?";

// ── POST /api/chat ────────────────────────────────────────────────────────────

export async function POST(req: Request) {
  const studentId = await getAuthenticatedStudentId();
  if (!studentId) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Rate limit: 10 messages per minute per student
  if (!checkRateLimit(`chat:${studentId}`, 10, 60_000)) {
    return Response.json({ error: 'Slow down a bit! Try again in a moment.' }, { status: 429 });
  }

  let sessionId: string | undefined;
  let message: string;
  let mode: string;
  let screenContext: ChatScreenContext | undefined;
  let imageBase64: string | undefined;
  let imageType: keyof typeof IMAGE_TYPES | undefined;
  try {
    const parsed = validateBody<{
      message: string; sessionId?: string; mode?: string; context?: Record<string, unknown>;
      imageBase64?: string; imageType?: string;
    }>(
      await req.json(),
      {
        message: 'string', sessionId: 'string?', mode: 'string?', context: 'object?',
        imageBase64: 'string?', imageType: 'string?',
      },
    );
    if (parsed.imageBase64) {
      const type = parsed.imageType ?? '';
      if (!(type in IMAGE_TYPES) || parsed.imageBase64.length > MAX_IMAGE_BASE64_CHARS
        || !/^[A-Za-z0-9+/]+=*$/.test(parsed.imageBase64)) {
        return Response.json({ error: 'That photo could not be used. Try a smaller or clearer one.' }, { status: 400 });
      }
      imageBase64 = parsed.imageBase64;
      imageType = type as keyof typeof IMAGE_TYPES;
    }
    sessionId = parsed.sessionId;
    message = parsed.message;
    mode = parsed.mode ?? 'general';
    // Sanitise/narrow the optional screen context — string fields only, NO answer.
    if (parsed.context && typeof parsed.context === 'object') {
      const c = parsed.context;
      screenContext = {
        screen:       typeof c.screen === 'string' ? c.screen : undefined,
        topicName:    typeof c.topicName === 'string' ? c.topicName : undefined,
        questionText: typeof c.questionText === 'string' ? c.questionText : undefined,
        options:      Array.isArray(c.options)
          ? c.options.filter((o): o is string => typeof o === 'string').slice(0, 6)
          : undefined,
        chosen:       typeof c.chosen === 'string' ? c.chosen : undefined,
        outcome:      c.outcome === 'right' || c.outcome === 'not yet' ? c.outcome : undefined,
      };
    }
  } catch (err) {
    if (err instanceof ValidationError) {
      return Response.json({ error: err.message }, { status: 400 });
    }
    return Response.json({ error: 'Invalid request body' }, { status: 400 });
  }

  if (typeof message !== 'string' || (!message.trim() && !imageBase64)) {
    return Response.json({ error: 'message required' }, { status: 400 });
  }
  if (message.length > MAX_MESSAGE_CHARS) {
    return Response.json({ error: 'Message too long' }, { status: 400 });
  }
  // What the child said, as text. With a photo and no words, ask for the obvious thing.
  const typed = message.trim() || 'Here is a photo of my working. Can you check it and help me?';

  // Rate limit / usage check
  const usage = await checkAndIncrementUsage(studentId, 'chat');
  if (!usage.allowed) {
    return Response.json(
      { error: 'Sparky needs to recharge! Keep practicing questions and chat again tomorrow 🔋' },
      { status: 429 },
    );
  }

  // Load student + their progress context
  const [student, progress] = await Promise.all([
    prisma.student.findUnique({
      where: { id: studentId },
      select: { id: true, name: true, grade: true },
    }),
    prisma.progress.findMany({
      where: { studentId },
      select: { topicId: true, mastery: true, attempted: true, correct: true, topic: { select: { name: true } } },
      orderBy: { updatedAt: 'desc' },
      take: 20,
    }),
  ]);

  if (!student) {
    return Response.json({ error: 'Student not found' }, { status: 404 });
  }

  // The child's practice record, so Sparky can recommend and pitch things properly.
  const progressLines = progress.map((p) => ({
    topicName: p.topic.name,
    mastery: p.mastery,
    attempted: p.attempted,
    correct: p.correct,
  }));

  // Get or create conversation session
  let session = sessionId
    ? await prisma.conversationSession.findUnique({
        where: { id: sessionId },
        include: { messages: { orderBy: { createdAt: 'desc' }, take: HISTORY_WINDOW } },
      })
    : null;

  // Ownership guard: never reuse a session owned by a different student. Without
  // this, a client passing someone else's sessionId would load the victim's
  // messages into the LLM context AND write new messages into their thread
  // (cross-child PII leak + tampering). Fall through to a fresh session, matching
  // the check in /api/chat/history.
  if (session && session.studentId !== studentId) {
    session = null;
  }

  if (!session) {
    session = await prisma.conversationSession.create({
      data: { studentId, mode },
      include: { messages: { orderBy: { createdAt: 'desc' }, take: HISTORY_WINDOW } },
    });
  }

  // Save user message
  await prisma.chatMessage.create({
    data: { sessionId: session.id, role: 'user', content: imageBase64 ? `${PHOTO_NOTE} ${typed}` : typed },
  });

  // Build conversation history for Anthropic: the most recent messages, oldest
  // first. (They are loaded newest-first so a long chat keeps its LATEST turns;
  // loading oldest-first kept only the first 20 messages of a session forever,
  // so Sparky could not see the question it had just asked.)
  const recent = [...session.messages].reverse();
  const history: LlmMessage[] = [];
  for (const m of recent) {
    const role: LlmMessage['role'] | null =
      m.role === 'assistant' ? 'assistant' : m.role === 'user' ? 'user' : null;
    if (!role) continue;
    if (role === 'assistant' && (m.content === ERROR_FALLBACK || m.content === EMPTY_FALLBACK)) continue;
    // The API needs the conversation to open with the student.
    if (history.length === 0 && role === 'assistant') continue;
    history.push({ role, content: m.content });
  }

  // This turn: the child's words, with the photo in front of them when there is one.
  const messages: Anthropic.MessageParam[] = history.map((m) => ({ role: m.role, content: m.content }));
  if (imageBase64 && imageType) {
    messages.push({
      role: 'user',
      content: [
        { type: 'image', source: { type: 'base64', media_type: IMAGE_TYPES[imageType], data: imageBase64 } },
        { type: 'text', text: typed },
      ],
    });
  } else {
    messages.push({ role: 'user', content: typed });
  }

  // Guard: API key must exist before we even open the stream
  if (!isLlmConfigured()) {
    logError('[chat] ANTHROPIC_API_KEY is not set');
    return Response.json({ error: 'AI tutor is not configured. Set ANTHROPIC_API_KEY in Vercel env vars.' }, { status: 503 });
  }

  const currentSessionId = session.id;

  const stream = streamChat(
    {
      model: 'chat',
      maxTokens: MAX_REPLY_TOKENS,
      system: [
        // Same for every student in a grade: cached by the API between turns.
        { type: 'text', text: buildTutorStablePrompt(student.grade), cache_control: { type: 'ephemeral' } },
        // Per student, per screen: after the cache point so it never invalidates it.
        { type: 'text', text: buildTutorStudentPrompt(student.grade, student.name, progressLines, screenContext) },
      ],
      messages,
    },
    {
      onErrorFallback: ERROR_FALLBACK,
      onEmptyFallback: EMPTY_FALLBACK,
      onError: (err) => {
        const e = err as { status?: number; message?: string };
        logError(`[chat] Anthropic error: ${e.status} ${e.message}`, err);
      },
      onComplete: async (text, truncated) => {
        if (!text) return;
        await prisma.chatMessage.create({
          data: {
            sessionId: currentSessionId,
            role: 'assistant',
            content: text,
            truncated,
          },
        });
      },
    },
  );

  return new Response(stream, {
    headers: {
      'Content-Type':  'text/plain; charset=utf-8',
      'Cache-Control': 'no-cache',
      'X-Session-Id':  currentSessionId,
      'X-Remaining':   String(usage.remaining),
    },
  });
}
