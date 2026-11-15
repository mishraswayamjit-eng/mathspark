"""Explore: wording templates of the generated Grade 5 families (numbers replaced by N).

    python -X utf8 scripts/fixes/gen/answers_templates.py [min_count] [substring]
"""
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")
PREFIXES = ("VAR_G5_vary_", "VAR_EXT_", "VAR2_EXT_", "BOOST_EXT_", "PH3_EXT_")

with io.open(SEED, encoding="utf-8") as f:
    qs = [q for q in json.load(f)["questions"] if q.get("topicId") == "grade5"]

min_count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
sub = sys.argv[2] if len(sys.argv) > 2 else ""
print("grade5 questions:", len(qs))
print("by prefix:", Counter(next((p for p in PREFIXES if q["id"].startswith(p)), "other") for q in qs))
print("by source:", Counter(q.get("source") for q in qs))

tmpl = Counter()
example = {}
for q in qs:
    if not q["id"].startswith(PREFIXES):
        continue
    t = re.sub(r"\d+(?:\.\d+)?", "N", q["questionText"])
    tmpl[t] += 1
    example.setdefault(t, q)
for t, n in tmpl.most_common():
    if n < min_count or sub not in t:
        continue
    q = example[t]
    opts = [o["text"] for o in q["options"]]
    print("%4d | %s\n       e.g. %s | %s | %s | %s" % (n, t, q["id"], q["questionText"], opts, q["correctAnswer"]))
print("templates:", len(tmpl), "questions:", sum(tmpl.values()))
