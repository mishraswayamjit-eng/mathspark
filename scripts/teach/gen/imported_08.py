"""Lessons for batch 08 of the imported Grade 5 questions.

    python -X utf8 scripts/teach/gen/imported_08.py

Reads data/bank-import/lessons/in-08.json (for the list of ids only) and writes
data/teach/parts/imported-08.json. Then check it with
    python -X utf8 scripts/teach/validate.py --part imported-08
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

from imported_08_hand import LESSONS as HAND  # noqa: E402
from imported_08_hcf import build  # noqa: E402
from imported_08_specs import SPECS  # noqa: E402

BATCH = os.path.join(ROOT, "data", "bank-import", "lessons", "in-08.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-08.json")

# Questions left out on purpose (their own data disagree, or the key is not right): id -> reason.
LEFT_OUT = {}


def main():
    with io.open(BATCH, encoding="utf-8") as f:
        batch = json.load(f)
    order = [q["id"] for q in batch]

    lessons = dict(HAND)
    for spec in SPECS:
        if spec["id"] in lessons:
            sys.exit("two lessons for %s" % spec["id"])
        lessons[spec["id"]] = build(spec)

    stray = [qid for qid in lessons if qid not in order]
    if stray:
        sys.exit("not in the batch: %s" % ", ".join(stray))
    missing = [qid for qid in order if qid not in lessons and qid not in LEFT_OUT]
    long_says = []
    for qid, script in lessons.items():
        for i, beat in enumerate(script["beats"]):
            if len(beat["say"]) > 240:
                long_says.append("%s beat %d: %d characters" % (qid, i + 1, len(beat["say"])))
            for op in beat.get("board", []):
                if op["op"] == "write" and len(op["text"]) > 60:
                    long_says.append("%s beat %d: line too long: %s" % (qid, i + 1, op["text"]))

    out = {qid: lessons[qid] for qid in order if qid in lessons}
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons to %s" % (len(out), os.path.relpath(PART, ROOT)))
    print("beats: %d to %d" % (min(len(s["beats"]) for s in out.values()), max(len(s["beats"]) for s in out.values())))
    for m in missing:
        print("NO LESSON  " + m)
    for m in long_says:
        print("TOO LONG   " + m)
    for qid, why in LEFT_OUT.items():
        print("LEFT OUT   %s: %s" % (qid, why))


if __name__ == "__main__":
    main()
