"""Carry over another part's hints/steps into answers.json for ids that both parts fix.

    python -X utf8 scripts/fixes/gen/answers_merge_overlap.py          # report only
    python -X utf8 scripts/fixes/gen/answers_merge_overlap.py --write  # update answers.json

check.py allows a question id in one part only, and only the 'answers' part may change a question's
text. When the scan finds a question whose wording must change but another part has already written
good hints/steps for it, the whole fix has to live in answers.json. This copies the other part's
`hints` and `steps` (only the fields answers.json does not already give) into the answers entry and
notes where they came from. It writes ONLY data/question-fixes/parts/answers.json; the other part
file is never touched, so its copy of the id still has to be removed by whoever owns that file.
"""
import glob
import io
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PARTS = os.path.join(ROOT, "data", "question-fixes", "parts")
MINE = os.path.join(PARTS, "answers.json")
NOTE = " Hints and steps carried over unchanged from %s.json (%s)"

with io.open(MINE, encoding="utf-8") as f:
    mine = json.load(f)

overlaps = []
changed = 0
for path in sorted(glob.glob(os.path.join(PARTS, "*.json"))):
    name = os.path.splitext(os.path.basename(path))[0]
    if name == "answers":
        continue
    with io.open(path, encoding="utf-8") as f:
        other = json.load(f)
    for qid in mine:
        if qid not in other:
            continue
        overlaps.append((qid, name))
        took = []
        for field in ("hints", "steps"):
            if field in other[qid] and field not in mine[qid]:
                mine[qid][field] = other[qid][field]
                took.append(field)
        if took:
            changed += 1
            reason = other[qid].get("why", "").strip().rstrip(".")
            mine[qid]["why"] = mine[qid]["why"].rstrip() + NOTE % (name, reason) + "."
        print("%-32s also in %-18s carried over: %s" % (qid, name, ", ".join(took) or "nothing (already present)"))

print("\n%d ids are in answers.json and another part; %d entries gained fields" % (len(overlaps), changed))
if "--write" in sys.argv and changed:
    with io.open(MINE, "w", encoding="utf-8", newline="\n") as f:
        json.dump(mine, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("answers.json updated")
