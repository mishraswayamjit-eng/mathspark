"""Move imported Grade 5 questions to the topic a reviewer judged right.

    python -X utf8 scripts/fixes/apply_retag.py            # report only
    python -X utf8 scripts/fixes/apply_retag.py --write

Reads data/bank-import/retag/out-NN.json (one entry per question: id, topic id, why).
For a question whose reviewed topic differs from its current one, sets `node` and gives it
the label of the new topic in the form the imported questions already use,
"Grade 5 — <Topic name> (<key>)", which the app's topic matching reaches. Only `node` and
`subTopic` change. A move is refused if the new label would be reached by another topic too.
"""
import collections
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

RETAG = os.path.join(ROOT, "data", "bank-import", "retag")


def main():
    nodes = bank.tree_nodes(5)
    by_node = {n["id"]: n for n in nodes}
    reviewed = {}
    for path in sorted(glob.glob(os.path.join(RETAG, "out-*.json"))):
        with io.open(path, encoding="utf-8") as f:
            for row in json.load(f):
                reviewed[row["id"]] = row
    questions = bank.load_bank()
    moves = collections.Counter()
    refused = []
    changed = 0
    examples = collections.defaultdict(list)
    for q in questions:
        r = reviewed.get(q["id"])
        if not r or r.get("topic") == q.get("node"):
            continue
        target = by_node.get(r.get("topic"))
        if target is None or target.get("db") != q.get("topicId") and target.get("dbTopicId") != q.get("topicId"):
            refused.append((q["id"], "unknown topic %r" % r.get("topic")))
            continue
        key = target.get("key") or target.get("subTopicKey")
        # The usual label first; if another topic's key also reaches it (the name
        # "Decimal Fractions" is reached by Fractions too), a plain label from the key.
        label, got, reach = None, None, []
        for attempt in ("Grade 5 — %s (%s)" % (target["name"], key), "Grade 5 — %s" % key.capitalize()):
            trial = dict(q)
            trial["subTopic"] = attempt
            got = bank.assign_node(trial, bank.tree_nodes())
            reach = [n["id"] for n in bank.candidate_nodes(trial, bank.tree_nodes())]
            label = attempt
            if got == target["id"] and len(reach) == 1:
                break
        if got != target["id"] or len(reach) != 1:
            refused.append((q["id"], "label %r is reached by %s" % (label, reach)))
            continue
        moves[(q.get("node"), target["id"])] += 1
        if len(examples[(q.get("node"), target["id"])]) < 2:
            examples[(q.get("node"), target["id"])].append("%s  (%s)" % ((q.get("questionText") or "")[:90], r.get("why")))
        q["node"] = target["id"]
        q["subTopic"] = label
        changed += 1

    names = {n["id"]: n["name"] for n in nodes}
    print("%d questions reviewed, %d to move, %d refused" % (len(reviewed), changed, len(refused)))
    for (a, b), n in moves.most_common():
        print("  %3d  %-28s -> %s" % (n, names.get(a, a), names.get(b, b)))
        for e in examples[(a, b)]:
            print("          %s" % e)
    for qid, why in refused[:20]:
        print("  REFUSED %s: %s" % (qid, why))
    after = collections.Counter(q.get("node") for q in questions if q.get("topicId") == "grade5")
    print("\nGrade 5 questions per topic after the moves:")
    for n in nodes:
        print("  %-34s %4d" % (n["name"], after.get(n["id"], 0)))
    if "--write" not in sys.argv:
        print("\nnothing written (use --write)")
        return
    bank.save_bank(questions)
    print("\nbank written")


if __name__ == "__main__":
    main()
