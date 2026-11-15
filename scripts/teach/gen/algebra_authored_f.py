"""Two past-paper wordings that come back year after year, each written once and filled in per question.

    build_up      "If 2x + 1 = 8, then 4x + 1 = ?"  (find 2x, double it; x itself is never needed)
    consecutive   "The sum of two consecutive odd numbers is 12. Which equation represents this, using m?"

These lessons are marked origin 'rule' because the words come from a shared template.
"""
from algebra_lib import B, T, W, answer, both, choose, given, lesson, mark, note, nth_at, strike

MINUS = "−"
LESSONS = {}


def build_up(v, k, plus1, b, c, mult, plus2, e, style):
    """`k v ± b = c`, find `(mult·k) v ± e`. `style` varies the words between the questions."""
    s1 = "+" if plus1 else MINUS
    un = MINUS if plus1 else "+"
    op1 = "plus" if plus1 else "minus"
    unw = "minus" if plus1 else "plus"
    s2 = "+" if plus2 else MINUS
    op2 = "plus" if plus2 else "minus"
    K = mult * k
    kv = c - b if plus1 else c + b
    big = mult * kv
    final = big + e if plus2 else big - e
    xval = ("%.2f" % (kv / k)).rstrip("0").rstrip(".")
    fact = "%d %s, %s %d, equals %d" % (k, v, op1, b, c)
    want = "%d %s, %s %d" % (K, v, op2, e)
    times = "double" if mult == 2 else "%d times" % mult

    beats = []
    beats.append(B([
        "We are told that %s. And we are asked for %s. Notice the question never asks for %s itself." % (fact, want, v),
        "Two lines here. The first is a fact: %s. The second is what we must find: %s." % (fact, want),
        "Here is what we know: %s. Here is what we want: %s. Let's see how to get from one to the other."
        % (fact, want),
    ][style % 3], given("l1", "%d%s %s %d = %d" % (k, v, s1, b, c), label=True),
        given("l2", "%d%s %s %d = ?" % (K, v, s2, e), label=True)))

    if style % 2 == 0:
        beats.append(B(
            "Start with the fact. What is in the way of the %d %s?" % (k, v),
            ask=choose(["the %d on the right" % c, "the %s %d" % (s1, b), "the %d in front of %s" % (k, v)], 1,
                       "Look at the left side. The %d %s has a %s %d hanging on to it. We clear that first."
                       % (k, v, op1, b))))
    else:
        good = ("take %d from both sides" if plus1 else "add %d to both sides") % b
        slip = ("add %d to both sides" if plus1 else "take %d from both sides") % b
        beats.append(B(
            "Start with the fact. How do we get the %d %s on its own?" % (k, v),
            ask=choose([slip, "divide both sides by %d" % k, good], 2,
                       "The %d %s has a %s %d with it. To undo %s %d we do the opposite, and we do it to both sides."
                       % (k, v, op1, b, op1, b))))

    beats.append(B(
        "To undo %s %d we %s %d, on both sides. %d %s %d is %d. So %d %s equals %d."
        % (op1, b, "take away" if plus1 else "add", b, c, unw, b, kv, k, v, kv),
        strike("l1", "%s %d" % (s1, b), "%s %d" % (un, b)), both("l1", "%s %d" % (un, b)),
        W("l3", "%d %s %d = %d" % (c, un, b, kv)), W("l4", "%d%s = %d" % (k, v, kv), label=True)))

    if mult == 2:
        choices = ["it is %d more" % k, "it is double", "it is half"]
    else:
        choices = ["it is %d more" % (K - k), "it is %d times as much" % mult, "it is double"]
    beats.append(B(
        "We could divide by %d now to find %s. But look at what we need: %d %s. How is %d %s related to %d %s?"
        % (k, v, K, v, K, v, k, v),
        ask=choose(choices, 1,
                   "%d is %d times %d. So %d %s is %d lots of %d %s. We do not even need to find %s."
                   % (K, mult, k, K, v, mult, k, v, v))))

    beats.append(B(
        "So %d %s is %s %d, which is %d." % (K, v, times, kv, big),
        note("l2", "%d%s" % (K, v), "%d × %d%s" % (mult, k, v)),
        W("l5", "%d × %d = %d" % (mult, kv, big)), W("l6", "%d%s = %d" % (K, v, big), label=True)))

    last = "%d %s %d = %d" % (big, s2, e, final)
    beats.append(B(
        "Do not stop there! The question wants %s. %d %s %d is %d." % (want, big, op2, e, final),
        answer("l7", last), mark("l7", T(str(final), nth_at(last, str(final), last.index("= ") + 2)))))

    beats.append(B(
        "We can check by finding %s after all. %d %s is %d, so %s is %d divided by %d, which is %s. "
        "And %d times %s, %s %d, gives %d again."
        % (v, k, v, kv, v, kv, k, xval, K, xval, op2, e, final),
        W("l8", "%d ÷ %d = %s" % (kv, k, xval)), W("l9", "%d × %s %s %d = %d" % (K, xval, s2, e, final))))

    beats.append(B([
        "So before you solve for the letter, look at what is asked. "
        "Sometimes you can build it straight from what you already know.",
        "The plan: find %d %s first, scale it up to %d %s, then finish with the %s %d. No need for %s on its own."
        % (k, v, K, v, op2, e, v),
    ][style % 2]))
    return lesson(beats, None, None, "rule")


