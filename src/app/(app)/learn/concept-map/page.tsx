'use client';

import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Sparky from '@/components/Sparky';
import { logError } from '@/lib/logger';

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

interface ConceptLinks {
  practice: { url: string; label: string } | null;
  flashcard: { url: string; label: string } | null;
  example: { url: string; label: string } | null;
}

interface ConceptProgress {
  mastery: string;
  attempted: number;
  correct: number;
  accuracy: number;
  difficultyBreakdown: { easy: number; medium: number; hard: number };
}

interface ConceptFlashcardProgress {
  totalCards: number;
  cardsSeen: number;
  avgBox: number;
}

interface ConceptDetail {
  concept: ConceptNode;
  prerequisites: { id: string; name: string; type: string }[];
  dependents: { id: string; name: string; type: string }[];
  links?: ConceptLinks;
  progress?: ConceptProgress | null;
  flashcardProgress?: ConceptFlashcardProgress | null;
  studentGrade?: number | null;
}

// ── Domain colors ─────────────────────────────────────────────────────────────

const DOMAIN_COLORS: Record<string, { bg: string; border: string; text: string; accent: string }> = {
  numbers:      { bg: '#ECFDF5', border: '#6EE7B7', text: '#065F46', accent: '#58CC02' },
  arithmetic:   { bg: '#EFF6FF', border: '#93C5FD', text: '#1E3A8A', accent: '#3B82F6' },
  factors:      { bg: '#FEF3C7', border: '#FCD34D', text: '#78350F', accent: '#F59E0B' },
  fractions:    { bg: '#FFF7ED', border: '#FDBA74', text: '#7C2D12', accent: '#F97316' },
  percentage:   { bg: '#FDF2F8', border: '#F9A8D4', text: '#831843', accent: '#EC4899' },
  ratio:        { bg: '#F5F3FF', border: '#C4B5FD', text: '#4C1D95', accent: '#8B5CF6' },
  algebra:      { bg: '#EDE9FE', border: '#A78BFA', text: '#3730A3', accent: '#6366F1' },
  geometry:     { bg: '#ECFEFF', border: '#67E8F9', text: '#155E75', accent: '#06B6D4' },
  mensuration:  { bg: '#F0FDF4', border: '#86EFAC', text: '#14532D', accent: '#58CC02' },
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
  if (d <= 1) return { text: 'Easy', color: '#5d6b8c' };
  if (d <= 2) return { text: 'Medium', color: '#5d6b8c' };
  if (d <= 3) return { text: 'Hard', color: '#5d6b8c' };
  return { text: 'Expert', color: '#5d6b8c' };
}

// ── Progress Ring SVG ─────────────────────────────────────────────────────────

function ProgressRing({ accuracy, mastery, size = 64 }: { accuracy: number; mastery: string; size?: number }) {
  const strokeWidth = 5;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (accuracy / 100) * circumference;

  const color = mastery === 'Mastered' ? '#12805c' : mastery === 'Practicing' ? '#4f46e5' : '#5d6b8c';

  return (
    <svg width={size} height={size} className="shrink-0">
      <circle
        cx={size / 2} cy={size / 2} r={radius}
        fill="none" stroke="#d3deee" strokeWidth={strokeWidth}
      />
      <circle
        cx={size / 2} cy={size / 2} r={radius}
        fill="none" stroke={color} strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text
        x={size / 2} y={size / 2}
        textAnchor="middle" dominantBaseline="central"
        className="text-sm font-extrabold"
        fill={color}
      >
        {accuracy}%
      </text>
    </svg>
  );
}

// ── Chevron Right Icon ────────────────────────────────────────────────────────

