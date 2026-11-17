"""Write the second-round review inputs for Grade 4.

    python -X utf8 scripts/fixes/g4_verify_inputs.py

  data/bank-import/g4/blind-in-N.json     every original whose key the first reviewer did not
                                          simply confirm, WITHOUT the key or the first verdict,
                                          to be solved blind by a second reviewer
  data/bank-import/g4/variants-in-NN.json every variant of an original, with its key and steps,
                                          for its own answer to be checked
Reads the bank and originals-out-*.json; changes nothing.
"""
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402

OUT = g4.OUT


def main():
    rows = bank.load_bank(4)
    by_id = {q["id"]: q for q in rows}
    verdict = {}
    for path in sorted(glob.glob(os.path.join(OUT, "originals-out-*.json"))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                verdict[row["id"]] = row

    doubt = sorted(qid for qid, v in verdict.items() if v["answerOk"] != "yes")
    parts = 2
    size = (len(doubt) + parts - 1) // parts
    for i in range(parts):
        chunk = doubt[i * size:(i + 1) * size]
        g4.dump("blind-in-%d.json" % (i + 1), [{
            "id": qid, "question": by_id[qid].get("questionText"),
            "options": {o["id"]: o["text"] for o in by_id[qid]["options"]},
        } for qid in chunk])
        print("blind-in-%d.json  %d questions" % (i + 1, len(chunk)))

    variants = sorted([q for q in rows if g4.family(q)[0] == "variant"], key=lambda q: (g4.family(q)[1], q["id"]))
    parts = 8
    size = (len(variants) + parts - 1) // parts
    for i in range(parts):
        chunk = variants[i * size:(i + 1) * size]
        out = []
        for q in chunk:
            parent = by_id.get(g4.family(q)[1])
            out.append({
                "id": q["id"], "parent": g4.family(q)[1],
                "parentQuestion": (parent or {}).get("questionText"),
                "question": q.get("questionText"), "options": {o["id"]: o["text"] for o in q["options"]},
                "answer": q.get("correctAnswer"),
                "steps": [(s.get("text") if isinstance(s, dict) else s) for s in (q.get("stepByStep") or [])][:5],
            })
        g4.dump("variants-in-%02d.json" % (i + 1), out)
        print("variants-in-%02d.json  %d variants" % (i + 1, len(out)))


if __name__ == "__main__":
    main()
