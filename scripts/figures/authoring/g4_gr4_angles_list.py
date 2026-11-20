"""List the Grade 4 angle / triangle questions, for authoring.
    python -X utf8 scripts/figures/authoring/g4_gr4_angles_list.py <node> [start] [end] [nosteps]
    python -X utf8 scripts/figures/authoring/g4_gr4_angles_list.py <node> families
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def load(node):
    qs = [q for q in bank.load_bank(4) if q.get("node") == node]
    qs.sort(key=lambda q: q["id"])
    return qs


def family(qid):
    return re.sub(r"\d+", "#", qid)


if __name__ == "__main__":
    node = sys.argv[1]
    qs = load(node)
    print("%d questions" % len(qs))
    if len(sys.argv) > 2 and sys.argv[2] == "families":
        c = collections.Counter((family(q["id"]), q.get("source", ""), q.get("subTopic", "")) for q in qs)
        for k, v in sorted(c.items()):
            print("%4d  %s" % (v, " | ".join(k)))
        sys.exit(0)
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    b = int(sys.argv[3]) if len(sys.argv) > 3 else len(qs)
    nosteps = len(sys.argv) > 4
    for i, q in enumerate(qs[a:b]):
        print("## %d %s [%s | %s] ans=%s" % (a + i, q["id"], q.get("subTopic", ""), q.get("source", ""), q["correctAnswer"]))
        print("Q: " + q["questionText"].replace("\n", " / "))
        print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
        if not nosteps:
            for j, s in enumerate(q.get("stepByStep") or []):
                print("  s%d: %s" % (j, s.get("text", "").replace("\n", " / ")))
