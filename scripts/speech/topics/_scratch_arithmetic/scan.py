"""Scratch: what notation do the imported arithmetic questions use?

    python -X utf8 scripts/speech/topics/_scratch_arithmetic/scan.py            # source text
    python -X utf8 scripts/speech/topics/_scratch_arithmetic/scan.py --spoken   # the narration
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..")))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

PRE = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")
qs = sorted((q for q in load_grade5() if topic_of(q) == "arithmetic" and q["id"].startswith(PRE)), key=lambda q: q["id"])
spoken = "--spoken" in sys.argv
if spoken:
    with io.open(os.path.join(PARTS, "arithmetic.json"), encoding="utf-8") as f:
        part = json.load(f)
texts = []
for q in qs:
    e = part[q["id"]] if spoken else source_strings(q)
    texts += [e["q"]] + e["options"] + e["hints"] + e["steps"]
chars = collections.Counter()
caps = collections.Counter()
glued = collections.Counter()
short = collections.Counter()
for t in texts:
    for c in t:
        if not (c.isalnum() or c in " .,?!'"):
            chars[c] += 1
    for w in re.findall(r"\b[A-Z]{2,}\b", t):
        caps[w] += 1
    for w in re.findall(r"\b\d+[A-Za-z]+\b|\b[A-Za-z]+\d+\b", t):
        glued[w] += 1
    for w in re.findall(r"(?<=\d )[a-zA-Z]{1,3}\b\.?", t):
        short[w] += 1
print("CHARS", " ".join("%r:%d" % (c, n) for c, n in chars.most_common()))
print("CAPS", " ".join("%s:%d" % (c, n) for c, n in caps.most_common()))
print("GLUED", " ".join("%s:%d" % (c, n) for c, n in glued.most_common()))
print("AFTER-NUMBER", " ".join("%s:%d" % (c, n) for c, n in short.most_common()))
src = collections.Counter(q.get("source") for q in qs)
print("SOURCES", dict(src))
sub = collections.Counter(q.get("subTopic") for q in qs)
print("SUBTOPICS", dict(sub))
