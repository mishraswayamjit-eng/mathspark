"""Lessons for the newly written Grade 5 questions listed in data/bank-import/g5/lessons-ids-3.json.

    python -X utf8 scripts/teach/gen/authored_03.py

Writes data/teach/parts/authored-03.json. Every lesson is written by hand, one per question,
in the helper modules whose names start authored_03_.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

MODULES = ["authored_03_meas", "authored_03_ops1", "authored_03_ops2", "authored_03_pct_a",
           "authored_03_pct_b", "authored_03_pv_a", "authored_03_pv_b"]


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "g5", "lessons-ids-3.json"), encoding="utf-8") as f:
        ids = json.load(f)

    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).LESSONS.items():
            assert qid in ids, "%s: %s is not in the list" % (name, qid)
            assert qid not in part, "%s: %s has two lessons" % (name, qid)
            part[qid] = lesson

    part = {qid: part[qid] for qid in ids if qid in part}
    missing = [qid for qid in ids if qid not in part]
    out = os.path.join(ROOT, "data", "teach", "parts", "authored-03.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; no lesson yet for %d" % (len(part), len(missing)))
    for qid in (missing if len(missing) <= 12 else []):
        print("  missing", qid)
    for qid, s in part.items():
        for i, b in enumerate(s["beats"]):
            if len(b["say"]) > 240:
                print("  too long", qid, i, len(b["say"]))
            if b.get("ask") and len(b["ask"].get("ifNot", "")) > 240:
                print("  ifNot too long", qid, i, len(b["ask"]["ifNot"]))
            for c in (b.get("ask") or {}).get("choices", []):
                if len(c) > 40:
                    print("  choice too long", qid, i, c)
            for op in b.get("board", []):
                if op["op"] == "write" and len(op["text"]) > 60:
                    print("  line too long", qid, i, op["text"])
                for key in ("note", "label"):
                    if op["op"] != "write" and isinstance(op.get(key), str) and len(op[key]) > 24:
                        print("  note too long", qid, i, op[key])
                if op["op"] == "note" and len(op["text"]) > 24:
                    print("  note too long", qid, i, op["text"])
        if not 6 <= len(s["beats"]) <= 16:
            print("  beats", qid, len(s["beats"]))


if __name__ == "__main__":
    main()
