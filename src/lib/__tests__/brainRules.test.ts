import { describe, it, expect } from 'vitest';
import {
  NUDGE_PRIORITY,
  buildNudges,
  endOfIstDay,
  findAccuracyDropNodeIds,
  isRenderableNudge,
  pickTopNudge,
  speedScore,
  streakBeforeToday,
  type NudgeFacts,
} from '../brain/rules';
import { buildPracticeUrl, practiceUrlForNode, practiceUrlForNodeId } from '../brain/practiceUrl';
import { getTopicsForGrade } from '../../data/topicTree';
import type { Nudge, NudgeKind, TopicMasteryEntry } from '../brain/engine';

const MS_PER_DAY = 86_400_000;

// 2026-11-11 is a Wednesday and 2026-11-14 a Saturday. India is UTC+5:30.
const WED_MORNING = new Date('2026-11-11T05:00:00Z'); // 10:30 in India
const WED_EVENING = new Date('2026-11-11T13:00:00Z'); // 18:30 in India
const SAT_MORNING = new Date('2026-11-14T05:00:00Z'); // 10:30 in India

/** A topic that needs nothing: practised today, well covered. */
function entry(
  topicId: string,
  topicName: string,
  over: Partial<TopicMasteryEntry> = {},
): TopicMasteryEntry {
  return {
    topicId,
    topicName,
    emoji: '',
    mastery: 0.5,
    accuracy: 0.7,
    speed: 0.5,
    coverage: 0.6,
    recency: 1,
    attemptsCount: 12,
    status: 'developing',
    ...over,
  };
}

/** A quiet weekday morning on which no rule fires. */
function facts(over: Partial<NudgeFacts> = {}): NudgeFacts {
  return {
    now: WED_MORNING,
    masteries: [entry('gr5_fractions', 'Fractions')],
    topPriorityNodeId: 'gr5_fractions',
    streakToday: 0,
    streakBeforeToday: 0,
    accuracyDropNodeIds: [],
    daysUntilExam: null,
    daysSinceMock: 2,
    ...over,
  };
}

function nudge(kind: NudgeKind, over: Partial<Nudge> = {}): Nudge {
  return {
    id: `n_${kind}`,
    kind,
    message: 'Hello',
    sparkyEmotion: 'happy',
    actionUrl: '/test',
    actionLabel: 'Go',
    priority: 0,
    ...over,
  };
}

function kinds(list: Nudge[]): Array<NudgeKind | undefined> {
  return list.map((n) => n.kind);
}

// ── Practice links ────────────────────────────────────────────────────────────

describe('practice links', () => {
  it('a plain topic has no query string', () => {
    expect(buildPracticeUrl('ch11')).toBe('/practice/ch11');
    expect(buildPracticeUrl('grade5', '')).toBe('/practice/grade5');
    expect(buildPracticeUrl('grade5', null)).toBe('/practice/grade5');
  });

  it('a sub-topic is carried in ?subTopic=', () => {
    expect(buildPracticeUrl('grade5', 'fraction')).toBe('/practice/grade5?subTopic=fraction');
    expect(buildPracticeUrl('grade5', 'place value')).toBe('/practice/grade5?subTopic=place%20value');
  });

  it('a Grade 5 node opens its own sub-topic, a Grade 4 node its own chapter', () => {
    expect(practiceUrlForNodeId('gr5_fractions')).toBe('/practice/grade5?subTopic=fraction');
    expect(practiceUrlForNodeId('gr4_decimals')).toBe('/practice/ch11');
  });

  it('an unknown node id gives null', () => {
    expect(practiceUrlForNodeId('nope')).toBeNull();
    expect(practiceUrlForNodeId(null)).toBeNull();
  });

  it('no two Grade 5 topics share a link, and none is the whole grade', () => {
    const nodes = getTopicsForGrade(5);
    const urls = nodes.map((n) => practiceUrlForNode(n));
    const unique = urls.filter((u, i) => urls.indexOf(u) === i);
    expect(nodes.length).toBeGreaterThan(1);
    expect(unique.length).toBe(nodes.length);
    expect(urls).not.toContain('/practice/grade5');
  });
});

// ── Speed ─────────────────────────────────────────────────────────────────────

describe('speedScore', () => {
  it('is the neutral 0.5 when no time was ever recorded', () => {
    expect(speedScore([])).toBe(0.5);
    expect(speedScore([0, 0, 0])).toBe(0.5);
  });

  it('leaves out old rows that hold 0 (not recorded, not instant)', () => {
    expect(speedScore([0, 30_000, 0])).toBeCloseTo(2 / 3, 5);
  });

  it('uses the real time: quicker is higher, 90 seconds or more is 0', () => {
    expect(speedScore([9_000])).toBeCloseTo(0.9, 5);
    expect(speedScore([200_000])).toBe(0);
    expect(speedScore([9_000])).toBeGreaterThan(speedScore([60_000]));
  });
});

