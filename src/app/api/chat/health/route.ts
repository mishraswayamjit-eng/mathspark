import { NextResponse } from 'next/server';
import { verifySecret } from '@/lib/adminAuth';
import { checkRateLimit } from '@/lib/rateLimit';
import { logError } from '@/lib/logger';
import { getAnthropicClient } from '@/lib/llm/client';
import { MODELS } from '@/lib/llm/models';

export const dynamic = 'force-dynamic';

// GET /api/chat/health?secret=SEED_SECRET
// Admin diagnostic: makes one small call to the chat model (the one Sparky uses)
// and says whether it worked. The upstream error text goes to the server log,
// never into the response.
export async function GET(req: Request) {
  // One shared ceiling: this makes a billable call, so it cannot be looped.
  if (!checkRateLimit('chat-health', 5, 60_000)) {
    return NextResponse.json({ ok: false, error: 'Too many requests' }, { status: 429 });
  }

  const { searchParams } = new URL(req.url);
  if (!verifySecret(searchParams.get('secret'))) {
    return NextResponse.json({ ok: false, error: 'Unauthorized' }, { status: 401 });
  }

  const key = process.env.ANTHROPIC_API_KEY;

  if (!key) {
    return NextResponse.json({ ok: false, error: 'ANTHROPIC_API_KEY env var is not set or empty' }, { status: 500 });
  }
  if (key.startsWith('"') || key.endsWith('"') || key.includes(' ')) {
    return NextResponse.json({ ok: false, error: 'ANTHROPIC_API_KEY has extra quotes or spaces — fix in Vercel env vars' }, { status: 500 });
  }

  try {
    const anthropic = getAnthropicClient();
    // No `temperature`: the chat model does not accept it. Room for it to think
    // before the one-word reply.
    const msg = await anthropic.messages.create(
      {
        model:      MODELS.chat,
        max_tokens: 512,
        messages:   [{ role: 'user', content: 'Say "ok"' }],
      },
      { timeout: 20_000, maxRetries: 0 },
    );
    return NextResponse.json({
      ok:         true,
      model:      MODELS.chat,
      stopReason: msg.stop_reason,
    });
  } catch (err: unknown) {
    const e = err as { status?: number; name?: string };
    logError('[chat/health] the chat model call did not succeed', err);
    return NextResponse.json({
      ok:     false,
      model:  MODELS.chat,
      status: typeof e.status === 'number' ? e.status : null,
      error:  'The chat model call did not succeed. See the server log for the reason.',
    }, { status: 500 });
  }
}
