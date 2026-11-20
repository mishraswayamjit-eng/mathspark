"""Print the questions of a Grade 4 topic (default gr4_quads) for figure authoring.

    python -X utf8 scripts/figures/authoring/g4_gr4_quads_list.py [topic] [start] [count] [full]
"""
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

topic = sys.argv[1] if len(sys.argv) > 1 else "gr4_quads"
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
count = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
full = len(sys.argv) > 4

qs = [q for q in bank.load_bank(4) if q.get("node") == topic]
print(len(qs), "questions in", topic)
for i, q in enumerate(qs[start:start + count], start):
    opts = " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"])
    print("#%d %s [%s] {%s} ans=%s" % (i, q["id"], q.get("subTopic", ""), q.get("source", ""), q["correctAnswer"]))
    print("  Q:", q["questionText"].replace("\n", " / "))
    print("  O:", opts)
    for j, s in enumerate(q.get("stepByStep") or []):
        t = s.get("text", "").replace("\n", " / ")
        print("  S%d: %s" % (j, t if full else t[:150]))
        if s.get("latex"):
            print("      L: %s" % s["latex"])
