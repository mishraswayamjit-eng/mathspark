"""Lessons for data/bank-import/lessons/in-20.json (triangles; sharing in a ratio).

    python -X utf8 scripts/teach/gen/imported_20.py

Writes data/teach/parts/imported-20.json. The builders are in imported_20_ratio.py
(sharing in a ratio) and imported_20_tri.py (triangles); the lessons themselves are
in imported_20_ratio_a.py, imported_20_ratio_b.py and imported_20_tri_a.py.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

from imported_20_lib import P  # noqa: E402

MODULES = ["imported_20_ratio_a", "imported_20_ratio_b", "imported_20_tri_a"]

# Left out on purpose (see the report): the question's own numbers disagree.
LEFT_OUT = {
    # Angles 36°, 54°, 90° (a right triangle) with sides 7, 9 and 13 cm: 7² + 9² is not 13².
    P + "d38bd58a-0efe-4558-845b-451ba6dc7fe1",
    # The largest angle is between the two equal sides, so the base must be the longest
    # side; the question makes the base 5 cm SHORTER than the equal sides.
    P + "e9d46e9a-a871-492a-8574-e37fd925328d",
}


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-20.json"), encoding="utf-8") as f:
        batch = {q["id"]: q for q in json.load(f)}

    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).LESSONS.items():
            assert qid in batch and qid not in part and qid not in LEFT_OUT, qid
            part[qid] = lesson

    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    long = [(qid, i) for qid, s in part.items() for i, b in enumerate(s["beats"]) if len(b["say"]) > 240]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-20.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(part), len(LEFT_OUT), len(missing)))
    for qid in missing:
        print("  missing", qid, batch[qid]["topic"])
    for qid, i in long:
        print("  too long", qid, i, len(part[qid]["beats"][i]["say"]))


if __name__ == "__main__":
    main()
