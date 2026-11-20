"""Print Grade 4 fractions questions, for writing lessons.

    python -X utf8 scripts/teach/gen/g4_gr4_fractions_dump.py --brief
    python -X utf8 scripts/teach/gen/g4_gr4_fractions_dump.py 0 20
    python -X utf8 scripts/teach/gen/g4_gr4_fractions_dump.py --ids
    python -X utf8 scripts/teach/gen/g4_gr4_fractions_dump.py --todo      # full dump of questions with no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_fractions_dump.py --figs 0 20  # with figure specs
"""
import argparse
import collections
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_fractions_lib import FIGS, OUT, option_texts, questions  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lo", nargs="?", type=int)
    ap.add_argument("hi", nargs="?", type=int)
    ap.add_argument("--grep")
    ap.add_argument("--max", type=int, default=2000)
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--ids", action="store_true")
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--figs", action="store_true")
    ap.add_argument("--shapes", action="store_true")
    args = ap.parse_args()
    qs = questions()
    done = {}
    if os.path.exists(OUT):
        with io.open(OUT, encoding="utf-8") as f:
            done = json.load(f)
    figs = {}
    if args.figs and os.path.exists(FIGS):
        with io.open(FIGS, encoding="utf-8") as f:
            figs = json.load(f)
    if args.ids:
        c = collections.Counter(re.sub(r"\d+", "#", q["id"]) for q in qs)
        for k, v in sorted(c.items()):
            print("%5d  %s" % (v, k))
        print(len(qs), "questions")
        return
    if args.shapes:
        c = collections.Counter()
        ex = {}
        for q in qs:
            if q["id"] in done:
                continue
            k = re.sub(r"\d+", "#", q["questionText"])
            c[k] += 1
            ex.setdefault(k, q["id"])
        for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
            print("%4d  %s  | %s" % (v, k[:150], ex[k]))
        return
    n = 0
    for i, q in enumerate(qs):
        if args.lo is not None and not (args.lo <= i <= (args.hi if args.hi is not None else args.lo)):
            continue
        if args.grep and args.grep not in q["questionText"] and args.grep not in q["id"]:
            continue
        if args.todo and q["id"] in done:
            continue
        n += 1
        if n > args.max:
            break
        opts = option_texts(q)
        key = q.get("correctAnswer")
        if args.brief:
            print("%3d %s [%s] | %s | %s | key %s" % (i, q["id"], q.get("difficulty", "")[:1], q["questionText"], " ; ".join(opts), key))
            continue
        print("=== %d %s  [%s] [%s]" % (i, q["id"], q.get("subTopic"), q.get("difficulty")))
        print("Q: %s" % q["questionText"])
        print("OPTS: %s   KEY %s" % (" | ".join(opts), key))
        for s in q.get("stepByStep") or []:
            print("  STEP: %s" % (s.get("text", "") if isinstance(s, dict) else s))
        for k, v in sorted((q.get("misconceptions") or {}).items()):
            if v:
                print("  MIS %s: %s" % (k, v))
        if args.figs and q["id"] in figs:
            print("  FIG: %s" % json.dumps(figs[q["id"]], ensure_ascii=False))
    print("%d shown" % min(n, args.max))


if __name__ == "__main__":
    main()