// ── Streak ────────────────────────────────────────────────────────────────────

describe('streakBeforeToday', () => {
  const now = new Date(2026, 10, 11, 12); // local noon, 11 November
  const on = (day: number) => ({ createdAt: new Date(2026, 10, day, 12) });

  it('counts the days in a row ending yesterday', () => {
    expect(streakBeforeToday([on(10), on(9), on(8)], now)).toBe(3);
  });

  it('does not count today', () => {
    expect(streakBeforeToday([on(11), on(10), on(9), on(8)], now)).toBe(3);
  });

  it('stops at a gap', () => {
    expect(streakBeforeToday([on(10), on(8)], now)).toBe(1);
  });

  it('is 0 when yesterday was missed', () => {
    expect(streakBeforeToday([on(9), on(8)], now)).toBe(0);
    expect(streakBeforeToday([], now)).toBe(0);
  });
});

// ── Accuracy drop, per node ───────────────────────────────────────────────────

describe('findAccuracyDropNodeIds', () => {
  const nodes = [
    { id: 'gr5_fractions', dbTopicId: 'grade5', subTopicKey: 'fraction' },
    { id: 'gr5_decimals', dbTopicId: 'grade5', subTopicKey: 'decimal' },
  ];
  const answer = (subTopic: string, daysAgo: number, isCorrect: boolean) => ({
    isCorrect,
    createdAt: new Date(WED_MORNING.getTime() - daysAgo * MS_PER_DAY),
    question: { topicId: 'grade5', subTopic },
  });
  const run = (subTopic: string, daysAgo: number, right: number, total: number) =>
    Array.from({ length: total }, (_, i) => answer(subTopic, daysAgo, i < right));

  it('names only the sub-topic that dropped, not the whole grade', () => {
    const attempts = [
      ...run('Fractions', 10, 5, 5),
      ...run('Fractions', 2, 2, 5),
      ...run('Decimals', 10, 5, 5),
      ...run('Decimals', 2, 5, 5),
    ];
    expect(findAccuracyDropNodeIds(nodes, attempts, WED_MORNING)).toEqual(['gr5_fractions']);
  });

  it('needs five answers in each week', () => {
    const attempts = [...run('Fractions', 10, 4, 4), ...run('Fractions', 2, 0, 5)];
    expect(findAccuracyDropNodeIds(nodes, attempts, WED_MORNING)).toEqual([]);
  });

  it('ignores a small dip and anything older than two weeks', () => {
    const attempts = [
      ...run('Fractions', 20, 5, 5),
      ...run('Fractions', 10, 4, 5),
      ...run('Fractions', 2, 4, 5),
    ];
    expect(findAccuracyDropNodeIds(nodes, attempts, WED_MORNING)).toEqual([]);
  });
});

// ── The rules ─────────────────────────────────────────────────────────────────

