"""Lessons for batch 09 of the imported Grade 5 questions (integers, simple interest).

    python -X utf8 scripts/teach/gen/imported_09.py

Reads data/bank-import/lessons/in-09.json and writes data/teach/parts/imported-09.json.
Lessons are keyed in the helper files by the first 8 characters of the question's uuid.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

BATCH = os.path.join(ROOT, "data", "bank-import", "lessons", "in-09.json")
PART = os.path.join(ROOT, "data", "teach", "parts", "imported-09.json")
PREFIX = "AIGEN_grade5_"
MODULES = ["imported_09_walks_a", "imported_09_walks_b", "imported_09_ledgers",
           "imported_09_si_a", "imported_09_si_b", "imported_09_si_c"]

# Questions deliberately left without a lesson: short key -> reason.
LEFT_OUT = {}


def main():
    with io.open(BATCH, encoding="utf-8") as f:
        batch = json.load(f)
    by_short = {}
    for q in batch:
        short = q["id"][len(PREFIX):len(PREFIX) + 8]
        assert q["id"].startswith(PREFIX) and short not in by_short, q["id"]
        by_short[short] = q["id"]

    lessons = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        mod = importlib.import_module(name)
        for short, script in mod.LESSONS.items():
            assert short in by_short, "%s: %s is not in the batch" % (name, short)
            assert short not in lessons, "%s: %s written twice" % (name, short)
            lessons[short] = script

    out = {}
    missing = []
    for q in batch:
        short = q["id"][len(PREFIX):len(PREFIX) + 8]
        if short in lessons:
            out[q["id"]] = lessons[short]
        elif short not in LEFT_OUT:
            missing.append(short)

    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons of %d questions to %s" % (len(out), len(batch), os.path.relpath(PART, ROOT)))
    if LEFT_OUT:
        print("left out on purpose: %s" % ", ".join(sorted(LEFT_OUT)))
    if missing:
        print("still to write (%d): %s" % (len(missing), ", ".join(missing)))


if __name__ == "__main__":
    main()
