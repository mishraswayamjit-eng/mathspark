"""Extra checks on the built part that the checker does not make.

    python -X utf8 scripts/teach/gen/g4_gr4_algebra_audit.py

  - a board mark must land on the thing it means: a number target must be a whole number on the line
    (not the 5 inside 15), and a single-letter target must not be a letter inside a word;
  - the right choice of an ask should not always sit in the same slot;
  - how long the lessons are, and how many asks they have.
"""
import collections
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_algebra.json")


def position(line, target):
    nth = target.get("nth", 1)
    i = -1
    for _ in range(nth):
        i = line.find(target["text"], i + 1)
    return i


def targets_of(op):
    k = op["op"]
    if k == "arc":
        return [op["from"]] + op["to"]
    if k in ("strike", "note", "mark"):
        return [op["target"]]
    if k == "group":
        return op["targets"]
    return []


def main():
    with io.open(OUT, encoding="utf-8") as f:
        part = json.load(f)
    problems = []
    slots = collections.Counter()
    beats = collections.Counter()
    asks = collections.Counter()
    for qid, script in part.items():
        lines = {}
        n_asks = 0
        for b, beat in enumerate(script["beats"]):
            for op in beat.get("board", []):
                if op["op"] == "write":
                    lines[op["id"]] = op["text"]
                    continue
                if op["op"] == "clear":
                    lines = {}
                    continue
                for t in targets_of(op):
                    line = lines[op["line"]]
                    text = t["text"]
                    i = position(line, t)
                    before = line[i - 1] if i > 0 else " "
                    after = line[i + len(text)] if i + len(text) < len(line) else " "
                    if text[0].isdigit() and before.isdigit():
                        problems.append("%s beat %d: %r lands inside a longer number on \"%s\"" % (qid, b + 1, text, line))
                    if text[-1].isdigit() and after.isdigit():
                        problems.append("%s beat %d: %r lands inside a longer number on \"%s\"" % (qid, b + 1, text, line))
                    if re.fullmatch(r"[A-Za-z]", text) and (before.isalpha() or after.isalpha()):
                        problems.append("%s beat %d: letter %r lands inside a word on \"%s\"" % (qid, b + 1, text, line))
            ask = beat.get("ask")
            if ask:
                n_asks += 1
                if ask["kind"] == "choose":
                    slots[(len(ask["choices"]), ask["answer"])] += 1
        beats[len(script["beats"])] += 1
        asks[n_asks] += 1
    for p in problems:
        print("PROBLEM  " + p)
    print("%d lessons, %d mark problems" % (len(part), len(problems)))
    print("beats per lesson:", dict(sorted(beats.items())))
    print("asks per lesson:", dict(sorted(asks.items())))
    print("right choice (choices, slot):", dict(sorted(slots.items())))


if __name__ == "__main__":
    main()
