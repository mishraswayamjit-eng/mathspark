import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import {
  BANK_TOPIC_IDS,
  CONTENT_COLUMNS,
  bankQuestionToRow,
  checkBank,
  loadBank,
  resolveTopicId,
  rowToBankQuestion,
} from '../../../scripts/bank/bankRows.mjs';
import type { BankQuestion } from '../../../scripts/bank/bankRows.mjs';

// The one mapping from a bank question to a `Question` row. The build-time
// sync (scripts/bank/sync.mjs) compares these rows with the database, so the
// mapping must stay exactly what the seed route has always written.

const FULL: BankQuestion = {
  id: 'EXT_G5_FRAC_001',
  node: 'gr5_fractions',
  topicId: 'grade5',
  subTopic: 'Grade 5 — Fractions',
  difficulty: 'Hard',
  questionText: 'What is 1/2 + 1/4?',
  questionLatex: '\\frac{1}{2}+\\frac{1}{4}',
  options: [
    { id: 'A', text: '3/4' },
    { id: 'B', text: '2/6' },
    { id: 'C', text: '1/6' },
    { id: 'D', text: '2/4' },
  ],
  correctAnswer: 'A',
  hints: ['Make the bottom numbers the same.', 'Change 1/2 into quarters.'],
  stepByStep: [{ step: 1, text: '1/2 = 2/4' }, { step: 2, text: '2/4 + 1/4 = 3/4' }],
  misconceptions: { B: 'Added tops and bottoms.', D: 'Forgot to add 1/4.' },
  source: 'pdf_extracted',
  year: 2016,
  questionNumber: 7,
};

describe('bankQuestionToRow', () => {
  it('writes a full question exactly as the seed route always has', () => {
    expect(bankQuestionToRow(FULL)).toEqual({
      id: 'EXT_G5_FRAC_001',
      topicId: 'grade5',
      subTopic: 'Grade 5 — Fractions',
      difficulty: 'Hard',
      questionText: 'What is 1/2 + 1/4?',
      questionLatex: '\\frac{1}{2}+\\frac{1}{4}',
      option1: '3/4',
      option2: '2/6',
      option3: '1/6',
      option4: '2/4',
      correctAnswer: 'A',
      hint1: 'Make the bottom numbers the same.',
      hint2: 'Change 1/2 into quarters.',
      hint3: '',
      stepByStep: '[{"step":1,"text":"1/2 = 2/4"},{"step":2,"text":"2/4 + 1/4 = 3/4"}]',
      misconceptionA: '',
      misconceptionB: 'Added tops and bottoms.',
      misconceptionC: '',
      misconceptionD: 'Forgot to add 1/4.',
      source: 'pdf_extracted',
      year: 2016,
      questionNumber: 7,
      nodeId: 'gr5_fractions',
    });
  });

  it('fills the same defaults as the seed route for a bare question', () => {
    expect(bankQuestionToRow({ id: 'Q_CH06_010' })).toEqual({
      id: 'Q_CH06_010',
      topicId: 'ch06',
      subTopic: '',
      difficulty: 'Medium',
      questionText: '',
      questionLatex: '',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      correctAnswer: 'A',
      hint1: '',
      hint2: '',
      hint3: '',
      stepByStep: '[]',
      misconceptionA: '',
      misconceptionB: '',
      misconceptionC: '',
      misconceptionD: '',
      source: 'auto_generated',
      year: null,
      questionNumber: null,
      nodeId: null,
    });
  });

  it('never sets retired, and has every content column', () => {
    const row = bankQuestionToRow(FULL) as unknown as { [key: string]: unknown };
    expect('retired' in row).toBe(false);
    for (let i = 0; i < CONTENT_COLUMNS.length; i++) {
      expect(Object.prototype.hasOwnProperty.call(row, CONTENT_COLUMNS[i])).toBe(true);
    }
    // id + the content columns + nodeId, and nothing else
    expect(Object.keys(row).length).toBe(CONTENT_COLUMNS.length + 2);
  });

  it('strips null bytes, which PostgreSQL rejects', () => {
    const row = bankQuestionToRow({ id: 'Q_CH11_001', questionText: 'a\u0000b', subTopic: '\u0000x' });
    expect(row.questionText).toBe('ab');
    expect(row.subTopic).toBe('x');
  });

  it('treats a missing or empty node as no node', () => {
    expect(bankQuestionToRow({ id: 'Q_CH11_001', node: null }).nodeId).toBeNull();
    expect(bankQuestionToRow({ id: 'Q_CH11_001', node: '' }).nodeId).toBeNull();
    expect(bankQuestionToRow({ id: 'Q_CH11_001' }).nodeId).toBeNull();
  });

  it('rejects a question with no id', () => {
    expect(() => bankQuestionToRow({ id: '' })).toThrow();
  });
});

