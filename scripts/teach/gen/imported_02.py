"""Lessons for the imported batch 02 (angles and lines; area and perimeter).

    python -X utf8 scripts/teach/gen/imported_02.py

Reads data/bank-import/lessons/in-02.json and writes data/teach/parts/imported-02.json.
Every lesson is written for its own question; questions that share a structure go
through one builder that computes each board line from the question's numbers.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

SOURCE = os.path.join(ROOT, "data", "bank-import", "lessons", "in-02.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-02.json")

# Left out on purpose: id -> reason.
SKIPPED = {
    "AIGEN_grade5_352cbeaf-fdd9-435f-9e60-a906f4bf9b96":
        "the question's data contradict each other: a triangle whose equal angles are each "
        "three times the third, with equal sides of 5 cm, cannot have a third side of 3.4 cm",
}


def main():
    import imported_02_angles
    import imported_02_area
    import imported_02_area2

    with io.open(SOURCE, encoding="utf-8") as f:
        batch = json.load(f)
    lessons = {}
    for module in (imported_02_angles, imported_02_area, imported_02_area2):
        for qid, script in module.LESSONS.items():
            if qid in lessons:
                sys.exit("two lessons for %s" % qid)
            lessons[qid] = script

    ids = [q["id"] for q in batch]
    unknown = sorted(set(lessons) - set(ids))
    if unknown:
        sys.exit("not in the batch: %s" % ", ".join(unknown))
    out = {qid: lessons[qid] for qid in ids if qid in lessons}
    missing = [qid for qid in ids if qid not in lessons and qid not in SKIPPED]

    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons to %s" % (len(out), os.path.relpath(PART, ROOT)))
    print("left out on purpose: %d" % len([q for q in ids if q in SKIPPED]))
    if missing:
        print("still to write: %d" % len(missing))
        for qid in missing:
            print("  " + qid)


if __name__ == "__main__":
    main()
