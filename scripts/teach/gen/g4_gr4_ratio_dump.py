"""Print Grade 4 questions of one topic, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_ratio_dump.py <topic> ids              # id, difficulty, source, short text
    python -X utf8 scripts/teach/gen/g4_gr4_ratio_dump.py <topic> full <from> <to>  # questions from..to in full
    python -X utf8 scripts/teach/gen/g4_gr4_ratio_dump.py <topic> missing          # ids with no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_ratio_dump.py <topic> id <question id> # one question in full
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def opts(q):
    return [(o.get("text", "") if isinstance(o, dict) else str(o)) for o in q.get("options", [])]


def full(q, n):
    print("=" * 70)
    print(n, q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"))
    print("Q:", q["questionText"])
    print("OPTS:", " | ".join(opts(q)), " KEY:", q.get("correctAnswer"))
    for h in q.get("hints") or []:
        print("HINT:", h)
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))


def main():
    topic = sys.argv[1]
    what = sys.argv[2] if len(sys.argv) > 2 else "ids"
    qs = [q for q in bank.load_bank(4) if q.get("node") == topic]
    if what == "ids":
        for n, q in enumerate(qs):
            print(n, q["id"], "|", q.get("difficulty"), "|", q.get("source"), "|", q["questionText"][:150].replace("\n", " "))
    elif what == "full":
        a, b = int(sys.argv[3]), int(sys.argv[4])
        for n, q in enumerate(qs):
            if a <= n < b:
                full(q, n)
    elif what == "id":
        for n, q in enumerate(qs):
            if q["id"] == sys.argv[3]:
                full(q, n)
    elif what == "missing":
        path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
        have = {}
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as f:
                have = json.load(f)
        for n, q in enumerate(qs):
            if q["id"] not in have:
                print(n, q["id"], "|", q["questionText"][:110].replace("\n", " "))
    print(len(qs), "questions")


if __name__ == "__main__":
    main()
