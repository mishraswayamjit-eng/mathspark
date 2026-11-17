"""Lessons for data/bank-import/lessons/in-12.json
(multiplication and division stories, textbook multiplication and division, percent and money).

    python -X utf8 scripts/teach/gen/imported_12.py

Writes data/teach/parts/imported-12.json. The lessons live in:
  imported_12_a.py      festival and shop stories (multiply, divide, remainders)
  imported_12_a2.py     more of the same
  imported_12_b.py      textbook questions written one by one
  imported_12_rules.py  textbook questions that share a structure, built from their numbers
  imported_12_c.py      percent and money
Every line of working is computed by imported_12_lib.E / A.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

MODULES = ["imported_12_a", "imported_12_a2", "imported_12_b", "imported_12_b2", "imported_12_rules", "imported_12_c"]

# Left out on purpose (see the report): none.
LEFT_OUT = set()


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-12.json"), encoding="utf-8") as f:
        batch = {q["id"]: q for q in json.load(f)}

    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        module = __import__(name)
        for qid, lesson in module.LESSONS.items():
            assert qid in batch, "%s: %s is not in the batch" % (name, qid)
            assert qid not in part, "%s: %s has two lessons" % (name, qid)
            part[qid] = lesson

    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-12.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(part), len(LEFT_OUT), len(missing)))
    for qid in missing[:5]:
        print("  missing", qid)
    for qid, s in part.items():
        for i, b in enumerate(s["beats"]):
            if len(b["say"]) > 240:
                print("  too long (%d)" % len(b["say"]), qid, i)
            for op in b.get("board", []):
                if op["op"] == "write" and len(op["text"]) > 60:
                    print("  line too long (%d)" % len(op["text"]), qid, op["text"])


if __name__ == "__main__":
    main()
