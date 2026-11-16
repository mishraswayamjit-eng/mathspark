// The question bank, as the database sees it.
//
// ONE place that (a) reads the bank files under data/bank and (b) turns a bank
// question into a row of the `Question` table, and back again. It is used by:
//   - scripts/bank/sync.mjs          the sync that runs in the production build
//   - src/app/api/seed/route.ts      the manual re-seed
//   - src/app/api/admin/bank-export  the export of database-only questions
//
// Plain JavaScript on purpose: the build-time sync is a plain Node script and
// cannot import TypeScript. The types live beside this file in bankRows.d.mts.
// Keep the imports to `fs` and `path` (default imports), so the same file loads
// in Node, in the Next.js server bundle and in the unit tests.
//
// The mapping must stay exactly what the seed route has always written: the
// sync compares these rows with the database, and any drift here shows up as
// thousands of "changed" questions.

import fs from 'fs';
import path from 'path';

// ---------------------------------------------------------------------------
// The pools (rows of the `Topic` table) a question can belong to
// ---------------------------------------------------------------------------

export const BANK_TOPICS = [
  // Grade 4 curriculum chapters
  { id: 'ch01-05', name: 'Number System & Place Value',    chapterNumber: '1-5'  },
  { id: 'ch06',    name: 'Factors & Multiples',             chapterNumber: '6'    },
  { id: 'ch07-08', name: 'Fractions',                       chapterNumber: '7-8'  },
  { id: 'ch09-10', name: 'Operations & BODMAS',             chapterNumber: '9-10' },
  { id: 'ch11',    name: 'Decimal Fractions',               chapterNumber: '11'   },
  { id: 'ch12',    name: 'Decimal Units of Measurement',    chapterNumber: '12'   },
  { id: 'ch13',    name: 'Algebraic Expressions',           chapterNumber: '13'   },
  { id: 'ch14',    name: 'Equations',                       chapterNumber: '14'   },
  { id: 'ch15',    name: 'Puzzles & Magic Squares',         chapterNumber: '15'   },
  { id: 'ch16',    name: 'Sequence & Series',               chapterNumber: '16'   },
  { id: 'ch17',    name: 'Measurement of Time & Calendar',  chapterNumber: '17'   },
  { id: 'ch18',    name: 'Angles',                          chapterNumber: '18'   },
  { id: 'ch19',    name: 'Triangles',                       chapterNumber: '19'   },
  { id: 'ch20',    name: 'Quadrilaterals',                  chapterNumber: '20'   },
  { id: 'ch21',    name: 'Circle',                          chapterNumber: '21'   },
  { id: 'dh',      name: 'Data Handling & Graphs',          chapterNumber: 'DH'   },
  // IPM past-paper / practice pools (Grades 2–9)
  { id: 'grade2',  name: 'Grade 2 — IPM Practice',         chapterNumber: 'G2'   },
  { id: 'grade3',  name: 'Grade 3 — IPM Practice',         chapterNumber: 'G3'   },
  { id: 'grade4',  name: 'Grade 4 — IPM Past Papers',      chapterNumber: 'G4'   },
  { id: 'grade5',  name: 'Grade 5 — IPM Practice',         chapterNumber: 'G5'   },
  { id: 'grade6',  name: 'Grade 6 — IPM Practice',         chapterNumber: 'G6'   },
  { id: 'grade7',  name: 'Grade 7 — IPM Practice',         chapterNumber: 'G7'   },
  { id: 'grade8',  name: 'Grade 8 — IPM Practice',         chapterNumber: 'G8'   },
  { id: 'grade9',  name: 'Grade 9 — IPM Practice',         chapterNumber: 'G9'   },
];

export const BANK_TOPIC_IDS = BANK_TOPICS.map((t) => t.id);

const DEFAULT_VALID_IDS = new Set(BANK_TOPIC_IDS);

/**
 * The columns of `Question` whose values come from the bank, apart from `id`
 * and `nodeId`. The sync compares exactly these.
 */
export const CONTENT_COLUMNS = [
  'topicId', 'subTopic', 'difficulty', 'questionText', 'questionLatex',
  'option1', 'option2', 'option3', 'option4', 'correctAnswer',
  'hint1', 'hint2', 'hint3', 'stepByStep',
  'misconceptionA', 'misconceptionB', 'misconceptionC', 'misconceptionD',
  'source', 'year', 'questionNumber',
];

