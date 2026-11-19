"""New Grade 4 questions: give them ids, send them for a blind check, and add the agreed ones.

    python -X utf8 scripts/fixes/g4_new_questions.py gate       # write the blind-check inputs (questions not yet in the bank)
    python -X utf8 scripts/fixes/g4_new_questions.py report     # compare writers and blind reviewers
    python -X utf8 scripts/fixes/g4_new_questions.py add        # add the agreed questions to the bank

The writers' files are data/bank-import/g4/new-N.json (each answer computed by the writer's
script). Ids are G4A_<topic>_<n>, numbered in the order written; the source is 'g4_authored'.

Two rounds have used this script:
  round 1 (sets 1-6)  one blind solver per question (blind-new-out-*.json); the question was
                      added when the solver reached the same option and raised no objection.
                      Its difficulty was settled later, with the rest of the bank.
  round 2 (sets 7+)   TWO blind reviewers per question (gate-out-*-A.json, gate-out-*-B.json),
                      each solving it and rating its difficulty against the rubric. A question
                      is added when both reach the writer's option and neither objects. Its
                      difficulty is the LOWER of the two ratings, so it is Hard only if both
                      reviewers rate it Hard, whatever the writer intended.
Every question added is kept in scripts/fixes/g4_authored.json.
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

# The grade is the second argument (4 unless given): gate 5, report 5, add 5.
GRADE = int(sys.argv[2]) if len(sys.argv) > 2 else 4
G4 = os.path.join(os.path.dirname(g4.OUT), "g%d" % GRADE)   # the grade's review folder
g4.OUT = G4
RECORD = os.path.join(ROOT, "scripts", "fixes", "g%d_authored.json" % GRADE)
SOURCE = "g%d_authored" % GRADE
# The blind solver marked these "above Grade 4" for using the circumference or area of a
# circle; the real Grade 4 papers use both (with pi = 22/7), so they are accepted.
ACCEPT_FIT = {"G4A_CIRCLE_015", "G4A_CIRCLE_021", "G4A_CIRCLE_022", "G4A_CIRCLE_025"}
# Let through by the blind solver with a note, but held back on a second look.
HOLD = {
    "G4A_DECIMALS_026": "'How many tenths are there in 3.7?' can fairly be read as the tenths digit, which is an option",
}
LETTERS = "ABCD"
RANK = {"Easy": 0, "Medium": 1, "Hard": 2}


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def written():
    """Every new question, with its id, in a fixed order."""
    out = []
    counters = collections.Counter()
    paths = [p for p in glob.glob(os.path.join(G4, "new-*.json")) if re.search(r"new-(\d+)\.json$", p)]
    for path in sorted(paths, key=lambda p: int(re.search(r"new-(\d+)\.json$", p).group(1))):
        for p in load(path):
            counters[p["topic"]] += 1
            qid = "G%dA_%s_%03d" % (GRADE, p["topic"].replace("gr%d_" % GRADE, "").upper(), counters[p["topic"]])
            out.append((qid, p))
    return out


def to_bank(qid, p, nodes, difficulty):
    node = nodes[p["topic"]]
    label = node["name"]
    if node.get("key"):
        # A label the topic's key reaches and no other topic's does.
        tree = bank.tree_nodes()
        for attempt in ("Grade %d — %s" % (GRADE, node["name"]), "Grade %d — %s (%s)" % (GRADE, node["name"], node["key"]),
                        "Grade %d — %s" % (GRADE, node["key"].capitalize())):
            trial = {"id": qid, "topicId": node["db"], "subTopic": attempt}
            label = attempt
            if bank.assign_node(trial, tree) == p["topic"] and len(bank.candidate_nodes(trial, tree)) == 1:
                break
    return {
        "id": qid, "node": p["topic"], "topicId": node["db"],
        "subTopic": label,
        "difficulty": difficulty, "questionText": p["question"], "questionLatex": "",
        "options": [{"id": LETTERS[i], "text": str(t)} for i, t in enumerate(p["options"])],
        "correctAnswer": LETTERS[p["answer"]],
        "hints": list(p["hints"]),
        "stepByStep": [dict([("step", i + 1), ("text", s["text"])] + ([("latex", s["latex"])] if s.get("latex") else []))
                       for i, s in enumerate(p["steps"])],
        "misconceptions": {LETTERS[i]: n for i, n in enumerate(p["notes"])},
        "source": SOURCE,
    }


def rows_of(pattern):
    out = {}
    for path in sorted(glob.glob(os.path.join(G4, pattern))):
        for row in load(path):
            out[row["id"]] = row
    return out


def judge(qid, p, round1, gate_a, gate_b):
    """(level, None) when the question passes; (None, why) when it is held back or not yet checked."""
    key = LETTERS[p["answer"]]
    if qid in HOLD:
        return None, HOLD[qid]
    if qid in round1:
        v = round1[qid]
        if v.get("answer") != key:
            return None, "writer says %s; blind solver says %s: %s" % (key, v.get("answer"), v.get("working") or "")
        if v.get("fit") != "ok" and qid not in ACCEPT_FIT:
            return None, "blind solver objects: %s" % (v.get("objection") or v.get("fit"))
        return p["difficulty"], None
    a, b = gate_a.get(qid), gate_b.get(qid)
    if a is None or b is None:
        return None, "not checked yet"
    for name, v in (("A", a), ("B", b)):
        if v.get("answer") != key:
            return None, "writer says %s (%s); reviewer %s says %s: %s" % (key, p["options"][p["answer"]], name, v.get("answer"), v.get("working") or "")
        if v.get("fit") != "ok":
            return None, "reviewer %s objects (%s): %s" % (name, v.get("fit"), v.get("objection") or "")
    return min((a["level"], b["level"]), key=RANK.get), None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "report"
    nodes = {n["id"]: n for n in bank.tree_nodes(GRADE)}
    rows = written()
    questions = bank.load_bank()
    have = {q["id"] for q in questions}
    round1 = rows_of("blind-new-out-*.json")
    gate_a, gate_b = rows_of("gate-out-*-A.json"), rows_of("gate-out-*-B.json")

    if mode == "gate":
        todo = [(qid, p) for qid, p in rows if qid not in have and qid not in round1]
        todo.sort(key=lambda r: (int(r[0].rsplit("_", 1)[1]), r[0]))  # mix topics across parts
        parts = max(1, (len(todo) + 119) // 120)
        size = (len(todo) + parts - 1) // parts
        for i in range(parts):
            chunk = todo[i * size:(i + 1) * size]
            g4.dump("gate-in-%d.json" % (i + 1), [{
                "id": qid, "topic": nodes[p["topic"]]["name"],
                "question": p["question"], "options": {LETTERS[j]: str(t) for j, t in enumerate(p["options"])},
            } for qid, p in chunk])
            print("gate-in-%d.json  %d questions" % (i + 1, len(chunk)))
        return

    agreed, held = [], []
    for qid, p in rows:
        level, why = judge(qid, p, round1, gate_a, gate_b)
        if level is None:
            held.append((qid, why))
        else:
            agreed.append((qid, p, level))
    new = [(qid, p, level) for qid, p, level in agreed if qid not in have]
    print("%d written; %d passed the blind check (%d already in the bank, %d to add); %d held back" % (
        len(rows), len(agreed), len(agreed) - len(new), len(new), len(held)))
    if new:
        aimed = collections.Counter((p["difficulty"], level) for _, p, level in new)
        print("to add, writer's aim -> settled level: " + ", ".join("%s -> %s: %d" % (a, s, n) for (a, s), n in sorted(aimed.items())))
        by_topic = collections.defaultdict(collections.Counter)
        for _, p, level in new:
            by_topic[p["topic"]][level] += 1
        for t, c in sorted(by_topic.items(), key=lambda kv: nodes[kv[0]]["name"]):
            print("   %-30s Easy %2d  Medium %2d  Hard %2d" % (nodes[t]["name"][:30], c["Easy"], c["Medium"], c["Hard"]))
    for qid, why in held[:60]:
        if why != "not checked yet":
            print("  HELD %s: %s" % (qid, why[:230]))
    waiting = sum(1 for _, why in held if why == "not checked yet")
    if waiting:
        print("  %d not checked yet" % waiting)
    if mode != "add":
        return

    texts = {re.sub(r"[^a-z0-9]+", " ", (q.get("questionText") or "").lower()).strip() for q in questions if str(q.get("node") or "").startswith("gr%d_" % GRADE)}
    record = load(RECORD) if os.path.exists(RECORD) else {}
    added = 0
    for qid, p, level in new:
        row = to_bank(qid, p, nodes, level)
        if re.sub(r"[^a-z0-9]+", " ", row["questionText"].lower()).strip() in texts:
            continue
        if bank.assign_node(row, bank.tree_nodes()) != p["topic"]:
            raise SystemExit("%s does not land in %s" % (qid, p["topic"]))
        questions.append(row)
        record[qid] = row
        added += 1
    bank.save_bank(questions)
    with io.open(RECORD, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(record.items())), f, ensure_ascii=False, indent=0)
        f.write("\n")
    print("added %d questions to the bank; record (%d in all) in %s" % (added, len(record), os.path.relpath(RECORD, ROOT)))


if __name__ == "__main__":
    main()
