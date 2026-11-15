"""List Grade 5 questions whose hints or steps need fixing, by kind of problem.

    python -X utf8 scripts/fixes/find.py                          # counts by problem and source
    python -X utf8 scripts/fixes/find.py --ids --prefix EXT_G5_WS_B3   # the questions, one line each
    python -X utf8 scripts/fixes/find.py --ids --problem thinking

Problems found by rule (a question can have several):
  generic      a hint is boilerplate that says nothing about the question
  thinking     a hint or step thinks aloud ("hmm", "wait", "let me recheck")
  filler       a step is filler ("The answer is option B", "Apply the relevant formula")
  false-sum    a sum written out in a hint or step is not true
  gives-away   a hint states the answer
  empty-hint   fewer than three hints
  one-step     fewer than two steps of its own
  same-options two answer choices are identical
"Already fixed" means a part file in data/question-fixes/parts has an entry for it.
This cannot spot a hint that belongs to a different question, or a wrong answer key: those need reading.
"""
import argparse
import collections
import glob
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check import FILLER, GENERIC, PARTS, THINKING, answer_numbers, false_arithmetic, load_seed, numbers_in, option_texts  # noqa: E402


def problems_of(q):
    found = []
    hints = [h for h in (q.get("hints") or []) if isinstance(h, str)]
    steps = [s.get("text", "") for s in (q.get("stepByStep") or [])]
    if any(any(g in h.lower() for g in GENERIC) for h in hints):
        found.append("generic")
    if any(THINKING.search(t) for t in hints + steps):
        found.append("thinking")
    if any(FILLER.search(t) for t in steps):
        found.append("filler")
    if any(false_arithmetic(t) for t in hints + steps):
        found.append("false-sum")
    giveaway = answer_numbers(q)
    if giveaway and any(numbers_in(h) & giveaway for h in hints):
        found.append("gives-away")
    if len([h for h in hints if h.strip()]) < 3:
        found.append("empty-hint")
    if 0 < len(steps) < 2:
        found.append("one-step")
    if len(set(option_texts(q))) < len(option_texts(q)):
        found.append("same-options")
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--ids", action="store_true", help="list the questions")
    parser.add_argument("--prefix", help="only question ids starting with this")
    parser.add_argument("--problem", help="only this problem")
    parser.add_argument("--todo", action="store_true", help="leave out questions that already have a fix")
    args = parser.parse_args()

    questions = load_seed()
    fixed = set()
    for path in glob.glob(os.path.join(PARTS, "*.json")):
        with io.open(path, encoding="utf-8") as f:
            fixed |= set(json.load(f))

    by_problem = collections.Counter()
    by_source = collections.defaultdict(collections.Counter)
    rows = []
    for qid in sorted(questions):
        q = questions[qid]
        if args.prefix and not qid.startswith(args.prefix):
            continue
        found = problems_of(q)
        if args.problem:
            found = [p for p in found if p == args.problem]
        if not found or (args.todo and qid in fixed):
            continue
        rows.append((qid, found))
        for p in found:
            by_problem[p] += 1
            by_source[q.get("source", "")][p] += 1

    if args.ids:
        for qid, found in rows:
            print("%-36s %-9s %-34s %s" % (qid, "fixed" if qid in fixed else "", ",".join(found), questions[qid]["questionText"][:70].replace("\n", " ")))
    print("%d questions with problems (%d already fixed)" % (len(rows), sum(1 for qid, _ in rows if qid in fixed)))
    for p, n in by_problem.most_common():
        print("  %-13s %d" % (p, n))
    if not args.ids:
        for src in sorted(by_source):
            print("  %-28s %s" % (src, dict(by_source[src])))


if __name__ == "__main__":
    main()
