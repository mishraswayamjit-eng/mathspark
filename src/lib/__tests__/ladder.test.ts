import { describe, it, expect } from 'vitest';
import {
  computeLadder,
  isRealExamSource,
  isStrongStart,
  ladderAfterAnswer,
  ladderTiers,
  stepOfQuestion,
  variantIdPrefixes,
  withServedQuestion,
  LADDER_NEEDED,
  LADDER_REFRESH_NEEDED,
} from '../practice/ladder';
import type { LadderAttempt, LadderQuestionMeta } from '../practice/ladder';

const GEN = 'variant_generator_phase1';
const REAL = 'g5_final_2019';

interface PoolQuestion extends LadderQuestionMeta {
  id: string;
}

function q(id: string, difficulty: string, source: string = GEN): PoolQuestion {
  return { id, difficulty, source };
}

/** Five Easy, five Medium, five Hard, and five real paper questions. */
function fullPool(): PoolQuestion[] {
  const out: PoolQuestion[] = [];
  for (let i = 1; i <= 5; i++) {
    out.push(q('e' + i, 'Easy'));
    out.push(q('m' + i, 'Medium'));
    out.push(q('h' + i, 'Hard'));
    out.push(q('x' + i, 'Medium', REAL));
  }
  return out;
}

function answer(questionId: string, difficulty: string, isCorrect: boolean, source: string = GEN): LadderAttempt {
  return { questionId, difficulty, source, isCorrect };
}

/** `n` right answers on different questions of one kind. */
function rights(prefix: string, difficulty: string, n: number, source: string = GEN): LadderAttempt[] {
  const out: LadderAttempt[] = [];
  for (let i = 1; i <= n; i++) out.push(answer(prefix + i, difficulty, true, source));
  return out;
}

function plan(attempts: LadderAttempt[], pool: LadderQuestionMeta[] = fullPool(), startHigher = false) {
  const p = computeLadder({ topicLabel: 'HCF & LCM', pool, attempts, startHigher });
  if (!p) throw new Error('expected a ladder');
  return p;
}

describe('which step a question belongs to', () => {
  it('knows the real past papers by their source', () => {
    expect(isRealExamSource('g5_final_2019')).toBe(true);
    expect(isRealExamSource('g6_final_2024')).toBe(true);
    expect(isRealExamSource('g4_mse_final_2017')).toBe(true);
    expect(isRealExamSource('g3_mega_final_2019')).toBe(true);
    expect(isRealExamSource('mega_final_2020')).toBe(true);
    expect(isRealExamSource('previous_year_2018')).toBe(true);
    expect(isRealExamSource('pdf_extracted')).toBe(false);
    expect(isRealExamSource('variant_generator_phase1')).toBe(false);
    expect(isRealExamSource('g5_final_')).toBe(false);
  });

  it('puts a real paper question on the Exam step whatever its difficulty', () => {
    expect(stepOfQuestion({ difficulty: 'Easy', source: GEN })).toBe('warmup');
    expect(stepOfQuestion({ difficulty: 'Medium', source: GEN })).toBe('build');
    expect(stepOfQuestion({ difficulty: 'Hard', source: GEN })).toBe('challenge');
    expect(stepOfQuestion({ difficulty: 'Easy', source: REAL })).toBe('exam');
  });
});

