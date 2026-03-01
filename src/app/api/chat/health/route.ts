import Anthropic from '@anthropic-ai/sdk';
import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

// GET /api/chat/health
// Diagnostic: tests Anthropic connectivity. Open in browser to see the real error.
export async function GET() {
  const key = process.env.ANTHROPIC_API_KEY;

  if (!key) {
    return NextResponse.json({ ok: false, error: 'ANTHROPIC_API_KEY env var is not set or empty' }, { status: 500 });
  }
  if (key.startsWith('"') || key.endsWith('"') || key.includes(' ')) {
    return NextResponse.json({ ok: false, error: 'ANTHROPIC_API_KEY has extra quotes or spaces — fix in Vercel env vars' }, { status: 500 });
  }

  try {
    const anthropic = new Anthropic({ apiKey: key });
    const msg = await anthropic.messages.create({
      model:      'claude-haiku-4-5-20251001',
      max_tokens: 10,
      messages:   [{ role: 'user', content: 'Say "ok"' }],
    });
    return NextResponse.json({
      ok:    true,
      model: 'claude-haiku-4-5-20251001',
      reply: msg.content,
    });
  } catch (err: unknown) {
    const e = err as { status?: number; message?: string; error?: unknown };
    return NextResponse.json({
      ok:      false,
      status:  e.status,
      message: e.message,
      detail:  e.error,
    }, { status: 500 });
  }
}
