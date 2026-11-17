"""Lessons for the imported batch 03 (58 one-off Grade 5 questions: area and perimeter, BODMAS).

    python -X utf8 scripts/teach/gen/imported_03.py

Writes data/teach/parts/imported-03.json. The lessons themselves are in
imported_03_a.py (story problems on area), imported_03_b.py (perimeter, textbook
chapter 19), imported_03_c.py (area, textbook chapter 20) and imported_03_d.py (BODMAS).
"""
import importlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imported_03_lib import PART, source_ids  # noqa: E402

MODULES = ["imported_03_a", "imported_03_b", "imported_03_c", "imported_03_d"]


def main():
    lessons = {}
    for name in MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
            continue
        for qid, script in mod.LESSONS.items():
            if qid in lessons:
                sys.exit("two lessons for %s" % qid)
            lessons[qid] = script
    wanted = source_ids()
    stray = [q for q in lessons if q not in wanted]
    if stray:
        sys.exit("not in this batch: %s" % ", ".join(stray))
    ordered = {q: lessons[q] for q in wanted if q in lessons}
    os.makedirs(os.path.dirname(PART), exist_ok=True)
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [q for q in wanted if q not in lessons]
    print("wrote %d lessons to %s; %d of the batch have none yet" % (len(ordered), os.path.relpath(PART), len(missing)))
    for q in missing:
        print("  no lesson: " + q)


if __name__ == "__main__":
    main()