describe('computeLadder', () => {
  it('has no ladder for a topic with no questions', () => {
    expect(computeLadder({ topicLabel: 'Triangles', pool: [], attempts: [] })).toBeNull();
  });

  it('starts a new child on Warm-up', () => {
    const { info } = plan([]);
    expect(info.topicLabel).toBe('HCF & LCM');
    expect(info.current).toBe(0);
    expect(info.got).toBe(0);
    expect(info.needed).toBe(LADDER_NEEDED);
    expect(info.complete).toBe(false);
    expect(info.steps.map((s) => s.id)).toEqual(['warmup', 'build', 'challenge', 'exam']);
    expect(info.steps.map((s) => s.label)).toEqual(['Warm-up', 'Build', 'Challenge', 'Real exam']);
    expect(info.steps.map((s) => s.done)).toEqual([false, false, false, false]);
  });

  it('counts right answers at the step and moves up after three', () => {
    expect(plan(rights('e', 'Easy', 2)).info.got).toBe(2);
    expect(plan(rights('e', 'Easy', 2)).info.current).toBe(0);

    const { info } = plan(rights('e', 'Easy', 3));
    expect(info.current).toBe(1);
    expect(info.got).toBe(0);
    expect(info.steps[0].done).toBe(true);
    expect(info.steps[1].done).toBe(false);
  });

  it('a slip does not wipe out what the child has shown', () => {
    const { info } = plan([
      answer('e1', 'Easy', true),
      answer('e2', 'Easy', false),
      answer('e3', 'Easy', true),
      answer('e4', 'Easy', true),
    ]);
    expect(info.current).toBe(1);
  });

  it('counts only the first answer to each question', () => {
    const { info } = plan([
      answer('e1', 'Easy', false),
      answer('e1', 'Easy', true), // a second go at the same question
      answer('e2', 'Easy', true),
      answer('e3', 'Easy', true),
    ]);
    expect(info.current).toBe(0);
    expect(info.got).toBe(2);
  });

  it('three in a row not right sends the child back a step for a short refresher', () => {
    const struggling = rights('e', 'Easy', 3).concat([
      answer('m1', 'Medium', false),
      answer('m2', 'Medium', false),
      answer('m3', 'Medium', false),
    ]);
    const back = plan(struggling).info;
    expect(back.current).toBe(0);
    expect(back.got).toBe(0);
    expect(back.needed).toBe(LADDER_REFRESH_NEEDED);
    expect(back.steps[0].done).toBe(false);

    const again = plan(struggling.concat([answer('e4', 'Easy', true), answer('e5', 'Easy', true)])).info;
    expect(again.current).toBe(1);
    expect(again.got).toBe(0);
    expect(again.needed).toBe(LADDER_NEEDED);
  });

  it('on the lowest step there is nowhere to go back to', () => {
    const { info } = plan([answer('e1', 'Easy', false), answer('e2', 'Easy', false), answer('e3', 'Easy', false)]);
    expect(info.current).toBe(0);
    expect(info.got).toBe(0);
    expect(info.needed).toBe(LADDER_NEEDED);
  });

  it('a right answer on a harder question counts; one that is not right is ignored', () => {
    // On Warm-up, a Medium answered right counts towards Warm-up.
    expect(plan([answer('m1', 'Medium', true)]).info.got).toBe(1);

    // On Build: two Medium misses, then a Hard miss (above the step, ignored).
    const onBuild = rights('e', 'Easy', 3).concat([
      answer('m1', 'Medium', false),
      answer('m2', 'Medium', false),
      answer('h1', 'Hard', false),
    ]);
    expect(plan(onBuild).info.current).toBe(1);
    // The third Medium miss is what sends the child back.
    expect(plan(onBuild.concat([answer('m3', 'Medium', false)])).info.current).toBe(0);
  });

  it('easier questions do not move a harder step along', () => {
    const { info } = plan(rights('e', 'Easy', 3).concat(rights('f', 'Easy', 3)));
    expect(info.current).toBe(1);
    expect(info.got).toBe(0);
  });

  it('skips a step the topic has no questions for and marks it done', () => {
    const pool = [q('m1', 'Medium'), q('m2', 'Medium'), q('x1', 'Hard', REAL), q('x2', 'Easy', REAL), q('x3', 'Medium', REAL)];
    const start = plan([], pool).info;
    expect(start.current).toBe(1);
    expect(start.steps.map((s) => s.done)).toEqual([true, false, true, false]);

    const after = plan(rights('m', 'Medium', 3), pool).info;
    expect(after.current).toBe(3);
  });

  it('a child who is already doing well starts after Warm-up, but never on the Exam step', () => {
    const strong = plan([], fullPool(), true).info;
    expect(strong.current).toBe(1);
    expect(strong.steps[0].done).toBe(true);

    const easyAndExamOnly = [q('e1', 'Easy'), q('x1', 'Hard', REAL), q('x2', 'Hard', REAL), q('x3', 'Hard', REAL)];
    expect(plan([], easyAndExamOnly, true).info.current).toBe(0);
  });

  it('calls the last step Exam-style when the topic has too few real paper questions', () => {
    const twoReal = [q('e1', 'Easy'), q('h1', 'Hard'), q('x1', 'Medium', REAL), q('x2', 'Medium', REAL)];
    expect(plan([], twoReal).info.steps[3].label).toBe('Exam-style');
    const noReal = [q('e1', 'Easy'), q('h1', 'Hard')];
    expect(plan([], noReal).info.steps[3].label).toBe('Exam-style');
    expect(plan([], noReal).info.steps[3].done).toBe(false);
  });

  it('on the Exam step, real paper questions and the hardest others count; easy ones do not', () => {
    const toExam = rights('e', 'Easy', 3).concat(rights('m', 'Medium', 3), rights('h', 'Hard', 3));
    expect(plan(toExam).info.current).toBe(3);
    expect(plan(toExam.concat([answer('e9', 'Easy', true)])).info.got).toBe(0);
    expect(plan(toExam.concat([answer('h9', 'Hard', true)])).info.got).toBe(1);
    expect(plan(toExam.concat([answer('x1', 'Easy', true, REAL)])).info.got).toBe(1);
  });

  it('finishes the topic after three right on the Exam step', () => {
    const all = rights('e', 'Easy', 3).concat(
      rights('m', 'Medium', 3),
      rights('h', 'Hard', 3),
      rights('x', 'Medium', 3, REAL),
    );
    const { info } = plan(all);
    expect(info.complete).toBe(true);
    expect(info.current).toBe(3);
    expect(info.got).toBe(3);
    expect(info.needed).toBe(3);
    expect(info.steps.map((s) => s.done)).toEqual([true, true, true, true]);

    // Later answers that are not right do not undo a finished topic.
    const later = all.concat([
      answer('x7', 'Hard', false, REAL),
      answer('x8', 'Hard', false, REAL),
      answer('x9', 'Hard', false, REAL),
    ]);
    expect(plan(later).info.complete).toBe(true);
  });
});

