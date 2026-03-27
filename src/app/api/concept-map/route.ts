import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';
import { prisma } from '@/lib/db';
import { getAuthenticatedStudentId } from '@/lib/studentAuth';
import { resolveLinksForGrade } from '@/data/conceptTopicMap';

export const dynamic = 'force-dynamic';

let cachedMap: Record<string, unknown> | null = null;
let cachedGraph: Record<string, unknown> | null = null;

function loadMap() {
  if (cachedMap) return cachedMap;
  const p = path.join(process.cwd(), 'data', 'concept-map.json');
  if (!fs.existsSync(p)) return null;
  cachedMap = JSON.parse(fs.readFileSync(p, 'utf-8'));
  return cachedMap;
}

function loadGraph() {
  if (cachedGraph) return cachedGraph;
  const p = path.join(process.cwd(), 'data', 'dependency-graph.json');
  if (!fs.existsSync(p)) return null;
  cachedGraph = JSON.parse(fs.readFileSync(p, 'utf-8'));
  return cachedGraph;
}

// GET /api/concept-map                → full map (nodes, edges, domains, gradeOverlays)
// GET /api/concept-map?domain=numbers → filter nodes by domain
// GET /api/concept-map?grade=4        → filter to grade overlay
// GET /api/concept-map?id=CN_001      → single concept detail (merged from both files) + links + progress
export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const id = searchParams.get('id');
    const domain = searchParams.get('domain');
    const grade = searchParams.get('grade');

    const mapData = loadMap() as {
      meta: Record<string, unknown>;
      nodes: Record<string, unknown>[];
      edges: Record<string, unknown>[];
    } | null;

    const graphData = loadGraph() as {
      meta: Record<string, unknown>;
      nodes: Record<string, unknown>[];
      edges: Record<string, unknown>[];
    } | null;

    if (!mapData) {
      return NextResponse.json({ error: 'Concept map not found' }, { status: 404 });
    }

    // Single concept detail — merge visual + dependency data + learning links
    if (id) {
      const mapNode = mapData.nodes.find((n) => n.id === id);
      const graphNode = graphData?.nodes.find((n) => n.id === id);
      if (!mapNode) {
        return NextResponse.json({ error: 'Concept not found' }, { status: 404 });
      }

      // Find prerequisite and dependent edges
      const edges = graphData?.edges ?? mapData.edges;
      const prerequisites = (edges as { source: string; target: string; type: string }[])
        .filter((e) => e.target === id)
        .map((e) => {
          const node = mapData.nodes.find((n) => n.id === e.source);
          return { id: e.source, name: (node as Record<string, unknown>)?.name ?? e.source, type: e.type };
        });
      const dependents = (edges as { source: string; target: string; type: string }[])
        .filter((e) => e.source === id)
        .map((e) => {
          const node = mapData.nodes.find((n) => n.id === e.target);
          return { id: e.target, name: (node as Record<string, unknown>)?.name ?? e.target, type: e.type };
        });

      // Resolve learning links + student progress
      let studentGrade: number | null = null;
      let studentId: string | null = null;
      try {
        studentId = await getAuthenticatedStudentId();
        if (studentId) {
          const student = await prisma.student.findUnique({
            where: { id: studentId },
            select: { grade: true },
          });
          studentGrade = student?.grade ?? null;
        }
      } catch {
        // Graceful fail for unauthenticated
      }

      const conceptGradeRange = (mapNode as Record<string, unknown>).gradeRange as number[] | undefined;
      const effectiveGrade = studentGrade ?? conceptGradeRange?.[0] ?? 4;
      const resolved = resolveLinksForGrade(id, effectiveGrade);

      // Build links object
      const links: Record<string, { url: string; label: string } | null> = {
        practice: resolved.practice ? { url: resolved.practice.url, label: resolved.practice.label } : null,
        flashcard: resolved.flashcard ? { url: resolved.flashcard.url, label: resolved.flashcard.label } : null,
        example: resolved.example ? { url: resolved.example.url, label: resolved.example.label } : null,
      };

      // Fetch progress data (only if authenticated and practice link exists)
      let progress: {
        mastery: string;
        attempted: number;
        correct: number;
        accuracy: number;
        difficultyBreakdown: { easy: number; medium: number; hard: number };
      } | null = null;
      let flashcardProgress: { totalCards: number; cardsSeen: number; avgBox: number } | null = null;

      if (studentId && resolved.practice) {
        const topicId = resolved.practice.topicId;

        const [progressRow, diffCounts] = await Promise.all([
          prisma.progress.findUnique({
            where: { studentId_topicId: { studentId, topicId } },
            select: { mastery: true, attempted: true, correct: true },
          }),
          prisma.question.groupBy({
            by: ['difficulty'],
            where: { topicId },
            _count: { id: true },
          }),
        ]);

        if (progressRow) {
          const breakdown = { easy: 0, medium: 0, hard: 0 };
          for (const row of diffCounts) {
            const d = row.difficulty.toLowerCase();
            if (d === 'easy') breakdown.easy = row._count.id;
            else if (d === 'medium') breakdown.medium = row._count.id;
            else if (d === 'hard') breakdown.hard = row._count.id;
          }
          progress = {
            mastery: progressRow.mastery,
            attempted: progressRow.attempted,
            correct: progressRow.correct,
            accuracy: progressRow.attempted > 0 ? Math.round((progressRow.correct / progressRow.attempted) * 100) : 0,
            difficultyBreakdown: breakdown,
          };
        } else {
          // No progress yet, but still show difficulty breakdown
          const breakdown = { easy: 0, medium: 0, hard: 0 };
          for (const row of diffCounts) {
            const d = row.difficulty.toLowerCase();
            if (d === 'easy') breakdown.easy = row._count.id;
            else if (d === 'medium') breakdown.medium = row._count.id;
            else if (d === 'hard') breakdown.hard = row._count.id;
          }
          progress = {
            mastery: 'NotStarted',
            attempted: 0,
            correct: 0,
            accuracy: 0,
            difficultyBreakdown: breakdown,
          };
        }
      }

      // Flashcard progress
      if (studentId && resolved.flashcard) {
        const fcTopicId = resolved.flashcard.topicId;
        const fcGrade = resolved.flashcard.grade;

        // Load flashcard data to count total cards for this deck
        const flashcardDataPath = path.join(process.cwd(), 'data', 'concept_flashcards_all_grades.json');
        let totalCards = 0;
        try {
          const fcData = JSON.parse(fs.readFileSync(flashcardDataPath, 'utf-8'));
          const cards = (fcData.cards as { topicId: string; grade: number; id: string }[])
            .filter((c) => c.topicId === fcTopicId && c.grade === fcGrade);
          totalCards = cards.length;

          if (totalCards > 0) {
            const cardIds = cards.map((c) => c.id);
            const fcProgress = await prisma.flashcardProgress.aggregate({
              where: { studentId, cardId: { in: cardIds } },
              _count: { id: true },
              _avg: { leitnerBox: true },
            });
            flashcardProgress = {
              totalCards,
              cardsSeen: fcProgress._count.id,
              avgBox: Math.round((fcProgress._avg.leitnerBox ?? 0) * 10) / 10,
            };
          }
        } catch {
          // Graceful fail if flashcard data unavailable
        }
      }

      return NextResponse.json({
        concept: { ...mapNode, ...graphNode },
        prerequisites,
        dependents,
        links,
        progress,
        flashcardProgress,
        studentGrade: studentGrade,
      });
    }

    let nodes = mapData.nodes;

    // Grade overlay filter
    if (grade) {
      const overlays = (mapData.meta as Record<string, unknown>)?.gradeOverlays as Record<string, string[]> | undefined;
      if (!overlays) {
        // Fall back to gradeRange filtering
        nodes = nodes.filter((n) => {
          const gr = n.gradeRange as number[] | undefined;
          return gr && gr.includes(Number(grade));
        });
      } else {
        // Use the precomputed gradeOverlays from concept-map.json
        // Merge all grades up to selected grade for cumulative view
        const gradeNum = Number(grade);
        const validIds = new Set<string>();
        for (let g = 2; g <= gradeNum; g++) {
          const ids = overlays[String(g)] as string[] | undefined;
          if (ids) ids.forEach((gid) => validIds.add(gid));
        }
        nodes = nodes.filter((n) => validIds.has(n.id as string));
      }
    }

    // Domain filter
    if (domain) {
      nodes = nodes.filter((n) => n.domain === domain);
    }

    // Build edge list filtered to visible nodes
    const nodeIds = new Set(nodes.map((n) => n.id as string));
    const edges = mapData.edges.filter(
      (e) => nodeIds.has((e as Record<string, unknown>).source as string) && nodeIds.has((e as Record<string, unknown>).target as string)
    );

    return NextResponse.json({
      meta: mapData.meta,
      nodes,
      edges,
      totalNodes: nodes.length,
      totalEdges: edges.length,
    });
  } catch (err) {
    console.error('[concept-map]', err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