describe('buildNudges', () => {
  it('says nothing on a quiet day', () => {
    expect(buildNudges(facts())).toEqual([]);
  });

  it('accuracy drop: links to that sub-topic', () => {
    const out = buildNudges(facts({ accuracyDropNodeIds: ['gr5_fractions'] }));
    expect(kinds(out)).toEqual(['accuracy_drop']);
    expect(out[0].actionUrl).toBe('/practice/grade5?subTopic=fraction');
    expect(out[0].message).toContain('Fractions');
  });

  it('keep it going: evening only, a run of two or more days, nothing yet today', () => {
    const evening = facts({ now: WED_EVENING, streakBeforeToday: 4 });
    const out = buildNudges(evening);
    expect(kinds(out)).toEqual(['streak_keep']);
    expect(out[0].message).toContain('4 days in a row');
    expect(out[0].actionUrl).toBe('/practice/grade5?subTopic=fraction');

    expect(buildNudges(facts({ now: WED_MORNING, streakBeforeToday: 4 }))).toEqual([]);
    expect(buildNudges(facts({ now: WED_EVENING, streakBeforeToday: 1 }))).toEqual([]);
    expect(buildNudges(facts({ now: WED_EVENING, streakBeforeToday: 4, streakToday: 5 }))).toEqual([]);
  });

  it('milestone: cheers on the day it is reached', () => {
    const out = buildNudges(facts({ streakToday: 7, streakBeforeToday: 6 }));
    expect(kinds(out)).toEqual(['streak_milestone']);
    expect(out[0].actionUrl).toBe('/progress');
    expect(buildNudges(facts({ streakToday: 8, streakBeforeToday: 7 }))).toEqual([]);
  });

  it('exam: suggests a practice test, unless one was taken this week', () => {
    const out = buildNudges(facts({ daysUntilExam: 20, daysSinceMock: null }));
    expect(kinds(out)).toEqual(['exam_mock']);
    expect(out[0].actionUrl).toBe('/test');
    expect(out[0].message).toContain('20 days');

    expect(buildNudges(facts({ daysUntilExam: 20, daysSinceMock: 2 }))).toEqual([]);
    expect(buildNudges(facts({ daysUntilExam: 45, daysSinceMock: null }))).toEqual([]);
    expect(buildNudges(facts({ daysUntilExam: 1, daysSinceMock: null }))).toEqual([]);
  });

  it('weekend: one test reminder at most, and never for a child who has not started', () => {
    const weekend = buildNudges(facts({ now: SAT_MORNING, daysSinceMock: 10 }));
    expect(kinds(weekend)).toEqual(['weekend_mock']);
    expect(weekend[0].actionUrl).toBe('/test');

    expect(buildNudges(facts({ now: SAT_MORNING, daysSinceMock: 3 }))).toEqual([]);
    expect(buildNudges(facts({ now: WED_MORNING, daysSinceMock: 10 }))).toEqual([]);

    const withExam = buildNudges(facts({ now: SAT_MORNING, daysSinceMock: 10, daysUntilExam: 20 }));
    expect(kinds(withExam)).toEqual(['exam_mock']);

    const brandNew = facts({
      now: SAT_MORNING,
      daysSinceMock: null,
      masteries: [entry('gr5_fractions', 'Fractions', { attemptsCount: 0, coverage: 0, recency: 0 })],
    });
    expect(buildNudges(brandNew)).toEqual([]);
  });

  it('idle and explore: each links to its own sub-topic, one nudge per topic', () => {
    const idle = buildNudges(facts({ masteries: [entry('gr5_decimals', 'Decimal Fractions', { recency: 0.4 })] }));
    expect(kinds(idle)).toEqual(['idle_topic']);
    expect(idle[0].actionUrl).toBe('/practice/grade5?subTopic=decimal');

    const explore = buildNudges(facts({ masteries: [entry('gr5_area', 'Area & Perimeter', { coverage: 0.1 })] }));
    expect(kinds(explore)).toEqual(['explore_topic']);
    expect(explore[0].actionUrl).toBe('/practice/grade5?subTopic=area');

    const both = buildNudges(facts({ masteries: [entry('gr5_area', 'Area & Perimeter', { coverage: 0.1, recency: 0.4 })] }));
    expect(kinds(both)).toEqual(['idle_topic']);
  });

  it('keeps at most three, highest priority first', () => {
    const out = buildNudges(facts({
      now: SAT_MORNING,
      streakToday: 7,
      streakBeforeToday: 6,
      accuracyDropNodeIds: ['gr5_fractions'],
      daysUntilExam: 20,
      daysSinceMock: null,
      masteries: [
        entry('gr5_fractions', 'Fractions'),
        entry('gr5_decimals', 'Decimal Fractions', { recency: 0.4 }),
      ],
    }));
    expect(kinds(out)).toEqual(['streak_milestone', 'accuracy_drop', 'exam_mock']);
  });

  it('every kind is warm, pressure-free and goes somewhere specific', () => {
    const all: Nudge[] = [
      ...buildNudges(facts({
        now: WED_EVENING,
        streakBeforeToday: 3,
        accuracyDropNodeIds: ['gr5_fractions'],
        daysUntilExam: 20,
        daysSinceMock: null,
      })),
      ...buildNudges(facts({
        now: WED_MORNING,
        streakToday: 14,
        streakBeforeToday: 13,
        masteries: [
          entry('gr5_decimals', 'Decimal Fractions', { recency: 0.4 }),
          entry('gr5_area', 'Area & Perimeter', { coverage: 0.1 }),
        ],
      })),
      ...buildNudges(facts({ now: SAT_MORNING, daysSinceMock: 10 })),
    ];

    const seen = kinds(all).filter((k, i, list) => list.indexOf(k) === i);
    expect(seen.length).toBe(Object.keys(NUDGE_PRIORITY).length);

    for (let i = 0; i < all.length; i++) {
      const n = all[i];
      expect(isRenderableNudge(n)).toBe(true);
      expect(n.message).not.toMatch(/wrong|incorrect|failed|error/i);
      expect(n.message).not.toMatch(/don't break|at risk|you haven't|needs attention|dropped/i);
      expect(n.message.length).toBeLessThanOrEqual(90);
      expect(n.actionUrl.charAt(0)).toBe('/');
      expect(n.actionUrl).not.toBe('/practice/grade5');
      expect(n.actionLabel.length).toBeGreaterThan(0);
      expect(typeof n.expiresAt).toBe('string');
    }
  });

  it('time-bound nudges run out at the end of the day in India', () => {
    expect(endOfIstDay(new Date('2026-11-14T13:00:00Z')).toISOString()).toBe('2026-11-14T18:30:00.000Z');
    expect(endOfIstDay(new Date('2026-11-14T19:00:00Z')).toISOString()).toBe('2026-11-15T18:30:00.000Z');
    const out = buildNudges(facts({ now: SAT_MORNING, daysSinceMock: 10 }));
    expect(out[0].expiresAt).toBe('2026-11-14T18:30:00.000Z');
  });
});

