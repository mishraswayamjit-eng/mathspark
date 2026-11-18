"""Write, for each Grade 4 topic, the questions the bank already has (for writers of new ones).

    python -X utf8 scripts/fixes/g4_topic_context.py

data/bank-import/g4/topic-<node id>.json: [{ id, source, real (a real exam question),
difficulty, question, options, rightAnswer }]. Reads the bank; changes nothing.
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bank"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import bank  # noqa: E402
import g4_classify_inputs as g4  # noqa: E402


def main():
    rows = bank.load_bank(4)
    for n in bank.tree_nodes(4):
        qs = [q for q in rows if q.get("node") == n["id"]]
        g4.dump("topic-%s.json" % n["id"], [{
            "id": q["id"], "source": q.get("source"),
            "real": (q.get("source") or "").startswith(("g4_mse_final", "previous_year")),
            "difficulty": q.get("difficulty"), "question": q.get("questionText"),
            "options": [o["text"] for o in q["options"]],
            "rightAnswer": next((o["text"] for o in q["options"] if o["id"] == q.get("correctAnswer")), ""),
        } for q in qs])
        print("topic-%s.json  %d" % (n["id"], len(qs)))


if __name__ == "__main__":
    main()