LESSONS["EXT_G5_WS_B6_015"] = build_up("m", 2, True, 1, 8, 2, True, 5, 0)      # 2m + 1 = 8  →  4m + 5 = 19
LESSONS["EXT_G5_FP_2017_020"] = build_up("x", 2, True, 1, 8, 2, True, 1, 1)    # 2x + 1 = 8  →  4x + 1 = 15
LESSONS["EXT_G5_FP_2021_013"] = build_up("x", 2, True, 1, 8, 2, True, 1, 2)    # the same question, two years on
LESSONS["EXT_G5_FP_2018_038"] = build_up("x", 2, False, 3, 10, 2, False, 5, 3)  # 2x − 3 = 10  →  4x − 5 = 21
LESSONS["EXT_G5_FP_2023_021"] = build_up("x", 4, False, 7, 12, 3, False, 14, 4)  # 4x − 7 = 12  →  12x − 14 = 43
LESSONS["EXT_G5_FP_2025_028"] = build_up("x", 4, True, 3, 22, 3, True, 3, 5)   # 4x + 3 = 22  →  12x + 3 = 60


def consecutive(v, total, first, traps, style):
    """Two consecutive odd numbers add to `total`; write the equation with the letter `v`."""
    second = first + 2
    beats = []
    beats.append(B([
        "This question does not want the two numbers. It wants the equation: the sentence, written in maths, using %s."
        % v,
        "Here we are not solving anything. We are translating a sentence into an equation, "
        "with %s standing for a number." % v,
        "The job here is to write the sentence as an equation. We do not have to solve it, only to build it, using %s."
        % v,
    ][style % 3], given("l1", "two consecutive odd numbers, sum = %d" % total, label=True)))

    beats.append(B(
        "Consecutive means next to each other. Here are some odd numbers in a row: 1, 3, 5, 7, 9. "
        "How far apart are neighbours?",
        W("l2", "1, 3, 5, 7, 9", label=True),
        ask=choose(["1", "2", "3"], 1,
                   "From 3 to 5 we jump over the 4. So odd numbers that are neighbours are always 2 apart.")))

    beats.append(B(
        "So if the first odd number is %s, the next one is %s plus 2." % (v, v),
        W("l3", "first = %s" % v, label=True), W("l4", "next = %s + 2" % v, label=True)))

    beats.append(B(
        "The question says the sum of the two numbers is %d. What does the word sum tell us to do?" % total,
        ask=choose(["multiply them", "add them", "double the first one"], 1,
                   "Sum is the answer to an addition. So we add the first number and the next number.")))

    eq = "%s + (%s + 2) = %d" % (v, v, total)
    beats.append(B(
        "So we add them, and that must equal %d. %s, plus %s plus 2, equals %d." % (total, v, v, total),
        answer("l5", eq, label=True), mark("l5", eq, "box")))

    beats.append(B(traps))

    beats.append(B(
        "Does our equation make sense? %d and %d are both odd, and they are neighbours. "
        "And %d plus %d is %d. It fits." % (first, second, first, second, total),
        W("l6", "%d + %d = %d" % (first, second, total))))

    beats.append(B([
        "To turn words into an equation: name the first number, write the others from it, "
        "then follow the key word. Sum means add.",
        "So the plan: give the first number a letter, build the second from it, and let the word sum tell you to add.",
    ][style % 2]))
    return lesson(beats, None, None, "rule")


LESSONS["EXT_G5_FP_2018_004"] = consecutive(
    "m", 12, 5,
    "Look at the other choices. m times m plus 2 would be the product, not the sum. "
    "m plus 2 equals 12 uses only the second number. And 2 m would mean both numbers are the same.", 0)
LESSONS["EXT_G5_FP_2019_007"] = consecutive(
    "m", 16, 7,
    "The other choices each miss something. m plus 2 equals 16 forgets the first number. "
    "2 m treats the two numbers as equal. And m times m plus 2 multiplies, when sum means add.", 1)
LESSONS["EXT_G5_FP_2022_035"] = consecutive(
    "W", 192, 95,
    "Why not the others? W plus 2 equals 192 leaves out the first number. 2 W would mean two equal numbers. "
    "And W squared multiplies, when the word sum tells us to add.", 2)
