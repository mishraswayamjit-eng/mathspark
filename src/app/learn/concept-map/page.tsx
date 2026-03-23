'use client';

import { useEffect, useState, useCallback } from 'react';
import Link from 'next/link';
import Sparky from '@/components/Sparky';

// ── Types ─────────────────────────────────────────────────────────────────────

interface ConceptNode {
  id: string;
  name: string;
  domain: string;
  domainIsland: string;
  icon: string;
  color: string;
  x: number;
  y: number;
  size: number;
  gradeRange: number[];
  difficulty: number;
  questionCount: number;
  status: string;
  glowOnMastery: boolean;
  // from dependency-graph merge
  description?: string;
  linkedFlashcardIds?: string[];
  linkedDrillTopic?: string | null;
  estimatedMinutesToMaster?: number;
  masteryThreshold?: number;
}

interface ConceptEdge {
  source: string;
  target: string;
  type: string;
  style?: string;
}

interface DomainMeta {
  name: string;
  island: string;
  description: string;
}

interface ConceptDetail {
  concept: ConceptNode;
  prerequisites: { id: string; name: string; type: string }[];
  dependents: { id: string; name: string; type: string }[];
}

// ── Domain colors ─────────────────────────────────────────────────────────────

const DOMAIN_COLORS: Record<string, { bg: string; border: string; text: string; accent: string }> = {
  numbers:      { bg: '#ECFDF5', border: '#6EE7B7', text: '#065F46', accent: '#10B981' },
  arithmetic:   { bg: '#EFF6FF', border: '#93C5FD', text: '#1E3A8A', accent: '#3B82F6' },
  factors:      { bg: '#FEF3C7', border: '#FCD34D', text: '#78350F', accent: '#F59E0B' },
  fractions:    { bg: '#FFF7ED', border: '#FDBA74', text: '#7C2D12', accent: '#F97316' },
  percentage:   { bg: '#FDF2F8', border: '#F9A8D4', text: '#831843', accent: '#EC4899' },
  ratio:        { bg: '#F5F3FF', border: '#C4B5FD', text: '#4C1D95', accent: '#8B5CF6' },
  algebra:      { bg: '#EDE9FE', border: '#A78BFA', text: '#3730A3', accent: '#6366F1' },
  geometry:     { bg: '#ECFEFF', border: '#67E8F9', text: '#155E75', accent: '#06B6D4' },
  mensuration:  { bg: '#F0FDF4', border: '#86EFAC', text: '#14532D', accent: '#22C55E' },
  speed:        { bg: '#FEF2F2', border: '#FCA5A5', text: '#7F1D1D', accent: '#EF4444' },
  statistics:   { bg: '#F8FAFC', border: '#CBD5E1', text: '#1E293B', accent: '#64748B' },
  squares:      { bg: '#FFFBEB', border: '#FDE68A', text: '#713F12', accent: '#EAB308' },
  patterns:     { bg: '#FFF1F2', border: '#FDA4AF', text: '#881337', accent: '#F43F5E' },
  practical:    { bg: '#F0F9FF', border: '#7DD3FC', text: '#0C4A6E', accent: '#0EA5E9' },
  advanced:     { bg: '#FAF5FF', border: '#D8B4FE', text: '#581C87', accent: '#A855F7' },
};

function getDomainStyle(domain: string) {
  return DOMAIN_COLORS[domain] ?? { bg: '#F9FAFB', border: '#D1D5DB', text: '#374151', accent: '#6B7280' };
}

// ── Difficulty label ──────────────────────────────────────────────────────────