describe('resolveTopicId', () => {
  it('keeps a pool that exists', () => {
    expect(resolveTopicId('EXT_G5_X_001', 'grade5')).toBe('grade5');
    expect(resolveTopicId('Q_CH06_001', 'ch06')).toBe('ch06');
  });

  it('remaps bare chapter numbers to the merged pools', () => {
    expect(resolveTopicId('Q_CH02_001', 'ch02')).toBe('ch01-05');
    expect(resolveTopicId('Q_CH08_001', 'ch08')).toBe('ch07-08');
    expect(resolveTopicId('Q_CH10_001', 'ch10')).toBe('ch09-10');
  });

  it('falls back to the pool the id implies, then to ch11', () => {
    expect(resolveTopicId('Q_DH_004', undefined)).toBe('dh');
    expect(resolveTopicId('PYQ_2016_Q01', null)).toBe('grade4');
    expect(resolveTopicId('VAR_G7_vary_x_V01', 'nowhere')).toBe('grade7');
    expect(resolveTopicId('SOMETHING_ELSE', 'nowhere')).toBe('ch11');
    expect(resolveTopicId('Q_CH14_003', 'constructor')).toBe('ch14');
  });

  it('knows the 24 pools', () => {
    expect(BANK_TOPIC_IDS.length).toBe(24);
    expect(BANK_TOPIC_IDS.indexOf('ch01-05')).not.toBe(-1);
    expect(BANK_TOPIC_IDS.indexOf('grade9')).not.toBe(-1);
  });
});

describe('rowToBankQuestion (the export)', () => {
  it('is the reverse of the mapping', () => {
    const row = bankQuestionToRow(FULL);
    const back = rowToBankQuestion(row);
    expect(back.node).toBeNull();
    expect(back.options).toEqual(FULL.options);
    expect(back.hints).toEqual(FULL.hints); // no trailing empty hints
    expect(back.stepByStep).toEqual(FULL.stepByStep);
    expect(back.misconceptions).toEqual({ A: '', B: 'Added tops and bottoms.', C: '', D: 'Forgot to add 1/4.' });
    expect(back.year).toBe(2016);
    expect(back.questionNumber).toBe(7);

    // Mapping the exported question again gives the same row, apart from the node.
    const again = bankQuestionToRow(back);
    expect(again).toEqual({ ...row, nodeId: null });
  });

  it('leaves out year and question number when there are none, and survives bad steps', () => {
    const row = { ...bankQuestionToRow({ id: 'AIGEN_grade5_x', topicId: 'grade5' }), stepByStep: 'not json' };
    const back = rowToBankQuestion(row);
    expect('year' in back).toBe(false);
    expect('questionNumber' in back).toBe(false);
    expect(back.stepByStep).toEqual([]);
    expect(back.hints).toEqual([]);
  });
});

describe('checkBank', () => {
  it('passes a good bank and returns its rows', () => {
    const result = checkBank([FULL, { ...FULL, id: 'EXT_G5_FRAC_002', node: null }]);
    expect(result.problemCount).toBe(0);
    expect(result.rows.length).toBe(2);
    expect(result.notes.noNode).toBe(1);
  });

  it('reports repeated ids, missing pools, missing text and bad answers', () => {
    const result = checkBank(
      [
        FULL,
        FULL,
        { ...FULL, id: 'B1', topicId: '' },
        { ...FULL, id: 'B2', questionText: '  ' },
        { ...FULL, id: 'B3', correctAnswer: 'E' },
        { ...FULL, id: '' },
      ],
      { fileOf: ['a.json', 'b.json', 'b.json', 'b.json', 'b.json', 'b.json'] },
    );
    expect(result.problemCount).toBe(5);
    expect(result.rows.length).toBe(1);
    expect(result.problems[0]).toContain('b.json');
    expect(result.problems[0]).toContain('repeated');
  });

  it('counts a question with an empty option as a note, not a problem', () => {
    const result = checkBank([{ ...FULL, options: [{ id: 'A', text: '3/4' }] }]);
    expect(result.problemCount).toBe(0);
    expect(result.notes.emptyOption).toBe(1);
  });
});

describe('loadBank', () => {
  it('says so, without failing, when data/bank does not exist', () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'bank-none-'));
    const bank = loadBank(root);
    expect(bank.exists).toBe(false);
    expect(bank.questions).toEqual([]);
  });

  it('reads every json file directly inside a grade folder, in a fixed order, and skips _meta.json', () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'bank-some-'));
    const dir = path.join(root, 'data', 'bank');
    fs.mkdirSync(path.join(dir, 'grade10'), { recursive: true });
    fs.mkdirSync(path.join(dir, 'grade5', 'nested'), { recursive: true });
    fs.writeFileSync(path.join(dir, '_meta.json'), '{"note":"not questions"}');
    fs.writeFileSync(path.join(dir, 'grade10', 'gr10_x.json'), '[{"id":"T10"}]');
    fs.writeFileSync(path.join(dir, 'grade5', 'gr5_fractions.json'), '[\n{"id":"F1"},\n{"id":"F2"}\n]\n');
    fs.writeFileSync(path.join(dir, 'grade5', '_unsorted.json'), '[{"id":"U1"}]');
    fs.writeFileSync(path.join(dir, 'grade5', 'nested', 'deep.json'), '[{"id":"NOPE"}]');

    const bank = loadBank(root);
    expect(bank.exists).toBe(true);
    expect(bank.questions.map((q) => q.id)).toEqual(['U1', 'F1', 'F2', 'T10']);
    expect(bank.files.length).toBe(3);
    expect(bank.fileOf[1]).toBe('data/bank/grade5/gr5_fractions.json');
  });

  it('names the file when one is not a list', () => {
    const root = fs.mkdtempSync(path.join(os.tmpdir(), 'bank-bad-'));
    fs.mkdirSync(path.join(root, 'data', 'bank', 'grade2'), { recursive: true });
    fs.writeFileSync(path.join(root, 'data', 'bank', 'grade2', 'gr2_x.json'), '{"questions":[]}');
    expect(() => loadBank(root)).toThrow(/gr2_x\.json/);
  });
});