/**
 * Pool ids that appear in question data but are not rows of `Topic`: bare
 * chapter numbers (ch01, ch07, ch09) where the database uses merged ranges.
 */
const TOPIC_ID_REMAP = {
  ch01: 'ch01-05', ch02: 'ch01-05', ch03: 'ch01-05', ch04: 'ch01-05', ch05: 'ch01-05',
  ch07: 'ch07-08', ch08: 'ch07-08',
  ch09: 'ch09-10', ch10: 'ch09-10',
};

// ---------------------------------------------------------------------------
// Bank question → database row
// ---------------------------------------------------------------------------

/**
 * Text for a database column: missing → '', and null bytes removed
 * (PostgreSQL rejects \x00 in text columns, error 22021). A number or boolean
 * becomes its text; anything else (a list, an object) is a mistake in the data.
 */
export function cleanText(value) {
  if (value === undefined || value === null) return '';
  if (typeof value === 'string') return value.replace(/\x00/g, '');
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  throw new TypeError('expected text, found ' + (Array.isArray(value) ? 'a list' : typeof value));
}

/** The pool a question id implies, for a question that names no usable pool. */
export function topicIdFromQuestionId(questionId) {
  const upper = String(questionId).toUpperCase();
  if (upper.startsWith('Q_DH_')) return 'dh';
  if (upper.startsWith('PYQ_')) return 'grade4'; // real IPM Std.4 past papers
  // EXT_G*, VAR_EXT_G*, VAR_G* patterns → grade pool
  const gradeMatch = upper.match(/(?:EXT|VAR_EXT|VAR)_G(\d)/);
  if (gradeMatch) {
    const g = parseInt(gradeMatch[1], 10);
    if (g >= 2 && g <= 9) return 'grade' + g;
  }
  const match = upper.match(/^Q_CH(\d+)_/);
  if (!match) return 'ch11';
  const n = parseInt(match[1], 10);
  if (n <= 5) return 'ch01-05';
  if (n === 6) return 'ch06';
  if (n === 7 || n === 8) return 'ch07-08';
  if (n === 9 || n === 10) return 'ch09-10';
  return 'ch' + String(n).padStart(2, '0');
}

/** A question's pool: the one it names, remapped, with the id as the fallback. */
export function resolveTopicId(questionId, rawTopicId, validIds) {
  const valid = validIds || DEFAULT_VALID_IDS;
  // 1. The explicit value, or the one the id implies.
  let tid = rawTopicId !== undefined && rawTopicId !== null ? rawTopicId : topicIdFromQuestionId(questionId);
  // 2. Known bare chapter numbers (ch01 → ch01-05, …).
  if (typeof tid === 'string' && Object.prototype.hasOwnProperty.call(TOPIC_ID_REMAP, tid)) tid = TOPIC_ID_REMAP[tid];
  // 3. Still not a pool: the one the id implies.
  if (!valid.has(tid)) tid = topicIdFromQuestionId(questionId);
  // 4. Still not a pool (an unexpected id): ch11.
  if (!valid.has(tid)) tid = 'ch11';
  return tid;
}

/**
 * One bank question as a row of the `Question` table. Never sets `retired`.
 * Throws when the question has no id or a text field holds a list or object.
 */
