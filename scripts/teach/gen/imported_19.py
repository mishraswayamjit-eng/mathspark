"""Lessons for the imported batch 19 (one-off Grade 5 questions: square numbers and roots, triangles).

    python -X utf8 scripts/teach/gen/imported_19.py

Writes data/teach/parts/imported-19.json. The lessons themselves are in
imported_19_squares_a.py (story problems and spotting squares), imported_19_squares_b.py
(rows, areas and roots), imported_19_squares_c.py (putting numbers in for letters),
imported_19_tri_a.py (angle sums) and imported_19_tri_b.py (sides, and mixed questions).
"""
import importlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imported_19_lib import PART, source_ids  # noqa: E402

MODULES = ["imported_19_squares_a", "imported_19_squares_b", "imported_19_squares_c",
           "imported_19_tri_a", "imported_19_tri_b"]


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
