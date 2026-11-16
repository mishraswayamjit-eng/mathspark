import type { Metadata } from 'next';
import Link from 'next/link';
import { TOPIC_TREE, type TopicNode } from '@/data/topicTree';
import { practiceUrlForNode } from '@/lib/brain/practiceUrl';
import TopicLinkRow from '@/components/topics/TopicLinkRow';
import { isExtraTopic } from '@/components/topics/TopicList';
import { buildTopicSections, practiceSummary } from './topicContent';

// One page per topic: Practise first, then whatever else exists for the topic
// (lesson, drill, tricks, stories, flashcards, solved examples). The topic tree
// and the content map are static, so this is a server component: nothing is
// fetched in the browser and nothing arrives late.

interface TopicPageProps {
  params: { nodeId: string };
  searchParams?: Record<string, string | string[] | undefined>;
}

function findNode(rawId: string): TopicNode | null {
  let id = rawId;
  try { id = decodeURIComponent(rawId); } catch { /* keep the raw id */ }
  for (let i = 0; i < TOPIC_TREE.length; i++) {
    if (TOPIC_TREE[i].id === id) return TOPIC_TREE[i];
  }
  return null;
}

function firstValue(value: string | string[] | undefined): string {
  if (Array.isArray(value)) return value.length > 0 ? value[0] : '';
  return value || '';
}

export function generateMetadata({ params }: TopicPageProps): Metadata {
  const node = findNode(params.nodeId);
  return { title: node ? node.name : 'Topic' };
}

export default function TopicPage({ params, searchParams }: TopicPageProps) {
  const node = findNode(params.nodeId);
  const fromLearn = firstValue(searchParams ? searchParams.from : undefined) === 'learn';
  const sample = firstValue(searchParams ? searchParams.sample : undefined) === 'true';
  const backHref = fromLearn ? '/learn' : '/chapters';

  if (!node) {
    return (
      <div className="min-h-screen bg-paper pb-24">
        <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
          <Link
            href={backHref}
            aria-label="Back"
            className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center"
          >
            &larr;
          </Link>
          <h1 className="text-white text-title">Topic</h1>
        </div>
        <div className="max-w-lg mx-auto px-4 pt-10 text-center">
          <p className="text-5xl" aria-hidden="true">🔎</p>
          <p className="font-display text-heading text-ink mt-3">We couldn&apos;t find that topic</p>
          <p className="text-label text-ink-muted mt-1">Let&apos;s pick one from the list instead.</p>
          <Link href={backHref} className="ui-btn ui-btn-primary mt-5">
            See all topics
          </Link>
        </div>
      </div>
    );
  }

  const basePracticeHref = practiceUrlForNode(node);
  const practiceHref = sample
    ? `${basePracticeHref}${basePracticeHref.indexOf('?') === -1 ? '?' : '&'}sample=true`
    : basePracticeHref;
  const sections = buildTopicSections(node);

  return (
    <div className="min-h-screen bg-paper pb-24">
      {/* Header */}
      <div className="sticky top-0 z-40 bg-ink px-4 py-4 flex items-center gap-3">
        <Link
          href={backHref}
          aria-label="Back"
          className="text-white/70 hover:text-white text-lg font-bold min-h-[48px] min-w-[48px] flex items-center justify-center"
        >
          &larr;
        </Link>
        <span className="text-2xl leading-none shrink-0" aria-hidden="true">{node.emoji}</span>
        <h1 className="text-white text-title flex-1 min-w-0">{node.name}</h1>
      </div>

      <div className="max-w-lg mx-auto px-4 pt-5 space-y-6">
        {/* Practise: always here, always first */}
        <section aria-labelledby="topic-practise" className="ui-card ui-card-pop">
          <div className="flex flex-wrap items-center gap-2">
            <span className="ui-chip">Grade {node.grade}</span>
            {isExtraTopic(node) && <span className="ui-chip">Extra practice</span>}
          </div>
          <h2 id="topic-practise" className="text-heading text-ink mt-3">Practise</h2>
          <p className="text-label text-ink-muted mt-1">{practiceSummary(node)}</p>
          <Link href={practiceHref} className="ui-btn ui-btn-primary w-full mt-4" data-testid="topic-practise">
            Start practising →
          </Link>
        </section>

        {sections.map((section) => (
          <section key={section.key} aria-labelledby={`topic-${section.key}`} data-testid={`topic-section-${section.key}`}>
            <h2 id={`topic-${section.key}`} className="text-heading text-ink mb-3">{section.title}</h2>
            <ul className="space-y-3">
              {section.links.map((link) => (
                <li key={link.href}>
                  <TopicLinkRow href={link.href} emoji={link.emoji} title={link.title} sub={link.sub} />
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </div>
  );
}
