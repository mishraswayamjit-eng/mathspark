"""Print Grade 4 questions of a topic in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_sequences_dump.py gr4_sequences stats
    python -X utf8 scripts/teach/gen/g4_gr4_sequences_dump.py gr4_sequences all 0 20
    python -X utf8 scripts/teach/gen/g4_gr4_sequences_dump.py gr4_sequences missing [full]
    python -X utf8 scripts/teach/gen/g4_gr4_sequences_dump.py gr4_sequences brief
    python -X utf8 scripts/teach/gen/g4_gr4_sequences_dump.py gr4_sequences <id prefix>
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def full(q, figs):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("source"), "|", q.get("difficulty"))
    print("Q:", q["questionText"])
    for o in q.get("options", []):
        print("   ", o.get("id", "") if isinstance(o, dict) else "", o.get("text", "") if isinstance(o, dict) else o)
    print("KEY:", q.get("correctAnswer"))
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", ""))
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))
    if q["id"] in figs:
        print("FIG:", json.dumps(figs[q["id"]].get("figure"), ensure_ascii=False))


def main():
    topic = sys.argv[1]
    what = sys.argv[2] if len(sys.argv) > 2 else "stats"
    lo = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 0
    hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10000
    qs = [q for q in bank.load_bank(4) if q.get("node") == topic]
    figs = {}
    fpath = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
    if os.path.exists(fpath):
        with io.open(fpath, encoding="utf-8") as f:
            figs = json.load(f)
    have = {}
    path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            have = json.load(f)
    if what == "stats":
        print(len(qs), "questions;", len(figs), "with figures;", len(have), "with lessons")
        c = collections.Counter(re.sub(r"\d+", "#", q["id"]) for q in qs)
        for k, n in sorted(c.items()):
            print("  %4d  %s" % (n, k))
        c = collections.Counter((q.get("subTopic"), q.get("difficulty")) for q in qs)
        for k, n in sorted(c.items(), key=str):
            print("  %4d  %s" % (n, k))
        return
    if what == "brief":
        for i, q in enumerate(qs):
            print(i, q["id"], "|", q["questionText"][:110].replace("\n", " "))
        return
    if what == "missing":
        qs = [q for q in qs if q["id"] not in have]
        if not (len(sys.argv) > 3 and sys.argv[3] == "full"):
            for q in qs:
                print(q["id"], "|", q["questionText"][:100].replace("\n", " "))
            print(len(qs), "missing")
            return
    elif what != "all":
        qs = [q for q in qs if q["id"].startswith(what)]
    total = len(qs)
    for q in qs[lo:hi]:
        full(q, figs)
    print(len(qs[lo:hi]), "of", total, "questions")


if __name__ == "__main__":
    main()
