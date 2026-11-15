"""Build the teach-mode lessons for the topic ratio-word-problems.

    python -X utf8 scripts/teach/gen/ratio_word_problems.py

Generated families (ids starting VAR_, VAR2_, BOOST_, PH3_) get their lesson from a
rule in ratio_word_problems_rules.py. One-off questions get a lesson written by hand
in ratio_word_problems_a.py ... _d.py. Writes data/teach/parts/ratio-word-problems.json.
Then check with:  python -X utf8 scripts/teach/validate.py --part ratio-word-problems
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
from common import load_grade5, topic_of  # noqa: E402

from ratio_word_problems_rules import by_rule  # noqa: E402

PART = "ratio-word-problems"
OUT = os.path.join(ROOT, "data", "teach", "parts", PART + ".json")
GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")
AUTHORED_MODULES = ["ratio_word_problems_a", "ratio_word_problems_b", "ratio_word_problems_c", "ratio_word_problems_d"]


def main():
    authored = {}
    for name in AUTHORED_MODULES:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        for qid, made in importlib.import_module(name).LESSONS.items():
            assert qid not in authored, qid
            authored[qid] = made

    questions = [q for q in load_grade5() if topic_of(q) == PART]
    ids = {q["id"] for q in questions}
    for qid in authored:
        assert qid in ids, "not in this topic: %s" % qid

    out = {}
    missing = []
    counts = {"rule": 0, "authored": 0}
    for q in questions:
        qid = q["id"]
        made = authored.get(qid)
        if made is None and qid.startswith(GENERATED):
            made = by_rule(q)
        if made is None:
            missing.append(qid)
            continue
        out[qid] = made
        counts[made["origin"]] += 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s: %d lessons (%d by rule, %d by hand) of %d questions"
          % (os.path.relpath(OUT, ROOT), len(out), counts["rule"], counts["authored"], len(questions)))
    for qid in missing:
        print("  no lesson yet: %s" % qid)


if __name__ == "__main__":
    main()
