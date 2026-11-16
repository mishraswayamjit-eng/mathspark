// Types for bankRows.mjs (plain JavaScript so the build-time sync can load it).

/** One question as it is written in a bank file (data/bank/gradeN/*.json). */
export interface BankQuestion {
  id: string;
  /** Topic-tree node id (src/data/topicTree.ts), or null. */
  node?: string | null;
  /** The database pool, e.g. "grade5", "ch06". */
  topicId?: string | null;
  subTopic?: string | null;
  difficulty?: string | null;
  questionText?: string | null;
  questionLatex?: string | null;
  options?: Array<{ id?: string; text?: string | null }> | null;
  correctAnswer?: string | null;
  hints?: Array<string | null> | null;
  stepByStep?: unknown[] | null;
  misconceptions?: { [key: string]: string | null | undefined } | null;
  source?: string | null;
  year?: number | null;
  questionNumber?: number | null;
}

/** The columns of `Question` the bank provides. */
export interface BankContent {
  topicId: string;
  subTopic: string;
  difficulty: string;
  questionText: string;
  questionLatex: string;
  option1: string;
  option2: string;
  option3: string;
  option4: string;
  correctAnswer: string;
  hint1: string;
  hint2: string;
  hint3: string;
  /** JSON text of the steps array. */
  stepByStep: string;
  misconceptionA: string;
  misconceptionB: string;
  misconceptionC: string;
  misconceptionD: string;
  source: string;
  year: number | null;
  questionNumber: number | null;
}

/** One bank question as a row of the `Question` table. */
export interface BankRow extends BankContent {
  id: string;
  nodeId: string | null;
}

/** A database row written back in the bank's shape (the export). */
export interface ExportedBankQuestion {
  id: string;
  node: null;
  topicId: string;
  subTopic: string;
  difficulty: string;
  questionText: string;
  questionLatex: string;
  options: Array<{ id: string; text: string }>;
  correctAnswer: string;
  hints: string[];
  stepByStep: unknown[];
  misconceptions: { A: string; B: string; C: string; D: string };
  source: string;
  year?: number;
  questionNumber?: number;
}

export interface BankFileInfo {
  file: string;
  grade: string;
  count: number;
}

export interface LoadedBank {
  /** False when data/bank does not exist. */
  exists: boolean;
  dir: string;
  files: BankFileInfo[];
  questions: BankQuestion[];
  /** The file each question came from, same order as `questions`. */
  fileOf: string[];
}

export interface BankCheck {
  rows: BankRow[];
  /** The first problems found, as readable lines. */
  problems: string[];
  /** How many problems there are in all. */
  problemCount: number;
  notes: { emptyOption: number; poolRemapped: number; noNode: number };
}

export const BANK_TOPICS: Array<{ id: string; name: string; chapterNumber: string }>;
export const BANK_TOPIC_IDS: string[];
export const CONTENT_COLUMNS: Array<keyof BankContent>;

export function cleanText(value: unknown): string;
export function topicIdFromQuestionId(questionId: string): string;
export function resolveTopicId(questionId: string, rawTopicId: string | null | undefined, validIds?: Set<string>): string;
export function bankQuestionToRow(q: BankQuestion, validIds?: Set<string>): BankRow;
export function rowToBankQuestion(row: BankContent & { id: string }): ExportedBankQuestion;
export function bankDir(rootDir?: string): string;
export function loadBank(rootDir?: string): LoadedBank;
export function checkBank(
  questions: BankQuestion[],
  opts?: { validIds?: Set<string>; fileOf?: string[] },
): BankCheck;
