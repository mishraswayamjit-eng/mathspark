"""Writes data/teach/parts/imported-10.json: authored lessons for the questions in
data/bank-import/lessons/in-10.json (simple interest, averages, addition and subtraction stories).

    python -X utf8 scripts/teach/gen/imported_10.py
    python -X utf8 scripts/teach/validate.py --part imported-10
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import imported_10_lib as lib  # noqa: E402
import imported_10_interest  # noqa: E402,F401
import imported_10_interest_b  # noqa: E402,F401
import imported_10_money  # noqa: E402,F401
import imported_10_cricket  # noqa: E402,F401
import imported_10_misc  # noqa: E402,F401


def main():
    order = [q["id"] for q in lib.QUESTIONS]
    out = {qid: lib.LESSONS[qid] for qid in order if qid in lib.LESSONS}
    missing = [qid for qid in order if qid not in lib.LESSONS]
    with io.open(lib.PART, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote %d lessons to %s" % (len(out), os.path.relpath(lib.PART, lib.ROOT)))
    for qid in missing:
        print("  no lesson: %s" % qid)


if __name__ == "__main__":
    main()
