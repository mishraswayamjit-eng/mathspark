# Narration for Grade 4, and for newly added Grade 5 questions

Read `scripts/speech/README.md` in full first. Everything it says about WHAT to write applies
here unchanged: the contract for an entry, what the checker enforces, and the whole section
"How to write for the ear". Only the file locations and commands differ, as below. Where
README.md says "Grade 5" or "age about 10", read Grade 4 and age about 9 for the Grade 4 work.

Your prompt tells you which of the two jobs you have.

## Job A: Grade 4, one or more topics

Grade 4 narration is kept one file per topic of the topic tree.

| What | Where |
|---|---|
| Your questions | `bank.load_bank(4)`, keeping those whose `node` is your topic id (see the snippet below) |
| Your output | `data/question-speech/parts-g4/<topic id>.json`: `{ "<question id>": entry }` for EVERY question of that topic |
| Your script | `scripts/speech/g4/<topic id>.py` (and helper files starting with that topic id). It writes the output file. |
| The checker | `python -X utf8 scripts/speech/validate.py --g4 <topic id>` |

    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    import common                                  # speak(), source_strings(), number_tokens(), bank
    questions = [q for q in common.bank.load_bank(4) if q.get("node") == "gr4_fractions"]
    src = common.source_strings(questions[0])      # {"q", "options", "hints", "steps"}: exactly what to narrate

`scripts/speech/show.py` only knows Grade 5; print what you need from your own script.

Each Grade 4 question has: the question, four options, three hints, and its worked steps. A step
may have a separate maths line (`latex`); as README.md says, you may say the numbers of the step's
text alone, or of its text followed by its maths line.

The Grade 4 bank holds real past exam questions (ids `PYQ_...`, `EXT_G4_FP_...`), worksheet
questions (`EXT_G4_WS...`), hand-written ones (`Q_CH...`, `Q_DH...`), newly written ones (`G4A_...`)
and generated families (`Q_CH..._V..`, `VAR...`, `BOOST...`, `PH3...`). Regular families deserve
carefully written rules; everything else deserves individual attention.

## Job B: the newly added Grade 5 questions

234 questions with ids starting `G5A_` were added to Grade 5 and have no narration yet.

| What | Where |
|---|---|
| Your questions | `[q for q in common.bank.load_bank(5) if q["id"].startswith("G5A_")]` |
| Your output | `data/bank-import/g5/speech-new.json`: `{ "<question id>": entry }` for every one |
| Your script | `scripts/speech/topics/g5_authored.py` (and helpers starting `g5_authored`) |
| The checker | `python -X utf8 scripts/speech/check_new.py data/bank-import/g5/speech-new.json` |

Do not edit the existing files in `data/question-speech/parts/`; your entries are merged into them afterwards.

## Working rules (both jobs)

- Use Read, Edit, Write, Grep, Glob, and Python only as plain single commands:
  `python -X utf8 <script path>` and the checker commands above. No `python -c`, no pipes, no `cd`,
  no `&&`, no `ls`, no other shell commands, no git. Nobody is watching: a command that needs
  permission will hang.
- Edit only your own script files and your own output file(s). Do not edit `common.py`,
  `validate.py`, anything under `data/bank/` or `src/`, or another writer's files.
- Work in small steps and keep your output file valid on disk at every stage, so nothing is lost
  if you are interrupted. Write the output early (rule-based first), then improve it.
- Passing the checker is the floor. Read your narration back as the voice would say it: at least
  60 questions in full across all the kinds in your topic, and every real past-paper question once.

## Your report

When your part passes the checker: how many questions are narrated and pass (it should be all of
them); roughly how many lines you wrote by hand against by rule; the notation rules you added;
the ids of questions whose SOURCE text is poor (garbled, filler, apparent mistakes) so they can be
repaired; and anything the checker forced you to say awkwardly.
