"""Lessons for data/bank-import/lessons/in-17.json (number series; speed, distance and time).

    python -X utf8 scripts/teach/gen/imported_17.py

Writes data/teach/parts/imported-17.json. Series that share a structure are taught by
the builders in imported_17_seq_rules (fed from imported_17_seq); the rest are written
one by one in imported_17_seq_hand and imported_17_speed_*.
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)

MODULES = ["imported_17_seq", "imported_17_seq_hand", "imported_17_speed_a", "imported_17_speed_b", "imported_17_speed_c"]

# Left out on purpose (see the report).
LEFT_OUT = set()


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "lessons", "in-17.json"), encoding="utf-8") as f:
        batch = {q["id"]: q for q in json.load(f)}
    part = {}
    for name in MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, lesson in importlib.import_module(name).L.items():
            assert qid in batch and qid not in part and qid not in LEFT_OUT, qid
            part[qid] = lesson
    ordered = {qid: part[qid] for qid in batch if qid in part}
    missing = [qid for qid in batch if qid not in part and qid not in LEFT_OUT]
    out = os.path.join(ROOT, "data", "teach", "parts", "imported-17.json")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d lessons; left out %d; no lesson yet for %d" % (len(ordered), len(LEFT_OUT), len(missing)))
    for qid in missing:
        print("  missing", qid)


if __name__ == "__main__":
    main()
