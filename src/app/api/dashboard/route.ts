import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { getTopicsCached } from '@/lib/topicCache';
import { TOPIC_ORDER, computeStreak, buildTopicNameMap, buildLookupMap } from '@/lib/sharedUtils';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { MONETIZATION_ENABLED, UNLIMITED_TIER } from '@/lib/monetization';
import { logError } from '@/lib/logger';
import { computeWeeklyData, computeRecentActivity } from '@/lib/studentDashboard';
import { getTopicsForGrade } from '@/data/topicTree';
import { buildPracticeUrl, practiceUrlForNode } from '@/lib/brain/practiceUrl';

/**
 * The weakest topic-tree node the child has started, from the Brain Engine's
 * stored per-node mastery. Only for keyed grades (grade2/3/5/6/7/8/9), where
 * every node shares one database topic and the Progress row is the whole
 * grade. Null when nothing is stored yet or nothing has been started.
 */
function weakestStartedNode(
  storedMastery: unknown,
  grade: number,
): { href: string; label: string } | null {
  const nodes = getTopicsForGrade(grade);
  if (!nodes.some((n) => Boolean(n.subTopicKey))) return null;

  let rows: unknown = storedMastery;
  if (typeof rows === 'string') {
    // Older rows may hold the JSON as a string.
    try { rows = JSON.parse(rows); } catch { return null; }
  }
  if (!Array.isArray(rows)) return null;

  let best: { href: string; label: string } | null = null;
  let bestMastery = Infinity;
  for (let i = 0; i < rows.length; i++) {
    const row: unknown = rows[i];
    if (!row || typeof row !== 'object') continue;
    const entry = row as { topicId?: unknown; mastery?: unknown; attemptsCount?: unknown; status?: unknown };
    const topicId = entry.topicId;
    const mastery = entry.mastery;
    const attemptsCount = entry.attemptsCount;
    if (typeof topicId !== 'string' || typeof mastery !== 'number') continue;
    if (typeof attemptsCount !== 'number' || attemptsCount <= 0) continue;
    if (entry.status === 'mastered') continue;
    if (mastery >= bestMastery) continue;
    // Only a node of the child's CURRENT grade (the grade can change).
    const node = nodes.find((n) => n.id === topicId);
    if (!node) continue;
    best = { href: practiceUrlForNode(node), label: node.name };
    bestMastery = mastery;
  }
  return best;
}

// ── Route ─────────────────────────────────────────────────────────────────────

export const dynamic = 'force-dynamic';

// GET /api/dashboard
export async function GET() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const [student, progress, attempts, allTopics, analytics] = await Promise.all([
      prisma.student.findUnique({
        where: { id: studentId },
        select: {
          id: true, name: true, displayName: true, grade: true,
          avatarColor: true, createdAt: true, currentLeagueTier: true,
          totalLifetimeXP: true, currentStreak: true, longestStreak: true,
          totalDaysPracticed: true, examName: true, examDate: true,
          dailyGoalMins: true, trialExpiresAt: true,
          subscription: { select: { tier: true } },
        },
      }),
      prisma.progress.findMany({ where: { studentId }, include: { topic: true } }),
      prisma.attempt.findMany({
        where: { studentId },
        select: {
          isCorrect: true,
          createdAt: true,
          question: { select: { topicId: true } },
        },
        orderBy: { createdAt: 'desc' },
        take: 100,
      }),
      getTopicsCached(),
      // Per-node mastery already worked out by the Brain Engine (read only; never recomputed here).
      prisma.studentAnalytics.findUnique({
        where: { studentId },
        select: { topicMastery: true },
      }),
    ]);

    if (!student) return NextResponse.json({ error: 'Student not found' }, { status: 404 });

    const topicMap = buildTopicNameMap(allTopics);

    const progressMap = buildLookupMap(progress, 'topicId');
    const gradeTopics = allTopics.filter((t) => t.grade === student.grade);
    const topics = gradeTopics
      .sort((a, b) => TOPIC_ORDER.indexOf(a.id) - TOPIC_ORDER.indexOf(b.id))
      .map((t) => {
        const p = progressMap.get(t.id);
        return {
          ...t,
          mastery:   p?.mastery   ?? 'NotStarted',
          attempted: p?.attempted ?? 0,
          correct:   p?.correct   ?? 0,
        };
      });

    // Prefer Practicing topics with lowest accuracy; fall back to any non-mastered
    const practicing = topics.filter((t) => t.mastery === 'Practicing');
    const fallback   = topics.filter((t) => t.attempted > 0 && t.mastery !== 'Mastered');
    const pool       = practicing.length > 0 ? practicing : fallback;
    const weakest    = pool.sort(
      (a, b) => (a.correct / Math.max(a.attempted, 1)) - (b.correct / Math.max(b.attempted, 1)),
    )[0];

    // A link that opens exactly the weakest topic. For a keyed grade the
    // Progress row above is the whole grade ("Grade 5"), so the sub-topic comes
    // from the engine's per-node mastery; otherwise the topic is already specific.
    const weakestTopicId = weakest?.id ?? topics[0]?.id ?? null;
    const weakestNode = weakestStartedNode(analytics?.topicMastery, student.grade);
    const weakestTopicHref = weakestNode
      ? weakestNode.href
      : weakestTopicId
        ? buildPracticeUrl(weakestTopicId)
        : '/chapters';
    const weakestTopicLabel = weakestNode ? weakestNode.label : (weakest?.name ?? null);

    return NextResponse.json(
      {
        student,
        stats: {
          totalSolved:      attempts.filter((a) => a.isCorrect).length,
          topicsMastered:   progress.filter((p) => p.mastery === 'Mastered').length,
          streakDays:       computeStreak(attempts),
          totalLifetimeXP:  (student as unknown as { totalLifetimeXP?: number }).totalLifetimeXP ?? 0,
        },
        topics,
        weeklyData:       computeWeeklyData(attempts),
        weakestTopicId,
        weakestTopicName: weakest?.name ?? null,
        weakestTopicHref,
        weakestTopicLabel,
        recentActivity:   computeRecentActivity(attempts, topicMap),
        subscriptionTier: MONETIZATION_ENABLED
          ? ((student as { subscription?: { tier: number } | null }).subscription?.tier ?? 0)
          : UNLIMITED_TIER,
      },
      {
        headers: {
          'Cache-Control': 'private, no-store',
        },
      },
    );
  } catch (err) {
    logError('[dashboard]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
