"""Lessons for the imported batch 06 (58 one-off questions: primes and factors, word-problem equations).

    python -X utf8 scripts/teach/gen/imported_06.py

Writes data/teach/parts/imported-06.json. The lessons live in imported_06_a.py (factors and
primes), imported_06_b.py (plain two-step equations), imported_06_c.py (equations that need
tidying first) and imported_06_d.py (two-part questions).
"""
import importlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imported_06_lib import PART, batch  # noqa: E402

MODULES = ["imported_06_a", "imported_06_b", "imported_06_c", "imported_06_d"]


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
    order = [q["id"] for q in batch()]
    stray = [k for k in lessons if k not in order]
    if stray:
        sys.exit("not in the batch: %s" % ", ".join(stray))
    out = {k: lessons[k] for k in order if k in lessons}
    os.makedirs(os.path.dirname(PART), exist_ok=True)
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [k for k in order if k not in lessons]
    print("wrote %d lessons to %s; %d of the batch have none" % (len(out), os.path.relpath(PART, ROOT_REL()), len(missing)))
    for k in missing:
        print("  no lesson: %s" % k)


def ROOT_REL():
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))


if __name__ == "__main__":
    main()
