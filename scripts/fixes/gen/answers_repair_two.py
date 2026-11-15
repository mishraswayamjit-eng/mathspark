"""Repair the two percentage questions that were marked for withdrawal.

Both asked for a per cent of 250 students that comes to a half child (62.5 and
12.5), with the key rounded down. Changing the number of students so that the
keyed choice is exactly right repairs them without touching the choices or the
key. The arithmetic is checked here before anything is written.

    python -X utf8 scripts/fixes/gen/answers_repair_two.py
"""
import io
import json
import os
from fractions import Fraction

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PART = os.path.join(ROOT, "data", "question-fixes", "parts", "answers.json")
WHY = ("The question asked for a per cent of 250 students that is not a whole number of children, and the key was "
       "rounded down. The number of students is changed so that the keyed choice is exactly right. The three hints "
       "were also the generic lines given to every generated question.")

REPAIRS = [
    # id, per cent, new total, keyed value, hint 2, hint 3
    ("VAR_G5_vary_percentage_V43", 25, 248, 62,
     "25% is the same as one quarter. So share the 248 students into 4 equal groups. How many are in one group?",
     "Try another one: 25% of 80. A quarter of 80 is 80 ÷ 4 = 20, so 25% of 80 is 20."),
    ("VAR_G5_vary_percentage_V287", 5, 240, 12,
     "Find 10% first: that is one tenth, so divide 240 by 10. Then 5% is half of that.",
     "Try another one: 5% of 60. 10% of 60 is 60 ÷ 10 = 6, and half of 6 is 3, so 5% of 60 is 3."),
]


def main():
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    for qid, percent, total, keyed, hint2, hint3 in REPAIRS:
        value = Fraction(percent, 100) * total
        assert value == keyed, (qid, value, keyed)
        part[qid] = {
            "questionText": "Out of %d students, %d%% are girls. How many girls are there?" % (total, percent),
            "hints": [
                "Per cent means 'out of every 100'. So %d%% girls means %d girls in every 100 students." % (percent, percent),
                hint2,
                hint3,
            ],
            "why": WHY,
            "proof": "%d%% of %d = %d × %d ÷ 100 = %d, a whole number of children and the value of the keyed choice. "
                     "With the old total, %d%% of 250 = %s." % (percent, total, percent, total, keyed, percent,
                                                                 float(Fraction(percent, 100) * 250)),
        }
        print("%s: %d%% of %d = %s (keyed choice %d)" % (qid, percent, total, value, keyed))
    with io.open(PART, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("answers.json now has %d entries" % len(part))


if __name__ == "__main__":
    main()
