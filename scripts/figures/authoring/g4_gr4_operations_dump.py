"""Print the questions of a Grade 4 topic for reading. Usage:
    python -X utf8 scripts/figures/authoring/g4_gr4_operations_dump.py <topic> [summary|full] [start] [count] [idregex]
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

topic = sys.argv[1] if len(sys.argv) > 1 else "gr4_operations"
mode = sys.argv[2] if len(sys.argv) > 2 else "summary"
start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
count = int(sys.argv[4]) if len(sys.argv) > 4 else 100000
rx = re.compile(sys.argv[5]) if len(sys.argv) > 5 else None

qs = [q for q in bank.load_bank(4) if q.get("node") == topic]
qs.sort(key=lambda q: q["id"])
if rx:
    qs = [q for q in qs if rx.search(q["id"]) or rx.search(q.get("questionText", ""))]
print(len(qs), "questions")
if mode == "summary":
    fam = collections.Counter(re.sub(r"\d+", "#", q["id"]) for q in qs)
    for k, n in sorted(fam.items()):
        print("%5d  %s" % (n, k))
    print()
    for k, n in collections.Counter(q.get("subTopic", "") for q in qs).most_common():
        print("%5d  %s" % (n, k))
    print()
    for k, n in collections.Counter(q.get("source", "") for q in qs).most_common():
        print("%5d  %s" % (n, k))
    print(sorted(qs[0].keys()))
else:
    for q in qs[start:start + count]:
        opts = " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"])
        print("## %s [%s] ans=%s" % (q["id"], q.get("subTopic", ""), q["correctAnswer"]))
        print("Q: " + q["questionText"].replace("\n", " / "))
        print("O: " + opts)
        if mode == "full":
            for i, s in enumerate(q.get("stepByStep") or []):
                print("  s%d: %s" % (i, (s.get("text") or "").replace("\n", " / ")))
