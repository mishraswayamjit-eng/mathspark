"""Algebra: a number times a bracket (two questions), and which pair fits the rule (two questions)."""
from imported_01_lib import ANS, ARC, B, GIVEN, M, N, TB, W, choose, lesson, placed

LESSONS = {}


# ── k × (x + y) ──────────────────────────────────────────────────────────────

def times_bracket(qid, k, tx, ty, v):
    """k(x + y) = kx + ky, shown with bags and tested with x = tx, y = ty."""
    bags = " + ".join(["(x + y)"] * k)
    total = k * (tx + ty)
    slip = k * tx + ty
    right = "%d x and %d y" % (k, k)
    choices, at = placed(qid, "bags", right, ["%d x and 1 y" % k, "1 x and %d y" % k])
    return lesson(
        B(["We multiply %d by the whole bracket, x plus y. What does that come to?" % k,
           "%d times the bracket x plus y. We want to write it without the bracket." % k][v],
          GIVEN("l1", "%d(x + y)" % k)),
        B("Think of the bracket as a bag holding one x and one y. %d times the bracket means %d of those bags." % (k, k),
          W("l2", bags, label=True)),
        B("Count what is inside all the bags. How many x, and how many y?",
          ask=choose(choices, at,
                     "Every bag has one x and one y inside. There are %d bags, so there are %d of each: %d x and %d y." % (k, k, k, k))),
        B("So the %d multiplies both things in the bracket: %d times x, and %d times y." % (k, k, k),
          ARC("l1", str(k), ["x", "y"]), W("l3", "%d × x + %d × y" % (k, k), label=True)),
        B("%d times the bracket is %d x plus %d y." % (k, k, k),
          ANS("ans", "%d(x + y) = %dx + %dy" % (k, k, k), True), M("ans", "%dx + %dy" % (k, k), "circle")),
        B("Careful: the classic slip is to multiply only the first one and write %d x plus y. The y is in the bracket too, so it gets its %d as well." % (k, k)),
        B("Let's test it with numbers. Say x is %d and y is %d. The bracket is %d, and %d times %d is %d." % (tx, ty, tx + ty, k, tx + ty, total),
          W("t1", "%d × (%d + %d) = %d" % (k, tx, ty, total))),
        B("Now our answer. %d times %d is %d, and %d times %d is %d. %d plus %d is %d. A match." % (k, tx, k * tx, k, ty, k * ty, k * tx, k * ty, total),
          W("t2", "%d × %d + %d × %d = %d + %d" % (k, tx, k, ty, k * tx, k * ty)),
          W("t3", "%d + %d = %d" % (k * tx, k * ty, total))),
        B("And the slip, %d x plus y, would give %d plus %d, which is only %d. No match." % (k, k * tx, ty, slip),
          W("t4", "%d × %d + %d = %d" % (k, tx, ty, slip)), N("t4", str(slip), "not %d" % total)),
        B(["A number outside a bracket multiplies everything inside it. Draw the arcs, and nobody gets left out.",
           "Outside the bracket means times everything inside. One arc to each term, every time."][v]),
    )


LESSONS[TB + "ch09_q010"] = times_bracket(TB + "ch09_q010", 4, 2, 5, 0)
LESSONS[TB + "ch09_q028"] = times_bracket(TB + "ch09_q028", 3, 4, 1, 1)


# ── 2x − 2y = 2: test each pair, then see the shortcut ───────────────────────

def pair_line(id, letter, x, y):
    d = 2 * x - 2 * y
    shown = ("−%d" % -d) if d < 0 else str(d)
    text = "2 × %d − 2 × %d = %d − %d = %s" % (x, y, 2 * x, 2 * y, shown)
    return [W(id, text), N(id, text, "%s: x = %d, y = %d" % (letter, x, y), "above")]


