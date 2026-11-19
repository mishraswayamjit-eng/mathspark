"""Print the questions of part authored-01 for reading (a writer's aid; writes nothing).

    python -X utf8 scripts/teach/gen/authored_01_dump.py [substring of id] [full]
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402


def main():
    with io.open(os.path.join(ROOT, "data", "bank-import", "g5", "lessons-ids-1.json"), encoding="utf-8") as f:
        ids = json.load(f)
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    full = len(sys.argv) > 2
    qs = {q["id"]: q for q in bank.load_bank(5) if q["id"] in set(ids)}
    for qid in ids:
        if want not in qid:
            continue
        q = qs[qid]
        print("=" * 8, qid, q.get("difficulty"), "|", q.get("subTopic"))
        print("Q:", q["questionText"])
        opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q["options"]]
        print("OPTS:", " | ".join(opts), "  KEY", q["correctAnswer"])
        for s in q.get("stepByStep") or []:
            print("  STEP:", s.get("text", "") if isinstance(s, dict) else s)
        if full:
            for h in q.get("hints") or []:
                print("  HINT:", h)
            print("  MISC:", json.dumps(q.get("misconceptions"), ensure_ascii=False))
            extra = {k: v for k, v in q.items() if k not in ("id", "questionText", "options", "correctAnswer", "stepByStep", "hints", "misconceptions", "difficulty", "subTopic")}
            print("  REST:", json.dumps(extra, ensure_ascii=False)[:400])


if __name__ == "__main__":
    main()
