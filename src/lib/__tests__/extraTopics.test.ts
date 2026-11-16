import { describe, it, expect, vi } from 'vitest';

// mockTest and the brain engine read the database in their loaders; the rules under test do not.
vi.mock('../db', () => import('../__mocks__/db'));

import { TOPIC_TREE, getTopicsForGrade, isExtraTopicId, extraTopicKeys } from '../../data/topicTree';
import { TEST_CONFIG, buildGradeBlueprint, isExtraPracticeQuestion } from '../mockTest';
import { examTopicEntries, orderPriorities } from '../brain/engine';
import { computeLadder } from '../practice/ladder';
import { matchesSubTopicKey } from '../sharedUtils';

const EXTRA_IDS = ['gr5_counting', 'gr5_measurement', 'gr5_mixed'];
const EXTRA_KEYS = ['counting', 'measurement', 'mixed'];

/** The Grade 5 topic keys that reach a sub-topic label. */
function keysReaching(label: string): string[] {
  const out: string[] = [];
  const nodes = getTopicsForGrade(5);
  for (let i = 0; i < nodes.length; i++) {
    const key = nodes[i].subTopicKey;
    if (key && matchesSubTopicKey(label, key)) out.push(key);
  }
  return out;
}

describe('Grade 5 extra-practice topics', () => {
  const grade5 = getTopicsForGrade(5);

  it('are the last three Grade 5 nodes, with the agreed ids and keys and no exam weight', () => {
    const last = grade5.slice(grade5.length - 3);
    expect(last.map((n) => n.id)).toEqual(EXTRA_IDS);
    expect(last.map((n) => n.subTopicKey)).toEqual(EXTRA_KEYS);
    for (let i = 0; i < last.length; i++) {
      expect(last[i].extra).toBe(true);
      expect(last[i].examWeight).toBe(0);
      expect(last[i].dbTopicId).toBe('grade5');
      expect(last[i].grade).toBe(5);
    }
  });

  it('leave the 21 exam topics as they were', () => {
    const exam = grade5.filter((n) => !n.extra);
    expect(exam.length).toBe(21);
    expect(exam[0].id).toBe('gr5_placevalue');
    expect(exam[20].id).toBe('gr5_area');
    for (let i = 0; i < exam.length; i++) expect(exam[i].examWeight).toBeGreaterThan(0);
  });

  it('are the only extra topics in the tree', () => {
    expect(TOPIC_TREE.filter((n) => n.extra === true).map((n) => n.id)).toEqual(EXTRA_IDS);
  });

  it('are told apart by id and by key', () => {
    expect(isExtraTopicId('gr5_mixed')).toBe(true);
    expect(isExtraTopicId('gr5_fractions')).toBe(false);
    expect(isExtraTopicId('no_such_node')).toBe(false);
    expect(extraTopicKeys(5)).toEqual(EXTRA_KEYS);
    expect(extraTopicKeys(4)).toEqual([]);
    expect(extraTopicKeys(6)).toEqual([]);
  });

  it('have labels that their own key reaches and no other', () => {
    expect(keysReaching('Grade 5 — Counting and number formation')).toEqual(['counting']);
    expect(keysReaching('Grade 5 — Counting and number formation (forming numbers)')).toEqual(['counting']);
    expect(keysReaching('Grade 5 — Measurement')).toEqual(['measurement']);
    expect(keysReaching('Grade 5 — Mixed problem solving (age problems)')).toEqual(['mixed']);
    expect(keysReaching('Grade 5 — Mixed problem solving (division word problem)')).toEqual(['mixed']);
    // Exam labels stay with their exam topic.
    expect(keysReaching('Grade 5 — Area and perimeter')).toEqual(['area']);
    expect(keysReaching('Grade 5 — Multiplication and division (finding the divisor)')).toEqual(['multiplication']);
  });

  it('end their ladder on "Exam-style", never "Real exam": they hold no real paper questions', () => {
    const pool = [
      { difficulty: 'Easy', source: 'variant_generator_phase3' },
      { difficulty: 'Medium', source: 'variant_generator_phase3' },
      { difficulty: 'Hard', source: 'pdf_extracted' },
    ];
    const plan = computeLadder({ topicLabel: 'Mixed Problem Solving', pool, attempts: [] });
    expect(plan).not.toBeNull();
    if (plan) expect(plan.info.steps[3].label).toBe('Exam-style');
  });
});

