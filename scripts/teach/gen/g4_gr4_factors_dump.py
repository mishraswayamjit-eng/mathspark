"""Print Grade 4 factors questions, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_factors_dump.py short            # one line each
    python -X utf8 scripts/teach/gen/g4_gr4_factors_dump.py short 0 100      # a slice
    python -X utf8 scripts/teach/gen/g4_gr4_factors_dump.py full 0 20        # in full, a slice
    python -X utf8 scripts/teach/gen/g4_gr4_factors_dump.py missing [short]  # with no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_factors_dump.py id <qid> ...     # these, in full
    python -X utf8 scripts/teach/gen/g4_gr4_factors_dump.py grep <regex>     # question text matches
    python -X utf8 scripts/teach/gen/g4_gr4_factors_dump.py stats
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

TOPIC = "gr4_factors"
OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)
FIGS = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)


def questions():
    return [q for q in bank.load_bank(4) if q.get("node") == TOPIC]


def opt_text(o):
    return o.get("text", "") if isinstance(o, dict) else str(o)


def short(q):
    print(q["id"], "|", q.get("difficulty"), "|", q["questionText"].replace("\n", " // "), "|",
          " ; ".join(opt_text(o) for o in q.get("options", [])), "|", q.get("correctAnswer"))


def full(q, figs):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"))
    print("Q:", q["questionText"])
    for o in q.get("options", []):
        print("   ", o.get("id", "") if isinstance(o, dict) else "", opt_text(o))
    print("KEY:", q.get("correctAnswer"))
    for h in q.get("hints") or []:
        print("HINT:", h)
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))
    if q["id"] in figs:
        print("FIG:", json.dumps(figs[q["id"]], ensure_ascii=False))


def main():
    args = sys.argv[1:]
    what = args[0] if args else "short"
    qs = questions()
    figs = {}
    if os.path.exists(FIGS):
        with io.open(FIGS, encoding="utf-8") as f:
            figs = json.load(f)
    if what == "stats":
        print(len(qs), "questions;", len([q for q in qs if q["id"] in figs]), "with a figure")
        pre = collections.Counter(re.sub(r"\d+", "#", q["id"]) for q in qs)
        for k, v in sorted(pre.items(), key=lambda kv: -kv[1]):
            print("  %4d  %s" % (v, k))
        word = collections.Counter(re.sub(r"\d[\d,]*", "#", q["questionText"])[:90] for q in qs)
        print(len(word), "wordings")
        for k, v in sorted(word.items(), key=lambda kv: -kv[1]):
            if v > 1:
                print("  %4d  %s" % (v, k.replace("\n", " // ")))
        print(collections.Counter(q.get("difficulty") for q in qs))
        return
    if what == "missing":
        have = {}
        if os.path.exists(OUT):
            with io.open(OUT, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
        mode = args[1] if len(args) > 1 else "short"
        lo = int(args[2]) if len(args) > 2 else 0
        hi = int(args[3]) if len(args) > 3 else len(qs)
        print(len(qs), "missing")
        for q in qs[lo:hi]:
            if mode == "short":
                short(q)
            elif mode == "brief":
                print("=" * 30, q["id"], q.get("difficulty"))
                print("Q:", q["questionText"])
                print("OPT:", " | ".join(opt_text(o) for o in q.get("options", [])), "KEY", q.get("correctAnswer"))
                for s in q.get("stepByStep") or []:
                    print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
                for k, v in sorted((q.get("misconceptions") or {}).items()):
                    if k != q.get("correctAnswer"):
                        print("MIS %s: %s" % (k, v))
                if q["id"] in figs and figs[q["id"]].get("figure"):
                    print("FIG:", json.dumps(figs[q["id"]]["figure"], ensure_ascii=False))
            else:
                full(q, figs)
        return
    if what == "id":
        want = set(args[1:])
        for q in qs:
            if q["id"] in want:
                full(q, figs)
        return
    if what == "grep":
        rx = re.compile(args[1])
        mode = args[2] if len(args) > 2 else "short"
        for q in qs:
            if rx.search(q["questionText"]) or rx.search(q["id"]):
                short(q) if mode == "short" else full(q, figs)
        return
    lo = int(args[1]) if len(args) > 1 else 0
    hi = int(args[2]) if len(args) > 2 else len(qs)
    for q in qs[lo:hi]:
        short(q) if what == "short" else full(q, figs)
    print(len(qs), "questions")


if __name__ == "__main__":
    main()
