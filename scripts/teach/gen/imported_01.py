"""Lessons for the imported batch 01 (algebraic expressions; angles and lines).

    python -X utf8 scripts/teach/gen/imported_01.py

Reads data/bank-import/lessons/in-01.json for the list of question ids, gathers the
lessons written in the imported_01_*.py files beside this one, and writes
data/teach/parts/imported-01.json. Then check with:

    python -X utf8 scripts/teach/validate.py --part imported-01
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from imported_01_lib import BATCH, PART  # noqa: E402

MODULES = ["imported_01_algebra_a", "imported_01_algebra_b", "imported_01_algebra_c", "imported_01_angles_a",
           "imported_01_angles_b", "imported_01_angles_c", "imported_01_angles_d", "imported_01_angles_e"]

# Questions deliberately left without a lesson: id -> reason.
LEFT_OUT = {}


def main():
    with io.open(BATCH, encoding="utf-8") as f:
        batch = [q["id"] for q in json.load(f)]
    lessons = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        mod = importlib.import_module(name)
        for qid, script in mod.LESSONS.items():
            if qid in lessons:
                sys.exit("two lessons for %s" % qid)
            if qid not in batch:
                sys.exit("%s is not in this batch (%s)" % (qid, name))
            lessons[qid] = script
    out = {qid: lessons[qid] for qid in batch if qid in lessons}
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [qid for qid in batch if qid not in lessons and qid not in LEFT_OUT]
    for qid, script in out.items():
        for beat in script["beats"]:
            if len(beat["say"]) > 240:
                print("  long say (%d) in %s: %s..." % (len(beat["say"]), qid[-12:], beat["say"][:50]))
    print("wrote %d lessons of %d to %s" % (len(out), len(batch), os.path.relpath(PART)))
    if missing:
        print("  no lesson yet for %d: %s" % (len(missing), ", ".join(q[-12:] for q in missing)))
    for qid, why in LEFT_OUT.items():
        print("  left out: %s (%s)" % (qid, why))


if __name__ == "__main__":
    main()