function ChevronRight({ className }: { className?: string }) {
  return (
    <svg className={className ?? 'w-5 h-5 opacity-80 shrink-0'} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
    </svg>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function ConceptMapPage() {
  const searchParams = useSearchParams();
  const [nodes, setNodes] = useState<ConceptNode[]>([]);
  const [edges, setEdges] = useState<ConceptEdge[]>([]);
  const [domains, setDomains] = useState<Record<string, DomainMeta>>({});
  const [loading, setLoading] = useState(true);
  const [fetchError, setFetchError] = useState(false);
  const [selectedGrade, setSelectedGrade] = useState<number | null>(null);
  const [expandedDomain, setExpandedDomain] = useState<string | null>(null);
  const [detail, setDetail] = useState<ConceptDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  // Lock body scroll when detail sheet is open
  useEffect(() => {
    if (detail || detailLoading) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => { document.body.style.overflow = ''; };
  }, [detail, detailLoading]);

  // Auto-detect student grade on mount
  useEffect(() => {
    fetch('/api/dashboard')
      .then((r) => { if (!r.ok) throw new Error('Fetch failed'); return r.json(); })
      .then((data) => {
        if (data.grade && typeof data.grade === 'number') {
          setSelectedGrade(data.grade);
        }
      })
      .catch((err) => logError('[concept-map] fetch dashboard grade', err));
  }, []);

  // Fetch map data
  useEffect(() => {
    const qs = selectedGrade ? `?grade=${selectedGrade}` : '';
    setLoading(true);
    fetch(`/api/concept-map${qs}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => {
        setNodes(data.nodes ?? []);
        setEdges(data.edges ?? []);
        if (data.meta?.domains) setDomains(data.meta.domains);
      })
      .catch((err) => { logError('[fetch]', err); setFetchError(true); })
      .finally(() => setLoading(false));
  }, [selectedGrade]);

  // Fetch concept detail
  const openDetail = useCallback((id: string) => {
    setDetailLoading(true);
    fetch(`/api/concept-map?id=${id}`)
      .then((r) => { if (!r.ok) throw new Error("Fetch failed"); return r.json(); })
      .then((data) => setDetail(data))
      .catch((err) => logError('[fetch]', err))
      .finally(() => setDetailLoading(false));
  }, []);

  // Deep link: ?open=CN_XXX auto-opens the concept detail sheet
  useEffect(() => {
    const openId = searchParams.get('open');
    if (openId && !loading) {
      openDetail(openId);
    }
  }, [searchParams, loading, openDetail]);

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
    <div className="min-h-screen bg-paper pb-24 animate-fade-in">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link href="/chapters" className="text-white/70 hover:text-white text-lg font-bold">&larr;</Link>
        <div className="flex-1">
          <h1 className="text-white text-title">Concept Map</h1>
          <p className="text-white/70 text-xs font-medium">
            {totalNodes} concepts &middot; {domainCount} domains &middot; {edges.length} connections
          </p>
        </div>
        <span className="text-2xl" aria-hidden="true">🗺️</span>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5">
        {/* Intro */}
        <div className="bg-white rounded-card px-4 py-3 border-2 border-line mb-5 flex items-start gap-3">
          <Sparky mood="happy" size={36} />
          <div>
            <p className="text-sm font-bold text-ink">Explore the Math Universe!</p>
            <p className="text-xs text-ink-muted mt-0.5">
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
                ? 'bg-action text-white border-action'
                : 'bg-white text-ink border-line'
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
                  ? 'bg-action text-white border-action'
                  : 'bg-white text-ink border-line'
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
              <div key={i} className="bg-white rounded-card p-4 border-2 border-line animate-pulse h-28" />
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
                  className="rounded-card overflow-hidden"
                  style={{ backgroundColor: style.bg, borderWidth: '2px', borderColor: style.border }}
                >
                  {/* Island header */}
                  <button
                    onClick={() => setExpandedDomain(isExpanded ? null : domain)}
                    className="w-full px-4 py-4 flex items-center gap-3 text-left active:opacity-80 transition-opacity"
                  >
                    <div
                      className="w-12 h-12 rounded-tile flex items-center justify-center text-2xl shrink-0"
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
                        <span className="text-xs font-bold px-2 py-0.5 rounded-full" style={{ backgroundColor: style.accent + '20', color: style.accent }}>
                          {isExpanded ? 'Hide concepts' : `Show ${domainNodes.length} concepts`}
                        </span>
                        <span className="text-xs font-bold text-ink-muted">
                          {connectionCount} links
                        </span>
                      </div>
                    </div>
                    <svg
                      className="w-5 h-5 shrink-0 transition-transform duration-200"
                      style={{ color: style.text, transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={2.5}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {/* Expanded: concept nodes */}
                  {isExpanded && (
                    <div className="px-4 pb-4 space-y-2 animate-fade-in">
                      <div className="border-t-2" style={{ borderColor: style.border }} />

                      {/* Concept list */}
                      <div className="space-y-1.5 mt-3">
                        {domainNodes
                          .sort((a, b) => a.difficulty - b.difficulty || a.gradeRange[0] - b.gradeRange[0])
                          .map((node) => {
                            const diff = diffLabel(node.difficulty);
                            return (
                              <button
                                key={node.id}
                                onClick={() => openDetail(node.id)}
                                className="w-full flex items-center gap-3 px-3 py-3 rounded-control bg-white border-2 active:bg-white transition-colors text-left"
                                style={{ borderColor: style.border }}
                              >
                                <span className="text-xl shrink-0">{node.icon}</span>
                                <div className="flex-1 min-w-0">
                                  <p className="text-sm font-extrabold text-ink leading-tight truncate">{node.name}</p>
                                  <div className="flex items-center gap-1.5 mt-1">
                                    <span className="text-xs font-bold px-1.5 py-0.5 rounded-full text-white" style={{ backgroundColor: diff.color }}>
                                      {diff.text}
                                    </span>
                                    <span className="text-xs font-bold text-ink-muted">
                                      Grade {node.gradeRange[0]}-{node.gradeRange[node.gradeRange.length - 1]}
                                    </span>
                                    {node.questionCount > 0 && (
                                      <span className="text-xs font-bold text-ink-muted">
                                        {node.questionCount} Qs
                                      </span>
                                    )}
                                  </div>
                                </div>
                                <svg className="w-5 h-5 text-ink-muted shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                                </svg>
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

        {/* Error state */}
        {!loading && fetchError && (
          <div className="flex flex-col items-center gap-4 py-12">
            <p className="text-ink font-extrabold text-lg">Something went wrong</p>
            <p className="text-ink-muted text-sm">Could not load the concept map.</p>
            <button onClick={() => window.location.reload()} className="bg-action hover:bg-action-dark text-white font-extrabold px-6 py-2.5 rounded-control border-2 border-ink shadow-hard-sm text-sm active:scale-95 transition-transform">
              Retry
            </button>
          </div>
        )}

        {/* Empty state */}
        {!loading && !fetchError && nodes.length === 0 && (
          <div className="flex flex-col items-center gap-4 py-12">
            <Sparky mood="thinking" size={64} />
            <p className="text-sm font-bold text-ink-muted">No concepts found for this grade.</p>
            <button onClick={() => setSelectedGrade(null)} className="text-sm text-action font-bold underline">
              Show all grades
            </button>
          </div>
        )}
      </div>

      {/* ── Concept Detail Sheet ───────────────────────────────────────────── */}
      {(detail || detailLoading) && (
        <div className="fixed inset-0 z-[60] flex items-end justify-center">
          {/* Backdrop */}
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => { setDetail(null); setDetailLoading(false); }}
          />
          {/* Sheet */}
          <div className="relative w-full max-w-lg bg-white rounded-t-card border-2 border-b-0 border-ink max-h-[90vh] overflow-y-auto overscroll-contain animate-slide-up">
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
  const { concept, prerequisites, dependents, links, progress, flashcardProgress } = detail;
  const style = getDomainStyle(concept.domain);
  const diff = diffLabel(concept.difficulty);

  return (
    <div className="p-5 pb-[calc(2rem+env(safe-area-inset-bottom,0px))] space-y-4">
      {/* Handle bar */}
      <div className="flex justify-center -mt-1 mb-2">
        <div className="w-10 h-1 rounded-full bg-line" />
      </div>

      {/* Header */}
      <div className="flex items-start gap-3">
        <div
          className="w-14 h-14 rounded-tile flex items-center justify-center text-3xl shrink-0"
          style={{ backgroundColor: style.bg, border: `2px solid ${style.border}` }}
        >
          {concept.icon}
        </div>
        <div className="flex-1">
          <h2 className="text-title text-ink leading-tight">{concept.name}</h2>
          <p className="text-xs text-ink-muted font-medium mt-0.5">{concept.domainIsland}</p>
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className="text-xs font-bold px-2 py-0.5 rounded-full text-white" style={{ backgroundColor: diff.color }}>
              {diff.text}
            </span>
            <span className="text-xs font-bold text-ink-muted">
              Grades {concept.gradeRange[0]}–{concept.gradeRange[concept.gradeRange.length - 1]}
            </span>
            {concept.questionCount > 0 && (
              <span className="text-xs font-bold text-ink-muted">
                {concept.questionCount} questions
              </span>
            )}
          </div>
        </div>
        <button
          onClick={onClose}
          className="w-11 h-11 rounded-tile bg-white border-2 border-line flex items-center justify-center text-ink font-bold text-lg shrink-0 active:bg-soft transition-colors"
          aria-label="Close concept details"
        >
          ✕
        </button>
      </div>

      {/* Description */}
      {concept.description && (
        <div className="bg-soft rounded-control p-3 border-2 border-line">
          <p className="text-sm text-ink font-medium leading-relaxed">{concept.description}</p>
        </div>
      )}

      {/* ── Action Buttons ─────────────────────────────────────────────────── */}
      {links && (
        <div className="space-y-2">
          {links.practice && (
            <Link
              href={links.practice.url}
              className="flex items-center gap-3 px-4 py-3 rounded-control bg-action text-white border-2 border-ink shadow-hard-sm font-bold text-sm active:opacity-90 transition-opacity min-h-[48px]"
            >
              <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <div className="flex-1 min-w-0">
                <p className="font-extrabold">Practice Questions</p>
                {progress && progress.attempted > 0 && (
                  <p className="text-white/80 text-xs font-medium">
                    {progress.correct}/{progress.attempted} correct ({progress.accuracy}%)
                  </p>
                )}
              </div>
              <ChevronRight />
            </Link>
          )}

          {links.flashcard && (
            <Link
              href={links.flashcard.url}
              className="flex items-center gap-3 px-4 py-3 rounded-control bg-white text-ink border-2 border-ink shadow-hard-sm font-bold text-sm active:opacity-90 transition-opacity min-h-[48px]"
            >
              <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              <div className="flex-1 min-w-0">
                <p className="font-extrabold">Study Flashcards</p>
                {flashcardProgress && flashcardProgress.cardsSeen > 0 && (
                  <p className="text-ink-muted text-xs font-medium">
                    {flashcardProgress.cardsSeen}/{flashcardProgress.totalCards} cards reviewed
                  </p>
                )}
              </div>
              <ChevronRight />
            </Link>
          )}

          {links.example && (
            <Link
              href={links.example.url}
              className="flex items-center gap-3 px-4 py-3 rounded-control bg-white text-ink border-2 border-ink shadow-hard-sm font-bold text-sm active:opacity-90 transition-opacity min-h-[48px]"
            >
              <svg className="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              <div className="flex-1 min-w-0">
                <p className="font-extrabold">Watch Examples</p>
              </div>
              <ChevronRight />
            </Link>
          )}
        </div>
      )}

      {/* ── Your Progress ──────────────────────────────────────────────────── */}
      {progress && progress.mastery !== 'NotStarted' && (
        <div>
          <p className="text-[13px] font-extrabold text-ink-muted mb-2">
            Your Progress
          </p>
          <div className="bg-soft rounded-control p-3 border-2 border-line flex items-center gap-4">
            <ProgressRing accuracy={progress.accuracy} mastery={progress.mastery} />
            <div>
              <p className="text-sm font-extrabold text-ink">
                {progress.mastery === 'Mastered' ? 'Mastered' : 'Practicing'}
              </p>
              <p className="text-xs text-ink-muted font-medium mt-0.5">
                {progress.correct} of {progress.attempted} questions correct
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ── Difficulty Breakdown ───────────────────────────────────────────── */}
      {progress && (progress.difficultyBreakdown.easy + progress.difficultyBreakdown.medium + progress.difficultyBreakdown.hard) > 0 && (
        <div>
          <p className="text-[13px] font-extrabold text-ink-muted mb-2">
            Question Bank
          </p>
          <div className="grid grid-cols-3 gap-2">
            <div className="bg-soft rounded-control p-2.5 border-2 border-line text-center">
              <p className="text-lg font-extrabold text-ink">{progress.difficultyBreakdown.easy}</p>
              <p className="text-xs font-bold text-ink-muted">Easy</p>
            </div>
            <div className="bg-soft rounded-control p-2.5 border-2 border-line text-center">
              <p className="text-lg font-extrabold text-ink">{progress.difficultyBreakdown.medium}</p>
              <p className="text-xs font-bold text-ink-muted">Medium</p>
            </div>
            <div className="bg-soft rounded-control p-2.5 border-2 border-line text-center">
              <p className="text-lg font-extrabold text-ink">{progress.difficultyBreakdown.hard}</p>
              <p className="text-xs font-bold text-ink-muted">Hard</p>
            </div>
          </div>
        </div>
      )}

      {/* Prerequisites */}
      {prerequisites.length > 0 && (
        <div>
          <p className="text-[13px] font-extrabold text-ink-muted mb-2">
            Prerequisites ({prerequisites.length})
          </p>
          <div className="space-y-1.5">
            {prerequisites.map((p) => (
              <button
                key={p.id}
                onClick={() => onNavigate(p.id)}
                className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-control bg-white border-2 border-line text-left active:bg-soft transition-colors"
              >
                <span className="text-sm shrink-0" aria-hidden="true">{p.type === 'must_know' ? '🔒' : '🟡'}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-[13px] font-bold text-ink truncate">{p.name}</p>
                  <p className="text-xs font-bold text-ink-muted">{p.type === 'must_know' ? 'Must know first' : 'Helpful to know'}</p>
                </div>
                <svg className="w-4 h-4 text-ink-muted shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Leads to (dependents) */}
      {dependents.length > 0 && (
        <div>
          <p className="text-[13px] font-extrabold text-ink-muted mb-2">
            Unlocks ({dependents.length})
          </p>
          <div className="space-y-1.5">
            {dependents.map((d) => (
              <button
                key={d.id}
                onClick={() => onNavigate(d.id)}
                className="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-control bg-white border-2 border-line text-left active:bg-soft transition-colors"
              >
                <span className="text-sm shrink-0" aria-hidden="true">{d.type === 'must_know' ? '🟢' : '🟡'}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-[13px] font-bold text-ink truncate">{d.name}</p>
                  <p className="text-xs font-bold text-ink-muted">{d.type === 'must_know' ? 'Requires this concept' : 'Benefits from this'}</p>
                </div>
                <svg className="w-4 h-4 text-ink-muted shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* ── Smart Sparky Says ──────────────────────────────────────────────── */}
      <div className="bg-soft rounded-control p-3 border-2 border-line flex items-start gap-2">
        <Sparky mood="happy" size={28} />
        <div>
          <p className="text-[13px] font-extrabold text-ink-muted">Sparky Says</p>
          <p className="text-[13px] text-ink font-medium mt-0.5 italic leading-snug">
            {getSparkyMessage(progress, flashcardProgress, prerequisites, dependents)}
          </p>
        </div>
      </div>
    </div>
  );
}

// ── Smart Sparky Message ──────────────────────────────────────────────────────

function getSparkyMessage(
  progress: ConceptProgress | null | undefined,
  flashcardProgress: ConceptFlashcardProgress | null | undefined,
  prerequisites: { id: string; name: string; type: string }[],
  dependents: { id: string; name: string; type: string }[],
): string {
  // Mastered
  if (progress?.mastery === 'Mastered') {
    if (dependents.length > 0) {
      return `You've mastered this! Time to unlock ${dependents.length === 1 ? 'the next concept' : `the ${dependents.length} concepts`} that come next!`;
    }
    return "You've mastered this concept! Amazing work!";
  }

  // Practicing with high accuracy
  if (progress?.mastery === 'Practicing' && progress.accuracy >= 70) {
    return 'Great progress! Keep going for mastery!';
  }

  // Practicing with low accuracy
  if (progress?.mastery === 'Practicing' && progress.accuracy < 70) {
    return 'Try the worked examples first, then practice again!';
  }

  // Has flashcard progress but no practice
  if (flashcardProgress && flashcardProgress.cardsSeen > 0 && (!progress || progress.attempted === 0)) {
    return 'You know the cards — now test yourself with practice questions!';
  }

  // Has prerequisites, no progress
  if (prerequisites.length > 0 && (!progress || progress.attempted === 0)) {
    return `Master the ${prerequisites.length} prerequisite${prerequisites.length > 1 ? 's' : ''} first, then this will be a breeze!`;
  }

  // Starting concept (no prerequisites)
  if (prerequisites.length === 0) {
    return 'No prerequisites needed — jump right in!';
  }

  return 'Tap Practice Questions to get started!';
}
