"""Print questions of a Grade 4 topic for reading. Usage:
    python -X utf8 g4_gr4_fractions_dump.py <node> [start] [count] [full]
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

node = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else -1
count = int(sys.argv[3]) if len(sys.argv) > 3 else 50
full = len(sys.argv) > 4
qs = [q for q in bank.load_bank(4) if q.get("node") == node]
qs.sort(key=lambda q: q["id"])
if start < 0:
    print(len(qs), "questions")
    fam = collections.Counter(re.sub(r"\d+", "#", q["id"]) for q in qs)
    for k, v in fam.most_common():
        print("  %4d  %s" % (v, k))
    print(collections.Counter(q.get("subTopic") for q in qs).most_common())
    print(collections.Counter(len(q.get("stepByStep") or []) for q in qs))
    print(sorted(qs[0].keys()))
    sys.exit()
for i, q in enumerate(qs[start:start + count]):
    print("#%d %s [%s] ans=%s" % (start + i, q["id"], q.get("subTopic"), q.get("correctAnswer")))
    print("  Q:", q["questionText"].replace("\n", " / "))
    print("  O:", " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
    for s in (q.get("stepByStep") or []):
        t = s.get("text", "")
        print("   s%s: %s" % (s.get("step"), t if full else t[:150]))
        if full and s.get("latex"):
            print("        L: %s" % s["latex"])
