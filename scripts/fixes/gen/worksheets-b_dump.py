"""Print every question whose id starts with the given prefix, compactly. Read-only.

    python -X utf8 scripts/fixes/gen/worksheets-b_dump.py EXT_G5_WS_B4_ [start] [end]
"""
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")

prefix = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
with io.open(SEED, encoding="utf-8") as f:
    qs = [q for q in json.load(f)["questions"] if q["id"].startswith(prefix)]
qs.sort(key=lambda q: q["id"])
print(len(qs), "questions")
for q in qs:
    n = int(q["id"].rsplit("_", 1)[1])
    if not (start <= n <= end):
        continue
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("source"), "| key", q.get("correctAnswer"))
    print("Q:", q.get("questionText"))
    for letter, o in zip("ABCD", q.get("options", [])):
        print("  %s) %s" % (letter, o.get("text") if isinstance(o, dict) else o))
    for i, h in enumerate(q.get("hints") or []):
        print("  H%d: %s" % (i + 1, h))
    for i, s in enumerate(q.get("stepByStep") or []):
        print("  S%d: %s%s" % (i + 1, s.get("text"), (" [latex: %s]" % s["latex"]) if s.get("latex") else ""))
    for k in ("figure", "visual", "diagram", "image"):
        if q.get(k):
            print("  %s: %s" % (k, json.dumps(q[k], ensure_ascii=False)[:300]))
