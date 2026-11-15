"""One-off review helper: prints the distinct wordings (numbers and names masked) of the generated
questions in ratio-word-problems, with a count and one example id. Reads only; writes nothing.

    python -X utf8 scripts/speech/topics/ratio_word_problems_templates.py
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import load_grade5, source_strings, topic_of  # noqa: E402

NAMES = r"\b(Dev|Tara|Meera|Aditya|Priya|Nikhil|Kavya|Siddharth|Vivek|Isha|Neha|Aarav|Siya|Diya|Karan|Arjun|Riya|Rohan|Sahil)\b"

seen = collections.OrderedDict()
qs = sorted((q for q in load_grade5() if topic_of(q) == "ratio-word-problems"), key=lambda q: q["id"])
for q in qs:
    if q["id"].startswith("EXT_"):
        continue
    v = source_strings(q)
    for key in ("q", "hints", "steps"):
        items = [v[key]] if key == "q" else v[key]
        for i, s in enumerate(items):
            t = re.sub(r"\d+", "N", s)
            t = re.sub(NAMES, "NAME", t)
            t = re.sub(r"marbles|toffees|stickers|books", "THINGS", t)
            seen.setdefault(("%s%d" % (key, i), t), []).append((q["id"], s))
for (key, t), ids in seen.items():
    print("%-7s x%-3d %s\n            e.g. %s: %s" % (key, len(ids), t, ids[0][0], ids[0][1]))