export function bankQuestionToRow(q, validIds) {
  if (!q || typeof q !== 'object' || Array.isArray(q)) throw new TypeError('a question must be an object');
  if (typeof q.id !== 'string' || q.id === '') throw new TypeError('a question must have a text id');

  const options = Array.isArray(q.options) ? q.options : [];
  const hints = Array.isArray(q.hints) ? q.hints : [];
  const misconceptions = q.misconceptions && typeof q.misconceptions === 'object' ? q.misconceptions : {};
  const optionText = (i) => cleanText(options[i] && typeof options[i] === 'object' ? options[i].text : undefined);

  return {
    id:             q.id,
    topicId:        resolveTopicId(q.id, q.topicId, validIds),
    subTopic:       cleanText(q.subTopic),
    difficulty:     cleanText(q.difficulty) || 'Medium',
    questionText:   cleanText(q.questionText),
    questionLatex:  cleanText(q.questionLatex),
    option1:        optionText(0),
    option2:        optionText(1),
    option3:        optionText(2),
    option4:        optionText(3),
    correctAnswer:  cleanText(q.correctAnswer) || 'A',
    hint1:          cleanText(hints[0]),
    hint2:          cleanText(hints[1]),
    hint3:          cleanText(hints[2]),
    stepByStep:     cleanText(JSON.stringify(q.stepByStep !== undefined && q.stepByStep !== null ? q.stepByStep : [])),
    misconceptionA: cleanText(misconceptions.A),
    misconceptionB: cleanText(misconceptions.B),
    misconceptionC: cleanText(misconceptions.C),
    misconceptionD: cleanText(misconceptions.D),
    source:         cleanText(q.source) || 'auto_generated',
    year:           q.year !== undefined && q.year !== null ? q.year : null,
    questionNumber: q.questionNumber !== undefined && q.questionNumber !== null ? q.questionNumber : null,
    nodeId:         typeof q.node === 'string' && q.node !== '' ? cleanText(q.node) : null,
  };
}

// ---------------------------------------------------------------------------
// Database row → bank question (the reverse, for the export)
// ---------------------------------------------------------------------------

/** One row of `Question` in the shape of a bank question. `node` is always null. */
export function rowToBankQuestion(row) {
  const hints = [row.hint1 || '', row.hint2 || '', row.hint3 || ''];
  while (hints.length > 0 && hints[hints.length - 1] === '') hints.pop();

  let steps = [];
  try {
    const parsed = JSON.parse(row.stepByStep || '[]');
    if (Array.isArray(parsed)) steps = parsed;
  } catch (err) {
    steps = [];
  }

  const out = {
    id:            row.id,
    node:          null,
    topicId:       row.topicId,
    subTopic:      row.subTopic || '',
    difficulty:    row.difficulty || '',
    questionText:  row.questionText || '',
    questionLatex: row.questionLatex || '',
    options: [
      { id: 'A', text: row.option1 || '' },
      { id: 'B', text: row.option2 || '' },
      { id: 'C', text: row.option3 || '' },
      { id: 'D', text: row.option4 || '' },
    ],
    correctAnswer: row.correctAnswer || '',
    hints,
    stepByStep:    steps,
    misconceptions: {
      A: row.misconceptionA || '',
      B: row.misconceptionB || '',
      C: row.misconceptionC || '',
      D: row.misconceptionD || '',
    },
    source:        row.source || '',
  };
  if (row.year !== undefined && row.year !== null) out.year = row.year;
  if (row.questionNumber !== undefined && row.questionNumber !== null) out.questionNumber = row.questionNumber;
  return out;
}

// ---------------------------------------------------------------------------
// Reading the bank files
// ---------------------------------------------------------------------------

/** data/bank under the given project root (default: the working directory). */
export function bankDir(rootDir) {
  return path.join(rootDir || process.cwd(), 'data', 'bank');
}

/**
 * Read every bank file: each `*.json` directly inside data/bank/gradeN, in a
 * fixed order (grades by number, files by name), concatenated.
 *
 * A missing data/bank is not an error: `exists` is false and the lists are
 * empty. A file that is not a JSON array throws, naming the file.
 */
