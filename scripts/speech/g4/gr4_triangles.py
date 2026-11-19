"""Narration for the Grade 4 topic gr4_triangles (kinds of triangle, angle sum, the triangle rule, perimeter, area).

    python -X utf8 scripts/speech/g4/gr4_triangles.py

Writes data/question-speech/parts-g4/gr4_triangles.json.

Two layers, most specific first:
  1. HAND   single strings written by hand, keyed "<question id>:<slot>" (gr4_triangles_hand.py).
  2. say()  rules (gr4_triangles_rules.py, which builds on gr4_angles_rules.py).
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import common  # noqa: E402
from gr4_angles_rules import narrate  # noqa: E402
from gr4_triangles_rules import maths_line, say  # noqa: E402
from gr4_triangles_hand import HAND  # noqa: E402

NODE = "gr4_triangles"
OUT = os.path.join(common.ROOT, "data", "question-speech", "parts-g4", NODE + ".json")


def main():
    counts = {"hand": 0, "rule": 0}
    used = set()
    questions = sorted((q for q in common.bank.load_bank(4) if q.get("node") == NODE), key=lambda q: q["id"])
    part = {q["id"]: narrate(q, HAND, counts, used, say=say, maths_line=maths_line) for q in questions}
    unused = sorted(set(HAND) - used)
    if unused:
        sys.exit("hand lines that match nothing:\n  %s" % "\n  ".join(unused))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %d questions: %d lines by hand, %d by rule" % (len(part), counts["hand"], counts["rule"]))
    if counts.get("dropped"):
        print("maths lines left unread (write these steps by hand): %s" % ", ".join(counts["dropped"]))


if __name__ == "__main__":
    main()
