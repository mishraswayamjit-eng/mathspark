"""Review aid for place-value narration. Reads the part file; writes nothing.

    python -X utf8 scripts/speech/topics/place_value_review.py            # one example of every generated wording
    python -X utf8 scripts/speech/topics/place_value_review.py spoken 5   # every 5th generated question, spoken lines only
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

with io.open(os.path.join(PARTS, "place-value.json"), encoding="utf-8") as f:
    part = json.load(f)
questions = sorted((q for q in load_grade5() if topic_of(q) == "place-value" and not q["id"].startswith("EXT_")),
                   key=lambda q: q["id"])


def flat(d):
    return [d["q"]] + d["options"] + d["hints"] + d["steps"]


if len(sys.argv) > 1 and sys.argv[1] == "spoken":
    step = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    for q in questions[::step]:
        e = part[q["id"]]
        print("##", q["id"])
        print("  Q:", e["q"])
        print("  O:", " | ".join(e["options"]))
        for h in e["hints"]:
            print("  H:", h)
        for s in e["steps"]:
            print("  S:", s)
else:
    seen = {}
    for q in questions:
        for printed, spoken in zip(flat(source_strings(q)), flat(part[q["id"]])):
            key = re.sub(r"\d[\d,.]*", "N", printed)
            if key not in seen:
                seen[key] = (printed, spoken, 0)
            seen[key] = seen[key][:2] + (seen[key][2] + 1,)
    for printed, spoken, n in seen.values():
        if printed == spoken:
            continue
        print("%4d  PRINT  %s" % (n, printed))
        print("      SPOKEN %s" % spoken)
    print("%d wordings, %d left unchanged" % (len(seen), sum(1 for p, s, _ in seen.values() if p == s)))
    for printed, spoken, n in seen.values():
        if printed == spoken and not re.match(r"^N$", re.sub(r"\d[\d,.]*", "N", printed)):
            print("%4d  SAME   %s" % (n, printed))
