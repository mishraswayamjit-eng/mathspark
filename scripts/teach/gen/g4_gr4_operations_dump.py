"""Print Grade 4 operations questions, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_operations_dump.py stats
    python -X utf8 scripts/teach/gen/g4_gr4_operations_dump.py brief [prefix]    # one line each
    python -X utf8 scripts/teach/gen/g4_gr4_operations_dump.py full <prefix> [from to]
    python -X utf8 scripts/teach/gen/g4_gr4_operations_dump.py missing [full [from to]]
    python -X utf8 scripts/teach/gen/g4_gr4_operations_dump.py figs [prefix]
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from g4_gr4_operations_common import PART, FIGS, questions, opts  # noqa: E402


def family(qid):
    m = re.match(r"(.*?)(_V\d+|_\d+)$", qid)
    return re.sub(r"\d+", "#", qid)


def full(q):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"))
    print("Q:", q["questionText"])
    print("OPTS:", " | ".join(opts(q)), "  KEY:", q.get("correctAnswer"))
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "stats"
    qs = list(questions().values())
    have = {}
    if os.path.exists(PART):
        with io.open(PART, encoding="utf-8") as f:
            have = json.load(f)
    if what == "stats":
        c = collections.Counter(family(q["id"]) for q in qs)
        for k, n in sorted(c.items()):
            print("%4d  %s" % (n, k))
        print(len(qs), "questions;", len(have), "lessons")
        print(collections.Counter(q.get("difficulty") for q in qs))
        print(collections.Counter(q.get("source") for q in qs))
        return
    if what == "brief":
        pre = sys.argv[2] if len(sys.argv) > 2 else ""
        n = 0
        for q in qs:
            if q["id"].startswith(pre):
                n += 1
                print(q["id"], "|", q.get("difficulty"), "|", q["questionText"].replace("\n", " / "), "|", opts(q), q.get("correctAnswer"))
        print(n, "questions")
        return
    if what == "figs":
        pre = sys.argv[2] if len(sys.argv) > 2 else ""
        with io.open(FIGS, encoding="utf-8") as f:
            figs = json.load(f)
        n = 0
        for k, v in figs.items():
            if k.startswith(pre):
                n += 1
                print(k, json.dumps(v, ensure_ascii=False)[:1500])
        print(n, "of", len(figs), "figures")
        return
    if what == "missing":
        qs = [q for q in qs if q["id"] not in have]
        if len(sys.argv) > 2 and sys.argv[2] == "full":
            if len(sys.argv) > 4:
                qs = qs[int(sys.argv[3]):int(sys.argv[4])]
            for q in qs:
                full(q)
        else:
            for q in qs:
                print(q["id"], "|", q.get("difficulty"), "|", q["questionText"][:100].replace("\n", " / "))
        print(len(qs), "missing")
        return
    pre = sys.argv[2] if len(sys.argv) > 2 else ""
    qs = [q for q in qs if q["id"].startswith(pre)]
    if len(sys.argv) > 4:
        qs = qs[int(sys.argv[3]):int(sys.argv[4])]
    for q in qs:
        full(q)
    print(len(qs), "questions")


if __name__ == "__main__":
    main()
