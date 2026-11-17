"""Lessons for data/bank-import/lessons/in-11.json (addition and subtraction;
multiplication and division stories).

    python -X utf8 scripts/teach/gen/imported_11.py

Writes data/teach/parts/imported-11.json. Every question is a one-off, so each
has its own lesson; the questions that come in pairs share a builder that is fed
each question's numbers (imported_11_a.py). The rest are written by hand in
imported_11_b.py (addition and subtraction) and imported_11_c.py / _d.py
(multiplication and division).
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

MODULES = ["imported_11_a", "imported_11_b", "imported_11_c", "imported_11_d"]

# Questions left out on purpose (id -> reason). None in this batch.
LEFT_OUT = {}


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-11.json"), encoding="utf-8") as f:
        batch = [q["id"] for q in json.load(f)]

    lessons = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).LESSONS.items():
            assert qid in batch, "not in this batch: %s" % qid
            assert qid not in lessons, "two lessons for %s" % qid
            lessons[qid] = lesson

    part = {qid: lessons[qid] for qid in batch if qid in lessons}  # batch order
    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    long = [(qid, i, len(b["say"])) for qid, s in part.items() for i, b in enumerate(s["beats"]) if len(b["say"]) > 240]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-11.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(part), len(LEFT_OUT), len(missing)))
    for qid in missing:
        print("  missing", qid)
    for qid, i, n in long:
        print("  too long", qid, i, n)


if __name__ == "__main__":
    main()
