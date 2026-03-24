import { NextResponse } from 'next/server';
import * as fs from 'fs';
import * as path from 'path';

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
// GET /api/concept-map?id=CN_001      → single concept detail (merged from both files)
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

    // Single concept detail — merge visual + dependency data
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

      return NextResponse.json({
        concept: { ...mapNode, ...graphNode },
        prerequisites,
        dependents,
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
