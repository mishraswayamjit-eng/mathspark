"""Build data/teach/parts/fractions.json: a lesson for every Grade 5 fractions question.

    python -X utf8 scripts/teach/gen/fractions_build.py

Generated families are written by rule (fractions_rules_*.py); one-off questions are
written by hand (fractions_authored_*.py). Then check with
    python -X utf8 scripts/teach/validate.py --part fractions
"""
import collections
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions_lib import OUT, questions  # noqa: E402
from fractions_rules_add import like_fractions, unlike_subtract  # noqa: E402
from fractions_rules_cmp import compare, equation, missing_top  # noqa: E402
from fractions_rules_of import fraction_of, marbles_left  # noqa: E402

AUTHORED = {}
for name in ("fractions_authored_1", "fractions_authored_2", "fractions_authored_3", "fractions_authored_4"):
    try:
        mod = __import__(name)
    except ImportError:
        continue
    AUTHORED.update(mod.LESSONS)

N = r"(\d+)"
F = r"(\d+)/(\d+)"
RULES = [
    ("fraction of a quantity", re.compile(r"^What is %s of %s\?$" % (F, N)),
     lambda q, m: fraction_of(q, int(m[1]), int(m[2]), int(m[3]))),
    ("add like fractions (Simplify)", re.compile(r"^Simplify: %s \+ %s$" % (F, F)),
     lambda q, m: _like(q, m, True, False)),
    ("add like fractions (simplest form)", re.compile(r"^Add, and give the answer in its simplest form: %s \+ %s$" % (F, F)),
     lambda q, m: _like(q, m, True, True)),
    ("marbles left", re.compile(r"^(\w+) has %s marbles\. \w+ gives %s of them to a friend\. How many marbles does \w+ have left\?$" % (N, F)),
     lambda q, m: marbles_left(q, m[1], int(m[2]), int(m[3]), int(m[4]))),
    ("which is greater", re.compile(r"^Which is greater: %s or %s\?$" % (F, F)),
     lambda q, m: compare(q, int(m[1]), int(m[2]), int(m[3]), int(m[4]))),
    ("missing top number", re.compile(r"^Find the missing number: %s = \?/%s$" % (F, N)),
     lambda q, m: missing_top(q, int(m[1]), int(m[2]), int(m[3]))),
    ("equation ax ± b = c", re.compile(r"^Solve: %sx ([−+-]) %s = %s$" % (N, N, N)),
     lambda q, m: equation(q, int(m[1]), m[2] != "+", int(m[3]), int(m[4]))),
    ("What is a/b ± c/d", re.compile(r"^What is %s ([−+-]) %s\?$" % (F, F)),
     lambda q, m: _what_is(q, m)),
]


def _like(q, m, plus, simplest):
    a, b, c, d = int(m[1]), int(m[2]), int(m[3]), int(m[4])
    assert b == d, q["id"]
    return like_fractions(q, a, b, c, plus, simplest)


def _what_is(q, m):
    a, b, c, d = int(m[1]), int(m[2]), int(m[4]), int(m[5])
    plus = m[3] == "+"
    if b == d:
        return like_fractions(q, a, b, c, plus)
    assert not plus, q["id"]
    return unlike_subtract(q, a, b, c, d)


def main():
    out = {}
    by = collections.Counter()
    missing = []
    for q in questions():
        qid = q["id"]
        if qid in AUTHORED:
            out[qid] = AUTHORED[qid]
            by["authored"] += 1
            continue
        for name, pattern, make in RULES:
            m = pattern.match(q["questionText"].strip())
            if m:
                out[qid] = make(q, m)
                by[name] += 1
                break
        else:
            missing.append(qid)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for name, n in sorted(by.items()):
        print("  %-40s %d" % (name, n))
    print("wrote %d lessons; %d questions without one" % (len(out), len(missing)))
    for qid in missing:
        print("  no lesson: %s" % qid)


if __name__ == "__main__":
    main()
