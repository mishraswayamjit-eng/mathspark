import Link from 'next/link';
import { getTopicsForGrade, type TopicNode } from '@/data/topicTree';
import { getTopicColor } from '@/data/topicColors';

// ── The one topic list ───────────────────────────────────────────────────────
// Learn and Practise → By topic both render this, from the topic tree, so the
// two tabs can never show different topics. Every row opens that topic's page
// (/topic/<nodeId>), which holds the lesson, practice, drill and the rest.
//
// A row is the same height with or without progress numbers, so nothing moves
// when they arrive late.

/** Which tab the list is shown on. The topic page uses it for its back arrow. */
export type TopicListOrigin = 'learn' | 'practice';

/** Progress on one database topic, as /api/dashboard reports it. */
export interface TopicProgress {
  mastery: string;
  attempted: number;
  correct: number;
}

/** True for a topic that is extra practice, not part of the exam syllabus. */
export function isExtraTopic(node: TopicNode): boolean {
  return (node as unknown as { extra?: boolean }).extra === true;
}

/**
 * The topics a child sees for a grade, in tree order. The whole-grade
 * past-paper pool (`…_ipm`) is not a topic: By topic shows it as its own card.
 */
export function getListedTopics(grade: number): TopicNode[] {
  return getTopicsForGrade(grade).filter((n) => n.id.slice(-4) !== '_ipm');
}

/** The link to a topic's page. */
export function topicPageHref(nodeId: string, from: TopicListOrigin, sample?: boolean): string {
  const qp: string[] = [];
  if (from === 'learn') qp.push('from=learn');
  if (sample) qp.push('sample=true');
  return `/topic/${encodeURIComponent(nodeId)}${qp.length > 0 ? `?${qp.join('&')}` : ''}`;
}

interface TopicListProps {
  grade: number;
  from: TopicListOrigin;
  /**
   * Progress by database topic id, or null when it is not known (yet). Topics
   * of a keyed grade share one database topic, so no numbers are shown for them.
   */
  progress?: Record<string, TopicProgress> | null;
  /** Carry "sample" access through to the topic page's practice link. */
  sample?: boolean;
}

function percentRight(p: TopicProgress): number {
  return p.attempted > 0 ? Math.round((p.correct / p.attempted) * 100) : 0;
}

function TopicRow({
  node,
  href,
  progress,
  suggested,
}: {
  node: TopicNode;
  href: string;
  progress: Record<string, TopicProgress> | null;
  suggested: boolean;
}) {
  // Sub-topics of a whole-grade pool share one progress record: its numbers
  // describe the grade, not this topic, so they are not shown.
  const sharesProgress = Boolean(node.subTopicKey);
  const own: TopicProgress | null =
    !sharesProgress && progress
      ? (Object.prototype.hasOwnProperty.call(progress, node.dbTopicId) ? progress[node.dbTopicId] : null)
      : null;
  const mastered = own !== null && own.mastery === 'Mastered';
  const pct = own ? percentRight(own) : 0;
  const color = getTopicColor(node.name);

  let status = 'Tap to open';
  if (!sharesProgress && progress) {
    if (own && own.mastery === 'Mastered') status = `Mastered · ${pct}% right`;
    else if (own && own.mastery === 'Practicing') status = `${own.correct} solved · ${pct}% right`;
    else status = 'Not started yet';
  }

  return (
    <Link
      href={href}
      className={`w-full bg-white rounded-card border-2 border-l-[10px] p-3 flex items-center gap-3 min-h-[76px] transition-transform active:scale-[0.98] ${
        suggested ? 'border-ink shadow-hard-sm' : 'border-line hover:border-ink'
      }`}
      style={{ borderLeftColor: color }}
    >
      {/* Emoji tile, tinted with the topic colour */}
      <span
        className="w-11 h-11 rounded-tile flex items-center justify-center text-xl leading-none shrink-0 select-none"
        style={{ backgroundColor: `${color}33` }}
        aria-hidden="true"
      >
        {node.emoji}
      </span>

      <span className="flex-1 min-w-0">
        <span className="block font-display text-title text-ink">{node.name}</span>
        <span className="block text-[13px] font-bold text-ink-muted mt-0.5">
          {suggested && <span className="text-action font-extrabold">Start here · </span>}
          {status}
        </span>
        {!sharesProgress && (
          <span className="block ui-meter h-2.5 mt-2">
            <span
              className={`block h-full rounded-full ${mastered ? 'bg-success' : 'bg-action'}`}
              style={{ width: `${own && own.attempted > 0 ? Math.max(4, pct) : 0}%` }}
            />
          </span>
        )}
      </span>

      <span className="text-2xl leading-none text-ink-muted shrink-0" aria-hidden="true">›</span>
    </Link>
  );
}

export default function TopicList({ grade, from, progress, sample }: TopicListProps) {
  const known = progress || null;
  const nodes = getListedTopics(grade);
  const exam: TopicNode[] = [];
  const extra: TopicNode[] = [];
  for (let i = 0; i < nodes.length; i++) {
    if (isExtraTopic(nodes[i])) extra.push(nodes[i]); else exam.push(nodes[i]);
  }

  if (nodes.length === 0) {
    return (
      <p className="text-center text-label text-ink-muted py-10">
        No topics here yet for Grade {grade}. More are on the way!
      </p>
    );
  }

  // Every topic is open. Once progress is known, the first exam topic that is
  // not mastered yet is suggested as the place to start.
  let suggestedId: string | null = null;
  if (known) {
    for (let i = 0; i < exam.length; i++) {
      const p = Object.prototype.hasOwnProperty.call(known, exam[i].dbTopicId) ? known[exam[i].dbTopicId] : null;
      if (!p || p.mastery !== 'Mastered') { suggestedId = exam[i].id; break; }
    }
  }

  const groups: { title: string; nodes: TopicNode[] }[] = [];
  if (exam.length > 0) groups.push({ title: 'Exam topics', nodes: exam });
  if (extra.length > 0) groups.push({ title: 'Extra practice', nodes: extra });

  return (
    <div className="space-y-6">
      {groups.map((group) => (
        <section key={group.title}>
          <h2 className="text-heading text-ink mb-3">{group.title}</h2>
          <ul className="space-y-3">
            {group.nodes.map((node) => (
              <li key={node.id}>
                <TopicRow
                  node={node}
                  href={topicPageHref(node.id, from, sample)}
                  progress={known}
                  suggested={node.id === suggestedId}
                />
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}
