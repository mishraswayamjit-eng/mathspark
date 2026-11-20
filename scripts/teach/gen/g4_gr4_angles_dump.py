"""Print Grade 4 angles questions, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_angles_dump.py summary
    python -X utf8 scripts/teach/gen/g4_gr4_angles_dump.py texts            # id + difficulty + question text only
    python -X utf8 scripts/teach/gen/g4_gr4_angles_dump.py full 0 15        # everything, a slice
    python -X utf8 scripts/teach/gen/g4_gr4_angles_dump.py id <prefix>      # ids starting with this, in full
    python -X utf8 scripts/teach/gen/g4_gr4_angles_dump.py missing [full]   # questions with no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_angles_dump.py figs <prefix>    # the figure specs for these ids
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

TOPIC = "gr4_angles"
PART = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)
FIGS = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)


def questions():
    return [q for q in bank.load_bank(4) if q.get("node") == TOPIC]


def opt_texts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def full(q):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"))
    print("Q:", q["questionText"])
    for i, t in enumerate(opt_texts(q)):
        print("   ", "ABCD"[i], t)
    print("KEY:", q.get("correctAnswer"))
    for h in q.get("hints") or []:
        print("HINT:", h)
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "summary"
    qs = questions()
    if what == "summary":
        print(len(qs), "questions")
        pre = collections.Counter(re.sub(r"\d+", "#", q["id"]) for q in qs)
        for k, n in sorted(pre.items(), key=lambda kv: -kv[1]):
            print("  %4d  %s" % (n, k))
        print(collections.Counter(q.get("difficulty") for q in qs))
        print(collections.Counter(q.get("source") for q in qs))
        figs = {}
        if os.path.exists(FIGS):
            with io.open(FIGS, encoding="utf-8") as f:
                figs = json.load(f)
        print("with figure entry:", sum(1 for q in qs if q["id"] in figs))
        return
    if what == "texts":
        for q in qs:
            print("%s | %s | %s" % (q["id"], q.get("difficulty"), q["questionText"].replace("\n", " / ")))
            print("      %s  (key %s)" % (" | ".join(opt_texts(q)), q.get("correctAnswer")))
        return
    if what == "figs":
        with io.open(FIGS, encoding="utf-8") as f:
            figs = json.load(f)
        for q in qs:
            if q["id"].startswith(sys.argv[2]) and q["id"] in figs:
                print(q["id"], json.dumps(figs[q["id"]], ensure_ascii=False))
        return
    if what == "missing":
        have = {}
        if os.path.exists(PART):
            with io.open(PART, encoding="utf-8") as f:
                have = json.load(f)
        qs = [q for q in qs if q["id"] not in have]
        for q in qs:
            if len(sys.argv) > 2:
                full(q)
            else:
                print(q["id"], "|", q["questionText"][:110].replace("\n", " / "))
        print(len(qs), "missing")
        return
    if what == "id":
        qs = [q for q in qs if q["id"].startswith(sys.argv[2])]
    total = len(qs)
    if what == "full" and len(sys.argv) > 3:
        qs = qs[int(sys.argv[2]):int(sys.argv[3])]
    for q in qs:
        full(q)
    print(len(qs), "of", total, "questions")


if __name__ == "__main__":
    main()