function diffLabel(d: number) {
  if (d <= 1) return { text: 'Easy', color: '#22C55E' };
  if (d <= 2) return { text: 'Medium', color: '#F59E0B' };
  if (d <= 3) return { text: 'Hard', color: '#EF4444' };
  return { text: 'Expert', color: '#8B5CF6' };
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ConceptMapPage() {
  const [nodes, setNodes] = useState<ConceptNode[]>([]);
  const [edges, setEdges] = useState<ConceptEdge[]>([]);
  const [domains, setDomains] = useState<Record<string, DomainMeta>>({});
  const [loading, setLoading] = useState(true);
  const [selectedGrade, setSelectedGrade] = useState<number | null>(null);
  const [expandedDomain, setExpandedDomain] = useState<string | null>(null);
  const [detail, setDetail] = useState<ConceptDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  // Fetch map data
  useEffect(() => {
    const qs = selectedGrade ? `?grade=${selectedGrade}` : '';
    setLoading(true);
    fetch(`/api/concept-map${qs}`)
      .then((r) => r.json())
      .then((data) => {
        setNodes(data.nodes ?? []);
        setEdges(data.edges ?? []);
        if (data.meta?.domains) setDomains(data.meta.domains);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [selectedGrade]);

  // Fetch concept detail
  const openDetail = useCallback((id: string) => {
    setDetailLoading(true);
    fetch(`/api/concept-map?id=${id}`)
      .then((r) => r.json())
      .then((data) => setDetail(data))
      .catch(() => {})
      .finally(() => setDetailLoading(false));
  }, []);

  // Group nodes by domain
  const grouped = new Map<string, ConceptNode[]>();
  for (const n of nodes) {
    const list = grouped.get(n.domain);
    if (list) list.push(n);
    else grouped.set(n.domain, [n]);
  }

  // Stats
  const totalNodes = nodes.length;
  const domainCount = grouped.size;

  // Edge counts per node (for showing connectivity)
  const edgeCounts = new Map<string, number>();
  for (const e of edges) {
    edgeCounts.set(e.source, (edgeCounts.get(e.source) ?? 0) + 1);
    edgeCounts.set(e.target, (edgeCounts.get(e.target) ?? 0) + 1);
  }

  const grades = [2, 3, 4, 5, 6, 7, 8, 9];

  return (
    <div className="min-h-screen bg-gray-50 pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-duo-dark px-4 py-4 flex items-center gap-3 shadow-md">
        <Link href="/home" className="text-white/60 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white font-extrabold text-lg">Concept Map</h1>
          <p className="text-white/50 text-xs font-medium">
            {totalNodes} concepts &middot; {domainCount} domains &middot; {edges.length} connections
          </p>
        </div>
        <span className="text-2xl">🗺️</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-gradient-to-r from-violet-50 to-purple-50 rounded-2xl px-4 py-3 border border-violet-200 mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-violet-800">Explore the Math Universe!</p>
            <p className="text-xs text-violet-600 mt-0.5">
              Each island is a math domain. Tap to explore concepts and see how they connect!
            </p>
          </div>
        </div>

        {/* Grade filter */}
        <div className="flex gap-1.5 mb-5 overflow-x-auto pb-1">
          <button
            onClick={() => setSelectedGrade(null)}
            className={`px-3 py-1.5 rounded-full text-xs font-bold border-2 shrink-0 transition-colors ${
              selectedGrade === null
                ? 'bg-duo-dark text-white border-duo-dark'
                : 'bg-white text-gray-600 border-gray-200'
            }`}
          >
            All Grades
          </button>
          {grades.map((g) => (
            <button
              key={g}
              onClick={() => setSelectedGrade(g)}
              className={`px-3 py-1.5 rounded-full text-xs font-bold border-2 shrink-0 transition-colors ${
                selectedGrade === g
                  ? 'bg-duo-dark text-white border-duo-dark'
                  : 'bg-white text-gray-600 border-gray-200'
              }`}
            >
              Grade {g}
            </button>
          ))}
        </div>

        {/* Loading */}
        {loading && (
          <div className="space-y-4">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-2xl p-4 border border-gray-100 animate-pulse h-28" />
            ))}
          </div>
        )}

        {/* Domain islands */}
        {!loading && (
          <div className="space-y-4">
            {Array.from(grouped.entries()).map(([domain, domainNodes]) => {
              const meta = domains[domain];
              const style = getDomainStyle(domain);
              const isExpanded = expandedDomain === domain;
              const connectionCount = domainNodes.reduce((sum, n) => sum + (edgeCounts.get(n.id) ?? 0), 0);

              return (
                <div
                  key={domain}
                  className="rounded-2xl overflow-hidden shadow-sm transition-shadow"
                  style={{ backgroundColor: style.bg, borderWidth: '2px', borderColor: style.border }}
                >
                  {/* Island header */}
                  <button
                    onClick={() => setExpandedDomain(isExpanded ? null : domain)}
                    className="w-full px-4 py-4 flex items-center gap-3 text-left active:opacity-80 transition-opacity"
                  >
                    <div
                      className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shrink-0 shadow-sm"
                      style={{ backgroundColor: style.accent + '20', border: `2px solid ${style.accent}40` }}
                    >
                      {meta?.name?.split(' ')[0] ?? '📘'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-extrabold leading-tight" style={{ color: style.text }}>
                        {meta?.island ?? domain}
                      </p>
                      <p className="text-xs font-medium mt-0.5" style={{ color: style.text + 'AA' }}>
                        {meta?.description ?? ''}
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: style.accent + '20', color: style.accent }}>
                          {domainNodes.length} concepts
                        </span>
                        <span className="text-[10px] font-bold text-gray-400">
                          {connectionCount} links
                        </span>
                      </div>
                    </div>
                    <span
                      className="text-sm transition-transform duration-200 shrink-0"
                      style={{ color: style.accent, transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
                    >
                      ▾
                    </span>
                  </button>

                  {/* Expanded: concept nodes */}
                  {isExpanded && (
                    <div className="px-4 pb-4 space-y-2 animate-fade-in">
                      <div className="border-t" style={{ borderColor: style.border }} />

                      {/* Mini graph: show connections within this domain */}
                      <DomainMiniGraph
                        nodes={domainNodes}
                        edges={edges.filter(
                          (e) =>
                            domainNodes.some((n) => n.id === e.source) &&
                            domainNodes.some((n) => n.id === e.target)
                        )}
                        style={style}
                        onNodeClick={openDetail}
                      />

                      {/* Concept list */}
                      <div className="space-y-1.5 mt-3">
                        {domainNodes
                          .sort((a, b) => a.difficulty - b.difficulty || a.gradeRange[0] - b.gradeRange[0])
                          .map((node) => {
                            const diff = diffLabel(node.difficulty);
                            const connections = edgeCounts.get(node.id) ?? 0;
                            return (
                              <button
                                key={node.id}
                                onClick={() => openDetail(node.id)}
                                className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-white/80 border active:bg-white transition-colors text-left"
                                style={{ borderColor: style.border }}
                              >
                                <span className="text-lg shrink-0">{node.icon}</span>
                                <div className="flex-1 min-w-0">
                                  <p className="text-xs font-extrabold text-gray-800 leading-tight truncate">{node.name}</p>
                                  <div className="flex items-center gap-1.5 mt-0.5">
                                    <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full text-white" style={{ backgroundColor: diff.color }}>
                                      {diff.text}
                                    </span>
                                    <span className="text-[9px] font-bold text-gray-400">
                                      G{node.gradeRange[0]}-{node.gradeRange[node.gradeRange.length - 1]}
                                    </span>
                                    {node.questionCount > 0 && (
                                      <span className="text-[9px] font-bold text-gray-400">
                                        {node.questionCount} Qs
                                      </span>
                                    )}
                                    {connections > 0 && (
                                      <span className="text-[9px] font-bold" style={{ color: style.accent }}>
                                        {connections} links
                                      </span>
                                    )}
                                  </div>
                                </div>
                                <span className="text-gray-300 text-xs shrink-0">→</span>
                              </button>
                            );
                          })}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Empty state */}
        {!loading && nodes.length === 0 && (
          <div className="flex flex-col items-center gap-4 py-12">
            <Sparky mood="thinking" size={64} />
            <p className="text-sm font-bold text-gray-500">No concepts found for this grade.</p>
            <button onClick={() => setSelectedGrade(null)} className="text-sm text-blue-500 underline">
              Show all grades
            </button>
          </div>
        )}
      </div>

      {/* ── Concept Detail Sheet ───────────────────────────────────────────── */}
      {(detail || detailLoading) && (
        <div className="fixed inset-0 z-50 flex items-end justify-center">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => { setDetail(null); setDetailLoading(false); }}
          />
          {/* Sheet */}
          <div className="relative w-full max-w-lg bg-white rounded-t-3xl shadow-2xl max-h-[85vh] overflow-y-auto animate-slide-up">
            {detailLoading && !detail ? (
              <div className="p-6 space-y-4 animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-48" />
                <div className="h-4 bg-gray-200 rounded w-full" />
                <div className="h-4 bg-gray-200 rounded w-3/4" />
              </div>
            ) : detail ? (
              <ConceptDetailSheet detail={detail} onClose={() => setDetail(null)} onNavigate={openDetail} />
            ) : null}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Mini Graph (SVG) ──────────────────────────────────────────────────────────

function DomainMiniGraph({
  nodes,
  edges,
  style,
  onNodeClick,
}: {
  nodes: ConceptNode[];
  edges: ConceptEdge[];
  style: { accent: string };
  onNodeClick: (id: string) => void;
}) {
  if (nodes.length <= 1) return null;

  // Layout nodes in a circle for clean visualization
  const W = 320;
  const H = Math.min(200, 80 + nodes.length * 12);
  const cx = W / 2;
  const cy = H / 2;
  const radius = Math.min(cx, cy) - 30;

  const positions = new Map<string, { x: number; y: number }>();
  nodes.forEach((n, i) => {
    const angle = (2 * Math.PI * i) / nodes.length - Math.PI / 2;
    positions.set(n.id, {
      x: cx + radius * Math.cos(angle),
      y: cy + radius * Math.sin(angle),
    });
  });

  return (
    <div className="flex justify-center">
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} className="overflow-visible">
        {/* Edges */}
        {edges.map((e, i) => {
          const s = positions.get(e.source);
          const t = positions.get(e.target);
          if (!s || !t) return null;
          return (
            <line
              key={i}
              x1={s.x} y1={s.y} x2={t.x} y2={t.y}
              stroke={e.type === 'must_know' ? style.accent : '#D1D5DB'}
              strokeWidth={e.type === 'must_know' ? 1.5 : 1}
              strokeDasharray={e.type === 'helpful' ? '4,3' : undefined}
              opacity={0.5}
            />
          );
        })}
        {/* Nodes */}
        {nodes.map((n) => {
          const pos = positions.get(n.id);
          if (!pos) return null;
          const r = Math.max(12, Math.min(20, 10 + n.questionCount / 50));
          return (
            <g
              key={n.id}
              onClick={() => onNodeClick(n.id)}
              style={{ cursor: 'pointer' }}
            >
              <circle
                cx={pos.x} cy={pos.y} r={r}
                fill="white"
                stroke={n.color || style.accent}
                strokeWidth={2}
              />
              <text
                x={pos.x} y={pos.y + 1}
                textAnchor="middle"
                dominantBaseline="central"
                fontSize={r * 0.9}
              >
                {n.icon}
              </text>
              <text
                x={pos.x} y={pos.y + r + 10}
                textAnchor="middle"
                fontSize="7"
                fill="#6B7280"
                fontWeight="600"
              >
                {n.name.length > 14 ? n.name.slice(0, 12) + '…' : n.name}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

// ── Concept Detail Sheet ──────────────────────────────────────────────────────

function ConceptDetailSheet({
  detail,
  onClose,
  onNavigate,
}: {
  detail: ConceptDetail;
  onClose: () => void;
  onNavigate: (id: string) => void;
}) {
  const { concept, prerequisites, dependents } = detail;
  const style = getDomainStyle(concept.domain);
  const diff = diffLabel(concept.difficulty);

  return (
    <div className="p-5 pb-8 space-y-4">
      {/* Handle bar */}
      <div className="flex justify-center -mt-1 mb-2">
        <div className="w-10 h-1 rounded-full bg-gray-300" />
      </div>

      {/* Header */}
      <div className="flex items-start gap-3">
        <div
          className="w-14 h-14 rounded-2xl flex items-center justify-center text-3xl shrink-0"
          style={{ backgroundColor: style.bg, border: `2px solid ${style.border}` }}
        >
          {concept.icon}
        </div>
        <div className="flex-1">
          <h2 className="text-base font-extrabold text-gray-800 leading-tight">{concept.name}</h2>
          <p className="text-xs text-gray-500 font-medium mt-0.5">{concept.domainIsland}</p>
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full text-white" style={{ backgroundColor: diff.color }}>
              {diff.text}
            </span>
            <span className="text-[10px] font-bold text-gray-400">
              Grades {concept.gradeRange[0]}–{concept.gradeRange[concept.gradeRange.length - 1]}
            </span>
            {concept.questionCount > 0 && (
              <span className="text-[10px] font-bold text-gray-400">
                {concept.questionCount} questions
              </span>
            )}
          </div>
        </div>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-xl shrink-0">×</button>
      </div>

      {/* Description */}
      {concept.description && (
        <div className="bg-gray-50 rounded-xl p-3 border border-gray-100">
          <p className="text-sm text-gray-700 font-medium leading-relaxed">{concept.description}</p>
        </div>
      )}

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-2">
        {concept.estimatedMinutesToMaster != null && (
          <div className="bg-blue-50 rounded-xl p-2.5 border border-blue-200 text-center">
            <p className="text-lg font-extrabold text-blue-600">{concept.estimatedMinutesToMaster}</p>
            <p className="text-[9px] font-bold text-blue-400 uppercase">min to master</p>
          </div>
        )}
        {concept.masteryThreshold != null && (
          <div className="bg-green-50 rounded-xl p-2.5 border border-green-200 text-center">
            <p className="text-lg font-extrabold text-green-600">{Math.round(concept.masteryThreshold * 100)}%</p>
            <p className="text-[9px] font-bold text-green-400 uppercase">mastery goal</p>
          </div>
        )}
        <div className="bg-purple-50 rounded-xl p-2.5 border border-purple-200 text-center">
          <p className="text-lg font-extrabold text-purple-600">{prerequisites.length + dependents.length}</p>
          <p className="text-[9px] font-bold text-purple-400 uppercase">connections</p>
        </div>
      </div>

      {/* Prerequisites */}
      {prerequisites.length > 0 && (
        <div>
          <p className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wide mb-2">
            Prerequisites ({prerequisites.length})
          </p>
          <div className="space-y-1.5">
            {prerequisites.map((p) => (
              <button
                key={p.id}
                onClick={() => onNavigate(p.id)}
                className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-red-50 border border-red-100 text-left active:bg-red-100 transition-colors"
              >
                <span className="text-sm shrink-0">{p.type === 'must_know' ? '🔴' : '🟡'}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-bold text-gray-800 truncate">{p.name}</p>
                  <p className="text-[9px] font-bold text-gray-400">{p.type === 'must_know' ? 'Must know first' : 'Helpful to know'}</p>
                </div>
                <span className="text-gray-300 text-xs shrink-0">→</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Leads to (dependents) */}
      {dependents.length > 0 && (
        <div>
          <p className="text-[10px] font-extrabold text-gray-400 uppercase tracking-wide mb-2">
            Unlocks ({dependents.length})
          </p>
          <div className="space-y-1.5">
            {dependents.map((d) => (
              <button
                key={d.id}
                onClick={() => onNavigate(d.id)}
                className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-green-50 border border-green-100 text-left active:bg-green-100 transition-colors"
              >
                <span className="text-sm shrink-0">{d.type === 'must_know' ? '🟢' : '🟡'}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-bold text-gray-800 truncate">{d.name}</p>
                  <p className="text-[9px] font-bold text-gray-400">{d.type === 'must_know' ? 'Requires this concept' : 'Benefits from this'}</p>
                </div>
                <span className="text-gray-300 text-xs shrink-0">→</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Sparky tip */}
      <div className="bg-purple-50 rounded-xl p-3 border border-purple-200 flex items-start gap-2">
        <Sparky mood="happy" size={28} />
        <div>
          <p className="text-[10px] font-extrabold text-purple-500 uppercase tracking-wide">Sparky Says</p>
          <p className="text-xs text-purple-800 font-medium mt-0.5 italic leading-snug">
            {prerequisites.length === 0
              ? "This is a starting concept — no prerequisites needed! Jump right in!"
              : `Master the ${prerequisites.length} prerequisite${prerequisites.length > 1 ? 's' : ''} first, then this will be a breeze!`}
          </p>
        </div>
      </div>
    </div>
  );
}
