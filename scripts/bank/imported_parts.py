"""Split the Grade 5 questions that came in from the database into parts for review work.

    python -X utf8 scripts/bank/imported_parts.py <name> <how many parts>

Writes data/bank-import/<name>/in-NN.json: for each imported question its id, current
topic id and name, difficulty, text, options, keyed answer, hints and steps. Also prints
how many of them have no hints or no steps. Reads the bank; changes nothing in it.
"""
import io
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402

IMPORTED_SOURCES = ("ai_generated", "ipm_textbook", "official_ipm_2020")


def imported():
    return [q for q in bank.load_bank(5) if q.get("source") in IMPORTED_SOURCES]


def main():
    name = sys.argv[1]
    parts = int(sys.argv[2])
    rows = sorted(imported(), key=lambda q: (q.get("node") or "", q["id"]))
    names = {n["id"]: n["name"] for n in bank.tree_nodes(5)}
    no_hints = [q for q in rows if not [h for h in (q.get("hints") or []) if str(h).strip()]]
    no_steps = [q for q in rows if not (q.get("stepByStep") or [])]
    few_hints = [q for q in rows if 0 < len([h for h in (q.get("hints") or []) if str(h).strip()]) < 3]
    print("%d imported Grade 5 questions; %d with no hints, %d with fewer than three, %d with no steps" % (
        len(rows), len(no_hints), len(few_hints), len(no_steps)))
    out = os.path.join(bank.ROOT, "data", "bank-import", name)
    if not os.path.isdir(out):
        os.makedirs(out)
    size = (len(rows) + parts - 1) // parts
    for i in range(parts):
        chunk = rows[i * size:(i + 1) * size]
        data = [{
            "id": q["id"], "topic": q.get("node"), "topicName": names.get(q.get("node")),
            "difficulty": q.get("difficulty"), "question": q.get("questionText"),
            "options": {o["id"]: o["text"] for o in q["options"]}, "answer": q.get("correctAnswer"),
            "hints": q.get("hints") or [], "steps": q.get("stepByStep") or [],
        } for q in chunk]
        with io.open(os.path.join(out, "in-%02d.json" % (i + 1)), "w", encoding="utf-8", newline="\n") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("  in-%02d.json  %d questions" % (i + 1, len(chunk)))
    print("topics: " + ", ".join("%s (%s)" % (k, v) for k, v in names.items()))


if __name__ == "__main__":
    main()