// ── Which one is shown ────────────────────────────────────────────────────────

describe('pickTopNudge', () => {
  const ORDER: NudgeKind[] = [
    'streak_milestone',
    'streak_keep',
    'accuracy_drop',
    'exam_mock',
    'idle_topic',
    'explore_topic',
    'weekend_mock',
  ];

  it('shows one nudge at a time, in the fixed priority order', () => {
    // Deliberately jumbled, with stored priorities that point the other way.
    const list: Nudge[] = [
      nudge('idle_topic', { priority: 99 }),
      nudge('weekend_mock', { priority: 98 }),
      nudge('streak_keep'),
      nudge('explore_topic'),
      nudge('streak_milestone'),
      nudge('exam_mock'),
      nudge('accuracy_drop'),
    ];
    const dismissedIds: string[] = [];
    const shown: Array<NudgeKind | undefined> = [];
    for (let i = 0; i < ORDER.length; i++) {
      const top = pickTopNudge(list, { dismissedIds });
      expect(top).not.toBeNull();
      if (!top) break;
      shown.push(top.kind);
      dismissedIds.push(top.id);
    }
    expect(shown).toEqual(ORDER);
    expect(pickTopNudge(list, { dismissedIds })).toBeNull();
  });

  it('the priority table covers every kind, with no ties', () => {
    const ranks = ORDER.map((k) => NUDGE_PRIORITY[k]);
    expect(Object.keys(NUDGE_PRIORITY).length).toBe(ORDER.length);
    for (let i = 1; i < ranks.length; i++) {
      expect(ranks[i - 1]).toBeGreaterThan(ranks[i]);
    }
  });

  it('nothing to show: an empty list, or something that is not a list', () => {
    expect(pickTopNudge([])).toBeNull();
    expect(pickTopNudge(null)).toBeNull();
    expect(pickTopNudge({})).toBeNull();
  });

  it('never shows a row stored before nudges had a kind', () => {
    const legacy = {
      id: 'nudge_streak',
      message: 'An old message',
      sparkyEmotion: 'encouraging',
      actionUrl: '/practice/grade5',
      actionLabel: 'Practice now',
      priority: 10,
    };
    expect(isRenderableNudge(legacy)).toBe(false);
    expect(pickTopNudge([legacy])).toBeNull();
    expect(pickTopNudge([legacy, nudge('weekend_mock')])?.kind).toBe('weekend_mock');
  });

  it('never shows a link that leaves the app', () => {
    expect(pickTopNudge([nudge('idle_topic', { actionUrl: 'https://example.com' })])).toBeNull();
  });

  it('skips a nudge that is out of date', () => {
    const list = [
      nudge('streak_milestone', { expiresAt: '2026-11-11T18:30:00.000Z' }),
      nudge('idle_topic', { expiresAt: '2026-11-14T05:00:00.000Z' }),
    ];
    expect(pickTopNudge(list, { now: WED_MORNING })?.kind).toBe('streak_milestone');
    expect(pickTopNudge(list, { now: new Date('2026-11-12T05:00:00Z') })?.kind).toBe('idle_topic');
    expect(pickTopNudge(list, { now: new Date('2026-11-15T05:00:00Z') })).toBeNull();
  });

  it('drops the "keep it going" invitation once the child has practised today', () => {
    const list = [nudge('streak_keep'), nudge('explore_topic')];
    expect(pickTopNudge(list)?.kind).toBe('streak_keep');
    expect(pickTopNudge(list, { practisedToday: true })?.kind).toBe('explore_topic');
  });
});
