# -*- coding: utf-8 -*-
"""Prove that check_new_lessons.py really catches slips.

    python -X utf8 scripts/lessons/selftest_checker.py

Feeds the equality reader sentences that are known to be true and sentences
with a planted slip, and checks it accepts the first kind and rejects the
second. A checker that passes everything is worth nothing, so run this after
changing the checker.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_new_lessons as c  # noqa: E402

ALG = "xymnpq"

# (letters, [sentences read in order as one lesson], should it pass?)
CASES = [
    ("", ["368 + 257 = 625"], True),
    ("", ["368 + 257 = 635"], False),
    ("", ["4,567 + 999 = 4,567 + 1,000 − 1 = 5,566."], True),
    ("", ["4,567 + 999 = 4,567 + 1,000 − 1 = 5,567."], False),
    ("", ["2,34,500 + 1,21,300 = 3,55,800."], True),
    ("", ["2,34,500 + 1,21,300 = 3,65,800."], False),
    ("", ["Step 1: pens sold = 1,180 + 765 = 1,945."], True),
    ("", ["Step 1: pens sold = 1,180 + 765 = 1,955."], False),
    ("", ["12 − 7 = 5 and 4 − 2 = 2, so 52 − 27 = 25."], True),
    ("", ["12 − 7 = 5 and 4 − 2 = 3, so 52 − 27 = 25."], False),
    ("", ["Look at 4_7 + 285 = 732."], False),            # blank digit: needs ALLOW
    ("", ["1 km = 1000 m"], True),                         # listed unit fact
    ("", ["1 km = 100 m"], False),                         # not a listed fact
    ("", ["36 km/h = 10 m/s"], True),
    ("", ["36 km/h = 12 m/s"], False),
    ("", ["Speed = Distance ÷ Time"], True),               # formula in words
    ("", ["150 ÷ 3 = 50, so the speed is 50 km/h."], True),
    ("", ["150 ÷ 3 = 60, so the speed is 60 km/h."], False),
    ("", ["24 × 15 = 360 and 360 ÷ 15 = 24."], True),
    ("", ["7 × 8 = 54"], False),
    ("", ["(12 + 8) × 5 = 100"], True),
    ("", ["(12 + 8) × 5 = 52"], False),
    ("", ["2.5 × 4 = 10"], True),
    ("", ["2.5 × 4 = 12"], False),
    ("", [c.latex_to_plain("4{,}231 + 3{,}546 = 7{,}777")], True),
    ("", [c.latex_to_plain("4{,}231 + 3{,}546 = 7{,}787")], False),
    ("", [c.latex_to_plain("\\tfrac{360}{15} = 24")], True),
    ("", [c.latex_to_plain("\\tfrac{360}{15} = 25")], False),
    ("", [c.latex_to_plain("1 + 6 = 7 \\quad 3 + 4 = 7")], True),
    ("", [c.latex_to_plain("1 + 6 = 7 \\quad 3 + 4 = 8")], False),
    (ALG, ["3x + 2x = 5x"], True),                          # identity
    (ALG, ["3x + 2x = 6x"], False),
    (ALG, ["3x + 2y = 5xy"], False),
    (ALG, ["2(x + 3) = 2x + 6"], True),
    (ALG, ["2(x + 3) = 2x + 3"], False),
    (ALG, ["If x = 4, then 3x + 5 = 17."], True),           # substitution
    (ALG, ["If x = 4, then 3x + 5 = 18."], False),
    (ALG, ["Let x = 4.", "3x + 5 = 3 × 4 + 5 = 17"], True),
    (ALG, ["Let x = 4.", "3x + 5 = 3 × 4 + 5 = 19"], False),
    (ALG, ["3x + 5 = 17"], False),                          # no value for x anywhere
    (ALG, ["x² + 1 = 10 when x = 3."], True),
    (ALG, ["x² + 1 = 11 when x = 3."], False),
    (ALG, ["Suppose x = 7, y = x − 2 and p = y + 5.", "(x + y) × p = (7 + 5) × 10 = 120."], True),
    (ALG, ["Suppose x = 7, y = x − 2 and p = y + 5.", "(x + y) × p = (7 + 5) × 10 = 130."], False),
    (ALG, ["Suppose x = 7, y = x − 2 and p = y + 5.", "First y = 7 − 2 = 6."], False),
    (ALG, ["Is 5x + 6 = 7x − 8 true when x = 7?"], True),
    (ALG, ["Is 5x + 6 = 7x − 9 true when x = 7?"], False),
    (ALG, ["(12xy + 8y) ÷ 4y = 3x + 2"], True),
    (ALG, ["(12xy + 8y) ÷ 4y = 3x + 2y"], False),
    (ALG, ["4y(3x + 2) = 12xy + 8y"], True),
    (ALG, [c.latex_to_plain("12xy \\div 4y = 3x")], True),
    (ALG, [c.latex_to_plain("12xy \\div 4y = 3y")], False),
]

EXACT = [
    ("345 + 278", "623"), ("10 / 4", "2.5"), ("7 // 2", "3"), ("17 % 5", "2"),
    ("rnd(6812, 1000)", "7000"), ("rnd(2500, 1000)", "3000"), ("ds(4123)", "10"),
    ("36 * 1000 / 3600", "10"), ("0.1 + 0.2", "0.3"), ("lcm(4, 6)", "12"),
]


def main():
    bad = 0
    for letters, sentences, should_pass in CASES:
        sc = c.Scanner(letters, "selftest")
        for s in sentences:
            sc.scan(s, "text", {})
        sc.finish({})
        passed = not sc.fails
        proved = sc.ok + sc.identities + sc.substituted + sc.facts
        if should_pass and passed and proved == 0 and "=" in "".join(sentences) and any(ch.isdigit() for ch in "".join(sentences)):
            print("BAD   accepted without proving anything: %r" % (sentences,))
            bad += 1
        elif passed != should_pass:
            print("BAD   %s but should %s: %r" % ("passed" if passed else "rejected",
                                                   "pass" if should_pass else "be rejected", sentences))
            bad += 1
    for expr, want in EXACT:
        got = c.show(c.exact(expr))
        if got != want:
            print("BAD   %s gave %s, expected %s" % (expr, got, want))
            bad += 1
    print("selftest: %d cases, %d exact sums, %s" % (len(CASES), len(EXACT),
                                                    "all behave as expected" if bad == 0 else "%d PROBLEM(S)" % bad))
    sys.exit(0 if bad == 0 else 1)


main()
