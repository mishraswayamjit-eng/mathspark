"""Print every question of the worksheets-a set compactly (read-only helper).

    python -X utf8 scripts/fixes/gen/worksheets-a_dump.py EXT_G5_WS_01_
"""
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)

prefix = sys.argv[1]
questions = bank.load_bank()
for q in sorted(questions, key=lambda q: q["id"]):
    if not q["id"].startswith(prefix) or q.get("topicId") != "grade5":
        continue
    print("=== %s [%s] key=%s src=%s" % (q["id"], q.get("subTopic"), q.get("correctAnswer"), q.get("source")))
    print("Q: " + q.get("questionText", ""))
    for letter, o in zip("ABCD", q.get("options", [])):
        print("  %s) %s" % (letter, o.get("text", "") if isinstance(o, dict) else o))
    for i, h in enumerate(q.get("hints") or []):
        print("  H%d: %s" % (i + 1, h))
    for i, s in enumerate(q.get("stepByStep") or []):
        print("  S%d: %s%s" % (i + 1, s.get("text", ""), ("  [latex: %s]" % s["latex"]) if s.get("latex") else ""))
