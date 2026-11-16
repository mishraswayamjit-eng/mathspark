import { describe, it, expect, vi } from 'vitest';

// The loader half of the module talks to the database; the rules under test do not.
vi.mock('../db', () => import('../__mocks__/db'));

import {
  rankNextActions,
  actionKey,
  dayKey,
  type NodeSignal,
  type RankInput,
  type NextAction,
} from '../brain/nextAction';
import { TOPIC_CONTENT_MAP } from '@/data/topicContentMap';

const TODAY = '2026-11-15';

function node(nodeId: string, name: string, subTopicKey: string, over?: Partial<NodeSignal>): NodeSignal {
  const base: NodeSignal = {
    nodeId,
    name,
    dbTopicId: 'grade5',
    subTopicKey,
    examWeight: 0.05,
    attempts: 0,
    accuracy: 0,
    mastery: 0,
    priority: 0,
    daysSinceLastAttempt: null,
    misses7d: 0,
    recentAttempts: 0,
    recentCorrect: 0,
    priorAttempts: 0,
    priorCorrect: 0,
  };
  return { ...base, ...(over || {}) };
}

function input(nodes: NodeSignal[], over?: Partial<RankInput>): RankInput {
  const base: RankInput = {
    today: TODAY,
    nodes,
    totalAttempts: 20,
    lessonBest: {},
    contentDone: {},
    flashcardsDue: 0,
    daysSinceLastMock: 1,
    daysUntilExam: null,
    mockInProgress: false,
    history: [],
  };
  return { ...base, ...(over || {}) };
}

function byRule(actions: NextAction[], ruleId: string): NextAction | undefined {
  for (let i = 0; i < actions.length; i++) if (actions[i].ruleId === ruleId) return actions[i];
  return undefined;
}

const decimals = (over?: Partial<NodeSignal>) => node('gr5_decimals', 'Decimal Fractions', 'decimal', over);
const fractions = (over?: Partial<NodeSignal>) => node('gr5_fractions', 'Fractions', 'fraction', over);
const integers = (over?: Partial<NodeSignal>) => node('gr5_integers', 'Integers', 'integer', over);
const area = (over?: Partial<NodeSignal>) => node('gr5_area', 'Area & Perimeter', 'area', over);
const placeValue = (over?: Partial<NodeSignal>) => node('gr5_placevalue', 'Numbers & Place Value', 'place value', over);
const percentage = (over?: Partial<NodeSignal>) => node('gr5_percentage', 'Percentage & Money', 'money', over);
const addSubtract = (over?: Partial<NodeSignal>) => node('gr5_operations1', 'Addition & Subtraction', 'addition', over);

/** The same checks POST /api/recommendations makes on a refId. */
const DRILL_REF = /^[a-z_]{1,60}:L[1-5]$/;
const STRATEGY_REF = /^STR_\d{1,4}$/;

