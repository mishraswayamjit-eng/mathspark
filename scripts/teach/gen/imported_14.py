"""Lessons for data/bank-import/lessons/in-14.json (place value; three profit-and-loss stories).

    python -X utf8 scripts/teach/gen/imported_14.py

Writes data/teach/parts/imported-14.json.
  imported_14_pairs.py     two values from one number, then subtract, add or divide (one builder)
  imported_14_extremes.py  greatest and smallest numbers with so many digits (one builder)
  imported_14_hand_a.py    single place values, clue puzzles, even numbers
  imported_14_hand_b.py    numbers formed from given digits; profit and loss
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

MODULES = ["imported_14_pairs", "imported_14_extremes", "imported_14_hand_a", "imported_14_hand_b"]

# Questions left out on purpose (id -> reason). None in this batch.
LEFT_OUT = {}


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-14.json"), encoding="utf-8") as f:
        batch = {q["id"]: q for q in json.load(f)}

    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        mod = importlib.import_module(name)
        for qid, lesson in mod.LESSONS.items():
            assert qid in batch, "not in the batch: %s" % qid
            assert qid not in part, "two lessons for %s" % qid
            part[qid] = lesson

    ordered = {qid: part[qid] for qid in batch if qid in part}
    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-14.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(ordered), len(LEFT_OUT), len(missing)))
    for qid in missing:
        print("  missing", qid)
    for qid, s in ordered.items():
        for i, beat in enumerate(s["beats"]):
            if len(beat["say"]) > 240:
                print("  too long", qid, i, len(beat["say"]))


if __name__ == "__main__":
    main()
