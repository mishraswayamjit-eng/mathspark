// Make the database mirror the question bank (data/bank).
//
//   node scripts/bank/sync.mjs --check     no database: read and check the bank
//   node scripts/bank/sync.mjs             the sync (production builds only)
//
// The production build runs the sync after `prisma db push` and before
// `next build` (see vercel.json). A failure exits non-zero, which stops the
// deploy and leaves the previous deployment live.
//
// What the sync does:
//   - a question in the bank and not in the database is created;
//   - a question whose content differs is updated to the bank's content;
//   - a question whose topic-tree node differs gets the bank's node;
//   - a question in the database and not in the bank is counted and listed.
//     It is marked `retired` only when BANK_RETIRE_MISSING=on. Nothing is ever
//     deleted: children's recorded answers point at these rows.
//
// Flags and switches:
//   --check           check the bank files only; never opens the database
//   --dry-run         read the database and print the plan, write nothing
//   --force           run outside a production build (VERCEL_ENV !== production)
//   --force-content   allow more than 3,000 content updates in one run
//   --force-retire    allow retiring more than a fifth of the database
//   BANK_SYNC=off             skip the sync entirely (an escape hatch for a deploy)
//   BANK_RETIRE_MISSING=on    mark database-only questions as retired
//
// Plain Node, no dependencies beyond @prisma/client and Node itself.

import path from 'path';
import { fileURLToPath } from 'url';
import { loadBank, checkBank, CONTENT_COLUMNS } from './bankRows.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

const READ_PAGE = 5000;            // rows per database read
const CREATE_CHUNK = 500;          // rows per createMany (22 columns each)
const ID_CHUNK = 2000;             // ids per grouped updateMany
const GROUPED_CONCURRENCY = 4;     // grouped statements in flight
const ROW_CONCURRENCY = 8;         // per-row updates in flight
const MAX_CONTENT_CHANGES = 3000;  // more than this: stop, a human should look
const MAX_RETIRE_SHARE = 0.2;      // refuse to retire more than this share of the database
const RETRIES = 4;

// Questions the app creates in code (the seed route's interactive set), not
// from the bank. They are never retired for being absent from the bank.
const CODE_SEEDED_SOURCES = ['interactive_seed'];

const TAG = '[bank-sync]';
const say = (text) => console.log(TAG + ' ' + text);
const n = (value) => Number(value).toLocaleString('en-US');

const KNOWN_FLAGS = ['--check', '--dry-run', '--force', '--force-content', '--force-retire'];
const flags = process.argv.slice(2);
const has = (flag) => flags.indexOf(flag) !== -1;

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------

function chunks(list, size) {
  const out = [];
  for (let i = 0; i < list.length; i += size) out.push(list.slice(i, i + size));
  return out;
}

/** Run the tasks (functions returning promises) a few at a time, in order. */
async function runPool(tasks, limit) {
  let next = 0;
  async function worker() {
    while (next < tasks.length) {
      const mine = next++;
      await tasks[mine]();
    }
  }
  const workers = [];
  for (let i = 0; i < Math.min(limit, tasks.length); i++) workers.push(worker());
  await Promise.all(workers);
}

function isTransient(err) {
  const code = err && err.code ? String(err.code) : '';
  if (['P1001', 'P1002', 'P1008', 'P1017', 'P2024'].indexOf(code) !== -1) return true;
  const name = err && err.name ? String(err.name) : '';
  if (name === 'PrismaClientInitializationError') return true;
  const message = err && err.message ? String(err.message) : String(err);
  return /ECONNRESET|ETIMEDOUT|ECONNREFUSED|EPIPE|EAI_AGAIN|Can't reach database server|Connection (terminated|closed|reset)|Server has closed the connection|Timed out|socket hang up/i.test(message);
}

/** A database call, retried a few times when the connection drops. Every call here is safe to repeat. */
async function withRetry(label, fn) {
  for (let attempt = 1; ; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt >= RETRIES || !isTransient(err)) throw err;
      const waitMs = 1500 * attempt * attempt;
      say(label + ': connection problem, trying again in ' + (waitMs / 1000) + 's (attempt ' + attempt + ' of ' + RETRIES + ')');
      await new Promise((resolve) => setTimeout(resolve, waitMs));
    }
  }
}

