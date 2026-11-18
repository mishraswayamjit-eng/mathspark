"""Write the inputs for rating question difficulty against one rubric.

    python -X utf8 scripts/fixes/difficulty_inputs.py

  data/bank-import/difficulty/g4-in-N.json   every Grade 4 question (4 parts, topics mixed)
  data/bank-import/difficulty/g5cal-in.json  240 Grade 5 real-paper questions, 80 from each
                                             third of the paper, as a like-for-like benchmark
Each entry: id, topic, question, options, rightAnswer, steps (the worked solution).
The current difficulty label is deliberately left out. Reads the bank; changes nothing.
"""
import hashlib
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

OUT = os.path.join(ROOT, "data", "bank-import", "difficulty")
REAL5 = re.compile(r"^g5_final_\d{4}$")


def brief(q, names):
    return {
        "id": q["id"], "topic": names.get(q.get("node")) or "",
        "question": q.get("questionText"), "options": [o["text"] for o in q["options"]],
        "rightAnswer": next((o["text"] for o in q["options"] if o["id"] == q.get("correctAnswer")), ""),
        "steps": [(s.get("text") or "") + ((" [" + s["latex"] + "]") if isinstance(s, dict) and s.get("latex") else "")
                  if isinstance(s, dict) else str(s) for s in (q.get("stepByStep") or [])],
    }


def mix(qid):
    return hashlib.md5(qid.encode("utf-8")).hexdigest()


def dump(name, data):
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    names4 = {n["id"]: n["name"] for n in bank.tree_nodes(4)}
    rows = sorted(bank.load_bank(4), key=lambda q: mix(q["id"]))
    parts = 4
    size = (len(rows) + parts - 1) // parts
    for i in range(parts):
        chunk = rows[i * size:(i + 1) * size]
        dump("g4-in-%d.json" % (i + 1), [brief(q, names4) for q in chunk])
        print("g4-in-%d.json  %d questions" % (i + 1, len(chunk)))

    names5 = {n["id"]: n["name"] for n in bank.tree_nodes(5)}
    thirds = {1: [], 2: [], 3: []}
    for q in sorted(bank.load_bank(5), key=lambda q: mix(q["id"])):
        m = re.search(r"_(\d{1,3})$", q["id"])
        if REAL5.match(q.get("source") or "") and m:
            p = int(m.group(1))
            thirds[1 if p <= 13 else 2 if p <= 26 else 3].append(q)
    sample = thirds[1][:80] + thirds[2][:80] + thirds[3][:80]
    sample.sort(key=lambda q: mix(q["id"] + "x"))
    dump("g5cal-in.json", [brief(q, names5) for q in sample])
    print("g5cal-in.json  %d questions" % len(sample))


if __name__ == "__main__":
    main()
