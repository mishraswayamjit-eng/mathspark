"""Print the whole seed record of one or more Grade 5 questions (read-only).

    python -X utf8 scripts/fixes/gen/answers_dump.py <id> [<id> ...]
    python -X utf8 scripts/fixes/gen/answers_dump.py --brief <id> [...]   # one compact block each
"""
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")

with io.open(SEED, encoding="utf-8") as f:
    qs = {q["id"]: q for q in json.load(f)["questions"]}

args = sys.argv[1:]
brief = "--brief" in args
for qid in [a for a in args if not a.startswith("--")]:
    q = qs.get(qid)
    if not q:
        print("no such question:", qid)
        continue
    if not brief:
        print(json.dumps(q, ensure_ascii=False, indent=1))
        continue
    print(qid, "|", q["questionText"])
    print("   ", " | ".join("%s=%s" % (o["id"], o["text"]) for o in q["options"]), "| key", q["correctAnswer"])
    for h in q.get("hints", []):
        print("    hint:", h)
    for s in q.get("stepByStep", []):
        print("    step:", s.get("text"), "||", s.get("latex", ""))
    print("    misconceptions:", json.dumps(q.get("misconceptions"), ensure_ascii=False))
