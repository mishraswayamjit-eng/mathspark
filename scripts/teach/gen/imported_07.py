"""Lessons for batch 07 of the imported Grade 5 questions (equations). Writes data/teach/parts/imported-07.json.

    python -X utf8 scripts/teach/gen/imported_07.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imported_07_lib import BATCH, PART  # noqa: E402

MODULES = ["imported_07_a", "imported_07_b", "imported_07_c", "imported_07_d", "imported_07_e"]


def main():
    with io.open(BATCH, encoding="utf-8") as f:
        batch = [q["id"] for q in json.load(f)]
    lessons = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py")):
            continue
        mod = __import__(name)
        for qid, script in mod.LESSONS.items():
            if qid not in batch:
                sys.exit("%s: %s is not in this batch" % (name, qid))
            if qid in lessons:
                sys.exit("%s: %s is written twice" % (name, qid))
            lessons[qid] = script
    out = {qid: lessons[qid] for qid in batch if qid in lessons}
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [qid for qid in batch if qid not in lessons]
    print("wrote %d lessons of %d; %d not written" % (len(out), len(batch), len(missing)))
    for qid in missing:
        print("  no lesson: %s" % qid)


if __name__ == "__main__":
    main()
