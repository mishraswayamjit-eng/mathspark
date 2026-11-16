"""List the Grade 5 worksheet questions extracted from PDFs, for authoring.
    python -X utf8 scripts/figures/authoring/c_list.py [start] [end]
"""
import io, json, os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)


def load():
    qs = bank.load_bank()
    return [q for q in qs if q.get("topicId") == "grade5" and q.get("source") == "pdf_extracted"]


if __name__ == "__main__":
    qs = load()
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    b = int(sys.argv[2]) if len(sys.argv) > 2 else len(qs)
    for q in qs[a:b]:
        print("## %s [%s] ans=%s" % (q["id"], q.get("subTopic", "")[10:], q["correctAnswer"]))
        print("Q: " + q["questionText"].replace("\n", " / "))
        print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
        for i, s in enumerate(q.get("stepByStep") or []):
            print("  s%d: %s" % (i, s.get("text", "").replace("\n", " / ")))