LESSONS[TB + "ch09_q008"] = lesson(
    B("Here is a rule that x and y must obey: 2 x, minus 2 y, equals 2. Four pairs are offered, and only one of them obeys the rule.",
      GIVEN("l1", "2x − 2y = 2")),
    B("How can we find out which pair works?",
      ask=choose(["Pick the biggest numbers", "Try each pair in the rule", "Add x and y"], 1,
                 "A rule is tested by trying it. Put each pair in place of x and y, and see whether the left side really comes to 2.")),
    B("Pair A: x is 1 and y is 1. 2 times 1 is 2, and 2 times 1 is 2 again. 2 minus 2 is 0, not 2.",
      pair_line("a", "A", 1, 1)),
    B("Pair B: x is 2 and y is 1. 2 times 2 is 4, and 2 times 1 is 2. 4 minus 2 is 2. That obeys the rule.",
      pair_line("b", "B", 2, 1), M("b", "= 2", "circle")),
    B("Check the last two as well. Pair C: x is 1 and y is 2. That gives 2 minus 4, which drops below zero. So it cannot be 2.",
      pair_line("c", "C", 1, 2)),
    B("Pair D: x is 4 and y is 2. 2 times 4 is 8, and 2 times 2 is 4. 8 minus 4 is 4. Too big.",
      pair_line("d", "D", 4, 2)),
    B("So only pair B fits: x is 2 and y is 1.", ANS("ans", "x = 2, y = 1", True), M("ans", "x = 2, y = 1", "circle")),
    B("Now a shortcut. 2 x minus 2 y is double the gap between x and y. If double the gap is 2, what is the gap?",
      ask=choose(["2", "1", "4"], 1, "Double the gap is 2, so the gap itself is half of 2. That is 1.")),
    B("So x must be exactly 1 more than y. And 2 is 1 more than 1.", W("gap", "2 − 1 = 1")),
    B("Careful with pair C. Its numbers are 1 apart too, but there y is the bigger one. In a take-away, the order matters."),
    B("To test a rule, put the numbers in and see. And when both parts are doubled, look at the gap between the letters."),
)

# ── 2x − 2y = 6: the shortcut first, then test ───────────────────────────────
LESSONS[TB + "ch09_q025"] = lesson(
    B("x and y must obey this rule: 2 x, minus 2 y, equals 6. Four pairs are offered. We could test all four, but let's look for something clever first.",
      GIVEN("l1", "2x − 2y = 6")),
    B("Both parts on the left are doubled: double x, take away double y. That is the same as doubling the gap between x and y.",
      W("l2", "2x − 2y = 2 × (x − y)", label=True)),
    B("So double the gap is 6. What is the gap between x and y?",
      ask=choose(["6", "12", "3"], 2, "Double the gap is 6, so the gap is half of 6. Half of 6 is 3.")),
    B("So x must be exactly 3 more than y.", W("l3", "x − y = 3", label=True), M("l3", "x − y = 3", "box")),
    B("Now run down the pairs and look at the gaps. A: 6 minus 4 is 2. B: 7 minus 2 is 5. C: 8 minus 6 is 2. D: 6 minus 3 is 3.",
      W("ga", "6 − 4 = 2"), W("gb", "7 − 2 = 5"), W("gc", "8 − 6 = 2"), W("gd", "6 − 3 = 3")),
    B("Which pair has the gap we need?",
      ask=choose(["x = 6, y = 4", "x = 7, y = 2", "x = 8, y = 6", "x = 6, y = 3"], 3,
                 "We need a gap of exactly 3, with x the bigger one. Only 6 and 3 are 3 apart.")),
    B("Now test that pair properly in the rule. 2 times 6 is 12, and 2 times 3 is 6. 12 minus 6 is 6. It works.",
      pair_line("d", "D", 6, 3), M("gd", "6 − 3 = 3", "circle")),
    B("So x is 6 and y is 3.", ANS("ans", "x = 6, y = 3", True), M("ans", "x = 6, y = 3", "circle")),
    B("Careful with pair A. It comes to 4, which is close to 6 but not equal. With an equals sign, close does not count.",
      pair_line("a", "A", 6, 4)),
    B("When both parts of a rule are doubled, halve everything in your head and look at the gap. Then test your pair in the real rule."),
)
