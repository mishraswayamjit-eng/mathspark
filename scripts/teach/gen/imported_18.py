"""Lessons for data/bank-import/lessons/in-18.json (time, distance and speed; square numbers and roots).

    python -X utf8 scripts/teach/gen/imported_18.py

Writes data/teach/parts/imported-18.json. Questions that share a structure are taught by
builders that compute every board line from the question's numbers; the rest are written
by hand, one lesson each.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

MODULES = ["imported_18_speed_a", "imported_18_speed_b", "imported_18_sq_rules",
           "imported_18_sq_a", "imported_18_sq_b", "imported_18_sq_c"]

# Left out on purpose (see the report).
LEFT_OUT = set()


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-18.json"), encoding="utf-8") as f:
        batch = {q["id"]: q for q in json.load(f)}

    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).LESSONS.items():
            assert qid in batch, "%s: %s is not in the batch" % (name, qid)
            assert qid not in part, "%s: %s has two lessons" % (name, qid)
            part[qid] = lesson

    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-18.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(part), len(LEFT_OUT), len(missing)))
    for qid in (missing if len(missing) <= 12 else []):
        print("  missing", qid)
    for qid, s in part.items():
        for i, b in enumerate(s["beats"]):
            if len(b["say"]) > 240:
                print("  too long", qid, i, len(b["say"]))
            if b.get("ask") and len(b["ask"].get("ifNot", "")) > 240:
                print("  ifNot too long", qid, i)
            for c in (b.get("ask") or {}).get("choices", []):
                if len(c) > 40:
                    print("  choice too long", qid, i, c)
            for op in b.get("board", []):
                if op["op"] == "write" and len(op["text"]) > 60:
                    print("  line too long", qid, i, op["text"])
        if not 6 <= len(s["beats"]) <= 16:
            print("  beats", qid, len(s["beats"]))


if __name__ == "__main__":
    main()
