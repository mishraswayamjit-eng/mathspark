"""Rule-written lessons: "Which of the following numbers is divisible by d?" and "Solve: ax ± b = c".

The divisibility rules are shown on the digits: the last digits underlined, or the digit
sum written as a true sum, with what is left over noted beside it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factors_lib import (  # noqa: E402
    ANS, B, BOTH, CHOOSE, CIRC, DIVIDE, GIVEN, GIVENM, LB, LESSON, NOTE, STRIKE, UL, W,
    nth_at, pick, say_plus, shuffled,
)

OPENERS = ["First,", "Next,", "Now", "Last one:"]


def digits(n):
    return [int(c) for c in str(n)]


def sum_line(n):
    return "%s = %d" % (" + ".join(str(d) for d in digits(n)), sum(digits(n)))


def split_text(v, d):
    """'9 × 2' or '9 × 1 + 4': v written in terms of d."""
    q, r = divmod(v, d)
    if q == 1 and r:
        return "%d + %d" % (d, r)
    return "%d × %d" % (d, q) if r == 0 else "%d × %d + %d" % (d, q, r)


def split_say(v, d):
    q, r = divmod(v, d)
    if q == 0:
        return "%d is smaller than %d" % (v, d)
    if q == 1 and r:
        return "%d is %d, plus %d left over" % (v, d, r)
    if r == 0:
        return "%d is %d times %d" % (v, d, q)
    return "%d is %d times %d, plus %d left over" % (v, d, q, r)


def end_mark(line, n, k):
    """Underline the last k digits of n."""
    s = str(n)
    tail = s[-k:]
    return UL(line, tail, nth_at(s, tail, len(s) - k))


def last_note(line, text):
    """A note under the number at the end of a sum line."""
    value = text.split("= ")[-1]
    return nth_at(text, value, len(text) - len(value))


def yes_no(yes, if_not):
    return CHOOSE([yes, "No: there is a remainder"], 0, if_not)


def option_beats(qid, d, n, i, is_key):
    """The beats that test one choice. Lines are o<i> (the number), s<i> (digit sum), t<i> (tail)."""
    o, s, t = "o%d" % i, "s%d" % i, "t%d" % i
    first = OPENERS[i]
    odd = n % 2 == 1
    last = n % 10
    beats = []

    def digit_sum_test(m, lead, pre_ops):
        """Test n for m (3 or 9) by its digit sum. Returns beats."""
        total = sum(digits(n))
        line = sum_line(n)
        at = last_note(s, line)
        if total % m:
            return [B("%s %s makes %d. %s, so %d is out." % (lead, say_plus(digits(n)), total, split_say(total, m)[0].upper() + split_say(total, m)[1:], n),
                      *(pre_ops + [W(s, line), NOTE(s, str(total), split_text(total, m), "below", at), STRIKE(o, str(n), "out")]))]
        return [
            B("%s %s makes %d. Is %d in the %d times table?" % (lead, say_plus(digits(n)), total, total, m),
              *(pre_ops + [W(s, line)]),
              ask=yes_no("Yes: %d = %s" % (total, split_text(total, m)),
                         "%s, so yes, it is in the %d times table." % (split_say(total, m)[0].upper() + split_say(total, m)[1:], m))),
            B("So %d passes. Ring it!" % n if d in (3, 9) else "So %d passes both tests. Ring it!" % n,
              NOTE(s, str(total), split_text(total, m), "below", at), CIRC(o, str(n))),
        ]

    def tail_test(m, k, lead, then_pass):
        """Test n for m (4 or 8) by its last k digits. Returns (beats, passed)."""
        tail = n % (10 ** k)
        words = "two" if k == 2 else "three"
        line = "%d = %s" % (tail, split_text(tail, m))
        if tail % m:
            return [B("%s Its last %s digits make %d. %s, so %d is out." % (lead, words, tail, split_say(tail, m)[0].upper() + split_say(tail, m)[1:], n),
                      W(o, str(n)), end_mark(o, n, k), W(t, line), STRIKE(o, str(n), "out"))], False
        if then_pass:
            return [B("%s Its last %s digits make %d, and %s. So it passes the test for %d." % (lead, words, tail, split_say(tail, m), m),
                      W(o, str(n)), end_mark(o, n, k), W(t, line))], True
        return [
            B("%s Its last %s digits make %d. Is %d in the %d times table?" % (lead, words, tail, tail, m),
              W(o, str(n)), end_mark(o, n, k),
              ask=yes_no("Yes: %s" % line,
                         "%s, so yes, it is in the %d times table." % (split_say(tail, m)[0].upper() + split_say(tail, m)[1:], m))),
            B("So %d passes. Ring it!" % n, W(t, line), CIRC(o, str(n))),
        ], True

    def odd_beat(why):
        return [B("%s %d. It ends in %d, so it is odd. %s" % (first, n, last, why),
                  W(o, str(n)), end_mark(o, n, 1), STRIKE(o, str(n), "odd"))]

    if d in (3, 9):
        return digit_sum_test(d, "%s %d." % (first, n), [W(o, str(n))])
    if d in (4, 8):
        if odd:
            return odd_beat("An odd number cannot even be halved, so %d has no chance." % d)
        return tail_test(d, 2 if d == 4 else 3, "%s %d." % (first, n), False)[0]
    if d == 6:
        if odd:
            return odd_beat("2 will not go into it, so 6 cannot either.")
        return digit_sum_test(3, "%s %d. It ends in %d, so it is even. Now the test for 3:" % (first, n, last),
                              [W(o, str(n)), end_mark(o, n, 1)])
    if d == 12:
        if odd:
            return odd_beat("4 will not go into an odd number, so 12 cannot either.")
        beats, passed = tail_test(4, 2, "%s %d." % (first, n), True)
        if passed:
            beats += digit_sum_test(3, "Now the test for 3.", [])
        return beats
    if d == 11:
        ds = digits(n)
        assert len(ds) == 4
        t1, t2 = ds[0] + ds[2], ds[1] + ds[3]
        sn = str(n)
        marks = [UL(o, str(ds[0]), nth_at(sn, str(ds[0]), 0)), UL(o, str(ds[2]), nth_at(sn, str(ds[2]), 2))]
        writes = [W(o, sn)] + marks + [W(s, "%d + %d = %d" % (ds[0], ds[2], t1)), W(t, "%d + %d = %d" % (ds[1], ds[3], t2))]
        gap = abs(t1 - t2)
        ok = gap in (0, 11)
        totals = "The 1st and 3rd digits, %d and %d, make %d. The 2nd and 4th, %d and %d, make %d%s." % (
            ds[0], ds[2], t1, ds[1], ds[3], t2, " as well" if t1 == t2 else "")
        verdict_ops = [CIRC(o, sn)] if ok else [STRIKE(o, sn, "out")]
        if ok:
            verdict = "The two totals match, so %d passes. Ring it!" % n if gap == 0 else "The two totals are exactly 11 apart, so %d passes. Ring it!" % n
        else:
            verdict = "%d and %d are not equal, and they are not 11 apart. So %d is out." % (t1, t2, n)
        if i == 0:
            if ok:
                ask = CHOOSE(["Yes, the totals fit the rule", "No, it is out"], 0,
                             "The totals are %d and %d. The rule wants them equal, or exactly 11 apart, and these fit." % (t1, t2))
            else:
                ask = CHOOSE(["No, the totals do not fit the rule", "Yes, it passes"], 0,
                             "The rule wants the totals equal, or exactly 11 apart. %d and %d are neither." % (t1, t2))
            return [B("%s %d. %s Does %d pass?" % (first, n, totals, n), *writes, ask=ask),
                    B(verdict, *verdict_ops)]
        short = "The 1st and 3rd digits make %d, and the 2nd and 4th make %d." % (t1, t2)
        if ok:
            end = "They match, so %d passes. Ring it!" % n if gap == 0 else "They are exactly 11 apart, so %d passes. Ring it!" % n
        else:
            end = "Not equal, and not 11 apart, so %d is out." % n
        return [B("%s %d. %s %s" % (first, n, short, end), *(writes + verdict_ops))]
    raise ValueError("no rule for %d" % d)


def divisible_lesson(qid, d, options, key):
    """options: the four numbers; key: index of the right one."""
    answer = options[key]
    beats = [B(
        "Which of these numbers is divisible by %d? We could do four long divisions. But there is a quicker way: a divisibility rule." % d,
        GIVEN("q", "Which number is divisible by %d?" % d))]

    if d in (3, 9):
        choices, at = shuffled(qid, "rule", "The sum of all the digits", ["Just the last digit", "The last two digits"])
        beats.append(B("For %d there is a lovely trick. What do you think we look at?" % d,
                       ask=CHOOSE(choices, at,
                                  "For %d, the last digits do not tell us enough. The trick is to add up all the digits." % d)))
        beats.append(B("Here is the rule. Add up the digits. If that sum is in the %d times table, then the whole number is too." % d,
                       LB("r", "Rule for %d: the digit sum must be a multiple of %d" % (d, d))))
    elif d in (4, 8):
        base, part, k, words = (100, 25, 2, "two") if d == 4 else (1000, 125, 3, "three")
        beats.append(B(
            "Here is a secret about %d. %d is %d times %d, so every %s is already in the %d times table." % (
                d, base, d, part, "hundred" if d == 4 else "thousand", d),
            W("r", "%d = %d × %d" % (base, d, part))))
        choices, at = shuffled(qid, "rule", "Only the last %s digits" % words, ["Only the last digit", "All the digits added up"])
        beats.append(B("So which part of a number do we still need to test?",
                       ask=CHOOSE(choices, at,
                                  "Everything from the %s place up is made of %ds, and %d goes into every %d. So only the last %s digits are left to test." % (
                                      "hundreds" if d == 4 else "thousands", base, d, base, words))))
        beats.append(B("So that is our rule. Underline the last %s digits, and test only those." % words,
                       LB("r2", "Rule for %d: test the last %s digits" % (d, words))))
    elif d == 6:
        choices, at = shuffled(qid, "rule", "It is even AND 3 divides it", ["It is even OR 3 divides it", "It ends in 6"])
        beats.append(B("6 is 2 times 3. So what must be true of a number that 6 divides?",
                       W("r", "6 = 2 × 3"),
                       ask=CHOOSE(choices, at,
                                  "If 6 goes into a number, then 2 and 3 both go into it. One of them alone is not enough: the number must pass both tests.")))
        beats.append(B("So we run two tests. The number must be even, and its digits must add up to a multiple of 3.",
                       LB("r2", "Rule for 6: even, and digit sum a multiple of 3")))
    elif d == 12:
        choices, at = shuffled(qid, "rule", "4 divides it AND 3 divides it", ["2 divides it AND 6 divides it", "It ends in 12"])
        beats.append(B("12 is 4 times 3. So what must be true of a number that 12 divides?",
                       W("r", "12 = 4 × 3"),
                       ask=CHOOSE(choices, at,
                                  "2 and 6 overlap, because 6 already has a 2 inside it. But 4 and 3 share nothing, so passing both of those tests means 12 divides the number.")))
        beats.append(B("Two tests, then. For 4, the last two digits must be in the 4 times table. For 3, the digits must add up to a multiple of 3.",
                       LB("r2", "Rule for 12: pass the 4 test and the 3 test")))
    elif d == 11:
        beats.append(B("The rule for 11 is a neat one. Add the 1st and 3rd digits. Then add the 2nd and 4th digits.",
                       LB("r", "Add the 1st and 3rd digits. Add the 2nd and 4th.")))
        beats.append(B("If the two totals are equal, or exactly 11 apart, then 11 divides the number.",
                       LB("r2", "Totals equal, or 11 apart: divisible by 11")))

    for i, n in enumerate(options):
        tested = option_beats(qid, d, n, i, i == key)
        if i == key + 1:
            # The right one has been found: say why we carry on.
            tested[0]["say"] = "A careful mathematician tests the rest too. " + tested[0]["say"]
        beats += tested

    beats.append(B(
        "Only %d passed, so that is our answer. And the division agrees: %d divided by %d is %d, with nothing left over." % (answer, answer, d, answer // d),
        W("c", "%d ÷ %d = %d" % (answer, d, answer // d)),
        ANS("ans", "%d is divisible by %d" % (answer, d)), CIRC("ans", str(answer))))
    summary = {
        3: "So for 3, never divide first. Add the digits, and see whether the sum is in the 3 times table.",
        9: "So for 9, never divide first. Add the digits, and see whether the sum is in the 9 times table.",
        4: "So for 4, look only at the last two digits. And if a number is odd, you can cross it out straight away.",
        8: "So for 8, look only at the last three digits. And if a number is odd, you can cross it out straight away.",
        6: "So for 6, run two quick tests: is it even, and do the digits add up to a multiple of 3? It must pass both.",
        12: "So for 12, run two tests: the last two digits for 4, and the digit sum for 3. It must pass both.",
        11: "So for 11, add every other digit to make two totals. Equal totals, or totals 11 apart, mean 11 divides the number.",
    }[d]
    beats.append(B(summary))
    return LESSON(*beats, origin="rule")


# ── Solve: ax ± b = c ────────────────────────────────────────────────────────

def equation_lesson(qid, a, sign, b, c):
    """sign is '+' or '−'."""
    plus = sign == "+"
    x = (c - b) // a if plus else (c + b) // a
    mid = c - b if plus else c + b
    undo_sign = "−" if plus else "+"
    word, undo_word = ("plus", "subtract") if plus else ("minus", "add")
    eq = "%dx %s %d = %d" % (a, sign, b, c)
    beats = [B(
        pick(qid, "intro", [
            "Here is our equation. %d x, %s %d, equals %d. Somewhere behind that x a number is hiding, and we are going to find it." % (a, word, b, c),
            "Look at this equation. %d x, %s %d, equals %d. The x stands for a secret number. Let's uncover it." % (a, word, b, c),
        ]),
        GIVENM("l1", eq))]
    choices, at = shuffled(qid, "way", "the %s %d" % (sign, b), ["the %d" % c, "the %d in %dx" % (a, a)])
    beats.append(B(
        "Think of the equals sign as a balance. Whatever we do to one side, we do to the other. So, what do we clear away first to get the %d x alone?" % a,
        ask=CHOOSE(choices, at,
                   "Look at the left side once more. The %d x has a %s %d hanging on to it. That is the first thing to clear away." % (a, word, b))))
    beats.append(B(
        "To undo %s %d, we %s %d. And to keep the balance level, we do it to both sides." % (word, b, undo_word, b),
        STRIKE("l1", "%s %d" % (sign, b), "%s %d" % (undo_sign, b)), BOTH("l1", "%s %d" % (undo_sign, b))))
    beats.append(B(
        "On the left, only %d x is left. On the right, %d %s %d makes %d." % (a, c, "minus" if plus else "plus", b, mid),
        W("l2", "%dx = %d %s %d" % (a, c, undo_sign, b)), W("l3", "%dx = %d" % (a, mid))))
    choices, at = shuffled(qid, "undo", "divide by %d" % a, ["subtract %d" % a, "multiply by %d" % a])
    beats.append(B(
        pick(qid, "near", [
            "Nearly there. %d x means %d times x. What undoes times %d?" % (a, a, a),
            "One more move. %d x is %d times x. How do we undo times %d?" % (a, a, a),
        ]),
        ask=CHOOSE(choices, at,
                   "Times and divide are partners. Whatever times does, divide undoes. So to undo times %d, we divide by %d." % (a, a))))
    beats.append(B("So we divide both sides by %d." % a, DIVIDE("l3", a)))
    beats.append(B(
        "%d divided by %d is %d. So x equals %d. There is our hidden number!" % (mid, a, x, x),
        W("l4", "x = %d" % x, "answer"), CIRC("l4", "x = %d" % x)))
    beats.append(B(
        "Good mathematicians always check. Put %d back in place of x. %d times %d is %d, and %d %s %d is %d. It works." % (
            x, a, x, a * x, a * x, word, b, c),
        W("l5", "%d × %d %s %d = %d" % (a, x, sign, b, c))))
    beats.append(B(pick(qid, "sum", [
        "So here is the plan for any equation like this. First clear away what is added or taken off. Then undo the times. Your turn next!",
        "Two moves, every time. Undo the plus or minus first, then divide to undo the times. And always do the same to both sides.",
    ])))
    return LESSON(*beats, origin="rule", check=("x", x))
