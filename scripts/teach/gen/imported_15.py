"""Lessons for data/bank-import/lessons/in-15.json (58 profit and loss stories).

    python -X utf8 scripts/teach/gen/imported_15.py

Writes data/teach/parts/imported-15.json. The plain stories (total cost, how many
were sold, sales, profit) are in imported_15_a.py and go through one builder,
imported_15_lib.stall, which computes every board line. The stories with a twist
(a percentage, a discount, an unknown number bought) are in imported_15_b.py and
imported_15_c.py, built from the same parts.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

P = "AIGEN_grade5_"

# Left out on purpose (see the report): none so far.
LEFT_OUT = set()


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-15.json"), encoding="utf-8") as f:
        batch = [q["id"] for q in json.load(f)]
    by_key = {qid[len(P):len(P) + 8]: qid for qid in batch}
    assert len(by_key) == len(batch)

    part = {}
    for name in ("imported_15_a", "imported_15_b", "imported_15_c"):
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        mod = importlib.import_module(name)
        for key, lesson in mod.LESSONS.items():
            qid = by_key[key]
            assert qid not in part, qid
            part[qid] = lesson

    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-15.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(part), len(LEFT_OUT), len(missing)))
    for qid in missing:
        print("  missing", qid)


if __name__ == "__main__":
    main()