describe('ladderTiers', () => {
  it('offers the current step first', () => {
    const tiers = ladderTiers(plan([]), fullPool());
    expect(tiers[0].map((t) => t.difficulty)).toEqual(['Easy', 'Easy', 'Easy', 'Easy', 'Easy']);
    expect(tiers[0].every((t) => t.source === GEN)).toBe(true);
  });

  it('falls forward to the next step when the current one has run out', () => {
    const unseen = fullPool().filter((x) => x.difficulty !== 'Easy' || x.source === REAL);
    const tiers = ladderTiers(plan([]), unseen);
    expect(tiers[0].every((t) => t.difficulty === 'Medium' && t.source === GEN)).toBe(true);
  });

  it('falls back to the nearest easier step only when nothing harder is left', () => {
    const onChallenge = plan(rights('e', 'Easy', 3).concat(rights('m', 'Medium', 3)));
    expect(onChallenge.info.current).toBe(2);
    const tiers = ladderTiers(onChallenge, [q('e7', 'Easy'), q('m7', 'Medium')]);
    expect(tiers.map((t) => t[0].id)).toEqual(['m7', 'e7']);
  });

  it('on the Exam step after Challenge: hard real questions, then other real ones, then the hardest of the rest', () => {
    const onExam = plan(rights('e', 'Easy', 3).concat(rights('m', 'Medium', 3), rights('h', 'Hard', 3)));
    const tiers = ladderTiers(onExam, [q('h7', 'Hard'), q('xe', 'Easy', REAL), q('xh', 'Hard', REAL), q('e7', 'Easy')]);
    expect(tiers.map((t) => t[0].id)).toEqual(['xh', 'xe', 'h7', 'e7']);
  });

  it('a topic that is only exam questions still goes from easy to hard', () => {
    const pool = [q('xe', 'Easy', REAL), q('xm', 'Medium', REAL), q('xh', 'Hard', REAL)];
    const fresh = plan([], pool);
    expect(fresh.info.current).toBe(3);
    expect(ladderTiers(fresh, pool)[0][0].id).toBe('xe');

    const oneRight = plan([answer('xe', 'Easy', true, REAL)], pool);
    expect(oneRight.info.got).toBe(1);
    expect(ladderTiers(oneRight, pool)[0][0].id).toBe('xm');
  });
});

describe('withServedQuestion', () => {
  it('says Real exam only while the question on screen is from a real paper', () => {
    const onExam = plan(rights('e', 'Easy', 3).concat(rights('m', 'Medium', 3), rights('h', 'Hard', 3))).info;
    expect(withServedQuestion(onExam, true).steps[3].label).toBe('Real exam');
    expect(withServedQuestion(onExam, false).steps[3].label).toBe('Exam-style');
  });

  it('leaves the ladder alone before the Exam step', () => {
    const early = plan([]).info;
    expect(withServedQuestion(early, false)).toBe(early);
  });
});

describe('ladderAfterAnswer', () => {
  it('does nothing for an answer that is not right', () => {
    const info = plan([]).info;
    expect(ladderAfterAnswer(info, false)).toBe(info);
  });

  it('adds one right answer', () => {
    const next = ladderAfterAnswer(plan([]).info, true);
    expect(next.got).toBe(1);
    expect(next.current).toBe(0);
  });

  it('finishes the step and moves to the next one that is not done', () => {
    const next = ladderAfterAnswer(plan(rights('e', 'Easy', 2)).info, true);
    expect(next.current).toBe(1);
    expect(next.got).toBe(0);
    expect(next.steps[0].done).toBe(true);
  });

  it('finishes the topic on the last step', () => {
    const nearly = plan(
      rights('e', 'Easy', 3).concat(rights('m', 'Medium', 3), rights('h', 'Hard', 3), rights('x', 'Medium', 2, REAL)),
    ).info;
    expect(nearly.current).toBe(3);
    expect(nearly.got).toBe(2);
    const done = ladderAfterAnswer(nearly, true);
    expect(done.complete).toBe(true);
    expect(done.got).toBe(done.needed);
    expect(done.steps.every((s) => s.done)).toBe(true);
  });
});

describe('isStrongStart', () => {
  it('needs at least five answers, four in five of them right', () => {
    expect(isStrongStart([true, true, true, true])).toBe(false);
    expect(isStrongStart([true, true, true, true, false])).toBe(true);
    expect(isStrongStart([true, true, true, true, true, true, true, false, false, false])).toBe(false);
    expect(isStrongStart([])).toBe(false);
  });
});

describe('variantIdPrefixes', () => {
  it('finds the generated questions whose topic is only in their id', () => {
    expect(variantIdPrefixes(5, 'hcf')).toEqual(['VAR_G5_vary_hcf_lcm_V']);
    expect(variantIdPrefixes(5, 'MONEY')).toEqual(['VAR_G5_vary_percentage_V']);
    expect(variantIdPrefixes(5, 'triangle')).toEqual([]);
    expect(variantIdPrefixes(6, 'hcf')).toEqual([]);
  });
});