export function loadBank(rootDir) {
  const dir = bankDir(rootDir);
  const out = { exists: false, dir, files: [], questions: [], fileOf: [] };

  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (err) {
    if (err && (err.code === 'ENOENT' || err.code === 'ENOTDIR')) return out;
    throw err;
  }
  out.exists = true;

  const grades = entries
    .filter((e) => e.isDirectory() && /^grade\d+$/.test(e.name))
    .map((e) => e.name)
    .sort((a, b) => Number(a.slice(5)) - Number(b.slice(5)));

  for (let g = 0; g < grades.length; g++) {
    const gradeDir = path.join(dir, grades[g]);
    const names = fs.readdirSync(gradeDir).filter((n) => /\.json$/i.test(n)).sort();
    for (let f = 0; f < names.length; f++) {
      const rel = 'data/bank/' + grades[g] + '/' + names[f];
      let parsed;
      try {
        let text = fs.readFileSync(path.join(gradeDir, names[f]), 'utf8');
        if (text.charCodeAt(0) === 0xfeff) text = text.slice(1); // a byte-order mark
        parsed = JSON.parse(text);
      } catch (err) {
        throw new Error(rel + ': could not be read as JSON (' + (err && err.message ? err.message : String(err)) + ')');
      }
      if (!Array.isArray(parsed)) throw new Error(rel + ': expected a JSON array of questions');
      out.files.push({ file: rel, grade: grades[g], count: parsed.length });
      for (let i = 0; i < parsed.length; i++) {
        out.questions.push(parsed[i]);
        out.fileOf.push(rel);
      }
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// Checking the bank (no database)
// ---------------------------------------------------------------------------

const MAX_LISTED_PROBLEMS = 40;

/**
 * Map every question and check the bank is fit to sync.
 *
 * Problems (the sync refuses to run): a question that is not an object, has no
 * id, repeats an id, names no pool, has no question text, has a correct answer
 * that is not A–D, has options that are not a list, a `node` that is not text
 * or null, a year or question number that is not a whole number, or a text
 * field holding a list or object.
 *
 * Notes (counted, not problems): questions with an empty option (the app never
 * serves those), a pool id that was remapped, and questions with no node.
 */
export function checkBank(questions, opts) {
  const validIds = (opts && opts.validIds) || DEFAULT_VALID_IDS;
  const fileOf = (opts && opts.fileOf) || [];
  const rows = [];
  const problems = [];
  let problemCount = 0;
  const notes = { emptyOption: 0, poolRemapped: 0, noNode: 0 };
  const firstSeenIn = new Map();

  function problem(i, id, text) {
    problemCount++;
    if (problems.length < MAX_LISTED_PROBLEMS) {
      problems.push((fileOf[i] || 'question ' + i) + (id ? ' [' + id + ']' : ' [item ' + i + ']') + ': ' + text);
    }
  }
  const wholeOrMissing = (v) => v === undefined || v === null || (typeof v === 'number' && Number.isInteger(v));

  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    if (!q || typeof q !== 'object' || Array.isArray(q)) { problem(i, '', 'is not an object'); continue; }
    if (typeof q.id !== 'string' || q.id === '') { problem(i, '', 'has no id'); continue; }
    const id = q.id;
    if (firstSeenIn.has(id)) { problem(i, id, 'id is repeated (first in ' + firstSeenIn.get(id) + ')'); continue; }
    firstSeenIn.set(id, fileOf[i] || 'question ' + i);

    let bad = false;
    if (typeof q.topicId !== 'string' || q.topicId === '') { problem(i, id, 'names no pool (topicId)'); bad = true; }
    if (typeof q.questionText !== 'string' || q.questionText.trim() === '') { problem(i, id, 'has no question text'); bad = true; }
    if (['A', 'B', 'C', 'D'].indexOf(q.correctAnswer) === -1) { problem(i, id, 'correctAnswer is not A, B, C or D'); bad = true; }
    // Missing options are a note below (the app never serves such a question); a wrong shape is a problem.
    if (q.options !== undefined && q.options !== null && !Array.isArray(q.options)) { problem(i, id, 'options is not a list'); bad = true; }
    if (!(q.node === undefined || q.node === null || typeof q.node === 'string')) { problem(i, id, 'node is not text or null'); bad = true; }
    if (!wholeOrMissing(q.year)) { problem(i, id, 'year is not a whole number'); bad = true; }
    if (!wholeOrMissing(q.questionNumber)) { problem(i, id, 'questionNumber is not a whole number'); bad = true; }
    if (bad) continue;

    let row;
    try {
      row = bankQuestionToRow(q, validIds);
    } catch (err) {
      problem(i, id, err && err.message ? err.message : String(err));
      continue;
    }
    if (row.option1 === '' || row.option2 === '' || row.option3 === '' || row.option4 === '') notes.emptyOption++;
    if (row.topicId !== q.topicId) notes.poolRemapped++;
    if (row.nodeId === null) notes.noNode++;
    rows.push(row);
  }

  return { rows, problems, problemCount, notes };
}
