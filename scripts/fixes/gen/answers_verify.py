"""Proof record for the 'answers' part: recompute each answer from the question's own numbers.

    python -X utf8 scripts/fixes/gen/answers_verify.py

For every question the script computes the answer independently, then shows the choice the bank
keys today and the choice that is right once the fix in data/question-fixes/parts/answers.json is
applied. A line is OK only when exactly one final choice matches the computed answer and it is the
final key. Questions to withdraw are computed too, to show why no choice can be right.
Read-only: prints a record, changes nothing. Exit code 1 if any line is not OK.
"""
import io
import json
import os
import re
import sys
from fractions import Fraction
from math import gcd, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")
PART = os.path.join(ROOT, "data", "question-fixes", "parts", "answers.json")

sys.path.insert(0, HERE)
from answers_scan import evaluate, option_value  # noqa: E402  (exact evaluator and choice reader)


def F(text):
    a, b = text.split("/")
    return Fraction(int(a), int(b))


def is_value(x):
    """Matcher: the choice states exactly the number x."""
    x = Fraction(x)
    return lambda t: option_value(t) == x


def is_text(s):
    return lambda t: t.strip().lower() == s.lower()


# ── One function per question: returns (what was computed, matcher for the right choice) ──

def b2_021(q):
    total, first_second, second_third = 27, 13, 19
    third = total - first_second
    first = total - second_third
    second = first_second - first
    assert first + second + third == total and second + third == second_third
    return "bags %d, %d, %d; first + third = %d" % (first, second, third, first + third), is_value(first + third)


def b5_005(q):
    n = max(k for k in range(1, 200) if 1000 <= k * k <= 9999)
    sq = str(n * n)
    places = [i for i, c in enumerate(sq) if c == "8"]
    assert len(places) == 1
    pv = 8 * 10 ** (len(sq) - 1 - places[0])
    return "greatest 4-digit square = %d² = %s; place value of 8 = %d" % (n, sq, pv), is_value(pv)


def percent(n, p):
    def fn(q):
        v = Fraction(n * p, 100)
        return "%d%% of %d = %s" % (p, n, float(v)), is_value(v)
    return fn


def b3_001(q):
    v = Fraction(12 * 100, 15)
    assert v.denominator == 1 and v % 10 == 0
    tens = int(v) // 10
    return "1200 ÷ 15 = %d = %d tens" % (v, tens), lambda t: t.strip() in ("%d" % v, "%d tens" % tens, "%dT" % tens)


