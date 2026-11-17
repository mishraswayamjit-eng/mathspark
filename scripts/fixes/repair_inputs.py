"""Write the review inputs for repairing the imported Grade 5 questions.

    python -X utf8 scripts/fixes/repair_inputs.py

Under data/bank-import/repairs/:
  hints-in-NN.json   (8 files) every imported question with its hints and step texts
  dedupe-in-N.json   (3 files) the AI-written questions, grouped by topic, for finding
                     the same template repeated with different numbers
Reads the bank; changes nothing in it.
"""
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

OUT = os.path.join(ROOT, "data", "bank-import", "repairs")
IMPORTED = ("ai_generated", "ipm_textbook", "official_ipm_2020")
FIGURES = os.path.join(ROOT, "src", "data", "questionFigures", "figures.json")


def dump(name, data):
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    names = {n["id"]: n["name"] for n in bank.tree_nodes(5)}
    rows = sorted([q for q in bank.load_bank(5) if q.get("source") in IMPORTED], key=lambda q: (q.get("node") or "", q["id"]))
    with io.open(FIGURES, encoding="utf-8") as f:
        figures = json.load(f)

    parts = 8
    size = (len(rows) + parts - 1) // parts
    for i in range(parts):
        chunk = rows[i * size:(i + 1) * size]
        dump("hints-in-%02d.json" % (i + 1), [{
            "id": q["id"], "topic": names.get(q.get("node")), "source": q.get("source"),
            "question": q.get("questionText"), "options": {o["id"]: o["text"] for o in q["options"]},
            "answer": q.get("correctAnswer"), "hints": q.get("hints") or [],
            "steps": [(s.get("text") if isinstance(s, dict) else s) for s in (q.get("stepByStep") or [])],
        } for q in chunk])
        print("hints-in-%02d.json   %d questions" % (i + 1, len(chunk)))

    ai = [q for q in rows if q.get("source") == "ai_generated"]
    groups = 3
    gsize = (len(ai) + groups - 1) // groups
    for i in range(groups):
        chunk = ai[i * gsize:(i + 1) * gsize]
        dump("dedupe-in-%d.json" % (i + 1), [{
            "id": q["id"], "topic": names.get(q.get("node")), "difficulty": q.get("difficulty"),
            "question": q.get("questionText"),
            "rightAnswer": next((o["text"] for o in q["options"] if o["id"] == q.get("correctAnswer")), ""),
            "hasFigure": q["id"] in figures,
        } for q in chunk])
        print("dedupe-in-%d.json    %d questions (%s .. %s)" % (i + 1, len(chunk), names.get(chunk[0].get("node")), names.get(chunk[-1].get("node"))))


if __name__ == "__main__":
    main()
