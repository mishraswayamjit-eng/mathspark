"""Lessons for the imported batch 05 (data/bank-import/lessons/in-05.json).

    python -X utf8 scripts/teach/gen/imported_05.py

Writes data/teach/parts/imported-05.json. The lessons themselves are in the
imported_05_*.py files beside this one; each has a LESSONS dict keyed by question id.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from imported_05_lib import PART, batch  # noqa: E402

MODULES = ["imported_05_counting", "imported_05_factors", "imported_05_money",
           "imported_05_shop", "imported_05_decimals_a", "imported_05_decimals_b"]

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
                sys.exit("%s: %s is not in batch 05" % (name, qid))
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
    for qid in missing[:6]:
        print("  to write: %s" % qid)


if __name__ == "__main__":
    main()
