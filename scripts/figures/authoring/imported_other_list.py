"""List the imported Grade 5 questions outside area, angles and triangles, for figure authoring.

    python -X utf8 scripts/figures/authoring/imported_other_list.py                 # counts by topic
    python -X utf8 scripts/figures/authoring/imported_other_list.py gr5_ratio       # one topic, text only
    python -X utf8 scripts/figures/authoring/imported_other_list.py gr5_ratio steps # with options and steps
    python -X utf8 scripts/figures/authoring/imported_other_list.py gr5_ratio steps 0 40
    python -X utf8 scripts/figures/authoring/imported_other_list.py ids ID1 ID2 ... # full detail of these ids
    python -X utf8 scripts/figures/authoring/imported_other_list.py grep "regex"    # questions whose text matches
"""
import collections
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

SOURCES = ("ai_generated", "ipm_textbook", "official_ipm_2020")
NOT_MINE = ("gr5_area", "gr5_angles", "gr5_triangles")


def load():
    qs = [q for q in bank.load_bank(5)
          if q.get("topicId") == "grade5" and q.get("source") in SOURCES and q.get("node") not in NOT_MINE]
    qs.sort(key=lambda q: (str(q.get("node")), q["id"]))
    return qs


def show(q, full):
    one = lambda s: s.replace("\n", " / ")
    if full == "short":
        t = one(q["questionText"])
        if len(t) > 300:
            t = t[:170] + " […] " + t[-120:]
        print("%s | %s" % (q["id"][-12:] if q["id"].startswith("AIGEN") else q["id"], t))
        return
    if not full:
        print("%s | %s" % (q["id"], one(q["questionText"])))
        return
    print("## %s [%s | %s] ans=%s" % (q["id"], q.get("node"), q.get("source"), q["correctAnswer"]))
    print("Q: " + one(q["questionText"]))
    print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
    for i, s in enumerate(q.get("stepByStep") or []):
        print("  s%d: %s" % (i, one(s.get("text", ""))))
        if s.get("latex"):
            print("      L: %s" % one(s["latex"]))


if __name__ == "__main__":
    qs = load()
    args = sys.argv[1:]
    if not args:
        c = collections.Counter(str(q.get("node")) for q in qs)
        for k, v in sorted(c.items()):
            print("%4d  %s" % (v, k))
        print("%4d  total" % len(qs))
    elif args[0] == "ids":
        want = set(args[1:])
        for q in qs:
            if q["id"] in want:
                show(q, True)
    elif args[0] == "qs":   # full question text (and answer) of these ids; the last 12 characters are enough
        want = set(args[1:])
        for q in qs:
            if q["id"] in want or q["id"][-12:] in want:
                key = [o["text"] for o in q["options"] if o["id"] == q["correctAnswer"]][0]
                print("%s | %s  ==> %s" % (q["id"][-12:], q["questionText"].replace("\n", " / "), key))
    elif args[0] == "grep":
        rx = re.compile(args[1], re.I)
        full = len(args) > 2 and args[2] == "steps"
        for q in qs:
            if rx.search(q["questionText"]):
                show(q, full)
    else:
        sel = [q for q in qs if str(q.get("node")) == args[0]]
        full = "short" if "short" in args else (len(args) > 1 and args[1] == "steps")
        rest = [a for a in args[1:] if a not in ("steps", "short")]
        a = int(rest[0]) if rest else 0
        b = int(rest[1]) if len(rest) > 1 else len(sel)
        for q in sel[a:b]:
            show(q, full)
