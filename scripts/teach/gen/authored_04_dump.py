"""Print the questions of part authored-04 for reading.

    python -X utf8 scripts/teach/gen/authored_04_dump.py [start] [count]
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
    with io.open(os.path.join(ROOT, "data", "bank-import", "g5", "lessons-ids-4.json"), encoding="utf-8") as f:
        ids = json.load(f)
    by = {q["id"]: q for q in bank.load_bank(5) if q["id"] in set(ids)}
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else len(ids)
    for qid in ids[start:start + count]:
        q = by[qid]
        print("=" * 8, qid, q.get("difficulty"), q.get("subTopic"))
        print("Q:", q["questionText"])
        opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q["options"]]
        print("OPTS:", " | ".join(opts), " KEY", q["correctAnswer"])
        for h in q.get("hints") or []:
            print("  H:", h if isinstance(h, str) else h.get("text", h))
        for s in q.get("stepByStep") or []:
            print("  S:", s.get("text", s) if isinstance(s, dict) else s)
        m = q.get("misconceptions") or {}
        if isinstance(m, dict):
            for k, v in m.items():
                if v:
                    print("  M%s: %s" % (k, v))


if __name__ == "__main__":
    main()
