"""Print Grade 4 questions of one topic, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_units_dump.py <topic> summary        # counts by id family and wording
    python -X utf8 scripts/teach/gen/g4_units_dump.py <topic> full A B       # questions number A to B in full
    python -X utf8 scripts/teach/gen/g4_units_dump.py <topic> brief A B      # one line each
    python -X utf8 scripts/teach/gen/g4_units_dump.py <topic> missing        # ids with no lesson yet
    python -X utf8 scripts/teach/gen/g4_units_dump.py <topic> fig <id>       # the figure specs of one question
    python -X utf8 scripts/teach/gen/g4_units_dump.py <topic> id <id> ...    # these questions in full
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


def questions(topic):
    return [q for q in bank.load_bank(4) if q.get("node") == topic]


def family(qid):
    m = re.match(r"(PYQ|EXT_G4_FP|EXT_G4_WS[A-Z0-9]*|G4A|VAR\d*|BOOST|PH3|Q_CH\d+_V|Q_CH|Q_DH)", qid)
    return m.group(1) if m else qid.split("_")[0]


def shape(text):
    return re.sub(r"\d+(?:[.,]\d+)*", "#", text)


def opt(o):
    return o.get("text", "") if isinstance(o, dict) else str(o)


HINTS = False


def full(q, n=None):
    print("=" * 70)
    print(n if n is not None else "", q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"))
    print("Q:", q["questionText"])
    print("OPTS:", " | ".join(opt(o) for o in q.get("options", [])), "  KEY:", q.get("correctAnswer"))
    for h in (q.get("hints") or []) if HINTS else []:
        print("HINT:", h)
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))


def main():
    topic = sys.argv[1]
    what = sys.argv[2] if len(sys.argv) > 2 else "summary"
    qs = questions(topic)
    part = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    if what == "summary":
        fams = collections.Counter(family(q["id"]) for q in qs)
        print(len(qs), "questions")
        for k, v in sorted(fams.items()):
            print("  %-14s %d" % (k, v))
        shapes = collections.defaultdict(list)
        for i, q in enumerate(qs):
            shapes[shape(q["questionText"])].append(i)
        print(len(shapes), "wordings")
        for s, idx in sorted(shapes.items(), key=lambda kv: -len(kv[1])):
            if len(idx) > 1:
                print("  %3d x  %s   [%s]" % (len(idx), s[:150], ",".join(str(i) for i in idx[:6])))
        print("difficulty", collections.Counter(q.get("difficulty") for q in qs))
    elif what in ("full", "brief"):
        a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        b = int(sys.argv[4]) if len(sys.argv) > 4 else len(qs) - 1
        for i, q in enumerate(qs):
            if a <= i <= b:
                if what == "full":
                    full(q, i)
                else:
                    print(i, q["id"], "|", q.get("difficulty"), "|", q["questionText"][:170].replace("\n", " "), "||",
                          " | ".join(opt(o) for o in q.get("options", [])), "| KEY", q.get("correctAnswer"))
    elif what == "missing":
        have = {}
        if os.path.exists(part):
            with io.open(part, encoding="utf-8") as f:
                have = json.load(f)
        miss = [(i, q["id"]) for i, q in enumerate(qs) if q["id"] not in have]
        print(len(miss), "missing of", len(qs))
        for i, qid in miss:
            print(i, qid)
    elif what == "fig":
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
        with io.open(path, encoding="utf-8") as f:
            figs = json.load(f)
        for qid in sys.argv[3:]:
            print(qid, json.dumps(figs.get(qid), ensure_ascii=False))
    elif what == "id":
        for q in qs:
            if q["id"] in sys.argv[3:]:
                full(q)


if __name__ == "__main__":
    main()
