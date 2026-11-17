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
import { loadStreakAttempts } from '@/lib/student/streakData';

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

/**
 * One topic of the child's grade as the Progress page shows it: a topic-tree
 * node with the Brain Engine's stored numbers for it.
 */
interface DashboardNodeTopic {
  /** Topic-tree node id, e.g. "gr5_fractions". */
  id: string;
  name: string;
  emoji: string;
  /** Practice link that serves exactly this topic (with `?subTopic=` for keyed grades). */
  href: string;
  /** True for an extra-practice topic (not a chapter of the real paper). */
  extra: boolean;
  /** Answers the engine counted for this topic (its latest window of attempts). */
  attempted: number;
  /** Right answers among `attempted`. */
  correct: number;
  /** 0–1. */
  accuracy: number;
  /** Brain Engine mastery, 0–1. */
  mastery: number;
  /** "mastered" | "strong" | "developing" | "weak" | "not_started". */
  status: string;
}

const NODE_STATUSES = ['mastered', 'strong', 'developing', 'weak', 'not_started'];

/**
 * Per-topic rows for a keyed grade (grade2/3/5/6/7/8/9), where every topic
 * shares one database topic and the Progress table holds a single row for the
 * whole grade. One row per topic-tree node, in tree order, with the stored
 * per-node mastery (zeros for a node nothing is stored for). Null for a grade
 * whose topics each have their own database topic (Grade 4).
 */
function nodeTopicRows(storedMastery: unknown, grade: number): DashboardNodeTopic[] | null {
  const nodes = getTopicsForGrade(grade);
  if (!nodes.some((n) => Boolean(n.subTopicKey))) return null;

  let rows: unknown = storedMastery;
  if (typeof rows === 'string') {
    // Older rows may hold the JSON as a string.
    try { rows = JSON.parse(rows); } catch { rows = null; }
  }
  const byId: Record<string, { mastery: number; accuracy: number; attempted: number; status: string }> = {};
  if (Array.isArray(rows)) {
    for (let i = 0; i < rows.length; i++) {
      const row: unknown = rows[i];
      if (!row || typeof row !== 'object') continue;
      const entry = row as { topicId?: unknown; mastery?: unknown; accuracy?: unknown; attemptsCount?: unknown; status?: unknown };
      if (typeof entry.topicId !== 'string') continue;
      const mastery = typeof entry.mastery === 'number' && isFinite(entry.mastery) ? entry.mastery : 0;
      const accuracy = typeof entry.accuracy === 'number' && isFinite(entry.accuracy) ? entry.accuracy : 0;
      const attempted = typeof entry.attemptsCount === 'number' && isFinite(entry.attemptsCount) ? entry.attemptsCount : 0;
      const status = typeof entry.status === 'string' && NODE_STATUSES.indexOf(entry.status) !== -1
        ? entry.status
        : (attempted > 0 ? 'developing' : 'not_started');
      byId[entry.topicId] = { mastery, accuracy, attempted, status };
    }
  }

  return nodes.map((node) => {
    const stored = Object.prototype.hasOwnProperty.call(byId, node.id) ? byId[node.id] : null;
    const attempted = stored ? Math.max(0, Math.round(stored.attempted)) : 0;
    const accuracy = stored ? Math.min(1, Math.max(0, stored.accuracy)) : 0;
    return {
      id: node.id,
      name: node.name,
      emoji: node.emoji,
      href: practiceUrlForNode(node),
      extra: node.extra === true,
      attempted,
      correct: Math.round(accuracy * attempted),
      accuracy,
      mastery: stored ? Math.min(1, Math.max(0, stored.mastery)) : 0,
      status: stored && attempted > 0 ? stored.status : 'not_started',
    };
  });
}

// ── Route ─────────────────────────────────────────────────────────────────────

export const dynamic = 'force-dynamic';

// Per-child data: never stored by the browser or any shared cache.
const NO_STORE = { 'Cache-Control': 'private, no-store' };

// GET /api/dashboard
export async function GET() {
  try {
    const studentId = await getAuthenticatedStudentId();
    if (!studentId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401, headers: NO_STORE });
    }

    const now = new Date();
    const [student, progress, attempts, allTopics, analytics, streakAttempts, totalSolved] = await Promise.all([
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
      // When the child answered (times only, up to a year back): the streak and
      // the weekly chart. The 100 rows above are only the recent-activity list.
      loadStreakAttempts(studentId, now),
      // "Solved" is every right answer ever, not the right ones among the last 100.
      prisma.attempt.count({ where: { studentId, isCorrect: true } }),
    ]);

    if (!student) {
      return NextResponse.json({ error: 'Student not found' }, { status: 404, headers: NO_STORE });
    }

    // Keyed grades: one row per topic-tree node (null for Grade 4).
    const nodeTopics = nodeTopicRows(analytics?.topicMastery, student.grade);

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
          totalSolved,
          topicsMastered:   progress.filter((p) => p.mastery === 'Mastered').length,
          streakDays:       computeStreak(streakAttempts, false, now),
          totalLifetimeXP:  (student as unknown as { totalLifetimeXP?: number }).totalLifetimeXP ?? 0,
        },
        topics,
        // Keyed grades only (else null): per-topic rows from the topic tree and
        // the Brain Engine's per-node mastery. `topics` above stays as it was.
        nodeTopics,
        nodeTopicsMastered: nodeTopics
          ? nodeTopics.filter((t) => t.status === 'mastered').length
          : null,
        weeklyData:       computeWeeklyData(streakAttempts, false, now),
        weakestTopicId,
        weakestTopicName: weakest?.name ?? null,
        weakestTopicHref,
        weakestTopicLabel,
        recentActivity:   computeRecentActivity(attempts, topicMap),
        subscriptionTier: MONETIZATION_ENABLED
          ? ((student as { subscription?: { tier: number } | null }).subscription?.tier ?? 0)
          : UNLIMITED_TIER,
      },
      { headers: NO_STORE },
    );
  } catch (err) {
    logError('[dashboard]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500, headers: NO_STORE });
  }
}
