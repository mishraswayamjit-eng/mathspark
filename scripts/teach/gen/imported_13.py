"""Lessons for the imported batch 13 (data/bank-import/lessons/in-13.json).

    python -X utf8 scripts/teach/gen/imported_13.py

Writes data/teach/parts/imported-13.json. The lessons themselves are in the
imported_13_*.py files beside this one; each has a LESSONS dict keyed by question id.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from imported_13_lib import PART, batch  # noqa: E402

MODULES = ["imported_13_money", "imported_13_money_b", "imported_13_place", "imported_13_place_b",
           "imported_13_puzzle"]

# Questions deliberately left without a lesson: id -> reason.
LEFT_OUT = {}


def main():
    questions = batch()
    lessons = {}
    for name in MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
            continue
        for qid, script in mod.LESSONS.items():
            if qid not in questions:
                sys.exit("%s: %s is not in batch 13" % (name, qid))
            if qid in lessons:
                sys.exit("%s: %s has two lessons" % (name, qid))
            lessons[qid] = script
    ordered = {qid: lessons[qid] for qid in questions if qid in lessons}
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [qid for qid in questions if qid not in lessons and qid not in LEFT_OUT]
    print("wrote %d lessons of %d; %d left out on purpose; %d still to write" % (
        len(ordered), len(questions), len(LEFT_OUT), len(missing)))
    for qid in missing[:8]:
        print("  to write: %s" % qid)


if __name__ == "__main__":
    main()
