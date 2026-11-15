"""Review helper: print the narration of arithmetic questions by position in the sorted list.

    python -X utf8 scripts/speech/topics/arithmetic_dump.py 24 50          # spoken lines only
    python -X utf8 scripts/speech/topics/arithmetic_dump.py 24 50 --print  # with the printed source
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

qs = sorted((q for q in load_grade5() if topic_of(q) == "arithmetic"), key=lambda q: q["id"])
with io.open(os.path.join(PARTS, "arithmetic.json"), encoding="utf-8") as f:
    part = json.load(f)
a, b = int(sys.argv[1]), int(sys.argv[2])
both = "--print" in sys.argv
for q in qs[a:b]:
    e, src = part[q["id"]], source_strings(q)
    print("##", q["id"])
    if both:
        print("   q<", src["q"].replace("\n", " / "))
    print("   Q:", e["q"])
    for key in ("options", "hints", "steps"):
        for i, t in enumerate(e[key]):
            if both and src[key][i]:
                print("  %s%d<" % (key[0], i), src[key][i])
            if t:
                print("  %s%d:" % (key[0], i), t)