function tallyText(counts) {
  const keys = Object.keys(counts).sort((a, b) => counts[b] - counts[a] || (a < b ? -1 : 1));
  return keys.length === 0 ? 'none' : keys.map((k) => k + ' ' + n(counts[k])).join(', ');
}

// ---------------------------------------------------------------------------
// Reading and checking the bank (no database)
// ---------------------------------------------------------------------------

/** Returns { code } to stop with that exit code, or { rows } to carry on. */
function readBank(label) {
  let bank;
  try {
    bank = loadBank(ROOT);
  } catch (err) {
    say(label + ' FAILED: ' + (err && err.message ? err.message : String(err)));
    return { code: 1 };
  }
  if (!bank.exists) {
    say(label + ': no bank directory yet (data/bank is missing): nothing to do');
    return { code: 0 };
  }
  if (bank.questions.length === 0) {
    say(label + ' FAILED: data/bank exists but holds no questions (expected data/bank/gradeN/*.json)');
    return { code: 1 };
  }

  const check = checkBank(bank.questions, { fileOf: bank.fileOf });
  const summary = n(bank.questions.length) + ' questions in ' + n(bank.files.length) + ' files, '
    + n(check.problemCount) + ' problems'
    + ' (' + n(check.notes.noNode) + ' with no topic node, '
    + n(check.notes.emptyOption) + ' with an empty option, '
    + n(check.notes.poolRemapped) + ' with a remapped pool)';
  if (check.problemCount > 0) {
    say(label + ' FAILED: ' + summary);
    for (let i = 0; i < check.problems.length; i++) say('  ' + check.problems[i]);
    if (check.problemCount > check.problems.length) say('  … and ' + n(check.problemCount - check.problems.length) + ' more');
    return { code: 1 };
  }
  say(label + ' ok: ' + summary);
  return { rows: check.rows };
}

// ---------------------------------------------------------------------------
// The sync
// ---------------------------------------------------------------------------

let prisma = null;

async function openDatabase() {
  let mod;
  try {
    mod = await import('@prisma/client');
  } catch (err) {
    throw new Error('could not load @prisma/client (has `prisma generate` run?): ' + (err && err.message ? err.message : String(err)));
  }
  const PrismaClient = mod.PrismaClient || (mod.default && mod.default.PrismaClient);
  if (!PrismaClient) throw new Error('@prisma/client has no PrismaClient (has `prisma generate` run?)');
  return new PrismaClient();
}

