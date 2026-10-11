import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { validateBody, ValidationError } from '@/lib/validateBody';
import { logError } from '@/lib/logger';
import { isLlmConfigured } from '@/lib/llm/client';
import { buildKidSafeSystemPrompt } from '@/lib/llm/guardrails';
import { streamCompletion } from '@/lib/llm/complete';
import { checkAndIncrementUsage } from '@/lib/llm/usage';
import type { LlmMessage } from '@/lib/llm/types';

export const dynamic = 'force-dynamic';
// NOTE: maxDuration is ignored on Vercel Hobby (10s hard limit). Only effective on Pro+.
export const maxDuration = 60;

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
  try {
    const parsed = validateBody<{ message: string; sessionId?: string; mode?: string }>(
      await req.json(),
      { message: 'string', sessionId: 'string?', mode: 'string?' },
    );
    sessionId = parsed.sessionId;
    message = parsed.message;
    mode = parsed.mode ?? 'general';
  } catch (err) {
    if (err instanceof ValidationError) {
      return Response.json({ error: err.message }, { status: 400 });
    }
    return Response.json({ error: 'Invalid request body' }, { status: 400 });
  }

  if (!message?.trim()) {
    return Response.json({ error: 'message required' }, { status: 400 });
  }
  if (typeof message !== 'string' || message.length > 2000) {
    return Response.json({ error: 'Message too long' }, { status: 400 });
  }

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

  // Build topic context string
  const mastered   = progress.filter((p) => p.mastery === 'Mastered').map((p) => p.topic.name);
  const practicing = progress.filter((p) => p.mastery === 'Practicing').map((p) => p.topic.name);
  const topicContext = [
    mastered.length   > 0 ? `Topics mastered: ${mastered.join(', ')}` : '',
    practicing.length > 0 ? `Currently practicing: ${practicing.join(', ')}` : '',
    mastered.length === 0 && practicing.length === 0 ? 'Just starting out — be especially encouraging!' : '',
  ].filter(Boolean).join('. ');

  // Get or create conversation session
  let session = sessionId
    ? await prisma.conversationSession.findUnique({
        where: { id: sessionId },
        include: { messages: { orderBy: { createdAt: 'asc' }, take: 20 } },
      })
    : null;

  if (!session) {
    session = await prisma.conversationSession.create({
      data: { studentId, mode },
      include: { messages: { orderBy: { createdAt: 'asc' }, take: 20 } },
    });
  }

  // Save user message
  await prisma.chatMessage.create({
    data: { sessionId: session.id, role: 'user', content: message.trim() },
  });

  // Build conversation history for Anthropic
  const history: LlmMessage[] = session.messages.map((m) => ({
    role: m.role as 'user' | 'assistant',
    content: m.content,
  }));
  history.push({ role: 'user', content: message.trim() });

  // Guard: API key must exist before we even open the stream
  if (!isLlmConfigured()) {
    logError('[chat] ANTHROPIC_API_KEY is not set');
    return Response.json({ error: 'AI tutor is not configured. Set ANTHROPIC_API_KEY in Vercel env vars.' }, { status: 503 });
  }

  const currentSessionId = session.id;

  const stream = streamCompletion(
    {
      model: 'sonnet',
      maxTokens: 300,
      system: buildKidSafeSystemPrompt(student.grade, student.name, topicContext),
      messages: history,
    },
    {
      onErrorFallback: "I'm having a little trouble thinking right now! 🤔 Could you try again in a moment?",
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