describe('tests leave extra practice out', () => {
  it('gives no slot to an extra topic in any Grade 5 paper, and still fills the paper', () => {
    const kinds: Array<'quick' | 'half' | 'full' | 'ipm'> = ['quick', 'half', 'full', 'ipm'];
    for (let k = 0; k < kinds.length; k++) {
      const cfg = TEST_CONFIG[kinds[k]];
      // The shorter papers share out what is left over at random: try a few.
      for (let run = 0; run < 5; run++) {
        const slots = buildGradeBlueprint(5, cfg);
        let total = 0;
        for (let i = 0; i < slots.length; i++) {
          total += slots[i].count;
          expect(EXTRA_KEYS.indexOf(slots[i].subTopicKey || '')).toBe(-1);
          expect(slots[i].count).toBe(slots[i].easy + slots[i].medium + slots[i].hard);
        }
        expect(total).toBe(cfg.totalQuestions);
      }
    }
  });

  it('builds the other grades from exam weights as before', () => {
    const slots = buildGradeBlueprint(6, TEST_CONFIG.ipm);
    let total = 0;
    for (let i = 0; i < slots.length; i++) total += slots[i].count;
    expect(total).toBe(40);
    expect(slots.length).toBe(getTopicsForGrade(6).length);
  });

  it('recognises an extra-practice question by its label', () => {
    expect(isExtraPracticeQuestion('Grade 5 — Mixed problem solving (average)', EXTRA_KEYS)).toBe(true);
    expect(isExtraPracticeQuestion('Grade 5 — Counting digits', EXTRA_KEYS)).toBe(true);
    expect(isExtraPracticeQuestion('Grade 5 — Measurement', EXTRA_KEYS)).toBe(true);
    expect(isExtraPracticeQuestion('Grade 5 — Fractions', EXTRA_KEYS)).toBe(false);
    expect(isExtraPracticeQuestion('Grade 5 — Money and transactions', EXTRA_KEYS)).toBe(false);
    expect(isExtraPracticeQuestion(null, EXTRA_KEYS)).toBe(false);
    // A grade with no extra topics drops nothing.
    expect(isExtraPracticeQuestion('Grade 6 — Measurement', [])).toBe(false);
  });
});

describe('the brain keeps exam topics first', () => {
  it('orders every exam topic ahead of every extra topic, each group by priority', () => {
    const ordered = orderPriorities([
      { topicId: 'gr5_mixed', priority: 0.9 },
      { topicId: 'gr5_fractions', priority: 0.2 },
      { topicId: 'gr5_counting', priority: 0.95 },
      { topicId: 'gr5_decimals', priority: 0.5 },
    ]);
    expect(ordered.map((p) => p.topicId)).toEqual(['gr5_decimals', 'gr5_fractions', 'gr5_counting', 'gr5_mixed']);
  });

  it('orders by priority alone where there are no extra topics', () => {
    const ordered = orderPriorities([
      { topicId: 'gr4_fractions', priority: 0.1 },
      { topicId: 'gr4_numbers', priority: 0.7 },
    ]);
    expect(ordered.map((p) => p.topicId)).toEqual(['gr4_numbers', 'gr4_fractions']);
  });

  it('leaves extra topics out of what exam readiness is worked out from', () => {
    const entries = [
      { topicId: 'gr5_fractions', mastery: 0.8 },
      { topicId: 'gr5_measurement', mastery: 0 },
      { topicId: 'gr5_mixed', mastery: 0 },
    ];
    expect(examTopicEntries(entries)).toEqual([{ topicId: 'gr5_fractions', mastery: 0.8 }]);
  });
});
