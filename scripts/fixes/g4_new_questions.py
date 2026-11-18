"""New Grade 4 questions: give them ids, send them for a blind check, and add the agreed ones.

    python -X utf8 scripts/fixes/g4_new_questions.py blind      # write the blind-check inputs
    python -X utf8 scripts/fixes/g4_new_questions.py report     # compare writers and blind solvers
    python -X utf8 scripts/fixes/g4_new_questions.py add        # add the agreed questions to the bank

The writers' files are data/bank-import/g4/new-N.json (each answer computed by the writer's
script). A question is added only when a second reviewer, given the question and options
but not the answer, independently reaches the same option and raises no objection.
Ids are G4A_<topic>_<n>, numbered in the order written; the source is 'g4_authored'.
The questions added are saved in scripts/fixes/g4_authored.json so the step can be repeated.
"""
import collections
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402

G4 = g4.OUT
RECORD = os.path.join(ROOT, "scripts", "fixes", "g4_authored.json")
SOURCE = "g4_authored"
# The blind solver marked these "above Grade 4" for using the circumference or area of a
# circle; the real Grade 4 papers use both (with pi = 22/7), so they are accepted.
ACCEPT_FIT = {"G4A_CIRCLE_015", "G4A_CIRCLE_021", "G4A_CIRCLE_022", "G4A_CIRCLE_025"}
# Let through by the blind solver with a note, but held back on a second look.
HOLD = {
    "G4A_DECIMALS_026": "'How many tenths are there in 3.7?' can fairly be read as the tenths digit, which is an option",
}
LETTERS = "ABCD"


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def written():
    """Every new question, with its id, in a fixed order."""
    out = []
    counters = collections.Counter()
    for path in sorted(glob.glob(os.path.join(G4, "new-[0-9].json"))):
        for p in load(path):
            counters[p["topic"]] += 1
            qid = "G4A_%s_%03d" % (p["topic"].replace("gr4_", "").upper(), counters[p["topic"]])
            out.append((qid, p))
    return out


def to_bank(qid, p, nodes):
    node = nodes[p["topic"]]
    return {
        "id": qid, "node": p["topic"], "topicId": node["db"],
        "subTopic": ("Grade 4 — %s" % node["name"]) if node.get("key") else node["name"],
        "difficulty": p["difficulty"], "questionText": p["question"], "questionLatex": "",
        "options": [{"id": LETTERS[i], "text": str(t)} for i, t in enumerate(p["options"])],
        "correctAnswer": LETTERS[p["answer"]],
        "hints": list(p["hints"]),
        "stepByStep": [dict([("step", i + 1), ("text", s["text"])] + ([("latex", s["latex"])] if s.get("latex") else []))
                       for i, s in enumerate(p["steps"])],
        "misconceptions": {LETTERS[i]: n for i, n in enumerate(p["notes"])},
        "source": SOURCE,
    }


def verdicts():
    out = {}
    for path in sorted(glob.glob(os.path.join(G4, "blind-new-out-*.json"))):
        for row in load(path):
            out[row["id"]] = row
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    nodes = {n["id"]: n for n in bank.tree_nodes(4)}
    rows = written()
    if mode == "blind":
        parts = 4
        mixed = sorted(rows, key=lambda r: (int(r[0].rsplit("_", 1)[1]), r[0]))  # mix topics across parts
        size = (len(mixed) + parts - 1) // parts
        for i in range(parts):
            chunk = mixed[i * size:(i + 1) * size]
            g4.dump("blind-new-in-%d.json" % (i + 1), [{
                "id": qid, "topic": nodes[p["topic"]]["name"], "labelledDifficulty": p["difficulty"],
                "question": p["question"], "options": {LETTERS[j]: str(t) for j, t in enumerate(p["options"])},
            } for qid, p in chunk])
            print("blind-new-in-%d.json  %d questions" % (i + 1, len(chunk)))
        return

    seen = verdicts()
    agreed, held = [], []
    for qid, p in rows:
        v = seen.get(qid)
        key = LETTERS[p["answer"]]
        if v is None:
            held.append((qid, "not checked yet"))
        elif v.get("answer") != key:
            held.append((qid, "writer says %s (%s); blind solver says %s: %s" % (key, p["options"][p["answer"]], v.get("answer"), v.get("working") or "")))
        elif qid in HOLD:
            held.append((qid, HOLD[qid]))
        elif v.get("fit") != "ok" and qid not in ACCEPT_FIT:
            held.append((qid, "blind solver agrees on the answer but objects: %s" % (v.get("objection") or v.get("fit"))))
        else:
            agreed.append((qid, p, v))
    print("%d written; %d agreed by the blind solver; %d held back" % (len(rows), len(agreed), len(held)))
    by_topic = collections.Counter(p["topic"] for _, p, _ in agreed)
    relabel = sum(1 for _, p, v in agreed if v.get("difficulty") in ("Easy", "Medium", "Hard") and v["difficulty"] != p["difficulty"])
    print("agreed, by topic: " + ", ".join("%s %d" % (nodes[t]["name"], n) for t, n in by_topic.most_common()))
    print("difficulty the blind solver would label differently: %d" % relabel)
    for qid, why in held[:60]:
        print("  HELD %s: %s" % (qid, why[:220]))
    if mode != "add":
        return

    questions = bank.load_bank()
    have = {q["id"] for q in questions}
    texts = {re.sub(r"[^a-z0-9]+", " ", (q.get("questionText") or "").lower()).strip() for q in questions if q.get("topicId") == "grade4" or q.get("node", "") and str(q.get("node")).startswith("gr4_")}
    added = []
    for qid, p, v in agreed:
        row = to_bank(qid, p, nodes)
        if qid in have or re.sub(r"[^a-z0-9]+", " ", row["questionText"].lower()).strip() in texts:
            continue
        if bank.assign_node(row, bank.tree_nodes()) != p["topic"]:
            raise SystemExit("%s does not land in %s" % (qid, p["topic"]))
        questions.append(row)
        added.append(row)
    bank.save_bank(questions)
    with io.open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        json.dump({r["id"]: r for r in added}, f, ensure_ascii=False, indent=0)
        f.write("\n")
    print("added %d questions to the bank; record in %s" % (len(added), os.path.relpath(RECORD, ROOT)))


if __name__ == "__main__":
    main()
