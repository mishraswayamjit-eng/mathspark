export const dynamic = 'force-dynamic';

import { NextResponse } from 'next/server';
import { loadTrainer, TRAINER_SLUG_RE } from '@/lib/conceptTrainerData';

export async function GET(
  _req: Request,
  { params }: { params: { slug: string } },
) {
  const { slug } = params;

  if (!TRAINER_SLUG_RE.test(slug)) {
    return NextResponse.json({ error: 'Invalid slug' }, { status: 400 });
  }

  const data = loadTrainer(slug);
  if (!data) {
    return NextResponse.json({ error: 'Trainer not found' }, { status: 404 });
  }

  return NextResponse.json(data);
}