async function sync(bankRows) {
  const started = Date.now();
  const dryRun = has('--dry-run');
  const retireMissing = process.env.BANK_RETIRE_MISSING === 'on';

  if (!process.env.DATABASE_URL) throw new Error('DATABASE_URL is not set');
  prisma = await openDatabase();

  const bankById = new Map();
  for (let i = 0; i < bankRows.length; i++) bankById.set(bankRows[i].id, bankRows[i]);

  // ── Read the database, comparing as we go ────────────────────────────────
  const select = { id: true, nodeId: true, retired: true };
  for (let i = 0; i < CONTENT_COLUMNS.length; i++) select[CONTENT_COLUMNS[i]] = true;

  const same = (a, b) => (a === undefined || a === null ? null : a) === (b === undefined || b === null ? null : b);

  const inDatabase = new Set();
  const contentChanged = [];           // bank rows to write in full
  const changedColumns = {};           // column → how many rows differ in it
  const nodeOnly = new Map();          // node (or null) → ids
  let nodeOnlyCount = 0;
  let unchanged = 0;
  const unretire = [];                 // in the bank, retired in the database, content the same
  const dbOnlyBySource = {};
  const dbOnlyByPool = {};
  let dbOnlyTotal = 0;
  let dbOnlyAlreadyRetired = 0;
  let dbOnlyCodeSeeded = 0;
  const retireCandidates = [];
  let databaseTotal = 0;
  let readStatements = 0;

  let after = null;
  for (;;) {
    const cursor = after;
    const page = await withRetry('reading questions', () => prisma.question.findMany({
      where: cursor === null ? {} : { id: { gt: cursor } },
      orderBy: { id: 'asc' },
      take: READ_PAGE,
      select,
    }));
    readStatements++;

    for (let i = 0; i < page.length; i++) {
      const row = page[i];
      databaseTotal++;
      const bank = bankById.get(row.id);

      if (!bank) {
        dbOnlyTotal++;
        const source = row.source || '(none)';
        dbOnlyBySource[source] = (dbOnlyBySource[source] || 0) + 1;
        dbOnlyByPool[row.topicId] = (dbOnlyByPool[row.topicId] || 0) + 1;
        if (CODE_SEEDED_SOURCES.indexOf(row.source) !== -1) dbOnlyCodeSeeded++;
        else if (row.retired) dbOnlyAlreadyRetired++;
        else retireCandidates.push(row.id);
        continue;
      }

      inDatabase.add(row.id);
      let differs = false;
      for (let c = 0; c < CONTENT_COLUMNS.length; c++) {
        const col = CONTENT_COLUMNS[c];
        if (!same(row[col], bank[col])) {
          differs = true;
          changedColumns[col] = (changedColumns[col] || 0) + 1;
        }
      }
      if (differs) {
        contentChanged.push(bank); // written in full, which also sets the node and un-retires
      } else {
        if (!same(row.nodeId, bank.nodeId)) {
          const list = nodeOnly.get(bank.nodeId);
          if (list) list.push(row.id); else nodeOnly.set(bank.nodeId, [row.id]);
          nodeOnlyCount++;
        } else if (!row.retired) {
          unchanged++;
        }
        if (row.retired) unretire.push(row.id);
      }
    }

    if (page.length < READ_PAGE) break;
    after = page[page.length - 1].id;
  }

  const created = [];
  for (let i = 0; i < bankRows.length; i++) if (!inDatabase.has(bankRows[i].id)) created.push(bankRows[i]);

  // ── Say what was found ───────────────────────────────────────────────────
  say('database: ' + n(databaseTotal) + ' questions (read in ' + readStatements + ' statements)');
  say('plan: ' + n(created.length) + ' new · ' + n(contentChanged.length) + ' changed · '
    + n(nodeOnlyCount) + ' topic node only · ' + n(unretire.length) + ' to un-retire · '
    + n(unchanged) + ' unchanged · ' + n(dbOnlyTotal) + ' only in the database');
  if (contentChanged.length > 0) {
    say('changed columns: ' + tallyText(changedColumns));
    say('changed, for example: ' + contentChanged.slice(0, 8).map((r) => r.id).join(', '));
  }
  if (dbOnlyTotal > 0) {
    say('only in the database, by source: ' + tallyText(dbOnlyBySource));
    say('only in the database, by pool: ' + tallyText(dbOnlyByPool));
    say('only in the database: ' + n(dbOnlyAlreadyRetired) + ' already retired · '
      + n(dbOnlyCodeSeeded) + ' created by the app in code (never retired) · '
      + n(retireCandidates.length) + ' live');
  }

  // ── Safety stops: all before the first write ─────────────────────────────
  if (contentChanged.length > MAX_CONTENT_CHANGES && !has('--force-content')) {
    throw new Error(n(contentChanged.length) + ' questions differ in content between the bank and the database '
      + '(the limit is ' + n(MAX_CONTENT_CHANGES) + '). Nothing was written. The bank and the database have diverged: '
      + 'look at the changed columns above. To accept the bank\'s content, run with --force-content; '
      + 'to deploy without syncing, set BANK_SYNC=off.');
  }

  if (created.length > 0 || contentChanged.length > 0) {
    const topics = await withRetry('reading pools', () => prisma.topic.findMany({ select: { id: true } }));
    readStatements++;
    const known = new Set(topics.map((t) => t.id));
    const missing = {};
    const needing = created.concat(contentChanged);
    for (let i = 0; i < needing.length; i++) {
      if (!known.has(needing[i].topicId)) missing[needing[i].topicId] = (missing[needing[i].topicId] || 0) + 1;
    }
    if (Object.keys(missing).length > 0) {
      throw new Error('the bank uses pools that are not in the Topic table: ' + tallyText(missing)
        + '. Nothing was written. Pools are created by the seed screen (/seed, "Seed Questions"): run it once, then deploy again.');
    }
  }

  if (retireMissing && retireCandidates.length > MAX_RETIRE_SHARE * databaseTotal && !has('--force-retire')) {
    throw new Error('BANK_RETIRE_MISSING=on would retire ' + n(retireCandidates.length) + ' of ' + n(databaseTotal)
      + ' questions, more than a fifth of the database. Nothing was written. Check the bank is complete; '
      + 'to go ahead anyway, run with --force-retire.');
  }

  if (dryRun) {
    say('dry run: nothing written');
    return;
  }

  // ── Write ────────────────────────────────────────────────────────────────
  let writeStatements = 0;

  // 1. New questions.
  let createdCount = 0;
  const createChunks = chunks(created, CREATE_CHUNK);
  for (let i = 0; i < createChunks.length; i++) {
    const result = await withRetry('creating questions', () => prisma.question.createMany({ data: createChunks[i], skipDuplicates: true }));
    writeStatements++;
    createdCount += result.count;
  }

  // 2. Topic node only: one statement per node per 2,000 ids.
  const nodeTasks = [];
  nodeOnly.forEach((ids, node) => {
    const idChunks = chunks(ids, ID_CHUNK);
    for (let i = 0; i < idChunks.length; i++) {
      nodeTasks.push(async () => {
        await withRetry('setting topic nodes', () => prisma.question.updateMany({ where: { id: { in: idChunks[i] } }, data: { nodeId: node } }));
        writeStatements++;
      });
    }
  });
  await runPool(nodeTasks, GROUPED_CONCURRENCY);

  // 3. Content: one statement per question (few, or it stopped above).
  const contentTasks = contentChanged.map((row) => async () => {
    const data = { nodeId: row.nodeId, retired: false };
    for (let c = 0; c < CONTENT_COLUMNS.length; c++) data[CONTENT_COLUMNS[c]] = row[CONTENT_COLUMNS[c]];
    await withRetry('updating ' + row.id, () => prisma.question.update({ where: { id: row.id }, data, select: { id: true } }));
    writeStatements++;
  });
  await runPool(contentTasks, ROW_CONCURRENCY);

  // 4. Back in the bank: un-retire.
  const unretireChunks = chunks(unretire, ID_CHUNK);
  for (let i = 0; i < unretireChunks.length; i++) {
    await withRetry('un-retiring', () => prisma.question.updateMany({ where: { id: { in: unretireChunks[i] } }, data: { retired: false } }));
    writeStatements++;
  }

  // 5. Not in the bank: retire, only when asked. Never delete.
  let retiredCount = 0;
  if (retireMissing) {
    const retireChunks = chunks(retireCandidates, ID_CHUNK);
    for (let i = 0; i < retireChunks.length; i++) {
      const result = await withRetry('retiring', () => prisma.question.updateMany({ where: { id: { in: retireChunks[i] } }, data: { retired: true } }));
      writeStatements++;
      retiredCount += result.count;
    }
  }

  say('done in ' + ((Date.now() - started) / 1000).toFixed(1) + 's: '
    + n(createdCount) + ' created · ' + n(contentChanged.length) + ' updated · '
    + n(nodeOnlyCount) + ' topic nodes set · ' + n(unretire.length) + ' un-retired · '
    + (retireMissing
      ? n(retiredCount) + ' retired'
      : '0 retired (BANK_RETIRE_MISSING is not on; ' + n(retireCandidates.length) + ' live questions are only in the database)')
    + ' · ' + n(writeStatements) + ' write statements');
}

