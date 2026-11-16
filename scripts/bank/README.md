# The question bank

`data/bank/` is the source of truth for every practice question: one file for each grade and topic. The database is filled from it at deploy time; every offline check (fixes, figures, narration, teach lessons, audits) reads it.

## Layout

    data/bank/
      _meta.json                 the bank's metadata; totalQuestions is kept true by the writer
      grade2/ … grade9/          one folder per grade
        gr5_fractions.json       one file per topic: the file name is the node id in src/data/topicTree.ts
        _unsorted.json           questions of that grade that belong to no topic
    src/data/bank/seedIds.json   every id in the bank, sorted (the admin topic audit reads it)

Every node in the tree has a file, and every grade has `_unsorted.json`, even when empty (`[` and `]` on two lines).

Each file is a JSON array with **one question per line**, sorted by `id`, UTF-8, compact, `\n` line ends, final newline:

    [
    {"id":"...","node":"gr5_fractions","topicId":"grade5","subTopic":"...","difficulty":"Medium","questionText":"...","questionLatex":"","options":[{"id":"A","text":"..."},…],"correctAnswer":"B","hints":["…","…","…"],"stepByStep":[{"step":1,"text":"…","latex":""}],"misconceptions":{"A":"…",…},"source":"..."},
    {"id":"...", ...}
    ]

- `node` is the question's topic: a node id from `src/data/topicTree.ts`, or `null` in `_unsorted.json`. It is explicit: nothing guesses it from `subTopic` any more.
- `topicId` is the database pool (`grade5`, `ch06`, …). It must be the node's `dbTopicId`.
- A question's grade is N for pool `gradeN`, and 4 for the Grade 4 chapter pools (`ch01-05` … `ch21`, `dh`).
- Keys come in the order `id`, `node`, then the rest.

## Rules

- Only `scripts/bank/bank.py` opens bank files. Scripts use `bank.load_bank()`, `bank.load_pool("grade5")`, `bank.load_by_id()`, `bank.save_bank(questions)`.
- `save_bank` checks every row first and writes nothing if one is not valid. It puts each question in the file of its grade and `node`, rewrites only files whose text changes, and keeps `_meta.json` and `seedIds.json` in step.
- Never write an answer by hand that has not been verified (see CLAUDE.md, Safety & Content Rules).

## Checks to run

After any change to the bank or to `src/data/topicTree.ts`:

    python -X utf8 scripts/bank/check.py

and, because they read the bank:

    python -X utf8 scripts/fixes/check.py
    python -X utf8 scripts/speech/validate.py
    python -X utf8 scripts/teach/validate.py
    python -X utf8 scripts/figures/validate.py

`check.py` exits non-zero with a list if: an id is used twice; a field is missing or of the wrong type; a question does not have exactly options A, B, C, D; `correctAnswer` is not one of them; `difficulty` is not Easy, Medium or Hard; `node` is not a node of the question's grade and pool; a question sits in the wrong file; a file is not sorted or not in the one-line-per-question form; a file or folder is missing or does not belong; `_meta.json` or `seedIds.json` disagrees with the bank.

## Change a question

Small edit (wording, a hint): edit its line in place, keep the form, run the checks. Grade 5 hints and steps are normally changed through a fix part instead (`scripts/fixes/README.md`), which `scripts/fixes/apply.py --write` writes into the bank.

Anything larger, from a script:

    import bank
    questions = bank.load_bank()
    q = bank.by_id(questions)["EXT_G5_FP_2021_015"]
    q["subTopic"] = "Grade 5 — Algebraic expressions"
    bank.save_bank(questions)

## Add a question

Add a row with every field above, a new unique `id`, and its `node` (`bank.assign_node(q)` proposes one from the `subTopic` label; `null` if none fits), then `bank.save_bank(questions + [q])`. By hand: add the line to the right file, keep the file sorted by `id`, then run `python -X utf8 scripts/bank/build_seed_ids.py` and the checks.

## Move a question to another topic

Set `node` to the new node id and call `save_bank`: the question moves to that node's file. By hand: cut the line, change `node`, paste it into the other file in id order. The node must be of the same grade and hold the question's `topicId`.

## Add a topic

1. Add the node to `src/data/topicTree.ts` (`id`, `grade`, `dbTopicId`, and a `subTopicKey` if it shares a `gradeN` pool).
2. Give it questions: set `node` to the new id on the questions that belong to it (for example those in the grade's `_unsorted.json` whose label the new key reaches: `bank.assign_node`), and call `bank.save_bank(questions)`. `save_bank` creates the new file, even if it is empty.
3. Run the checks. Removing or renaming a node works the same way: re-point its questions first, then `save_bank` removes the left-over file.

## How `node` was first assigned (`bank.assign_node`)

- Chapter pool (`ch06`, `dh`, …): the node whose `dbTopicId` is the pool.
- Shared pool (`grade5`, …): the node whose `subTopicKey` starts a word in the `subTopic` label (the old `matchesSubTopicKey` rule). No key matches: `null`. A node with no key on a shared pool (`gr4_ipm`) is never a catch-all.
- Several keys match: (1) keys in the head phrase (before a dash, colon, bracket or with/of/on/in/for/using) beat keys after it; (2) a subject key beats an operation key (`addition`, `multiplication`, `number`); (3) then the right-most key wins ("Fraction equations" is equations).

## Files here

- `bank.py`: the module. `check.py`: the validator. `build_seed_ids.py`: rewrites `seedIds.json` from the bank.
- `split.py`: the one-time migration from the old `data/mathspark_complete_seed.json`. It refuses to run once the bank exists.
- `sync.mjs`, `bankRows.mjs`: the app side's deploy-time load of the bank into the database (see those files).
