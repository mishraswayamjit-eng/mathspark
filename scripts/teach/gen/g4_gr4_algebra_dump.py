"""Print Grade 4 algebra questions, for reading while lessons are written.

    python -X utf8 scripts/teach/gen/g4_gr4_algebra_dump.py ids            # one line per question
    python -X utf8 scripts/teach/gen/g4_gr4_algebra_dump.py full <prefix>  # full text, ids starting with prefix
    python -X utf8 scripts/teach/gen/g4_gr4_algebra_dump.py missing        # full text, questions with no lesson
    python -X utf8 scripts/teach/gen/g4_gr4_algebra_dump.py range <a> <b>  # full text, questions a..b of the sorted list
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

NODE = "gr4_algebra"
OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-gr4_algebra.json")


def questions():
    return sorted([q for q in bank.load_bank(4) if q.get("node") == NODE], key=lambda q: q["id"])


def opt_texts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def full(q):
    print("=" * 70)
    print(q["id"], "|", q.get("subTopic"), "|", q.get("difficulty"), "|", q.get("source"))
    print("Q:", q["questionText"])
    for letter, t in zip("ABCD", opt_texts(q)):
        print("   %s) %s" % (letter, t))
    print("KEY:", q.get("correctAnswer"))
    for h in q.get("hints") or []:
        print("HINT:", h)
    for s in q.get("stepByStep") or []:
        print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
    for k, v in sorted((q.get("misconceptions") or {}).items()):
        print("MIS %s: %s" % (k, v))


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "ids"
    qs = questions()
    if what == "ids":
        for i, q in enumerate(qs):
            print("%3d %-28s %-6s %s || %s || %s" % (i, q["id"], q.get("difficulty"), q["questionText"][:110].replace("\n", " "),
                                               " | ".join(opt_texts(q))[:60], q.get("correctAnswer")))
    elif what == "full":
        for q in qs:
            if q["id"].startswith(sys.argv[2]):
                full(q)
    elif what == "range":
        for q in qs[int(sys.argv[2]):int(sys.argv[3])]:
            full(q)
    elif what == "figs":
        path = os.path.join(ROOT, "data", "question-figures", "parts", "g4-gr4_algebra.json")
        with io.open(path, encoding="utf-8") as f:
            figs = json.load(f)
        for q in qs:
            spec = (figs.get(q["id"]) or {}).get("figure")
            if spec and not q["id"].startswith(("VAR", "BOOST")) and "_V" not in q["id"]:
                print(q["id"], json.dumps(spec, ensure_ascii=False))
    elif what == "missing":
        have = {}
        if os.path.exists(OUT):
            with io.open(OUT, encoding="utf-8") as f:
                have = json.load(f)
        for q in qs:
            if q["id"] not in have:
                full(q)
    print(len(qs), "questions in", NODE)


if __name__ == "__main__":
    main()
