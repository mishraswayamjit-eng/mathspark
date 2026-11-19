"""Print the source strings of gr4_units questions (for the narration writer to read).

    python -X utf8 scripts/speech/g4/gr4_units_dump.py            # compact list of every question
    python -X utf8 scripts/speech/g4/gr4_units_dump.py 0 40       # full source for questions 0..39
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import common  # noqa: E402

NODE = "gr4_units"


def main():
    qs = sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])
    args = sys.argv[1:]
    if not args:
        for i, q in enumerate(qs):
            print("%3d %-28s %s" % (i, q["id"], q.get("questionText", "").replace("\n", " // ")[:110]))
        return
    lo, hi = int(args[0]), int(args[1])
    for i, q in enumerate(qs[lo:hi], lo):
        src = common.source_strings(q)
        own = q.get("stepByStep") or []
        print("=== %d %s" % (i, q["id"]))
        print("Q : " + json.dumps(src["q"], ensure_ascii=False))
        print("O : " + "  ¦  ".join(src["options"]))
        for j, h in enumerate(src["hints"]):
            if h.strip():
                print("H%d: %s" % (j, json.dumps(h, ensure_ascii=False)))
        for j, s in enumerate(src["steps"]):
            lx = own[j].get("latex") if j < len(own) else None
            if s.strip():
                print("S%d: %s%s" % (j, json.dumps(s, ensure_ascii=False), ("   [latex: %s]" % lx) if lx else ""))


if __name__ == "__main__":
    main()
