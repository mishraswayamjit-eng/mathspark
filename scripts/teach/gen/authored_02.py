"""Lessons for the new Grade 5 questions listed in data/bank-import/g5/lessons-ids-2.json.

    python -X utf8 scripts/teach/gen/authored_02.py

Writes data/teach/parts/authored-02.json. Every lesson is written by hand for its one
question, in the helper modules authored_02_a, authored_02_b, ...
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from authored_02_lib import OUT, load_questions  # noqa: E402

MODULES = ["authored_02_a", "authored_02_b", "authored_02_c", "authored_02_d",
           "authored_02_e", "authored_02_f", "authored_02_g", "authored_02_h"]


def main():
    batch = {q["id"]: q for q in load_questions()}

    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).LESSONS.items():
            assert qid in batch, "%s: %s is not in the batch" % (name, qid)
            assert qid not in part, "%s: %s has two lessons" % (name, qid)
            part[qid] = lesson

    ordered = {qid: part[qid] for qid in batch if qid in part}
    missing = [qid for qid in batch if qid not in part]
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; no lesson yet for %d" % (len(ordered), len(missing)))
    for qid in (missing if len(missing) <= 12 else []):
        print("  missing", qid)
    for qid, s in ordered.items():
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
