"""Print the questions of part 03 so their lessons can be written.

    python -X utf8 scripts/teach/gen/authored_03_dump.py <start> <count>
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
    with io.open(os.path.join(ROOT, "data", "bank-import", "g5", "lessons-ids-3.json"), encoding="utf-8") as f:
        ids = json.load(f)
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else len(ids)
    qs = {q["id"]: q for q in bank.load_bank(5) if q["id"] in set(ids)}
    for qid in ids[start:start + count]:
        q = qs[qid]
        print("=" * 70)
        print(qid, "|", q.get("difficulty"), "|", q.get("subTopic"))
        print("Q:", q["questionText"])
        for i, o in enumerate(q["options"]):
            t = o.get("text", "") if isinstance(o, dict) else str(o)
            print("  %s) %s%s" % ("ABCD"[i], t, "   <== KEY" if "ABCD"[i] == q["correctAnswer"] else ""))
        for h in q.get("hints") or []:
            print("HINT:", h)
        for s in q.get("stepByStep") or []:
            print("STEP:", s.get("text", "") if isinstance(s, dict) else s)
        m = q.get("misconceptions") or {}
        if isinstance(m, dict):
            for k, v in m.items():
                if v:
                    print("MISC %s: %s" % (k, v))


if __name__ == "__main__":
    main()
