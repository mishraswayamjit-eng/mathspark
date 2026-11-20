"""Print Grade 4 equations questions, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_equations_dump.py summary        # counts by id prefix and source
    python -X utf8 scripts/teach/gen/g4_gr4_equations_dump.py short [prefix] # one line per question
    python -X utf8 scripts/teach/gen/g4_gr4_equations_dump.py full <prefix> [start] [count]
    python -X utf8 scripts/teach/gen/g4_gr4_equations_dump.py missing [start] [count]  # full, no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_equations_dump.py ids <id> <id> ...
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_equations_lib import OUT, questions  # noqa: E402


def prefix_of(qid):
    return re.sub(r"\d+", "#", qid)


def full(q):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("source"), "|", q.get("difficulty"))
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


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "summary"
    qs = sorted(questions(), key=lambda q: q["id"])
    if what == "summary":
        c = collections.Counter((prefix_of(q["id"]), q.get("source"), q.get("subTopic")) for q in qs)
        for k, n in sorted(c.items()):
            print(n, k)
        print(len(qs), "questions")
        return
    if what == "short":
        pre = sys.argv[2] if len(sys.argv) > 2 else ""
        for q in qs:
            if q["id"].startswith(pre):
                print(q["id"], "|", q.get("difficulty"), "|", q["questionText"].replace("\n", " ")[:150])
        return
    if what == "figs":
        # the first figure of every question that is not a plain balance
        from g4_gr4_equations_lib import ROOT
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-gr4_equations.json")
        with io.open(path, encoding="utf-8") as f:
            figs = json.load(f)
        for q in qs:
            fig = figs.get(q["id"])
            if not fig:
                print(q["id"], "| no figure")
            elif (fig.get("figure") or {}).get("kind") != "balance" or len(sys.argv) > 2:
                print(q["id"], "|", json.dumps(fig.get("figure"), ensure_ascii=False))
                for s in fig.get("stepFigures") or []:
                    print("      step:", json.dumps(s, ensure_ascii=False))
        return
    if what == "ids":
        want = set(sys.argv[2:])
        for q in qs:
            if q["id"] in want:
                full(q)
        return
    if what == "missing":
        have = {}
        if os.path.exists(OUT):
            with io.open(OUT, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
        args = sys.argv[2:]
    else:
        pre = sys.argv[2]
        qs = [q for q in qs if q["id"].startswith(pre)]
        args = sys.argv[3:]
    start = int(args[0]) if args else 0
    count = int(args[1]) if len(args) > 1 else 1000
    for q in qs[start:start + count]:
        full(q)
    print(len(qs), "questions in all; shown from", start)


if __name__ == "__main__":
    main()