// ---------------------------------------------------------------------------
// Entry
// ---------------------------------------------------------------------------

async function main() {
  for (let i = 0; i < flags.length; i++) {
    if (KNOWN_FLAGS.indexOf(flags[i]) === -1) {
      say('unknown option ' + flags[i] + ' (known: ' + KNOWN_FLAGS.join(', ') + ')');
      return 1;
    }
  }

  if (has('--check')) {
    const checked = readBank('bank check');
    return checked.rows ? 0 : checked.code;
  }

  if (process.env.BANK_SYNC === 'off') {
    say('BANK_SYNC=off: sync skipped');
    return 0;
  }
  if (process.env.VERCEL_ENV !== 'production' && !has('--force')) {
    say('not a production build: sync skipped (VERCEL_ENV=' + (process.env.VERCEL_ENV || 'not set') + ')');
    return 0;
  }

  const checked = readBank('bank');
  if (!checked.rows) return checked.code;

  await sync(checked.rows);
  return 0;
}

let exitCode = 1;
try {
  exitCode = await main();
} catch (err) {
  say('FAILED: ' + (err && err.message ? err.message : String(err)));
  exitCode = 1;
} finally {
  if (prisma) {
    try { await prisma.$disconnect(); } catch (err) { /* the result is already decided */ }
  }
}
process.exitCode = exitCode;
// Nothing should be left running; if something is, do not hang the build.
setTimeout(() => process.exit(exitCode), 5000).unref();
