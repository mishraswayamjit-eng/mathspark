"""Build data/teach/parts/arithmetic.json from the rule lessons and the hand-written ones.

    python -X utf8 scripts/teach/gen/arithmetic_build.py

Rules live in arithmetic_rules*.py; one-off lessons in arithmetic_authored_*.py (each has a LESSONS dict).
Then check with: python -X utf8 scripts/teach/validate.py --part arithmetic
"""
import glob
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from arithmetic_common import PART, questions  # noqa: E402
from arithmetic_rules3 import rule_for  # noqa: E402

GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")


def main():
    qs = questions()
    out = {}
    for qid, q in qs.items():
        if qid.startswith(GENERATED):
            script = rule_for(q)
            if script:
                out[qid] = script
    by_rule = len(out)
    for path in sorted(glob.glob(os.path.join(HERE, "arithmetic_authored_*.py"))):
        module = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        for qid, script in module.LESSONS.items():
            if qid not in qs:
                sys.exit("%s: %s is not an arithmetic question" % (os.path.basename(path), qid))
            if qid in out:
                sys.exit("%s: %s already has a lesson" % (os.path.basename(path), qid))
            out[qid] = script
    ordered = {qid: out[qid] for qid in qs if qid in out}
    os.makedirs(os.path.dirname(PART), exist_ok=True)
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
        f.write("\n")
    missing = [qid for qid in qs if qid not in out]
    print("wrote %d lessons (%d by rule, %d by hand); %d questions without one" % (
        len(ordered), by_rule, len(ordered) - by_rule, len(missing)))


if __name__ == "__main__":
    main()
