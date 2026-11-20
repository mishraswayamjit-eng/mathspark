"""Print Grade 4 questions of a topic in full, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_time_dump.py gr4_time list            # one line per question
    python -X utf8 scripts/teach/gen/g4_gr4_time_dump.py gr4_time full A B        # questions number A to B in full
    python -X utf8 scripts/teach/gen/g4_gr4_time_dump.py gr4_time missing A B     # questions with no lesson yet
    python -X utf8 scripts/teach/gen/g4_gr4_time_dump.py gr4_time figs A B        # figure specs for questions A to B
    python -X utf8 scripts/teach/gen/g4_gr4_time_dump.py gr4_time say A B         # lessons A to B, as spoken
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def questions(topic):
    return [q for q in bank.load_bank(4) if q.get("node") == topic]


def part(topic):
    path = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % topic)
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def figures(topic):
    path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % topic)
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def otext(o):
    return o.get("text", "") if isinstance(o, dict) else str(o)


def full(q, figs):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"), "| FIG" if q["id"] in figs else "")
    print("Q:", q["questionText"])
    print("OPTS:", " | ".join(otext(o) for o in q.get("options", [])), "  KEY:", q.get("correctAnswer"))
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", ""))
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))


def main():
    topic = sys.argv[1]
    what = sys.argv[2] if len(sys.argv) > 2 else "list"
    a = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    b = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 6
    qs = questions(topic)
    figs = figures(topic)
    if what == "list":
        for i, q in enumerate(qs):
            if a <= i <= b:
                print("%3d %s | %s | %s | %s%s | %s" % (i, q["id"], q.get("subTopic"), q.get("difficulty"), q.get("source"),
                                                    " | FIG" if q["id"] in figs else "", q["questionText"][:90].replace("\n", " ")))
        print(len(qs), "questions")
    elif what == "full":
        for q in qs[a:b + 1]:
            full(q, figs)
    elif what == "missing":
        have = part(topic)
        left = [q for q in qs if q["id"] not in have]
        for q in left[a:b + 1]:
            full(q, figs)
        print(len(left), "missing")
    elif what == "figs":
        for q in qs[a:b + 1]:
            if q["id"] in figs:
                print(q["id"], json.dumps(figs[q["id"]], ensure_ascii=False))
    elif what == "say":
        have = part(topic)
        for q in qs[a:b + 1]:
            print("=" * 70)
            print(q["id"], "|", q.get("difficulty"))
            print("Q:", q["questionText"])
            print("OPTS:", " | ".join(otext(o) for o in q.get("options", [])), "  KEY:", q.get("correctAnswer"))
            for i, beat in enumerate(have.get(q["id"], {}).get("beats", [])):
                print(" %2d  %s" % (i + 1, beat["say"]))
                for op in beat.get("board", []):
                    if op["op"] == "figure":
                        print("       [figure] %s" % op["spec"].get("kind"))
                        continue
                    rest = {k: v for k, v in op.items() if k != "op"}
                    print("       [%s] %s" % (op["op"], json.dumps(rest, ensure_ascii=False)))
                if beat.get("ask"):
                    ask = beat["ask"]
                    if ask["kind"] == "choose":
                        print("       ASK %s -> %d | %s" % (ask["choices"], ask["answer"], ask["ifNot"]))
                    else:
                        print("       ASK think")


if __name__ == "__main__":
    main()
