"""Build data/teach/parts/g4-gr4_fractions.json: a lesson for every Grade 4 fractions question.

    python -X utf8 scripts/teach/gen/g4_gr4_fractions.py

Generated families are written by rule (g4_gr4_fractions_rules_*.py); the other questions are
written one by one (g4_gr4_fractions_hand_*.py). Then check with
    python -X utf8 scripts/teach/validate.py --part g4-gr4_fractions
"""
import collections
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_fractions_lib import OUT, _h, questions  # noqa: E402
from g4_gr4_fractions_rules_a import like_fractions, unlike  # noqa: E402
from g4_gr4_fractions_rules_b import compare, fraction_of, marbles_left, missing_top  # noqa: E402

AUTHORED = {}
for name in ("g4_gr4_fractions_hand_a", "g4_gr4_fractions_hand_b", "g4_gr4_fractions_hand_c", "g4_gr4_fractions_hand_d",
             "g4_gr4_fractions_hand_e", "g4_gr4_fractions_hand_f"):
    try:
        mod = __import__(name)
    except ImportError:
        continue
    AUTHORED.update(mod.LESSONS)

N = r"(\d+)"
F = r"(\d+)/(\d+)"
GENERATED = re.compile(r"^(VAR|VAR2|BOOST|PH3)_|^Q_CH\d+_\d+_V\d+$")
RULES = [
    ("fraction of a quantity", re.compile(r"^What is %s of %s\?$" % (F, N)),
     lambda q, m: fraction_of(q, int(m[1]), int(m[2]), int(m[3]))),
    ("sweets given away", re.compile(r"^(\w+) has %s sweets and gives away %s of them\. How many sweets does \w+ give away\?$" % (N, F)),
     lambda q, m: fraction_of(q, int(m[3]), int(m[4]), int(m[2]), m[1])),
    ("add like fractions (Simplify)", re.compile(r"^Simplify: %s \+ %s$" % (F, F)),
     lambda q, m: _two(q, int(m[1]), int(m[2]), int(m[3]), int(m[4]), True)),
    ("marbles left", re.compile(r"^(\w+) has %s marbles\. \w+ gives %s of them to a friend\. How many marbles does \w+ have left\?$" % (N, F)),
     lambda q, m: marbles_left(q, m[1], int(m[2]), int(m[3]), int(m[4]))),
    ("which is greater", re.compile(r"^Which is greater: %s or %s\?$" % (F, F)),
     lambda q, m: compare(q, int(m[1]), int(m[2]), int(m[3]), int(m[4]))),
    ("missing top number", re.compile(r"^Find the missing number: %s = \?/%s$" % (F, N)),
     lambda q, m: missing_top(q, int(m[1]), int(m[2]), int(m[3]))),
    ("What is a/b ± c/d", re.compile(r"^What is %s ([−+-]) %s\?$" % (F, F)),
     lambda q, m: _two(q, int(m[1]), int(m[2]), int(m[4]), int(m[5]), m[3] == "+")),
]


def _two(q, a, b, c, d, plus):
    if b == d:
        return like_fractions(q, a, b, c, plus)
    return unlike(q, a, b, c, d, plus)


def spread(qid, script):
    """The hand-written lessons list the right choice first; move it to a place that depends on the question."""
    for i, beat in enumerate(script["beats"]):
        ask = beat.get("ask")
        if not ask or ask.get("kind") != "choose":
            continue
        choices = ask["choices"]
        right = choices[ask["answer"]]
        k = _h(qid, "ask%d" % i) % len(choices)
        ask["choices"] = choices[k:] + choices[:k]
        ask["answer"] = ask["choices"].index(right)
    return script


def main():
    for qid in AUTHORED:
        spread(qid, AUTHORED[qid])
    out = {}
    by = collections.Counter()
    missing = []
    for q in questions():
        qid = q["id"]
        if qid in AUTHORED:
            out[qid] = AUTHORED[qid]
            by["authored"] += 1
            continue
        if GENERATED.search(qid):
            for name, pattern, make in RULES:
                m = pattern.match(q["questionText"].strip())
                if m:
                    out[qid] = make(q, m)
                    by[name] += 1
                    break
            else:
                missing.append(qid)
        else:
            missing.append(qid)
    extra = sorted(set(AUTHORED) - {q["id"] for q in questions()})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    for name, n in sorted(by.items()):
        print("  %-40s %d" % (name, n))
    print("wrote %d lessons; %d questions without one" % (len(out), len(missing)))
    if "--list" in sys.argv:
        for qid in missing:
            print("  no lesson: %s" % qid)
    for qid in extra:
        print("  NOT A QUESTION OF THIS TOPIC: %s" % qid)


if __name__ == "__main__":
    main()