def b6_011(q):
    pairs = [(a, 600 // a) for a in range(1, 25) if 600 % a == 0 and gcd(a, 600 // a) == 5]
    greater = sorted({max(p) for p in pairs})
    assert len(greater) > 1
    return "pairs with product 600 and HCF 5: %s; greater number could be %s" % (pairs, " or ".join(map(str, greater))), is_text("data inadequate")


def ws01_010(q):
    possible = {}
    for d in range(10):
        number = "6%d8%d4" % (d, d)
        possible[d * 1000 - d * 10] = (d, number)
    opts = [int(o) for o in q["options"]]
    hits = [o for o in opts if o in possible]
    return "differences possible for digits 0-9: %s; choices that fit: %s (digit %d, number %s)" % (
        sorted(possible), hits, possible[hits[0]][0], possible[hits[0]][1]), lambda t: t.strip().isdigit() and int(t) in possible


def b2_011(q):
    old = "469571"
    assert old.count("5") == 1 and old.count("6") == 1
    new = old.replace("5", "#").replace("6", "5").replace("#", "6")
    diff = int(new) - int(old)
    phrase = "%s by %d" % ("more" if diff > 0 else "less", abs(diff))
    return "%s -> %s; new − old = %d, so %s" % (old, new, diff, phrase), is_text(phrase)


def simplify(q):
    expr = q["questionText"].split(":", 1)[1] if ":" in q["questionText"] else q["questionText"].replace("= ?", "")
    v = evaluate(expr)
    assert v is not None, expr
    return "%s = %s" % (expr.strip(), v if v.denominator == 1 else "%s (= %s)" % (v, mixed(v))), is_value(v)


def mixed(v):
    whole, rest = divmod(v, 1)
    return "%d %s" % (whole, rest) if whole else str(rest)


def b3_012(q):
    best = min(1000 - 7 * n for n in range(1, 1000) if 7 * n <= 1000)
    n = (1000 - best) // 7
    return "1000 cm, 7 parts of n whole cm: longest n = %d (7 × %d = %d), least left over = %d cm" % (n, n, 7 * n, best), is_text("%d cm" % best)


def times_01_014(q):
    number = "27511"
    units, tens = int(number[-1]) * 1, int(number[-2]) * 10
    v = Fraction(units, tens)
    return "place values %d and %d; %d ÷ %d = %s" % (units, tens, units, tens, float(v)), is_value(v)


def pages(q):
    n = int(re.search(r"has (\d+) pages", q["questionText"]).group(1))
    v = sum(len(str(i)) for i in range(1, n + 1))
    return "digits in page numbers 1..%d = %d" % (n, v), is_value(v)


def glasses(q):
    m = re.search(r"holds (\d+) litres of water\. How many glasses of (\d+) ml", q["questionText"])
    ml, glass = int(m.group(1)) * 1000, int(m.group(2))
    full, left = divmod(ml, glass)
    return "%d ml ÷ %d ml = %d full glasses, %d ml left over" % (ml, glass, full, left), is_value(full)


def fp_2022_009(q):
    roots = [n for n in range(1, 100) if 100 <= n * n <= 999 and (n * n) % 2 == 1]
    count = len(roots)
    numeric = [int(o) for o in q["options"] if o.strip().isdigit()]
    assert count not in numeric
    return "odd 3-digit squares: %d (roots %d..%d); %d is not among %s" % (count, roots[0], roots[-1], count, numeric), is_text("None of these")


def fp_2021_031(q):
    fits = [n for n in range(1, 61) if Fraction(n + 17) == Fraction(60, n)]
    assert len(fits) == 1
    return "n + 17 = 60 ÷ n holds only for n = %d (%d + 17 = %d = 60 ÷ %d)" % (fits[0], fits[0], fits[0] + 17, fits[0]), is_value(fits[0])


def fp_2020_019(q):
    either = F("5/8") + F("3/8") - F("1/4")
    neither = 1 - either
    return "at least one game = 5/8 + 3/8 − 1/4 = %s; neither = %s" % (either, neither), is_value(neither)


def fp_2019_025(q):
    right = Fraction(72 * 25, 100)
    assert right.denominator == 1
    return "right = 72%% of 25 = %d; not correct = 25 − %d = %d" % (right, right, 25 - right), is_value(25 - right)


def fp_2018_017(q):
    def works(t):
        m = re.fullmatch(r"(\d+) and (\d+)", t.strip())
        s = int(m.group(1)) ** 2 + int(m.group(2)) ** 2
        return isqrt(s) ** 2 == s
    shown = []
    for t in q["options"]:
        a, b = [int(x) for x in t.split(" and ")]
        s = a * a + b * b
        shown.append("%d²+%d²=%d %s" % (a, b, s, "= %d²" % isqrt(s) if isqrt(s) ** 2 == s else "not a square"))
    return "; ".join(shown), works


def fp_2017_034(q):
    r = isqrt(370)
    return "largest square not above 370 is %d² = %d; 370 − %d = %d" % (r, r * r, r * r, 370 - r * r), is_value(370 - r * r)


def simplest_sum(q):
    """'a/b + c/b' in simplest form: the right choice must be written in lowest terms."""
    m = re.search(r"(\d+)/(\d+) \+ (\d+)/(\d+)$", q["questionText"])
    a, b, c, d = [int(x) for x in m.groups()]
    assert b == d
    v = Fraction(a, b) + Fraction(c, d)
    lowest = str(v.numerator) if v.denominator == 1 else "%d/%d" % (v.numerator, v.denominator)
    same_value = [t for t in q["options"] if option_value(t) == v]
    return "%d/%d + %d/%d = %d/%d = %s in simplest form; choices with that value: %s" % (
        a, b, c, d, a + c, b, lowest, same_value), is_text(lowest)


def by_value(compute):
    def fn(q):
        text, v = compute()
        return text, is_value(v)
    return fn


CHECKS = [
    # the 26 flagged questions
    ("EXT_G5_WS_B2_021", b2_021),
    ("EXT_G5_WS_B5_005", b5_005),
    ("VAR_G5_vary_percentage_V29", percent(250, 5)),
    ("VAR_G5_vary_percentage_V43", percent(250, 25)),
    ("VAR_G5_vary_percentage_V287", percent(250, 5)),
    ("EXT_G5_WS_B3_001", b3_001),
    ("EXT_G5_WS_B6_011", b6_011),
    ("EXT_G5_WS_01_010", ws01_010),
    ("EXT_G5_WS_B2_011", b2_011),
    ("EXT_G5_WS_B4_032", simplify),
    ("EXT_G5_WS_B3_012", b3_012),
    ("VAR_EXT_G5_WS_B4_023_03", simplify),
    ("VAR_EXT_G5_WS_B4_029_03", simplify),
    ("VAR_EXT_G5_WS_01_014_04_b2", times_01_014),
    ("PH3_EXT_G5_WS_01_003_02", pages),
    ("VAR2_EXT_G5_WS_B2_026_02", glasses),
    ("VAR2_EXT_G5_WS_B3_006_02", glasses),
    ("VAR2_EXT_G5_WS_B3_037_02", glasses),
    ("VAR2_EXT_G5_WS_B6_003_02", glasses),
    ("VAR2_EXT_G5_WS_B6_012_02", glasses),
    ("EXT_G5_FP_2022_009", fp_2022_009),
    ("EXT_G5_FP_2021_031", fp_2021_031),
    ("EXT_G5_FP_2020_019", fp_2020_019),
    ("EXT_G5_FP_2019_025", fp_2019_025),
    ("EXT_G5_FP_2018_017", fp_2018_017),
    ("EXT_G5_FP_2017_034", fp_2017_034),
    # found by answers_scan.py: the sum appears in two choices
    ("VAR2_EXT_G5_WS_B7_003_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_005_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_012_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_014_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_015_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_016_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_020_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_021_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_025_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_028_02", simplest_sum),
    ("VAR2_EXT_G5_WS_B7_033_02", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_002_05", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_005_07", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_010_05", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_012_06", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_013_07", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_014_05", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_016_06", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_023_06", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_028_07", simplest_sum),
    ("BOOST_EXT_G5_WS_B7_029_06", simplest_sum),
    # found by the scan, left alone: two choices equal in value, but neither is the answer
    ("EXT_G5_WS_B7_023", by_value(lambda: ("smallest of A = %s, greatest of B = %s, product = %s" % (
        min(map(F, ["7/12", "7/11", "7/9", "7/10"])), max(map(F, ["3/8", "5/8", "6/8", "1/8"])),
        min(map(F, ["7/12", "7/11", "7/9", "7/10"])) * max(map(F, ["3/8", "5/8", "6/8", "1/8"]))),
        min(map(F, ["7/12", "7/11", "7/9", "7/10"])) * max(map(F, ["3/8", "5/8", "6/8", "1/8"]))))),
    ("EXT_G5_WS_B7_025", by_value(lambda: ("m = 13/20 − 3/5 + 1/4 = %s" % (F("13/20") - F("3/5") + F("1/4")),
                                           F("13/20") - F("3/5") + F("1/4")))),
    ("EXT_G5_FP_2024_009", by_value(lambda: ("A = 9/4 ÷ (3/4 ÷ 9/4) = %s" % (F("9/4") / (F("3/4") / F("9/4"))),
                                             F("9/4") / (F("3/4") / F("9/4"))))),
]

WITHDRAW = {
    "VAR_G5_vary_percentage_V43": "62.5 girls: a count of children cannot be a half",
    "VAR_G5_vary_percentage_V287": "12.5 girls: a count of children cannot be a half",
}


def main():
    with io.open(SEED, encoding="utf-8") as f:
        seed = {q["id"]: q for q in json.load(f)["questions"]}
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)

    bad = 0
    for qid, fn in CHECKS:
        q = seed[qid]
        fix = part.get(qid, {})
        old_opts = [o["text"] for o in q["options"]]
        final = {
            "questionText": fix.get("questionText", q["questionText"]),
            "options": fix.get("options", old_opts),
            "correctAnswer": fix.get("correctAnswer", q["correctAnswer"]),
        }
        computed, matcher = fn(final)
        old_key = q["correctAnswer"]
        hits = ["ABCD"[i] for i, t in enumerate(final["options"]) if matcher(t)]
        changed = [k for k in ("questionText", "options", "correctAnswer") if k in fix]
        if qid in WITHDRAW:
            status = "WITHDRAW (%s)" % WITHDRAW[qid]
            ok = qid not in part and not hits
        else:
            ok = hits == [final["correctAnswer"]]
            status = "OK" if ok else "MISMATCH: choices matching the computed answer = %s" % (hits or "none")
        bad += 0 if ok else 1
        print(qid)
        print("    computed : %s" % computed)
        print("    keyed    : %s = %s" % (old_key, old_opts["ABCD".find(old_key)]))
        if qid in WITHDRAW:
            print("    corrected: no fix written; no choice equals the computed value")
        else:
            idx = "ABCD".find(final["correctAnswer"])
            print("    corrected: %s = %s%s" % (final["correctAnswer"], final["options"][idx],
                                               "   (changed: %s)" % ", ".join(changed) if changed else "   (key and choices unchanged)"))
        print("    result   : %s" % status)
    print("\n%d questions checked, %d not OK" % (len(CHECKS), bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
