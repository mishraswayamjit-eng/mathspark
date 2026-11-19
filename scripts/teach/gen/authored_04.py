"""Lessons for the Grade 5 questions listed in data/bank-import/g5/lessons-ids-4.json.

    python -X utf8 scripts/teach/gen/authored_04.py

Writes data/teach/parts/authored-04.json. Every lesson is written by hand, one per question,
in the helper modules named below.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

MODULES = ["authored_04_a", "authored_04_b", "authored_04_c", "authored_04_d",
           "authored_04_e", "authored_04_f", "authored_04_g"]


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "g5", "lessons-ids-4.json"), encoding="utf-8") as f:
        ids = json.load(f)

    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).LESSONS.items():
            assert qid in ids, "%s: %s is not in the list" % (name, qid)
            assert qid not in part, "%s: %s has two lessons" % (name, qid)
            part[qid] = lesson

    part = {qid: part[qid] for qid in ids if qid in part}
    missing = [qid for qid in ids if qid not in part]
    out = os.path.join(ROOT, "data", "teach", "parts", "authored-04.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; no lesson yet for %d" % (len(part), len(missing)))
    for qid in (missing if len(missing) <= 12 else []):
        print("  missing", qid)


if __name__ == "__main__":
    main()