describe('rankNextActions', () => {
  describe('a brand-new child', () => {
    it('gets one starting action on the first sub-topic', () => {
      const out = rankNextActions(input([placeValue(), fractions()], { totalAttempts: 0 }));
      expect(out).toHaveLength(1);
      expect(out[0].ruleId).toBe('new_start');
      expect(out[0].actionType).toBe('practice');
      expect(out[0].nodeId).toBe('gr5_placevalue');
      expect(out[0].href).toBe('/practice/grade5?subTopic=place+value');
    });

    it('is pointed at the chapter list when the grade has no topic tree', () => {
      const out = rankNextActions(input([], { totalAttempts: 0 }));
      expect(out).toHaveLength(1);
      expect(out[0].href).toBe('/chapters');
    });
  });

  it('recommends nothing while a mock test is in progress', () => {
    const out = rankNextActions(input([decimals({ misses7d: 5 })], { mockInProgress: true, flashcardsDue: 30 }));
    expect(out).toEqual([]);
  });

  describe('rule 1: a lesson after repeated misses', () => {
    it('offers the concept lesson after three misses in a week', () => {
      const out = rankNextActions(input([decimals({ misses7d: 3, attempts: 6, accuracy: 0.5 })]));
      expect(out[0].ruleId).toBe('lesson_after_misses');
      expect(out[0].actionType).toBe('lesson');
      expect(out[0].href).toBe('/learn/lessons/decimals');
      expect(out[0].refId).toBe('decimals');
      expect(out[0].nodeId).toBe('gr5_decimals');
    });

    it('does not fire on two misses', () => {
      const out = rankNextActions(input([decimals({ misses7d: 2, attempts: 6, accuracy: 0.5 })]));
      expect(byRule(out, 'lesson_after_misses')).toBeUndefined();
    });

    it('skips a lesson already passed with 70 or more, and offers it again below 70', () => {
      const passed = rankNextActions(input([decimals({ misses7d: 4 })], { lessonBest: { decimals: 70 } }));
      expect(byRule(passed, 'lesson_after_misses')).toBeUndefined();

      const notYet = rankNextActions(input([decimals({ misses7d: 4 })], { lessonBest: { decimals: 60 } }));
      expect(byRule(notYet, 'lesson_after_misses')).toBeDefined();
    });

    it('prefers a hands-on lesson where one is mapped, then falls back to the concept lesson', () => {
      const ids = TOPIC_CONTENT_MAP.gr5_fractions.handsOnLessonIds || [];
      expect(ids.length).toBeGreaterThan(0);

      const first = rankNextActions(input([fractions({ misses7d: 3 })]));
      expect(first[0].actionType).toBe('hands_on');
      expect(first[0].href).toBe(`/learn/hands-on/${ids[0]}`);

      const done: Record<string, number> = {};
      for (let i = 0; i < ids.length; i++) done[`hands_on:${ids[i]}`] = 1;
      const after = rankNextActions(input([fractions({ misses7d: 3 })], { contentDone: done }));
      expect(after[0].actionType).toBe('lesson');
      expect(after[0].href).toBe('/learn/lessons/fractions');
    });
  });

  describe('rule 2: a recent miss with an "Explain it to me" lesson', () => {
    it('sends the child to practice on that sub-topic, carrying the question', () => {
      const out = rankNextActions(input([integers({ misses7d: 1, explainQuestionId: 'Q_TEST_1' })]));
      expect(out[0].ruleId).toBe('explain_missed');
      expect(out[0].actionType).toBe('explain');
      expect(out[0].refId).toBe('Q_TEST_1');
      expect(out[0].href).toBe('/practice/grade5?subTopic=integer&teach=Q_TEST_1');
    });

    it('comes after a lesson, and on a different sub-topic gives way to it (one learn action)', () => {
      const out = rankNextActions(input([
        decimals({ misses7d: 3 }),
        integers({ misses7d: 1, explainQuestionId: 'Q_TEST_1' }),
      ]));
      expect(out[0].ruleId).toBe('lesson_after_misses');
      expect(byRule(out, 'explain_missed')).toBeUndefined();
    });
  });

  describe('rule 3: review', () => {
    it('offers a review of a strong sub-topic left alone for 14 days', () => {
      const out = rankNextActions(input([area({ attempts: 12, accuracy: 0.9, mastery: 0.7, daysSinceLastAttempt: 14 })]));
      expect(out[0].ruleId).toBe('review_idle');
      expect(out[0].actionType).toBe('review');
      expect(out[0].href).toBe('/practice/grade5?subTopic=area');
    });

    it('leaves a strong sub-topic alone when it was practised lately, and a weak one when idle', () => {
      const fresh = rankNextActions(input([area({ attempts: 12, accuracy: 0.9, mastery: 0.7, daysSinceLastAttempt: 13 })]));
      expect(byRule(fresh, 'review_idle')).toBeUndefined();
      const weak = rankNextActions(input([area({ attempts: 4, accuracy: 0.4, mastery: 0.3, daysSinceLastAttempt: 20 })]));
      expect(byRule(weak, 'review_idle')).toBeUndefined();
    });

    it('offers a review when accuracy has dropped this week', () => {
      const out = rankNextActions(input([integers({
        attempts: 15, accuracy: 0.7, mastery: 0.5, daysSinceLastAttempt: 1,
        priorAttempts: 10, priorCorrect: 9, recentAttempts: 5, recentCorrect: 3, misses7d: 2,
      })]));
      expect(out[0].ruleId).toBe('review_dropped');
    });
  });

  describe('rule 4: flashcards', () => {
    it('fires at ten due cards and not at nine', () => {
      expect(byRule(rankNextActions(input([decimals()], { flashcardsDue: 10 })), 'flashcards_due')).toBeDefined();
      expect(byRule(rankNextActions(input([decimals()], { flashcardsDue: 9 })), 'flashcards_due')).toBeUndefined();
    });
  });

  describe('rule 5: skill drill', () => {
    it('offers the mapped drill at 60–80% over eight or more attempts', () => {
      const out = rankNextActions(input([area({ attempts: 8, accuracy: 0.7, daysSinceLastAttempt: 1 })]));
      expect(out[0].ruleId).toBe('drill_close');
      expect(out[0].href).toBe('/practice/skill-drill/area_perimeter_mensuration/L1');
      expect(out[0].refId).toBe('area_perimeter_mensuration:L1');
    });

    it('needs eight attempts, the 60–80% band, and a mapped drill', () => {
      expect(byRule(rankNextActions(input([area({ attempts: 7, accuracy: 0.7 })])), 'drill_close')).toBeUndefined();
      expect(byRule(rankNextActions(input([area({ attempts: 9, accuracy: 0.85 })])), 'drill_close')).toBeUndefined();
      expect(byRule(rankNextActions(input([area({ attempts: 9, accuracy: 0.5 })])), 'drill_close')).toBeUndefined();
      // Integers has no skill drill.
      expect(byRule(rankNextActions(input([integers({ attempts: 9, accuracy: 0.7 })])), 'drill_close')).toBeUndefined();
    });

    it('links Fractions and Decimals to their lowest Grade 5 level, which is not L1', () => {
      const f = rankNextActions(input([fractions({ attempts: 9, accuracy: 0.7 })]));
      expect(f[0].ruleId).toBe('drill_close');
      expect(f[0].href).toBe('/practice/skill-drill/fractions_decimals/L2');
      expect(f[0].refId).toBe('fractions_decimals:L2');
      expect(f[0].nodeId).toBe('gr5_fractions');

      const d = rankNextActions(input([decimals({ attempts: 9, accuracy: 0.7 })]));
      expect(d[0].ruleId).toBe('drill_close');
      expect(d[0].href).toBe('/practice/skill-drill/fractions_decimals/L2');
      expect(d[0].nodeId).toBe('gr5_decimals');
    });

    it('maps a level to every sub-topic with a drill, as a refId the event route accepts', () => {
      const ids = Object.keys(TOPIC_CONTENT_MAP);
      let withDrill = 0;
      for (let i = 0; i < ids.length; i++) {
        const c = TOPIC_CONTENT_MAP[ids[i]];
        if (!c.drillTopicId) continue;
        withDrill += 1;
        expect(c.drillLevelId).toBeDefined();
        expect(`${c.drillTopicId}:${c.drillLevelId}`).toMatch(DRILL_REF);
      }
      expect(withDrill).toBe(19);
    });

    it('offers a drill shared by two sub-topics only once', () => {
      const out = rankNextActions(input([
        decimals({ attempts: 9, accuracy: 0.7, examWeight: 0.11 }),
        fractions({ attempts: 9, accuracy: 0.7, examWeight: 0.14 }),
      ]));
      const drills = out.filter((a) => a.ruleId === 'drill_close');
      expect(drills).toHaveLength(1);
      // Same accuracy, so the heavier exam weight wins it.
      expect(drills[0].nodeId).toBe('gr5_fractions');
      expect(out).toHaveLength(2);
      expect(out[1].ruleId).toBe('continue_top');
      expect(out[1].nodeId).toBe('gr5_decimals');
    });

    it('rests a drill finished in the last week, and offers it again after that', () => {
      const out = rankNextActions(input([area({ attempts: 9, accuracy: 0.7 })], {
        contentDone: { 'drill:area_perimeter_mensuration:L1': 2 },
      }));
      expect(byRule(out, 'drill_close')).toBeUndefined();

      const later = rankNextActions(input([area({ attempts: 9, accuracy: 0.7 })], {
        contentDone: { 'drill:area_perimeter_mensuration:L1': 7 },
      }));
      expect(byRule(later, 'drill_close')).toBeDefined();
    });
  });

  describe('rule 6: a trick when the misses go on', () => {
    it('offers a mapped strategy after three misses once the lesson is passed', () => {
      const out = rankNextActions(input([percentage({ misses7d: 3 })], { lessonBest: { percentage: 70 } }));
      expect(out[0].ruleId).toBe('strategy_after_misses');
      expect(out[0].actionType).toBe('strategy');
      expect(out[0].refId).toBe('STR_009');
      expect(out[0].nodeId).toBe('gr5_percentage');
      expect(out[0].href).toBe('/learn/strategies?open=STR_009');
    });

    it('does not fire on two misses', () => {
      const out = rankNextActions(input([percentage({ misses7d: 2 })], { lessonBest: { percentage: 70 } }));
      expect(byRule(out, 'strategy_after_misses')).toBeUndefined();
    });

    it('gives way to the lesson while the lesson is still to do', () => {
      const out = rankNextActions(input([percentage({ misses7d: 4 })]));
      expect(out[0].ruleId).toBe('lesson_after_misses');
      expect(byRule(out, 'strategy_after_misses')).toBeUndefined();
    });

    it('fires for another sub-topic once its lesson is done', () => {
      expect(TOPIC_CONTENT_MAP.gr5_operations1.lessonSlug).toBe('addition-subtraction');
      const out = rankNextActions(input([addSubtract({ misses7d: 3 })], { lessonBest: { 'addition-subtraction': 90 } }));
      expect(out[0].ruleId).toBe('strategy_after_misses');
      expect(out[0].refId).toBe('STR_017');
    });

    it('moves on to the next strategy not yet opened, and stops when all are opened', () => {
      const second = rankNextActions(input([percentage({ misses7d: 3 })], {
        lessonBest: { percentage: 90 },
        contentDone: { 'strategy:STR_009': 40 },
      }));
      const hit = byRule(second, 'strategy_after_misses');
      expect(hit).toBeDefined();
      expect(hit!.refId).toBe('STR_031');
      expect(hit!.href).toBe('/learn/strategies?open=STR_031');

      const none = rankNextActions(input([percentage({ misses7d: 3 })], {
        lessonBest: { percentage: 90 },
        contentDone: { 'strategy:STR_009': 40, 'strategy:STR_031': 0 },
      }));
      expect(byRule(none, 'strategy_after_misses')).toBeUndefined();
      // The floor still gives the child something to do.
      expect(none.length).toBeGreaterThan(0);
    });

    it('stays quiet for a sub-topic with no strategy mapped', () => {
      expect(TOPIC_CONTENT_MAP.gr5_decimals.strategyIds).toBeUndefined();
      const out = rankNextActions(input([decimals({ misses7d: 5 })], { lessonBest: { decimals: 90 } }));
      expect(byRule(out, 'strategy_after_misses')).toBeUndefined();
    });

    it('is a learn action, so a lesson on another sub-topic takes its place', () => {
      const out = rankNextActions(input(
        [decimals({ misses7d: 3 }), percentage({ misses7d: 5 })],
        { lessonBest: { percentage: 90 } },
      ));
      expect(out[0].ruleId).toBe('lesson_after_misses');
      expect(out[0].nodeId).toBe('gr5_decimals');
      expect(byRule(out, 'strategy_after_misses')).toBeUndefined();
    });

    it('is dropped when shown on two earlier days and never taken', () => {
      const id = actionKey('strategy_after_misses', 'gr5_percentage', 'STR_009');
      const out = rankNextActions(input([percentage({ misses7d: 3 })], {
        lessonBest: { percentage: 90 },
        history: [
          { actionId: id, day: '2026-11-13', taken: false },
          { actionId: id, day: '2026-11-14', taken: false },
        ],
      }));
      expect(byRule(out, 'strategy_after_misses')).toBeUndefined();
      expect(out).toHaveLength(1);
      expect(out[0].ruleId).toBe('continue_top');
    });

    it('maps only strategy ids the event route accepts', () => {
      const ids = Object.keys(TOPIC_CONTENT_MAP);
      let mapped = 0;
      for (let i = 0; i < ids.length; i++) {
        const list = TOPIC_CONTENT_MAP[ids[i]].strategyIds || [];
        if (list.length > 0) mapped += 1;
        for (let k = 0; k < list.length; k++) expect(list[k]).toMatch(STRATEGY_REF);
      }
      expect(mapped).toBe(8);
    });
  });

  describe('rule 7: mock test', () => {
    const covered = [decimals({ attempts: 6, accuracy: 0.9 }), integers({ attempts: 5, accuracy: 0.9 }), area({ attempts: 1 })];

    it('fires with good coverage and no mock for a week', () => {
      expect(byRule(rankNextActions(input(covered, { daysSinceLastMock: null })), 'mock_coverage')).toBeDefined();
      expect(byRule(rankNextActions(input(covered, { daysSinceLastMock: 7 })), 'mock_coverage')).toBeDefined();
      expect(byRule(rankNextActions(input(covered, { daysSinceLastMock: 6 })), 'mock_coverage')).toBeUndefined();
    });

    it('does not fire on thin coverage', () => {
      const thin = [decimals({ attempts: 6 }), integers({ attempts: 1 }), area({ attempts: 1 })];
      expect(byRule(rankNextActions(input(thin, { daysSinceLastMock: null })), 'mock_coverage')).toBeUndefined();
    });

    it('fires when the exam is within 30 days, whatever the coverage', () => {
      const thin = [decimals({ attempts: 1 })];
      const soon = rankNextActions(input(thin, { daysUntilExam: 30, daysSinceLastMock: null }));
      expect(byRule(soon, 'mock_exam_soon')).toBeDefined();
      const far = rankNextActions(input(thin, { daysUntilExam: 31, daysSinceLastMock: null }));
      expect(byRule(far, 'mock_exam_soon')).toBeUndefined();
    });
  });

  describe('rule 8: otherwise', () => {
    it('continues the top-priority sub-topic', () => {
      const out = rankNextActions(input([
        decimals({ attempts: 2, priority: 0.4 }),
        integers({ attempts: 2, priority: 0.9 }),
        area({ attempts: 2, priority: 0.6 }),
      ]));
      expect(out).toHaveLength(1);
      expect(out[0].ruleId).toBe('continue_top');
      expect(out[0].nodeId).toBe('gr5_integers');
      expect(out[0].href).toBe('/practice/grade5?subTopic=integer');
    });
  });

  describe('ordering and limits', () => {
    it('keeps the rule order and stops at the limit', () => {
      const out = rankNextActions(input(
        [
          decimals({ misses7d: 3, attempts: 6, accuracy: 0.5 }),
          area({ attempts: 12, accuracy: 0.9, mastery: 0.7, daysSinceLastAttempt: 20 }),
          integers({ attempts: 6, accuracy: 0.9 }),
        ],
        { flashcardsDue: 15, daysSinceLastMock: null },
      ));
      expect(out.map((a) => a.ruleId)).toEqual(['lesson_after_misses', 'review_idle', 'flashcards_due']);
    });

    it('gives at most one learn action and one action per sub-topic', () => {
      const out = rankNextActions(input([
        decimals({ misses7d: 5, attempts: 10, accuracy: 0.7 }),
        integers({ misses7d: 3, attempts: 10, accuracy: 0.7 }),
        area({ misses7d: 4, attempts: 10, accuracy: 0.7 }),
      ]));
      const learn = out.filter((a) => a.actionType === 'lesson' || a.actionType === 'hands_on' || a.actionType === 'explain' || a.actionType === 'strategy');
      expect(learn).toHaveLength(1);
      // The most misses wins the lesson.
      expect(learn[0].nodeId).toBe('gr5_decimals');
      const seen: Record<string, number> = {};
      out.forEach((a) => { if (a.nodeId) seen[a.nodeId] = (seen[a.nodeId] || 0) + 1; });
      Object.keys(seen).forEach((k) => expect(seen[k]).toBe(1));
    });

    it('breaks a tie on exam weight, then node id, the same way every time', () => {
      const nodes = [
        integers({ misses7d: 3, examWeight: 0.03 }),
        decimals({ misses7d: 3, examWeight: 0.11 }),
      ];
      const a = rankNextActions(input(nodes));
      const b = rankNextActions(input(nodes.slice().reverse()));
      expect(a[0].nodeId).toBe('gr5_decimals');
      expect(b.map((x) => x.id)).toEqual(a.map((x) => x.id));
    });
  });

  describe('suppression', () => {
    const lessonId = actionKey('lesson_after_misses', 'gr5_decimals', 'decimals');
    const nodes = () => [decimals({ misses7d: 3, attempts: 6, accuracy: 0.5 }), integers({ attempts: 2 })];

    it('drops an action shown on two earlier days and never taken', () => {
      const out = rankNextActions(input(nodes(), {
        history: [
          { actionId: lessonId, day: '2026-11-13', taken: false },
          { actionId: lessonId, day: '2026-11-14', taken: false },
        ],
      }));
      expect(byRule(out, 'lesson_after_misses')).toBeUndefined();
      // The floor still gives the child something to do.
      expect(out.length).toBeGreaterThan(0);
    });

    it('keeps it when it was taken, shown on one earlier day only, or shown only today', () => {
      const taken = rankNextActions(input(nodes(), {
        history: [
          { actionId: lessonId, day: '2026-11-13', taken: true },
          { actionId: lessonId, day: '2026-11-14', taken: false },
        ],
      }));
      expect(byRule(taken, 'lesson_after_misses')).toBeDefined();

      const once = rankNextActions(input(nodes(), {
        history: [
          { actionId: lessonId, day: '2026-11-14', taken: false },
          { actionId: lessonId, day: '2026-11-14', taken: false },
          { actionId: lessonId, day: TODAY, taken: false },
        ],
      }));
      expect(byRule(once, 'lesson_after_misses')).toBeDefined();
    });

    it('ignores showings older than three days', () => {
      const out = rankNextActions(input(nodes(), {
        history: [
          { actionId: lessonId, day: '2026-11-10', taken: false },
          { actionId: lessonId, day: '2026-11-11', taken: false },
        ],
      }));
      expect(byRule(out, 'lesson_after_misses')).toBeDefined();
    });

    it('never suppresses the fallback', () => {
      const fallbackId = actionKey('continue_top', 'gr5_integers', undefined);
      const out = rankNextActions(input([integers({ attempts: 2 })], {
        history: [
          { actionId: fallbackId, day: '2026-11-13', taken: false },
          { actionId: fallbackId, day: '2026-11-14', taken: false },
        ],
      }));
      expect(out).toHaveLength(1);
      expect(out[0].ruleId).toBe('continue_top');
    });
  });

  it('speaks kindly: no harsh words, one short reason each', () => {
    const out = rankNextActions(input(
      [
        decimals({ misses7d: 4, attempts: 10, accuracy: 0.5 }),
        fractions({ misses7d: 1, explainQuestionId: 'Q_TEST_2' }),
        area({ attempts: 12, accuracy: 0.9, mastery: 0.7, daysSinceLastAttempt: 20 }),
        integers({ attempts: 15, priorAttempts: 10, priorCorrect: 9, recentAttempts: 5, recentCorrect: 2 }),
      ],
      {
        flashcardsDue: 12,
        daysSinceLastMock: null,
        daysUntilExam: 10,
        limit: 5,
      },
    ))
      .concat(rankNextActions(input([fractions({ misses7d: 3 })])))
      .concat(rankNextActions(input([integers({ misses7d: 1, explainQuestionId: 'Q_TEST_1' })])))
      .concat(rankNextActions(input([area({ attempts: 8, accuracy: 0.7 })])))
      .concat(rankNextActions(input([placeValue({ attempts: 9, accuracy: 0.7 })])))
      .concat(rankNextActions(input([percentage({ misses7d: 3 })], { lessonBest: { percentage: 80 } })))
      .concat(rankNextActions(input([addSubtract({ misses7d: 3 })])))
      .concat(rankNextActions(input([decimals({ attempts: 6 }), integers({ attempts: 6 })], { daysSinceLastMock: null })))
      .concat(rankNextActions(input([placeValue()], { totalAttempts: 0 })))
      .concat(rankNextActions(input([], { totalAttempts: 0 })));

    // Every rule is represented.
    const rules: Record<string, boolean> = {};
    out.forEach((a) => { rules[a.ruleId] = true; });
    expect(Object.keys(rules).sort()).toEqual([
      'continue_top', 'drill_close', 'explain_missed', 'flashcards_due', 'lesson_after_misses',
      'mock_coverage', 'mock_exam_soon', 'new_start', 'review_dropped', 'review_idle', 'strategy_after_misses',
    ]);

    for (let i = 0; i < out.length; i++) {
      const words = `${out[i].title} ${out[i].reason}`;
      expect(words).not.toMatch(/wrong|incorrect|fail|error|mistake|bad|poor|weak/i);
      // One sentence, not too long.
      expect(out[i].reason).toMatch(/^[^.!?]+[.!?]$/);
      expect(out[i].reason.length).toBeLessThan(170);
      expect(out[i].href.charAt(0)).toBe('/');
    }
  });

  it('dayKey gives the India day', () => {
    // 20:00 UTC on the 14th is 01:30 on the 15th in India.
    expect(dayKey(new Date('2026-11-14T20:00:00.000Z'))).toBe('2026-11-15');
    expect(dayKey(new Date('2026-11-14T18:00:00.000Z'))).toBe('2026-11-14');
  });
});
