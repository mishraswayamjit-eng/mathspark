"""Print the authored-02 questions to read: python -X utf8 scripts/teach/gen/authored_02_dump.py [start] [count]"""
import sys

from authored_02_lib import load_questions


def main():
    qs = load_questions()
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    count = int(sys.argv[2]) if len(sys.argv) > 2 else len(qs)
    print("%d questions" % len(qs))
    for q in qs[start:start + count]:
        print("\n== %s  [%s]  %s" % (q["id"], q.get("difficulty", ""), q.get("subTopic", "")))
        print("Q: " + q["questionText"])
        opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q["options"]]
        print("OPTS: " + " | ".join(opts) + "   KEY " + q["correctAnswer"])
        for h in q.get("hints") or []:
            print("HINT: " + (h if isinstance(h, str) else h.get("text", "")))
        for s in q.get("stepByStep") or []:
            print("STEP: " + (s.get("text", "") if isinstance(s, dict) else str(s)))
        m = q.get("misconceptions") or {}
        if isinstance(m, dict):
            for k, v in m.items():
                if v:
                    print("MIS %s: %s" % (k, v))


if __name__ == "__main__":
    main()
