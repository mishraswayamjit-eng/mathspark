"""Rules for generated variants, part 2: fractions (hints that state the answer, 'one-2th', no-op steps)."""
import math
import re
from fractions import Fraction

from variants_papers_util import Skip, make_steps, matches, need_key, pick, step_texts

PART_WORD = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth",
             10: "tenth", 11: "eleventh", 12: "twelfth", 15: "fifteenth", 16: "sixteenth", 20: "twentieth"}

# (numerator, denominator, whole): worked examples for "a/b of N", tried in order.
FRACTION_OF_EXAMPLES = [(2, 3, 12), (3, 4, 20), (2, 5, 15), (3, 7, 14)]
UNIT_FRACTION_EXAMPLES = [(1, 3, 12), (1, 4, 20), (1, 5, 15), (1, 7, 14)]
COUNT_WORD = {2: "two", 3: "three"}
PLURAL = {"half": "halves", "third": "thirds", "quarter": "quarters", "fifth": "fifths", "seventh": "sevenths"}


def fraction_of_example(a, b, n):
    one = n // b
    word = PART_WORD[b]
    if a == 1:
        return "Try a smaller one: 1/%d of %d. One %s of %d is %d ÷ %d = %d." % (b, n, word, n, n, b, one)
    return ("Try a smaller one: %d/%d of %d. One %s of %d is %d ÷ %d = %d, so %s %s is %d × %d = %d."
            % (a, b, n, word, n, n, b, one, COUNT_WORD[a], PLURAL[word], a, one, a * one))


def rule_fraction_of(q):
    m = matches(q, r"What is (\d+)/(\d+) of (\d+)\?")
    if not m:
        return None
    a, b, n = int(m.group(1)), int(m.group(2)), int(m.group(3))
    old_hints = q.get("hints") or []
    if len(old_hints) != 3 or not old_hints[2].startswith("Think: one-"):
        return None
    if b not in PART_WORD or n % b or a >= b:
        raise Skip("not a proper fraction of a whole number of parts")
    word = PART_WORD[b]
    need_key(q, a * n // b)
    pool = UNIT_FRACTION_EXAMPLES if a == 1 else FRACTION_OF_EXAMPLES
    examples = [fraction_of_example(*e) for e in pool if e[1] != b and e[2] != n]
    if a == 1:
        second = "1/%d means just one %s, so that single division gives you the answer." % (b, word)
    else:
        second = "That gives you one %s of %d. You need %d of them, so multiply your result by %d." % (word, n, a, a)
    hints = [
        "To find %d/%d of %d, first find one %s of %d: divide %d by %d." % (a, b, n, word, n, n, b),
        second,
        pick(q, examples, avoid=[n // b] if n // b >= 10 else []),
    ]
    return {"hints": hints, "why": "Hint 3 said 'one-%dth' and stated the working's result (the answer itself when the numerator is 1)." % b}


SAME_DENOMINATOR_PLAIN = [
    "Try a smaller one: 1/7 + 2/7 = 3/7. The sevenths stay sevenths; only the top numbers are added. 3 and 7 share no factor, so that is the final answer.",
    "Try a smaller one: 2/11 + 3/11 = 5/11. The bottom number stays 11; only the top numbers are added. 5 and 11 share no factor, so that is the final answer.",
]
SAME_DENOMINATOR_SIMPLIFY = [
    "Try a smaller one: 1/6 + 3/6 = 4/6. Both 4 and 6 can be divided by 2, so 4/6 simplifies to 2/3.",
    "Try a smaller one: 1/8 + 5/8 = 6/8. Both 6 and 8 can be divided by 2, so 6/8 simplifies to 3/4.",
]


def rule_fraction_add(q):
    m = matches(q, r"Simplify: (\d+)/(\d+) \+ (\d+)/(\d+)")
    if not m:
        return None
    a, d, b, d2 = (int(g) for g in m.groups())
    old = step_texts(q)
    if d != d2 or len(old) != 2 or not old[0].startswith("Same denominators, so add numerators"):
        return None
    n = a + b
    g = math.gcd(n, d)
    value = Fraction(n, d)
    answer = str(value.numerator) if value.denominator == 1 else "%d/%d" % (value.numerator, value.denominator)
    need_key(q, answer)
    first = "The denominators are the same, so add the numerators: (%d + %d)/%d = %d/%d." % (a, b, d, n, d)
    if g == 1:
        texts = [first, "%d and %d have no common factor other than 1, so %d/%d is already in its simplest form." % (n, d, n, d)]
        examples = SAME_DENOMINATOR_PLAIN
    elif value.denominator == 1:
        texts = [first, "%d ÷ %d = %d, so %d/%d is the whole number %d." % (n, d, value.numerator, n, d, value.numerator)]
        examples = SAME_DENOMINATOR_SIMPLIFY
    else:
        texts = [first, "Simplify by dividing the top and the bottom by %d: %d/%d = %s." % (g, n, d, answer)]
        examples = SAME_DENOMINATOR_SIMPLIFY
    hints = [
        "Both fractions have the same bottom number, %d. So the size of the pieces stays the same and you only add the top numbers." % d,
        "Add the top numbers %d and %d, and keep the bottom number %d. Then see whether the result can be simplified." % (a, b, d),
        pick(q, [e for e in examples if "/%d " % d not in e]),
    ]
    return {"hints": hints, "steps": make_steps(q, texts),
            "why": "Hint 2 worked out the sum (the answer, or one step short of it); the last step was a no-op such as 'Simplify: 8/9 = 8/9' where nothing simplifies."}


def rule_compare_fractions(q):
    m = matches(q, r"Which is greater: (\d+)/(\d+) or (\d+)/(\d+)\?")
    if not m:
        return None
    a, b, c, d = (int(g) for g in m.groups())
    old = q.get("stepByStep") or []
    if len(old) != 3 or not old[1].get("text", "").startswith("Convert: "):
        return None
    lcm = b * d // math.gcd(b, d)
    if b != lcm and d != lcm:
        return None  # both fractions really are converted: nothing the matter
    x, y = a * (lcm // b), c * (lcm // d)
    if not re.fullmatch(r"Compare numerators: %d vs %d\. So \d+/\d+ is greater\." % (x, y), old[2].get("text", "")):
        raise Skip("the old last step does not compare %d and %d" % (x, y))
    if b == lcm and d == lcm:
        middle = "Both fractions already have the denominator %d, so nothing needs converting." % lcm
    elif b == lcm:
        middle = "%d/%d already has the denominator %d. Convert the other one: %d/%d = %d/%d." % (a, b, lcm, c, d, y, lcm)
    else:
        middle = "Convert %d/%d = %d/%d. The other fraction, %d/%d, already has the denominator %d." % (a, b, x, lcm, c, d, lcm)
    keep = lambda s: {"text": s["text"], "latex": s.get("latex", "")}  # noqa: E731
    steps = [keep(old[0]), {"text": middle, "latex": ""}, keep(old[2])]
    return {"steps": steps, "why": "The middle step 'converted' a fraction to itself (e.g. '2/8 = 2/8')."}


RULES = [
    ("fraction-of-hints", rule_fraction_of),
    ("fraction-add-hints-and-noop", rule_fraction_add),
    ("compare-fractions-noop", rule_compare_fractions),
]
