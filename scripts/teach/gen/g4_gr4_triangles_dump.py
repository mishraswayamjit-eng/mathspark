"""Print gr4_triangles questions in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_triangles_dump.py summary
    python -X utf8 scripts/teach/gen/g4_gr4_triangles_dump.py all 0 20      # a slice
    python -X utf8 scripts/teach/gen/g4_gr4_triangles_dump.py missing 0 20  # no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_triangles_dump.py id <question id>
    python -X utf8 scripts/teach/gen/g4_gr4_triangles_dump.py figs          # figure specs
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

TOPIC = "gr4_triangles"


def questions():
    return [q for q in bank.load_bank(4) if q.get("node") == TOPIC]


def show(q, figs):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"))
    print("Q:", q["questionText"])
    for o in q.get("options", []):
        print("   ", o.get("id", "") if isinstance(o, dict) else "", o.get("text", "") if isinstance(o, dict) else o)
    print("KEY:", q.get("correctAnswer"))
    for h in q.get("hints") or []:
        print("HINT:", h)
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))
    f = figs.get(q["id"])
    if f:
        print("FIG:", json.dumps(f.get("figure"), ensure_ascii=False))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "summary"
    qs = questions()
    figs = {}
    fpath = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)
    if os.path.exists(fpath):
        with io.open(fpath, encoding="utf-8") as f:
            figs = json.load(f)
    if what == "summary":
        c = collections.Counter()
        for q in qs:
            c[re.sub(r"\d+", "#", q["id"])] += 1
        for k, n in sorted(c.items()):
            print("%4d  %s" % (n, k))
        print(len(qs), "questions;", len(figs), "with figures")
        print(collections.Counter(q.get("difficulty") for q in qs))
        return
    if what == "id":
        for q in qs:
            if q["id"] in sys.argv[2:]:
                show(q, figs)
        return
    if what == "figs":
        for q in qs:
            if q["id"] in figs:
                print(q["id"], json.dumps(figs[q["id"]], ensure_ascii=False))
        return
    if what == "missing":
        path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)
        have = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
    total = len(qs)
    if len(sys.argv) > 3:
        qs = qs[int(sys.argv[2]):int(sys.argv[3])]
    for q in qs:
        show(q, figs)
    print(len(qs), "of", total, "questions")


if __name__ == "__main__":
    main()
