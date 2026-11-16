"""Check the question bank (data/bank/). Reads only; changes nothing. Exit 1 on any problem.

    python -X utf8 scripts/bank/check.py

Checks:
  rows    unique ids across the whole bank; every required field present and of the right
          type; exactly four options with ids A B C D; correctAnswer one of them; difficulty
          Easy, Medium or Hard; node null or a node of the question's grade (src/data/topicTree.ts)
          whose pool (dbTopicId) is the question's topicId;
  files   data/bank/ holds _meta.json and one folder per grade, and nothing else; each folder
          holds one file per tree node of that grade plus _unsorted.json, and nothing else;
          every question sits in the file of its grade and node; each file is sorted by id,
          one question per line, keys starting id, node, in the exact form bank.py writes;
  lists   _meta.json totalQuestions and src/data/bank/seedIds.json agree with the bank.
Plain Python 3 standard library only.
"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402


def rel(path):
    return os.path.relpath(path, bank.ROOT).replace(os.sep, "/")


def layout_problems():
    """Files and folders that should not be there, or are missing."""
    problems = []
    if not os.path.isdir(bank.BANK):
        return ["%s is missing: run scripts/bank/split.py" % rel(bank.BANK)]
    expected_dirs = set("grade%d" % g for g in bank.GRADES)
    for name in sorted(os.listdir(bank.BANK)):
        if name != "_meta.json" and name not in expected_dirs:
            problems.append("%s: not part of the bank" % rel(os.path.join(bank.BANK, name)))
    if not os.path.isfile(bank.META):
        problems.append("%s is missing" % rel(bank.META))
    for g in bank.GRADES:
        folder = bank.grade_dir(g)
        expected = set(n["id"] + ".json" for n in bank.tree_nodes(g)) | {bank.UNSORTED + ".json"}
        have = set(os.listdir(folder)) if os.path.isdir(folder) else set()
        for name in sorted(expected - have):
            problems.append("%s is missing (an empty file is '[' and ']' on two lines)" % rel(os.path.join(folder, name)))
        for name in sorted(have - expected):
            problems.append("%s: no node of Grade %d has this name" % (rel(os.path.join(folder, name)), g))
    return problems


def file_problems(path, grade):
    """(problems, rows) for one bank file."""
    name = rel(path)
    stem = os.path.splitext(os.path.basename(path))[0]
    try:
        text = bank.read_file(path)
    except UnicodeDecodeError as e:
        return ["%s: not UTF-8 (%s)" % (name, e)], []
    try:
        rows = json.loads(text)
    except ValueError as e:
        return ["%s: not valid JSON (%s)" % (name, e)], []
    if not isinstance(rows, list) or not all(isinstance(r, dict) and isinstance(r.get("id"), str) for r in rows):
        return ["%s: not a list of questions with ids" % name], []
    problems = []
    want_node = None if stem == bank.UNSORTED else stem
    for r in rows:
        if "node" in r and r["node"] != want_node:
            problems.append("%s: %s has node %r, so it belongs in %s" % (name, r["id"], r["node"], rel(bank.file_for(r)) if bank.grade_of(r.get("topicId")) else "?"))
        elif bank.grade_of(r.get("topicId")) not in (None, grade):
            problems.append("%s: %s has topicId %s, which is Grade %d" % (name, r["id"], r.get("topicId"), bank.grade_of(r.get("topicId"))))
        if list(r.keys())[:2] != ["id", "node"]:
            problems.append("%s: %s keys must start with id, node" % (name, r["id"]))
    ids = [r["id"] for r in rows]
    if ids != sorted(ids):
        problems.append("%s: not sorted by id (first out of place: %s)" % (
            name, next(b for a, b in zip(ids, ids[1:]) if b < a)))
    if "\r" in text:
        problems.append("%s: has Windows line ends; the bank uses \\n" % name)
    elif not problems and text != bank.file_text(rows):
        lines = text.split("\n")
        want = bank.file_text(rows).split("\n")
        at = next((i for i, (a, b) in enumerate(zip(lines, want)) if a != b), min(len(lines), len(want)))
        problems.append("%s: line %d is not in the bank's form (one question per line, compact, UTF-8 not \\u escapes, final newline)" % (name, at + 1))
    return problems, rows


def main():
    problems = layout_problems()
    questions = []
    files = 0
    for g in bank.GRADES:
        for path in bank.bank_files(g):
            files += 1
            found, rows = file_problems(path, g)
            problems += found
            questions += rows
    problems += bank.row_problems(questions)

    ids = sorted(q["id"] for q in questions)
    if os.path.isfile(bank.META):
        try:
            total = bank.load_meta().get("totalQuestions")
        except ValueError as e:
            total = "unreadable (%s)" % e
        if total != len(questions):
            problems.append("%s: totalQuestions is %s, the bank holds %d" % (rel(bank.META), total, len(questions)))
    if not os.path.isfile(bank.SEED_IDS):
        problems.append("%s is missing: run scripts/bank/build_seed_ids.py" % rel(bank.SEED_IDS))
    else:
        try:
            listed = bank.load_seed_ids()
        except ValueError:
            listed = None
        if listed != ids:
            extra = set(listed or []) - set(ids)
            missing = set(ids) - set(listed or [])
            problems.append("%s is not the bank's ids (%d missing, %d extra, or not sorted): run scripts/bank/build_seed_ids.py" % (
                rel(bank.SEED_IDS), len(missing), len(extra)))

    per_grade = collections.Counter(bank.grade_of(q.get("topicId")) for q in questions)
    unsorted = collections.Counter(bank.grade_of(q.get("topicId")) for q in questions if q.get("node") is None)
    for g in bank.GRADES:
        print("  grade%d  %5d questions, %5d unsorted, %2d files" % (g, per_grade[g], unsorted[g], len(bank.bank_files(g))))
    print("  bank    %5d questions, %5d unsorted, %2d files" % (len(questions), sum(unsorted.values()), files))
    if problems:
        print("%d PROBLEMS" % len(problems))
        for p in problems[:200]:
            print("  " + p)
        if len(problems) > 200:
            print("  ... and %d more" % (len(problems) - 200))
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
